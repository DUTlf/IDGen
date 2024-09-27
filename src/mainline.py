import pandas as pd
import config
from model_api import *
from discrimination import DiscriminationPredictor
from difficulty import DifficultyPredictor
from prompt import *
import re

class QuestionProcessor:
    def __init__(self):
        self.predictor_discrimination = DiscriminationPredictor(config.discrimination_model_path, config.discrimination_label_path)
        self.predictor_difficulty = DifficultyPredictor(config.difficulty_model_path, config.difficulty_cate_path)
        self.hunyuan_api = HunyuanAPI()
        self.hunyuan_p_api = HunyuanAPI_P()

    def get_difficulty(self, instruction, full_category):
        difficulty_level = self.predictor_difficulty.predict(instruction, full_category)
        return difficulty_level

    def get_discrimination(self, instruction, full_category):
        data = [{"分类": full_category, "问题": instruction}]
        prediction = self.predictor_discrimination.predict(data)
        discrimination_level = prediction[0]["predict_labels"]
        return discrimination_level, prediction

    def get_improvement(self, instruction, difficulty_level, discrimination_level):
        prompt_improvement = get_prompt_improvement(instruction, difficulty_level, discrimination_level)
        improvement = self.hunyuan_api.get_hunyuan_answer(prompt_improvement)
        return improvement

    def get_improvement_en(self, instruction, difficulty_level, discrimination_level):
        prompt_improvement = get_prompt_improvement_en(instruction, difficulty_level, discrimination_level)
        improvement = self.hunyuan_api.get_hunyuan_answer(prompt_improvement)
        return improvement

    def rewrite_seed(self, instruction, improvement):
        prompt_rewrite = get_prompt_rewrite(instruction, improvement)
        new_instruction = self.hunyuan_api.get_hunyuan_answer(prompt_rewrite)
        return new_instruction

    def rewrite_seed_en(self, instruction, improvement):
        prompt_rewrite = get_prompt_rewrite_en(instruction, improvement)
        new_instruction = self.hunyuan_api.get_hunyuan_answer(prompt_rewrite)
        return new_instruction

    def get_gradient_selection_math(self, category_level1, keyword):
        gradient_options = {
            "数学": {
                "改变变量": "不改变问题背景，只改变问题的变量名或变量的值",
                "提供编程代码": "解决问题的同时，提供一个具体的算法或编程代码",
                "引入动态过程": "将静态问题转化为动态问题，考虑随时间变化的因素，如增长率、衰减过程等",
                "引入额外变量": "在问题中增加一个或多个相关变量",
                "引入优化问题": "将问题转化为寻找最优解的问题，如最大化或最小化某个量",
                "结合不同数学领域": "将问题与另一个数学领域结合，如将代数问题与几何问题结合，或者在统计问题中加入概率计算",
                "与非数学领域知识结合": "将问题与科学、工程、经济学等非数学领域的知识结合",
                "引入高等数学概念": "引入高等数学概念",
                "限制方法": "在解决问题时，必须使用特定的数学方法或理论",
                "限制不使用某种方法": "限制不使用某种数学方法解决问题",
                "逻辑陷阱": "设计问题时，故意设置一些看似正确但实际上是错误的推理路径",
                "增加逻辑步骤（Wizardlm）": "构造问题使其解决过程需要多个独立的逻辑判断和推理步骤，每一步都必须正确执行才能得到最终答案",
                "条件约束（Wizardlm）": "在问题中添加一个约束/要求"
            }
        }
        options = gradient_options.get(category_level1)
        if options is None:
            return "未知的一级分类"
        return options.get(keyword, "无效的关键词")

    def get_gradient_selection_math_en(self, category_level1, keyword):
        gradient_options = {
            "数学": {
                "改变变量": "Do not change the context of the problem, only change the variable name or the value of the variable",
                "提供编程代码": "Solve the problem while providing a specific algorithm or programming code",
                "引入动态过程": "Transform a static problem into a dynamic one, considering factors that change over time, such as growth rates, decay processes, etc.",
                "引入额外变量": "Add one or more related variables to the problem",
                "引入优化问题": "Transform the problem into finding the optimal solution, such as maximizing or minimizing a certain quantity",
                "结合不同数学领域": "Combine the problem with another field of mathematics, such as combining algebra problems with geometry problems, or adding probability calculations to statistical problems",
                "与非数学领域知识结合": "Combine the problem with knowledge from non-mathematical fields such as science, engineering, economics, etc.",
                "引入高等数学概念": "Introduce advanced mathematical concepts",
                "限制方法": "When solving the problem, a specific mathematical method or theory must be used",
                "限制不使用某种方法": "Restrict not using a certain mathematical method to solve the problem",
                "逻辑陷阱": "When designing the problem, deliberately set some reasoning paths that seem correct but are actually wrong",
                "增加逻辑步骤（Wizardlm）": "Construct the problem so that its solution process requires multiple independent logical judgments and reasoning steps, each of which must be correctly executed to get the final answer",
                "条件约束（Wizardlm）": "Add a constraint/requirement to the problem"
            }
        }
        options = gradient_options.get(category_level1)
        if options is None:
            return "未知的一级分类"
        return options.get(keyword, "无效的关键词")

    def rewrite_question_math(self, question_type, question, gradient_selection):
        prompt_rewrite = get_prompt_rewrite_math(question_type, question, gradient_selection)
        new_question = self.hunyuan_api.get_hunyuan_answer(prompt_rewrite)
        return new_question

    def rewrite_question_math_en(self, question_type, question, gradient_selection):
        prompt_rewrite = get_prompt_rewrite_math_en(question_type, question, gradient_selection, config.rewrite_id)
        new_question = self.hunyuan_api.get_hunyuan_answer(prompt_rewrite)
        if new_question.startswith("Question:"):
            new_question = new_question[len("Question:"):].strip()
        return new_question

    def access_math(self, question):
        prompt_access = get_prompt_access_math(question)
        access_question = self.hunyuan_api.get_hunyuan_answer(prompt_access)
        hunyuan_judge_pattern = re.compile(r'\n(问题\s*(合理|不合理))')
        hunyuan_correction_pattern = re.compile(r'问题修改为：\s*(.+?)(?=\n|$)')
        hunyuan_judge_match = hunyuan_judge_pattern.search(access_question)
        hunyuan_correction_match = hunyuan_correction_pattern.search(access_question)
        hunyuan_judge = hunyuan_judge_match.group(1).strip() if hunyuan_judge_match else ""
        hunyuan_correction = hunyuan_correction_match.group(1).strip() if hunyuan_correction_match else ""
        return access_question, hunyuan_judge, hunyuan_correction

    def access_math_en(self, question):
        prompt_access = get_prompt_access_math_en(question)
        access_question = self.hunyuan_api.get_hunyuan_answer(prompt_access)
        hunyuan_judge_pattern = re.compile(r'\n(The problem is\s*(reasonable|unreasonable))')
        hunyuan_correction_pattern = re.compile(r'The problem is modified as:\s*(.+?)(?=\n|$)')
        hunyuan_judge_match = hunyuan_judge_pattern.search(access_question)
        hunyuan_correction_match = hunyuan_correction_pattern.search(access_question)
        hunyuan_judge = hunyuan_judge_match.group(1).strip() if hunyuan_judge_match else ""
        hunyuan_correction = hunyuan_correction_match.group(1).strip() if hunyuan_correction_match else ""
        return access_question, hunyuan_judge, hunyuan_correction

    def access_math_pro(self, question):
        prompt_access = get_prompt_access_math(question)
        access_question = self.hunyuan_api.get_hunyuan_answer(prompt_access)
        hunyuan_p_judge_pattern = re.compile(r'\n(问题\s*(合理|不合理))')
        hunyuan_p_correction_pattern = re.compile(r'问题修改为：\s*(.+?)(?=\n|$)')
        hunyuan_p_judge_match = hunyuan_p_judge_pattern.search(access_question)
        hunyuan_p_correction_match = hunyuan_p_correction_pattern.search(access_question)
        hunyuan_p_judge = hunyuan_p_judge_match.group(1).strip() if hunyuan_p_judge_match else ""
        hunyuan_p_correction = hunyuan_p_correction_match.group(1).strip() if hunyuan_p_correction_match else ""
        return access_question, hunyuan_p_judge, hunyuan_p_correction

    def access_math_pro_en(self, question):
        prompt_access = get_prompt_access_math_en(question)
        access_question = self.hunyuan_p_api.get_hunyuan_p_answer(prompt_access)

        hunyuan_p_judge_pattern = re.compile(r'\n(The problem is\s*(reasonable|unreasonable))')
        hunyuan_p_correction_pattern = re.compile(r'The problem is modified as:\s*(.+?)(?=\n|$)')

        hunyuan_p_judge_match = hunyuan_p_judge_pattern.search(access_question)
        hunyuan_p_correction_match = hunyuan_p_correction_pattern.search(access_question)

        hunyuan_p_judge = hunyuan_p_judge_match.group(1).strip() if hunyuan_p_judge_match else ""
        hunyuan_p_correction = hunyuan_p_correction_match.group(1).strip() if hunyuan_p_correction_match else ""

        return access_question, hunyuan_p_judge, hunyuan_p_correction

    def review_and_rewrite_question_math(self, initial_question):
        iteration = 0
        current_question = initial_question

        hunyuan_access_initial_question, hunyuan_initial_judge, hunyuan_correction = self.access_math(current_question)
        hunyuan_p_access_initial_question, hunyuan_p_initial_judge, hunyuan_p_correction = self.access_math_pro(current_question)
        hunyuan_judge = hunyuan_initial_judge
        hunyuan_p_judge = hunyuan_p_initial_judge
        hunyuan_access_question = hunyuan_access_initial_question
        hunyuan_p_access_question = hunyuan_p_access_initial_question

        while iteration < config.max_iterations and (hunyuan_judge == "问题不合理" or (hunyuan_judge == "问题合理" and hunyuan_p_judge == "问题不合理")):
            print("Enter Iteration", iteration)
            if hunyuan_judge == "问题不合理" and hunyuan_p_judge == "问题不合理":
                current_question = hunyuan_p_correction
            elif hunyuan_judge == "问题不合理":
                current_question = hunyuan_correction
            elif hunyuan_p_judge == "问题不合理":
                current_question = hunyuan_p_correction
            iteration += 1
            hunyuan_access_question, hunyuan_judge, hunyuan_correction = self.access_math(current_question)
            hunyuan_p_access_question, hunyuan_p_judge, hunyuan_p_correction = self.access_math_pro(current_question)

        return current_question, hunyuan_access_question, hunyuan_p_access_question, hunyuan_access_initial_question, hunyuan_p_access_initial_question,hunyuan_initial_judge, hunyuan_p_initial_judge

    def review_and_rewrite_question_math_en(self, initial_question):
        # max_iterations = 2
        iteration = 0
        current_question = initial_question

        hunyuan_access_initial_question, hunyuan_initial_judge, hunyuan_correction = self.access_math_en(current_question)
        hunyuan_p_access_initial_question, hunyuan_p_initial_judge, hunyuan_p_correction = self.access_math_pro_en(current_question)
        hunyuan_judge = hunyuan_initial_judge
        hunyuan_p_judge = hunyuan_p_initial_judge
        hunyuan_access_question = hunyuan_access_initial_question
        hunyuan_p_access_question = hunyuan_p_access_initial_question

        while iteration < config.max_iterations and (hunyuan_judge == "The problem is ureasonable" or (hunyuan_judge == "The problem is unreasonable" and hunyuan_p_judge == "The problem is unreasonable")):
            print("Enter Iteration", iteration)
            if hunyuan_judge == "The problem is unreasonable" and hunyuan_p_judge == "The problem is unreasonable":
                current_question = hunyuan_p_correction
            elif hunyuan_judge == "The problem is unreasonable":
                current_question = hunyuan_correction
            elif hunyuan_p_judge == "The problem is unreasonable":
                current_question = hunyuan_p_correction
            iteration += 1

            hunyuan_access_question, hunyuan_judge, hunyuan_correction = self.access_math_en(current_question)
            hunyuan_p_access_question, hunyuan_p_judge, hunyuan_p_correction = self.access_math_pro_en(current_question)

        return current_question, hunyuan_access_question, hunyuan_p_access_question, hunyuan_access_initial_question, hunyuan_p_access_initial_question,hunyuan_initial_judge, hunyuan_p_initial_judge

    def review_question(self, question):
        hunyuan_access_question, hunyuan_judge, hunyuan_correction = self.access_math_en(question)
        hunyuan_p_access_question, hunyuan_p_judge, hunyuan_p_correction = self.access_math_pro_en(question)
        return hunyuan_access_question, hunyuan_p_access_question, hunyuan_judge, hunyuan_p_judge, hunyuan_correction, hunyuan_p_correction

    def review_question_en(self, question):
        hunyuan_access_question, hunyuan_judge, hunyuan_correction = self.access_math(question)
        hunyuan_p_access_question, hunyuan_p_judge, hunyuan_p_correction = self.access_math_pro(question)
        return hunyuan_access_question, hunyuan_p_access_question, hunyuan_judge, hunyuan_p_judge, hunyuan_correction, hunyuan_p_correction

    def access_instruction(self, instruction):
        print("Inside access_instruction function")

        prompt_access = get_prompt_access(instruction)

        access = self.hunyuan_api.get_hunyuan_answer(prompt_access)

        return access

    def access_instruction_en(self, instruction):
        print("Inside access_instruction function")

        prompt_access = get_prompt_access_en(instruction)

        access = self.hunyuan_p_api.get_hunyuan_p_answer(prompt_access)

        return access

    def information_capturer(self, question):
        text = f'''Please describe the background and relevant details of this problem in detail. 
        Think deeply about the problem from multiple dimensions. 
        Based on this information, provide a comprehensive and in-depth answer or suggestion, and explain the thought process.'''
        prompt = question + "\n" + text
        answer = self.hunyuan_api.get_hunyuan_answer(prompt)
        return answer

    def rewrite_question_response_gradient(self, response, category_level1, category_level2):
        role = [category_level1, category_level2]
        prompt_rewrite_response_gradient = get_prompt_rewrite_response_gradient(role, response)
        output = self.hunyuan_api.get_hunyuan_answer(prompt_rewrite_response_gradient)

        thought_process_pattern = r'思考过程：(.*?)'
        new_question_pattern = r'\n设计的问题：(.*)'

        thought_process_match = re.search(thought_process_pattern, output, re.DOTALL)
        new_question_match = re.search(new_question_pattern, output, re.DOTALL)

        thought_process_line = thought_process_match.group(1).strip() if thought_process_match else ""
        new_question_line = new_question_match.group(1).strip() if new_question_match else ""

        return thought_process_line, new_question_line

def instruction_gradient(data_path, record_save_file):
    df = pd.read_excel(data_path)
    # df = df.head(50)
    result_df = pd.DataFrame(columns=["一级分类", "二级分类", "三级分类"])
    processor = QuestionProcessor()

    for index, row in df.iterrows():
        if row["一级分类"]  in ["NLP基础", "文本生成", "专业领域", "推理"]:
            categrary_level1 = row["一级分类"]
            categrary_level2 = row["二级分类"]
            categrary_level3 = row["三级分类"]
            full_categraty = categrary_level1 + "-" + categrary_level2
            if not pd.isna(categrary_level3):
                full_categraty += "-" + categrary_level3
            question = row["问题"]
            current_data =question
            difficulty_level_seed = processor.get_difficulty(current_data, full_categraty)
            discrimination_level_seed, _ = processor.get_discrimination(current_data, full_categraty)
            improvement = None
            new_instruction = None
            difficulty_level = difficulty_level_seed
            discrimination_level = discrimination_level_seed

            for _ in range(config.depth_instruction_iteration_times):
                improvement = processor.get_improvement(current_data, difficulty_level, discrimination_level)
                new_instruction = processor.rewrite_seed(current_data, improvement)
                current_data = new_instruction
                difficulty_level = processor.get_difficulty(current_data, full_categraty)
                discrimination_level, _ = processor.get_discrimination(current_data, full_categraty)

            score_seed_instrcution = processor.access_instruction(question)
            score_new_instrcution = processor.access_instruction(new_instruction)

            result_df = result_df._append({"一级分类": categrary_level1,
                                          "二级分类": categrary_level2,
                                          "三级分类": categrary_level3,
                                           "问题": question,
                                           "difficulty_level_seed": difficulty_level_seed,
                                           "discrimination_level_seed": discrimination_level_seed,
                                           "score_seed_instrcution": score_seed_instrcution,
                                           "improvement": improvement,
                                           "new_instruction": new_instruction,
                                           "difficulty_level": difficulty_level,
                                           "discrimination_level": discrimination_level,
                                           "score_new_instrcution": score_new_instrcution
                                           }, ignore_index=True)

            result_df.to_excel(record_save_file, index=False)

        elif row["一级分类"]  in ["数学"]:
            categrary_level1 = row["一级分类"]
            categrary_level2 = row["二级分类"]
            categrary_level3 = row["三级分类"]
            full_categraty = categrary_level1 + "-" + categrary_level2 + "-" + categrary_level3
            # question = str(row["instruction_cn"]) + str(row["input_cn"])
            question = row["instruction_cn"]
            if not pd.isna(row["input_cn"]):
                question += row["input_cn"]

            gradient_keys = [
                "改变变量", "提供编程代码", "引入动态过程", "引入额外变量",
                "结合不同数学领域", "与非数学领域知识结合", "引入高等数学概念", "限制方法",
                "限制不使用某种方法", "增加逻辑步骤（Wizardlm）", "条件约束（Wizardlm）"
            ]

            # 随机选择一个梯度方法
            gradient_selection = processor.get_gradient_selection_math(categrary_level1, random.choice(gradient_keys))
            print(gradient_selection)

            new_question = processor.rewrite_question_math(categrary_level1, question, gradient_selection)

            if pd.isna(new_question):
                print("重写失败")
                continue
            access_question, _, _, _,_, _ = processor.review_question(question)
            new_question_refine, access_refine_question, _, _, _, _, _ = processor.review_and_rewrite_question_math(new_question)

            # 计算原始问题的难度与区分度
            difficulty_level_seed = processor.get_difficulty(question, full_categraty)
            discrimination_level_seed, _ = processor.get_discrimination(question, full_categraty)
            # 计算重写问题的难度与区分度
            difficulty_level = processor.get_difficulty(new_question_refine, full_categraty)
            discrimination_level, _ = processor.get_discrimination(new_question_refine, full_categraty)

            result_df = result_df._append({"一级分类": categrary_level1,
                                          "二级分类": categrary_level2,
                                          "三级分类": categrary_level3,
                                           "问题": question,
                                           "difficulty_level_seed": difficulty_level_seed,
                                           "discrimination_level_seed": discrimination_level_seed,
                                           "score_seed_instrcution": access_question,
                                           "improvement": gradient_selection,
                                           "new_instruction": new_question_refine,
                                           "difficulty_level": difficulty_level,
                                           "discrimination_level": discrimination_level,
                                           "score_new_instrcution": access_refine_question
                                           }, ignore_index=True)

            result_df.to_excel(record_save_file, index=False)

def response_gradient(data_path, record_save_file):
    df = pd.read_excel(data_path)
    result_df = pd.DataFrame(columns=["一级分类", "二级分类", "三级分类"])
    processor = QuestionProcessor()

    for index, row in df.iterrows():
        question = row["问题"]
        category_level1 = row["一级分类"]
        category_level2 = row["二级分类"]
        category_level3 = row["三级分类"]

        response = processor.information_capturer(question)
        new_question = processor.rewrite_question_response_gradient(response, category_level1, category_level2)

        result_df = result_df._append(
            {"一级分类": category_level1,
             "二级分类": category_level2,
             "三级分类": category_level3,
             "Question": question,
             "LLMs' Response": response,
             "new_question": new_question},
            ignore_index=True)

        result_df.to_excel(record_save_file, index=False)
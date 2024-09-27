def get_difficulty_standard():
    difficulty_standard = f'''
    0：问题没有难度，答案显而易见，模型都可以答出来。
    1：问题较容易，大部分模型可以回答出来。 
    2：问题有一定难度，少数模型可以回答出来。 
    3：问题很难，只有标杆模型可以回答出来。
    '''
    return  difficulty_standard

def get_difficulty_standard_en():
    difficulty_standard = f'''
    0: The question has no difficulty, and the answer is obvious. All models can answer it. 
    1: The question is relatively easy, and most models can answer it. 
    2: The question has some difficulty, and only a few models can answer it. 
    3: The question is very difficult, and only the benchmark models can answer it.
    '''
    return  difficulty_standard

def get_discrimination_standard():
    discrimination_standard = f'''
    区分度，是指一个测验题目能够在多大程度上区分所要测量的心理品质，反映了测验题目对心理品质区分的有效性。
    一个具有良好区分度的题目，在区分被测者时应当是有效的。能通过该项目或是在该项目上得分高的被测者，其对应的品质也较突出；
    反之，区分度较差的项目就不能有效地鉴别水平高或低的被测者。
    因此，区分度也叫做项目的效度，并作为评价项目质量、筛选项目的主要依据。
    我们的区分度共分为四种情况：低、较低、较高、高
    '''
    return discrimination_standard

def get_discrimination_standard_en():
    discrimination_standard = f'''
    Discrimination refers to the extent to which a test item can differentiate the psychological quality being measured, reflecting the effectiveness of the test item in distinguishing the psychological quality. 
    A test item with good discrimination should be effective in differentiating test-takers. 
    Those who score high on such an item or through it should have more prominent corresponding qualities; conversely, items with poor discrimination cannot effectively identify high or low-level test-takers. 
    Therefore, discrimination is also called the validity of the item and serves as the primary basis for evaluating item quality and selecting items. 
    We have four levels of discrimination: low, somewhat low, somewhat high, and high.
    '''
    return discrimination_standard

def get_instruction_follow():
    instruction_follow = f'''
    1.提高对创造力和新颖性的要求
    2.用具体的概念代替一般的概念
    3.提高抽象层次，将问题从具体实例中抽象出来
    4.跨领域整合知识
    5.限制回答使用语言
    6.设计禁用特定词汇、约束使用词汇频率、要求使用特定词汇
    7.约束句子数量、字数、特殊格式或段落数等
    8.对标点符号进行约束，只使用或不使用特定标点符号等
    9.限制开头或者结尾词
    10.要求突出显示、JSON格式、部分数量
    11.约束占位符的数量、选择是否增加附言等
    12.可使用上面多种约束方式
    '''
    return instruction_follow

def get_instruction_follow_en():
    instruction_follow = f'''
    1.Increase the requirements for creativity and novelty
    2.Replace general concepts with specific ones
    3.Raise the level of abstraction, abstracting problems from concrete instances
    4.Integrate knowledge across domains
    5.Limit the language used in the answer.
    6.Design restrictions on specific vocabulary, constrain the frequency of word usage, or require the use of specific words.
    7.Constrain the number of sentences, word count, special formats, or the number of paragraphs.
    8.Impose restrictions on punctuation marks, such as using or not using specific punctuation marks.
    9.Limit the starting or ending words.
    10.Require highlighting, JSON format, or partial quantities.
    11.Constrain the number of placeholders, choose whether to add a postscript, etc.
    12.Use multiple constraint methods from the list above.
    '''
    return instruction_follow

def get_method_list():
    method_list = f'''
    1.陷阱选项: 将问题转化为选择题，并设计陷阱选项
    2.延长逻辑链: 设计一个多阶段的逻辑推理问题，其中每一步的结论都是下一步推理的前提
    3.添加约束: 添加一个或多个约束/要求，包括但不限于使用特定的统计数据、遵循特定的推理方法、限定问题的讨论范围和引入特定的假设条件等
    4.增加信息量: 在问题的基础上创建更多的信息，如提供更多的背景信息，引入了额外的角色、数据和变量等
    5.指令跟随: 限定回答使用语言或特定关键词等，如限制使用英语或中文回答、必须包含某些关键词或禁用某些关键词、限制开头或结尾的语句等
    6.引入新颖的问题情境: 引入新颖的问题情境，如引入不同文化、不同社会背景下的情境或设定政策改变的背景
    7.将问题与其他领域知识结合: 将问题与其他领域知识结合，如结合经济学和心理学来分析消费者行为、引入特定行业或领域的实际案例、结合技术进步对社会、文化或环境的潜在影响进行分析等
    8.提高抽象水平: 提高抽象水平，将具体事物上升到概念层面，寻找其背后的普遍原则或规律
    9.组合：可使用上面多种方式
    '''
    return method_list

def get_prompt_improvement(instruction, difficulty_level, discrimination_level):
    difficulty_standard = get_difficulty_standard()
    discrimination_standard = get_discrimination_standard()
    instruction_follow = get_instruction_follow()
    prompt = f'''
    你是一个指令评估器，负责对现有指令的困难度和区分度进行评估
        
    现有指令是：
    {instruction}
    
    该指令获得的困难度得分是：
    {difficulty_level}
    困难度评判方法是：
    {difficulty_standard}
    
    该指令获得的区分度等级是：
    {discrimination_level}
    区分度的定义是：
    {discrimination_standard}
    
    如果指令的区分度等级为*低*或*较低*，可参考使用指令跟随的方式提高指令的区分度
    注意：
    1.你可以酌情的去选择适当指令跟随方式，也可以不选择
    2.最多使用其中一条
    指令跟随方式包括：{instruction_follow}
    
    根据以上信息，请给出最多三条对指令的改进建议,至少从困难度和区分度两个角度：
    '''

    return prompt

def get_prompt_improvement_en(instruction, difficulty_level, discrimination_level):
    difficulty_standard = get_difficulty_standard_en()
    discrimination_standard = get_discrimination_standard_en()
    instruction_follow = get_instruction_follow_en()
    prompt = f'''
    You are an instruction evaluator responsible for assessing the difficulty and discrimination of existing instructions.

    The existing instruction is: 
    {instruction}

    The difficulty score for this instruction is: 
    {difficulty_level} 
    The difficulty evaluation method is: {difficulty_standard}

    The discrimination level of this instruction is: 
    {discrimination_level} 
    The definition of discrimination is: 
    {discrimination_standard}

    If the discrimination level of the instruction is low or somewhat low, you can consider using an instruction follow-up method to improve the discrimination of the instruction. 
    Note that:
    You can choose an appropriate instruction follow-up method at your discretion, or you may choose not to use one.
    Use only one of the methods at most. 
    Instruction follow-up methods include: 
    {instruction_follow}
    Based on the above information, please provide up to three suggestions for improving the instruction, considering at least difficulty and discrimination aspects:
    '''
    return prompt

def get_prompt_rewrite(instruction, improvement):
    prompt = f'''
        你是一个指令设计器，负责根据现有指令和现在指令存在的问题，对原有指令进行设计和重写
        
        现有指令为：
        {instruction}
        
        但是他获得的评估是：
        {improvement}
        
        根据以上信息，重新设计并重写现有指令，使指令能够得到进一步的改善
        注意：
        1.重新设计或者重写的指令不应该包括对问题的分析和评估
        2.设计的指令应当是明确的，禁止出现如"深度"、"详细"等笼统的词语
        3.设计的指令不应该一味追求题目长度
        
        直接输出重写结果即可，无需其他内容
        重写后的指令：
        '''

    return prompt

def get_prompt_rewrite_en(instruction, improvement):
    prompt = f'''
        You are an instruction designer, responsible for redesigning and rewriting existing instructions based on their current issues.
        
        The existing instruction is: {instruction}
        
        However, the evaluation it received is: {improvement}
        
        Based on the above information, redesign and rewrite the existing instruction to further improve it. Please note:
        
        The redesigned or rewritten instruction should not include an analysis or evaluation of the problem.
        The designed instruction should be clear and specific, avoiding vague words like "in-depth" or "detailed."
        The designed instruction should not focus solely on the length of the question.
        Directly output the rewritten result without any additional content. 
        The rewritten instruction:
        '''
    return prompt

def get_prompt_rewrite_math(question_type, question, gradient_selection, prompt_id):
    prompt = f'''
你需要对数学题进行改写，让现有的AI系统（ChatGPT、GPT3等）更有困难度与区分度（有的能答对，有的答不对），你可以通过以下方法对问题进行重写/改善：
{gradient_selection}
问题：
{question}
要求：
1.重写/改善的问题应该是合理的，能被人类理解
2.确保问题描述不要冗余

请直接输出改写的问题，无需输出其他内容：
        '''
    return prompt

def get_prompt_rewrite_math_en(question_type, question, gradient_selection, prompt_id):
    prompt = f'''
You are required to rewrite a math problem to make it more challenging and discriminatory for existing AI systems (such as ChatGPT, GPT3, etc.), meaning some systems can answer correctly while others cannot. 
You can rewrite/improve the problem using the following methods: {gradient_selection} 
Question: {question} 
Requirements:
The rewritten/improved problem should be reasonable and understandable to humans.
Ensure that the problem description is not redundant.
Please directly output the rewritten question, no need to output other content:
        '''
    return prompt

def get_prompt_access_math(question):
    prompt = f'''
我希望你对问题的合理性进行评估，我将提供给你问题、问题分析步骤、输出格式。请你扮演一位数学大师，你的任务是判断问题是否合理，如果问题不合理，指出任何不合理之处，并且对问题进行修改。

问题：
{question}

问题分析步骤:
第一步：详细分析问题的各个组成部分，识别和理解问题中涉及到的相关概念，检查它们是否在数学上有定义且使用恰当
第二步：深入思考各个组成部分之间的逻辑关系。评估问题中的关系是否在数学上合理。如果可能，提供支持合理的数学证明或找出潜在的矛盾
第三步：全面评估问题的可解性。判断问题是否可以解决，是否有足够的信息或条件来求解，对于选择题需检查是否包含正确选项。如果问题无法解决，请指出缺失的信息或条件，并解释为什么这些是必要的。
第四步：仔细检查确定问题或步骤中是否有悖常识或不合理的假设。检查问题中的数字、计算的结果是否符合实际情况，如人/物的相关结果是否为整数，问题或过程中是否有违背奇偶的认知情况等

输出格式：
请严格按照下面的要求输出：
第一行输出你按照问题分析步骤进行的思考，每一步的思考都应详细解释你的推理过程和结论。如果在分析过程中发现问题不合理，请提供具体的数学证明或反例。中间禁止使用换行符。
第二行请基于上述思考，给出你对于问题的合理性的判断，如有任何分析步骤是不合理或有歧义，应当认为问题是不合理的：
    如果问题是合理的，请输出：问题合理。
    如果问题是不合理的，请输出：问题不合理。
第三行输出对问题的修改：
    如果问题是合理的，请输出：无需修改
    如果问题是不合理的，根据上述思考，对问题进行修改，并以"问题修改为："开头输出，*注意*，修改之后的问题不要给出正确答案
请严格按照上面的规定输出这三行内容，每一行之间用单换行符分开，并且请用中文作答。

请输出你的判断：
        '''

    return prompt

def get_prompt_access_math_en(question):
    prompt = f'''
I would like you to evaluate the reasonableness of a problem. 
I will provide you with the question, steps for problem analysis, and output format. 
Please play the role of a math master, and your task is to determine whether the problem is reasonable. 
If the problem is unreasonable, point out any unreasonable aspects and modify the problem accordingly.

Question:
{question}

Problem analysis steps:
Step 1: Analyze in detail the various components of the problem, identify and understand the relevant concepts involved in the problem, and check whether they are mathematically defined and used appropriately.
Step 2: Think deeply about the logical relationships between the various components. Evaluate whether the relationships in the problem are mathematically reasonable. If possible, provide supporting mathematical proofs or identify potential contradictions.
Step 3: Evaluate the solvability of the problem comprehensively. Determine whether the problem can be solved and whether there is enough information or conditions to solve it. For multiple-choice questions, check whether the correct option is included. If the problem cannot be solved, point out the missing information or conditions and explain why they are necessary.
Step 4: Carefully check for any violations of common sense or unreasonable assumptions in the problem or steps. Check whether the numbers and calculation results in the problem are consistent with reality, such as whether the results related to people/objects are integers, whether there are any violations of odd-even cognition in the problem or process, etc.

Output format:
Please strictly follow the requirements below for output:
In the first line, output your thoughts according to the problem analysis steps. Each step of thinking should explain your reasoning process and conclusions in detail. If you find the problem unreasonable during the analysis process, provide specific mathematical proofs or counterexamples. Do not use line breaks in between.
In the second line, based on the above thoughts, give your judgment on the reasonableness of the problem. If any step of the analysis is unreasonable or ambiguous, the problem should be considered unreasonable:
    If the problem is reasonable, please output: The problem is reasonable.
    If the problem is unreasonable, please output: The problem is unreasonable.
In the third line, output the modification of the problem:
    If the problem is reasonable, please output: No modification required.
    If the problem is unreasonable, modify the problem based on the above thoughts, and output with the prefix "The problem is modified as:". *Note* that the modified problem should not provide the correct answer.
Please strictly output these three lines of content according to the above regulations, separated by a single line break between each line, and answer in English.

Please output your judgment:
        '''
    return prompt

def get_prompt_access(instruction):
    prompt_access = f'''
你是一个的指令打分器，负责为以下指令进行打分：
{instruction}

【评判标准】
1.安全（1分）：指令无涉黄涉政，无暴力违法内容

2.中立（1分）：指令不带偏见，没有种族歧视

3.信息完整（1分）：指令中提供了足够的信息以明确执行任务，包括所有必要的上下文和具体细节，没有遗漏关键信息，且无需额外假设或推断。

4.可行（1分）：指令没有超出AI系统能力范围

根据以上评判标准，对指令进行打分。根据以上评判标准，对指令进行打分。
请确保指令中包含了所有必要的信息，例如如果指令要求改写句子、分析文本或提供解释，必须提供要改写的原句、要分析的文本或需要解释的具体内容。
缺少这些信息的指令可在“信息完整”和“可行”上扣分。
你的输出格式应当如下，并且只输出分值，每个点应该是0/1，总分输出0~4，无需输出其他内容：
安全：
中立：
信息完整：
可行：
总分：
        '''
    return prompt_access

def get_prompt_access_en(instruction):
    prompt_access = f'''
You are an instruction scorer, responsible for scoring the following instruction: {instruction}

【Evaluation Criteria】

Safety (1 point): The instruction does not contain any inappropriate, politically sensitive, violent, or illegal content.

Neutrality (1 point): The instruction is unbiased and does not involve racial discrimination.

Information completeness (1 point): The instruction provides enough information to clearly execute the task, including all necessary context and specific details, without omitting key information or requiring additional assumptions or inferences.

Feasibility (1 point): The instruction does not exceed the capabilities of the AI system.

Based on the above criteria, score the instruction. 
Please ensure that the instruction contains all necessary information. 
For example, if the instruction requires rewriting a sentence, analyzing text, or providing an explanation, it must provide the original sentence to be rewritten, the text to be analyzed, or the specific content to be explained. 
Instructions lacking this information can be penalized in "information completeness" and "feasibility." 
Your output format should be as follows, and only output the score. 
Each point should be 0/1, with a total score output of 0-4, without any additional content: 
Safety: 
Neutrality: 
Information completeness: 
Feasibility: 
Total score:
    '''
    return prompt_access

def get_prompt_rewrite_response_gradient(role, response):
    method_list = get_instruction_follow()
    prompt = f'''
    你是一个「{role[0]}的大师」，有「丰富的{role[1]}经验」，请结合你的专业知识扮演一个“考官”，考生是现有的AI系统（如ChatGPT、讯飞星火、通义千问、GPT3等），你的任务是根据给定的信息，设计一个问题
    我将提供给你：
    [信息：{response}]
    
    [出题要求：
    **请先考虑{role[1]}范畴内重要的标准，并作为出题的参考
    **设计的问题应该逻辑清晰，内容完整
    **设计的问题应该对考生有所困难
    **设计的问题尽量对考生具有区分度，有的考生能答对，有的考生答不对
    **问题应当具有新颖性，可以不仅局限于给定的信息
    
    [参考出题思路：
        为提高问题的困难度和区分度，你可以参考如下出题思路：
        注意：
            1.你可以酌情的去选择适当的参考出题思路，也可以不选择
            2.最多使用其中一条
        参考出题思路：{method_list}
    
    [输出格式要求]
    请严格按照下面的要求输出
        第一行：要求分点论述，给出对于给定信息可挖掘的思考点，对于提升的困难度与区分度的“思考过程”，并以"思考过程："开头，中间禁止使用换行符。Å
        第二行：根据上述思考，输出设计的问题，并以"设计的问题："开头
    请严格按照上面的规定输出者两行内容，每一行之间用单换行符分开。
    
    请输出你的设计：
    '''
    return prompt

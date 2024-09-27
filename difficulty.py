import pandas as pd
from joblib import load

class DifficultyPredictor:
    def __init__(self, model_path, cate_path):
        self.linear_model = load(model_path)
        self.cate_filename = cate_path
        self.cate_df = pd.read_excel(self.cate_filename)
        self.cate_df = self.cate_df[["二级分类", "平均难度分", "问题平均长度", "样本数"]]
        self.cate_df = self.cate_df[self.cate_df["二级分类"] != "其他-其他"]
        self.cate_df['难度总分'] = self.cate_df['平均难度分'] * self.cate_df['样本数']
        self.cate_df['问题总长度'] = self.cate_df['问题平均长度'] * self.cate_df['样本数']
        self.avg_difficulty_score = self.cate_df['难度总分'].sum() / self.cate_df['样本数'].sum()
        self.avg_prompt_len = self.cate_df['问题总长度'].sum() / self.cate_df['样本数'].sum()
        self.median_prompt_len = self.cate_df['问题平均长度'].median()

    def prepare_sample(self, prompt, category):
        data = {
            "问题": [prompt],
            "category": [category],
            "gpt4_难度分": [1.0]
        }
        data_df = pd.DataFrame(data)
        data_df["二级分类"] = data_df["category"].apply(lambda x: "-".join(x.split("-")[0:2]))
        data_df = data_df.merge(self.cate_df, on=["二级分类"], how="left")
        data_df['问题平均长度'] = data_df['问题平均长度'].fillna(self.median_prompt_len)
        data_df['平均难度分'] = data_df['平均难度分'].fillna(self.avg_difficulty_score)
        data_df["问题长度"] = data_df["问题"].apply(lambda x: len(x))
        data_df["问题长度/平均问题长度"] = data_df["问题长度"] / data_df["问题平均长度"]
        return data_df[["平均难度分", "gpt4_难度分", "问题长度/平均问题长度"]]

    def predict(self, prompt, category):
        sample = self.prepare_sample(prompt, category)
        difficulty_score_pred = self.linear_model.predict(sample)
        difficulty_score_pred = difficulty_score_pred.ravel()  # Convert to 1D array
        bins = [0, 1, 2, 4, float('inf')]
        labels = [0, 1, 2, 3]
        difficulty_level_pred = pd.cut(difficulty_score_pred, bins=bins, labels=labels, include_lowest=True)
        return difficulty_level_pred[0]
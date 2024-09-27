# coding:utf-8
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import torch
import math
import time
import numpy as np

class DiscriminationPredictor:
    def __init__(self, model_path, label_path, max_length=512, batch_size=64):
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        label_dict_df = pd.read_csv(label_path, sep="\t")
        self.label_dict = {i[0]: i[1] for i in zip(label_dict_df['label'], label_dict_df["discrimination_level"])}
        self.max_length = max_length
        self.batch_size = batch_size

        # Load cate_statis_all.csv
        self.cate_df = pd.read_csv("cate_statis_all.csv", sep='\t')
        self.cate_df = self.cate_df[["二级分类", "平均难度分", "问题平均长度", "样本数"]]
        self.cate_df = self.cate_df[self.cate_df["二级分类"] != "其他-其他"]
        self.cate_df['难度总分'] = self.cate_df['平均难度分'] * self.cate_df['样本数']
        self.cate_df['问题总长度'] = self.cate_df['问题平均长度'] * self.cate_df['样本数']
        self.avg_difficulty_score = self.cate_df['难度总分'].sum() / self.cate_df['样本数'].sum()
        self.avg_prompt_len = self.cate_df['问题总长度'].sum() / self.cate_df['样本数'].sum()
        self.median_prompt_len = self.cate_df['问题平均长度'].median()

    def predict(self, data):
        """
        data: list of dict, each dict contains "分类" and "问题"
        """
        df = pd.DataFrame(data)
        df["二级分类"] = df["分类"].apply(lambda x: "-".join(x.split("-")[0:2]))
        df = df.merge(self.cate_df[["二级分类", "平均难度分", "问题平均长度"]], on=["二级分类"], how="left")

        df['问题平均长度'] = df['问题平均长度'].fillna(self.median_prompt_len)
        df['平均难度分'] = df['平均难度分'].fillna(self.avg_difficulty_score)
        df["问题长度"] = df["问题"].apply(lambda x: len(x))
        df["问题长度/平均问题长度"] = df["问题长度"] / df["问题平均长度"]

        df['questions_predict'] = "问题分类:" + df["分类"] + "[SEP]" + "问题:" + df['问题'].apply(str) + "[SEP]" + "问题平均长度:" + df["问题平均长度"].apply(lambda x: str(x).split(".")[0]) + "[SEP]" + "问题长度比:" + df['问题长度/平均问题长度'].apply(lambda x: str(round(x, 2)))
        df["questions_predict"] = df["questions_predict"].apply(lambda x: str(x)[:self.max_length])
        test_sentences = df['questions_predict'].to_list()
        test = self.tokenizer(test_sentences, truncation=True, return_tensors="pt", padding="max_length", max_length=self.max_length)
        batch = self.batch_size
        epoch_num = math.ceil(len(test_sentences) / batch)
        print("epoch num is {n}".format(n=epoch_num))
        predict_res_total = []
        res_list = []
        df_lst = df.to_dict(orient="records")
        with torch.no_grad():
            for k in range(epoch_num):
                if k%20 == 0:
                    print(k)
                start = time.time()
                outputs = self.model(test["input_ids"][k*batch:(k+1)*batch], token_type_ids=None, attention_mask=test["attention_mask"][k*batch:(k+1)*batch])
                res = np.argmax(outputs['logits'], axis=1).tolist()
                end = time.time()
                print("predict batch {ii} cost time {t1}".format(ii=k, t1=end-start))
                for idx in range(batch):
                    now_idx = k*batch + idx
                    if now_idx >= len(df_lst):
                        break
                    tmp_dict = df_lst[now_idx]
                    predict_res = res[idx]
                    if predict_res not in self.label_dict:
                        print(predict_res)
                        continue
                    tmp_dict["predict_labels"] = self.label_dict[predict_res]
                    res_list.append(tmp_dict)
        return res_list
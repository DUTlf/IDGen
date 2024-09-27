import os
import json
import time
import random
import requests
import dashscope
from http import HTTPStatus
from abc import abstractmethod


class GPT4API():
    def __init__(self):
        self.url = ''
        self.headers = {
        }

    def get_gpt4_answer(self, prompt):
        data = {
        }
        gpt_answer = 'None'
        return gpt_answer


class GPT4API_T():
    def __init__(self):
        self.url = ''
        self.headers = {
        }

    def get_gpt4_turbo_answer(self, prompt):
        data = {
        }
        gpt_answer = 'None'
        return gpt_answer

class HunyuanAPI():
    def get_hunyuan_answer(self, prompt):
        hy_answer = 'none'
        return hy_answer

class HunyuanAPI_P():
    def get_hunyuan_p_answer(self, prompt):
        hy_answer = 'none'
        return hy_answer

class Wenxin4API():
    def __init__(self, **args):
        self.wenxin_url = ""
        self.headers = {}

    def get_answer(self, prompt):
        wenxin_answer = ''
        return wenxin_answer


class ChatGPTAPI():
    def __init__(self, **args):
        self.url = ''
        self.headers = {
            'Authorization': '',
            'Content-Type': 'json'
        }

    def get_answer(self, prompt):
        answer = ''
        return answer

class Claude3API:
    def __init__(self):
        self.url = ''
        self.headers = {
            'Authorization': '',
            'Content-Type': 'application/json'
        }

    def get_claude3_answer(self, prompt):
        claude_answer = 'None'
        return claude_answer

import dashscope
from http import HTTPStatus

dashscope.api_key = ''
class QWenMaxAPI():
    def get_answer(self, prompt):
        response = dashscope.Generation.call(
            model=dashscope.Generation.Models.qwen_max,
            prompt=prompt
        )
        if response.status_code == HTTPStatus.OK:
            print(response.output['text'])
            return response.output['text']
        else:
            print(response.code)
            print(response.message)
            return ''
# -*- coding: utf-8 -*-


import json

import requests

from utils.calctoken import TokenCalculator


class LLM:
    def __init__(self):
        self._host, self._api_key, self._api_key_primary_val = self._get_config()
        self.resume_prompt = self._get_resume_prompt()
        self.recruit_prompt = self._get_recruit_prompt()
        self.question_prompt = self._get_question_prompt()
        self._request_id = None
        self.tc = TokenCalculator()

    def _get_config(self):
        with open("config.json", "r") as cf:
            config = json.load(cf)
        return config["LLM"]["HOST"], config["LLM"]["API_KEY"], config["LLM"]["API_KEY_PRIMARY_VAL"]
    
    def _get_resume_prompt(self):
        with open('resources/resume_prompt.txt', 'r') as resume_prompt_file:
            resume_prompt = resume_prompt_file.readlines()
        resume_prompt = "".join(resume_prompt)
        return resume_prompt
    
    def _get_recruit_prompt(self):
        with open('resources/recruit_prompt.txt', 'r') as recruit_prompt_file:
            recruit_prompt = recruit_prompt_file.readlines()
        recruit_prompt = "".join(recruit_prompt)
        return recruit_prompt
    
    def _get_question_prompt(self):
        with open('resources/question_prompt.txt', 'r') as question_prompt_file:
            question_prompt = question_prompt_file.readlines()
        question_prompt = "".join(question_prompt)
        return question_prompt
    
    def resume_summary(self, text):
        self._request_id = "Resume-Summary"
        resume_prompt_with_input = self.resume_prompt.format(resume=text)
        # print(resume_prompt_with_input)
        # print(self.tc.calculate(resume_prompt_with_input))
        preset_text = [{"role":"system","content":str(resume_prompt_with_input)}]
        request_data = {
            'messages': preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 2500,
            'temperature': 0.5,
            'repeatPenalty': 5.0,
            'stopBefore': [],
            'includeAiFilters': False
        }
        return self._execute(request_data)

    def recruit_summary(self, text):
        self._request_id = "Recruit-Summary"
        recruit_prompt_with_input = self.recruit_prompt.format(recruit=text)
        # print(recruit_prompt_with_input)
        # print(self.tc.calculate(recruit_prompt_with_input))
        preset_text = [{"role":"system","content":str(recruit_prompt_with_input)}]
        request_data = {
            'messages': preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 2000,
            'temperature': 0.5,
            'repeatPenalty': 5.0,
            'stopBefore': [],
            'includeAiFilters': False
        }
        return self._execute(request_data)

    def make_question(self, resume_summary, recruit_summay):
        self._request_id = "Make-Question"
        qustion_prompt_with_input = self.question_prompt.format(resume_summary=resume_summary, recruit_summay=recruit_summay)
        print(qustion_prompt_with_input)
        print(self.tc.calculate(qustion_prompt_with_input))
        preset_text = [{"role":"system","content":str(qustion_prompt_with_input)}]
        request_data = {
            'messages': preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 1500,
            'temperature': 0.5,
            'repeatPenalty': 5.0,
            'stopBefore': [],
            'includeAiFilters': False
        }
        return self._execute(request_data)

    def _execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            # 'Accept': 'text/event-stream'
        }

        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-002',
                           headers=headers, json=completion_request, stream=False) as r:
            # for line in r.iter_lines():
            #     if line:
            #         print(line.decode('utf-8'))
            return r

# -*- coding: utf-8 -*-


import json

import requests

# from utils.calctoken import TokenCalculator


class LLM:
    def __init__(self):
        self._host, self._api_key, self._api_key_primary_val = self._get_config()
        self.resume_prompt = self._get_resume_prompt()
        self.recruit_prompt = self._get_recruit_prompt()
        self.question_prompt = self._get_question_prompt()
        self.interviewer_feel_prompt = self._get_interviewer_feel_prompt()
        self.keyword_prompt = self._get_keyword_prompt()
        self.bestanswer_prompt = self._get_bestanswer_prompt()
        self._request_id = None
        # self.tc = TokenCalculator()

    def _get_config(self):
        with open("config.json", "r") as cf:
            config = json.load(cf)
        return config["LLM"]["HOST"], config["LLM"]["API_KEY"], config["LLM"]["API_KEY_PRIMARY_VAL"]
    
    def _get_resume_prompt(self):
        with open('resources/resume_prompt.txt', 'r') as resume_prompt_file:
            resume_prompt = resume_prompt_file.readlines()
        resume_prompt = "\n".join(resume_prompt)
        return resume_prompt
    
    def _get_recruit_prompt(self):
        with open('resources/recruit_prompt.txt', 'r') as recruit_prompt_file:
            recruit_prompt = recruit_prompt_file.readlines()
        recruit_prompt = "\n".join(recruit_prompt)
        return recruit_prompt
    
    def _get_question_prompt(self):
        with open('resources/question_prompt.txt', 'r') as question_prompt_file:
            question_prompt = question_prompt_file.readlines()
        question_prompt = "\n".join(question_prompt)
        return question_prompt

    def _get_interviewer_feel_prompt(self):
        with open('resources/interviewer_feel_prompt.txt', 'r') as interviewer_feel_prompt_file:
            interviewer_feel_prompt = interviewer_feel_prompt_file.readlines()
        interviewer_feel_prompt = "\n".join(interviewer_feel_prompt)
        return interviewer_feel_prompt

    def _get_keyword_prompt(self):
        with open('resources/keyword_prompt.txt', 'r') as keyword_prompt_file:
            keyword_prompt = keyword_prompt_file.readlines()
        keyword_prompt = "\n".join(keyword_prompt)
        return keyword_prompt

    def _get_bestanswer_prompt(self):
        with open('resources/bestanswer_prompt.txt', 'r') as bestanswer_prompt_file:
            bestanswer_prompt = bestanswer_prompt_file.readlines()
        bestanswer_prompt = "\n".join(bestanswer_prompt)
        return bestanswer_prompt
    
    def resume_summary(self, text):
        self._request_id = "Resume-Summary"
        # resume_prompt_with_input = self.resume_prompt.format(resume=text)
        # print(resume_prompt_with_input)
        # print(self.tc.calculate(resume_prompt_with_input))
        preset_text = [{"role":"system", "content":str(self.resume_prompt)}, {"role":"user","content": str(text)}]
        request_data = {
            'messages': preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 700,
            'temperature': 1.0,
            'repeatPenalty': 4.0,
            'stopBefore': [],
            'includeAiFilters': False
        }
        return self._execute(request_data)

    def recruit_summary(self, text):
        self._request_id = "Recruit-Summary"
        # recruit_prompt_with_input = self.recruit_prompt.format(recruit=text)
        # print(recruit_prompt_with_input)
        # print(self.tc.calculate(recruit_prompt_with_input))
        preset_text = [{"role":"system", "content":str(self.recruit_prompt)}, {"role":"user","content":str(text)}]
        request_data = {
            'messages': preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 500,
            'temperature': 1.0,
            'repeatPenalty': 4.0,
            'stopBefore': [],
            'includeAiFilters': False
        }
        return self._execute(request_data)

    def make_question(self, resume_summary, recruit_summary):
        self._request_id = "Make-Question"
        # qustion_prompt_with_input = self.question_prompt.format(resume_summary=resume_summary, recruit_summary=recruit_summary)
        # print(qustion_prompt_with_input)
        # print(self.tc.calculate(qustion_prompt_with_input))
        user_input = f"#채용공고\n{recruit_summary}\n\n#이력서\n{resume_summary}"
        preset_text = [{"role":"system", "content":str(self.question_prompt)},{"role":"user","content":user_input}]
        request_data = {
            'messages': preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 1000,
            'temperature': 0.25,
            'repeatPenalty': 6.0,
            'stopBefore': [],
            'includeAiFilters': False
        }
        return self._execute(request_data)

    def interviewer_feel(self, text):
        self._request_id = "Interviewer`s-Feel"
        # interveiwer_feel_prompt_with_input = self.interviewer_feel_prompt.format(applicant_answer=text)
        # print(interveiwer_feel_prompt_with_input)
        # print(self.tc.calculate(interveiwer_feel_prompt_with_input))
        user_input = f"#답변\n{text}"
        preset_text = [{"role":"system", "content":str(self.interviewer_feel_prompt)}, {"role":"user","content":user_input}]
        request_data = {
            'messages': preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 500,
            'temperature': 0.76,
            'repeatPenalty': 7.0,
            'stopBefore': [],
            'includeAiFilters': False
        }
        return self._execute(request_data)

    def keyword(self, text):
        self._request_id = "Keyword"
        # keyword_prompt_with_input = self.keyword_prompt.format(applicant_answer=text)
        # print(keyword_prompt_with_input)
        # print(self.tc.calculate(keyword_prompt_with_input))
        user_input = f"#답변\n{text}"
        preset_text = [{"role":"system","content":self.keyword_prompt}, {"role":"user","content":user_input}]
        request_data = {
            'messages': preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 800,
            'temperature': 0.5,
            'repeatPenalty': 7.0,
            'stopBefore': [],
            'includeAiFilters': False
        }
        return self._execute(request_data)

    def bestanswer(self, question, answer):
        self._request_id = "Best-Answer"
        # bestanswer_prompt_with_input = self.bestanswer_prompt.format(applicant_answer=text)
        # print(bestanswer_prompt_with_input)
        # print(self.tc.calculate(bestanswer_prompt_with_input))
        user_input = f"#답변\n{answer}"
        preset_text = [{"role":"system", "content":self.bestanswer_prompt}, {"role":"user","content":user_input}]
        request_data = {
            'messages': preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 1000,
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

        with requests.post(self._host + '/serviceapp/v1/chat-completions/HCX-002',
                           headers=headers, json=completion_request, stream=False) as r:
            # for line in r.iter_lines():
            #     if line:
            #         print(line.decode('utf-8'))
            return r

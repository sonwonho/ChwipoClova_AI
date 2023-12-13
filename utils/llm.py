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
        print(resume_prompt_with_input)
        print(self.tc.calculate(resume_prompt_with_input))
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
        print(recruit_prompt_with_input)
        print(self.tc.calculate(recruit_prompt_with_input))
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

        ## To-Do DataBase 연동
        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-002',
                           headers=headers, json=completion_request, stream=False) as r:
            # for line in r.iter_lines():
            #     if line:
            #         print(line.decode('utf-8'))
            return r

                    

if __name__ == '__main__':
    llm = LLM()
    # resume_text = '''010-5626-7771 신유진 · hewwnewd@gmail.ccom Product Designer https://intothewaves.github.io/portfolio-ko/ EXPERIENCE 2023.03-Present Freelancer 퍼블리싱 프리랜서로 LB 루셈, 부뜰정보시스템 홈페이지 개발에 참여했습니다. 2021.05-2023.02 홀릭디자인 UX디자이너· 퍼블리셔 디자인 에이전시 홀릭디자인에서 UX 디자이너로 일하며 각 기업의 브랜딩 전략을 세워 이를 기반으로 디자인 작 업을 진행했습니다. 또한, 안정적이고 인터렉티브한 화면을 개발하는 퍼블리싱 작업도 담당했습니다. 대표적으로 kt cs는 사이트 오픈 이후 트래픽이 273.7%증가(9.3k → 34.6k), LB 세미콘은 33%증가(6k → 8k)하는 등의 성과가 있었습니다. 4개 국어로 개발된 대구시 홍보 앱 대구트립은 7만명 이상이 다운로드 받았습니다. 또한 다양 한 프로젝트들이 여러 디자인 어워드의 수상작으로 선정되었습니다. Web · kt cs · LB 세미콘 · airbox · 디자인3.3 · pnc tech . 판교 청년지원센터 ·봉화 농촌체험휴양마을 App · 대구트립 . 어웨이캠프 2014.09 - 2019.12 카이스트 공동육아 연구소 '우리두리' 회장 · 회원 연구소로 확대 개편 된 공동 육아 동아리 '우리두리'에서 회장 및 회원으로 활동하며 유아 교육 프로그램을 기획 하고 진행하였습니다. '우리두리'는 카이스트 대학원생 가족들로 구성된 동아리로, 매일 3시간씩 아이이의 발달 단계에 맞춘 교육과 놀이 활동에 참여한 후 식사와 교류를 이어가는 곳입니다. 2012.07 - 2012.12 민주당 문재인 후보 대통령 선거캠프 | 디지털 캠페인 본부 SNS 팀원·문재인tv 리포터 디지털 캠페인 본부의 SNS팀에서 문재인 후보의 메세지 작성에 참여하고, 후보 이미지 보정 및 업로드, 홍보 컨 텐츠 제작에 참여했습니다. 9월부터는 문재인tv팀으로로 배속되어 문재인 후보와 함께 전국을 돌며 시청자들께 일정 및 정책 브리핑을 진행했습니다. 2011.09-2012.06 ingToon | 대표 멸종위기 동물 키우기 게임 앱을 만드는 스타트업을 창업했습니다. 유저가 동물을 키우면서 아이템을 구매하거나 광고를 클릭하면 수익금의 일부가 환경보호 단체에 기부되는 게임입니다. 한국 사회적 기업가 육성사업과 서울시 청년창업 1000프로젝트에 선정되었습니다. 2009.07-2010.03 이화여대 U카드 대표 대학가 영세상인과 이화여대 학생들간의 멤버십 카드를 만들었습니다. 카드 발급비도 유료이고, 방학중인 7월에 시작했음에도 출시 2주만에 재학생의 10%가 가입하는 등 폭발적인 성장이 있었습니다. 이후 제가 총학생회 선거 에 당선되어 이를 모든 재학생이 사용가능한 복지카드로 확대하고 정착시켰습니다. EDUCATION ACHIVEMENT 2023.03-2023.06 Google UX Design 2022 GDWEB DESIGN AWARD Google UX Design Certificate Winner Prize 6개 프로젝트 수상 2008.03-2013.02 이화여자대학교 i-AWARDS KOREA WEB AWARD 4개 분야 대상·2개 분야 최우수상 수상 조형예술대학 조소과 · 42대 총학생회 부총학생회장 2012 서울시 청년창업 1000프로젝트 선정 2011.07 - 2011.08 IESEG School of Management 2011 한국 사회적 기업가 육성사업 선정 교환학생 캠퍼스 CEO 창업경진대회 2005.03-2008.02 선화예술고등학교 최우수상 EBS 청년 창업오디션 브레인 빅뱅 최종 본선 12인 진출 SKILLS CERTIFICATE RESEARCH DESIGN PROGRAMMING 2023 SQLD(SQL Developer) Google Analytics, Figma, AfterEffects, HTML, CSS, JS 2021 웹디자인 기능사 Oracle, Tableau Blender, Photoshop, Illustrartor, Protopie 2019 토익 930점'''
    # llm.resume_summary(resume_text)
    resume_sum = '''[지원자 이름] = 신유진\n[지원자 적합 포지션] = Product Designer, UX designer\n[지원자 학력 사항] = 선화예술고등학교 (2005년 3월 ~ 2008년 2월) / 이화여자대학교 조형예술대학 조소과 (2008년 3월 ~ 2013년 2월) / IESEG School of Management 교환학생 (2011년 7월 ~ 2011년 8월)\n[지원자 경력 사항] =\n1.홀릭디자인 UX디자이너·퍼블리셔 (2021년 5월 - 2023년 2월) : KT cs, LB 세미콘, Airbox, 디자인33, PNC Tech, 판교 청년지원센터, 봉화 농촌체험휴양마을 애플리케이션 UIUX 디자인 및 퍼블리싱 업무 수행\n2.민주당 문재인 후보 대통령 선거캠프 디지털 캠페인 본부 SNS 팀원·문재인 TV 리포터 (2012년 7월 - 2012년 12월)\n3.ingToon 대표 (2011년 9월 - 2012년 6월): 멸종 위기 동물 키우기 게임 앱 운영, 한국 사회적 기업가 육성 사업과 서울시 청년창업 1000프로젝트 선정\n4.이화여대 U카드 대표 (2009년 7월 - 2010년 3월): 대학가 영세상인과 이화여대 학생들을 위한 멤버십 카드 발행 성공 사례 구축\n5.프리랜서 퍼블리셔 (2023년 3월 - 현재): LB 루셈, 부뜰정보시스템 홈페이지 개발 참여\n[지원자 자격/어학/수상] =\n1.자격증: 웹디자인 기능사, SQLD(SQL Developer)\n2.어학: 토익 930점\n3.수상내역: \n   -2022 GDWEB DESIGN AWARD Google UX Design Certificate Winner Prize 6개 프로젝트 수상\n   -i-AWARDS KOREA WEB AWARD 4개 분야 대상·2개 분야 최우수상 수상\n   -캠퍼스 CEO 창업경진대회 최우수상\n   -EBS 청년 창업오디션 브레인 빅뱅 최종 본선 12인 진출\n[지원자 기술] = Google Analytics, Figma, AfterEffects, HTML, CSS, JS, Oracle, Tableau, Blender, Photoshop, Illustrator, Protopie\n[지원자 진행 프로젝트] =\n1.대구 트립: 4개 국어로 개발된 대구시 홍보 애플리케이션으로 7만 명 이상이 다운로드 받음\n2.어웨이 캠프: 여행지 추천 서비스 제공 모바일 애플리케이션\n3.KT cs, LB 세미콘, Airbox, 디자인33, PNC Tech, 판교 청년지원센터, 봉화 농촌체험휴양마을 애플리케이션: 브랜드 전략 수립부터 GUI 디자인, 퍼블리싱까지 종합적인 프로세스 경험\n4.기타 개인 포트폴리오 다수([지원자 링크])\n[지원자 요약] = 뛰어난 커뮤니케이션 능력과 문제 해결 능력을 바탕으로 팀 내 협업 시 원활한 소통을 주도함. 다국어 구사 능력 보유하였으며, 글로벌 시장에서도 경쟁력 있는 인재임. 클라이언트와의 적극적인 소통을 통해 요구사항을 정확하게 파악하고 구현할 수 있음.'''

#     recruit_text = '''테이블매니저(TableManager)는 레스토랑의 예약 및 고객관리 혁신을 통해 외식업 소상공인과 소비자 모두에게 더 나은 경험을 제공하는 IT 스타트업입니다.

# 매장 입장에서는 테이블매니저 소프트웨어 하나로 전화, 카카오톡(챗봇), 네이버 예약 등 여러 경로를 통해 들어오는 예약을 효율적으로 실시간 통합관리하고 고객 데이터를 쌓을 수 있습니다. 현재 이랜드이츠(애슐리, 자연별곡 등), 가온, 알라프리마, 울프강스테이크하우스, 엔타스그룹(경복궁, 삿뽀로, 고구려 등) 국내 유명 레스토랑, 프렌차이즈 브랜드, 소상공인, 공공기관 등 2,000여곳이 테이블매니저 솔루션을 사용하고 있습니다.

# 국내외 다른 기업이 제공하지 못하던 외식업 소상공인 전용 디지털 솔루션을 통해 경영을 효율화하는 한편, 독자적인 빈자리 수요예측AI를 개발하였고 국내 유수의 플랫폼과 협업하고 잇습니다. 이러한 경쟁력을 통해 국내 최대 규모로 축적한 고객 예약 데이터와 서비스의 가능성을 인정받아 카카오, 네이버 계열 VC의 초기투자에 이어 2020년 2월 메가인베스트먼트, 신한캐피탈, 캡스톤파트너스 등으로부터 Series A 단계의 투자를 유치하였습니다. 현재 Series B 단계로의 성장과 외식업 외 효율적인 예약관리가 필요한 모든 영역과 유관 업종으로의 확장, B2B에서 B2C로 서비스 환경 및 고도화, 구글과의 협력을 통한 해외진출 등 사업 확장을 위한 대규모 인재채용, 조직개편, 사업영역 확대 등을 추진 중입니다.

# 테이블매니저팀만의 독보적인 전략과 성장가능성에 설레신다면, 지금 바로 합류하실 때입니다.

# Digitalize Each and Every Business on the Globe TIl No Empty Tables!

# 주요업무
# • Product 기획부터 출시까지 전반적인 프로세스에 참여 합니다. 
# • 서비스 운영 정책과 업무 프로세스 등을 분석하여 어드민 기능 개선, 프로세스 개선, 기획업무 등을 수행합니다.
# • 쉽고 편리한 고객 경험을 제공하기 위해 데이터를 분석하고 개선안을 도출합니다.

# 자격요건
# • 웹/앱 서비스에 대한 PM/PO 경험 1년 이상이신 분
# • 서비스 성장을 위한 개선 기획과 안정적이고 효율성을 위한 기획을 경험하신 분
# • 다양한 협업 팀과 사용자/기술/사업 측면에서 원활한 커뮤니케이션이 가능한 분

# 우대사항
# • 멀티플랫폼 서비스 기획 경험자
# • 실시간 웹서비스 기획 경험자
# • 외식업 및 푸드테크 업계 경험자'''
    # llm.recruit_summary(recruit_text)
    recruit_sum = '''1. 기업 : 테이블매니저(TableManager)\n2. 팀명 : 테이블매니저팀\n3. 직무 : Product Manager / Project Manager\n4. 주요수행 업무 : • Product 기획부터 출시까지 전반적인 프로세스에 참여 합니다. \n• 서비스 운영 정책과 업무 프로세스 등을 분석하여 어드민 기능 개선, 프로세스 개선, 기획업무 등을 수행합니다.\n• 쉽고 편리한 고객 경험을 제공하기 위해 데이터를 분석하고 개선안을 도출합니다.\n5. 자격 요건 : 웹/앱 서비스에 대한 PM/PO 경험 1년 이상이신 분\n서비스 성장을 위한 개선 기획과 안정적이고 효율성을 위한 기획을 경험하신 분\n다양한 협업 팀과 사용자/기술/사업 측면에서 원활한 커뮤니케이션이 가능한 분\n6. 우대사항 : 멀티플랫폼 서비스 기획 경험자\n실시간 웹서비스 기획 경험자\n외식업 및 푸드테크 업계 경험자'''

    llm.make_question(resume_sum, resume_sum)

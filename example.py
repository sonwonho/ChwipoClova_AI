# -*- coding: utf-8 -*-

import requests


class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            # 'Accept': 'text/event-stream'
        }

        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-002',
                           headers=headers, json=completion_request, stream=True) as r:
            # for line in r.iter_lines():
            #     if line:
            #         print(line.decode("utf-8"))
            print(r)
            print(r.json())


if __name__ == '__main__':
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY9GzXJ4v/+CTlSVXp8ep1tXlrwo3scVAggWC0+DNnMZ1BY9DvXgSdqqRXlh2NF8SdXoXvctXJ4+FPyYGbnmCEY23TV6D8+kgQoFQWKP5PBew1KLVrkaRHIW4K0Wylw5nSVmafUvew6VyD2MhWUCRPpFCco3uj3dD+tSy4OeMmA+0oivyeyQw3rP9SMeiAbQTGDNyw19W85gTRmSP8zhT1Qk=',
        api_key_primary_val='FFqZmhEUFGG8Xe0akva0GfVXag3LTtTCQatQ0SOe',
        request_id='eef28803b0004a419588d234782318d8'
    )

    text = bytes('''#페르소나
당신은 기업의 유능한 인사 담당자입니다. 지원자의 [이력서]를 확인하였습니다.
[이력서]의 내용을 토대로 지원자에 대하여 요약을 하고자 합니다. 당신은 지원자의 필수 정보들은 [이력서]의 내용을 토대로 작성합니다.

#필수정보
[지원자 이름] = 지원자의 이름
[지원자 적합 포지션] = 지원자의 [이력서]의 내용을 고려하여 1~2개의 적합 포지션 작성
[지원자 학력 사항] = 지원자의 학력을 시간 순서대로  [입학-졸업] [학교명]에 대하여 정리하며 [학과]가 있다면 추가
[지원자 경력 사항] = 지원자의 경력을 시간 순서대로  [시작일-종료일] [회사명] [업무]에 대하여 정리
[지원자 자격/어학/수상] = 지원자의 자격, 어학, 수상 내역을 정리
[지원자 기술] = 지원자의 기술중 가장 언급이 많이된 순서로 나열
[지원자 진행 프로젝트] = 지원자가 진행한 프로젝트를 지원자가 작성한 순서로 나열하며, [프로젝트명] [프로젝트 요약]은 필수로 작성
[지원자 요약] = 지원자의 장단점을 2~3줄로 요약

#추가정보
당신이 중요하다 생각되는 지원자의 특징을 필수정보 내용과 중복되지 않도록 요약해줘
''', 'utf-8')
    text1 = bytes('''#이력서\n 010-5626-7771 신유진 · hewwnewd@gmail.ccom Product Designer https://intothewaves.github.io/portfolio-ko/ EXPERIENCE 2023.03-Present Freelancer 퍼블리싱 프리랜서로 LB 루셈, 부뜰정보시스템 홈페이지 개발에 참여했습니다. 2021.05-2023.02 홀릭디자인 UX디자이너· 퍼블리셔 디자인 에이전시 홀릭디자인에서 UX 디자이너로 일하며 각 기업의 브랜딩 전략을 세워 이를 기반으로 디자인 작 업을 진행했습니다. 또한, 안정적이고 인터렉티브한 화면을 개발하는 퍼블리싱 작업도 담당했습니다. 대표적으로 kt cs는 사이트 오픈 이후 트래픽이 273.7%증가(9.3k → 34.6k), LB 세미콘은 33%증가(6k → 8k)하는 등의 성과가 있었습니다. 4개 국어로 개발된 대구시 홍보 앱 대구트립은 7만명 이상이 다운로드 받았습니다. 또한 다양 한 프로젝트들이 여러 디자인 어워드의 수상작으로 선정되었습니다. Web · kt cs · LB 세미콘 · airbox · 디자인3.3 · pnc tech . 판교 청년지원센터 ·봉화 농촌체험휴양마을 App · 대구트립 . 어웨이캠프 2014.09 - 2019.12 카이스트 공동육아 연구소 '우리두리' 회장 · 회원 연구소로 확대 개편 된 공동 육아 동아리 '우리두리'에서 회장 및 회원으로 활동하며 유아 교육 프로그램을 기획 하고 진행하였습니다. '우리두리'는 카이스트 대학원생 가족들로 구성된 동아리로, 매일 3시간씩 아이이의 발달 단계에 맞춘 교육과 놀이 활동에 참여한 후 식사와 교류를 이어가는 곳입니다. 2012.07 - 2012.12 민주당 문재인 후보 대통령 선거캠프 | 디지털 캠페인 본부 SNS 팀원·문재인tv 리포터 디지털 캠페인 본부의 SNS팀에서 문재인 후보의 메세지 작성에 참여하고, 후보 이미지 보정 및 업로드, 홍보 컨 텐츠 제작에 참여했습니다. 9월부터는 문재인tv팀으로로 배속되어 문재인 후보와 함께 전국을 돌며 시청자들께 일정 및 정책 브리핑을 진행했습니다. 2011.09-2012.06 ingToon | 대표 멸종위기 동물 키우기 게임 앱을 만드는 스타트업을 창업했습니다. 유저가 동물을 키우면서 아이템을 구매하거나 광고를 클릭하면 수익금의 일부가 환경보호 단체에 기부되는 게임입니다. 한국 사회적 기업가 육성사업과 서울시 청년창업 1000프로젝트에 선정되었습니다. 2009.07-2010.03 이화여대 U카드 대표 대학가 영세상인과 이화여대 학생들간의 멤버십 카드를 만들었습니다. 카드 발급비도 유료이고, 방학중인 7월에 시작했음에도 출시 2주만에 재학생의 10%가 가입하는 등 폭발적인 성장이 있었습니다. 이후 제가 총학생회 선거 에 당선되어 이를 모든 재학생이 사용가능한 복지카드로 확대하고 정착시켰습니다. EDUCATION ACHIVEMENT 2023.03-2023.06 Google UX Design 2022 GDWEB DESIGN AWARD Google UX Design Certificate Winner Prize 6개 프로젝트 수상 2008.03-2013.02 이화여자대학교 i-AWARDS KOREA WEB AWARD 4개 분야 대상·2개 분야 최우수상 수상 조형예술대학 조소과 · 42대 총학생회 부총학생회장 2012 서울시 청년창업 1000프로젝트 선정 2011.07 - 2011.08 IESEG School of Management 2011 한국 사회적 기업가 육성사업 선정 교환학생 캠퍼스 CEO 창업경진대회 2005.03-2008.02 선화예술고등학교 최우수상 EBS 청년 창업오디션 브레인 빅뱅 최종 본선 12인 진출 SKILLS CERTIFICATE RESEARCH DESIGN PROGRAMMING 2023 SQLD(SQL Developer) Google Analytics, Figma, AfterEffects, HTML, CSS, JS 2021 웹디자인 기능사 Oracle, Tableau Blender, Photoshop, Illustrartor, Protopie 2019 토익 930점''', 'utf-8')

    preset_text = [{"role":"system","content":str(text, 'utf-8')}, {'role':"user", "content":str(text1, "utf-8")}]

    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 900,
        'temperature': 0.5,
        'repeatPenalty': 5.0,
        'stopBefore': [],
        'includeAiFilters': True
    }

    print(preset_text)
    completion_executor.execute(request_data)

import json
import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, Response, request, send_file

from utils.articledb import ArticleDB
from utils.calctoken import TokenCalculator
from utils.clovaocr import FILE_OCR
from utils.llm import LLM

app = Flask(__name__)
fo = FILE_OCR()
tc = TokenCalculator()
llm = LLM()
article_db = ArticleDB()


@app.route("/file_test", methods=["POST"])
def test_file():
    file = request.files["file"]
    filename = file.filename
    filename, ext = os.path.splitext(filename)
    if ext in [".jpg", ".jpeg", ".png"]:
        return Response(file.stream.read(), mimetype=f"image/{ext}")
    elif ext == ".pdf":
        return Response(file.stream.read(), mimetype="application/pdf")
    elif ext == ".txt":
        return Response(bytes(file.stream.read()), mimetype="text/plain")
    else:
        return Response(json.dumps({"message": "file_error"}))


@app.route("/ocr", methods=["POST"])
def ocr_file():
    file = request.files["file"]

    text = fo.byte_convert_txt(file)
    return Response(bytes(text, "utf-8"), mimetype="text/plain")


@app.route("/url_ocr", methods=["POST"])
def ocr_url():
    btext = request.data
    url = str(btext, "utf-8")
    text = fo.url_convert_txt(url)
    return Response(bytes(text, "utf-8"), mimetype="text/plain")


@app.route("/count_token", methods=["POST"])
def count_token():
    btext = request.data
    text = str(btext, "utf-8")
    token_count = tc.calculate(text)
    return Response(str(token_count), mimetype="text/plain")


@app.route("/llm/resume", methods=["POST"])
def llm_resume():
    btext = request.data
    text = str(btext, "utf-8")
    result_response = llm.resume_summary(text)
    return Response(result_response, mimetype="application/json")


@app.route("/llm/recruit", methods=["POST"])
def llm_recruit():
    btext = request.data
    text = str(btext, "utf-8")
    result_response = llm.recruit_summary(text)
    return Response(result_response, mimetype="application/json")


@app.route("/llm/question", methods=["POST"])
def llm_question():
    input_json = request.json
    recruit_summary = str(input_json["recruit_summary"])
    resume_summary = str(input_json["resume_summary"])
    result_response = llm.make_question(recruit_summary, resume_summary)
    return Response(result_response, mimetype="application/json")


@app.route("/llm/interviewer_feel", methods=["POST"])
def llm_interviewer_feel():
    btext = request.data
    text = str(btext, "utf-8")
    result_response = llm.interviewer_feel(text)
    return Response(result_response, mimetype="application/json")


@app.route("/llm/keyword", methods=["POST"])
def llm_keyword():
    btext = request.data
    text = str(btext, "utf-8")
    result_response = llm.keyword(text)
    return Response(result_response, mimetype="application/json")


@app.route("/llm/best-answer", methods=["POST"])
def llm_bestanswer():
    input_json = request.json
    question = str(input_json["question"])
    answer = str(input_json["answer"])
    result_response = llm.bestanswer(question, answer)
    return Response(result_response, mimetype="application/json")


@app.route("/article/update_category/<day>", methods=["GET"])
def update_category(day):
    update_count = 0
    llm_result = ""
    for id, link in article_db.get_feed_information_iter(day):
        update_count += 1
        if update_count > 10:
            continue
        try:
            ocr = fo.url_convert_txt(link)
        except Exception as e:
            print(e)
            print("Failed OCR")

        try:
            llm_result = llm.article_category(ocr).text
        except Exception as e:
            print(e)
            print("Failed category LLM")

        for categore_name in article_db.get_category_list():
            if categore_name in llm_result:
                article_db.insert_feed_category_result(id, categore_name)
                # print(article_db.get_category_id(categore_name))
            else:
                print(f"No categore = {categore_name}")
                continue

    return Response(str(update_count), mimetype="text/plain")


def auto_update_category():
    update_category(1)


if __name__ == "__main__":
    sched = BackgroundScheduler(timezone="Asia/Seoul")
    sched.add_job(auto_update_category, "cron", hour="3", minute="00", id="article")
    sched.start()
    app.run(host="10.41.182.236", port=5000, debug=False)

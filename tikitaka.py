import json
import os

from flask import Flask, Response, request, send_file

from utils.calctoken import TokenCalculator
from utils.clovaocr import FILE_OCR
from utils.llm import LLM

app = Flask(__name__)
fo = FILE_OCR()
tc = TokenCalculator()
llm = LLM()

@app.route('/file_test', methods=["POST"])
def test_file():
    file = request.files['file']
    filename = file.filename
    filename, ext = os.path.splitext(filename)
    if ext in ['.jpg', '.jpeg', '.png']:
        return Response(file.stream.read(), mimetype=f"image/{ext}")
    elif ext == ".pdf":
        return Response(file.stream.read(), mimetype="application/pdf")
    elif ext == ".txt":
        return Response(bytes(file.stream.read()), mimetype="text/plain")
    else:
        return Response(json.dumps({"message":"file_error"}))

@app.route('/ocr', methods=["POST"])
def ocr_file():
    file = request.files['file']

    text = fo.byte_convert_txt(file)
    return Response(bytes(text, 'utf-8'), mimetype="text/plain")

@app.route('/count_token', methods=["POST"])
def count_token():
    btext = request.data
    text = str(btext, 'utf-8')
    token_count = tc.calculate(text)
    return Response(str(token_count), mimetype="text/plain")

@app.route('/llm/resume', methods=["POST"])
def llm_resume():
    btext = request.data
    text = str(btext, 'utf-8')
    result_response = llm.resume_summary(text)
    return Response(result_response, mimetype="application/json")

@app.route('/llm/recruit', methods=["POST"])
def llm_recruit():
    btext = request.data
    text = str(btext, 'utf-8')
    result_response = llm.recruit_summary(text)
    return Response(result_response, mimetype="application/json")

@app.route('/llm/question', methods=["POST"])
def llm_question():
    input_json = json.loads(request.json)
    recruit_summay = str(input_json["recruit_summay"])
    resume_summary = str(input_json["resume_summary"])
    result_response = llm.make_question(recruit_summay, resume_summary)
    return Response(result_response, mimetype="application/json")


if __name__ == '__main__':
    app.run(debug=False)

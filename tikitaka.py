import json
import os

from flask import Flask, Response, request, send_file

from utils.clovaocr import FILE_OCR

app = Flask(__name__)
fo = FILE_OCR()

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



if __name__ == '__main__':
    app.run(debug=True)

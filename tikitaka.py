import json
import os

from flask import Flask, Response, request, send_file

app = Flask(__name__)

@app.route('/file_test', methods=["POST"])
def test_file():
    file = request.files['file']
    filename = file.filename
    filename, ext = os.path.splitext(filename)
    if ext in ['.jpg', '.jpeg', '.png']:
        return Response(file.stream.read(), mimetype=f"image/{ext}")
    elif ext == ".pdf":
        return Response(file.stream.read(), mimetype="application/pdf")
    else:
        return Response(json.dumps({"message":"file_error"}))

if __name__ == '__main__':
    app.run(debug=True)

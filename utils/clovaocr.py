import json
import os
import time
import uuid

import requests


class FILE_OCR:
    def __init__(self):
        self.api_url, self.secret_key = self._get_config()

    def _get_config(self):
        with open("config.json", "r") as cf:
            config = json.load(cf)
        return config["CLOVA_OCR"]["API_URL"], config["CLOVA_OCR"]["KEY"]

    def file_convert_txt(self, file_path, is_save=False):
        file_name = os.path.basename(file_path)
        ext = os.path.splitext(file_path)[-1].replace(".","")
        request_json = {
            "images": [{"format": ext, "name": file_name}],
            "requestId": str(uuid.uuid4()),
            "version": "V2",
            "timestamp": int(round(time.time() * 1000)),
        }

        payload = {"message": json.dumps(request_json).encode("UTF-8")}
        files = [("file", open(file_path, "rb"))]
        headers = {"X-OCR-SECRET": self.secret_key}

        response = requests.request("POST", self.api_url, headers=headers, data=payload, files=files)

        json_file = os.path.join("results",file_name.replace(ext, "json"))
        if is_save:
            with open(json_file, "w") as jf:
                json.dump(response.json(), jf)

            with open(json_file, "r") as jf:
                js = json.load(jf)
        else:
            js = response.json()

        text = []
        for image in js['images']:
            for filed in image['fields']:
                text.append(filed['inferText'])
        
        txt_file = os.path.join("results", file_name.replace(ext, "txt"))
        if is_save:
            with open(txt_file, 'w') as txt:
                txt.write(" ".join(text))
        return " ".join(text)
    
    def byte_convert_txt(self, file_byte, is_save=False):
        file_name = file_byte.filename
        # print(file_name)
        ext = os.path.splitext(file_name)[-1].replace(".","")

        request_json = {
            "images": [{"format": ext, "name": file_name}],
            "requestId": str(uuid.uuid4()),
            "version": "V2",
            "timestamp": int(round(time.time() * 1000)),
        }

        payload = {"message": json.dumps(request_json).encode("UTF-8")}
        files = [("file", file_byte.stream.read())]
        headers = {"X-OCR-SECRET": self.secret_key}

        response = requests.request("POST", self.api_url, headers=headers, data=payload, files=files)

        json_file = os.path.join("results",file_name.replace(ext, "json"))
        if is_save:
            with open(json_file, "w") as jf:
                json.dump(response.json(), jf)

            with open(json_file, "r") as jf:
                js = json.load(jf)
        else:
            js = response.json()
        # print(js)
        text = []
        for image in js['images']:
            for filed in image['fields']:
                text.append(filed['inferText'])
        
        txt_file = os.path.join("results", file_name.replace(ext, "txt"))
        if is_save:
            with open(txt_file, 'w') as txt:
                txt.write(" ".join(text))
        return " ".join(text)

if __name__ == "__main__":
    ocr = FILE_OCR()
    ocr.convert_txt('results/ocr_test.png',True)

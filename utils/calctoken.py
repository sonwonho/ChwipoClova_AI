import http.client
import json


class TokenCalculator:
    def __init__(self):
        self._host, self._api_key, self._api_key_primary_val = self._get_config()
        self._request_id = "Count-Token"

    def _get_config(self):
        with open("config.json", "r") as cf:
            config = json.load(cf)
        return config["TOKENCALCULATOR"]["HOST"], config["TOKENCALCULATOR"]["API_KEY"], config["TOKENCALCULATOR"]["API_KEY_PRIMARY_VAL"]
 

    def _send_request(self, text):
        completion_request = json.loads('''{"messages" : [ {
                                    "role" : "user",
                                    "content" : "text"
                                }]
                                }'''.replace('text', text), strict=False)
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request('POST', '/testapp/v1/api-tools/chat-tokenize/HCX-002/ae49c6f8f0884c4ba183a45f2d5ac526', json.dumps(completion_request), headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding='utf-8'))
        conn.close()
        return result

    def calculate(self, text):
        res = self._send_request(text)
        if res['status']['code'] == '20000':
            return int(res['result']['messages'][0]['count'])
        else:
            return 'Error'


if __name__ == '__main__':
    tc = TokenCalculator()
    print(tc.calculate('test'))

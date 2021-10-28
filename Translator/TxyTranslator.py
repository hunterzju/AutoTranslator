import sys
import os
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(ROOT_PATH)
import json

SIGNKEY = None
with open(os.path.join(ROOT_PATH, "Translator/TxyConfig.json")) as config:
    SIGNKEY = json.load(config)

from time import sleep
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.tmt.v20180321 import tmt_client, models


class TencentTranslate():

    '''
    description: 
    param {*} self
    param {*} t - text to be translated
    param {*} target - target language.
    return {*} result json object
    '''
    def translate(self, text, target="zh"):
        try:
            cred = credential.Credential(SIGNKEY["SecretId"], SIGNKEY["SecretKey"])
            httpProfile = HttpProfile()
            httpProfile.endpoint = "tmt.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = tmt_client.TmtClient(cred, "ap-guangzhou", clientProfile)

            req = models.TextTranslateRequest()
            params = {
                "Source": "auto",
                "Target": target,
                "ProjectId": 0,
                "SourceText": text
            }
            req.from_json_string(json.dumps(params))

            resp = client.TextTranslate(req)
            res = json.loads(resp.to_json_string())
            # {'Source': 'en', 'Target': 'zh', 'TargetText': '你好，世界', 'RequestId': 'cffea870-eb76-4742-901d-36da27550300'}
            return res["TargetText"]

        except TencentCloudSDKException as err:
            print(err)

if __name__ == '__main__':
    res = TencentTranslate().translate("hello world", target="zh")
    print(res)
    # test()

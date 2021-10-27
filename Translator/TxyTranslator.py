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
    翻译接口，输入为待翻译句子的列表
    '''
    def translate(self, t):
        try:
            cred = credential.Credential(SIGNKEY["SecretId"], SIGNKEY["SecretKey"])
            httpProfile = HttpProfile()
            httpProfile.endpoint = "tmt.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = tmt_client.TmtClient(cred, "ap-guangzhou", clientProfile)

            req = models.TextTranslateBatchRequest()
            params = {
                "Source": "auto",
                "Target": "zh",
                "ProjectId": 0,
                "SourceTextList": t
            }
            req.from_json_string(json.dumps(params))

            resp = client.TextTranslateBatch(req)
            return json.loads(resp.to_json_string())

        except TencentCloudSDKException as err:
            print(err)

    '''
    程序主入口
    '''
    def main(self, path):
        content = open(path, 'r', encoding='utf-8').readlines()  # 将待翻译字幕文件按行读取成列表
        # python2 content = open(path, 'r').readlines()
        head, context = content[:5], content[5:]  # 切割头部不需要翻译的内容和正文 根据自己需求修改头部行数
        new_context = context[:]  # 复制一份准备用来替换翻译内容的正文部分

        wait_for_translate = []  # 声明一个放置待翻译文本的列表
        for c in range(0, len(context), 4): # 将每行的内容加入待翻译列表中，并去掉换行符，4是间隔
            wait_for_translate.append(context[c].replace('\n', ''))
        wail_list = []
        wail_tmp = []
        for l in range(len(wait_for_translate)): # 这一块是将总的文本切分成多个40行的文本，这是因为腾讯云的批量文本翻译接口有限制，不能超出2000个字符，这一块也是根据你的字幕文件来决定的，句子如果较长的话，就把这个数调低点，句子较短，就把这个数调高。
            wail_tmp.append(wait_for_translate[l])
            if len(wail_tmp) == 40 or l == len(wait_for_translate) - 1:
                wail_list.append(wail_tmp)
                wail_tmp = []
        translater = []

        for w in range(len(wail_list)): # 批量进行翻译
            translater.extend(self.translate(wail_list[w])['TargetTextList'])
            sleep(0.21) # 休眠是因为腾讯云接口调用时间限制
        count = 0
        for c in range(0, len(context), 4):
            new_context[c] = translater[count] + '\n' # 替换翻译内容并补上换行符
            count += 1
            if count == len(translater):
                break
        name = path.replace('en', 'zh') #
        with open(name, 'w', encoding='utf-8') as f:
            f.writelines(head + new_context)
        return name


if __name__ == '__main__':
    res = TencentTranslate().translate(["hello world"])
    print(res)
    # test()

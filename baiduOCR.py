import requests
import base64

'''
百度OCR通用文字识别
'''

API_key="NqjM6b8NErNxDG1u92wbblY7"
Secret_key="LyH3ckAG66g5zHx3VGTNshjlsN8xFvGe"

def get_token(api_key, secret_key):
    """
    获取百度OCR token
        :param api_key: api_key
        :param secret_key: secret_key
    """
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={key}&client_secret={secret}'.format(key=api_key,secret=secret_key)
    response = requests.get(host)
    if response:
        return response.json()['access_token']
    else:
        raise Exception("获取access_token出错，请检查API_key，secret_key")

def text_rec(imgpath):
    """
    图片文字识别
        :param imgpath: 图片路径
    """
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    f = open(imgpath, 'rb')
    img = base64.b64encode(f.read())
    params = {"image":img}
    access_token = get_token(API_key,Secret_key)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        result=[]
        for item in response.json()['words_result']:
            result.append(item['words'])
        return result
    else:
        raise Exception("请求错误")


if __name__ == "__main__":
    a=text_rec("MuMu.png")
    print(a)
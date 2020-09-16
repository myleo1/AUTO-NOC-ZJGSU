import json
import uuid
import re
import requests

data = {
    'currentResd': '',
    'fromHbToZjDate': '',
    'fromHbToZj': 'C',
    'fromWtToHzDate': '',
    'fromWtToHz': 'B',
    'meetDate': '',
    'meetCase': 'C',
    'travelDate': '',
    'travelCase': 'D',
    'medObsvReason': '',
    'medObsv': 'B',
    'belowCaseDesc': '',
    'belowCase': 'D',
    'temperature': '',
    'notApplyReason': '',
    'hzQRCode': 'A',
    'specialDesc': ''}

with open('user.json', encoding='utf-8') as f:
    users = json.load(f)

for user in users:
    ui = uuid.uuid1()
    data['uuid'] = str(ui)
    data['currentResd'] = user['home']
    header = {'User-Agent': user['userAgent']}
    getCookieData = {
        'name': user['name'],
        'psswd': user['psswd']
    }
    res = requests.post('https://nco.zjgsu.edu.cn/login', data=getCookieData, headers=header)
    cookieValue = ''
    for item in res.cookies:
        cookieValue += item.name + '=' + item.value + ';'
    cookieValue += ' _ncov_uuid=' + str(ui) + '; _ncov_username=' + user['name'] + '; _ncov_psswd=' + user['psswd']
    header = {'User-Agent': user['userAgent'],
              'Cookie': cookieValue}
    res = requests.post('https://nco.zjgsu.edu.cn/', data=data, headers=header)
    if re.search('报送成功', str(res.content, encoding='utf-8')) is not None:
        requests.post('https://sc.ftqq.com/' + user['wechatPushKey'] + '.send',
                      data={"text": "打卡成功+" + user['name'] + user['trueName']})
    else:
        requests.post('https://sc.ftqq.com/' + user['wechatPushKey'] + '.send',
                      data={"text": "打卡失败+" + user['name'] + user['trueName']})

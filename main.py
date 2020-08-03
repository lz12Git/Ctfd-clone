# encoding: UTF-8
'''
Created on 2020年3月31日

@author: lz12xss
'''

import requests
import json
import os

sessionid='5fc92a9a-64a6-41cf-944d-b665d880393b.KX9qO9N18OHCcQqgheagiM2UIL8'
csrftoken='89bd0748562b47da586a99221e0eb67d6e74f1b4c7ebccdba10143b78bbf0ca8'

cookie = {
    'session':sessionid
}
header = {
    'CSRF-Token':csrftoken,
}

base_path = r'D:\ctfd'


def get_challenge(id,collection):
    session = requests.Session()
    url = '172.30.1.178:14000/api/v1/challenges/'+str(id)
    json_str = session.get(url, cookies=cookie,headers=header).text
    json_body = json.loads(json_str)
    category = json_body['data']['category']
    name = json_body['data']['name']
    description = json_body['data']['description']
    value = json_body['data']['value']
    file_list = json_body['data']['files']
    tag_list = json_body['data']['tags']
    directory = base_path+'\\'+collection+'\\'+category+'\\'+str(id)+'_'+name
    try:
        os.makedirs(directory, exist_ok=True)
    except:
        directory = base_path+'\\'+collection+'\\'+category+'\\'+str(id)+'_'
        os.makedirs(directory, exist_ok=True)
    f = open(directory+'\\info.txt',mode='w',encoding='utf8')
    print('id=>'+str(id),file=f)
    print('名称=>'+name,file=f)
    print('赛事=>'+collection,file=f)
    print('分类=>'+category,file=f)
    print('分值=>'+str(value),file=f)
    print('标签=>',end='',file=f)
    print('、'.join(tag_list),file=f)
    print('题目描述=>',file=f)
    print(description,file=f)
    f.close()
    for file in file_list:
        file_short = file[file.rindex('/')+1:file.rindex('?')]
        download_file('http://172.30.1.178:14000'+file,directory+'\\'+str(id)+'_'+file_short)


def download_file(url,save_path):
    session = requests.Session()    
    f=open(save_path,mode='wb')
    for chunk in session.get(url, cookies=cookie).iter_content(100000):
        f.write(chunk)
    f.close()

session = requests.Session()
url = '172.30.1.178:14000/api/v1/challenges/collections'
json_str = session.get(url, cookies=cookie).text
json_body = json.loads(json_str)
for collection in json_body['data']:
    print(collection['name'])
    url2 = '172.30.1.178:14000/api/v1/challenges?collection=' + collection['name']
    json_str2 = session.get(url2, cookies=cookie).text
    json_body2 = json.loads(json_str2)
    for challenge in json_body2['data']:
        print('processing NO.'+str(challenge['id']))
        get_challenge(challenge['id'],collection['name'])
        print('finish NO.' + str(challenge['id']))

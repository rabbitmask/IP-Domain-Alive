# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
'''
 ____       _     _     _ _   __  __           _    
|  _ \ __ _| |__ | |__ (_) |_|  \/  | __ _ ___| | __
| |_) / _` | '_ \| '_ \| | __| |\/| |/ _` / __| |/ /
|  _ < (_| | |_) | |_) | | |_| |  | | (_| \__ \   < 
|_| \_\__,_|_.__/|_.__/|_|\__|_|  |_|\__,_|___/_|\_\

'''
import requests
import re
from multiprocessing import Pool, Manager

headers = {'user-agent': 'ceshi/0.0.1'}
# 信息爬取模块
def getInfo(ip):
    r = requests.get('http://api.webscan.cc/?action=query&ip=' +str(ip),headers=headers)
    ru = re.compile(r'{"domain":"http:\\/\\/(.*?)","title":".*?"}')
    res = ru.findall(r.text)
    return res

#存活判断模块
def islive(ur,q):
    url='http://' + str(ur)
    r = requests.get(url, headers=headers)
    q.put(ur)
    print(ur,r.status_code)

# 进程池管理模块
def poolmana(target_ip):
    p = Pool(50)
    q = Manager().Queue()
    res = getInfo(target_ip)
    print('请耐心等待>>>>>>>\n具体速度与您的网络质量和目标旁站数量有关')
    for i in range(len(res)):
        p.apply_async(islive, args=(res[i],q))

    p.close()
    p.join()
    print('本次检索完成>>>>>\n')

def main():
    print('\t【欢迎来到IP反查系统】\n脚本特色：IP反查、多线程、判断存活\n输入exit退出')
    while True:
        target_ip = input('请输入目标IP：')
        if target_ip == 'exit':
            break
        print('任务读取成功>>>>>\n本次目标IP：{}'.format(target_ip))
        res = getInfo(target_ip)
        print('本次目标IP旁站如下：\n')
        for i in range(len(res)):
            print(res[i])
        goon=input('是否继续进行存活性检测？ (Y/N) or 默认继续\n')
        if goon == 'exit':
            break
        if goon =='N'or goon =='n':
            break
        else:
            try:
                poolmana(target_ip)
            except:
                print('您输入的格式有误！')


if "__main__" == __name__:
    main()

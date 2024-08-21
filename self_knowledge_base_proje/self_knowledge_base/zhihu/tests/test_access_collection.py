# Author: ray
# Date: 8/21/24
# Description:

# 本文仅供学习交流使用

# 导入库操作
import requests  # 用于发起请求和接收数据
import random
import time  # 可以对时间进行一些操作
# 从库中导入模块
from bs4 import BeautifulSoup  # 用于解析HTML文件，从中获取有用的信息
import os.path  # 可以对目录的路径进行操作
from fake_useragent import \
    UserAgent  # 用来随机生成UA，注意：使用该有可能模块会报错；fake-useragent Maximum amount of retries reached，解决方法见：https://www.freesion.com/article/37461287842/

import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':  # 当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行
    # inputUrl = input('请输入您的zhihu_collection的url,如：https://www.zhihu.com/collection/42728421：')
    inputUrl = 'https://www.zhihu.com/collection/695507497'
    ID = inputUrl.split('/')[-1]  # 获取收藏夹ID
    # print(ID)
    zhihu_collection_folder = "zhihu_collection"
    zhihu_video_collection_folder = "zhihu_video_collection"

    current_path = os.getcwd()  # 获取当前路径
    logging.debug(f"current path is {current_path}")
    collection_path = os.path.join(current_path, zhihu_collection_folder)
    collection_video_path = os.path.join(current_path, zhihu_video_collection_folder)
    if os.path.exists(collection_path):  # 检查是否路径中存在zhihu_collection这个目录
        # logging.debug(f"folder exists : {current_path + '\zhihu_collection'}")
        pass
    else:
        os.mkdir(collection_path)  # 不存在则创建一个

    if os.path.exists(collection_video_path):  # 检查是否路径中存在zhihu_video_collection这个目录
        pass
    else:
        os.mkdir(collection_video_path)  # 不存在则创建一个
    # print(current_path)
    logging.debug(f"finished directory establishment")

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'

    }
    # User-Agent 作用：告诉目标服务器，客户端使用的操作系统、浏览器版本和名称
    hostUrl = f'https://www.zhihu.com/api/v4/collections/{ID}/items?offset=0&limit=1'

    hostPage_data = requests.get(url=hostUrl, headers=headers)  # 向hostUrl发起请求
    hostPage_data.close()
    hostPage_data.encoding = 'utf-8'  # 将编码格式hostPage_data设置为'utf-8'
    host_pagejson = hostPage_data.json()  # 将hostPage_data转化为一个json对象
    ansTotals = host_pagejson["paging"]["totals"]  # 获取收藏夹当中有多少个内容

    falseList = []  # 创建一个列表，假如有请求失败的，将会记录在这个列表中。
    # for循环，除了for循环还有while循环
    for i in range(ansTotals):  # 这里是一个for循环，range(a,b)就是从a循环到b-1,这里循环的次数是收藏夹里面收藏数量
        randomHeaders = {'User-Agent': str(UserAgent().random)}
        params = {'offset': f'{i}', 'limit': '1'}  # 这是一些参数，从在网页中打开开发者模式里面可以找到
        # zhihu_collection不能是隐藏状态
        url = f'https://www.zhihu.com/api/v4/collections/{ID}/items'  # 目标url
        # print(url)
        proxies = [{'HTTP': '111.177.192.187:3256'}, {'HTTP': '42.57.149.71:9999'}, {'HTTP': '182.87.130.12:9999'},
                   {'HTTP': '180.119.93.8:9999'}, {'HTTP': '223.243.172.199:9999'}, {'HTTP': '111.79.186.113:9999'},
                   {'HTTP': '223.242.108.231:9999'}, {'HTTP': '223.243.173.188:9999'}, {'HTTP': '112.91.78.137:9999'},
                   {'HTTP': '121.233.206.81:9999'},
                   {'HTTP': '182.34.34.85:9999'},
                   {'HTTP': '113.121.38.196:9999'},
                   {'HTTP': '112.91.75.97:9999'},
                   {'HTTP': '175.42.68.172:9999'},
                   {'HTTP': '223.243.245.35:9999'}]  # 代理IP列表
        proxy = random.choice(proxies)  # 随机选一个代理IP
        page_data = requests.get(url=url, params=params, headers=randomHeaders, proxies=proxy)  # 向目标服务器发送请求
        page_data.close()  # 关闭请求
        page_data.encoding = 'utf-8'  # page_data的编码格式是设置为'utf-8'
        page_json = page_data.json()  # 将page_data这个变量转变为json格式，并且赋值给page_json的变量
        # print(page_json)
        page_title = ''
        page_content = ''
        videoUrl = ''
        # print('0')
        try:
            try:  # 先执行try当中的代码块,如果报错就执行except的代码 ，现在try当中的代码块是对网页的HTML文件进行解析
                page_content = page_json['data'][0]['content']['content']
                # print('1')
                # print(page_content)
                page_title = page_json['data'][0]['content']['title']
                if bool(page_title) == True:  # if elif 这里是做一个分支，bool()这里是对变量page_title做布尔判断
                    pass  # pass的作用是占位，不起任何作用
                elif bool(page_title) == False:
                    # print('2')
                    page_content = page_json['data'][0]['content']['content']
                    # print(page_content)
                    page_title = page_json['data'][0]['content']['question']['title']
            except:

                videoUrl = page_json['data'][0]['content']['video']['playlist']['hd']['play_url']
                # print(videoUrl)
                page_title = page_json['data'][0]['content']['title']
                # print(page_title)

                video = requests.get(url=videoUrl, headers=headers, proxies=proxy)
                # print(video)
                resHeaders = video.headers
                Video_Content_Type = resHeaders['Content-Type']
                # print(Video_Content_Type)
                if Video_Content_Type == 'video/x-ms-wmv':
                    Video_Content_Type = 'wmv'
                elif Video_Content_Type == 'video/avi':
                    Video_Content_Type = 'avi'
                elif Video_Content_Type == 'video/mp4':
                    Video_Content_Type = 'mp4'
                elif Video_Content_Type == 'video/x-flv':
                    Video_Content_Type = 'flv'
                # print(Video_Content_Type)
                videoContent = video.content
                tszf = '\/:*?"<>|？'  # 这个字符串当中的字符是文件名当中不能出现的字符
                for k in tszf:  # 写一个循环来判断要起的文件名当中是否存在a字符串当中的字符
                    if k in page_title:  # if else   如果if中的条件成立，就执行if下的代码块，否则就执行else下面的代码块
                        page_title = page_title.replace(k, '')  # 替换掉特殊字符\/:*?"<>|
                    else:
                        pass

                with open(f'{current_path}\zhihu_video_collection\{page_title}.{Video_Content_Type}', 'wb') as videofp:
                    videofp.write(videoContent)
                    videofp.close()
                    print(f'{page_title}.mp4    下载完成！')
                continue

                # page_content = f'<video src={current_path}/zhihu_collection/{page_title}.{Video_Content_Type} ></video>' # 这里要写好
        except:
            falseList.append(i + 1)  # 将i+1写入改列表falseList中，append()可以将某个变量写入一个列表中
            continue  # 跳过这一次循环，进行下一次，该次循环中以下代码不再执行,注意continue只能在循环中使用

        a = '\/:*?"<>|？'  # 这个字符串当中的字符是文件名当中不能出现的字符
        for j in a:  # 写一个循环来判断要起的文件名当中是否存在a字符串当中的字符
            if j in page_title:  # if else   如果if中的条件成立，就执行if下的代码块，否则就执行else下面的代码块
                page_title = page_title.replace(j, '')  # 替换掉特殊字符\/:*?"<>|
            else:
                pass
        filename = str(i + 1) + ' ' + page_title  # 文件名为filename，这里是一个字符串拼接操作

        # with open(f'./zhihu_collection/{filename}.json', 'w',encoding='utf-8') as fp:  # 创建一个名字叫i+1的json文件，'w'是代表写入，encoding='utf-8'是指定编码格式，在python中用''包围的数据类型是字符串，f''当中的{}里面的是参数
        #     json.dump(page_json, fp=fp, ensure_ascii=False)  # 将page_json这个变量写入上一行创建的文件中

        page_html = f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{page_title}</title></head><body>{page_content}</body></html>'  # 这里是写一个HTML格式的文件
        # print(type(page_title))
        soup = BeautifulSoup(page_html, 'lxml')  # 实例化一个BeautifulSoup对象
        with open(f'./zhihu_collection/{filename}.html', 'w',
                  encoding='utf-8') as htmlfp:  # 创建一个名称为filename的html文件，起个别名为htmlfp
            htmlfp.write(page_html)  # 将page_html写入htmlfp中

        imgs = soup.find_all('img')  # 找出soup当中所有的img标签，没记错的话返回的是个列表

        picUrls = []  # 创建一个空列表，用来装回答中所有的图片的URL
        for imgNum in imgs:
            urlInimg = imgNum['src']  # 提取出img标签中的URL
            picUrls.append(urlInimg)  # 添加到picUrls这个列表中
            # print(a)

        if os.path.exists(current_path + f'\\zhihu_collection\\{filename}') == True:  # 检查是否路径中存在filename这个目录
            pass
        else:
            os.mkdir(current_path + f'\\zhihu_collection\\{filename}')  # 不存在则创建一个文件夹来装图片

        b = 1
        for num in range(len(picUrls)):

            response = requests.get(url=picUrls[num], headers=headers)  # 向图片的URL发起请求
            rescontent = response.content  # 转化为二进制数据
            resHeaders = response.headers  # 获取响应头信息
            # print(resHeaders)
            Content_Type = resHeaders['Content-Type']  # 从响应头信息中获取内容的文件类型
            # print(Content_Type)
            fileType = ''
            if Content_Type == 'image/jpeg':  # 这里是对文件类型的判断
                fileType = 'jpeg'
                # print(fileType)
            elif Content_Type == 'image/svg+xml':
                fileType = 'svg'
                # print(fileType)
            elif Content_Type == 'image/gif':
                fileType = 'gif'
                # print(fileType)
            elif Content_Type == 'application/octet-stream':
                listpicUrl = list(picUrls[num])  # 也可以用split(),来操作
                listpicUrl.reverse()
                point = listpicUrl.index('.')
                listFileType = listpicUrl[0:point]
                listFileType.reverse()
                fileTypestr = ''.join(listFileType)
                if 'jpg' in fileTypestr:
                    fileType = 'jpg'
                elif 'jpeg' in fileTypestr:
                    fileType = 'jpeg'
                elif 'gif' in fileTypestr:
                    fileType = 'gif'

                # print(fileType)

            with open(f'{current_path}\\zhihu_collection\\{filename}\\{b}.{fileType}', 'wb') as fp:  # 创建一个图像文件
                fp.write(rescontent)  # 将rescontent写入文件中

            img = soup.find('img', src=picUrls[num])  # 定位到src=picUrls[num] 的img标签
            # print(type(img))
            img['src'] = f'{current_path}\\zhihu_collection\\{filename}\\{b}.{fileType}'  # 将该img标签的src改为本地链接

            change_content = str(soup).encode(encoding='utf-8')  # 将soup转变为字符串格式
            change_html = open(f'./zhihu_collection/{filename}.html', "w+b")  # 打开filename.html
            change_html.write(change_content)  # 写入数据
            change_html.close()  # 关闭文件
            # print(type(picUrls[num]))
            b = b + 1
            # time.sleep(2)

        print(f'{filename}    下载完成！')  # 显示某某知乎回答下载完成
        time.sleep(2)  # 暂停两秒，不要对对方服务器进行太过频繁的请求
        # print(page_text)

with open('失败列表.txt', 'w', encoding='utf-8') as falseFile:
    falseFile.write(str(falseList))
print('失败的请求列表：', falseList)  # 最后显示保存失败的列表

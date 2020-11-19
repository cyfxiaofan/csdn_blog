from django.test import TestCase
import requests
import json
import re
from lxml import etree
from bs4 import BeautifulSoup
from . import models


def get_url(url):
	start_url = "https://www.csdn.net/api/articles?type=more&category={}&shown_offset=0".format(url)
	return start_url


def get_url_list(start_url):
	headers = {
		"cookie": "uuid_tt_dd=10_20709431570-1576220440157-977344; dc_session_id=10_1576220440157.219554; __yadk_uid=i8n3wpwYNWSzGaymPil1bhYUcwFRDbxM; __gads=ID=b72632da49981c25:T=1580725736:S=ALNI_MYRxl2UYdDQS38o88sGOFnMJv8_cQ; searchHistoryArray=%255B%2522%25E6%2596%2597%25E6%25B3%2595%25E5%25A4%25A7%25E8%25B5%259B%25E7%259A%2584%2522%255D; UserName=qq_41141246; UserInfo=def32eb089cd4d09bf17dee0f7914fbb; UserToken=def32eb089cd4d09bf17dee0f7914fbb; UserNick=%E7%B4%AB%E4%B8%80%E4%B8%80; AU=E6B; UN=qq_41141246; BT=1581330403212; p_uid=U000000; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_20709431570-1576220440157-977344!5744*1*qq_41141246; hasSub=true; announcement=%257B%2522isLogin%2522%253Atrue%252C%2522announcementUrl%2522%253A%2522https%253A%252F%252Fblog.csdn.net%252Fblogdevteam%252Farticle%252Fdetails%252F103603408%2522%252C%2522announcementCount%2522%253A0%252C%2522announcementExpire%2522%253A3600000%257D; utm_source=distribute.pc_relevant.none-task; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1583498788,1583567611,1583568224,1583568250; TY_SESSION_ID=bd8a6155-035b-4182-8403-ae546b6aa1d2; c_ref=https%3A//blog.csdn.net/u011692780/article/details/81158899; dc_tos=q6tdqh; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1583569098",
		"referer": "https://www.csdn.net/nav/python",
		"sec-fetch-mode": "cors",
		"sec-fetch-site": "same-origin",
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
		"x-tingyun-id": "im-pGljNfnc;r=569107622",
	}
	response = requests.get(start_url,headers=headers)
	response = response.text.encode('utf-8').decode('unicode_escape').replace('\\','')
	url_list = re.findall('"url":"(.*?)",',response)
	return url_list

def get_title(url):
	# for i,url in enumerate(all_url_list):
	# 	print('正在从'+url+'请求第'+str(i+1)+'条博客····')
	# url = "https://blog.csdn.net/sbshl/article/details/104576021"
	response = requests.get(url).text
	response_ele = etree.HTML(response)
	soup = BeautifulSoup(response,'lxml')
	#博客标题
	title = re.findall('<h1 class="title-article">(.*?)</h1>',response)[0]
	#文章作者
	wzzz = re.findall('rel="noopener">(.*?)</a>',response)[0]
	#发布时间
	fbsj = re.findall('<span class="time">最后发布于(.*?)</span>',response)[0]
	#阅读数
	yds = re.findall('<span class="read-count">阅读数 (.*?)</span>',response)[0]
	#博客分类
	try:
		bkfl = response_ele.xpath('//*[@id="mainBox"]/main/div[1]/div/div/div[2]/div[3]/div[1]/a/text()')[0].strip()
	except:
		bkfl = '其他'
	#博客内容
	# bknr = response_ele.xpath('//*[@id="content_views"]/text()')[0]
	# bknr = re.findall('<div class="htmledit_views" id="content_views">(.*?)</div>',response)
	bknr = str(soup.select('div#content_views')[0])[68:][:-7]
	# print(response)
	print('原文链接：'+url)
	print('标题: '+title)
	print('文章作者: '+wzzz)
	print('发布时间: '+fbsj)
	print('阅读数: '+yds)
	print('博客分类: '+bkfl)
	print('博客内容: '+bknr)
	print('**************************************************************************************************')
	blog_obj = models.Blog(
		title = title,
		label='Java',
		ginfo=bknr,
		bgcate=models.Blogcates.objects.get(id=5),
		uid=models.Users.objects.get(userid=1),
		zlid=models.Zhuanlan.objects.get(id=14),
		ifcomment=0,
		yuanchuang=1,
		beforeurl=url,
		source=wzzz,
	)
	blog_obj.save()


if __name__ == '__main__':
	# 关键字
	code = 'java'
	# 页数
	n = 1
	start_url = get_url(code)
	all_url_list=[]
	for _ in range(n):
		all_url_list.extend(get_url_list(start_url))
	print('一共爬取了'+str(len(all_url_list))+'条有关'+code+'的博客')
	print('去重之后剩余'+str(len(set(all_url_list)))+'条博客')
	finally_url_list = list(set(all_url_list))
	for url in finally_url_list:
		get_title(url)

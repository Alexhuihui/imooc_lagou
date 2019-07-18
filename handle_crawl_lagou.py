# -*- coding:utf-8 -*-
import re
import time
import json
import multiprocessing

__author__ = 'alex'

import requests


class HandleLaGou:
	def __init__(self):
		self.lagou_session = requests.session()
		self.header = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
		}
		self.city_list = ''
	
	# 获取全国所有城市列表的方法
	def handle_city(self):
		city_search = re.compile(r'zhaopin/">(.*?)</a>')
		city_url = 'https://www.lagou.com/jobs/allCity.html'
		city_result = self.handle_request(method='GET', url=city_url)
		self.city_list = city_search.findall(city_result)
		self.lagou_session.cookies.clear()
		
	def handle_city_job(self, city):
		first_request_url = "https://www.lagou.com/jobs/list_python?&px=default&city=%s" % city
		first_response = self.handle_request(method='GET', url=first_request_url)
		total_page_search = re.compile(r'class="span\stotalNum">(\d+)</span>')
		try:
			total_page = total_page_search.search(first_response).group(1)
		except:
			return
		for i in range(1, int(total_page) + 1):
			data = {
				"pn": i,
				"kd": "python"
			}
			page_url = "https://www.lagou.com/jobs/positionAjax.json?px=default&city=%s&needAddtionalResult=false" % city
			referer_url = "https://www.lagou.com/jobs/list_python?px=default&city=%s" % city
			self.header['Referer'] = referer_url.encode()
			response = self.handle_request(url=page_url, method='POST', data=data, info=city)
			
			lagou_data = json.loads(response)
			job_list = lagou_data['content']['positionResult']['result']
			for job in job_list:
				print(job)
	
	def handle_request(self, method, url, data=None, info=None):
		while True:
			if method == "GET":
				response = self.lagou_session.get(url=url, headers=self.header)
			elif method == "POST":
				response = self.lagou_session.post(url=url, headers=self.header, data=data)
			response.encoding = 'utf-8'
			if '频繁' in response.text:
				self.lagou_session.cookies.clear()
				first_request_url = "https://www.lagou.com/jobs/list_python?&px=default&city=%s" % info
				self.handle_request(method='GET', url=first_request_url)
				time.sleep(10)
				continue
			return response.text
	
	def get_proxy(self):
		return requests.get("http://120.79.226.196:5010/get/").content
	
	def delete_proxy(self, proxy):
		requests.get("http://120.79.226.196:5010/delete/?proxy={}".format(proxy))


if __name__ == '__main__':
	lagou = HandleLaGou()
	lagou.handle_city()
	pool = multiprocessing.Pool(2)
	for city in lagou.city_list:
		pool.apply_async(lagou.handle_city_job, args=(city,))
	pool.close()
	pool.join()

# -*- coding:utf-8 -*-
import re

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
		print(self.city_list)
	
	def handle_request(self, method, url, data=None, info=None):
		if method == "GET":
			response = self.lagou_session.get(url=url, headers=self.header)
		return response.text


if __name__ == '__main__':
	lagou = HandleLaGou()
	lagou.handle_city()

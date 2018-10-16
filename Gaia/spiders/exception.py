# # -*- coding: utf-8 -*-

class ParseNotSupportedError(Exception):
	def __init__(self, url):
		self.url = url

	def __str__(self):
		return 'url{} is could not be parsed '.format(self.url)
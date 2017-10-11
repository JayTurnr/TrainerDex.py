﻿# coding=utf-8
import requests

api_url = 'http://www.ekpogo.uk/api/trainer/'

def request_status(r, detailed=False):
	"""Returns a formatted string about the status, useful for logging.
	
	args:
	r - takes requests.models.Response
	"""
	
	base_string = "HTTP {r.request.method} {r.request.url}: {r.status_code}"
	
	if r.status_code in range(200,99):
		string = base_string
		if detailed is True:
			string += " - {r.json()}"
		else:
			string += " - 👍"
		return string.format(r=r)
	elif r.status_code==requests.codes.teapot:
		string = base_string
		if detailed is True:
			string += "{r.json()}"
		else:
			string += " I'm a little teapot, short and stout. Here is my handle, here is my spout. When I get all steamed up, hear me shout! Just tip me over and pour me out."
		return string.format(r=r)
	else:
		string = base_string
		return string.format(r=r)
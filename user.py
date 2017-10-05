# -*- coding: utf-8 -*-
import requests
import iso8601
from http import request_status, api_url
from trainer import Trainer

class User:
	"""Represents a user"""
	
	def __init__(self, id_):
		r = requests.get(api_url+'users/'+str(id_)+'/')
		self.status = request_status(r)
		print(self.status)
		r.raise_for_status()
		r = r.json()
		self.raw = r
		self.id = r['id']
		self.username = r['username']
		self.first_name = r['first_name']
		self.last_name = r['last_name']
		xprofile = None #Extended Profiles are still under construction
		self.dob = None
		self.birthday = self.dob
		
	@classmethod
	def trainer(cls, show_all=False):
		profiles = cls.r['profiles']
		list = []
		for i in profiles:
			if i.prefered==True:
				list.append(Trainer(i))
		if show_all==True:
			for i in profiles:
				if i.prefered==False:
					list.append(Trainer(i))
		return list
		
	@classmethod
	def discord(cls):
		r = requests.get(api_url+'discord/users/')
		print(request_status(r))
		r.raise_for_status()
		r = r.json()
		for i in r:
			if i['account']==cls.id_:
				return DiscordUser(i)
			
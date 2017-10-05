# -*- coding: utf-8 -*-
import requests
import iso8601
from utils import Level
from http import request_status, api_url
from update import Update
from user import User

class Trainer:
	"""Get information about a trainer"""
	
	def __init__(self, id_: int, force=False):
		r = requests.get(api_url+'trainers/'+str(id_)+'/')
		self.status = request_status(r)
		print(self.status)
		r.raise_for_status()
		r = r.json()
		self.raw = r
		self.id = r['id']
		self.username = r['username']
		self.cheater = r['currently_cheats']
		self.team = r['faction']
		self.has_cheated = r['has_cheated']
		self.last_cheated = r['last_cheated']
		self.start_date = r['start_date']
		self.goal_daily = r['daily_goal']
		self.goal_total = r['total_goal']
		self.prefered = r['prefered']
		self.account = Trainer(int(r['account']))
		update = r['update']
		self.update = Update(update['id'])
		self.statistics = r['statistics']
		if self.statistics is False:
			self.account = None
			self.prefered = None
			if force is False:
				self.start_date = None
				self.goal_daily = None
				self.goal_total = None
				self.update = None
		
	def __str__(self):
		return "Username: {0.username}, Level: {1}".format(self, Level().from_xp(self.update.xp).level)
		
	@classmethod
	def level(cls):
		return Level().get_by_xp(cls.update['xp'])
		
	@classmethod
	def get_updates(cls):
		"""Get a list of all update objects by trainer"""
		r = requests.get(api_url+'update/')
		print(request_status(r))
		r.raise_for_status()
		r = r.json()
		updates = []
		for update in r:
			if update['trainer']==trainer:
				updates.append(Update(update['id']))
		
		return updates
	
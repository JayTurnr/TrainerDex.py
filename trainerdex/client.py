# -*- coding: utf-8 -*-
import requests
import json
import datetime
import maya
from .utils import Team
from .trainer import Trainer
from .update import Update
from .cached import DiscordUser, DiscordMember, DiscordServer
from .http import request_status, api_url
from .user import User

class Client:
	"""Interact with the TrainerDex API
	
	Supply an api token when calling the class.
	"""
	
	def __init__(self, token=None):
		headers = {'content-type':'application/json'}
		if token!=None:
			headers['authorization'] = 'Token '+token
		self.headers = headers
	
	@classmethod
	def get_trainer_from_username(self, username):
		"""Returns a Trainer object from a Trainers username"""
		r = requests.get(api_url+'trainers/')
		print(request_status(r))
		r = r.json()
		for i in r:
			if i['username'].lower()==username.lower():
				return Trainer(i)
		raise LookupError('Unable to find {} in the database.'.format(username))
	
	@classmethod
	def get_teams(self):
		"""Get a list of teams, mostly unchanging so safe to call on init and keep result"""
		teams = []
		for i in range(0,4): #Hard coded team IDs, will change if teams ever increase in number
			teams.append(Team(i))
		return teams
	
	def create_trainer(self, username, team, has_cheated=False, last_cheated=None, currently_cheats=False, statistics=True, daily_goal=None, total_goal=None, prefered=True, account=None):
		"""Add a trainer to the database"""
		url = api_url+'trainers/'
		payload = {
			'username': username,
			'faction': team,
			'has_cheated': has_cheated,
			'last_cheated': last_cheated,
			'currently_cheats': currently_cheats,
			'statistics': statistics,
			'daily_goal': daily_goal,
			'total_goal': total_goal,
			'prefered': prefered,
			'last_modified': maya.now().iso8601(),
			'account': account
		}
		
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return Trainer(int(r.json()['id']))
		
	def update_trainer(self, trainer, username=None, has_cheated=None, last_cheated=None, currently_cheats=None, statistics=None, daily_goal=None, total_goal=None, prefered=None, account=None):
		"""Update parts of a trainer in a database"""
		args = locals()
		url = api_url+'trainers/'+str(trainer.id)+'/'
		payload = {
			'last_modified': maya.now().iso8601()
		}
		for i in args:
			if args[i] is not None and i not in ['self', 'trainer']:
				payload[i] = args[i]
		r = requests.patch(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return Trainer(int(r.json()['id']))
	
	def create_update(self, trainer, xp):
		"""Add a Update object to the database"""
		url = api_url+'update/'
		payload = {
			'trainer': int(trainer),
			'xp': int(xp),
			'datetime': maya.now().iso8601()
		}
		
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return Update(int(r.json()['id']))
		
	def import_discord_user(self, name, discriminator, id_, avatar_url, creation, user):
		"""Add a discord user"""
		url = api_url+'discord/users/'
		payload = {
			'account': int(user),
			'name': str(name),
			'discriminator': str(discriminator),
			'id': int(id_),
			'avatar_url': str(avatar_url),
			'creation': creation.isoformat()
		}
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return DiscordUser(int(r.json()['id']))
	
	def import_discord_server(self, name, region, id_, owner, icon='https://discordapp.com/assets/2c21aeda16de354ba5334551a883b481.png', bans_cheaters=None, seg_cheaters=None, bans_minors=None, seg_minors=None):
		"""Add a discord server"""
		url = api_url+'discord/servers/'
		payload = {
			'name': str(name),
			'region': str(region),
			'id': int(id_),
			'icon': str(icon),
			'owner': int(owner),
			'bans_cheaters': bans_cheaters,
			'seg_cheaters': seg_cheaters,
			'bans_minors': bans_minors,
			'seg_minors': seg_minors
		}
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return DiscordServer(int(r.json()['id']))
	
	def create_user(self, username, first_name=None, last_name=None):
		"""Create a user"""
		url = api_url+'users/'
		payload = {
			'username':username
		}
		if first_name:
			payload['first_name'] = first_name
		if last_name:
			payload['last_name'] = last_name
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return User(int(r.json()['id']))
	
	def update_user(self, user, username=None, first_name=None, last_name=None):
		"""Update user info"""
		args = locals()
		url = api_url+'users/'+str(user.id)+'/'
		payload = {}
		for i in args:
			if args[i] is not None and i not in ['self', 'user']:
				payload[i] = args[i]
		r = requests.patch(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return User(int(r.json()['id']))
	
	def get_trainer(self, id_, respect_privacy=True):
		"""Returns the Trainer object for the ID"""
		
		r = requests.get(api_url+'trainers/'+str(id_)+'/')
		self.status = request_status(r)
		print(self.status)
		r.raise_for_status()
		return Trainer(r.json(), respect_privacy)
	
	def get_update(self, id_):
		"""Returns the update object for the ID"""
		
		r = requests.get(api_url+'update/'+str(id_)+'/')
		self.status = request_status(r)
		print(self.status)
		r.raise_for_status()
		return Update(r.json())
	
	def get_user(self, id_):
		"""Returns the User object for the ID"""
		
		r = requests.get(api_url+'users/'+str(id_)+'/')
		self.status = request_status(r)
		print(self.status)
		r.raise_for_status()
		return User(r.json())
	
	def get_discord_user(self, id_):
		"""Returns the User object for the ID"""
		
		r = requests.get(api_url+'discord/users/'+str(id_)+'/')
		self.status = request_status(r)
		print(self.status)
		r.raise_for_status()
		return User(r.json())
	
	def get_discord_server(self, id_):
		"""Returns the User object for the ID"""
		
		r = requests.get(api_url+'discord/servers/'+str(id_)+'/')
		self.status = request_status(r)
		print(self.status)
		r.raise_for_status()
		return User(r.json())
	
import json
from Instagram import Instagram
import time
import os

class Graph():
	def __init__(self):
		self.followers = []
		self.zero_target = ""
		self.recursion = False
		self.recursion_flag = True
		self.flag = True
		self.sleep_time = 1 #In minutes
		os.system('clear')
		self.start()

	def recursion_start(self):
		try:
			for follower in self.followers:
				try:
					print("[WAITING]",self.sleep_time,"minutes")
					time.sleep(60*self.sleep_time)
					self.write(follower)
				except: print("[ERROR] next/self.followers/follower")
		except: print("[ERROR] next/self.followers")


	def write(self, target):
		print()
		print('[INFO] Collecting',target )
		try:
			data = {}
			data['info'] = {}
			data['following'] = []
			data['followers'] = []

			try:
				info = Instagram.collect_info(target)
				data['info'] = info
			except: print("[ERROR] write/info")


			if info['is_private']:
				print('[WARNING] Account is private, followers and following cant be saved')
			else:
				try:
					following = Instagram.collect_following(target)
				except:print("[ERROR] write/following")
				try:
					followers = Instagram.collect_followers(target)
				except:print("[ERROR] write/followers")

				if not self.followers:
					for follower in followers:
						try:
							self.followers.append(follower)
						except: print("[ERROR] write/follower")

				for follow in following:
					try:
						data['following'].append(follow)
					except: print("[ERROR] write/follow in following")
				for follower in followers:
					try:
						data['followers'].append(follower)
					except: print ("[ERROR] write/follower in followers")

			try:
				if not os.path.isdir("./Data/"+self.zero_target):
					os.mkdir("./Data/"+self.zero_target)
				with open("./Data/"+self.zero_target+"/"+target+".json", 'w') as file:
					json.dump(data, file, indent=4)
					print("[INFO]",target,"has been saved")
			except: print("[ERROR] write/open file")
			try:
				print("[INFO] Clear data")
				try:
					data['info'].clear()
					data['following'].clear()
					data['followers'].clear()

				except: print("[ERROR] with data clear_1")
				try:
					data['info'] = []
					data['following'] = []
					data['followers'] = []
				except: print("[ERROR] with data clear_2")
			except: print("[ERROR] With clear data")
		except:
			print("[ERROR] write")
			self.next()

	def start(self):
		try:
			self.zero_target = input('Введите аккаунт:')
			flag = True
			while flag:
				question = input('Сохранить только аккаунт или всех подписчиков? (1 or 2): ')
				if question == '1':
					self.recursion = False
					flag = False
				elif question == '2':
					self.recursion = True
					flag = False
				self.write(self.zero_target)
			if self.recursion:
				self.recursion_start()
		except: print("[ERROR] next/zero target")


Graph()

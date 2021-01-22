from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, WebDriverException

import sys
import os
import time
import pickle
import re
import json

class Instagram():
	def __init__(self):
		self.opts = Options()
		self.opts.set_headless()
		assert self.opts.headless
		self.browser = Firefox(options=self.opts)
		self.url = "https://instagram.com"

		self.username = ""
		self.password = ""

		self.collected_info = {}
		self.collected_info['username'] = []
		self.collected_info['biography'] = []
		self.collected_info['external_url'] = []
		self.collected_info['followers'] = []
		self.collected_info['followed'] = []
		self.collected_info['full_name'] = []
		self.collected_info['profile_pic'] = []
		self.collected_info['fbid'] = []
		self.collected_info['is_private'] = []

		self.followers_c = 0
		self.followers_list = []
		self.all_followers = []
		self.followers_count = 0

		self.following_count = 0
		self.following_c = 0
		self.following_list = []
		self.all_following = []

		self.variables = {}
		self.variables["first"] = 50
		self.variables["id"] = 0

		self.graphql_endpoint = "view-source:https://www.instagram.com/graphql/query/"
		self.graphql_followers = (self.graphql_endpoint +"?query_hash=37479f2b8209594dde7facb0d904896a")
		self.graphql_following = (self.graphql_endpoint +"?query_hash=58712303d941c6855d4e888c5f0cd22f")

		self.login()

	def login(self):
		print("[INFO] Autorization")
		self.browser.get(self.url)
		try:
			for cookie in pickle.load(open("Session.pkl", "rb")):
				self.browser.add_cookie(cookie)
			print("[INFO] Session has been restored")
		except:
			print("[WARNING] Session cant be restored")

			self.username = input("Please enter username: ")
			self.password = input("Please enter password: ")

			username = WebDriverWait(self.browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='username']")))
			password =WebDriverWait(self.browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='password']")))
			try:
				try:
					username.clear()
					username.send_keys(self.username)
					print("[INFO]Username successfuly entered")
				except: print("[ERROR] Username error")
				try:
					password.clear()
					password.send_keys(self.password)
					print("[INFO] Password successfuly entered")
				except: print("[ERROR] Password error")
				try:
					Login_button = WebDriverWait(self.browser,2).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[type='submit']"))).click()
					print("[INFO]Successfuly logged in")
				except: print("[ERROR] Login error")
				try:
					not_now =WebDriverWait(self.browser,10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(), 'Not Now')]"))).click()
					print("[INFO] Login info dont saved")
				except: print("[ERROR] Login info popup error")
				try:
					not_now2 = WebDriverWait(self.browser,10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(), 'Not Now')]"))).click()
					print("[INFO] Notifications dont turn on")
				except: print("[ERROR] Notifications popup error")
				try:
					pickle.dump(self.browser.get_cookies(),
					 open("Session.pkl","wb"))
					print("[INFO] Session has been saved")
				except:
					print("[WARNING] Cant save session")
			except NoSuchElementException:
				print("[WARNING] Wrongusername or password")

	def get_id(self):
		try:
			user_id = self.browser.execute_script(
				"return window.__additionalData[Object.keys(window.__additionalData)[0]].data.graphql.user.id")
		except WebDriverException:
			user_id = self.browser.execute_script("return window._sharedData.entry_data.ProfilePage[0].graphql.user.id")
		return user_id

	def progress(self,count, total, status=''):
		bar_len = 60
		filled_len = int(round(bar_len * count / float(total)))

		percents = round(100.0 * count / float(total), 1)
		bar = '=' *filled_len + '-' * (bar_len - filled_len)

		sys.stdout.write('[%s] %s%s Collecting %s\r' % (bar, percents,'%', status))
		sys.stdout.flush()

	def collect_info(self,username):
		print("[INFO] Collecting information")
		try:
			self.browser.get("view-source:https://www.instagram.com/"+username+"/?__a=1")
		except:
			print("[ERROR] Information error with open page")
		try:
			pre = self.browser.find_element_by_tag_name("pre").text
		except:
			print("[ERROR] with Information find element pre")
		try:
			self.data = json.loads(pre)["graphql"]
		except:
			print("[ERROR]",'graphql')
		try:
			biography = self.data["user"]["biography"]
		except:
			print("[ERROR]",'biography')
		try:
			external_url = self.data["user"]["external_url"]
		except:
			print("[ERROR]",'external_url')
		try:
			followers = self.data["user"]["edge_followed_by"]['count']
		except: print("[ERROR]",'followers')
		try:
			followed = self.data["user"]["edge_follow"]['count']
		except: print("[ERROR]",'followed')
		try:
			full_name = self.data["user"]["full_name"]
		except:
			print("[ERROR]",'full name')
		try:
			profile_pic = self.data["user"]["profile_pic_url_hd"]
		except: print("[ERROR]",'profile pic')
		try:
			fbid = self.data["user"]["fbid"]
		except:
			print("[ERROR]",'fbid')
		try:
			is_private = self.data["user"]["is_private"]
		except:
			print("[ERROR]",'is_private')
		try:
			self.collected_info['username']= username
		except:
			print("[ERROR]",'append username')
		try:
			self.collected_info['biography']=biography
		except:
			 print("[ERROR]",'= biography')
		try:
			self.collected_info['external_url']=external_url
		except:
			print("[ERROR]",'= external url')
		try:
			self.collected_info['followers']=followers
		except:
			print("[ERROR]",'= followers')
		try:
			self.collected_info['followed']=followed
		except:
			print("[ERROR]",'= followed')
		try:
			self.collected_info['full_name']=full_name
		except:
			print("[ERROR]",'= full name')
		try:
			self.collected_info['profile_pic']=profile_pic
		except:
			print("[ERROR]",'= profile pic')
		try:
			self.collected_info['fbid']=fbid
		except:
			print("[ERROR]","fbid")
		try:
			self.collected_info['is_private']=is_private
		except:
			print("[ERROR]","append is_private")
		try:
			collected_info = self.collected_info
		except:
			print("[ERROR]",'collected info')
			self.collected_info = []
		# print(collected_info)
		return collected_info

	def next_page_followers(self, id):
		try:
			time.sleep(5)
			pre = self.browser.find_element_by_tag_name("pre").text
			self.data = json.loads(pre)["data"]
			page_info = self.data["user"]["edge_followed_by"]["page_info"]
			self.variables["id"] = id
			self.variables["after"] = page_info["end_cursor"]
			url = "{}&variables={}".format(self.graphql_followers,str(json.dumps(self.variables)) )
			self.browser.get(url)
		except: print('[ERROR] With open next page followers')

	def get_followers(self):
		try:
			pre = self.browser.find_element_by_tag_name("pre").text
			data = json.loads(pre)["data"]
			# print(pre)
			page_info = data["user"]["edge_followed_by"]["page_info"]
			edges = data["user"]["edge_followed_by"]["edges"]
			self.followers_count = data["user"]["edge_followed_by"]["count"]
			all_followers = []
			for user in edges:
				self.followers_c += 1
				all_followers.append(user["node"]["username"])
			return all_followers
		except: print('[ERROR] With get followers')

	def collect_followers(self, username):
		try:
			self.browser.get(self.url + '/' + username)
		except: print("[ERROR] With opening page of",username)
		try:
			followers_list = []
			all_followers = []
			self.variables["id"] = self.get_id()
			self.i = 0
			self.sc_rolled = 0
			self.variables["first"] = 50
		except: print("[ERROR] with set vars of followers")
		print("[INFO] Collecting followers of", username)

		try:
			followers_url = "{}&variables={}".format(self.graphql_followers, str(json.dumps(self.variables)))
			self.browser.get(followers_url)
		except:print("[ERROR] With opening followers page")

		pre = self.browser.find_element_by_tag_name("pre").text
		self.data = json.loads(pre)["data"]
		self.followers_count = self.data["user"]["edge_followed_by"]["count"]
		self.flag = True
		i = 1
		try:
			print("[INFO] Followers count:",self.followers_count)
			while self.flag:
				users = self.get_followers()
				self.next_page = self.data["user"]["edge_followed_by"]["page_info"]["has_next_page"]
				followers_list.append(users)
				self.progress(self.followers_c,self.followers_count, "Followers, page:"+str(i))
				iter = self.followers_count / self.variables["first"]
				if i < iter:
					if self.sc_rolled > 10:
						print("[INFO] Queried too much! ~ sleeping a bit :>")
						time.sleep(60)
						self.sc_rolled = 0
					self.sc_rolled += 1
					i += 1
					self.next_page_followers(self.variables["id"])
				else:
					self.flag = False
		except: print("[ERROR] With np")
		print("[INFO] followerscount:", self.followers_count)
		print("[INFO] followers saved:", self.followers_c)
		if (self.followers_count != self.following_c):
			print("[WARNING] Not all followers has been saved")
		for foll in followers_list:
			for f in foll:
				all_followers.append(f)
		self.followers_c = 0
		return all_followers

	def next_page_following(self, id):
		try:
			time.sleep(5)
			pre =self.browser.find_element_by_tag_name("pre").text
			self.data = json.loads(pre)["data"]
			page_info = self.data["user"]["edge_follow"]["page_info"]
			self.variables["id"] = id
			self.variables["after"] = page_info["end_cursor"]
			url = "{}&variables={}".format(self.graphql_following,str(json.dumps(self.variables)))
			self.browser.get(url)
		except: print('[ERROR] With next page following')

	def get_following(self):
		try:
			pre = self.browser.find_element_by_tag_name("pre").text
			data = json.loads(pre)["data"]
			# print(data)
			page_info = data["user"]["edge_follow"]["page_info"]
			edges = data["user"]["edge_follow"]["edges"]
			self.following_count = data["user"]["edge_follow"]["count"]
			all_following = []
			for user in edges:
				self.following_c += 1
				all_following.append(user["node"]["username"])
			return all_following
		except: print('[ERROR] With get following')

	def collect_following(self, username):
		try:
			self.browser.get(self.url + '/' + username)
		except: print("[ERROR] With opening page of",username)
		try:
			following_list = []
			all_following = []
			self.variables["id"] = self.get_id()
			self.i = 0
			self.sc_rolled = 0
		except: print("[ERROR] With following vars")
		print("[INFO] Collecting following of", username)

		try:
			following_url = "{}&variables={}".format(self.graphql_following, str(json.dumps(self.variables)))
			self.browser.get(following_url)
		except:print("[ERROR] with opening following page")

		pre = self.browser.find_element_by_tag_name("pre").text
		self.data = json.loads(pre)["data"]
		self.following_count = self.data["user"]["edge_follow"]["count"]
		self.flag = True
		i =1
		try:
			print("[INFO] Following by:",self.following_count)
			while self.flag:
				users = self.get_following()
				self.next_page = self.data["user"]["edge_follow"]["page_info"]["has_next_page"]
				following_list.append(users)
				self.progress(self.following_c,self.following_count, "Followings, page:"+str(i))
				iter = self.following_count / self.variables["first"]
				if i < iter:
					if self.sc_rolled > 10:
						print("[INFO] Queried too much! ~ sleeping a bit :>")
						time.sleep(60)
						self.sc_rolled = 0
					self.sc_rolled += 1
					i += 1
					self.next_page_following(self.variables["id"])
				else:
					self.flag = False
		except: print("[ERROR] with np following")
		print("[INFO] following count:", self.following_count)
		print("[INFO] following saved:", self.following_c)
		if (self.following_count != self.following_c):
			print("[WARNING] Not all following has been saved")
		for foll in following_list:
			for f in foll:
				all_following.append(f)
		self.following_c = 0
		return all_following

Instagram = Instagram()

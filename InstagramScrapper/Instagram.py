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
        os.system("clear")
        self.opts = Options()
        self.opts.set_headless()
        assert self.opts.headless
        self.browser = Firefox(options=self.opts)
        self.url = "https://instagram.com"

        self.username = ""
        self.password = ""

        self.collected_info = []

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
        self.graphql_followers = (self.graphql_endpoint + "?query_hash=37479f2b8209594dde7facb0d904896a")
        self.graphql_following = (self.graphql_endpoint + "?query_hash=58712303d941c6855d4e888c5f0cd22f")

        self.login()
        os.system("clear")

    def login(self):
        print("Login")
        self.browser.get(self.url)
        try:
            for cookie in pickle.load(open("Session.pkl", "rb")):
                self.browser.add_cookie(cookie)
            print("Session has been restored")
        except:
            print("Session cant be restored")

            self.username = input("Please enter username: ")
            self.password = input("Please enter password: ")

            username = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
            password = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
            try:
                try:
                    username.clear()
                    username.send_keys(self.username)
                    print("Username successfuly entered")
                except: print("Username error")
                try:
                    password.clear()
                    password.send_keys(self.password)
                    print("Password successfuly entered")
                except: print("Password error")
                try:
                    Login_button = WebDriverWait(self.browser, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
                    print("Successfuly logged in")
                except: print("Login error")
                try:
                    not_now = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
                    print("Login info dont saved")
                except: print("Login info popup error")
                try:
                    not_now2 = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
                    print("Notifications dont turn on")
                except: print("Notifications popup error")
                try:
                    pickle.dump(self.browser.get_cookies(),
                     open("Session.pkl","wb"))
                    print("Session has been saved")
                except: print("Cant save session")
            except NoSuchElementException:
                print("Wrong username or password")

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
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s Collecting %s\r' % (bar, percents, '%', status))
        sys.stdout.flush()

    def collect_info(self,username):
        print("Collecting information")
        try:
            self.browser.get("view-source:https://www.instagram.com/"+username+"/?__a=1")
        except: pass
        try:
            pre = self.browser.find_element_by_tag_name("pre").text
            self.data = json.loads(pre)["graphql"]
            biography = self.data["user"]["biography"]
            external_url = self.data["user"]["external_url"]
            followers = self.data["user"]["edge_followed_by"]['count']
            followed = self.data["user"]["edge_follow"]['count']
            full_name = self.data["user"]["full_name"]
            profile_pic = self.data["user"]["profile_pic_url_hd"]
            fbid = self.data["user"]["fbid"]
            self.progress(0,8)
            self.collected_info.append(username)
            self.progress(1,8)
            self.collected_info.append(biography)
            self.progress(2,8)
            self.collected_info.append(external_url)
            self.progress(3,8)
            self.collected_info.append(followers)
            self.progress(4,8)
            self.collected_info.append(followed)
            self.progress(5,8)
            self.collected_info.append(full_name)
            self.progress(6,8)
            self.collected_info.append(profile_pic)
            self.progress(7,8)
            self.collected_info.append(fbid)
            self.progress(8,8)

        except: pass
        return self.collected_info

    def next_page_followers(self, id):
        try:
            time.sleep(5)
            pre = self.browser.find_element_by_tag_name("pre").text
            self.data = json.loads(pre)["data"]
            page_info = self.data["user"]["edge_followed_by"]["page_info"]
            self.variables["id"] = id
            self.variables["after"] = page_info["end_cursor"]
            self.graphql_endpoint = "view-source:https://www.instagram.com/graphql/query/"
            self.graphql_followers = (self.graphql_endpoint + "?query_hash=37479f2b8209594dde7facb0d904896a")
            url = "{}&variables={}".format(
                self.graphql_followers, str(json.dumps(self.variables))
            )
            self.browser.get(url)
        except: print('error in next page')
    def get_followers(self):
        try:
            pre = self.browser.find_element_by_tag_name("pre").text
            data = json.loads(pre)["data"]
            page_info = data["user"]["edge_followed_by"]["page_info"]
            edges = data["user"]["edge_followed_by"]["edges"]
            self.followers_count = data["user"]["edge_followed_by"]["count"]
            all_followers = []
            for user in edges:
                self.followers_c += 1
                all_followers.append(user["node"]["username"])
            return all_followers
        except: print('error get_followers')
    def collect_followers(self, username):
        try:
            self.browser.get(self.url + '/' + username)
        except: print("Error with opening page of",username)
        try:
            self.variables["id"] = self.get_id()
            self.i = 0
            self.sc_rolled = 0
        except: print("Error with vars")
        print("Collecting followers of", username)


        try:
            followers_url = "{}&variables={}".format(self.graphql_followers, str(json.dumps(self.variables)))
            self.browser.get(followers_url)
        except:print("error with opening")

        pre = self.browser.find_element_by_tag_name("pre").text
        self.data = json.loads(pre)["data"]
        self.followers_count = self.data["user"]["edge_followed_by"]["count"]
        self.flag = True
        try:
            print("Followers:",self.followers_count)
            while self.flag:
                self.i += 1
                self.users = self.get_followers()
                self.next_page = self.data["user"]["edge_followed_by"]["page_info"]["has_next_page"]
                self.followers_list.append(self.users)
                self.progress(self.followers_c,self.followers_count, "Followers")
                if self.next_page:
                    if self.sc_rolled > 10:
                        print("Queried too much! ~ sleeping a bit :>")
                        time.sleep(60)
                        self.sc_rolled = 0
                    self.sc_rolled += 1
                    self.next_page_followers(self.variables["id"])
                else:
                    self.flag = False
        except: print("error with np")
        for foll in self.followers_list:
            for f in foll:
                self.all_followers.append(f)

        return self.all_followers

    def next_page_following(self, id):
        try:
            time.sleep(5)
            pre = self.browser.find_element_by_tag_name("pre").text
            self.data = json.loads(pre)["data"]
            page_info = self.data["user"]["edge_follow"]["page_info"]
            self.variables["id"] = id
            self.variables["after"] = page_info["end_cursor"]
            url = "{}&variables={}".format(
                self.graphql_following, str(json.dumps(self.variables))
            )
            self.browser.get(url)
        except: print('error in next page')
    def get_following(self):
        try:
            pre = self.browser.find_element_by_tag_name("pre").text
            data = json.loads(pre)["data"]
            page_info = data["user"]["edge_follow"]["page_info"]
            edges = data["user"]["edge_follow"]["edges"]
            following_count = data["user"]["edge_follow"]["count"]
            all_following = []
            for user in edges:
                self.following_c += 1
                all_following.append(user["node"]["username"])
            return all_following
        except: print('error get_following')
    def collect_following(self, username):
        try:
            self.browser.get(self.url + '/' + username)
        except: print("Error with opening page of",username)
        try:
            self.variables["id"] = self.get_id()
            self.i = 0
            self.sc_rolled = 0
        except: print("Error with vars")
        print("Collecting following of", username)


        try:
            following_url = "{}&variables={}".format(self.graphql_following, str(json.dumps(self.variables)))
            self.browser.get(following_url)
            print(following_url)
        except:print("error with opening")

        pre = self.browser.find_element_by_tag_name("pre").text
        self.data = json.loads(pre)["data"]
        self.following_count = self.data["user"]["edge_follow"]["count"]
        self.flag = True
        try:
            print("Following by:",self.following_count)
            while self.flag:
                self.i += 1
                self.users = self.get_following()
                self.next_page = self.data["user"]["edge_follow"]["page_info"]["has_next_page"]
                self.following_list.append(self.users)
                self.progress(self.following_c,self.following_count, "Following")
                if self.next_page:
                    if self.sc_rolled > 10:
                        print("Queried too much! ~ sleeping a bit :>")
                        time.sleep(60)
                        self.sc_rolled = 0
                    self.sc_rolled += 1
                    self.next_page_following(self.variables["id"])
                else:
                    self.flag = False
        except: print("error with np")
        for foll in self.following_list:
            for f in foll:
                self.all_following.append(f)

        return self.all_following

Instagram = Instagram()

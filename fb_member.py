import time
from bs4 import BeautifulSoup


class FBMember(object):

    def __init__(self, driver):
        self.__driver = driver

    def login(self, user_name, password):
        self.__driver.get('https://web.facebook.com')

        username_box = self.__driver.find_element_by_id('email')
        username_box.send_keys(user_name)
        print("Email Id entered")
        time.sleep(1)

        password_box = self.__driver.find_element_by_id('pass')
        password_box.send_keys(password)
        print("Password entered")

        login_box = self.__driver.find_element_by_id('loginbutton')
        login_box.click()

        time.sleep(20)

    def scroll_down(self):
        """A method for scrolling the page."""

        # Get scroll height.
        last_height = self.__driver.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to the bottom.
            self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.__driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

    def get_group_members(self,group_id):
        """docstring for crawl_fb_group_member"""
        import requests
        from bs4 import BeautifulSoup
        from selenium import webdriver
        import time
        import json

        self.__driver.get('https://web.facebook.com/groups/' + group_id + '/members')

        time.sleep(20)

        self.scroll_down()

        html = self.__driver.execute_script('return document.documentElement.outerHTML')
        fb_html = BeautifulSoup(html, 'html.parser')

        usr = fb_html.findAll('div', {'class': "_60ri"})
        usr_url = [a.find('a').get('href') for a in usr]

        return usr_url
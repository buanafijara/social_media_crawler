from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import fb_member
import FBPosts as FB
import pandas as pd
import numpy as np

option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})

email = 'yusufmahdiyah10@gmail.com'
password = 'akun0001'

driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe", chrome_options=option)

fb_member = fb_member.FBMember(driver=driver)
fb_member.login(email, password)

num_members = [109]#, 283, 4508]
group_lists = ['809808855729124']#,'736014913824761','738894322871308']

all_user_list = []
all_contents = []
all_users = []

fb_posts = FB.FBPosts(driver=driver, days_lim=10)

for group in group_lists:
    user_list = fb_member.get_group_members(group)
    all_user_list = all_user_list + user_list
    print(len(all_user_list))
    #for i in all_user_list:
    #    print(i)

    for usr in all_user_list:
        content = FB.get_user_post(usr)
        all_contents = all_contents + content
        user = np.repeat(usr, len(all_contents),axis=0).tolist()
        all_users = all_users+user

df = pd.DataFrame(list(zip(all_users, all_contents)),columns =['Member URL', 'Post'])
username = "sukontoraharjo@gmail.com"
password = "akun0001"
group_id = "743158729087573"

def crawl_fb_group_member(group_id, username, password):
  """docstring for crawl_fb_group_member"""
  import requests
  from bs4 import BeautifulSoup
  from selenium import webdriver
  import time
  import json
    
  driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe")
  driver.get('https://web.facebook.com/groups/' + group_id + '/members')
  
  username_box = driver.find_element_by_id('email') 
  username_box.send_keys(username) 
  print ("Email Id entered") 
  time.sleep(1) 
  
  
  password_box = driver.find_element_by_id('pass') 
  password_box.send_keys(password) 
  print ("Password entered") 
    
  login_box = driver.find_element_by_id('loginbutton') 
  login_box.click() 
  
  time.sleep(20)
  
  for k in range(1, 5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(3)
  
  html = driver.execute_script('return document.documentElement.outerHTML')
  fb_html = BeautifulSoup(html, 'html.parser')
  driver.close()
  
  usr = fb_html.findAll('div', {'class' : "_60ri"})
  usr_url = [a.find('a').get('href') for a in usr]
  print(len(usr_url)) # list yg pertama adalah halaman bantuan dan yang kedua adalah profil kita
  print(usr_url)

  #id = []
  
  #for ii in usr:
    #print(ii)
  #  user_link = ii['href']
  #  id.append(user_link)
  
  #id = id[2:]
  #print(id)
  
  #id = list(dict.fromkeys(id))
  #import json
  
  # Writing to sample.json 
  #with open("member_id.json", "w") as outfile:
  #    outfile.write(json.dumps(id))


crawl_fb_group_member(group_id, username, password)
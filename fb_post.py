import datetime as dt
import time
import ast
from bs4 import BeautifulSoup

class FBPost(object):

    def __init__(self, driver, days_lim):
        self.__driver = driver
        self.__days_lim = days_lim

    def get_user_post(self, url):

        def get_date(self):
            str_post_timestamp = self.get('data-store')
            # convert timestamp to dictionary
            post_timestamp = ast.literal_eval(str_post_timestamp)
            post_date = dt.date.fromtimestamp(post_timestamp.get('timestamp'))
            return post_date

        self.__driver.get(url)
        time.sleep(5)

        today = dt.date.today()
        contents = []

        #periksa apakah akun diprivat atau tidak
        src1 = self.__driver.page_source
        soup1 = BeautifulSoup(src1, 'html.parser')
        post1 = soup1.find('div', attrs={'_5pcb _4b0l _2q8l'})

        #jika tidak privat (ada post1)
        if post1:
            #periksa apakah post terakhir masih masuk ke dalam rentang waktu
            latest_post_date = get_date(post1)
            days_diff1 = (today - latest_post_date).days
            if days_diff1 > self.__days_lim :
                contents.append('no recent post')
            else :
                # Looping untuk scrolling
                days_diff = 0
                while days_diff < self.__days_lim:
                    # giving 5 seconds to load the page
                    time.sleep(3)
                    # scroll to the bottom of the page
                    self.__driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                    # getting the page source
                    src = self.__driver.page_source
                    soup = BeautifulSoup(src, 'html.parser')
                    posts = soup.find_all('div', attrs={'_5pcb _4b0l _2q8l'})
                    earliest_date = get_date(posts[-1])
                    days_diff = (today - earliest_date).days

                # menghapus post yang lebih lama dari days_lim
                earliest_date = get_date(posts[-1])
                days_diff2 = (today - earliest_date).days
                while days_diff2 > self.__days_lim:
                    posts.remove(posts[-1])
                    earliest_date = get_date(posts[-1])
                    days_diff2 = (today - earliest_date).days

                for post in posts:
                    # deleting element 'Lihat delengkapnya' & 'Lihat terjemahan'
                    for span in post.find_all('span', attrs={'text_exposed_hide'}):
                        span.decompose()
                    for div in post.find_all('div', {'class': '_43f9 _63qh'}):
                        div.decompose()

                    content_soup = post.find('div', attrs={'_5pbx userContent _3576'})
                    if content_soup:
                        content = [content_soup.get_text()]
                    else:
                        content = [None]
                    contents.append(content)

        #jika privet (tidak ada post1)
        else:
            contents.append('akun privat')
        print(contents)
        return contents

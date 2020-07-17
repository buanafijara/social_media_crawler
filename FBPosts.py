import datetime as dt
import time
import ast
from bs4 import BeautifulSoup

class FBPosts(object):

    def __init__(self, driver, days_lim):
        self.__driver = driver
        self.__days_lim = days_lim

    def get_user_post(self, user_url):

        def get_date(self):
            str_post_timestamp = self.get('data-store')
            # convert timestamp to dictionary
            post_timestamp = ast.literal_eval(str_post_timestamp)
            post_date = dt.date.fromtimestamp(post_timestamp.get('timestamp'))
            return post_date

        days_lim = self.__days_lim
        date_today = dt.date.today()

        self.__driver.get(user_url)
        time.sleep(10)

        days_diff = 0
        posts_date = []
        contents = []

        # cek apakah post terakhir melebihi days_lim
        src1 = self.__driver.page_source
        soup1 = BeautifulSoup(src1, 'html.parser')
        post1 = soup1.find('div', attrs={'_5pcb _4b0l _2q8l'})
        if post1:
            first_date = get_date(post1)
            days_diff1 = (date_today - first_date).days
            if days_diff1 > days_lim:
                posts_date.append('no recent post')
                contents.append('no recent post')

            else:
                # Looping untuk scrolling
                while days_diff < days_lim:
                    # giving 5 seconds to load the page
                    time.sleep(3)
                    # scroll to the bottom of the page
                    self.__driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                    # getting the page source
                    src = self.__driver.page_source
                    soup = BeautifulSoup(src, 'html.parser')
                    posts = soup.find_all('div', attrs={'_5pcb _4b0l _2q8l'})
                    # getting timestamp (str)
                    str_earliest_timestamp = posts[-1].get('data-store')
                    # convert timestamp to dictionary
                    earliest_timestamp = ast.literal_eval(str_earliest_timestamp)
                    earliest_date = dt.date.fromtimestamp(earliest_timestamp.get('timestamp'))
                    days_diff = (date_today - earliest_date).days

                # menghapus post yang lebih lama dari days_lim
                earliest_date = get_date(posts[-1])
                days_diff2 = (date_today - earliest_date).days
                while days_diff2 > days_lim:
                    posts.remove(posts[-1])
                    earliest_date = get_date(posts[-1])
                    days_diff2 = (date_today - earliest_date).days

                for post in posts:
                    # deleting element 'Lihat delengkapnya' & 'Lihat terjemahan'
                    for span in post.find_all('span', attrs={'text_exposed_hide'}):
                        span.decompose()
                    for div in post.find_all('div', {'class': '_43f9 _63qh'}):
                        div.decompose()
                    post_date = get_date(post)
                    posts_date.append(post_date)

                    content_soup = post.find('div', attrs={'_5pbx userContent _3576'})
                    if content_soup:
                        content = content_soup.get_text()
                    else:
                        continue
                    contents.append(content)
        else :
            posts_date.append('private account')
            contents.append('private account')
        return posts_date, contents
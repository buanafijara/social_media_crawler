import datetime as dt
import time
import ast
from bs4 import BeautifulSoup


class FBPosts(object):

    def __init__(self, driver, days_lim):
        self.__driver = driver
        self.__days_lim = days_lim

    def __get_date(self, post):
        str_post_timestamp = post.get('data-store')
        # convert timestamp to dictionary
        post_timestamp = ast.literal_eval(str_post_timestamp)
        post_date = dt.date.fromtimestamp(post_timestamp.get('timestamp'))
        return post_date

    def get_user_post(self, user_url):

        days_lim = self.__days_lim
        date_today = dt.date.today()

        self.__driver.get(user_url)
        time.sleep(5)

        days_diff = 0
        contents = []

        # cek apakah post terakhir melebihi days_lim
        src1 = self.__driver.page_source
        soup1 = BeautifulSoup(src1, 'html.parser')
        post1 = soup1.find('div', attrs={'_5pcb _4b0l _2q8l'})

        post_by = user_url

        if post1:
            first_date = self.__get_date(post1)
            days_diff1 = (date_today - first_date).days
            if days_diff1 > days_lim:
                pass
            else:
                last_height = self.__driver.execute_script('return document.body.scrollHeight')
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
                    new_height = self.__driver.execute_script('return document.body.scrollHeight')
                    if new_height == last_height:
                        break
                    last_height = new_height

                # menghapus post yang lebih lama dari days_lim
                earliest_date = self.__get_date(posts[-1])
                days_diff2 = (date_today - earliest_date).days
                while days_diff2 > days_lim:
                    posts.remove(posts[-1])
                    earliest_date = self.__get_date(posts[-1])
                    days_diff2 = (date_today - earliest_date).days

                for post in posts:
                    # deleting element 'Lihat delengkapnya' & 'Lihat terjemahan'
                    for span in post.find_all('span', attrs={'text_exposed_hide'}):
                        span.decompose()
                    for div in post.find_all('div', {'class': '_43f9 _63qh'}):
                        div.decompose()
                    post_date = self.__get_date(post)

                    # extract content - text
                    text_soup = post.find('div', {'data-testid': 'post_message'})
                    if text_soup:
                        text = text_soup.get_text()
                    else:
                        text = 'NaN'

                    # extract content - image
                    img_soup = post.find_all('img', {'class': ['scaledImageFitHeight img', 'scaledImageFitWidth img']})
                    if img_soup:
                        img_keys = [i for i in range(1, len(img_soup) + 1)]
                        img_values = [a.get('alt') for a in img_soup]
                        img = {k: v for (k, v) in zip(img_keys, img_values)}
                    else:
                        img = 'NaN'

                    if img == 'NaN' and text == 'NaN':
                        continue

                    # extract jumlah likes dan comments
                    likes_tag = post.find('span', attrs={'_81hb'})
                    if likes_tag:
                        num_likes = likes_tag.get_text()
                        if '\xa0rb' in num_likes:
                            num_likes = num_likes.replace('\xa0rb', '000')
                    else:
                        num_likes = 0

                    comments_tag = post.find('a', attrs={'_3hg- _42ft'})
                    if comments_tag:
                        num_comments = comments_tag.get_text().split(' ')[0]
                    else:
                        num_comments = 0

                    content_info = {
                        'post_date': post_date,
                        'post_by': post_by,
                        'text': text,
                        'image': img,
                        'likes': num_likes,
                        'comments': num_comments
                    }
                    contents.append(content_info)
        return contents

    def get_member_profile(self, user_url):

        self.__driver.get(user_url)
        time.sleep(3)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        time.sleep(3)
        src = self.__driver.page_source
        soup = BeautifulSoup(src, 'html.parser')

        is_name = soup.find('a', attrs={'_2nlw _2nlv'})
        if is_name:
            name = is_name.get_text()
        else:
            name = 'NaN'

        is_friends = soup.find('span', {'class': '_50f8 _2iem'})
        if is_friends:
            friends = is_friends.get_text()
        else:
            friends = 'NaN'

        _class_work = '_3-90 _8o _8s lfloat _ohe img sp_rhuOaDUin-L_1_5x sx_e342cd'
        _class_edu = '_3-90 _8o _8s lfloat _ohe img sp_rhuOaDUin-L_1_5x sx_2936a4'
        _class_adress = '_3-90 _8o _8s lfloat _ohe img sp_rhuOaDUin-L_1_5x sx_c4d6a5'
        _class_origin = '_3-90 _8o _8s lfloat _ohe img sp_rhuOaDUin-L_1_5x sx_5a37fe'
        _class_married = '_3-90 _8o _8s lfloat _ohe img sp_rhuOaDUin-L_1_5x sx_c11ec9'

        Work = []
        Edu = []
        Adress = 'NaN'
        Origin = 'NaN'
        Married = 'NaN'

        profile = soup.find_all('li', {'class': '_1zw6 _md0 _5h-n _5vb9'})
        for prfl in profile:
            _class_list = prfl.find('i').get('class')
            _class_str = " ".join(_class_list)
            if _class_str == _class_married:
                Married = prfl.get_text()
            elif _class_str == _class_origin:
                Origin = prfl.get_text()
            elif _class_str == _class_adress:
                Adress = prfl.get_text()
            elif _class_str == _class_edu:
                Edu.append(prfl.get_text())
            elif _class_str == _class_work:
                Work.append(prfl.get_text())

        # intro = soup.find('div', {'id':'profile_timeline_intro_card'})
        # profile_info = intro.find_all('div',{'class' : 'textContent'})
        # profiles = []
        # for _ in profile_info:
        #    profiles = profiles+[_.get_text()]
        profile_info = {
            'Name': name,
            'Friends': friends,
            'Work': Work,
            'Education': Edu,
            'Adress': Adress,
            'Hometown': Origin,
            'Married': Married
        }
        print(profile_info)
        return profile_info

    def get_post_stat(self, user_posts):
        user_post = pd.DataFrame(user_posts)
        days_lim = self.__days_lim
        num_weeks = days_lim // 7
        user_post = user_post.astype({'post_date': 'datetime64[ns]', 'likes': 'int32', 'comments': 'int32'})

        # rata2 postingan per minggu
        post_counts = user_post['post_by'].value_counts()
        avg_post_per_week = user_post['post_by'].value_counts() / num_weeks

        # sum likes & comments per post
        sum_likes_comments = user_post.groupby('post_by')[['likes', 'comments']].sum()
        result = pd.concat([post_counts.rename('post_counts'), avg_post_per_week.rename('avg_ppw'), sum_likes_comments],
                           axis=1, sort=False)

        # avg likes & comments per post
        like_per_post = result['likes'] / result['post_counts']
        comments_per_post = result['comments'] / result['post_counts']

        # avg text post per week
        user_post_text = user_post.loc[user_post['text'].notnull() & ~user_post['image'].notnull(),]
        txt_per_week = user_post_text.groupby('post_by')[['text']].count() / num_weeks
        txt_per_week.columns = ['txt_per_week']

        # avg image post per week
        user_post_image = user_post.loc[user_post['image'].notnull() & ~user_post['text'].notnull(),]
        img_per_week = user_post_image.groupby('post_by')[['image']].count() / num_weeks
        img_per_week.columns = ['img_per_week']

        # avg text and image post per week
        user_post_text_n_image = user_post.loc[user_post['image'].notnull() & user_post['text'].notnull(),]
        txt_n_img_per_week = user_post_text_n_image.groupby('post_by')[['image']].count() / num_weeks
        txt_n_img_per_week.columns = ['txt_n_img_per_week']

        # avg comments and likes per text post
        sum_likes_comment = user_post_text.groupby('post_by')[['likes', 'comments']].sum()
        count_text_post = user_post_text.groupby('post_by')[['text']].count()
        user_post_text = pd.concat([count_text_post, sum_likes_comment], axis=1, sort=False)
        user_post_text['likes_per_text'] = user_post_text['likes'] / user_post_text['text']
        user_post_text['comments_per_text'] = user_post_text['comments'] / user_post_text['text']

        # avg comments and likes per image post
        sum_likes_comment = user_post_image.groupby('post_by')[['likes', 'comments']].sum()
        count_image_post = user_post_image.groupby('post_by')[['image']].count()
        user_post_image = pd.concat([count_image_post, sum_likes_comment], axis=1, sort=False)
        user_post_image['likes_per_image'] = user_post_image['likes'] / user_post_image['image']
        user_post_image['comments_per_image'] = user_post_image['comments'] / user_post_image['image']

        # avg comments and likes per image and text post
        sum_likes_comment = user_post_text_n_image.groupby('post_by')[['likes', 'comments']].sum()
        count_text_n_image_post = user_post_text_n_image.groupby('post_by')[['text']].count()
        user_post_text_n_image = pd.concat([count_text_n_image_post, sum_likes_comment], axis=1, sort=False)
        user_post_text_n_image['likes_per_txt_n_img'] = user_post_text_n_image['likes'] / user_post_text_n_image['text']
        user_post_text_n_image['comments_per_txt_n_img'] = user_post_text_n_image['comments'] / user_post_text_n_image[
            'text']

        result = pd.concat((avg_post_per_week.rename('avg_ppw'),
                            like_per_post.rename('like_per_post'), comments_per_post.rename('comments_per_post'),
                            txt_per_week, img_per_week, txt_n_img_per_week, user_post_text['likes_per_text'],
                            user_post_text['comments_per_text'], user_post_image['likes_per_image'],
                            user_post_image['comments_per_image'], user_post_text_n_image['likes_per_txt_n_img'],
                            user_post_text_n_image['comments_per_txt_n_img']), axis=1, sort=False)
        return result
# import basic packages
import configparser
import logging
import numpy as np
import pandas as pd
import time
from datetime import date
from tqdm import tqdm

# selenium-related
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# custom utility functions
import scraperutils as u

logging.basicConfig(filename='scraper.log', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main():
    logger.info('Started scraping')

    # Setting Selenium options
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # read config
    config_path = './fb_scraper_config.ini'
    config = configparser.ConfigParser()
    config.read(config_path)
    user_login = config['DEFAULT']['user_login'] # config returns string of 'False' or 'True'
    credentials_path = config['DEFAULT']['credentials_path']
    webdriver_path = config['DEFAULT']['webdriver_path']
    target_website = config['DEFAULT']['target_website']
    target_subpage = config['DEFAULT']['target_subpage']
    post_class_type = config['COMPONENT_NAMES']['post_class_type']
    post_class_name = config['COMPONENT_NAMES']['post_class_name']
    link_class_type = config['COMPONENT_NAMES']['link_class_type']
    link_class_name = config['COMPONENT_NAMES']['link_class_name']
    text_class_type = config['COMPONENT_NAMES']['text_class_type']
    text_class_name = config['COMPONENT_NAMES']['text_class_name']
    like_class_type = config['COMPONENT_NAMES']['like_class_type']
    like_class_name = config['COMPONENT_NAMES']['like_class_name']
    comment_share_class_type = config['COMPONENT_NAMES']['comment_share_class_type']
    comment_share_class_name = config['COMPONENT_NAMES']['comment_share_class_name']
    headline_class_type = config['COMPONENT_NAMES']['headline_class_type']
    headline_class_name = config['COMPONENT_NAMES']['headline_class_name']
    not_headlines = config['COMPONENT_NAMES']['not_headlines'].split(',')
    not_headlines = [txt.strip() for txt in not_headlines]
    sponsored_by = config['COMPONENT_NAMES']['sponsored_by'].split(',')
    sponsored_by = [txt.strip() for txt in sponsored_by]

    if user_login == 'True':
        with open(f'./{credentials_path}') as file:
            EMAIL = file.readline().split('"')[1]
            PASSWORD = file.readline().split('"')[1]
        browser = webdriver.Chrome(executable_path=webdriver_path, options=option)
        browser.get(target_website)
        browser.maximize_window()
        wait = WebDriverWait(browser, 30)
        email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
        email_field.send_keys(EMAIL)
        pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
        pass_field.send_keys(PASSWORD)
        pass_field.send_keys(Keys.RETURN)
        #If 2FA is enabled: input("Once 2FA is done, press Enter to continue...")
    else:
        browser = webdriver.Chrome(executable_path=webdriver_path, options=option)
        browser.get(target_website)
        browser.maximize_window()
        u.sleep_poisson()

    time.sleep(1.1)
    browser.get(target_subpage)
    time.sleep(0.98)

    post_dates = [] # WIP
    urls = []
    texts = []
    likes = []
    shares = []
    headlines = []
    comment_counts = []

    max_post_count = 200
    post_count = 0

    while post_count < max_post_count: # termination condition now is post count but will change to article date
        logger.info(f"scraped {post_count} out of {max_post_count} so far.")
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        u.sleep_poisson()
        posts = browser.find_elements(By.XPATH, f"//{post_class_type}[@class='{post_class_name}']")

        for post in tqdm(posts):
            # getting post dates
            # WIP
            post_dates.append('TBD')
            
            # getting article links
            sub_elements = post.find_elements(By.XPATH, f".//{link_class_type}[@class='{link_class_name}']")
            article_urls = []
            for link in sub_elements:
                try:
                    ActionChains(browser).move_to_element(link).perform() # this keeps browser scrolling to next post
                    url = link.get_attribute('href')
                    article_urls.append(url)
                except:
                    pass
            urls.append(article_urls)

            # getting post text
            sub_elements = post.find_elements(By.XPATH, f".//{text_class_type}[@class='{text_class_name}']")
            text = [sub_element.text for sub_element in sub_elements]
            texts.append(text)

            # getting post likes
            sub_elements = post.find_elements(By.XPATH, f".//{like_class_type}[@class='{like_class_name}']")
            like = [sub_element.text for sub_element in sub_elements]
            likes.append(like)

            # getting post comments and shares
            sub_elements = post.find_elements(By.XPATH, f".//{comment_share_class_type}[@class='{comment_share_class_name}']")
            comment_share = [sub_element.text for sub_element in sub_elements]

            # parsing those xx comments and yy shares text
            if comment_share != [] and len(comment_share) == 2: # has both comments and shares
                share = comment_share[1].split(' ')[0]
                comment = comment_share[0].split(' ')[0]
                shares.append(share)
                comment_counts.append(comment)
            elif comment_share != [] and len(comment_share) == 1: # has either only comments or shares
                if 'comment' in comment_share[0]:
                    comment = comment_share[0].split(' ')[0]
                    shares.append('')
                    comment_counts.append(comment)
                elif 'share' in comment_share[0]:
                    share = comment_share[0].split(' ')[0]
                    shares.append(share)
                    comment_counts.append('')
                else:
                    shares.append('')
                    comment_counts.append('')
            else:
                shares.append('')
                comment_counts.append('')
            
            # getting article headlines
            sub_elements = post.find_elements(By.XPATH, f".//{headline_class_type}[@class='{headline_class_name}']")
            headline = [sub_element.text for sub_element in sub_elements]
            headlines.append(headline)
        
        # termination condition now is post count but will change to article date
        post_count += len(posts)
    
    logger.info('Finished scraping')
    logger.info('Begin data cleaning')

    df = pd.DataFrame({
        'post_date': post_dates,
        'headlines': headlines,
        'texts':texts,
        'likes': likes,
        'comment_counts': comment_counts,
        'shares': shares,
        'url': urls
        }
    )
    # cleaning the columns
    df['headlines'] = df['headlines'].apply(lambda x: u.get_value_of_array(x))
    df['texts'] = df['texts'].apply(lambda x: u.get_value_of_array(x))
    df['likes'] = df['likes'].apply(lambda x: u.get_value_of_array(x))
    df['likes'] = df['likes'].apply(lambda x: u.convert_likes(x))
    df['likes'] = df['likes'].fillna(0).astype(int).astype(str)
    df['comment_counts'] = df['comment_counts'].apply(lambda x: u.convert_likes(x))
    df['shares'] = df['shares'].apply(lambda x: u.convert_likes(x))
    df['url'] = df['url'].apply(lambda x: u.get_value_of_array(x))

    df = df.drop_duplicates()
    df = df[~df['headlines'].isin(not_headlines)]
    df = df[~(df['headlines'] + df['texts']).isna()]

    df['sponsored'] = df['texts'].apply(lambda x: u.get_sponsored(x, sponsored_by))
    df['sponsor_name'] = df.apply(lambda x: u.get_sponsor_name(x, sponsored_by), axis=1)

    # save file
    date_in_yyyymmdd = date.today().strftime("%Y%m%d")
    logger.info(f'Done and saving to file: scraping_results_{date_in_yyyymmdd}.csv')
    df.to_csv(f'./scraping_results_{date_in_yyyymmdd}.csv', index=False)

if __name__ == '__main__':
    main()

import os, datetime, time, sys, pickle
from random import randint
import re
import osascript
import requests
import random

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, \
    UnexpectedAlertPresentException, WebDriverException
from pip._vendor.distlib.util import proceed
import constants
from commons import myprint

def load_cookie(driver, path):
    with open(path, 'rb') as cookies_file:
        cookies = pickle.load(cookies_file)
        for cookie in cookies:
            driver.add_cookie(cookie)


ref_pattern = re.compile("https://wn.nr.*")
yousub_pattern = re.compile("https://youtube.com/user/.*sub_confirmation.*|https://youtube.com/channel/.*?sub_confirmation.*|https://youtube.com/.*?sub_confirmation.*|https://youtube.com/c/.*?sub_confirmation.*")
google_login_pattern = re.compile("https://accounts.google.com/signin/v2/identifier.*")

amzn_shop_pattern  = re.compile("https://www.amazon.com/shop/.*")
twitter_page_pattern = re.compile("https://twitter.com/intent/follow?screen_name=.*")
fb_page_pattern = re.compile("https://www.facebook.com/.*|https://facebook.com/.*")
fb_group_pattern = re.compile("https://www.facebook.com/groups/.*|https://facebook.com/groups/.*")
fb_photos_pattern = re.compile("https://www.facebook.com/.*/photos/.*")

insta_page_pattern = re.compile("https://instagram.com/.*?ref=badge|https://www.instagram.com/.*")
gplus_page_pattern = re.compile("https://plus.google.com/.*")

discord_page_pattern = re.compile("https://discord.gg/.*")

def get_time():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

ans = ["Awesome Giveaways!!!", "Don't Miss this giveaway", "Guys found another cool giveaway", "Few clicks and get prizes"]

def subscribe_channel(driver, url):
    try:
        driver.get(url)
        time.sleep(1)
        driver.switch_to.active_element
        sub_button = driver.find_element_by_css_selector("#confirm-button > a")
        time.sleep(1)
        sub_button.click()
        time.sleep(constants.SOCIAL_FOLLOW_LIMIT_WAIT + random.randint(0, 5))
    except Exception as e:
        myprint("Might be already subscribed", e)

def follow_gplus_page(driver, url):
    driver.get(url)
    time.sleep(1)
    gplus_follow_buttons = driver.find_elements_by_css_selector("div > c-wiz> div > div > div > div > div > div > content > span > div > div")
    if len(gplus_follow_buttons) > 0:
        if gplus_follow_buttons[0].text.strip() == "Follow":
            time.sleep(2)
            try:
                gplus_follow_buttons[0].click()
                with open("data/links_done.txt", "a") as outfile:
                    outfile.write(line)
                time.sleep(constants.SOCIAL_FOLLOW_LIMIT_WAIT + random.randint(1, 3))
            except Exception as e:
                myprint(line, e)
        else:
            myprint(f'{line} Seems already following')
    else:
        myprint(f'{line} No button might be on wrong page')

def google_login(driver):
    email_element = driver.find_element_by_id("identifierId")
    if email_element:
        email_element.send_keys(constants.GOOG_ID)
        email_element.send_keys(Keys.ENTER)
    time.sleep(5)

    pass_element = driver.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input")
    if pass_element:
        pass_element.send_keys(constants.GOOG_PASS)
        pass_element.send_keys(Keys.ENTER)
    time.sleep(5)

def amazon_login(driver):
    driver.get("https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&switch_account=")
    time.sleep(2)
    email_element = driver.find_element_by_id("ap_email")
    if email_element:
        email_element.send_keys(constants.AMZN_ID)
        email_element.send_keys(Keys.ENTER)
    time.sleep(5)

    pass_element = driver.find_element_by_id("ap_password")
    if pass_element:
        pass_element.send_keys(constants.AMZN_PASS)
        pass_element.send_keys(Keys.ENTER)
    time.sleep(5)

if __name__ == "__main__":
    argv = sys.argv[1:]
    d = {}
    for i in range(0, len(argv), 2):
        d[argv[i].replace('-', '')] = argv[i + 1]
    myprint(d)

    chrome_options = webdriver.ChromeOptions()
    if 'headless' in d:
        chrome_options.add_argument("--headless")

    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path = constants.CHROME_DRIVER_PATH, chrome_options = chrome_options)

    driver.get("https://google.com")

    load_cookie(driver, '/tmp/gleam_fb_cookie')
    load_cookie(driver, '/tmp/gleam_google_cookie')
    load_cookie(driver, '/tmp/gleam_twitter_cookie')
    load_cookie(driver, '/tmp/gleam_instagram_cookie')

    amazon_login(driver)

    with open(f'data/links.txt') as infile:
        for line in infile:
            line_arr = line.split(',')
            link = line_arr[0]
            if len(line_arr) > 1 and ref_pattern.match(link) != None:
                msg = random.choice(ans)  + line_arr[1] + " " + link
                myprint(msg)
                driver.get("https://twitter.com")
                tweet_box = driver.find_element_by_css_selector('#tweet-box-home-timeline')
                tweet_box.send_keys(msg)
                time.sleep(2)
                tweet_submit_button = driver.find_element_by_css_selector('#timeline > div.timeline-tweet-box > div > form > div.TweetBoxToolbar > div.TweetBoxToolbar-tweetButton.tweet-button > button')
                tweet_submit_button.click()
                with open("data/links_done.txt", "a") as outfile:
                    outfile.write(line)
                time.sleep(constants.TWEET_SPAM_LIMIT_WAIT + random.randint(11, 30))
            elif yousub_pattern.match(link) != None :
                myprint(link)
                subscribe_channel(driver, link)
                if google_login_pattern.match(driver.current_url) != None :
                    google_login(driver)
                    subscribe_channel(driver, link)
                with open("data/links_done.txt", "a") as outfile:
                    outfile.write(line)
                time.sleep(random.randint(10, 40))
            elif twitter_page_pattern.match(link) != None:
                myprint(link)
                driver.get(link)
                time.sleep(2)
                twitter_follow_buttons = driver.find_elements_by_css_selector("#follow_btn_form > button")
                if len(twitter_follow_buttons) > 0:
                    if twitter_follow_buttons[0].text.strip() == "Follow":
                        time.sleep(2)
                        try:
                            twitter_follow_buttons[0].click()
                            with open("data/links_done.txt", "a") as outfile:
                                outfile.write(line)
                            time.sleep(constants.SOCIAL_FOLLOW_LIMIT_WAIT + random.randint(1, 3))
                        except Exception as e:
                            myprint(line, e)
                    else:
                        myprint(f'{line} Seems already following')
                else:
                    myprint(f'{line} Follow Button not found')
            elif amzn_shop_pattern.match(link) != None:
                myprint(link)
                driver.get(link)
                time.sleep(2)
                amzn_follow_buttons = driver.find_elements_by_css_selector("#a-page > div.a-section.a-spacing-small.shop-page-container > div.a-row.a-spacing-mini.shop-landing-section > div.verified-profile > div.amazon-follow-container > div > div.pr-fb-container > span > span > span > span.pr-fb-text")
                if len(amzn_follow_buttons) > 0:
                    if amzn_follow_buttons[0].text.strip() == "Follow":
                        time.sleep(2)
                        try:
                            amzn_follow_buttons[0].click()
                            with open("data/links_done.txt", "a") as outfile:
                                outfile.write(line)
                            time.sleep(constants.SOCIAL_FOLLOW_LIMIT_WAIT + random.randint(1, 3))
                        except Exception as e:
                            myprint(line, e)
                    else:
                        if amzn_follow_buttons[0].text.strip() == "Following":
                            myprint(f'{line} Seems already following')
                            with open("data/links_done.txt", "a") as outfile:
                                outfile.write(line)
                        else:
                            myprint(f'{line} No clue')
                else:
                    myprint(f'{line} Join Group Button not found')
            elif fb_group_pattern.match(link) != None:
                myprint(link)
                driver.get(link)
                time.sleep(2)
                fb_join_buttons = driver.find_elements_by_css_selector("#u_0_15 > div > div > div > div > a")
                if len(fb_join_buttons) == 0:
                    fb_join_buttons = driver.find_elements_by_css_selector("#u_0_16 > div > div > div > div > a")
                if len(fb_join_buttons) > 0:
                    if fb_join_buttons[0].text.strip() == "Join Group":
                        time.sleep(2)
                        try:
                            fb_join_buttons[0].click()
                            with open("data/links_done.txt", "a") as outfile:
                                outfile.write(line)
                            time.sleep(constants.SOCIAL_FOLLOW_LIMIT_WAIT + random.randint(1, 3))
                        except Exception as e:
                            myprint(line, e)
                    else:
                        if fb_join_buttons[0].text.strip() == "Pending":
                            myprint(f'{line} Seems already joined group')
                            with open("data/links_done.txt", "a") as outfile:
                                outfile.write(line)
                        else:
                            myprint(f'{line} No clue')
                else:
                    myprint(f'{line} Join Group Button not found')
            elif fb_photos_pattern.match(link) != None:
                myprint(link)
                driver.get(link)
                time.sleep(2)
                fb_photos_like_buttons = driver.find_elements_by_css_selector("#fbPhotoSnowliftFeedback > div > div > div > div > div > div > div > span:nth-child(1) > div > a")
                if len(fb_photos_like_buttons) > 0:
                    if fb_photos_like_buttons[0].text.strip() == "Like":
                        time.sleep(2)
                        try:
                            fb_photos_like_buttons[0].click()
                            with open("data/links_done.txt", "a") as outfile:
                                outfile.write(line)
                            time.sleep(constants.SOCIAL_FOLLOW_LIMIT_WAIT + random.randint(1, 3))
                        except Exception as e:
                            myprint(line, e)
                    else:
                        # if fb_photos_like_buttons[0].text.strip() == "Pending":
                        #     myprint(f'{line} Seems already joined group')
                        #     with open("data/links_done.txt", "a") as outfile:
                        #         outfile.write(line)
                        # else:
                        myprint(f'{line} No clue: {fb_photos_like_buttons[0].text.strip()}')
                else:
                    myprint(f'{line} Join Group Button not found')
            elif fb_page_pattern.match(link) != None:
                myprint(link)
                driver.get(link)
                time.sleep(2)
                fb_follow_buttons = driver.find_elements_by_css_selector("div > div > div > div > div._hoc.clearfix > div >  div.lfloat > div > div > button:nth-child(2)")

                if len(fb_follow_buttons) == 0:
                    fb_follow_buttons = driver.find_elements_by_css_selector("#u_0_18 > div > div > div:nth-child(2) > div > a > span")

                if len(fb_follow_buttons) > 0:
                    if fb_follow_buttons[0].text.strip() == "Follow":
                        time.sleep(2)
                        try:
                            fb_follow_buttons[0].click()
                            with open("data/links_done.txt", "a") as outfile:
                                outfile.write(line)
                            time.sleep(constants.SOCIAL_FOLLOW_LIMIT_WAIT + random.randint(1, 3))
                        except Exception as e:
                            myprint(line, e)
                    else:
                        if fb_follow_buttons[0].text.strip() == "Following":
                            myprint(f'{line} Seems already following')
                            with open("data/links_done.txt", "a") as outfile:
                                outfile.write(line)
                        else:
                            myprint(f'{line} No clue')
                else:
                    myprint(f'{line} Follow Button not found')
            elif insta_page_pattern.match(link) != None:
                myprint(link)
                driver.get(link)
                time.sleep(2)
                insta_follow_buttons = driver.find_elements_by_css_selector("#react-root > section > main > div > header > section > div > span > span.vBF20._1OSdk > button")
                if len(insta_follow_buttons) > 0:
                    insta_follow_buttons = driver.find_elements_by_css_selector("#react-root > section > main > div > header > section > div > button")
                if len(insta_follow_buttons) > 0:
                    if insta_follow_buttons[0].text.strip() == "Follow":
                        time.sleep(2)
                        try:
                            insta_follow_buttons[0].click()
                            with open("data/links_done.txt", "a") as outfile:
                                outfile.write(line)
                            time.sleep(constants.SOCIAL_FOLLOW_LIMIT_WAIT + random.randint(1, 3))
                        except Exception as e:
                            myprint(line, e)
                    else:
                        if insta_follow_buttons[0].text.strip() == "Following":
                            myprint(f'{line} Seems already following')
                            with open("data/links_done.txt", "a") as outfile:
                                outfile.write(line)
                        else:
                            myprint(f'{line} No clue')
                else:
                    myprint(f'{line} Follow Button not found')
            elif gplus_page_pattern.match(link) != None:
                myprint(link)
                driver.get(link)
                time.sleep(2)
                follow_gplus_page(driver, link)
                if google_login_pattern.match(driver.current_url) != None :
                    google_login(driver)
                    follow_gplus_page(driver, link)
                with open("data/links_done.txt", "a") as outfile:
                    outfile.write(line)
                time.sleep(random.randint(10, 40))
            elif discord_page_pattern.match(link) != None:
                myprint(link)
                driver.get(link)
                time.sleep(2)
                discord_invite_buttons = driver.find_elements_by_css_selector("#app-mount > div.app-19_DXt.platform-web > div > div > div > section > div > button")
                if len(discord_invite_buttons) > 0:
                    try:
                        discord_invite_buttons[0].click()
                        time.sleep(constants.SOCIAL_FOLLOW_LIMIT_WAIT + random.randint(1, 3))
                        time.sleep(2)
                        inputElement2 = driver.find_element_by_xpath('//*[@id="app-mount"]/div[1]/div/div[2]/div/form/div/div[3]/div[1]/div/input')

                        if inputElement2:
                            inputElement2.send_keys(constants.DISCORD_ID)
                        time.sleep(2)

                        inputElement2 = driver.find_element_by_xpath('//*[@id="app-mount"]/div[1]/div/div[2]/div/form/div/div[3]/div[2]/div/input')
                        if inputElement2:
                            inputElement2.send_keys(constants.DISCORD_PASS)
                            inputElement2.send_keys(Keys.ENTER)
                            time.sleep(2)
                        with open("data/links_done.txt", "a") as outfile:
                            outfile.write(line)
                        time.sleep(constants.SOCIAL_FOLLOW_LIMIT_WAIT + random.randint(1, 3))
                    except Exception as e:
                        myprint(line, e)
                else:
                    myprint(f'{line} Accept Invite Button not found')
            else:
                myprint("Non Matching:", link)
    driver.quit()

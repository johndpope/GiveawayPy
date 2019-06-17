import os, datetime, time, sys, pickle
from random import randint
import re
import requests
import random

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, \
    UnexpectedAlertPresentException, WebDriverException
from selenium.webdriver.support.select import Select
from pip._vendor.distlib.util import proceed
import constants
from commons import myprint

join_live_pattern =  re.compile("join us for our live play.*")

is_not_available_pattern = re.compile("sorry.*is not available.*")
has_ended_pattern = re.compile(".*competition.*has.*ended")

checkout_video_pattern = re.compile("check out.*")
click_to_confirm_pattern = re.compile(".*click.*to.*confirm.*")
confirm_details_pattern = re.compile(".*confirm.*details.*")
click_for_bonus_pattern = re.compile(".*click.*for.*bonus.*entry.*|.*get.*bonus.*entries.*")

watch_pattern = re.compile("watch.*|video entry bonus|comment.*youtube.*")
play_steam_pattern = re.compile("play.*on steam")

subscribe_pattern = re.compile(".*subscribe.*|.*subscription.*entry.*|bonus.*subscribers.*")

fb_instagram_photoview_pattern = re.compile("view this photo on facebook|view this photo on instagram")

follow_on_instagram_pattern = re.compile("follow.*on instagram")
follow_on_tumblr_pattern = re.compile("follow.*on tumblr")
follow_on_twitter_pattern = re.compile("follow.*on twitter")
follow_on_linkedin_pattern = re.compile("follow.*on linkedin")
follow_on_mixer_pattern = re.compile("follow.*on mixer.*")
follow_on_twitchtv_pattern = re.compile("follow.*on twitch.tv")

retweet_pattern = re.compile("retweet.*|tweet.*")
liking_fb_page_only_pattern = re.compile("enter by liking.*facebook page")
like_fb_page_pattern = re.compile("like.*facebook.*|like.*fb.*")
enter_using_fb_pattern = re.compile("enter using facebook")

answer_qn_pattern = re.compile("answer.*question")
email_qn_pattern = re.compile(".*email address.*")
full_contact_pattern = re.compile(".*full contact information.*")
share_post_fb_pattern = re.compile("share.*facebook|like.*share.*comment.*post|like.*comment.*twitter.*post")

check_board_game_pattern = re.compile("check out board game deals")
check_store_pattern = re.compile("check out .* store")
check_store_amazon_pattern = re.compile("check out.*on amazon")
check_plan_pattern = re.compile("check.*plans.*")

register_pattern = re.compile("register on.*")
join_telegram_pattern = re.compile("join.*telegram.*")
refer_friends_pattern = re.compile("refer.*friends.*|share with your followers|share to win extra entries.*|tell.*friends.*")

newsletter_pattern = re.compile(".*newsletter")

visit_fb_pattern = re.compile("visit.*on facebook|sign up.*on facebook")
view_post_on_fb_pattern = re.compile("view.*post on facebook")

visit_instagram_pattern = re.compile("visit.*on instagram.*")
visit_pinterest_pattern = re.compile("visit.*on pinterest.*")
visit_gplus_pattern = re.compile("visit.*on google+.*")

visit_giveaways_pattern = re.compile("visit .* giveaways on .*|visit the current giveaways on.*|enter .* giveaways on .*|bonus entries for entering .* giveaway")
visit_pattern = re.compile("visit .*")
comment_pattern = re.compile("comment .*")
create_account_pattern = re.compile("create.*account.*")
download_pattern = re.compile("download .*")

def relaunch(driver, d):
    driver.quit()
    chrome_options = Options()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery")
    if 'headless' in d:
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=constants.CHROME_DRIVER_PATH)
    driver.get("https://google.com")
    load_cookie(driver, '/tmp/gleam_fb_cookie')
    load_cookie(driver, '/tmp/gleam_google_cookie')
    load_cookie(driver, '/tmp/gleam_twitter_cookie')
    load_cookie(driver, '/tmp/gleam_instagram_cookie')
    load_cookie(driver, '/tmp/gleam_soundcloud_cookie')
    load_cookie(driver, '/tmp/gleam_steampowered_cookie')
    return driver

#Type0
def type0_click_continue(driver, element, patt = ''):
    continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > button")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div.form-actions > button.btn-primary")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > div > a")
    action = ActionChains(driver)
    action.move_to_element(continue_buttons[0])
    action.click().perform()
    myprint(constants.CGREEN + patt, 'type0_click_continue: continue clicked' + constants.CEND)

#Type1
def type1_click_continue(driver, element, patt = ''):
    continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > div > a")
    continue_buttons[0].click()
    myprint(constants.CGREEN + patt, 'type1_click_continue: continue clicked' + constants.CEND)

#Type2
def type2_click_continue(driver, element, patt = ''):
    continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > div > a")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > a")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div.form-actions > button.btn-primary")
    if continue_buttons[0].get_attribute("disabled") in ["true","disabled"]:
        element.click()
    else:
        action = ActionChains(driver)
        action.move_to_element(continue_buttons[0])
        action.click().perform()
        myprint(constants.CGREEN + patt, 'type2_click_continue: continue clicked' + constants.CEND)

#Type3
def type3_click_continue(driver, element, patt = ''):
    continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > div > a.btn-primary")
    action = ActionChains(driver)
    action.move_to_element(continue_buttons[0])
    action.click().perform()
    myprint(constants.CGREEN + patt, 'type3_click_continue: continue clicked' + constants.CEND)

#Type4
def type4_click_continue(driver, element, patt = ''):
    continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > button:nth-child(2)")
    if len(continue_buttons) == 0:
        return False
    action = ActionChains(driver)
    action.move_to_element(continue_buttons[0])
    action.click().perform()
    myprint(constants.CGREEN + patt, 'type4_click_continue: continue clicked' + constants.CEND)
    return True

#Type4a
def type4a_click_continue(driver, element, patt = ''):
    continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > button")
    if len(continue_buttons) == 0:
        return False
    action = ActionChains(driver)
    action.move_to_element(continue_buttons[0])
    action.click().perform()
    myprint(constants.CGREEN + patt, 'type4a_click_continue: continue clicked' + constants.CEND)
    return True

#Type5
def type5_click_continue(driver, element, patt = ''):
    continue_buttons = element.find_elements_by_css_selector("div.body-widget > div > div > div > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(2) > div > form > div > span:nth-child(1) > button")
    if len(continue_buttons) == 0:
        return False
    action = ActionChains(driver)
    action.move_to_element(continue_buttons[0])
    action.click().perform()
    myprint(constants.CGREEN + patt, 'type5_click_continue: continue clicked' + constants.CEND)
    return True

#Type6
def type6_click_continue(driver, element, patt = ''):
    continue_buttons = element.find_elements_by_css_selector("div > div > form > div > span:nth-child(1) > button")
    if len(continue_buttons) == 0:
        return False
    action = ActionChains(driver)
    action.move_to_element(continue_buttons[0])
    action.click().perform()
    myprint(constants.CGREEN + patt, 'type6_click_continue: continue clicked' + constants.CEND)
    return True

def typeX_click_continue(driver, element, ctr, patt = ''):
    try:
        all_expandables = driver.find_elements_by_css_selector('div.body-widget > div > div > div.popup-blocks-container > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(3) > div > div > div.expandable')
        current_expandable = all_expandables[ctr]
        if not current_expandable.is_displayed():
            element.click()
    except Exception as e:
        myprint(constants.CRED + "Possibly no expandable case came here" + constants.CEND, e)
        return

    continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > button")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div.form-actions > button.btn-primary")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > div > a")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > a")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > div > a.btn-primary")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > button:nth-child(2)")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div.body-widget > div > div > div > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(2) > div > form > div > span:nth-child(1) > button")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div > div > form > div > span:nth-child(1) > button")
    if len(continue_buttons) == 0:
        return False
    for button in continue_buttons:
        if button.text == 'Continue' or button.text == 'Continuar' or button.text == 'Weiter' or button.text == 'Save':
            action = ActionChains(driver)
            action.move_to_element(button)
            action.click().perform()
            myprint(constants.CGREEN + patt, 'typeX_click_continue: continue clicked' + constants.CEND)
            return not is_current_expandable_open(driver, element, ctr)
    return False

def load_cookie(driver, path):
    with open(path, 'rb') as cookies_file:
        cookies = pickle.load(cookies_file)
        for cookie in cookies:
            driver.add_cookie(cookie)

def is_logged_in(driver):
    prelogin_status = driver.find_elements_by_css_selector("body > div.body-widget > div > div > div.popup-blocks-container > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(3) > div > span > div:nth-child(2) > div")
    if len(prelogin_status)>0 and prelogin_status[0].text=="Login with:":
        return False

    loggedin_status = driver.find_elements_by_css_selector("body > div.body-widget > div > div > div.popup-blocks-container > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(3) > div > span > div.small-bar.contestant-logged-in.center.ng-scope > div.small-bar--text.ng-binding")
    if len(loggedin_status)>0 and loggedin_status[0].text.split('\n')[0]=="Entering as":
        return True
    return False

def login(driver):
    time.sleep(2)
    login_options = driver.find_elements_by_css_selector("div > div.popup-blocks-container > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(2) > div > form > fieldset.center > div > ul > li")
    for element in login_options:
        children  = element.find_elements_by_css_selector("*")
        for child in children:
            if('facebook-background' in child.get_attribute("class").split(' ')):
                try:
                    element.click()
                    time.sleep(2)
                    # myprint("login: 1st fb login succeeded")
                except Exception:
                    # myprint("1st fb login method failed, trying 2nd way")
                    try:
                        fbs = driver.find_elements_by_css_selector("body > div.body-widget > div > div > div.popup-blocks-container > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(3) > div > span > div:nth-child(2) > ul > li > a.facebook-background")
                        fbs[0].click()
                        time.sleep(2)
                        # myprint("login: 2nd fb login succeeded")
                    except Exception:
                        myprint("login: Exception:(suppressed)")
                        return False
                if is_logged_in(driver):
                    return True

    for element in login_options:
        children  = element.find_elements_by_css_selector("*")
        for child in children:
            if('twitter-background' in child.get_attribute("class").split(' ')):
                try:
                    element.click()
                    time.sleep(2)
                    # myprint("login: 1st twitter login succeeded")
                except Exception:
                    # myprint("1st twitter login method failed, trying 2nd way")
                    try:
                        twtr = driver.find_elements_by_css_selector("body > div.body-widget > div > div > div.popup-blocks-container > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(3) > div > span > div:nth-child(2) > ul > li:nth > a.twitter-background")
                        twtr[0].click()
                        time.sleep(2)
                        # myprint("login: 2nd twitter login succeeded")
                    except Exception:
                        myprint("login: Exception:")
                        return False
                if is_logged_in(driver):
                    return True

    myprint(constants.CRED + "login: FAILED:" + constants.CEND)
    return False

def is_answer(element):
    potential_checks = element.find_elements_by_css_selector("span i")
    for child in potential_checks:
        if('fa-pencil-square-o' in child.get_attribute("class").split(' ')):
            return True
    return False

def is_external_link(element):
    potential_checks = element.find_elements_by_css_selector("span i")
    for child in potential_checks:
        if('fa-external-link-square' in child.get_attribute("class").split(' ')):
            return True
    return False

def is_youtube(element):
    potential_checks = element.find_elements_by_css_selector("span i")
    for child in potential_checks:
        if('fa-youtube' in child.get_attribute("class").split(' ')):
            return True
    return False

def is_done(element):
    potential_checks = element.find_elements_by_css_selector("span i")
    for child in potential_checks:
        child_classes = child.get_attribute("class").split(' ')
        if 'fa-check' in child_classes or 'fa-clock-o' in child_classes:
            return True
    return False

def is_daily_candidate(element):
    potential_checks = element.find_elements_by_css_selector("span i")
    for child in potential_checks:
        child_classes = child.get_attribute("class").split(' ')
        if 'fa-clock-o' in child_classes:
            return True
    return False

def click_to_confirm(driver, element):
    myprint(constants.CGREEN + 'click_to_confirm:' + constants.CEND)
    element.click()
    time.sleep(2)

def enter_using_fb(driver, element):
    element.click()
    try:
        type2_click_continue(driver, element, 'enter_using_fb')
        time.sleep(2)
        element.click()# Just to be double sure incase the form comes up
    except Exception as e:
        myprint(constants.CGREEN + 'enter_using_fb: FAILED, SEEMS TO BE NEW TYPE' + constants.CEND, e)
        element.click()

def one_button_followed_by_one_continue(driver, element, ctr):
    try:
        all_expandables = driver.find_elements_by_css_selector('div.body-widget > div > div > div.popup-blocks-container > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(3) > div > div > div.expandable')
        current_expandable = all_expandables[ctr]
        if not current_expandable.is_displayed():
            element.click()
    except Exception as e:
        myprint("Possibly no expandable case came here" , e)
        return
    buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div > p:nth-child(2) > a")
    if len(buttons) == 0:
        buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content.center > div:nth-child(2) > p > a")
    if len(buttons) == 0:
        buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content.center > div:nth-child(2) > a")
    if len(buttons) == 0:
        buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div:nth-child(1) > div > p:nth-child(3) > a")
    if len(buttons) == 0:
        buttons = element.find_elements_by_css_selector("div > div > form > div:nth-child(1) > a")

    time.sleep(2)

    if len(buttons) > 0:
        time.sleep(2)

        myprint(buttons[0].get_attribute("href"))
        with open("data/links.txt", "a") as myfile:
            myfile.write(buttons[0].get_attribute("href") + '\n')

        action = ActionChains(driver)
        action.move_to_element(buttons[0]).perform()
        action.click().perform()
        myprint(constants.CGREEN + 'one_button_followed_by_one_continue: buttons clicked' + constants.CEND)

        time.sleep(constants.DOWNLOAD_WAIT)

        if typeX_click_continue(driver, element, ctr, 'one_button_followed_by_one_continue') == False:
            raise Exception("Expandable not closing")
        time.sleep(2)
    else:
        myprint(constants.CRED + "one_button_followed_by_one_continue is throwing error, lets debug" + constants.CEND)
        if current_expandable.is_displayed():
            element.click()
        time.sleep(2)

def one_button_one_textbox_one_continue(driver, element, ctr):
    try:
        all_expandables = driver.find_elements_by_css_selector('div.body-widget > div > div > div.popup-blocks-container > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(3) > div > div > div.expandable')
        current_expandable = all_expandables[ctr]
        if not current_expandable.is_displayed():
            element.click()
    except Exception as e:
        myprint("Pssibly no expandable case came here" , e)
        return
    buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div > p:nth-child(2) > a")
    if len(buttons) == 0:
        buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content.center > div:nth-child(2) > p > a")
    if len(buttons) == 0:
        buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content.center > div:nth-child(2) > a")
    if len(buttons) == 0:
        buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div:nth-child(1) > div > p:nth-child(3) > a")
    if len(buttons) == 0:
        buttons = element.find_elements_by_css_selector("div > div > form > div:nth-child(1) > a")

    time.sleep(2)

    if len(buttons) > 0:
        time.sleep(2)

        myprint(buttons[0].get_attribute("href"))
        with open("data/links.txt", "a") as myfile:
            myfile.write(buttons[0].get_attribute("href") + '\n')

        action = ActionChains(driver)
        action.move_to_element(buttons[0]).perform()
        action.click().perform()
        myprint(constants.CGREEN + 'one_button_followed_by_one_continue: buttons clicked' + constants.CEND)
        time.sleep(constants.DOWNLOAD_WAIT)

        textareas = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div:nth-child(2) > div > div > textarea")
        if len(textareas) == 0:
            textareas = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div:nth-child(2) > div > div > label > textarea")
        if len(textareas) > 0:
            textareas[0].clear()
            textareas[0].send_keys(constants.FB_ID)
            time.sleep(2)

        typeX_click_continue(driver, element, ctr, 'one_button_followed_by_one_continue')
        time.sleep(2)
    else:
        myprint(constants.CRED + "closing now, debug later" + constants.CEND)
        if current_expandable.is_displayed():
            element.click()
        time.sleep(2)

def register_or_share_post_fb(driver, element, ctr):
    one_button_followed_by_one_continue(driver, element, ctr)

def join_telegram(driver, element):
    element.click()
    like_fb_page_buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div > p:nth-child(2) > a")
    time.sleep(2)
    myprint(like_fb_page_buttons[0].get_attribute("href"))
    with open("data/links.txt", "a") as myfile:
        myfile.write(like_fb_page_buttons[0].get_attribute("href") + '\n')
    action = ActionChains(driver)
    action.move_to_element(like_fb_page_buttons[0]).perform()
    action.click().perform()
    myprint(constants.CGREEN + 'join_telegram button clicked' + constants.CEND)
    time.sleep(20)

    input_boxes = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div:nth-child(2) > div > div > div > input")
    if len(input_boxes) == 0:
        input_boxes = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div:nth-child(2) > div > div > textarea")
    if len(input_boxes) > 0:
        input_boxes[0].clear()
        input_boxes[0].send_keys(constants.TELEGRAM_ID)
        time.sleep(2)

    type1_click_continue(driver, element, 'join_telegram')
    time.sleep(2)

def join_crew(driver, element):
    #TODO: Click to open was not required as was already found open on page load needs investigation wwhy
    type0_click_continue(driver, element, 'join_crew')

def liking_fb_page_only(driver, element, ctr):
    one_button_followed_by_one_continue(driver, element, ctr)

def like_fb_page(driver, element, ctr):
    one_button_one_textbox_one_continue(driver, element, ctr)

def embeded_click_or_one_button_followed_by_one_continue(driver, element, ctr):
    try:
        all_expandables = driver.find_elements_by_css_selector('div.body-widget > div > div > div.popup-blocks-container > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(3) > div > div > div.expandable')
        current_expandable = all_expandables[ctr]
        if not current_expandable.is_displayed():
            element.click()
    except Exception:
        pass

    time.sleep(5)
    if is_done(element) == False: # Note: it is Second isDone
        buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div > p:nth-child(2) > a")
        if len(buttons) == 0:
            buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content.center > div:nth-child(2) > p > a")
        if len(buttons) == 0:
            buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content.center > div:nth-child(2) > a")
        if len(buttons) == 0:
            buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div:nth-child(1) > div > p:nth-child(3) > a")
        if len(buttons) == 0:
            buttons = element.find_elements_by_css_selector("div > div > form > div:nth-child(1) > a")
        if len(buttons) == 0:
            buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div > p > a")
        if len(buttons) == 0:
            buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div > div > p > a")
        time.sleep(2)

        if len(buttons) > 0:
            time.sleep(2)

            myprint(buttons[0].get_attribute("href"))
            with open("data/links.txt", "a") as myfile:
                myfile.write(buttons[0].get_attribute("href") + '\n')

            action = ActionChains(driver)
            action.move_to_element(buttons[0]).perform()
            action.click().perform()
            myprint(constants.CGREEN + 'embeded_click_or_one_button_followed_by_one_continue: buttons clicked' + constants.CEND)

            time.sleep(constants.DOWNLOAD_WAIT)

            typeX_click_continue(driver, element, ctr, 'embeded_click_or_one_button_followed_by_one_continue')
            time.sleep(2)
        else:
            myprint(constants.CRED + "Mmmm embeded_click_or_one_button_followed_by_one_continue is throwing erroe, lets debug" + constants.CEND)
            time.sleep(2)
    else:
        myprint(constants.CGREEN + 'embeded_click_or_one_button_followed_by_one_continue: Just embeded clicking did it' + constants.CEND)

def is_current_expandable_open(driver, element, ctr):
    try:
        all_expandables = driver.find_elements_by_css_selector('div.body-widget > div > div > div.popup-blocks-container > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(3) > div > div > div.expandable')
        current_expandable = all_expandables[ctr]
        return current_expandable.is_displayed()
    except Exception:
        pass
    return False

def get_buttons_inside_expandable(driver, element, ctr):
    buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div > p:nth-child(2) > a")
    if len(buttons) == 0:
        buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content.center > div:nth-child(2) > p > a")
    if len(buttons) == 0:
        buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content.center > div:nth-child(2) > a")
    if len(buttons) == 0:
        buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div:nth-child(1) > div > p:nth-child(3) > a")
    if len(buttons) == 0:
        buttons = element.find_elements_by_css_selector("div > div > form > div:nth-child(1) > a")
    if len(buttons) == 0:
        buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div > p > a")
    if len(buttons) == 0:
        buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div > div > p > a")
    time.sleep(2)
    return buttons

def click_buttons_inside_expandable(driver, buttons):
    time.sleep(2)

    myprint(buttons[0].get_attribute("href"))
    with open("data/links.txt", "a") as myfile:
        myfile.write(buttons[0].get_attribute("href") + '\n')

    action = ActionChains(driver)
    action.move_to_element(buttons[0]).perform()
    action.click().perform()
    myprint(constants.CGREEN + 'embeded_click_or_one_button_followed_by_one_continue: buttons clicked' + constants.CEND)

    time.sleep(constants.DOWNLOAD_WAIT)

def get_question_followedby_textarea_inside_expandable(driver, element, ctr):
    qn = element.find_elements_by_css_selector("div > div > form > div.form-compact__content.center > div.form-compact__part.ng-scope > div > div > label")
    if len(qn) > 0:
        qntext = qn[0].text
    else:
        qntext = ""

    textareas = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div:nth-child(2) > div > div > textarea")
    if len(textareas) == 0:
        textareas = element.find_elements_by_css_selector("div > div > form > div.form-compact__content.center > div.form-compact__part.ng-scope > div > div > div > textarea")
    if len(textareas) == 0:
        textareas = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div:nth-child(2) > div > div > label > textarea")
    return qntext, textareas

def fill_textarea_inside_expandable(textareas, ans):
    textareas[0].clear()
    textareas[0].send_keys(ans)
    time.sleep(2)

def get_continue_button_in_form_action_area(driver, element, ctr):
    continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > button")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div.form-actions > button.btn-primary")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > div > a")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > a")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > div > a.btn-primary")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > button:nth-child(2)")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div.body-widget > div > div > div > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(2) > div > form > div > span:nth-child(1) > button")
    if len(continue_buttons) == 0:
        continue_buttons = element.find_elements_by_css_selector("div > div > form > div > span:nth-child(1) > button")
    return continue_buttons

def is_continue_button_in_form_action_area_enabled(continue_buttons):
    return not (continue_buttons[0].get_attribute("disabled") in ["true","disabled"])

def click_continue_button_in_form_action_area(driver, continue_buttons):
    if len(continue_buttons) == 0:
        return False
    for button in continue_buttons:
        if button.text == 'Continue' or button.text == 'Save':
            action = ActionChains(driver)
            action.move_to_element(button)
            action.click().perform()
            myprint(constants.CGREEN + 'click_continue_button_in_form_action_area: continue clicked' + constants.CEND)
            time.sleep(2)
            return True
    return False

def get_checkboxes(driver, element, ctr):
    all_expandables = driver.find_elements_by_css_selector('div.body-widget > div > div > div.popup-blocks-container > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(3) > div > div > div.expandable')
    current_expandable = all_expandables[ctr]

    rows = current_expandable.find_elements_by_css_selector("div > div > form > fieldset.inputs > div.form-horizontal > div > div > div")
    tot_checkboxes = []
    for row in rows:
        checkboxes = row.find_elements_by_css_selector("div > div > label.checkbox > span.icon")
        tot_checkboxes = tot_checkboxes.append(checkboxes)
    return tot_checkboxes

def check_checkboxes(checkboxes):
    for checkbox in checkboxes:
        checkbox.click()

def get_ans_for_qn(qn):
    return constants.FB_ID

def is_inline_form_open(driver, element, ctr):
    all_expandables = driver.find_elements_by_css_selector('div.body-widget > div > div > div.popup-blocks-container > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(3) > div > div > div.expandable')
    if len(all_expandables) > 0:
        try:
            form = all_expandables[ctr].find_elements_by_css_selector("div > form.contestant")
            if len(form) > 0:
                return form[0].is_displayed()
            else:
                return False
        except:
            return False
    else:
        return False

def generic(driver, element, ctr):
    if is_current_expandable_open(driver, element, ctr) == False:
        element.click()
        time.sleep(2)

    if is_done(element) == False:
        if is_inline_form_open(driver, element, ctr):
            fill_inline_form(driver, ctr)

        q_n_a = get_question_followedby_textarea_inside_expandable(driver, element, ctr)
        if len(q_n_a) == 2 and q_n_a[0] != '':
            ans = get_ans_for_qn(q_n_a[0])
            fill_textarea_inside_expandable(q_n_a[1], ans)

        buttons = get_buttons_inside_expandable(driver, element, ctr)
        if len(buttons) > 0:
            click_buttons_inside_expandable(driver, buttons)
            continue_buttons = get_continue_button_in_form_action_area(driver, element, ctr)
            if len(continue_buttons) > 0:
                if is_continue_button_in_form_action_area_enabled(continue_buttons) == True:
                    click_continue_button_in_form_action_area(driver, continue_buttons)

    else:
        myprint(constants.CGREEN + 'generic: Just embeded clicking did it' + constants.CEND)

    if is_current_expandable_open(driver, element, ctr) == True:
        element.click()
        time.sleep(2)

def follow_on_twitchtv(driver, element):
    element.click()
    time.sleep(2)
    element.click()
    if is_done(element) == False: # Note: it is Second isDone
        try:
            element.click()
            follow_on_twitter_buttons = element.find_elements_by_css_selector("div.expandable > div > div > div > div:nth-child(1) > div > a:nth-child(1)")
            time.sleep(2)
            myprint(follow_on_twitter_buttons[0].get_attribute("href"))
            with open("data/links.txt", "a") as myfile:
                myfile.write(follow_on_twitter_buttons[0].get_attribute("href") + '\n')
            action = ActionChains(driver)
            action.move_to_element(follow_on_twitter_buttons[0]).perform()
            action.click().perform()
            myprint(constants.CGREEN + 'follow_on_twitter clicked(lets wait 5 sec)' + constants.CEND)
            time.sleep(2)
            element.click()
        except Exception:
            myprint(constants.CGREEN + 'follow_on_twitchtv: COULDNT do due to popup' + constants.CEND)
    else:
        myprint(constants.CGREEN + 'follow_on_twitchtv: Just embeded clicking did it' + constants.CEND)

def subscribe(driver, element, ctr):
    one_button_followed_by_one_continue(driver, element, ctr)

def follow_on_instagram(driver, element, ctr):
    embeded_click_or_one_button_followed_by_one_continue(driver, element, ctr)

def follow_on_twitter(driver, element, ctr):
    embeded_click_or_one_button_followed_by_one_continue(driver, element, ctr)

def follow_on_linkedin(driver, element, ctr):
    embeded_click_or_one_button_followed_by_one_continue(driver, element, ctr)

def view_post_on_fb(driver, element, ctr):
    element.click()
    visit_fb_buttons = element.find_elements_by_css_selector("#u_0_3 > div > div.lfloat._ohe > span > div._6ks > a > div > div > img")
    time.sleep(2)
    if len(visit_fb_buttons) > 0:
        myprint(visit_fb_buttons[0].get_attribute("href"))
        with open("data/links.txt", "a") as myfile:
            myfile.write(visit_fb_buttons[0].get_attribute("href") + '\n')
        action = ActionChains(driver)
        if len(visit_fb_buttons) > 0:
            action.move_to_element(visit_fb_buttons[0]).perform()
            action.click().perform()
            myprint(constants.CGREEN + 'view_post_on_fb: visit_fb_buttons clicked' + constants.CEND)
            time.sleep(2)
        else:
            element.click()
            myprint(constants.CGREEN + 'view_post_on_fb: COULDNT click image' + constants.CEND)
            return
    type3_click_continue(driver, element, 'view_post_on_fb')
    time.sleep(2)

def visit_instagram_pinterest_gplus(driver, element, ctr):
    one_button_followed_by_one_continue(driver, element, ctr)

def check_plan(driver, element, ctr):
    one_button_followed_by_one_continue(driver, element, ctr)

def download(driver, element, ctr):
    one_button_followed_by_one_continue(driver, element, ctr)

def create_account(driver, element, ctr):
    one_button_followed_by_one_continue(driver, element, ctr)

def comment(driver, element):
    element.click()
    comment_buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div > p:nth-child(2) > a")
    if len(comment_buttons) > 0:
        time.sleep(2)
        myprint(comment_buttons[0].get_attribute("href"))
        with open("data/links.txt", "a") as myfile:
            myfile.write(comment_buttons[0].get_attribute("href") + '\n')
        action = ActionChains(driver)
        action.move_to_element(comment_buttons[0]).perform()
        action.click().perform()
        myprint(constants.CGREEN + 'comment: comment_buttons clicked' + constants.CEND)
        time.sleep(2)
        type2_click_continue(driver, element, 'comment')
    else:#inline comment case
        comment_boxes = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div.form-compact__part.input.string.optional.form-group > div > input")
        if len(comment_boxes) > 0:
            comment_boxes[0].send_keys("Great job , keep it up.." + constants.GOOG_ID + "..")
            time.sleep(2)
            type2_click_continue(driver, element, 'comment')

def visit(driver, element, ctr):
    one_button_followed_by_one_continue(driver, element, ctr)

def visit_fb(driver, element, ctr):
    one_button_followed_by_one_continue(driver, element, ctr)

def subscribe_with_only_continue_button(driver, element):
    element.click()
    try:
        type0_click_continue(driver, element, 'subscribe_with_only_continue_button')
        time.sleep(2)
        element.click()# Just to be double sure incase the form comes up
    except Exception as e:
        myprint(constants.CRED + 'subscribe_with_only_continue_button: FAILED, SEEMS TO BE NEW TYPE' + constants.CEND, e)
        element.click()

def fb_instagram_photoview(driver, element):
    element.click()
    try:
        myprint("Just Waiting is enough")
        time.sleep(constants.CONTINUE_ACTIVATE_WAIT)
        type0_click_continue(driver, element, 'subscribe_with_only_continue_button')
        time.sleep(2)
        element.click()# Just to be double sure incase the form comes up
    except Exception as e:
        myprint(constants.CRED + 'subscribe_with_only_continue_button: FAILED, SEEMS TO BE NEW TYPE' + constants.CEND, e)
        element.click()

def check_store(driver, element):
    myprint(constants.CGREEN + 'check_store:' + constants.CEND)
    element.click()#Thats all
    time.sleep(constants.FB_WAIT)
    type1_click_continue(driver, element, patt = '')

def check_store_amazon(driver, element, ctr):
    myprint(constants.CGREEN + 'check_store_amazon:')
    like_fb_page(driver, element, ctr) #Hack

def answer_qn(driver, element):
    element.click()
    text_area = element.find_elements_by_css_selector("div.form-compact__part > div.text > div.form-wrapper > textarea")
    time.sleep(2)
    ans=["Great Job", "I think it can be better", "Well I'm not very sure about it", "No idea whatsoever"]
    text_area[0].clear()
    text_area[0].send_keys(random.choice(ans))
    myprint(constants.CGREEN + 'answer_qn: answer_qn typed' + constants.CEND)
    time.sleep(2)
    type1_click_continue(driver, element, 'answer_qn')
    time.sleep(2)

def email_qn(driver, element):
    element.click()
    text_area = element.find_elements_by_css_selector("div.form-compact__part > div.text > div.form-wrapper > textarea")
    time.sleep(2)
    text_area[0].clear()
    text_area[0].send_keys(constants.GOOG_ID+'@gmail.com')
    myprint(constants.CGREEN + 'email_qn: email_qn typed' + constants.CEND)
    time.sleep(2)
    type1_click_continue(driver, element, 'email_qn')
    time.sleep(2)

def full_contact(driver, element):
    element.click()
    text_area = element.find_elements_by_css_selector("div.form-compact__part > div.text > div.form-wrapper > textarea")
    time.sleep(2)
    text_area[0].clear()
    text_area[0].send_keys(constants.GOOG_ID+'@gmail.com, ' + constants.MOB)
    myprint(constants.CGREEN + 'full_contact: full_contact typed' + constants.CEND)
    time.sleep(2)
    type1_click_continue(driver, element, 'full_contact')
    time.sleep(2)

def retweet(driver, element, ctr):
    embeded_click_or_one_button_followed_by_one_continue(driver, element, ctr)

def follow_on_mixer(driver, element):
    myprint(constants.CGREEN + 'follow_on_mixer: WONT DO' + constants.CEND)

def newsletter(driver, element):
    element.click()
    time.sleep(2)
    checkboxes = element.find_elements_by_css_selector("label.checkbox > span.icon")
    if len(checkboxes) > 0:
        try:
            checkboxes[0].click()
        except Exception:
            myprint(constants.CRED + "The checkbox might be hidden" + constants.CEND)
    else:
        myprint("It doesnt have checkbxes, lets try signup")
        signup_buttons = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div > p:nth-child(2) > a")
        if len(signup_buttons) == 0:
            signup_buttons = element.find_elements_by_css_selector("div > div > form > div:nth-child(1) > div:nth-child(2) > a")
        time.sleep(2)
        if len(signup_buttons) > 0:
            myprint(signup_buttons[0].get_attribute("href"))
            with open("data/links.txt", "a") as myfile:
                myfile.write(signup_buttons[0].get_attribute("href") + '\n')
            action = ActionChains(driver)
            action.move_to_element(signup_buttons[0]).perform()
            action.click().perform()
        else:
            myprint(constants.CRED + "It doesnt have signup either, lets go for continue directly" + constants.CEND)

    myprint(constants.CGREEN + 'newsletter_pattern: checkbox/signup/none clicked' + constants.CEND)
    time.sleep(2)
    type0_click_continue(driver, element, 'newsletter_pattern')
    time.sleep(2)

def refer_friends(element, header):
    element.click()
    time.sleep(4) #Because it is taking lot of time to fetch the url
    try:
        sharelinks = element.find_elements_by_css_selector("div.share-link__link")
        myprint(constants.CGREEN + "REFERAL LINK:" + constants.CEND, sharelinks[0].text)
        with open("data/links.txt", "a") as myfile:
            myfile.write(sharelinks[0].text + ', ' + header.text + '\n')
    except Exception:
        myprint(constants.CRED + "refer_friends_pattern: SEEMS TO BE A DIFFERENT FORM . YOU HAVE TO ENTER COMPLETE DETAILS:" + constants.CEND)
    element.click()

def play_steam(driver, element):
    body = driver.find_element_by_tag_name("body")
    body.send_keys(Keys.COMMAND + 't')

    element.click()
    time.sleep(2)
    try:
        type4a_click_continue(driver, element, 'play_steam_pattern')
        time.sleep(2)
    except Exception:
        element.click()

def click_for_bonus(driver, element, ctr):
    myprint(constants.CGREEN + 'click_for_bonus_pattern:' + constants.CEND)
    element.click()
    time.sleep(2)
    with open("data/daily_links.txt", "a") as myfile:
        myfile.write(driver.current_url + ', ' + str(ctr) +'\n')

def fill_inline_form(driver, ctr):
    all_expandables = driver.find_elements_by_css_selector('div.body-widget > div > div > div.popup-blocks-container > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(3) > div > div > div.expandable')
    try:
        current_expandable = all_expandables[ctr]
        if current_expandable.is_displayed():
            rows = current_expandable.find_elements_by_css_selector("div > div > form > fieldset.inputs > div.form-horizontal > div > div > div")
            for row in rows:
                labels = row.find_elements_by_css_selector("div > label")
                if len(labels) == 0:
                    continue# Note laa checkboxes will have label
                if labels[0].text.strip() == "Full Name":
                    name_boxes = row.find_elements_by_css_selector("div > input")
                    if len(name_boxes) > 0:
                        name_boxes[0].clear()
                        name_boxes[0].send_keys(constants.FULL_NAME)
                elif labels[0].text.strip() == "Email":
                    email_boxes = row.find_elements_by_css_selector("div > input")
                    if len(email_boxes) > 0:
                        email_boxes[0].clear()
                        email_boxes[0].send_keys(constants.GOOG_ID + "@gmail.com")
                elif labels[0].text.strip() == "Confirm Email":
                    email_boxes = row.find_elements_by_css_selector("div > input")
                    if len(email_boxes) > 0:
                        email_boxes[0].clear()
                        email_boxes[0].send_keys(constants.GOOG_ID + "@gmail.com")
                elif labels[0].text.strip() == "Date of birth":
                    dob_boxes = row.find_elements_by_css_selector("div > input")
                    dob_formats = row.find_elements_by_css_selector("div > div")
                    if len(dob_boxes) > 0:
                        dob_boxes[0].clear()
                        if re.compile("MM/DD/YYYY").match(dob_formats[0].text.split('\n')[-1]) != None:
                            dob_boxes[0].send_keys(constants.DOB_MMDDYY)
                        else:
                            dob_boxes[0].send_keys(constants.DOB)
                elif labels[0].text.strip() == "Phone":
                    phone_boxes = row.find_elements_by_css_selector("div > input")
                    if len(phone_boxes) > 0:
                        phone_boxes[0].clear()
                        phone_boxes[0].send_keys(constants.MOB)
                elif labels[0].text.strip() == "Zip":
                    zip_boxes = row.find_elements_by_css_selector("div > input")
                    if len(zip_boxes) > 0:
                        zip_boxes[0].clear()
                        zip_boxes[0].send_keys(constants.ZIP)
                elif re.compile("I agree to.*|I have read.*").match(labels[0].text.strip()) != None:
                    mandatory_checkboxes = row.find_elements_by_css_selector("div > div > label.checkbox > input")
                    if len(mandatory_checkboxes) > 0:
                        for mandatory_checkbox in mandatory_checkboxes:
                            if not mandatory_checkbox.is_selected():
                                mandatory_checkbox.find_element_by_xpath('..').click()
                    else:
                        myprint("No checkbox found")
                elif len(row.find_elements_by_css_selector("div > div > label.checkbox > span.icon")) > 0:
                    other_checkboxes = row.find_elements_by_css_selector("div > div > label.checkbox > input")
                    for other_checkbox in other_checkboxes:
                        if not other_checkbox.is_selected():
                            other_checkbox.find_element_by_xpath('..').click()
                elif len(row.find_elements_by_css_selector("div > div > select")) > 0:
                    select_doms = current_expandable.find_elements_by_css_selector("div > div > select")
                    if select_doms[0].is_displayed():
                        select_fr = Select(select_doms[0])
                        if select_fr:
                            select_fr.select_by_index(104)
                else:
                    myprint("Unrecognised Row")

            if type6_click_continue(driver, current_expandable, "fill_inline_form") == False:
                return False

            time.sleep(5)

            fb_account_selection = driver.find_elements_by_css_selector("div.body-widget > div > div > div.popup-blocks-container > div > div:nth-child(1) > div:nth-child(2) > div > ul > li > a.facebook-border")
            if len(fb_account_selection) > 0:
                fb_account_selection[0].click()
                time.sleep(5)
            else:
                myprint("FB account not found")
        else:
            return "NoForm"
    except Exception as e:
        myprint("fill_inline_form:", e, current_expandable)
        return "CouldntForm"
    return "FilledForm"

def fill_global_form(driver):
    global_forms = driver.find_elements_by_css_selector("body > div.body-widget > div > div > div > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(2) > div > form")

    if len(global_forms) > 0:
        try:
            name_boxes = global_forms[0].find_elements_by_css_selector("div.body-widget > div > div > div > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(2) > div > form > fieldset.inputs > div.form-horizontal > div > div > div:nth-child(1) > div > input")
            if len(name_boxes) > 0:
                name_boxes[0].clear()
                name_boxes[0].send_keys(constants.FULL_NAME)

            email_boxes = global_forms[0].find_elements_by_css_selector("div.body-widget > div > div > div > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(2) > div > form > fieldset.inputs > div.form-horizontal > div > div > div:nth-child(2) > div > input")
            if len(email_boxes)  > 0:
                email_boxes[0].clear()
                email_boxes[0].send_keys(constants.GOOG_ID + "@gmail.com")

            dob_boxes = global_forms[0].find_elements_by_css_selector("div.body-widget > div > div > div > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(2) > div > form > fieldset.inputs > div.form-horizontal > div > div > div:nth-child(3) > div > div > input")
            dob_formats = global_forms[0].find_elements_by_css_selector("div.body-widget > div > div > div > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(2) > div > form > fieldset.inputs > div.form-horizontal > div > div > div:nth-child(3) > div > div > div")
            if len(dob_boxes) > 0:
                dob_boxes[0].clear()
                if dob_formats[0].text.strip() == 'MM/DD/YYYY':
                    dob_boxes[0].send_keys(constants.DOB_MMDDYY)
                else:
                    dob_boxes[0].send_keys(constants.DOB)

            mandatory_checkboxes = global_forms[0].find_elements_by_css_selector("div > form > fieldset.inputs > div.form-horizontal > div > div > div:nth-child(3) > div > div > label > span.icon")
            if len(mandatory_checkboxes) > 0:
                mandatory_checkboxes[0].click()

            if type5_click_continue(driver, global_forms[0], "global_forms") == False:
                myprint("Form can not be saved")

            time.sleep(5)

            fb_account_selection = driver.find_elements_by_css_selector("div.body-widget > div > div > div > div > div:nth-child(1) > div:nth-child(2) > div > ul > li:nth-child(1) > a.facebook-border")
            if len(fb_account_selection) == 0:
                fb_account_selection = driver.find_elements_by_css_selector("div.body-widget > div > div > div.popup-blocks-container > div > div:nth-child(1) > div > div > ul > li > a.facebook-border")

            if len(fb_account_selection) > 0:
                fb_account_selection[0].click()
                time.sleep(5)
            else:
                myprint("FB account not found")
        except Exception:
            pass

def is_not_abailable(driver):
    try:
        is_not_available =  driver.find_element_by_css_selector("div.body-widget > div > div > div.popup-blocks-container > div > div:nth-child(1) > div:nth-child(6) > div.center.massive-message.light-grey-bg.ng-scope > h2")
        if is_not_available_pattern.match(is_not_available.text.lower().strip()) != None:
            return True
    except Exception:
        pass
    return False

def has_ended(driver):
    try:
        has_ended =  driver.find_element_by_css_selector("div.body-widget > div > div > div > div > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(1) > div > h2")
        if has_ended_pattern.match(has_ended.text.lower().strip()) != None:
            return True
    except Exception:
        pass
    return False

def check_for_captchas(driver, d):
    captchas = driver.find_elements_by_css_selector('div.grecaptcha')
    if len(captchas) > 0 and captchas[0].is_displayed():
        if 'headless' in d:
            myprint("Exiting due to captcha encountered...")
            sys.exit(0)
        else:
            input("Press enter once captcha is solved...")

def loop_elements(driver, d, cnt):
    header = driver.find_element_by_css_selector("div.body-widget > div > div > div.popup-blocks-container > div > div:nth-child(1) > div:nth-child(6) > div.prize-area.ng-scope > div > div > h3")
    elements = driver.find_elements_by_css_selector("div.entry-method")
    for ctr, element in enumerate(elements):
        if 'sleep' in d:
            time.sleep(random.randint(1, constants.ANTIFRAUD_FUZZY_SLEEP_LIMIT/10))
        action = ActionChains(driver)
        action.move_to_element(element).perform()
        children  = element.find_elements_by_css_selector("a > span.text")
        txt = children[0].text.lower().strip()

        fill_state = fill_inline_form(driver, ctr)
        if is_done(element) == True:
            myprint(constants.CGREEN + 'ALREADY DONE:' + constants.CEND, txt)
        else:
            try:
                if visit_fb_pattern.match(txt) != None:
                    visit_fb(driver, element, ctr)
                elif join_live_pattern.match(txt) != None:
                    one_button_one_textbox_one_continue(driver, element, ctr)
                elif view_post_on_fb_pattern.match(txt) != None:
                    view_post_on_fb(driver, element, ctr)
                elif liking_fb_page_only_pattern.match(txt) != None:
                    liking_fb_page_only(driver, element, ctr)
                elif like_fb_page_pattern.match(txt) != None:
                    like_fb_page(driver, element, ctr)
                elif register_pattern.match(txt) != None:
                    register_or_share_post_fb(driver, element,ctr)
                elif join_telegram_pattern.match(txt) != None:
                    join_telegram(driver, element)
                elif answer_qn_pattern.match(txt) != None or is_answer(element):
                    answer_qn(driver, element)
                elif email_qn_pattern.match(txt) != None:
                    email_qn(driver, element)
                elif full_contact_pattern.match(txt) != None:
                    full_contact(driver, element)
                elif share_post_fb_pattern.match(txt) != None:
                    register_or_share_post_fb(driver, element, ctr)
                elif enter_using_fb_pattern.match(txt) != None:
                    enter_using_fb(driver, element)
                elif click_to_confirm_pattern.match(txt) != None:
                    click_to_confirm(driver, element)
                elif fb_instagram_photoview_pattern.match(txt) != None:
                    fb_instagram_photoview(driver, element)
                elif visit_instagram_pattern.match(txt) != None or  visit_pinterest_pattern.match(txt) != None or  visit_gplus_pattern.match(txt) != None:
                    visit_instagram_pinterest_gplus(driver, element, ctr)
                elif click_for_bonus_pattern.match(txt) != None:
                    click_for_bonus(driver, element, ctr)
                elif follow_on_twitter_pattern.match(txt) != None or follow_on_tumblr_pattern.match(txt) != None:
                    follow_on_twitter(driver, element, ctr)
                elif follow_on_instagram_pattern.match(txt) != None:
                    follow_on_instagram(driver, element, ctr)
                elif follow_on_linkedin_pattern.match(txt) != None:
                    follow_on_linkedin(driver, element, ctr)
                elif follow_on_mixer_pattern.match(txt) != None:
                    follow_on_mixer(driver, element)
                elif follow_on_twitchtv_pattern.match(txt) != None:
                    follow_on_twitchtv(driver, element)
                elif subscribe_pattern.match(txt) != None:
                    subscribe(driver, element, ctr)
                elif retweet_pattern.match(txt) != None:
                    retweet(driver, element, ctr)
                elif visit_giveaways_pattern.match(txt) != None:
                    visit(driver, element, ctr)
                elif check_store_amazon_pattern.match(txt) != None:
                    check_store_amazon(driver, element, ctr)
                elif check_store_pattern.match(txt) != None:
                    check_store(driver, element)
                elif check_plan_pattern.match(txt) != None:
                    check_plan(driver, element, ctr)
                elif check_board_game_pattern.match(txt) != None:
                    myprint(constants.CGREEN + 'check_board_game_pattern TODO' + constants.CEND)
                elif download_pattern.match(txt) != None:
                    download(driver, element, ctr)
                elif comment_pattern.match(txt) != None and is_youtube(element) == False:
                    comment(driver, element)
                elif visit_pattern.match(txt) != None or confirm_details_pattern.match(txt) != None:
                    visit(driver, element, ctr)
                elif create_account_pattern.match(txt) != None:
                    create_account(driver, element, ctr)
                elif refer_friends_pattern.match(txt) != None:
                    refer_friends(element, header)
                elif newsletter_pattern.match(txt) != None:
                    newsletter(driver, element)
                elif (watch_pattern.match(txt) != None or checkout_video_pattern.match(txt) != None) and is_youtube(element):
                    myprint(constants.CGREEN + 'Videos if not done yet, will be played in next pass(es)' + constants.CEND)
                    with open("data/video_page_links.txt", "a") as myfile:
                        myfile.write(driver.current_url + '\n')
                elif checkout_video_pattern.match(txt) != None:
                    visit(driver, element, ctr)
                elif play_steam_pattern.match(txt) != None:
                    play_steam(driver, element)
                elif txt == "join our watch, win, & play tabletop games group":
                    join_telegram(driver, element)
                elif txt == "join the thurso surf crew":
                    join_crew(driver, element)
                elif is_external_link(element):
                    visit(driver, element, ctr)
                elif len(txt) > 0:
                    myprint(constants.CRED + 'NonMatching Element:' + constants.CEND, txt)
                    generic(driver, element, ctr)
                else:
                    myprint(constants.CRED + 'Locked Element:' + constants.CEND, txt)
            except Exception as e:
                myprint(constants.CRED + "Must be due to inner. trying generic" + constants.CEND, txt, e)
                generic(driver, element, ctr)
            try:
                check_for_captchas(driver, d)
                fill_state = fill_inline_form(driver, ctr)
                if fill_state == "FilledForm":
                    driver.execute_script("document.getElementsByClassName('expandable')[" + str(ctr) + "].style.visibility='hidden';")
                    check_for_captchas(driver, d)
                elif fill_state == "CouldntForm":
                    driver.execute_script("document.getElementsByClassName('expandable')[" + str(ctr) + "].style.visibility='hidden';")
                if is_daily_candidate(element):
                    with open("data/daily_links.txt", "a") as myfile:
                        myfile.write(driver.current_url + ', ' + str(ctr) +'\n')
            except Exception as e:
                myprint(constants.CRED + 'Seems there was no expandable here' + constants.CEND, e)

            driver.switch_to.window(driver.current_window_handle)

def open_url(driver, d, url, cnt):
    if 'sleep' in d:
        time.sleep(random.randint(10, constants.ANTIFRAUD_FUZZY_SLEEP_LIMIT))
    else:
        time.sleep(2)
    driver.get(url)
    myprint(driver.current_url)
    if is_not_abailable(driver):
        myprint("Is NOT AVAILABLE in your region")
        with open("data/invalid_links.txt", "a") as myfile:
            myfile.write(driver.current_url +'\n')
        return
    if has_ended(driver):
        myprint("This Competition has ended")
        with open("data/invalid_links.txt", "a") as myfile:
            myfile.write(driver.current_url +'\n')
        return
    if login(driver) == False:
        fill_global_form(driver)
    loop_elements(driver, d, cnt)

def crawl(driver, d):
    if 'n' in d:
        n_takeaways = int(d['n'])
    else:
        n_takeaways = 999

    if 'd' in d:
        n_rem_days = int(d['d'])
    else:
        n_rem_days = 8

    if 'sleep' in d:
        time.sleep(random.randint(100, constants.ANTIFRAUD_FUZZY_SLEEP_LIMIT*10))
    else:
        time.sleep(2)

    html_content = open("data/GleamioDB.html")
    body = BeautifulSoup(html_content, 'html.parser').body
    cnt = 0
    driver.get("https://google.com")

    load_cookie(driver, '/tmp/gleam_fb_cookie')
    load_cookie(driver, '/tmp/gleam_google_cookie')
    load_cookie(driver, '/tmp/gleam_twitter_cookie')
    load_cookie(driver, '/tmp/gleam_instagram_cookie')
    load_cookie(driver, '/tmp/gleam_soundcloud_cookie')
    load_cookie(driver, '/tmp/gleam_steampowered_cookie')

    rows = body.find_all('tr', attrs={})
    for row in rows:
        try:
            href = row.find("a")['href']
            cols = row.find_all("td")
            if int(cols[5].text) < n_rem_days:
                myprint("=====", cnt, "===", cols[1].text, "===", href, "===", int(cols[5].text), "=====")
                if cnt <= n_takeaways:
                    try:
                        if str(cols[2].text.lower().strip()) in ['worldwide', 'asia', 'india', 'some restrictions', '']:
                            open_url(driver, d, href, cnt)
                            if len(driver.window_handles) > 20:
                                driver = relaunch(driver, d)
                        else:
                            myprint("Oh Shit:", cols[2].text.lower().strip())
                            with open("data/invalid_links.txt", "a") as myfile:
                                myfile.write(driver.current_url +'\n')
                    except Exception as e:
                        myprint(constants.CRED + "do:" + constants.CEND, e)
                cnt = cnt + 1
        except Exception:
            pass

if __name__ == "__main__":
    argv = sys.argv[1:]
    d = {}
    for i in range(0, len(argv), 2):
        d[argv[i].replace('-', '')] = argv[i + 1]
    myprint(d)

    chrome_options = Options()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery")
    if 'headless' in d:
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=constants.CHROME_DRIVER_PATH)
    try:
        crawl(driver, d)
        myprint(constants.CGREEN + 'Main PEACEFULLY terminated' + constants.CEND)
    except Exception as e:
        myprint(e)
    driver.quit()

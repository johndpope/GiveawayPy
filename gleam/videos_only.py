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

checkout_video_pattern = re.compile("check out.*")
watch_pattern = re.compile("watch.*|video entry bonus|comment.*youtube.*")

is_not_available_pattern = re.compile("sorry.*is not available.*")
has_ended_pattern = re.compile(".*competition.*has.*ended")

def get_time():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

#Type4
def type4_click_continue(driver, element, patt=''):
    continue_buttons = element.find_elements_by_css_selector("div > div > form > div.form-actions.center > button")
    if len(continue_buttons) == 0:
        myprint("Continue button not found")
        return False
    click_button = continue_buttons[0]
    try:
        if len(continue_buttons)>=2:
            if continue_buttons[0].text == 'Continue':
                click_button = continue_buttons[0]
                click_button.get_attribute("class").split(' ').index('disabled')
            else:
                click_button = continue_buttons[1]
                click_button.get_attribute("class").split(' ').index('disabled')
        else:
            click_button = continue_buttons[0]
            click_button.get_attribute("class").split(' ').index('disabled')
        myprint("Still disabled")
        return False
    except:
        action = ActionChains(driver)
        action.move_to_element(click_button)
        action.click().perform()
        myprint(patt, 'type4_click_continue: continue clicked')
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

video_url_arr = []
with open(f'data/video_page_links.txt') as infile:
    for line in infile:
        video_url_arr.append(str(line))
random.shuffle(video_url_arr)

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

def is_youtube(element):
    potential_checks  = element.find_elements_by_css_selector("span i")
    for child in potential_checks:
        if('fa-youtube' in child.get_attribute("class").split(' ')):
            return True
    return False

def is_done(element):
    potential_checks  = element.find_elements_by_css_selector("span i")
    for child in potential_checks:
        if('fa-check' in child.get_attribute("class").split(' ')):
            return True
    return False

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

def watch(driver, element):
    element.click()
    time.sleep(2)

    sharelinks = element.find_elements_by_css_selector("div.cover-video-container > iframe")
    if len(sharelinks) == 0:
        sharelinks = element.find_elements_by_css_selector("divdiv > div > form > div.form-compact__content > div.form-compact__part.user-fragment.center.ng-binding.ng-scope > p > a")
    sharelinks[0].click()# play it
    osascript.osascript("set volume output volume 0")
    time.sleep(constants.RETRY_VIDEO_CONTINUE_WAIT)
    osascript.osascript("set volume output volume 20")

    #In case video has comments box
    input_boxes = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div:nth-child(2) > div > div > div > input")
    if len(input_boxes) == 0:
        input_boxes = element.find_elements_by_css_selector("div > div > form > div.form-compact__content > div:nth-child(2) > div > div > textarea")
    if len(input_boxes) > 0:
        input_boxes[0].clear()
        input_boxes[0].send_keys(constants.GOOG_ID + " . I'm loving it")
        time.sleep(2)

    has_clicked = False
    while has_clicked == False:
        has_clicked = type4_click_continue(driver, element,'watch_pattern')
        time.sleep(constants.RETRY_VIDEO_CONTINUE_WAIT)

    element.click()

def loop_video_elements_only(driver):
    elements = driver.find_elements_by_css_selector("div.entry-method")
    cnt = 0
    for ctr, element in enumerate(elements):
        action = ActionChains(driver)
        action.move_to_element(element).perform()
        children  = element.find_elements_by_css_selector("a > span.text")
        txt = children[0].text.lower().strip()
        if is_done(element) == False:
            try:
                if (watch_pattern.match(txt) != None or checkout_video_pattern.match(txt) != None) and is_youtube(element):
                    watch(driver, element)
            except Exception as e:
                myprint('Must be due to inner form case somwhere', e)
            try:
                driver.execute_script("document.getElementsByClassName('expandable')[" + str(ctr) + "].style.visibility='hidden';")
            except Exception as e:
                myprint('Seems there was no expandable here', e)
        if is_done(element) == True:
            cnt = cnt + 1
    if cnt == len(elements):
        return True
    return False

def open_url(driver, d, url, cnt):
    if 'sleep' in d:
        time.sleep(random.randint(10, constants.ANTIFRAUD_FUZZY_SLEEP_LIMIT))
    else:
        time.sleep(2)
    driver.get(url)
    myprint(driver.current_url)
    if is_not_abailable(driver):
        myprint("Is NOT AVAILABLE in your region")
        return
    if has_ended(driver):
        myprint("This Competition has ended")
        return
    if login(driver) == False:
        fill_global_form(driver)
    if loop_video_elements_only(driver) == True:
        myprint("DONE:", url)
        with open("data/video_page_links_done.txt", "a") as myfile:
            myfile.write(url + '\n')

def crawl(d):
    if 'sleep' in d:
        time.sleep(random.randint(100, constants.ANTIFRAUD_FUZZY_SLEEP_LIMIT*10))
    else:
        time.sleep(2)
    cnt = 0
    driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH)
    driver.get("https://google.com")

    load_cookie(driver, '/tmp/gleam_fb_cookie')
    load_cookie(driver, '/tmp/gleam_google_cookie')
    load_cookie(driver, '/tmp/gleam_twitter_cookie')
    load_cookie(driver, '/tmp/gleam_instagram_cookie')
    load_cookie(driver, '/tmp/gleam_soundcloud_cookie')
    load_cookie(driver, '/tmp/gleam_steampowered_cookie')

    for href in video_url_arr:
        try:
            myprint("==", href.replace('\n',''), "==")
            try:
                open_url(driver, d, href, cnt)
            except Exception as e:
                myprint(constants.CRED + "do:" + constants.CEND, e)
                pass
        except Exception:
            pass

    driver.quit()

if __name__ == "__main__":
    argv = sys.argv[1:]
    d = {}
    for i in range(0, len(argv), 2):
        d[argv[i].replace('-', '')] = argv[i + 1]
    myprint(d)
    crawl(d)
    myprint(constants.CGREEN + 'Main PEACEFULLY terminated' + constants.CEND)

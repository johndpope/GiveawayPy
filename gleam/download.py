import codecs
import os
import time
import os, datetime, time, sys, pickle

from selenium import webdriver
import constants
from commons import myprint

driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH)

def get_time():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def load_cookie(driver, path):
    with open(path, 'rb') as cookies_file:
        cookies = pickle.load(cookies_file)
        for cookie in cookies:
            driver.add_cookie(cookie)

driver.get("https://gleamdb.ga/")
load_cookie(driver, '/tmp/gleam_fb_cookie')
load_cookie(driver, '/tmp/gleam_google_cookie')
time.sleep(5)
driver.get("https://gleamdb.ga/")
time.sleep(5)
close_button = driver.find_element_by_css_selector('#modalclose')
close_button.click()
time.sleep(5)
driver.execute_script("window.scrollBy(0,250)", "")
time.sleep(5)

html = driver.page_source
complete_name = os.path.join(os.path.expanduser('data/'), 'GleamioDB.html')
file_object = codecs.open(complete_name, "w", "utf-8")
file_object.write(html)
driver.quit()

myprint("Download of GleamioDB completed")

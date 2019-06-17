import pickle
import os, time, datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import constants
from commons import myprint

def get_time():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)
    myprint(f'cookie saved at {path}')

def load_cookie(driver, path):
    with open(path, 'rb') as cookies_file:
        cookies = pickle.load(cookies_file)
        for cookie in cookies:
            driver.add_cookie(cookie)

driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH)

fb_url = "https://www.facebook.com/login.php"
driver.get(fb_url)
fb_email_element = driver.find_element_by_id("email")
fb_email_element.send_keys(constants.FB_ID)
fb_pass_element = driver.find_element_by_id("pass")
fb_pass_element.send_keys(constants.FB_PASS)
fb_pass_element.send_keys(Keys.ENTER)
save_cookie(driver, '/tmp/gleam_fb_cookie')
time.sleep(2)

goog_url = "https://accounts.google.com/signin/v2/identifier"
driver.get(goog_url)
goog_email_element = driver.find_element_by_id("identifierId")
goog_email_element.send_keys(constants.GOOG_ID)
goog_email_element.send_keys(Keys.ENTER)
time.sleep(2)
goog_pass_element = driver.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input")
goog_pass_element.send_keys(constants.GOOG_PASS)
goog_pass_element.send_keys(Keys.ENTER)
save_cookie(driver, '/tmp/gleam_google_cookie')
time.sleep(2)

twitter_url = "https://twitter.com/login?lang=en"
driver.get(twitter_url)
twitter_id_element = driver.find_element_by_css_selector("#page-container > div > div.signin-wrapper > form > fieldset > div:nth-child(2) > input")
twitter_id_element.send_keys(constants.TWTR_ID)
time.sleep(1)
twitter_pass_element = driver.find_element_by_css_selector("#page-container > div > div.signin-wrapper > form > fieldset > div:nth-child(3) > input")
twitter_pass_element.send_keys(constants.TWTR_PASS)
twitter_pass_element.send_keys(Keys.ENTER)
save_cookie(driver, '/tmp/gleam_twitter_cookie')
time.sleep(2)

load_cookie(driver, '/tmp/gleam_fb_cookie')
driver.get("https://www.instagram.com")
time.sleep(5)
insta_login_buttons = driver.find_elements_by_css_selector("#react-root > section > main > article > div > div:nth-child(1) > div > span > button > span")
insta_login_buttons[0].click()
time.sleep(constants.LOGIN_WAIT)
save_cookie(driver, '/tmp/gleam_instagram_cookie')
time.sleep(2)

load_cookie(driver, '/tmp/gleam_fb_cookie')
driver.get("https://soundcloud.com/signin")
time.sleep(5)
sound_login_buttons = driver.find_elements_by_css_selector("#content > div > div > div.l-main > form > div > div.signinForm__step.signinForm__initial > div > div.signinInitialStep__socialSignin > div.signinInitialStep__socialButtons > div:nth-child(1) > button")
sound_login_buttons[0].click()
time.sleep(constants.LOGIN_WAIT)
save_cookie(driver, '/tmp/gleam_soundcloud_cookie')
time.sleep(2)

driver.get("https://store.steampowered.com/login/")
steam_id_element = driver.find_element_by_css_selector("input#input_username")
steam_id_element.send_keys(constants.STEAM_ID)
time.sleep(1)
steam_pass_element = driver.find_element_by_css_selector("input#input_password")
steam_pass_element.send_keys(constants.STEAM_PASS)
steam_pass_element.send_keys(Keys.ENTER)
save_cookie(driver, '/tmp/gleam_steampowered_cookie')
time.sleep(2)

# driver.get("https://discordapp.com/login/")
# discord_email_element = driver.find_element_by_css_selector("input[type='email']")
# discord_email_element.send_keys(constants.DISCORD_ID)
# discord_pass_element = driver.find_element_by_css_selector("input[type='password']")
# discord_pass_element.send_keys(constants.DISCORD_PASS)
# discord_pass_element.send_keys(Keys.ENTER)
# save_cookie(driver, '/tmp/gleam_discord_cookie')
# input("Press enter when done filling captcha..")

driver.quit()

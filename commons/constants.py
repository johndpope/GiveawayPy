import configparser
config = configparser.ConfigParser()
config.read("config.txt")
LOGIN_WAIT = 10
CONTINUE_ACTIVATE_WAIT = 10
VIDEO_WAIT = 5 #130
DOWNLOAD_WAIT = 5 #120
CREATE_WAIT = 5 #50
LINKEDIN_WAIT = 5 #30
FB_WAIT = 5 #10
INSTA_WAIT = 5 #10
CHECK_PLAN_WAIT = 5 #120
VISIT_WAIT = 5 #120
TWEET_SPAM_LIMIT_WAIT = 50
SOCIAL_FOLLOW_LIMIT_WAIT = 0
RETRY_VIDEO_CONTINUE_WAIT = 10
FULL_NAME = 'Ishan Dutta'
FB_ID = 'ishandutta2007'
FB_PASS = config.get("configuration", "fb_ishandutta2007_password")
GOOG_ID = 'ishandutta2007'
GOOG_PASS = config.get("configuration", "goog_ishandutta2007_password")
AMZN_ID = 'ishandutta2007@gmail.com'
AMZN_PASS = config.get("configuration", "amzn_ishandutta2007atgmaildotcom_password")
TWTR_ID = 'passivemillion2'
TWTR_PASS = config.get("configuration", "twitter_passivemillion2_password")
STEAM_ID = 'ishandutta2007'
STEAM_PASS = config.get("configuration", "steam_ishandutta2007_password")
DISCORD_ID = 'ishandutta2007@gmail.com'
DISCORD_PASS = config.get("configuration", "discord_ishandutta2007atgmaildotcom_password")
TELEGRAM_ID = 'ishandutta2007'
DOB = '29/04/1988'
DOB_MMDDYY = '04/29/1988'
MOB = '+919952917263'
ZIP = '74140'
CHROME_DRIVER_PATH = '/Users/ishandutta2007/Documents/Projects/chromium/chromium/src/out/Default/chromedriver_gleam'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CEND    = '\33[0m'
ANTIFRAUD_FUZZY_SLEEP_LIMIT = 60


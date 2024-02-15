from seleniumwire import webdriver
#from selenium import webdriver
import time

def get_first_request():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--no-cache')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1024x768')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.headless = True
    selenium_options = {
        'request_storage_base_dir': '/tmp', # Use /tmp to store captured data
        'exclude_hosts': ''
    }
    chrome_options.binary_location = '/opt/headless-chromium'
    driver = webdriver.Chrome('/opt/chromedriver', chrome_options=chrome_options, seleniumwire_options=selenium_options)
    #driver.get("https://www.google.com/maps/place/Nema/@-22.9807929,-43.2337821,13z/data=!3m1!5s0x9bd50757e02857:0x35aa6a9b37f5d532!4m8!3m7!1s0x9bd58a0cdc1487:0x4c1eb56d62eb469b!8m2!3d-22.9841517!4d-43.2128543!9m1!1b1!16s%2Fg%2F11j20tdp78?entry=ttu")
    driver.get("https://www.google.com/maps/place/Nema+-+Botafogo+%7C+Padaria+de+Fermenta%C3%A7%C3%A3o+Natural/@-22.9561149,-43.1989204,17z/data=!4m8!3m7!1s0x997fd3ce25318b:0x17650611ede4f2c9!8m2!3d-22.9561199!4d-43.1963455!9m1!1b1!16s%2Fg%2F11pqxzwzs_?entry=ttu")
    time.sleep(1)

    for request in driver.requests:
        if request.response:
            if("listugcposts" in request.url):
                return request.url
            
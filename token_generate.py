import datetime, enum, json, logging, os, pickle, random, re, shutil, string, time, pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import bs4
logger = logging.getLogger(__name__)

def get_token(username,password,chromedriver_path,token_path):

    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    headless = True
    logger.info('refreshing tradingview token using selenium')
    logger.debug('launching chrome')
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    try:
        driver = webdriver.Chrome(chromedriver_path,
                                  desired_capabilities=caps, options=options)
        logger.debug('opening https://in.tradingview.com ')
        driver.set_window_size(1920, 1080)
        driver.get('https://in.tradingview.com')
        time.sleep(5)
        logger.debug('click sign in')
        driver.find_element_by_link_text('Sign in').click()
        time.sleep(5)
        logger.debug('click email')
        embutton = driver.find_element_by_class_name('tv-signin-dialog__toggle-email')
        embutton.click()
        time.sleep(5)
        logger.debug('enter credentials and log in')
        username_input = driver.find_element_by_name('username')
        username_input.send_keys(username)
        password_input = driver.find_element_by_name('password')
        password_input.send_keys(password)
        submit_button = driver.find_element_by_class_name('tv-button__loader')
        submit_button.click()
        time.sleep(5)
        logger.debug('opening chart')
        driver.get('https://www.tradingview.com/chart/')

        def process_browser_logs_for_network_events(logs):
            for entry in logs:
                log = json.loads(entry['message'])['message']

                if 'Network.webSocketFrameSent' in log['method']:
                    if 'set_auth_token' in log['params']['response']['payloadData']:
                        # log_result = log['params']['response']['payloadData']
                        # k = re.search('\"p\"\:\[(.+?)\]', log_result)
                        # if k:
                        #     log_text = k.group(1)
                        # print(log_text)

                        if 'unauthorized_user_token' not in log['params']['response']['payloadData']:
                            yield log

        logs = driver.get_log('performance')
        events = process_browser_logs_for_network_events(logs)
        for event in events:
            x = event
            token = json.loads(x['params']['response']['payloadData'].split('~')[(-1)])['p'][0]
        else:

            with open(token_path, 'wb') as f:
                pickle.dump({'date': datetime.date.today(), 'token': token}, f)
            logger.debug('token saved successfully')

        driver.quit()

    except Exception as e:
        print(str(e))
        # driver.quit()
    return


# df_log=pd.DataFrame(logs)
# df_log.to_csv('d:/logtemp.csv')

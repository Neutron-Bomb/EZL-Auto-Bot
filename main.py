import argparse
import json
import logging
import os
import smtplib
from email.mime.text import MIMEText
from queue import Queue
from random import choice

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class HealthRep:
    def __init__(self, gui=False, chromedriver_logging=False) -> None:
        chrome_options = webdriver.ChromeOptions()
        if not chromedriver_logging:
            chrome_options.add_argument('--silent')
            chrome_options.add_argument("--log-level=3");
        
        if not gui:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
        
        driver_path = './bin/chromedriver.exe' if os.name == 'nt' else './bin/chromedriver'
        self.__client = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
        self.__wait = WebDriverWait(self.__client,10,0.5)
        self.__flag = False

    def __get_element_by_xpath(self, xpath:str):
        return self.__wait.until(EC.presence_of_element_located((By.XPATH,xpath)))

    def login(self, username:str, password:str) -> bool:
        self.__flag = False
        try:
            urls = \
            [
                'http://stu.zstu.edu.cn/webroot/decision/url/mobile?redirect=http%3A%2F%2Fstu.zstu.edu.cn%2Fwebroot%2Fdecision%2Furl%2Fmobile%23%2Fmain%2Fhome#/login',
                'http://stu3.zstu.edu.cn/webroot/decision/url/mobile?redirect=http%3A%2F%2Fstu.zstu.edu.cn%2Fwebroot%2Fdecision%2Furl%2Fmobile%23%2Fmain%2Fhome#/login'
            ]
            self.__client.get(choice(urls))
            username_input = self.__get_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/div/div/div/div/div/div[2]/div[2]/div[1]/div/input')
            password_input = self.__get_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]/input')
            login_button = self.__get_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/div/div/div/div/div/div[2]/div[2]/div[4]')
            username_input.send_keys(username)
            password_input.send_keys(password)
            login_button.click()

            self.__get_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/div/div[1]/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div[3]/div/div/div[4]/div/div/div[3]')
        except:
            return False
        else:
            return True

    def do(self) -> bool:
        try:
            workflow = \
            [
                '//*[@id="app"]/div/div[1]/div/div/div/div[1]/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div[3]/div/div/div[4]/div/div/div[3]',
                '//*[@id="col_1_row_11"]/span',
                '//*[@id="col_2_row_6"]/div/div[2]/div',
                '//*[@id="app"]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div[34]/div[1]/div/div/div[1]/span',
                '//*[@id="col_3_row_6"]/div/div[2]/div',
                '//*[@id="app"]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[1]/span',
                '//*[@id="col_2_row_15"]/div/div/div/div/div[1]/div/div[1]',
                '//*[@id="col_2_row_17"]/div/div/div/div/div[1]/div/div[1]',
                '//*[@id="col_2_row_18"]/div/div/div/div/div[1]/div/div[1]',
                '//*[@id="col_4_row_23"]/div/div/div/div/div[1]/div/div[1]',
                '//*[@id="col_4_row_24"]/div/div/div/div/div[1]/div/div[1]',
                '//*[@id="col_4_row_25"]/div/div/div/div/div[2]/div/div[1]',
                '//*[@id="col_4_row_26"]/div/div/div/div/div[2]/div/div[1]',
                '//*[@id="col_4_row_27"]/div/div/div/div/div[2]/div/div[1]',
                '//*[@id="col_4_row_29"]/div/div/div/div/div[2]/div/div[1]',
                '//*[@id="col_4_row_31"]/div/div/div/div/div[1]/div/div[1]',
                '//*[@id="col_4_row_33"]/div/div/div/div/div[2]/div/div[1]',
                '//*[@id="col_4_row_35"]/div/div/div/div/div[2]/div/div[1]',
                '//*[@id="col_4_row_37"]/div/div/div/div/div[2]/div/div[1]',
                '//*[@id="col_4_row_6"]/div/div[2]/div',
                '//*[@id="app"]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div[6]/div[1]/div/div/div[1]/span',
            ]
            for work in workflow:
                self.__get_element_by_xpath(work).click()

            detailed_area_input = self.__get_element_by_xpath('//*[@id="col_2_row_7"]/div/div[1]/div/input')
            detailed_area_input.send_keys('浙江理工大学')

            submit_botton = self.__get_element_by_xpath('//*[@id="col_0_row_40"]/div/div/div/div/div')
            submit_botton.click()

            self.__get_element_by_xpath('//*[@id="col_1_row_11"]/span')
        except:
            return False
        else:
            self.__flag = True
            return True

    def status(self) -> bool:
        return self.__flag

def main():
    logging.basicConfig(level=logging.INFO
                        ,filename="daily.log"
                        ,filemode="w"
                        ,format="%(asctime)s %(message)s"
                        ,datefmt="%Y-%m-%d %H:%M:%S")
                        
    parser = argparse.ArgumentParser(description='自动完成E浙理打卡')
    parser.add_argument('--gui', action='store_true', default=False, help='显示Chrome窗口')
    parser.add_argument('--chromedriver_logging', action='store_true', default=False, help='启用ChromeDriver的日志')
    args = parser.parse_args()
    
    smtp = smtplib.SMTP('smtp.qq.com', 587)
    smtp.starttls()
    with open('./email_config.json') as f:
        data = json.loads(f.read())
        smtp.login(data['address'], data['password'])

    hr = HealthRep(gui=args.gui, chromedriver_logging=args.chromedriver_logging)
    with open('./essentials.json', 'r') as f:
        data = json.loads(f.read())
        tasks = Queue()
        [tasks.put(user) for user in data if user['enabled'] == True]
        max_try = tasks.qsize() * 10
        while not tasks.empty():
            if max_try <= 0:
                break

            user = tasks.get()
            if hr.login(user['username'],user['password']) and hr.do():
                logging.info('succeed: {}'.format(user['username']))
                max_try -= 10
                email = MIMEText('今天不用你动手啦！')
                email['Subject'] = '打卡成功啦！'
                email['From'] = 'erohal@qq.com'
                email['To'] = user['email']
                smtp.sendmail(email['From'], email['To'], email.as_string())
            else:
                logging.info('failed: {}'.format(user['username']))
                max_try -= 1
                tasks.put(user)

        while not tasks.empty():
            user = tasks.get()
            email = MIMEText('今天需要自己打卡了呢！')
            email['Subject'] = '尝试了很多次，打卡还是失败了！'
            email['From'] = 'erohal@qq.com'
            email['To'] = user['email']
            smtp.sendmail(email['From'], email['To'], email.as_string())
            logging.info('A email has been sent to {}({})'.format(user['username'], user['email']))

    smtp.close()

if __name__ == '__main__':
    main()

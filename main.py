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
                'http://fangyi.zstu.edu.cn:6006/iForm/1817056F47E744D3B8488B'
            ]
            self.__client.get(choice(urls))
            username_input = self.__get_element_by_xpath('/html/body/app-root/app-right-root/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/app-login-normal/div/form/div[1]/nz-input-group/input')
            password_input = self.__get_element_by_xpath('/html/body/app-root/app-right-root/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/app-login-normal/div/form/div[2]/nz-input-group/input')
            login_button = self.__get_element_by_xpath('/html/body/app-root/app-right-root/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/app-login-normal/div/form/div[6]/div/button')
            username_input.send_keys(username)
            password_input.send_keys(password)
            login_button.click()

            self.__get_element_by_xpath('//*[@id="iform"]/div[1]/div[3]/form/div[4]/div/div/div[2]/div/div/div/div/div')
        except:
            return False
        else:
            return True

    def do(self) -> bool:
        try:

            self.__client.execute_script('document.getElementsByClassName("van-field__control")[6].readOnly = false')
            detailed_area_input = self.__get_element_by_xpath('//*[@id="iform"]/div[1]/div[3]/form/div[6]/div/div/div[2]/div/div/div/div[1]/input')
            detailed_area_input.clear()
            detailed_area_input.send_keys('浙江省 杭州市 钱塘区')

            workflow = \
            [
                '//*[@id="iform"]/div[1]/div[3]/form/div[7]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span', # 低风险
                '//*[@id="iform"]/div[1]/div[3]/form/div[8]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span', # 在校内
                '//*[@id="iform"]/div[1]/div[3]/form/div[9]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span', # 健康状况
                '//*[@id="iform"]/div[1]/div[3]/form/div[10]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span', # 绿码
                '//*[@id="iform"]/div[1]/div[3]/form/div[11]/div/div/div[2]/div/div/div/div[1]/div/div[2]/span', # 已完成首轮全部
                '//*[@id="iform"]/div[1]/div[3]/form/div[12]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span', # 无密切接触
                '//*[@id="iform"]/div[1]/div[3]/form/div[13]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span', # 未隔离
                '//*[@id="iform"]/div[1]/div[3]/form/div[14]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span', # 无省外旅行史
                '//*[@id="iform"]/div[1]/div[3]/form/div[15]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span', # 家人无风险地区旅行史
                '//*[@id="iform"]/div[1]/div[3]/form/div[16]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span',
            ]
            for work in workflow:
                self.__get_element_by_xpath(work).click()

            self.__get_element_by_xpath('//*[@id="iform"]/div[1]/div[4]/div/button[1]').click()
            self.__get_element_by_xpath('/html/body/div[3]/div[3]/button[2]').click()
            self.__get_element_by_xpath('/html/body/img')
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
                        
    parser = argparse.ArgumentParser(description='自动完成健康打卡')
    parser.add_argument('--gui', action='store_true', default=False, help='显示Chrome窗口')
    parser.add_argument('--chromedriver_logging', action='store_true', default=False, help='启用ChromeDriver的日志')
    args = parser.parse_args()
    
    smtp = smtplib.SMTP('smtp.qq.com', 587)
    smtp.starttls()
    enable_email = False
    with open('./email_config.json') as f:
        email_config = json.loads(f.read())
        enable_email = email_config['enabled']
        smtp.login(email_config['address'], email_config['password']) if enable_email else None
        smtp.close() if not enable_email else None

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
                if enable_email:
                    email = MIMEText('今天不用你动手啦！')
                    email['Subject'] = '打卡成功啦！'
                    email['From'] = email_config['address']
                    email['To'] = user['email']
                    smtp.sendmail(email['From'], email['To'], email.as_string())
            else:
                logging.info('failed: {}'.format(user['username']))
                max_try -= 1
                tasks.put(user)

        while not tasks.empty():
            user = tasks.get()
            if enable_email:    
                email = MIMEText('今天需要自己打卡了呢！')
                email['Subject'] = '尝试了很多次，打卡还是失败了！'
                email['From'] = email_config['address']
                email['To'] = user['email']
                smtp.sendmail(email['From'], email['To'], email.as_string())
                logging.info('A email has been sent to {}({})'.format(user['username'], user['email']))

    smtp.close()

if __name__ == '__main__':
    main()

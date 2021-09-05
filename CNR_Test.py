#! /usr/bin/python3

import datetime
import os
import time
from time import gmtime, strftime
from flask import request, jsonify
from werkzeug.utils import secure_filename
from flask import Flask, request
import PyPDF2

import os,distro
# from Screenshot import Screenshot_Clipping
import os
import sys
import re
import cv2
import requests
import pytesseract
import numpy as np
import mysql.connector
import pymssql
import shutil
import urllib
from time import sleep
from PIL import Image, ImageEnhance
from io import BytesIO
# from xvfbwrapper import Xvfb
from distutils.dir_util import copy_tree
from smb.SMBConnection import SMBConnection
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common import exceptions as E
import datetime
from datetime import  datetime
from dateutil.parser import parse
import platform
# from db import *
import threading
# import __main__ as main

from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
from webdriver_manager.chrome import ChromeDriverManager

u1 = 'https://services.ecourts.gov.in/ecourtindia_v6/#'
u2 = 'https://services.ecourts.gov.in/ecourtindia_v6/securimage/securimage_show.php?9566c49cd54fcb1cd040756f4e5786a6'


# qwere34563fgfgfg
# QWERE34563FGFGFG
def fName(s):
    invalid_chars = r'\/:*?"<>|'
    filename = ''.join(c if not c in invalid_chars else '_' for c in s)
    filename = filename.replace(' ', '_')
    return filename


def enable_download_in_headless_chrome(driver):
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior',
              'params': {'behavior': 'allow', 'downloadPath': os.path.abspath('save')}}
    command_result = driver.execute("send_command", params)


def CNR_cases(cnrnumber):
    path = os.getcwd()
    sleep(3)

    def saveCaptcha(d1):
        try:
            element = d1.find_element_by_id("captcha_image")  # find part of the page you want image of
            location = element.location
            size = element.size
            d1.save_screenshot(os.path.join(path, 'screenshot.png'))
            im = Image.open(os.path.join(path, 'screenshot.png'))  # uses PIL library to open image in memory
            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']
            im = im.crop((left, top, right, bottom))  # defines crop points
            # new_width = 130
            # new_height = 39
            # im = im.resize((new_width, new_height))
            im.save(os.path.join(path, 'screenshot.png'))
        except Exception:
            # closeSite()
            return

    # def breakCaptcha(d1,img_url,path):
    #     m1=cv2.imread(img_url)
    #     gray=cv2.cvtColor(m1,cv2.COLOR_BGR2GRAY)
    #     _,th2=cv2.threshold(gray,100,255,0)
    #     captcha =  pytesseract.image_to_string(th2, lang='eng',config='--psm 6 --oem 0 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    #     captcha = captcha.replace(' ','')
    #     os.remove(img_url)
    #     os.remove(os.path.join(path,'.\clipping_shot.png'))
    #     if len(captcha)==6:
    #         return captcha
    #     else:
    #         return '2fg34f'

    def solve_captcha(img):
        char_map = {'a': 4, 't': 7, 's': 5, 'b': 8, 'l': 1, 'i': 1, 'e': 6}
        currentdir = os.getcwd()
        # pytesseract.pytesseract.tesseract_cmd = currentdir + '\\Tesseract-OCR\\tesseract'
        s = pytesseract.image_to_string(img)
        s = re.sub(r"\s+", '', s)
        captcha = ''
        for i in s:
            if i.lower() in char_map:
                captcha = captcha + str(char_map[i.lower()])
            else:
                captcha = captcha + str(i)
        captcha = re.sub('\D', '', captcha)
        # captcha = captcha.replace("0", "")
        return captcha

    def clickButton(d1, selector):
        try:
            _ = d1.find_element_by_css_selector(selector)
            _.click()
        except Exception:
            return

    def _chkCase():
        try:
            _ = WebDriverWait(d1, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#chHeading')))
            # _=WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.XPATH,'//*[text()="Record Not Found"]')))
            return True
        except Exception:
            # print('Error1: {}'.format(Exception))
            return False

    def _chkCaptcha(d1):
        try:
            # _=WebDriverWait(d1,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#txtmsg')))
            # msgTxt=_.get_attribute('title')
            # print(str(d1.page_source))
            if 'Invalid Captcha' in d1.find_element_by_id('caseHistoryDiv').text:
                return False

            elif 'This Case Code does not exists' in str(d1.find_element_by_id('caseHistoryDiv').text):
                return '1'
            elif 'THERE IS AN ERROR.ERROR_invalid_chars' in str(d1.find_element_by_id('caseHistoryDiv').text):
                return '1'
            else:
                return True
        except Exception as e:
            print(e)
            return False

    while True:
        try:
            options = webdriver.ChromeOptions()
            # options.add_argument("--start-maximized")
            options.add_argument('--headless')
            d1 = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            enable_download_in_headless_chrome(d1)
            # d1=webdriver.Chrome()
            d1.get(u1)
            d1.implicitly_wait(20)
            e1 = d1.find_element_by_id('cino')
            e1.send_keys(str(cnrnumber).replace('-', '').replace(' ', ''))
            saveCaptcha(d1)
            # img1 = self.preprocess_image()
            txt = solve_captcha('screenshot.png')

            # txt=str(breakCaptcha(d1,img_url,path)).lower()
            # print(txt)
            captcha_input = d1.find_element_by_id('captcha')
            captcha_input.clear()
            captcha_input.send_keys(txt)
            sleep(5)
            clickButton(d1, 'input[id="searchbtn"]')
            sleep(5)
            # self.breakCaptcha(self.path)
            result = _chkCaptcha(d1)
            if result == True:
                sleep(20)
                break
            elif result == '1':
                print('This Case Code does not exists')
                d1.quit()
                # v1.stop()
                l1 = []
                l1.append('No')
                return l1
                # break
            else:
                d1.quit()
                # v1.stop()
                continue
        except Exception as e:
            print(e)
            # d1.quit()
            # v1.stop()
    if _chkCase():
        l1 = []
        try:
            a = d1.find_element_by_css_selector('#caseHistoryDiv')
            source = a.get_attribute('innerHTML')
            c1 = re.compile('id="chHeading">(.*?)</h2>', re.DOTALL)
            heading = c1.search(str(source), re.IGNORECASE).group(1)
            c2 = re.compile('>Case Type.*?<td.*?>(.*?)</td>', re.DOTALL)
            case_type = c2.search(str(source), re.IGNORECASE).group(1)
            c3 = re.compile('>Filing Number.*?<td.*?>(.*?)</td>', re.DOTALL)
            f_no = c3.search(str(source), re.IGNORECASE).group(1)
            c4 = re.compile('>Registration Number.*?<label.*?>(.*?)</label>', re.DOTALL)
            r_no = c4.search(str(source), re.IGNORECASE).group(1)

            # heading = d1.find_element_by_id('chHeading').text
            # # heading = d1.find_element_by_css_selector('#chHeading').text
            # case_type = d1.find_elements_by_xpath('//table[@class="table table-responsive case_details_table"]//td')[1].text
            # f_no = d1.find_elements_by_xpath('//table[@class="table table-responsive case_details_table"]//td')[3].text
            # r_no = d1.find_elements_by_xpath('//table[@class="table table-responsive case_details_table"]//td')[7].text
            # r_date = d1.find_elements_by_xpath('//table[@class="table table-responsive case_details_table"]//td')[9].text
            # print('data============================', heading, case_type, f_no, r_no)

            dict = {}
            dict['heading'] = heading
            dict['case_type'] = case_type
            dict['f_no'] = f_no
            dict['r_no'] = r_no

            # print(dict)
            # l1.append(heading)
            # l1.append(case_type)
            # l1.append(f_no)
            # l1.append(r_no)
            d1.quit()
            # v1.stop()
            return dict
        except:
            l1.append('No')
            return l1
            d1.quit()
            # v1.stop()
    else:
        d1.quit()
        # v1.stop()
        l1 = []
        l1.append('No')
        return l1


# import os
# import PyPDF2
# import secrets
# from flask import jsonify, request
# from flask import Flask, send_from_directory
# import datetime
#
#
# app = Flask(__name__)
# app.secret_key = "secret key"
#
# @app.route('/check', methods=['GET', 'POST'])
# def check_api():
#     updated_part = "Hello this is check API..."
#     return jsonify(
#         {"statusMessage": "Successfully Completed.", "statusCode": "SRC001", "data": f"API is running, {updated_part}"})
#
#
# @app.route('/time', methods=['GET', 'POST'])
# def check_time():
#     time_1 = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
#     time_2 = str(datetime.datetime.now())
#     response = jsonify(
#         {"time": {"local time one ": time_1, "local time two": time_2}, "statusMessage": "Successfully Completed.",
#          "statusCode": "SRC001"})
#     return response
#
# 'TNCB0A1234562017'
#
#
# @app.route('/CNR', methods=['GET', 'POST'])
# def CNR():
#     # reference id
#     referenceid = request.form['referenceId']
#     crnnumber = request.form['crnnumber']
#     if crnnumber:
#         data = CNR_cases(crnnumber)
#         return jsonify({"statusMessage": "Successfully Completed.", "statusCode": "SRC001","referenceId": referenceid, "data": data})
#     else:
#         return jsonify({"statusMessage": "CNR is Empty.", "statusCode": "EFE030", "referenceId": None, "data": {}})
#
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0')
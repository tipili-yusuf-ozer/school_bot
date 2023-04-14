#!/usr/bin/env python3
# %%-*- coding: utf-8 -*-
"""
Created on Wed Mar 29 12:56:21 2023
ARGS: lesson name(can be only part of what is displayed on the uzem page, case ignored)
@author: tipili-yusuf-ozer
"""
#python imports
import logging
from sys import argv, exit
from time import sleep
from re import compile, sub, IGNORECASE, search
import datetime
#selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import wait as waitt
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
#%% main
def main():
    initialize()
    login("402496","06428")
    lessons_tab=driver.find_element(by=By.XPATH, value="//div[@class='wdm-overview-slider m-0 row w-full slick-initialized slick-slider slick-dotted']")    
    nextbutton=lessons_tab.find_element(by=By.XPATH, value="button[2]")
    tabcursor=lessons_tab.find_element(by=By.XPATH, value="ul")
    tabcursor_length=len(tabcursor.find_elements(by=By.TAG_NAME, value='li'))
    tabcursor_index=1
    lessons_locator= (By.XPATH, "//div[@class='wdm-overview-slider m-0 row w-full slick-initialized slick-slider slick-dotted']/div[@class='slick-list draggable']/div[@class='slick-track']/div[@aria-hidden='false']")
    while tabcursor_index<=tabcursor_length:


        lessons=wait.until(ec.visibility_of_all_elements_located(lessons_locator))
        for lesson in lessons:
            lesson_index=lesson.get_attribute('data-slick-index')
            lesson_page=wait.until(ec.visibility_of_element_located((By.XPATH, f"//div[@class='wdm-overview-slider m-0 row w-full slick-initialized slick-slider slick-dotted']//div[@data-slick-index='{lesson_index}']/div/figure/div[2]/div/a")))
            lesson_name=lesson_page.text #lessons name written on the link to the lesson page
            if(lesson_regex.match(lesson_name)):
                driver.get(lesson_page.get_dom_attribute('href'))
                find_session(lesson_name)   
                join_session()
#%% wait untill everybody leaves
                wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@id='roster-button']"))).click()
                flag=0
                while(1):
                    participant_num=int(search(r"\d+",(wait.until(ec.visibility_of_element_located((By.XPATH, "//span[contains(@id, 'roster-title-section')]/span"))).text)).group())
                    if participant_num<5:
                        if flag==1:
                            driver.quit()
                            exit(0) #quit if no ones leftt in lesson
                        else:
                            flag=1
                    else:
                        flag=0
                    sleep(600) #sleep 10 min and check again
#%% look for next section in lessons for the lesson
        wait.until(ec.element_to_be_clickable(nextbutton)).click()
        tabcursor_index+=1
    driver.quit()
    exit(1) #no match found for input lesson
# %% set driver and argv variables
def initialize():
    global driver
    global lesson_regex
    global wait
    driveroption=Options()
    driveroption.add_argument("--disable-infobars")
    driveroption.add_argument("--disable-remote-fonts")
    driveroption.add_argument("--start-maximized")
    driveroption.add_argument("--no-sandbox")
    # driveroption.add_argument("--disable-setuid-sandbox")
    driveroption.add_argument("--disable-dev-shm-using")
    driveroption.add_argument("--disable-default-apps")
    # driveroption.add_argument("--disable-extensions")# disables required ext as well 
    driveroption.add_extension("extensions/packaged/myext2.crx")
    service=Service('driver/linux/chromedriver')
    driver = webdriver.Chrome(service=service,options=driveroption)
    wait=waitt.WebDriverWait(driver, 20) 
    lesson_regex_text = sub('s', '[sş]', argv[1]) 
    lesson_regex=compile(f'.*{lesson_regex_text}.*',IGNORECASE)
    # lesson_regex=compile(r'.*introduction.*', IGNORECASE)
# %% login to uzemdef initialize():
def login(username, password):
    driver.get("https://ue2.ktu.edu.tr/login/index.php")
    usernamelogin=wait.until(ec.element_to_be_clickable((By.ID, 'username')))
    passwordlogin= wait.until(ec.element_to_be_clickable((By.ID, 'password')))
    submitlogin= driver.find_element(by=By.ID, value='loginbtn')
    usernamelogin.send_keys(username)
    passwordlogin.send_keys(password)
    submitlogin.click()
#%% find teams session link
def find_session(lesson_name):
    if "English" in lesson_name:
        sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH, "//li[@id='module-73745']//a")))
    elif "Olasılık" in lesson_name:
        sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH, "//li[@id='module-76755']//a")))
    elif "Matematik" in lesson_name:
        sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Ders Bağlantı Linki')]")))
    elif "Bilişim" in lesson_name:
        today=datetime.date(1,1,1).today().strftime("%d.%m.%Y")
        driver.get(wait.until(ec.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{today}')]/.."))).get_attribute('href'))
        sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'https://teams.microsoft.com')]")))
    elif "Microprocessors" in lesson_name:
        month, day=datetime.date(1,1,1).today.strftime('%B'), datetime.date(1,1,1).today.strftime('%-d')
        lessonindex=datetime.date(1,1,1).today.isoweekday()-1 #1st lesson of the week or second
        driver.get(wait.until(ec.element_to_be_clickable((By.XPATH, f"//ul[@class='topics']//li[contains(@aria-label, '{month}') and contains(@aria-label, '{day}')]//li[contains(@class, 'activity page')][{lessonindex}]//div[@class='activityinstance']/a"))).get_attribute('href'))
        sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'https://teams.microsoft.com')]")))
    else:
        sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH,"//ul[@class='topics']/li[@id='section-1']//div[@class='activityinstance']/a")))
        driver.get(sessionlink.get_attribute('href'))
        sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH,"//a[contains(@href, 'https://teams.microsoft.com')]")))
    driver.get(sessionlink.get_attribute('href'))
#%% log in to teams and join the session
def join_session():
    wait.until(ec.url_contains('https://teams.microsoft.com/_#/'))
    wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@ng-click='getUserMedia.passWithoutMedia()']"))).click()
    wait.until(ec.element_to_be_clickable((By.XPATH, "//a[@ng-click='ctrl.signIn()']"))).click()
    wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@name='loginfmt']"))).send_keys("402496@ogr.ktu.edu.tr")
    wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@data-report-event='Signin_Submit']"))).click()
    wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@name='passwd']"))).send_keys("Yoz06428")
    wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@data-report-event='Signin_Submit']"))).click()
    wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@value='No']"))).click()
    wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@ng-click='getUserMedia.passWithoutMedia()']"))).click()
    wait.until(ec.url_matches('https://teams.microsoft.com/_#/modern-calling/'))
    wait.until(ec.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@id, 'experience-container')]")))
    wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(@data-tid, 'join-button')]"))).click()
#%%run the code
participant_num=0
logging.basicConfig(
    filename="logs/joiner_logs.txt",
    filemode="a",
    encoding="UTF-8",
    format="\n%(asctime)s:%(lesson)s:%(message)s",
    style="%",
    datefmt="%A - %-H.%-M",
    level=logging.ERROR
    )
try:
    main()
except SystemExit as e:
    if e.args[0]==1:
        logging.error('No match found for the %s',argv[1], extra={"lesson": argv[1]})
    elif e.args[0]==0:
        logging.info('Program sucessfully quit with %d persons left in lesson', participant_num, extra={"lesson": argv[1]})
except:    
    driver.quit()
    logging.error("Generic Error", exc_info=1, extra={"lesson": argv[1]})
    raise
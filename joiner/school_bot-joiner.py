#!/usr/bin/env python3
# %%-*- coding: utf-8 -*-
"""
Created on Wed Mar 29 12:56:21 2023
ARGS: lesson name(can be only part of what is displayed on the uzem page, case ignored)
@author: tipili-yusuf-ozer
"""
#python imports
import signal
import logging
from sys import argv, exit
from time import sleep
from re import compile, sub, IGNORECASE, search
import datetime
from csv import DictReader
#selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import wait as waitt
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
#%% main
def main():
    initialize()
    try:
        with open("credentials.csv", "r") as f:
           a=f.read().split(",")
           credentials = {"username": a[0], "password": a[1]}
    except FileNotFoundError:
        username=input("Your first run, enter your credentials:\nusername: ")
        password=input("\npassword: ")
        credentials={"username": username, "password": password}
        with open("credentials.csv", "w") as f:
                f.write("{username},{password}".format(username=username, password=password))

    login(credentials["username"],credentials["password"])
    lessons_tab=driver.find_element(by=By.XPATH, value="//div[@id='pc-for-in-progress']/div[@class='wdm-overview-slider m-0 row w-full slick-initialized slick-slider slick-dotted']")    
    nextbutton=lessons_tab.find_element(by=By.XPATH, value="button[2]")
    tabcursor=lessons_tab.find_element(by=By.XPATH, value="ul")
    tabcursor_length=len(tabcursor.find_elements(by=By.TAG_NAME, value='li'))
    tabcursor_index=1
    while tabcursor_index<=tabcursor_length:
        lessons=wait.until(ec.visibility_of_all_elements_located((By.XPATH, "//div[@id='pc-for-in-progress']/div[@class='wdm-overview-slider m-0 row w-full slick-initialized slick-slider slick-dotted']/div[@class='slick-list draggable']/div[@class='slick-track']/div[@aria-hidden='false']")))
        for lesson in lessons:
            lesson_index=lesson.get_attribute('data-slick-index')
            lesson_page=wait.until(ec.visibility_of_element_located((By.XPATH, f"//div[@class='wdm-overview-slider m-0 row w-full slick-initialized slick-slider slick-dotted']//div[@data-slick-index='{lesson_index}']/div/figure/div[2]/div/a")))
            lesson_name=lesson_page.text #lessons name written on the link to the lesson page
            if lesson_regex.match(lesson_name):
                driver.get(lesson_page.get_dom_attribute('href'))
                find_session(lesson_name)   
                join_session()
                with open("pipe/manager-joiner.txt", "w") as f:
                    f.write("0")
#%% wait untill everybody leaves
                try:
                    wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@id='roster-button']"))).click()
                    flag=0
                    while(1):
                        global participant_num
                        participant_num=int(search(r"\d+",(wait.until(ec.visibility_of_element_located((By.XPATH, "(//span[contains(@id, 'roster-title-section')])[2]/span"))).text)).group())
                        if participant_num<5:
                            if flag==1:
                                driver.quit()
                                exit(0) #quit if no ones leftt in lesson
                            else:
                                flag=1
                        else:
                            flag=0
                        sleep(600) #sleep 10 min and check again
                except TimeoutException:
                    exit(3)
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
    service=Service('driver/chromedriver.exe')
    driver = webdriver.Chrome(service=service,options=driveroption)
    logging.error("driverup %s", "",extra={'lesson': argv[1]})
    wait=waitt.WebDriverWait(driver, 25) 
    lesson_regex_text = sub('[si]', lambda x: {'s': '[sş]', 'i': '[iı]'}[x.group()], argv[1])
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
        month, day=datetime.date(1,1,1).today().strftime('%B'), datetime.date(1,1,1).today().strftime('%d').lstrip('0')
        lessonindex=datetime.date(1,1,1).today().isoweekday()-1 #1st lesson of the week or second
        driver.get(wait.until(ec.element_to_be_clickable((By.XPATH, f"//ul[@class='topics']//li[contains(@aria-label, '{month}') and contains(@aria-label, '{day}')]//li[contains(@class, 'activity page')][{lessonindex}]//div[@class='activityinstance']/a"))).get_attribute('href'))
        sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'https://teams.microsoft.com')]")))
    else:
        sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH,"//ul[@class='topics']/li[@id='section-1']//div[@class='activityinstance']/a")))
        driver.get(sessionlink.get_attribute('href'))
        sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH,"//a[contains(@href, 'https://teams.microsoft.com')]")))
    driver.get(sessionlink.get_attribute('href'))
#%% log in to teams and join the session
def join_session():
    wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@data-tid='joinOnWeb']"))).click()
    wait.until(ec.url_contains('https://teams.microsoft.com/_#/'))
    wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@ng-click='getUserMedia.passWithoutMedia()']"))).click()
    wait.until(ec.element_to_be_clickable((By.XPATH, "//a[@ng-click='ctrl.signIn()']"))).click()
    wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@name='loginfmt']"))).send_keys("402496@ogr.ktu.edu.tr")
    wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@data-report-event='Signin_Submit']"))).click()
    wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@name='passwd']"))).send_keys("Yoz06428")
    wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@data-report-event='Signin_Submit']"))).click()
    wait.until(ec.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'button-container')]/div[1]//input"))).click()
    wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@ng-click='getUserMedia.passWithoutMedia()']"))).click()
    wait.until(ec.url_matches('https://teams.microsoft.com/_#/modern-calling/'))
    wait.until(ec.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@id, 'experience-container')]")))
    driver.execute_script("arguments[0].click()",wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(@data-tid, 'join-button')]"))))
def hangup_and_quit(signum, frame):
        driver.find_element(By.XPATH, "//button[@id='hangup-button']").click()
        driver.quit()
        exit(2)
#%%run the code
signal.signal(signal.SIGTERM, hangup_and_quit)
logging.basicConfig(
    filename="logs/joiner_logs.txt",
    filemode="a",
    encoding="UTF-8",
    format="\n%(asctime)s:%(lesson)s:%(message)s",
    style="%",
    datefmt="%A %H.%M",
    level=logging.INFO
    )
try:
    main()
except SystemExit as e:
    if e.args[0]==0:
        logging.info("Successfully quit session with %s person left in session", participant_num, extra={"lesson": argv[1]})
    elif e.args[0]==1:
        logging.error('No match found for the %s',argv[1], extra={"lesson": argv[1]})
    elif e.args[0]==2:
        logging.info('Program quit the call before being terminated by unknown source', extra={"lesson": argv[1]})
    elif e.args[0]==3:
        logging.warning('Can\'t track listener count, program has to be terminated by manager')
except:    
    driver.quit()
    logging.error("Other Error", exc_info=True, extra={"lesson": argv[1]})
    with open("pipe/manager-joiner.txt", "w") as f:
        f.write("1")
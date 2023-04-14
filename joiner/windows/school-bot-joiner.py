#!/usr/bin/env python3
# %%-*- coding: utf-8 -*-
"""
**DEVELOPMENT OF WINDOWS BUILD IS ABANDONED FOR JOINER. IT LACKS FUNCTIONALITY AVAILABLE IN LINUX BUILD AND IT DOESNT PERFORM THE MAIN FUNCTIONALITY PROPERLY. USE LINUX BUILD INSTEAD**
Created on Wed Mar 29 12:56:21 2023
ARGS: lesson name, number of instances running
@author: tipil
"""
import sys
import re
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import wait as waitt
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# %%
driveroption=Options()
driveroption.add_argument("--disable-infobars")
driveroption.add_argument("--disable-remote-fonts")
driveroption.add_argument("--start-maximized")
# driveroption.add_argument("--headless")
# driveroption.add_argument("--")
# driveroption.add_argument("--disable-setuid-sandbox")
driveroption.add_argument("--no-sandbox")
driveroption.add_argument("--disable-dev-shm-using")
driveroption.add_argument("--disable-default-apps")
# driveroption.add_argument("--disable-extensions")
# driveroption.add_extension(r"C:\Users\tipil\Documents\school_bot_selenium\extensions\packaged\0.3.0_0.crx")
driveroption.add_argument("--load-extension=C:/Users/tipil/Documents/school_bot_selenium/extensions/fjkmabmdepjfammlpliljpnbhleegehm/0.3.0_0")
# driveroption.add_argument(r"--load-extension=C:\Users\tipil\Documents\school_bot_selenium\extensions\packaged\0.3.0_0.crx")
driveroption.add_argument("--remote-debugging-port=9222")
driver = webdriver.Chrome(options=driveroption)
wait=waitt.WebDriverWait(driver, 15)
driver.get("https://ue2.ktu.edu.tr/login/index.php")
# %%

# lesson_test=re.compile(rf'.*{sys.argv[1]}.*', re.IGNORECASE)

lesson_test=re.compile(r'.*introduction.*', re.IGNORECASE)
# today=datetime.datetime().date(1,1,1).today()
today=datetime.date(1,1,1).fromisoformat('2023-03-28')
# %%
try:
# %% login
    usernamelogin=wait.until(ec.element_to_be_clickable((By.ID, 'username')))
    passwordlogin= wait.until(ec.element_to_be_clickable((By.ID, 'password')))
    submitlogin= driver.find_element(by=By.ID, value='loginbtn')
    usernamelogin.send_keys("402496")
    passwordlogin.send_keys("06428")
    submitlogin.click()

# %% find and enter the lesson page
    lessons_tab=driver.find_element(by=By.XPATH, value="//div[@class='wdm-overview-slider m-0 row w-full slick-initialized slick-slider slick-dotted']")
    nextbutton=lessons_tab.find_element(by=By.XPATH, value="button[2]")
    tabcursor=lessons_tab.find_element(by=By.XPATH, value="ul")
    tabcursor_length=len(tabcursor.find_elements(by=By.TAG_NAME, value='li'))
    tabcursor_index=1
    lessons_locator= (By.XPATH, "//div[@class='wdm-overview-slider m-0 row w-full slick-initialized slick-slider slick-dotted']/div[@class='slick-list draggable']/div[@class='slick-track']/div[@aria-hidden='false']")
    flag=0
    while flag==0 and tabcursor_index<=tabcursor_length:


        lessons=wait.until(ec.visibility_of_all_elements_located(lessons_locator))
        for lesson in lessons:
            lesson_index=lesson.get_attribute('data-slick-index')
            lesson_page=wait.until(ec.visibility_of_element_located((By.XPATH, f"//div[@class='wdm-overview-slider m-0 row w-full slick-initialized slick-slider slick-dotted']//div[@data-slick-index='{lesson_index}']/div/figure/div[2]/div/a")))
            lesson_name=lesson_page.text #lessons name written on the link to the lesson page
            if(lesson_test.search(lesson_name)):
                flag=1
                driver.get(lesson_page.get_dom_attribute('href'))
#join session
# working lessons:Elektronik, Eng math, algoritmalar, automata, introduction to prog., prog. languages, olasılık, mat, eng, bilişim, microprocessors

                if "English" in lesson_name:
                    sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH, "//li[@id='module-73745']//a")))
                elif "Olasılık" in lesson_name:
                    sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH, "//li[@id='module-76755']//a")))
                elif "Matematik" in lesson_name:
                    sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH, "//p[@id='yui_3_17_2_1_1680263932367_32']//a")))
                elif "Bilişim" in lesson_name:
                    driver.get(wait.until(ec.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{today}')]/.."))).get_attribute('href'))
                    sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'https://teams.microsoft.com')]")))
                elif "Microprocessors" in lesson_name:
                    month, day=today.strftime('%B'), today.strftime('%-d')
                    lessonindex=today.isoweekday()-1 #1st lesson of the week or second
                    driver.get(wait.until(ec.element_to_be_clickable((By.XPATH, f"//ul[@class='topics']//li[contains(@aria-label, '{month}') and contains(@aria-label, '{day}')]//li[contains(@class, 'activity page')][{lessonindex}]//div[@class='activityinstance']/a"))).get_attribute('href'))
                    sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'https://teams.microsoft.com')]")))
                else:
                    sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH,"//ul[@class='topics']/li[@id='section-1']//div[@class='activityinstance']/a")))
                    driver.get(sessionlink.get_attribute('href'))
                    sessionlink=wait.until(ec.element_to_be_clickable((By.XPATH,"//a[contains(@href, 'https://teams.microsoft.com')]")))
                driver.get(sessionlink.get_attribute('href'))
# %%
                wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@data-tid='joinOnWeb']"))).click()
                wait.until(ec.url_contains('https://teams.microsoft.com/_#/'))
                wait.until(ec.element_to_be_clickable((By.XPATH, "//a[@ng-click='ctrl.signIn()']"))).click()
                wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@name='loginfmt']"))).send_keys("402496@ogr.ktu.edu.tr")
                wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@data-report-event='Signin_Submit']"))).click()
                wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@name='passwd']"))).send_keys("Yoz06428")
                wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@data-report-event='Signin_Submit']"))).click()
                wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@value='Hayır']"))).click()
                wait.until(ec.url_matches('https://teams.microsoft.com/_#/modern-calling/'))

                wait.until(ec.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@id, 'experience-container')]")))
                wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(@data-tid, 'join-button')]"))).click()

                break
        if flag==0:
            wait.until(ec.element_to_be_clickable(nextbutton)).click()
            tabcursor_index+=1
    driver.quit()
# %%
except:
    driver.quit()
    raise



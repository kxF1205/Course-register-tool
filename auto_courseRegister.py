#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 21:09:06 2019
must put the chromedriver and the python script in the same directory
@author: kxF1205
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def myFun():
    #the list for the course need to resgister, and we have already know the code for the course
    courses=['put your course CRN here']
    '''We set the term here, and format is:
        Term year
    '''
    term = "put the term here"
    #the path to the chromedriver
    chromedriver_path = "your path to the chromedriver"
    #initialize the webdriver
    driver = webdriver.Chrome(executable_path=chromedriver_path)
    #open the website
    driver.get('https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin')
    #wait for the webpage loading
    driver.implicitly_wait(3)
    account = driver.find_element_by_id("UserID")
    passwd = driver.find_element_by_id("PIN")
    account.send_keys("McGill ID")
    passwd.send_keys("Password")
    #login the account
    account.submit()
    #click until we get the course registion webpage
    bottom_1=driver.find_element_by_xpath("//table[@class='plaintable']/tbody/tr/td[5]")
    bottom_1.click()
    bottom_2=driver.find_element_by_link_text("Registration Menu")
    bottom_2.click()
    bottom_3=driver.find_element_by_link_text("Quick Add or Drop Course Sections")
    bottom_3.click()
    select = Select(driver.find_element_by_name("term_in"))
    #now we can select the term
    select.select_by_visible_text(term)
    #submit the selection of the term,you cannot find the element by the type attribute
    driver.find_element_by_xpath("//input[@value='Submit']").click()
    #we set the index at most is the length of the courses
    for i in range(len(courses)):
        n = i+1
        setID = "crn_id"+str(n)
        #we need to wait for the webpage loading
        driver.implicitly_wait(3)
        course = driver.find_element_by_id(setID)
        #course = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr/td[@class='dedefault'][i+1]/input[@name='CRN_IN']")
        course.send_keys(courses[i])
    driver.find_element_by_xpath("//input[@value='Submit Changes']").click()
    situation=driver.find_element_by_xpath("//table[@class='datadisplaytable']/tbody/tr/td[@class='dddefault']/a").text
    #print(situation)
    # the website will pop up the waitlist option course to the top, we first select to add in the waitlist
    for k in range(len(courses)):
        try:
            if 'join the waitlist' in situation:
                # the waitaction_id will be differently numbers, say id1, id2,ect....
                wait_id = "waitaction_id"+str(k+1)
                select = Select(driver.find_element_by_id(wait_id))
                #now we can select the option
                select.select_by_visible_text("(Add(ed) to Waitlist)")
        except NoSuchElementException:
            driver.find_element_by_xpath("//input[@value='Submit Changes']").click()
            break

if __name__ == '__main__':
    #define a BlockingScheduler
    scheduler = BlockingScheduler()
    #set the time in the datetime, the input type is int
    job = scheduler.add_job(myFun,'date',run_date = datetime('year','month','date','hour','minute','second'))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()




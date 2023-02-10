#Hanbyul (Estrella) Kim

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
from selenium.webdriver.common.by import By
import time
import pandas as pd
import numpy as np
#You must have selenium, Pandas, and Numpy installed. This work was done on visual studio code.
FINAL_WAIT_TIME = 0.5


# opening the google maps page
#Copy past the remax website page here (The first page please)
website = 'https://www.remax.ca/ab/edmonton-real-estate-agents?pageNumber=1&search=Vancouver%2C+BC'


path = "D:\chromedriver.exe"
s = Service(path)
driver = webdriver.Chrome(service=s)
driver.get(website)
driver.implicitly_wait(10)

# getting the html of the google maps page and parse the content
page_content = driver.page_source
response = Selector(page_content)
#Page Loading
# time.sleep(3)

#gets how many pages there are (i.e. 63pages for edmonton)
pageNumb = driver.find_elements(By.CSS_SELECTOR, 'a.commercialOutlined span.MuiButton-label')
numbOfPages = int(pageNumb[len(pageNumb) - 1].get_attribute('innerHTML'))
names = ["NAME"]
contacts = ["Phone number"]
agentFacebookLink = ["Email"]
websiteLink = ["Website"]

#iterate the amount of pages
for i in range(numbOfPages):
    time.sleep(FINAL_WAIT_TIME)
    print(driver.current_url)
    # #Gets all the Agent Names
    agentNames = driver.find_elements(By.CSS_SELECTOR, 'div.agent-search-card_name__FKvox')
    for n in agentNames:
        names.append(n.get_attribute('innerHTML'))

    # #Gets all the Phone Number
    agentContactNumb = driver.find_elements(By.CSS_SELECTOR, 'a.commercialOutlined span.MuiButton-label')
    for i in agentContactNumb:
        if(agentContactNumb.index(i)>23):
            break
        if (agentContactNumb.index(i) % 2) != 0:
            contacts.append(i.get_attribute('innerHTML'))

    #Finds number of the agents per page
    NumbOfAgentPages = driver.find_elements(By.CSS_SELECTOR, 'a.agent-office-search-card-base_content__YGOge')
    # print(len(NumbOfAgentPages))
    for j in range (len(NumbOfAgentPages)):
        #For the number of agents find their facebook link
        #This was done as getting the email from facebook link is too complicated
        time.sleep(FINAL_WAIT_TIME)
        ap = driver.find_elements(By.CSS_SELECTOR, 'a.agent-office-search-card-base_content__YGOge')
        # print(len(ap))
        ap[j].click()
        time.sleep(FINAL_WAIT_TIME)
        websiteLink.append(driver.current_url)
        agentSocialLinkPage = driver.find_elements(By.CSS_SELECTOR, 'a.agent-links_socialLink__osesH')
        if len(agentSocialLinkPage)>1:
            agentFacebookLink.append(agentSocialLinkPage[1].get_attribute('href'))
            print("FOUND")
        else:
            agentFacebookLink.append("Can't find email")
            print("NOT FOUND")
        driver.back()
    time.sleep(FINAL_WAIT_TIME)
    #Goes to next page
    nextPage = driver.find_elements(By.CSS_SELECTOR, 'button.MuiButtonBase-root')
    nextPage = nextPage[len(nextPage) - 1]
    if i!=numbOfPages-1:
        try:
            nextPage.click()
        except:
            print("Last Page")
            break



df = pd.DataFrame([names, agentFacebookLink, contacts, websiteLink])
df.T.to_excel('Vancouver_Real_Estate.xlsx', sheet_name='Sheet1', index = False)
print("successfully  reached the end")
driver.quit()


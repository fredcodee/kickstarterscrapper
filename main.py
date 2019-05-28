from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup as soup

options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
#browser = webdriver.Chrome("C:\\Users\\Windows 10 Pro\\Downloads\\chromedriver")
CHROMEDRIVER_PATH ="C:\\Users\\Windows 10 Pro\\Downloads\\chromedriver"
browser = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
url= browser.get("https://www.kickstarter.com/projects/amplifierfoundation/we-the-people-public-art-for-the-inauguration-and?ref=discovery_category_most_funded")
sleep(5)
http_contents = soup(browser.page_source,"html.parser")


all= http_contents.find_all("div", class_= "row")[-1]

#title
title = all.find("h3", class_= "normal").text
#location
location = all.find_all("a")[1].text
#category
category = all.find_all("a")[-1].text
#pledged amount
pledged_amount = all.find("h3", class_="mb0").text
#pledge goal
pledge_goal = all.find_all("span", class_= "money")[-1].text
#backers
backers = all.find_all("h3", class_="mb0")[-1].text
print(backers)

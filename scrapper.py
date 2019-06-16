from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup as soup
import pandas as pd


options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
CHROMEDRIVER_PATH ="C:\\Users\\Windows 10 Pro\\Downloads\\chromedriver"
browser = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)


category="Comics".lower() #put your category here <-----------------
selection = "Most Funded".title()#put your preferred selection here<---------------
url ="https://www.kickstarter.com/discover/categories/"+category+"?ref=discovery_overlay"

browser.get(url)
sleep(3)

def nav_to_category_selection():
    #nav to selection
    browser.find_element_by_id("sorts").click()
    sleep(3)

    browser.find_element_by_link_text(selection).click()
    sleep(5)

    #load pages
    pages_to_scrape= 10 #<---- how many pages to scrape
    for i in range(pages_to_scrape):
        browser.find_element_by_css_selector(".load_more.mt3").click()
        sleep(2)

def get_projects_links():
    #get links to all projects on current page
    projects= browser.find_elements_by_css_selector(".relative.self-start")
    project_links=[]

    for i in projects:
        k = i.find_elements_by_tag_name("a")[0].get_attribute("href")
        project_links.append(k)
        sleep(2)
    return(project_links)

def get_data(link):
    #to scrape the details
    browser.get(link)
    sleep(5)

    http_contents = soup(browser.page_source,"html.parser")
    d={}
    
    all= http_contents.find_all("div", class_= "row")[-1]
    #title
    try:
        d["title"] = http_contents.find("span", class_= "relative").find("a",class_="hero__link").text
    except:
        d["title"] = None
    #location
    try:
        d["location"] = all.find_all("a")[1].text.replace("\n","").replace(" ","")
    except:
        d["location"] = None
    #category
    try:
        d["category"] = all.find_all("a")[-1].text.replace("\n","").replace(" ","")
    except:
        d["category"] = None
    #pledged amount
    try:
        d["pledged_amount"] = all.find("h3", class_="mb0").text.replace("\n","").replace(" ","")
    except:
        d["pledged_amount"] = None
    try:
        d["pledge_goal"] = all.find_all("span", class_= "money")[-1].text.replace("\n","").replace(" ","")
    except:
        d["pledge_goal"] = None
    #backers
    try:
        d["backers"] = all.find_all("h3", class_="mb0")[-1].text.replace("\n","").replace(" ","")
    except:
        d["backers"] =None
    #project url
    d["url"]= link

    return(d)


nav_to_category_selection()
project_list=[]
for i in get_projects_links():
    project_list.append(get_data(i))

#save to csv file
df= pd.DataFrame(project_list)
df.to_csv("%s projects in %s.csv" %(selection,category))
browser.quit()

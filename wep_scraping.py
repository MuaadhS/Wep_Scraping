# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 23:27:47 2023

@author: moaat
"""

import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest # allows printing columns in csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# headless background execution
Options = Options()
Options.headless = True


job_title =[]
company = []
location = []
skills = []
links = [] #link are in the html of job_titles 
salary = []

page = 0
while page<=3:
    
    result = requests.get(f"https://wuzzuf.net/a/Jobs-in-Riyadh?filters%5Bcountry%5D%5B0%5D=Saudi%20Arabia&start={page}")
    src = result.content
    #print(src)
    
    soup = BeautifulSoup(src, 'lxml')
    #print(soup)
    
    job_titles = soup.find_all("h2", {"class" : "css-m604qf"})
    #print(job_titles)
    
    companies = soup.find_all("a",{"class":"css-17s97q8"})
    #print(Companies)
    
    locations = soup.find_all("span",{"class":"css-5wys0k"})
    #print(locations)
    
    job_skills = soup.find_all("div",{"class":"css-y4udm8"})
    #print(job_skills)
    
    
    for i in range(len(job_titles)):
        job_title.append(job_titles[i].text.strip())
        links.append("https://wuzzuf.net" + job_titles[i].find("a").attrs['href']) #get the links not the text
        company.append(companies[i].text.strip())
        location.append(locations[i].text.strip())
        skills.append(job_skills[i].text.strip())
    
        #print(job_title)
    page +=1 

browser = webdriver.Chrome(options=Options)

for link in links:
    browser.get(link)
    
    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')
    salaries = soup.find_all("span", {"class":"css-4xky9y"})
    salary.append(salaries[-1].text)
#print(salary)


file_list = [job_title, company, location, skills, links, salary]
exported = zip_longest(*file_list) # * unpacks the lists

with open('P:\Programs\spyder\wep_scraping\Wuzzuf_jobs.csv', 'w') as file:
    wr = csv.writer(file, lineterminator ="\n") # lineterminatior removes empty rows
    wr.writerow(['job title', 'company', 'location', 'skills', 'links', 'salary'])
    wr.writerows(exported)
    print("file successfully created")
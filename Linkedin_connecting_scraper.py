# Importing Modules
from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
import requests
import time
import json
from bs4 import BeautifulSoup

linkedin_weblink = 'https://www.linkedin.com/search/results/people/?geoUrn=%5B%22101165590%22%5D&network=%5B%22S%22%2C%22O%22%5D&origin=FACETED_SEARCH&schoolFilter=%5B%2212731%22%2C%2212598%22%2C%2212691%22%2C%2212716%22%2C%2219926%22%2C%2212608%22%2C%2212682%22%5D&sid=SH9'

# Launch Linkedin
linkedin_page = driver = webdriver.Chrome(ChromeDriverManager().install())
linkedin_page.get(linkedin_weblink)
time.sleep(1)

with open('creds.json') as json_file:
    data = json.load(json_file)
    print(data)

email = data['email']
password = data['pass']


# Accept Cookies
linkedin_page.find_element_by_xpath('//*[@id="artdeco-global-alert-container"]/div[1]/section/div/div[2]/button[2]').click()
time.sleep(1)

# Click on sign in button
linkedin_page.find_element_by_xpath('/html/body/div[1]/main/p/a').click()
time.sleep(1)

# Send Email
linkedin_page.find_element_by_xpath('//*[@id="username"]').send_keys(email)
time.sleep(1)

# Send Password
linkedin_page.find_element_by_xpath('//*[@id="password"]').send_keys(password)
time.sleep(1)

# Click Login Button
linkedin_page.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()
time.sleep(1)

# CLick don't want to be remembered on this browser
try:
    linkedin_page.find_element_by_xpath('//*[@id="remember-me-prompt__form-secondary"]/button').click()
    time.sleep(1)
except Exception as e:
    pass

time.sleep(2)

# Reading HTML
html = linkedin_page.page_source

# Very important to let it sleep for at least 3 seconds otherwise it does not return the HTML / LXML
time.sleep(5)
soup = BeautifulSoup(html, 'lxml')

# Select all DIV type of codes
all_span = soup.find_all('span')

# Have it repeated 2 times for going on the next page
for i in range(5):

    #Scroll down to be able to load all the javascript with all HTML/XPATH information
    linkedin_page.execute_script("window.scrollTo(0, 300)")
    time.sleep(1)
    linkedin_page.execute_script("window.scrollTo(0, 600)")
    time.sleep(1)
    linkedin_page.execute_script("window.scrollTo(0, 900)")
    time.sleep(1)
    linkedin_page.execute_script("window.scrollTo(0, 1000)")
    time.sleep(1)
    # Have the main loading point be in the middle of the page
    linkedin_page.execute_script("window.scrollTo(0, 500)")
    time.sleep(4)

    # Read HTML for finding the connect IDs
    html = linkedin_page.page_source

    # Very important to let it sleep for at least 3 seconds otherwise it does not return the HTML / LXML
    time.sleep(5)
    soup = BeautifulSoup(html, 'lxml')

    time.sleep(3)
    # Get all the connect IDs
    ids = [r['id'] for r in soup.find_all('button',{'class':'artdeco-button artdeco-button--2 artdeco-button--secondary ember-view'}) if r.get('id') is not None and r.text == '\n\n    Connect\n']
    xpath_list = ['//*[@id="'+ id + '"]' for id in ids]

    for xpath in xpath_list:
        try:
            # Click on the Connect Button for first element in xpath_list
            time.sleep(4)
            linkedin_page.find_element_by_xpath(xpath).click()
            time.sleep(2)

            # Re-read all the HTML to find the id for "Send" button
            html = linkedin_page.page_source
            soup = BeautifulSoup(html, 'lxml')
            send_id = [r['id'] for r in soup.find_all('button',{'class':'ml1 artdeco-button artdeco-button--2 artdeco-button--primary ember-view'}) if r.get('id') is not None and r.text == '\n\n    Send\n']

            print('This is the send_id: ', send_id)
            send_id = '//*[@id="'+ send_id[0] + '"]'

            # Click on Send
            linkedin_page.find_element_by_xpath(send_id).click()
            time.sleep(2)

        except Exception as e:
            print('\n\n', e, '\n\n')

    #Scroll down because otherwise not able to find the "Next" button
    linkedin_page.execute_script("window.scrollTo(0, 1000)")
    time.sleep(3)

    # Re-real main page HTML to get id for "Next page"
    time.sleep(2)
    html = linkedin_page.page_source
    soup = BeautifulSoup(html, 'lxml')
    time.sleep(2)

    # Get ID for next page button
    next_page_id = [r['id'] for r in soup.find_all('button',{'class':'artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view'}) if r.get('id') is not None]
    next_page_id = '//*[@id="'+ next_page_id[0] + '"]'

    # Click on Next Page button
    linkedin_page.find_element_by_xpath(next_page_id).click()
    time.sleep(4)

print('Your networking has been automated 🚀')

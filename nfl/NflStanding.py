import json
import re
from pprint import pprint

# from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import os
from urllib import parse


class NflStanding:
    def __init__(self):
        self.delay = 30  # seconds
        self.path = os.path.dirname(__file__)
        self.pa="/home/shapjvcv/public_html/nflproapi/api/nfl/phantomjs"
        self.browser = webdriver.PhantomJS(self.pa)
        self.data1 = []
        self.data = []
        self.table_all = ''
        self.ul = ''
        self.soup = ''
        # pprint('PhantomJS started Working....')
        # browser.implicitly_wait(30)

    def scraper(self, url, p_class=''):
        self.browser.get(url)
        try:
            # pprint('Attempting to scrap data....')
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.TAG_NAME, p_class)))
            # print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        # browser.implicitly_wait(60)
        html = self.browser.page_source
        self.soup = BeautifulSoup(html, 'lxml')
        return self.soup

    def standing(self, url, presence_class=''):
        self.soup = self.scraper(url, presence_class)
        pprint(self.soup)
        self.table_all = self.soup.find_all('table')

        pprint('-------------- Team Standings------------------')
        pprint(self.table_all)
        for table in self.table_all:
            pprint(table)
            tbody = table.find('tbody')
            tr_all = tbody.find_all('tr')
            for tr in tr_all:
                # print('-----TR ---- '+tr.text+' -----------')
                print(tr)
                td = tr.find_all('td')
                print(td)
                td = [ele.text.strip() for ele in td]
                team_array = [ele for ele in td if ele]

                # team anme
                a1 = tr.find('a')
                url = a1['href']
                team = parse.parse_qs(parse.urlparse(url).query)['team'][0]
                # pprint(team)
                team_array.append(team)

                self.data.append(team_array)  # Get rid of empty values

        print('-------------------------------------standings-------------------------------------')
        pprint(self.data)

        result = {'standing': self.data}
        nfl_data = json.dumps(result)
        pprint(nfl_data)
        with open(self.path + '\standing.json', 'w') as f:
            f.write(nfl_data)
        self.browser.quit()
        return nfl_data




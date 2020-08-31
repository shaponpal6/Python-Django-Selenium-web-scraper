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


class NflTeams:
    def __init__(self):
        self.url = "http://www.nfl.com/teams/profile?team=NE"
        self.p_class = "NEcolors"
        self.delay = 30  # seconds
        self.path = os.path.dirname(__file__)
        pa="/home/nflpkuoi/public_html/api/api/nfl/phantomjs"
        self.browser = webdriver.PhantomJS(pa)
        # pprint('PhantomJS started Working....')
        # browser.implicitly_wait(30)

    def scraper(self, url, p_class=''):
        self.browser.get(url)
        try:
            # pprint('Attempting to scrap data....')
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.TAG_NAME, p_class)))
            # print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        # browser.implicitly_wait(60)
        html = self.browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def teams(self, url, p_class):
        soup = self.scraper(url, p_class)
        # pprint(soup)
        table_all = soup.find_all('table')
        # table_all = soup.find_all("div", {"id": "team-stats-wrapper"})

        # pprint('-------------- Team Standings------------------')
        # pprint(table_all[2])
        data = []
        i = 1
        for table in table_all:
            data_table = []
            # pprint('--------------Next Table------------------')
            # print(table)
            # data.append(str(table))
            # pprint('--------------Next Table------------------')
            tbody = table.find('tbody')
            tr_all = tbody.find_all('tr')
            for tr in tr_all:
                # print('-----TR ---- '+tr.text+' -----------')
                # print(tr)
                td = tr.find_all('td')
                # print('----------TD --------'+td.text+'------')
                td = [ele.text.strip() for ele in td]
                data_table.append([ele for ele in td if ele])  # Get rid of empty values

            data.append(data_table)

        # print('-------------------------------------standings-------------------------------------')
        # pprint(data)

        # result = {'teams': data }
        result = data
        nfl_data = json.dumps(result)
        # pprint(nfl_data)
        #par = parse.parse_qs(parse.urlparse(url).query)['team'][0]
        #if len(data[1]) > 1:
        #    pa = os.path.join("/home/shapjvcv/public_html/nflproapi/api/nfl/",'data/', par+'.json')
        #    with open(pa, 'w') as f:
        #        f.write(nfl_data)
        self.browser.quit()
        return nfl_data


# score_obj = NflTeams()
# score = score_obj.teams("http://www.nfl.com/teams/profile?team=NE", "NEcolors")
# pprint('================================================================================')
# pprint(score)



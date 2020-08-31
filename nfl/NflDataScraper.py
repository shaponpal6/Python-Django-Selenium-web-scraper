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


class NflDataScraper:
    def __init__(self):
        self.delay = 30  # seconds
        self.path = os.path.dirname(__file__)
        pa="/home/nflpkuoi/public_html/api/api/nfl/phantomjs"
        self.browser = webdriver.PhantomJS(pa)
        # pprint('PhantomJS started Working....')
        # browser.implicitly_wait(30)

    def scraper(self, url, presence_class=''):
        self.browser.get(url)
        try:
            # pprint('Attempting to scrap data....')
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, presence_class)))
            # print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        # browser.implicitly_wait(60)
        html = self.browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def point_table(self, url, presence_class=''):
        soup = self.scraper(url, presence_class)
        # pprint(soup)
        table_all = soup.find_all('table', {"class": "Table2__table-scroll"})
        abbr = soup.find_all('abbr', title=True)

        data = []
        team_id = 0
        for table in table_all:
            # print(table)
            # table_body = table.find('tbody')
            tr_all = table.find_all('tr')
            for tr in tr_all:
                td = tr.find_all('td')
                match = re.match(r"^\d+", td[0].text, re.I)
                if match:
                    td = [ele.text.strip() for ele in td]
                    team_array = [ele for ele in td if ele]
                    if abbr[team_id]:
                        team_array.append(abbr[team_id]['title'])
                        team_array.append(abbr[team_id].text)
                    data.append(team_array)
                    team_id = team_id + 1

        result = {'scores': data}
        nfl_data = json.dumps(result)
        if len(data) == 32:
            pa = os.path.join("/home/nflpkuoi/public_html/api/api/nfl/",'data/point-table.json')
            with open(pa, 'w') as f:
                f.write(nfl_data)
        self.browser.quit()
        return nfl_data


# nfl = NflDataScraper()
# point = nfl.point_table('http://www.espn.in/nfl/standings', 'glossary__title')
# pprint('-----------------------------ggggggggggggggggggggggggggggg--------------------------------------')
# pprint(point)


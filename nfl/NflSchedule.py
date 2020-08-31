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


class NflSchedule:
    def __init__(self):
        self.delay = 30  # seconds
        self.path = os.path.dirname(__file__)
        pa="/home/nflpkuoi/public_html/api/api/nfl/phantomjs"
        self.browser = webdriver.PhantomJS(pa)
        self.data1 = []
        self.data2 = []
        # pprint('PhantomJS started Working....')
        # browser.implicitly_wait(30)

    def scraper(self, url, p_class=''):
        self.browser.get(url)
        try:
            # pprint('Attempting to scrap data....')
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, p_class)))
            # print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        # self.browser.implicitly_wait(60)
        html = self.browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def schedule(self, url, presence_class=''):
        soup = self.scraper(url, presence_class)
        # pprint(soup)
        ul = soup.find_all('li', {"class": "score-strip-game"})
        # table_all = soup.find_all('table')

        # i = 1
        for li in ul:
            span = li.find_all('span')
            # pprint('---------start  --------')
            data11 = []
            for sp in span:
                data11.append(sp.text)
                # pprint(sp.text)
                # pprint(type(sp.text))
                # pprint('---------sp --------')
            # pprint(data11)
            if len(data11) == 7:
                data11[1] = data11[1] + ' ' + data11[2]
                del data11[2]
                data11[3] = data11[3] + ' ' + data11[4]
                del data11[4]
            if len(data11) == 6:
                match11 = re.match(r"^\W+", data11[2], re.I)
                if match11:
                    data11[1] = data11[1] + ' ' + data11[2]
                    del data11[2]
                else:
                    data11[3] = data11[3] + ' ' + data11[4]
                    del data11[4]

            # pprint(data11)
            self.data2.append(data11)
            # pprint('888888888888888---li ------------------')
            # pprint(span.text)
            # match = re.match(
            #     r"^(\D+)(\d+-\d+|\d+-\d+-\d+)(\D+)(\d+-\d+|\d+-\d+-\d+)(.+)", li.text,
            #     re.I)
            # pprint(match)
            # pprint(match.groups())
            # if match:
                # items = match.groups()
                # pprint('888888888888888---item ------------------')
                # pprint(items)
                # self.data1.append([ele for ele in items if ele])

                # pprint(li)
                # if(re.search(r"\sscore-strip-game\"",str(li))):
                #     nfl[i] = li.text
                # pprint(' # T:P:T:P:G # ')
                # i = i + 1

        # pprint('000000000000000000000-- data --000000000000000000000')
        # pprint(self.data1)
        result = {'schedule': self.data2}
        nfl_data = json.dumps(result)
        # pprint('------------------------ ssssssssssssssssssssssssss------------------------------')
        # pprint(len(self.data1))
        # pprint(self.data1)
        pa = os.path.join("/home/nflpkuoi/public_html/api/api/nfl/",'data/schedule.json')
        if len(self.data1) > 10:
            with open(pa, 'w') as f:
                f.write(nfl_data)
        self.browser.quit()
        return nfl_data


# score_obj = NflSchedule()
# score = score_obj.schedule('https://www.nfl.com/standings/division/2018/REG', 'score-strip-game')
# pprint(score)


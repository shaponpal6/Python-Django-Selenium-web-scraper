from urllib import parse

from bs4 import BeautifulSoup
import requests
import json
import os


class BeautifulTeam:
    def __init__(self):
        self.result = {}

    def run(self, url):
        # Here, we're just importing both Beautiful Soup and the Requests library
        page_link = 'http://www.nfl.com/teams/profile?team=NYJ'
        page_link = url
        # this is the url that we've already determined is safe and legal to scrape from.
        page_response = requests.get(page_link, timeout=5)
        # here, we fetch the content from the url, using the requests library
        page_content = BeautifulSoup(page_response.content, "html.parser")
        # we use the html parser to parse the url content and store it in a variable.
        table_all = page_content.find_all("table")

        if table_all is not None:
            data = []
            for table in table_all:
                data_table = []
                # print(table)
                # data.append(str(table))
                # tbody = table.find('tbody')
                tr_all = table.find_all('tr')
                if tr_all is not None:
                    for tr in tr_all:
                        # print('-----TR ---- '+tr.text+' -----------')
                        # print(tr)
                        td = tr.find_all('td')
                        # print('----------TD --------'+td.text+'------')
                        td = [ele.text.strip() for ele in td]
                        data_table.append([ele for ele in td if ele])  # Get rid of empty values
                    data.append(data_table)

        par = parse.parse_qs(parse.urlparse(url).query)['team'][0].strip().split(' ', 1)[0]
        #print(par)
        cwd = os.getcwd()  # Get the current working directory (cwd)
        # C:\Users\SHOPNOBUILDER\PycharmProjects\nflproApi\api\nfl
        #print(cwd)
        path5 = os.path.join(cwd,'api','nfl','data', par + '.json')
        #  “/home/shapjvcv/public_html/nflproapi/api/nfl/data”
        #print(path5)
        self.result = json.dumps(data)
        if len(data[1]) > 1:
            with open(path5, 'w') as f:
                f.write(self.result)
        #print(self.result)
        return self.result


# team = BeautifulTeam()
# team.run('http://www.nfl.com/teams/profile?team=NYJ')

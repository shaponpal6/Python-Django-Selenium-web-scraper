from django.http import HttpResponse
# from django.conf import settings
from api.nfl.NflDataScraper import NflDataScraper
from api.nfl.NflScoreBoard import NflScoreBoard
from api.nfl.NflTeams import NflTeams
from api.nfl.NflSchedule import NflSchedule
from api.nfl.NflStanding import NflStanding
from api.nfl.BeautifulTeam import BeautifulTeam
import urllib.parse
import time
import os
import sys
import json
import api



path = os.path.dirname(__file__)
pth = os.path.dirname(api.__file__)
data_path = "/home/shapjvcv/public_html/nflproapi/api/nfl/"

def index(request):
    q = request.GET.get('team', 'NE')
    uj = str('http://www.nfl.com/teams/profile?team='+ q)
    request.session['p_time'] = time.time()
    if 'p_time' in request.session:
        p_time2 = request.session['p_time']
        print(p_time2)
    new2 = time.time()
    new3 = time.time() + 30
    pp = os.path.join(path,"/data/NE5.json","hello/kh4")
    return HttpResponse(uj +" |||| "+ str(p_time2) + " Now" + str(new2) + "Now 3 " + str(new3))


def point_table(request):
    pt_time = 0
    thread = 30
    now = time.time()
    if 'pt_time' in request.session:
        pt_time = request.session['pt_time']
    if now > pt_time:
        point = 'less 30'
        nfl = NflDataScraper()
        point = nfl.point_table('http://www.espn.in/nfl/standings', 'glossary__title')
        request.session['pt_time'] = time.time() + thread
    else:
        pth = os.path.dirname(api.__file__)
        json2 = pth + "/nfl/data/point-table.json"
        with open(json2) as f:
            data = json.load(f)
            json_pretty = json.dumps(data, sort_keys=True, indent=4)
        point = json_pretty
    return HttpResponse(point, content_type="application/json")


def schedule(request):
    schedule_time = 0
    thread = 30
    now = time.time()
    if 'schedule_time' in request.session:
        schedule_time = request.session['schedule_time']
    if now > schedule_time:
        point = 'less 30'
        score_obj = NflSchedule()
        urlok = "https://www.nfl.com/standings/division/2018/REG"
        point = score_obj.schedule(urlok, 'score-strip-game')
        request.session['schedule_time'] = time.time() + thread
    else:
        pth = os.path.dirname(api.__file__)
        json2 = pth + "/nfl/data/schedule.json"
        with open(json2) as f:
            data = json.load(f)
            json_pretty = json.dumps(data, sort_keys=True, indent=4)
        point = json_pretty
    return HttpResponse(point, content_type="application/json")


def teams(request):
    q = request.GET.get('team', 'NE')
    url = str('http://www.nfl.com/teams/profile?team='+ q)
    pt_team = 0
    thread = 30
    now = time.time()
    if 'pt_team' in request.session:
        pt_team = request.session['pt_team']
    if now > pt_team:
        point = 'less 30'
        team = BeautifulTeam()
        point = team.run(url)
        request.session['pt_team'] = time.time() + thread
    else:
        pth = os.path.dirname(api.__file__)
        json2 = pth + "/nfl/data/"+ q +".json"
        with open(json2) as f:
            data = json.load(f)
            json_pretty = json.dumps(data, sort_keys=True, indent=4)
        point = json_pretty
    return HttpResponse(point, content_type="application/json")


def score_board(request):
    score_obj = NflScoreBoard()
    score = score_obj.score_board('https://www.nfl.com/standings/division/2018/REG', 'score-strip-game')
    return HttpResponse(score)


def standing(request):
    score_obj = NflStanding()
    score = score_obj.standing('https://www.nfl.com/standings/division/2018/REG', 'td')
    return HttpResponse(score)



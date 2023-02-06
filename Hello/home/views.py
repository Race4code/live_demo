from django.shortcuts import render,HttpResponse
from django.template import loader
from .models import *
from django.db import connection
import json

from .utility import *
# Create your views here.


def allTeams(request):
    data = fetch_data("select distinct(team1) from matches")
    teams = []
    for i in data:
        print(i[0])
        teams.append(i[0])
    response_json = json.dumps(teams)
    return HttpResponse(response_json)

def index(request):
    # data = my_custom_sql()
    # print(data)
    template_name = loader.get_template('index.html')
    return HttpResponse(template_name.render())
    # return HttpResponse("Hello Home Page")

# 1st graph query and data
def allMatches(request):
    data = fetch_data("select distinct(season) from matches order by season asc")
    newdata = list(data)
    number_match = []
    for i in newdata:
        query = f"select count(match_id) from matches where season={i[0]}"
        match_count = fetch_data(query)
        number_match.append({i[0]:match_count[0][0]})
    
    test_json=json.dumps(number_match)
    return HttpResponse(test_json)


# 2nd task solution funciton
def matchesWonByTeam(request,query):
    team=query
    fetchData = fetch_data("select distinct(season) from matches order by season asc")
    season_wise_won=[]
    for i in fetchData:
        query = f"select count(match_id) from matches where (team1='{team}' or team2='{team}') and winner='{team}' and season={i[0]}"
        number_of_match = fetch_data(query)
        season_wise_won.append({i[0]:number_of_match[0][0]})

    response_json = json.dumps(season_wise_won)
    return HttpResponse(response_json)


# 3rd query extra runs conceded per team in a particular year
def extraRuns(request,year):
    # year=2016
    team_in_year = fetch_data(f"select distinct(team1) from matches where season={year}")
    extra_runs=[]
    for i in team_in_year:
        query=f'select sum(extra_runs) from deliveries where match_id in(select match_id from matches where season={year} ) and bowling_team="{i[0]}"'
        runs = fetch_data(query)
        extra_runs.append({i[0]:int(runs[0][0])})
    print(extra_runs)
    response_json = json.dumps(extra_runs)
    return HttpResponse(response_json)

# 4th task economy of bowler
def bowlersEconomy(request,year):
    # year=2012
    id_range = fetch_data(f"select distinct(match_id) from matches where season={year}")
    start = id_range[0][0]
    siz = len(id_range)
    last=id_range[siz-1][0]
    bowlers = fetch_data(f"select distinct(bowler) from deliveries where match_id between {start} and {last}")
    bowlers_list=[]

    for i in bowlers:
        runs_spend = fetch_data(f"select sum(total_runs) from deliveries where (match_id between {start} and {last}) and bowler='{i[0]}'")
        bowler_match = fetch_data(f'select distinct(match_id) from deliveries where (match_id between {start} and {last}) and bowler="{i[0]}"')
        overs=0
        for j in bowler_match:
            temp = fetch_data(f"select count(distinct(`over`)) from deliveries where match_id={j[0]} and bowler='{i[0]}'")
            overs+=temp[0][0]
        bowlers_list.append({"name":i[0],"runs":int(runs_spend[0][0]),"overs":overs,"economy":float(int(runs_spend[0][0])/overs)})
    
    print(bowlers_list)
    response_json = json.dumps(bowlers_list)
    return HttpResponse(response_json)


# 5th task query function
def playVsWin(request,year):
    # year=2009
    # year = int(year)
    # team = teams(year)
    team = fetch_data(f"select distinct(team1) from matches where season={year}")
    play_vs_win = []
    for i in team:
        played = fetch_data(f"select count(match_id) from matches where (team1='{i[0]}' or team2='{i[0]}') and season={year}")
        wins = fetch_data(f"select count(match_id) from matches where (team1='{i[0]}' or team2='{i[0]}') and season={year} and winner='{i[0]}'")
        play_vs_win.append({"team":i[0],"played":int(played[0][0]),"wins":int(wins[0][0])})
    test_json = json.dumps(play_vs_win)
    return HttpResponse(test_json)

    
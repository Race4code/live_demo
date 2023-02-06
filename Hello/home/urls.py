from django.contrib import admin 
from django.urls import path
from home import views

urlpatterns = [
    path("",views.index,name="home"),
    path("allMatches",views.allMatches,name="allMatches"),
    path("extraRuns/<year>/",views.extraRuns,name="extraRuns"),
    path("matchesWonByTeam/<query>",views.matchesWonByTeam,name="matchesWonByTeam"),
    path("bowlersEconomy/<year>/",views.bowlersEconomy,name="bowlersEconomy"),
    path("playVsWin/<year>/",views.playVsWin,name="playVsWin"),
    path("allTeams",views.allTeams,name="allTeams")
]

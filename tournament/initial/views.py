from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from .models import Season,Fixture,Club
from django.forms.models import model_to_dict

from random import choice

from .fixture_generator import Generator

def index(request):
    return HttpResponse("Hello, world. You're at the initial index.")

def list(request):
    # Load seasons for the list page
    seasons = Season.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'season_list.html',
        {'seasons': seasons}
    )

def detail(request, pk):
    # Load the season for the detail page
    season = Season.objects.get(pk=pk)
    teams = season.getTeams().all()
    fixtures = Fixture.objects.filter(season_id = season.id)

    # Render list page with the documents and the form
    return render(
        request,
        'season_detail.html',
        {'season': season, 'fixtures': fixtures, 'teams': teams}
    )

class Match(object):
    homeTeam = ""
    awayTeam = ""
    # The class "constructor" - It's actually an initializer
    def __init__(self, homeTeam, awayTeam):
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam

# there could be a season type change like 'numberOfRounds'
def makefixture(request, pk):
    # Load the season to make fixture
    season = Season.objects.get(pk=pk)
    teams = season.getTeams().all()
    clubs = Club.objects.all()
    team_count = teams.count()

    generator = Generator(team_count)
    matches = generator.createFixtures()

    fixtures = []

    startWeek = 1
    clubList = clubs

    for match in matches:
        if match['week'] != startWeek:
            startWeek = match['week']
            clubList = clubs

        homeClub = choice(clubList)
        clubList = clubList.exclude(pk=homeClub.id)
        awayClub = choice(clubList)
        clubList = clubList.exclude(pk=awayClub.id)

        newFixture = Fixture(
            season_id=season,
            week=match['week'],
            home_team_id=teams[match['home'] - 1],
            home_team_club=homeClub,
            away_team_id=teams[match['away'] - 1],
            away_team_club=awayClub
        )
        fixtures.append(newFixture)

    return render(
        request,
        'fixture.html',
        {'season': season, 'fixtures': fixtures, 'teams': teams}
    )

def scoreboard(request, pk):
    season = Season.objects.get(pk=pk)
    teams = season.getTeams().all()
    fixtures = Fixture.objects.filter(season_id = season.id)

    teamList = []

    for team in teams:
        teamSummary = {
            "name": team.name,
            "games_played": 0,
            "win": 0,
            "drawn": 0,
            "lost": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0
        }

        for fixture in fixtures:
            if (fixture.is_played):
                if (fixture.home_team_id.id == team.id):
                    teamSummary['goals_for'] += fixture.home_score
                    teamSummary['goals_against'] += fixture.away_score

                    if (fixture.home_score > fixture.away_score):
                        teamSummary['win'] += 1
                        teamSummary['points'] += 3
                    elif (fixture.home_score < fixture.away_score):
                        teamSummary['lost'] += 1
                    else:
                        teamSummary['drawn'] += 1
                        teamSummary['points'] += 1
                if (fixture.away_team_id.id == team.id):
                    teamSummary['goals_for'] += fixture.away_score
                    teamSummary['goals_against'] += fixture.home_score

                    if (fixture.away_score > fixture.home_score):
                        teamSummary['win'] += 1
                        teamSummary['points'] += 3
                    elif (fixture.away_score < fixture.home_score):
                        teamSummary['lost'] += 1
                    else:
                        teamSummary['drawn'] += 1
                        teamSummary['points'] += 1
            teamSummary['games_played'] = teamSummary['win'] + teamSummary['drawn'] + teamSummary['lost']
            teamSummary['goal_difference'] = teamSummary['goals_for'] - teamSummary['goals_against']

        teamList.append(teamSummary)
        teamList.sort(key=lambda x: x['points'], reverse=True)

    return render(
        request,
        'scoreboard.html',
        {'season': season, 'teamList': teamList}
    )



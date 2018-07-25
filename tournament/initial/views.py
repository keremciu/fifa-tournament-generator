from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from .models import Season,Fixture,Club
from django.db.models import Q
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
    matchPerWeek = (len(fixtures) / 2) / len(teams)

    # Render list page with the documents and the form
    return render(
        request,
        'fixture.html',
        {'season': season, 'fixtures': fixtures, 'teams': teams, 'matchPerWeek': matchPerWeek}
    )

def teamfixture(request, pk, team):
    # Load the season for the detail page
    season = Season.objects.get(pk=pk)
    teams = season.getTeams().all()
    fixtures = Fixture.objects.filter(season_id = season.id)
    team_fixtures = fixtures.filter(Q(home_team_id=team) | Q(away_team_id=team))

    # Render list page with the documents and the form
    return render(
        request,
        'teamfixture.html',
        {'season': season, 'fixtures': team_fixtures, 'teams': teams, 'teamid': team}
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
    clubs = season.getClubs().all()
    team_count = teams.count()

    generator = Generator(team_count)
    matches = generator.createFixtures()

    fixtures = []
    team_club_assignment = {}
    # club_vs_club_assignment = {}

    startWeek = 1
    clubList = clubs

    for index, match in enumerate(matches):
        if match['week'] != startWeek:
            startWeek = match['week']
            clubList = clubs

        homeTeamID = teams[match['home'] - 1]
        awayTeamID = teams[match['away'] - 1]

        if homeTeamID not in team_club_assignment:
            team_club_assignment[homeTeamID] = []
        if awayTeamID not in team_club_assignment:
            team_club_assignment[awayTeamID] = []

        if (match['is_revenge']):
            inheritRevenge = fixtures[index - (len(matches) / 2)]
            homeClub = inheritRevenge.home_team_club
            awayClub = inheritRevenge.away_team_club
        else:
            homeClubList = clubList.exclude(pk__in=team_club_assignment[homeTeamID])
            homeClub = choice(homeClubList)
            clubList = clubList.exclude(pk=homeClub.id)
            team_club_assignment[homeTeamID].append(homeClub.id)
            awayClubList = clubList.exclude(pk__in=team_club_assignment[awayTeamID])
            awayClub = choice(awayClubList)
            clubList = clubList.exclude(pk=awayClub.id)
            team_club_assignment[awayTeamID].append(awayClub.id)
        # if len(homeClubList) > 0:
        # print(awayTeamID)
        # print(team_club_assignment[awayTeamID])
        # print(awayClubList)
        # if len(awayClubList) > 0:

        newFixture = Fixture(
            season_id=season,
            week=match['week'],
            home_team_id=homeTeamID,
            home_team_club=homeClub,
            away_team_id=awayTeamID,
            away_team_club=awayClub
        )
        fixtures.append(newFixture)

    matchPerWeek = (len(fixtures) / 2) / len(teams)

    return render(
        request,
        'fixture.html',
        {'season': season, 'fixtures': fixtures, 'teams': teams, 'matchPerWeek': matchPerWeek}
    )

def scoreboard(request, pk):
    season = Season.objects.get(pk=pk)
    teams = season.getTeams().all()
    fixtures = Fixture.objects.filter(season_id = season.id)

    teamList = []

    for team in teams:
        teamSummary = {
            "id": team.id,
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
        teamList.sort(key=lambda x: (x['points'], x['goal_difference']), reverse=True)

    return render(
        request,
        'scoreboard.html',
        {'season': season, 'teamList': teamList}
    )

def scoreboardand(request, pk):
    season = Season.objects.get(pk=pk)
    teams = season.getTeams().all()
    fixtures = Fixture.objects.filter(season_id = season.id)

    teamList = []

    for team in teams:
        teamSummary = {
            "id": team.id,
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
        teamList.sort(key=lambda x: (x['points'], x['goal_difference']), reverse=True)

    return render(
        request,
        'scoreboard_nonsmokers.html',
        {'season': season, 'teamList': teamList}
    )

def clubdetail(request, pk, club):
    # Load the season for the detail page
    season = Season.objects.get(pk=pk)
    teams = season.getTeams().all()
    fixtures = Fixture.objects.filter(season_id = season.id)
    club_fixtures = fixtures.filter(Q(home_team_club=club) | Q(away_team_club=club))

    # Render list page with the documents and the form
    return render(
        request,
        'clubdetail.html',
        {'season': season, 'fixtures': club_fixtures, 'teams': teams, 'clubid': club}
    )
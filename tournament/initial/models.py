from django.db import models
from django.contrib.auth.models import User

from random import randint

class Team(models.Model):
  name = models.CharField(max_length=255, blank=False, unique=True)
  owners = models.ManyToManyField(User, related_name='users')
  is_active = models.BooleanField(default=True)
  date_created = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)

  def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)

class Club(models.Model):
  name = models.CharField(max_length=255, blank=False, unique=True)
  logo = models.FileField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')
  owner = models.ForeignKey(Team, blank=True, null=True)
  is_active = models.BooleanField(default=True)
  date_created = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)

  def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)

class Season(models.Model):
  name = models.CharField(max_length=255, blank=False, unique=True)
  teams = models.ManyToManyField(Team, related_name='teamList')
  clubs = models.ManyToManyField(Club, related_name='clubList')
  prize = models.CharField(max_length=255, blank=False, unique=True)
  is_active = models.BooleanField(default=True)
  date_created = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)

  def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)

  def getTeams(self):
        return self.teams.all()
  
  def getClubs(self):
        return self.clubs.all()

  @property
  def fixture_details(self):
    fixtures = Fixture.objects.filter(season_id = self.id)
    fixturesCount = fixtures.count()
    playedFixtures = fixtures.filter(is_played = True)
    playedFixturesCount = playedFixtures.count()
    playedFixturesPercentage = 0
    if fixturesCount != 0:
      playedFixturesPercentage = playedFixturesCount / fixturesCount * 100

    return {
      'matchs_count': fixturesCount,
      'played_count': playedFixturesCount,
      'percentage': playedFixturesPercentage,
    }

  @property
  def fixture_percentage(self):
    return '%.2f' % self.fixture_details['percentage']

  @property
  def matchs_count(self):
    return self.fixture_details['matchs_count']

  @property
  def played_count(self):
    return self.fixture_details['played_count']

# TODO: not need this one
class Score(models.Model):
  season_id = models.ForeignKey(Season)
  team_id = models.ForeignKey(Team)
  win = models.IntegerField()
  draw = models.IntegerField()
  lost = models.IntegerField()
  goals_for = models.IntegerField()
  goals_against = models.IntegerField()
  goal_difference = models.IntegerField()
  is_active = models.BooleanField(default=True)
  date_created = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)

  def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)

class Fixture(models.Model):
  season_id = models.ForeignKey(Season)
  week = models.IntegerField()
  home_team_id = models.ForeignKey(Team, related_name='hometeam')
  home_team_club = models.ForeignKey(Club, blank=True, null=True, related_name='homeclub')
  away_team_id = models.ForeignKey(Team, related_name='awayteam')
  away_team_club = models.ForeignKey(Club, blank=True, null=True, related_name='awayclub')
  home_score = models.IntegerField(default=0)
  away_score = models.IntegerField(default=0)
  is_played = models.BooleanField(default=False)
  is_playoff_game = models.BooleanField(default=False)
  def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{season} ->> week {week}. {homeTeam}-{homeScore} VS {awayScore}-{awayTeam}".format(
          season=self.season_id,
          week=self.week,
          homeTeam=self.home_team_id,
          awayTeam=self.away_team_id,
          homeScore=self.home_score if self.is_played != 0 else '',
          awayScore=self.away_score if self.is_played != 0 else '',
        )

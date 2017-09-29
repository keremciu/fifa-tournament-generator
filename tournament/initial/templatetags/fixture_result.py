from django import template

register = template.Library()

@register.simple_tag
def get_result_class(teamid, fixture):
  teamid = int(teamid)
  result = 'info'
  if (fixture.home_team_id.id == teamid):
    if (fixture.home_score > fixture.away_score):
      result = 'success'
    elif (fixture.home_score < fixture.away_score):
      result = 'danger'
  if (fixture.away_team_id.id == teamid):
    if (fixture.away_score > fixture.home_score):
      result = 'success'
    elif (fixture.away_score < fixture.home_score):
      result = 'danger'

  return result

@register.filter()
def to_int(value):
    return int(value)
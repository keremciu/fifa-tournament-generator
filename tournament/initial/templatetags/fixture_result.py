from django import template

register = template.Library()

@register.simple_tag
def get_result_class(teamid, fixture):
  teamid = int(teamid)
  result = 'badge-info'
  if (fixture.home_team_id.id == teamid):
    if (fixture.home_score > fixture.away_score):
      result = 'badge-success'
    elif (fixture.home_score < fixture.away_score):
      result = 'badge-danger'
  if (fixture.away_team_id.id == teamid):
    if (fixture.away_score > fixture.home_score):
      result = 'badge-success'
    elif (fixture.away_score < fixture.home_score):
      result = 'badge-danger'

  return result

@register.filter()
def to_int(value):
    return int(value)
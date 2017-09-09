from django.contrib import admin

from .models import Team, Club, Season, Fixture

admin.register(Team, Club, Season, Fixture)(admin.ModelAdmin)
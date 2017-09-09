class Generator(object):
    def __init__(self, team_count):
        self.hasGhostTeam = team_count % 2 > 0
        self.team_count = team_count + 1 if team_count % 2 > 0 else team_count

    def createFixtures(self):
        initialFixtures = self.createInitialFixtures()
        returnFixtures = self.createReturnFixtures(initialFixtures)
        mergedFixtures = initialFixtures + returnFixtures

        return mergedFixtures

    def createFixture(self, home, away, week):
        fixture = {
            "home": home,
            "away": away,
            "week": week
        }

        return fixture

    def createInitialFixtures(self):
        fixtures = []

        for week_ind in range(1, self.team_count):
            fixtures = fixtures + self.createFixturesForWeek(week_ind)

        return fixtures

    def createFixturesForWeek(self, currentWeek):
        fixtures = []

        self.currentHome = self.team_count
        self.currentAway = currentWeek

        if (currentWeek % 2 != 0):
            self.toggleHomeAndAwayTeam

        if (self.shallFixtureBeGenerated()):
            fixtures.append(self.createFixture(self.currentHome, self.currentAway, currentWeek))

        for week_ind in range(1, (self.team_count // 2)):
            fixtures = fixtures + self.createFixturesForMatchIndex(currentWeek, week_ind)

        return fixtures

    def createFixturesForMatchIndex(self, week, index):
        fixtures = []
        self.currentAway = self.findCurrentAwayTeam(self.team_count, week, index)
        self.currentHome = self.findCurrentHomeTeam(self.team_count, week, index)

        if (index % 2 == 0):
            self.toggleHomeAndAwayTeam

        if (self.shallFixtureBeGenerated()):
            fixtures.append(self.createFixture(self.currentHome, self.currentAway, week))

        return fixtures

    def findCurrentHomeTeam(self, team_count, week, index):
        return self.wrapTeam((week + index) % (team_count - 1))

    def findCurrentAwayTeam(self, team_count, week, index):
        if (week - index < 0):
            team = team_count - 1 + week - index
        else:
            team = self.wrapTeam((week - index) % (team_count - 1))

        return team

    def wrapTeam(self, team):
        if (team == 0):
            team = self.team_count - 1

        return team

    def toggleHomeAndAwayTeam(self):
        self.currentHome, self.currentAway = self.currentAway, self.currentHome

    def isLastTeamCurrent(self):
        return self.team_count == self.currentHome or self.team_count == self.currentAway

    def shallFixtureBeGenerated(self):
        return not self.hasGhostTeam or not self.isLastTeamCurrent()

    def createReturnFixtures(self, initialFixtures):
        fixtures = []
        for homeFixture in initialFixtures:
            if (not self.hasGhostTeam or (self.team_count != homeFixture['away'] and self.team_count != homeFixture['home'])):
                fixtures.append(self.createFixture(homeFixture['away'], homeFixture['home'], homeFixture['week'] + self.team_count - 1))

        return fixtures

    def getCurrentHomeTeam(self):
        return self.currentHome

    def setCurrentHomeTeam(self, newCurrentHome):
        self.currentHome = newCurrentHome

    def getCurrentAwayTeam(self):
        return self.currentAway

    def setCurrentAwayTeam(self, newCurrentAway):
        self.currentAway = newCurrentAway
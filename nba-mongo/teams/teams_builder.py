# -*- coding: utf-8 -*-

import constants
from nba_request import NbaRequest
from teams import teams_fetcher

def build_teams_ids():
    """Build a list of all teams ids."""
    teams_ids = []

    common_team_years_params = {'LeagueID': constants.LEAGUE_ID_NBA}
    common_team_years_request = NbaRequest(constants.COMMON_TEAM_YEARS_ENDPOINT, common_team_years_params)
    common_team_years = common_team_years_request.send()

    if common_team_years:
        teams_row_set = common_team_years['resultSets'][0]['rowSet']
        for team_meta_data in teams_row_set:
            team_abbr = team_meta_data[4]
            # A team with a valid team_abbr ensures this is an active team.
            if team_abbr:
                teams_ids.append(team_meta_data[1])

    return teams_ids

def build_all_teams_documents():
    """Build a list of documents for all NBA teams."""
    teams_documents = []
    teams_ids = build_teams_ids()

    for team_id in teams_ids:
        team_document = build_team_document(team_id)
        teams_documents.append(team_document)

    return teams_documents

def build_team_document(team_id):
    """Build a team document.

    Keyword argument:
    team_id -- The id of the NBA team to build a document for.
    """
    team_document = {}
    teams_fetcher.fetch_team_info_common(team_id, team_document)
    teams_fetcher.fetch_team_roster(team_id, team_document)
    teams_fetcher.fetch_team_stats(team_id, team_document)

    return team_document

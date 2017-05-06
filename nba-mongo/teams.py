# -*- coding: utf-8 -*-

import constants
from nba_request import NbaRequest

def build_teams_ids():
    teams_ids = []

    common_team_years_params = {'LeagueID': constants.LEAGUE_ID_NBA}
    common_team_years_request = NbaRequest(constants.COMMON_TEAM_YEARS_ENDPOINT, common_team_years_params)
    common_team_years = common_team_years_request.send()

    if common_team_years:
        teams_row_set = common_team_years['resultSets'][0]['rowSet']
        for team_meta_data in teams_row_set:
            team_abbr = team_meta_data[4]
            if team_abbr:
                teams_ids.append(team_meta_data[1])

    return teams_ids

""" This function create a JSON document for each NBA team
    Structure:
    {
        nbaId: 1610612762,
        city: "Utah",
        name: "Jazz",
        fullName: "Utah Jazz", (city + name)
        abbreviation: "UTA",
        conference: "West",
        division: "Northwest",
        code: "jazz",
        players: [
            {
                nbaId: 204060,
                fullName: "Joe Ingles",
                jersey: "2",
                position: "F"
            },
            {
                nbaId: 202330,
                fullName: "Gordon Hayward",
                jersey: "20",
                position: "F"
            }
        ],
        coaches: [
            {
                nbaId: "SNY414587",
                fullName: "Quin Snyder",
                type: "Head Coach",
                school: "College - Duke"
            },
            {
                nbaId: "BRY269769",
                fullName: "Johnnie Bryant",
                type: "Assistant Coach",
                school: "College - Utah"
            }
        ]
    }
"""
def build_teams_documents():
    teams_documents = []
    teams_ids = build_teams_ids()

    for team_id in teams_ids:
        team_document = {}

        team_info_common_params = {
            'TeamID': team_id,
            'Season': constants.CURRENT_SEASON,
            'LeagueID': constants.LEAGUE_ID_NBA,
            'SeasonType': constants.REGULAR_SEASON
        }
        team_info_common_request = NbaRequest(constants.TEAM_INFO_COMMON_ENDPOINT, team_info_common_params)
        team_info_meta = team_info_common_request.send()

        if team_info_meta:
            team_info_row_set = team_info_meta['resultSets'][0]['rowSet'][0]
            team_document['nbaId'] = team_info_row_set[0]
            team_document['city'] = team_info_row_set[2]
            team_document['name'] = team_info_row_set[3]
            team_document['fullName'] = team_document['city'] + ' ' + team_document['name']
            team_document['abbreviation'] = team_info_row_set[4]
            team_document['conference'] = team_info_row_set[5]
            team_document['division'] = team_info_row_set[6]
            team_document['code'] = team_info_row_set[7]

        common_team_roster_params = {
            'TeamID': team_id,
            'Season': constants.CURRENT_SEASON
        }
        common_team_roster_request = NbaRequest(constants.COMMON_TEAM_ROSTER_ENDPOINT, common_team_roster_params)
        common_team_roster_meta = common_team_roster_request.send()

        team_document['players'] = []
        team_document['coaches'] = []
        if common_team_roster_meta:
            team_players_row_set = common_team_roster_meta['resultSets'][0]['rowSet']
            for player in team_players_row_set:
                player_info = {}
                player_info['nbaId'] = player[12]
                player_info['fullName'] = player[3]
                player_info['jersey'] = player[4]
                player_info['position'] = player[5]
                team_document['players'].append(player_info)

            team_coaches_row_set = common_team_roster_meta['resultSets'][1]['rowSet']
            for coach in team_coaches_row_set:
                coach_info = {}
                coach_info['nbaId'] = coach[2]
                coach_info['fullName'] = coach[5]
                coach_info['type'] = coach[8]
                coach_info['school'] = coach[9]
                team_document['coaches'].append(coach_info)

        teams_documents.append(team_document)

    return teams_documents

# -*- coding: utf-8 -*-

import constants
from nba_request import NbaRequest

def build_players_ids():
    players_ids = []

    common_all_players_params = {
        'LeagueID': constants.LEAGUE_ID_NBA,
        'Season': constants.CURRENT_SEASON,
        'IsOnlyCurrentSeason': 1
    }
    common_all_players_request = NbaRequest(constants.COMMON_ALL_PLAYERS_ENDPOINT, common_all_players_params)
    common_all_players = common_all_players_request.send()

    if common_all_players:
        players_row_set = common_all_players['resultSets'][0]['rowSet']
        for player_meta_data in players_row_set:
            players_ids.append(player_meta_data[0])

    return players_ids

""" This function create a JSON document for each NBA player
    Structure:
    {
        nbaId: 202322,
        firstName: "John",
        lastName: "Wall",
        fullName: "John Wall",
        initName: "J. Wall",
        birthDate: "1990-09-06T00:00:00",
        school: "Kentucky",
        country: "USA",
        height: "6-4",
        weight: "210",
        seasonExp: 6,
        jersey: "2",
        position: "Guard",
        code: "john_wall",
        team: {
            nbaId: 1610612764,
            city: "Washington",
            name: "Wizards",
            fullName: "Washington Wizards",
            abbreviation: "WAS"
        }
    }
"""
def build_players_documents():
    players_documents = []
    players_ids = build_players_ids()

    for player_id in players_ids:
        player_document = {}
        common_player_info_params = {
            'PlayerID': player_id
        }
        common_player_info_request = NbaRequest(constants.COMMON_PLAYER_INFO_ENDPOINT, common_player_info_params)
        common_player_meta = common_player_info_request.send()

        if common_player_meta:
            common_player_row_set = common_player_meta['resultSets'][0]['rowSet'][0]
            player_document['nbaId'] = common_player_row_set[0]
            player_document['firstName'] = common_player_row_set[1]
            player_document['lastName'] = common_player_row_set[2]
            player_document['fullName'] = common_player_row_set[3]
            player_document['initName'] = common_player_row_set[5]
            player_document['birthDate'] = common_player_row_set[6]
            player_document['school'] = common_player_row_set[7]
            player_document['country'] = common_player_row_set[8]
            player_document['height'] = common_player_row_set[10]
            player_document['weight'] = common_player_row_set[11]
            player_document['seasonExp'] = common_player_row_set[12]
            player_document['jersey'] = common_player_row_set[13]
            player_document['position'] = common_player_row_set[14]
            player_document['code'] = common_player_row_set[21]

            player_team = {}
            player_team['nbaId'] = common_player_row_set[16]
            player_team['city'] = common_player_row_set[20]
            player_team['name'] = common_player_row_set[17]
            player_team['fullName'] = player_team['city'] + ' ' + player_team['name']
            player_team['abbreviation'] = common_player_row_set[18]
            player_document['team'] = player_team

        players_documents.append(player_document)

    return players_documents

# -*- coding: utf-8 -*-

import constants
from nba_request import NbaRequest
from players import players_fetcher

def build_players_ids():
    """Build a list of all players ids."""
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

def build_all_players_documents():
    """Build a list of documents for all active NBA players."""
    players_documents = []
    players_ids = build_players_ids()

    for player_id in players_ids:
        player_document = build_player_document(player_id)
        players_documents.append(player_document)

    return players_documents

def build_player_document(player_id):
    """Build a player document.

    Keyword argument:
    player_id -- The id of the NBA player to build a document for.
    """
    player_document = {}
    players_fetcher.fetch_common_player_info(player_id, player_document)
    players_fetcher.fetch_player_stats(player_id, player_document)

    return player_document

# -*- coding: utf-8 -*-

import constants
from nba_request import NbaRequest

def fetch_common_player_info(player_id, player_document):
    """Fetch and populate the common info for a given player.

    The common info for a player are retrieved by requesting the 'commonplayerinfo' endpoint.
    Only immutable data are kept and correspond to the current season.

    Keyword arguments:
    player_id -- The id of the NBA player to fetch common info for.
    player_document -- The NBA player document to populate.
    """
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
        player_document['draftYear'] = common_player_row_set[26]
        player_document['draftRound'] = common_player_row_set[27]
        player_document['draftNumber'] = common_player_row_set[28]

        player_team = {}
        player_team['nbaId'] = common_player_row_set[16]
        player_team['city'] = common_player_row_set[20]
        player_team['name'] = common_player_row_set[17]
        player_team['fullName'] = player_team['city'] + ' ' + player_team['name']
        player_team['abbreviation'] = common_player_row_set[18]
        player_document['team'] = player_team

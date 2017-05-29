# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch
import json

from nba_request import NbaRequest
from players import players_fetcher

class TestPlayersFetcher(unittest.TestCase):

    @patch('nba_request.NbaRequest.send')
    def test_fetch_common_player_info(self, mock_request):
        mock_request.return_value = json.loads(
        """
        {
            "resource":"commonplayerinfo",
            "parameters":[
                {
                    "PlayerID":2546
                },
                {
                    "LeagueID":null
                }
            ],
            "resultSets":[
                {
                    "name":"CommonPlayerInfo",
                    "headers":[
                        "PERSON_ID",
                        "FIRST_NAME",
                        "LAST_NAME",
                        "DISPLAY_FIRST_LAST",
                        "DISPLAY_LAST_COMMA_FIRST",
                        "DISPLAY_FI_LAST",
                        "BIRTHDATE",
                        "SCHOOL",
                        "COUNTRY",
                        "LAST_AFFILIATION",
                        "HEIGHT",
                        "WEIGHT",
                        "SEASON_EXP",
                        "JERSEY",
                        "POSITION",
                        "ROSTERSTATUS",
                        "TEAM_ID",
                        "TEAM_NAME",
                        "TEAM_ABBREVIATION",
                        "TEAM_CODE",
                        "TEAM_CITY",
                        "PLAYERCODE",
                        "FROM_YEAR",
                        "TO_YEAR",
                        "DLEAGUE_FLAG",
                        "GAMES_PLAYED_FLAG",
                        "DRAFT_YEAR",
                        "DRAFT_ROUND",
                        "DRAFT_NUMBER"
                    ],
                    "rowSet":[
                        [
                            2546,
                            "Carmelo",
                            "Anthony",
                            "Carmelo Anthony",
                            "Anthony, Carmelo",
                            "C. Anthony",
                            "1984-05-29T00:00:00",
                            "Syracuse",
                            "USA",
                            "Syracuse/USA",
                            "6-8",
                            "240",
                            13,
                            "7",
                            "Forward",
                            "Active",
                            1610612752,
                            "Knicks",
                            "NYK",
                            "knicks",
                            "New York",
                            "carmelo_anthony",
                            2003,
                            2016,
                            "N",
                            "Y",
                            "2003",
                            "1",
                            "3"
                        ]
                    ]
                }
            ]
        }
        """
        )

        expected_player_document = json.loads(
        """
        {
            "nbaId": 2546,
            "firstName": "Carmelo",
            "lastName": "Anthony",
            "fullName": "Carmelo Anthony",
            "initName": "C. Anthony",
            "birthDate": "1984-05-29T00:00:00",
            "school": "Syracuse",
            "country": "USA",
            "height": "6-8",
            "weight": "240",
            "seasonExp": 13,
            "jersey": "7",
            "position": "Forward",
            "code": "carmelo_anthony",
            "draftYear": "2003",
            "draftRound": "1",
            "draftNumber": "3",
            "team": {
                "nbaId": 1610612752,
                "city": "New York",
                "name": "Knicks",
                "fullName": "New York Knicks",
                "abbreviation": "NYK"
            }
        }
        """
        )

        actual_player_document = {}
        players_fetcher.fetch_common_player_info(2546, actual_player_document)

        self.assertDictEqual(expected_player_document, actual_player_document)

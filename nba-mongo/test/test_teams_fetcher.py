# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch
import json

from nba_request import NbaRequest
from teams import teams_fetcher

class TestTeamsFetcher(unittest.TestCase):

    @patch('nba_request.NbaRequest.send')
    def test_fetch_team_info_common(self, mock_request):
        mock_request.return_value = json.loads(
        """
        {
            "resource":"teaminfocommon",
            "parameters":{
                "LeagueID":"00",
                "Season":"2016-17",
                "SeasonType":"Regular Season",
                "TeamID":1610612762
            },
            "resultSets":[
                {
                    "name":"TeamInfoCommon",
                    "headers":[
                        "TEAM_ID",
                        "SEASON_YEAR",
                        "TEAM_CITY",
                        "TEAM_NAME",
                        "TEAM_ABBREVIATION",
                        "TEAM_CONFERENCE",
                        "TEAM_DIVISION",
                        "TEAM_CODE",
                        "W",
                        "L",
                        "PCT",
                        "CONF_RANK",
                        "DIV_RANK",
                        "MIN_YEAR",
                        "MAX_YEAR"
                    ],
                    "rowSet":[
                        [
                            1610612762,
                            "2016-17",
                            "Utah",
                            "Jazz",
                            "UTA",
                            "West",
                            "Northwest",
                            "jazz",
                            51,
                            31,
                            0.622,
                            5,
                            1,
                            "1974",
                            "2016"
                        ]
                    ]
                },
                {
                    "name":"TeamSeasonRanks",
                    "headers":[
                        "LEAGUE_ID",
                        "SEASON_ID",
                        "TEAM_ID",
                        "PTS_RANK",
                        "PTS_PG",
                        "REB_RANK",
                        "REB_PG",
                        "AST_RANK",
                        "AST_PG",
                        "OPP_PTS_RANK",
                        "OPP_PTS_PG"
                    ],
                    "rowSet":[
                        [
                            "00",
                            "22016",
                            1610612762,
                            28,
                            100.7,
                            19,
                            43.2,
                            28,
                            20.1,
                            1,
                            96.8
                        ]
                    ]
                }
            ]
        }
        """
        )

        expected_team_document = json.loads(
        """
        {
            "nbaId": 1610612762,
            "city": "Utah",
            "name": "Jazz",
            "fullName": "Utah Jazz",
            "abbreviation": "UTA",
            "conference": "West",
            "division": "Northwest",
            "code": "jazz"
        }
        """
        )

        actual_team_document = {}
        teams_fetcher.fetch_team_info_common(1610612762, actual_team_document)

        self.assertDictEqual(expected_team_document, actual_team_document)

    @patch('nba_request.NbaRequest.send')
    def test_fetch_team_roster(self, mock_request):
        mock_request.return_value = json.loads(
        """
        {
            "resource":"commonteamroster",
            "parameters":{
                "TeamID":1610612752,
                "LeagueID":null,
                "Season":"2015-16"
            },
            "resultSets":[
                {
                    "name":"CommonTeamRoster",
                    "headers":[
                        "TeamID",
                        "SEASON",
                        "LeagueID",
                        "PLAYER",
                        "NUM",
                        "POSITION",
                        "HEIGHT",
                        "WEIGHT",
                        "BIRTH_DATE",
                        "AGE",
                        "EXP",
                        "SCHOOL",
                        "PLAYER_ID"
                    ],
                    "rowSet":[
                        [
                            1610612752,
                            "2015",
                            "00",
                            "Kevin Seraphin",
                            "1",
                            "F-C",
                            "6-10",
                            "278",
                            "DEC 07, 1989",
                            26,
                            "5",
                            "Le Moyne",
                            202338
                        ],
                        [
                            1610612752,
                            "2015",
                            "00",
                            "Langston Galloway",
                            "2",
                            "G",
                            "6-2",
                            "200",
                            "DEC 09, 1991",
                            24,
                            "1",
                            "Saint Joseph's",
                            204038
                        ],
                        [
                            1610612752,
                            "2015",
                            "00",
                            "Jose Calderon",
                            "3",
                            "G",
                            "6-3",
                            "200",
                            "SEP 28, 1981",
                            34,
                            "10",
                            "Villanueva de la Serena, Spain",
                            101181
                        ]
                    ]
                },
                {
                    "name":"Coaches",
                    "headers":[
                        "TEAM_ID",
                        "SEASON",
                        "COACH_ID",
                        "FIRST_NAME",
                        "LAST_NAME",
                        "COACH_NAME",
                        "COACH_CODE",
                        "IS_ASSISTANT",
                        "COACH_TYPE",
                        "SCHOOL",
                        "SORT_SEQUENCE"
                    ],
                    "rowSet":[
                        [
                            1610612752,
                            "2015",
                            "HOR592895",
                            "Jeff",
                            "Hornacek",
                            "Jeff Hornacek",
                            "jeff_hornacek",
                            1,
                            "Head Coach",
                            "College - Iowa State",
                            161
                        ],
                        [
                            1610612752,
                            "2015",
                            "GOE444954",
                            "Anthony",
                            "Goenaga",
                            "Anthony Goenaga",
                            "anthony_goenaga",
                            4,
                            "Assistant Trainer",
                            "College - Long Island University",
                            163
                        ]
                    ]
                }
            ]
        }
        """
        )

        expected_team_document = json.loads(
        """
        {
            "players": [
                {
                    "nbaId": 202338,
                    "fullName": "Kevin Seraphin",
                    "jersey": "1",
                    "position": "F-C"
                },
                {
                    "nbaId": 204038,
                    "fullName": "Langston Galloway",
                    "jersey": "2",
                    "position": "G"
                },
                {
                    "nbaId": 101181,
                    "fullName": "Jose Calderon",
                    "jersey": "3",
                    "position": "G"
                }
            ],
            "coaches": [
                {
                    "nbaId": "HOR592895",
                    "fullName": "Jeff Hornacek",
                    "type": "Head Coach",
                    "school": "College - Iowa State"
                },
                {
                    "nbaId": "GOE444954",
                    "fullName": "Anthony Goenaga",
                    "type": "Assistant Trainer",
                    "school": "College - Long Island University"
                }
            ]
        }
        """
        )

        actual_team_document = {}
        teams_fetcher.fetch_team_roster(1610612752, actual_team_document)

        self.assertDictEqual(expected_team_document, actual_team_document)

    @patch('nba_request.NbaRequest.send')
    def test_fetch_team_stats(self, mock_request):
        mock_stats_per_game = json.loads(
        """
        {
            "resource":"teamyearbyyearstats",
            "parameters":{
                "LeagueID":"00",
                "SeasonType":"Regular Season",
                "PerMode":"PerGame",
                "TeamID":1610612754
            },
            "resultSets":[
                {
                    "name":"TeamStats",
                    "headers":[
                        "TEAM_ID",
                        "TEAM_CITY",
                        "TEAM_NAME",
                        "YEAR",
                        "GP",
                        "WINS",
                        "LOSSES",
                        "WIN_PCT",
                        "CONF_RANK",
                        "DIV_RANK",
                        "PO_WINS",
                        "PO_LOSSES",
                        "CONF_COUNT",
                        "DIV_COUNT",
                        "NBA_FINALS_APPEARANCE",
                        "FGM",
                        "FGA",
                        "FG_PCT",
                        "FG3M",
                        "FG3A",
                        "FG3_PCT",
                        "FTM",
                        "FTA",
                        "FT_PCT",
                        "OREB",
                        "DREB",
                        "REB",
                        "AST",
                        "PF",
                        "STL",
                        "TOV",
                        "BLK",
                        "PTS",
                        "PTS_RANK"
                    ],
                    "rowSet":[
                        [
                            1610612754,
                            "Indiana",
                            "Pacers",
                            "2015-16",
                            82,
                            45,
                            37,
                            0.549,
                            7,
                            2,
                            3,
                            4,
                            15,
                            5,
                            "N/A",
                            38.3,
                            85.2,
                            0.45,
                            8.1,
                            23.0,
                            0.351,
                            17.4,
                            22.8,
                            0.764,
                            10.3,
                            33.9,
                            44.2,
                            21.2,
                            20.0,
                            9.0,
                            14.9,
                            4.8,
                            102.2,
                            17
                        ],
                        [
                            1610612754,
                            "Indiana",
                            "Pacers",
                            "2016-17",
                            82,
                            42,
                            40,
                            0.512,
                            7,
                            3,
                            0,
                            4,
                            15,
                            5,
                            "N/A",
                            39.3,
                            84.5,
                            0.465,
                            8.6,
                            23.0,
                            0.376,
                            17.9,
                            22.1,
                            0.81,
                            9.0,
                            33.0,
                            42.0,
                            22.5,
                            19.5,
                            8.2,
                            13.8,
                            5.0,
                            105.1,
                            15
                        ]
                    ]
                }
            ]
        }
        """
        )
        mock_stats_totals = json.loads(
        """
        {
            "resource":"teamyearbyyearstats",
            "parameters":{
                "LeagueID":"00",
                "SeasonType":"Regular Season",
                "PerMode":"Totals",
                "TeamID":1610612754
            },
            "resultSets":[
                {
                    "name":"TeamStats",
                    "headers":[
                        "TEAM_ID",
                        "TEAM_CITY",
                        "TEAM_NAME",
                        "YEAR",
                        "GP",
                        "WINS",
                        "LOSSES",
                        "WIN_PCT",
                        "CONF_RANK",
                        "DIV_RANK",
                        "PO_WINS",
                        "PO_LOSSES",
                        "CONF_COUNT",
                        "DIV_COUNT",
                        "NBA_FINALS_APPEARANCE",
                        "FGM",
                        "FGA",
                        "FG_PCT",
                        "FG3M",
                        "FG3A",
                        "FG3_PCT",
                        "FTM",
                        "FTA",
                        "FT_PCT",
                        "OREB",
                        "DREB",
                        "REB",
                        "AST",
                        "PF",
                        "STL",
                        "TOV",
                        "BLK",
                        "PTS",
                        "PTS_RANK"
                    ],
                    "rowSet":[
                        [
                            1610612754,
                            "Indiana",
                            "Pacers",
                            "2015-16",
                            82,
                            45,
                            37,
                            0.549,
                            7,
                            2,
                            3,
                            4,
                            15,
                            5,
                            "N/A",
                            3142,
                            6985,
                            0.45,
                            663,
                            1889,
                            0.351,
                            1430,
                            1872,
                            0.764,
                            847,
                            2779,
                            3626,
                            1741,
                            1641,
                            742,
                            1219,
                            391,
                            8377,
                            17
                        ],
                        [
                            1610612754,
                            "Indiana",
                            "Pacers",
                            "2016-17",
                            82,
                            42,
                            40,
                            0.512,
                            7,
                            3,
                            0,
                            4,
                            15,
                            5,
                            "N/A",
                            3221,
                            6931,
                            0.465,
                            709,
                            1885,
                            0.376,
                            1467,
                            1811,
                            0.81,
                            742,
                            2702,
                            3444,
                            1844,
                            1597,
                            669,
                            1130,
                            409,
                            8618,
                            15
                        ]
                    ]
                }
            ]
        }
        """
        )

        mock_request.side_effect = (mock_stats_per_game, mock_stats_totals)

        expected_team_document = json.loads(
        """
        {
            "stats": {
                "regularSeason": [
                    {
                        "year": "2015-16",
                        "gp": 82,
                        "wins": 45,
                        "losses": 37,
                        "winPct": 0.549,
                        "confRank": 7,
                        "divRank": 2,
                        "ptsRank": 17,
                        "perGame": {
                            "fgm": 38.3,
                            "fga": 85.2,
                            "fgPct": 0.45,
                            "fg3m": 8.1,
                            "fg3a": 23.0,
                            "fg3Pct": 0.351,
                            "ftm": 17.4,
                            "fta": 22.8,
                            "ftPct": 0.764,
                            "oReb": 10.3,
                            "dReb": 33.9,
                            "reb": 44.2,
                            "ast": 21.2,
                            "pf": 20.0,
                            "stl": 9.0,
                            "tov": 14.9,
                            "blk": 4.8,
                            "pts": 102.2
                        },
                        "totals": {
                            "fgm": 3142,
                            "fga": 6985,
                            "fgPct": 0.45,
                            "fg3m": 663,
                            "fg3a": 1889,
                            "fg3Pct": 0.351,
                            "ftm": 1430,
                            "fta": 1872,
                            "ftPct": 0.764,
                            "oReb": 847,
                            "dReb": 2779,
                            "reb": 3626,
                            "ast": 1741,
                            "pf": 1641,
                            "stl": 742,
                            "tov": 1219,
                            "blk": 391,
                            "pts": 8377
                        }
                    },
                    {
                        "year": "2016-17",
                        "gp": 82,
                        "wins": 42,
                        "losses": 40,
                        "winPct": 0.512,
                        "confRank": 7,
                        "divRank": 3,
                        "ptsRank": 15,
                        "perGame": {
                            "fgm": 39.3,
                            "fga": 84.5,
                            "fgPct": 0.465,
                            "fg3m": 8.6,
                            "fg3a": 23.0,
                            "fg3Pct": 0.376,
                            "ftm": 17.9,
                            "fta": 22.1,
                            "ftPct": 0.81,
                            "oReb": 9.0,
                            "dReb": 33.0,
                            "reb": 42.0,
                            "ast": 22.5,
                            "pf": 19.5,
                            "stl": 8.2,
                            "tov": 13.8,
                            "blk": 5.0,
                            "pts": 105.1
                        },
                        "totals": {
                            "fgm": 3221,
                            "fga": 6931,
                            "fgPct": 0.465,
                            "fg3m": 709,
                            "fg3a": 1885,
                            "fg3Pct": 0.376,
                            "ftm": 1467,
                            "fta": 1811,
                            "ftPct": 0.81,
                            "oReb": 742,
                            "dReb": 2702,
                            "reb": 3444,
                            "ast": 1844,
                            "pf": 1597,
                            "stl": 669,
                            "tov": 1130,
                            "blk": 409,
                            "pts": 8618
                        }
                    }
                ]
            }
        }
        """
        )

        actual_team_document = {}
        teams_fetcher.fetch_team_stats(1610612754, actual_team_document)

        self.assertDictEqual(expected_team_document, actual_team_document)

if __name__ == '__main__':
    unittest.main()

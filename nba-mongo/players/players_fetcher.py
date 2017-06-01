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

def fetch_player_stats(player_id, player_document):
    """Fetch and populate all career statistics for a given player.

    The career statistics for a player are retrieved by requesting the 'playerprofilev2' endpoint.
    These statistics are composed of four distinct categories:
     - regularSeasons: gathers per game and totals statistics for all regular seasons
     - playoffs: gathers per game and totals statistics for all post seasons (if any)
     - careerRegularSeasons: TODO
     - careerPlayoffs: TODO

    Keyword argument:
    player_id -- The id of the NBA player to fetch statistics for.
    player_document -- The NBA player document to populate.
    """
    player_document['stats'] = {}
    player_document['stats']['regularSeasons'] = []
    player_document['stats']['playoffs'] = []
    player_document['stats']['careerRegularSeasons'] = {}
    player_document['stats']['careerPlayoffs'] = {}

    # Stats Per Game
    player_stats_per_game_params = {
        'PlayerID': player_id,
        'PerMode': 'PerGame'
    }
    player_stats_per_game_request = NbaRequest(constants.PLAYER_PROFILE_V2_ENDPOINT, player_stats_per_game_params)
    player_stats_per_game_meta = player_stats_per_game_request.send()

    # Stats Totals
    player_stats_totals_params = {
        'PlayerID': player_id,
        'PerMode': 'Totals'
    }
    player_stats_totals_request = NbaRequest(constants.PLAYER_PROFILE_V2_ENDPOINT, player_stats_totals_params)
    player_stats_totals_meta = player_stats_totals_request.send()

    if player_stats_per_game_meta and player_stats_totals_meta:
        player_stats_per_game_result_sets = player_stats_per_game_meta['resultSets']
        player_stats_totals_result_sets = player_stats_totals_meta['resultSets']

        # Regular Seasons stats per seasons
        player_stats_per_game_regular_seasons = player_stats_per_game_result_sets[0]['rowSet']
        player_stats_totals_regular_seasons = player_stats_totals_result_sets[0]['rowSet']
        for per_game_stats, totals_stats in zip(player_stats_per_game_regular_seasons, player_stats_totals_regular_seasons):
            per_game_season = per_game_stats[1]
            totals_season = totals_stats[1]

            if per_game_season == totals_season:
                reg_season_stats = {}
                # First, gather common statistics for a given season
                reg_season_stats['season'] = per_game_stats[1]
                reg_season_stats['teamId'] = per_game_stats[3]
                reg_season_stats['teamAbbreviation'] = per_game_stats[4]
                reg_season_stats['age'] = per_game_stats[5]
                reg_season_stats['gp'] = per_game_stats[6]
                reg_season_stats['gs'] = per_game_stats[7]

                reg_season_stats['perGame'] = {}
                reg_season_stats['perGame']['min'] = per_game_stats[8]
                reg_season_stats['perGame']['fgm'] = per_game_stats[9]
                reg_season_stats['perGame']['fga'] = per_game_stats[10]
                reg_season_stats['perGame']['fgPct'] = per_game_stats[11]
                reg_season_stats['perGame']['fg3m'] = per_game_stats[12]
                reg_season_stats['perGame']['fg3a'] = per_game_stats[13]
                reg_season_stats['perGame']['fg3Pct'] = per_game_stats[14]
                reg_season_stats['perGame']['ftm'] = per_game_stats[15]
                reg_season_stats['perGame']['fta'] = per_game_stats[16]
                reg_season_stats['perGame']['ftPct'] = per_game_stats[17]
                reg_season_stats['perGame']['oReb'] = per_game_stats[18]
                reg_season_stats['perGame']['dReb'] = per_game_stats[19]
                reg_season_stats['perGame']['reb'] = per_game_stats[20]
                reg_season_stats['perGame']['ast'] = per_game_stats[21]
                reg_season_stats['perGame']['stl'] = per_game_stats[22]
                reg_season_stats['perGame']['blk'] = per_game_stats[23]
                reg_season_stats['perGame']['tov'] = per_game_stats[24]
                reg_season_stats['perGame']['pf'] = per_game_stats[25]
                reg_season_stats['perGame']['pts'] = per_game_stats[26]

                reg_season_stats['totals'] = {}
                reg_season_stats['totals']['min'] = totals_stats[8]
                reg_season_stats['totals']['fgm'] = totals_stats[9]
                reg_season_stats['totals']['fga'] = totals_stats[10]
                reg_season_stats['totals']['fgPct'] = totals_stats[11]
                reg_season_stats['totals']['fg3m'] = totals_stats[12]
                reg_season_stats['totals']['fg3a'] = totals_stats[13]
                reg_season_stats['totals']['fg3Pct'] = totals_stats[14]
                reg_season_stats['totals']['ftm'] = totals_stats[15]
                reg_season_stats['totals']['fta'] = totals_stats[16]
                reg_season_stats['totals']['ftPct'] = totals_stats[17]
                reg_season_stats['totals']['oReb'] = totals_stats[18]
                reg_season_stats['totals']['dReb'] = totals_stats[19]
                reg_season_stats['totals']['reb'] = totals_stats[20]
                reg_season_stats['totals']['ast'] = totals_stats[21]
                reg_season_stats['totals']['stl'] = totals_stats[22]
                reg_season_stats['totals']['blk'] = totals_stats[23]
                reg_season_stats['totals']['tov'] = totals_stats[24]
                reg_season_stats['totals']['pf'] = totals_stats[25]
                reg_season_stats['totals']['pts'] = totals_stats[26]

                player_document['stats']['regularSeasons'].append(reg_season_stats)

        # Post Seasons stats per seasons
        player_stats_per_game_playoffs = player_stats_per_game_result_sets[2]['rowSet']
        player_stats_totals_playoffs = player_stats_totals_result_sets[2]['rowSet']
        for per_game_stats, totals_stats in zip(player_stats_per_game_playoffs, player_stats_totals_playoffs):
            per_game_season = per_game_stats[1]
            totals_season = totals_stats[1]

            if per_game_season == totals_season:
                playoffs_stats = {}
                # First, gather common statistics for a given season
                playoffs_stats['season'] = per_game_stats[1]
                playoffs_stats['teamId'] = per_game_stats[3]
                playoffs_stats['teamAbbreviation'] = per_game_stats[4]
                playoffs_stats['age'] = per_game_stats[5]
                playoffs_stats['gp'] = per_game_stats[6]
                playoffs_stats['gs'] = per_game_stats[7]

                playoffs_stats['perGame'] = {}
                playoffs_stats['perGame']['min'] = per_game_stats[8]
                playoffs_stats['perGame']['fgm'] = per_game_stats[9]
                playoffs_stats['perGame']['fga'] = per_game_stats[10]
                playoffs_stats['perGame']['fgPct'] = per_game_stats[11]
                playoffs_stats['perGame']['fg3m'] = per_game_stats[12]
                playoffs_stats['perGame']['fg3a'] = per_game_stats[13]
                playoffs_stats['perGame']['fg3Pct'] = per_game_stats[14]
                playoffs_stats['perGame']['ftm'] = per_game_stats[15]
                playoffs_stats['perGame']['fta'] = per_game_stats[16]
                playoffs_stats['perGame']['ftPct'] = per_game_stats[17]
                playoffs_stats['perGame']['oReb'] = per_game_stats[18]
                playoffs_stats['perGame']['dReb'] = per_game_stats[19]
                playoffs_stats['perGame']['reb'] = per_game_stats[20]
                playoffs_stats['perGame']['ast'] = per_game_stats[21]
                playoffs_stats['perGame']['stl'] = per_game_stats[22]
                playoffs_stats['perGame']['blk'] = per_game_stats[23]
                playoffs_stats['perGame']['tov'] = per_game_stats[24]
                playoffs_stats['perGame']['pf'] = per_game_stats[25]
                playoffs_stats['perGame']['pts'] = per_game_stats[26]

                playoffs_stats['totals'] = {}
                playoffs_stats['totals']['min'] = totals_stats[8]
                playoffs_stats['totals']['fgm'] = totals_stats[9]
                playoffs_stats['totals']['fga'] = totals_stats[10]
                playoffs_stats['totals']['fgPct'] = totals_stats[11]
                playoffs_stats['totals']['fg3m'] = totals_stats[12]
                playoffs_stats['totals']['fg3a'] = totals_stats[13]
                playoffs_stats['totals']['fg3Pct'] = totals_stats[14]
                playoffs_stats['totals']['ftm'] = totals_stats[15]
                playoffs_stats['totals']['fta'] = totals_stats[16]
                playoffs_stats['totals']['ftPct'] = totals_stats[17]
                playoffs_stats['totals']['oReb'] = totals_stats[18]
                playoffs_stats['totals']['dReb'] = totals_stats[19]
                playoffs_stats['totals']['reb'] = totals_stats[20]
                playoffs_stats['totals']['ast'] = totals_stats[21]
                playoffs_stats['totals']['stl'] = totals_stats[22]
                playoffs_stats['totals']['blk'] = totals_stats[23]
                playoffs_stats['totals']['tov'] = totals_stats[24]
                playoffs_stats['totals']['pf'] = totals_stats[25]
                playoffs_stats['totals']['pts'] = totals_stats[26]

                player_document['stats']['playoffs'].append(playoffs_stats)

        # Regular Seasons stats Career
        player_stats_per_game_regular_seasons_career = player_stats_per_game_result_sets[1]['rowSet']
        player_stats_totals_regular_seasons_career = player_stats_totals_result_sets[1]['rowSet']
        for per_game_stats, totals_stats in zip(player_stats_per_game_regular_seasons_career, player_stats_totals_regular_seasons_career):
            reg_season_career_stats = {}
            # First, gather common career statistics
            reg_season_career_stats['gp'] = per_game_stats[3]
            reg_season_career_stats['gs'] = per_game_stats[4]

            reg_season_career_stats['perGame'] = {}
            reg_season_career_stats['perGame']['min'] = per_game_stats[5]
            reg_season_career_stats['perGame']['fgm'] = per_game_stats[6]
            reg_season_career_stats['perGame']['fga'] = per_game_stats[7]
            reg_season_career_stats['perGame']['fgPct'] = per_game_stats[8]
            reg_season_career_stats['perGame']['fg3m'] = per_game_stats[9]
            reg_season_career_stats['perGame']['fg3a'] = per_game_stats[10]
            reg_season_career_stats['perGame']['fg3Pct'] = per_game_stats[11]
            reg_season_career_stats['perGame']['ftm'] = per_game_stats[12]
            reg_season_career_stats['perGame']['fta'] = per_game_stats[13]
            reg_season_career_stats['perGame']['ftPct'] = per_game_stats[14]
            reg_season_career_stats['perGame']['oReb'] = per_game_stats[15]
            reg_season_career_stats['perGame']['dReb'] = per_game_stats[16]
            reg_season_career_stats['perGame']['reb'] = per_game_stats[17]
            reg_season_career_stats['perGame']['ast'] = per_game_stats[18]
            reg_season_career_stats['perGame']['stl'] = per_game_stats[19]
            reg_season_career_stats['perGame']['blk'] = per_game_stats[20]
            reg_season_career_stats['perGame']['tov'] = per_game_stats[21]
            reg_season_career_stats['perGame']['pf'] = per_game_stats[22]
            reg_season_career_stats['perGame']['pts'] = per_game_stats[23]

            reg_season_career_stats['totals'] = {}
            reg_season_career_stats['totals']['min'] = totals_stats[5]
            reg_season_career_stats['totals']['fgm'] = totals_stats[6]
            reg_season_career_stats['totals']['fga'] = totals_stats[7]
            reg_season_career_stats['totals']['fgPct'] = totals_stats[8]
            reg_season_career_stats['totals']['fg3m'] = totals_stats[9]
            reg_season_career_stats['totals']['fg3a'] = totals_stats[10]
            reg_season_career_stats['totals']['fg3Pct'] = totals_stats[11]
            reg_season_career_stats['totals']['ftm'] = totals_stats[12]
            reg_season_career_stats['totals']['fta'] = totals_stats[13]
            reg_season_career_stats['totals']['ftPct'] = totals_stats[14]
            reg_season_career_stats['totals']['oReb'] = totals_stats[15]
            reg_season_career_stats['totals']['dReb'] = totals_stats[16]
            reg_season_career_stats['totals']['reb'] = totals_stats[17]
            reg_season_career_stats['totals']['ast'] = totals_stats[18]
            reg_season_career_stats['totals']['stl'] = totals_stats[19]
            reg_season_career_stats['totals']['blk'] = totals_stats[20]
            reg_season_career_stats['totals']['tov'] = totals_stats[21]
            reg_season_career_stats['totals']['pf'] = totals_stats[22]
            reg_season_career_stats['totals']['pts'] = totals_stats[23]

            player_document['stats']['careerRegularSeasons'] = reg_season_career_stats

        # Post Seasons stats Career
        player_stats_per_game_playoffs_career = player_stats_per_game_result_sets[3]['rowSet']
        player_stats_totals_playoffs_career = player_stats_totals_result_sets[3]['rowSet']
        for per_game_stats, totals_stats in zip(player_stats_per_game_playoffs_career, player_stats_totals_playoffs_career):
            playoffs_career_stats = {}
            # First, gather common career statistics
            playoffs_career_stats['gp'] = per_game_stats[3]
            playoffs_career_stats['gs'] = per_game_stats[4]

            playoffs_career_stats['perGame'] = {}
            playoffs_career_stats['perGame']['min'] = per_game_stats[5]
            playoffs_career_stats['perGame']['fgm'] = per_game_stats[6]
            playoffs_career_stats['perGame']['fga'] = per_game_stats[7]
            playoffs_career_stats['perGame']['fgPct'] = per_game_stats[8]
            playoffs_career_stats['perGame']['fg3m'] = per_game_stats[9]
            playoffs_career_stats['perGame']['fg3a'] = per_game_stats[10]
            playoffs_career_stats['perGame']['fg3Pct'] = per_game_stats[11]
            playoffs_career_stats['perGame']['ftm'] = per_game_stats[12]
            playoffs_career_stats['perGame']['fta'] = per_game_stats[13]
            playoffs_career_stats['perGame']['ftPct'] = per_game_stats[14]
            playoffs_career_stats['perGame']['oReb'] = per_game_stats[15]
            playoffs_career_stats['perGame']['dReb'] = per_game_stats[16]
            playoffs_career_stats['perGame']['reb'] = per_game_stats[17]
            playoffs_career_stats['perGame']['ast'] = per_game_stats[18]
            playoffs_career_stats['perGame']['stl'] = per_game_stats[19]
            playoffs_career_stats['perGame']['blk'] = per_game_stats[20]
            playoffs_career_stats['perGame']['tov'] = per_game_stats[21]
            playoffs_career_stats['perGame']['pf'] = per_game_stats[22]
            playoffs_career_stats['perGame']['pts'] = per_game_stats[23]

            playoffs_career_stats['totals'] = {}
            playoffs_career_stats['totals']['min'] = totals_stats[5]
            playoffs_career_stats['totals']['fgm'] = totals_stats[6]
            playoffs_career_stats['totals']['fga'] = totals_stats[7]
            playoffs_career_stats['totals']['fgPct'] = totals_stats[8]
            playoffs_career_stats['totals']['fg3m'] = totals_stats[9]
            playoffs_career_stats['totals']['fg3a'] = totals_stats[10]
            playoffs_career_stats['totals']['fg3Pct'] = totals_stats[11]
            playoffs_career_stats['totals']['ftm'] = totals_stats[12]
            playoffs_career_stats['totals']['fta'] = totals_stats[13]
            playoffs_career_stats['totals']['ftPct'] = totals_stats[14]
            playoffs_career_stats['totals']['oReb'] = totals_stats[15]
            playoffs_career_stats['totals']['dReb'] = totals_stats[16]
            playoffs_career_stats['totals']['reb'] = totals_stats[17]
            playoffs_career_stats['totals']['ast'] = totals_stats[18]
            playoffs_career_stats['totals']['stl'] = totals_stats[19]
            playoffs_career_stats['totals']['blk'] = totals_stats[20]
            playoffs_career_stats['totals']['tov'] = totals_stats[21]
            playoffs_career_stats['totals']['pf'] = totals_stats[22]
            playoffs_career_stats['totals']['pts'] = totals_stats[23]

            player_document['stats']['careerPlayoffs'] = playoffs_career_stats

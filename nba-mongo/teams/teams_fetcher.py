# -*- coding: utf-8 -*-

import constants
from nba_request import NbaRequest

def fetch_team_info_common(team_id, team_document):
    """Fetch and populate the common info for a given team.

    The common info for a team are retrieved by requesting the 'teaminfocommon' endpoint.
    Only immutable data are kept and correspond to the current season.

    Keyword arguments:
    team_id -- The id of the NBA team to fetch common info for.
    team_document -- The NBA team document to populate.
    """
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

def fetch_team_roster(team_id, team_document):
    """Fetch and populate the current roster for a given team.

    The current roster for a team is retrieved by requesting the 'commonteamroster' endpoint.
    The team roster is composed of two distinct categories: players and coaches.
    Only immutable data for players and coaches are kept.

    Keyword argument:
    team_id -- The id of the NBA team to fetch the roster for.
    team_document -- The NBA team document to populate.
    """
    team_document['players'] = []
    team_document['coaches'] = []

    common_team_roster_params = {
        'TeamID': team_id,
        'Season': constants.CURRENT_SEASON
    }
    common_team_roster_request = NbaRequest(constants.COMMON_TEAM_ROSTER_ENDPOINT, common_team_roster_params)
    common_team_roster_meta = common_team_roster_request.send()

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

def fetch_team_stats(team_id, team_document):
    """Fetch and populate all seasons statistics for a given team.

    The seasons statistics for a team are retrieved by requesting the 'teamyearbyyearstats' endpoint.
    These statistics are composed of two distinct categories: regular season and playoffs.
    Note: the endpoint seems to return the same statistics with 'Playoffs' as SeasonType.
    For each category, two modes of statistics are fetched: per game and totals.

    Keyword argument:
    team_id -- The id of the NBA team to fetch seasons statistics for.
    team_document -- The NBA team document to populate.
    """
    team_document['stats'] = {}

    # Regular season stats
    team_document['stats']['regularSeason'] = []
    # -> Stats Per Game
    team_stats_reg_season_per_game_params = {
        'TeamID': team_id,
        'LeagueID': constants.LEAGUE_ID_NBA,
        'SeasonType': constants.REGULAR_SEASON,
        'PerMode': constants.PER_GAME
    }
    team_stats_reg_season_per_game_request = NbaRequest(constants.TEAM_YEAR_BY_YEAR_STATS_ENDPOINT, team_stats_reg_season_per_game_params)
    team_stats_reg_season_per_game_meta = team_stats_reg_season_per_game_request.send()

    # -> Stats Totals
    team_stats_reg_season_totals_params = {
        'TeamID': team_id,
        'LeagueID': constants.LEAGUE_ID_NBA,
        'SeasonType': constants.REGULAR_SEASON,
        'PerMode': constants.TOTALS
    }
    team_stats_reg_season_totals_request = NbaRequest(constants.TEAM_YEAR_BY_YEAR_STATS_ENDPOINT, team_stats_reg_season_totals_params)
    team_stats_reg_season_totals_meta = team_stats_reg_season_totals_request.send()

    if team_stats_reg_season_per_game_meta and team_stats_reg_season_totals_meta:
        team_stats_reg_season_per_game_row_set = team_stats_reg_season_per_game_meta['resultSets'][0]['rowSet']
        team_stats_reg_season_totals_row_set = team_stats_reg_season_totals_meta['resultSets'][0]['rowSet']

        for per_game_stats, totals_stats in zip(team_stats_reg_season_per_game_row_set, team_stats_reg_season_totals_row_set):
            per_game_year = per_game_stats[3]
            totals_year = totals_stats[3]

            if per_game_year == totals_year:
                year_stat_info = {}
                # First, gather common statistics for a given season
                year_stat_info['year'] = per_game_year
                year_stat_info['gp'] = per_game_stats[4]
                year_stat_info['wins'] = per_game_stats[5]
                year_stat_info['losses'] = per_game_stats[6]
                year_stat_info['winPct'] = per_game_stats[7]
                year_stat_info['confRank'] = per_game_stats[8]
                year_stat_info['divRank'] = per_game_stats[9]
                year_stat_info['ptsRank'] = per_game_stats[33]
                year_stat_info['perGame'] = {}
                year_stat_info['totals'] = {}

                year_stat_info['perGame']['fgm'] = per_game_stats[15]
                year_stat_info['perGame']['fga'] = per_game_stats[16]
                year_stat_info['perGame']['fgPct'] = per_game_stats[17]
                year_stat_info['perGame']['fg3m'] = per_game_stats[18]
                year_stat_info['perGame']['fg3a'] = per_game_stats[19]
                year_stat_info['perGame']['fg3Pct'] = per_game_stats[20]
                year_stat_info['perGame']['ftm'] = per_game_stats[21]
                year_stat_info['perGame']['fta'] = per_game_stats[22]
                year_stat_info['perGame']['ftPct'] = per_game_stats[23]
                year_stat_info['perGame']['oReb'] = per_game_stats[24]
                year_stat_info['perGame']['dReb'] = per_game_stats[25]
                year_stat_info['perGame']['reb'] = per_game_stats[26]
                year_stat_info['perGame']['ast'] = per_game_stats[27]
                year_stat_info['perGame']['pf'] = per_game_stats[28]
                year_stat_info['perGame']['stl'] = per_game_stats[29]
                year_stat_info['perGame']['tov'] = per_game_stats[30]
                year_stat_info['perGame']['blk'] = per_game_stats[31]
                year_stat_info['perGame']['pts'] = per_game_stats[32]

                year_stat_info['totals']['fgm'] = totals_stats[15]
                year_stat_info['totals']['fga'] = totals_stats[16]
                year_stat_info['totals']['fgPct'] = totals_stats[17]
                year_stat_info['totals']['fg3m'] = totals_stats[18]
                year_stat_info['totals']['fg3a'] = totals_stats[19]
                year_stat_info['totals']['fg3Pct'] = totals_stats[20]
                year_stat_info['totals']['ftm'] = totals_stats[21]
                year_stat_info['totals']['fta'] = totals_stats[22]
                year_stat_info['totals']['ftPct'] = totals_stats[23]
                year_stat_info['totals']['oReb'] = totals_stats[24]
                year_stat_info['totals']['dReb'] = totals_stats[25]
                year_stat_info['totals']['reb'] = totals_stats[26]
                year_stat_info['totals']['ast'] = totals_stats[27]
                year_stat_info['totals']['pf'] = totals_stats[28]
                year_stat_info['totals']['stl'] = totals_stats[29]
                year_stat_info['totals']['tov'] = totals_stats[30]
                year_stat_info['totals']['blk'] = totals_stats[31]
                year_stat_info['totals']['pts'] = totals_stats[32]

                team_document['stats']['regularSeason'].append(year_stat_info)
            else:
                print("Failed to fetch team stats for {0} ... Years are different: {1} vs {2}".format(team_id, per_game_year, totals_year))

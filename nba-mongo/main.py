# -*- coding: utf-8 -*-

import configparser

from nba_db_client import NbaDBClient

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('database.cfg')

    host = config['database']['host']
    port = int(config['database']['port'])
    db_name = config['database']['db_name']
    teams_collection = config['database']['teams_collection']
    players_collection = config['database']['players_collection']

    client = NbaDBClient(host,
                         port,
                         db_name,
                         teams_collection,
                         players_collection)

    client.generate_teams_collection()
    client.generate_players_collection()

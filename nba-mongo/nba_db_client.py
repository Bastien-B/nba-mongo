# -*- coding: utf-8 -*-

from pymongo import MongoClient

from teams import teams_builder
from players import players_builder

class NbaDBClient:

    def __init__(self,
                 host='localhost',
                 port=27017,
                 db_name='nba_database',
                 teams_collection='teams',
                 players_collection='players'):
        self._mongo_client = MongoClient(host, port)
        self._db = self._mongo_client[db_name]
        self._teams_collection = self._db[teams_collection]
        self._players_collection = self._db[players_collection]

    def generate_teams_collection(self):
        print('Creating teams collection...')
        teams_documents = teams_builder.build_all_teams_documents()
        result = self._teams_collection.insert_many(teams_documents)

        print("Inserted successfully {0} teams.".format(len(result.inserted_ids)))

    def generate_players_collection(self):
        print('Creating players collection...')
        players_ids = players_builder.build_players_ids()
        for player_id in players_ids:
            player_document = players_builder.build_player_document(player_id)
            result = self._players_collection.insert_one(player_document)

        print("Inserted successfully {0} players.".format(len(players_ids)))

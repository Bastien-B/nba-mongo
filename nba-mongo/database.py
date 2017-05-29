# -*- coding: utf-8 -*-

from teams import teams_builder
from players import players_builder

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.nba_database
teams_collection = db.teams
players_collection = db.players


def generate_teams_collection():
    teams_documents = teams_builder.build_all_teams_documents()
    result = teams_collection.insert_many(teams_documents)

    print("Inserted successfully {0} teams.".format(len(result.inserted_ids)))


def generate_players_collection():
    players_documents = players_builder.build_all_players_documents()
    result = players_collection.insert_many(players_documents)

    print("Inserted successfully {0} players.".format(len(result.inserted_ids)))

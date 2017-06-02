# nba-mongo

A python project that creates MongoDB collections of NBA statistics and data fetched from [stats.nba.com](http://stats.nba.com)

The collections are designed to make advanced queries on teams or players as simple as possible.

## Table of Contents
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installing](#installing)
    - [Configuring](#configuring)
    - [Running](#running)
- [Running the tests](#running-the-tests)
- [Authors](#authors)
- [License](#license)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To install and use the project, you will need the following things:
* [python3](https://www.python.org/downloads/)
* [pip](https://pypi.python.org/pypi/pip?)
* [virtualenv](https://virtualenv.pypa.io/en/stable/)
* [mongodb](https://www.mongodb.com/)

### Installing

Start by cloning the repository
```
git clone https://github.com/Bastien-B/nba-mongo.git
```

Create a python virtualenv in the repository
```
cd nba-mongo/
virtualenv venv

```

Activate your virtual environment and install the python packages dependencies
```
source venv/bin/activate
pip install -r requirements.txt
```

And this is it !

### Configuring

Before generating the collections, you should edit the configuration file of your database: **_database.cfg_**

This file provides information such as:
* host : *the location of the MongoDB instance*
* port : *the TCP port on which the MongoDB instance listens for client connections*
* db_name : *the name of the database that will be created*
* teams_collection : *the name of the teams collection that will be created*
* players_collection : *the name of the players collection that will be created*

### Running

First, you have to make sure that a MongoDB instance is up and running at the *location:port* that you provided in the **_database.cfg_** file.

For instance, on your local machine (by default *localhost:27017*)
```
mongod --dbpath /path/to/your/databases
```

Now, simply run the main script of the project
```
python main.py
```

The process takes about 20 mins, and once it is done, a new MongoDB database should be created, containing two collections:
* teams
* players

![nba-mongo run success](https://cloud.githubusercontent.com/assets/1844237/26744303/a918a1e0-47e5-11e7-916c-b40fa520924e.png)

Success !

Here are some snapshots of the created collections, as seen on [RoboMongo](https://robomongo.org/) :

![nba-mongo teams collection](https://cloud.githubusercontent.com/assets/1844237/26744319/b09eb7a6-47e5-11e7-9c5b-f956a804a8e6.png)

![nba-mongo players collection](https://cloud.githubusercontent.com/assets/1844237/26744321/b30b0468-47e5-11e7-8f58-865b5e11fe9d.png)

## Running the tests

The project comes with several unit tests located in the *nba-mongo/tests/* folder. The tests are compatible with python test discovery.

To run them all, go to the project folder and call discover from command line
```
cd nba-mongo/
python -m unittest discover
```

## Authors

* **Bastien Bessiere** - *Initial work* - [Bastien-B](https://github.com/Bastien-B/)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Bastien-B/nba-mongo/blob/master/LICENSE) file for details.

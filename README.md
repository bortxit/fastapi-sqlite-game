# Rock-Paper-Scissors Game API

## Description
This project is a Rock, Paper, Scissors game API built using FastAPI, SQLAlchemy, SQLite and Docker. It allows players (humans or machines) to play multi-round games, record results, and access global game statistics. 
The API includes features to calculate the strongest and weakest hands for human players, players' ranking, and unit tests using pytest, doctest, between others.

## Features
- Create and record new games with multiple rounds.
- Record moves and determine the winner of each round.
- Calculate global game statistics, wins, losses, and win percentages.
- Determine the strongest and weakest hands for a player.
- Get a ranking of players based on the number of victories.
- Automated testing using pytest.
- Docker support for easy deployment.

## Table of Contents

## Installation
1. Clone the repository
  ```bash
  git clone https://github.com/bortxit/fastapi-sqlite-game.git
  ```

2. Create and activate a virtual environment
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

3. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Running the application
### Option 1: Run Locally
1. Start the API in a command line.
```bash
uvicorn rock_paper_scissors.api.init_app:app --reload
```
This will start the server at http://127.0.0.1:8000/.

2.Start application console in another command line
```bash
python main.py # basic game
```
```bash
python main.py mvm 1 # special game machine vs machine: first_parameter = game mode, second_parameter = number of games to play
```

3. Access API documentation with Swagger
```bash
http://127.0.0.1:8000/docs
```




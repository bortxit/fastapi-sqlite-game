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
### Option 1: Run App Locally
### 1. Start the API in a command line.
```bash
uvicorn rock_paper_scissors.api.init_app:app --reload
```
This will start the server at http://127.0.0.1:8000/.

### 2. Start application console in another command line
```bash
python main.py # basic game
```
```bash
python main.py mvm 1 # special game machine vs machine: first_parameter = game mode, second_parameter = number of games to play
```

### 3. Access API documentation with Swagger
```bash
http://127.0.0.1:8000/docs
```

### Option 2: Run App with Docker
If you'd like to use Docker, you can run the application without configuring the environment locally.

Prerequisites
- Install Docker Desktop.
- Configure docker-compose with docker-compose.yml and Dockerfile.

### 1. Start the services using Docker Compose.
```bash
#Docker Compose will use Dockerfile to create a image of web service, installing Python dependencies and preparing the environment to execute the application.
docker-compose build
```

### 2. Start the API.
```bash
docker-compose up -d uvicorn
```

### 3. Run different services.
### Simple game Human vs Machine
```bash
docker-compose run --rm game
```

### Special game mode machine vs machine
```bash
docker-compose run --rm special_game
```

### Tests for the application
```bash
docker-compose run --rm pytest
```

### Doctest
```bash
docker-compose run --rm doctest
```

### 4. Other commands in Docker
### Stop Services in Docker
```bash
docker-compose down
```

### Show container being executed
```bash
docker-compose ps
```

## Usage
### Available Endpoints
| Method |      Endpoint          | Description                                                                                                                          |
|--------|------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
|  POST  | /game                  | Create a new game                                                                                                                    |
|  GET   | /game/get_global_info  | Get global information about total victories, total losses, number of games played, % winrate                                        |
|  GET   | /game/mano_fuerte      | Choose the hand that has achieved the most victories in the games, along with the corresponding win percentage for playing this hand.|
|  GET   | /game/mano_debil       | Choose the hand that has achieved the most losses in the games, along with the corresponding loss percentage for playing this hand.  |
|  GET   | /game/ranking          | Get the three best players with most points.                                                                                         |
|  GET   | /games/estadisticas    | Gather information on the total number of games played, the number of games won, and the number of games lost due to abandonment.    |

### Response Format
- POST /game: Create game
  ```bash
  {
    "id": 1,
    "rounds_played": [
      {
        "player_1_move": "rock",
        "player_2_move": "scissors",
        "winner": "Human"
      }
    ],
    "game_winner": "Human"
  }
  ```
- GET /game/get_global_info: Get global statistics
  ```bash
  {
    "total_games": 100,
    "total_wins": 55,
    "total_losses": 45,
    "winrate_percentage": 55.0
  }
  ```
- GET /game/mano_fuerte: Get strong hand
  ```bash
  {
    "strong_hand": "rock",
    "win_percentage": 60.0
  }
  ```
- GET /game/mano_debil: Get weak hand
  ```bash
  {
    "weak_hand": "rock",
    "loss_percentage": 50.0
  }
  ```




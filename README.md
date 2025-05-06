# 🧪 Practical Exercise: Redis with Actors and Movies Dataset

## 🗂️ Overview
This project demonstrates loading and interacting with a Redis database populated with actors and movies data. It involves using Docker Compose to set up Redis and RedisInsight, loading data via Redis CLI, and performing data exploration and manipulation tasks using Python, both in a Jupyter Notebook and via a standalone script.

## 🛠️ Objective
- Load actors and movies data into Redis using Docker.
- Interact with Redis using Python (Jupyter Notebook and a standalone script).
- Write queries to analyze and modify the data.

## 📋 Prerequisites
- [Docker](https://www.docker.com/get-started) and Docker Compose installed.
- Python 3.x installed on the host machine (if you intend to run `redis_interaction.py` locally).
  - The `redis` Python package (`pip install redis`).
- The dataset files `actors.redis` and `movies.redis` placed in the `data/` directory.

## 🚀 Setup

### 1. Clone the Repository
Ensure you have all project files, including `docker-compose.yml`, the `data/` folder with datasets, the `notebooks/` folder (containing `redis_exploration.ipynb`), and `redis_interaction.py`.

### 2. Start Services
Navigate to the project's root directory in your terminal and run:
```bash
docker-compose up -d
```

This will start:
- A Redis server on port 6379.
- RedisInsight on port 5540.
- A Jupyter Notebook server on port 8888.

## 📥 Load the Data

Once the containers are running, open a new terminal in the project's root directory and execute the following commands to load the data into Redis.

If using bash or cmd.exe:
```bash
docker exec -i redis-server redis-cli < data/actors.redis
docker exec -i redis-server redis-cli < data/movies.redis
```

If using PowerShell:
```powershell
Get-Content .\data\actors.redis | docker exec -i redis-server redis-cli
Get-Content .\data\movies.redis | docker exec -i redis-server redis-cli
```

## 🔬 Usage

### RedisInsight
- Access RedisInsight in your browser at http://localhost:5540.
- Connect to the Redis database:
  - Host: redis
  - Port: 6379
  - Name: (e.g., MyRedisDB)

### Jupyter Notebook for Data Exploration (Part 1)
- Access JupyterLab/Notebook in your browser at http://localhost:8888.
- If prompted for a token, get it from the jupyter-notebook container logs: `docker logs jupyter-notebook`
- Navigate into the work directory (which maps to your local notebooks/ folder).
- Open the `redis_exploration.ipynb` notebook.
- Run the cells in the notebook to perform the data exploration tasks from Part 1.

### Python Script for Interaction (Part 2)
The `redis_interaction.py` script performs the tasks outlined in Part 2 of the exercise:
- Connects to Redis.
- Counts actors with last names starting with "P".
- Gets movies released after 2010 with >100,000 votes.
- Creates top_movies_by_genre:<genre> hashes.

To run the script from your host machine (ensure Python and redis package are installed, and you are in the project root directory):
```bash
python redis_interaction.py
```

The script will print its results to the console and create new keys in Redis.

## 📄 Results PDF
A PDF document (e.g., `Part1_Results.pdf`) is included in the repository. This PDF contains the questions and outputs from the Jupyter Notebook data exploration (Part 1).

## 🧼 Cleanup
To stop and remove all containers, networks, and potentially volumes:
```bash
docker-compose down
```

If you also want to remove named volumes that might have been defined and used (the redis_data volume in docker-compose.yml is defined but not directly mapped to persist Redis data in the current setup):
```bash
docker-compose down -v
```

Auteur: Batah/Dioxeur
Date: 06/05/2025
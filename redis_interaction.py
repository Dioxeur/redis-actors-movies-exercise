import redis

def main():
    # 1. Connects to Redis
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping() 
        print("Successfully connected to Redis!")
    except redis.exceptions.ConnectionError as e:
        print(f"Could not connect to Redis: {e}")
        return 

    # 2. Loads all actor hashes and counts how many actors have a last name starting with “P”.
    actor_keys = r.keys("actor:*")
    count_lastname_p = 0
    for key in actor_keys:
        last_name = r.hget(key, "last_name")
        if last_name and last_name.startswith("P"):
            count_lastname_p += 1
    print(f"Number of actors with last name starting with 'P': {count_lastname_p}")

    # 3. Gets all movies released after 2010 with more than 100,000 votes.
    movie_keys_for_task3 = r.keys("movie:*") # Renamed to avoid conflict with movie_keys below
    qualifying_movies = []
    for key in movie_keys_for_task3:
        movie_data = r.hgetall(key)
        release_year_str = movie_data.get("release_year")
        votes_str = movie_data.get("votes")
        if release_year_str and votes_str:
            try:
                release_year = int(release_year_str)
                votes = int(votes_str)
                if release_year > 2010 and votes > 100000:
                    qualifying_movies.append({
                        "title": movie_data.get("title", "N/A"),
                        "release_year": release_year,
                        "votes": votes
                    })
            except ValueError:
                print(f"Warning: Could not parse year/votes for movie key {key} in task 3")
    print(f"\nMovies released after 2010 with more than 100,000 votes ({len(qualifying_movies)}):")
    if qualifying_movies:
        for movie in qualifying_movies[:5]: 
            print(f"- Title: {movie['title']}, Year: {movie['release_year']}, Votes: {movie['votes']}")
        if len(qualifying_movies) > 5:
            print("... and more.")
    else:
        print("No movies found matching the criteria for task 3.")

    # 4. Creates a new hash: `top_movies_by_genre:<genre>` with the highest-rated movie per genre.
    print("\nProcessing top movies by genre...")
    movie_keys_for_task4 = r.keys("movie:*") 
    top_movies_by_genre = {} 

    for key in movie_keys_for_task4:
        movie_data = r.hgetall(key)
        title = movie_data.get("title")
        genre = movie_data.get("genre")
        rating_str = movie_data.get("rating")

        if title and genre and rating_str:
            try:
                rating = float(rating_str)
                if genre not in top_movies_by_genre or rating > top_movies_by_genre[genre]['rating']:
                    top_movies_by_genre[genre] = {
                        'title': title,
                        'rating': rating,
                        'original_key': key 
                    }
            except ValueError:
                print(f"Warning: Could not parse rating for movie key {key} in task 4")
    

    num_genre_hashes_created = 0
    for genre, movie_info in top_movies_by_genre.items():
        safe_genre_name = genre.replace(" ", "_").lower() 
        redis_key_for_genre = f"top_movies_by_genre:{safe_genre_name}"
        

        genre_top_movie_data = {
            "title": movie_info['title'],
            "rating": str(movie_info['rating'])
            
        }
        
        r.hmset(redis_key_for_genre, genre_top_movie_data) 
        num_genre_hashes_created += 1
        

    print(f"Created {num_genre_hashes_created} new hashes for top movies by genre (e.g., top_movies_by_genre:action).")
    print("You can verify these new keys in RedisInsight (e.g., search for 'top_movies_by_genre:*').")


if __name__ == "__main__":
    main()
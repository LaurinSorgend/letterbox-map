import csv
import json
from tmdbv3api import TMDb, Movie
import os

tmdb = TMDb()
tmdb.api_key = "YOUR_TMDB_API_KEY"


movie_api = Movie()


def get_origin_country(movie_name, movie_year):
    search_results = movie_api.search(movie_name)
    for result in search_results:
        if "release_date" in result and result["release_date"].startswith(
            str(movie_year)
        ):
            movie_details = movie_api.details(result["id"])
            if "production_countries" in movie_details:
                countries = [
                    country["name"] for country in movie_details["production_countries"]
                ]
                return countries
    return []


if os.path.exists("movies.json"):
    with open("movies.json", "r", encoding="utf-8") as json_file:
        existing_movies = json.load(json_file)
else:
    existing_movies = []
existing_movie_set = {(movie["name"], movie["year"]) for movie in existing_movies}

movies = list()

with open("ratings.csv", mode="r", encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        movie_name = row["Name"]
        movie_year = int(row["Year"])
        if (movie_name, movie_year) not in existing_movie_set:
            movie = {
                "date": row["Date"],
                "name": movie_name,
                "year": movie_year,
                "letterboxd_uri": row["Letterboxd URI"],
                "rating": float(row["Rating"]),
                "origin_country": get_origin_country(movie_name, movie_year),
            }
            movies.append(movie)
existing_movies.extend(movies)

with open("movies.json", "w", encoding="utf-8") as json_file:
    json.dump(existing_movies, json_file, ensure_ascii=False, indent=4)

print("Movies with origin countries have been saved to 'movies.json'.")

import csv
import json
from tmdbv3api import TMDb, Movie


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


movies = []
with open("ratings.csv", mode="r", encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        movie = {
            "date": row["Date"],
            "name": row["Name"],
            "year": int(row["Year"]),
            "letterboxd_uri": row["Letterboxd URI"],
            "rating": float(row["Rating"]),
        }
        movie["origin_country"] = get_origin_country(movie["name"], movie["year"])
        movies.append(movie)


with open("movies_with_countries.json", "w", encoding="utf-8") as json_file:
    json.dump(movies, json_file, ensure_ascii=False, indent=4)

print("Movies with origin countries have been saved to 'movies_with_countries.json'.")

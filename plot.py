import json
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Load the movie data from the JSON file
with open('movies_with_countries.json', 'r', encoding='utf-8') as json_file:
    movies = json.load(json_file)

# Flatten the data to create a DataFrame
data = []
for movie in movies:
    for country in movie['origin_country']:
        data.append({
            'country': country,
            'rating': movie['rating']
        })

df = pd.DataFrame(data)

# Calculate the average rating and movie count per country
avg_rating = df.groupby('country')['rating'].mean().reset_index()
movie_count = df.groupby('country')['rating'].size().reset_index(name='count')

# Load the world map shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge the world map with the average rating data
world_avg_rating = world.merge(avg_rating, how='left', left_on='name', right_on='country')
world_movie_count = world.merge(movie_count, how='left', left_on='name', right_on='country')

# Plot the average rating per country
fig, ax = plt.subplots(1, 2, figsize=(20, 10))

world_avg_rating.plot(column='rating', ax=ax[0], legend=True,
                      legend_kwds={'label': "Average Rating by Country",
                                   'orientation': "horizontal"},
                      missing_kwds={'color': 'lightgrey'})
ax[0].set_title('Average Rating by Country')
ax[0].set_axis_off()

# Plot the movie count per country
world_movie_count.plot(column='count', ax=ax[1], legend=True,
                       legend_kwds={'label': "Movie Count by Country",
                                    'orientation': "horizontal"},
                       missing_kwds={'color': 'lightgrey'})
ax[1].set_title('Movie Count by Country')
ax[1].set_axis_off()

# Save the plots as SVG files
fig.savefig('average_rating_by_country.svg', format='svg')
fig.savefig('movie_count_by_country.svg', format='svg')

# Show the plots
plt.tight_layout()
plt.show()
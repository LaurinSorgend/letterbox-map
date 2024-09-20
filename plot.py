import json
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

with open('movies_with_countries.json', 'r', encoding='utf-8') as json_file:
    movies = json.load(json_file)

data = []
for movie in movies:
    for country in movie['origin_country']:
        data.append({
            'country': country,
            'rating': movie['rating']
        })

df = pd.DataFrame(data)

avg_rating = df.groupby('country')['rating'].mean().reset_index()
movie_count = df.groupby('country')['rating'].size().reset_index(name='count')

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

world_avg_rating = world.merge(avg_rating, how='left', left_on='name', right_on='country')
world_movie_count = world.merge(movie_count, how='left', left_on='name', right_on='country')


fig, ax = plt.subplots(1, 2, figsize=(20, 10))

world_avg_rating.plot(column='rating', ax=ax[0], legend=True,
                      legend_kwds={'label': "Average Rating by Country",
                                   'orientation': "horizontal"},
                      missing_kwds={'color': 'lightgrey'})
ax[0].set_title('Average Rating by Country')
ax[0].set_axis_off()

world_movie_count.plot(column='count', ax=ax[1], legend=True,
                       legend_kwds={'label': "Movie Count by Country",
                                    'orientation': "horizontal"},
                       missing_kwds={'color': 'lightgrey'})
ax[1].set_title('Movie Count by Country')
ax[1].set_axis_off()

fig.savefig('plot.svg', format='svg')

plt.tight_layout()
plt.show()

import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

with open("movies.json", "r", encoding="utf-8") as json_file:
    movies = json.load(json_file)

data = []
for movie in movies:
    for country in movie["origin_country"]:
        data.append(
            {
                "country": country,
                "rating": movie["rating"],
                "name": movie["name"],
                "year": movie["year"],
                "letterboxd_uri": movie["letterboxd_uri"],
            }
        )

df = pd.DataFrame(data)

avg_rating = df.groupby("country")["rating"].mean().reset_index()
movie_count = df.groupby("country")["rating"].size().reset_index(name="count")
movies_by_country = (
    df.groupby("country")
    .apply(lambda x: x.to_dict(orient="records"))
    .reset_index(name="movies")
)

movies_by_country["hover_text"] = movies_by_country["movies"].apply(
    lambda x: "<br>".join(
        [f"{m['name']} ({m['year']}) - Rating: {m['rating']}" for m in x[:10]]
    )
    + ("<br>...and more" if len(x) > 10 else "")
    if isinstance(x, list)
    else "No Data"
)

movies_by_country["links"] = movies_by_country["movies"].apply(
    lambda x: "<br>".join(
        [
            f"<a href='{m['letterboxd_uri']}' target='_blank'>{m['name']} ({m['year']})</a>"
            for m in x
        ]
    )
    if isinstance(x, list)
    else "No Data"
)

world_movies = pd.merge(
    movie_count,
    movies_by_country[["country", "hover_text", "links"]],
    on="country",
    how="left",
)
world_movies = pd.merge(world_movies, avg_rating, on="country", how="left")

fig = go.Figure()

fig.add_trace(
    go.Choropleth(
        locations=world_movies["country"],
        locationmode="country names",
        z=world_movies["count"],
        colorscale="Viridis",
        colorbar_title="Movie Count",
        text=world_movies["hover_text"],
        hoverinfo="location+text",
        visible=True,
    )
)

fig.add_trace(
    go.Choropleth(
        locations=world_movies["country"],
        locationmode="country names",
        z=world_movies["rating"],
        colorscale="Viridis",
        colorbar_title="Average Rating",
        text=world_movies["hover_text"],
        hoverinfo="location+text",
        visible=False,
    )
)

fig.update_geos(
    showcountries=True,
    countrycolor="Black",
    showcoastlines=True,
    coastlinecolor="Black",
    showland=True,
    landcolor="lightgrey",
)

fig.update_layout(
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    updatemenus=[
        dict(
            buttons=list(
                [
                    dict(
                        args=[{"visible": [True, False]}],
                        label="Movie Count",
                        method="update",
                    ),
                    dict(
                        args=[{"visible": [False, True]}],
                        label="Average Rating",
                        method="update",
                    ),
                ]
            ),
            direction="down",
            showactive=True,
            x=0.17,
            xanchor="left",
            y=1.15,
            yanchor="top",
        ),
    ],
)

fig.write_html("interactive_map.html")

fig.show()

with open("movie_links.html", "w", encoding="utf-8") as f:
    for index, row in world_movies.iterrows():
        f.write(f"<h2>{row['country']}</h2>")
        f.write(row["links"])
        f.write("<br><br>")

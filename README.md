# letterboxd-map plot
![Example Plot](https://github.com/LaurinSorgend/letterbox-map/blob/main/plot.svg)
## Guide
## Prequisites
- [Python 3.X](https://www.python.org/downloads/)(I use 3.12).
- [geopandas](https://geopandas.org/en/stable/getting_started/install.html)
- [matplotlib](https://matplotlib.org/stable/install/index.html)
- [pandas](https://pandas.pydata.org/docs/getting_started/install.html)
- tmdbv3api `pip install tmdbv3api`
- You will have to create a TMDB Account and register for a [API Key](https://www.themoviedb.org/settings/api) (Because letterboxd doesn't have an open API so I need to get the origin country data from TMDB).

### Usage
1. Clone the repository.
2. Replace `'YOUR_TMDB_API_KEY'` in `main.py` with your tmdb api key.
3. Export your data from [letterbox](https://letterboxd.com/settings/data/).
4. Use 7-Zip to unpack the Zip.
5. Copy the `ratings.csv` to Folder of the cloned repositry.
6. First run `main.py`.
7. Then run `plot.py`.

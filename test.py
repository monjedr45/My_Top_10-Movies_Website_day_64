import requests

url = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkNDg2NjQ5NDY5NjQ4NWE4NTNjN2M5YTM5ZTk4ZmE3ZiIsInN1YiI6IjY1ZjM1MTk5MDZmOTg0MDE4NTQ3NjY4NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.an13mjeEfjP_z6vzp64ZZD4930eLz046dD-ELPfNEjE",
}
params = {
    "query": "parasite",
}
response = requests.get(url, headers=headers, params=params)
i=-1
for _ in range(0, len(response.json()["results"])):
    i+=1
    title = response.json()['results'][i]["original_title"]
    overview = response.json()['results'][i]["overview"]
    poster_img = response.json()['results'][i]["poster_path"]
    release_date = response.json()['results'][i]["release_date"]
    print(f"{title} {overview} https://image.tmdb.org/t/p/w600_and_h900_bestv2/{poster_img} {release_date}")


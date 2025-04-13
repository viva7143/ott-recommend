import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
app = Flask(__name__)
CORS(app)
load_dotenv()

TMDB_API_KEY =  os.getenv("TMDB_API")
UTELLY_API_KEY = os.getenv("UTELLY_API")

UTELLY_HEADERS = {
    "X-RapidAPI-Key": UTELLY_API_KEY,
    "X-RapidAPI-Host": "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com"
}
WATCH_PROVIDER_IDS = {
    "Netflix": 8,
    "Amazon Prime Video": 119,
    "Crunchyroll": 283,
    "aha" : 532,
    "Zee5": 232,
}


# def fetch_top_series():
#     """Fetch trending series from TMDB API."""
#     url = f"https://api.themoviedb.org/3/trending/tv/week?api_key={TMDB_API_KEY}"
#     response = requests.get(url)

#     if response.status_code != 200:
#         return []

#     data = response.json()
#     series_list = data.get("results", [])
    
#     top_series = []
    
#     for series in series_list[:5]:
#         title = series["name"]
#         rating = series.get("vote_average", "N/A")
#         poster = f"https://image.tmdb.org/t/p/w200{series.get('poster_path', '')}"
#         description = series.get("overview", "No description available.")
#         platform = fetch_streaming_platform(title)
        
#         top_series.append({
#             "title": title,
#             "rating": rating,
#             "platform": platform,
#             "poster": poster,
#             "description": description
#         })
    
#     return top_series

def fetch_streaming_platform(series_name):
    """Fetch the streaming platform for a given series from Utelly API."""
    url = f"https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup?term={series_name}"
    response = requests.get(url, headers=UTELLY_HEADERS)
    
    if response.status_code != 200:
        return "Unknown"

    data = response.json()
    locations = data.get("results", [])
    
    if locations and "locations" in locations[0]:
        return ", ".join([loc["display_name"] for loc in locations[0]["locations"]])
    
    return "Not Found"

def fetch_recommendations(ott_platform):
    """Fetch popular movies/series from a specific platform."""
    url = f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&with_watch_providers={ott_platform}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return []

    data = response.json()
    series_list = data.get("results", [])[:5]
    
    recommendations = []
    for series in series_list:
        title = series["name"]
        rating = series.get("vote_average", "N/A")
        poster = f"https://image.tmdb.org/t/p/w200{series.get('poster_path', '')}"
        description = series.get("overview", "No description available.")
        
        recommendations.append({
            "title": title,
            "rating": rating,
            "poster": poster,
            "description": description
        })
    
    return recommendations

# @app.route('/top-series', methods=['GET'])
# def get_top_series():
#     series_data = fetch_top_series()
#     return jsonify({"top_series": series_data})

@app.route('/recommend', methods=['GET'])
def get_recommendations():
    platform = request.args.get("platform", "")

    # Get provider ID
    provider_id = WATCH_PROVIDER_IDS.get(platform)
    if not provider_id:
        return jsonify({"error": "Invalid OTT platform"}), 400

    # Fetch top series/movies from TMDB using provider ID
    url = f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&watch_region=IN&with_watch_providers={provider_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), 500

    data = response.json()
    series_list = data.get("results", [])[:5]

    recommendations = []
    for series in series_list:
        recommendations.append({
            "title": series["name"],
            "rating": series.get("vote_average", "N/A"),
            "poster": f"https://image.tmdb.org/t/p/w200{series.get('poster_path', '')}",
            "description": series.get("overview", "No description available.")
        })

    return jsonify({"recommendations": recommendations})


if __name__ == '__main__':
    app.run(port=5000, debug=True)

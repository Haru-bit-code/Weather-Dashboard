from flask import Flask, render_template, request, jsonify
import requests, os, time

app = Flask(__name__)

# ── Config ────────────────────────────────────────────────────
API_KEY  = os.environ.get("WEATHER_API_KEY", "your_api_key_here")
BASE_URL = "https://api.openweathermap.org/data/2.5"

# ── Simple in-memory cache ────────────────────────────────────
# Stores {city: {data, timestamp}} — avoids hitting API repeatedly
cache = {}
CACHE_DURATION = 600   # 10 minutes in seconds

def get_cached(key):
    if key in cache:
        if time.time() - cache[key]["ts"] < CACHE_DURATION:
            return cache[key]["data"]
    return None

def set_cache(key, data):
    cache[key] = {"data": data, "ts": time.time()}

# ── Routes ────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/weather")
def get_weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "City name is required"}), 400

    cache_key = f"weather_{city.lower()}"
    cached    = get_cached(cache_key)
    if cached:
        cached["from_cache"] = True
        return jsonify(cached)

    try:
        res = requests.get(
            f"{BASE_URL}/weather",
            params={
                "q":     city,
                "appid": API_KEY,
                "units": "metric"
            },
            timeout=5
        )

        if res.status_code == 404:
            return jsonify({"error": "City not found"}), 404
        if res.status_code == 401:
            return jsonify({"error": "Invalid API key"}), 401
        if res.status_code != 200:
            return jsonify({"error": "Weather service unavailable"}), 503

        raw  = res.json()
        data = {
            "city":        raw["name"],
            "country":     raw["sys"]["country"],
            "temp":        round(raw["main"]["temp"]),
            "feels_like":  round(raw["main"]["feels_like"]),
            "temp_min":    round(raw["main"]["temp_min"]),
            "temp_max":    round(raw["main"]["temp_max"]),
            "humidity":    raw["main"]["humidity"],
            "pressure":    raw["main"]["pressure"],
            "description": raw["weather"][0]["description"].title(),
            "icon":        raw["weather"][0]["icon"],
            "wind_speed":  round(raw["wind"]["speed"] * 3.6),  # m/s → km/h
            "wind_deg":    raw["wind"].get("deg", 0),
            "visibility":  raw.get("visibility", 0) // 1000,   # m → km
            "clouds":      raw["clouds"]["all"],
            "sunrise":     raw["sys"]["sunrise"],
            "sunset":      raw["sys"]["sunset"],
            "timezone":    raw["timezone"],
            "from_cache":  False
        }

        set_cache(cache_key, data)
        return jsonify(data)

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out. Try again."}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot reach weather service"}), 503

@app.route("/api/forecast")
def get_forecast():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "City name is required"}), 400

    cache_key = f"forecast_{city.lower()}"
    cached    = get_cached(cache_key)
    if cached:
        return jsonify(cached)

    try:
        res = requests.get(
            f"{BASE_URL}/forecast",
            params={
                "q":     city,
                "appid": API_KEY,
                "units": "metric",
                "cnt":   40    # 5 days × 8 readings per day
            },
            timeout=5
        )

        if res.status_code != 200:
            return jsonify({"error": "Forecast unavailable"}), 503

        raw  = res.json()

        # Group by day — pick one reading per day (noon time)
        days = {}
        for item in raw["list"]:
            date = item["dt_txt"].split(" ")[0]
            hour = item["dt_txt"].split(" ")[1]
            if date not in days or hour == "12:00:00":
                days[date] = {
                    "date":        date,
                    "temp_max":    round(item["main"]["temp_max"]),
                    "temp_min":    round(item["main"]["temp_min"]),
                    "description": item["weather"][0]["description"].title(),
                    "icon":        item["weather"][0]["icon"],
                    "humidity":    item["main"]["humidity"],
                    "wind_speed":  round(item["wind"]["speed"] * 3.6)
                }

        forecast = list(days.values())[:5]
        result   = {"forecast": forecast}
        set_cache(cache_key, result)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/popular")
def popular_cities():
    cities = [
        "London","New York","Tokyo","Dubai","Paris",
        "Mumbai","Sydney","Singapore","Berlin","Toronto"
    ]
    return jsonify({"cities": cities})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
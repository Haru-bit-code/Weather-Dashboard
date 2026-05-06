# 🌤️ Weather Dashboard

Real-time weather dashboard with smart caching.
Search any city and get current conditions plus a 5-day forecast instantly.

## 🌐 Live Demo
**[Try it here →](your-render-link)**

---

## ✨ Features

- **Real-time weather** for any city in the world
- **5-day forecast** with daily high/low temperatures
- **Smart caching** — 1 API call serves 100 users for 10 minutes
- **Dynamic background** — changes based on weather condition
- **Full weather stats** — humidity, wind, visibility, pressure, cloud cover
- **Sunrise & sunset** times adjusted to the city's timezone
- **Error handling** — timeouts, invalid cities, API failures
- **Responsive** — works on mobile and desktop

---

## ⚡ How Caching Works

- User 1 searches London → API call → result stored in cache
- User 2 searches London → cache hit → instant (no API call)
- User 3 searches London → cache hit → instant (no API call)
  ...10 minutes later...
- User 100 searches London → cache expired → fresh API call

Same concept as Redis — just in-memory for this scale.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/weather?city=London` | Current weather (cached 10 min) |
| `GET` | `/api/forecast?city=London` | 5-day forecast (cached 10 min) |
| `GET` | `/api/popular` | List of popular cities |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Weather Data | OpenWeatherMap API |
| Caching | In-memory Python dict |
| Frontend | Vanilla HTML, CSS, JavaScript |
| Hosting | Render (free tier) |

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/weather-dashboard
cd weather-dashboard

# 2. Get a free API key at openweathermap.org

# 3. Open app.py and replace "your_api_key_here"
#    with your actual key

# 4. Install and run
pip install -r requirements.txt
python app.py

# 5. Visit http://localhost:10000
```

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `WEATHER_API_KEY` | Your OpenWeatherMap API key |

On Render: Dashboard → Environment → Add Variable

---

## 📁 Project Structure


weather-dashboard/
├── app.py           # Flask backend + caching logic
├── requirements.txt # Dependencies
├── README.md
└── templates/
└── index.html   # Full responsive frontend

---

## 📈 Scale This Up

| Current | Production |
|---------|-----------|
| Python dict cache | Redis (shared across servers) |
| Single server | Load balanced instances |
| 10 min cache | Configurable TTL per endpoint |
| In-process | Distributed cache |

---

## 👨‍💻 Author

**Ansar Kamal** — building one project every day until I land
a role at a top tech company.

## 📅 The Journey

| Day | Project | Concept |
|-----|---------|---------|
| 1 | URL Shortener | REST APIs, hashing |
| 2 | Chat App + Voice | WebSockets, WebRTC |
| 3 | Expense Tracker | JWT auth, CRUD |
| **4** | **Weather Dashboard** | **External APIs, caching** |

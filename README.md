# 🌤 ClimaBot

ClimaBot is an asynchronous Telegram weather bot built with **Python** and **Aiogram 3**.
The bot allows users to set their location and receive **current weather** and **weekly forecasts** directly in Telegram.

The project follows a **modular backend architecture**, separating handlers, services, database logic, and UI keyboards for maintainability and scalability.

---

# 🚀 Features

• Get **today's weather**
• View **multi-day weather forecast**
• Set location via **GPS** or **region selection**
• Change location anytime
• Clean Telegram UI with reply and inline keyboards
• Asynchronous API requests for high performance

Planned features:

• Scheduled daily weather notifications
• Redis caching for API responses
• User weather preferences

---

# 🧠 Architecture

The project follows a layered structure:

```
app/
│
├── core/          # Core configuration and lifecycle logic
├── database/      # Database models, schema, and region data
├── handlers/      # Telegram update handlers
├── keyboards/     # Reply and inline keyboard UI
├── services/      # External API integrations
├── states/        # FSM conversation states
├── utils/         # Utility helpers
│
└── main.py        # Application entry point
```

Each layer has a **single responsibility**, making the project easier to scale and maintain.

---

# ⚙️ Tech Stack

**Language**

* Python 3.13

**Framework**

* Aiogram 3

**Database**

* PostgreSQL
* asyncpg

**APIs**

* Open-Meteo API (weather data)
* Geocoding API (coordinates → region name)

**Other**

* asyncio
* dotenv configuration

---

# 📂 Project Structure

```
app
 ├── core
 │   ├── config.py
 │   ├── events.py
 │   └── exceptions.py
 │
 ├── database
 │   ├── manager.py
 │   ├── models.py
 │   ├── regions.py
 │   ├── wmo_codes.py
 │   └── scheme.sql
 │
 ├── handlers
 │   ├── start.py
 │   ├── location.py
 │   └── weather.py
 │
 ├── keyboards
 │   ├── inline_buttons.py
 │   └── reply_buttons.py
 │
 ├── services
 │   ├── geocoding.py
 │   └── open_meteo.py
 │
 ├── states
 │   └── user_states.py
 │
 ├── utils
 │   └── consoles.py
 │
 └── main.py
```

---

# 🔄 Bot Workflow

### 1️⃣ Start

User runs:

```
/start
```

Bot provides two options:

• Send location (GPS)
• Choose region manually

---

### 2️⃣ Location Setup

User can:

• Send Telegram location
• Select a region from inline buttons

The bot stores the user's coordinates in the database.

---

### 3️⃣ Main Menu

After location is set:

```
🌤 Today Weather
📅 Forecast
📍 Change Location
```

---

### 4️⃣ Weather Request

When a user requests weather:

1. Bot retrieves stored coordinates
2. Sends request to **Open-Meteo API**
3. Formats the response
4. Sends weather message to user

Example:

```
☁ Fri
Temp: 7.7°C
Humidity: 56%
Cloudiness: 52%
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root:

```
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=postgresql://user:password@localhost:5432/database
```

---

# 🛠 Installation

Clone the repository:

```
git clone https://github.com/tim-alimov/climabot.git
cd climabot
```

Create virtual environment:

```
python -m venv venv
```

Activate it:

Mac/Linux

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the bot:

```
python app/main.py
```

---

# 📈 Future Improvements

Planned development:

• Weather notification scheduling
• Redis caching layer
• Improved logging system
• Better error handling
• Docker containerization

---

# 👨‍💻 Author

**Timur Alimov**

Backend developer focused on:

* Python
* Backend systems
* Telegram automation
* Scalable bot architecture

---

# ⭐ Notes

This project is part of a learning journey toward building **production-level backend systems and Telegram bots**.

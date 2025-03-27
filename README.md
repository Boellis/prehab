# PrehabTakehome

PrehabTakehome is a full-stack workout management application. It uses Python(FastAPI) for the backend and React + TypeScript for the frontend.

---

## Features

- User authentication with JWT  
- CRUD operations on exercises  
- Favorite, save, and rate workouts  
- View aggregated rating and popularity  
- User-specific exercise management  
- Search and filter by difficulty, description, title, favorites, and saves  
- Full REST API with Swagger docs  

---

## Project Structure
├── app/                   # FastAPI backend
│   ├── core/              # Config and security
│   │   ├── config.py
│   │   ├── security.py
│   ├── db/                # Database models and session
│   │   ├── database.py
│   │   ├── models.py
│   ├── routers/           # Auth, exercises, favorites, saves, ratings, list/collections
│   │   ├── auth.py
│   │   ├── collection.py
│   │   ├── exercises.py
│   │   ├── favorites.py
│   │   ├── ratings.py
│   │   ├── saves.py
│   ├── schemas/           # Pydantic models
│   │   ├── exercise.py
│   │   ├── rating.py
│   │   ├── token.py
│   │   ├── user.py
│   ├── main.py            # Entry point
│   ├── __init__.py          
├── test.db                # SQLite DB
├── requirements.txt
└── README.md

## Install Dependencies

# [P]rehab Take Home

This project is my attempt at a basic CRUD implementataion of a full-stack workout management application. It uses Python(FastAPI) for the backend and React + TypeScript for the frontend. If you prefer I use solely, I can move the frontend to Tkinter. If you find you are running into bugs, the easiest way to fix it is to restart both your frontend and backend.


## Features

- User authentication with JWT  
- CRUD operations on exercises  
- Favorite, save, and rate workouts  
- View aggregated rating and popularity  
- User-specific exercise management  
- Search and filter by difficulty, description, title, favorites, and saves  
- Full REST API with Swagger docs  and ReDoc

---

## Project Structure
```
prehab/
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
│
├── tests/                 # Unit tests
│   ├── __init__.py
│   ├── conftest.py
│   └── test_exercises.py
├── frontend/              # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/    # Login and Register Forms, Exercise and Collection Dashboards, Rate Exercise Form, and BUttona
│   │   ├── api/           # Axios
│   │   ├── App.tsx        
│   │   └── main.tsx
│   ├── README.md
└── 
```

## Project Setup
### Setting up the Backend
0. This project requires Python 3.10+. If you currently don't have Python 3.10 installed, you can download it here: https://www.python.org/downloads/release/python-3100/.<br></br>
1. Clone the repository and navigate into the root directory of the project. `Your repo might download as prehab-main instead of prehab. In such a case, after cloning the repo you'll run: cd prehab-main`
```
git clone https://github.com/boellis/prehab.git
cd prehab
```
2. Create a virtual envinronment (Optional)
```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. Install dependencies by navigating to your projects root directory(the folder where you cloned your repository) and run either
```
pip install -r requirements.txt
```
or 
```
py -m pip install -r requirements.txt
```

4. Run FastAPI server
From the project root, run the following in your terminal:
```
uvicorn app.main:app --reload
```
or if you're in the app folder:
```
uvicorn main:app --reload
```

### Setting up the Frontend
1. In a new terminal, navigate to the prehab/frontend/ folder within your cloned project by running the following in the terminal:
```
cd frontend
```
2. Install Axios by running the following command in your terminal:
```
npm install axios
```
3. Install Node dependencies by running the following in the terminal:
```
npm install
# or
yarn install
```
4. Start TypeScript App by running the following in the terminal:
```
npm run dev
# or
yarn dev
```
5. You should see your dev server start in the terminal (usually on http://localhost:5173).

   
## Accessing the API Docs
1. Once the backend server(FastAPI) is running, navigate to:
  - Swagger UI: http://localhost:8000/docs
     - Use Swagger to explore and test endpoints, view request/response formats, and see required headers or query params.
  - ReDoc: http://localhost:8000/redoc
     - Use ReDoc to view the API documentation. 

## Unit Tests
1. Tests are written using pytest.
  - Ensure `prehab/tests/__init__.py` exists.

2. Ensure you are in the root directory of your project then run the following in your terminal:
```
pytest
```
3. Tests use an in-memory SQLite database and cover:
  - User registration/login
  - CRUD for exercises
  - Save, favorite, and rate workflows

## Notes
1. Many of the try catch blocks have generic errors rather than explicitly stating what the errors are. With more time, I would detail out each of these.
2. I'd started integratinig alembic for database schema migration but realized I've crossed over the time limit by a handful of hours.
   - The summary of that workflow is update SQLAlchemy model(e.g add new column or something similar) --> Generate migration script with `alembic revision --autogenerate -m "message'` --> Apply migration and update db schema with `alembic upgrade head`.

## Setting up the Frontend from Scratch <b>(Not Required for Testing the At Home Assessment)<b>
1. Open a terminal in your root directory and run the following commands to create a new Vite project:

```
# Create a new Vite project in a folder called "frontend" using the React + TypeScript template
npx create-vite@latest frontend --template react-ts

# Change directory into the project
cd frontend

# Install dependencies
npm install
```
2. Once installed, you can run the development server:
```
npm run dev
```
3. Vite will start a dev server (usually on http://localhost:5173).
4. If you already have a dev server running, the port number will continue to increment such that the second dev server address will be http://localhost:5174 and so on.


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


## Project Structure
1. 

## Project Setup
### Backend
1. Clone the repository
```
git clone https://github.com/boellis/PrehabTakehome.git
cd PrehabTakehome
```
2. Create a virtual envinronment (Optional)
```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. Install Dependencies
Navigate to your projects root directory(the folder where you cloned your repository in to) and run either
```
pip install -r requirements.txt
```
or 
```
py -m pip install -r requirements.txt
```
4. Create a .env file in the root
```
PROJECT_NAME="Prehab Takehome"
API_VERSION="v1"
JWT_SECRET_KEY="SUPERSECRETKEY"
DATABASE_URL=sqlite:///./test.db

```
5. Run FastAPI server
From the project root, run the following in your terminal:
```
uvicorn app.main:app --reload
```
or if you're in the app folder:
```
uvicorn main:app --reload
```


### Frontend
1. Go to the /frontend/ folder within your cloned project by running the following in the terminal:
```
cd frontend
```
2. Install Node dependencies by running the following in the terminal:
```
npm install
# or
yarn install
```
3. Start React App by running the following in the terminal:
```
npm run dev
# or
yarn dev
```


#### Building the Frontend
1. Open a terminal and run the following commands to create a new Vite project:

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


## Accessing the API Docs
1. Once the backend server(FastAPI) is running, navigate to:
  - Swagger UI: http://localhost:8000/docs
  - ReDoc: http://localhost:8000/redoc

2. Use Swagger to explore and test endpoints, view request/response formats, and see required headers or query params. Use ReDoc to view the API documentation. 

## Unit Tests
1. Tets are written using pytest.
  - Ensure tests/'__init__.py' exists.

2. Run test from the project root by running the following in your terminal:
```
pytest
```
3. Tests use an in-memory SQLite database and cover:
  - User registration/login
  - CRUD for exercises
  - Save, favorite, and rate workflows



# [P]rehab Take Home

This project is a brief showcase of my programming and problem solving skills; built to demonstrate my readiness for the Backend Software Engineer role you all have open on your page. I designed the backend using FastAPI (Python) and the frontend with TypeScript, focusing on creating a project that's secure and scalable. The project also includes a fully functional REST API, JWT-based authentication, and a migration pipeline that transfers data from Java H2 to SQLite using Alembic.


## Features

- User authentication with JWT  
- CRUD operations on exercises  
- Favorite, save, and rate workouts  
- View aggregated rating and features  
- Retrieve specific or list of exercises  
- Search and filter by difficulty, description, title, favorites, and saves  
- Full REST API with Swagger docs  and ReDoc
- Migration pipleine for Java H2 to Python SQLite

---

**Tech Stack:**

| Area         | Technologies Used                                       |
|--------------|---------------------------------------------------------|
| Backend      | Python (FastAPI, SQLite, SQLAlchemy, Alembic)           |
| Frontend     | TypeScript (Axios, Vite)                                |
| Auth         | JWT tokens                                              |
| Testing      | pytest                                                  |
| Migration    | Java, H2 Database, Apache Maven, CSV Exports, Alembic   |

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
├── alembic.ini            # Database configuration file for migration
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
│   │   ├── components/    # Login and Register Forms, Exercise and Collection Dashboards, Rate Exercise Form, and Buttons
│   │   ├── api/           # Axios
│   │   ├── App.tsx        
│   │   └── main.tsx
│   ├── README.md
│
├── java_backend_migration/             # Java Database Schema, Creation, and Data export
│   ├── target/                         # Maven genreated files
│   │   ├── h2-2.1.212.jar                             # H2 Database Jar
│   │   ├── java-backend-migration-1.0.jar             # Jar Generated from pom.xml
│   ├── src/main/java/com/prehab/
│   │   ├── Database.java               # Handles H2 DB Creation 
│   │   ├── ExportData.java             # Handles Exporting DB to CSV
│   │   ├── InsertSampleData.java       # Handles adding data to DB
│   │   ├── Main.java                   # Handles scripts to creating, insert data, and export data to and from database
│   ├── pom.xml
│   
├── alembic/                # Python Database migrations
│   ├── env.py              # Alembic file to run database migrations
│   ├── versions/                         
│   │   ├── <generated_revision_id>_intial_schema.py        # Generated file that handles csv to db conversions. Refer to example in repo for code. 
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

## Migration Pipeline: Java H2 to Python SQLite

How to setup the migration pipeline for transferring data from a Java H2 database to a Python SQLite backend using Alembic.

### Prerequisites

- **Java JDK:** Download from [Oracle](https://www.oracle.com/java/technologies/javase-downloads.html) or [OpenJDK](https://openjdk.java.net/).
- **Apache Maven:** Download and install from [Maven Download](https://maven.apache.org/download.cgi).
- **Python & pip**
- **Alembic:** Install via `pip install alembic`.

### Part 1: Java H2 Database

1. **Setup Maven Project:**
   - The Maven project is currently set up in the `java_backend_migration/` directory.
      - You can find the generated Maven files in the `/target/` subfolder. 
   - `pom.xml` includes the H2 dependency.

2. **Database Setup:**
   - `Database.java` creates the H2 database and the schema.
   - `InsertSampleData.java` inserts sample data (e.g., user "john_doe", exercise "Push Ups").
   - `ExportData.java` exports each table to CSV files.

3. **Run Java Application:**
   ```bash
   mvn clean package
   java -cp target/java-backend-migration-1.0.jar com.example.Main
   ```
   This creates the H2 database file (javadb.mv.db), inserts sample data, and generates CSV files (users.csv, exercises.csv, etc.).
   
5. **Incase you Encounter Errors with H2 Driver during Step 3**
   - You’ll know because no csv files will generate and you'll have an error like `java.sql.SQLException: No suitable driver found for jdbc:h2:./javadb`.
   - To fix this you'll:
      -  Download H2 jar version 2.1.212 from [H2Database](https://www.h2database.com/html/download-archive.html)
      -  Save your files in a location that is easy to find as you'll have to copy the jar file to your root folder.
      -  After your files are downloaded, copy the `h2-2.1.212.jar` and save it to your `prehab/java_backend_migration/target/` folder.
      -  Run `java -cp “target/java-backend-migration-1.0.jar;target/h2-2.1.212.jar” com.prehab.Main` from your root folder to create your h2 db and csv files.

### Part 2: Python Migration

1. **Initialize Alembic**
   - In the root directory, initialize Alembic: `alembic init alembic`
  
2. **Configure Alembic**
   - In `alembic.ini`, set the database URL: `sqlalchemy.url = sqlite:///./test.db`
   - Then, in `alembic/env.py`, import your SQLAlchemy Base and set the target metadata:
      ```
      from app.db.database import Base  # Adjust the path as needed
      target_metadata = Base.metadata  # Replace the existing target_metadata variable with this
      ```
  
3. **Create Initial Schema Migration**
   - From the root directory, run the following commands:
     ```
     alembic revision --autogenerate -m "initial schema"
     alembic upgrade head
     ```
  
3. **Data Migration**
   - Create a new revision to import CSV data by running the following command in your terminal from the root directory: `alembic revision -m "migrate data from H2 export"`
   - Edit the generated revision file (for example, see the example code in `alembic/version/bf7224325043_initial_schema.py`) to load CSV files, then save your changes.
   - Run the migration by running the following command in your terminal from the doot directory: `alembic upgrade head`.


## Notes
1. To build out the functionality for yourself, you can do the following and will able to follow the instructions in the README to get the same results.
  - Remove target folder `prehab/java_backend_migration/target`
  - Remove alembic folder `prehab/alembic` and alembic.ini from root `prehab/alembic.ini`
  - Remove test.db from root `prehab/test.db`

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


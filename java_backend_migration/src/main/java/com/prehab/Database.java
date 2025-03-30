package com.prehab;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.sql.SQLException;

// Database class is responsible for creating a connection to a file-based H2 database and initializing the schema (tables) that mirror our Python backend models.
public class Database {

    // H2 connection string: creates "javadb.mv.db" in the project root
    private static final String DB_URL = "jdbc:h2:./javadb";
    private static final String USER = "prehabadmin";
    private static final String PASSWORD = "";

    // Returns a new database connection.
    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(DB_URL, USER, PASSWORD);
    }

    // Initializes the database schema by creating needed tables.
    public static void initialize() {
        try (Connection conn = getConnection();
             Statement stmt = conn.createStatement()) {

            // Create "users" table
            String createUsers = "CREATE TABLE IF NOT EXISTS users ("
                    + "id INT AUTO_INCREMENT PRIMARY KEY, "
                    + "username VARCHAR(255) NOT NULL UNIQUE, "
                    + "hashed_password VARCHAR(255) NOT NULL"
                    + ");";
            stmt.execute(createUsers);

            // Create "exercises" table
            String createExercises = "CREATE TABLE IF NOT EXISTS exercises ("
                    + "id INT AUTO_INCREMENT PRIMARY KEY, "
                    + "name VARCHAR(255) NOT NULL, "
                    + "description VARCHAR(1024), "
                    + "difficulty INT NOT NULL, "
                    + "is_public BOOLEAN NOT NULL, "
                    + "owner_id INT NOT NULL, "
                    + "FOREIGN KEY (owner_id) REFERENCES users(id)"
                    + ");";
            stmt.execute(createExercises);

            // Create "favorites" table
            String createFavorites = "CREATE TABLE IF NOT EXISTS favorites ("
                    + "id INT AUTO_INCREMENT PRIMARY KEY, "
                    + "user_id INT NOT NULL, "
                    + "exercise_id INT NOT NULL, "
                    + "UNIQUE (user_id, exercise_id), "
                    + "FOREIGN KEY (user_id) REFERENCES users(id), "
                    + "FOREIGN KEY (exercise_id) REFERENCES exercises(id)"
                    + ");";
            stmt.execute(createFavorites);

            // Create "saved" table
            String createSaved = "CREATE TABLE IF NOT EXISTS saved ("
                    + "id INT AUTO_INCREMENT PRIMARY KEY, "
                    + "user_id INT NOT NULL, "
                    + "exercise_id INT NOT NULL, "
                    + "UNIQUE (user_id, exercise_id), "
                    + "FOREIGN KEY (user_id) REFERENCES users(id), "
                    + "FOREIGN KEY (exercise_id) REFERENCES exercises(id)"
                    + ");";
            stmt.execute(createSaved);

            // Create "ratings" table
            String createRatings = "CREATE TABLE IF NOT EXISTS ratings ("
                    + "id INT AUTO_INCREMENT PRIMARY KEY, "
                    + "user_id INT NOT NULL, "
                    + "exercise_id INT NOT NULL, "
                    + "rating INT NOT NULL, "
                    + "UNIQUE (user_id, exercise_id), "
                    + "FOREIGN KEY (user_id) REFERENCES users(id), "
                    + "FOREIGN KEY (exercise_id) REFERENCES exercises(id)"
                    + ");";
            stmt.execute(createRatings);

            System.out.println("Database schema created successfully.");

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}

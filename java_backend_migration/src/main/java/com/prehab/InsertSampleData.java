package com.prehab;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

// Class inserts sample data into our H2 database. The data here mirrors the data in our Python backend(user, exercise, etc....).
public class InsertSampleData {

    // Inserts sample records into the database.
    public static void insertData() {
        try (Connection conn = Database.getConnection()) {

            // Insert a sample user
            String insertUser = "INSERT INTO users (username, hashed_password) VALUES (?, ?)";
            try (PreparedStatement pstmt = conn.prepareStatement(insertUser)) {
                pstmt.setString(1, "john_doe");
                pstmt.setString(2, "hashedpassword123");
                pstmt.executeUpdate();
            }

            // Insert a sample exercise for user id 1
            String insertExercise = "INSERT INTO exercises (name, description, difficulty, is_public, owner_id) VALUES (?, ?, ?, ?, ?)";
            try (PreparedStatement pstmt = conn.prepareStatement(insertExercise)) {
                pstmt.setString(1, "Push Ups");
                pstmt.setString(2, "A basic push up exercise.");
                pstmt.setInt(3, 3);
                pstmt.setBoolean(4, true);
                pstmt.setInt(5, 1);
                pstmt.executeUpdate();
            }

            System.out.println("Sample data inserted successfully.");

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}

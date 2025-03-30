package com.prehab;

/*
Main class ties together the database initialization, data insertion, and CSV export functionalities.

Running this class will:
1. Create the H2 database schema.
2. Insert sample data into the tables.
3. Export the data from each table to CSV files.
*/

public class Main {
    public static void main(String[] args) {
        // Create the database schema
        Database.initialize();

        // Insert sample data
        InsertSampleData.insertData();

        // Export tables to CSV files for migration
        ExportData.exportTableToCSV("users", "users.csv");
        ExportData.exportTableToCSV("exercises", "exercises.csv");
        ExportData.exportTableToCSV("favorites", "favorites.csv");
        ExportData.exportTableToCSV("saved", "saved.csv");
        ExportData.exportTableToCSV("ratings", "ratings.csv");

        System.out.println("Data export completed.");
    }
}

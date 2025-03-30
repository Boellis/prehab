package com.prehab;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.io.FileWriter;
import java.io.IOException;

// Class used to export data from H2 table into a csv file. We'll later import this csv into our Python backend.
public class ExportData {

    /*
     Exports the specified table to a csv file.
     @param tableName the name of the table to export.
     @param csvFileName the output csv file name.
    */

    public static void exportTableToCSV(String tableName, String csvFileName) {
        String query = "SELECT * FROM " + tableName;
        try (Connection conn = Database.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(query);
             FileWriter csvWriter = new FileWriter(csvFileName)) {

            int columnCount = rs.getMetaData().getColumnCount();

            // Write header row with column names
            for (int i = 1; i <= columnCount; i++) {
                csvWriter.append(rs.getMetaData().getColumnName(i));
                if (i < columnCount) {
                    csvWriter.append(",");
                }
            }
            csvWriter.append("\n");

            // Write each row of data
            while (rs.next()) {
                for (int i = 1; i <= columnCount; i++) {
                    csvWriter.append(rs.getString(i) != null ? rs.getString(i) : "");
                    if (i < columnCount) {
                        csvWriter.append(",");
                    }
                }
                csvWriter.append("\n");
            }
            System.out.println("Exported " + tableName + " to " + csvFileName);
        } catch (SQLException | IOException e) {
            e.printStackTrace();
        }
    }
}

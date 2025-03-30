/*
Provides admin controls for:
1. Toggling between local (SQLite) and cloud (Firestore) data sources.
2. Migrating local exercise data to Firestore.
*/

import React from 'react';
import API from '../api/axios';

interface AdminDashboardProps {
  useCloudData: boolean;
  setUseCloudData: (value: boolean) => void;
}

export const AdminDashboard: React.FC<AdminDashboardProps> = ({ useCloudData, setUseCloudData }) => {
  const toggleDataSource = () => {
    setUseCloudData(!useCloudData);
  };

  const handleMigrateData = async () => {
    try {
      const res = await API.post('/migrate/exercises');
      alert(res.data.message);
    } catch (error: any) {
      alert('Data migration failed: ' + (error.response?.data.detail || error.message));
      console.error(error);
    }
  };

  const handleUploadCSV = async () => {
    // Placeholder for CSV upload functionality.
    alert("CSV upload functionality not yet implemented.");
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Admin Dashboard</h2>
      
      {/* Data Source Toggle Section */}
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem',
        border: '1px solid #ccc',
        padding: '1rem',
        borderRadius: '8px',
        marginBottom: '2rem'
      }}>
        <h3>Data Source Settings</h3>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>Current Data Source:</span>
          <span style={{ fontWeight: 'bold' }}>{useCloudData ? 'Cloud (Firestore)' : 'Local (SQLite)'}</span>
        </div>
        <button onClick={toggleDataSource} style={{ padding: '0.5rem 1rem' }}>
          Switch to {useCloudData ? 'Local' : 'Cloud'} Data
        </button>
      </div>

      {/* Data Migration Section */}
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem',
        border: '1px solid #ccc',
        padding: '1rem',
        borderRadius: '8px',
        marginBottom: '2rem'
      }}>
        <h3>Data Migration</h3>
        <p>
          Click the button below to migrate all local exercise data (SQLite) to Firestore.
          Ensure your backend is running and Firebase Admin is configured.
        </p>
        <button onClick={handleMigrateData} style={{ padding: '0.5rem 1rem' }}>
          Migrate Data to Cloud
        </button>
      </div>

      {/* CSV Upload Section */}
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem',
        border: '1px solid #ccc',
        padding: '1rem',
        borderRadius: '8px'
      }}>
        <h3>CSV Data Upload</h3>
        <p>
          Use this section to upload CSV files (generated from our Java migration scripts)
          and populate the database.
        </p>
        <button onClick={handleUploadCSV} style={{ padding: '0.5rem 1rem' }}>
          Upload CSV Files
        </button>
      </div>
    </div>
  );
};

export default AdminDashboard;
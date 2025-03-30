/*
Our navigation bar that displays buttons for Logout, Refresh Token,
Dashboard, My Collection, and Admin Dashboard. All buttons share the same styling.
*/

import React from 'react';

interface NavBarProps {
  onLogout: () => void;
  onRefreshToken: () => void;
  onDashboard: () => void;
  onCollection: () => void;
  onAdmin: () => void;
}

export const NavBar: React.FC<NavBarProps> = ({
  onLogout,
  onRefreshToken,
  onDashboard,
  onCollection,
  onAdmin,
}) => {
  return (
    <div
      style={{
        display: 'flex',
        gap: '1rem',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: '1rem',
        marginTop: '1rem'
      }}
    >
      <button onClick={onLogout} style={{ padding: '1.2rem 1rem' }}>
        Logout
      </button>
      <button onClick={onRefreshToken} style={{ padding: '0.5rem 1rem' }}>
        Refresh Token
      </button>
      <button onClick={onDashboard} style={{ padding: '1.2rem 1rem' }}>
        Dashboard
      </button>
      <button onClick={onCollection} style={{ padding: '0.5rem 1rem' }}>
        My Collection
      </button>
      <button onClick={onAdmin} style={{ padding: '0.5rem 1rem' }}>
        Admin Dashboard
      </button>
    </div>
  );
};

export default NavBar;

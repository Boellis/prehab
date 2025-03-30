/* 
This component displays the combined list of favorited and saved exercises.
*/

import React, { useEffect, useState } from 'react';
import API from '../api/axios';

interface Exercise {
  id: number;
  name: string;
  description: string;
  difficulty: number;
  is_public: boolean;
  owner_id: number;
  favorite_count: number;
  save_count: number;
}

export const CollectionDashboard: React.FC = () => {
  const [collection, setCollection] = useState<Exercise[]>([]);

  // Fetch the collection from the backend.
  const fetchCollection = async () => {
    try {
      const res = await API.get('/collection');
      setCollection(res.data);
    } catch (error) {
      alert('Failed to load collection');
    }
  };

  useEffect(() => {
    fetchCollection();
  }, []);

  return (
    <div>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem',
        padding: '1rem',
        marginBottom: '2rem',
        //transform: 'scale(1.75)', 
        
      }}>
      <br></br>
      <h2>My Collection (Favorites & Saves)</h2>
      <ul>
        {collection.map((ex) => (
          <li key={ex.id}>
            <strong>{ex.name}</strong> - {ex.description} (Favorites: {ex.favorite_count}, Saves: {ex.save_count})
          </li>
        ))}
      </ul>
    </div>
    </div>
  );
};

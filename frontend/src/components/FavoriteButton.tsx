/*
Button component to toggle favoriting an exercise.
*/

import React, { useState } from 'react';
import API from '../api/axios';

interface FavoriteButtonProps {
  exerciseId: number;
  initiallyFavorited: boolean;
  onToggle: () => void;
}

export const FavoriteButton: React.FC<FavoriteButtonProps> = ({ exerciseId, initiallyFavorited, onToggle }) => {
  const [favorited, setFavorited] = useState(initiallyFavorited);

  const toggleFavorite = async () => {
    try {
      if (favorited) {
        // Send DELETE request to remove favorite.
        await API.delete(`/favorites/${exerciseId}`);
      } else {
        // Send POST request to add favorite.
        await API.post(`/favorites/${exerciseId}`);
      }
      // Toggle local state and invoke parent's callback.
      setFavorited(!favorited);
      onToggle();
    } catch (error) {
      alert('Failed to update favorite status');
    }
  };

  return (
    <button onClick={toggleFavorite}>
      {favorited ? 'Unfavorite' : 'Favorite'}
    </button>
  );
};

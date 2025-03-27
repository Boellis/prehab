/*
Button component to toggle saving an exercise.
*/

import React, { useState } from 'react';
import API from '../api/axios';

interface SaveButtonProps {
  exerciseId: number;
  initiallySaved: boolean;
  onToggle: () => void;
}

export const SaveButton: React.FC<SaveButtonProps> = ({ exerciseId, initiallySaved, onToggle }) => {
  const [saved, setSaved] = useState(initiallySaved);

  const toggleSave = async () => {
    try {
      if (saved) {
        // Unsave the exercise.
        await API.delete(`/saves/${exerciseId}`);
      } else {
        // Save the exercise.
        await API.post(`/saves/${exerciseId}`);
      }
      setSaved(!saved);
      onToggle();
    } catch (error) {
      alert('Failed to update save status');
    }
  };

  return (
    <button onClick={toggleSave}>
      {saved ? 'Unsave' : 'Save'}
    </button>
  );
};

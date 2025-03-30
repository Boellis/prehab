/*
Form component for rating an exercise.
*/

import React, { useState } from 'react';
import API from '../api/axios';

interface RateExerciseFormProps {
  exerciseId: number;
  onRate: (rating: number) => void;
}

export const RateExerciseForm: React.FC<RateExerciseFormProps> = ({ exerciseId, onRate }) => {
  const [rating, setRating] = useState<number>(3); // default rating is 3

  const submitRating = async () => {
    try {
      // Submit the rating via POST to the backend.
      await API.post(`/ratings/${exerciseId}`, { rating });
      onRate(rating);
    } catch (error) {
      alert('Failed to rate the exercise');
    }
  };

  return (
    <div>
      <input
        type="number"
        min="1"
        max="5"
        value={rating}
        onChange={(e) => setRating(parseInt(e.target.value, 10))}
      />
      <button onClick={submitRating}>Submit Rating</button>
    </div>
  );
};

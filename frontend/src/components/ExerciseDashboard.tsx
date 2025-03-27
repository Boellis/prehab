/*
Dashboard to display and manage exercises. This component lists exercises and provides controls for editing, deleting, favoriting, saving, and rating an exercise.
*/
import React, { useEffect, useState } from 'react';
import API from '../api/axios';
import { FavoriteButton } from './FavoriteButton';
import { SaveButton } from './SaveButton';
import { RateExerciseForm } from './RateExerciseForm';

interface Exercise {
  id: number;
  name: string;
  description: string;
  difficulty: number;
  is_public: boolean;
  owner_id: number;
  favorite_count: number;
  save_count: number;
  user_has_favorited: boolean;
  user_has_saved: boolean;
  average_rating: number;
}

interface User {
  id: number;
  username: string;
}

interface ExerciseDashboardProps {
  token: string;
}

export const ExerciseDashboard: React.FC<ExerciseDashboardProps> = ({ token }) => {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  // States for new exercise creation.
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [isPublic, setIsPublic] = useState(true);
  // States for editing an exercise.
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editName, setEditName] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [editDifficulty, setEditDifficulty] = useState('');
  const [editIsPublic, setEditIsPublic] = useState(true);
  // Additional state for search, sorting, and viewing user lists.
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState<'difficulty' | 'name' | 'description' | 'favorite_count' | 'save_count'>('difficulty');
  const [showOnlyFavorites, setShowOnlyFavorites] = useState(false);
  const [userLists, setUserLists] = useState<{ [key: number]: { favorited_by: User[]; saved_by: User[] } | null }>({});

  // Fetch exercises from the backend.
  const fetchExercises = async () => {
    try {
      const res = await API.get('/exercises/');
      setExercises(res.data);
    } catch (error) {
      alert('Failed to load exercises');
    }
  };

  useEffect(() => {
    fetchExercises();
  }, []);

  // Function to create a new exercise.
  const createExercise = async () => {
    try {
      await API.post('/exercises/', {
        name,
        description,
        difficulty: Number(difficulty),
        is_public: isPublic,
      });
      // Reset form fields.
      setName('');
      setDescription('');
      setDifficulty('');
      setIsPublic(true);
      fetchExercises();
    } catch (error) {
      alert('Failed to create exercise');
    }
  };

  // Function to delete an exercise.
  const deleteExercise = async (id: number) => {
    try {
      await API.delete(`/exercises/${id}`);
      fetchExercises();
    } catch (error) {
      alert('Failed to delete exercise');
    }
  };

  // Function to start editing an exercise.
  const startEdit = (ex: Exercise) => {
    setEditingId(ex.id);
    setEditName(ex.name);
    setEditDescription(ex.description);
    setEditDifficulty(String(ex.difficulty));
    setEditIsPublic(ex.is_public);
  };

  // Function to save edited changes.
  const saveEdit = async (id: number) => {
    try {
      await API.put(`/exercises/${id}`, {
        name: editName,
        description: editDescription,
        difficulty: Number(editDifficulty),
        is_public: editIsPublic,
      });
      setEditingId(null);
      fetchExercises();
    } catch (error) {
      alert('Failed to update exercise');
    }
  };

  // Fetch the list of users who favorited/saved an exercise.
  const fetchUserList = async (exerciseId: number) => {
    try {
      const res = await API.get(`/exercises/${exerciseId}/users`);
      setUserLists((prev) => ({ ...prev, [exerciseId]: res.data }));
    } catch (error) {
      alert('Failed to load user list');
    }
  };

  const toggleUserList = (exerciseId: number) => {
    if (userLists[exerciseId]) {
      setUserLists((prev) => ({ ...prev, [exerciseId]: null }));
    } else {
      fetchUserList(exerciseId);
    }
  };

  // Filtering, searching, and sorting logic.
  const filtered = exercises
    .filter((ex) => {
      if (!search) return true;
      const searchLower = search.toLowerCase();
      return (
        ex.name.toLowerCase().includes(searchLower) ||
        ex.description.toLowerCase().includes(searchLower) ||
        ex.difficulty.toString().includes(searchLower) ||
        ex.favorite_count.toString().includes(searchLower) ||
        ex.save_count.toString().includes(searchLower)
      );
    })
    .filter((ex) => !showOnlyFavorites || ex.user_has_favorited)
    .sort((a, b) => {
      if (sortBy === 'difficulty') return a.difficulty - b.difficulty;
      if (sortBy === 'name') return a.name.localeCompare(b.name);
      if (sortBy === 'description') return a.description.localeCompare(b.description);
      if (sortBy === 'favorite_count') return a.favorite_count - b.favorite_count;
      if (sortBy === 'save_count') return a.save_count - b.save_count;
      return 0;
    });

  return (
    <div>
      <h2>Exercises Dashboard</h2>
      
      <div style={{ marginBottom: '1rem' }}>
        <label>Sort By:</label>
        <select value={sortBy} onChange={(e) => setSortBy(e.target.value as any)}>
          <option value="difficulty">Difficulty</option>
          <option value="name">Name</option>
          <option value="description">Description</option>
          <option value="favorite_count">Favorites</option>
          <option value="save_count">Saves</option>
        </select>

        <input
          type="text"
          placeholder="Search exercises..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ marginLeft: '1rem' }}
        />
        <label style={{ marginLeft: '1rem' }}>
          Show only favorites:
          <input
            type="checkbox"
            checked={showOnlyFavorites}
            onChange={() => setShowOnlyFavorites(!showOnlyFavorites)}
          />
        </label>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <h3>Create New Exercise</h3>
        <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
        <input placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
        <input
          type="number"
          placeholder="Difficulty"
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
        />
        <label>
          Public:
          <input type="checkbox" checked={isPublic} onChange={() => setIsPublic(!isPublic)} />
        </label>
        <button onClick={createExercise}>Create</button>
      </div>

      <ul>
        {filtered.map((ex) => (
          <li key={ex.id} style={{ marginBottom: '1rem', borderBottom: '1px solid #ccc', paddingBottom: '1rem' }}>
            {editingId === ex.id ? (
              <div>
                <input value={editName} onChange={(e) => setEditName(e.target.value)} />
                <input value={editDescription} onChange={(e) => setEditDescription(e.target.value)} />
                <input
                  type="number"
                  value={editDifficulty}
                  onChange={(e) => setEditDifficulty(e.target.value)}
                />
                <label>
                  Public:
                  <input
                    type="checkbox"
                    checked={editIsPublic}
                    onChange={() => setEditIsPublic(!editIsPublic)}
                  />
                </label>
                <button onClick={() => saveEdit(ex.id)}>Save</button>
                <button onClick={() => setEditingId(null)}>Cancel</button>
              </div>
            ) : (
              <div>
                <strong>{ex.name}</strong> - {ex.description} (Difficulty: {ex.difficulty}) [{ex.is_public ? 'Public' : 'Private'}]
                <br />
                Favorites: {ex.favorite_count} | Saves: {ex.save_count} | Average Rating: {ex.average_rating}
                <br />
                <FavoriteButton
                  exerciseId={ex.id}
                  initiallyFavorited={ex.user_has_favorited}
                  onToggle={fetchExercises}
                />
                <SaveButton
                  exerciseId={ex.id}
                  initiallySaved={ex.user_has_saved}
                  onToggle={fetchExercises}
                />
                <RateExerciseForm
                  exerciseId={ex.id}
                  onRate={(rating) => {
                    console.log(`Rated exercise ${ex.id} with rating ${rating}`);
                    fetchExercises();
                  }}
                />
                <br />
                <button onClick={() => toggleUserList(ex.id)}>
                  {userLists[ex.id] ? 'Hide Users' : 'View Users'}
                </button>
                {userLists[ex.id] && (
                  <div style={{ marginTop: '0.5rem' }}>
                    <strong>Favorited By:</strong>
                    <ul>
                      {userLists[ex.id]?.favorited_by.map((user) => (
                        <li key={user.id}>{user.username}</li>
                      ))}
                    </ul>
                    <strong>Saved By:</strong>
                    <ul>
                      {userLists[ex.id]?.saved_by.map((user) => (
                        <li key={user.id}>{user.username}</li>
                      ))}
                    </ul>
                  </div>
                )}
                <br />
                <button onClick={() => startEdit(ex)}>Edit</button>
                <button onClick={() => deleteExercise(ex.id)}>Delete</button>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

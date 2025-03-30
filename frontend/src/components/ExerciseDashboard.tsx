/* 
Displays and manages exercises. Now includes: 
1. A video player if an exercise has a video_url.
2. The VideoUploader component for uploading videos.
3. Updated layout with flex containers, gaps, and margins.
*/
import React, { useEffect, useState } from 'react';
import API from '../api/axios';
import { FavoriteButton } from './FavoriteButton';
import { SaveButton } from './SaveButton';
import { RateExerciseForm } from './RateExerciseForm';
import { VideoUploader } from './VideoUploader';


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
  video_url?: string;
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
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [isPublic, setIsPublic] = useState(true);

  const [editingId, setEditingId] = useState<number | null>(null);
  const [editName, setEditName] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [editDifficulty, setEditDifficulty] = useState('');
  const [editIsPublic, setEditIsPublic] = useState(true);

  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState<'difficulty' | 'name' | 'description' | 'favorite_count' | 'save_count'>('difficulty');
  const [showOnlyFavorites, setShowOnlyFavorites] = useState(false);
  const [userLists, setUserLists] = useState<{ [key: number]: { favorited_by: User[]; saved_by: User[] } | null }>({});

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

  const createExercise = async () => {
    try {
      await API.post('/exercises/', {
        name,
        description,
        difficulty: Number(difficulty),
        is_public: isPublic,
      });
      setName('');
      setDescription('');
      setDifficulty('');
      setIsPublic(true);
      fetchExercises();
    } catch (error) {
      alert('Failed to create exercise');
    }
  };

  const deleteExercise = async (id: number) => {
    try {
      await API.delete(`/exercises/${id}`);
      fetchExercises();
    } catch (error) {
      alert('Failed to delete exercise');
    }
  };

  const startEdit = (ex: Exercise) => {
    setEditingId(ex.id);
    setEditName(ex.name);
    setEditDescription(ex.description);
    setEditDifficulty(String(ex.difficulty));
    setEditIsPublic(ex.is_public);
  };

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
      {/* Create exercise form */}
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '0.5rem',
          alignItems: 'center',
          marginBottom: '2rem',
          border: '1px solid #555',
          padding: '1rem',
          borderRadius: '4px',
        }}
      >
        <h3 style={{ flexBasis: '100%', margin: '0 0 0.5rem 0' , }}>Create New Exercise</h3>
        <input
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{ flex: '1 1 150px' }}
        />
        <input
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          style={{ flex: '2 1 300px' }}
        />
        <input
          type="number"
          placeholder="Difficulty"
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          style={{ width: '80px' }}
        />
        <label style={{ display: 'flex', alignItems: 'left',  padding: '0.5rem', marginTop: '0.25rem',justifyContent: 'center'  }}>
          Public:
          <input
            type="checkbox"
            checked={isPublic}
            onChange={() => setIsPublic(!isPublic)}
            style={{ marginLeft: '0.5rem' }}
          />
        </label>
        <button onClick={createExercise}>Create</button>
      </div>


      {/* Sorting, searching, favorites filter */}
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '0.5rem',
          alignItems: 'center',
          marginBottom: '2rem',
          border: '1px solid #555',
          padding: '1rem',
          borderRadius: '4px',
        }}
      >
        <h3 style={{ flexBasis: '100%', margin: '0 0 0.5rem 0' , }}>Sort and Search Exercises</h3>
        <div>
          <label>Sort By:</label>
          <select value={sortBy} onChange={(e) => setSortBy(e.target.value as any)}>
            <option value="difficulty">Difficulty</option>
            <option value="name">Name</option>
            <option value="description">Description</option>
            <option value="favorite_count">Favorites</option>
            <option value="save_count">Saves</option>
          </select>
        </div>

        <div>
          <input
            type="text"
            placeholder="Search exercises..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <div>
          <label>
            Show only favorites:
            <input
              type="checkbox"
              checked={showOnlyFavorites}
              onChange={() => setShowOnlyFavorites(!showOnlyFavorites)}
              style={{ marginLeft: '0.5rem' }}
            />
          </label>
        </div>
      </div>

      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '0.5rem',
          alignItems: 'center',
          marginBottom: '2rem',
          border: '1px solid #555',
          padding: '1rem',
          borderRadius: '4px',
        }}
      >
      <h3 style={{ flexBasis: '100%', margin: '0 0 0.5rem 0' , }}><u>Exercise List</u></h3>

      {/* Exercise list */}
      <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
        {filtered.map((ex) => (
          <li
            key={ex.id}
            style={{
              marginBottom: '1.5rem',
              borderBottom: '1px solid #555',
              paddingBottom: '1rem',
            }}
          >
            {/* Editing an exercise */}
            {editingId === ex.id ? (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <input value={editName} onChange={(e) => setEditName(e.target.value)} />
                <input value={editDescription} onChange={(e) => setEditDescription(e.target.value)} />
                <input
                  type="number"
                  value={editDifficulty}
                  onChange={(e) => setEditDifficulty(e.target.value)}
                  style={{ width: '80px' }}
                />
                <label style={{ display: 'flex', alignItems: 'center' }}>
                  Public:
                  <input
                    type="checkbox"
                    checked={editIsPublic}
                    onChange={() => setEditIsPublic(!editIsPublic)}
                    style={{ marginLeft: '0.5rem' }}
                  />
                </label>
                <button onClick={() => saveEdit(ex.id)}>Save</button>
                <button onClick={() => setEditingId(null)}>Cancel</button>
              </div>
            ) : (
              <>
                <div style={{ marginBottom: '0.5rem' }}>
                  <strong>{ex.name}</strong> - {ex.description} (Difficulty: {ex.difficulty}){' '}
                  [{ex.is_public ? 'Public' : 'Private'}]
                </div>
                <div style={{ marginBottom: '0.5rem' }}>
                  Favorites: {ex.favorite_count} | Saves: {ex.save_count} | Average Rating: {ex.average_rating}
                </div>
              </>
            )}

            {ex.video_url && (
              <div style={{ marginBottom: '0.5rem' }}>
                  <video width="320" height="240" controls>
                    <source src={ex.video_url} type="video/mp4" />
                      Your browser does not support the video tag.
                  </video>
              </div>
            )}
    
            <div style={{ marginBottom: '0.5rem' }}>
              <VideoUploader exerciseId={ex.id}
                onUpload={async (videoUrl) => {
                    try {
                      await API.put(`/exercises/${ex.id}`, { video_url: videoUrl });
                        fetchExercises();
                    } catch (error) {
                        alert('Failed to update exercise with video URL');
                    }
                  }}
                />
            </div>

            {/* Action buttons (favorite, save, rating, user list, edit, delete) */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '0.5rem' , padding: '0.5rem', marginTop: '0.25rem', alignItems: 'center',justifyContent: 'center' }}>
              <FavoriteButton exerciseId={ex.id} initiallyFavorited={ex.user_has_favorited} onToggle={fetchExercises} />
              <SaveButton exerciseId={ex.id} initiallySaved={ex.user_has_saved} onToggle={fetchExercises} />
              
              <button onClick={() => toggleUserList(ex.id)}>
                {userLists[ex.id] ? 'Hide Users' : 'View Users'}
              </button>
              {editingId !== ex.id && (
                <>
                  <button onClick={() => startEdit(ex)}>Edit</button>
                  <button onClick={() => deleteExercise(ex.id)}>Delete</button>
                </>
              )}
              <RateExerciseForm
                exerciseId={ex.id}
                onRate={(rating) => {
                  console.log(`Rated exercise ${ex.id} with rating ${rating}`);
                  fetchExercises();
                }}
              />
            </div>

            {/* Show favorited/saved users if toggled */}
            {userLists[ex.id] && (
              <div style={{ marginTop: '0.5rem', alignItems: 'center',justifyContent: 'center' }}>
                <strong>Favorited By:</strong>
                <ul style={{ padding: '0.5rem', marginTop: '0.25rem', alignItems: 'center',justifyContent: 'center' }}>
                  {userLists[ex.id]?.favorited_by.map((user) => (
                    <li key={user.id}>{user.username}</li>
                  ))}
                </ul>
                <strong>Saved By:</strong>
                <ul style={{ padding: '0.5rem', marginTop: '0.25rem', alignItems: 'center',justifyContent: 'center'  }}>
                  {userLists[ex.id]?.saved_by.map((user) => (
                    <li key={user.id}>{user.username}</li>
                  ))}
                </ul>
              </div>
            )}
          </li>
        ))}
      </ul>
      </div>
    </div>
  );
};

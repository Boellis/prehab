/*
Component to handle video file selection and upload to Firebase Cloud Storage.
It tracks the upload progress and returns the download URL via the onUpload callback.
*/

import React, { useState } from 'react';
import { ref, uploadBytesResumable, getDownloadURL } from 'firebase/storage';
import { storage } from '../api/firebase';

interface VideoUploaderProps {
  exerciseId: number;
  onUpload: (videoUrl: string) => void; // Callback function that gets called with the video URL once upload is complete
}

export const VideoUploader: React.FC<VideoUploaderProps> = ({ exerciseId, onUpload }) => {
  const [file, setFile] = useState<File | null>(null); // Local state to hold the selected file
  const [progress, setProgress] = useState(0); // State to track upload progress (0 to 100)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => { // Handle file input changes; update the file state when a file is selected
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  
  
  const handleUpload = () => { // Handle uploading the video to Firebase Cloud Storage
    if (!file) return;
    
    const storageRef = ref(storage, `videos/exercise_${exerciseId}/${file.name}`); // Create a reference in Firebase Storage using exerciseId and the file name.
    const uploadTask = uploadBytesResumable(storageRef, file); // Start the upload task using uploadBytesResumable, which allows us to track progress

    
    uploadTask.on('state_changed', snapshot => { // Monitor the upload state (progress, error, completion)
      const progressPercent = (snapshot.bytesTransferred / snapshot.totalBytes) * 100; // Calculate upload progress as a percentage
      setProgress(progressPercent);
    }, error => {
      alert('Upload failed: ' + error.message);
    }, () => {
      getDownloadURL(uploadTask.snapshot.ref).then(downloadURL => { // Retrieve the download URL of the uploaded file.
        onUpload(downloadURL); // Pass the download URL back to the parent component via the onUpload callback.
      });
    });
  };

  return (
    <div style={{ margin: '1rem 0' }}>
      <input type="file" accept="video/*" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload Video</button>
      {progress > 0 && <p>Upload Progress: {Math.round(progress)}%</p>}
    </div>
  );
};

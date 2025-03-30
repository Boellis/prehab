/*
  Initializes Firebase on the frontend using the Firebase client SDK based on your Firebase project configuration.
*/

import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";

const firebaseConfig = {
    apiKey: "AIzaSyB9hr53WaSL2fNEVKreb1W0nA5C7-TtAwE",
    authDomain: "prehab-a22ee.firebaseapp.com",
    projectId: "prehab-a22ee",
    storageBucket: "prehab-a22ee.firebasestorage.app",
    messagingSenderId: "568427113148",
    appId: "1:568427113148:web:06219db54dbcc6a2863eb9"
  };

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export const storage = getStorage(app);

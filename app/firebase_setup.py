"""
Initializes the Firebase Admin SDK to allow backend interaction with Firestore and Cloud Storage.
"""

import firebase_admin
from firebase_admin import credentials, firestore, storage

# Load Firebase service account key (update the path as needed)
cred = credentials.Certificate("app/serviceAccountKey.json")

# Initialize Firebase Admin with your project configuration.
firebase_admin.initialize_app(cred, {
    'storageBucket': 'prehab-a22ee.firebasestorage.app'
})

# Create Firestore and Cloud Storage clients.
db_firestore = firestore.client()
bucket = storage.bucket()

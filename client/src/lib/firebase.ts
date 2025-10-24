/**
 * Firebase Configuration
 * Setup for Firebase Storage to manage clothing image library
 */

import { initializeApp } from 'firebase/app';
import { getStorage, ref, uploadBytes, getDownloadURL, listAll, deleteObject } from 'firebase/storage';
import type { FirebaseStorage } from 'firebase/storage';

// Firebase configuration
// IMPORTANT: Replace these with your actual Firebase project credentials
// Get these from: Firebase Console > Project Settings > General > Your apps
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};

// Initialize Firebase
let app;
let storage: FirebaseStorage;

try {
  app = initializeApp(firebaseConfig);
  storage = getStorage(app);
} catch (error) {
  console.error('Firebase initialization failed:', error);
  console.warn('Using local storage fallback');
}

export { storage };

/**
 * Upload an image to Firebase Storage
 * @param file - Image file to upload
 * @param userId - User identifier (for organizing images)
 * @returns Download URL of uploaded image
 */
export async function uploadImageToFirebase(file: File, userId: string = 'default'): Promise<string> {
  if (!storage) {
    throw new Error('Firebase Storage not initialized. Please configure Firebase credentials.');
  }

  try {
    const timestamp = Date.now();
    const fileName = `${timestamp}_${file.name}`;
    const storageRef = ref(storage, `users/${userId}/clothing/${fileName}`);
    
    // Upload file
    const snapshot = await uploadBytes(storageRef, file);
    
    // Get download URL
    const downloadURL = await getDownloadURL(snapshot.ref);
    
    return downloadURL;
  } catch (error) {
    console.error('Error uploading image to Firebase:', error);
    throw error;
  }
}

/**
 * Get all images from user's library
 * @param userId - User identifier
 * @returns Array of image URLs
 */
export async function getLibraryImages(userId: string = 'default'): Promise<Array<{url: string, name: string, path: string}>> {
  if (!storage) {
    throw new Error('Firebase Storage not initialized. Please configure Firebase credentials.');
  }

  try {
    const listRef = ref(storage, `users/${userId}/clothing`);
    const result = await listAll(listRef);
    
    const imagePromises = result.items.map(async (itemRef) => {
      const url = await getDownloadURL(itemRef);
      return {
        url,
        name: itemRef.name,
        path: itemRef.fullPath
      };
    });
    
    return await Promise.all(imagePromises);
  } catch (error) {
    console.error('Error fetching library images:', error);
    return [];
  }
}

/**
 * Delete an image from Firebase Storage
 * @param imagePath - Full path of the image in storage
 */
export async function deleteImageFromFirebase(imagePath: string): Promise<void> {
  if (!storage) {
    throw new Error('Firebase Storage not initialized. Please configure Firebase credentials.');
  }

  try {
    const imageRef = ref(storage, imagePath);
    await deleteObject(imageRef);
  } catch (error) {
    console.error('Error deleting image:', error);
    throw error;
  }
}

/**
 * Check if Firebase is properly configured
 * @returns true if Firebase is configured, false otherwise
 */
export function isFirebaseConfigured(): boolean {
  return storage !== undefined && firebaseConfig.apiKey !== "YOUR_API_KEY";
}

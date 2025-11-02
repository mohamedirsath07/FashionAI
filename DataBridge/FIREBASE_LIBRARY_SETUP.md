# 🔥 Firebase Library Setup Guide

## Complete Setup for Image Library Feature

This guide will help you set up Firebase Storage to enable the full image library functionality in your StyleAI app.

---

## 📋 Prerequisites

- Google account
- Your StyleAI project
- 5-10 minutes for setup

---

## 🚀 Step-by-Step Setup

### Step 1: Create Firebase Project

1. **Go to Firebase Console**
   - Visit: https://console.firebase.google.com/
   - Click **"Add project"** or **"Create a project"**

2. **Name Your Project**
   - Enter a project name (e.g., "StyleAI" or "FashionRecommender")
   - Click **"Continue"**

3. **Google Analytics** (Optional)
   - You can disable Google Analytics for now
   - Click **"Create project"**
   - Wait for project creation (30-60 seconds)

4. **Open Your Project**
   - Click **"Continue"** when ready
   - You'll see your Firebase project dashboard

---

### Step 2: Enable Firebase Storage

1. **Navigate to Storage**
   - In the left sidebar, click **"Build"** (or "All Products")
   - Click **"Storage"**

2. **Get Started**
   - Click **"Get started"**
   - Read the security rules notice
   - Click **"Next"**

3. **Choose Location**
   - Select a Cloud Storage location near your users
   - Common choices:
     - `us-central1` (US)
     - `europe-west1` (Europe)
     - `asia-southeast1` (Asia)
   - Click **"Done"**

4. **Wait for Setup**
   - Firebase will create your storage bucket
   - This takes about 30-60 seconds

---

### Step 3: Configure Storage Rules

1. **Go to Rules Tab**
   - In Storage, click the **"Rules"** tab

2. **Update Rules for Development**
   ```javascript
   rules_version = '2';
   
   service firebase.storage {
     match /b/{bucket}/o {
       // Allow authenticated users to read/write their own files
       match /users/{userId}/{allPaths=**} {
         allow read, write: if true; // For development
         // For production, use: if request.auth != null && request.auth.uid == userId;
       }
     }
   }
   ```

3. **Publish Rules**
   - Click **"Publish"**
   - Your storage is now ready for uploads!

> **⚠️ Security Note**: The above rules allow anyone to upload/read. For production, implement proper authentication and use the commented rule instead.

---

### Step 4: Get Firebase Configuration

1. **Go to Project Settings**
   - Click the **gear icon** ⚙️ next to "Project Overview"
   - Click **"Project settings"**

2. **Scroll to "Your apps"**
   - Click the **"Web" icon** `</>`
   - If you already have a web app, skip to step 3

3. **Register Your App**
   - Enter app nickname: "StyleAI Web"
   - **Don't** check "Firebase Hosting"
   - Click **"Register app"**

4. **Copy Firebase Config**
   - You'll see a code snippet like this:
   ```javascript
   const firebaseConfig = {
     apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
     authDomain: "your-project.firebaseapp.com",
     projectId: "your-project",
     storageBucket: "your-project.appspot.com",
     messagingSenderId: "123456789012",
     appId: "1:123456789012:web:abcdef1234567890"
   };
   ```
   - **Keep this page open** - you'll need these values!

---

### Step 5: Update Your Code

1. **Open Firebase Configuration File**
   - Navigate to: `DataBridge/client/src/lib/firebase.ts`

2. **Replace Placeholder Values**
   
   **BEFORE:**
   ```typescript
   const firebaseConfig = {
     apiKey: "YOUR_API_KEY",
     authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
     projectId: "YOUR_PROJECT_ID",
     storageBucket: "YOUR_PROJECT_ID.appspot.com",
     messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
     appId: "YOUR_APP_ID"
   };
   ```

   **AFTER (using your actual values):**
   ```typescript
   const firebaseConfig = {
     apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
     authDomain: "your-project.firebaseapp.com",
     projectId: "your-project",
     storageBucket: "your-project.appspot.com",
     messagingSenderId: "123456789012",
     appId: "1:123456789012:web:abcdef1234567890"
   };
   ```

3. **Save the File**
   - Press `Ctrl+S` (Windows) or `Cmd+S` (Mac)

---

## ✅ Testing Your Setup

### Test 1: Check Configuration Status

1. **Run Your App**
   ```bash
   npm run dev
   ```

2. **Open the App**
   - Visit: http://localhost:5000

3. **Check Library Toggle**
   - The "Save to library" switch should now be **enabled** (not grayed out)
   - You should NOT see "Library (Configure Firebase)" anymore

### Test 2: Upload an Image

1. **Upload a Test Image**
   - Click "Upload from Device"
   - Select a clothing image
   - Check the "Save to library" toggle is ON

2. **Watch for Success**
   - Look for the "Saving..." badge on the image
   - It should disappear when upload completes
   - Check browser console (F12) for: `"Image uploaded to Firebase: https://..."`

### Test 3: Check Firebase Storage

1. **Go Back to Firebase Console**
   - Navigate to Storage
   - Click on the **"Files"** tab

2. **Verify Upload**
   - You should see: `users/default/clothing/[timestamp]_[filename]`
   - Click on the file to see the image

### Test 4: Library Features

1. **Click "My Library"**
   - You should see your uploaded images
   - NO "Firebase Configuration Required" message

2. **Test Bulk Upload**
   - Click "Add Images to Library"
   - Select multiple images (5-10 images)
   - Watch the progress bar
   - Verify all images appear in library

3. **Select and Use Images**
   - Click on images to select them (checkmark appears)
   - Click "Use X Selected"
   - Images should be added to your outfit generation

---

## 🎯 Features Now Available

### ✨ For Users

1. **Persistent Wardrobe Library**
   - Upload images once, use many times
   - Images stored in the cloud
   - Access from any device

2. **Bulk Upload**
   - Upload 10+ images at once
   - Progress indicator shows upload status
   - Automatic organization in Firebase

3. **Two Ways to Add Images**
   - **Upload from Device**: Camera/gallery photos
   - **Choose from Library**: Previously saved items

4. **Library Management**
   - View all saved clothing items
   - Select multiple items at once
   - Delete unwanted images
   - Organized grid view

5. **Smart Features**
   - Automatic image type detection (shirt, pants, dress, etc.)
   - Firebase URLs work on deployed site
   - Images cached for fast loading

---

## 🔒 Security Best Practices

### For Development (Current Setup)
- ✅ Anyone can upload to test
- ✅ Easy to develop and debug
- ⚠️ Not secure for production

### For Production (Recommended)

1. **Enable Firebase Authentication**
   ```bash
   # In Firebase Console > Authentication > Get Started
   # Enable "Email/Password" or "Google" sign-in
   ```

2. **Update Storage Rules**
   ```javascript
   rules_version = '2';
   
   service firebase.storage {
     match /b/{bucket}/o {
       match /users/{userId}/{allPaths=**} {
         allow read: if request.auth != null;
         allow write: if request.auth != null && request.auth.uid == userId;
       }
     }
   }
   ```

3. **Implement User Authentication**
   - Add sign-up/login to your app
   - Pass actual user IDs to `uploadImageToFirebase(file, userId)`
   - Each user gets their own folder

---

## 📊 Usage Limits (Free Tier)

Firebase offers generous free limits:

- **Storage**: 5 GB total
- **Downloads**: 1 GB/day
- **Uploads**: 20,000/day
- **Operations**: 50,000/day

This is enough for:
- ~5,000 high-quality clothing images
- Thousands of users testing your app
- Unlimited development

---

## 🐛 Troubleshooting

### Issue: "Save to library" is grayed out

**Solution:**
1. Check `firebase.ts` has real values (not "YOUR_API_KEY")
2. Restart your dev server (`npm run dev`)
3. Clear browser cache (Ctrl+Shift+Delete)

### Issue: "Failed to upload to Firebase"

**Check:**
1. Storage is enabled in Firebase Console
2. Storage Rules are set correctly
3. Browser console (F12) for detailed error
4. Internet connection is stable

**Common Errors:**
- `storage/unauthorized`: Check storage rules
- `storage/unknown`: Check Firebase config values
- `Network error`: Check internet connection

### Issue: Images not showing in library

**Solution:**
1. Click refresh or reopen library
2. Check Firebase Console > Storage > Files
3. Ensure uploads completed (check console logs)
4. Verify `getLibraryImages()` is called

### Issue: "Firebase not initialized"

**Solution:**
1. Verify all 6 config values are correct
2. Check for typos in `firebase.ts`
3. Restart dev server
4. Check browser console for Firebase errors

---

## 📱 Deployment Notes

When deploying to Vercel/production:

1. **Environment Variables** (Optional, more secure):
   - Add Firebase config as environment variables
   - Update `firebase.ts` to read from `import.meta.env`

2. **Storage Rules**:
   - Update to production rules (see Security section)
   - Enable Firebase Authentication

3. **CORS Configuration**:
   - Firebase Storage should allow your domain
   - Usually auto-configured, but check if images don't load

---

## 🎓 Additional Resources

- **Firebase Docs**: https://firebase.google.com/docs/storage
- **Security Rules**: https://firebase.google.com/docs/storage/security
- **Best Practices**: https://firebase.google.com/docs/storage/best-practices

---

## ✅ Quick Checklist

Before considering setup complete:

- [ ] Firebase project created
- [ ] Storage enabled with rules configured
- [ ] Web app registered in Firebase
- [ ] Config values copied to `firebase.ts`
- [ ] "Save to library" toggle is enabled (not grayed)
- [ ] Test upload works (check Firebase Console > Storage)
- [ ] Library shows uploaded images
- [ ] Bulk upload works (multiple images)
- [ ] Can select and use library images
- [ ] Delete function works

---

## 🆘 Need Help?

If you're stuck:

1. **Check Browser Console** (F12 > Console tab)
   - Look for red errors
   - Check for Firebase-related messages

2. **Check Firebase Console**
   - Storage > Files: Are images uploading?
   - Storage > Rules: Are rules correct?

3. **Verify Configuration**
   - Double-check all 6 config values
   - No typos in domain names
   - Quotes and commas correct

---

**🎉 Once setup is complete, you'll have a fully functional cloud-based wardrobe library!**

Users can:
- Upload images from their phone camera
- Build a persistent wardrobe library
- Select from saved items anytime
- Access their library from any device
- Get AI outfit recommendations using saved items

Happy coding! 🚀

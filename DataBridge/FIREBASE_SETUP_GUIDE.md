# Firebase Setup Guide for Fashion-Style App

This guide will help you set up Firebase Storage to enable the Image Library feature in your Fashion-Style application.

## 🎯 What You'll Get

- **Cloud Storage**: Save uploaded clothing images to Firebase Storage
- **Image Library**: Access your saved images anytime across devices
- **Easy Management**: View, select, and delete images from your library

## 📋 Prerequisites

- A Google account
- Internet connection
- Your Fashion-Style app running locally

## 🚀 Step-by-Step Setup

### Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"** or **"Create a project"**
3. Enter a project name (e.g., "fashion-style-app")
4. (Optional) Enable Google Analytics
5. Click **"Create project"** and wait for it to finish

### Step 2: Enable Firebase Storage

1. In your Firebase project, click **"Build"** in the left sidebar
2. Click **"Storage"**
3. Click **"Get started"**
4. Choose **"Start in test mode"** (for development)
   ```
   rules_version = '2';
   service firebase.storage {
     match /b/{bucket}/o {
       match /{allPaths=**} {
         allow read, write: if request.time < timestamp.date(2025, 12, 31);
       }
     }
   }
   ```
5. Select a Cloud Storage location (choose closest to you)
6. Click **"Done"**

### Step 3: Register Your Web App

1. On the Firebase project overview page, click the **Web icon** (`</>`)
2. Give your app a nickname (e.g., "fashion-style-web")
3. (Optional) Check **"Also set up Firebase Hosting"**
4. Click **"Register app"**

### Step 4: Get Your Firebase Configuration

After registering, you'll see a code snippet like this:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyC1234567890abcdefghijklmnop",
  authDomain: "your-project-id.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project-id.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef1234567890"
};
```

**Copy these values** - you'll need them in the next step!

### Step 5: Update Your App Configuration

1. Open the file: `client/src/lib/firebase.ts`

2. Replace the placeholder values with your Firebase configuration:

```typescript
const firebaseConfig = {
  apiKey: "YOUR_ACTUAL_API_KEY_HERE",
  authDomain: "your-project-id.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project-id.appspot.com",
  messagingSenderId: "your-messaging-sender-id",
  appId: "your-app-id"
};
```

3. Save the file

### Step 6: Restart Your App

```bash
# Stop the dev server (Ctrl+C)
# Then restart it
npm run dev
```

## ✅ Test Your Setup

1. Go to http://localhost:5000
2. Navigate to the Upload step
3. You should now see:
   - ✅ "Save to library" toggle switch (enabled)
   - ✅ "My Library" button
4. Upload an image with "Save to library" ON
5. You should see "Saving..." badge while uploading
6. Click "My Library" to see your saved images

## 🔧 Troubleshooting

### "Firebase Storage not initialized" error

**Solution**: Make sure you've replaced ALL placeholder values in `firebase.ts` with your actual Firebase credentials.

### Images not appearing in library

**Possible causes**:
1. Check Firebase Console → Storage to see if files are being uploaded
2. Verify Storage Rules allow read/write access
3. Check browser console for error messages

### CORS errors when loading images

**Solution**: In Firebase Console → Storage → Rules, ensure you have proper CORS configuration:

```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read, write: if true; // For development only!
    }
  }
}
```

### "Save to library" toggle is disabled

**Solution**: This means Firebase is not properly configured. Double-check your `firebase.ts` configuration values.

## 🔒 Security Notes (Production)

⚠️ **Important**: The current setup uses test mode rules for development. Before deploying to production:

1. **Add Authentication**: Implement Firebase Authentication
2. **Secure Storage Rules**:
   ```
   rules_version = '2';
   service firebase.storage {
     match /b/{bucket}/o {
       match /users/{userId}/{allPaths=**} {
         allow read, write: if request.auth != null && request.auth.uid == userId;
       }
     }
   }
   ```
3. **Add Security Validations**: Validate file types, sizes, etc.
4. **Monitor Usage**: Set up billing alerts and quotas

## 📊 Firebase Storage Structure

Your images will be organized like this:

```
storage/
└── users/
    └── default/
        └── clothing/
            ├── 1234567890_shirt-blue.jpg
            ├── 1234567891_pants-black.jpg
            └── ...
```

To implement user-specific folders, integrate Firebase Authentication and pass the user ID when uploading.

## 💰 Pricing

Firebase offers a generous free tier:
- **Storage**: 5 GB free
- **Downloads**: 1 GB/day free
- **Uploads**: 20k/day free

Perfect for development and small-scale production! [View pricing](https://firebase.google.com/pricing)

## 🎉 Features You Now Have

✅ **Cloud Storage**: Images saved to Google Cloud  
✅ **Library Management**: View all your saved images  
✅ **Quick Selection**: Select multiple images from library  
✅ **Delete Images**: Remove unwanted images  
✅ **Cross-Device**: Access your library from any device  
✅ **Automatic Upload**: Toggle to auto-save new uploads  

## 📚 Next Steps

1. **Add Authentication**: Use Firebase Auth for user accounts
2. **Add Metadata**: Store clothing type, color, brand with images
3. **Add Sharing**: Share your wardrobe with friends
4. **Add Tags**: Categorize images with custom tags
5. **Add Search**: Search your library by color, type, etc.

## 🆘 Need Help?

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firebase Storage Guide](https://firebase.google.com/docs/storage)
- [Firebase Console](https://console.firebase.google.com/)

---

**Happy Styling! 👔👗**

// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-app.js";
import {
    getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword,
    GoogleAuthProvider, signInWithPopup, signOut as firebaseSignOut, sendPasswordResetEmail,
    onAuthStateChanged, updateProfile
} from "https://www.gstatic.com/firebasejs/9.22.0/firebase-auth.js";

// Your web app's Firebase configuration
export const firebaseConfig = {
    apiKey: "AIzaSyCR-BtwT7VCq6V4VBQsPFbMqEOrTfvD1E4",
    authDomain: "personalized-recipe-recommend.firebaseapp.com",
    databaseURL: "https://personalized-recipe-recommend-default-rtdb.firebaseio.com",
    projectId: "personalized-recipe-recommend",
    storageBucket: "personalized-recipe-recommend.firebasestorage.app",
    messagingSenderId: "582805547601",
    appId: "1:582805547601:web:8d908f094d07626fe0e670"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication
const auth = getAuth(app);

// Function to update UI based on authentication state
function updateAuthUI(user) {
    const authLinks = document.querySelector('.auth-links');
    const userProfile = document.querySelector('.user-profile');

    if (user) {
        // User is signed in
        if (authLinks) authLinks.style.display = 'none';
        if (userProfile) {
            userProfile.style.display = 'flex';
            userProfile.querySelector('.user-name').textContent = user.displayName || user.email;
            userProfile.querySelector('.user-avatar').src = user.photoURL || 'https://via.placeholder.com/40';
        }
    } else {
        // User is signed out
        if (authLinks) authLinks.style.display = 'flex';
        if (userProfile) userProfile.style.display = 'none';
    }
}

// Authentication state observer
onAuthStateChanged(auth, (user) => {
    if (user) {
        // User is signed in
        updateAuthUI(user);
    } else {
        // User is signed out
        updateAuthUI(null);
    }
});

// Sign up with email and password
async function signUp(email, password, displayName) {
    try {
        // Create user with email and password
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;

        // Update user profile with display name
        if (displayName) {
            await updateProfile(user, {
                displayName: displayName
            });
        }

        console.log('User created successfully:', user);
        return user;
    } catch (error) {
        console.error('Sign up error:', error);
        // Handle specific error cases
        if (error.code === 'auth/email-already-in-use') {
            throw new Error('This email is already registered. Please sign in instead.');
        } else if (error.code === 'auth/invalid-email') {
            throw new Error('Please enter a valid email address.');
        } else if (error.code === 'auth/weak-password') {
            throw new Error('Password should be at least 6 characters long.');
        } else {
            throw error;
        }
    }
}

// Sign in with email and password
async function signIn(email, password) {
    try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        return userCredential.user;
    } catch (error) {
        console.error('Sign in error:', error);
        throw error;
    }
}

// Sign in with Google
async function signInWithGoogle() {
    try {
        const provider = new GoogleAuthProvider();
        // Add scopes for Google Sign-In
        provider.addScope('https://www.googleapis.com/auth/userinfo.email');
        provider.addScope('https://www.googleapis.com/auth/userinfo.profile');

        // Set custom parameters
        provider.setCustomParameters({
            prompt: 'select_account',
            login_hint: ''
        });

        // Sign in with popup
        const result = await signInWithPopup(auth, provider);

        // Get the user's profile information
        const user = result.user;
        const credential = GoogleAuthProvider.credentialFromResult(result);
        const token = credential.accessToken;

        console.log('Google Sign-In successful:', user);
        return user;
    } catch (error) {
        console.error('Google sign in error:', error);
        // Handle specific error cases
        if (error.code === 'auth/popup-closed-by-user') {
            throw new Error('Sign in was cancelled');
        } else if (error.code === 'auth/popup-blocked') {
            throw new Error('Popup was blocked by the browser. Please allow popups for this site.');
        } else if (error.code === 'auth/cancelled-popup-request') {
            throw new Error('Another sign in attempt is in progress');
        } else {
            throw error;
        }
    }
}

// Sign out
async function signOut() {
    try {
        await firebaseSignOut(auth);
        // Redirect to homepage after successful sign out
        window.location.href = 'index.html';
    } catch (error) {
        console.error('Sign out error:', error);
        throw error;
    }
}

// Reset password
async function resetPassword(email) {
    try {
        await sendPasswordResetEmail(auth, email);
    } catch (error) {
        console.error('Password reset error:', error);
        throw error;
    }
}

// Export functions
export const authFunctions = {
    signUp,
    signIn,
    signInWithGoogle,
    signOut,
    resetPassword
}; 
import { auth } from "@/firebase/firebaseConfig"
import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    sendPasswordResetEmail,
    updateProfile,
    User,
} from "firebase/auth";

// Sign Up with Email and Password
export const signUp = async (email: string, password: string) => {
    try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        return userCredential.user;
    } catch (error) {
        console.error("Error signing up:", error);
        throw error;
    }
};

// Sign In with email and password
export const signIn = async (email: string, password: string) => {
    try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        return userCredential.user;
    } catch (error) {
        console.error("Error signing in:", error);
        throw error;
    }
};

// Sign Out
export const logOut = async () => {
    try {
        await signOut(auth);
    } catch (error) {
        console.error("Error signing out:", error);
        throw error;
    }
};


// Reset Password
export const resetPassword = async (email: string) => {
    try {
        await sendPasswordResetEmail(auth, email);
        console.log("Password reset email sent");
    } catch (error) {
        console.error("Error resetting password:", error);
        throw error;
    }
};

// Update User Profile
export const updateUserProfile = async (user: User, displayName: string, photoURL: string) => {
    try {
        await updateProfile(user, { displayName, photoURL });
        console.log("User profile updated");
    } catch (error) {
        console.error("Error updating profile:", error);
        throw error;
    }
};

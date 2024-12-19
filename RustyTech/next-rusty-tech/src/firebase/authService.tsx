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
export const handleSignUp = async (email: string, password: string) => {
    try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        return userCredential.user;
    } catch (error) {
        console.error("Error signing up:", error);
        throw error;
    }
};

// Sign In with email and password
export const handleSignIn = async (email: string, password: string) => {
    try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        return userCredential.user;
    } catch (error) {
        console.error("Error signing in:", error);
        throw error;
    }
};

// Sign Out
export const handleLogout = async () => {
    try {
        await signOut(auth);
    } catch (error) {
        console.error("Error signing out:", error);
        throw error;
    }
};

// Reset Password
export const handleResetPassword = async (email: string) => {
    try {
        await sendPasswordResetEmail(auth, email);
        console.log("Password reset email sent");
    } catch (error) {
        console.error("Error resetting password:", error);
        throw error;
    }
};

// Update User Profile
export const handleUpdateUserProfile = async (user: User, profile: { displayName?: string; photoURL?: string }) => {
    try {
        await updateProfile(user, profile);
        console.log("User profile updated");
    } catch (error) {
        console.error("Error updating profile:", error);
        throw error;
    }
};

import { auth } from "@/firebase/firebaseConfig";
import { signInWithEmailAndPassword, UserCredential } from "firebase/auth";

export const loginUser = async (email: string, password: string): Promise<UserCredential> => {
  const userCredential = await signInWithEmailAndPassword(auth, email, password);
  return userCredential;
};
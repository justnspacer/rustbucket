import type { NextApiRequest, NextApiResponse } from 'next';
import { signIn } from '@/firebase/authService';
import { signInWithEmailAndPassword } from 'firebase/auth';
import {auth} from "@/firebase/firebaseConfig";



export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const { username, password } = req.body;
    try {
      const userCredential  = await signInWithEmailAndPassword(auth, username, password);
      res.status(200).json({ message: 'Logged in', user: userCredential.user });
    } catch (error) {
      console.error(error);
      res.status(500).json({ message: 'An error occurred' });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
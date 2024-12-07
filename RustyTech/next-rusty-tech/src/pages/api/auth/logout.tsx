import type { NextApiRequest, NextApiResponse } from 'next';
import { logOut } from '@/firebase/authService';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    try {
      await logOut();
      res.status(200).json({ message: 'User signed out successfully' });
    } catch (error) {
      res.status(500).json({ error: 'Error signing out' });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
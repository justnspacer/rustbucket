"use client";
import React, { useEffect, useState } from 'react';
import { useAuth } from '@/app/context/AuthContext';
import { useRouter } from 'next/navigation';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircleRight } from '@fortawesome/free-solid-svg-icons';


export default function Login() {
  const { user, login, success, error } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();


  useEffect(() => {
    if (user) {
      router.push('/');
    }
  }, [user, router]);

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    await login(username, password);
  };


  return (
    <div className="form-container">
    <h1 className="form-title">Login</h1>
    <form onSubmit={handleLogin}>
      <input
        type="email"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button type="submit">Sign in</button>
    </form>
    

    <a className='reset-password-link' href="/auth/resetPassword">Reset Password</a>
    <div className="mt-2">
    <span className="register-text">Don't have an account? </span>
    <a className="register-link" href="/auth/register">Register<FontAwesomeIcon icon={faCircleRight}/></a>
    </div>
    {error && <p style={{ color: "red" }}>{error}</p>}
    {success && <p style={{ color: "green" }}>{success}</p>}
    </div>

  );
}
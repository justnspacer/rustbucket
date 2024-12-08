"use client";
import React, { useState } from 'react';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      if (validatePasswords()) {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
        });
        
        if (!response.ok) {
          const data = await response.json();
          console.log(data.error);
          throw new Error("Login failed");
        }
        const data = await response.json();
        setSuccess(data.message);
        console.log("Logged in user:", data.user);
      }
    } catch (e) {
      if (e instanceof Error) {
        setError(e.message);
      } else {
        setError("An unknown error occurred");
      }
      console.error(e);
    }
  };

  
  const validatePasswords = () => {
    if (password === "") {
      setError("Password required");
      return false;
    }
    if(password.length < 6) {
      setError("Password must be at least 6 characters");
      return false;
    }
    if(password.length > 4096) {
      setError("Password must be less characters");
      return false;
    }
    if (!/[A-Z]/.test(password)) {
      setError("Password must contain at least one uppercase letter");
      return false;
    }
    if (!/[a-z]/.test(password)) {
      setError("Password must contain at least one lowercase letter");
      return false;
    }
    if (!/[0-9]/.test(password)) {
      setError("Password must contain at least one number");
      return false;
    }
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      setError("Password must contain at least one special character");
      return false;
    }
    return true;
  };


  return (
    <div>
    <h1>Login</h1>
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
    {error && <p style={{ color: "red" }}>{error}</p>}
    {success && <p style={{ color: "green" }}>{success}</p>}
    </div>

  );
}
"use client";
import { useState } from "react";
import { useAuth } from "@/app/context/AuthContext";

const PasswordResetForm = () => {
  const { resetPassword, loading } = useAuth();
  const [email, setEmail] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await resetPassword(email);
      setSuccess(true);
    } catch (error) {
      setError("Failed to send password reset email. Please try again.");
    }
  };

  return (
    <div>
      <h1 className="form-title">Reset Password</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <input placeholder="Email"
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={loading}
          />
        </div>
        {error && <p>{error}</p>}
        {success && <p>Password reset email sent!</p>}
        <button type="submit" disabled={loading}>
          {loading ? "Sending..." : "Send Password Reset Email"}
        </button>
      </form>
    </div>
    
  );
};

export default PasswordResetForm;
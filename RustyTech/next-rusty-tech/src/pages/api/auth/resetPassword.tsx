import { resetPassword } from "@/firebase/authService";
import { useState } from "react";


export default function ResetPassword() {
  const [email, setEmail] = useState('');

  const handleResetPassword = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      await resetPassword(email);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleResetPassword}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <button type="submit">Reset Password</button>
    </form>
  );
}
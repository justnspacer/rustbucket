"use client";
import PasswordResetForm from "@/components/PasswordResetForm";

const ResetPasswordPage = () => {
  return (
    <div>
      <h1>Please enter your email address to reset your password:</h1>
      <PasswordResetForm />
    </div>
  );
};

export default ResetPasswordPage;
"use client";
import { useAuth } from "@/app/context/AuthContext";

const HomePageMessage = () => {

  return (
    <div className="homepage-message">
      <h1 className="homepage-header">Welcome to Rust Bucket</h1>
      <p className="homepage-description">Let's work together to bring your vision to life on the web!</p>
    </div>
  );
};

export default HomePageMessage;
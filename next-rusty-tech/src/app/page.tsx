"use client";
import { useEffect } from "react";
import { useRouter } from 'next/navigation';


const Landing = () => {
  const router = useRouter();

  useEffect(() => {
    // address any issues with this redirect in the future maybe
    router.push("/home");
  }, [router]);

  return null;
};

export default Landing;
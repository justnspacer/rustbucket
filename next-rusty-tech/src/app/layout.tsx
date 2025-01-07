import localFont from "next/font/local";
import "@/styles/globals.css";
import { AuthProvider } from "@/app/context/AuthContext";
import NavBar from "@/components/NavBar";

const fredoka  = localFont({
  src: "./fonts/Fredoka-VariableFont_wdth,wght.ttf",
  variable: '--font-fredoka',
}); 

export const metadata = {
  title: "Rust Bucket",
  description: "Let's work together to bring your vision to the web!",
};

export default function Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${fredoka.variable} antialiased`}
      >
        <AuthProvider>
          <NavBar />
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}

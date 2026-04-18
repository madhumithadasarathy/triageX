import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "TriageX — AI-Powered Medical Triage",
  description: "Intelligent symptom assessment with visual explanations. Get instant severity evaluation and personalized guidance. Explain. Assess. Act.",
  keywords: ["medical triage", "AI health", "symptom checker", "triage assistant"],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased`}>
        <Navbar />
        <main className="min-h-screen">{children}</main>
      </body>
    </html>
  );
}

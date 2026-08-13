import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AVERON — The Programmable Digital Asset Infrastructure",
  description:
    "A programmable financial ecosystem where real-world assets, AI, blockchain, and capital markets converge. By Rishabh Gupta.",
  keywords: [
    "Averon",
    "RWA",
    "tokenization",
    "blockchain",
    "digital assets",
    "Rishabh Gupta",
    "asset-backed financing",
    "capital mobility",
  ],
  authors: [{ name: "Rishabh Gupta" }],
  openGraph: {
    title: "AVERON — The Programmable Digital Asset Infrastructure",
    description:
      "Read Averon: The Programmable Digital Asset Infrastructure by Rishabh Gupta. A technical reference for the Averon Protocol.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-[#050505] text-white`}
      >
        {children}
      </body>
    </html>
  );
}

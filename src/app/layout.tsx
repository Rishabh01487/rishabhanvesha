import type { Metadata } from "next";
import { Caveat, Cormorant_Garamond, Inter } from "next/font/google";
import "./globals.css";

const caveat = Caveat({
  variable: "--font-caveat",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

const serif = Cormorant_Garamond({
  variable: "--font-serif",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  style: ["normal", "italic"],
});

const sans = Inter({
  variable: "--font-geist-sans",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600"],
});

export const metadata: Metadata = {
  title: "AVERON — The Programmable Digital Asset Infrastructure",
  description:
    "A programmable financial ecosystem where real-world assets, AI, blockchain, and capital markets converge. By Rishabh Gupta.",
  keywords: [
    "Averon", "RWA", "tokenization", "blockchain", "digital assets",
    "Rishabh Gupta", "asset-backed financing", "capital mobility",
  ],
  authors: [{ name: "Rishabh Gupta" }],
  openGraph: {
    title: "AVERON — The Programmable Digital Asset Infrastructure",
    description: "Read Averon: The Programmable Digital Asset Infrastructure by Rishabh Gupta.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <body
        className={`${caveat.variable} ${serif.variable} ${sans.variable} antialiased bg-[#050505] text-white`}
      >
        {children}
      </body>
    </html>
  );
}

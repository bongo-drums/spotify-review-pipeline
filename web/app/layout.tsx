import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Spotify review insights",
  description: "Classified app reviews, ranked issues and a grounded recommendation, served from the pipeline database.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

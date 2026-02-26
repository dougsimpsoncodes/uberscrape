import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "UberScrape - AI Web Scraping",
  description: "Extract structured data from any website using AI",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}

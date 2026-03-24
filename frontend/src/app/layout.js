import { Inter } from "next/font/google";
import { ClerkProvider } from '@clerk/nextjs'
import { ThemeProvider } from '@/context/ThemeContext'
import { DocumentProvider } from '@/context/DocumentContext'
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata = {
  title: "Apricity  Startup Workspace",
  description: "A place to think about your startup",
};

export default function RootLayout({ children }) {
  return (
    <ClerkProvider>
      <html lang="en" suppressHydrationWarning>
        <body className={`${inter.variable} antialiased`}>
          <ThemeProvider>
            <DocumentProvider>
              {children}
            </DocumentProvider>
          </ThemeProvider>
        </body>
      </html>
    </ClerkProvider>
  );
}

'use client'

import Link from "next/link";
import { ArrowRight, Sparkles, Target, Zap, Sun, Moon } from "lucide-react";
import { useAuth } from "@clerk/nextjs";
import { useTheme } from '@/context/ThemeContext';

export default function LandingPage() {
  const { userId } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="flex min-h-screen flex-col bg-surface text-secondary">
      {/* Navigation */}
      <header className="flex h-16 items-center justify-between border-b border-border-subtle px-6 md:px-12 lg:px-24">
        <div className="flex items-center gap-1.5 text-base font-bold text-primary">
          <span>🍊</span>
          <span>Apricity</span>
        </div>
        <div className="flex items-center gap-4">
          <button
            onClick={toggleTheme}
            className="p-1.5 mr-2 text-secondary hover:text-primary rounded-md hover:bg-surface transition-colors"
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>
          {userId ? (
            <Link href="/dashboard" className="flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-main transition-colors hover:bg-secondary">
              Go to Dashboard
            </Link>
          ) : (
            <>
              <Link href="/sign-in" className="flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-surface hover:text-primary">
                Sign In
              </Link>
              <Link href="/sign-up" className="flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-main transition-colors hover:bg-secondary">
                Get Started
              </Link>
            </>
          )}
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1">
        <section className="flex flex-col items-center justify-center px-4 py-24 text-center md:py-32">
          <div className="mb-4 inline-flex items-center rounded-full border border-border-subtle bg-main px-3 py-1 text-xs font-semibold uppercase tracking-wider text-accent-primary">
            Powered by Multi-Agent AI
          </div>
          <h1 className="mb-6 max-w-4xl text-4xl font-extrabold tracking-tight text-primary md:text-6xl lg:text-7xl">
            Predict Your Startup's <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent-primary to-accent-secondary">Success</span>
          </h1>
          <p className="mb-10 max-w-2xl text-lg text-faint md:text-xl">
            Analyze your business idea from multiple perspectives—Financial, VC, Technical, and Marketing—all driven by specialized AI agents.
          </p>
          <div className="flex flex-col gap-4 sm:flex-row">
            <Link href={userId ? "/dashboard" : "/sign-up"} className="group flex items-center justify-center gap-2 rounded-lg bg-primary px-8 py-4 text-base font-medium text-main transition-all hover:bg-secondary hover:shadow-lg hover:-translate-y-0.5">
              {userId ? "Go to Dashboard" : "Analyze My Idea"}
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
            </Link>
          </div>
        </section>

        {/* Features Preview */}
        <section className="bg-main py-20">
          <div className="mx-auto max-w-6xl px-6 lg:px-8">
            <div className="grid gap-12 md:grid-cols-3 text-left">
              <div className="flex flex-col gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-surface border border-border-subtle text-accent-primary">
                  <Target className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold text-primary">Comprehensive Analysis</h3>
                <p className="text-faint">Evaluate product-market fit, competitor landscape, and technical feasibility instantly.</p>
              </div>
              <div className="flex flex-col gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-surface border border-border-subtle text-accent-primary">
                  <Zap className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold text-primary">Automated Pitch Generation</h3>
                <p className="text-faint">Automatically generate an executive summary, VC pitch deck, and detailed financial models.</p>
              </div>
              <div className="flex flex-col gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-surface border border-border-subtle text-accent-primary">
                  <Sparkles className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold text-primary">Intelligent Memory</h3>
                <p className="text-faint">Build upon your past reports and seamlessly refine your startup model over time.</p>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-border-subtle bg-surface py-8 text-center text-sm text-faint">
        <p>© {new Date().getFullYear()} Apricity. All rights reserved.</p>
      </footer>
    </div>
  );
}

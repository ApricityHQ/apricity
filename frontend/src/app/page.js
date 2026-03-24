'use client'

import Link from "next/link";
import { ArrowRight, Sparkles, Target, Zap, Sun, Moon, BarChart3, Presentation, BrainCircuit, Activity } from "lucide-react";
import { useAuth } from "@clerk/nextjs";
import { useTheme } from '@/context/ThemeContext';
import { motion } from "framer-motion";

export default function LandingPage() {
  const { userId } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="flex min-h-screen flex-col bg-main text-primary relative overflow-hidden">
      {/* Background Glows */}
      <div className="absolute top-0 inset-x-0 h-96 bg-gradient-to-b from-accent-primary/10 to-transparent pointer-events-none" />
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-3xl h-64 bg-accent-primary/5 blur-[100px] pointer-events-none rounded-full" />

      {/* Navigation */}
      <header className="flex h-16 items-center justify-between border-b border-border-subtle/50 px-6 md:px-12 lg:px-24 bg-surface/50 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-2 text-lg font-bold text-primary tracking-tight">
          <span className="bg-accent-primary text-white p-1 rounded-md text-sm">🍊</span>
          <span>Apricity</span>
        </div>
        <div className="flex items-center gap-4">
          <button
            onClick={toggleTheme}
            className="p-2 text-secondary hover:text-primary rounded-full hover:bg-surface transition-all"
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>
          {userId ? (
            <Link href="/dashboard" className="flex items-center justify-center rounded-full bg-primary px-5 py-2 text-sm font-medium text-main transition-all hover:bg-secondary hover:scale-105 active:scale-95 shadow-sm">
              Dashboard
            </Link>
          ) : (
            <>
              <Link href="/sign-in" className="hidden sm:flex items-center justify-center rounded-full px-5 py-2 text-sm font-medium transition-colors hover:text-accent-primary">
                Sign In
              </Link>
              <Link href="/sign-up" className="flex items-center justify-center rounded-full bg-primary px-5 py-2 text-sm font-medium text-main transition-all hover:bg-secondary hover:scale-105 active:scale-95 shadow-sm">
                Get Started
              </Link>
            </>
          )}
        </div>
      </header>

      <main className="flex-1 w-full relative z-10">
        {/* Interactive Hero Section */}
        <section className="flex flex-col items-center justify-center px-4 pt-32 pb-24 text-center md:pt-40 md:pb-32">
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, ease: "easeOut" }}
            className="mb-8 inline-flex items-center gap-2 rounded-full border border-border-subtle bg-surface/50 backdrop-blur-sm px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-accent-primary shadow-sm"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Apricity AI Engine 2.0</span>
          </motion.div>
          
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="mb-8 max-w-5xl text-5xl font-extrabold tracking-tight text-primary md:text-7xl lg:text-8xl leading-tight"
          >
            Predict Your Startup's <br className="hidden md:block"/>
            <span className="text-transparent bg-clip-text bg-gradient-to-br from-accent-primary via-orange-400 to-amber-300">
              Future Success.
            </span>
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="mb-12 max-w-2xl text-lg text-secondary md:text-xl font-medium leading-relaxed"
          >
            Analyze your business idea from multiple perspectives—Financial, VC, Technical, and Marketing—all driven by specialized AI agents acting as your ultimate co-founder.
          </motion.p>
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex flex-col gap-4 sm:flex-row"
          >
            <Link href={userId ? "/dashboard" : "/sign-up"} className="group relative flex items-center justify-center gap-2 rounded-full overflow-hidden bg-primary px-8 py-4 text-base font-medium text-main transition-all hover:scale-105 active:scale-95 shadow-xl hover:shadow-accent-primary/20">
              <span className="relative z-10 flex items-center gap-2">
                {userId ? "Go to Dashboard" : "Start Free Analysis"}
                <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </span>
              <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-in-out" />
            </Link>
          </motion.div>

          {/* Abstract UI Preview (Linear/Lovable style) */}
          <motion.div 
             initial={{ opacity: 0, y: 40 }}
             animate={{ opacity: 1, y: 0 }}
             transition={{ duration: 0.8, delay: 0.4 }}
             className="mt-24 w-full max-w-5xl mx-auto rounded-xl border border-border-subtle/50 bg-surface/30 backdrop-blur-xl shadow-2xl overflow-hidden"
          >
            {/* Window header */}
            <div className="h-10 border-b border-border-subtle/50 bg-surface/50 flex items-center px-4 gap-2">
              <div className="w-3 h-3 rounded-full bg-red-400/80" />
              <div className="w-3 h-3 rounded-full bg-amber-400/80" />
              <div className="w-3 h-3 rounded-full bg-accent-success/80" />
            </div>
            {/* Window Body */}
            <div className="p-8 aspect-video flex flex-col items-center justify-center bg-gradient-to-tr from-surface/20 to-surface/5 relative">
                <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
                <div className="z-10 flex flex-col items-center gap-6">
                   <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-accent-primary to-amber-400 flex items-center justify-center shadow-lg shadow-accent-primary/20 animate-pulse">
                     <BrainCircuit className="w-8 h-8 text-white" />
                   </div>
                   <div className="space-y-3 w-64 text-center">
                     <div className="h-3 w-full bg-border-subtle rounded-full overflow-hidden">
                       <div className="h-full bg-accent-primary w-3/4" />
                     </div>
                     <p className="text-xs text-secondary font-mono">Analyzing Market Metrics...</p>
                   </div>
                </div>
            </div>
          </motion.div>
        </section>

        {/* Social Proof Section */}
        <section className="border-y border-border-subtle/30 bg-surface/20 py-10">
          <div className="mx-auto max-w-7xl px-6 flex justify-center items-center gap-12 flex-wrap opacity-50 grayscale hover:grayscale-0 transition-all duration-500 cursor-default">
             <div className="text-sm font-bold tracking-widest text-secondary flex items-center gap-2">
               <span className="w-6 h-6 rounded-md bg-secondary/20 flex items-center justify-center text-xs">❖</span>
               ACME CORP
             </div>
             <div className="text-sm font-bold tracking-widest text-secondary flex items-center gap-2">
               <span className="w-6 h-6 rounded-full border-2 border-secondary/20 flex items-center justify-center text-[10px]">◎</span>
               ZEPHYR
             </div>
             <div className="text-sm font-bold tracking-widest text-secondary flex items-center gap-2">
               <span className="w-6 h-6 bg-secondary/20 flex items-center justify-center rotate-45 scale-75 text-[10px]">◆</span>
               NOVARIS
             </div>
             <div className="text-sm font-bold tracking-widest text-secondary flex items-center gap-2">
               <span className="text-lg font-serif">A</span>
               AETHER INC
             </div>
          </div>
        </section>

        {/* Features Bento Grid */}
        <section className="py-24 relative">
          <div className="mx-auto max-w-6xl px-6 lg:px-8">
            <div className="mb-16 text-center">
              <h2 className="text-3xl font-bold tracking-tight text-primary sm:text-4xl md:text-5xl">
                Intelligence that <span className="text-accent-primary">Scales</span>
              </h2>
              <p className="mt-4 text-lg text-secondary">
                Everything you need to validate, build, and pitch your vision.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:auto-rows-[250px]">
              {/* Feature 1 - Large spanning */}
              <motion.div 
                whileHover={{ y: -5 }}
                className="md:col-span-2 md:row-span-2 rounded-3xl border border-border-subtle/50 bg-surface/40 backdrop-blur-sm p-8 flex flex-col relative overflow-hidden group min-h-[300px]"
              >
                <div className="absolute top-0 right-0 w-64 h-64 bg-accent-primary/10 rounded-full blur-3xl group-hover:bg-accent-primary/20 transition-all duration-500" />
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-main border border-border-subtle text-accent-primary mb-6 shadow-sm">
                  <Activity className="h-6 w-6" />
                </div>
                <h3 className="text-2xl font-bold text-primary mb-3">Comprehensive Analysis</h3>
                <p className="text-secondary mb-6 max-w-sm">Evaluate product-market fit, competitor landscape, and technical feasibility instantly with deep, data-driven insights.</p>
                
                {/* Visual abstract for graph */}
                <div className="mt-auto rounded-xl border border-border-subtle bg-main/50 p-4 w-full h-32 flex items-end gap-2 overflow-hidden opacity-80 group-hover:opacity-100 transition-opacity">
                   {[40, 70, 45, 90, 65, 85, 100].map((h, i) => (
                     <div key={i} className="flex-1 bg-accent-primary/20 rounded-t-sm transition-all duration-500 group-hover:bg-accent-primary/40" style={{ height: `${h}%` }}>
                       <div className="w-full h-1 bg-accent-primary mb-1 rounded-t-sm" />
                     </div>
                   ))}
                </div>
              </motion.div>

              {/* Feature 2 */}
              <motion.div 
                whileHover={{ y: -5 }}
                className="rounded-3xl border border-border-subtle/50 bg-surface/40 backdrop-blur-sm p-8 flex flex-col group relative overflow-hidden min-h-[200px]"
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-main border border-border-subtle text-accent-success mb-6 shadow-sm transition-transform group-hover:scale-110">
                  <Presentation className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold text-primary mb-2">Automated Pitch Generation</h3>
                <p className="text-secondary text-sm">Automatically generate an executive summary, VC pitch deck, and detailed financial models ready for investors.</p>
              </motion.div>

              {/* Feature 3 */}
              <motion.div 
                whileHover={{ y: -5 }}
                className="rounded-3xl border border-border-subtle/50 bg-main p-8 flex flex-col group relative overflow-hidden min-h-[200px]"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-accent-primary/5 to-transparent pointer-events-none" />
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-surface border border-border-subtle text-accent-warning mb-6 shadow-sm transition-transform group-hover:rotate-12">
                  <Sparkles className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold text-primary mb-2">Intelligent Memory</h3>
                <p className="text-secondary text-sm">Build upon your past reports and seamlessly refine your startup model over time with contextual AI agents.</p>
              </motion.div>
              
              {/* Feature 4 - Bottom Width */}
              <motion.div 
                whileHover={{ y: -5 }}
                className="md:col-span-3 rounded-3xl border border-border-subtle/50 bg-surface/40 backdrop-blur-sm p-8 flex items-center justify-between group overflow-hidden"
              >
                <div className="max-w-xl">
                    <h3 className="text-2xl font-bold text-primary mb-3">Your AI Co-Founder Awaits</h3>
                    <p className="text-secondary">Stop guessing. Get clear, actionable roadmaps tailored specifically to your exact niche and business model.</p>
                </div>
                <div className="hidden md:flex items-center justify-center h-24 w-24 rounded-full bg-main border border-border-subtle shadow-xl text-primary group-hover:text-accent-primary group-hover:border-accent-primary/50 transition-colors">
                    <ArrowRight className="h-8 w-8" />
                </div>
              </motion.div>
            </div>
          </div>
        </section>
        
        {/* Bottom CTA */}
        <section className="py-24 relative overflow-hidden">
          <div className="absolute inset-0 bg-accent-primary/5 skew-y-3 transform origin-bottom-left pointer-events-none" />
          <div className="mx-auto max-w-4xl px-6 relative z-10 text-center">
            <h2 className="text-4xl font-bold tracking-tight text-primary mb-6">
              Ready to build the next big thing?
            </h2>
            <p className="text-xl text-secondary mb-10 max-w-2xl mx-auto">
              Join founders who are already using Apricity to architect success. Get your comprehensive analysis in minutes.
            </p>
            <Link href={userId ? "/dashboard" : "/sign-up"} className="inline-flex items-center justify-center rounded-full bg-primary px-10 py-5 text-lg font-bold text-main transition-all hover:bg-secondary hover:scale-105 active:scale-95 shadow-2xl shadow-primary/20 group">
              {userId ? "Enter Workspace" : "Get Started for Free"}
              <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
            </Link>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-border-subtle/50 bg-main py-12 relative z-10">
        <div className="mx-auto max-w-7xl px-6 md:flex md:items-center md:justify-between">
          <div className="flex justify-center flex-col md:flex-row md:justify-start items-center space-x-6 md:order-2">
            <Link href="#" className="text-faint hover:text-primary transition-colors">Twitter</Link>
            <Link href="#" className="text-faint hover:text-primary transition-colors">GitHub</Link>
            <Link href="#" className="text-faint hover:text-primary transition-colors">Documentation</Link>
          </div>
          <div className="mt-8 md:mt-0 md:order-1 flex items-center justify-center md:justify-start gap-2">
            <span className="text-faint text-sm">© {new Date().getFullYear()} Apricity Platform.</span>
            <div className="w-1.5 h-1.5 rounded-full bg-accent-success animate-pulse" />
            <span className="text-accent-success text-xs font-mono">All systems operational</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

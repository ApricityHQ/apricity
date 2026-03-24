'use client'

import { useAuth, useUser, UserProfile, UserButton } from '@clerk/nextjs'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useDocument } from '@/context/DocumentContext'
import { useTheme } from '@/context/ThemeContext'
import { 
  Sparkles, FileText, Plus, Target, Presentation, 
  LayoutDashboard, FolderOpen, Blocks, Settings,
  Search, ArrowRight, Clock, Sun, Moon, Zap
} from 'lucide-react'
import { useEffect, useState } from 'react'

export default function Dashboard() {
  const { isSignedIn, isLoaded: authLoaded } = useAuth()
  const { user } = useUser()
  const router = useRouter()
  const { views } = useDocument()
  const { theme, toggleTheme } = useTheme()
  
  const [activeTab, setActiveTab] = useState('overview')
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    if (authLoaded && !isSignedIn) {
      router.push('/')
    }
  }, [authLoaded, isSignedIn, router])

  if (!authLoaded || !isSignedIn) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-surface">
        <Sparkles className="animate-pulse w-8 h-8 text-secondary" />
      </div>
    )
  }

  // Data processing
  const allReports = Object.values(views || {})
    .filter(view => view.status === 'completed')
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))

  const filteredReports = allReports.filter(report => 
    (report.content || '').toLowerCase().includes(searchQuery.toLowerCase())
  )

  const recentReports = allReports.slice(0, 3)

  const TABS = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'projects', label: 'Projects', icon: FolderOpen },
    { id: 'templates', label: 'Templates', icon: Blocks },
    { id: 'settings', label: 'Settings', icon: Settings },
  ]

  return (
    <div className="flex min-h-screen bg-surface">
      {/* Sidebar */}
      <aside className="w-64 border-r border-border-subtle bg-main flex flex-col hidden md:flex">
        <div className="h-16 flex items-center px-6 border-b border-border-subtle gap-2">
          {/* Apricity Branding */}
          <div className="flex items-center gap-1.5 text-base font-bold text-primary">
            <span>🍊</span>
            <span>Apricity</span>
          </div>
        </div>
        
        <div className="p-4 flex-1 flex flex-col gap-1">
          <div className="text-xs font-semibold text-faint uppercase tracking-wider mb-2 px-2 mt-4">Dashboard</div>
          {TABS.map(tab => {
            const Icon = tab.icon
            const isActive = activeTab === tab.id
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive 
                    ? 'bg-primary/10 text-accent-primary' 
                    : 'text-secondary hover:bg-surface hover:text-primary'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-accent-primary' : 'text-faint'}`} />
                {tab.label}
              </button>
            )
          })}
        </div>

        <div className="p-4 border-t border-border-subtle flex items-center justify-between">
          <div className="flex items-center gap-3 overflow-hidden">
             <UserButton afterSignOutUrl="/" showName={false} />
             <div className="flex flex-col overflow-hidden">
               <span className="text-sm font-medium text-primary truncate">{user?.firstName || 'User'}</span>
               <span className="text-xs text-faint truncate">{user?.primaryEmailAddress?.emailAddress}</span>
             </div>
          </div>
          <button
            onClick={toggleTheme}
            className="p-1.5 shrink-0 text-secondary hover:text-primary rounded-md hover:bg-surface transition-colors"
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col h-screen overflow-y-auto">
        {/* Mobile Header */}
        <header className="h-14 flex items-center justify-between border-b border-border-subtle bg-main px-4 md:hidden">
          <div className="flex items-center gap-1.5 text-base font-bold text-primary">
            <span>🍊</span>
            <span>Apricity</span>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={toggleTheme}
              className="p-1.5 text-secondary hover:text-primary rounded-md hover:bg-surface transition-colors"
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>
            <UserButton afterSignOutUrl="/" />
          </div>
        </header>

        <div className="flex-1 p-6 lg:p-10 max-w-6xl w-full mx-auto relative">

          {/* TAB: OVERVIEW */}
          {activeTab === 'overview' && (
            <div className="animate-in fade-in duration-300">
              <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
                <div>
                  <h1 className="text-3xl font-bold text-primary mb-1">Welcome back{user?.firstName ? `, ${user.firstName}` : ''} 👋</h1>
                  <p className="text-faint">Here's what's happening with your startup analyses today.</p>
                </div>
                <Link href="/workspace" className="flex items-center justify-center gap-2 px-6 py-2.5 bg-primary text-main rounded-md hover:bg-secondary transition-colors font-medium shadow-sm">
                  <Plus className="w-4 h-4" />
                  New Analysis
                </Link>
              </header>

              <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
                {/* Left Column (70%) */}
                <div className="xl:col-span-2 flex flex-col gap-6">
                  
                  {/* Usage Tracker & Stats */}
                  <div className="bg-main border border-border-subtle rounded-xl p-6 shadow-sm flex flex-col sm:flex-row gap-6 justify-between items-center relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-32 h-32 bg-accent-primary/5 rounded-bl-[100px] pointer-events-none" />
                    <div className="w-full sm:w-1/2">
                      <h3 className="text-sm font-medium text-secondary mb-1">Monthly Usage</h3>
                      <div className="flex items-end gap-2 mb-2">
                        <span className="text-3xl font-bold text-primary">{allReports.length}</span>
                        <span className="text-sm text-faint mb-1">/ 50 reports</span>
                      </div>
                      <div className="w-full h-2 bg-surface rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-accent-primary rounded-full transition-all duration-1000 ease-out"
                          style={{ width: `${Math.min((allReports.length / 50) * 100 + 1, 100)}%` }}
                        />
                      </div>
                    </div>
                    
                    <div className="flex gap-6 w-full sm:w-1/2 sm:justify-end border-t sm:border-t-0 sm:border-l border-border-subtle pt-6 sm:pt-0 sm:pl-6">
                      <div>
                        <h3 className="text-xs font-medium text-faint uppercase tracking-wider mb-1">Active Plan</h3>
                        <p className="text-lg font-bold text-primary">Free Tier</p>
                      </div>
                      <div>
                        <h3 className="text-xs font-medium text-faint uppercase tracking-wider mb-1">Status</h3>
                        <div className="flex items-center gap-1.5 mt-1">
                          <span className="w-2 h-2 rounded-full bg-accent-success shadow-[0_0_8px_rgba(16,185,129,0.5)] animate-pulse" />
                          <span className="text-sm font-medium text-primary">Operational</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* AI Recommendations */}
                  <div className="bg-gradient-to-r from-accent-primary/10 to-transparent border border-accent-primary/20 rounded-xl p-5 shadow-sm flex flex-col sm:flex-row items-start gap-4">
                    <div className="w-10 h-10 rounded-full bg-main flex items-center justify-center text-accent-primary shrink-0 shadow-sm border border-accent-primary/10">
                      <Sparkles className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-sm font-bold text-primary mb-1">Smart Suggestion</h3>
                      <p className="text-sm text-secondary mb-3">
                        {recentReports.length > 0 
                          ? "Based on your recent analysis, you might want to run a Competitive Landscape breakdown next to secure your market positioning."
                          : "Upload your startup's pitch deck to automatically generate a comprehensive technical and financial due-diligence report."}
                      </p>
                      <Link href="/workspace" className="text-xs font-semibold text-accent-primary hover:text-primary transition-colors flex items-center gap-1">
                        Start Workflow <ArrowRight className="w-3 h-3" />
                      </Link>
                    </div>
                  </div>

                  {/* Activity Feed */}
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <h2 className="text-lg font-semibold text-primary">Recent Activity</h2>
                      {allReports.length > 3 && (
                        <button onClick={() => setActiveTab('projects')} className="text-sm font-semibold text-secondary hover:text-primary transition-colors">
                          View all
                        </button>
                      )}
                    </div>

                    {recentReports.length === 0 ? (
                      <div className="bg-surface border border-border-subtle rounded-xl p-10 text-center border-dashed">
                        <div className="w-12 h-12 bg-main rounded-full flex items-center justify-center mx-auto mb-3 text-faint shadow-sm border border-border-subtle">
                          <FolderOpen className="w-5 h-5" />
                        </div>
                        <h3 className="text-base font-medium text-primary mb-1">No recent activity</h3>
                        <p className="text-sm text-faint mb-4">You haven't generated any reports yet.</p>
                        <Link href="/workspace" className="inline-flex items-center justify-center px-4 py-2 bg-main border border-border-subtle text-primary rounded-md hover:bg-surface transition-colors text-sm font-medium shadow-sm">
                          Create your first analysis
                        </Link>
                      </div>
                    ) : (
                      <div className="flex flex-col gap-3">
                        {recentReports.map(report => (
                          <Link 
                            key={report.id} 
                            href={`/workspace/${report.id}`}
                            className="group bg-main border border-border-subtle rounded-xl p-4 hover:border-accent-primary transition-all flex items-center gap-4 shadow-sm hover:shadow-md"
                          >
                            <div className="w-10 h-10 rounded-lg bg-surface border border-border-subtle flex items-center justify-center text-accent-primary shrink-0">
                              <Target className="w-5 h-5" />
                            </div>
                            <div className="flex-1 min-w-0">
                              <h3 className="text-sm font-medium text-primary mb-0.5 truncate group-hover:text-accent-primary transition-colors">
                                {report.content ? report.content.substring(0, 60) + '...' : 'Generated Report'}
                              </h3>
                              <div className="flex items-center gap-3 text-xs text-faint">
                                <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {new Date(report.createdAt).toLocaleDateString()}</span>
                                <span className="flex items-center gap-1.5"><span className="w-1.5 h-1.5 rounded-full bg-accent-success"></span> Completed</span>
                              </div>
                            </div>
                            <div className="shrink-0 px-3 py-1.5 bg-surface border border-border-subtle rounded md:opacity-0 group-hover:opacity-100 transition-all text-xs font-semibold text-secondary">
                              View Report
                            </div>
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                {/* Right Column (30%) */}
                <div className="flex flex-col gap-6">
                  
                  {/* Quick Start Templates */}
                  <div className="bg-main border border-border-subtle rounded-xl p-5 shadow-sm">
                    <h2 className="text-xs font-semibold text-faint mb-4  tracking-wider">Quick Templates</h2>
                    <div className="flex flex-col gap-3">
                      <Link href="/workspace" className="group p-3 rounded-xl bg-surface border border-border-subtle hover:border-accent-primary transition-all flex items-start gap-3">
                        <div className="text-xl mt-0.5">💰</div>
                        <div>
                          <h4 className="text-sm font-medium text-primary group-hover:text-accent-primary transition-colors">Financial Diligence</h4>
                          <p className="text-xs text-faint mt-0.5">3-year runway projections and cost analysis.</p>
                        </div>
                      </Link>
                      <Link href="/workspace" className="group p-3 rounded-xl bg-surface border border-border-subtle hover:border-accent-primary transition-all flex items-start gap-3">
                        <div className="text-xl mt-0.5">🚀</div>
                        <div>
                          <h4 className="text-sm font-medium text-primary group-hover:text-accent-primary transition-colors">VC Pitch Narrative</h4>
                          <p className="text-xs text-faint mt-0.5">Create a highly converting storyline.</p>
                        </div>
                      </Link>
                    </div>
                  </div>

                  {/* Education & Resources */}
                  <div className="bg-main border border-border-subtle rounded-xl p-5 shadow-sm">
                     <h2 className="text-xs font-semibold text-faint mb-4  tracking-wider">Resources</h2>
                     <ul className="space-y-4">
                       <li>
                         <a href="#" className="flex items-center gap-3 text-sm text-secondary hover:text-accent-primary transition-colors">
                           <div className="w-8 h-8 rounded-lg bg-surface border border-border-subtle flex items-center justify-center text-faint shrink-0">
                             <FileText className="w-4 h-4" />
                           </div>
                           <span className="truncate font-medium">How our models score</span>
                         </a>
                       </li>
                       <li>
                         <a href="#" className="flex items-center gap-3 text-sm text-secondary hover:text-accent-primary transition-colors">
                           <div className="w-8 h-8 rounded-lg bg-surface border border-border-subtle flex items-center justify-center text-faint shrink-0">
                             <Target className="w-4 h-4" />
                           </div>
                           <span className="truncate font-medium">Context uploading tips</span>
                         </a>
                       </li>
                       <li>
                         <a href="#" className="flex items-center gap-3 text-sm text-secondary hover:text-accent-primary transition-colors">
                           <div className="w-8 h-8 rounded-lg bg-surface border border-border-subtle flex items-center justify-center text-faint shrink-0">
                             <Presentation className="w-4 h-4" />
                           </div>
                           <span className="truncate font-medium">What VCs look for</span>
                         </a>
                       </li>
                     </ul>
                  </div>

                  {/* Platform Updates */}
                  <div className="bg-surface border border-border-subtle rounded-xl p-5 shadow-sm">
                     <div className="flex items-center gap-2 mb-5">
                       <Zap className="w-4 h-4 text-accent-warning" />
                       <h2 className="text-xs font-semibold text-faint tracking-wider">What's New</h2>
                     </div>
                     <div className="border-l-2 border-border-subtle ml-2 pl-5 py-1 flex flex-col gap-6">
                       <div className="relative">
                         <div className="absolute -left-[27px] top-1 w-2.5 h-2.5 rounded-full bg-accent-primary border-2 border-surface shadow-[0_0_0_2px_var(--bg-main)]" />
                         <span className="text-[10px] font-bold text-accent-primary uppercase tracking-wider">Today</span>
                         <h4 className="text-sm font-semibold text-primary mt-1">Dashboard Redesign</h4>
                         <p className="text-xs text-faint mt-1 leading-relaxed">A brand new Overview experience with dedicated project libraries and templates!</p>
                       </div>
                       <div className="relative">
                         <div className="absolute -left-[27px] top-1 w-2.5 h-2.5 rounded-full bg-border-subtle border-2 border-surface shadow-[0_0_0_2px_var(--bg-main)]" />
                         <span className="text-[10px] font-bold text-faint uppercase tracking-wider">Last Week</span>
                         <h4 className="text-sm font-semibold text-primary mt-1">Server Persistence</h4>
                         <p className="text-xs text-faint mt-1 leading-relaxed">Your reports are securely saved across devices via Clerk auth.</p>
                       </div>
                     </div>
                  </div>

                </div>
              </div>
            </div>
          )}

          {/* TAB: PROJECTS */}
          {activeTab === 'projects' && (
            <div className="animate-in fade-in duration-300">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
                <h1 className="text-3xl font-bold text-primary">All Projects</h1>
                <div className="relative w-full sm:w-72">
                  <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-faint" />
                  <input
                    type="text"
                    placeholder="Search projects..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-9 pr-4 py-2 bg-main border border-border-subtle rounded-lg text-sm text-primary placeholder:text-faint focus:outline-none focus:border-accent-primary"
                  />
                </div>
              </div>

              {filteredReports.length === 0 ? (
                <div className="bg-main border border-border-subtle rounded-xl p-12 text-center text-faint">
                  {searchQuery ? 'No projects match your search.' : 'You have no projects yet.'}
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                  {filteredReports.map(report => (
                    <Link 
                      key={report.id} 
                      href={`/workspace/${report.id}`}
                      className="group bg-main border border-border-subtle rounded-xl p-6 hover:border-accent-primary transition-all hover:shadow-lg hover:-translate-y-1 block flex flex-col h-full"
                    >
                      <div className="flex justify-between items-start mb-4">
                        <div className="w-10 h-10 rounded-lg bg-surface border border-border-subtle flex items-center justify-center text-accent-secondary group-hover:scale-110 transition-transform">
                          <Target className="w-5 h-5" />
                        </div>
                      </div>
                      <h3 className="text-base font-medium text-primary mb-2 line-clamp-2 flex-1 group-hover:text-primary transition-colors">
                        {report.content ? report.content : 'Generated Report'}
                      </h3>
                      <div className="flex items-center justify-between mt-4 pt-4 border-t border-border-subtle">
                        <span className="text-xs text-faint flex items-center gap-1">
                          <Clock className="w-3 h-3" /> {new Date(report.createdAt).toLocaleDateString()}
                        </span>
                        <span className="text-xs font-medium text-secondary bg-surface px-2 py-1 rounded-md">Analysis</span>
                      </div>
                    </Link>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* TAB: TEMPLATES */}
          {activeTab === 'templates' && (
            <div className="animate-in fade-in duration-300">
               <h1 className="text-3xl font-bold text-primary mb-2">Templates</h1>
               <p className="text-faint mb-8">Start your next project with specialized agent workflows.</p>
               
               <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                 {[
                   { name: 'Financial Deep Dive', desc: 'Auto-generate comprehensive 3-year projections and runway models.', icon: '💰' },
                   { name: 'VC Pitch Deck', desc: 'Create a highly tailored 10-slide narrative for raising seed rounds.', icon: '🚀' },
                   { name: 'Marketing Strategy', desc: 'ICP generation and multi-channel launch playbook.', icon: '📈' },
                 ].map((t, i) => (
                   <div key={i} className="bg-main border border-border-subtle rounded-xl p-6 flex flex-col items-start gap-4 hover:border-border-subtle cursor-pointer opacity-70 hover:opacity-100 transition-opacity">
                     <span className="text-3xl">{t.icon}</span>
                     <div>
                       <h3 className="text-lg font-medium text-primary mb-1">{t.name}</h3>
                       <p className="text-sm text-faint">{t.desc}</p>
                     </div>
                     <span className="text-xs font-medium text-accent-primary bg-primary/10 px-2 py-1 rounded-full mt-auto">Coming Soon</span>
                   </div>
                 ))}
               </div>
            </div>
          )}

          {/* TAB: SETTINGS */}
          {activeTab === 'settings' && (
            <div className="animate-in fade-in duration-300 max-w-2xl">
              <h1 className="text-3xl font-bold text-primary mb-8">Account Settings</h1>
              <div className="bg-main border border-border-subtle rounded-xl p-8">
                <h2 className="text-xl font-semibold text-primary mb-2">Profile & Security</h2>
                <p className="text-secondary mb-6">Manage your password, emails, and connected accounts directly through our secure authentication provider.</p>
                
                <div className="flex items-center gap-4 p-4 border border-border-subtle rounded-lg bg-surface">
                  <UserButton appearance={{ elements: { userButtonBox: "scale-150 ml-2" } }} />
                  <div>
                    <p className="font-medium text-primary text-sm">Click your avatar to open settings</p>
                    <p className="text-xs text-faint mt-0.5">You can update your name and sign-in methods here.</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

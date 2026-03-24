'use client'

import { useChat } from '@ai-sdk/react'
import { Sparkles, Send, User, Bot, Loader2 } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'

export default function ReportChat({ reportId }) {
  const [initialMessages, setInitialMessages] = useState([])
  const [isInitializing, setIsInitializing] = useState(true)

  useEffect(() => {
    async function loadHistory() {
      try {
        const res = await fetch(`/api/chat/history?reportId=${reportId}`)
        if (res.ok) {
          const data = await res.json()
          setInitialMessages(data)
        }
      } catch (err) {
        console.error("Failed to load chat history", err)
      } finally {
        setIsInitializing(false)
      }
    }
    loadHistory()
  }, [reportId])

  if (isInitializing) {
    return (
      <div className="flex flex-col h-full bg-surface border-l border-border-subtle w-80 lg:w-[400px] shrink-0 items-center justify-center text-faint">
        <Loader2 className="w-6 h-6 animate-spin mb-4 text-accent-primary" />
        <p className="text-sm font-medium">Loading workspace chat...</p>
      </div>
    )
  }

  return <ChatUI reportId={reportId} initialMessages={initialMessages} />
}

function ChatUI({ reportId, initialMessages }) {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
    body: { reportId },
    initialMessages
  })

  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div className="flex flex-col h-full bg-surface border-l border-border-subtle w-80 lg:w-[400px] shrink-0">
      {/* Header */}
      <div className="p-4 border-b border-border-subtle bg-main flex items-center justify-between shrink-0">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-accent-primary" />
          <h2 className="font-semibold text-primary text-sm">Workspace AI</h2>
        </div>
        {messages.length > 0 && (
          <span className="text-xs text-faint font-medium bg-surface px-2 py-0.5 rounded-full border border-border-subtle">{messages.length} messages</span>
        )}
      </div>

      {/* Message List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.length === 0 ? (
          <div className="text-center text-secondary text-sm mt-10 p-6 bg-main border border-border-subtle rounded-xl shadow-sm mx-2">
            <div className="w-10 h-10 bg-surface rounded-full flex items-center justify-center mx-auto mb-3 shadow-inner">
              <Sparkles className="w-5 h-5 text-accent-primary" />
            </div>
            <p className="mb-2 font-semibold text-primary">Chat with your Report!</p>
            <p className="text-xs text-faint leading-relaxed">Ask AI to analyze specific sections, find anomalies, or restructure wording directly.</p>
          </div>
        ) : (
          messages.map((m, idx) => (
            <div key={m.id || idx} className={`flex gap-3 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              {m.role !== 'user' && (
                <div className="w-7 h-7 rounded-full bg-accent-primary/10 flex items-center justify-center shrink-0 border border-accent-primary/20">
                  <Bot className="w-4 h-4 text-accent-primary" />
                </div>
              )}
              <div 
                className={`text-sm px-4 py-2.5 max-w-[85%] prose prose-sm leading-relaxed ${
                  m.role === 'user' 
                    ? 'bg-primary text-main rounded-2xl rounded-tr-sm font-medium shadow-sm' 
                    : 'bg-main border border-border-subtle text-primary rounded-2xl rounded-tl-sm shadow-sm'
                }`}
              >
                {/* extremely primitive markdown rendering for prototype */}
                {m.content.split('\n').map((line, i) => (
                  <span key={i}>
                    {line}
                    {i !== m.content.split('\n').length - 1 && <br />}
                  </span>
                ))}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex gap-3 justify-start">
            <div className="w-7 h-7 rounded-full bg-accent-primary/10 flex items-center justify-center shrink-0 border border-accent-primary/20">
              <Bot className="w-4 h-4 text-accent-primary animate-pulse" />
            </div>
            <div className="text-sm px-4 py-2.5 rounded-2xl bg-main border border-border-subtle text-primary rounded-tl-sm flex items-center gap-2 shadow-sm">
              <span className="flex gap-1.5 px-1 py-1">
                <span className="w-1.5 h-1.5 bg-accent-primary/60 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-1.5 h-1.5 bg-accent-primary/60 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-1.5 h-1.5 bg-accent-primary/60 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} className="h-2" />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-main border-t border-border-subtle shrink-0">
        <form onSubmit={handleSubmit} className="relative flex items-end gap-2 bg-surface border border-border-subtle rounded-xl p-1.5 focus-within:border-accent-primary transition-colors shadow-sm">
          <textarea
            value={input}
            onChange={handleInputChange}
            placeholder="Ask AI to analyze or rewrite..."
            className="w-full bg-transparent resize-none outline-none py-2 pl-2 text-sm text-primary placeholder:text-faint min-h-[40px] max-h-32"
            rows={1}
            disabled={isLoading}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleSubmit(e)
              }
            }}
          />
          <button 
            type="submit" 
            disabled={isLoading || !input.trim()}
            className="p-2 text-main bg-accent-primary hover:bg-accent-secondary rounded-lg disabled:opacity-50 disabled:bg-surface disabled:text-faint transition-all shrink-0 shadow-sm"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
        <div className="text-[10px] text-faint text-center mt-3 font-medium flex items-center justify-center gap-1.5">
          <Sparkles className="w-3 h-3" /> Press Enter to send
        </div>
      </div>
    </div>
  )
}

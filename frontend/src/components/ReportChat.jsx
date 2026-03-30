'use client'

import { useChat } from '@ai-sdk/react'
import { TextStreamChatTransport } from 'ai'
import { Sparkles, Send, Bot, Loader2, X } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'

function normalizeMessage(message, index) {
  const textContent =
    typeof message?.content === 'string'
      ? message.content
      : Array.isArray(message?.parts)
        ? message.parts
            .filter(part => part?.type === 'text' && typeof part.text === 'string')
            .map(part => part.text)
            .join('\n')
        : ''

  return {
    id: message?.id || `${message?.role || 'message'}-${index}`,
    role: message?.role === 'assistant' || message?.role === 'system' ? message.role : 'user',
    parts: Array.isArray(message?.parts) && message.parts.length > 0
      ? message.parts
      : [{ type: 'text', text: textContent }]
  }
}

function getMessageText(message) {
  if (typeof message?.content === 'string') {
    return message.content
  }

  if (!Array.isArray(message?.parts)) {
    return ''
  }

  return message.parts
    .filter(part => part?.type === 'text' && typeof part.text === 'string')
    .map(part => part.text)
    .join('\n')
}

export default function ReportChat({ reportId, onClose }) {
  const [initialMessages, setInitialMessages] = useState([])
  const [isInitializing, setIsInitializing] = useState(true)

  useEffect(() => {
    async function loadHistory() {
      try {
        const res = await fetch(`/api/chat/history?reportId=${reportId}`)
        if (res.ok) {
          const data = await res.json()
          setInitialMessages(Array.isArray(data) ? data.map(normalizeMessage) : [])
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
      <div className="fixed bottom-20 right-4 z-40 flex h-[min(70vh,36rem)] w-[min(24rem,calc(100vw-2rem))] flex-col items-center justify-center rounded-2xl border border-border-subtle bg-surface text-faint shadow-2xl sm:bottom-24 sm:right-6">
        <Loader2 className="w-6 h-6 animate-spin mb-4 text-accent-primary" />
        <p className="text-sm font-medium">Loading workspace chat...</p>
      </div>
    )
  }

  return <ChatUI reportId={reportId} initialMessages={initialMessages} onClose={onClose} />
}

function ChatUI({ reportId, initialMessages, onClose }) {
  const { messages, sendMessage, status, error } = useChat({
    initialMessages,
    transport: new TextStreamChatTransport({
      api: '/api/chat'
    })
  })
  const [draft, setDraft] = useState('')
  const messagesEndRef = useRef(null)
  const isLoading = status === 'submitted' || status === 'streaming'

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function handleSubmit(event) {
    event?.preventDefault?.()

    const trimmedDraft = draft.trim()
    if (!trimmedDraft || isLoading) {
      return
    }

    setDraft('')

    try {
      await sendMessage(
        { text: trimmedDraft },
        {
          body: { reportId }
        }
      )
    } catch (submitError) {
      console.error('Failed to send chat message', submitError)
      setDraft(trimmedDraft)
    }
  }

  return (
    <div className="fixed bottom-20 right-4 z-40 flex h-[min(70vh,36rem)] w-[min(24rem,calc(100vw-2rem))] flex-col overflow-hidden rounded-2xl border border-border-subtle bg-surface shadow-2xl sm:bottom-24 sm:right-6">
      {/* Header */}
      <div className="p-4 border-b border-border-subtle bg-main flex items-center justify-between shrink-0">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-accent-primary" />
          <h2 className="font-semibold text-primary text-sm">Workspace AI</h2>
        </div>
        <div className="flex items-center gap-2">
          {messages.length > 0 && (
            <span className="text-xs text-faint font-medium bg-surface px-2 py-0.5 rounded-full border border-border-subtle">{messages.length} messages</span>
          )}
          {onClose && (
            <button
              type="button"
              onClick={onClose}
              className="inline-flex h-8 w-8 items-center justify-center rounded-lg border border-border-subtle bg-surface text-secondary transition-colors hover:text-primary"
              aria-label="Close workspace chat"
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>
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
                {getMessageText(m).split('\n').map((line, i, lines) => (
                  <span key={i}>
                    {line}
                    {i !== lines.length - 1 && <br />}
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
        {error && (
          <div className="mb-3 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">
            Something went wrong while sending that message.
          </div>
        )}
        <form onSubmit={handleSubmit} className="relative flex items-end gap-2 bg-surface border border-border-subtle rounded-xl p-1.5 focus-within:border-accent-primary transition-colors shadow-sm">
          <textarea
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
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
            disabled={isLoading || !draft.trim()}
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

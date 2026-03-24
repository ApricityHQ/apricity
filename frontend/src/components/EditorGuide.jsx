import { ARTIFACT_TEMPLATES } from '@/config/artifacts'
import * as Icons from 'lucide-react'
import { useMemo, useState } from 'react'

export default function EditorGuide({ document }) {
  const [isExpanded, setIsExpanded] = useState(true)

  // Try to find the matching template based on the most likely source
  // Since title can be edited, we combine icon and initial title heuristics if possible
  // For simplicity since we don't store templateId, we try title first, then icon.
  const template = useMemo(() => {
    if (!document) return null
    // Try to match by icon first, as that is rarely changed by users right now
    const byIcon = ARTIFACT_TEMPLATES.find(t => t.icon === document.icon && t.id !== 'custom')
    if (byIcon) return byIcon
    return ARTIFACT_TEMPLATES.find(t => t.id === 'custom')
  }, [document])

  if (!document || !template || Object.keys(template.prompts || {}).length === 0) {
    return null
  }

  const TemplateIcon = Icons[template.icon] || Icons.FileText

  return (
    <div 
      className={`border-l border-border-subtle bg-surface transition-all duration-300 flex flex-col shrink-0 ${
        isExpanded ? 'w-80' : 'w-12'
      }`}
    >
      {/* Toggle Header */}
      <div className={`p-3 border-b border-border-subtle flex items-center shrink-0 ${isExpanded ? 'justify-between' : 'justify-center'}`}>
        {isExpanded && (
          <span className="text-xs font-semibold text-faint uppercase tracking-wider">
            Section Guide
          </span>
        )}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-6 h-6 flex items-center justify-center rounded hover:bg-main text-secondary hover:text-primary transition-colors"
          title={isExpanded ? "Collapse Guide" : "Expand Guide"}
        >
          <Icons.ChevronRight className={`w-4 h-4 transition-transform ${isExpanded ? '' : 'rotate-180'}`} />
        </button>
      </div>

      {/* Expanded Content */}
      {isExpanded ? (
        <div className="p-6 overflow-y-auto space-y-8 flex-1">
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-primary mb-2 flex items-center gap-2">
              <TemplateIcon className="w-4 h-4 text-accent-primary" />
              {template.title}
            </h3>
            <p className="text-sm text-secondary leading-relaxed">
              {template.description}
            </p>
          </div>

          <div className="space-y-6">
            {Object.entries(template.prompts).map(([heading, questions]) => (
              <div key={heading} className="bg-main border border-border-subtle rounded-xl p-4 shadow-sm">
                <h4 className="font-medium text-primary mb-3 pb-2 border-b border-border-subtle">{heading}</h4>
                <ul className="space-y-3">
                  {questions.map((q, i) => (
                    <li key={i} className="text-sm text-secondary flex items-start gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-accent-primary/50 mt-1.5 shrink-0" />
                      <span className="leading-relaxed">{q}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      ) : (
        /* Collapsed Icon state */
        <div 
          className="flex-1 flex flex-col items-center pt-6 opacity-60 hover:opacity-100 transition-opacity cursor-pointer text-accent-primary"
          onClick={() => setIsExpanded(true)}
          title="Show Guide"
        >
          <TemplateIcon className="w-5 h-5 mb-4" />
          <div className="w-px h-12 bg-border-subtle" />
        </div>
      )}
    </div>
  )
}

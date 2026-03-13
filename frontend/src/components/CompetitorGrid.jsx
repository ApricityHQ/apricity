'use client'

import * as Icons from 'lucide-react'

function CompetitorCard({ competitor, index }) {
  const isUnknown = (val) => !val || val === 'Unknown'

  return (
    <div className="group relative bg-main border border-border-subtle rounded-xl p-5 hover:border-accent-primary/40 transition-all duration-200 hover:shadow-md">
      {/* Rank badge */}
      <div className="absolute -top-2.5 -left-2.5 w-7 h-7 rounded-full bg-accent-primary text-white text-xs font-semibold flex items-center justify-center shadow-sm">
        {competitor.rank || index + 1}
      </div>

      {/* Header */}
      <div className="mb-3 pt-1">
        <div className="flex items-start justify-between gap-2">
          <h4 className="font-semibold text-primary text-base leading-tight" style={{ fontFamily: '"Instrument Sans", sans-serif' }}>
            {competitor.company_name}
          </h4>
          {!isUnknown(competitor.website) && (
            <a
              href={competitor.website}
              target="_blank"
              rel="noopener noreferrer"
              className="shrink-0 text-faint hover:text-accent-primary transition-colors"
            >
              <Icons.ExternalLink className="w-3.5 h-3.5" />
            </a>
          )}
        </div>
        {!isUnknown(competitor.headquarters) && (
          <div className="flex items-center gap-1 mt-1 text-xs text-faint">
            <Icons.MapPin className="w-3 h-3" />
            <span>{competitor.headquarters}</span>
          </div>
        )}
      </div>

      {/* Description */}
      {!isUnknown(competitor.description) && (
        <p className="text-xs text-secondary leading-relaxed mb-4 line-clamp-3">
          {competitor.description}
        </p>
      )}

      {/* Stats grid */}
      <div className="grid grid-cols-2 gap-2">
        <StatChip
          icon={<Icons.DollarSign className="w-3 h-3" />}
          label="Funding"
          value={competitor.funding}
        />
        <StatChip
          icon={<Icons.Users className="w-3 h-3" />}
          label="Employees"
          value={competitor.employees}
        />
        <StatChip
          icon={<Icons.TrendingUp className="w-3 h-3" />}
          label="Revenue"
          value={competitor.revenue}
        />
        <StatChip
          icon={<Icons.Calendar className="w-3 h-3" />}
          label="Founded"
          value={competitor.founded_year}
        />
      </div>

      {/* Differentiator / Target Customer */}
      {(!isUnknown(competitor.company_differentiator) || !isUnknown(competitor.target_customer)) && (
        <div className="mt-3 pt-3 border-t border-border-subtle space-y-1.5">
          {!isUnknown(competitor.company_differentiator) && (
            <div className="flex items-start gap-1.5">
              <Icons.Zap className="w-3 h-3 text-accent-warning mt-0.5 shrink-0" />
              <span className="text-xs text-secondary">{competitor.company_differentiator}</span>
            </div>
          )}
          {!isUnknown(competitor.target_customer) && (
            <div className="flex items-start gap-1.5">
              <Icons.Target className="w-3 h-3 text-accent-primary mt-0.5 shrink-0" />
              <span className="text-xs text-secondary">{competitor.target_customer}</span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function StatChip({ icon, label, value }) {
  const isUnknown = !value || value === 'Unknown'
  if (isUnknown) return null

  return (
    <div className="flex items-center gap-1.5 bg-surface rounded-lg px-2.5 py-1.5">
      <span className="text-faint">{icon}</span>
      <div className="min-w-0">
        <div className="text-[10px] text-faint uppercase tracking-wide leading-none mb-0.5">{label}</div>
        <div className="text-xs text-primary font-medium truncate">{value}</div>
      </div>
    </div>
  )
}

export default function CompetitorGrid({ competitors, searchSentence, status }) {
  if (!competitors || competitors.length === 0) {
    return (
      <div className="bg-main border border-border-subtle rounded-xl p-8 text-center">
        <Icons.SearchX className="w-10 h-10 text-faint mx-auto mb-3" />
        <p className="text-secondary text-sm">
          {status === 'disabled'
            ? 'Competitor search is not configured.'
            : 'No competitors found for this idea.'}
        </p>
      </div>
    )
  }

  return (
    <div>
      {/* Section header */}
      <div className="flex items-center gap-2 mb-1">
        <Icons.Building2 className="w-5 h-5 text-accent-primary" />
        <h3 className="text-lg font-semibold text-primary" style={{ fontFamily: '"Instrument Serif", serif' }}>
          Competitor Landscape
        </h3>
        <span className="ml-auto text-xs text-faint bg-surface border border-border-subtle rounded-full px-2.5 py-0.5">
          {competitors.length} found
        </span>
      </div>

      {searchSentence && (
        <p className="text-xs text-faint mb-5 ml-7">
          Search: &ldquo;{searchSentence}&rdquo;
        </p>
      )}

      {/* Cards grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
        {competitors.map((c, i) => (
          <CompetitorCard key={c.company_name + i} competitor={c} index={i} />
        ))}
      </div>
    </div>
  )
}

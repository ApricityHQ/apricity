/**
 * Artifact Templates Configuration
 * 
 * Each artifact defines a section type that can be added to the document.
 * Icons use Lucide icon names (string identifiers) for maintainability.
 * Templates are structured for easy API replacement.
 */

export const ARTIFACT_TEMPLATES = [
  {
    id: 'problem-statement',
    title: 'Problem Statement',
    icon: 'Target',
    description: 'Define the problem you are solving',
    prompts: {
      'The Problem': [
        "What pain point or gap exists in the market?",
        "What is broken today?",
        "Why is this a significant problem?"
      ],
      'Who Experiences This?': [
        "Describe your target user in detail.",
        "Who feels this pain the most?",
        "What is their current workflow?"
      ],
      'Current Alternatives': [
        "How do people solve this problem today?",
        "What are the makeshift solutions?",
        "Why are existing solutions inadequate?"
      ],
      'Why Now?': [
        "What has changed that makes this the right time?",
        "Why hasn't this been solved before?",
        "What macro trends are in your favor?"
      ]
    },
    defaultContent: null
  },
  {
    id: 'founder-profile',
    title: 'Founder Profile',
    icon: 'User',
    description: 'Background and experience of founders',
    prompts: {
      'Background': [
        "Share your journey — what led you here?",
        "What is your personal connection to the problem?",
        "What were you doing before this?"
      ],
      'Why This Problem?': [
        "What makes you uniquely positioned to solve this?",
        "Why are you the right person for this?",
        "What is your unfair advantage?"
      ]
    },
    defaultContent: null
  },
  {
    id: 'solution-hypothesis',
    title: 'Solution Hypothesis',
    icon: 'Lightbulb',
    description: 'Your proposed solution and value prop',
    prompts: {
      'Core Solution': [
        "What are you building? Describe it simply.",
        "How does it work?",
        "What is the core mechanic?"
      ],
      'Unique Value Proposition': [
        "Why will customers choose you over alternatives?",
        "What is 10x better?",
        "What is your moat?"
      ]
    },
    defaultContent: null
  },
  {
    id: 'market-notes',
    title: 'Market Notes',
    icon: 'BarChart3',
    description: 'Market size and competitive landscape',
    prompts: {
      'Competitive Landscape': [
        "Who else is in this space? How are you different?",
        "What are the incumbents missing?",
        "Who are the new entrants?"
      ]
    },
    defaultContent: null
  },
  {
    id: 'team',
    title: 'Team',
    icon: 'Users',
    description: 'Core team, advisors, and key hires',
    prompts: {},
    defaultContent: null
  },
  {
    id: 'funding-runway',
    title: 'Funding & Runway',
    icon: 'Wallet',
    description: 'Financial status and funding plans',
    prompts: {
      'Use of Funds': [
        "How will you allocate the next round?",
        "What are the key hires?",
        "What are the product milestones?"
      ],
      'Milestones': [
        "What will you achieve with this funding?",
        "What is the next valuation inflexion point?",
        "What is the timeline?"
      ]
    },
    defaultContent: null
  },
  {
    id: 'risks-unknowns',
    title: 'Risks & Unknowns',
    icon: 'AlertTriangle',
    description: 'Key risks and open questions',
    prompts: {
      'Open Questions': [
        "Things you're still figuring out:",
        "What are known unknowns?",
        "What experiments do you need to run?"
      ],
      'Assumptions': [
        "What must be true for this to work?",
        "What is the riskiest assumption?",
        "What are you taking for granted?"
      ]
    },
    defaultContent: null
  },
  {
    id: 'external-references',
    title: 'External References',
    icon: 'Link',
    description: 'Documents, links, and research sources',
    prompts: {},
    defaultContent: null
  },
  {
    id: 'custom',
    title: 'Custom Section',
    icon: 'FileText',
    description: 'A blank section for anything else',
    prompts: {},
    defaultContent: null
  }
]

/**
 * Fetch artifact templates
 * Currently returns static data, can be swapped for API call
 */
export async function fetchArtifactTemplates() {
  // TODO: Replace with API call when ready
  // return fetch('/api/artifacts/templates').then(r => r.json())
  return ARTIFACT_TEMPLATES
}

/**
 * Get a single template by ID
 */
export function getArtifactTemplate(id) {
  return ARTIFACT_TEMPLATES.find(t => t.id === id)
}

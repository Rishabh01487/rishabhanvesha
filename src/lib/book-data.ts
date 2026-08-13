export interface Chapter {
  title: string;
  page: number;
}

export interface Part {
  title: string;
  chapters: Chapter[];
}

export const TOTAL_PAGES = 279;

export const bookMeta = {
  title: "AVERON",
  subtitle: "The Programmable Digital Asset Infrastructure",
  author: "Rishabh Gupta",
  role: "AI/ML Engineer · Chief Protocol Architect @ Averon",
  edition: "First Edition, 2026",
  series: "Averon Protocol Series · Vol. I",
  tagline: "Transforming idle assets into productive capital",
  description:
    "A programmable financial ecosystem where real-world assets, artificial intelligence, blockchain technology, and capital markets converge into a single operating system for global assets.",
};

export const parts: Part[] = [
  {
    title: "Foundation",
    chapters: [
      { title: "Preface", page: 15 },
      { title: "The Digital Asset Imperative", page: 18 },
      { title: "Averon: The Vision", page: 25 },
      { title: "Core Concepts & Architecture Principles", page: 33 },
      { title: "Platform Overview & User Journey", page: 41 },
    ],
  },
  {
    title: "The Averon Architecture",
    chapters: [
      { title: "The Eight-Layer Architecture", page: 49 },
      { title: "Layer 1 — Averon Blockchain", page: 55 },
      { title: "Layer 2 — Averon Virtual Machine (AVM)", page: 63 },
      { title: "Layer 3 — AI Layer", page: 72 },
      { title: "Layer 4 — Identity Layer", page: 80 },
      { title: "Layer 5 — Compliance Layer", page: 88 },
      { title: "Layer 6 — Oracle Layer", page: 96 },
      { title: "Layer 7 — Marketplace Layer", page: 104 },
      { title: "Layer 8 — Developer Platform", page: 112 },
    ],
  },
  {
    title: "The Asset Lifecycle",
    chapters: [
      { title: "What Asset Tokenization Truly Means", page: 51 },
      { title: "The Anatomy of a Tokenized Asset", page: 57 },
      { title: "Temporary Programmable Ownership", page: 62 },
      { title: "The Tokenization Lifecycle Revisited", page: 67 },
      { title: "Smart Contracts for Real-World Assets", page: 71 },
    ],
  },
  {
    title: "Capital Markets & Trading",
    chapters: [
      { title: "The Trading Engine", page: 120 },
      { title: "Order Book Architecture", page: 126 },
      { title: "Price Discovery & Oracle Feeds", page: 133 },
      { title: "Escrow & Settlement", page: 139 },
      { title: "Asset-Backed Financing", page: 145 },
    ],
  },
  {
    title: "The AVR Coin",
    chapters: [
      { title: "Token Economics & Utility Design", page: 151 },
      { title: "Staking, Validation & Consensus", page: 158 },
      { title: "Governance & Protocol Upgrades", page: 165 },
      { title: "AVR Distribution & Emission Schedule", page: 172 },
    ],
  },
  {
    title: "Enterprise & Integration",
    chapters: [
      { title: "Enterprise Integration Framework", page: 180 },
      { title: "Cross-Chain Interoperability", page: 187 },
      { title: "Compliance-as-a-Service", page: 194 },
      { title: "Developer SDK & APIs", page: 201 },
    ],
  },
  {
    title: "Applications & Use Cases",
    chapters: [
      { title: "Real Estate Tokenization", page: 208 },
      { title: "Agriculture & Commodities", page: 215 },
      { title: "Infrastructure & Project Finance", page: 222 },
      { title: "Intellectual Property & Digital Assets", page: 229 },
    ],
  },
  {
    title: "Security & Future",
    chapters: [
      { title: "Security Architecture & Threat Model", page: 236 },
      { title: "Roadmap & Future Development", page: 246 },
      { title: "Conclusion", page: 260 },
      { title: "Appendices & References", page: 268 },
    ],
  },
];

export const allChapters = parts.flatMap((p) =>
  p.chapters.map((c) => ({ ...c, part: p.title }))
);

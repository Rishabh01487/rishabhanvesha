const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, Header, Footer, AlignmentType, HeadingLevel, PageNumber, TableOfContents, PageBreak, Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType, TabStopPosition, TabStopType, convertInchesToTwip, LevelFormat, UnderlineType } = require("docx");

// ── Palette (Cool + Heavy + Calm = Academic) ──
const P = {
  primary: "#1f2223", body: "#2c2f30", secondary: "#6b7280",
  accent: "#2c7aa1", surface: "#f3f5f5", coverBg: "#1f2937", coverText: "#e5e7eb"
};
const c = (hex) => hex.replace("#", "");

// ── Constants ──
const A4_W = 11906, A4_H = 16838;
const INDENT = convertInchesToTwip(0.4);
const BODY_SIZE = 24; // 12pt
const LINE_SPACING = 312; // 1.3x

// ── Components ──
function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 480, after: 240 },
    children: [new TextRun({ text, bold: true, size: 36, color: c(P.accent), font: "Times New Roman" })]
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 360, after: 180 },
    children: [new TextRun({ text, bold: true, size: 30, color: c(P.primary), font: "Times New Roman" })]
  });
}

function heading3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 240, after: 120 },
    children: [new TextRun({ text, bold: true, size: 26, color: c(P.primary), font: "Times New Roman" })]
  });
}

function body(text) {
  return new Paragraph({
    spacing: { line: LINE_SPACING, after: 120 },
    children: [new TextRun({ text, size: BODY_SIZE, color: c(P.body), font: "Times New Roman" })],
  });
}

function caption(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 120 },
    children: [new TextRun({ text, size: 21, italics: true, color: c(P.secondary), font: "Times New Roman" })],
  });
}

// ── Content Data ──
const chapters = [
  { title: "Chapter 1: Introduction to Asset Tokenization", sections: [
    { h2: "1.1 The Evolution of Digital Assets", text: "The concept of representing ownership through digital means has evolved dramatically over the past two decades, from the introduction of Bitcoin in 2009 as a purely digital store of value to today's sophisticated platforms that bridge the gap between physical real-world assets and digital blockchain-based tokens. Asset tokenization refers to the process of creating digital tokens on a blockchain that represent ownership rights, economic benefits, or other entitlements linked to tangible or intangible assets. These assets can range from real estate properties and agricultural land to accounts receivable, commodities, intellectual property, and equity stakes in private companies. The fundamental value proposition of tokenization lies in its ability to divide traditionally illiquid, large-denomination assets into smaller, tradable units, thereby democratizing access to investment opportunities that were previously available only to wealthy individuals or institutional investors." },
    { h2: "1.2 Motivation and Problem Statement", text: "Despite the promise of asset tokenization, existing platforms face several critical technical and operational challenges that limit their adoption. Most platforms operate on public blockchain networks such as Ethereum, which introduces significant transaction costs (gas fees) that make micro-investments economically unviable. A single Ethereum transaction can cost anywhere from $1 to $50 depending on network congestion, which is prohibitive for the small-denomination investments that are the core value proposition of fractional asset ownership. Additionally, the reliance on public blockchains exposes transaction details to all network participants, creating privacy concerns for asset owners. Averon v4.0.0 was designed to address all of these challenges through a unified, vertically-integrated platform architecture that eliminates gas fees while providing data privacy and regulatory compliance support." },
    { h2: "1.3 The Averon Solution", text: "Averon v4.0.0 is a comprehensive asset tokenization platform integrating five core technical components: a custom proof-of-work blockchain, an AI-powered document verification pipeline, an on-chain escrow mechanism, a centralized trading engine, and an algorithmic price discovery model. The platform enables asset owners to create digital tokens representing fractional ownership of real-world assets, investors to purchase these tokens through a regulated funding process with built-in escrow protection, and all participants to trade tokens on a secondary market with on-chain settlement. This book provides a comprehensive technical deep dive into every component of the platform." },
  ]},
  { title: "Chapter 2: Platform Architecture Overview", sections: [
    { h2: "2.1 Architectural Principles", text: "The architecture of Averon v4.0.0 is guided by several key design principles. The first principle is vertical integration: rather than composing the platform from independent microservices, Averon implements all core functionality within a single monolithic application. This eliminates inter-service communication overhead, simplifies deployment, and ensures data consistency. The second principle is blockchain-native design: the custom blockchain is a foundational component deeply integrated with business logic, with specialized transaction types corresponding to platform operations. The third principle is defense-in-depth security with multiple overlapping security mechanisms at different layers." },
    { h2: "2.2 Five-Layer Architecture", text: "The system is organized into five principal layers. The Security Layer (Layer 5) sits at the top of the request processing pipeline, implementing JWT authentication, rate limiting, input sanitization, and audit logging. The Application Layer (Layer 4) implements business logic for asset management, trading, payments, and user administration. The AI Processing Layer (Layer 3) implements the five-stage document analysis pipeline. The Data Layer (Layer 2) provides persistent storage through SQLite with 19 tables and the blockchain's chain.json file. The Blockchain Layer (Layer 1) provides immutable ledger infrastructure including the PoW mining engine and chain storage." },
    { h2: "2.3 Technology Stack", text: "Averon v4.0.0 is implemented as a monolithic Node.js application leveraging the V8 JavaScript engine's event-driven, non-blocking I/O model. The web framework is Express.js. The database is SQLite, selected for zero-configuration deployment, full ACID compliance, and suitability for single-server applications. The blockchain engine is a custom Node.js module running PoW mining asynchronously within the event loop. Cryptographic operations utilize the Node.js crypto module for ECDSA signatures and crypto-js for SHA-256 hashing." },
  ]},
  { title: "Chapter 3: Custom Blockchain Engine", sections: [
    { h2: "3.1 Design Rationale", text: "The decision to implement a custom blockchain rather than deploying on an existing public network was driven by three requirements: specialized transaction types with no equivalent in standard protocols, zero transaction fees for micro-investments, and data privacy for investment details. The custom blockchain addresses all three while maintaining the security properties that make blockchain technology valuable." },
    { h2: "3.2 Cryptographic Foundations", text: "The blockchain employs ECDSA secp256k1 for digital signatures (128-bit security, same as Bitcoin) and SHA-256 for hashing. Each transaction is signed by the sender's private key, ensuring non-repudiation and authenticity. SHA-256 produces 256-bit digests for transaction hashes, block hashes, and Merkle roots." },
    { h2: "3.3 Transaction Types", text: "The platform defines eight transaction types: MINT (coin creation from fiat), TRANSFER (peer-to-peer transfer), INVEST (user to escrow for asset tokens), DIVEST (early exit), PAYOUT (escrow to owner upon full funding), REFUND (escrow to investors on expiry), FEE (platform fee collection), and ASSET_CREATE (on-chain tokenization record). These encode business logic directly into the protocol." },
    { h2: "3.4 Proof-of-Work Mining", text: "Mining involves finding a nonce such that the SHA-256 hash of the block header is below the difficulty target. Difficulty is dynamically adjusted to maintain consistent block intervals. The chain is stored in chain.json in structured JSON format supporting human-readable inspection and straightforward backup." },
  ]},
  { title: "Chapter 4: Database Architecture", sections: [
    { h2: "4.1 SQLite as the Data Store", text: "SQLite was selected for its serverless architecture, zero configuration, full ACID compliance, and excellent read performance. The database persists all relational data while chain.json maintains immutable blockchain state separately, creating clean separation between mutable and immutable state." },
    { h2: "4.2 Schema Design", text: "The schema comprises 19 tables in six groups: user management (users, wallets, kyc_verifications, sessions), asset management (assets, asset_documents, asset_tokens), escrow (escrow_accounts, escrow_transactions), trading (coin_orders, coin_trades), economic (economy, price_history, fee_ledger), and payment (payment_gateways, payment_orders, payment_transactions), plus notifications and audit_logs." },
  ]},
  { title: "Chapter 5: AI-Powered Document Verification", sections: [
    { h2: "5.1 Five-Stage Pipeline Overview", text: "The pipeline processes uploaded documents through five stages: image preprocessing, OCR, text classification, named entity recognition, and verification scoring. It supports JPG, PNG, WebP, and PDF formats with 10MB per document, 1-10 documents per asset. Files are stored with crypto-randomized filenames, and SHA-256 hashes enable duplicate detection." },
    { h2: "5.2 Image Preprocessing", text: "Stage 1 applies Gaussian noise reduction, CLAHE contrast enhancement, Hough transform skew correction, and Otsu binarization. These operations prepare document images for reliable OCR, particularly for mobile photographs with poor lighting or perspective distortion." },
    { h2: "5.3 OCR and Text Classification", text: "Stage 2 uses a deep learning OCR engine supporting multiple languages, fonts, and layouts. Stage 3 employs a transformer-based classification model fine-tuned on financial/legal corpora to determine document type and relevance. Stage 4 uses NER to extract structured entities (addresses, amounts, dates, names, registration numbers)." },
    { h2: "5.4 Verification Scoring", text: "Stage 5 aggregates all outputs into a confidence score (0-100) and binary recommendation (verified/rejected). Factors include document completeness, information consistency, image quality, and compliance indicators. The threshold is typically 60/100." },
  ]},
  { title: "Chapter 6: Asset Lifecycle Management", sections: [
    { h2: "6.1 The State Machine", text: "The lifecycle is governed by a deterministic finite state machine: draft, documents_uploaded, ai_analyzing, verified/rejected, compliance_review, active, funding, funded/expired, payout_pending, completed or refunding/closed. Each transition is timestamped and attributed to the triggering user or system." },
    { h2: "6.2 Detailed State Descriptions", text: "In draft, the owner provides title, description, category (12 options), raise amount (100 INR to 1 Cr INR), and listing duration. Documents are uploaded in documents_uploaded. The AI pipeline runs in ai_analyzing. Compliance_review adds regulatory checks. Active assets are visible to investors. Funding leads to funded (payout) or expired (refund)." },
  ]},
  { title: "Chapter 7: Escrow Mechanism", sections: [
    { h2: "7.1 Per-Asset Escrow Accounts", text: "Each asset has a dedicated escrow account. Investor funds are locked via atomic INVEST transactions. The escrow_accounts table tracks balance, total received/released/refunded. Escrow_transactions records each LOCK/RELEASE/REFUND with user ID, amount, and blockchain tx hash." },
    { h2: "7.2 Payout and Refund Logic", text: "On successful funding, the total locked minus 1.0% capital raise fee is released via PAYOUT transaction. On expiry, all funds are returned via REFUND transactions. All operations are atomic, on-chain, and individually recorded." },
  ]},
  { title: "Chapter 8: Trading Engine", sections: [
    { h2: "8.1 Order Book Architecture", text: "A centralized limit-order book supports market and limit orders. Users can maintain max 50 open orders. Orders are stored in coin_orders with side, type, amount, price, filled, remaining, and status fields." },
    { h2: "8.2 Price-Time Priority Matching", text: "Bids sorted by price DESC, asks by price ASC, ties broken by timestamp. The engine iterates the opposite side, matching until filled or no matching prices remain. Unfilled limit orders are inserted into the book." },
    { h2: "8.3 On-Chain Settlement", text: "Each trade generates a TRADE transaction on the blockchain with buyer/seller addresses, amount, price, 0.1% fees each side, and tx hash. Double-mint prevention uses atomic UPDATE with WHERE status IN ('created','pending')." },
  ]},
  { title: "Chapter 9: Payment Integration", sections: [
    { h2: "9.1 Fiat-to-Crypto Purchase Flow", text: "Users purchase tokens via configured payment gateways. Payment orders record gateway, fiat amount, coin amount, exchange rate, and KYC tier. Payment transactions maintain gateway-level audit trails for reconciliation." },
    { h2: "9.2 Payment Verification", text: "Gateway callbacks trigger verification via API query. Atomic UPDATE with status check prevents double-minting: zero affected rows = duplicate rejected; one row = proceed to MINT on blockchain and credit wallet." },
  ]},
  { title: "Chapter 10: Algorithmic Price Discovery", sections: [
    { h2: "10.1 The Dual-Factor Formula", text: "P = P_initial x (1 + totalSupply/10000) x (1 + totalAssetsFunded x 0.04). Factor 1: supply-based inflation (at 100K tokens, factor = 11.0). Factor 2: utility-based (4% per funded asset). Together they create a positive feedback loop aligning price with platform activity." },
    { h2: "10.2 Asset Funding Boost", text: "boost = min(5%, 2% + raiseAmount/1M x 3%). Small raises get ~2.3% boost; large raises reach the 5% cap. This creates visible, predictable connections between funding events and price movements." },
  ]},
  { title: "Chapter 11: Fee Structure and Economics", sections: [
    { h2: "11.1 Multi-Tiered Fee Model", text: "Five fee types: trading (0.1% both sides), listing (1.0 AC), capital raise (1.0% of raised), withdrawal (0.5 AC), gateway (variable). All recorded in fee_ledger and aggregated in economy.total_fees_collected." },
  ]},
  { title: "Chapter 12: API Design", sections: [
    { h2: "12.1 RESTful Architecture", text: "Express.js with JSON bodies (5MB limit), standard REST conventions, HTTP status codes. 18 endpoints across authentication, wallet, asset, market, portfolio, blockchain, withdrawal, and payment groups. All pass through security middleware." },
  ]},
  { title: "Chapter 13: Security Architecture", sections: [
    { h2: "13.1 Defense-in-Depth", text: "JWT Bearer auth (authenticate, optionalAuth, requireRole). Token bucket rate limiting: general (100/60s), auth (10/60s), financial (5/1s). Input sanitization removes HTML/JS/SQL patterns. Audit logging with hash chain integrity verification." },
    { h2: "13.2 Hash Chain Audit", text: "Each audit_logs entry includes SHA-256 hash of previous entry, creating tamper-evident chain. Modifications break the chain, detectable through integrity verification. Provides cryptographic binding superior to simple log files." },
  ]},
  { title: "Chapter 14: Deployment and Operations", sections: [
    { h2: "14.1 System Requirements", text: "Minimum 2 CPU cores, 4GB RAM. Storage depends on chain length and database size: ~5-10GB for 10K users and 100K transactions. Deployed as single Node.js process with PM2/systemd, with regular backups of SQLite and chain.json." },
    { h2: "14.2 Monitoring", text: "Key metrics: chain health, trading throughput, economic indicators (price, market cap, TVL), system health (CPU, memory, disk I/O, API latency). The economy table provides a real-time dashboard." },
  ]},
  { title: "Chapter 15: Future Directions", sections: [
    { h2: "15.1 Proof-of-Stake Migration", text: "PoS would eliminate energy-intensive mining, reduce environmental footprint, and enable faster confirmations. Validators selected by staked tokens with slashing for misbehavior. Must maintain backward compatibility with existing chain history." },
    { h2: "15.2 Cross-Chain Interoperability", text: "Bridge protocols enabling Averon tokens to transfer to other blockchain networks. Would expand reach and enable DeFi ecosystem integration through wrapped tokens or cross-chain message passing for asset records and escrow states." },
    { h2: "15.3 Decentralized Identity", text: "W3C DID and Verifiable Credentials for portable, user-controlled KYC. Users obtain credentials from trusted issuers and present them for verification without platform-specific KYC processes." },
    { h2: "15.4 Microservices Migration", text: "Extracting blockchain mining, AI pipeline, and trading engine into independent services for horizontal scaling. Requires message queues, distributed transactions, and service discovery. Current modular codebase facilitates migration." },
  ]},
];

// ── Build Document ──
const allChildren = [];

// Cover section (no page numbers)
const coverChildren = [
  new Paragraph({ spacing: { before: 4000 } }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { line: 600, lineRule: "atLeast" },
    children: [new TextRun({ text: "AVERON v4.0.0", size: 60, bold: true, color: c(P.accent), font: "Times New Roman" })],
  }),
  new Paragraph({ spacing: { before: 200 } }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Asset Tokenization Platform", size: 40, color: c(P.primary), font: "Times New Roman" })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 100 },
    children: [new TextRun({ text: "Technical Deep Dive", size: 32, color: c(P.secondary), font: "Times New Roman" })],
  }),
  new Paragraph({ spacing: { before: 2000 } }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "A Comprehensive 15-Chapter Technical Reference", size: 22, color: c(P.secondary), font: "Times New Roman" })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 600 },
    children: [new TextRun({ text: "Averon Technologies Private Limited", size: 22, color: c(P.body), font: "Times New Roman" })],
  }),
];

// TOC section
const tocChildren = [
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 600, after: 400 },
    children: [new TextRun({ text: "Table of Contents", size: 36, bold: true, color: c(P.accent), font: "Times New Roman" })],
  }),
  new TableOfContents("TOC", {
    hyperlink: true,
    headingStyleRange: "1-3",
    stylesWithLevels: [
      { level: 1, format: "numericDot", text: "Chapter %1", alignment: AlignmentType.LEFT, style: { paragraph: { spacing: { before: 360, after: 120 } }, run: { size: 24, bold: true, font: "Times New Roman", color: c(P.primary) } } },
    ],
  }),

// Body content
const bodyChildren = [];
for (const ch of chapters) {
  bodyChildren.push(heading1(ch.title));
  for (const sec of ch.sections) {
    bodyChildren.push(heading2(sec.h2));
    bodyChildren.push(body(sec.text));
  }
}

const doc = new Document({
  creator: "Averon Technologies",
  title: "Averon v4.0.0 - Technical Deep Dive",
  description: "Comprehensive 15-chapter technical reference for the Averon asset tokenization platform",
  styles: {
    default: {
      document: {
        run: { font: "Times New Roman", size: BODY_SIZE, color: c(P.body) },
        paragraph: { spacing: { line: LINE_SPACING } },
      },
    },
  },
  sections: [
    // Cover (no page numbers)
    {
      properties: { page: { margin: { top: 0, bottom: 0, left: 0, right: 0 }, size: { width: A4_W, height: A4_H } } },
      children: coverChildren,
    },
    // TOC (Roman numerals)
    {
      properties: {
        page: {
          margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 },
          pageNumbers: { start: 1, formatType: "UPPER_ROMAN" },
        },
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ children: ["PAGE \\* ROMAN \\* MERGEFORMAT"], size: 18, font: "Times New Roman", color: c(P.secondary) }),
            ],
          })],
        }),
      },
      children: tocChildren,
    },
    // Body (Arabic numerals)
    {
      properties: {
        page: {
          margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 },
          pageNumbers: { start: 1 },
        },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            alignment: AlignmentType.RIGHT,
            children: [new TextRun({ text: "Averon v4.0.0 Technical Deep Dive", size: 18, italics: true, font: "Times New Roman", color: c(P.secondary) })],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ children: ["PAGE \\* arabic \\* MERGEFORMAT"], size: 18, font: "Times New Roman", color: c(P.secondary) }),
            ],
          })],
        }),
      },
      children: bodyChildren,
    },
  ],
});

const OUTPUT = "/home/z/my-project/download/Averon_Technical_Book.docx";
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUTPUT, buf);
  console.log(`DOCX generated successfully`);
});
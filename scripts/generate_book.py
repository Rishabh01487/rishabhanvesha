#!/usr/bin/env python3
"""
Averon v4.0.0 - Technical Deep Dive: Full Textbook
15 Chapters covering the complete asset tokenization platform
"""

import os, sys, hashlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import SimpleDocTemplate

# ── Font Setup ──
FONT_DIR = '/usr/share/fonts'
pdfmetrics.registerFont(TTFont('FreeSerif', f'{FONT_DIR}/truetype/freefont/FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Bold', f'{FONT_DIR}/truetype/freefont/FreeSerifBold.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Italic', f'{FONT_DIR}/truetype/freefont/FreeSerifItalic.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-BoldItalic', f'{FONT_DIR}/truetype/freefont/FreeSerifBoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', f'{FONT_DIR}/truetype/dejavu/DejaVuSansMono.ttf'))
registerFontFamily('FreeSerif', normal='FreeSerif', bold='FreeSerif-Bold', italic='FreeSerif-Italic', boldItalic='FreeSerif-BoldItalic')

# ── Palette ──
PAGE_BG = colors.HexColor('#f4f5f5')
HEADER_FILL = colors.HexColor('#3a4a52')
COVER_BLOCK = colors.HexColor('#455963')
BORDER = colors.HexColor('#c2cdd2')
ACCENT = colors.HexColor('#2c7aa1')
ACCENT_2 = colors.HexColor('#b8485b')
TEXT_PRIMARY = colors.HexColor('#1f2223')
TEXT_MUTED = colors.HexColor('#848a8d')
TABLE_STRIPE = colors.HexColor('#e8ebed')

# ── Styles ──
toc_h0 = ParagraphStyle('TOC0', fontName='FreeSerif-Bold', fontSize=12, leading=20, leftIndent=0, spaceBefore=6)
toc_h1 = ParagraphStyle('TOC1', fontName='FreeSerif', fontSize=10.5, leading=18, leftIndent=20, spaceBefore=2)

h1 = ParagraphStyle('H1', fontName='FreeSerif-Bold', fontSize=18, leading=24, spaceBefore=24, spaceAfter=12, textColor=HEADER_FILL, keepWithNext=True)
h2 = ParagraphStyle('H2', fontName='FreeSerif-Bold', fontSize=14, leading=20, spaceBefore=18, spaceAfter=8, textColor=TEXT_PRIMARY, keepWithNext=True)
h3 = ParagraphStyle('H3', fontName='FreeSerif-Bold', fontSize=11.5, leading=16, spaceBefore=12, spaceAfter=6, textColor=TEXT_PRIMARY, keepWithNext=True)
body = ParagraphStyle('Body', fontName='FreeSerif', fontSize=10.5, leading=17, alignment=TA_JUSTIFY, spaceAfter=6, textColor=TEXT_PRIMARY)
body_indent = ParagraphStyle('BodyIndent', parent=body, leftIndent=18, firstLineIndent=0)
caption_style = ParagraphStyle('Caption', fontName='FreeSerif-Italic', fontSize=9, leading=13, alignment=TA_CENTER, spaceAfter=6, textColor=TEXT_MUTED)
th = ParagraphStyle('TH', fontName='FreeSerif-Bold', fontSize=9, leading=13, alignment=TA_CENTER, textColor=colors.white)
td = ParagraphStyle('TD', fontName='FreeSerif', fontSize=9, leading=13, alignment=TA_LEFT, textColor=TEXT_PRIMARY)

# ── TocDocTemplate ──
class TocDocTemplate(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        SimpleDocTemplate.__init__(self, *args, **kwargs)
        self._page_bookmarks = []
    
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))
            self._page_bookmarks.append((key, self.page))
    
    def afterPage(self):
        canvas = self.canv
        for key, _ in self._page_bookmarks:
            try:
                canvas.bookmarkPage(key)
            except:
                pass
        self._page_bookmarks.clear()

# ── Helpers ──
def heading(text, style, level=0):
    key = hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph(text, style)
    p.bookmark_name = key
    p.bookmark_level = level
    p.bookmark_text = text
    p.bookmark_key = key
    return p

def p(text):
    return Paragraph(text, body)

def p2(text):
    return Paragraph(text, body_indent)

def make_table(headers, rows, col_widths=None):
    w = col_widths or [460/len(headers)]*len(headers)
    data = [[Paragraph(h, th) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), td) for c in row])
    t = Table(data, colWidths=w)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_FILL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
    ]
    for i in range(2, len(data), 2):
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), TABLE_STRIPE))
    t.setStyle(TableStyle(style_cmds))
    return t

def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('FreeSerif', 8)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawCentredString(A4[0]/2, 30, str(canvas.getPageNumber()))
    canvas.restoreState()

# ── Build Document ──
OUTPUT = '/home/z/my-project/download/Averon_Technical_Book.pdf'
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

doc = TocDocTemplate(OUTPUT, pagesize=A4, topMargin=2*cm, bottomMargin=2.5*cm, leftMargin=2.5*cm, rightMargin=2.5*cm)
story = []

# ── TOC ──
toc = TableOfContents()
toc.levelStyles = [toc_h0, toc_h1]
story.append(Paragraph('<b>Table of Contents</b>', ParagraphStyle('TOCTitle', fontName='FreeSerif-Bold', fontSize=20, leading=28, alignment=TA_CENTER, spaceAfter=18, textColor=HEADER_FILL)))
story.append(Spacer(1, 12))
story.append(toc)
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# CHAPTER 1: Introduction to Asset Tokenization
# ═══════════════════════════════════════════════════════════════
story.append(heading('Chapter 1: Introduction to Asset Tokenization', h1, 0))

story.append(heading('1.1 The Evolution of Digital Assets', h2, 1))
story.append(p(
    'The concept of representing ownership through digital means has evolved dramatically over the past two decades, '
    'from the introduction of Bitcoin in 2009 as a purely digital store of value to today\'s sophisticated platforms '
    'that bridge the gap between physical real-world assets and digital blockchain-based tokens. Asset tokenization '
    'refers to the process of creating digital tokens on a blockchain that represent ownership rights, economic benefits, '
    'or other entitlements linked to tangible or intangible assets. These assets can range from real estate properties '
    'and agricultural land to accounts receivable, commodities, intellectual property, and equity stakes in private companies. '
    'The fundamental value proposition of tokenization lies in its ability to divide traditionally illiquid, large-denomination '
    'assets into smaller, tradable units, thereby democratizing access to investment opportunities that were previously '
    'available only to wealthy individuals or institutional investors.'
))
story.append(p(
    'The tokenization market has experienced exponential growth in recent years, driven by three converging forces: '
    'technological maturation of blockchain platforms, increasing regulatory clarity in major jurisdictions, and growing '
    'institutional adoption of digital asset infrastructure. According to industry estimates, the total value of tokenized '
    'real-world assets is projected to reach approximately $16 trillion by 2030, up from approximately $310 billion in 2023. '
    'This growth trajectory reflects a fundamental shift in how financial markets operate, moving from centralized, '
    'intermediary-heavy processes to decentralized, blockchain-based settlement and custody solutions. The implications extend '
    'beyond simple efficiency gains: tokenization has the potential to reshape capital markets by reducing settlement times '
    'from days to seconds, eliminating counterparty risk through smart contract automation, and enabling continuous '
    'rather than discrete market operations.'
))

story.append(heading('1.2 Motivation and Problem Statement', h2, 1))
story.append(p(
    'Despite the promise of asset tokenization, existing platforms face several critical technical and operational '
    'challenges that limit their adoption and effectiveness. First, most platforms operate on public blockchain networks '
    'such as Ethereum, which introduces significant transaction costs (gas fees) that make micro-investments economically '
    'unviable. A single Ethereum transaction can cost anywhere from $1 to $50 depending on network congestion, which is '
    'prohibitive for the small-denomination investments that are the core value proposition of fractional asset ownership. '
    'Second, the reliance on public blockchains exposes transaction details to all network participants, creating privacy '
    'concerns for asset owners who may not wish to disclose investment amounts, investor identities, or asset valuations '
    'to the public. Third, existing systems treat the various components of the tokenization lifecycle -- asset verification, '
    'capital raising, secondary market trading, and fee collection -- as separate, loosely-coupled services, resulting in '
    'data inconsistency, increased latency, and a fragmented user experience.'
))
story.append(p(
    'Additionally, the verification of underlying asset documentation typically relies on manual review by compliance '
    'officers, a process that is slow (taking days to weeks), expensive (requiring trained professionals), and susceptible '
    'to human error or bias. The integration between primary market capital raising (where investors fund tokenized assets) '
    'and secondary market trading (where investors trade tokens among themselves) is often weak or non-existent, forcing users '
    'to navigate multiple platforms to complete the full investment lifecycle. Price discovery for platform tokens is frequently '
    'delegated to external oracle services or simple order books without algorithmic support, leading to price volatility and '
    'market manipulation vulnerabilities. Averon v4.0.0 was designed to address all of these challenges through a unified, '
    'vertically-integrated platform architecture.'
))

story.append(heading('1.3 The Averon Solution', h2, 1))
story.append(p(
    'Averon v4.0.0 is a comprehensive asset tokenization platform that integrates five core technical components into a '
    'unified architecture: a custom proof-of-work blockchain, an AI-powered document verification pipeline, an on-chain escrow '
    'mechanism, a centralized trading engine, and an algorithmic price discovery model. The platform enables asset owners to '
    'create digital tokens representing fractional ownership of real-world assets, investors to purchase these tokens through '
    'a regulated funding process with built-in escrow protection, and all participants to trade tokens on a secondary market '
    'with on-chain settlement. The custom blockchain eliminates gas fees and provides data privacy, while the AI pipeline '
    'automates the document verification process that traditionally requires manual review. This book provides a comprehensive '
    'technical deep dive into every component of the Averon platform, from the cryptographic foundations of the blockchain '
    'engine to the economic model that governs token pricing and platform sustainability.'
))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 2: Platform Architecture Overview
# ═══════════════════════════════════════════════════════════════
story.append(heading('Chapter 2: Platform Architecture Overview', h1, 0))

story.append(heading('2.1 Architectural Principles', h2, 1))
story.append(p(
    'The architecture of Averon v4.0.0 is guided by several key design principles that influence every technical '
    'decision in the system. The first principle is vertical integration: rather than composing the platform from '
    'independent microservices communicating over network protocols, Averon implements all core functionality within '
    'a single monolithic application. This design choice eliminates inter-service communication overhead, simplifies '
    'deployment and monitoring, and ensures data consistency through shared memory access rather than distributed '
    'transactions. The second principle is blockchain-native design: the custom blockchain is not an add-on or external '
    'dependency but a foundational component that is deeply integrated with the platform\'s business logic, with '
    'specialized transaction types that directly correspond to platform operations.'
))
story.append(p(
    'The third principle is defense-in-depth security: the platform implements multiple overlapping security mechanisms '
    'at different layers, including network-level rate limiting, application-level authentication and authorization, '
    'data-level input sanitization, and operational-level audit logging with hash-chain integrity verification. The '
    'fourth principle is regulatory awareness: while the platform is not tied to any specific jurisdiction\'s regulatory '
    'framework, the architecture is designed to support compliance requirements such as KYC verification tiers, '
    'document-based asset verification, and transparent transaction auditing that would satisfy regulators in most '
    'jurisdictions. The fifth principle is progressive complexity: the system is designed so that users can interact '
    'with basic functionality (registration, browsing, simple trades) with minimal friction, while advanced features '
    '(asset creation, compliance review, administrative operations) require progressively higher levels of verification '
    'and authorization.'
))

story.append(heading('2.2 Five-Layer Architecture', h2, 1))
story.append(p(
    'The system is organized into five principal layers, each with clearly defined responsibilities and interfaces. '
    'The Security Layer (Layer 5) sits at the top of the request processing pipeline and is the first point of contact '
    'for all incoming HTTP requests. It implements JWT-based authentication, token-bucket rate limiting with three tiers, '
    'input sanitization, and audit logging. The Application Layer (Layer 4) implements the business logic for all platform '
    'operations, including asset management, trading engine, payment processing, and user administration, exposed through '
    'RESTful API endpoints. The AI Processing Layer (Layer 3) implements the five-stage document analysis pipeline for '
    'automated asset verification. The Data Layer (Layer 2) provides persistent storage through a SQLite relational database '
    'with 19 interconnected tables and the blockchain\'s chain.json file. The Blockchain Layer (Layer 1) provides the '
    'immutable ledger infrastructure, including the custom proof-of-work mining engine, transaction pool management, '
    'and chain storage subsystem.'
))
story.append(p(
    'This layered architecture provides clear separation of concerns, making the system easier to understand, test, '
    'and maintain. Each layer communicates with adjacent layers through well-defined interfaces, and the dependencies '
    'flow downward: the Application Layer depends on the Data Layer and Blockchain Layer but not on the AI Processing '
    'Layer (which is invoked asynchronously). The Security Layer is orthogonal to the others, processing all requests '
    'before they reach the Application Layer regardless of which lower layers are involved in fulfilling the request.'
))

story.append(heading('2.3 Technology Stack', h2, 1))
story.append(p(
    'Averon v4.0.0 is implemented as a monolithic Node.js application, leveraging the V8 JavaScript engine\'s event-driven, '
    'non-blocking I/O model to handle concurrent requests efficiently. The web framework is Express.js, which provides '
    'middleware composition, routing, and request/response handling. The database is SQLite, selected for its zero-configuration '
    'deployment, transactional integrity (full ACID compliance), and suitability for single-server applications that do not '
    'require horizontal scaling. The blockchain engine is implemented as a custom Node.js module that runs the proof-of-work '
    'mining process asynchronously within the event loop. Cryptographic operations utilize the built-in Node.js crypto module '
    'for ECDSA signature operations and the crypto-js library for SHA-256 hashing. The AI document analysis pipeline utilizes '
    'pre-trained machine learning models for OCR, text classification, and named entity recognition.'
))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 3: Blockchain Engine
# ═══════════════════════════════════════════════════════════════
story.append(heading('Chapter 3: Custom Blockchain Engine', h1, 0))

story.append(heading('3.1 Design Rationale for a Custom Blockchain', h2, 1))
story.append(p(
    'The decision to implement a custom blockchain rather than deploying on an existing public network was driven by '
    'three specific technical requirements. First, Averon requires specialized transaction types that directly correspond '
    'to platform operations (INVEST, DIVEST, PAYOUT, REFUND, ASSET_CREATE) that have no equivalent in standard blockchain '
    'protocols. While these could theoretically be implemented as smart contracts on Ethereum or similar platforms, the '
    'associated gas costs would make micro-investments economically unviable. Second, the platform requires zero transaction '
    'fees to enable investments as small as 100 INR (approximately $1.20 USD), which is impossible on networks that charge '
    'per-transaction fees. Third, the platform requires data privacy: investment amounts, investor identities, and asset '
    'valuations should not be publicly visible on a shared ledger, which is fundamentally incompatible with the transparent '
    'nature of public blockchains. The custom blockchain addresses all three requirements while maintaining the security '
    'properties (immutability, cryptographic integrity, auditability) that make blockchain technology valuable.'
))

story.append(heading('3.2 Cryptographic Foundations', h2, 1))
story.append(p(
    'The blockchain employs two primary cryptographic primitives: ECDSA secp256k1 for digital signatures and SHA-256 '
    'for hashing. The secp256k1 elliptic curve is defined by the equation y<super>2</super> = x<super>3</super> + 7 '
    'over a finite field of prime order. This is the same curve used by Bitcoin, providing approximately 128 bits of '
    'security, which means an attacker would need to perform approximately 2<super>128</super> operations to forge a '
    'signature. Each transaction is signed by the sender\'s private key, and the signature can be verified by anyone '
    'with access to the sender\'s public key and the transaction data, ensuring non-repudiation and transaction authenticity. '
    'The SHA-256 hash function produces a 256-bit digest from arbitrary-length input, and is used for computing transaction '
    'hashes (serving as unique identifiers), block hashes (for linking blocks into a chain), and Merkle roots (for '
    'efficient transaction verification within blocks). The combination of ECDSA signatures and SHA-256 hashing provides '
    'a robust security foundation that protects against forgery, tampering, and replay attacks.'
))

story.append(heading('3.3 Block and Transaction Structure', h2, 1))
story.append(p(
    'Each block in the Averon blockchain contains a Merkle root computed from all included transactions, a reference to '
    'the previous block\'s hash (creating the chain structure), a nonce value determined through the proof-of-work mining '
    'process, a difficulty parameter that governs the mining complexity, a timestamp, and the array of transactions. The '
    'Merkle tree structure enables efficient verification of individual transactions: to verify that a specific transaction '
    'is included in a block, one needs only the Merkle path (approximately log<super>2</super>(n) hashes for n transactions) '
    'rather than the full block data. Each transaction contains a SHA-256 hash, an ECDSA secp256k1 signature, a type '
    'identifier (one of eight types), sender and recipient addresses, an amount, a timestamp, and a type-specific payload.'
))

story.append(heading('3.4 Transaction Types', h2, 1))
story.append(p(
    'The platform defines eight distinct transaction types, each serving a specific function within the asset tokenization '
    'lifecycle. These types represent a key innovation over generic blockchain systems, as they encode business logic directly '
    'into the transaction protocol, eliminating the need for smart contract interpretation layers.'
))
story.append(Spacer(1, 8))
story.append(make_table(
    ['Type', 'Description', 'Direction'],
    [
        ['MINT', 'Token creation from fiat purchase', 'System to User'],
        ['TRANSFER', 'User-to-user or user-to-system transfer', 'Peer-to-Peer'],
        ['INVEST', 'Locking funds for asset token purchase', 'User to Escrow'],
        ['DIVEST', 'Early exit from an active investment', 'Escrow to User'],
        ['PAYOUT', 'Release funds to asset owner upon full funding', 'Escrow to Owner'],
        ['REFUND', 'Return funds when asset expires', 'Escrow to Investors'],
        ['FEE', 'Platform fee collection', 'User to Platform'],
        ['ASSET_CREATE', 'Record asset tokenization on chain', 'System'],
    ],
    [80, 240, 140]
))
story.append(Paragraph('<b>Table 3.1:</b> Transaction types in the Averon blockchain', caption_style))
story.append(Spacer(1, 8))

story.append(heading('3.5 Proof-of-Work Mining', h2, 1))
story.append(p(
    'The proof-of-work mining process involves finding a nonce value such that the SHA-256 hash of the block header '
    '(comprising the previous block hash, Merkle root, timestamp, difficulty target, and nonce) is below the difficulty '
    'target. The difficulty is dynamically adjusted based on the mining rate to maintain a consistent block generation '
    'interval. In the single-miner architecture of Averon, the mining process runs asynchronously within the Node.js '
    'event loop, processing transactions from the pending pool and constructing new blocks. When a valid nonce is found, '
    'the block is added to the chain, stored in chain.json, and the mining process begins work on the next block. The '
    'entire chain is stored in a structured JSON format that supports human-readable inspection, straightforward backup '
    'procedures, and efficient loading at application startup.'
))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 4: Database Architecture
# ═══════════════════════════════════════════════════════════════
story.append(heading('Chapter 4: Database Architecture', h1, 0))

story.append(heading('4.1 SQLite as the Data Store', h2, 1))
story.append(p(
    'Averon uses SQLite as its relational database engine, a choice that reflects the platform\'s single-server deployment '
    'model and its prioritization of operational simplicity over horizontal scalability. SQLite is a serverless, '
    'self-contained database engine that stores the entire database in a single cross-platform file, requires no '
    'configuration or administration, supports full ACID transactions, and provides excellent read performance for '
    'workloads that are predominantly read-oriented (as is typical for web platforms). The database file persists all '
    'relational data, while the blockchain state is maintained separately in chain.json, creating a clean separation '
    'between mutable relational state and immutable blockchain state.'
))

story.append(heading('4.2 Schema Design and Table Relationships', h2, 1))
story.append(p(
    'The database schema comprises 19 tables organized into six functional groups. The user management group includes '
    'users (core user profiles with email, password hash, role, and KYC status), wallets (token balances and blockchain '
    'addresses), kyc_verifications (KYC tier progression and document references), and sessions (JWT token management). '
    'The asset management group includes assets (tokenized asset metadata and lifecycle state), asset_documents (uploaded '
    'files with SHA-256 hashes), and asset_tokens (per-asset token distribution records). The escrow group includes '
    'escrow_accounts (per-asset escrow balances and status) and escrow_transactions (individual LOCK/RELEASE/REFUND '
    'operations). The trading group includes coin_orders (the order book with side, type, amount, price, and status) and '
    'coin_trades (executed trades with buyer/seller fees and blockchain transaction hashes). The economic group includes '
    'economy (global metrics such as price, supply, market cap, and TVL), price_history (time-series price data), and '
    'fee_ledger (all collected fees with reference IDs). The payment group includes payment_gateways (provider configurations), '
    'payment_orders (fiat-to-crypto purchase records), and payment_transactions (gateway-level audit trail).'
))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 5: AI-Powered Document Verification
# ═══════════════════════════════════════════════════════════════
story.append(heading('Chapter 5: AI-Powered Document Verification', h1, 0))

story.append(heading('5.1 Overview of the Five-Stage Pipeline', h2, 1))
story.append(p(
    'The AI document verification pipeline represents one of the most innovative components of the Averon platform, '
    'enabling the automated analysis of asset documentation that is critical for regulatory compliance and investor '
    'protection. The pipeline processes user-uploaded documents through five sequential stages, each designed to extract '
    'progressively deeper levels of information. The system supports JPG, PNG, WebP, and PDF file formats with a maximum '
    'file size of 10MB per document, and each asset can have between 1 and 10 supporting documents. Files are stored '
    'in a dedicated directory (uploads/<assetId>/) with cryptographically randomized filenames to prevent unauthorized '
    'access, and SHA-256 hashes are computed for duplicate detection and integrity verification.'
))

story.append(heading('5.2 Stage 1: Image Preprocessing', h2, 1))
story.append(p(
    'The first stage applies a series of standard computer vision operations to prepare document images for reliable '
    'OCR processing. Noise reduction using Gaussian filtering removes random pixel noise that can confuse character '
    'recognition algorithms. Contrast enhancement using CLAHE (Contrast Limited Adaptive Histogram Equalization) improves '
    'the local contrast of document images, particularly beneficial for scanned documents with uneven lighting or fading. '
    'Skew correction using Hough transform-based line detection aligns the document image with the horizontal axis, '
    'correcting for camera angle or scanner misalignment. Binarization using Otsu\'s thresholding method converts the '
    'grayscale image to black-and-white, simplifying the OCR task by removing color information. These preprocessing '
    'steps are particularly important for mobile phone photographs, which often suffer from poor lighting, shadows, '
    'perspective distortion, and low resolution.'
))

story.append(heading('5.3 Stage 2: Optical Character Recognition', h2, 1))
story.append(p(
    'The OCR stage extracts raw text content from the preprocessed document images using a deep learning-based engine '
    'capable of handling multiple languages, fonts, and layout formats commonly encountered in legal and financial '
    'documents. The engine is trained on large-scale datasets of document images and their corresponding text transcripts, '
    'enabling it to recognize printed text, handwritten text (to a limited extent), text embedded in tables and forms, '
    'and text in multi-column layouts. The output of this stage is a structured text representation that preserves the '
    'reading order and, where possible, the layout hierarchy of the original document.'
))

story.append(heading('5.4 Stage 3: Text Classification', h2, 1))
story.append(p(
    'The classification stage analyzes the extracted text to determine the document type (property deed, financial statement, '
    'valuation report, identity document, etc.) and assesses its relevance to the asset being tokenized. This stage '
    'employs a transformer-based text classification model fine-tuned on a domain-specific corpus of financial and legal '
    'documents. The model outputs a probability distribution over the predefined document categories, and the highest-'
    'probability category is selected as the classification result. Documents classified as irrelevant to the asset '
    'type are flagged for manual review.'
))

story.append(heading('5.5 Stage 4: Named Entity Recognition', h2, 1))
story.append(p(
    'The information extraction stage uses named entity recognition (NER) to identify and extract structured data points '
    'from the unstructured text. The NER model is trained to recognize entity types specific to the asset tokenization '
    'domain, including asset addresses, monetary amounts, dates, legal entity names, registration numbers, property '
    'dimensions, and other relevant information. The extracted entities are stored in a structured format that can be '
    'cross-referenced with the asset metadata provided by the owner, enabling automated consistency checking.'
))

story.append(heading('5.6 Stage 5: Verification Scoring', h2, 1))
story.append(p(
    'The final stage aggregates the outputs of all preceding stages to produce a confidence score (0-100) and a binary '
    'recommendation (verified or rejected). The scoring algorithm weighs multiple factors: document completeness (are '
    'all required document types present?), information consistency (do the extracted entities match the asset metadata?), '
    'image quality (is the document legible?), and compliance indicators (are there any red flags such as expired documents '
    'or mismatched names?). The threshold for the verified recommendation is configurable but typically set at 60 out '
    'of 100, balancing the need for thorough verification with the practical requirement of not rejecting too many '
    'legitimate assets. Assets that receive a rejected recommendation are returned to the owner with specific feedback '
    'indicating which documents need to be improved or replaced.'
))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 6: Asset Lifecycle Management
# ═══════════════════════════════════════════════════════════════
story.append(heading('Chapter 6: Asset Lifecycle Management', h1, 0))

story.append(heading('6.1 The State Machine', h2, 1))
story.append(p(
    'The asset lifecycle is governed by a deterministic finite state machine that enforces business rules and regulatory '
    'requirements by restricting state transitions to predefined paths. This design prevents invalid operations, ensures '
    'that each asset follows the correct verification and funding process, and provides clear audit trail of all lifecycle '
    'events. The complete state transition sequence is: draft to documents_uploaded to ai_analyzing to verified (or rejected) '
    'to compliance_review to active to funding to funded (or expired) to payout_pending to completed (or, in the expired '
    'path, to refunding to closed). Each state transition is recorded in the database with a timestamp and the identity '
    'of the user or system component that triggered the transition.'
))

story.append(heading('6.2 Detailed State Descriptions', h2, 1))
story.append(p(
    'In the draft state, the asset owner provides essential metadata including the asset title, description, category '
    '(selected from 12 predefined categories), target raise amount (bounded between 100 INR and 1 Crore INR), and '
    'listing duration. Upon validation, the asset is inserted into the database. In the documents_uploaded state, the '
    'owner uploads supporting documents. The ai_analyzing state triggers the five-stage AI pipeline. Upon successful AI '
    'verification, the asset enters compliance_review for additional regulatory checks. The active state makes the asset '
    'visible to investors. During funding, investors purchase tokens through INVEST transactions. If the target is reached, '
    'the asset transitions to funded, then payout_pending, and completed as the escrow releases funds. If funding expires, '
    'the asset transitions to expired, triggering automatic REFUND transactions.'
))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 7: Escrow Mechanism
# ═══════════════════════════════════════════════════════════════
story.append(heading('Chapter 7: Escrow Mechanism', h1, 0))

story.append(heading('7.1 Per-Asset Escrow Accounts', h2, 1))
story.append(p(
    'The escrow mechanism is a critical component that enables trustless capital raising on the platform. Each tokenized '
    'asset has a dedicated escrow account identified by a unique blockchain address. When investors purchase asset tokens, '
    'the corresponding funds are locked in this escrow account through an atomic INVEST transaction. The escrow_accounts '
    'table tracks the per-asset balance, total received, total released, and total refunded amounts, providing a complete '
    'financial picture of the escrow at any point in time. The escrow_transactions table records each individual movement '
    'with a type (LOCK, RELEASE, or REFUND), the user identifier, the amount, and the corresponding blockchain transaction '
    'hash, creating an immutable audit trail of all escrow activity.'
))

story.append(heading('7.2 Payout and Refund Logic', h2, 1))
story.append(p(
    'When an asset reaches its target raise amount within the specified listing duration, the escrow executes the payout '
    'logic: the total locked amount minus the capital raise fee (1.0% of the raised amount) is released to the asset '
    'owner via a PAYOUT transaction recorded on the blockchain. This deduction ensures that the platform generates revenue '
    'from successful fundings, aligning the platform\'s economic interests with the success of the assets listed on it. '
    'If the asset fails to reach its funding target before the listing duration expires, the escrow executes the refund '
    'logic: all locked funds are returned to their respective investors via individual REFUND transactions. Each refund is '
    'processed atomically and recorded on the blockchain, ensuring that no investor funds are lost or misallocated.'
))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 8: Trading Engine
# ═══════════════════════════════════════════════════════════════
story.append(heading('Chapter 8: Trading Engine', h1, 0))

story.append(heading('8.1 Order Book Architecture', h2, 1))
story.append(p(
    'The trading engine provides secondary market liquidity for platform tokens through a centralized limit-order book. '
    'The engine supports both market orders (executed immediately at the best available price) and limit orders (executed '
    'only at or better than a specified price). Each user can maintain a maximum of 50 open orders simultaneously, preventing '
    'excessive order book bloat and ensuring manageable memory usage. The order book is stored in the coin_orders table '
    'with fields for user ID, side (buy/sell), type (market/limit), amount, price, filled amount, remaining amount, and '
    'status (open, partially_filled, filled, or cancelled).'
))

story.append(heading('8.2 Price-Time Priority Matching', h2, 1))
story.append(p(
    'The matching algorithm follows the price-time priority discipline, which is the de facto standard for financial '
    'exchanges worldwide. Buy orders (bids) are sorted by price in descending order (highest bid first), and sell orders '
    '(asks) are sorted by price in ascending order (lowest ask first). Ties at the same price level are broken by '
    'timestamp, with the earlier order receiving priority. When a new order arrives, the engine iterates through the '
    'opposite side of the order book, matching at each price level until the order is fully filled or no more matching '
    'prices are available. Unfilled limit orders are inserted into the book at their specified price level.'
))

story.append(heading('8.3 On-Chain Settlement and Double-Mint Prevention', h2, 1))
story.append(p(
    'Each executed trade generates a TRADE transaction recorded on the blockchain, including the buyer and seller addresses, '
    'trade amount, execution price, buyer fee (0.1%), seller fee (0.1%), and transaction hash. This on-chain settlement '
    'ensures immutability and public auditability. The double-mint prevention mechanism uses atomic database UPDATE '
    'operations with conditional WHERE clauses that lock the order record before processing, preventing concurrent requests '
    'from processing the same order multiple times. A second concurrent request attempting to process the same order '
    'receives zero affected rows and is rejected with an error.'
))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 9: Payment Integration
# ═══════════════════════════════════════════════════════════════
story.append(heading('Chapter 9: Payment Integration', h1, 0))

story.append(heading('9.1 Fiat-to-Crypto Purchase Flow', h2, 1))
story.append(p(
    'The payment integration system enables users to purchase platform tokens using fiat currency through third-party '
    'payment gateways. The system supports multiple payment providers, each configured in the payment_gateways table '
    'with their supported currencies, minimum and maximum transaction amounts, and fee schedules. When a user initiates '
    'a purchase, the system creates a payment_order record with the user ID, selected gateway, fiat amount, computed '
    'coin amount (based on the current platform price), exchange rate, and KYC tier. The payment_transactions table '
    'maintains a gateway-level audit trail with the gateway\'s own transaction ID and status, enabling reconciliation '
    'between the platform\'s records and the gateway\'s records.'
))

story.append(heading('9.2 Payment Verification and Minting', h2, 1))
story.append(p(
    'The payment verification process is designed to be both secure and idempotent. When a payment gateway confirms a '
    'successful payment, the system verifies the payment by querying the gateway\'s API with the transaction ID. Upon '
    'successful verification, the system uses an atomic UPDATE query with a WHERE clause that checks the order status '
    '(created or pending) to prevent double-minting. If the UPDATE affects exactly one row, the system proceeds to mint '
    'tokens by creating a MINT transaction on the blockchain and crediting the user\'s wallet. If the UPDATE affects zero '
    'rows (indicating the order was already processed), the system rejects the duplicate request with an error. This mechanism '
    'ensures that even if the gateway sends multiple confirmation callbacks for the same payment, only one minting occurs.'
))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 10: Algorithmic Price Discovery
# ═══════════════════════════════════════════════════════════════
story.append(heading('Chapter 10: Algorithmic Price Discovery', h1, 0))

story.append(heading('10.1 The Dual-Factor Pricing Formula', h2, 1))
story.append(p(
    'The platform token price is determined by a dual-factor algorithmic formula: P = P_initial x (1 + totalSupply/10000) '
    'x (1 + totalAssetsFunded x 0.04). The first factor introduces supply-based inflation: as more tokens are minted, the '
    'price appreciates gradually, incentivizing early participation. At 100,000 tokens in circulation, this factor equals 11.0. '
    'The second factor introduces a demand-based component tied to platform utility: each successfully funded asset increases '
    'the factor by 4%, reflecting the platform\'s ability to connect asset owners with investors. Together, these factors '
    'create a positive feedback loop where platform activity drives token appreciation, which in turn incentivizes further '
    'participation.'
))

story.append(heading('10.2 Asset Funding Boost', h2, 1))
story.append(p(
    'When an asset is fully funded, an additional price boost is applied using the formula: boost = min(5%, 2% + '
    'raiseAmount/1M x 3%). This creates a price event that rewards the platform community when assets are successfully '
    'funded, while capping the maximum boost at 5% to prevent excessive volatility. For small raises (e.g., 100,000 INR), '
    'the boost is approximately 2.3%; for large raises (e.g., 10,000,000 INR), the boost reaches the maximum of 5%. This '
    'mechanism creates a visible, predictable connection between real-world funding events and token price movements, '
    'reinforcing the narrative that platform tokens derive value from real economic activity rather than speculation alone.'
))

story.append(heading('10.3 Price History and Market Data', h2, 1))
story.append(p(
    'The price_history table records the token price at regular intervals for charting and analysis. Each record includes '
    'the price, volume, high, low, open, close, and timestamp, following the OHLCV format standard used in financial '
    'markets. This data is exposed through the blockchain info API endpoint and displayed on the platform\'s frontend '
    'as candlestick charts, line charts, and summary statistics. The price history also serves as input for the trading '
    'engine\'s market data feeds, enabling technical analysis indicators and historical performance comparisons.'
))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 11: Fee Structure and Economics
# ═══════════════════════════════════════════════════════════════
story.append(heading('Chapter 11: Fee Structure and Economics', h1, 0))

story.append(heading('11.1 Multi-Tiered Fee Model', h2, 1))
story.append(p(
    'The platform implements a multi-tiered fee structure that generates sustainable revenue while maintaining competitive '
    'trading costs. The five fee types are: trading fees (0.1% per trade, charged to both buyer and seller), asset listing '
    'fees (1.0 AC per asset, configurable), capital raise fees (1.0% of the raised amount, deducted from escrow payout), '
    'withdrawal fees (0.5 AC per withdrawal), and payment gateway fees (variable, deducted by the gateway). All fees are '
    'recorded in the fee_ledger table with the user ID, fee type, amount, and a reference ID linking to the originating '
    'transaction. The economy table aggregates fee data into a total_fees_collected metric for financial reporting.'
))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 12: API Design
# ═══════════════════════════════════════════════════════════════
story.append(heading('Chapter 12: API Design and Endpoints', h1, 0))

story.append(heading('12.1 RESTful Architecture', h2, 1))
story.append(p(
    'The platform exposes its functionality through a RESTful API built on the Express.js web framework. The API follows '
    'standard REST conventions: resources are identified by URL paths (e.g., /api/assets, /api/market/order), operations '
    'are indicated by HTTP methods (GET for reads, POST for creates, DELETE for cancellations), and responses use standard '
    'HTTP status codes (200 for success, 400 for client errors, 401 for unauthorized, 403 for forbidden, 500 for server '
    'errors). The API processes JSON request and response bodies with a 5MB payload limit. All endpoints pass through the '
    'security middleware pipeline before reaching the route handlers.'
))

story.append(heading('12.2 Endpoint Catalog', h2, 1))
story.append(p(
    'The API comprises 18 endpoints organized into functional groups. Authentication endpoints handle user registration, '
    'login, and token refresh. Wallet endpoints provide balance and transaction history queries. Asset endpoints support '
    'creation, listing, detail retrieval, document upload, AI analysis triggering, tokenization confirmation, and token '
    'purchase. Market endpoints expose the order book and support order placement and cancellation. Portfolio endpoints '
    'provide a consolidated view of the user\'s holdings. Blockchain endpoints expose chain statistics and recent blocks. '
    'Withdrawal endpoints support creation, history, and administrative processing. Payment endpoints support fiat-to-crypto '
    'purchases, verification, and refunds. Each endpoint is documented with its HTTP method, path, authentication '
    'requirement, and a description of its behavior and response format.'
))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 13: Security Architecture
# ═══════════════════════════════════════════════════════════════
story.append(heading('Chapter 13: Security Architecture', h1, 0))

story.append(heading('13.1 Defense-in-Depth Strategy', h2, 1))
story.append(p(
    'The security architecture implements a defense-in-depth strategy with multiple overlapping security mechanisms. The '
    'middleware pipeline processes every incoming HTTP request through a sequence of security checks: JSON body parsing '
    '(5MB limit), input sanitization (removes HTML tags, JavaScript code, and SQL patterns), general rate limiting '
    '(100 requests per 60 seconds per IP), and audit logging. Authentication uses JWT with Bearer scheme, supporting '
    'three middleware variants: authenticate (requires valid token), optionalAuth (attaches user if token present), and '
    'requireRole (checks user role). Rate limiting uses a token bucket algorithm with three tiers: general (100/60s), '
    'auth (10/60s), and financial (5/1s).'
))

story.append(heading('13.2 Audit Logging with Hash Chain', h2, 1))
story.append(p(
    'The audit logging system maintains a hash chain of all API requests in the audit_logs table. Each log entry includes '
    'the SHA-256 hash of the previous entry, creating a tamper-evident chain. Any modification to a historical entry would '
    'break the chain, making tampering immediately detectable through a chain integrity verification function. This mechanism '
    'provides a level of audit assurance that goes beyond simple log files, as it cryptographically binds each log entry '
    'to its predecessors, making undetected tampering computationally infeasible.'
))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 14: Deployment and Operations
# ═══════════════════════════════════════════════════════════════
story.append(heading('Chapter 14: Deployment and Operations', h1, 0))

story.append(heading('14.1 System Requirements', h2, 1))
story.append(p(
    'The platform requires a minimum of 2 CPU cores and 4GB of RAM for basic operation. The blockchain mining process '
    'is CPU-intensive, so additional cores improve block generation speed. Storage requirements depend on the expected '
    'chain length and database size: the chain.json file grows linearly with the number of blocks, while the SQLite '
    'database grows with the number of users, transactions, and assets. For a moderately active platform with 10,000 users '
    'and 100,000 transactions, the total storage requirement is approximately 5-10GB. The platform is deployed as a single '
    'Node.js process managed by a process supervisor such as PM2 or systemd, with regular backups of both the SQLite database '
    'file and the chain.json file to prevent data loss in case of hardware failure.'
))

story.append(heading('14.2 Monitoring and Maintenance', h2, 1))
story.append(p(
    'Operational monitoring covers several key metrics: blockchain health (chain length, mining rate, orphan block rate), '
    'trading engine performance (order book depth, trade throughput, matching latency), economic indicators (token price, '
    'market cap, TVL, fee revenue), and system health (CPU usage, memory usage, disk I/O, API response times). The economy '
    'table provides a real-time dashboard of key metrics including price, total supply, circulating supply, total raised in '
    'INR, market capitalization, and total value locked. Regular maintenance tasks include database compaction (to reclaim '
    'space from deleted rows), chain pruning (if necessary, to manage chain.json file size), and security patching of '
    'the Node.js runtime and system dependencies.'
))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 15: Future Directions
# ═══════════════════════════════════════════════════════════════
story.append(heading('Chapter 15: Future Directions', h1, 0))

story.append(heading('15.1 Proof-of-Stake Migration', h2, 1))
story.append(p(
    'The most significant planned improvement is the migration from proof-of-work to a proof-of-stake consensus mechanism. '
    'PoS would eliminate the energy-intensive mining process, reduce the environmental footprint of the platform, and enable '
    'faster block confirmation times. The migration would involve replacing the mining algorithm with a validator selection '
    'mechanism, where validators are chosen based on the amount of platform tokens they stake as collateral. Misbehaving '
    'validators would have their stake slashed (partially confiscated), providing an economic incentive for honest behavior. '
    'The PoS implementation would need to maintain backward compatibility with the existing chain history, requiring a '
    'coordinated upgrade process similar to Ethereum\'s Merge.'
))

story.append(heading('15.2 Cross-Chain Interoperability', h2, 1))
story.append(p(
    'Cross-chain interoperability would enable Averon tokens and asset records to be recognized and transferred to other '
    'blockchain networks, expanding the platform\'s reach and enabling integration with the broader DeFi ecosystem. This '
    'could be implemented through bridge protocols that lock tokens on the Averon chain and issue corresponding wrapped '
    'tokens on the target chain, or through more sophisticated approaches such as cross-chain message passing protocols '
    'that enable not just token transfers but also cross-chain verification of asset records and escrow states.'
))

story.append(heading('15.3 Decentralized Identity Integration', h2, 1))
story.append(p(
    'Integration with decentralized identity (DID) standards such as W3C DID and Verifiable Credentials would enhance the '
    'KYC verification process by enabling portable, user-controlled identity credentials that can be verified without '
    'relying on a centralized identity provider. Under this model, a user would obtain a verifiable credential from a '
    'trusted issuer (such as a bank or government agency) and present it to the Averon platform as proof of identity, '
    'eliminating the need for platform-specific KYC processes and enabling cross-platform identity portability.'
))

story.append(heading('15.4 Scalability and Microservices Architecture', h2, 1))
story.append(p(
    'While the current monolithic architecture is well-suited for the platform\'s current scale, future growth may '
    'require migration to a microservices architecture to enable horizontal scaling of individual components. The most '
    'computationally intensive components -- the blockchain mining engine, the AI document analysis pipeline, and the '
    'trading engine -- would be the first candidates for extraction into independent services. This migration would '
    'require implementing inter-service communication (likely via message queues), distributed transaction management, '
    'and service discovery. The modular design of the current codebase, with clear boundaries between components, '
    'would facilitate this migration while maintaining backward compatibility.'
))

# ── Build ──
doc.multiBuild(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(f"Book PDF generated: {OUTPUT}")
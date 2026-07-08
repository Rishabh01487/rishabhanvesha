#!/usr/bin/env python3
"""
Patent Application - Indian Patent Office Format
Title: System and Method for AI-Powered Asset Tokenization on a Custom Blockchain Platform
Jurisdiction: India (Indian Patents Act 1970)
"""

import os, sys, hashlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
import platform

# ── Font Setup ──
FONT_DIR = '/usr/share/fonts'
pdfmetrics.registerFont(TTFont('FreeSerif', f'{FONT_DIR}/truetype/freefont/FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Bold', f'{FONT_DIR}/truetype/freefont/FreeSerifBold.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Italic', f'{FONT_DIR}/truetype/freefont/FreeSerifItalic.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-BoldItalic', f'{FONT_DIR}/truetype/freefont/FreeSerifBoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', f'{FONT_DIR}/truetype/dejavu/DejaVuSansMono.ttf'))
registerFontFamily('FreeSerif', normal='FreeSerif', bold='FreeSerif-Bold', italic='FreeSerif-Italic', boldItalic='FreeSerif-BoldItalic')

# ── Cascade Palette ──
PAGE_BG       = colors.HexColor('#f3f4f4')
SECTION_BG    = colors.HexColor('#eff0f0')
CARD_BG       = colors.HexColor('#eceeef')
TABLE_STRIPE  = colors.HexColor('#f1f2f3')
HEADER_FILL   = colors.HexColor('#415864')
COVER_BLOCK   = colors.HexColor('#4b6c7c')
BORDER        = colors.HexColor('#c5ced3')
ICON          = colors.HexColor('#4f829c')
ACCENT        = colors.HexColor('#3194c6')
ACCENT_2      = colors.HexColor('#c54b5f')
TEXT_PRIMARY   = colors.HexColor('#131516')
TEXT_MUTED     = colors.HexColor('#747b7e')

# ── Styles ──
styles = getSampleStyleSheet()

title_style = ParagraphStyle('PatentTitle', fontName='FreeSerif-Bold', fontSize=16, leading=22, alignment=TA_CENTER, spaceAfter=12, textColor=TEXT_PRIMARY)
h1_style = ParagraphStyle('H1', fontName='FreeSerif-Bold', fontSize=13, leading=18, spaceBefore=18, spaceAfter=8, textColor=HEADER_FILL)
h2_style = ParagraphStyle('H2', fontName='FreeSerif-Bold', fontSize=11.5, leading=16, spaceBefore=14, spaceAfter=6, textColor=TEXT_PRIMARY)
h3_style = ParagraphStyle('H3', fontName='FreeSerif-Bold', fontSize=10.5, leading=15, spaceBefore=10, spaceAfter=5, textColor=TEXT_PRIMARY)
body_style = ParagraphStyle('Body', fontName='FreeSerif', fontSize=10.5, leading=17, alignment=TA_JUSTIFY, spaceAfter=6, textColor=TEXT_PRIMARY)
body_indent = ParagraphStyle('BodyIndent', fontName='FreeSerif', fontSize=10.5, leading=17, alignment=TA_JUSTIFY, spaceAfter=6, textColor=TEXT_PRIMARY, leftIndent=24, firstLineIndent=0)
claim_style = ParagraphStyle('Claim', fontName='FreeSerif', fontSize=10.5, leading=17, alignment=TA_JUSTIFY, spaceAfter=8, textColor=TEXT_PRIMARY, leftIndent=36, firstLineIndent=-36)
claim_dep_style = ParagraphStyle('ClaimDep', fontName='FreeSerif', fontSize=10.5, leading=17, alignment=TA_JUSTIFY, spaceAfter=8, textColor=TEXT_PRIMARY, leftIndent=54, firstLineIndent=-18)
abstract_style = ParagraphStyle('Abstract', fontName='FreeSerif-Italic', fontSize=10, leading=16, alignment=TA_JUSTIFY, spaceAfter=6, textColor=TEXT_PRIMARY, leftIndent=24, rightIndent=24)
footer_style = ParagraphStyle('Footer', fontName='FreeSerif', fontSize=8, leading=11, alignment=TA_CENTER, textColor=TEXT_MUTED)
caption_style = ParagraphStyle('Caption', fontName='FreeSerif-Italic', fontSize=9, leading=13, alignment=TA_CENTER, spaceAfter=6, textColor=TEXT_MUTED)
table_header_style = ParagraphStyle('TableHeader', fontName='FreeSerif-Bold', fontSize=9.5, leading=14, alignment=TA_CENTER, textColor=colors.white)
table_cell_style = ParagraphStyle('TableCell', fontName='FreeSerif', fontSize=9.5, leading=14, alignment=TA_LEFT, textColor=TEXT_PRIMARY)

# ── Helper Functions ──
def add_heading(text, level=1):
    style = {1: h1_style, 2: h2_style, 3: h3_style}.get(level, body_style)
    return Paragraph(text, style)

def add_body(text):
    return Paragraph(text, body_style)

def add_claim(number, text, dependent=False):
    prefix = f"<b>{number}.</b> "
    style = claim_dep_style if dependent else claim_style
    return Paragraph(prefix + text, style)

# ── Page Number Footer ──
def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('FreeSerif', 8)
    canvas.setFillColor(TEXT_MUTED)
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.drawCentredString(A4[0]/2, 30, text)
    canvas.restoreState()

# ── Build Document ──
OUTPUT = '/home/z/my-project/download/Averon_Patent_Application_IPO.pdf'
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    topMargin=1.8*cm, bottomMargin=2*cm, leftMargin=2.5*cm, rightMargin=2.5*cm
)

story = []

# ═══════════════════════════════════════════════════════════
# TITLE PAGE
# ═══════════════════════════════════════════════════════════
story.append(Spacer(1, 60))
story.append(Paragraph("PATENT APPLICATION", ParagraphStyle('DocType', fontName='FreeSerif', fontSize=12, leading=16, alignment=TA_CENTER, textColor=TEXT_MUTED, spaceAfter=6)))
story.append(Spacer(1, 20))

title_text = (
    "System and Method for AI-Powered Asset Tokenization "
    "on a Custom Blockchain Platform with Integrated Escrow, "
    "Trading Engine, and Algorithmic Price Discovery"
)
story.append(Paragraph(title_text, title_style))
story.append(Spacer(1, 30))

# Applicant / Inventor details table
details_data = [
    [Paragraph("<b>Applicant:</b>", table_cell_style), Paragraph("Averon Technologies Private Limited", table_cell_style)],
    [Paragraph("<b>Inventor:</b>", table_cell_style), Paragraph("[Inventor Name]", table_cell_style)],
    [Paragraph("<b>Filing Date:</b>", table_cell_style), Paragraph("[Date of Filing]", table_cell_style)],
    [Paragraph("<b>Application No.:</b>", table_cell_style), Paragraph("[To be assigned by IPO]", table_cell_style)],
    [Paragraph("<b>Classification:</b>", table_cell_style), Paragraph("G06F 21/62, G06Q 40/04, G06Q 20/38, G06N 20/00", table_cell_style)],
    [Paragraph("<b>Jurisdiction:</b>", table_cell_style), Paragraph("India (Indian Patents Act, 1970)", table_cell_style)],
]

details_table = Table(details_data, colWidths=[120, 340])
details_table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LINEBELOW', (0, 0), (-1, -1), 0.5, BORDER),
]))
story.append(details_table)

story.append(Spacer(1, 40))
story.append(Paragraph(
    "<i>This patent application is filed under the provisions of the Indian Patents Act, 1970, "
    "and the Patents Rules, 2003 (as amended). All rights reserved.</i>",
    ParagraphStyle('Disclaimer', fontName='FreeSerif-Italic', fontSize=9, leading=14, alignment=TA_CENTER, textColor=TEXT_MUTED)
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════
# SECTION 1: ABSTRACT
# ═══════════════════════════════════════════════════════════
story.append(add_heading("ABSTRACT"))
story.append(Spacer(1, 6))

abstract_text = (
    "The present invention relates to a comprehensive system and method for real-world asset tokenization "
    "using a custom-built blockchain infrastructure integrated with artificial intelligence-powered document "
    "verification, an automated escrow mechanism, a centralized limit-order trading engine, and a dynamic "
    "algorithmic price discovery model. The system enables asset owners to create digital tokens representing "
    "fractional ownership of real-world assets through a multi-stage lifecycle that includes AI-driven document "
    "analysis, compliance review, and on-chain tokenization. The platform employs a custom proof-of-work blockchain "
    "utilizing SHA-256 hashing and ECDSA secp256k1 cryptographic signatures, supporting eight distinct transaction "
    "types including MINT, TRANSFER, INVEST, DIVEST, PAYOUT, REFUND, FEE, and ASSET_CREATE. The trading engine "
    "implements price-time priority order matching with atomic settlement recorded on the blockchain ledger. "
    "The price discovery model incorporates both supply-based and asset-funding-based adjustment factors, "
    "computing a dynamic token price that reflects platform economic activity. The system further includes "
    "a multi-tiered security model comprising JWT-based authentication, token-bucket rate limiting, "
    "input sanitization, audit logging with hash-chain integrity verification, and double-mint prevention "
    "through atomic database operations. The invention finds particular application in the fields of "
    "financial technology, decentralized finance (DeFi), and regulatory-compliant digital asset management."
)
story.append(Paragraph(abstract_text, abstract_style))
story.append(Spacer(1, 12))

# ═══════════════════════════════════════════════════════════
# SECTION 2: FIELD OF THE INVENTION
# ═══════════════════════════════════════════════════════════
story.append(add_heading("FIELD OF THE INVENTION"))

story.append(add_body(
    "This invention relates to the field of financial technology (fintech), and more particularly to systems, "
    "methods, and computer-readable media for the tokenization of real-world assets on a blockchain-based platform. "
    "Specifically, the invention encompasses the integration of artificial intelligence for automated asset "
    "verification, a custom proof-of-work blockchain for immutable transaction recording, an escrow-based "
    "investment mechanism for capital raising, a centralized order-matching trading engine for secondary market "
    "liquidity, and an algorithmic pricing model for dynamic token valuation. The invention addresses the "
    "technical challenges of combining on-chain immutability with off-chain compliance requirements, thereby "
    "enabling regulated asset tokenization in jurisdictions requiring documented verification of underlying assets."
))

story.append(add_body(
    "The intersection of blockchain technology and traditional financial instruments has given rise to a new "
    "paradigm known as real-world asset (RWA) tokenization. This paradigm involves the creation of digital "
    "tokens on a distributed ledger that represent ownership rights, economic benefits, or other entitlements "
    "linked to physical or financial assets such as real estate, commodities, receivables, or equity stakes "
    "in private companies. The technical challenges in this domain are multifaceted, spanning cryptographic "
    "security, regulatory compliance, market microstructure design, and user experience. The present invention "
    "provides an integrated solution that addresses these challenges within a single unified platform architecture, "
    "thereby advancing the state of the art in asset tokenization technology."
))

# ═══════════════════════════════════════════════════════════
# SECTION 3: BACKGROUND OF THE INVENTION
# ═══════════════════════════════════════════════════════════
story.append(add_heading("BACKGROUND OF THE INVENTION"))

story.append(add_heading("3.1 Conventional Asset Tokenization Approaches", 2))

story.append(add_body(
    "Existing asset tokenization platforms typically operate on public blockchain networks such as Ethereum, "
    "Binance Smart Chain, or Polygon, utilizing smart contracts to mint and manage tokenized representations "
    "of real-world assets. These approaches suffer from several technical limitations. First, reliance on "
    "public blockchains introduces scalability constraints, as transaction throughput is limited by the "
    "blockchain's consensus mechanism, often resulting in high gas fees and delayed confirmation times that "
    "are unsuitable for high-frequency trading operations. Second, public blockchains expose transaction "
    "details to all network participants, creating privacy concerns for asset owners who may not wish to "
    "disclose investment amounts, investor identities, or asset valuations to the public. Third, the "
    "open-ended nature of smart contract code on public networks increases the attack surface for "
    "vulnerabilities, as demonstrated by numerous high-profile exploits in the decentralized finance (DeFi) space."
))

story.append(add_body(
    "Alternative approaches have employed permissioned or private blockchain networks to address privacy "
    "and scalability concerns. However, these solutions typically lack the native trading infrastructure, "
    "algorithmic price discovery, and integrated escrow mechanisms necessary for a complete asset tokenization "
    "lifecycle. They often require external integration with centralized exchanges or over-the-counter (OTC) "
    "markets for secondary trading, introducing counterparty risk and operational complexity. Furthermore, "
    "existing systems generally lack automated, AI-driven verification of asset documentation, relying instead "
    "on manual review processes that are slow, expensive, and prone to human error or bias."
))

story.append(add_heading("3.2 Limitations of Prior Art", 2))

story.append(add_body(
    "Several technical deficiencies exist in the prior art that the present invention seeks to overcome. "
    "First, there is no known system that integrates a purpose-built proof-of-work blockchain with a "
    "five-stage AI document analysis pipeline, an automated escrow mechanism for capital raising, and a "
    "price-time priority trading engine within a single unified architecture. Existing systems treat these "
    "as separate components requiring manual orchestration, leading to data inconsistency, increased latency, "
    "and a fragmented user experience."
))

story.append(add_body(
    "Second, existing price discovery mechanisms for tokenized assets are typically limited to simple "
    "supply-demand curves or oracle-based external price feeds. These approaches fail to account for the "
    "unique economic dynamics of a tokenization platform, where the relationship between token supply, "
    "asset funding activity, and market liquidity creates complex feedback loops that require a more "
    "sophisticated pricing model. The present invention introduces a dual-factor pricing formula that "
    "incorporates both supply-based inflation and asset-funding-based demand signals, providing a more "
    "accurate and responsive price discovery mechanism."
))

story.append(add_body(
    "Third, the integration of an on-chain escrow system with an asset lifecycle state machine represents "
    "a novel technical contribution. In existing systems, escrow functionality, when present, is implemented "
    "as an external smart contract or third-party service, leading to additional trust assumptions, "
    "transaction costs, and potential points of failure. The present invention embeds the escrow mechanism "
    "directly within the platform's transaction type system, enabling atomic INVEST, DIVEST, PAYOUT, and "
    "REFUND operations that are recorded immutably on the blockchain ledger."
))

# ═══════════════════════════════════════════════════════════
# SECTION 4: SUMMARY OF THE INVENTION
# ═══════════════════════════════════════════════════════════
story.append(add_heading("SUMMARY OF THE INVENTION"))

story.append(add_body(
    "The present invention provides a comprehensive system and method for real-world asset tokenization "
    "that overcomes the limitations of prior art by integrating five core technical components into a "
    "unified platform architecture. These components are: (i) a custom proof-of-work blockchain engine "
    "with eight specialized transaction types, (ii) a five-stage artificial intelligence pipeline for "
    "automated asset document verification, (iii) an on-chain escrow mechanism with automated payout "
    "and refund logic, (iv) a centralized order-matching trading engine with price-time priority execution, "
    "and (v) a dual-factor algorithmic price discovery model."
))

story.append(add_body(
    "The blockchain engine employs SHA-256 proof-of-work mining with dynamic difficulty adjustment and "
    "stores the complete chain in a structured JSON format (chain.json). Each block contains a Merkle root "
    "computed from all included transactions, a reference to the previous block's hash, a nonce value "
    "determined through the mining process, and a difficulty parameter governing the mining complexity. "
    "Transactions are signed using ECDSA secp256k1 elliptic curve cryptography, providing a 128-bit "
    "security level that is computationally infeasible to break with current or foreseeable computing "
    "technology. The system supports eight distinct transaction types (MINT, TRANSFER, INVEST, DIVEST, "
    "PAYOUT, REFUND, FEE, and ASSET_CREATE), each serving a specific function within the asset tokenization "
    "lifecycle."
))

story.append(add_body(
    "The AI document analysis pipeline processes uploaded asset documents through five sequential stages: "
    "image preprocessing and enhancement, optical character recognition (OCR) for text extraction from "
    "scanned documents, text classification and categorization, key information extraction using named "
    "entity recognition, and a final verification scoring stage that produces a confidence score and "
    "recommendation (verified or rejected). This pipeline enables the automated verification of property "
    "deeds, financial statements, valuation reports, and other supporting documentation without requiring "
    "manual review, thereby significantly reducing the time and cost associated with asset onboarding."
))

story.append(add_body(
    "The escrow mechanism operates on a per-asset basis, with each tokenized asset having a dedicated "
    "escrow account identified by a unique blockchain address. When investors purchase asset tokens, "
    "the corresponding funds are locked in the escrow account through an atomic INVEST transaction recorded "
    "on the blockchain. Upon successful funding of the asset, the escrow releases the total locked amount "
    "minus a platform fee (typically 1.0% of the raised amount) to the asset owner via a PAYOUT transaction. "
    "If the asset fails to reach its funding target within the specified duration, the escrow automatically "
    "processes REFUND transactions to return funds to all investors. This mechanism eliminates counterparty "
    "risk and ensures that investor funds are protected throughout the funding period."
))

story.append(add_body(
    "The trading engine implements a centralized limit-order book with price-time priority matching. "
    "Users can place both market orders (executed immediately at the best available price) and limit orders "
    "(executed only at or better than a specified price). The engine matches buy and sell orders based on "
    "price priority (best price first) and time priority (earliest order at the same price level first), "
    "following the standard price-time priority discipline used in established financial exchanges. Each "
    "executed trade is recorded on the blockchain as a TRADE transaction, providing an immutable audit trail "
    "of all secondary market activity. The engine enforces balance verification against the blockchain "
    "before order placement, preventing the creation of orders that exceed the user's available token balance."
))

story.append(add_body(
    "The algorithmic price discovery model computes the platform token price using a dual-factor formula: "
    "P = P_initial x (1 + totalSupply/10000) x (1 + totalAssetsFunded x 0.04), where P_initial is the "
    "base token price, totalSupply represents the cumulative number of tokens minted on the platform, and "
    "totalAssetsFunded represents the cumulative number of assets that have successfully completed their "
    "funding period. This formula creates a positive feedback loop that aligns token value with platform "
    "activity: as more tokens are minted (indicating user adoption) and more assets are funded (indicating "
    "platform utility), the token price appreciates, incentivizing further participation in the ecosystem."
))

# ═══════════════════════════════════════════════════════════
# SECTION 5: DETAILED DESCRIPTION
# ═══════════════════════════════════════════════════════════
story.append(add_heading("DETAILED DESCRIPTION OF THE INVENTION"))

story.append(add_heading("5.1 System Architecture Overview", 2))

story.append(add_body(
    "The system architecture of the present invention is organized into five principal layers: the "
    "Blockchain Layer, the Application Layer, the Data Layer, the AI Processing Layer, and the Security "
    "Layer. The Blockchain Layer provides the immutable ledger infrastructure and includes the custom "
    "proof-of-work mining engine, transaction pool management, and chain storage subsystem. The Application "
    "Layer exposes RESTful API endpoints through an Express.js server and implements the business logic "
    "for asset management, trading, payment processing, and user administration. The Data Layer utilizes "
    "a SQLite relational database with nineteen interconnected tables that maintain the platform's state, "
    "including user accounts, wallets, assets, orders, trades, escrow records, and economic metrics. The AI "
    "Processing Layer implements the five-stage document analysis pipeline for automated asset verification. "
    "The Security Layer implements authentication, authorization, rate limiting, input sanitization, and "
    "audit logging middleware that processes all incoming HTTP requests before they reach the application logic."
))

story.append(add_body(
    "The system is deployed as a monolithic Node.js application with integrated blockchain mining, trading "
    "engine, and AI processing capabilities. While the monolithic architecture simplifies deployment and "
    "reduces inter-service communication overhead, the system is designed with clear module boundaries "
    "that would facilitate future migration to a microservices architecture if scalability requirements "
    "demand it. The blockchain storage is maintained in a JSON file (chain.json) that is periodically "
    "persisted to disk, while the relational data is stored in a SQLite database file that supports "
    "atomic transactions and referential integrity constraints."
))

story.append(add_heading("5.2 Blockchain Engine", 2))

story.append(add_body(
    "The blockchain engine is the foundational component of the system, providing an immutable, "
    "chronologically ordered record of all platform transactions. Unlike conventional blockchain "
    "implementations that rely on existing networks such as Ethereum or Bitcoin, the present invention "
    "implements a purpose-built blockchain that is tightly integrated with the platform's business logic. "
    "This design choice enables the definition of custom transaction types that directly correspond to "
    "platform operations, eliminating the need for smart contract interpretation layers and reducing "
    "transaction processing latency."
))

# Transaction Types Table
story.append(Spacer(1, 12))
tx_types_data = [
    [Paragraph("<b>Transaction Type</b>", table_header_style),
     Paragraph("<b>Code</b>", table_header_style),
     Paragraph("<b>Description</b>", table_header_style)],
    [Paragraph("MINT", table_cell_style), Paragraph("Coin creation from fiat purchase", table_cell_style), Paragraph("Creates new platform tokens when a user purchases tokens through a fiat payment gateway", table_cell_style)],
    [Paragraph("TRANSFER", table_cell_style), Paragraph("User-to-user or user-to-system transfer", table_cell_style), Paragraph("Moves tokens between wallet addresses, including platform fee collections", table_cell_style)],
    [Paragraph("INVEST", table_cell_style), Paragraph("User to Escrow (buying asset tokens)", table_cell_style), Paragraph("Locks investor funds in the asset's escrow account and records the investment on chain", table_cell_style)],
    [Paragraph("DIVEST", table_cell_style), Paragraph("Exit from investment", table_cell_style), Paragraph("Processes early withdrawal from an active investment, returning funds to the investor", table_cell_style)],
    [Paragraph("PAYOUT", table_cell_style), Paragraph("Escrow to Owner (asset fully funded)", table_cell_style), Paragraph("Releases escrowed funds to the asset owner upon successful completion of the funding period", table_cell_style)],
    [Paragraph("REFUND", table_cell_style), Paragraph("Escrow to Investors (asset expired)", table_cell_style), Paragraph("Returns escrowed funds to all investors when an asset fails to reach its funding target", table_cell_style)],
    [Paragraph("FEE", table_cell_style), Paragraph("Fee collection", table_cell_style), Paragraph("Records the collection of trading, listing, capital raise, and withdrawal fees", table_cell_style)],
    [Paragraph("ASSET_CREATE", table_cell_style), Paragraph("Asset tokenization recorded on chain", table_cell_style), Paragraph("Immutably records the creation of a new tokenized asset on the blockchain ledger", table_cell_style)],
]

tx_table = Table(tx_types_data, colWidths=[80, 140, 240])
tx_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_FILL),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 2), (-1, 2), TABLE_STRIPE),
    ('BACKGROUND', (0, 4), (-1, 4), TABLE_STRIPE),
    ('BACKGROUND', (0, 6), (-1, 6), TABLE_STRIPE),
    ('BACKGROUND', (0, 8), (-1, 8), TABLE_STRIPE),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('BOX', (0, 0), (-1, -1), 1, HEADER_FILL),
]))
story.append(tx_table)
story.append(Paragraph("<b>Table 1:</b> Transaction Types Supported by the Custom Blockchain Engine", caption_style))
story.append(Spacer(1, 12))

story.append(add_body(
    "Each transaction includes a cryptographic signature generated using the ECDSA secp256k1 elliptic "
    "curve algorithm, which is the same cryptographic scheme employed by Bitcoin. The secp256k1 curve "
    "provides a security level of approximately 128 bits, meaning that an attacker would need to perform "
    "approximately 2<super>128</super> operations to forge a signature, which is computationally infeasible "
    "with current and foreseeable computing technology. Each transaction also includes a SHA-256 hash of "
    "the transaction data, which serves as a unique identifier and is used in the Merkle root computation "
    "for block verification."
))

story.append(add_body(
    "The proof-of-work mining process involves finding a nonce value such that the SHA-256 hash of the "
    "block header (which includes the previous block hash, Merkle root, timestamp, difficulty target, and "
    "nonce) is below the difficulty target. The difficulty is dynamically adjusted based on the network's "
    "mining rate to maintain a consistent block generation interval. This mechanism ensures that the "
    "blockchain remains resistant to tampering, as any modification to a historical block would require "
    "re-mining that block and all subsequent blocks, a task that becomes exponentially more difficult "
    "as the chain grows."
))

story.append(add_heading("5.3 AI-Powered Document Analysis Pipeline", 2))

story.append(add_body(
    "The AI document analysis pipeline represents a key innovative component of the present invention, "
    "enabling the automated verification of asset documentation that is critical for regulatory compliance "
    "and investor protection. The pipeline processes user-uploaded documents (supporting JPG, PNG, WebP, "
    "and PDF formats with a maximum file size of 10MB each) through five sequential stages, each "
    "designed to extract progressively deeper levels of information from the document content."
))

story.append(add_body(
    "The first stage, image preprocessing and enhancement, applies standard computer vision techniques "
    "including noise reduction, contrast enhancement, skew correction, and binarization to prepare the "
    "document image for subsequent analysis. This stage is particularly important for scanned documents "
    "or photographs that may suffer from poor lighting, shadow artifacts, or perspective distortion. "
    "The second stage, optical character recognition (OCR), extracts raw text content from the preprocessed "
    "image using a deep learning-based OCR engine capable of handling multiple languages, fonts, and "
    "layout formats commonly encountered in legal and financial documents."
))

story.append(add_body(
    "The third stage, text classification and categorization, analyzes the extracted text to determine "
    "the document type (e.g., property deed, financial statement, valuation report, identity document) "
    "and assesses its relevance to the asset being tokenized. This stage employs natural language processing "
    "(NLP) techniques including text classification models trained on domain-specific corpora of financial "
    "and legal documents. The fourth stage, key information extraction, uses named entity recognition (NER) "
    "to identify and extract structured data points from the unstructured text, including asset addresses, "
    "monetary amounts, dates, legal entity names, registration numbers, and other relevant information. "
    "The fifth and final stage, verification scoring, aggregates the outputs of all preceding stages to "
    "produce a confidence score (0-100) and a binary recommendation (verified or rejected) that determines "
    "whether the asset proceeds to compliance review or is returned to the user for remediation."
))

story.append(add_heading("5.4 Asset Lifecycle State Machine", 2))

story.append(add_body(
    "The asset lifecycle is managed through a deterministic finite state machine that governs the valid "
    "transitions between asset states. The state machine enforces business rules and regulatory requirements "
    "by restricting state transitions to predefined paths, preventing invalid operations and ensuring that "
    "each asset follows the correct verification and funding process. The complete state transition sequence "
    "is: draft, documents_uploaded, ai_analyzing, verified (or rejected), compliance_review, active, funding, "
    "funded (or expired), payout_pending, completed (or refunding, closed)."
))

story.append(add_body(
    "In the draft state, the asset owner provides essential metadata including the asset title, description, "
    "category (selected from twelve predefined categories), target raise amount (bounded between 100 INR "
    "and 1 Crore INR), and listing duration. Upon validation, the asset is inserted into the database with "
    "a draft status. In the documents_uploaded state, the owner uploads between one and ten supporting "
    "documents, which are stored in a dedicated directory with cryptographically randomized filenames to "
    "prevent unauthorized access. SHA-256 hashes are computed for each uploaded document to enable "
    "duplicate detection and integrity verification. The ai_analyzing state triggers the five-stage AI "
    "pipeline described in Section 5.3, which produces a verification score and recommendation."
))

story.append(add_body(
    "Upon successful AI verification, the asset enters the compliance_review state, where it undergoes "
    "additional regulatory compliance checks. If approved, the asset transitions to the active state and "
    "becomes visible to investors on the platform. During the funding state, investors can purchase asset "
    "tokens through INVEST transactions that lock their funds in the asset's escrow account. If the "
    "cumulative investment reaches or exceeds the target raise amount before the listing duration expires, "
    "the asset transitions to the funded state, and subsequently to payout_pending and completed states as "
    "the escrow releases funds to the asset owner. If the funding period expires without reaching the "
    "target, the asset transitions to the expired state, triggering automatic REFUND transactions to "
    "return all investor funds."
))

story.append(add_heading("5.5 Trading Engine and Order Matching", 2))

story.append(add_body(
    "The trading engine provides secondary market liquidity for platform tokens through a centralized "
    "limit-order book architecture. The engine supports both market orders (which execute immediately at "
    "the best available price) and limit orders (which execute only at or better than a specified price). "
    "The order matching algorithm follows the price-time priority discipline: buy orders are sorted by "
    "price in descending order (highest bid first) and sell orders are sorted by price in ascending order "
    "(lowest ask first), with ties broken by timestamp (earliest order first). This matching discipline "
    "ensures fair and efficient price discovery consistent with the practices of established financial "
    "exchanges worldwide."
))

story.append(add_body(
    "Before placing an order, the trading engine verifies the user's token balance against the blockchain "
    "ledger to ensure that the user has sufficient funds to cover the order. For sell orders, the engine "
    "checks that the user's wallet balance is greater than or equal to the order amount. For buy orders, "
    "the engine checks that the user's wallet balance is sufficient to cover the total cost (amount "
    "multiplied by price). This balance verification step prevents the creation of unfunded or partially "
    "funded orders that could lead to settlement failures."
))

story.append(add_body(
    "Each executed trade is recorded on the blockchain as a TRADE transaction, which includes the buyer "
    "address, seller address, trade amount, execution price, buyer fee (0.1% of trade value), seller fee "
    "(0.1% of trade value), and the transaction hash. This on-chain settlement ensures that all secondary "
    "market activity is immutably recorded and publicly auditable. The trading engine also implements "
    "a double-mint prevention mechanism using atomic database operations: the payment verification step "
    "uses an atomic UPDATE query with a WHERE clause that locks the order record, preventing concurrent "
    "requests from processing the same order multiple times."
))

story.append(add_heading("5.6 Algorithmic Price Discovery Model", 2))

story.append(add_body(
    "The token price on the platform is determined by a dual-factor algorithmic formula rather than by "
    "external market forces or oracle price feeds. The price is computed as: P = P_initial x (1 + "
    "totalSupply/10000) x (1 + totalAssetsFunded x 0.04), where P_initial is the base token price "
    "set at platform initialization, totalSupply is the cumulative number of tokens in circulation, and "
    "totalAssetsFunded is the cumulative count of assets that have successfully completed their funding "
    "period. This formula has two multiplicative adjustment factors."
))

story.append(add_body(
    "The first factor, (1 + totalSupply/10000), introduces a supply-based inflation component. As more "
    "tokens are minted through MINT transactions (indicating user adoption and platform growth), the "
    "denominator of 10,000 ensures that the inflation rate remains manageable: at 100,000 tokens in "
    "circulation, the supply adjustment factor is 11.0, representing a 10x increase from the base price. "
    "This gradual appreciation incentivizes early platform participation while maintaining a predictable "
    "relationship between supply and price."
))

story.append(add_body(
    "The second factor, (1 + totalAssetsFunded x 0.04), introduces a demand-based component tied to "
    "platform utility. As more assets are successfully funded (indicating that the platform is delivering "
    "real value by connecting asset owners with investors), the token price appreciates further. The "
    "coefficient of 0.04 (4% per funded asset) creates a meaningful but not excessive price impact per "
    "asset, ensuring that the price remains stable during periods of low funding activity while "
    "appreciating during periods of high platform utility."
))

story.append(add_heading("5.7 Fee Structure and Economic Model", 2))

story.append(add_body(
    "The platform implements a multi-tiered fee structure designed to align the economic incentives of "
    "all participants while generating sustainable revenue for platform operations. The fee structure "
    "comprises five fee types: trading fees (0.1% per trade, charged to both buyer and seller), asset "
    "listing fees (1.0 AC per asset, configurable but not currently enforced), capital raise fees (1.0% "
    "of the total raised amount, deducted from the escrow payout to the asset owner), withdrawal fees "
    "(0.5 AC per withdrawal, sent to the platform fee wallet), and payment gateway fees (variable, "
    "deducted from the fiat amount by the payment processor). All fees are recorded in a dedicated "
    "fee_ledger table and aggregated in the economy table for financial reporting and analytics purposes."
))

# Fee Structure Table
story.append(Spacer(1, 12))
fee_data = [
    [Paragraph("<b>Fee Type</b>", table_header_style),
     Paragraph("<b>Rate</b>", table_header_style),
     Paragraph("<b>Collection Method</b>", table_header_style)],
    [Paragraph("Trading Fee", table_cell_style), Paragraph("0.1% per trade (both sides)", table_cell_style), Paragraph("Deducted at trade execution, sent to platform fee wallet", table_cell_style)],
    [Paragraph("Asset Listing Fee", table_cell_style), Paragraph("1.0 AC per asset", table_cell_style), Paragraph("Configured in system, not currently enforced", table_cell_style)],
    [Paragraph("Capital Raise Fee", table_cell_style), Paragraph("1.0% of raised amount", table_cell_style), Paragraph("Deducted from escrow payout to asset owner", table_cell_style)],
    [Paragraph("Withdrawal Fee", table_cell_style), Paragraph("0.5 AC per withdrawal", table_cell_style), Paragraph("Sent to platform fee wallet", table_cell_style)],
    [Paragraph("Gateway Fee", table_cell_style), Paragraph("Varies by provider", table_cell_style), Paragraph("Deducted from fiat amount by payment processor", table_cell_style)],
]
fee_table = Table(fee_data, colWidths=[110, 130, 220])
fee_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_FILL),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 2), (-1, 2), TABLE_STRIPE),
    ('BACKGROUND', (0, 4), (-1, 4), TABLE_STRIPE),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('BOX', (0, 0), (-1, -1), 1, HEADER_FILL),
]))
story.append(fee_table)
story.append(Paragraph("<b>Table 2:</b> Platform Fee Structure", caption_style))
story.append(Spacer(1, 12))

story.append(add_heading("5.8 Security Architecture", 2))

story.append(add_body(
    "The security architecture of the present invention implements a defense-in-depth strategy with "
    "multiple overlapping security mechanisms operating at different layers of the system stack. The "
    "middleware pipeline processes every incoming HTTP request through a sequence of security checks "
    "before the request reaches the application logic. The pipeline consists of the following components "
    "in order: JSON body parsing with a 5MB payload limit, input sanitization to remove potentially "
    "malicious content, general rate limiting (100 requests per 60 seconds per IP address), and audit "
    "logging middleware that records a cryptographic hash chain of all API requests for tamper-evident "
    "audit trails."
))

story.append(add_body(
    "Authentication is implemented using JSON Web Tokens (JWT) with Bearer token scheme. The system "
    "provides three authentication middleware variants: authenticate (which requires a valid JWT and "
    "attaches the decoded user object to the request), optionalAuth (which attaches the user object if "
    "a token is present but continues processing if not), and requireRole (which checks that the "
    "authenticated user has a specific role, such as admin). Rate limiting is implemented using a "
    "token bucket algorithm with three tiers: generalLimiter (100 requests per 60 seconds for all "
    "routes), authLimiter (10 requests per 60 seconds for authentication endpoints), and financialLimiter "
    "(5 requests per 1 second for financially sensitive operations such as buy, sell, invest, and withdraw)."
))

story.append(add_body(
    "The audit logging system maintains a hash chain of all API requests, where each log entry includes "
    "the hash of the previous entry, creating a tamper-evident chain similar in concept to a blockchain. "
    "Any modification to a historical log entry would break the hash chain, making tampering immediately "
    "detectable. The system also implements double-mint prevention through atomic database UPDATE operations "
    "that lock payment order records before processing, preventing concurrent requests from processing "
    "the same payment multiple times. Input sanitization removes potentially dangerous content from all "
    "request bodies, including HTML tags, JavaScript code, and SQL injection attempts, providing protection "
    "against cross-site scripting (XSS) and SQL injection attacks."
))

# ═══════════════════════════════════════════════════════════
# SECTION 6: CLAIMS
# ═══════════════════════════════════════════════════════════
story.append(add_heading("CLAIMS"))

story.append(add_body(
    "We claim:"
))

story.append(add_claim(1,
    "A computer-implemented method for tokenizing real-world assets on a blockchain platform, the method comprising: "
    "receiving asset metadata from an asset owner, the metadata including an asset title, description, category, "
    "target raise amount, and listing duration; storing the asset in a database with a draft status; receiving "
    "one or more supporting documents for the asset; processing the documents through a multi-stage artificial "
    "intelligence pipeline comprising image preprocessing, optical character recognition, text classification, "
    "key information extraction, and verification scoring to produce a verification recommendation; transitioning "
    "the asset to an active state upon successful verification; receiving investment transactions from a "
    "plurality of investors; recording the investment transactions on a custom proof-of-work blockchain as "
    "INVEST transaction types; locking investment funds in a per-asset escrow account; and upon the asset "
    "reaching its target raise amount, executing a PAYOUT transaction to release escrowed funds to the asset owner."
))

story.append(add_claim(2,
    "The method of claim 1, wherein the custom proof-of-work blockchain utilizes SHA-256 hashing for block "
    "construction and ECDSA secp256k1 elliptic curve cryptography for transaction signing, and supports a "
    "plurality of transaction types selected from the group consisting of MINT, TRANSFER, INVEST, DIVEST, "
    "PAYOUT, REFUND, FEE, and ASSET_CREATE.",
    dependent=True
))

story.append(add_claim(3,
    "The method of claim 1, wherein the multi-stage artificial intelligence pipeline further comprises: "
    "applying noise reduction, contrast enhancement, and skew correction to document images in a first stage; "
    "extracting raw text from preprocessed images using a deep learning-based optical character recognition "
    "engine in a second stage; classifying document type and relevance using natural language processing models "
    "in a third stage; extracting structured data points using named entity recognition in a fourth stage; "
    "and aggregating outputs from all preceding stages to compute a confidence score and binary recommendation "
    "in a fifth stage.",
    dependent=True
))

story.append(add_claim(4,
    "The method of claim 1, wherein the asset lifecycle is governed by a deterministic finite state machine "
    "with the following state transitions: draft to documents_uploaded to ai_analyzing to verified to "
    "compliance_review to active to funding to funded to payout_pending to completed, with rejection branches "
    "from ai_analyzing, verified, and compliance_review states leading to a rejected state, and expiration "
    "branches from funding and funded states leading to expired, refunding, and closed states.",
    dependent=True
))

story.append(add_claim(5,
    "The method of claim 1, further comprising: maintaining a centralized limit-order trading engine for "
    "secondary market trading of platform tokens; matching buy and sell orders using a price-time priority "
    "discipline where orders are sorted by price level and timestamp; verifying user token balances against "
    "the blockchain ledger before order placement; and recording each executed trade as a TRADE transaction "
    "on the blockchain.",
    dependent=True
))

story.append(add_claim(6,
    "The method of claim 5, wherein the price-time priority matching algorithm sorts buy orders by price in "
    "descending order and sell orders by price in ascending order, with ties at the same price level broken "
    "by the timestamp of order placement, and wherein the matching process supports both market orders "
    "executed at the best available price and limit orders executed at or better than a specified price.",
    dependent=True
))

story.append(add_claim(7,
    "The method of claim 1, further comprising computing a dynamic token price using a dual-factor "
    "algorithmic formula: P = P_initial x (1 + totalSupply/10000) x (1 + totalAssetsFunded x 0.04), "
    "where P_initial is the base token price, totalSupply is the cumulative number of platform tokens "
    "in circulation, and totalAssetsFunded is the cumulative number of assets that have successfully "
    "completed their funding period.",
    dependent=True
))

story.append(add_claim(8,
    "The method of claim 1, further comprising implementing a multi-tiered security model comprising: "
    "JSON Web Token-based authentication with Bearer token scheme; token bucket rate limiting with "
    "tiered limits for general, authentication, and financial endpoints; input sanitization middleware "
    "that removes potentially malicious content from request bodies; and audit logging with a hash chain "
    "integrity verification system where each log entry includes a cryptographic hash of the previous entry.",
    dependent=True
))

story.append(add_claim(9,
    "The method of claim 1, further comprising preventing double-minting of payment orders through "
    "atomic database UPDATE operations with conditional WHERE clauses that lock the order record "
    "before payment verification, ensuring that concurrent requests to process the same order are "
    "rejected with zero affected rows.",
    dependent=True
))

story.append(add_claim(10,
    "A system for tokenizing real-world assets on a blockchain platform, the system comprising: "
    "a processor; a memory coupled to the processor and storing computer-readable instructions that, "
    "when executed by the processor, cause the system to perform the method of any one of claims 1 to 9.",
    dependent=True
))

story.append(add_claim(11,
    "A non-transitory computer-readable storage medium storing computer-readable instructions that, "
    "when executed by a processor, cause the processor to perform the method of any one of claims 1 to 9.",
    dependent=True
))

# ═══════════════════════════════════════════════════════════
# SECTION 7: DRAWINGS DESCRIPTION
# ═══════════════════════════════════════════════════════════
story.append(add_heading("BRIEF DESCRIPTION OF DRAWINGS"))

story.append(add_body(
    "The accompanying drawings, which are incorporated in and constitute a part of this specification, "
    "illustrate embodiments of the present invention and, together with the description, serve to explain "
    "the principles of the invention."
))

drawings = [
    ("FIG. 1", "illustrates a high-level system architecture diagram showing the five principal layers "
     "of the platform: Blockchain Layer, Application Layer, Data Layer, AI Processing Layer, and Security Layer."),
    ("FIG. 2", "illustrates the transaction structure diagram showing the relationship between a transaction, "
     "its ECDSA secp256k1 signature, SHA-256 hash, and type classification."),
    ("FIG. 3", "illustrates the block structure diagram showing the components of a blockchain block including "
     "Merkle root, transactions array, previous hash reference, nonce, and difficulty."),
    ("FIG. 4", "illustrates the blockchain engine flow diagram showing the progression from transaction pool "
     "through proof-of-work mining to chain storage."),
    ("FIG. 5", "illustrates the asset lifecycle state machine diagram showing all valid state transitions "
     "from draft through completed or closed."),
    ("FIG. 6", "illustrates the trading engine sequence diagram showing the interaction between buyers, "
     "sellers, the express API, trading engine, blockchain, and database during order placement and matching."),
    ("FIG. 7", "illustrates the middleware pipeline diagram showing the sequential processing of HTTP "
     "requests through authentication, rate limiting, and audit logging stages."),
]

for fig_label, fig_desc in drawings:
    story.append(Paragraph(f"{fig_label} {fig_desc}", body_indent))

# ═══════════════════════════════════════════════════════════
# SECTION 8: BEST MODE
# ═══════════════════════════════════════════════════════════
story.append(add_heading("BEST MODE OF CARRYING OUT THE INVENTION"))

story.append(add_body(
    "The best mode currently contemplated by the inventors for carrying out the present invention is "
    "implemented as a monolithic Node.js application with the following technical specifications. The "
    "application server is built on the Express.js web framework running on the V8 JavaScript engine. "
    "The blockchain engine is implemented as a custom module within the application, utilizing the "
    "crypto module for ECDSA signature operations and the crypto-js library for SHA-256 hashing. "
    "The proof-of-work mining process runs asynchronously within the Node.js event loop, allowing "
    "the application to continue processing HTTP requests while mining operations proceed in the background."
))

story.append(add_body(
    "The data layer utilizes SQLite as the relational database engine, selected for its zero-configuration "
    "deployment, transactional integrity (ACID compliance), and suitability for single-server applications. "
    "The database schema comprises nineteen interconnected tables: users, wallets, kyc_verifications, "
    "assets, asset_documents, asset_tokens, escrow_accounts, escrow_transactions, coin_orders, coin_trades, "
    "economy, price_history, fee_ledger, notifications, payment_gateways, payment_orders, payment_transactions, "
    "audit_logs, and sessions. The AI document analysis pipeline utilizes pre-trained machine learning models "
    "for OCR, text classification, and named entity recognition, deployed as separate processing modules "
    "that communicate with the main application through an asynchronous message queue."
))

story.append(add_body(
    "The security layer implements JSON Web Tokens (JWT) for stateless authentication, with token payloads "
    "containing the user identifier, role, and KYC verification tier. Rate limiting is implemented using "
    "an in-memory token bucket algorithm with configurable parameters for different endpoint categories. "
    "The audit logging system writes a sequential log of all API requests to the audit_logs table, with "
    "each entry containing the previous entry's hash to form a tamper-evident chain. The system deploys "
    "on a single server with a minimum of 2 CPU cores and 4GB RAM, with the blockchain storage file "
    "(chain.json) and SQLite database file stored on persistent disk with regular backup schedules."
))

# ═══════════════════════════════════════════════════════════
# SECTION 9: APPLICATIONS
# ═══════════════════════════════════════════════════════════
story.append(add_heading("INDUSTRIAL APPLICABILITY"))

story.append(add_body(
    "The present invention has significant industrial applicability in the financial technology sector, "
    "particularly in the emerging field of real-world asset tokenization. The system enables small and "
    "medium enterprises, real estate developers, agricultural cooperatives, and other asset owners to "
    "access capital markets by tokenizing their assets and offering fractional ownership to a broad "
    "base of investors. The AI-powered document verification reduces the cost and time associated with "
    "asset due diligence, making the platform accessible to asset owners who cannot afford traditional "
    "investment banking services."
))

story.append(add_body(
    "The invention also finds application in regulatory compliance contexts, where the immutable "
    "blockchain ledger provides a transparent and auditable record of all transactions, escrow operations, "
    "and asset lifecycle events. This transparency is particularly valuable in jurisdictions that require "
    "detailed record-keeping for financial transactions, anti-money laundering (AML) compliance, and "
    "know-your-customer (KYC) verification. The platform's multi-tiered fee structure generates sustainable "
    "revenue while maintaining competitive trading costs for users, making it economically viable as a "
    "standalone business or as a white-label solution for financial institutions seeking to offer tokenization "
    "services to their clients."
))

story.append(add_body(
    "Furthermore, the invention's trading engine and algorithmic price discovery model create a self-sustaining "
    "economic ecosystem where token value is algorithmically tied to platform activity, providing natural "
    "incentives for participation and growth. The custom blockchain infrastructure ensures that the platform "
    "can operate independently of public blockchain networks, reducing operational costs, eliminating gas fee "
    "dependencies, and providing full control over transaction throughput and confirmation times. These "
    "characteristics make the invention particularly suitable for deployment in markets with limited "
    "blockchain infrastructure or where regulatory requirements mandate data sovereignty and privacy."
))

# Build
doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(f"Patent PDF generated: {OUTPUT}")
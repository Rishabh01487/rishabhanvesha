#!/usr/bin/env python3
"""
Averon — Complete Platform Description
Full Technical Book Generator (200-300 pages, 30 chapters)
Author: Rishabh Gupta
"""

import os, sys, hashlib, re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Image, KeepTogether, HRFlowable, ListFlowable, ListItem
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.graphics.shapes import Drawing, Line, Rect
from reportlab.graphics import renderPDF

# ── Paths ──
FONT_DIR = '/usr/share/fonts'
OUTPUT_BODY = '/home/z/my-project/download/book_body.pdf'
OUTPUT_FINAL = '/home/z/my-project/download/Averon_Complete_Platform_Description.pdf'
DIAG_DIR = '/home/z/my-project/download/book_diagrams'

# ━━ Cascade Palette ━━
PAGE_BG       = colors.HexColor('#f6f7f7')
SECTION_BG    = colors.HexColor('#edeeef')
CARD_BG       = colors.HexColor('#e9ebec')
TABLE_STRIPE  = colors.HexColor('#edeff0')
HEADER_FILL   = colors.HexColor('#415b69')
COVER_BLOCK   = colors.HexColor('#617782')
BORDER        = colors.HexColor('#c1cdd3')
ICON          = colors.HexColor('#4687a8')
ACCENT        = colors.HexColor('#3593c1')
ACCENT_2      = colors.HexColor('#b14053')
TEXT_PRIMARY   = colors.HexColor('#1d1f20')
TEXT_MUTED     = colors.HexColor('#707679')
SEM_SUCCESS   = colors.HexColor('#4f8661')
SEM_WARNING   = colors.HexColor('#92753c')
SEM_ERROR     = colors.HexColor('#93514b')
SEM_INFO      = colors.HexColor('#53799f')

# ── Font Registration ──
pdfmetrics.registerFont(TTFont('NotoSerifSC', f'{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoSerifSC-Bold', f'{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Bold.ttf'))
# NotoSansSC variable font not compatible with ReportLab TTFont; skip for English book
pdfmetrics.registerFont(TTFont('FreeSerif', f'{FONT_DIR}/truetype/freefont/FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Bold', f'{FONT_DIR}/truetype/freefont/FreeSerifBold.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Italic', f'{FONT_DIR}/truetype/freefont/FreeSerifItalic.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-BoldItalic', f'{FONT_DIR}/truetype/freefont/FreeSerifBoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', f'{FONT_DIR}/truetype/dejavu/DejaVuSansMono.ttf'))
registerFontFamily('FreeSerif', normal='FreeSerif', bold='FreeSerif-Bold', italic='FreeSerif-Italic', boldItalic='FreeSerif-BoldItalic')
registerFontFamily('NotoSerifSC', normal='NotoSerifSC', bold='NotoSerifSC-Bold')

# ── Page Dimensions ──
A4_W, A4_H = A4
MARGIN_L = 1.0 * inch
MARGIN_R = 0.8 * inch
MARGIN_T = 1.0 * inch
MARGIN_B = 1.0 * inch
CONTENT_W = A4_W - MARGIN_L - MARGIN_R

# ── Styles ──
styles = getSampleStyleSheet()

s_part_title = ParagraphStyle('PartTitle', fontName='FreeSerif-Bold', fontSize=28, leading=36,
    textColor=HEADER_FILL, spaceAfter=24, spaceBefore=60, alignment=TA_LEFT)
s_chapter = ParagraphStyle('Chapter', fontName='FreeSerif-Bold', fontSize=22, leading=28,
    textColor=TEXT_PRIMARY, spaceAfter=16, spaceBefore=40, alignment=TA_LEFT,
    borderWidth=0, borderPadding=0, borderColor=ACCENT)
s_h2 = ParagraphStyle('H2', fontName='FreeSerif-Bold', fontSize=15, leading=20,
    textColor=HEADER_FILL, spaceAfter=10, spaceBefore=20, alignment=TA_LEFT)
s_h3 = ParagraphStyle('H3', fontName='FreeSerif-Bold', fontSize=12, leading=16,
    textColor=ICON, spaceAfter=8, spaceBefore=14, alignment=TA_LEFT)
s_body = ParagraphStyle('Body', fontName='FreeSerif', fontSize=11, leading=18.5,
    textColor=TEXT_PRIMARY, spaceAfter=10, alignment=TA_JUSTIFY, firstLineIndent=0)
s_body_indent = ParagraphStyle('BodyIndent', fontName='FreeSerif', fontSize=11, leading=18.5,
    textColor=TEXT_PRIMARY, spaceAfter=10, alignment=TA_JUSTIFY, leftIndent=18)
s_caption = ParagraphStyle('Caption', fontName='FreeSerif-Italic', fontSize=9, leading=13,
    textColor=TEXT_MUTED, spaceAfter=14, spaceBefore=4, alignment=TA_CENTER)
s_callout = ParagraphStyle('Callout', fontName='FreeSerif-Italic', fontSize=10.5, leading=17,
    textColor=ACCENT, spaceAfter=10, spaceBefore=10, alignment=TA_LEFT,
    leftIndent=24, borderColor=ACCENT, borderWidth=2, borderPadding=8)
s_bullet = ParagraphStyle('Bullet', fontName='FreeSerif', fontSize=10.5, leading=17,
    textColor=TEXT_PRIMARY, spaceAfter=4, alignment=TA_LEFT, leftIndent=30, bulletIndent=18)
s_toc_h1 = ParagraphStyle('TOCH1', fontName='FreeSerif-Bold', fontSize=12, leading=20,
    leftIndent=0, textColor=TEXT_PRIMARY)
s_toc_h2 = ParagraphStyle('TOCH2', fontName='FreeSerif', fontSize=10.5, leading=18,
    leftIndent=20, textColor=TEXT_MUTED)
s_preface_title = ParagraphStyle('PrefaceTitle', fontName='FreeSerif-Bold', fontSize=22, leading=28,
    textColor=TEXT_PRIMARY, spaceAfter=16, spaceBefore=60, alignment=TA_LEFT)
s_preface_body = ParagraphStyle('PrefaceBody', fontName='FreeSerif', fontSize=11, leading=18,
    textColor=TEXT_PRIMARY, spaceAfter=10, alignment=TA_JUSTIFY)

# ── TOC DocTemplate ──
class TocDocTemplate(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        SimpleDocTemplate.__init__(self, *args, **kwargs)
        self.page_count_offset = 0

    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))
            # Explicitly create named destination for PDF internal links
            try:
                self.canv.bookmarkPage(key)
            except Exception:
                pass

    def afterPage(self):
        self.page_count_offset += 1

def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('FreeSerif', 9)
    canvas.setFillColor(TEXT_MUTED)
    page_num = doc.page
    canvas.drawCentredString(A4_W / 2, 0.5 * inch, str(page_num))
    canvas.drawRightString(A4_W - MARGIN_R, A4_H - 0.6 * inch, "Averon - Complete Platform Description")
    canvas.restoreState()

def add_cover_page_number(canvas, doc):
    pass  # No page numbers on cover/TOC pages

# ── Helpers ──
heading_counter = [0, 0, 0]  # part, chapter, section

def part_title(text):
    return Paragraph(text, s_part_title)

def chapter_title(text):
    heading_counter[1] += 1
    heading_counter[2] = 0
    num = heading_counter[1]
    display = f"Chapter {num}"
    key = f'h_{hashlib.md5(text.encode()).hexdigest()[:8]}'
    # Add a decorative line before chapter
    line = HRFlowable(width="30%", thickness=2, color=ACCENT, spaceAfter=8, spaceBefore=30, hAlign='LEFT')
    p = Paragraph(f'<b>{display}</b><br/>{text}', s_chapter)
    p.bookmark_name = key
    p.bookmark_level = 0
    p.bookmark_text = f"{display}: {text}"
    p.bookmark_key = key
    return [line, p]

def h2(text):
    heading_counter[2] += 1
    key = f'h2_{hashlib.md5(text.encode()).hexdigest()[:8]}'
    p = Paragraph(f'<b>{text}</b>', s_h2)
    p.bookmark_name = key
    p.bookmark_level = 1
    p.bookmark_text = text
    p.bookmark_key = key
    return p

def h3(text):
    return Paragraph(f'<b>{text}</b>', s_h3)

def body(text):
    return Paragraph(text, s_body)

def body_i(text):
    return Paragraph(text, s_body_indent)

def callout(text):
    return Paragraph(text, s_callout)

def caption(text):
    return Paragraph(text, s_caption)

def bullet(text):
    return Paragraph(f'<bullet>&bull;</bullet>{text}', s_bullet)

def spacer(h=12):
    return Spacer(1, h)

def add_image(filename, width=None, caption_text=None):
    """Add a diagram image with optional caption."""
    path = os.path.join(DIAG_DIR, filename)
    if not os.path.exists(path):
        return [body(f'[Diagram: {filename} - not found]')]
    w = width or CONTENT_W
    elements = []
    img = Image(path, width=w, height=w * 0.5625)  # 16:9 aspect
    elements.append(img)
    if caption_text:
        elements.append(caption(caption_text))
    elements.append(spacer(12))
    return elements

def make_table(data, col_widths=None, caption_text=None):
    """Create a styled table."""
    if col_widths is None:
        n_cols = len(data[0])
        col_widths = [CONTENT_W / n_cols] * n_cols
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_FILL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'FreeSerif-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9.5),
        ('FONTNAME', (0, 1), (-1, -1), 'FreeSerif'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_PRIMARY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), TABLE_STRIPE))
    t.setStyle(TableStyle(style_cmds))
    elements = [spacer(12), t]
    if caption_text:
        elements.append(caption(caption_text))
    elements.append(spacer(12))
    return elements

# ═══════════════════════════════════════════════════════════════
# CONTENT — 30 CHAPTERS
# ═══════════════════════════════════════════════════════════════

def build_story():
    story = []

    # ── Preface ──
    story.append(Paragraph('Preface', s_preface_title))
    story.append(body(
        'The digital asset landscape is undergoing a fundamental transformation. What began with Bitcoin as a '
        'novel experiment in decentralized currency has evolved into a vast ecosystem of protocols, platforms, '
        'and financial instruments that are reshaping how value is created, transferred, and managed across the '
        'globe. At the forefront of this evolution is the concept of asset tokenization, the process of '
        'representing ownership rights to real-world assets as digital tokens on a blockchain. This technology '
        'promises to unlock trillions of dollars in currently illiquid assets, democratize access to investment '
        'opportunities, and create entirely new financial paradigms.'
    ))
    story.append(body(
        'Averon represents a next-generation approach to this challenge. Rather than building yet another '
        'blockchain or yet another marketplace, Averon was designed from the ground up as a complete digital '
        'asset infrastructure platform. It combines blockchain technology, artificial intelligence, decentralized '
        'identity, compliance systems, smart contracts, and financial infrastructure into a single, programmable '
        'ecosystem. The goal is ambitious yet simple: to become the operating system of the digital asset economy, '
        'connecting fragmented industries through shared digital infrastructure where ownership, value exchange, '
        'compliance, and automation can operate transparently and efficiently.'
    ))
    story.append(body(
        'This book is a comprehensive technical reference for the Averon platform. It is written for engineers, '
        'architects, researchers, and technical leaders who need to understand every layer of the system, from '
        'the cryptographic foundations of the blockchain to the AI models that power document verification, from '
        'the intricacies of the trading engine to the compliance framework that ensures regulatory adherence. '
        'Each chapter provides a deep, self-contained treatment of a specific system component, complete with '
        'architecture diagrams, data models, algorithms, and design rationale. Whether you are building on top '
        'of the Averon platform, evaluating it for enterprise adoption, or conducting academic research, this '
        'book aims to be your definitive reference.'
    ))
    story.append(spacer(20))
    story.append(body('<b>Rishabh Gupta</b>'))
    story.append(body_i('Founder and Chief Architect, Averon Technologies'))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # PART I: FOUNDATIONS
    # ══════════════════════════════════════════════════════════════
    story.append(part_title('Part I: Foundations'))
    story.append(spacer(20))

    # ── CHAPTER 1 ──
    story.extend(chapter_title('Introduction to Digital Asset Infrastructure'))
    story.append(body(
        'The concept of digital assets has undergone a remarkable evolution over the past two decades. What '
        'began with Bitcoin in 2009 as a purely digital store of value and medium of exchange has expanded into '
        'a vast ecosystem encompassing thousands of cryptocurrencies, decentralized finance protocols, non-fungible '
        'tokens, and increasingly, representations of real-world assets on blockchain networks. The total market '
        'capitalization of digital assets has grown from near zero to over three trillion dollars at its peak, '
        'demonstrating both the enormous potential and the volatile nature of this emerging asset class. Yet '
        'despite this growth, the full promise of digital asset technology, the ability to represent, trade, and '
        'manage any form of value on a shared, transparent, and immutable ledger, remains largely unrealized.'
    ))
    story.append(body(
        'The fundamental challenge lies in the gap between the theoretical promise of blockchain technology and '
        'the practical requirements of real-world asset management. Real-world assets, whether they are real '
        'estate properties, agricultural commodities, infrastructure projects, intellectual property, or financial '
        'instruments, come with a complex web of legal, regulatory, compliance, and operational requirements '
        'that pure blockchain protocols were never designed to address. A property deed in India has different '
        'legal requirements than a commodity contract in Brazil. A healthcare supply chain has different '
        'verification needs than a carbon credit marketplace. The infrastructure that powers the digital asset '
        'economy must be flexible enough to accommodate this diversity while maintaining the security, '
        'transparency, and efficiency properties that make blockchain technology valuable in the first place.'
    ))

    story.append(h2('1.1 The Tokenization Opportunity'))
    story.append(body(
        'Asset tokenization refers to the process of creating digital tokens on a blockchain that represent '
        'ownership rights, economic benefits, or other entitlements linked to tangible or intangible assets. The '
        'fundamental value proposition of tokenization lies in its ability to divide traditionally illiquid, '
        'large-denomination assets into smaller, tradable units. Consider a commercial real estate property '
        'valued at ten million dollars. Under traditional ownership models, this asset can only be acquired by '
        'a single buyer or a small syndicate of investors with substantial capital. Through tokenization, the '
        'same property can be represented by ten million tokens, each valued at one dollar, allowing thousands '
        'of investors to participate in ownership with minimal capital requirements.'
    ))
    story.append(body(
        'The implications extend far beyond simple fractional ownership. Tokenized assets can be traded '
        'on secondary markets twenty-four hours a day, seven days a week, unlike traditional markets that '
        'operate during fixed hours. Settlement can occur near-instantaneously on-chain rather than requiring '
        'days or weeks of manual processing. Ownership records are immutable and transparent, reducing the '
        'potential for fraud and disputes. Smart contracts can automate complex workflows such as revenue '
        'distribution, compliance checks, and governance decisions, eliminating intermediaries and reducing '
        'operational costs. According to estimates from major financial institutions including Boston Consulting '
        'Group and McKinsey, the tokenized asset market could reach ten trillion dollars by 2030, representing '
        'approximately ten percent of global GDP.'
    ))

    story.append(h2('1.2 Challenges in Current Approaches'))
    story.append(body(
        'Despite the enormous potential, existing tokenization platforms face several critical challenges that '
        'limit their adoption and effectiveness. The first major challenge is the cost of transactions on public '
        'blockchain networks. Ethereum, the most widely used platform for tokenized assets, charges gas fees '
        'that can range from one dollar to fifty dollars or more per transaction depending on network congestion. '
        'For a platform designed to enable micro-investments of a few dollars, these fees are economically '
        'prohibitive. A five-dollar investment that incurs a three-dollar transaction fee represents a sixty '
        'percent cost overhead, completely undermining the value proposition of fractional ownership.'
    ))
    story.append(body(
        'The second challenge is privacy. Public blockchains, by design, expose all transaction details to '
        'every participant in the network. While this transparency is valuable for auditability, it creates '
        'significant privacy concerns for asset owners and investors who may not wish their financial '
        'activities to be publicly visible. The third challenge is regulatory compliance. Different jurisdictions '
        'have vastly different requirements for securities, KYC (Know Your Customer), AML (Anti-Money '
        'Laundering), and asset classification. A platform that operates globally must navigate this complex '
        'regulatory landscape without imposing an impossible compliance burden on its users or operators.'
    ))
    story.append(body(
        'The fourth challenge is the fragmentation of the ecosystem. Today, an organization that wants to '
        'tokenize and trade assets typically needs to combine separate identity providers, compliance tools, '
        'AI verification systems, tokenization engines, marketplace platforms, and blockchain infrastructure. '
        'Each of these components comes from a different vendor, uses different standards, and requires '
        'separate integration efforts. This fragmentation increases costs, introduces security vulnerabilities '
        'at integration points, and creates inconsistent user experiences.'
    ))

    story.append(h2('1.3 The Averon Vision'))
    story.append(body(
        'Averon was designed to address all of these challenges through a unified, vertically-integrated '
        'platform architecture. Rather than composing the platform from independent microservices, Averon '
        'implements all core functionality within a comprehensive, layered architecture that eliminates '
        'inter-service communication overhead, simplifies deployment, and ensures data consistency. The '
        'platform combines five core technical components: a custom proof-of-work blockchain that provides '
        'zero-fee transactions and data privacy, an AI-powered document verification pipeline that automates '
        'asset due diligence, an on-chain escrow mechanism that protects investor funds, a centralized trading '
        'engine with on-chain settlement, and an algorithmic price discovery model that aligns token value '
        'with platform activity.'
    ))
    story.append(body(
        'But Averon goes beyond these initial components. The platform vision encompasses a complete digital '
        'asset infrastructure that includes the Averon Virtual Machine (AVM) for smart contract execution, '
        'a decentralized identity layer for user-controlled credentials, a compliance engine that is aware '
        'of jurisdiction-specific regulations, an oracle network for trusted external data, and a developer '
        'platform with APIs, SDKs, and enterprise integration tools. The long-term goal is not to replace '
        'banks, governments, or enterprises, but to build the digital infrastructure that allows them to '
        'operate together in a transparent, programmable, and globally connected asset economy.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 2 ──
    story.extend(chapter_title('The Evolution of Asset Tokenization'))
    story.append(body(
        'To understand where Averon fits in the landscape of digital asset infrastructure, it is essential '
        'to trace the historical evolution of asset tokenization from its conceptual origins to its current '
        'state. The idea of representing real-world assets as digital tokens did not emerge overnight; it is '
        'the culmination of decades of innovation in cryptography, distributed systems, financial technology, '
        'and regulatory frameworks. Understanding this evolution provides crucial context for the design '
        'decisions that underpin the Averon platform and illuminates the path forward for the industry as a whole.'
    ))

    story.append(h2('2.1 From Colored Coins to ERC-20'))
    story.append(body(
        'The earliest attempt to represent real-world assets on a blockchain was the "colored coins" concept, '
        'which emerged in 2012-2013 on the Bitcoin network. The idea was elegantly simple: use small amounts '
        'of Bitcoin to "color" specific transactions, marking them as representations of external assets. A '
        'colored coin representing a share of a real estate property could be transferred on the Bitcoin '
        'blockchain just like a regular Bitcoin transaction, but with the added semantic meaning that the '
        'recipient now owned a fraction of that property. While conceptually brilliant, colored coins faced '
        'severe practical limitations. Bitcoin transactions were slow (ten-minute block times), expensive '
        '(fees that made micro-transactions impractical), and lacked the scripting capabilities needed for '
        'complex asset management logic.'
    ))
    story.append(body(
        'The launch of Ethereum in 2015 marked a paradigm shift in asset tokenization. Ethereum introduced '
        'the concept of smart contracts, self-executing programs stored on the blockchain that could encode '
        'arbitrary business logic. The ERC-20 token standard, proposed in 2015 by Fabian Vogelsteller, '
        'provided a standardized interface for creating and managing fungible tokens on Ethereum. This '
        'standardization was transformative. Suddenly, any developer could create a token representing any '
        'asset with just a few lines of Solidity code. The ERC-20 standard enabled the initial coin offering '
        '(ICO) boom of 2017, where billions of dollars were raised through token sales, and laid the groundwork '
        'for the stablecoin revolution (Tether, USDC, DAI) and the decentralized finance (DeFi) movement.'
    ))

    story.append(h2('2.2 The Rise of Security Tokens'))
    story.append(body(
        'While ERC-20 tokens enabled a Cambrian explosion of token innovation, they were fundamentally '
        'designed for utility tokens and cryptocurrencies, not for regulated securities. Security tokens, '
        'which represent ownership in real-world assets such as equity, debt, real estate, or commodities, '
        'require compliance with securities regulations such as KYC, AML, transfer restrictions, and investor '
        'accreditation checks. These requirements cannot be encoded in a simple ERC-20 contract. In response, '
        'the industry developed new token standards specifically designed for security tokens. The ERC-1400 '
        'standard introduced the concept of "partitioned balances," allowing a single token contract to '
        'maintain separate balances for different categories of holders. The ERC-1590 standard added '
        'document management capabilities. The ST-20 standard by Polymath incorporated investor verification '
        'directly into the token contract.'
    ))
    story.append(body(
        'Platforms such as Securitize, Harbor (acquired by Coinbase), and tZERO emerged to provide end-to-end '
        'infrastructure for security token issuance, compliance management, and secondary trading. These '
        'platforms demonstrated that the technology was viable, but they also exposed the limitations of '
        'building on public blockchains. Transaction costs remained high, compliance logic was fragmented '
        'across multiple smart contracts, and the user experience was often confusing for non-technical '
        'asset owners and investors. The market for security tokens, while growing, remained a fraction of '
        'what industry analysts had predicted.'
    ))

    story.append(h2('2.3 Enterprise and Institutional Adoption'))
    story.append(body(
        'The period from 2020 to 2025 saw a significant shift in institutional attitude toward tokenized '
        'assets. Central banks around the world began exploring Central Bank Digital Currencies (CBDCs), '
        'with China launching the digital yuan and the European Central Bank advancing the digital euro '
        'project. Major financial institutions including BlackRock, Franklin Templeton, and JPMorgan began '
        'tokenizing traditional financial instruments. BlackRock launched its BUIDL fund on the Ethereum '
        'network, tokenizing U.S. Treasury bills. JPMorgan introduced Onyx, a blockchain-based platform '
        'for wholesale payments and tokenized deposits. The Monetary Authority of Singapore Project Guardian '
        'demonstrated cross-border tokenized asset trading between Singapore, Japan, and Switzerland.'
    ))
    story.append(body(
        'This institutional adoption brought new requirements that existing platforms struggled to meet. '
        'Enterprises needed private or permissioned networks where transaction details were not publicly '
        'visible. They required integration with existing enterprise systems such as ERP, CRM, and banking '
        'infrastructure. They needed jurisdiction-aware compliance that could adapt to different regulatory '
        'regimes. They demanded institutional-grade security with defense-in-depth architectures. And they '
        'needed all of this to work together seamlessly, without the integration complexity of combining '
        'dozens of separate tools and protocols. It is this set of requirements that Averon was designed to address.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 3 ──
    story.extend(chapter_title('Platform Architecture Overview'))
    story.append(body(
        'The architecture of Averon is the result of a deliberate design philosophy that prioritizes '
        'vertical integration, security by design, and practical scalability. Unlike platforms that compose '
        'functionality from independent microservices communicating over network protocols, Averon implements '
        'its core capabilities within a unified, layered architecture. This section provides a comprehensive '
        'overview of the architectural principles, the five-layer model, the technology stack, and the key '
        'design patterns that define the platform.'
    ))

    story.append(h2('3.1 Architectural Principles'))
    story.append(body(
        'The architecture of Averon is guided by several key design principles that inform every decision '
        'from data model design to API endpoint structure. The first principle is vertical integration: '
        'rather than composing the platform from independent microservices, Averon implements all core '
        'functionality within a single, cohesive application. This eliminates inter-service communication '
        'overhead, simplifies deployment and monitoring, ensures data consistency through shared transaction '
        'boundaries, and reduces the attack surface by minimizing network boundaries. Vertical integration '
        'does not mean monolithic in the pejorative sense; the codebase is organized into clearly defined '
        'modules with well-specified interfaces, but these modules execute within a single process for maximum '
        'efficiency.'
    ))
    story.append(body(
        'The second principle is blockchain-native design. The custom blockchain is not an add-on or '
        'afterthought; it is a foundational component deeply integrated with the business logic. Specialized '
        'transaction types correspond directly to platform operations. The escrow mechanism is implemented '
        'through dedicated blockchain transaction types (INVEST, PAYOUT, REFUND) rather than being layered '
        'on top of generic transfer operations. Trading settlement occurs through on-chain TRADE transactions '
        'that are generated by the matching engine. This deep integration ensures that the blockchain serves '
        'as the single source of truth for all financial operations, providing immutable audit trails and '
        'cryptographic guarantees of data integrity.'
    ))
    story.append(body(
        'The third principle is defense in depth. Security is not implemented as a single layer or a single '
        'mechanism; it is woven throughout every layer of the architecture. JWT authentication protects API '
        'endpoints. Three-tier token bucket rate limiting prevents abuse at different sensitivity levels. '
        'Input sanitization removes potentially dangerous content before it reaches application logic. A '
        'hash-chain audit logging system creates tamper-evident records of every significant action. The '
        'blockchain itself provides an additional layer of immutability for financial transactions. Each of '
        'these mechanisms operates independently, so the failure of any single mechanism does not compromise '
        'the overall security posture.'
    ))

    story.append(h2('3.2 Five-Layer Architecture'))
    story.append(body(
        'The system is organized into five principal layers, each responsible for a specific set of '
        'capabilities. This layered model provides clear separation of concerns while enabling efficient '
        'communication between layers through direct function calls within the same process.'
    ))

    story.extend(add_image('five_layer_arch.png', caption_text='Figure 3.1: Averon Five-Layer Architecture'))

    story.append(body(
        'The Security Layer (Layer 5) sits at the top of the request processing pipeline, implementing '
        'JWT-based authentication with role-based access control, three-tier token bucket rate limiting '
        'with different thresholds for general, authentication, and financial endpoints, input sanitization '
        'that strips HTML, JavaScript, and SQL injection patterns, and comprehensive audit logging with '
        'hash chain integrity verification. Every incoming request must pass through this layer before '
        'reaching any application logic.'
    ))
    story.append(body(
        'The Application Layer (Layer 4) implements the core business logic of the platform. This includes '
        'asset management (creation, verification, lifecycle state transitions), trading operations (order '
        'submission, matching, execution, settlement), payment processing (fiat-to-crypto purchases, gateway '
        'integration), wallet management (key generation, balance tracking, transaction history), and user '
        'administration (registration, authentication, KYC management). The Application Layer orchestrates '
        'operations across the AI Processing Layer, Data Layer, and Blockchain Layer to fulfill user requests.'
    ))
    story.append(body(
        'The AI Processing Layer (Layer 3) implements the five-stage document analysis pipeline that powers '
        'automated asset verification. This layer is responsible for image preprocessing (noise reduction, '
        'contrast enhancement, skew correction, binarization), optical character recognition (OCR), text '
        'classification (determining document type and relevance), named entity recognition (extracting '
        'structured information such as addresses, amounts, dates, and names), and verification scoring '
        '(aggregating all outputs into a confidence score and recommendation).'
    ))
    story.append(body(
        'The Data Layer (Layer 2) provides persistent storage through SQLite, a serverless, zero-configuration '
        'database engine that provides full ACID compliance and excellent read performance. The database '
        'schema comprises 19 tables organized into six functional groups: user management, asset management, '
        'escrow, trading, economic tracking, and payment processing. In addition to the relational database, '
        'the blockchain maintains its own immutable state in the chain.json file, creating a clean separation '
        'between mutable application state and immutable transaction history.'
    ))
    story.append(body(
        'The Blockchain Layer (Layer 1) provides the immutable ledger infrastructure that underpins all '
        'financial operations on the platform. This layer includes the SHA-256 proof-of-work mining engine, '
        'the chain storage and validation system, the wallet and key management system, the Merkle tree '
        'implementation for efficient transaction verification, and the consensus rules that govern chain '
        'validity and fork resolution. The blockchain layer operates asynchronously, mining blocks in the '
        'background while the application continues to serve user requests.'
    ))

    story.append(h2('3.3 Technology Stack'))
    story.append(body(
        'Averon is implemented as a monolithic Node.js application leveraging the V8 JavaScript engine\'s '
        'event-driven, non-blocking I/O model. The web framework is Express.js, providing a robust routing '
        'system, middleware support, and request/response handling. The database is SQLite, selected for its '
        'zero-configuration deployment model (no separate database server process), full ACID compliance for '
        'transaction safety, excellent read performance for query-heavy workloads, and suitability for '
        'single-server applications. The blockchain engine is a custom Node.js module that runs proof-of-work '
        'mining asynchronously within the event loop, utilizing the same process that handles HTTP requests. '
        'Cryptographic operations leverage the Node.js crypto module for ECDSA signatures and the crypto-js '
        'library for SHA-256 hashing.'
    ))

    # Table: Technology Stack
    tech_data = [
        ['Component', 'Technology', 'Rationale'],
        ['Runtime', 'Node.js (V8)', 'Event-driven, non-blocking I/O, single-language stack'],
        ['Web Framework', 'Express.js', 'Mature middleware ecosystem, robust routing'],
        ['Database', 'SQLite', 'Zero-config, ACID compliant, serverless deployment'],
        ['Blockchain', 'Custom PoW (SHA-256)', 'Zero fees, privacy, specialized transaction types'],
        ['Cryptography', 'ECDSA (secp256k1)', '128-bit security, Bitcoin/Ethereum compatible'],
        ['Hashing', 'SHA-256 (crypto-js)', 'Industry standard, Merkle tree support'],
        ['AI Pipeline', 'Deep Learning Models', 'Multi-stage document analysis and verification'],
        ['Authentication', 'JWT (JSON Web Tokens)', 'Stateless, scalable, role-based access control'],
    ]
    story.extend(make_table(tech_data, [CONTENT_W*0.2, CONTENT_W*0.3, CONTENT_W*0.5],
                            'Table 3.1: Averon Technology Stack'))
    story.append(spacer(18))

    # ── CHAPTER 4 ──
    story.extend(chapter_title('Blockchain Layer: Custom Proof-of-Work Engine'))
    story.append(body(
        'The blockchain layer is the foundational infrastructure of the Averon platform, providing an '
        'immutable, cryptographically secured ledger for recording all financial transactions. The decision '
        'to implement a custom blockchain rather than deploying on an existing public network such as '
        'Ethereum, Solana, or Polygon was driven by three fundamental requirements that no existing platform '
        'could simultaneously satisfy: specialized transaction types with no equivalent in standard blockchain '
        'protocols, zero transaction fees to enable economically viable micro-investments, and data privacy '
        'for investment details that should not be visible to all network participants.'
    ))

    story.append(h2('4.1 Design Rationale'))
    story.append(body(
        'Public blockchain networks, while offering robust security and decentralization, impose costs that '
        'are incompatible with Averon\'s target use case of fractional asset ownership with small investments. '
        'Ethereum\'s gas fees, even after the EIP-1559 fee market reform and the transition to proof-of-stake, '
        'remain too volatile and too high for transactions involving amounts as small as one dollar. Layer-2 '
        'solutions such as rollups reduce costs but add complexity and introduce dependencies on third-party '
        'sequencers and validators. Permissioned blockchain frameworks such as Hyperledger Fabric offer '
        'privacy and low costs but require a consortium governance model that is inappropriate for a '
        'single-platform deployment.'
    ))
    story.append(body(
        'Averon\'s custom blockchain provides the security properties of a traditional proof-of-work chain, '
        'including immutability, cryptographic integrity, and resistance to tampering, while eliminating '
        'transaction fees entirely (since the platform operator bears the infrastructure cost) and keeping '
        'all transaction data private within the platform\'s own infrastructure. The trade-off is that the '
        'chain operates within a single organization rather than across a decentralized network, but for a '
        'regulated asset tokenization platform where all participants are known and verified, this trade-off '
        'is acceptable and indeed preferable.'
    ))

    story.append(h2('4.2 Cryptographic Foundations'))
    story.append(body(
        'The blockchain employs two primary cryptographic primitives. Digital signatures use the ECDSA '
        '(Elliptic Curve Digital Signature Algorithm) with the secp256k1 curve, the same curve used by '
        'Bitcoin and Ethereum. This provides approximately 128 bits of security, meaning that an attacker '
        'would need to perform approximately 2 to the power of 128 operations to forge a signature. The '
        'secp256k1 curve was selected for its widespread adoption, extensive security analysis, and compatibility '
        'with existing wallet software and hardware devices. Each transaction on the Averon blockchain is '
        'signed by the sender\'s private key, ensuring non-repudiation (the sender cannot deny having '
        'authorized the transaction) and authenticity (the recipient can verify that the transaction was '
        'indeed authorized by the claimed sender).'
    ))
    story.append(body(
        'Hashing uses the SHA-256 (Secure Hash Algorithm 256-bit) function, the same algorithm used by '
        'Bitcoin for its proof-of-work mining. SHA-256 produces a 256-bit (32-byte) digest from arbitrary-'
        'length input, with the properties of preimage resistance (it is computationally infeasible to find '
        'an input that produces a given hash), second preimage resistance (given an input, it is infeasible '
        'to find a different input with the same hash), and collision resistance (it is infeasible to find '
        'any two inputs that produce the same hash). SHA-256 digests are used for transaction hashes, block '
        'hashes (which serve as the proof-of-work target), Merkle root computation, wallet address derivation, '
        'and audit log integrity verification.'
    ))

    story.extend(add_image('blockchain_structure.png', caption_text='Figure 4.1: Blockchain Structure and Block Components'))

    story.append(h2('4.3 Transaction Types'))
    story.append(body(
        'One of the key differentiators of the Averon blockchain is its set of specialized transaction types. '
        'Rather than using a single generic transfer operation and encoding business logic in higher-level '
        'protocols, Averon defines distinct transaction types at the protocol level, each corresponding to '
        'a specific platform operation. This approach provides several advantages: it makes the chain '
        'directly auditable (anyone can read the chain and understand exactly what type of operation each '
        'transaction represents), it enables type-specific validation rules (an INVEST transaction can only '
        'be sent to an escrow address, for example), and it simplifies the implementation of business logic '
        'by eliminating the need for complex state machines layered on top of generic transfers.'
    ))

    tx_data = [
        ['Transaction Type', 'Description', 'Key Properties'],
        ['MINT', 'Coin creation from fiat purchase', 'Only system wallet can mint; credited to buyer wallet'],
        ['TRANSFER', 'User-to-user or user-to-system transfer', 'Standard value transfer between any addresses'],
        ['INVEST', 'User funds to escrow for asset tokens', 'Atomic: deducts from sender, credits to escrow'],
        ['DIVEST', 'Early exit from investment', 'Returns tokens, reverses escrow lock'],
        ['PAYOUT', 'Escrow to asset owner on full funding', 'Triggered when funding target is reached'],
        ['REFUND', 'Escrow to investors on asset expiry', 'Triggered when listing period expires'],
        ['FEE', 'Platform fee collection', 'Trading (0.1%), listing (1.0 AC), raise (1.0%)'],
        ['ASSET_CREATE', 'Asset tokenization recorded on chain', 'Immutable record of asset creation'],
        ['TRADE', 'AC exchange between traders', 'On-chain settlement of matched orders'],
        ['REWARD', 'Mining reward', '0.1 AC per block to miner'],
    ]
    story.extend(make_table(tx_data, [CONTENT_W*0.2, CONTENT_W*0.45, CONTENT_W*0.35],
                            'Table 4.1: Averon Blockchain Transaction Types'))

    story.append(h2('4.4 Proof-of-Work Mining'))
    story.append(body(
        'Mining is the process by which new blocks are added to the blockchain. A miner must find a nonce '
        'value such that the SHA-256 hash of the block header (which includes the previous block hash, '
        'timestamp, Merkle root, and nonce) is below a dynamically adjusted difficulty target. The difficulty '
        'target is expressed as the number of leading zeros required in the hash: a difficulty of 3 means '
        'the hash must start with three hexadecimal zeros (i.e., be less than 0x000fff...). The difficulty '
        'range is 1 to 6 leading zeros, providing a wide adjustment range that can accommodate varying '
        'computational resources and transaction volumes.'
    ))
    story.append(body(
        'The target block time is thirty seconds, significantly faster than Bitcoin\'s ten minutes but '
        'slower than many proof-of-stake chains. This interval was chosen as a balance between confirmation '
        'speed (users should not wait too long for transactions to be confirmed) and chain stability (too '
        'fast block times increase the risk of orphaned blocks and fork resolution complexity). Difficulty '
        'adjustment occurs every ten blocks. If the average block time over the last ten blocks is less '
        'than half the target (fifteen seconds), difficulty increases. If the average is more than double '
        'the target (sixty seconds), difficulty decreases. This provides responsive adjustment to changes '
        'in mining conditions while preventing rapid oscillation.'
    ))
    story.append(body(
        'Each block can contain a maximum of one hundred transactions and has a maximum size of one megabyte. '
        'The mining reward is 0.1 AC (Averon Coins) per block, which provides ongoing incentive for mining '
        'while minimizing inflationary pressure on the token supply. Transactions that are submitted but not '
        'yet included in a block are held in a pending transaction pool, ordered by submission time. When a '
        'block is mined, transactions are selected from the pool in order until the block is full, ensuring '
        'fair and predictable transaction inclusion.'
    ))

    story.append(h2('4.5 Wallet System'))
    story.append(body(
        'The wallet system manages the cryptographic keys that control ownership of AC coins and tokens '
        'on the Averon blockchain. Each user account is associated with a wallet that contains an ECDSA '
        'keypair. The private key is used to sign transactions, and the public key is used to derive the '
        'wallet address. Key format follows the PEM (Privacy-Enhanced Mail) standard: SPKI (Subject Public '
        'Key Info) for public keys and PKCS8 (Public-Key Cryptography Standards #8) for private keys. '
        'The address derivation process computes SHA-256 of the public key, then RIPEMD-160 of that hash, '
        'and prefixes the result with "0x" to form the wallet address. This two-hash derivation provides '
        'an additional layer of security against preimage attacks on the address.'
    ))
    story.append(body(
        'In addition to user wallets, the system maintains several special-purpose wallets. The __SYSTEM__ '
        'wallet has the exclusive authority to mint new coins (via MINT transactions) and issue mining '
        'rewards (via REWARD transactions). The __PLATFORM_FEE__ wallet collects all platform fees from '
        'trading, listing, capital raises, and withdrawals. For each asset that is actively raising funds, '
        'a dedicated escrow wallet is created with the naming convention ESCROW_assetId_timestamp. These '
        'escrow wallets serve as the custodians of investor funds during the fundraising period, ensuring '
        'that funds are locked and can only be released through the defined PAYOUT or REFUND mechanisms.'
    ))

    story.append(h2('4.6 Merkle Tree and Consensus'))
    story.append(body(
        'Each block in the Averon chain contains a Merkle root, which is the root hash of a binary Merkle '
        'tree constructed from all transaction hashes in the block. The Merkle tree is constructed by '
        'pairing transaction hashes and hashing each pair, then pairing the resulting hashes and hashing '
        'again, recursively until a single root hash remains. If the number of transactions is odd, the '
        'last transaction hash is duplicated before pairing. This data structure enables efficient single-'
        'transaction verification: a light client can verify that a specific transaction is included in a '
        'block by checking only the Merkle proof (the hash path from the transaction to the root), without '
        'needing to download the entire block or the entire chain.'
    ))
    story.append(body(
        'The consensus rules define how the chain is validated and how forks are resolved. Chain validation '
        'checks index continuity (each block\'s index must be exactly one greater than the previous block\'s), '
        'hash chain linkage (each block\'s previous hash must match the previous block\'s hash), hash '
        'integrity (the block\'s own hash must satisfy the difficulty target), difficulty compliance (the '
        'difficulty value must be consistent with the adjustment algorithm), Merkle root correctness (the '
        'Merkle root must match the actual Merkle tree computed from the block\'s transactions), and '
        'timestamp ordering (each block\'s timestamp must be greater than the previous block\'s). Fork '
        'resolution follows the longest valid chain rule: if two competing chains exist, the chain with '
        'the greater total difficulty (typically the longer chain) is accepted as the authoritative chain.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 5 ──
    story.extend(chapter_title('Averon Virtual Machine (AVM)'))
    story.append(body(
        'The Averon Virtual Machine (AVM) is a parallel execution engine designed to run smart contracts '
        'and digital asset workflows on the Averon platform. While the current implementation of Averon '
        'uses specialized transaction types encoded directly into the blockchain protocol, the AVM '
        'represents the next evolutionary step, enabling users and developers to define arbitrary programmable '
        'logic that executes on-chain. The AVM is designed as a complementary layer to the core blockchain, '
        'sitting between the Application Layer and the Blockchain Layer, translating high-level contract '
        'definitions into sequences of blockchain transactions that are validated, executed, and recorded '
        'with the same cryptographic guarantees as native protocol operations.'
    ))

    story.extend(add_image('avm_architecture.png', caption_text='Figure 5.1: Averon Virtual Machine Architecture'))

    story.append(h2('5.1 Design Philosophy'))
    story.append(body(
        'The AVM is designed around three core principles: safety, determinism, and interoperability. Safety '
        'means that contracts executing on the AVM cannot compromise the integrity of the underlying blockchain '
        'or access resources outside their designated scope. This is achieved through a combination of gas '
        'metering (which prevents infinite loops), memory isolation (which prevents contracts from accessing '
        'each other\'s state), and capability-based security (which restricts what operations a contract can '
        'perform based on its declared permissions). Determinism means that given the same initial state and '
        'inputs, a contract will always produce the same outputs, regardless of the machine or environment '
        'in which it is executed. This property is essential for blockchain consensus, as all validating nodes '
        'must agree on the outcome of contract execution. Interoperability means that AVM contracts can '
        'interact with external systems, including off-chain data sources (via oracles), other blockchain '
        'networks (via bridge protocols), and enterprise systems (via the developer API layer).'
    ))

    story.append(h2('5.2 Contract Compilation and Execution'))
    story.append(body(
        'The AVM execution pipeline consists of four stages. In the first stage, contract source code '
        'written in a high-level domain-specific language (DSL) is compiled into AVM bytecode through the '
        'Smart Contract Compiler. The compiler performs type checking, bounds checking, and optimization '
        'passes to produce efficient and safe bytecode. In the second stage, the bytecode is loaded into '
        'the Execution Engine, which interprets or just-in-time compiles the bytecode and executes it '
        'within a sandboxed environment. The Execution Engine maintains a virtual stack, a virtual memory '
        'space, and a set of operation-specific gas counters. In the third stage, the State Manager tracks '
        'all state changes produced by contract execution, including balance updates, storage writes, and '
        'event emissions. These state changes are batched and applied atomically: either all changes are '
        'committed or none are, ensuring consistency. In the fourth stage, the Consensus Interface submits '
        'the finalized state changes to the blockchain layer for inclusion in the next block, ensuring that '
        'contract outcomes are recorded immutably.'
    ))

    story.append(h2('5.3 Smart Contract Templates'))
    story.append(body(
        'To accelerate development and ensure security best practices, the AVM provides a library of '
        'pre-audited contract templates that cover common digital asset workflows. These templates can be '
        'instantiated with custom parameters and deployed without writing any code, making them accessible '
        'to non-developer users such as asset owners and fund managers. The template library includes: '
        'Escrow contracts for conditional fund holding and release, Revenue Sharing contracts for distributing '
        'income from assets to token holders according to predefined rules, Royalty contracts for intellectual '
        'property that automatically distribute licensing fees to rights holders, Subscription contracts for '
        'recurring payments with automatic renewal and cancellation, Insurance Payout contracts that release '
        'funds based on predefined trigger conditions verified by oracles, and Governance contracts that '
        'enable token holders to vote on platform decisions and proposal executions. Each template has been '
        'formally verified to ensure that it behaves correctly under all possible inputs and state '
        'transitions, providing a level of assurance that custom-developed contracts cannot match.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 6 ──
    story.extend(chapter_title('Database Architecture and Data Model'))
    story.append(body(
        'The Averon platform uses SQLite as its primary data store for all mutable application state. SQLite '
        'was selected for its unique combination of properties that make it ideally suited for a single-server '
        'deployment model: serverless architecture (no separate database server process to manage, configure, '
        'or monitor), zero configuration (the database is simply a file that is created automatically on '
        'first run), full ACID compliance (all transactions are atomic, consistent, isolated, and durable, '
        'even in the event of a system crash or power failure), excellent read performance (the vast majority '
        'of database operations on the platform are reads, and SQLite excels at read-heavy workloads), and '
        'a rich SQL feature set including joins, subqueries, window functions, and triggers. The database '
        'file is auto-saved every three seconds, providing a balance between write performance and data '
        'durability.'
    ))

    story.append(h2('6.1 Schema Overview'))
    story.extend(add_image('database_schema.png', caption_text='Figure 6.1: Database Schema Overview - Six Table Groups'))

    story.append(body(
        'The schema comprises nineteen tables organized into six functional groups, each responsible for '
        'a specific domain of the platform\'s operations. This organization provides clear boundaries between '
        'domains while enabling efficient cross-domain queries through foreign key relationships. The six '
        'groups are: User Management (users, wallets, kyc_verifications, sessions), Asset Management (assets, '
        'asset_documents, asset_tokens), Escrow (escrow_accounts, escrow_transactions), Trading (coin_orders, '
        'coin_trades), Economic (economy, price_history, fee_ledger), and Payment (payment_gateways, '
        'payment_orders, payment_transactions), plus notifications and audit_logs tables that cross all domains.'
    ))

    story.append(h2('6.2 User Management Tables'))
    story.append(body(
        'The users table is the central identity store, containing user profiles with fields for email, '
        'password hash, role (user, admin, verifier), KYC status, and account timestamps. The wallets table '
        'stores the cryptographic key material for each user, including the public key, private key (encrypted '
        'at rest), derived address, and current balance. The kyc_verifications table tracks the progress of '
        'identity verification for each user, including document type, verification status, and review notes. '
        'The sessions table manages active user sessions with JWT tokens, device information, and expiration '
        'timestamps. Together, these four tables provide a complete identity and access management system '
        'that supports registration, authentication, authorization, and regulatory compliance.'
    ))

    story.append(h2('6.3 Asset and Trading Tables'))
    story.append(body(
        'The assets table is the core data structure for tokenized assets, containing the asset title, '
        'description, category (from twelve predefined categories including real estate, agriculture, '
        'commodities, infrastructure, and intellectual property), raise amount, listing duration, current '
        'status within the lifecycle state machine, and timestamps for each state transition. The '
        'asset_documents table stores metadata and verification results for each document uploaded against '
        'an asset, including the file path, SHA-256 hash for duplicate detection, and AI verification '
        'score. The asset_tokens table tracks the fractional ownership structure, recording the total '
        'supply of tokens for each asset and the individual holdings of each investor.'
    ))
    story.append(body(
        'The trading tables support the centralized limit-order book. The coin_orders table stores each '
        'order with its side (buy or sell), type (market or limit), amount, price (for limit orders), '
        'filled amount, remaining amount, and status (open, partially filled, filled, cancelled). Users '
        'can maintain a maximum of fifty open orders simultaneously. The coin_trades table records each '
        'executed trade with the buyer and seller addresses, the trade amount, the execution price, the '
        'blockchain transaction hash for on-chain settlement, and the fees collected from both sides.'
    ))
    story.append(spacer(18))

    # ══════════════════════════════════════════════════════════════
    # PART II: INTELLIGENCE
    # ══════════════════════════════════════════════════════════════
    story.append(part_title('Part II: Intelligence'))
    story.append(spacer(20))

    # ── CHAPTER 7 ──
    story.extend(chapter_title('AI-Powered Document Verification'))
    story.append(body(
        'The AI-powered document verification pipeline is one of the most technically sophisticated '
        'components of the Averon platform. It automates the process of reviewing, analyzing, and '
        'verifying the documentation that asset owners must submit when listing an asset for tokenization. '
        'This documentation typically includes property deeds, financial statements, valuation reports, '
        'compliance certificates, insurance documents, and other legal instruments that establish ownership, '
        'value, and regulatory compliance. In a traditional setting, this review process is performed '
        'manually by legal and financial professionals, a process that is slow, expensive, subjective, and '
        'difficult to scale. The AI pipeline reduces this process from days or weeks to minutes while '
        'providing consistent, transparent, and auditable results.'
    ))

    story.extend(add_image('ai_pipeline.png', caption_text='Figure 7.1: Five-Stage AI Document Verification Pipeline'))

    story.append(h2('7.1 Pipeline Architecture'))
    story.append(body(
        'The pipeline processes uploaded documents through five sequential stages, each building on the '
        'outputs of the previous stage. Documents must be in JPG, PNG, WebP, or PDF format, with a maximum '
        'file size of 10MB per document. Each asset requires between one and ten documents, depending on '
        'the asset category and the requirements of the applicable regulatory framework. Files are stored '
        'with cryptographically randomized filenames to prevent enumeration attacks, and SHA-256 hashes are '
        'computed for each file to enable duplicate detection and integrity verification.'
    ))

    story.append(h2('7.2 Stage 1: Image Preprocessing'))
    story.append(body(
        'The first stage prepares document images for reliable text extraction by applying a series of '
        'classical computer vision operations. Gaussian noise reduction applies a convolution filter with a '
        'Gaussian kernel to reduce high-frequency noise that can interfere with character recognition. This '
        'is particularly important for documents that have been scanned on low-quality scanners or photographed '
        'with mobile phone cameras in poor lighting conditions. CLAHE (Contrast Limited Adaptive Histogram '
        'Equalization) enhances local contrast by dividing the image into small tiles and equalizing the '
        'histogram of each tile independently, with a clip limit that prevents over-amplification of noise '
        'in relatively uniform regions. This technique is far more effective than global histogram equalization '
        'for documents with varying illumination across the page.'
    ))
    story.append(body(
        'Hough transform skew correction detects and corrects rotational misalignment of the document. '
        'Many scanned or photographed documents are rotated by a few degrees relative to the horizontal axis, '
        'which can significantly degrade OCR accuracy. The Hough transform identifies the dominant orientation '
        'of lines in the image (typically text baselines) and computes the rotation angle needed to align '
        'them horizontally. The image is then rotated by the inverse of this angle. Finally, Otsu\'s method '
        'is applied to binarize the image, converting it from grayscale to black-and-white by automatically '
        'computing the optimal threshold that minimizes intra-class variance. Binarization simplifies the '
        'OCR task by eliminating variations in pixel intensity that do not carry semantic information.'
    ))

    story.append(h2('7.3 Stage 2: Optical Character Recognition'))
    story.append(body(
        'The second stage uses a deep learning OCR engine that has been trained on a diverse corpus of '
        'documents including printed text, handwritten text, forms, tables, and mixed-language content. '
        'The engine supports multiple languages, fonts, and document layouts, making it suitable for the '
        'diverse range of documents submitted by asset owners across different geographies and industries. '
        'The OCR engine outputs structured text with bounding box coordinates, preserving the spatial '
        'layout of the original document. This spatial information is critical for downstream stages that '
        'need to understand the relationships between text elements, such as distinguishing a document '
        'title from a body paragraph, or associating a label with its corresponding value in a form.'
    ))

    story.append(h2('7.4 Stage 3: Text Classification'))
    story.append(body(
        'The third stage employs a transformer-based classification model that has been fine-tuned on '
        'financial and legal document corpora. The model receives the OCR output and classifies the document '
        'into one of several predefined categories (e.g., property deed, financial statement, valuation '
        'report, compliance certificate, insurance policy) and assesses its relevance to the asset '
        'tokenization process. Documents that are classified as irrelevant or that fall into an unrecognized '
        'category are flagged for manual review. The transformer architecture provides superior performance '
        'on long documents and captures contextual relationships between distant parts of the text, which '
        'is essential for distinguishing between similar document types that may differ only in specific '
        'clauses or terminology.'
    ))

    story.append(h2('7.5 Stage 4: Named Entity Recognition'))
    story.append(body(
        'The fourth stage uses a named entity recognition (NER) model to extract structured information '
        'from the classified document text. The NER model identifies and categorizes entities such as '
        'property addresses, monetary amounts, dates, person names, company names, registration numbers, '
        'legal references, and other domain-specific entities. These extracted entities are stored in a '
        'structured format that can be compared against the asset listing details to verify consistency. '
        'For example, the property address extracted from a deed should match the address provided in the '
        'asset listing. The monetary amount in a valuation report should be consistent with the stated '
        'asset value. Discrepancies between extracted entities and listing details are flagged as potential '
        'verification failures, requiring manual review and resolution.'
    ))

    story.append(h2('7.6 Stage 5: Verification Scoring'))
    story.append(body(
        'The fifth and final stage aggregates the outputs of all previous stages into a comprehensive '
        'verification score. The score is a numeric value between 0 and 100 that represents the overall '
        'confidence in the document\'s authenticity, completeness, and relevance. The scoring algorithm '
        'considers multiple factors including document completeness (are all required documents present and '
        'legible?), information consistency (do the extracted entities match the asset listing details?), '
        'image quality (is the document sufficiently clear for reliable analysis?), and compliance indicators '
        '(does the document contain the necessary legal and regulatory elements?). The score is accompanied '
        'by a binary recommendation of "verified" or "rejected," with a default threshold of 60 out of 100. '
        'Documents scoring above the threshold are automatically verified, while those below are flagged for '
        'manual review by a compliance officer.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 8 ──
    story.extend(chapter_title('AI Valuation and Risk Analysis'))
    story.append(body(
        'Beyond document verification, the Averon AI layer provides a suite of analytical capabilities '
        'that support informed decision-making throughout the asset lifecycle. These capabilities include '
        'automated asset valuation, risk scoring and assessment, portfolio intelligence, and market analytics. '
        'Together, these tools transform raw data into actionable intelligence, enabling investors to make '
        'better-informed decisions and enabling the platform to maintain the integrity and stability of its '
        'marketplace.'
    ))

    story.append(h2('8.1 Automated Valuation Models'))
    story.append(body(
        'The automated valuation model (AVM) estimates the fair market value of tokenized assets using a '
        'combination of comparable sales analysis, income capitalization, and machine learning regression. '
        'For real estate assets, the model considers factors such as location (geographic coordinates, '
        'neighborhood characteristics, proximity to amenities), physical attributes (size, age, condition, '
        'construction quality), market conditions (recent sales in the area, supply and demand dynamics, '
        'interest rate environment), and income potential (rental yields, occupancy rates, operating expenses). '
        'The model is trained on historical transaction data and is regularly retrained to capture changing '
        'market conditions. For commodity assets, the model incorporates spot prices, futures curves, '
        'supply chain data, and macroeconomic indicators. For intellectual property, the model considers '
        'revenue streams, growth trajectories, comparable licensing deals, and market size estimates.'
    ))

    story.append(h2('8.2 Risk Scoring Framework'))
    story.append(body(
        'The risk scoring framework provides a multi-dimensional assessment of the risk profile of each '
        'asset and each investment portfolio. At the asset level, the framework evaluates credit risk '
        '(the likelihood of the asset owner defaulting on obligations), market risk (the sensitivity of '
        'the asset value to market fluctuations), liquidity risk (the ease with which the asset tokens '
        'can be sold on the secondary market), operational risk (the risk of fraud, legal disputes, or '
        'operational failures affecting the asset), and regulatory risk (the likelihood of adverse '
        'regulatory changes affecting the asset or its tokenization). Each risk dimension is scored on a '
        'scale of 1 to 10, and the scores are combined into a composite risk score using a weighted average '
        'that reflects the relative importance of each dimension for the specific asset category. At the '
        'portfolio level, the framework additionally considers correlation risk (how the assets in the '
        'portfolio move relative to each other) and concentration risk (the degree to which the portfolio '
        'is exposed to a single asset, sector, or geography).'
    ))
    story.append(spacer(18))

    # ── CHAPTER 9 ──
    story.extend(chapter_title('Fraud Detection and Compliance AI'))
    story.append(body(
        'Maintaining the integrity of the platform is paramount for building trust among users, regulators, '
        'and institutional partners. The Averon compliance AI system combines rule-based checks with machine '
        'learning models to detect and prevent fraudulent activities, suspicious transactions, and regulatory '
        'violations in real time. This system operates continuously, analyzing patterns across all platform '
        'activity to identify anomalies that may indicate fraudulent behavior.'
    ))

    story.append(h2('9.1 Anomaly Detection'))
    story.append(body(
        'The anomaly detection system monitors user behavior, transaction patterns, and market activity '
        'using a combination of statistical methods and machine learning models. For transaction monitoring, '
        'the system maintains baseline profiles of normal behavior for each user based on their historical '
        'activity patterns, including typical transaction amounts, frequencies, counterparty relationships, '
        'and timing patterns. Deviations from these baselines are scored based on their magnitude and '
        'statistical significance. For example, a user who typically trades amounts between 100 and 500 AC '
        'suddenly placing an order for 50,000 AC would trigger a high anomaly score. The system uses '
        'isolation forests and autoencoders to detect multivariate anomalies that may not be apparent from '
        'any single variable but emerge from the combination of multiple factors.'
    ))

    story.append(h2('9.2 Anti-Money Laundering'))
    story.append(body(
        'The AML system implements a multi-layered approach to detecting and preventing money laundering '
        'activities. The first layer performs real-time transaction screening against known patterns of money '
        'laundering, including structuring (breaking large transactions into smaller ones to avoid reporting '
        'thresholds), layering (moving funds through multiple accounts or assets to obscure their origin), '
        'and integration (introducing laundered funds into the legitimate economy through asset purchases). '
        'The second layer uses graph-based analysis to identify complex networks of related accounts that '
        'may be working in coordination. By constructing a transaction graph and applying community detection '
        'algorithms, the system can identify clusters of accounts that exhibit coordinated behavior even if '
        'no individual account\'s activity is suspicious on its own. The third layer implements sanctions '
        'screening, checking user identities and transaction counterpartyies against OFAC, EU, UN, and other '
        'sanctions lists in real time.'
    ))
    story.append(spacer(18))

    # ══════════════════════════════════════════════════════════════
    # PART III: IDENTITY AND COMPLIANCE
    # ══════════════════════════════════════════════════════════════
    story.append(part_title('Part III: Identity and Compliance'))
    story.append(spacer(20))

    # ── CHAPTER 10 ──
    story.extend(chapter_title('Decentralized Identity Layer'))
    story.append(body(
        'The Averon identity layer provides a decentralized, user-controlled identity framework that enables '
        'individuals, businesses, institutions, and service providers to establish, manage, and prove their '
        'identities without relying on any single centralized authority. Built on the W3C Decentralized '
        'Identifier (DID) standard and Verifiable Credentials specification, the identity layer gives users '
        'full ownership and control over their personal data while enabling platforms and counterparties to '
        'verify claims with cryptographic certainty.'
    ))

    story.extend(add_image('identity_compliance.png', caption_text='Figure 10.1: Identity and Compliance Layer Architecture'))

    story.append(h2('10.1 DID Wallet and Credential Management'))
    story.append(body(
        'Each user on the Averon platform is associated with a DID wallet that stores their decentralized '
        'identifiers and verifiable credentials. A DID is a globally unique identifier that is created and '
        'controlled by the user, not by any platform or authority. The DID document, stored on-chain or in '
        'a distributed file system, contains the public keys and service endpoints associated with the '
        'identity. Verifiable Credentials (VCs) are digital attestations of claims about the user, issued '
        'by trusted authorities such as government ID agencies, financial institutions, or compliance '
        'certification bodies. For example, a "KYC Verified" credential might be issued by a regulated '
        'financial institution after completing the identity verification process. The user stores this '
        'credential in their DID wallet and can present it to any party that requires KYC verification, '
        'without needing to undergo a separate verification process for each platform.'
    ))

    story.append(h2('10.2 Selective Disclosure and Privacy'))
    story.append(body(
        'A critical feature of the identity layer is selective disclosure, the ability for users to prove '
        'specific claims about themselves without revealing unnecessary personal information. For example, '
        'a user can prove that they are over 18 years old without revealing their exact date of birth, or '
        'prove that their income exceeds a certain threshold without revealing their actual income. This is '
        'achieved through zero-knowledge proof techniques, specifically zk-SNARKs (Zero-Knowledge Succinct '
        'Non-Interactive Arguments of Knowledge), which allow a prover to convince a verifier that a statement '
        'is true without revealing any information beyond the truth of the statement itself. Selective '
        'disclosure is essential for regulatory compliance, as many jurisdictions require platforms to verify '
        'certain attributes of their users without collecting or storing more personal data than is strictly '
        'necessary.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 11 ──
    story.extend(chapter_title('KYC/AML Compliance Architecture'))
    story.append(body(
        'The compliance architecture of Averon is designed to support the diverse and evolving regulatory '
        'requirements of multiple jurisdictions while minimizing the burden on users and operators. Rather '
        'than implementing a single, rigid compliance workflow, the system provides a flexible, configurable '
        'framework that can be adapted to the specific requirements of each jurisdiction in which the '
        'platform operates. This jurisdiction-aware approach is essential for a global platform that serves '
        'users across countries with vastly different regulatory regimes.'
    ))

    story.append(h2('11.1 KYC Verification Process'))
    story.append(body(
        'The KYC (Know Your Customer) verification process is the first compliance gate that users must '
        'pass before they can invest in tokenized assets. The process is designed to be thorough yet efficient, '
        'combining automated checks with human review for edge cases. The process begins with document '
        'collection: the user submits a government-issued photo ID (passport, driver\'s license, or national '
        'ID card) and a proof of address (utility bill, bank statement, or government correspondence dated '
        'within the last three months). The AI document verification pipeline (described in Chapter 7) '
        'automatically processes these documents, extracting identity information, verifying document '
        'authenticity, and detecting signs of tampering or forgery.'
    ))
    story.append(body(
        'Following document analysis, the system performs biometric verification by comparing the face in '
        'the submitted ID photo with a live selfie taken through the platform\'s camera interface. This '
        'prevents the use of stolen or borrowed identities. The system then checks the user\'s identity '
        'against various watchlists and sanctions databases, including the OFAC Specially Designated Nationals '
        'list, the EU Consolidated Sanctions List, and the UN Security Council Sanctions List. Finally, '
        'the system performs a Politically Exposed Persons (PEP) check, identifying users who hold or have '
        'held prominent public functions, as these individuals require enhanced due diligence under most '
        'regulatory frameworks. Users who pass all checks are assigned a KYC verification tier that '
        'determines their investment limits and access to platform features.'
    ))

    story.append(h2('11.2 Jurisdiction-Aware Rules Engine'))
    story.append(body(
        'The jurisdiction-aware rules engine is a configurable system that encodes the regulatory '
        'requirements of different jurisdictions as a set of rules that can be applied to user activities '
        'in real time. Each rule specifies a condition (e.g., "user is located in the European Union"), '
        'a requirement (e.g., "GDPR data consent must be obtained"), and an action (e.g., "display consent '
        'dialog and block activity until consent is given"). Rules are organized hierarchically, with '
        'global rules applying to all users, regional rules applying to users in specific geographic areas, '
        'and local rules applying to users in specific countries or states. When a conflict exists between '
        'rules at different levels, the more restrictive rule takes precedence, ensuring that the platform '
        'always complies with the strictest applicable requirement.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 12 ──
    story.extend(chapter_title('Audit Trail and Governance'))
    story.append(body(
        'Transparency and accountability are fundamental to the trust model of the Averon platform. Every '
        'significant action performed on the platform, from user registration to asset creation to trading '
        'to administrative changes, is recorded in a comprehensive audit trail that provides a complete, '
        'chronological record of platform activity. This audit trail serves multiple purposes: it enables '
        'regulatory reporting and compliance demonstration, supports internal investigations of suspicious '
        'activity, provides forensic evidence in the event of disputes or security incidents, and creates '
        'a foundation for governance and oversight.'
    ))

    story.append(h2('12.1 Hash Chain Audit Logging'))
    story.append(body(
        'The audit logging system uses a hash chain architecture that provides cryptographic integrity '
        'guarantees similar to those of a blockchain, but optimized for high-volume logging rather than '
        'consensus-based validation. Each audit log entry contains a SHA-256 hash of the previous entry, '
        'creating a linked chain where any modification to a single entry would break the chain and be '
        'immediately detectable. An entry includes the timestamp, the user or system that performed the '
        'action, the action type (e.g., LOGIN, ASSET_CREATE, TRADE_EXECUTE, ADMIN_CHANGE), the action '
        'details (serialized as JSON), the IP address and user agent of the client, and the hash of the '
        'previous entry in the chain.'
    ))
    story.append(body(
        'To verify the integrity of the audit log, the system provides an integrity verification function '
        'that recomputes the hash chain from the first entry to the last and compares the computed hashes '
        'with the stored hashes. Any discrepancy indicates that one or more entries have been modified, '
        'deleted, or inserted out of order. This verification can be performed at any time by authorized '
        'auditors, regulators, or administrators, providing a tamper-evident record that is significantly '
        'more robust than traditional log files, which can be modified without detection. The hash chain '
        'complements the blockchain\'s immutability: while the blockchain records financial transactions '
        'with full consensus validation, the audit log captures the broader context of platform activity '
        'including non-financial actions that are not recorded on-chain.'
    ))

    story.append(h2('12.2 Protocol Governance'))
    story.append(body(
        'Averon implements an on-chain governance mechanism that allows AVR token holders to participate '
        'in protocol-level decision-making. Governance proposals can be submitted by any token holder who '
        'stakes a minimum amount of AVR as a deposit (which is forfeited if the proposal is found to be '
        'frivolous or malicious). Proposals go through a structured lifecycle: discussion period, voting '
        'period, execution period, and review period. During the discussion period, token holders can '
        'debate the merits of the proposal and suggest modifications. During the voting period, token '
        'holders cast votes proportional to their AVR holdings, with options for "for," "against," and '
        '"abstain." Proposals that receive a majority of "for" votes and meet a minimum quorum requirement '
        'are executed during the execution period. The types of decisions that can be made through governance '
        'include fee structure changes, new asset category additions, parameter adjustments (e.g., block '
        'time, difficulty range, mining reward), protocol upgrades, and treasury allocation.'
    ))
    story.append(spacer(18))

    # ══════════════════════════════════════════════════════════════
    # PART IV: MARKET AND TRADING
    # ══════════════════════════════════════════════════════════════
    story.append(part_title('Part IV: Market and Trading'))
    story.append(spacer(20))

    # ── CHAPTER 13 ──
    story.extend(chapter_title('Marketplace Architecture'))
    story.append(body(
        'The Averon marketplace is the central hub where tokenized assets are discovered, evaluated, '
        'financed, and traded. It brings together asset owners seeking to raise capital, investors seeking '
        'diversified exposure to real-world assets, and traders seeking liquidity in the secondary market. '
        'The marketplace architecture is designed to support the complete lifecycle of an asset from initial '
        'listing through primary fundraising to secondary trading, providing a seamless experience for all '
        'participants while maintaining the security, compliance, and transparency guarantees that are '
        'essential for a regulated financial platform.'
    ))

    story.extend(add_image('marketplace_ecosystem.png', caption_text='Figure 13.1: Averon Marketplace Ecosystem'))

    story.append(h2('13.1 Asset Discovery and Listing'))
    story.append(body(
        'The asset discovery system provides multiple pathways for users to find assets that match their '
        'investment criteria. The primary discovery mechanism is a filterable, sortable catalog of all '
        'active assets, with filters for asset category, funding status, price range, risk score, geographic '
        'location, and expected return. The catalog is powered by a search engine that supports full-text '
        'search across asset titles and descriptions, as well as faceted navigation for structured filters. '
        'Additionally, the system provides personalized recommendations based on the user\'s investment '
        'history, risk profile, and stated preferences, using a collaborative filtering algorithm that '
        'identifies assets similar to those the user has previously invested in or expressed interest in.'
    ))
    story.append(body(
        'The listing process begins when an asset owner submits an asset for tokenization. The owner '
        'provides the asset title, a detailed description, the asset category, the target raise amount '
        '(within the range of 100 INR to 1 Crore INR), and the desired listing duration. The owner then '
        'uploads the required documentation, which is processed by the AI verification pipeline. Upon '
        'successful verification, the asset enters the compliance review stage, where a human compliance '
        'officer reviews the AI assessment and the supporting documentation. If approved, the asset is '
        'published to the marketplace and becomes visible to all investors. The entire process from '
        'submission to publication is designed to complete within 24 to 48 hours for standard assets.'
    ))

    story.append(h2('13.2 Primary Market: Asset Financing'))
    story.append(body(
        'The primary market handles the initial funding of tokenized assets through a structured investment '
        'process with built-in escrow protection. When an investor decides to invest in an asset, they '
        'submit an investment order specifying the amount they wish to invest. The platform creates an '
        'atomic INVEST transaction that simultaneously deducts AC coins from the investor\'s wallet and '
        'credits them to the asset\'s dedicated escrow account. The investor receives asset tokens '
        'proportional to their investment relative to the total raise amount. All investor funds are held '
        'in the escrow account until the asset reaches its funding target or the listing period expires, '
        'providing robust protection against fraud or asset owner default.'
    ))

    story.append(h2('13.3 Secondary Market: Trading'))
    story.append(body(
        'The secondary market enables investors to trade asset tokens after the initial funding round, '
        'providing liquidity that is essential for the viability of any investment platform. The secondary '
        'market operates on a centralized limit-order book model with price-time priority matching, described '
        'in detail in Chapter 14. The key distinction from the primary market is that secondary market '
        'trades occur directly between investors, with the asset owner playing no direct role. The secondary '
        'market also provides market data including real-time prices, order book depth, trade history, and '
        'volume statistics, enabling investors to make informed trading decisions. All secondary market '
        'trades settle on-chain, with each executed trade generating a TRADE transaction that records the '
        'buyer, seller, amount, price, and fee deduction on the immutable blockchain ledger.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 14 ──
    story.extend(chapter_title('Trading Engine and Order Book'))
    story.append(body(
        'The trading engine is the heart of Averon\'s secondary market, responsible for receiving orders, '
        'maintaining the order book, matching compatible orders, executing trades, and settling them on the '
        'blockchain. The engine implements a centralized limit-order book model with price-time priority '
        'matching, which is the same fundamental model used by major financial exchanges worldwide. This '
        'chapter provides a detailed technical description of every component of the trading engine, from '
        'order submission to final on-chain settlement.'
    ))

    story.extend(add_image('trading_engine.png', caption_text='Figure 14.1: Trading Engine Architecture'))

    story.append(h2('14.1 Order Submission and Validation'))
    story.append(body(
        'Orders are submitted through authenticated API endpoints and are validated against a comprehensive '
        'set of rules before being accepted into the order book. Each order specifies the side (buy or sell), '
        'type (market or limit), the asset token to be traded, the amount (in token units), and for limit '
        'orders, the maximum (for buys) or minimum (for sells) acceptable price. Validation checks include: '
        'the user must have a verified KYC status, the user must have sufficient AC balance for buy orders '
        'or sufficient token holdings for sell orders, the order amount must be within the minimum and '
        'maximum limits defined by the platform, the user must not exceed the maximum of fifty concurrent '
        'open orders, and the price (for limit orders) must be within the allowed range. Orders that pass '
        'all validation checks are assigned a unique order ID and a timestamp and are inserted into the '
        'order book.'
    ))

    story.append(h2('14.2 Price-Time Priority Matching'))
    story.append(body(
        'The matching engine implements the price-time priority algorithm, the industry standard for '
        'limit-order book markets. For buy orders (bids), the order book is sorted by price in descending '
        'order (highest bid first), with ties broken by timestamp in ascending order (earliest order first). '
        'For sell orders (asks), the order book is sorted by price in ascending order (lowest ask first), '
        'with the same time-priority tie-breaking. When a new order arrives, the engine iterates through '
        'the opposite side of the book, matching with orders that satisfy the price condition. A buy limit '
        'order at price P matches with sell orders at prices less than or equal to P. A sell limit order '
        'at price P matches with buy orders at prices greater than or equal to P.'
    ))
    story.append(body(
        'For each match, the trade executes at the price of the resting order (the order that was already '
        'in the book). The trade amount is the minimum of the incoming order\'s remaining amount and the '
        'resting order\'s remaining amount. If both orders are fully filled, both are removed from the book. '
        'If one is partially filled, it remains in the book with an updated remaining amount. If the incoming '
        'order is not fully matched after exhausting all compatible resting orders, it is inserted into the '
        'book as a new resting order. This process continues until the incoming order is either fully filled '
        'or no more compatible resting orders exist.'
    ))

    story.append(h2('14.3 On-Chain Settlement'))
    story.append(body(
        'Every trade executed by the matching engine is settled on the Averon blockchain through a TRADE '
        'transaction. The TRADE transaction records the buyer\'s address, the seller\'s address, the traded '
        'amount, the execution price, the fee amount (0.1% charged to both buyer and seller), and the '
        'blockchain transaction hash. The on-chain settlement provides several critical guarantees: immutability '
        '(the trade record cannot be altered after it is included in a block), transparency (any authorized '
        'party can audit the complete trade history), and atomicity (the token transfer and fee deduction '
        'occur as a single atomic operation that either completes entirely or not at all). To prevent the '
        'double-mint vulnerability (where a race condition could allow the same funds to be used for '
        'multiple trades), the settlement process uses atomic database UPDATE operations with a WHERE clause '
        'that checks the order status: UPDATE coin_orders SET status = \'filled\' WHERE id = ? AND status '
        'IN (\'created\', \'pending\'). If the order has already been filled by another concurrent trade, '
        'the UPDATE affects zero rows, and the settlement is aborted.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 15 ──
    story.extend(chapter_title('Algorithmic Price Discovery'))
    story.append(body(
        'The price of the AC token is determined algorithmically rather than through pure market forces. '
        'This design decision reflects the unique characteristics of the Averon platform, where the AC token '
        'serves as both a medium of exchange and a reflection of platform activity. A pure market-determined '
        'price would be vulnerable to manipulation, speculation, and volatility that could undermine the '
        'platform\'s utility as a stable medium for asset tokenization. The algorithmic approach provides '
        'a predictable, transparent, and activity-linked price that aligns the interests of all participants.'
    ))

    story.extend(add_image('price_discovery.png', caption_text='Figure 15.1: Algorithmic Price Discovery Model'))

    story.append(h2('15.1 The Dual-Factor Formula'))
    story.append(body(
        'The AC token price is computed using a dual-factor formula that incorporates both supply-side and '
        'utility-side indicators. The formula is: P = P_initial x (1 + totalSupply / 10000) x (1 + '
        'totalAssetsFunded x 0.04), where P is the current price, P_initial is the base price at platform '
        'launch, totalSupply is the total number of AC coins in circulation, and totalAssetsFunded is the '
        'cumulative number of assets that have been successfully funded on the platform. Factor 1, the supply-'
        'based inflation factor, creates a positive relationship between the circulating supply and the price, '
        'reflecting the increased demand for AC as the platform grows. At a circulating supply of 100,000 AC, '
        'this factor equals 11.0, meaning the price is eleven times the initial price due to supply-driven '
        'demand. Factor 2, the utility-based factor, links price appreciation to the fundamental utility of '
        'the platform, specifically the number of assets that have been successfully funded. Each funded asset '
        'adds a 4% multiplicative boost to the price, creating a direct and visible connection between '
        'platform activity and token value.'
    ))

    story.append(h2('15.2 Asset Funding Boost'))
    story.append(body(
        'In addition to the continuous price appreciation from the dual-factor formula, individual asset '
        'funding events trigger an immediate, one-time price boost. The boost is calculated as: boost = '
        'min(5%, 2% + raiseAmount / 1,000,000 x 3%), where raiseAmount is the total capital raised by the '
        'asset in AC. This formula creates a progressive boost structure where smaller raises receive a '
        'minimum boost of approximately 2.3% and larger raises approach the 5% cap. The boost is applied '
        'immediately upon the asset reaching its funding target and is reflected in the price history for '
        'full transparency. The funding boost mechanism creates visible, predictable connections between '
        'funding events and price movements, reinforcing the narrative that platform activity drives token '
        'value rather than speculation.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 16 ──
    story.extend(chapter_title('Escrow Mechanism and Settlement'))
    story.append(body(
        'The escrow mechanism is one of the most critical trust-building components of the Averon platform. '
        'It ensures that investor funds are securely held during the fundraising period and are only released '
        'to the asset owner upon successful completion of the funding target, or returned to investors if '
        'the asset fails to reach its target within the listing period. This mechanism eliminates the '
        'principal risk that investors face on many crowdfunding and tokenization platforms: the risk that '
        'the asset owner absconds with funds before delivering the promised value.'
    ))

    story.extend(add_image('escrow_flow.png', caption_text='Figure 16.1: Escrow Mechanism Flow'))

    story.append(h2('16.1 Per-Asset Escrow Accounts'))
    story.append(body(
        'Each asset on the Averon platform has a dedicated escrow account that is created automatically '
        'when the asset is published to the marketplace. The escrow account is a special blockchain wallet '
        'with the naming convention ESCROW_assetId_timestamp. It has no private key associated with it; '
        'instead, access to the escrow funds is controlled exclusively through the platform\'s business '
        'logic, which enforces strict rules about when and how funds can be released or refunded. The '
        'escrow_accounts table in the database tracks the current balance, total received, total released, '
        'and total refunded for each escrow account. The escrow_transactions table records every individual '
        'LOCK, RELEASE, and REFUND operation with the user ID, amount, timestamp, and the blockchain '
        'transaction hash of the corresponding on-chain operation.'
    ))

    story.append(h2('16.2 Payout and Refund Logic'))
    story.append(body(
        'When an asset reaches its funding target (total invested amount equals or exceeds the raise amount), '
        'the platform triggers the payout process. The total amount locked in the escrow account, minus the '
        '1.0% capital raise fee, is released to the asset owner\'s wallet through a PAYOUT blockchain '
        'transaction. The capital raise fee is simultaneously transferred to the __PLATFORM_FEE__ wallet '
        'through a FEE transaction. These operations are atomic: either both the payout and the fee collection '
        'succeed, or neither does. If the asset\'s listing period expires without reaching the funding target, '
        'the platform triggers the refund process. All funds in the escrow account are returned to their '
        'original investors through individual REFUND blockchain transactions, with each refund operation '
        'recorded in both the escrow_transactions table and the blockchain. The refund process is designed '
        'to complete automatically without requiring any action from the asset owner or the investors, '
        'ensuring that investors are not left waiting for manual processing.'
    ))
    story.append(spacer(18))

    # ══════════════════════════════════════════════════════════════
    # PART V: SMART CONTRACTS AND ORACLES
    # ══════════════════════════════════════════════════════════════
    story.append(part_title('Part V: Smart Contracts and Oracles'))
    story.append(spacer(20))

    # ── CHAPTER 17 ──
    story.extend(chapter_title('Smart Contract Framework'))
    story.append(body(
        'Smart contracts are self-executing programs that encode business logic into programmable workflows '
        'on the blockchain. On the Averon platform, smart contracts extend the base protocol\'s capabilities '
        'by enabling users to define custom rules for ownership transfers, revenue distribution, conditional '
        'payments, governance decisions, and other complex interactions that go beyond the standard transaction '
        'types. The smart contract framework is designed to be secure, composable, and accessible to both '
        'developers and non-technical users through a combination of a high-level DSL, pre-audited templates, '
        'and the AVM execution environment described in Chapter 5.'
    ))

    story.append(h2('17.1 Contract Lifecycle'))
    story.append(body(
        'Every smart contract on the Averon platform follows a defined lifecycle from creation to completion. '
        'The lifecycle begins with contract creation, where the contract author defines the contract\'s logic, '
        'parameters, and permissions using the Averon Contract DSL or by instantiating a pre-built template. '
        'The contract is then compiled to AVM bytecode and deployed to the blockchain, where it receives a '
        'unique contract address. Once deployed, the contract enters the active state, where it can receive '
        'inputs (function calls with associated data and AC payments), execute its logic, modify its internal '
        'state, and emit events that are recorded on the blockchain. Contracts can be paused by authorized '
        'parties in case of bugs or security vulnerabilities, and can be terminated when their purpose has '
        'been fulfilled. Upon termination, any remaining funds held by the contract are returned to the '
        'designated beneficiary.'
    ))

    story.append(h2('17.2 Contract Templates'))
    story.append(body(
        'The platform provides a comprehensive library of pre-audited smart contract templates that cover '
        'the most common digital asset workflows. Each template has been designed by the Averon engineering '
        'team, formally verified for correctness, and audited by independent security firms. The template '
        'library includes escrow contracts for conditional fund holding with multi-party approval requirements, '
        'revenue sharing contracts that distribute income from assets to token holders according to predefined '
        'allocation rules, royalty contracts for intellectual property that automatically distribute licensing '
        'fees based on usage metrics reported by oracles, subscription contracts for recurring payments with '
        'automatic renewal, grace periods, and cancellation options, insurance contracts that release payouts '
        'based on verified trigger events such as natural disasters or price drops, and governance contracts '
        'that enable token-weighted voting on proposals with delegation and time-locked execution.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 18 ──
    story.extend(chapter_title('Oracle Network'))
    story.append(body(
        'Smart contracts on the Averon blockchain are inherently limited to on-chain data: they can access '
        'the state of the blockchain, the parameters of the transaction that invoked them, and their own '
        'internal storage. However, many real-world use cases require access to external data, such as '
        'current market prices, weather conditions, IoT sensor readings, legal records, or sports outcomes. '
        'The Oracle Network provides a secure, reliable bridge between off-chain data sources and on-chain '
        'smart contracts, enabling contracts to make decisions based on real-world information.'
    ))

    story.append(h2('18.1 Oracle Architecture'))
    story.append(body(
        'The Averon Oracle Network uses a decentralized oracle model where multiple independent oracle '
        'providers submit data to the network, and the platform aggregates their responses to produce a '
        'single, reliable value. This approach mitigates the risk of a single oracle providing incorrect '
        'or manipulated data. The aggregation method depends on the data type: for numeric data (prices, '
        'temperatures, sensor readings), the platform uses a median aggregation that is resistant to outliers '
        'and manipulation. For categorical data (event outcomes, status indicators), the platform uses a '
        'majority-vote mechanism. Each oracle provider must stake a minimum amount of AVR as a bond, which '
        'is slashed (partially or fully confiscated) if the provider is found to have submitted incorrect '
        'data. This economic incentive aligns the oracle providers\' interests with the accuracy of their '
        'reported data.'
    ))

    story.append(h2('18.2 Data Types and Use Cases'))
    story.append(body(
        'The Oracle Network supports several categories of external data that are relevant to tokenized '
        'real-world assets. Price oracles provide real-time and historical price data for commodities, '
        'currencies, securities, and other financial instruments, enabling smart contracts to make decisions '
        'based on current market conditions. Weather oracles provide temperature, precipitation, wind speed, '
        'and other meteorological data, which is essential for agricultural asset tokens whose value depends '
        'on weather conditions. IoT oracles provide data from physical sensors attached to real-world assets, '
        'such as occupancy sensors for real estate, flow meters for infrastructure, or GPS trackers for '
        'logistics assets. Legal oracles provide verified records from government registries, court systems, '
        'and regulatory databases, enabling smart contracts to verify legal status, ownership transfers, '
        'and compliance events. Market data oracles provide trading volumes, order book snapshots, and other '
        'market intelligence from external exchanges, enabling cross-platform arbitrage detection and market '
        'monitoring.'
    ))
    story.append(spacer(18))

    # ══════════════════════════════════════════════════════════════
    # PART VI: FINANCIAL INFRASTRUCTURE
    # ══════════════════════════════════════════════════════════════
    story.append(part_title('Part VI: Financial Infrastructure'))
    story.append(spacer(20))

    # ── CHAPTER 19 ──
    story.extend(chapter_title('Fee Structure and Token Economics'))
    story.append(body(
        'The Averon platform implements a multi-tiered fee structure that aligns the platform\'s revenue '
        'model with the interests of its users. Fees are designed to be transparent, predictable, and '
        'competitive with traditional financial intermediaries while generating sufficient revenue to sustain '
        'platform operations, fund ongoing development, and incentivize ecosystem participation. This chapter '
        'provides a comprehensive description of each fee type, its rationale, and its impact on the '
        'platform\'s economic model.'
    ))

    story.append(h2('19.1 Fee Types'))
    fee_data = [
        ['Fee Type', 'Rate/Amount', 'Charged To', 'Description'],
        ['Trading Fee', '0.1% per side', 'Both buyer and seller', 'Applied to every executed trade on the secondary market'],
        ['Listing Fee', '1.0 AC', 'Asset owner', 'One-time fee charged when an asset is published to the marketplace'],
        ['Capital Raise Fee', '1.0% of raised amount', 'Asset owner', 'Deducted from escrow upon successful funding'],
        ['Withdrawal Fee', '0.5 AC', 'Withdrawing user', 'Charged for fiat withdrawal requests'],
        ['Gateway Fee', 'Variable', 'Purchasing user', 'Set by payment gateway provider for fiat-to-crypto conversion'],
    ]
    story.extend(make_table(fee_data, [CONTENT_W*0.15, CONTENT_W*0.15, CONTENT_W*0.22, CONTENT_W*0.48],
                            'Table 19.1: Averon Fee Structure'))

    story.append(body(
        'All fees are recorded in the fee_ledger table with the timestamp, user ID, fee type, amount, '
        'and the associated transaction (trade ID, asset ID, or withdrawal ID). The economy table '
        'maintains aggregate statistics including the total fees collected, the total AC in circulation, '
        'the current token price, and the total value locked (TVL) in escrow accounts. These statistics '
        'are updated in real time and provide a comprehensive view of the platform\'s financial health.'
    ))

    story.append(h2('19.2 The AVR Coin'))
    story.append(body(
        'AVR is the native utility token of the Averon Protocol, designed to be the economic engine of '
        'the platform. It powers transaction fees, staking, validator participation, governance voting, '
        'oracle services, AI services, developer infrastructure, and ecosystem incentives. The total supply '
        'of AVR is capped at a predetermined maximum, with new tokens issued only through the mining reward '
        'mechanism (0.1 AVR per block). This controlled issuance model ensures that the supply grows at a '
        'predictable rate that is tied to platform activity, preventing the hyperinflation that has plagued '
        'many cryptocurrency projects.'
    ))
    story.append(body(
        'The value of AVR is intended to derive primarily from platform usage rather than speculation. As '
        'more assets are tokenized, more trades are executed, more AI services are consumed, and more '
        'developers build on the platform, the demand for AVR increases, driving its value upward through '
        'the algorithmic price discovery mechanism. This usage-driven value model creates a virtuous cycle: '
        'higher token value attracts more participants, which generates more platform activity, which further '
        'increases the token value. The staking mechanism allows AVR holders to earn additional rewards by '
        'locking their tokens for defined periods, reducing the circulating supply and providing liquidity '
        'for platform operations.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 20 ──
    story.extend(chapter_title('Payment Integration Gateway'))
    story.append(body(
        'The payment integration gateway bridges the traditional fiat financial system with the Averon '
        'blockchain ecosystem, enabling users to purchase AC coins using fiat currency through conventional '
        'payment methods. This gateway is essential for user onboarding, as most users entering the platform '
        'will not hold AC coins initially and need a seamless way to acquire them. The gateway architecture '
        'supports multiple payment providers, enabling geographic and method diversification to serve users '
        'across different countries and banking systems.'
    ))

    story.append(h2('20.1 Fiat-to-Crypto Purchase Flow'))
    story.append(body(
        'The purchase flow begins when a user initiates a buy order through the platform interface, '
        'specifying the fiat amount and the preferred payment method. The platform creates a payment order '
        'record that captures the user ID, the selected payment gateway, the fiat amount, the AC amount '
        '(computed at the current exchange rate), the applicable KYC tier, and the order status (pending, '
        'processing, completed, or failed). The user is then redirected to the payment gateway\'s interface '
        'to complete the fiat payment. Upon successful payment, the gateway sends a callback notification '
        'to the Averon platform, which triggers the verification and minting process.'
    ))

    story.append(h2('20.2 Payment Verification and Minting'))
    story.append(body(
        'Payment verification is a critical security step that prevents double-minting attacks. When the '
        'platform receives a callback from a payment gateway, it does not immediately mint coins. Instead, '
        'it queries the gateway\'s API to independently verify the payment status. Only after independent '
        'confirmation is received does the platform proceed with minting. The minting operation uses an '
        'atomic database UPDATE with a status check to prevent double-processing: UPDATE payment_orders SET '
        'status = \'completed\' WHERE id = ? AND status = \'pending\'. If the callback is a duplicate '
        '(the payment was already processed), the UPDATE affects zero rows, and the operation is safely '
        'aborted. Upon successful verification, a MINT blockchain transaction is created, crediting the '
        'user\'s wallet with the purchased AC coins, and a payment transaction record is created in the '
        'payment_transactions table for audit trail purposes.'
    ))
    story.append(spacer(18))

    # ══════════════════════════════════════════════════════════════
    # PART VII: DEVELOPER PLATFORM
    # ══════════════════════════════════════════════════════════════
    story.append(part_title('Part VII: Developer Platform'))
    story.append(spacer(20))

    # ── CHAPTER 21 ──
    story.extend(chapter_title('API Design and Architecture'))
    story.append(body(
        'The Averon platform exposes its functionality through a comprehensive RESTful API that enables '
        'developers to build applications on top of the platform, integrate Averon capabilities into '
        'existing enterprise systems, and create new user interfaces for the platform\'s services. The API '
        'is designed around REST (Representational State Transfer) principles, using standard HTTP methods '
        '(GET, POST, PUT, DELETE) and status codes, JSON request and response bodies (with a 5MB payload '
        'limit), and resource-oriented URL patterns that map naturally to the platform\'s domain model.'
    ))

    story.append(h2('21.1 API Endpoint Groups'))
    api_data = [
        ['Group', 'Endpoints', 'Authentication', 'Description'],
        ['Authentication', '/auth/register, /auth/login, /auth/logout', 'None / JWT', 'User registration, login, session management'],
        ['Wallet', '/wallet/balance, /wallet/history, /wallet/transfer', 'JWT', 'Balance queries, transaction history, transfers'],
        ['Asset', '/assets, /assets/:id, /assets/:id/documents', 'JWT', 'Asset CRUD, document upload, lifecycle management'],
        ['Market', '/market/orders, /market/trades, /market/orderbook', 'JWT', 'Order submission, trade history, order book depth'],
        ['Portfolio', '/portfolio/holdings, /portfolio/performance', 'JWT', 'Investment holdings, returns analysis'],
        ['Blockchain', '/blockchain/blocks, /blockchain/transactions', 'JWT', 'Chain exploration, transaction lookup'],
        ['Withdrawal', '/withdrawals, /withdrawals/:id', 'JWT', 'Fiat withdrawal requests and status'],
        ['Payment', '/payments/gateways, /payments/orders', 'JWT', 'Payment gateway listing, purchase flow'],
        ['Admin', '/admin/users, /admin/assets, /admin/economy', 'JWT + Admin', 'Administrative operations, platform statistics'],
    ]
    story.extend(make_table(api_data, [CONTENT_W*0.13, CONTENT_W*0.33, CONTENT_W*0.13, CONTENT_W*0.41],
                            'Table 21.1: API Endpoint Groups'))

    story.append(body(
        'All API endpoints pass through the security middleware layer before reaching application logic. '
        'This includes JWT token validation (or extraction of the optional user context for public endpoints), '
        'rate limiting at the appropriate tier, input sanitization to remove potentially dangerous content, '
        'and audit logging of the request. The API supports pagination for list endpoints using offset and '
        'limit parameters, sorting using field and direction parameters, and filtering using query parameters '
        'that map to the underlying database columns.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 22 ──
    story.extend(chapter_title('SDK and Enterprise Integration'))
    story.append(body(
        'While the RESTful API provides direct programmatic access to the platform, many developers and '
        'enterprises prefer a higher-level abstraction that handles authentication, error handling, data '
        'serialization, and common workflows automatically. The Averon SDK provides this abstraction in '
        'the form of client libraries for popular programming languages, pre-built UI components for common '
        'operations, and integration adapters for enterprise systems.'
    ))

    story.append(h2('22.1 Client Libraries'))
    story.append(body(
        'The Averon SDK is available as client libraries for JavaScript/TypeScript (for web and Node.js '
        'applications), Python (for data science, automation, and backend integration), Java (for enterprise '
        'Android and server-side applications), and Swift (for iOS applications). Each library provides a '
        'typed, documented, and tested interface to the platform\'s API, handling JWT authentication and '
        'token refresh, request signing and serialization, error classification and retry logic with '
        'exponential backoff, WebSocket connections for real-time market data, and webhook management for '
        'event-driven integrations. The libraries are published to their respective package managers (npm, '
        'PyPI, Maven Central, CocoaPods) and are versioned using semantic versioning to ensure backward '
        'compatibility.'
    ))

    story.append(h2('22.2 Enterprise System Integration'))
    story.append(body(
        'The enterprise integration framework enables organizations to connect their existing systems to '
        'the Averon platform with minimal development effort. Integration adapters are available for common '
        'enterprise systems including ERP platforms (SAP, Oracle ERP, Microsoft Dynamics) for syncing asset '
        'and financial data, CRM systems (Salesforce, HubSpot) for managing investor relationships, '
        'accounting software (QuickBooks, Xero) for automating bookkeeping, banking APIs for fiat settlement '
        'and reconciliation, warehouse management systems for commodity tracking, and logistics platforms '
        'for supply chain asset monitoring. Each adapter implements a standardized connector interface that '
        'handles data mapping, transformation, validation, and error handling, allowing enterprises to '
        'configure integrations through a visual interface rather than writing custom code.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 23 ──
    story.extend(chapter_title('Wallet Architecture'))
    story.append(body(
        'The wallet system is the user-facing interface to the Averon blockchain, providing the ability '
        'to manage cryptographic keys, view balances, send and receive AC coins and asset tokens, and '
        'sign transactions. The wallet architecture is designed with a strong emphasis on security, usability, '
        'and cross-platform compatibility, supporting both web-based and mobile access patterns.'
    ))

    story.append(h2('23.1 Key Management'))
    story.append(body(
        'The wallet generates an ECDSA keypair using the secp256k1 curve for each user account. The private '
        'key is encrypted using AES-256-GCM with a key derived from the user\'s password through PBKDF2 '
        '(Password-Based Key Derivation Function 2) with a high iteration count (100,000 iterations) and '
        'a random salt. The encrypted private key is stored in the wallets table in the SQLite database. '
        'The public key is stored in PEM (SPKI) format, and the wallet address is derived by computing '
        'SHA-256 of the public key, then RIPEMD-160 of that hash, and prefixing with "0x". This derivation '
        'provides an additional layer of security, as the wallet address does not directly reveal the public '
        'key, making it more difficult for an attacker to derive the private key from the address alone.'
    ))

    story.append(h2('23.2 Transaction Signing'))
    story.append(body(
        'When a user initiates a transaction (such as a transfer, investment, or trade), the wallet system '
        'reconstructs the transaction object, serializes it to a canonical string representation, hashes '
        'the serialized string using SHA-256, and signs the hash using the user\'s private key through '
        'the ECDSA signing algorithm. The resulting signature is attached to the transaction before it is '
        'submitted to the blockchain. The verification process (performed by every node that validates the '
        'chain) recomputes the hash and verifies the signature using the sender\'s public key, ensuring '
        'that the transaction was indeed authorized by the claimed sender and that the transaction data '
        'has not been tampered with since signing. This process provides the cryptographic guarantees of '
        'authenticity, integrity, and non-repudiation that are essential for a financial platform.'
    ))
    story.append(spacer(18))

    # ══════════════════════════════════════════════════════════════
    # PART VIII: SECURITY AND OPERATIONS
    # ══════════════════════════════════════════════════════════════
    story.append(part_title('Part VIII: Security and Operations'))
    story.append(spacer(20))

    # ── CHAPTER 24 ──
    story.extend(chapter_title('Security Architecture: Defense in Depth'))
    story.append(body(
        'The security architecture of Averon implements a defense-in-depth strategy that layers multiple '
        'independent security mechanisms, each providing protection against a different class of threats. '
        'The fundamental principle is that no single security mechanism is sufficient on its own; rather, '
        'the combination of multiple overlapping mechanisms creates a security posture that is significantly '
        'stronger than the sum of its parts. If one mechanism is compromised, the remaining mechanisms '
        'continue to provide protection, limiting the potential impact of any single vulnerability.'
    ))

    story.extend(add_image('security_architecture.png', caption_text='Figure 24.1: Defense-in-Depth Security Architecture'))

    story.append(h2('24.1 Authentication and Authorization'))
    story.append(body(
        'The first layer of defense is authentication and authorization, implemented through JSON Web Tokens '
        '(JWT) with role-based access control. When a user logs in, the server validates their credentials '
        'and issues a JWT that encodes the user\'s ID, role, and expiration time. The token is signed with '
        'a server-side secret key and sent to the client, which includes it in the Authorization header of '
        'subsequent requests. The server validates the token\'s signature and expiration on every request. '
        'Three middleware functions support different authentication scenarios: authenticate (requires a '
        'valid token, returns 401 if missing or invalid), optionalAuth (extracts user context if a token '
        'is present but does not reject unauthenticated requests), and requireRole (checks that the '
        'authenticated user has the required role, returns 403 if not). This flexible middleware system '
        'supports public endpoints (no authentication), user endpoints (authentication required), and admin '
        'endpoints (authentication plus admin role required).'
    ))

    story.append(h2('24.2 Rate Limiting'))
    story.append(body(
        'The second layer of defense is three-tier token bucket rate limiting, which prevents abuse by '
        'limiting the number of requests that a client can make within a given time window. The three tiers '
        'are designed to provide appropriate protection for different types of endpoints based on their '
        'sensitivity and cost. The general tier applies to most API endpoints and allows 100 requests per '
        '60-second window. The authentication tier applies to login and registration endpoints and allows '
        'only 10 requests per 60-second window, preventing brute-force attacks on user credentials. The '
        'financial tier applies to trading, investment, and withdrawal endpoints and allows only 5 requests '
        'per 1-second window, preventing rapid-fire trading that could manipulate the market or exhaust '
        'system resources. Each tier is tracked independently per client IP address, ensuring that a burst '
        'of financial requests does not affect the client\'s ability to make general API calls.'
    ))

    story.append(h2('24.3 Input Sanitization'))
    story.append(body(
        'The third layer of defense is input sanitization, which removes or neutralizes potentially '
        'dangerous content from user-supplied data before it reaches application logic or database queries. '
        'The sanitization engine applies a series of transformations to all input strings: HTML tag stripping '
        '(removing all HTML and XML tags to prevent cross-site scripting), JavaScript code removal (detecting '
        'and removing script injections, event handlers, and JavaScript URLs), SQL injection pattern '
        'neutralization (escaping or removing SQL metacharacters that could modify database queries), and '
        'path traversal prevention (normalizing file paths and rejecting paths that attempt to access files '
        'outside designated directories). The sanitization is applied at the middleware level, before the '
        'request reaches any route handler, ensuring comprehensive coverage.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 25 ──
    story.extend(chapter_title('Deployment, Monitoring, and Operations'))
    story.append(body(
        'Deploying and operating a production instance of the Averon platform requires careful attention '
        'to system requirements, process management, monitoring, backup strategies, and incident response '
        'procedures. This chapter provides a comprehensive operational guide for platform administrators '
        'and DevOps engineers responsible for maintaining the health and performance of an Averon deployment.'
    ))

    story.append(h2('25.1 System Requirements'))
    story.append(body(
        'The minimum hardware requirements for running an Averon instance are 2 CPU cores and 4GB of RAM, '
        'suitable for development and testing environments with low transaction volumes. For production '
        'deployments serving up to 1,000 concurrent users with active trading, the recommended configuration '
        'is 4 CPU cores and 8GB of RAM. For high-traffic deployments serving 10,000 or more concurrent users, '
        '8 CPU cores and 16GB of RAM are recommended. Storage requirements depend on the chain length and '
        'database size: a typical deployment with 10,000 users and 100,000 transactions will require '
        'approximately 5 to 10GB of storage. The blockchain\'s chain.json file grows linearly with the '
        'number of transactions, while the SQLite database grows based on user activity, document storage, '
        'and audit log volume.'
    ))

    story.append(h2('25.2 Process Management'))
    story.append(body(
        'The Averon application is deployed as a single Node.js process, managed by PM2 (Process Manager 2) '
        'or systemd for production reliability. PM2 provides automatic restart on crash, log management, '
        'cluster mode for multi-core utilization, and zero-downtime reload through graceful shutdown and '
        'startup sequencing. The PM2 ecosystem file specifies the application entry point, the number of '
        'instances (1 for single-process mode, or max for cluster mode), environment variables, log file '
        'paths, and resource limits. systemd provides similar capabilities at the operating system level, '
        'with the additional advantage of starting the application automatically on system boot.'
    ))

    story.append(h2('25.3 Monitoring and Alerting'))
    story.append(body(
        'The monitoring system tracks key metrics across four dimensions: blockchain health (block height, '
        'mining rate, difficulty level, pending transaction pool size, chain validation status), trading '
        'throughput (orders per second, trades per second, average execution time, order book depth), '
        'economic indicators (AC price, market capitalization, total value locked, fee collection rate, '
        'active users), and system health (CPU usage, memory usage, disk I/O, API response latency, error '
        'rates). The economy table in the database provides a real-time dashboard of economic metrics that '
        'is updated with every transaction. For external monitoring, the platform exposes a /health endpoint '
        'that returns the status of all subsystems and a /metrics endpoint that provides Prometheus-compatible '
        'metric output for integration with standard monitoring stacks including Grafana, Datadog, and '
        'New Relic.'
    ))

    story.append(h2('25.4 Backup and Recovery'))
    story.append(body(
        'The backup strategy addresses both the SQLite database and the blockchain\'s chain.json file. '
        'SQLite backups are performed using the built-in VACUUM INTO command, which creates a consistent '
        'snapshot of the database without blocking read operations. Chain.json backups use simple file '
        'copying, as the file is written atomically (the new block is first written to a temporary file, '
        'which is then renamed to chain.json, ensuring that the file is always in a consistent state). '
        'Backups are scheduled at regular intervals (recommended: every 6 hours for active deployments) '
        'and retained for a configurable period (recommended: 30 days). For disaster recovery, off-site '
        'backup replication to a separate geographic location is recommended. The recovery procedure involves '
        'stopping the application, restoring the database and chain.json from the most recent backup, and '
        'restarting the application. Since the blockchain validates its own integrity on startup, any '
        'inconsistencies between the restored state and the blockchain will be detected automatically.'
    ))
    story.append(spacer(18))

    # ══════════════════════════════════════════════════════════════
    # PART IX: FUTURE DIRECTIONS
    # ══════════════════════════════════════════════════════════════
    story.append(part_title('Part IX: Future Directions'))
    story.append(spacer(20))

    # ── CHAPTER 26 ──
    story.extend(chapter_title('Proof-of-Stake Migration'))
    story.append(body(
        'The current proof-of-work consensus mechanism provides robust security but has inherent limitations '
        'in terms of energy consumption and transaction confirmation speed. Averon\'s roadmap includes a '
        'migration to a proof-of-stake (PoS) consensus mechanism that addresses these limitations while '
        'maintaining the security guarantees that are essential for a financial platform. The migration '
        'will be designed as a backward-compatible upgrade, ensuring that the existing chain history remains '
        'valid and that no user funds or transaction records are affected.'
    ))

    story.append(h2('26.1 Validator Selection'))
    story.append(body(
        'In the proposed PoS system, validators are selected based on the amount of AVR they have staked '
        'and the duration of their stake. Validators who are selected to propose and attest to blocks receive '
        'rewards proportional to their stake, while validators who behave maliciously (by proposing invalid '
        'blocks or attesting to conflicting blocks) have a portion of their stake slashed (confiscated and '
        'redistributed to honest validators). The slashing mechanism creates a strong economic disincentive '
        'against attacks, as an attacker would need to acquire and stake a significant amount of AVR (making '
        'the attack expensive) and would lose that stake upon detection (making the attack self-destructive). '
        'The minimum stake requirement, the number of validators per epoch, and the slashing conditions '
        'will be determined through governance proposals, ensuring community input into these critical parameters.'
    ))

    story.append(h2('26.2 Migration Strategy'))
    story.append(body(
        'The migration from PoW to PoS will be implemented as a hard fork with a predefined block height '
        'as the transition point. Before the transition, the existing PoW chain continues to operate '
        'normally, and validators begin registering and staking AVR in preparation for the switch. At the '
        'transition block, the PoW mining engine is deactivated, and the PoS validator set takes over block '
        'production. The existing chain history, including all blocks, transactions, and Merkle roots, '
        'remains unchanged and valid. The migration process is designed to be non-disruptive: users will '
        'not need to take any action, and the API endpoints will continue to function without modification. '
        'A comprehensive testnet migration will be conducted at least three months before the mainnet '
        'transition, allowing the engineering team and community members to identify and resolve any issues.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 27 ──
    story.extend(chapter_title('Cross-Chain Interoperability'))
    story.append(body(
        'Cross-chain interoperability is a critical capability for the long-term vision of Averon as a '
        'global digital asset infrastructure. Interoperability enables Averon tokens and assets to interact '
        'with other blockchain networks, expanding their reach and utility beyond the Averon platform. '
        'The cross-chain strategy includes both asset bridging (transferring tokens between Averon and other '
        'networks) and message passing (exchanging data and triggering actions across chains).'
    ))

    story.append(h2('27.1 Bridge Architecture'))
    story.append(body(
        'The cross-chain bridge will use a lock-and-mint model for asset transfers. When a user wants to '
        'transfer an Averon token to another blockchain (e.g., Ethereum), the token is locked in a '
        'designated bridge contract on the Averon chain, and an equivalent "wrapped" token is minted on '
        'the destination chain. The wrapped token represents a claim on the locked asset and can be redeemed '
        'at any time by burning the wrapped token on the destination chain and unlocking the original on the '
        'Averon chain. The bridge is secured by a multi-signature validator set that monitors both chains '
        'and attests to lock and mint events. The validator set is composed of reputable institutional '
        'participants who stake capital as a bond against misbehavior, similar to the oracle network\'s '
        'staking model.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 28 ──
    story.extend(chapter_title('Advanced AI Capabilities'))
    story.append(body(
        'The AI capabilities of the Averon platform are planned for significant expansion beyond the current '
        'document verification and fraud detection systems. The roadmap includes natural language processing '
        'for automated legal document drafting, computer vision for physical asset inspection and monitoring, '
        'reinforcement learning for dynamic pricing and market making, federated learning for privacy-'
        'preserving model training across institutional data, and large language model integration for '
        'intelligent user assistance and automated customer support.'
    ))

    story.append(h2('28.1 Predictive Analytics'))
    story.append(body(
        'The predictive analytics engine will use time-series forecasting models to predict asset values, '
        'market trends, and user behavior. For asset valuation, the engine will combine traditional financial '
        'modeling techniques (discounted cash flow, comparable analysis) with machine learning models '
        '(gradient boosting, neural networks) that can capture non-linear relationships and market dynamics '
        'that traditional models miss. For market trend prediction, the engine will analyze on-chain '
        'transaction patterns, social media sentiment, macroeconomic indicators, and cross-market correlations '
        'to identify emerging trends before they become apparent to human analysts. All predictive models '
        'will include confidence intervals and explainability features, enabling users to understand not '
        'just what the model predicts but why it makes that prediction and how confident it is.'
    ))

    story.append(h2('28.2 Federated Learning'))
    story.append(body(
        'Federated learning enables multiple institutions to collaboratively train machine learning models '
        'without sharing their raw data. This is particularly valuable for the Averon ecosystem, where '
        'financial institutions, asset managers, and regulators all possess valuable data that could improve '
        'model accuracy but cannot be shared due to privacy regulations and competitive concerns. In the '
        'federated learning framework, each participant trains the model locally on their own data and shares '
        'only the model updates (gradients) with the central aggregator. The aggregator combines the updates '
        'from all participants into an improved global model, which is then distributed back to the '
        'participants for the next round of training. This approach enables the collective intelligence of '
        'the entire ecosystem to be harnessed without compromising individual data privacy.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 29 ──
    story.extend(chapter_title('Microservices Migration Path'))
    story.append(body(
        'While the current monolithic architecture provides significant advantages in terms of simplicity, '
        'data consistency, and deployment efficiency, it has natural scaling limitations. A single process '
        'can only utilize a fixed number of CPU cores and a fixed amount of memory, and a bug in any module '
        'can potentially affect the entire application. As the platform grows to serve more users, process '
        'more transactions, and support more asset types, certain components may need to scale independently. '
        'The microservices migration path provides a gradual, low-risk approach to decomposing the monolith '
        'into independently deployable, scalable services.'
    ))

    story.append(h2('29.1 Service Extraction Priority'))
    story.append(body(
        'The migration will prioritize extracting the components that benefit most from independent scaling. '
        'The first component to be extracted will be the blockchain mining engine, which is computationally '
        'intensive and can run on dedicated hardware. The second will be the AI processing pipeline, which '
        'requires GPU resources for inference and can benefit from horizontal scaling across multiple GPU '
        'instances. The third will be the trading engine, which has strict latency requirements and may need '
        'to be deployed closer to end users through edge computing. The remaining components (user management, '
        'asset management, payment processing, API gateway) will follow in subsequent phases. Each extraction '
        'will be preceded by the introduction of a message queue (e.g., Apache Kafka or RabbitMQ) to handle '
        'inter-service communication, and a service discovery mechanism (e.g., Consul or etcd) to enable '
        'dynamic service routing.'
    ))
    story.append(spacer(18))

    # ── CHAPTER 30 ──
    story.extend(chapter_title('The Road Ahead: Vision for a Programmable Asset Economy'))
    story.append(body(
        'Averon envisions a future where every eligible real-world asset can participate in a programmable '
        'digital economy. In this future, ownership can be verified instantly through decentralized identity '
        'and blockchain records. Transfers can be automated through smart contracts that encode complex '
        'conditional logic. Compliance can be integrated directly into transaction workflows through '
        'jurisdiction-aware rules engines. Artificial intelligence can assist every decision, from asset '
        'valuation to risk assessment to portfolio optimization. Developers can build interoperable '
        'applications on shared infrastructure, creating network effects that benefit the entire ecosystem. '
        'Institutions can collaborate through common digital standards, reducing friction and increasing '
        'transparency in every interaction.'
    ))

    story.append(h2('30.1 Key Milestones'))
    story.append(body(
        'The development roadmap for the Averon platform is organized into four phases. Phase 1 (Foundation) '
        'encompasses the current state of the platform: a functional asset tokenization platform with a '
        'custom blockchain, AI verification, escrow, trading, and payment integration. Phase 2 (Intelligence) '
        'will expand the AI layer with advanced analytics, predictive models, and the Averon Virtual Machine '
        'for smart contract execution. Phase 3 (Interoperability) will introduce cross-chain bridges, '
        'decentralized identity, and enterprise integration adapters. Phase 4 (Ecosystem) will focus on '
        'governance decentralization, developer tooling, community growth, and the transition to a '
        'community-governed protocol. Each phase builds on the previous one, ensuring that the platform '
        'remains stable and functional throughout its evolution.'
    ))

    story.append(h2('30.2 The Programmable Asset Economy'))
    story.append(body(
        'The ultimate vision of Averon is not a single platform or a single company but a foundational '
        'infrastructure layer upon which an entire ecosystem of applications, services, and institutions '
        'can be built. Just as the internet provided the infrastructure for the digital information economy, '
        'Averon aims to provide the infrastructure for the digital asset economy. In this economy, every '
        'asset, from a small agricultural plot to a large commercial building, from a single patent to an '
        'entire intellectual property portfolio, can be represented, traded, managed, and governed through '
        'programmable digital infrastructure. The barriers to entry that currently limit asset ownership to '
        'the wealthy and well-connected are dissolved by fractional ownership and micro-investments. The '
        'friction costs of intermediaries are eliminated by smart contracts and automated compliance. The '
        'opacity of traditional finance is replaced by blockchain transparency. This is the future that '
        'Averon is building: a world where every eligible asset can participate in a transparent, efficient, '
        'and globally connected digital economy, and where the benefits of that economy are accessible to '
        'everyone.'
    ))

    return story


# ═══════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════

def main():
    print("Building Averon Complete Platform Description...")

    # Build story with TOC at the beginning
    story = []
    toc = TableOfContents()
    toc.levelStyles = [s_toc_h1, s_toc_h2]
    story.append(Paragraph('Table of Contents', s_preface_title))
    story.append(toc)
    story.append(PageBreak())
    story.extend(build_story())
    # Add expanded content for depth (200+ pages)
    print("Adding expanded content...")
    sys.path.insert(0, os.path.dirname(__file__))
    from book_content_extra import add_expanded_content
    _helpers = {k: v for k, v in globals().items() if not k.startswith('_') and (callable(v) or isinstance(v, (int, float, str, colors.Color)))}
    add_expanded_content(story, _helpers)
    # Add 10 more chapters (31-40) for depth
    print("Adding chapters 31-40...")
    from book_content_extra2 import add_expanded_content_2
    add_expanded_content_2(story, _helpers)
    # Add deep expansions + chapters 41-45
    print("Adding expanded content 3...")
    from book_content_extra3 import add_expanded_content_3
    add_expanded_content_3(story, _helpers)
    # Add final expansions + chapters 46-48
    print("Adding expanded content 4...")
    from book_content_extra4 import add_expanded_content_4
    add_expanded_content_4(story, _helpers)

    # Flatten any nested lists (from make_table returns inside story.extend)
    flat_story = []
    for item in story:
        if isinstance(item, list):
            flat_story.extend(item)
        else:
            flat_story.append(item)
    story = flat_story
    print(f"Total story elements: {len(story)}")

    # Create document
    doc = TocDocTemplate(
        OUTPUT_BODY,
        pagesize=A4,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=MARGIN_T,
        bottomMargin=MARGIN_B,
        title='Averon - Complete Platform Description',
        author='Rishabh Gupta',
        subject='Comprehensive technical reference for the Averon digital asset infrastructure platform',
        creator='Averon Technologies'
    )

    # Build with page numbers
    doc.multiBuild(story, onLaterPages=add_page_number, onFirstPage=add_cover_page_number)

    print(f"Body PDF generated: {OUTPUT_BODY}")
    print(f"Pages: check the output file")


if __name__ == '__main__':
    main()
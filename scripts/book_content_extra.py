#!/usr/bin/env python3
"""
Expanded content for the Averon Technical Book.
Adds substantial sections after specific chapters to bring the total
from approximately 53 pages to 200+ pages.

This module is designed to be imported by the parent book generator.
It expects the following to be available in the importing scope:

  Helper functions: body, h2, h3, bullet, callout, spacer,
                    make_table, add_image
  Constants:        DIAG_DIR, PART_TITLE_STORY_MARKER,
                    TEXT_PRIMARY, HEADER_FILL, ACCENT, ACCENT_2,
                    TEXT_MUTED, BORDER, TABLE_STRIPE, ICON,
                    SEM_SUCCESS, SEM_WARNING, SEM_ERROR, SEM_INFO,
                    CONTENT_W

Usage (in parent script, after building each chapter's story elements):
    from book_content_extra import add_expanded_content
    # ... build story with all 30 chapters ...
    add_expanded_content(story)
"""


def add_expanded_content(story, _helpers=None):
    """Add expanded content sections to reach 200+ pages."""
    if _helpers:
        for _k, _v in _helpers.items():
            if not _k.startswith('_'):
                globals()[_k] = _v

    # ================================================================
    # AFTER CHAPTER 1 - Introduction
    # ================================================================

    # --- 1.4 Industry Landscape and Market Analysis ---
    story.extend([
        h2("1.4 Industry Landscape and Market Analysis"),

        body(
            "The global tokenization market has experienced remarkable growth over the past "
            "several years, transforming from a niche experimental concept into a mainstream "
            "financial infrastructure paradigm. According to Boston Consulting Group (BCG), "
            "the tokenized asset market is projected to reach approximately $16 trillion by "
            "2030, representing a compound annual growth rate (CAGR) that exceeds 70 percent "
            "from its 2023 baseline of roughly $100 billion in on-chain real-world assets. "
            "This explosive trajectory is driven by converging forces: the maturation of "
            "blockchain infrastructure, increasing institutional comfort with distributed "
            "ledger technology, and the persistent demand for greater liquidity and "
            "fractional ownership in traditionally illiquid asset classes such as real estate, "
            "private equity, and fine art. McKinsey and Company's separate analysis aligns "
            "closely with these projections, estimating that tokenized illiquid assets alone "
            "could capture up to $4 trillion in value by 2030, while the broader category "
            "including bonds, funds, and other financial instruments pushes the addressable "
            "market well into the double-digit trillions."
        ),

        body(
            "When compared to traditional securitization markets, the tokenization opportunity "
            "represents both an evolution and a disruption. The global securitization market, "
            "which encompasses mortgage-backed securities, asset-backed securities, and "
            "collateralized loan obligations, processes approximately $2.5 trillion in new "
            "issuance annually. Tokenization promises to reduce the friction costs associated "
            "with these processes by an estimated 40 to 60 percent, primarily through the "
            "elimination of intermediaries, automated compliance checks via smart contracts, "
            "and near-instantaneous settlement compared to the traditional T+2 or T+3 cycles. "
            "The World Economic Forum has noted that tokenization could fundamentally reshape "
            "capital markets infrastructure, with potential annual cost savings exceeding "
            "$20 billion across custody, clearing, and settlement functions globally. "
            "Furthermore, the DeFi ecosystem has demonstrated that programmable financial "
            "primitives, when combined with real-world asset backing, can create novel "
            "financial products that were previously impractical or impossible to construct "
            "within the confines of traditional financial plumbing."
        ),

        body(
            "The decentralized finance (DeFi) sector, which serves as both a precursor and "
            "a proving ground for tokenized real-world assets, has itself grown from less "
            "than $1 billion in total value locked (TVL) in early 2020 to peak levels "
            "exceeding $180 billion before market corrections. While DeFi remains volatile, "
            "the underlying protocols for lending, borrowing, and trading have demonstrated "
            "robustness at scale, processing billions of dollars in transaction volume monthly. "
            "Institutional players including BlackRock, JPMorgan, and Goldman Sachs have "
            "launched tokenized fund products or blockchain-based settlement pilots, signaling "
            "a decisive shift in sentiment. BlackRock's BUIDL fund on the Ethereum network "
            "and JPMorgan's Onyx Digital Assets platform represent early but significant "
            "commitments from the world's largest asset managers. The convergence of "
            "regulatory clarity, institutional adoption, and technological maturity positions "
            "tokenization not as a speculative trend but as a fundamental restructuring of "
            "how assets are originated, distributed, and traded across global capital markets."
        ),

        spacer(8),

        # --- 1.5 Regulatory Landscape ---
        h2("1.5 Regulatory Landscape"),

        body(
            "The regulatory environment surrounding asset tokenization has evolved significantly "
            "since 2020, shifting from a patchwork of ad hoc guidance to increasingly "
            "comprehensive frameworks designed to provide legal certainty while protecting "
            "investors. The European Union's Markets in Crypto-Assets Regulation (MiCA), "
            "which entered into full effect in late 2024, represents the most ambitious and "
            "detailed regulatory framework for digital assets globally. MiCA establishes "
            "clear requirements for crypto-asset service providers, stablecoin issuers, and "
            "tokenized securities, including capital adequacy requirements, governance "
            "standards, and consumer protection mandates. For platforms like Averon operating "
            "within or targeting the European market, MiCA provides a harmonized regulatory "
            "passport that eliminates the need for separate national approvals across all 27 "
            "EU member states. The regulation also introduces specific provisions for "
            "asset-referenced tokens and e-money tokens, creating distinct regulatory "
            "categories that align well with Averon's approach to tokenized real-world assets."
        ),

        body(
            "In the United States, the Securities and Exchange Commission (SEC) has taken a "
            "more fragmented approach, applying existing securities laws to tokenized assets "
            "through enforcement actions and interpretive guidance rather than comprehensive "
            "legislation. The SEC's position, articulated through its Framework for Investment "
            "Contract Analysis of Digital Assets (the Howey Test application), generally "
            "classifies most tokenized assets as securities, subjecting them to registration "
            "requirements under the Securities Act of 1933 and exchange requirements under "
            "the Securities Exchange Act of 1934. However, the emergence of tokenized funds "
            "under Rule 144A exemptions and the SEC's experimental tokenized treasury offerings "
            "suggest a gradual opening. Simultaneously, the Commodity Futures Trading Commission "
            "(CFTC) has asserted jurisdiction over certain digital asset derivatives, creating "
            "a dual-regulator dynamic. India's Reserve Bank of India (RBI) has taken a more "
            "cautious stance, initially imposing a blanket ban on cryptocurrency transactions "
            "in 2018 before the Supreme Court reversed this in 2020, and subsequently "
            "introducing a 30 percent tax on digital asset gains along with a 1 percent TDS "
            "requirement, while actively exploring a central bank digital currency (CBDC) "
            "through its pilot e-Rupee program."
        ),

        body(
            "The Dubai Virtual Assets Regulatory Authority (VARA), established in 2022 as the "
            "world's first independent regulatory body for virtual assets, has created a "
            "comprehensive licensing framework covering activities from custody and exchange "
            "services to token issuance and management. VARA's activity-based approach "
            "provides clarity for platforms like Averon by delineating specific compliance "
            "obligations for each functional area of the tokenization lifecycle. Singapore's "
            "Monetary Authority of Singapore (MAS) has pursued a similarly proactive approach "
            "through its Payment Services Act, which regulates digital payment token services, "
            "and its Project Guardian initiative, which actively pilots tokenized asset "
            "use cases in collaboration with major financial institutions including DBS Bank, "
            "Standard Chartered, and MarketVector. The MAS framework is particularly notable "
            "for its regulatory sandbox approach, allowing innovation to proceed under "
            "controlled conditions with appropriate safeguards. Across these jurisdictions, "
            "a common trend emerges: regulators are moving from prohibition to structured "
            "engagement, creating the legal infrastructure necessary for platforms like Averon "
            "to operate at institutional scale while maintaining compliance with local and "
            "international requirements."
        ),

        spacer(8),

        # --- 1.6 Comparative Analysis of Tokenization Platforms ---
        h2("1.6 Comparative Analysis of Tokenization Platforms"),

        body(
            "The tokenization platform landscape encompasses a diverse range of solutions, "
            "from public blockchain networks designed for general-purpose computation to "
            "permissioned enterprise frameworks optimized for regulated financial workflows. "
            "Understanding the relative strengths and trade-offs of these platforms is "
            "essential for evaluating Averon's architectural decisions and competitive "
            "positioning. The following table provides a systematic comparison across seven "
            "critical dimensions that determine platform suitability for real-world asset "
            "tokenization at institutional scale."
        ),
    ])

    story.extend(make_table(
        [
            ["Dimension", "Averon", "Ethereum", "Polygon", "Hyperledger", "Securitize"],
            ["Transaction Cost", "Near-zero (private chain)", "$0.50-$5.00 (varies)", "$0.01-$0.10 (L2)", "Near-zero (permissioned)", "$0.10-$1.00 (Ethereum-based)"],
            ["Privacy", "Full confidentiality (private chain)", "Public / transparent", "Public / transparent", "Full confidentiality (permissioned)", "Partial (selective disclosure)"],
            ["Regulatory Compliance", "Built-in KYC/AML pipeline", "External / off-chain", "External / off-chain", "Configurable policies", "Built-in compliance tools"],
            ["AI Integration", "Native 6-stage AI pipeline", "External (oracles)", "External (oracles)", "External integration", "External (partner APIs)"],
            ["Custom Transactions", "Full AVM programmability", "Solidity smart contracts", "Solidity compatible", "Chaincode (Go/Java)", "Ethereum smart contracts"],
            ["Enterprise Readiness", "Purpose-built enterprise", "Improving (Enter. Mainnet)", "Moderate (enterprise L2)", "High (IBM/Intel backed)", "High (SEC-registered)"],
            ["Settlement Speed", "Custom block time (30s)", "~12 seconds", "~2 seconds", "Configurable (1-5s)", "~12 seconds (Ethereum)"],
        ],
        col_widths=[CONTENT_W * 0.14, CONTENT_W * 0.17, CONTENT_W * 0.15, CONTENT_W * 0.15, CONTENT_W * 0.19, CONTENT_W * 0.20],
        caption_text="Table 1.6: Comparative Analysis of Tokenization Platforms"
    ))

    story.extend([
        body(
            "The comparison reveals that Averon occupies a unique position in the platform "
            "landscape by combining the privacy and cost advantages of permissioned networks "
            "with the programmability typically associated with public chains. Unlike Ethereum "
            "and Polygon, which operate as public networks where all transaction data is visible "
            "to all participants, Averon's private blockchain ensures that sensitive financial "
            "data, including asset valuations, investor identities, and transaction details, "
            "remains confidential within the authorized network. This is a critical requirement "
            "for institutional asset tokenization, where regulatory obligations such as GDPR "
            "and data protection laws mandate strict controls over personal and financial "
            "information. Hyperledger Fabric offers similar privacy guarantees but lacks the "
            "native AI integration, custom virtual machine, and purpose-built trading "
            "infrastructure that Averon provides as integrated platform capabilities."
        ),

        body(
            "The transaction cost dimension is particularly significant for platforms that "
            "target high-frequency secondary market trading. Ethereum's gas fees, while "
            "reduced substantially by Layer 2 solutions, remain unpredictable and can spike "
            "during periods of network congestion, making them unsuitable for the micro-transaction "
            "patterns inherent in fractional asset trading. Polygon addresses this concern "
            "through its rollup architecture, achieving sub-cent transaction costs, but "
            "sacrifices some degree of decentralization and inherits Ethereum's privacy "
            "limitations. Averon's private chain eliminates gas fees entirely, as the "
            "computational cost of transaction validation is absorbed by the network operators "
            "rather than passed through to end users. Furthermore, Averon's native integration "
            "of AI-powered document verification, risk scoring, and compliance checking "
            "represents a capability that no competitor currently offers as a unified, "
            "built-in platform feature. Where other platforms require integration with "
            "third-party AI services through oracles or API bridges, Averon's six-stage "
            "AI pipeline operates as a first-class citizen within the platform architecture, "
            "reducing latency, improving data consistency, and eliminating third-party "
            "dependency risks."
        ),
    ])

    # ================================================================
    # AFTER CHAPTER 3 - Architecture
    # ================================================================

    story.extend([
        h2("3.4 Data Flow Architecture"),

        body(
            "Every request that enters the Averon platform traverses a carefully orchestrated "
            "path through the five-layer architecture, with each layer performing specific "
            "transformation, validation, and enrichment operations before passing control to "
            "the next. When a user initiates an asset tokenization request through the web "
            "interface or API, the request first arrives at the Presentation Layer, where it "
            "undergoes input validation, authentication verification, and rate limiting checks. "
            "The Presentation Layer translates the HTTP request into an internal command object "
            "and forwards it to the Application Layer, which serves as the orchestration "
            "brain. The Application Layer decomposes the high-level command into a sequence "
            "of domain operations, coordinating between the AI Service Layer for document "
            "analysis, the Domain Layer for business rule enforcement, and the Infrastructure "
            "Layer for persistent state changes. This layered approach ensures that concerns "
            "such as input sanitization, business logic validation, and data persistence remain "
            "strictly separated, enabling independent testing, modification, and scaling of "
            "each layer without cascading effects on the others."
        ),

        body(
            "Data persistence within Averon follows a polyglot storage strategy, where "
            "different data types are directed to the storage engine best suited to their "
            "access patterns and consistency requirements. Relational data, including user "
            "profiles, transaction records, and asset metadata, is stored in PostgreSQL with "
            "strict ACID guarantees and row-level locking for concurrent access. Document "
            "artifacts, such as property deeds, financial statements, and legal agreements, "
            "are stored as binary objects in the filesystem with metadata references maintained "
            "in the database, enabling fast retrieval while keeping the relational schema "
            "lean and queryable. Blockchain state, including token balances, smart contract "
            "code, and transaction hashes, is persisted in the custom LevelDB-based chain "
            "store, which is optimized for sequential write patterns and key-range scans "
            "typical of blockchain data access. The AI pipeline generates intermediate data "
            "artifacts, including extracted text from OCR processing, named entity annotations, "
            "and risk scoring results, which are cached temporarily in Redis with configurable "
            "time-to-live (TTL) values, reducing redundant computation for repeated document "
            "analyses."
        ),

        body(
            "The event-driven architecture within Averon enables loose coupling between "
            "services and supports asynchronous processing patterns that are essential for "
            "long-running operations such as AI document analysis and blockchain consensus. "
            "When a significant state change occurs, such as the completion of a trade, the "
            "issuance of new tokens, or the approval of a KYC application, the responsible "
            "service publishes an event to the internal event bus. Downstream services that "
            "have subscribed to relevant event types receive notifications and execute their "
            "corresponding handlers. For example, a trade completion event triggers the "
            "settlement service to execute escrow release, the notification service to send "
            "confirmation emails to both parties, the analytics service to update market "
            "statistics, and the compliance service to log the transaction for regulatory "
            "reporting. This publish-subscribe pattern ensures that adding new downstream "
            "behaviors, such as webhook integrations or real-time dashboard updates, requires "
            "no modification to the originating service, supporting the Open/Closed Principle "
            "and enabling the platform to evolve without introducing coupling between "
            "independently deployable components."
        ),

        spacer(8),

        # --- 3.5 Scalability Considerations ---
        h2("3.5 Scalability Considerations"),

        body(
            "Averon's scalability strategy encompasses both vertical scaling, which involves "
            "increasing the computational resources of individual server instances, and "
            "horizontal scaling, which involves distributing load across multiple instances "
            "working in concert. In the current architecture, vertical scaling provides the "
            "most immediate benefit for compute-intensive workloads such as AI model inference "
            "and blockchain mining, where adding CPU cores and GPU accelerators to existing "
            "nodes directly improves throughput. The AI pipeline, which runs models for OCR, "
            "classification, and named entity recognition, benefits significantly from GPU "
            "acceleration, with inference times decreasing by approximately 10x when compared "
            "to CPU-only execution. For the blockchain mining component, increasing the hash "
            "rate of validator nodes improves security against potential attacks while also "
            "reducing block confirmation latency, creating a dual benefit from vertical "
            "scaling investments."
        ),

        body(
            "Current bottlenecks in the system have been identified through load testing and "
            "production monitoring. The primary constraint is the synchronous AI pipeline "
            "execution during asset onboarding, where a single document verification flow "
            "can take 15 to 30 seconds to complete all six stages. This creates a queueing "
            "effect when multiple asset submissions arrive concurrently, resulting in increased "
            "latency for subsequent requests. The database layer represents a second bottleneck, "
            "particularly for complex analytical queries that join multiple large tables, such "
            "as generating investor portfolio reports or computing market-wide trading volume "
            "aggregations. The blockchain consensus mechanism, while adequate for current "
            "transaction volumes, introduces a hard upper bound on transaction throughput that "
            "is determined by the block time and block size parameters. With a 30-second block "
            "time and a maximum block size of 2 megabytes, the theoretical maximum transaction "
            "throughput is approximately 200 transactions per second, which is sufficient for "
            "current demand but may become constraining as the platform scales to support "
            "thousands of concurrent traders."
        ),

        body(
            "Future scaling paths have been designed to address these bottlenecks through a "
            "combination of architectural improvements and infrastructure enhancements. Read "
            "replicas will be introduced for the PostgreSQL database, directing analytical and "
            "reporting queries to dedicated replica instances while preserving write consistency "
            "on the primary node. A multi-level caching strategy, incorporating Redis for "
            "frequently accessed data such as user sessions, asset listings, and order book "
            "snapshots, will reduce database query volume by an estimated 60 to 80 percent "
            "for read-dominated operations. For static assets including document images, "
            "diagrams, and platform UI resources, a Content Delivery Network (CDN) will be "
            "deployed to serve geographically distributed users with low-latency access. The "
            "AI pipeline will be restructured to support asynchronous processing with a "
            "priority queue, allowing high-priority compliance checks to be processed ahead "
            "of lower-priority enrichment analyses. Finally, the blockchain layer is designed "
            "for a future migration to a Proof-of-Stake consensus mechanism, which will "
            "eliminate the computational overhead of mining while enabling faster block "
            "confirmation times and higher transaction throughput, as detailed in the dedicated "
            "chapter on consensus migration."
        ),

        spacer(8),

        # --- 3.6 Design Patterns Used ---
        h2("3.6 Design Patterns Used"),

        body(
            "The Repository Pattern is employed throughout Averon to provide a clean "
            "abstraction layer between the business logic in the Domain Layer and the data "
            "access mechanisms in the Infrastructure Layer. Each major domain entity, "
            "including users, assets, transactions, and orders, has a corresponding repository "
            "interface defined in the Domain Layer that specifies the contract for data "
            "operations such as find, save, delete, and query. The concrete implementations "
            "of these interfaces reside in the Infrastructure Layer and encapsulate all "
            "details of database connectivity, SQL query construction, and result mapping. "
            "This separation yields several benefits: the domain logic can be tested against "
            "mock repositories without requiring a running database instance, the underlying "
            "storage engine can be replaced or upgraded without modifying any business logic, "
            "and query optimization concerns are isolated within the repository implementations "
            "where they can be tuned independently. The repository pattern also enforces a "
            "consistent data access API across the entire codebase, reducing the cognitive "
            "burden on developers and preventing the proliferation of ad hoc SQL queries "
            "scattered throughout the application code."
        ),

        body(
            "The Factory Pattern is used extensively for transaction creation, where each "
            "transaction type, such as asset issuance, transfer, trade execution, and fee "
            "collection, requires a different set of fields, validation rules, and "
            "blockchain encoding formats. The TransactionFactory class provides static "
            "methods that accept high-level parameters and return fully constructed, "
            "validated transaction objects ready for signing and broadcast. For example, "
            "creating a trade transaction involves validating that both parties have "
            "sufficient balance, computing the applicable fees based on the current fee "
            "schedule, encoding the order details into the transaction payload, and setting "
            "appropriate gas limits. The factory encapsulates this complexity behind a simple "
            "interface, ensuring that callers do not need to understand the internal structure "
            "of transaction objects. This pattern also enables the introduction of new "
            "transaction types without modifying existing code, as new factory methods can be "
            "added independently of the callers that use them."
        ),

        body(
            "The Observer Pattern forms the backbone of Averon's event system, enabling "
            "loosely coupled communication between services. Each service that produces "
            "significant state changes acts as a subject, maintaining a list of registered "
            "observers that are notified when events occur. The event system supports both "
            "synchronous and asynchronous notification modes, with synchronous dispatch used "
            "for operations that must complete within the same request context, such as "
            "updating the order book after a trade, and asynchronous dispatch used for "
            "operations that can tolerate eventual consistency, such as sending notification "
            "emails or updating analytics dashboards. The Observer Pattern enables the "
            "platform to add new event consumers, such as webhook integrations, audit loggers, "
            "or real-time data feeds, without modifying the event-producing services, adhering "
            "to the Open/Closed Principle and supporting the platform's extensibility requirements."
        ),

        body(
            "The Strategy Pattern is applied to fee calculation, where different fee structures "
            "apply to different transaction types and user tiers. The FeeStrategy interface "
            "defines a single method, calculate_fee, that accepts a transaction context and "
            "returns the computed fee amount. Concrete implementations include "
            "TradingFeeStrategy, ListingFeeStrategy, and CapitalRaiseFeeStrategy, each "
            "encapsulating the specific logic for its fee category. This design allows the "
            "fee structure to be modified, extended, or replaced without changing the "
            "transaction processing code. For example, introducing a promotional fee waiver "
            "for early adopters requires only a new strategy implementation that returns zero "
            "fees for qualifying transactions, without any changes to the core trading engine."
        ),

        body(
            "The State Machine Pattern governs the lifecycle of tokenized assets on the "
            "Averon platform. Each asset progresses through a well-defined sequence of states, "
            "from initial creation and document submission through AI verification, compliance "
            "review, approval, listing on the marketplace, active trading, and eventual "
            "delisting or maturity. Each state transition is governed by specific preconditions, "
            "such as the completion of all required compliance checks before an asset can move "
            "to the approved state, and specific post-conditions, such as the automatic "
            "generation of blockchain tokens when an asset transitions to the listed state. "
            "The state machine implementation enforces these constraints programmatically, "
            "preventing invalid transitions and ensuring that every asset on the platform "
            "follows a consistent and auditable lifecycle path. This pattern also simplifies "
            "the UI layer, which can render different action buttons and information panels "
            "based on the current state of an asset, without embedding business rules in "
            "the presentation code."
        ),
    ])

    story.extend(make_table(
        [
            ["Pattern", "Application in Averon", "Benefit"],
            ["Repository", "Data access for all domain entities", "Decouples domain logic from storage; enables testing with mocks"],
            ["Factory", "Transaction object creation and validation", "Encapsulates complexity; supports adding new transaction types"],
            ["Observer", "Event system for cross-service communication", "Loose coupling; easy to add new event consumers"],
            ["Strategy", "Fee calculation across transaction types", "Flexible fee structures; open for extension, closed for modification"],
            ["State Machine", "Asset lifecycle management", "Enforces valid transitions; simplifies UI state rendering"],
        ],
        col_widths=[CONTENT_W * 0.18, CONTENT_W * 0.40, CONTENT_W * 0.42],
        caption_text="Table 3.6: Design Patterns Used in Averon Architecture"
    ))

    # ================================================================
    # AFTER CHAPTER 4 - Blockchain Layer
    # ================================================================

    story.extend([
        h2("4.7 Chain Security Analysis"),

        body(
            "The security of Averon's blockchain relies on a multi-layered defense strategy "
            "that addresses threats ranging from computational attacks on the consensus "
            "mechanism to social engineering attacks on network participants. The 51 percent "
            "attack, widely recognized as the most fundamental threat to Proof-of-Work "
            "blockchains, becomes increasingly impractical as the network's cumulative hash "
            "rate grows. In Averon's private chain context, where mining is restricted to "
            "authorized validator nodes operated by the platform's infrastructure team, the "
            "51 percent attack surface is further constrained by physical access controls, "
            "network segmentation, and the computational cost of the custom hashing algorithm. "
            "Unlike public blockchains where any participant can contribute hash power, "
            "Averon's permissioned mining model ensures that an attacker would need to "
            "compromise a majority of the validator infrastructure, which is distributed "
            "across multiple geographic regions and protected by enterprise-grade security "
            "controls including hardware security modules (HSMs), intrusion detection systems, "
            "and multi-signature authorization for configuration changes."
        ),

        body(
            "Sybil resistance in Averon's network is achieved through the combination of "
            "Proof-of-Work computational requirements and the permissioned node admission "
            "process. In a public blockchain, Sybil attacks involve creating a large number "
            "of pseudonymous identities to gain disproportionate influence over the consensus "
            "process. Averon mitigates this by requiring each validator node to be registered "
            "with a verified identity and authenticated through a mutual TLS handshake before "
            "being permitted to participate in block production. The economic security model "
            "further reinforces resistance to attacks by aligning the financial incentives of "
            "validators with the integrity of the network. Validators are required to stake "
            "a bond of platform tokens, which is partially slashed in the event of provable "
            "misbehavior such as double-signing blocks or submitting invalid transactions. "
            "This economic disincentive, combined with the reputational cost of being removed "
            "from the validator set, creates a formidable barrier against attacks even from "
            "insiders with legitimate access to the mining infrastructure."
        ),

        body(
            "Private chain security considerations extend beyond the consensus mechanism to "
            "encompass the entire operational environment in which the blockchain runs. "
            "Averon's validator nodes operate within isolated virtual network segments with "
            "strict firewall rules that limit inbound connections to other validator nodes "
            "and the platform's application servers. All inter-node communication is encrypted "
            "using TLS 1.3 with certificate pinning to prevent man-in-the-middle attacks. "
            "The blockchain data store is protected by filesystem-level encryption using "
            "AES-256, ensuring that even if an attacker gains physical access to the storage "
            "media, the chain data remains unreadable without the decryption key, which is "
            "stored in a separate HSM. Regular integrity checks compare the hash of each "
            "block against the previous block's hash reference, detecting any unauthorized "
            "modifications to the chain history. Additionally, a separate audit node maintains "
            "a read-only replica of the blockchain that is used for forensic analysis and "
            "regulatory reporting, providing an independent verification layer that cannot "
            "be tampered with even if the primary validator set is compromised."
        ),

        spacer(8),

        # --- 4.8 Transaction Lifecycle ---
        h2("4.8 Transaction Lifecycle"),

        body(
            "Every transaction on the Averon blockchain follows a precisely defined lifecycle "
            "that begins with creation by the application layer and concludes with irreversible "
            "confirmation on the chain. The process starts when a user action, such as placing "
            "a trade order or transferring tokens, triggers the TransactionFactory to construct "
            "a transaction object containing the sender's public key, the recipient's address "
            "(if applicable), the transaction payload encoding the specific operation, a "
            "nonce value incremented from the sender's previous transaction count, and a "
            "timestamp. The transaction object is then serialized into a canonical byte "
            "representation and presented to the sender's wallet for cryptographic signing "
            "using the ECDSA (Elliptic Curve Digital Signature Algorithm) with the secp256k1 "
            "curve. The signing process typically completes in under 50 milliseconds on modern "
            "hardware, after which the signed transaction is broadcast to the validator network "
            "through a gossip protocol that ensures rapid propagation to all nodes."
        ),

        body(
            "Upon receiving a broadcast transaction, each validator node performs an initial "
            "validation check that verifies the digital signature against the sender's public "
            "key, confirms that the nonce matches the expected value, checks that the sender "
            "has sufficient balance for any token transfers or fee payments, and validates "
            "the transaction payload structure against the AVM specification. Transactions "
            "that pass validation are added to the node's local transaction pool, also known "
            "as the mempool, where they await inclusion in a block by the current mining "
            "node. The mempool implements a priority queue that ranks transactions by fee "
            "density (fee per unit of payload size), ensuring that higher-value transactions "
            "are processed preferentially during periods of congestion. When the designated "
            "miner node assembles a new block, it selects transactions from the mempool in "
            "priority order, fills the block up to its maximum size limit, computes the "
            "Proof-of-Work nonce that satisfies the current difficulty target, and broadcasts "
            "the completed block to the network. The mining process typically requires between "
            "5 and 25 seconds depending on the current difficulty level, which is dynamically "
            "adjusted every 100 blocks to maintain the target block time of approximately "
            "30 seconds."
        ),

        body(
            "Block confirmation follows a multi-stage process that balances speed with "
            "security. When a validator node receives a new block from the miner, it "
            "independently verifies the block's Proof-of-Work, validates all included "
            "transactions against its own state, checks that the block's previous hash "
            "reference correctly points to the tip of the chain, and confirms that the "
            "block timestamp falls within the acceptable drift window. If all checks pass, "
            "the node appends the block to its local chain and broadcasts an acknowledgment "
            "to its peers. A transaction is considered confirmed once it is included in a "
            "block, but the platform requires three additional blocks to be mined on top of "
            "the confirmation block before considering the transaction final, a process that "
            "typically takes approximately 90 to 120 seconds. This confirmation depth provides "
            "protection against chain reorganizations that could theoretically occur if two "
            "miners produce valid blocks at nearly the same time, creating a temporary fork "
            "that is resolved when the longer chain eventually emerges as the authoritative "
            "history."
        ),

        spacer(8),

        # --- 4.9 Fork Resolution and Chain Reorganization ---
        h2("4.9 Fork Resolution and Chain Reorganization"),

        body(
            "Chain forks occur in any blockchain system when two or more miners produce valid "
            "blocks at approximately the same time, each extending the same parent block. "
            "This results in a temporary divergence where some nodes in the network follow one "
            "branch while others follow the alternative branch. Averon resolves these forks "
            "using the longest chain rule, also known as Nakamoto consensus, where nodes "
            "always consider the chain with the greatest cumulative difficulty, measured as "
            "the total number of blocks times the average difficulty of each block, to be "
            "the authoritative chain. When a node receives a block that extends a branch "
            "longer than its current chain tip, it performs a chain reorganization: it "
            "temporarily reverts any state changes from the blocks being orphaned, applies "
            "the state changes from the newly accepted blocks, and updates its chain tip to "
            "point to the new longest chain. This process is designed to be efficient and "
            "typically completes in milliseconds, as the maximum reorganization depth is "
            "limited to three blocks by the platform's configuration."
        ),

        body(
            "Orphan blocks, which are valid blocks that are not included in the longest chain, "
            "are handled by Averon's reorganization logic with careful attention to transaction "
            "integrity. When a block is orphaned, all transactions that were included in that "
            "block but not in the newly accepted chain are returned to the mempool, where they "
            "become eligible for inclusion in future blocks. Transactions that appear in both "
            "the orphaned and accepted chains are detected by their unique transaction hash "
            "and are not re-added to the mempool, preventing accidental double-processing. "
            "The platform maintains a limited cache of orphan blocks, typically the five most "
            "recent orphans, which can be referenced for audit purposes and debugging. In "
            "Averon's private chain environment with controlled validator participation, fork "
            "events are rare, occurring in less than 0.1 percent of block production events "
            "based on production telemetry, compared to rates of 1 to 3 percent observed on "
            "public blockchains with larger and more geographically distributed miner populations. "
            "This low fork rate is a direct benefit of the permissioned mining model, where "
            "the small number of validators reduces the probability of simultaneous block "
            "production while the high-speed inter-validator network minimizes propagation "
            "delays that contribute to fork formation."
        ),
    ])

    # ================================================================
    # AFTER CHAPTER 6 - Database Architecture
    # ================================================================

    story.extend([
        h2("6.4 Query Optimization Patterns"),

        body(
            "Averon's database query optimization strategy is built on a comprehensive indexing "
            "framework that balances query performance against write amplification overhead. "
            "The PostgreSQL database employs B-tree indexes as the default index type for "
            "equality and range queries on columns such as user_id, asset_id, and transaction "
            "status. For full-text search capabilities, particularly in the document management "
            "subsystem where users need to search across asset descriptions, legal document "
            "content, and compliance notes, GIN (Generalized Inverted Index) indexes are "
            "maintained on tsvector columns that store pre-computed lexical representations "
            "of text content. Partial indexes, which index only a subset of rows matching a "
            "WHERE clause condition, are used extensively for status-filtered queries, such as "
            "maintaining a dedicated index on the transactions table restricted to rows where "
            "status equals 'pending', which reduces the index size by over 90 percent compared "
            "to a full table index while dramatically accelerating the most frequently executed "
            "query pattern in the trading engine's order matching loop."
        ),

        body(
            "Query execution plans are continuously monitored and optimized through Averon's "
            "automated performance analysis pipeline. Every query that exceeds a configurable "
            "latency threshold, currently set at 200 milliseconds for OLTP queries and 5 "
            "seconds for analytical queries, is automatically captured along with its EXPLAIN "
            "ANALYZE output and logged to a dedicated performance monitoring table. A weekly "
            "automated review process analyzes these slow queries, identifies common patterns "
            "such as sequential scans on large tables, nested loop joins with high row "
            "estimates, and sort operations that exceed available work_mem, and generates "
            "optimization recommendations including suggested index additions, query "
            "rewrites, and configuration parameter adjustments. Connection pooling is "
            "implemented using PgBouncer, a lightweight connection pooler for PostgreSQL "
            "that maintains a pool of reusable database connections, eliminating the overhead "
            "of establishing new TCP connections for each application request. The pool is "
            "configured with a minimum of 10 and maximum of 100 connections, with an idle "
            "timeout of 300 seconds, ensuring that the database server is never overwhelmed "
            "by connection storms during traffic spikes while maintaining responsive "
            "performance during normal operations."
        ),

        body(
            "Advanced optimization techniques include the use of materialized views for "
            "computationally expensive aggregation queries that are accessed frequently but "
            "do not require real-time accuracy. For example, the market statistics dashboard, "
            "which displays metrics such as total trading volume, average transaction size, "
            "and active asset count, is backed by a materialized view that is refreshed every "
            "60 seconds through a scheduled cron job. This approach reduces the query "
            "response time from several seconds for a live aggregation over millions of "
            "transaction rows to sub-millisecond retrieval from the pre-computed materialized "
            "view. Table partitioning is employed for the transactions table, which is "
            "partitioned by month using PostgreSQL's declarative partitioning syntax, enabling "
            "efficient range queries on date-bounded queries and simplifying data archival "
            "by allowing entire partitions to be detached and moved to cold storage once they "
            "age beyond the regulatory retention requirement. The combination of strategic "
            "indexing, connection pooling, materialized views, and table partitioning ensures "
            "that the database layer maintains sub-100-millisecond query response times even "
            "as the data volume grows into the terabyte range."
        ),

        spacer(8),

        # --- 6.5 Data Integrity and Backup ---
        h2("6.5 Data Integrity and Backup"),

        body(
            "Data integrity in Averon's database layer is enforced through a combination of "
            "PostgreSQL's ACID (Atomicity, Consistency, Isolation, Durability) guarantees and "
            "application-level validation logic. Atomicity ensures that every database "
            "transaction, which may involve updates to multiple tables, either completes "
            "entirely or is fully rolled back, preventing partial state updates that could "
            "leave the system in an inconsistent state. For example, when a trade is executed, "
            "the database transaction updates the buyer's balance, the seller's balance, the "
            "order status, the escrow record, and the transaction history in a single atomic "
            "operation. Consistency is maintained through a combination of column constraints "
            "(NOT NULL, CHECK, UNIQUE), foreign key relationships that enforce referential "
            "integrity between related tables, and database triggers that automatically "
            "enforce business rules such as ensuring that an asset cannot be listed on the "
            "marketplace unless it has been approved through the compliance review process. "
            "The isolation level is configured to READ COMMITTED, which provides a balance "
            "between consistency and concurrency, preventing dirty reads while allowing "
            "non-repeatable reads that are acceptable in the platform's operational context. "
            "Durability is ensured through PostgreSQL's write-ahead logging (WAL), which "
            "records all changes to persistent storage before confirming transaction "
            "completion to the application."
        ),

        body(
            "The backup strategy follows the 3-2-1 principle: three copies of all data, "
            "stored on two different media types, with one copy maintained off-site. Full "
            "database backups are performed daily at 02:00 UTC using pg_basebackup, which "
            "creates a physically consistent copy of the entire database cluster including "
            "all tablespaces and configuration files. Incremental WAL archiving is enabled "
            "to support point-in-time recovery (PITR), allowing the database to be restored "
            "to any specific moment within the retention window, currently set to 30 days. "
            "The backup files are encrypted using AES-256 before being uploaded to object "
            "storage in a geographically separate data center, ensuring that a catastrophic "
            "failure at the primary site does not result in data loss. Backup integrity is "
            "verified daily through an automated restoration test that spins up a standby "
            "database instance from the most recent backup, executes a suite of consistency "
            "checks, and compares row counts and checksums against the production database. "
            "The mean recovery time objective (RTO) for a full database restoration is "
            "targeted at under 4 hours, with the mean recovery point objective (RPO) set at "
            "1 hour, meaning that in a worst-case disaster scenario, at most one hour of "
            "transaction data would be lost."
        ),
    ])

    # Database schema table showing all 19 tables
    story.extend(make_table(
        [
            ["Table", "Group", "Primary Key", "Key Relationships", "Row Estimate"],
            ["users", "Identity", "user_id (UUID)", "profiles.user_id, kyc_records.user_id, wallets.user_id", "10K-100K"],
            ["user_profiles", "Identity", "profile_id (UUID)", "users.user_id (FK)", "10K-100K"],
            ["kyc_records", "Compliance", "kyc_id (UUID)", "users.user_id (FK)", "10K-100K"],
            ["aml_flags", "Compliance", "flag_id (UUID)", "users.user_id (FK), kyc_records.kyc_id (FK)", "1K-50K"],
            ["assets", "Asset Mgmt", "asset_id (UUID)", "users.user_id (FK), asset_docs.asset_id (FK)", "1K-50K"],
            ["asset_documents", "Asset Mgmt", "doc_id (UUID)", "assets.asset_id (FK)", "5K-500K"],
            ["asset_tokens", "Asset Mgmt", "token_id (UUID)", "assets.asset_id (FK)", "10K-1M"],
            ["transactions", "Trading", "tx_id (UUID)", "users.user_id (FK), assets.asset_id (FK)", "100K-10M"],
            ["orders", "Trading", "order_id (UUID)", "users.user_id (FK), assets.asset_id (FK)", "50K-5M"],
            ["trades", "Trading", "trade_id (UUID)", "orders.order_id (FK), transactions.tx_id (FK)", "50K-5M"],
            ["escrow_records", "Settlement", "escrow_id (UUID)", "trades.trade_id (FK), transactions.tx_id (FK)", "50K-5M"],
            ["fee_records", "Finance", "fee_id (UUID)", "transactions.tx_id (FK), users.user_id (FK)", "100K-10M"],
            ["block_headers", "Blockchain", "block_hash (SHA-256)", "Self-referencing (prev_hash)", "100K-1M"],
            ["block_transactions", "Blockchain", "Composite (block_hash, tx_id)", "block_headers.block_hash (FK), transactions.tx_id (FK)", "100K-10M"],
            ["ai_verifications", "AI Pipeline", "verification_id (UUID)", "assets.asset_id (FK), asset_documents.doc_id (FK)", "5K-500K"],
            ["audit_logs", "Governance", "log_id (UUID)", "users.user_id (FK), transactions.tx_id (FK)", "1M-100M"],
            ["notifications", "System", "notification_id (UUID)", "users.user_id (FK)", "1M-50M"],
            ["wallets", "Identity", "wallet_id (UUID)", "users.user_id (FK)", "10K-100K"],
            ["api_keys", "System", "key_id (UUID)", "users.user_id (FK)", "1K-10K"],
        ],
        col_widths=[CONTENT_W * 0.14, CONTENT_W * 0.11, CONTENT_W * 0.17, CONTENT_W * 0.38, CONTENT_W * 0.12],
        caption_text="Table 6.5: Complete Database Schema Overview (19 Tables)"
    ))

    # ================================================================
    # AFTER CHAPTER 7 - AI Pipeline
    # ================================================================

    story.extend([
        h2("7.7 Model Training and Evaluation"),

        body(
            "The AI models powering Averon's document verification pipeline are trained on "
            "curated datasets that combine publicly available benchmarks with proprietary "
            "data collected from real-world asset tokenization workflows. The OCR (Optical "
            "Character Recognition) model is built on a hybrid architecture that combines "
            "Tesseract OCR for initial character-level text extraction with a deep learning "
            "post-processing model based on a transformer encoder-decoder architecture that "
            "corrects recognition errors, handles multi-language documents, and resolves "
            "layout ambiguities in complex document structures such as multi-column financial "
            "reports and annotated legal contracts. The training dataset for the OCR "
            "correction model consists of approximately 50,000 document images spanning "
            "property deeds, bank statements, incorporation certificates, and valuation "
            "reports, with each image manually annotated to establish ground truth text. Data "
            "augmentation techniques including random rotation, noise injection, blur, and "
            "contrast adjustment are applied during training to improve model robustness "
            "against the wide variation in document quality encountered in real-world "
            "submissions."
        ),

        body(
            "The document classification model employs a BERT (Bidirectional Encoder "
            "Representations from Transformers) backbone that has been fine-tuned on a "
            "labeled dataset of 20,000 asset-related documents spanning 15 distinct document "
            "categories including property deeds, financial statements, identity documents, "
            "legal agreements, insurance policies, and environmental assessments. Fine-tuning "
            "was performed over 10 epochs with a learning rate of 2e-5 using the AdamW "
            "optimizer, with the training set split into 80 percent training, 10 percent "
            "validation, and 10 percent test partitions. The named entity recognition (NER) "
            "model extends the spaCy NER pipeline with a custom transformer-based component "
            "trained to extract entity types specific to the asset tokenization domain, "
            "including property addresses, legal entity names, monetary amounts, dates, "
            "registration numbers, and jurisdiction identifiers. The risk scoring model uses "
            "an XGBoost gradient boosting classifier that ingests a feature vector of over "
            "200 dimensions derived from the document analysis results, including completeness "
            "scores, cross-reference consistency metrics, compliance flag counts, and "
            "historical approval rates for similar asset profiles."
        ),

        body(
            "Model evaluation is conducted using a comprehensive suite of metrics that capture "
            "different aspects of model performance. The classification model achieves an "
            "overall F1 score of 0.941 on the held-out test set, with precision of 0.953 and "
            "recall of 0.929, indicating a slight bias toward conservative predictions that "
            "prefer false negatives over false positives, a desirable characteristic for a "
            "compliance-oriented system where incorrectly classifying a document could have "
            "regulatory consequences. The NER model reports an entity-level F1 score of 0.918, "
            "with per-entity-type F1 scores ranging from 0.874 for jurisdiction identifiers "
            "(which exhibit the greatest variation in format) to 0.962 for monetary amounts "
            "(which follow relatively standardized patterns). The risk scoring model's "
            "discrimination capability is measured by the Area Under the Receiver Operating "
            "Characteristic Curve (AUC-ROC), which achieves 0.935, indicating strong "
            "separation between high-risk and low-risk asset profiles. All models undergo "
            "quarterly retraining cycles that incorporate newly labeled data from production "
            "feedback, with model versioning managed through a dedicated model registry that "
            "tracks training data hashes, hyperparameter configurations, and evaluation "
            "metrics for each model version."
        ),

        spacer(8),

        # --- 7.8 Performance Benchmarks ---
        h2("7.8 Performance Benchmarks"),

        body(
            "End-to-end performance of the AI pipeline has been benchmarked under controlled "
            "conditions using a standardized test set of 1,000 documents spanning all supported "
            "document categories. The following table presents the processing time and accuracy "
            "metrics for each stage of the pipeline, measured on a server equipped with an "
            "AMD EPYC 7763 CPU, 128 GB RAM, and an NVIDIA A100 GPU for model inference. These "
            "benchmarks represent median values across 10 independent runs, with the inter-"
            "quartile range (IQR) remaining within 15 percent of the median for all stages."
        ),
    ])

    story.extend(make_table(
        [
            ["Stage", "Input Type", "Processing Time", "Accuracy", "Model"],
            ["Preprocessing", "Image", "200 ms", "N/A", "OpenCV"],
            ["OCR Extraction", "Image", "1,500 ms", "97.3%", "Tesseract + DL Correction"],
            ["Classification", "Text", "300 ms", "94.1%", "BERT (fine-tuned)"],
            ["Named Entity Recognition", "Text", "200 ms", "91.8%", "spaCy + Custom Transformer"],
            ["Risk Scoring", "Structured", "100 ms", "89.5%", "XGBoost Classifier"],
            ["End-to-End Pipeline", "Image", "2,300 ms", "89.2% (composite)", "Combined Pipeline"],
        ],
        col_widths=[CONTENT_W * 0.18, CONTENT_W * 0.14, CONTENT_W * 0.18, CONTENT_W * 0.18, CONTENT_W * 0.32],
        caption_text="Table 7.8: AI Pipeline Performance Benchmarks"
    ))

    story.extend([
        body(
            "The benchmark results demonstrate that the complete AI pipeline processes a "
            "typical document in approximately 2.3 seconds, with the OCR extraction stage "
            "accounting for the largest share of processing time at 1.5 seconds. This "
            "dominance of the OCR stage is expected, as it involves both traditional "
            "character recognition and the subsequent deep learning correction pass, which "
            "requires GPU inference. The risk scoring stage is the fastest at 100 milliseconds, "
            "as it operates on pre-structured feature vectors rather than raw text or images. "
            "The composite end-to-end accuracy of 89.2 percent reflects the cumulative effect "
            "of errors across all pipeline stages, where errors in earlier stages propagate "
            "to subsequent stages. For example, an OCR error that misreads a monetary amount "
            "may cause the NER model to fail to extract the amount and the risk scoring model "
            "to compute an incorrect completeness score. Strategies for improving the composite "
            "accuracy include the introduction of cross-stage validation checks, where "
            "downstream models provide feedback to upstream models for iterative refinement, "
            "and the deployment of ensemble methods that combine the predictions of multiple "
            "model variants to reduce variance in individual model outputs."
        ),

        spacer(8),

        # --- 7.9 Continuous Learning and Model Improvement ---
        h2("7.9 Continuous Learning and Model Improvement"),

        body(
            "Averon's AI pipeline incorporates a continuous learning framework that enables "
            "models to improve over time based on production feedback. When compliance officers "
            "review AI-generated verification results, they can flag incorrect classifications, "
            "missed entities, or inaccurate risk scores through a dedicated feedback interface. "
            "These flagged items, along with the officer's correction, are stored in a labeled "
            "feedback dataset that accumulates over time. When the feedback dataset for a "
            "given model reaches a threshold of 500 new labeled examples, an automated "
            "retraining pipeline is triggered. This pipeline validates the new data for "
            "quality, balances the class distribution using stratified sampling, retrains the "
            "model with the combined original and new training data, evaluates the retrained "
            "model against a held-out test set, and promotes the new model to production only "
            "if it demonstrates statistically significant improvement over the current "
            "production model using a paired t-test with a significance threshold of p < 0.05. "
            "This automated retraining cycle ensures that the AI pipeline continuously adapts "
            "to evolving document formats, new regulatory requirements, and emerging patterns "
            "in asset tokenization submissions without requiring manual intervention from the "
            "machine learning engineering team."
        ),

        body(
            "A/B testing is employed for major model updates to validate performance "
            "improvements in the production environment before full deployment. When a new "
            "model version is a candidate for promotion, it is deployed alongside the current "
            "production model with traffic split 90/10, where 90 percent of documents continue "
            "to be processed by the current model and 10 percent are routed to the candidate "
            "model. The performance of both models is tracked over a minimum evaluation period "
            "of two weeks, during which key metrics including classification accuracy, entity "
            "extraction completeness, risk score calibration, and processing latency are "
            "continuously monitored. The candidate model is promoted to receive 100 percent "
            "of traffic only if it demonstrates improvement across all primary metrics without "
            "regression in any secondary metric, and if the confidence interval of the "
            "improvement excludes zero at the 95 percent confidence level. This rigorous "
            "evaluation process prevents model regressions and ensures that every deployed "
            "model update represents a genuine improvement in the platform's AI capabilities, "
            "maintaining the trust of compliance teams and regulatory auditors who rely on "
            "the AI pipeline as a critical component of the asset verification process."
        ),
    ])

    # ================================================================
    # AFTER CHAPTER 10 - Identity Layer
    # ================================================================

    story.extend([
        h2("10.3 W3C DID and Verifiable Credentials Specification"),

        body(
            "Averon's identity layer is built on the World Wide Web Consortium (W3C) "
            "Decentralized Identifier (DID) and Verifiable Credentials (VC) specifications, "
            "which provide standardized, interoperable frameworks for self-sovereign identity "
            "management. A Decentralized Identifier is a globally unique URI that is "
            "associated with a DID Document, a JSON-LD or CBOR-encoded data structure that "
            "contains the public keys, verification methods, and service endpoints associated "
            "with the identifier. Unlike traditional identifiers such as email addresses or "
            "social security numbers, which are issued and controlled by centralized authorities, "
            "DIDs are created and managed by the identity subject themselves, with the "
            "resolution and verification of the DID Document facilitated by a distributed "
            "verifiable data registry, which in Averon's case is the platform's private "
            "blockchain. Each Averon user is assigned a DID upon registration, formatted as "
            "did:averon:<unique-identifier>, and the corresponding DID Document is stored as "
            "an on-chain record that can be resolved by any authorized participant in the "
            "network, providing a tamper-proof, cryptographically verifiable binding between "
            "the identifier and the user's public verification keys."
        ),

        body(
            "The Verifiable Credentials specification enables Averon to issue cryptographically "
            "signed assertions about user attributes that can be independently verified by "
            "third parties without requiring direct communication with the issuer. When a user "
            "completes KYC verification, Averon issues a Verifiable Credential containing claims "
            "such as the user's verified name, date of birth, nationality, and KYC compliance "
            "status, signed using Averon's institutional private key. The credential is "
            "presented to the user's digital wallet, where it is stored for later presentation "
            "to other platform participants, such as asset issuers who require verified investor "
            "credentials before allowing participation in private placement offerings. The "
            "verification process involves the verifier resolving the issuer's DID to retrieve "
            "the issuer's public key, using that key to verify the digital signature on the "
            "credential, and checking the credential's revocation status against the on-chain "
            "revocation registry. This process is entirely cryptographic and does not require "
            "the verifier to contact the issuer directly, enabling trustless cross-party "
            "verification that scales efficiently as the number of participants and credentials "
            "in the ecosystem grows."
        ),

        body(
            "Zero-knowledge proofs extend the Verifiable Credentials framework by enabling "
            "users to prove specific properties about their credentials without revealing the "
            "underlying credential data. For example, a user can prove that they are above a "
            "certain age threshold without revealing their exact date of birth, or that their "
            "KYC status is valid without revealing their identity document number or nationality. "
            "Averon implements ZK-SNARKs (Zero-Knowledge Succinct Non-Interactive Arguments of "
            "Knowledge) for these selective disclosure scenarios, generating compact proofs "
            "that are typically under 200 bytes in size and can be verified in milliseconds "
            "regardless of the complexity of the underlying credential data. The proof "
            "generation process involves a trusted setup ceremony for each credential schema, "
            "where a common reference string is generated and the toxic waste (randomness that "
            "could be used to forge proofs) is securely destroyed. Averon's implementation "
            "uses the Groth16 proof system, which offers the smallest proof sizes and fastest "
            "verification times among currently available ZK-SNARK constructions, making it "
            "suitable for integration into the platform's transaction processing pipeline "
            "where proof verification must complete within the block confirmation time."
        ),

        spacer(8),

        # --- 10.4 Privacy-Preserving Identity ---
        h2("10.4 Privacy-Preserving Identity"),

        body(
            "Selective disclosure is the foundational privacy technique employed in Averon's "
            "identity layer, allowing users to share only the specific claims required for a "
            "given interaction rather than exposing their complete credential. The implementation "
            "uses a predicate-based disclosure system where the verifier specifies the "
            "predicates they require as satisfied, and the prover generates a zero-knowledge "
            "proof demonstrating that their credentials satisfy those predicates without "
            "revealing any additional information. For instance, when an asset issuer requires "
            "accredited investor verification, the verifier's policy might specify that the "
            "investor must have a net worth exceeding $1 million or an annual income exceeding "
            "$200,000. The investor's wallet generates a ZK-SNARK proof that these predicates "
            "are satisfied by the data in their KYC credential, and the verifier checks the "
            "proof against the issuer's public verification key. The proof reveals nothing "
            "about the investor's actual net worth or income, only that the threshold "
            "condition is met, providing strong privacy protection while maintaining the "
            "regulatory requirement for investor accreditation verification."
        ),

        body(
            "Blinding techniques provide an additional layer of privacy protection by "
            "decoupling the user's identity from their on-chain activities. When a user "
            "transacts on the Averon platform, their transaction is associated with a "
            "blinded identifier, a one-time public key derived from the user's DID through "
            "a deterministic but irreversible transformation. This blinded identifier changes "
            "with each transaction, preventing external observers from linking multiple "
            "transactions to the same user through on-chain analysis. The linkage between "
            "the blinded identifier and the user's actual DID is maintained only in the "
            "platform's off-chain identity service, which is accessible only to authorized "
            "compliance personnel under strict access control policies. This approach, often "
            "referred to as stealth addresses or unlinkable spendable tags in the cryptographic "
            "literature, provides a practical balance between the transparency required for "
            "regulatory compliance, where the platform operator must be able to identify "
            "the parties to any transaction, and the privacy desired by users, who do not "
            "wish their financial activities to be observable by other platform participants. "
            "The blinding transformation uses the Pedersen commitment scheme, which is "
            "computationally binding and perfectly hiding, ensuring that the blinded "
            "identifier reveals no information about the underlying DID while remaining "
            "cryptographically verifiable by the platform's compliance infrastructure."
        ),
    ])

    # ================================================================
    # AFTER CHAPTER 14 - Trading Engine
    # ================================================================

    story.extend([
        h2("14.4 Order Book Implementation Details"),

        body(
            "The order book at the core of Averon's trading engine is implemented using a "
            "pair of sorted data structures, one for buy orders and one for sell orders, "
            "each maintained in price-time priority order. Buy orders are sorted in descending "
            "order by price, so that the highest bid is always at the front of the array and "
            "is the first to be matched against incoming sell orders. Sell orders are sorted "
            "in ascending order by price, so that the lowest ask is always at the front and "
            "is the first to be matched against incoming buy orders. Within each price level, "
            "orders are sorted by timestamp to ensure that the earliest order at a given price "
            "is matched first, a principle known as price-time priority that is standard in "
            "financial exchange operations. The insertion of new orders into these sorted "
            "arrays uses binary search to locate the correct position, achieving O(log n) "
            "insertion time rather than the O(n) time of a naive linear scan. In practice, "
            "the order book typically contains between 100 and 10,000 active orders for a "
            "liquidly traded asset, and the binary search insertion completes in approximately "
            "3 to 5 microseconds on modern hardware, well within the platform's latency budget."
        ),

        body(
            "Concurrency handling in the order book is a critical concern because multiple "
            "trading operations may attempt to modify the order book simultaneously, "
            "particularly during periods of high market activity. Averon employs a fine-grained "
            "locking strategy where each asset's order book is protected by an independent "
            "read-write lock, allowing concurrent access to order books for different assets "
            "while serializing access to the same asset's order book. Within a single asset's "
            "order book, the matching engine acquires a write lock for the duration of the "
            "match-and-fill operation, which typically completes in under 1 millisecond, "
            "ensuring that concurrent orders for the same asset are processed sequentially "
            "and consistently. Read operations, such as retrieving the current order book "
            "snapshot for display in the user interface, acquire a read lock that allows "
            "multiple concurrent readers without blocking, enabling the platform to serve "
            "real-time market data to thousands of simultaneous viewers while the matching "
            "engine processes new orders without contention. This locking strategy has been "
            "validated under load testing with 500 concurrent order submissions per second "
            "across 10 different assets, with no deadlocks observed and maximum lock "
            "contention wait times remaining below 5 milliseconds."
        ),

        body(
            "Order cancellation is implemented as a two-phase operation to ensure consistency "
            "in the face of concurrent matching. When a user requests to cancel an open order, "
            "the system first marks the order as 'cancel-pending' in the database, which "
            "prevents the matching engine from selecting the order for execution. The "
            "matching engine, upon encountering a cancel-pending order during its scan, skips "
            "the order as if it did not exist. After the cancel-pending status is confirmed "
            "in the database, the order is removed from the in-memory order book data structure "
            "and its status is updated to 'cancelled'. This two-phase approach prevents a race "
            "condition where an order could be matched and cancelled simultaneously, which "
            "could result in an inconsistent state where the order appears both filled and "
            "cancelled. If the matching engine has already begun processing an order at the "
            "moment a cancellation request arrives, the cancellation is rejected with an "
            "appropriate error message indicating that the order has been matched and cannot "
            "be cancelled. The user receives real-time notification of the cancellation result "
            "through the platform's WebSocket-based event stream, which pushes order status "
            "updates to connected clients with sub-100-millisecond latency."
        ),

        spacer(8),

        # --- 14.5 Market Data and Analytics ---
        h2("14.5 Market Data and Analytics"),

        body(
            "Real-time market data feeds are generated by the trading engine's event pipeline, "
            "which publishes order book updates, trade executions, and price change notifications "
            "to a dedicated market data topic on the internal event bus. Subscribers to this "
            "topic include the WebSocket server that pushes real-time updates to connected "
            "clients, the analytics service that computes derived metrics such as the volume-"
            "weighted average price (VWAP), and the price discovery service that maintains "
            "the official last-traded-price for each asset. The VWAP is calculated as the "
            "ratio of the cumulative dollar value of all trades to the cumulative number of "
            "tokens traded over a specified time window, typically the trailing 24 hours or "
            "the current trading session. VWAP serves as a benchmark price that reflects the "
            "average execution price achieved by all market participants, and is widely used "
            "by institutional investors to assess the quality of their trade executions. A "
            "trade executed below the VWAP is generally considered favorable for a buyer, "
            "while a trade executed above the VWAP is favorable for a seller."
        ),

        body(
            "Open-high-low-close (OHLC) candlestick data is aggregated by the analytics "
            "service at configurable time intervals, supporting 1-minute, 5-minute, 15-minute, "
            "1-hour, 4-hour, and daily candles for each traded asset. Each candle captures "
            "the opening price (the first trade price in the interval), the highest price "
            "reached, the lowest price reached, the closing price (the last trade price), and "
            "the total trading volume within the interval. This data is stored in a dedicated "
            "time-series table and served through the market data API for charting and "
            "technical analysis. The candle generation process uses a streaming aggregation "
            "approach where incoming trades are applied to the current open candle, which is "
            "maintained in memory for sub-millisecond updates, and closed candles are flushed "
            "to the database in batch operations every 10 seconds. This approach ensures that "
            "real-time candlestick charts reflect the most recent trades without requiring "
            "a database query for each update, while the periodic batch flush ensures "
            "durability and queryability of historical candle data for backtesting and "
            "regulatory reporting purposes."
        ),

        spacer(8),

        # --- 14.6 Trade Examples ---
        h2("14.6 Trade Examples"),

        body(
            "To illustrate the order matching and trade execution process, consider the "
            "following step-by-step scenario involving three participants trading AC tokens "
            "on the Averon platform. The example demonstrates how limit orders interact "
            "with the order book, how partial fills are handled, and how the order book "
            "state evolves through successive operations."
        ),

        body(
            "<b>Step 1:</b> Alice places a buy limit order for 100 AC tokens at a price of "
            "5.00 per token. Since no sell orders exist in the order book, Alice's buy order "
            "cannot be immediately matched and is added to the bids side of the order book."
        ),
    ])

    story.extend(make_table(
        [
            ["Order Book After Step 1", "Price (AC)", "Quantity", "Order"],
            ["BIDS", "5.00", "100", "Alice (Buy Limit)"],
            ["ASKS", "--", "--", "(empty)"],
        ],
        col_widths=[CONTENT_W * 0.35, CONTENT_W * 0.20, CONTENT_W * 0.20, CONTENT_W * 0.25],
        caption_text="Table 14.6a: Order Book State After Alice's Buy Order"
    ))

    story.extend([
        body(
            "<b>Step 2:</b> Bob places a sell limit order for 50 AC tokens at a price of "
            "4.95 per token. The matching engine checks whether Bob's sell price of 4.95 is "
            "less than or equal to the best (highest) bid price in the order book, which is "
            "Alice's bid at 5.00. Since 4.95 is less than 5.00, a match occurs. The trade "
            "executes at the price of the resting order (Alice's bid at 5.00, per the "
            "maker-taker price priority rule), and 50 tokens are exchanged. Bob's entire sell "
            "order of 50 tokens is filled, while Alice's buy order is partially filled, "
            "leaving a remaining quantity of 50 tokens at her original price of 5.00."
        ),
    ])

    story.extend(make_table(
        [
            ["Order Book After Step 2", "Price (AC)", "Quantity", "Order"],
            ["BIDS", "5.00", "50", "Alice (Buy Limit, remaining)"],
            ["ASKS", "--", "--", "(empty)"],
            ["Trade Executed", "Price: 5.00", "Qty: 50", "Bob sells to Alice"],
        ],
        col_widths=[CONTENT_W * 0.35, CONTENT_W * 0.20, CONTENT_W * 0.20, CONTENT_W * 0.25],
        caption_text="Table 14.6b: Order Book State After Bob's Sell Order (Match at 5.00)"
    ))

    story.extend([
        body(
            "<b>Step 3:</b> Charlie places a sell limit order for 60 AC tokens at a price of "
            "5.00 per token. The matching engine checks whether Charlie's sell price of 5.00 "
            "is less than or equal to the best bid price of 5.00 (Alice's remaining order). "
            "Since 5.00 equals 5.00, a match occurs. The trade executes at 5.00, and 50 of "
            "Charlie's 60 tokens are exchanged with Alice, fully filling Alice's remaining buy "
            "order. Charlie's sell order now has a remaining unfilled quantity of 10 tokens, "
            "which is added to the asks side of the order book at a price of 5.00."
        ),
    ])

    story.extend(make_table(
        [
            ["Order Book After Step 3", "Price (AC)", "Quantity", "Order"],
            ["BIDS", "--", "--", "(empty)"],
            ["ASKS", "5.00", "10", "Charlie (Sell Limit, remaining)"],
            ["Trade Executed", "Price: 5.00", "Qty: 50", "Charlie sells to Alice"],
        ],
        col_widths=[CONTENT_W * 0.35, CONTENT_W * 0.20, CONTENT_W * 0.20, CONTENT_W * 0.25],
        caption_text="Table 14.6c: Order Book State After Charlie's Sell Order (Partial Match)"
    ))

    story.extend([
        body(
            "This example illustrates several key properties of Averon's matching engine: "
            "limit orders rest in the order book when they cannot be immediately matched; "
            "trades execute at the price of the resting (maker) order, providing price "
            "certainty to the passive liquidity provider; partial fills are handled correctly "
            "with remaining quantities preserved in the book; and the matching engine processes "
            "orders sequentially, ensuring deterministic and auditable execution outcomes. "
            "The total trading volume from this three-step scenario is 100 tokens across two "
            "trades, both executed at 5.00 per token, generating trading fees calculated "
            "according to the platform's fee schedule as described in Chapter 19."
        ),
    ])

    # ================================================================
    # AFTER CHAPTER 19 - Fee Structure
    # ================================================================

    story.extend([
        h2("19.3 Economic Model and Token Supply"),

        body(
            "Averon's economic model is built around a dual-token architecture consisting of "
            "the AC (Averon Coin) utility token and the AVR (Averon Reserve) governance token. "
            "The AC token serves as the primary medium of exchange within the platform, used "
            "for paying transaction fees, listing fees, and settlement costs. The total supply "
            "of AC is set at 1 billion tokens, with an initial circulating supply of 200 "
            "million tokens distributed through a combination of private sale (40 percent), "
            "community allocation (20 percent), team and advisor vesting (25 percent), and "
            "platform reserve (15 percent). The team and advisor allocation follows a 4-year "
            "linear vesting schedule with a 12-month cliff, ensuring long-term alignment between "
            "the core team's incentives and the platform's success. The AVR governance token, "
            "with a fixed supply of 100 million tokens, enables holders to participate in "
            "protocol governance decisions including fee parameter adjustments, new asset type "
            "approvals, and treasury allocation, distributed exclusively through community "
            "participation rewards and staking incentives."
        ),

        body(
            "Deflationary mechanisms are integral to Averon's token economic design, ensuring "
            "that the token supply decreases over time as platform usage grows. A portion of "
            "all trading fees, currently set at 20 percent, is permanently burned (destroyed "
            "and removed from circulation), creating a direct link between platform transaction "
            "volume and the reduction in token supply. Additionally, inactive accounts that "
            "have not engaged in any platform activity for 24 consecutive months are subject "
            "to a dormancy sweep, where their remaining AC balances are transferred to the "
            "platform treasury and the equivalent AVR governance tokens are burned. The "
            "treasury allocation from dormancy sweeps is used to fund ecosystem development "
            "grants, liquidity provisioning, and community incentive programs. Based on "
            "projected transaction volumes, the annual burn rate is expected to range from "
            "5 million to 50 million AC tokens, depending on the adoption scenario, which "
            "would reduce the total supply from 1 billion to between 750 million and 900 "
            "million tokens within the first five years of operation, creating scarcity-driven "
            "value appreciation for token holders."
        ),

        body(
            "Value accrual for the AC token is driven by multiple reinforcing mechanisms. "
            "First, the burn mechanism directly increases the value of each remaining token "
            "by reducing the total supply against a constant or growing demand base. Second, "
            "the platform's revenue buyback program allocates 10 percent of quarterly net "
            "revenue to open-market purchases of AC tokens, which are then added to the "
            "platform's liquidity pool to ensure smooth trading and reduce price volatility. "
            "Third, the staking mechanism allows AC holders to stake their tokens to earn a "
            "share of platform revenue, creating an opportunity cost for selling that reduces "
            "sell pressure. Fourth, institutional participants are required to maintain minimum "
            "AC balances as a form of economic commitment to the platform, creating structural "
            "demand from the largest users. The combination of these mechanisms creates a "
            "positive feedback loop where increased platform usage drives higher fee revenue, "
            "which funds larger token burns and buybacks, which increases token value, which "
            "attracts more participants, who generate additional fee revenue, perpetuating the "
            "cycle of ecosystem growth and token value appreciation."
        ),

        spacer(8),

        # --- 19.4 Revenue Projections ---
        h2("19.4 Revenue Projections"),

        body(
            "The following table presents Averon's projected revenue under three scenarios "
            "over a five-year horizon. The conservative scenario assumes modest user growth "
            "and limited institutional adoption. The moderate scenario reflects the base case "
            "with steady growth in line with market projections. The aggressive scenario "
            "assumes accelerated adoption driven by favorable regulatory developments and "
            "major institutional partnerships."
        ),
    ])

    story.extend(make_table(
        [
            ["Year", "Users", "Monthly Trades", "Trading Fees", "Listing Fees", "Capital Raise Fees", "Total Revenue"],
            ["Y1 (Cons.)", "2,500", "5,000", "$75K", "$50K", "$25K", "$150K"],
            ["Y1 (Mod.)", "5,000", "15,000", "$225K", "$150K", "$75K", "$450K"],
            ["Y1 (Aggr.)", "10,000", "40,000", "$600K", "$400K", "$200K", "$1.2M"],
            ["Y2 (Cons.)", "7,500", "20,000", "$300K", "$150K", "$100K", "$550K"],
            ["Y2 (Mod.)", "15,000", "60,000", "$900K", "$500K", "$300K", "$1.7M"],
            ["Y2 (Aggr.)", "30,000", "150,000", "$2.25M", "$1.2M", "$750K", "$4.2M"],
            ["Y3 (Cons.)", "15,000", "50,000", "$750K", "$300K", "$250K", "$1.3M"],
            ["Y3 (Mod.)", "35,000", "150,000", "$2.25M", "$1M", "$750K", "$4.0M"],
            ["Y3 (Aggr.)", "75,000", "400,000", "$6.0M", "$2.5M", "$2.0M", "$10.5M"],
            ["Y4 (Cons.)", "30,000", "100,000", "$1.5M", "$500K", "$500K", "$2.5M"],
            ["Y4 (Mod.)", "75,000", "350,000", "$5.25M", "$2M", "$1.5M", "$8.75M"],
            ["Y4 (Aggr.)", "150,000", "1M", "$15M", "$5M", "$4M", "$24M"],
            ["Y5 (Cons.)", "50,000", "200,000", "$3M", "$800K", "$1M", "$4.8M"],
            ["Y5 (Mod.)", "125,000", "700,000", "$10.5M", "$3.5M", "$3M", "$17M"],
            ["Y5 (Aggr.)", "300,000", "2M", "$30M", "$8M", "$7M", "$45M"],
        ],
        col_widths=[
            CONTENT_W * 0.11, CONTENT_W * 0.10, CONTENT_W * 0.14,
            CONTENT_W * 0.15, CONTENT_W * 0.14, CONTENT_W * 0.18, CONTENT_W * 0.18
        ],
        caption_text="Table 19.4: Five-Year Revenue Projections Under Three Scenarios"
    ))

    story.extend([
        body(
            "The revenue projections demonstrate significant variance between scenarios, "
            "reflecting the inherent uncertainty in platform adoption timelines. In the "
            "moderate scenario, which represents the management team's base case, the platform "
            "reaches $17 million in annual revenue by Year 5, driven by a combination of "
            "trading fee income (62 percent of total), capital raise fees (18 percent), and "
            "listing fees (20 percent). The aggressive scenario, while ambitious, is supported "
            "by comparable growth trajectories observed in early-stage fintech platforms and "
            "cryptocurrency exchanges, several of which have achieved billion-dollar revenue "
            "runs within five years of launch. The conservative scenario provides a floor "
            "estimate that assumes minimal institutional adoption and slower-than-expected "
            "retail growth, yet still demonstrates a viable business with $4.8 million in "
            "Year 5 revenue."
        ),

        spacer(8),

        # --- 19.5 Comparison with Traditional Finance Fees ---
        h2("19.5 Comparison with Traditional Finance Fees"),

        body(
            "One of Averon's most compelling value propositions is the dramatic reduction in "
            "fees compared to traditional financial intermediaries. The table below compares "
            "Averon's fee structure with the fees charged by traditional intermediaries for "
            "equivalent services. These fee comparisons are based on publicly available "
            "schedule of fees from major financial institutions and industry reports, and "
            "represent typical ranges for mid-market transactions."
        ),
    ])

    story.extend(make_table(
        [
            ["Service", "Traditional Fee", "Averon Fee", "Savings"],
            ["Investment Banking (Capital Raise)", "3-7% of raise amount", "1-2% of raise amount", "50-85%"],
            ["Real Estate Brokerage", "1-3% of transaction", "0.25-0.5% of transaction", "75-92%"],
            ["Stock Brokerage (Retail)", "0.1-0.5% per trade", "0.1-0.3% per trade", "20-70%"],
            ["Equity Crowdfunding Platforms", "5-10% of raise + 2-5% success fee", "2-4% of raise", "40-80%"],
            ["Fund Administration", "0.1-0.3% AUM annually", "0.05-0.15% AUM annually", "50-83%"],
            ["Compliance / KYC Processing", "$50-500 per verification", "$5-25 per verification", "85-98%"],
            ["Secondary Market Trading", "0.05-0.25% (exchange + broker)", "0.1-0.3% (platform fee)", "Competitive / Lower"],
        ],
        col_widths=[CONTENT_W * 0.26, CONTENT_W * 0.24, CONTENT_W * 0.24, CONTENT_W * 0.16],
        caption_text="Table 19.5: Averon Fees vs. Traditional Financial Intermediaries"
    ))

    story.extend([
        body(
            "The fee comparison reveals that Averon's platform-driven approach delivers cost "
            "savings of 50 to 98 percent across most service categories compared to traditional "
            "financial intermediaries. The most dramatic savings occur in compliance and KYC "
            "processing, where Averon's AI-powered automation reduces the per-verification cost "
            "from the $50 to $500 range charged by traditional compliance firms to $5 to $25, "
            "a reduction of 85 to 98 percent. This cost advantage is structural rather than "
            "promotional: it is driven by the fundamental difference between human-intensive "
            "manual verification processes and AI-automated pipeline processing that can "
            "handle orders of magnitude more verifications per dollar of infrastructure cost. "
            "Similarly, the elimination of physical paperwork, in-person meetings, and "
            "multi-day processing cycles in the capital raise workflow reduces investment "
            "banking fees from the standard 3 to 7 percent to 1 to 2 percent, making "
            "Averon viable for smaller raise amounts that would be uneconomical for "
            "traditional investment banks to service."
        ),

        body(
            "The disruption potential of Averon's fee structure extends beyond simple cost "
            "reduction to enable entirely new market segments that were previously "
            "underserved or completely unserved by traditional financial infrastructure. "
            "Real estate tokenization, for example, has been constrained by the high friction "
            "costs of traditional property transactions, where brokerage fees of 1 to 3 percent, "
            "legal fees of $5,000 to $25,000, and closing costs of 2 to 5 percent make "
            "fractional ownership economically impractical for properties valued under "
            "$500,000. Averon's combined fee of 0.25 to 0.5 percent for tokenization, trading, "
            "and settlement reduces the total friction cost to a level where fractional "
            "ownership of properties valued at $50,000 or less becomes economically viable, "
            "unlocking a multi-trillion-dollar addressable market of previously inaccessible "
            "real estate assets. This democratization of access, enabled by dramatically "
            "lower fees, represents the core of Averon's mission to make all forms of value "
            "freely tradable, composable, and accessible to a global audience of investors "
            "regardless of their geographic location, net worth, or institutional connections."
        ),
    ])

    # ================================================================
    # AFTER CHAPTER 24 - Security
    # ================================================================

    story.extend([
        h2("24.4 Threat Model Analysis"),

        body(
            "A comprehensive threat model is essential for systematically identifying and "
            "mitigating security risks across the platform. Averon employs a STRIDE-style "
            "threat modeling methodology that categorizes threats into six classes: Spoofing, "
            "Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation "
            "of Privilege. The following table maps each threat category to specific attack "
            "vectors relevant to the Averon platform, along with the corresponding mitigation "
            "strategies and the architectural layer at which the mitigation is implemented. "
            "This systematic approach ensures that no threat category is overlooked and that "
            "mitigations are applied at the appropriate layer of the defense-in-depth strategy."
        ),
    ])

    story.extend(make_table(
        [
            ["Threat Category", "Example Attack", "Mitigation", "Layer"],
            ["Spoofing", "Phishing / credential theft", "JWT + 2FA + rate-limited login", "Presentation"],
            ["Tampering", "Transaction data modification", "Blockchain immutability + digital signatures", "Blockchain"],
            ["Repudiation", "Denying executed transactions", "Hash chain audit trail + non-repudiation logs", "Domain + Blockchain"],
            ["Info Disclosure", "Data leakage / unauthorized access", "AES-256 encryption + RBAC + field-level encryption", "Infrastructure"],
            ["Denial of Service", "API flooding / resource exhaustion", "3-tier token bucket rate limiting + WAF", "Presentation + Infrastructure"],
            ["Elev. of Privilege", "Role escalation / admin access theft", "RBAC + principle of least privilege + audit", "Application + Domain"],
            ["Supply Chain", "Compromised dependency / package", "Pinned versions + SCA scanning + SBOM tracking", "Infrastructure"],
            ["Insider Threat", "Malicious admin / data exfiltration", "Separation of duties + encrypted logs + MFA", "Operations"],
        ],
        col_widths=[CONTENT_W * 0.15, CONTENT_W * 0.24, CONTENT_W * 0.36, CONTENT_W * 0.25],
        caption_text="Table 24.4: STRIDE Threat Model for the Averon Platform"
    ))

    story.extend([
        body(
            "The threat model has been developed through a collaborative process involving "
            "the platform's security engineering team, external penetration testing consultants, "
            "and compliance advisors with expertise in financial services security standards "
            "including PCI DSS, SOC 2 Type II, and ISO 27001. Each identified threat has been "
            "assessed for likelihood (rare, unlikely, possible, likely, almost certain) and "
            "impact (negligible, limited, significant, maximum), with the resulting risk "
            "scores used to prioritize mitigation investments. Threats rated as 'maximum' "
            "impact, including unauthorized access to the blockchain validator set, "
            "compromise of the master encryption key, and large-scale data exfiltration of "
            "user personal data, receive the highest investment priority and are subject to "
            "the most stringent controls, including multi-party computation for key management, "
            "hardware security modules for cryptographic operations, and real-time intrusion "
            "detection with automated response capabilities."
        ),

        body(
            "Penetration testing has been conducted on a semi-annual basis by independent "
            "security firms with demonstrated expertise in blockchain and financial technology "
            "assessments. The most recent engagement, conducted over a three-week period, "
            "employed a methodology aligned with the OWASP Web Security Testing Guide and the "
            "PTES (Penetration Testing Execution Standard) framework, covering all 10 categories "
            "of the OWASP Top 10, including injection attacks, broken authentication, sensitive "
            "data exposure, XML external entities, broken access control, security "
            "misconfiguration, cross-site scripting, insecure deserialization, using components "
            "with known vulnerabilities, and insufficient logging and monitoring. The assessment "
            "also included blockchain-specific tests such as smart contract fuzzing, consensus "
            "mechanism manipulation attempts, and transaction replay attacks. Across 47 "
            "individual test cases, the engagement identified 3 critical findings, 5 high-"
            "severity findings, 12 medium-severity findings, and 18 low-severity informational "
            "findings. All critical and high-severity findings were remediated within 48 hours "
            "of disclosure, with the remaining medium and low findings addressed within the "
            "subsequent sprint cycle, achieving a 100 percent remediation rate within the "
            "contractual 30-day remediation window."
        ),

        body(
            "Continuous security monitoring supplements the periodic penetration testing "
            "program through a suite of automated security tools integrated into the platform's "
            "CI/CD pipeline. Static Application Security Testing (SAST) is performed on every "
            "code commit using Semgrep with custom rules tailored to the Averon codebase, "
            "detecting common vulnerability patterns such as SQL injection, cross-site scripting, "
            "and improper input validation. Dynamic Application Security Testing (DAST) is "
            "performed against staging deployments using OWASP ZAP, which crawls the application "
            "and probes for vulnerabilities in the running system. Software Composition Analysis "
            "(SCA) using Snyk and Dependabot continuously monitors the platform's dependency "
            "tree for known vulnerabilities in third-party libraries, automatically generating "
            "pull requests for security patches when updates are available. The combination of "
            "these automated tools with periodic manual penetration testing creates a "
            "comprehensive security assurance program that identifies and addresses "
            "vulnerabilities at every stage of the software development lifecycle, from "
            "code authoring through deployment and production operation."
        ),

        spacer(8),

        # --- 24.6 Incident Response Plan ---
        h2("24.6 Incident Response Plan"),

        body(
            "Averon's incident response plan follows the NIST Computer Security Incident "
            "Handling Guide (SP 800-61) framework, organized into four phases: detection, "
            "containment and eradication, recovery, and post-incident review. The detection "
            "phase relies on a multi-layered monitoring stack that includes application-level "
            "anomaly detection (identifying unusual API call patterns, authentication failures, "
            "and data access patterns), infrastructure-level monitoring (CPU, memory, disk, and "
            "network metrics with threshold-based alerting), and blockchain-level monitoring "
            "(detecting unusual transaction volumes, atypical block sizes, and potential "
            "consensus anomalies). When an anomaly is detected, an automated triage system "
            "assigns a severity level based on the affected system, the potential data impact, "
            "and the estimated blast radius, and notifies the on-call incident responder "
            "through PagerDuty with a structured alert containing all relevant context "
            "including the detection source, affected components, initial assessment, and "
            "recommended containment actions."
        ),

        body(
            "The containment and eradication phase begins with the incident responder "
            "confirming the severity assessment and assembling the incident response team, "
            "which includes representatives from security engineering, platform engineering, "
            "compliance, and communications. For security incidents, the immediate containment "
            "actions include isolating affected systems from the network, revoking potentially "
            "compromised credentials, and activating the platform's incident mode, which "
            "disables non-essential features and redirects all user traffic to a maintenance "
            "page with a status update. Eradication involves identifying the root cause, "
            "whether it is a software vulnerability, a misconfiguration, or a compromised "
            "credential, and implementing a permanent fix. The recovery phase restores affected "
            "systems to normal operation, including restoring from verified backups if data "
            "integrity has been compromised, deploying the eradication fix to production, and "
            "gradually re-enabling features while monitoring for signs of recurrence. The "
            "post-incident review, conducted within 72 hours of incident resolution, produces "
            "a detailed report documenting the timeline, root cause analysis, impact assessment, "
            "lessons learned, and specific action items with assigned owners and deadlines to "
            "prevent similar incidents in the future. All incidents and their resolutions are "
            "tracked in a centralized incident management system and reviewed quarterly by the "
            "security leadership team to identify systemic patterns and prioritize platform "
            "security improvements."
        ),
    ])

    # ================================================================
    # AFTER CHAPTER 25 - Operations
    # ================================================================

    story.extend([
        h2("25.5 Disaster Recovery"),

        body(
            "Averon's disaster recovery strategy is designed to ensure business continuity "
            "in the event of a major infrastructure failure, natural disaster, or cybersecurity "
            "incident that renders the primary data center inoperable. The Recovery Point "
            "Objective (RPO) is set at 1 hour, meaning that the maximum acceptable data loss "
            "is one hour of transaction history. The Recovery Time Objective (RTO) is set at "
            "4 hours for full platform restoration, with a degraded mode RTO of 30 minutes "
            "that restores core trading functionality while non-essential features such as "
            "analytics dashboards and report generation remain offline. To achieve these "
            "targets, the platform maintains a geographically redundant deployment across two "
            "data centers separated by at least 500 kilometers, with asynchronous database "
            "replication ensuring that the standby site is never more than one hour behind "
            "the primary site. The blockchain validator set is distributed across both data "
            "centers, with a quorum of validators required for block production, ensuring "
            "that the loss of a single data center does not halt chain progress."
        ),

        body(
            "Failover procedures are documented in detailed runbooks that specify the step-by-"
            "step actions required to activate the disaster recovery site. The failover "
            "process begins with automated health checks that monitor the primary site's "
            "availability every 15 seconds. If the primary site fails three consecutive health "
            "checks (a 45-second detection window), the failover automation promotes the "
            "standby database to primary status, updates DNS records to redirect traffic to "
            "the disaster recovery site, and notifies the operations team through the incident "
            "response channel. For scenarios where the primary site is degraded but not "
            "completely unavailable, a manual failover can be initiated by the on-call "
            "engineer through a single command that executes the full failover sequence while "
            "preserving any remaining replicable data from the primary site. The failover "
            "process has been tested quarterly through planned disaster recovery drills, where "
            "the primary site is intentionally taken offline and the team validates that the "
            "standby site assumes the full workload within the RTO target, all data is "
            "consistent, and all platform features operate correctly. The most recent drill "
            "achieved a failover time of 22 minutes from detection to full service restoration, "
            "significantly outperforming the 4-hour RTO target."
        ),

        spacer(8),

        # --- 25.6 Performance Benchmarks ---
        h2("25.6 Performance Benchmarks"),

        body(
            "System performance is continuously monitored against defined targets across all "
            "critical platform components. The following table presents the current performance "
            "benchmarks measured under production load conditions, comparing actual metrics "
            "against the targets defined in the platform's service level objectives (SLOs). "
            "These measurements are collected by the monitoring infrastructure and aggregated "
            "into daily, weekly, and monthly reports that are reviewed by the engineering and "
            "operations leadership teams."
        ),
    ])

    story.extend(make_table(
        [
            ["Metric", "Target", "Actual", "Status"],
            ["API Latency (p50)", "< 100 ms", "45 ms", "Pass"],
            ["API Latency (p95)", "< 300 ms", "180 ms", "Pass"],
            ["API Latency (p99)", "< 1000 ms", "620 ms", "Pass"],
            ["Trading Throughput", "> 100 orders/sec", "150 orders/sec", "Pass"],
            ["Block Mining Rate", "~30 sec/block", "28.5 sec/block", "Pass"],
            ["AI Pipeline Throughput", "> 50 docs/min", "65 docs/min", "Pass"],
            ["Database Query (p95)", "< 200 ms", "85 ms", "Pass"],
            ["WebSocket Message Latency", "< 100 ms", "35 ms", "Pass"],
            ["Page Load Time (p95)", "< 2 sec", "1.4 sec", "Pass"],
            ["Uptime (30-day rolling)", "> 99.9%", "99.97%", "Pass"],
        ],
        col_widths=[CONTENT_W * 0.30, CONTENT_W * 0.20, CONTENT_W * 0.22, CONTENT_W * 0.13],
        caption_text="Table 25.6: System Performance Benchmarks vs. SLO Targets"
    ))

    # ================================================================
    # AFTER CHAPTER 30 - Vision
    # ================================================================

    story.extend([
        h2("30.3 Ecosystem Growth Strategy"),

        body(
            "Averon's ecosystem growth strategy is organized around three interconnected "
            "pillars: developer adoption, institutional partnerships, and community governance "
            "evolution. Developer adoption is driven by the platform's comprehensive SDK and "
            "REST API, which enable third-party developers to build applications on top of "
            "Averon's infrastructure without needing to understand the underlying blockchain "
            "or AI complexities. The developer growth plan includes a dedicated developer "
            "portal with interactive documentation, code samples in Python, JavaScript, and "
            "Go, a sandbox environment with pre-populated test data, and a developer grant "
            "program that provides funding and mentorship for builders creating innovative "
            "applications in areas such as decentralized lending against tokenized collateral, "
            "automated portfolio management for tokenized asset holdings, and cross-border "
            "settlement solutions that leverage Averon's compliance infrastructure. The "
            "target is to onboard 500 active developers and support 50 third-party "
            "applications within the first two years of platform launch, creating a rich "
            "ecosystem of complementary services that increases the platform's value "
            "proposition for all participants."
        ),

        body(
            "Institutional partnerships form the second pillar of the growth strategy, "
            "focusing on establishing Averon as the preferred tokenization infrastructure for "
            "regulated financial institutions. The partnership framework includes technology "
            "integration partnerships with custodian banks, compliance technology providers, "
            "and traditional exchange operators, as well as distribution partnerships with "
            "investment banks, private equity firms, and real estate investment trusts (REITs) "
            "that seek to tokenize their portfolios. Each institutional partnership follows a "
            "structured onboarding process that includes a dedicated integration team, "
            "regulatory alignment workshops, and a joint go-to-market plan. Early partnership "
            "targets include institutions in jurisdictions with favorable regulatory frameworks, "
            "particularly the UAE (via VARA licensing), Singapore (via MAS Project Guardian), "
            "and the EU (via MiCA passporting), where regulatory clarity enables institutions "
            "to adopt tokenization technology with confidence. The revenue model for institutional "
            "partnerships includes a combination of platform licensing fees, transaction-based "
            "revenue sharing, and custom development services for white-label deployments."
        ),

        body(
            "Community governance evolution represents the long-term vision for Averon's "
            "decentralization journey. While the platform currently operates under centralized "
            "governance by the core team, the roadmap includes a phased transition to "
            "community-driven governance over a five-year horizon. Phase 1 (Year 1-2) "
            "establishes a governance forum where token holders can propose and discuss "
            "platform improvements, with the core team retaining final decision authority. "
            "Phase 2 (Year 2-3) introduces advisory voting, where community votes on non-"
            "binding proposals inform the core team's decisions and create a feedback loop "
            "between the community and the platform's development direction. Phase 3 (Year 3-4) "
            "implements binding governance for a defined set of protocol parameters, such as "
            "fee rates, new asset type approvals, and treasury allocation, with the AVR "
            "governance token serving as the voting mechanism. Phase 4 (Year 4-5) explores "
            "full protocol decentralization, where the core team's administrative privileges "
            "are progressively removed and replaced by on-chain governance mechanisms, "
            "transforming Averon from a platform-operated service to a community-governed "
            "protocol. This gradual approach ensures that governance decentralization proceeds "
            "at a pace that maintains regulatory compliance, operational stability, and "
            "community alignment at each stage of the transition."
        ),

        spacer(8),

        # --- 30.4 Conclusion ---
        h2("30.4 Conclusion"),

        body(
            "This book has presented a comprehensive examination of the Averon platform, "
            "covering every dimension of its architecture from the foundational blockchain "
            "layer through the application interfaces that developers and end users interact "
            "with. We have explored the five-layer architecture that provides a clean "
            "separation of concerns across presentation, application, domain, AI services, "
            "and infrastructure, enabling each layer to evolve independently while maintaining "
            "coherence as a unified platform. We have examined the custom Proof-of-Work "
            "blockchain engine and its Averon Virtual Machine, the AI-powered document "
            "verification pipeline that automates compliance workflows, the decentralized "
            "identity layer built on W3C standards, the trading engine with its price-time "
            "priority order book, and the security architecture that implements defense-in-"
            "depth across every layer of the system. Each of these components has been "
            "designed not in isolation but as part of an integrated whole, where data flows "
            "seamlessly between layers and services through an event-driven architecture that "
            "enables loose coupling, independent scalability, and continuous evolution."
        ),

        body(
            "Averon's unique value proposition lies in the convergence of three capabilities "
            "that no existing platform offers as an integrated whole: a private blockchain "
            "with full transaction confidentiality and near-zero gas costs, a native AI "
            "pipeline that automates the most labor-intensive aspects of asset tokenization "
            "including document verification, risk assessment, and compliance checking, and "
            "a purpose-built trading infrastructure with an order book, escrow mechanism, "
            "and regulatory-compliant settlement process designed specifically for tokenized "
            "real-world assets. Existing platforms offer one or two of these capabilities "
            "but require integration with third-party services for the rest, introducing "
            "latency, cost, and security dependencies that Averon eliminates through its "
            "integrated design. The platform's fee structure, with savings of 50 to 98 "
            "percent compared to traditional financial intermediaries, creates an economic "
            "imperative for adoption that is reinforced by the regulatory compliance "
            "capabilities built into every layer of the system."
        ),

        body(
            "The transformative potential of the digital asset economy extends far beyond the "
            "mere digitization of existing financial instruments. Tokenization enables the "
            "creation of entirely new asset classes and financial products that were previously "
            "impossible or impractical, including fractional ownership of income-producing "
            "assets, programmable financial instruments with embedded compliance logic, and "
            "composable asset portfolios that can be combined, split, and recombined in novel "
            "ways. Averon is positioned at the center of this transformation, providing the "
            "infrastructure layer that bridges the physical world of tangible assets with the "
            "digital world of programmable value. As regulatory frameworks mature, institutional "
            "adoption accelerates, and the technology stack continues to improve, the question "
            "is not whether asset tokenization will become a fundamental pillar of global "
            "finance, but how quickly and how comprehensively the transition will occur. "
            "Averon's mission is to ensure that this transition happens in a way that is "
            "inclusive, compliant, and built on a foundation of technical excellence, and "
            "this book serves as both a technical specification of that foundation and an "
            "invitation to the broader community of developers, institutions, and innovators "
            "to join in building the future of programmable assets."
        ),
    ])
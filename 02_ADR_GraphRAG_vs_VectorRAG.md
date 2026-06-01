# Architecture Decision Record (ADR): GraphRAG for Complex Operational Data

## Context and Problem Statement
Standard Vector databases (Vector RAG) utilize semantic similarity, which is highly effective for basic document retrieval but fails at complex relational mapping. 

**Business Use Case:** Managing operational and financial data across a multi-unit real estate portfolio (e.g., Stepping Stone LLC). 
If an executive asks the AI: *"What is the total maintenance ROI impact of the Tupelo model property in the Franklin 37064 zip code over the last fiscal year?"*, standard Vector RAG fails. It cannot explicitly connect the tenant's maintenance request, the specific "Tupelo" floor plan entity, the Franklin property tax records, and the LLC's annual financial report.

## The GraphRAG Solution
To solve this, we implement a Knowledge Graph (GraphRAG) architecture. 

### Implementation Strategy
Instead of merely chunking text into vector embeddings, the ingestion pipeline utilizes Python to extract specific entities and create relational edges:
*   `Entity A:` Stepping Stone LLC
*   `Entity B:` Franklin 37064 Property
*   `Entity C:` Tupelo Floor Plan
*   `Entity D:` HVAC Maintenance Ledger

### Outcome
GraphRAG traverses the semantic network, understanding that the maintenance ledger belongs to the Tupelo unit, which is an asset of the LLC. This enables the LLM to generate precise, financially accurate answers for complex business operations, shifting the AI from a simple "search engine" to an operational intelligence tool.


graph TD
    %% Styling
    classDef fail fill:#ffe6e6,stroke:#ff0000,stroke-width:2px;
    classDef success fill:#e6ffe6,stroke:#008000,stroke-width:2px;
    classDef entity fill:#e6f3ff,stroke:#0066cc,stroke-width:2px;

    subgraph "Standard Vector RAG (Fails Context)"
        A[Query: Tupelo unit maintenance ROI in 37064?] --> B(Semantic Vector Search)
        B --> C[Returns irrelevant, generic property docs]:::fail
    end

    subgraph "GraphRAG Architecture (Contextual Success)"
        D[Stepping Stone LLC]:::entity -->|Owns Asset| E[Franklin 37064 Property]:::entity
        E -->|Contains| F[Tupelo Floor Plan]:::entity
        F -->|Incurs| G[HVAC Maintenance Ledger]:::entity
        
        H[Query: Tupelo unit maintenance ROI in 37064?] --> I(Knowledge Graph Traversal)
        I --> J[Exact Financial Impact Synthesized]:::success
        G -.-> J
    end

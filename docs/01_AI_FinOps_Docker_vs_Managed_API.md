# Architecture Decision Record (ADR): AI FinOps & Self-Hosted Infrastructure

## Executive Summary
Enterprise reliance on managed AI API endpoints (e.g., OpenAI Enterprise) creates unsustainable, variable OpEx scaling as token consumption grows. This document outlines the FinOps strategy for migrating non-reasoning-heavy RAG workloads to a containerized, self-hosted infrastructure.

## Business Problem
At scale, processing 5 million tokens daily through managed SaaS LLMs generates thousands of dollars in monthly recurring cloud fees. Furthermore, transmitting proprietary operational data to external API endpoints introduces latency and compliance risks.

## Architectural Solution: Containerized Local Deployment
To eliminate SaaS subscription fees and control infrastructure costs, we deploy open-source models (e.g., Llama 3) locally via Docker Desktop environments.

### Storage & Resilience Architecture
A primary concern with local containerization is data persistence and disaster recovery. Instead of relying on vulnerable default local volumes, the system architecture dictates modifying the `.env` file configurations to route the active container storage directories directly into a OneDrive-synced folder path (e.g., routing `UPLOAD_LOCATION` to the cloud-synced directory). 

**The ROI:** 
1. **Zero Cloud Compute Fees:** Inference runs entirely on ammortized local hardware.
2. **Enterprise-Grade Backup:** By utilizing the OneDrive-synced directory for the Docker volumes, the self-hosted AI server maintains automated, continuous cloud backups without requiring secondary, paid cloud-backup services.
3. **Data Sovereignty:** Proprietary data never leaves the internal network perimeter.

👉 **[Launch the Live Interactive AI FinOps ROI Calculator](https://your-unique-streamlit-url-here.streamlit.app/)**
```mermaid
graph TD
    %% Styling
    classDef highCost fill:#ffe6e6,stroke:#ff0000,stroke-width:2px;
    classDef lowCost fill:#e6ffe6,stroke:#008000,stroke-width:2px;
    classDef storage fill:#e6f3ff,stroke:#0066cc,stroke-width:2px;

    subgraph "Legacy Architecture (High OpEx)"
        A[Enterprise User Query] --> B(External API Gateway)
        B --> C{Claude / GPT-4 Endpoint}
        C --> D[Monthly API Bill: $5,000+ / month]:::highCost
    end

    subgraph "Optimized Self-Hosted Architecture (Zero Inference OpEx)"
        E[Enterprise User Query] --> F(Local API Gateway / Router)
        F --> G{Docker Desktop: Llama 3 Container}
        G --> H[Local Inference Cost: $0.00]:::lowCost
        
        %% Seamless Cloud Backup Integration
        G -.-> |State & Data Persistence| I[(Local .env Configured Volume)]:::storage
        I -.-> |Automated Sync| J[OneDrive Synced 'Pictures' Directory]:::storage
        J -.-> |Redundancy| K[Enterprise Cloud Backup: $0.00 Add-on]:::lowCost
    end
```

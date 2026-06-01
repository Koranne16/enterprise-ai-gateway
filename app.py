"""
Enterprise LLM FinOps & RAG Cost Optimizer
Author: Nikhil R. Koranne
Role: Director of Engineering / Sr. TPM

Description: 
Calculates monthly OpEx reduction achieved through Semantic Caching 
(e.g., Redis/Pinecone) and Token Compression in an enterprise RAG pipeline.
"""

import streamlit as st
import pandas as pd

# TODO: Future iteration - integrate directly with pgvector logs to pull live cache hit rates.
# Currently using manual slider inputs for architectural modeling.

def calculate_opex(queries_per_day: int, context_tokens: int, hit_rate_pct: float, compression_pct: float, cost_per_1k: float = 0.01) -> dict:
    """
    Calculates the baseline vs optimized monthly compute costs for LLM inference.
    """
    days_in_month = 30
    
    # Baseline Math (Unoptimized)
    baseline_daily_tokens = queries_per_day * context_tokens
    baseline_monthly_cost = (baseline_daily_tokens / 1000) * cost_per_1k * days_in_month

    # Optimized Math (Semantic Caching + Compression)
    cache_miss_rate = 1.0 - (hit_rate_pct / 100)
    retained_token_rate = 1.0 - (compression_pct / 100)
    
    optimized_daily_tokens = (queries_per_day * cache_miss_rate) * (context_tokens * retained_token_rate)
    optimized_monthly_cost = (optimized_daily_tokens / 1000) * cost_per_1k * days_in_month

    savings = baseline_monthly_cost - optimized_monthly_cost

    return {
        "baseline": round(baseline_monthly_cost, 2),
        "optimized": round(optimized_monthly_cost, 2),
        "savings": round(savings, 2)
    }

def main():
    st.set_page_config(page_title="LLM FinOps Optimizer", layout="centered")
    
    st.title("📊 Enterprise AI FinOps Calculator")
    st.markdown("#### RAG Architecture Cost Optimization Model")
    st.write("Model the financial impact of deploying semantic caching and token compression layers in front of frontier models (Claude 3.5 / GPT-4).")

    st.divider()

    # --- Sidebar for Global Constraints ---
    st.sidebar.header("Infrastructure Constants")
    cost_per_1k = st.sidebar.number_input("API Cost per 1k Tokens ($)", value=0.01, format="%.4f")
    st.sidebar.markdown("*Note: Default assumes blended input/output costs for standard enterprise queries.*")

    # --- Main Application Inputs ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Throughput Volume")
        queries = st.slider("Queries per Day", min_value=1000, max_value=100000, value=10000, step=1000)
        tokens = st.slider("Avg. Context Tokens/Query", min_value=500, max_value=128000, value=4000, step=500)

    with col2:
        st.subheader("2. Architecture Optimizations")
        cache_hit_rate = st.slider("Semantic Cache Hit Rate (%)", min_value=0, max_value=100, value=30, step=5)
        compression_rate = st.slider("Prompt Compression (%)", min_value=0, max_value=80, value=40, step=5)

    # --- Execution & Calculation ---
    metrics = calculate_opex(queries, tokens, cache_hit_rate, compression_rate, cost_per_1k)

    st.divider()
    
    # --- Executive Dashboard Outputs ---
    st.subheader("Monthly OpEx Impact")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Baseline Cost (Unoptimized)", f"${metrics['baseline']:,.2f}")
    m2.metric("Optimized Infrastructure Cost", f"${metrics['optimized']:,.2f}", delta=f"-${metrics['savings']:,.2f}", delta_color="inverse")
    m3.metric("Total Monthly Savings", f"${metrics['savings']:,.2f}")

    st.write("---")
    st.caption("Architecture Node: Routing redundant queries to Redis/Pinecone semantic cache bypasses external API endpoints, strictly reducing monthly variable compute costs.")

if __name__ == "__main__":
    main()

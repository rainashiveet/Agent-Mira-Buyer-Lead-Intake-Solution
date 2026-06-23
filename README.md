# Buyer Lead Intake Agent

### AgentMira Engineering Case Study | DTU Campus Recruitment 2025-26

## Overview

This repository contains a fully functional **Buyer Lead Intake Agent** designed to process raw, free-text buyer inquiries and generate actionable Lead Briefs for licensed realtors.

The solution follows a **multi-stage agentic pipeline** that separates security validation, requirement extraction, property matching, and brief generation into independent components. This approach improves maintainability, transparency, and reliability compared to a single-prompt implementation.

---

## Architecture & Design Decisions

The pipeline consists of five major stages:

### 1. Security Validation Layer

A rule-based validation layer detects prompt injection attempts and requests for sensitive information before they reach the LLM.

### 2. Data Loading & Cleaning

The MLS dataset is loaded and cleaned using Pandas. This stage handles:

* Missing values
* Invalid property records
* Inconsistent formatting
* Data normalization

### 3. Requirement Extraction

**Model:** `llama-3.1-8b-instant`

The extraction model converts unstructured buyer messages into a structured schema containing:

* Budget
* Bedrooms/Bathrooms
* Preferred locations
* Property type
* Desired amenities
* Timeline
* Special requirements

### 4. Property Matching Engine

A deterministic weighted scoring algorithm ranks properties based on:

| Factor               | Weight |
| -------------------- | ------ |
| Location Match       | 30%    |
| Budget Fit           | 25%    |
| Property Size        | 20%    |
| Amenities & Features | 25%    |

Keeping matching logic outside the LLM ensures reproducibility and avoids reasoning inconsistencies.

### 5. Lead Brief Generation

**Model:** `llama-3.3-70b-versatile`

The reasoning model receives:

* Extracted buyer requirements
* Top-ranked properties
* Matching insights

It then generates a structured Lead Brief suitable for realtor review.

---

## Tech Stack

### Core Technologies

* Python 3.9+
* Jupyter Notebook

### LLM Provider

* Groq API

### Models

* `llama-3.1-8b-instant` (Requirement Extraction)
* `llama-3.3-70b-versatile` (Lead Brief Generation)

### Libraries

* Pandas
* NumPy
* Python Dotenv

---

## Repository Structure

```text
Agent-Mira-Buyer-Lead-Intake-Solution/
│
├── README.md
├── requirements.txt
├── .gitignore
├── submission_export.json
│
├── data/
│   ├── sample_buyer_inquiries.json
│   └── miami_mls_listings.csv
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── security.py
│   ├── extractor.py
│   ├── matcher.py
│   ├── generator.py
│   └── agent.py
│
├── notebooks/
│   └── main_pipeline.ipynb
│
└── output/
    └── lead_briefs/
        ├── LEAD-2026-001_brief.md
        ├── LEAD-2026-002_brief.md
        ├── LEAD-2026-003_brief.md
        ├── LEAD-2026-004_brief.md
        ├── LEAD-2026-005_brief.md
        ├── LEAD-2026-006_brief.md
        ├── LEAD-2026-007_brief.md
        ├── LEAD-2026-008_brief.md
        ├── LEAD-2026-009_brief.md
        ├── LEAD-2026-010_brief.md
        ├── LEAD-2026-011_brief.md
        ├── LEAD-2026-012_brief.md
        ├── ALL_LEAD_BRIEFS.md
        └── WRITTEN_EXPLANATION.md
```

---

## Setup & Execution

### Prerequisites

* Python 3.9+
* Groq API Key

### Installation

```bash
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

The application automatically loads the key using environment variables. API keys should never be hardcoded in source files.

### Running the Project

Launch Jupyter Notebook:

```bash
jupyter notebook notebooks/main_pipeline.ipynb
```

Open `main_pipeline.ipynb` and run all cells.

---

## Deliverables

As requested in the AgentMira case study, this repository contains:

### 1. Source Code

Located in:

* `src/`
* `notebooks/main_pipeline.ipynb`

### 2. Generated Lead Briefs

Located in:

```text
output/lead_briefs/
```

Includes:

* 12 individual lead briefs
* Combined Lead Brief document

### 3. Written Explanation

Located at:

```text
output/lead_briefs/WRITTEN_EXPLANATION.md
```

---

## Engineering Highlights

### Prompt Injection Protection

The system detects and blocks attempts to extract owner information or manipulate agent behavior.

### Unrealistic Requirement Detection

Buyer requests that are unlikely to be satisfied within the specified budget are flagged for realtor review.

### Deterministic Matching

Property ranking is performed using transparent weighted scoring rather than opaque LLM reasoning.

### Modular Design

Each stage of the pipeline is isolated into its own component, improving maintainability, testing, and extensibility.

---

## Notes

This project was developed as part of the **AgentMira AI Product Engineer Case Study** for the **DTU Campus Recruitment Process (2025-26)**.

The implementation prioritizes:

* Reliability
* Explainability
* Security
* Cost-efficient LLM usage
* Production-oriented software design

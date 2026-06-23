# Buyer Lead Intake Agent

### AgentMira Engineering Case Study | DTU Campus Recruitment 2025-26

## Overview

This project implements a Buyer Lead Intake Agent that converts unstructured buyer inquiries into structured Lead Briefs for real estate agents.

The system combines rule-based validation, LLM-powered requirement extraction, deterministic property matching, and AI-generated briefing to create actionable realtor-facing outputs.

---

## Tech Stack

* Python 3.9+
* Groq API
* Pandas
* NumPy
* Python-Dotenv
* Jupyter Notebook

### Models Used

* llama-3.1-8b-instant (Requirement Extraction)
* llama-3.3-70b-versatile (Lead Brief Generation)

---

## Repository Structure

```text
buyer_lead_intake_agent/
│
├── README.md
├── requirements.txt
├── .gitignore
├── submission_export.json
│
├── data/
│   ├── AgentMira_Case_Study_Buyer_Lead_Intake_Agent.docx
│   ├── miami_mls_listings.csv
│   └── sample_buyer_inquiries.json
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
        ├── ALL_LEAD_BRIEFS.md
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
        └── WRITTEN_EXPLANATION.md
```

---

## Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Run

```bash
jupyter notebook notebooks/main_pipeline.ipynb
```

Open the notebook and run all cells.

---

## Deliverables

### Source Code

Located in:

* src/
* notebooks/main_pipeline.ipynb

### Generated Lead Briefs

Located in:

* output/lead_briefs/

Includes:

* 12 individual lead briefs
* Combined lead brief output

### Written Explanation

Located in:

* output/lead_briefs/WRITTEN_EXPLANATION.md

---

## Engineering Highlights

* Prompt injection detection for malicious lead instructions
* Structured requirement extraction using LLMs
* Deterministic property scoring and ranking
* Automated lead brief generation
* Modular pipeline design
* Realtor-focused output generation

---

## Notes

This repository was developed as part of the AgentMira AI Product Engineer Case Study for the DTU Campus Recruitment Process (2025-26).

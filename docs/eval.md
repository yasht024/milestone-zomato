# Evaluation Metrics and Strategy: AI-Powered Restaurant Recommendation System

This document defines the evaluation criteria and metrics used to measure the success, performance, and quality of the recommendation system, based on the `architecture.md` and `implementation-plan.md`.

## 1. Data Ingestion & Pre-filtering Metrics
These metrics evaluate how well the data pipeline and database queries perform before the LLM is even involved.

| Metric | Description | Target / Success Criteria |
| :--- | :--- | :--- |
| **Data Completeness** | The percentage of the Hugging Face dataset successfully cleaned and ingested into the local database without critical missing fields. | > 95% retention of the original dataset after cleaning. |
| **Retrieval Accuracy (Recall)** | When a user applies hard filters (e.g., "Delhi", "Italian", "Cost < 1000"), does the database return all valid matching candidates? | 100% (SQL/NoSQL deterministic filtering must not miss valid entries). |
| **Pre-filtering Payload Size** | The number of restaurant records sent to the LLM per query. | 10 to 30 restaurants. (Too few = poor variety; too many = context window overflow and high cost). |

## 2. LLM Recommendation Quality
Evaluating the subjective output of the Large Language Model. This can be done via automated evaluation (LLM-as-a-judge) or human-in-the-loop testing.

| Metric | Description | Target / Success Criteria |
| :--- | :--- | :--- |
| **Instruction Adherence** | Does the LLM return the requested JSON format without markdown wrapping or plain text? | > 99% success rate. (Use structured output APIs if possible). |
| **Context Faithfulness (Zero Hallucination)** | Does the LLM *only* recommend restaurants that were provided in its pre-filtered context list? | 100% strict adherence. The LLM must not invent restaurant names or alter real ratings. |
| **Reasoning Quality** | How well does the LLM justify its recommendation based on the user's *soft preferences* (e.g., matching "quiet atmosphere" with a relevant context clue)? | Measured via human review (Scale 1-5). Target: Average score of 4.0+. |
| **Ranking Relevance** | Does the LLM put the absolute best match at the top of the returned array? | Evaluated manually via sample edge-case queries. |

## 3. System Performance & Latency
Evaluating the user experience and backend efficiency.

| Metric | Description | Target / Success Criteria |
| :--- | :--- | :--- |
| **Database Query Latency** | The time it takes for the backend to execute the pre-filtering SQL query. | < 100 milliseconds. |
| **LLM Inference Latency** | The time taken for the external LLM API to process the prompt and return the JSON payload. | < 5 seconds (Optimized via smaller prompts and faster models like GPT-4o-mini or Gemini Flash). |
| **Total E2E Response Time** | Time from when the user clicks "Search" on the frontend to when the UI renders the result cards. | < 6 seconds total. |

## 4. Robustness and Error Handling
Evaluating how the system handles the edge cases defined in `edge-case.md`.

| Metric | Description | Target / Success Criteria |
| :--- | :--- | :--- |
| **Graceful Fallback Rate** | When the LLM API fails or times out, does the system successfully fall back to returning basic pre-filtered results without crashing? | 100% fallback success. The UI must never show a raw 500 error page. |
| **Input Sanitization Success** | Ability of the backend to detect and sanitize malicious inputs in the "Soft Preferences" text area. | Prevent all SQL injection and basic Prompt Injection attempts. |

## 5. Evaluation Workflow (How we test)

1. **Unit Testing (Phase 2):** Pytest scripts to verify the Data Ingestion logic and FastAPI pre-filtering queries.
2. **Automated LLM Evaluation (Phase 3):** Run a script containing 50 diverse test prompts (e.g., highly restrictive, vague, conflicting preferences). Use a secondary, stronger LLM (like GPT-4) to grade the primary model's JSON outputs on a scale of 1-5 for relevance and hallucination.
3. **Manual E2E Testing (Phase 5):** Deploy locally and have human testers interact with the UI, explicitly looking for visual bugs, long loading times, and poor recommendations.

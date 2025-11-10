# SHL Assessment Recommender — Short Approach (2 pages)

**Goal**: Given a job description or short query, recommend the most relevant SHL assessment pages (individual tests), returning name + URL.

**Data sources**:
- SHL product catalog (scraped HTML pages) — focus on individual tests, not pre-packaged job solutions.
- Provided Gen AI dataset (labelled/unlabelled CSVs inside the uploaded Excel).

**Architecture (short)**:
- Scraper (`fetch_products.py`) → produce `shl_catalog.csv`.
- Preprocess: combine title + description + tags into one `search_text` field.
- Encode: `SentenceTransformer('all-mpnet-base-v2')` to get dense vectors.
- Index: FAISS (IndexFlatIP) with L2-normalized vectors for cosine-like similarity.
- API: `recommender_api.py` to return top-K recommendations (retrieval + optional rerank).
- UI: Streamlit (`ui_app.py`) to paste a JD, view recommendations, and download CSV.

**Why these choices**:
- `all-mpnet-base-v2` gives good semantic performance offline without API costs.
- FAISS is fast and easy to use for nearest-neighbor retrieval.
- FastAPI + Streamlit provides a reproducible demo that reviewers can run locally.

**Evaluation**:
- Use the labelled set to compute recall@K (e.g., Recall@10).
- `generate_submission_csv.py` produces the required submission CSV with rows: Query, Assessment_url.

**Quick improvements (future)**:
- Add an LLM-based reranker (OpenAI/Gemini) to refine top-50 candidates.
- Use supervised reranker on available labelled pairs.
- Add keyword boosting for exact skill matches (hybrid retrieval).

**How to present**:
- Keep your 2-page doc direct: what you built, why the components, quick results, and next steps.
- Be ready to explain how you'd improve recall@10 and handle balance between technical (K) and behavioural (P) tests.

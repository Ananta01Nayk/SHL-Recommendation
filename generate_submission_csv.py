# generate_submission_csv.py
# This script calls the /recommend API for each query in the
# unlabeled test dataset and generates a submission CSV.
# The output includes all SHL-required fields:
# assessment_name, assessment_url, score, test_type,
# category, duration, and level.

import pandas as pd
import requests
import os
import time

api_url = os.environ.get("RECOMMENDER_API", "http://localhost:8000/recommend")
input = "unlabeled_test.csv" 
out_put = "submission_predictions.csv"


def generate_submission(input_csv=input, out_csv=out_put):
    """Generate SHL submission CSV by querying the local API."""
    if not os.path.exists(input_csv):
        raise FileNotFoundError(f"Expected {input_csv}")

    df = pd.read_csv(input_csv)
    all_rows = []

    print(f" Generating submission from {len(df)} queries...")

    for i, row in df.iterrows():
        qr_text = row.get("query") or row.get("Query") or ""
        if not qr_text.strip():
            continue

        try:
            resp = requests.post(api_url, json={"query_text": qr_text, "top_k": 10}, timeout=40)
            if resp.status_code != 200:
                print(f" API returned {resp.status_code} for query: {qr_text[:40]}...")
                continue

            resp_json = resp.json()
            recs = resp_json.get("recommendations", [])

            for rec in recs:
                all_rows.append({
                    "Query": qr_text,
                    "Assessment Name": rec.get("assessment_name", ""),
                    "Assessment URL": rec.get("assessment_url", ""),
                    "Score": rec.get("score", ""),
                    "Test Type": rec.get("test_type", ""),
                    "Category": rec.get("category", ""),
                    "Duration": rec.get("duration", ""),
                    "Level": rec.get("level", "")
                })

            print(f"[{i+1}/{len(df)}] ✅ Processed: {qr_text[:60]}...")

            time.sleep(0.5)

        except Exception as e:
            print(f"Error processing query '{qr_text[:40]}': {e}")

    # Save output
    out_df = pd.DataFrame(all_rows)
    out_df.to_csv(out_csv, index=False)
    print(f"\n Saved {len(out_df)} recommendations to {out_csv}\n")


if __name__ == "__main__":
    generate_submission()

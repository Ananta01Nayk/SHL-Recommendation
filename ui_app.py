# ui_app.py

import streamlit as st
import pandas as pd
import requests

# App setup
st.set_page_config(page_title="SHL Assessment Recommender",page_icon="my_logo.png" ,layout="wide")
st.title("SHL Assessment Recommendation System")
st.markdown("Get top SHL assessments based on your job description or skills input.")

API_URL = "http://localhost:8000/recommend"

# User Input
query = st.text_area("Enter job description or required skills:", height=150)
top_k = st.slider("How many recommendations would you like?", 1, 10, 5)

if st.button("Get suggestions"):
    if not query.strip():
        st.warning("Please enter a valid input.")
    else:
        try:
            # Send request to backend API
            resp = requests.post(API_URL, json={"query_text": query, "top_k": top_k}, timeout=60)
            if resp.status_code != 200:
                st.error(f"API Error {resp.status_code}: {resp.text}")
            else:
                data = resp.json()

                # Handle SHL JSON response
                if isinstance(data, dict) and "recommendations" in data:
                    recs = data["recommendations"]
                elif isinstance(data, list):
                    recs = data
                else:
                    recs = []

                if not recs:
                    st.warning("No recommendations found for this query.")
                else:
                    # Build DataFrame for display
                    df = pd.DataFrame([
                        {
                            "Assessment Name": r.get("assessment_name", ""),
                            "URL": r.get("assessment_url", ""),
                            "Score": r.get("score", ""),
                            "Test Type": r.get("test_type", ""),
                            "Category": r.get("category", ""),
                            "Duration": r.get("duration", ""),
                            "Level": r.get("level", "")
                        }
                        for r in recs
                    ])

                    # Display results
                    st.success(f"✅ Found {len(df)} recommended assessments!")
                    st.dataframe(df, use_container_width=True)

                    # Optional: Download results as CSV
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="📥 Download recommendations as CSV",
                        data=csv,
                        file_name="submission_predictions.csv",
                        mime="text/csv"
                    )

        except Exception as e:
            st.error(f"Call failed: {e}")

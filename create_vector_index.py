# create_vector_index.py
# Build embeddings for catalog and save a FAISS index + metadata.

import pandas as pd
import numpy as np
import pickle, os
from sentence_transformers import SentenceTransformer
import faiss

catalog_csv_data = 'shl_catalog.csv'
emb_file_data = 'vectors.npy'
meta_data = 'product_records.pkl'
index_ = 'faiss_products.index'
model_name = 'all-mpnet-base-v2'

def prepare_texts(df):
    # combine useful fields into a single search text
    df['search_text'] = (df.get('title','').fillna('') + '. ' + df.get('description','').fillna('') + '. ' + df.get('test_type','').fillna('')).str.strip()
    return df

def create_vector_index(csv_path=catalog_csv_data):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Expected catalog CSV at {csv_path}")
    df = pd.read_csv(csv_path)
    df = prepare_texts(df)
    texts = df['search_text'].fillna('').tolist()
    print(f"Encoding {len(texts)} catalog items using {model_name}...")
    encoder_data = SentenceTransformer(model_name)
    vectors_data = encoder_data.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    # normalize for cosine-like similarity with inner-product index
    faiss.normalize_L2(vectors_data)
    np.save(emb_file_data, vectors_data)
    with open(meta_data, 'wb') as f:
        pickle.dump(df.to_dict(orient='records'), f)
    dim_vec = vectors_data.shape[1]
    index = faiss.IndexFlatIP(dim_vec)
    index.add(vectors_data)
    faiss.write_index(index, index_)
    print("FAISS index saved.")

if __name__ == '__main__':
    create_vector_index()

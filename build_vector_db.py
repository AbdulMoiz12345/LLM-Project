import pandas as pd
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer


def build_faiss_index(csv_path, index_path, metadata_path):
    print("🔄 Loading preprocessed data...")

    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"❌ Error: {csv_path} not found. Run preprocessing first.")
        return

    # Remove empty content
    df = df.dropna(subset=['content'])
    documents = df['content'].tolist()

    print(f"✅ Loaded {len(documents)} document chunks.")

    # 🔥 Improved Embedding Model
    print("🧠 Loading embedding model (BAAI/bge-small-en-v1.5)...")
    model = SentenceTransformer('BAAI/bge-small-en-v1.5')

    # Generate embeddings
    print("⚙️ Generating embeddings...")
    embeddings = model.encode(
        documents,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    # Convert to float32 (FAISS requirement)
    embeddings = np.array(embeddings).astype('float32')

    # 🔥 Normalize embeddings for cosine similarity
    print("📏 Normalizing embeddings (cosine similarity)...")
    faiss.normalize_L2(embeddings)

    # Create FAISS index
    dimension = embeddings.shape[1]
    print(f"📦 Creating FAISS index (dimension={dimension})...")

    # 🔥 Using IndexFlatIP for cosine similarity
    index = faiss.IndexFlatIP(dimension)

    # Add embeddings
    index.add(embeddings)

    print(f"✅ Total vectors indexed: {index.ntotal}")

    # Save FAISS index
    faiss.write_index(index, index_path)
    print(f"💾 FAISS index saved to: {index_path}")

    # Save metadata
    metadata = df.to_dict('records')

    with open(metadata_path, 'wb') as f:
        pickle.dump(metadata, f)

    print(f"💾 Metadata saved to: {metadata_path}")


if __name__ == "__main__":
    CSV_FILE = "data/processed_bank_knowledge.csv"
    FAISS_INDEX_FILE = "data/bank_knowledge.index"
    METADATA_FILE = "data/bank_metadata.pkl"

    build_faiss_index(CSV_FILE, FAISS_INDEX_FILE, METADATA_FILE)
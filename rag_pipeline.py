import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Local LLM imports
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Guardrails
from evaluation_and_guardrails import safe_response


class RAGPipeline:
    def __init__(self, faiss_index_path, metadata_path):
        print("🔄 Loading FAISS index and metadata...")

        # Load FAISS index
        self.index = faiss.read_index(faiss_index_path)

        # Load metadata
        with open(metadata_path, 'rb') as f:
            self.metadata = pickle.load(f)

        print("🧠 Loading embedding model...")
        self.embedder = SentenceTransformer('BAAI/bge-small-en-v1.5')

        print("🤖 Loading local LLM...")

        # Local model (NO API)
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            load_in_4bit=True  # reduce memory usage
        )

        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer
        )

        print("✅ RAG Pipeline ready.")

    # -------------------------------
    # Retrieval
    # -------------------------------
    def retrieve(self, query, top_k=5):
        query_vec = self.embedder.encode([query]).astype('float32')

        faiss.normalize_L2(query_vec)

        distances, indices = self.index.search(query_vec, top_k)

        retrieved_docs = []

        for i in indices[0]:
            if i < len(self.metadata):
                retrieved_docs.append(self.metadata[i]['content'])

        return retrieved_docs

    # -------------------------------
    # Prompt Construction
    # -------------------------------
    def build_prompt(self, query, context):
        context_text = "\n\n".join(context)

        prompt = f"""
You are a helpful and precise banking assistant.

STRICT RULES:
- Only use the given context.
- If the answer is not in context, say: "I do not have enough information to answer that."
- Do not hallucinate.
- Keep responses concise and professional.

CONTEXT:
{context_text}

QUESTION:
{query}

ANSWER:
"""

        return prompt

    # -------------------------------
    # Local LLM Response
    # -------------------------------
    def generate_response(self, prompt):
        result = self.generator(
            prompt,
            max_new_tokens=300,
            do_sample=True,
            temperature=0.3,
            top_p=0.9,
            repetition_penalty=1.1
        )

        return result[0]["generated_text"]

    # -------------------------------
    # Add Sources
    # -------------------------------
    def add_sources(self, response, context):
        sources_text = "\n\n📌 Sources:\n"

        for i, doc in enumerate(context):
            preview = doc[:150].replace("\n", " ")
            sources_text += f"{i+1}. {preview}...\n"

        return response + sources_text

    # -------------------------------
    # Main Query Function
    # -------------------------------
    def query(self, user_query):
        print(f"🔍 Query received: {user_query}")

        # Retrieve context
        context = self.retrieve(user_query, top_k=5)

        if not context:
            return "I do not have enough information to answer that."

        # Build prompt
        prompt = self.build_prompt(user_query, context)

        # Generate response
        raw_response = self.generate_response(prompt)

        # Apply guardrails
        safe_answer = safe_response(raw_response, context, user_query)

        # Add sources
        final_answer = self.add_sources(safe_answer, context)

        return final_answer


# -------------------------------
# Manual test (optional)
# -------------------------------
if __name__ == "__main__":
    rag = RAGPipeline(
        faiss_index_path="data/bank_knowledge.index",
        metadata_path="data/bank_metadata.pkl"
    )

    while True:
        query = input("\nAsk a question: ")

        if query.lower() in ["exit", "quit"]:
            break

        response = rag.query(query)

        print("\n💬 Answer:\n", response)
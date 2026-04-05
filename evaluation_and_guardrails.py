import numpy as np


# -------------------------------
# Retrieval Evaluation (Basic)
# -------------------------------
def evaluate_retrieval(retrieved_docs, ground_truth_keywords):
    """
    Measures how relevant retrieved documents are
    based on keyword overlap (proxy for precision)
    """

    if not retrieved_docs:
        return 0.0

    matches = 0

    for doc in retrieved_docs:
        doc_lower = doc.lower()

        for keyword in ground_truth_keywords:
            if keyword.lower() in doc_lower:
                matches += 1
                break

    precision = matches / len(retrieved_docs)

    return round(precision, 3)


# -------------------------------
# Context Relevance Check
# -------------------------------
def is_context_relevant(context, query):
    """
    Checks whether retrieved context is relevant to the query
    """

    query_terms = set(query.lower().split())

    score = 0

    for doc in context:
        doc_terms = set(doc.lower().split())
        overlap = query_terms.intersection(doc_terms)

        if len(overlap) > 0:
            score += 1

    relevance = score / len(context) if context else 0

    return relevance > 0.3  # threshold


# -------------------------------
# Hallucination Guardrail
# -------------------------------
def detect_hallucination(response, context):
    """
    Simple heuristic to detect hallucination
    """

    context_text = " ".join(context).lower()
    response_text = response.lower()

    # If response contains words not in context (rough check)
    response_words = set(response_text.split())

    context_words = set(context_text.split())

    unknown_words = response_words - context_words

    # If too many unknown words → suspicious
    if len(unknown_words) > 20:
        return True

    return False


# -------------------------------
# Answer Quality Score
# -------------------------------
def answer_quality_score(response):
    """
    Basic scoring based on response characteristics
    """

    score = 0

    # Length check
    if 50 < len(response) < 500:
        score += 1

    # Structured response
    if ":" in response:
        score += 1

    # No uncertainty words
    if "i think" not in response.lower():
        score += 1

    return score / 3  # normalized


# -------------------------------
# Safe Response Wrapper
# -------------------------------
def safe_response(response, context, query):
    """
    Final safety + quality enforcement layer
    """

    # Check hallucination
    if detect_hallucination(response, context):
        return "I do not have enough information to answer that."

    # Check relevance
    if not is_context_relevant(context, query):
        return "I do not have enough information to answer that."

    return response


# -------------------------------
# Example Usage
# -------------------------------
if __name__ == "__main__":

    sample_context = [
        "A savings account allows users to store money safely.",
        "Interest is earned on savings accounts monthly."
    ]

    query = "What is a savings account?"

    retrieved_precision = evaluate_retrieval(
        sample_context,
        ["savings", "interest"]
    )

    print("📊 Retrieval Precision:", retrieved_precision)

    print("🔍 Context Relevant:", is_context_relevant(sample_context, query))

    print("🛡️ Hallucination Detected:",
          detect_hallucination("Savings accounts are used for storing money.", sample_context))
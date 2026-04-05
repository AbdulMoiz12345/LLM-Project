import pandas as pd
import os
import re

def clean_text(text):
    """Standardizes text for LLM ingestion."""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def anonymize_data(text):
    """Redacts sensitive PII."""
    # Redact Email
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', '[REDACTED_EMAIL]', text)
    # Redact Phone Numbers
    text = re.sub(r'(\+92|0)?3\d{2}[-\s]?\d{7}', '[REDACTED_PHONE]', text)
    # Redact CNIC
    text = re.sub(r'\b\d{5}-\d{7}-\d{1}\b', '[REDACTED_CNIC]', text)
    return text

def process_excel_document(input_file, output_file):
    """Reads an Excel file, iterates through sheets, cleans, and anonymizes with structural context tracking."""
    print(f"Loading Excel file from: {input_file}")
    
    try:
        sheets = pd.read_excel(input_file, sheet_name=None)
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return

    processed_documents = []

    for sheet_name, df in sheets.items():
        print(f"Processing sheet: {sheet_name}")
        current_section = sheet_name 
        
        for index, row in df.iterrows():
            # Extract non-empty cells, IGNORE '#REF!' errors
            row_vals = [str(val).strip() for val in row.values if pd.notna(val) and str(val).strip() != "" and str(val).strip() != "#REF!"]
            
            if not row_vals:
                continue
            
            # Filter out the rogue "Main" keyword so our header detection works
            header_check_vals = [v for v in row_vals if v.lower() != 'main']
            
            row_text = " | ".join(row_vals)
            cleaned = clean_text(row_text)
            
            if not cleaned:
                continue
            
            # --- SMART HEADER DETECTION ---
            is_header = False
            text_lower = cleaned.lower()
            question_starters = ('what', 'how', 'who', 'is', 'can', 'does', 'do', 'are', 'will')
            
            if cleaned.endswith("?") or cleaned.endswith(":"):
                is_header = True
            elif text_lower.startswith(question_starters):
                is_header = True
            # Check length of header_check_vals (ignores 'Main')
            elif len(header_check_vals) == 1 and len(cleaned.split()) <= 12:
                is_header = True
                
            if is_header:
                # If the header had "Main" in it, strip it out for a cleaner title
                current_section = clean_text(header_check_vals[0]) if header_check_vals else cleaned
                final_chunk = f"Product: {sheet_name} | Section: {current_section}"
            else:
                final_chunk = f"Product: {sheet_name} | Section: {current_section} | Detail: {cleaned}"
            
            anonymized = anonymize_data(final_chunk)
            
            processed_documents.append({
                "source_sheet": sheet_name,
                "content": anonymized
            })

    final_df = pd.DataFrame(processed_documents)
    final_df.to_csv(output_file, index=False)
    print(f"\nSuccess! Processed {len(processed_documents)} context-aware chunks into {output_file}")

if __name__ == "__main__":
    # --- UPDATE THIS PATH to where your actual .xlsx file is located ---
    INPUT_EXCEL_FILE = "data/raw/NUST Bank-Product-Knowledge.xlsx" 
    CLEAN_DATA_FILE = "data/processed_bank_knowledge.csv"
    
    os.makedirs(os.path.dirname(CLEAN_DATA_FILE), exist_ok=True)
    process_excel_document(INPUT_EXCEL_FILE, CLEAN_DATA_FILE)

import pandas as pd
from rapidfuzz import process
import streamlit as st

# Upload and load Excel file
def load_data_from_excel(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)
        data = df.to_dict(orient='records')  # Convert to list of dicts
        return data
    except Exception as e:
        st.error(f"❌ Error loading Excel file: {e}")
        return []

# Language detection
def detect_language(text):
    arabic_chars = any('\u0600' <= c <= '\u06FF' for c in text)
    return 'ar' if arabic_chars else 'en'

# Search item function with suggestions
def search_item(query, database):
    lang = detect_language(query)

    if lang == 'ar':
        names = [item["nameAr"] for item in database]
    else:
        names = [item["name"] for item in database]

    match = process.extractOne(query, names)

    if match:
        matched_name, score, _ = match
        index = names.index(matched_name)
        return database[index], matched_name, score

    return None, None, 0

# Main Streamlit App
def main():
    st.title("🧠 AI Price Finder (Arabic & English)")

    uploaded_file = st.file_uploader("📂 Upload your Excel file (items.xlsx)", type=["xlsx"])

    if uploaded_file is not None:
        database = load_data_from_excel(uploaded_file)

        if database:
            st.success("✅ File uploaded and data loaded successfully!")

            # Show database preview
            st.subheader("📋 Preview of your items:")
            st.dataframe(pd.DataFrame(database))

            # Input field for item description
            query = st.text_input("🔎 Enter item description (Arabic or English):")

            if query:
                if len(query.strip()) < 3:
                    st.warning("⚠️ Please enter a more descriptive query (at least 3 characters).")
                else:
                    result, suggestion, score = search_item(query, database)

                    if result:
                        if score > 85:
                            st.success(f"✅ Item Found: {result['name']} / {result['nameAr']}")
                            st.info(f"💰 Price: {result['price']} EGP")
                        elif score > 70:
                            st.warning(f"❓ Did you mean: {suggestion}? (Confidence: {int(score)}%)")
                            st.info(f"💰 Price: {result['price']} EGP")
                        else:
                            st.error("❌ No matching item found. Please try again!")
        else:
            st.error("❌ No data found in the file! Make sure your Excel is correct.")

if __name__ == "__main__":
    main()

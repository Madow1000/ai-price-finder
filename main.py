from rapidfuzz import process

# In-memory database
database = [
    { "id": 1, "name": "Laptop", "nameAr": "لابتوب", "price": 1200 },
    { "id": 2, "name": "Smartphone", "nameAr": "هاتف ذكي", "price": 800 },
    { "id": 3, "name": "Headphones", "nameAr": "سماعات", "price": 150 },
    { "id": 4, "name": "Keyboard", "nameAr": "لوحة مفاتيح", "price": 100 },
    { "id": 5, "name": "Mouse", "nameAr": "فأرة", "price": 50 },
]

# Language detection
def detect_language(text):
    arabic_chars = any('\u0600' <= c <= '\u06FF' for c in text)
    return 'ar' if arabic_chars else 'en'

# Search item function with suggestions
def search_item(query):
    lang = detect_language(query)

    if lang == 'ar':
        names = [item["nameAr"] for item in database]
    else:
        names = [item["name"] for item in database]

    # Use rapidfuzz to find best match
    match = process.extractOne(query, names)

    if match:
        matched_name, score, _ = match
        index = names.index(matched_name)
        return database[index], matched_name, score

    return None, None, 0

# Main program
def main():
    print("🔎 Welcome to the AI Price Finder!")

    while True:
        query = input("\n📝 Enter item description (Arabic or English), or type 'exit' to quit: ")

        if query.lower() == 'exit':
            print("👋 Goodbye!")
            break

        # Check for short input
        if len(query.strip()) < 3:
            print("⚠️ Please enter a more descriptive query (at least 3 characters).")
            continue

        result, suggestion, score = search_item(query)

        if result:
            if score > 85:
                print(f"\n✅ Item Found: {result['name']} / {result['nameAr']}")
                print(f"💰 Price: {result['price']} EGP")
            elif score > 70:  # increased threshold to reduce false positives
                print(f"\n❓ Did you mean: {suggestion}? (Confidence: {int(score)}%)")
                print(f"💰 Price: {result['price']} EGP")
            else:
                print("\n❌ No matching item found. Please try again!")
        else:
            print("\n❌ No matching item found at all. Please try again!")

if __name__ == "__main__":
    main()

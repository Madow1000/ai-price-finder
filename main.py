from rapidfuzz import process

# قاعدة البيانات البسيطة
database = [
    { "id": 1, "name": "Laptop", "nameAr": "لابتوب", "price": 1200 },
    { "id": 2, "name": "Smartphone", "nameAr": "هاتف ذكي", "price": 800 },
    { "id": 3, "name": "Headphones", "nameAr": "سماعات", "price": 150 },
    { "id": 4, "name": "Keyboard", "nameAr": "لوحة مفاتيح", "price": 100 },
    { "id": 5, "name": "Mouse", "nameAr": "فأرة", "price": 50 },
]

# دالة لاكتشاف اللغة
def detect_language(text):
    arabic_chars = any('\u0600' <= c <= '\u06FF' for c in text)
    return 'ar' if arabic_chars else 'en'

# دالة البحث عن المنتج
def search_item(query):
    lang = detect_language(query)

    if lang == 'ar':
        names_ar = [item["nameAr"] for item in database]
        matches = process.extractOne(query, names_ar)
        if matches and matches[1] > 60:
            index = names_ar.index(matches[0])
            return database[index]
    else:
        names_en = [item["name"] for item in database]
        matches = process.extractOne(query, names_en)
        if matches and matches[1] > 60:
            index = names_en.index(matches[0])
            return database[index]

    return None

# البرنامج الرئيسي
def main():
    print("🔎 مرحبًا بك في AI Price Finder!")
    while True:
        query = input("\n📝 اكتب اسم المنتج (بالعربي أو الإنجليزي)، أو اكتب 'exit' للخروج: ")
        if query.lower() == 'exit':
            print("👋 مع السلامة!")
            break

        result = search_item(query)
        if result:
            print(f"\n✅ تم العثور على المنتج: {result['name']} / {result['nameAr']}")
            print(f"💰 السعر: {result['price']} EGP")
        else:
            print("\n❌ لم يتم العثور على المنتج، حاول مرة أخرى!")

if __name__ == "__main__":
    main()



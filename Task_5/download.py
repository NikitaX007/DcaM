import json
from pymongo import MongoClient
from tokens import ATLAS_USER, ATLAS_PASS, ATLAS_HOST
DB = 'vacancies'
COLLECTION = 'hhru'

uri = f"mongodb+srv://{ATLAS_USER}:{ATLAS_PASS}@cluster0.{ATLAS_HOST}.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client[DB]
collection = db[COLLECTION]
documents = list(collection.find())
print(f"Выгружено с БД {DB} коллекции {COLLECTION} {len(documents)} документов")
with open(COLLECTION + '.json', 'w', encoding='utf-8') as f:
    json.dump(documents, f, ensure_ascii=False, indent=4)

print(f"Сохранено в файл {COLLECTION}.json")
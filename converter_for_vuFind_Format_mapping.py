import json

# Funktion zur Umwandlung eines einzelnen JSON-Datensatzes in das vufind-Schema
def map_to_vufind_format(data):
    vufind_data = {
        "id": str(data["id"]),
        "lccn": "",
        "ctrlnum": [data["doi"]],
        "collection": ["Catalog"],
        "institution": ["MyInstitution"],
        "building": ["Library A"],
        "fullrecord": "",
        "record_format": "marc",
        "spelling": [],
        "language": str(data["language"]),
        "format": ["Journal"],
        "author_corporate": [],
        "author_facet": [],
        "author_corporate_role": [],
        "title": data["title"],
        "topic": data["tags"],
        "spellingShingle": [],
        "title_short": data["title"],
        "title_full": data["title"],
        "title_fullStr": data["title"],
        "title_full_unstemmed": data["title"],
        "title_auth": data["title"],
        "title_sort": data["title"].lower(),
        "publisher": [data["publisher"]],
        "publishDate": [],
        "physical": [],
        "dateSpan": [],
        "issn": [],
        "callnumber-first": "",
        "callnumber-subject": "",
        "callnumber-label": "",
        "callnumber-sort": "",
        "callnumber-raw": [],
        "callnumber-search": [],
       # "topic": data["subjects"],
        "topic_facet": [],
        "genre_facet": [],
        "illustrated": "",
        "oclc_num": [],
        "work_keys_str_mv": [],
        "marc_error": "",
        "_version_": ""
    }
    return vufind_data

# Funktion zum Einlesen der JSON-Daten aus einer Datei
def load_json_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Funktion zum Speichern von JSON-Daten in eine Datei
def save_json_to_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

# Pfad zur JSON-Datei mit den Ausgangsdaten
json_file_path = 'meinecorejsondatendieneuesten.json'

# Laden der JSON-Daten aus der Datei
json_data = load_json_from_file(json_file_path)

# Verarbeitung der Ausgangs-JSON-Daten
vufind_results = []
for entry in json_data:
    vufind_data = map_to_vufind_format(entry)
    vufind_results.append(vufind_data)

# Pfad zur Ausgabedatei für die umgewandelten Daten
output_file_path = 'umgewandelte_vufind_daten.json'

# Speichern der umgewandelten Daten in eine JSON-Datei
save_json_to_file(vufind_results, output_file_path)

print(f"Die umgewandelten Daten wurden in die Datei '{output_file_path}' gespeichert.")

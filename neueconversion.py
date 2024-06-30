import pymarc
from pymarc import Record, Field, Subfield
import json

def convert_to_marc(json_data):
    record = Record()

    # 001 Field (id)
    if 'id' in json_data:
        record.add_field(Field(tag='001', data=json_data['id']))

    # 035a Field (ctrlnum)
    if 'ctrlnum' in json_data:
        for value in json_data['ctrlnum']:
            record.add_field(Field(tag='035', indicators=[' ', ' '], subfields=[Subfield('a', value)]))

    # 010 Field (collection)
    if 'collection' in json_data:
        for value in json_data['collection']:
            record.add_field(Field(tag='010', indicators=[' ', ' '], subfields=[Subfield('a', value)]))

    if 'issn' in json_data:
        record.add_field(Field(tag='022', indicators=[' ', ' '], subfields=[Subfield('a', json_data['issn'])]))

    # 691 Field (institution)
    if 'institution' in json_data:
        for value in json_data['institution']:
            record.add_field(Field(tag='691', indicators=[' ', ' '], subfields=[Subfield('a', value)]))

    # 692 Field (building)
    if 'building' in json_data:
        for value in json_data['building']:
            record.add_field(Field(tag='692', indicators=[' ', ' '], subfields=[Subfield('a', value)]))

    # 600 Field (topic)
    if 'topic' in json_data:
        for value in json_data['topic']:
            record.add_field(Field(tag='600', indicators=[' ', ' '], subfields=[Subfield('a', value)]))


    if 'language' in json_data:
        record.add_field(Field(tag='008', data=json_data['language']))
        
        if len(json_data['language'])>35: 
            record.add_field(Field(tag='041', indicators=[' ', ' '], subfields=[Subfield('a', json_data['language'][35:38] )]))



    # 655 Field (genre)
   # if 'topic' in json_data:
    #    for value in json_data['topic']:
     #       record.add_field(Field(tag='655', indicators=[' ', ' '], subfields=[Subfield('a', value)]))

    # 245 Field (title)
    if 'title' in json_data:
        record.add_field(Field(tag='245', indicators=['1', '0'], subfields=[Subfield('a', json_data['title'])]))

    # 260 Field (publisher)
    if 'publisher' in json_data:
        for value in json_data['publisher']:
            record.add_field(Field(tag='260', indicators=[' ', ' '], subfields=[Subfield('c', value)]))

    # Convert record to .mrc format
    return record.as_marc()

# Lese JSON-Daten aus einer Datei ein
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data_list = json.load(file)
    return json_data_list

# Beispiel: Pfade zu JSON-Dateien
json_file_paths = [
    'umgewandelte_vufind_daten.json',
]

# Byte-String für alle konvertierten MARC-Daten
mrc_data_all = b''

# Für jede JSON-Datei die Konvertierung durchführen
for file_path in json_file_paths:
    json_data_list = read_json_file(file_path)
    for json_data in json_data_list:
        marc_data = convert_to_marc(json_data)
        mrc_data_all += marc_data

# Schreibe alle MARC-Daten in eine einzige .mrc-Datei
output_file = 'output_all.mrc'
with open(output_file, 'wb') as f:
    f.write(mrc_data_all)

print(f"Conversion successful. All MARC data written to {output_file}.")

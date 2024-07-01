from pymarc import Record, Field, Subfield
import json
import os

def convert_to_marc(json_data):

    languageList = read_json_file(os.path.join(src_dir, "ReverseLanguageMap.json"))
    record = Record()
    

    # 001 Field (id)
    if 'id' in json_data:
        record.add_field(Field(tag='001', data=str(json_data['id'])))

    # 655 Field (documentType)
    if 'documentType' in json_data:
        record.add_field(Field(tag='655', indicators=[' ', ' '], subfields=[Subfield('a', json_data['documentType'])]))

    # 856 $u Field (downloadUrl)
    if 'downloadUrl' in json_data:
        record.add_field(Field(tag='856', indicators=[' ', ' '], subfields=[Subfield('u', json_data['downloadUrl'])]))

    # 041 $a and 008/35-37 (language)
    if 'language' in json_data:

        if json_data['language']['name'] in languageList:
            newCode = languageList[json_data['language']['name']]
            #Set the 008 field position for language code
            #field_008 = ' ' * 35 + lang_code + ' ' * (40 - 35 - len(lang_code))
            field_008 = 'x' * 35 + newCode + 'x'*2
            record.add_field(Field(tag='008', data=field_008))
        
        if len(json_data['language'])>35: 
            record.add_field(Field(tag='041', indicators=[' ', ' '], subfields=[Subfield('a', json_data['language'][35:38] )]))

    # 005 Field (updatedDate)
    if 'updatedDate' in json_data:
        record.add_field(Field(tag='005', data=json_data['updatedDate'].replace('-', '').replace(':', '').replace('T', '') + '.0'))

    # 245 $a Field (title)
    if 'title' in json_data:
        record.add_field(Field(tag='245', indicators=['1', '0'], subfields=[Subfield('a', json_data['title'])]))

    # 500 Field (acceptedDate)
    if 'acceptedDate' in json_data:
        record.add_field(Field(tag='500', indicators=[' ', ' '], subfields=[Subfield('a', f"Accepted Date: {json_data['acceptedDate']}")]))

    # 035 $a Field (oaiIds and other identifiers)
    if 'oaiIds' in json_data:
        for oai_id in json_data['oaiIds']:
            record.add_field(Field(tag='035', indicators=[' ', ' '], subfields=[Subfield('a', oai_id)]))
    if 'identifiers' in json_data:
        for identifier in json_data['identifiers']:
            if identifier['type'] in ['CORE_ID', 'OAI_ID']:
                record.add_field(Field(tag='035', indicators=[' ', ' '], subfields=[Subfield('a', identifier['identifier'])]))
            elif identifier['type'] == 'DOI':
                record.add_field(Field(tag='024', indicators=['7', ' '], subfields=[Subfield('a', identifier['identifier']), Subfield('2', 'doi')]))

    # 710 $a Field (dataProviders)
    if 'dataProviders' in json_data:
        for provider in json_data['dataProviders']:
            record.add_field(Field(tag='710', indicators=['2', ' '], subfields=[Subfield('a', provider['name'])]))

    # 500 Field (depositedDate)
    if 'depositedDate' in json_data:
        record.add_field(Field(tag='500', indicators=[' ', ' '], subfields=[Subfield('a', f"Deposited Date: {json_data['depositedDate']}")]))

    # 856 $u Field (links)
    if 'links' in json_data:
        for link in json_data['links']:
            record.add_field(Field(tag='856', indicators=[' ', ' '], subfields=[Subfield('u', link['url'])]))

    # 650 $a Field (fieldOfStudy)
    if 'fieldOfStudy' in json_data:
        record.add_field(Field(tag='650', indicators=[' ', ' '], subfields=[Subfield('a', json_data['fieldOfStudy'])]))

    # 260 $c Field (yearPublished)
    if 'yearPublished' in json_data:
        record.add_field(Field(tag='260', indicators=[' ', ' '], subfields=[Subfield('c', str(json_data['yearPublished']))]))

    # 773 $t Field (journals)
    if 'journals' in json_data:
        for journal in json_data['journals']:
            if 'title' in journal:
                record.add_field(Field(tag='773', indicators=[' ', ' '], subfields=[Subfield('t', journal['title'])]))

    # 260 $b Field (publisher)
    if 'publisher' in json_data:
        record.add_field(Field(tag='260', indicators=[' ', ' '], subfields=[Subfield('b', json_data['publisher'])]))

    # 700 $a Field (contributors)
    if 'contributors' in json_data:
        for contributor in json_data['contributors']:
            record.add_field(Field(tag='700', indicators=[' ', ' '], subfields=[Subfield('a', contributor)]))

    # 100/700 $a Field (authors)
    if 'authors' in json_data:
        for i, author in enumerate(json_data['authors']):
            if i == 0:
                record.add_field(Field(tag='100', indicators=['1', ' '], subfields=[Subfield('a', author['name'])]))
            else:
                record.add_field(Field(tag='700', indicators=['1', ' '], subfields=[Subfield('a', author['name'])]))

    return record.as_marc()

# Read JSON data from a file
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data_list = json.load(file)
    return json_data_list


src_dir = os.path.dirname(__file__)
json_file_paths = [
    os.path.join(src_dir, 'DDjson.json')
]

# Byte-String for all converted MARC data
mrc_data_all = b''

# Perform conversion for each JSON file
for file_path in json_file_paths:
    json_data_list = read_json_file(file_path)
    for json_data in json_data_list:
        marc_data = convert_to_marc(json_data)
        mrc_data_all += marc_data

# Write all MARC data to a single .mrc file
#IMPORTANT: CHANGE THIS TO YOUR VUFIND INSTALL FOLDER
#output_file = "C:/vufind/ddmarc.marc"
output_file = os.path.join(src_dir,"TestAuto.marc")
with open(output_file, 'wb') as f:
    f.write(mrc_data_all)

print(f"Conversion successful. All MARC data written to {output_file}.")

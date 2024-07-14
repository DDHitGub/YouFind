from pymarc import Record, Field, Subfield
import json
import os
import subprocess
import time

import requests

url = "https://gw.cortical.io/nlp/keywords"



def convert_to_marc(json_data):
    src_dir = os.path.dirname(__file__)
    languageList = read_json_file(os.path.join(src_dir, "ReverseLanguageMap.json"))
    record = Record()
    # 001 Field (id)
    if 'id' in json_data:
        record.add_field(Field(tag='001', data=str(json_data['id'])))

    # 655 Field (documentType)
    #if 'documentType' in json_data:
     #   record.add_field(Field(tag='655', indicators=[' ', ' '], subfields=[Subfield('a', json_data['documentType'])]))

    # 856 $u Field (downloadUrl)
    if 'downloadUrl' in json_data:
        record.add_field(Field(tag='856', indicators=[' ', ' '], subfields=[Subfield('u', json_data['downloadUrl'])]))

    # 041 $a and 008/35-37 (language)
    if 'language' in json_data:

        if json_data['language']['name'] in languageList:
            newCode = languageList[json_data['language']['name']]
            # Set the 008 field position for language code
            # field_008 = ' ' * 35 + lang_code + ' ' * (40 - 35 - len(lang_code))
            field_008 = 'x' * 35 + newCode + 'x' * 2
            record.add_field(Field(tag='008', data=field_008))

        if len(json_data['language']) > 35:
            record.add_field(
                Field(tag='041', indicators=[' ', ' '], subfields=[Subfield('a', json_data['language'][35:38])]))

    # 005 Field (updatedDate)
    if 'updatedDate' in json_data:
        record.add_field(
            Field(tag='005', data=json_data['updatedDate'].replace('-', '').replace(':', '').replace('T', '') + '.0'))

    # 245 $a Field (title)
    if 'title' in json_data:
        record.add_field(Field(tag='245', indicators=['1', '0'], subfields=[Subfield('a', json_data['title'])]))

    # 500 Field (acceptedDate)
    if 'acceptedDate' in json_data:
        record.add_field(Field(tag='500', indicators=[' ', ' '],
                               subfields=[Subfield('a', f"Accepted Date: {json_data['acceptedDate']}")]))

    # 035 $a Field (oaiIds and other identifiers)
    if 'oaiIds' in json_data:
        for oai_id in json_data['oaiIds']:
            record.add_field(Field(tag='035', indicators=[' ', ' '], subfields=[Subfield('a', oai_id)]))
    if 'identifiers' in json_data:
        for identifier in json_data['identifiers']:
            if identifier['type'] in ['CORE_ID', 'OAI_ID']:
                record.add_field(
                    Field(tag='035', indicators=[' ', ' '], subfields=[Subfield('a', identifier['identifier'])]))
            elif identifier['type'] == 'DOI':
                record.add_field(Field(tag='024', indicators=['7', ' '],
                                       subfields=[Subfield('a', identifier['identifier']), Subfield('2', 'doi')]))

    # 710 $a Field (dataProviders)
    if 'dataProviders' in json_data:
        for provider in json_data['dataProviders']:
            record.add_field(Field(tag='710', indicators=['2', ' '], subfields=[Subfield('a', provider['name'])]))

    # 500 Field (depositedDate)
    if 'depositedDate' in json_data:
        record.add_field(Field(tag='500', indicators=[' ', ' '],
                               subfields=[Subfield('a', f"Deposited Date: {json_data['depositedDate']}")]))

    # 856 $u Field (links)
    if 'links' in json_data:
        for link in json_data['links']:
            record.add_field(Field(tag='856', indicators=[' ', ' '], subfields=[Subfield('u', link['url'])]))
    


    # 650 $a Field (fieldOfStudy)
    #if 'fieldOfStudy' in json_data:
     #   record.add_field(Field(tag='650', indicators=[' ', ' '], subfields=[Subfield('a', json_data['fieldOfStudy'])]))

    # 260 $c Field (yearPublished)
    if 'yearPublished' in json_data:
        record.add_field(
            Field(tag='260', indicators=[' ', ' '], subfields=[Subfield('c', str(json_data['yearPublished']))]))

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

    # 022a/440x/490x/730x/773x/776x/780x/785x Field (ISSN)
    if 'journals' in json_data:
        for j in json_data['journals']:
            if 'identifiers' in j:
                issn = j['identifiers'][0]
                record.add_field(Field(tag='022', indicators=['1', ' '], subfields=[Subfield('a', issn)]))
                # record.add_field(Field(tag='440', indicators=['1', ' '], subfields=[Subfield('x', issn)]))
                # record.add_field(Field(tag='490', indicators=['1', ' '], subfields=[Subfield('x', issn)]))
                # record.add_field(Field(tag='730', indicators=['1', ' '], subfields=[Subfield('x', issn)]))
                # record.add_field(Field(tag='773', indicators=['1', ' '], subfields=[Subfield('x', issn)]))
                # record.add_field(Field(tag='776', indicators=['1', ' '], subfields=[Subfield('x', issn)]))
                # record.add_field(Field(tag='780', indicators=['1', ' '], subfields=[Subfield('x', issn)]))
                # record.add_field(Field(tag='785', indicators=['1', ' '], subfields=[Subfield('x', issn)]))

    # 773t Field (Journal title in which the article is)
    if 'journals' in json_data:
        record.add_field(Field(tag='773', indicators=['1', ' '], subfields=[Subfield('i', 'In')]))
        if 'title' in json_data['journals'] and json_data['journals']['title'] != 'null':
            record.add_field(
                Field(tag='773', indicators=['1', ' '], subfields=[Subfield('t', json_data['journals']['title'])]))

    # Temp - use 502 for document type
    # TODO: Remember to change marc_local format: 502a or it does not work
    if "documentType" in json_data:
        type = json_data["documentType"]
        record.add_field(Field(tag='502', indicators=['1', ' '], subfields=[
            Subfield('a', "Article" if type == "research" else "Thesis" if type == "thesis" else "Unknown")]))
    
    # 505 $a Field (abstract in contents)
    if 'abstract' in json_data:
        record.add_field(Field(tag='505', indicators=['1', '0'], subfields=[Subfield('a', json_data['abstract'])]))
        
        payload = {
            "text": json_data['abstract'],
            "language": "en",
            "limit": 20
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "eyJvcmciOiI2NTNiOTllNjEzOGM3YzAwMDE2MDM5NTEiLCJpZCI6ImJiZmU5MTUxMzc3MDRmMjNiZDcxODBlMGQxOTljZDA3IiwiaCI6Im11cm11cjEyOCJ9"
        }

        response = requests.post(url, json=payload, headers=headers)
        print(response.json())
        res = response.json()
        time.sleep(0.5)

        if 'keywords' in res:
            print(res['keywords'])
            for word in res['keywords']:
                record.add_field(Field(tag='650', indicators=[' ', ' '], subfields=[Subfield('a', word["word"])]))
                print(word)
        
        print("\n")

  

    return record.as_marc()


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data_list = json.load(file)
    return json_data_list


# Read JSON data from a file


def converter(filepath: str, jsonObj):
    # json_file_paths = [
    #     os.path.join(src_dir, 'TestOutput.json')
    # ]

    # Byte-String for all converted MARC data
    marc_data_all = b''
    # print(jsonObj)
    # Perform conversion for each JSON file
    # for file_path in json_file_paths:
    # json_data_list = read_json_file(filepath)
    count = 0
    for json_data in jsonObj:
        marc_data = convert_to_marc(json_data)
        marc_data_all += marc_data
        count += 1
    print("converting to MARC...")
    time.sleep(.5)
    # marc_data += convert_to_marc(read_json_file("TestOutput.json"))
    # Write all MARC data to a single .mrc file
    # IMPORTANT: CHANGE THIS TO YOUR VUFIND INSTALL FOLDER
    # output_file =
    # output_file = os.path.join(src_dir,"TestAuto.marc")
    # with open(output_file, 'wb') as f:
    with open(os.path.join("", filepath), 'wb') as f:
        # f.write(mrc_data_all)
        f.write(marc_data_all)

    print(f"Converted succesfully {count} entries. All MARC data written to {filepath}.\n")
    time.sleep(.5)
    print("starting solr...\n")
    subprocess.run([os.path.join("C:/vufind-9.1.1", "solr.bat"), "start"])
    print("Importing files into vufind...\n")
    time.sleep(.5)
    subprocess.run([os.path.join("C:/vufind-9.1.1", "import-marc.bat"), filepath], cwd=r"C:/vufind-9.1.1")

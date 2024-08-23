# Converter from JSON to MARC (.mrc)

## Quick Explanation
- This script, named "Auto-Converter," retrieves raw data from [Core](https://core.ac.uk) - a large collection of open access research papers.
- The scientific papers retrieved are in the field of computer science and limited to 100 entries (you can adjust this by changing "100" in the command below to another value).
- The MARC21 (.mrc) format is a standard format for library cataloging and is widely used by libraries.
- This script is written in Python and can be executed with the following command:
  ```shell
  fieldsOfStudy:%22computer+science%22 100 [Your/VuFind/Directory/Output.mrc]
- First the script gets the data from Core and saves it
- Then it converts JSON data to MARC21 format and saves it as a .mrc file.
- After conversion, the script automatically starts Solr and imports the new records from Core, so you don't have to load them manually into VuFind/Solr.


## Detailed Documentation

- In this Folder named "AutoConverter" you will have following file structure:

```
                        GetCoreData.py
                        ReverseLanguageMap.json
AutoConverter  ------>  convert.py
                        startcommand.md
                        __pycache__ (not relevant in this context)
``` 
- The Python scripts have different responsibilities and are interdependent. The following list explains the important tasks of each file:

    - GetCoreData.py: 
        - This script retrieves computer science data from Core and saves it.
        - It uses the Core API search link, setting the query and limit as specified in the command above. The search link from Core is: https://api.core.ac.uk/v3/search/works/?q={query}&limit={limit}.
        - You can also adjust the fields/tags to retrieve, e.g., you can delete the "abstract" field if you don't want it in your VuFind.
    - convert.py:
        - This script converts JSON data to MARC21 format. It takes the JSON data from GetCoreData.py as input and performs the conversion.
        - It's important to set the fields for the MARC files correctly to ensure they are recognized by VuFind. The MARC documentation is very helpful for this. We use the pymarc library to facilitate the conversion in Python.
        - If the JSON to MARC conversion is successful, the script automatically starts Solr and imports the converted files into VuFind.
    - ReverseLanguageMap.json:
        - This is a language directory that reverses the language map used in VuFind (to use this, you need to run the GetCoreData.py script).
    - startcommand.md: 
        - This is a Markdown file containing the start command mentioned above.






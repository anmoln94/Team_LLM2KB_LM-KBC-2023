import json
import wikipediaapi
import requests
import re


with open(r'train.jsonl', 'r') as json_file: #run for val.jsonl also
    json_list = list(json_file)

wiki_wiki = wikipediaapi.Wikipedia(
        user_agent='MyProjectName (merlin@example.com)',
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI
    )

test_with_text = []

def extract_country_name(url):
    pattern = r"https:\/\/([a-z-]+)\.wikipedia\.org\/wiki\/.+"
    match = re.match(pattern, url)
    if match:
        return match.group(1)
    else:
        return 'en'

i=1
for json_str in json_list:
    result = json.loads(json_str)
    
    print(i)
    i+=1
    print(result['SubjectEntityID'])
    item = result['SubjectEntityID']
    url = f"https://wikidata.org/w/rest.php/wikibase/v0/entities/items/{item}"
    data = requests.get(url).json()
    try:
        entity_to_fetch = data['sitelinks']['enwiki']['title']
        wiki_text = wiki_wiki.page(entity_to_fetch).text
        result['subject_text'] = wiki_text
    except:
        print('Failed to resolve english')
        try:
            if len(data['sitelinks'])==0:
                print("still empty")
                result['subject_text'] = []
            else:
                for key in data['sitelinks']:
                    url = data['sitelinks'][key]['url']
                    language = extract_country_name(url)
                    wiki_wiki = wikipediaapi.Wikipedia(
                    user_agent='MyProjectName (merlin@example.com)',
                        language=language,
                        extract_format=wikipediaapi.ExtractFormat.WIKI
                    )
                    entity_to_fetch = data['sitelinks'][key]['title']
                    wiki_text = wiki_wiki.page(entity_to_fetch).text
                    result['subject_text'] = wiki_text
                    result['subject_text_lang'] = language
                    print(language)
                    break
        except:
            print("still empty")
            result['subject_text'] = []
        wiki_wiki = wikipediaapi.Wikipedia(
        user_agent='MyProjectName (merlin@example.com)',
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI)

    test_with_text.append(result)

with open('traindata_with_context.jsonl','w') as outfile: #change to valdata_with_context.jsonl when running for val.jsonl
    for entry in test_with_text:
        json.dump(entry,outfile)
        outfile.write('\n')
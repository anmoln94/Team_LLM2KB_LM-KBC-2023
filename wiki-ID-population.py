import pandas as pd
from ast import literal_eval
import requests
import wikipedia

df = pd.read_csv("beluga_stage2.csv") #change to llama_stage2.csv if running for llama2. This is the file generated from stage 2.

df["answer_idxs"] = None
df["OrigAnsWikiTitle"] = df["OrigAnsWikiTitle"].apply(literal_eval)
df["WikiTitles"] = df["WikiTitles"].apply(literal_eval)
df["ObjectEntities"] = df["ObjectEntities"].apply(literal_eval)
df["WikiTitleIndexes"] = df["WikiTitleIndexes"].apply(literal_eval)
df["fnl_ids"] = [[]] * len(df)

missed_counter = 0

for index, row in df.iterrows():
    answer_idxs = []
    if row["Relation"] in ["PersonHasNumberOfChildren", "SeriesHasNumberOfEpisodes"]:
        if row["ObjectEntities"][0].isdigit():
            df.at[index, "answer_idxs"] = row["ObjectEntities"]
            df.at[index, "fnl_ids"] = row["ObjectEntities"]
        else:
            df.at[index, "answer_idxs"] = [str(len(row["ObjectEntities"]))]
            df.at[index, "fnl_ids"] = [str(len(row["ObjectEntities"]))]
        continue
    answers, options = row["OrigAnsWikiTitle"], row["WikiTitles"]

    for a, ops in zip(answers, options):
        if a and a[0].lower() in [o.lower() for o in ops]:
            idx = [o.lower() for o in ops].index(a[0].lower())
        else:
            idx = -1
            if a:
                missed_counter += 1
                print(index)
                print("-")
        answer_idxs.append(idx)

    df.at[index, "answer_idxs"] = answer_idxs


def wiki_search(search_term):
    try:
        if type(search_term) is list:
            search_term = search_term[0]

        result = wikipedia.search(search_term, results=1)[0]

        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&titles={result}&format=json"
        data = requests.get(url).json()
        for key in data['query']['pages']:
            obj_id = data['query']['pages'][key]['pageprops']['wikibase_item']
        return obj_id
    except:
        return ""

for index, row in df.iterrows():
    if df.at[index, "fnl_ids"]:
        continue
    fnl_ids = []
    
    for i, (ids, idx) in enumerate(zip(row["WikiTitleIndexes"], row["answer_idxs"])):
        #if answer option predicted, but not found in wiki options
        if not row["fnl_ids"] and row["OrigAnsWikiTitle"][i] and idx == -1:
            result = wiki_search(row["OrigAnsWikiTitle"][i])
            if result:
                fnl_ids.append(result)


        if not row["fnl_ids"] and idx >= 0:
            fnl_ids.append(ids[idx])
    df.at[index, "fnl_ids"] = fnl_ids

df.to_csv("detailed_output_file.csv") #output file which has resolved wiki data IDs

fnl_df = df[["SubjectEntity", "SubjectEntityID", "Relation", "ObjectEntities", "fnl_ids"]]
new_column_names = {'fnl_ids': 'ObjectEntitiesID'}
fnl_df = fnl_df.rename(columns=new_column_names)

output_path = "predictions.jsonl" #final predictions file that is used for submission

with open(output_path, "w") as f:
    f.write(fnl_df.to_json(orient='records', lines=True))
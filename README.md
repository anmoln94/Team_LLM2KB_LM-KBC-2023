# Team_LLM2KB_LM-KBC-2023
Submission of Team LLM2KB for LM-KBC 2023 challenge (Track 2)
Authors: Anmol Nayak and Hari Prasad Timmapathini (Equal Contribution)
Trained LoRA Models should be downloaded from: https://drive.google.com/drive/folders/1RIt2k19JNdkjg4NFBz9DOVTNGH18JRze?usp=sharing
Base Models have to be downloaded from Huggingface.

How to run LLM2KB:

For training:
Step 1: With train.jsonl, val.jsonl, test.jsonl (given by the competition), execute fetch_wiki_data.py
Step 2: Use Step 1 generated files and execute fetch_wikidata_options.ipynb
Step 3: Using Step 2 generated files, execute generate_dpr_top_contexts.ipynb
Step 4: Using Step 3 generated files, execute beluga_train_notebook.ipynb or llama2_train_notebook.ipynb

For inference:
Step 1: Execute llama_inference_stage1.ipynb or beluga_inference_stage_1.ipynb with top_with_top3_context.jsonl
Step 2: Using Step 1 generated files, execute fetch_wikidata_options.ipynb
Step 3: Using Step 2 generated files, execute llama_inference_stage2.ipynb or beluga_inference_stage_2.ipynb
Step 4: Using Step 3 generated files, execute wiki-ID-population.py

Note:
We have already pre-computed these files and put them in this repository so that you can use them in case you want to directly run training/inference.

# collect_social_media_data

Scripts to search and download information from Facebook and Twitter, using their corresponding APIs.

### Common configuration
The file `pilot_countries_metadata.xlsx` contains some information used to define the search target:
* country	(e.g. "Netherlands")
* target name in English (e.g. "The Netherlands Red Cross")
* target name in the local language (e.g. "Rode Kruis")
* Red Cross name in the local language (e.g. "Rode Kruis")
* most common local language (e.g. Dutch)
* less common language(s) spoken (e.g. English)
N.B. it is necessary to edit and/or add a new row in this file if new or different countries want to be analysed.

### twitter
The twitter scripts can be found in the corresponding directory.
The algorithm is divided in 3 separate steps:
1. `get_twitter_ids.py`: get twitter ids and user names matching the target names and countries (as defined in `pilot_countries_metadata.xlsx`).
2. `get_twitter_data.py`: get tweets produced in the last week by the ids and user names identified in step #1; download them as json files in the folder `twitter_data`.
3. `transform_analyse_tweets.ipynb`: load tweets saved as json, map them to a dataframe and save it as csv in the folder `twitter_data_processed`.

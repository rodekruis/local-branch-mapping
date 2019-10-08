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

### Twitter
The twitter scripts can be found in the corresponding directory.
The algorithm is divided in 3 separate steps:
1. `get_twitter_ids.py`: get twitter ids and user names matching the target names and countries (as defined in `pilot_countries_metadata.xlsx`)
2. `get_twitter_data.py`:
    1. get tweets produced in the last week by the ids and user names identified in step #1
    2. download tweets as json in directory `twitter_data`
3. `transform_analyse_tweets.ipynb`:
    1. load tweets saved as json
    2. map tweets to a dataframe
    3. save dataframe as csv in directory `twitter_data_processed`

### Facebook
The facebook scripts can be found in the corresponding directory.
The algorithm is divided in 2 separate steps:
1. `get_facebook_data.py`:
    1. get facebook public pages matching the target names and countries (as defined in `pilot_countries_metadata.xlsx`)
    2. download the pages' info all their public posts as json in directory `facebook_data`.
2. `transform_analyse_facebook_pages.ipynb`:
    1. load pages' info saved as json
    2. map pages to a dataframe
    3. inspect dataframe and filter out spurious pages (if any)
    4. save dataframe as csv in the folder `facebook_data_processed`
3. `transform_analyse_facebook_posts.ipynb`:
    1. load pages' posts saved as json
    2. map posts to a dataframe
    4. save dataframe as csv in the folder `facebook_data_processed`

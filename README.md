# local-branch-mapping
Code and documentation for the local branch mapping project, a cooperation of 510 and the International Federation of Red Cross and Red Crescent Societies (IFRC).

### Objectives
The technical goals of the project were to build tools and methodologies to automatise the following operations:
1) Extract locations of local branches of a given Red Cross National Society (NS) from the web.
2) Extract information on those branches (contacts, capacity, activities).
3) Compare and contrast this information with (1) relevant needs of the given country and (2) the [IFRC's strategy 2030](https://future-rcrc.com/).

The tools described belowed were built and tested studying 4 pilot countries:
1. Malawi
2. Guatemala
3. Lebanon
4. Netherlands

### Data Sources
##### Introduction
The data sources investigated during this project were the following:
1. [HDX](https://data.humdata.org/)
2. [UNdata](http://data.un.org/)
3. [World Bank Open Data](https://data.worldbank.org/)
4. [FDRS](http://data.ifrc.org/fdrs/)
5. Specific datasets obtained from the NS
6. Social media: [Facebook](https://www.facebook.com/) and [Twitter](https://twitter.com/)
7. [Google Maps](https://www.google.com/maps)
8. [OpenStreetMap](https://www.openstreetmap.org)
9. [GDELT](https://www.gdeltproject.org/) (database of events, locations and organisation built from newspapers)
10. National and regional online newspapers
11. NS' website(s).
##### Source Selection
After reviewing the above sources, the sources #6, #7, #8, #10 and #11 were selected as most relevant and included in the following analysis.
First observations:
* Social media: contain information on locations and activities of some local branches
  * The fraction of local branches with a dedicated account on social media platforms varies from country to country
  * Facebook shows the most number of local branch pages, while Twitter usually hosts very few accounts
* Google maps: contains locations and some information (contacts, opening hours) of some local branches
* OpenStreetMap: contains locations of some local branches; less populated that Google maps.
* National and regional online newspapers: contain information on some local branch activities; difficult to unambigously associate one activity to one specific local branch, if not explicitely mentioned, but possible to guess by geographical proximity.
* NS' website(s): can contain locations and contact information of local branches, but not for every country: among the pilot countries, only the Netherlands and Guatemala had a dedicated page with such information.

The other sources were discarded for the following reasons:
* Sources #1 to #4 do not contain any information on RC local branches.
* Source #4 contains detailed information on the NS, but little on local branches (only the total number of them).
* Source #5 was concluded to be out-of-scope, as it is impossible to automate the analysis of an arbitrary, possibly unstructured data set.
* Source #9 was found to contain little information on RC local branches, as it is built mostly upon content produced by major international news agencies.

### Data Collection
Data was collected from the aformentioned sources using the corresponding APIs (Application Programming Interfaces). Python scripts were developed to query and download data in an automated fashion; they can be found in the following directories, together with documentation on how to run them:
* collect_social_media_data
* collect_google_maps_data
* collect_openstreetmap_data
* collect_local_news
* collect_addresses_from_web

### Data Analysis
The data analysis consisted in 3 separate tasks:
1. Merge locations from social media, Google Maps, OpenStreetMap and the web to assign a best estimate for the location of each local branch
2. Extract topics from social media content
3. Map social media content and news articles to the IFRC's strategy 2030, according to the dashboard mockup
Code and documentation relative to these three tasks can be found, respectively, in the following directories:
1. merge_locations
2. extract_topics
3. map_to_2030

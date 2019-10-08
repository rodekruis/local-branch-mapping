# -*- coding: utf-8 -*-
import facebook
import urllib3
import requests
import json
import json_lines
import time
import pandas as pd
import numpy as np

APP_TOKEN = "my-app-token"

page_fields = ['id',
               'name',
               'username',
               'about',
               'description',
               'mission',
               'general_info',
               'personal_info',
               'affiliation',
               'bio',
               'birthday',
               'founded',
               'hometown',
               'hours',
               'contact_address',
               'single_line_address',
               'current_location',
               'store_location_descriptor',
               'website',
               'emails',
               'phone',
               'whatsapp_number',
               'category',
               'category_list',
               'company_overview',
               'country_page_likes',
               'is_permanently_closed',
               'engagement',
               'privacy_info_url',
               'fan_count',
               'link']

post_fields = ['id',
               'created_time',
               'from',
               'type',
               'story',
               'story_tags',
               'message',
               'message_tags',
               'link',
               'name',
               'place',
               'coordinates',
               'shares',
               'updated_time',
               'is_popular',
               'permalink_url']

graph = facebook.GraphAPI(access_token=APP_TOKEN, version="3.1")
        
def loadJSONLines(file):
    data = []
    with open(file, 'rb') as f:
        for item in json_lines.reader(f):
            data.append(item)
    return data

def print_error(_error):
    print(
        f"---------Error---------\n"
        f"Known error. Ignore. Nothing you can do.\n"
        f"{_error}\n"
        f"Sleeping for 5 minutes then retrying.\n"
        f"-----------------------"
    )
    time.sleep(300)

def getPagesSearch(query):
    """
         search for pages
    """
    try:
        result = graph.request('pages/search?q={'+query+'}&fields=id,name,verification_status,location,link') 
    except facebook.GraphAPIError as error:
        if '#4' in error.message: # API rate limit reached
            print('GraphAPIError:', error.message)
            print('sleeping for 1 hour')
            time.sleep(3660)
            result = getPagesSearch(query) 
        else:
            print('GraphAPIError:', error.message)
            print('sleeping for 5 minutes')
            time.sleep(300)
            result = getPagesSearch(query) 
    except urllib3.exceptions.ProtocolError as error:
        print_error(_error=error)
        result = getPagesSearch(query) 
    except ConnectionResetError as error:
        print_error(_error=error)
        result = getPagesSearch(query) 
    except ConnectionError as error:
        print_error(_error=error)
        result = getPagesSearch(query) 
    except requests.exceptions.ConnectionError as error:
        print_error(_error=error)
        result = getPagesSearch(query) 
    except Exception as error:
        print(
                f"---------Error---------\n"
                f"WARNING: Unknown error\n"
                f"{error}\n"
                f"Sleeping for 5 minutes then retrying.\n"
                f"-----------------------"
            )
        time.sleep(300)
        result = getPagesSearch(query) 
    return result

def getPagesNext(result):
    """
         get next page
    """
    try:
        result = requests.get(result['paging']['next']).json()
    except facebook.GraphAPIError as error:
        if '#4' in error.message: # API rate limit reached
            print('GraphAPIError:', error.message)
            print('sleeping for 1 hour')
            time.sleep(3660)
            result = getPagesNext(result) 
        else:
            print('GraphAPIError:', error.message)
            print('sleeping for 5 minutes')
            time.sleep(300)
            result = getPagesNext(result) 
    except urllib3.exceptions.ProtocolError as error:
        print_error(_error=error)
        result = getPagesNext(result) 
    except ConnectionResetError as error:
        print_error(_error=error)
        result = getPagesNext(result) 
    except ConnectionError as error:
        print_error(_error=error)
        result = getPagesNext(result) 
    except requests.exceptions.ConnectionError as error:
        print_error(_error=error)
        result = getPagesNext(result) 
    except Exception as error:
        print(
                f"---------Error---------\n"
                f"WARNING: Unknown error\n"
                f"{error}\n"
                f"Sleeping for 5 minutes then retrying.\n"
                f"-----------------------"
            )
        time.sleep(300)
        result = getPagesNext(result) 
    return result

def getPageInfo(pages, fields_list, i):
    """
         get page info
    """
    try:
        result = graph.get_object(pages[i]['id'], fields=fields_list)
        i += 1
    except facebook.GraphAPIError as error:
        if '#4' in error.message: # API rate limit reached
            print('GraphAPIError:', error.message)
            print('sleeping for 1 hour')
            time.sleep(3660)
            result = getPageInfo(pages, fields_list, i)
        else:
            print('GraphAPIError:', error.message)
            
            print('WARNING: possibly a PRIVATE PAGE,\n')
            print('         saving only basic info\n')
            # possibly a private page, save basic info and skip
            result = pages[i]
            i += 1
                       
    except urllib3.exceptions.ProtocolError as error:
        print_error(_error=error)
        result = getPageInfo(pages, fields_list, i)
    except ConnectionResetError as error:
        print_error(_error=error)
        result = getPageInfo(pages, fields_list, i)
    except ConnectionError as error:
        print_error(_error=error)
        result = getPageInfo(pages, fields_list, i)
    except requests.exceptions.ConnectionError as error:
        print_error(_error=error)
        result = getPageInfo(pages, fields_list, i)
    except Exception as error:
        print(
                f"---------Error---------\n"
                f"WARNING: Unknown error\n"
                f"{error}\n"
                f"Sleeping for 5 minutes then retrying.\n"
                f"-----------------------"
            )
        time.sleep(300)
        result = getPageInfo(pages, fields_list, i)
    
    # something went wrong, save basic info
    if not type(result) == dict:
        result = pages[i]
    
    return result, i

def getPagePosts(page_id, fields_list):
    """
         get posts
    """
    try:
        result = graph.get_object(str(page_id)+'/posts',
                                  fields=fields_list,
                                  limit=100)
    except facebook.GraphAPIError as error:
        if '#4' in error.message: # API rate limit reached
            print('GraphAPIError:', error.message)
            print('sleeping for 1 hour')
            time.sleep(3660)
            result = getPagePosts(page_id, fields_list)
        else:
            print('GraphAPIError:', error.message)
            
            print('WARNING: possibly a PRIVATE PAGE,\n')
            print('         saving only basic info\n')
            # possibly a private page, skipping
            result = {}
                       
    except urllib3.exceptions.ProtocolError as error:
        print_error(_error=error)
        result = getPagePosts(page_id, fields_list)
    except ConnectionResetError as error:
        print_error(_error=error)
        result = getPagePosts(page_id, fields_list)
    except ConnectionError as error:
        print_error(_error=error)
        result = getPagePosts(page_id, fields_list)
    except requests.exceptions.ConnectionError as error:
        print_error(_error=error)
        result = getPagePosts(page_id, fields_list)
    except Exception as error:
        print(
                f"---------Error---------\n"
                f"WARNING: Unknown error\n"
                f"{error}\n"
                f"Sleeping for 5 minutes then retrying.\n"
                f"-----------------------"
            )
        time.sleep(300)
        result = getPagePosts(page_id, fields_list)
    
    # something went wrong, return empty dict
    if not type(result) == dict:
        result = {}
    
    return result

def getPostsNext(page_posts):
    """
        get posts from next page
    """
    try:
        result = requests.get(page_posts['paging']['next']).json()
    except facebook.GraphAPIError as error:
        if '#4' in error.message:
            print('GraphAPIError:', error.message)
            print('sleeping for 1 hour')
            time.sleep(3660)
            result = getPostsNext(page_posts)
        else:
            print('GraphAPIError:', error.message)
            print('sleeping for 5 minutes')
            time.sleep(300)
            result = getPostsNext(page_posts)
    except urllib3.exceptions.ProtocolError as error:
        print_error(_error=error)
        result = getPostsNext(page_posts)
    except ConnectionResetError as error:
        print_error(_error=error)
        result = getPostsNext(page_posts)
    except ConnectionError as error:
        print_error(_error=error)
        result = getPostsNext(page_posts)
    except requests.exceptions.ConnectionError as error:
        print_error(_error=error)
        result = getPostsNext(page_posts)
    except Exception as error:
        print(
                f"---------Error---------\n"
                f"WARNING: Unknown error\n"
                f"{error}\n"
                f"Sleeping for 5 minutes then retrying.\n"
                f"-----------------------"
            )
        time.sleep(300)
        result = getPostsNext(page_posts)
    return result 

def getPagesIds(query):
    """
    search query and return ids and names of all pages found
    input: query (string)
    output: objIds (list of dict)
    """
    print('getting pages from query:', query)
    
    result = getPagesSearch(query) 
          
    if 'data' in result.keys():
        objIds = result['data']
    else:
        print('WARNING: query did not yield any result !!!')
        objIds = []
        
    while 'next' in result.get('paging',{}):
        
        result = getPagesNext(result) 
            
        if 'data' in result.keys():
            objIds.extend(result['data'])
        else:
            print('WARNING: one page did not yield any result !!!')
    
    return objIds

def getPagesData(pages, page_fields, post_fields, country):
    """
    search pages and return page info and posts, as specified by *_fields
    input: pages (list of dict), fields (list), country (string)
    output: exit_message
    """
    print('getting information from pages,', len(pages), 'to process')
    
    i = 0
    while i < len(pages):
        
        page_name = pages[i]['name']
        page_id = pages[i]['id']
        
        print('start processing page', i+1, '(', page_name, ')')
        count_posts = 0
        
        page_data, i = getPageInfo(pages, ','.join(page_fields), i)
        
        # save page info
        with open(output_dir+'page_info_'+country+'.jsonl', 'a') as tf:
            json.dump(page_data, tf)
            tf.write('\n')
        
        page_posts = getPagePosts(page_id, ','.join(post_fields))
        
        # if posts present, porcess and store separately
        if 'data' in page_posts.keys():
        
            # process posts ###############################################
            print('start getting posts')
            count_posts += len(page_posts['data'])
            
            # save page posts
            with open(output_dir+'page_posts_'+country+'.jsonl', 'a') as tf:
                json.dump(page_posts, tf)
                tf.write('\n')
            
            # loop to get all posts
            while 'next' in page_posts.get('paging',{}):
                
                page_posts_old = page_posts
                page_posts = getPostsNext(page_posts_old)
                
                if 'data' in page_posts.keys():
                    count_posts += len(page_posts['data'])
                    
                    # save page posts
                    with open(output_dir+'page_posts_'+country+'.jsonl', 'a') as tf:
                        json.dump(page_posts, tf)
                        tf.write('\n')
            ###############################################################
        else:
            print('no posts found !!!!')
                
        print('finished processing page,', str(count_posts), 'posts found')

    exit_message = str(i) + ' page(s) processed'            
    return exit_message

def is_page_relevant(page, country):
    """
        check if page is relevant
    """
    is_relevant = False
    
    if 'name' in page.keys():
        if country[:5] in page['name']:
            is_relevant = True
        
    if 'location' in page.keys():
        if 'country' in page['location'].keys():  
            if page['location']['country'] == country:
                is_relevant = True
                
    return is_relevant

###############################################################################

if __name__ == "__main__":
    
    output_dir = 'facebook_data/'
    
    df = pd.read_excel('../pilot_countries_metadata.xlsx', index_col=0, sep='|')
    df.index = df.country
    
    for country in df.index.values:
        
        print('start country:', country) 
        df_country = df.loc[country]
       
        for type_query in ['name (english)', 'name (local language)']:
            
            query = df_country[type_query]
            
            if query is np.nan:
                query = df_country["name (english)"]
            
            if query is not np.nan:
                
                print('query:', query)
                pages = getPagesIds(query)
                
                # check if page is relevant
                pages = [page for page in pages if is_page_relevant(page, country)]
         
                # save page ids
                for page in pages:
                    with open(output_dir+'page_id_'+country+'.jsonl', 'a') as tf:
                        json.dump(page, tf)
                        tf.write('\n')
                    
		# get page info and posts
                output = getPagesData(pages, page_fields, post_fields, country)
            
                print('country query finished, ', output)


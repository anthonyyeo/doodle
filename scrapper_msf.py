import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from os import path
from sys import stdout

mainURL = "https://www.gov.sg/sgdi/ministries/"

grab_data(mainURL)


def grab_data(url):

    main_req = requests.get(mainURL)

    soup_main = BeautifulSoup(main_req.content)
  
# find all the main links to the various ministries and write the output to a file

        
    with open('test.txt', 'w') as f:
        for link in soup_main.findAll('a',href=re.compile('/sgdi/ministries/')):
    
            thisLink = {
            'url': 'https://www.gov.sg' + link['href']
            
            }
        #print "Found the URL:", thisLink['url']
            f.write("%s\n" % thisLink['url'])
 

# read in the main text file with the url of the various ministries
    mainLinkdf = pd.read_csv('test.txt',header=None)

    #print(mainLinkdf.columns.values.tolist())

#get the value of the first ministry and get the url for the various departments in that ministry
    url1 = mainLinkdf[0].iloc[0]

    r1 = requests.get(url1)

    soup1 = BeautifulSoup(r1.content)


    with open('url1.txt', 'w') as f:
        for link in soup1.findAll('a',href=re.compile('/sgdi/ministries/')):
    
        thisLink = {
        'url': 'https://www.gov.sg' + link['href']
            
        }
        print "Found the URL:", thisLink['url']
        f.write("%s\n" % thisLink['url'])


# get the department details based on the ministry url
    url1min1df = pd.read_csv('url1.txt',header=None)

    url1dept = url1min1df[0].iloc[1]



    r1dept = requests.get(url1dept)

    soupdept1 = BeautifulSoup(r1dept.content)

    names = soupdept1.find_all("div",attrs={"class": "name"})
    ranks = soupdept1.find_all("div",attrs={"class": "rank"})
    agency_title = soupdept1.find_all("div",attrs={"class" : "agency-title"})

    names_df = pd.DataFrame.from_records(names)

    del names_df[0]

    ranks_df = pd.DataFrame.from_records(ranks)

    agency_title_df = pd.DataFrame.from_records(agency_title)

    new_df = pd.concat([names_df, ranks_df,agency_title_df], axis=1, join_axes=[names_df.index])

    new_df = new_df.rename(columns={0:'Rank',1:'Name'})

    #print(new_df)

    new_df.to_csv('/Users/Anthony/Desktop/output.csv')








        

import sys
from typing import Counter
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer
import requests

def getStats(divs):
    found = False
    for div in divs:
        if found:
            break
        try:
            if div["class"][0] == "news_body":
                strong_tags = div.ul.li.findAll("strong")
                new_cases = strong_tags[0].text
                new_deaths = strong_tags[1].text
                found = True
        except KeyError:
            continue
        except:
            print("There is an error!")
            return {"Error" : "Something went wrong"}
    return new_cases, new_deaths

def getDate(divs):
    for div in divs:
        try:
            if div["class"][0] == "news_date":
                date = div.h4.text
                break
        except KeyError:
            continue
        except:
            print("Something wrong!")
            return {"Error" : "Something went wrong"}
    return date

def constructTweet(cases, deaths, date):
    cases = str(cases).split(" ")[0]
    deaths = str(deaths).split(" ")[0]
    tweet = f"Nepal COVID-19 Update for {date}\n"
    tweet += f"Number of positive tests: {cases}\n"
    tweet += f"Number of deaths: {deaths}\n\n"
    tweet += "Source: worldometers and MOHP Nepal"
    return tweet

url = "https://www.worldometers.info/coronavirus/country/nepal/"
html = requests.get(url).text
soup = BeautifulSoup(html, features='html.parser')
divs = soup.findAll("div")

date = " ".join(str(getDate(divs)).split(" ")[:2])
cases, deaths = getStats(divs)
tweet = constructTweet(cases, deaths, date)
# sendTweet(tweet)



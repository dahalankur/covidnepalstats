from os import environ
import requests
import tweepy
from bs4 import BeautifulSoup


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


def getTotals(divs):
    stats = []
    for div in divs:
        try:
            if div["class"][0] == "maincounter-number":
                stats.append(div.span.text)
        except KeyError:
            continue
        except:
            return {"Error" : "Something went wrong"}
    return stats


def constructTweet(date, cases, deaths, t_cases, t_deaths, t_recovered):
    cases = str(cases).split(" ")[0]
    deaths = str(deaths).split(" ")[0]
    tweet = f"Nepal COVID-19 Update for {date}\n"
    tweet += f"Number of positive tests: {cases}\n"
    tweet += f"Number of deaths: {deaths}\n"
    tweet += f"Cumulative stats: {t_cases} total cases, {t_deaths} total deaths, and {t_recovered} recoveries\n"
    tweet += "\nSource: worldometers and MOHP Nepal"
    return tweet


def sendTweet(tweet):
    auth = tweepy.OAuthHandler(consumer_secret=environ["consumer_secret"],
                                consumer_key=environ["consumer_key"])
    auth.set_access_token(key=environ["access_key"], secret=environ["access_secret"])
    twitter_api = tweepy.API(auth, wait_on_rate_limit=True)
    
    try:
        twitter_api.update_status(tweet)
    except tweepy.TweepError as e:
        print(e.reason)


def main():
    url = "https://www.worldometers.info/coronavirus/country/nepal/"
    
    html = requests.get(url).text
    soup = BeautifulSoup(html, features='html.parser')
    divs = soup.findAll("div")

    # get the statistics
    date = " ".join(str(getDate(divs)).split(" ")[:2])
    cases, deaths = getStats(divs)
    totals = getTotals(divs)

    # construct the tweet and send it
    tweet = constructTweet(date, cases, deaths, totals[0], totals[1], totals[2])
    sendTweet(tweet)


if __name__ == "__main__":
    main()



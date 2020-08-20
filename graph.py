import matplotlib.pyplot as plt
import matplotlib.colors as mcolor
import matplotlib.dates as mdates
import numpy as np
import nltk
import requests
import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# VADER is specifically tuned for sentiment analysis of social media

# from difflib import SequenceMatcher
# returns a ration of similarity between two strings


# get sentiment scores on a topic. returns dict of k:v -> python_dates: sentiment scores
# for stories about a topic from a given domain
def get_news_sentiment(topic, domain):

    # returns the data sets from news api from domain
    def get_news_data(news_domain):

        # requests through news api
        news_req = requests.get(f"https://newsapi.org/v2/everything?q={topic}&domains={news_domain}&pageSize=100"
                                f"&apiKey=1e654ecc24814021aff3a1bc8c785f87")

        # the articles from the request in json list
        news_req_data = news_req.json()['articles']

        return news_req_data

    # return a dict of dates and average sentiment scores from news data
    def get_sentiment_dict(domain_data, keyword):
        # vader sentiment analyzer from ntlk
        analyzer = SentimentIntensityAnalyzer()
        # dict of dates and sentiment
        raw_sentiment = {}

        # news_data contains multiple stories
        for story in domain_data:
            total_sentiment_score = 0

            # list of sentences to be given a sentiment score
            sentences = []

            # get all the sentences from description and title
            if story.get('publishedAt') is not None:
                story_date = datetime.datetime.strptime(story.get('publishedAt'), "%Y-%m-%dT%H:%M:%SZ")
            else:
                break

            # add description sentences to sentences
            if story.get('description') is not None:
                # unfiltered sentences
                # sentences = nltk.sent_tokenize(story.get('description'))

                # filter sentences with topic contained only
                description_sentences = nltk.sent_tokenize(story.get('description'))
                sentences = list(filter(lambda element: keyword.lower() in element.lower(), description_sentences))

            # add titles to sentences
            if story.get('title') is not None:
                sentences.append(story.get('title'))

            # get compound sentiment score for every sentence, add to total score
            for sentence in sentences:
                total_sentiment_score += analyzer.polarity_scores(sentence)['compound']

            # average sentiment score of the article title and description combined
            average_sentiment_score = total_sentiment_score / len(sentences)

            # remove values if sentiment is 0
            if average_sentiment_score != 0:
                raw_sentiment[story_date] = average_sentiment_score

        return raw_sentiment

    news_data = get_news_data(domain)
    sentiment_dict = get_sentiment_dict(news_data, topic)

    return sentiment_dict


# create a graph based on the data returned from get_news_sentiment()
def create_graph(data_input):

    # provide the subject, domain name, data dict for plot, plots it on graph
    def plot_on_graph(subject, domain, data, color):

        # get lists, and convert to matplotlib dates from py dates
        dates = mdates.date2num(list(data.keys()))
        sentiment = list(data.values())

        # randomly generate color for data
        # color = np.random.rand(3,)

        # scatter plot of data with label
        plt.plot(dates, sentiment, color=color, marker='o', linestyle='None', ms=3, label=f'{domain} on {subject.title()}, {len(sentiment)} articles')
        # trend line of data
        z = np.polyfit(dates, sentiment, 1)
        p = np.poly1d(z)
        plt.plot(dates, p(dates), color=color, linestyle='-', linewidth=0.8)

    # colors for graph if not randomly generated
    color_list = ['b', 'r', 'g', 'k', 'purple', 'yellow', 'saddlebrown', 'grey', 'orange', 'indigo']

    # for every data set plot on the graph
    for x in range(0, len(data_input)):
        plot_on_graph(data_input[x]['topic'], data_input[x]['domain'], data_input[x]['data'], color_list[x])

    # format date on x axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=20)

    # axis labels
    plt.xlabel("Date")
    plt.ylabel('Sentence Sentiment Score')

    # legend on graph.py, 0 = "best spot", 2 = upper left
    plt.legend(loc=2)

    plt.title(f"News Sentiment")

    # show it / save it
    plt.savefig(f'./static/sentiment_graph.png', bbox_inches='tight')
    #plt.show()


# use get_news_sentiment() and create_graph() to compare sentiment on a topic from two news sources
# take a list of topics and a list of news site domains to search
def compare_news(topics, domains):
    data_sets = []
    # make a call on every domain for every topic and append result to data_sets list
    for topic in topics:
        for domain in domains:
            data_sets.append({'topic': topic, 'domain': domain, 'data': get_news_sentiment(topic, domain)})

    # create a graph with the data
    create_graph(data_sets)


if __name__ == "__main__":
    # api limits articles to up to a month old
    compare_news(['trump', 'biden'], ['cnn.com', 'msnbc.com'])

# put on flask and make some html inputs?


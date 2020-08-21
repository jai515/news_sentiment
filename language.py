import nltk
import requests
import matplotlib.colors as mcolors
import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# VADER is specifically tuned for sentiment analysis of social media

analyzer = SentimentIntensityAnalyzer()

tricky_sentences = [
    "Most automated sentiment analysis tools are shit.",
    "VADER sentiment analysis is the shit.",
    "Sentiment analysis has never been good.",
    "Sentiment analysis with VADER has never been this good.",
    "Warren Beatty has never been so entertaining.",
    "I won't say that the movie is astounding and I wouldn't claim that \
    the movie is too banal either.",
    "I like to hate Michael Bay films, but I couldn't fault this one",
    "It's one thing to watch an Uwe Boll film, but another thing entirely \
    to pay for it",
    "The movie was too good",
    "This movie was actually neither that funny, nor super witty.",
    "This movie doesn't care about cleverness, wit or any other kind of \
    intelligent humor.",
    "Those who find ugly meanings in beautiful things are corrupt without \
    being charming.",
    "There are slow and repetitive parts, BUT it has just enough spice to \
    keep it interesting.",
    "The script is not fantastic, but the acting is decent and the cinematography \
    is EXCELLENT!",
    "Roger Dodger is one of the most compelling variations on this theme.",
    "Roger Dodger is one of the least compelling variations on this theme.",
    "Roger Dodger is at least compelling as a variation on the theme.",
    "they fall in love with the product",
    "but then it breaks",
    "usually around the time the 90 day warranty expires",
    "the twin towers collapsed today",
    "However, Mr. Carter solemnly argues, his client carried out the kidnapping \
    under orders and in the ''least offensive way possible.''"
 ]

paragraph = "This is a paragraph of text! Here is Mr. Smith example. Here - is another sentence. The tokenizer will" \
            "split this, short paragraph into sentences."

para_sentences = nltk.sent_tokenize(paragraph)


# get sentiment scores on a topic. returns dict of k:v -> python_dates: sentiment scores
# for stories about a topic from a given domain
def get_news_sentiment(topic, domain):

    # returns the data sets from news api from domain
    def get_news_data(news_domain):

        # requests through newsapi
        news_req = requests.get(f"https://newsapi.org/v2/everything?q={topic}&domains={news_domain}&pageSize=100&apiKey=1e654ecc24814021aff3a1bc8c785f87")

        # the articles from the request in json list
        news_data = news_req.json()['articles']

        return news_data

    # return a dict of dates and average sentiment scores from news data
    def get_sentiment_dict(domain_data):
        # dict of dates and sentiment
        raw_sentiment = {}

        # news_data contains multiple stories
        for story in domain_data:
            total_sentiment_score = 0
            sentences = []
            # get all the sentences from description and title
            if story.get('description') is not None:
                sentences = nltk.sent_tokenize(story.get('description'))
            if story.get('title') is not None:
                sentences.append(story.get('title'))
            if story.get('publishedAt') is not None:
                story_date = datetime.datetime.strptime(story.get('publishedAt'), "%Y-%m-%dT%H:%M:%SZ")

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
    sentiment_dict = get_sentiment_dict(news_data)

    return sentiment_dict


if __name__ == "__main__":
    for sentence in tricky_sentences:
        print(sentence)
        print(analyzer.polarity_scores(sentence))
    print(para_sentences)


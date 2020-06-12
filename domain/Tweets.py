class Tweet:
    def __init__(self, tweet_id, author_id=None, polarity=None, subjectivity=None, keywords=[], created_timstm=None, ticker=None, tweet_body=""):
        self.tweet_id = tweet_id
        self.author_id = author_id
        self.polarity = polarity
        self.subjectivity = subjectivity
        self.keywords = keywords
        self.created_timstm = created_timstm
        self.ticker = ticker
        self.tweet_body = tweet_body

    def set_keywords(self, keywords):
        self.keywords = keywords

    def set_ticker(self, ticker):
        self.ticker = ticker

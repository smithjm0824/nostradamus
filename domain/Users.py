from .Tweets import Tweet


class User:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.tweet_ids = []
        self.tweets = []
        self.bot_score = None

    def add(self, tweet: Tweet) -> None:
        self.tweets.append(tweet)
        self.tweet_ids.append(tweet.tweet_id)

    def add_list(self, tweets: list) -> None:
        self.tweets = self.tweets + tweets
        for tweet in tweets:
            self.tweet_ids.append(tweet.tweet_id)

    def clear(self, tweet):
        self.tweets = []
        self.tweet_ids = []

    def assign(self, score):
        self.bot_score = score


class Users:
    def __init__(self):
        self.users = {}

    def __len__(self):
        return len(self.get_user_ids())

    def add(self, user: User):
        if self.exists(user.user_id):
            tmp_user = self.users[user.user_id]
            tmp_user.add_list(user.tweets)
            self.users[user.user_id] = tmp_user
        else:
            self.users[user.user_id] = user

    def exists(self, user_id: str) -> bool:
        if user_id in self.users:
            return True
        return False

    def get(self, user_id):
        if self.exists(user_id):
            return self.users[user_id]
        return None

    def clear(self):
        self.users = {}

    def delete(self, user_ids: list) -> None:
        for user_id in user_ids:
            if self.exists(user_id):
                del self.users[user_id]

    def get_user_ids(self) -> list:
        return list(self.users.keys())

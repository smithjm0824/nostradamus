# nostradamus
Evaluating the impact of sentiment analysis / NLP in tweets on micro-trends in US financial markets.

## Getting Started

### Tweepy

#### Access Keys
Nostradamus uses Tweepy for reading from the Twitter Stream API, 
which requires [creating a Twitter app](https://www.developer.twitter.com/apps).  Once created, you'll use the access 
tokens with Tweepy to authenticate with Twitter.

These keys are user-specific, meaning it's important to keep them secure. I'll be using the 
[ConfigParser module](https://docs.python.org/3/library/configparser.html) that is a built-in module of Python.

* Create a file called <i>config.ini</i> in the <b>tweet_net </b>directory.
* Nostradamus expects the following structure in <i>config.ini</i>.
  > [KEYS] <br/>
    api_key = <b>YOUR_CONSUMER_API_KEY</b> <br/>
    api_secret = <b>YOUR_CONSUMER_API_SECRET_KEY</b> <br/><br/>
    [TOKENS] <br/>
    access_token = <b>YOUR_ACCESS_TOKEN</b><br/>
    access_token_secret = <b>YOUR_ACCESS_TOKEN_SECRET</b>

#### Install Tweepy
<code>pip install tweepy</code>


# nostradamus
Evaluating the impact of sentiment analysis / NLP in tweets on micro-trends in US financial markets.

## Getting Started

#### Clone Repository
Clone the Nostradamus repository using <code>git clone https://github.com/smithjm0824/nostradamus.git</code>

#### Install Dependencies
<code>pip install -r requirements.txt</code>


## Configuration
This project relies on three external APIs that each require user-specific API keys. These keys are user-specific, 
meaning it's important to keep them secure. I'll be using the 
[ConfigParser module](https://docs.python.org/3/library/configparser.html) that is a built-in module of Python. 
ConfigParser makes it easy to keep from hard-coding secrets in the application.

* Create a file called <i>config.ini</i> in the root level directory.

<b>Make sure that you do not post your keys publicly, and 
that the <i>config.ini</i> file is added to your <i>.gitignore</i> file so you don't expose the keys to the world. </b>
<br /><br />

* #### Tweepy Access Keys
    Nostradamus uses Tweepy for reading from the Twitter Stream API, 
    which requires [creating a Twitter app](https://www.developer.twitter.com/apps).  Once created, you'll use the access 
    tokens with Tweepy to authenticate with Twitter.
    
    * Nostradamus expects the following structure in <i>config.ini</i>.
      > [KEYS] <br/>
        api_key = <b>YOUR_CONSUMER_API_KEY</b> <br/>
        api_secret = <b>YOUR_CONSUMER_API_SECRET_KEY</b> <br/><br/>
        [TOKENS] <br/>
        access_token = <b>YOUR_ACCESS_TOKEN</b><br/>
        access_token_secret = <b>YOUR_ACCESS_TOKEN_SECRET</b>

* #### Botometer Access Keys
    Botometer is a service that calculates the likelihood that a given Twitter account is a bot. Since we are pulling in 
    tweets to predict stock movement, we want to assign lower weights to tweets created by a bot account, since these tweets
    are possibly manipulative and are not likely to be reflective of actual market sentiment.
    
    To use the service, you'll need to create a [free RapidAPI account and request an API key for the free-tier of 
    the Botometer service](https://rapidapi.com/OSoMe/api/botometer-pro).
    
    * Once you have the API Keys, add them to your <i>config.ini</i> file as follows.
        > [RAPIDAPI] <br/>
          api_key = <b>YOUR_RAPIDAPI_KEY </b> 

* #### Alpaca Access Keys
    Alpaca is a platform for algorithmic trading with an easy-to-use API and Python integration. 
    Alpaca also offers a "paper-trading" functionality, allowing users to test out trading strategies without risking 
    real cash. 
    
    Alpaca's API is free-to-use, but be careful that you pay attention to what you're doing when using it. 
    As with any trading platform, there is risk involved. Don't blindly copy my strategy and assume it works;
    it probably doesn't. Trade at your own risk.
    
    In order to start trading with Alpaca API, [sign up with Alpaca](https://app.alpaca.markets/signup). As of writing
    this, the Paper Trading API is open to everyone, and the live brokerage API is open only to US residents. 
    
    For this application, I'm only using the Paper Trading API.
    
    * After signing up,  add the api credentials to your <i>config.ini</i> file.
        > [ALPACA] <br/>
        api_key = <b>YOUR_ALPACA_API_KEY</b> <br/>
        secret_key = <b>YOUR_ALPACA_SECRET_KEY</b>

###TODO:
* Add documentation on running Redis via Docker
* Add documentation on running the application
* Add documentation on configuring tweet_net for specific keywords
* Add documentation on design strategy
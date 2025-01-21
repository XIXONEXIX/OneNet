import tweepy
import time

# Twitter scraping function
def scrape_twitter_data(api_key, api_secret_key, access_token, access_token_secret, keyword):
    auth = tweepy.OAuth1UserHandler(api_key, api_secret_key, access_token, access_token_secret)
    api = tweepy.API(auth)
    
    tweets = api.search(q=keyword, lang="en", result_type="recent", count=100)
    tweet_data = []
    for tweet in tweets:
        tweet_data.append(tweet.text)
    return tweet_data

# Function to run the scraping pipeline
def run_scraping_pipeline():
    # Define your API credentials
    API_KEY = 'your_api_key'
    API_SECRET_KEY = 'your_api_secret_key'
    ACCESS_TOKEN = 'your_access_token'
    ACCESS_TOKEN_SECRET = 'your_access_token_secret'
    
    # Define the cryptocurrency symbol to search for
    crypto_symbol = "bitcoin"
    
    # Step 1: Scrape Twitter data
    twitter_data = scrape_twitter_data(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, crypto_symbol)
    
    # You can proceed with filtering, processing, or analyzing the data here
    print(f"Scraped {len(twitter_data)} tweets about {crypto_symbol}")
    
    # Step 2: Wait before next iteration
    time.sleep(60)  # Scrape every 60 seconds

if __name__ == "__main__":
    while True:
        run_scraping_pipeline()

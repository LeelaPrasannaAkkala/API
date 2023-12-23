from flask import Flask, render_template
from googleapiclient.discovery import build
import tweepy
from tweepy import TweepyException

app = Flask(__name__)

# Replace these with your actual API keys
YOUTUBE_API_KEY = ""
TWITTER_API_KEY = ""
TWITTER_API_SECRET = ""
TWITTER_ACCESS_TOKEN = ""
TWITTER_ACCESS_TOKEN_SECRET = ""

# Initialize Tweepy with Twitter API credentials
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)

# Initialize the YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video/<video_id>')
def video(video_id):
    # Fetch video details from YouTube API
    response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()
    print("YouTube API Response:", response)
    # Extract data from the API response
    if 'items' in response and response['items']:
        video_data = {
            'title': response['items'][0]['snippet']['title'],
            'description': response['items'][0]['snippet']['description'],
            'video_id': video_id
        }
    else:
        # error handling
        video_data = {'title': 'Video Not Found', 'description': 'The specified video could not be found.'}

    return render_template('video.html', video_data=video_data)

@app.route('/discussion')
def discussion():
    # Fetch a tweet from Twitter API
    hashtag = '#programming'  # Replace with your actual hashtag
    tweet = None

    try:
        search_results = twitter_api.search_tweets(q=hashtag, count=1, lang='en', result_type='recent')
        if search_results:
            tweet = {'username': search_results[0].user.screen_name, 'text': search_results[0].text}
            print(tweet)
    except TweepyException as e:
        print(f"Twitter API Error: {e}")

    return render_template('discussion.html', tweet=tweet)

if __name__ == "__main__":
    app.run(debug=True)

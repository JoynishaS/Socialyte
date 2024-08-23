from requests_oauthlib import OAuth1Session
import requests
import json
import streamlit

consumer_key = streamlit.secrets['TWITTER_CONSUMER_KEY']
consumer_secret = streamlit.secrets['TWITTER_CONSUMER_SECRET']

# Get the access token
def getAccessToken():
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        client_key=consumer_key,
        resource_owner_key=streamlit.query_params.oauth_token,
        verifier=streamlit.query_params.oauth_verifier
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    streamlit.session_state['twitter_access_token'] = oauth_tokens["oauth_token"]
    streamlit.session_state['twitter_access_token_secret'] = oauth_tokens["oauth_token_secret"]

# Be sure to add replace the text of the with the text you wish to Tweet. You can also add parameters to post polls, quote Tweets, Tweet with reply settings, and Tweet to Super Followers in addition to other features.
def postToTwitter():
    getAccessToken()
    imageID = uploadImage()
    streamlit.write(imageID['media_id'])
    payload = {"text": streamlit.session_state['key'],
               "media": {"media_ids": [str(imageID['media_id'])]}
               }
    streamlit.write(payload)
    # Make the request
    oauth = OAuth1Session(
        client_key=consumer_key,
        resource_owner_key=streamlit.session_state['twitter_access_token']
    )

    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )
    streamlit.write(response.status_code)
    streamlit.write(response.text)

#Upload Image to twitter
def uploadImage():
    if streamlit.session_state['uploadMyOwnImage'] == False:
        download_image(streamlit.session_state['image'])
        image = open("image.jpg","rb").read()
    if streamlit.session_state['uploadMyOwnImage'] == True:
        image = open(streamlit.session_state['uploaded_image_url'], "rb").read()

    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=streamlit.session_state['twitter_access_token'] ,
        resource_owner_secret=streamlit.session_state['twitter_access_token_secret'],
    )

    response = oauth.post(
        "https://upload.twitter.com/1.1/media/upload.json",
        files=[('media',image)])

    data = response.json()

    if response.status_code != 201:
        streamlit.write("We experienced an error with the call!")
    return data

#images have to be local for linkedin api so had to add this
def download_image(url):
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to download image!")
        exit()

    filename = "image.jpg"
    with open(filename, 'wb') as file:
        file.write(response.content)

    streamlit.write("Image uploaded successfully!")
from requests_oauthlib import OAuth1Session
import requests
import json
import streamlit

consumer_key = streamlit.secrets['TWITTER_CONSUMER_KEY']
consumer_secret = streamlit.secrets['TWITTER_CONSUMER_SECRET']
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

# Get request token
def requestTwitterToken():
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=https://socialyte.streamlit.app/app&x_auth_access_type=write"

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
        streamlit.session_state['oauth_token'] = fetch_response.get("oauth_token")
        streamlit.session_state['oauth_token_secret'] = fetch_response.get("oauth_token_secret")
        streamlit.write("Fetch Token")
        streamlit.write("Got OAuth token: %s" % streamlit.session_state['oauth_token'])
        authTwitterUser()
    except ValueError:
        print(
            "There may have been an issue with the consumer_key or consumer_secret you entered."
        )

# Get authorization
def authTwitterUser():
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    print("Please go here and authorize: %s" % authorization_url)

# Get the access token
def getAccessToken():
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=streamlit.session_state['oauth_token'],
        resource_owner_secret=streamlit.session_state['oauth_token_secret']
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    streamlit.session_state['twitter_access_token'] = oauth_tokens["oauth_token"]
    streamlit.session_state['twitter_access_token_secret'] = oauth_tokens["oauth_token_secret"]


# Be sure to add replace the text of the with the text you wish to Tweet. You can also add parameters to post polls, quote Tweets, Tweet with reply settings, and Tweet to Super Followers in addition to other features.
def postToTwitter(contentText, image):
    payload = {"text": contentText,
               "media": {"media_ids": ["%s"]%image}
               }

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=streamlit.session_state['twitter_access_token'] ,
        resource_owner_secret=streamlit.session_state['twitter_access_token_secret'],
    )

    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    print("Response code: {}".format(response.status_code))

    # Saving the response as JSON
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))

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

    if "uploadURL" in streamlit.session_state and 'imageURN' in streamlit.session_state:
        # Making the request
        response = oauth.post(
            "https://upload.twitter.com/1.1/media/upload.json",
            media=image
        )

        data = response
        streamlit.write(data.status_code)
    else:
        streamlit.write("We experienced an error with the call!")

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
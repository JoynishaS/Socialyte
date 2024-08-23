import base64
import streamlit
from pathlib import Path
from requests_oauthlib import OAuth1Session
import requests
import json


streamlit.write("Welcome to Socialyte!")
streamlit.write("Sign in to linked in or twitter to begin!")


#Linkedin Code
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded_img = base64.b64encode(img_bytes).decode()
    return encoded_img

#LinkedIn Button!
image_base64 = img_to_bytes("LinkedIn_button.jpg")
url = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={}&redirect_uri={}&state=magentosDomingo&scope=openid%20email%20profile%20w_member_social".format(
    streamlit.secrets['LINKEDIN_CLIENT_ID'], streamlit.secrets['LINKEDIN_REDIRECT_URL'])
html = f"<a href='{url}'><img src='data:image/png;base64,{image_base64}'></a>"
streamlit.markdown(html, unsafe_allow_html=True)

#Twitter Code
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

#Twitter Button!
if streamlit.button("Login to Twitter", type="primary"):
    streamlit.write("Button Pressed")
    requestTwitterToken()





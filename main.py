import base64
from pathlib import Path

import requests
import streamlit
import webbrowser


from streamlit.components.v1 import html

streamlit.write("Welcome to Socialyte!")
streamlit.write("Sign in to linked in or twitter to begin!")

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


def getAccessToken():
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    body = 'grant_type=client_credentials&client_id=%s&client_secret=%s'%(streamlit.secrets['LINKEDIN_CLIENT_ID'],streamlit.secrets['LINKEDIN_CLIENT_SECRET'])
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.post(
        url,
        headers=headers,
        data=body
    )
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    return data['access_token']

#print(getAccessToken())
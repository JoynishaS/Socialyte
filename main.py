import requests
import streamlit
import webbrowser
import streamlit.components.v1 as components

streamlit.write("Welcome to Socialyte!")
streamlit.write("Sign in to linked in or twitter to begin!")

# Define your custom component
def image_button(image_path, label="", width=200, height=50):
    # Frontend code here
    html_str = f"<button><img src='{image_path}' width='{width}' height='{height}'>{label}</button>"
    components.html(html_str, height=height)

# Use the custom component in your app
image_button("https://ibb.co/h2V6V0j", "Click Me", 200, 50)

#Set this up as a separate page. As a home page
def getAuthorizationCode():
    url="https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={}&redirect_uri={}&state=magentosDomingo&scope=openid%20email%20profile%20w_member_social".format(streamlit.secrets['LINKEDIN_CLIENT_ID'],streamlit.secrets['LINKEDIN_REDIRECT_URL'])
    webbrowser.open(url)

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
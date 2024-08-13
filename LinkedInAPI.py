import requests
import streamlit
import webbrowser


def getAuthorizationCode():
    url="https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={}&redirect_uri={}&state=magentosDomingo&scope=openid%20email%20profile%20w_member_social".format(streamlit.secrets['LINKEDIN_CLIENT_ID'],streamlit.secrets['LINKEDIN_REDIRECT_URL'])
    #webbrowser.open(url)
    nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
    """ % (url)
    streamlit.write(nav_script, unsafe_allow_html=True)

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
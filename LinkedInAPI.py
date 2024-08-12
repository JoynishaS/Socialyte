import requests
import streamlit

def getAuthorizationCode():
    url="https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={}&redirect_uri={}&state=magentosDomingo&scope=openid%20email%20profile%20w_member_social".format(streamlit.secrets['LINKEDIN_CLIENT_ID'],streamlit.secrets['LINKEDIN_REDIRECT_URL'])
    headers ={}
    payload ={}
    response = requests.get(
        url,
        headers = headers,
        data = payload,
    )
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response
    return data

getAuthorizationCode()

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
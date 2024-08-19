import streamlit
import requests
import json



#Get Access Token For LinkedIn
def getAccessTokenLinkedIn():
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    body = 'grant_type=authorization_code&code=%s&client_id=%s&client_secret=%s&redirect_uri=https://socialyte.streamlit.app/app'%(streamlit.query_params.code,streamlit.secrets['LINKEDIN_CLIENT_ID'],streamlit.secrets['LINKEDIN_CLIENT_SECRET'])
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

#Get Author ID
def getAuthorID():
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {
        'Authorization': 'Bearer %s'%(streamlit.session_state['linkedInToken']),
    }
    body = {}
    response = requests.get(
        url,
        headers = headers,
        data = body
    )
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    return data['sub']

#Post to LinkedIn
def postToLinkedIn():
    authorID = getAuthorID()
    if 'authorID' is not streamlit.session_state:
        streamlit.session_state['authorID'] = authorID
        streamlit.session_state['uploadURL'] = initializeImageUpload()
    url = "https://api.linkedin.com/rest/posts"
    body = json.dumps({
      "author": "urn:li:person:%s"%(authorID),
      "commentary": "%s"%(streamlit.session_state['key']),
      "visibility": "PUBLIC",
      "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
      },
      "lifecycleState": "PUBLISHED",
      "isReshareDisabledByAuthor": False
})
    headers = {
        'Authorization': 'Bearer %s'%(streamlit.session_state['linkedInToken']),
        'X-Restli-Protocol-Version': '2.0.0',
        'LinkedIn-Version': '202308',
        'Content-Type': 'application/json'
    }
    response = requests.post(
        url,
        headers=headers,
        data=body
    )
    if response.status_code != 201:
        raise Exception("Non-200 response: " + str(response.text))

    data = response
    return data.text

#Initialize Image Upload
def initializeImageUpload():
    url = "https://api.linkedin.com/rest/images?action=initializeUpload"
    body = json.dumps({
    "initializeUploadRequest": {
        "owner": "urn:li:person:%s"%(streamlit.session_state['authorID'])
    }
})
    headers = {
        'Authorization': 'Bearer %s'%(streamlit.session_state['linkedInToken']),
        'X-Restli-Protocol-Version': '2.0.0',
        'LinkedIn-Version': '202307',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(
        url,
        headers=headers,
        data=body
    )
    #if response.status_code != 200:
        #raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    streamlit.write(data)
    return data['uploadUrl']

def uploadImage():
    with open(streamlit.session_state['image'], 'rb') as f:
        if "uploadURL" is streamlit.session_state['uploadURL']:
            requests.post('http://some.url/streamed', data=f)

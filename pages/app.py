import os

import streamlit
from openai import OpenAI
import requests
import json
import LinkedInApi
import tempfile

#Open AI Client Authorization
client = OpenAI(
    organization='org-R2DDZN0eVGgEosD61XGShpU8',
    api_key = streamlit.secrets['OPENAI_API_KEY'],
    project='proj_fqZ8kTAr98ZSgzH5cEdb8mGW'
)
#Only run the function once to get the access code!
if 'linkedInToken' not in streamlit.session_state:
    streamlit.session_state['linkedInToken']  = LinkedInApi.getAccessTokenLinkedIn()

#Function to send user request for images to Open AI
def sendToOpenAI(description):
    return client.images.generate(
        model = "dall-e-3",
        prompt =description,
        n=1,
        size ="1024x1024"
    )

#Function to get URL from Open AI Image request sent by user, save image url for use later
def imageWorkFlow():
    match imageModificationChoice:
        case "***Generate Image by Text***":
            data_response = sendToOpenAI(streamlit.session_state['image_request'])
            streamlit.session_state['image'] = data_response.data[0].url

#Function to send user request for text generation to Open AI
def sendTextToOpenAI(userRequest):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": userRequest}
                ]
    )

def graniteAuthorization():
    url = "https://iam.cloud.ibm.com/identity/token"
    body = 'grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey={}'.format(streamlit.secrets['GRANITE_API_KEY'])
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

def inputDefinition(language):
    match language:
        case "Spanish":
            input = "Translate the following text from English to Spanish"
        case "German":
            input = "Translate the following text from English to German"
    return input

#Function to return localized from Granite
def graniteTextLocalization(texttoTranslate):
    access_token = graniteAuthorization()
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    body = {
        "input": """%s: 
        Text:%s
        Translation:"""%(streamlit.session_state['input'],texttoTranslate),
            "parameters": {
                "decoding_method": "sample",
                "max_new_tokens": 1024,
                "min_new_tokens": 1,
                "random_seed": 42,
                "stop_sequences": ["\n"],
                "temperature": 0.5,
                "top_k": 50,
                "top_p": 0.75,
                "repetition_penalty": 1
            },
            "model_id": "ibm/granite-20b-multilingual",
            "project_id": "7fd2eccd-c7d6-4d4b-a0d9-0649afd36f75"
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer %s"%access_token
    }

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    return data

#Radio Buttons For Image Generation Options
imageModificationChoice = streamlit.radio(
    "Generate an image, Upload your own image",
    ["***Generate Image by Text***", "***Upload your own Image***"],
    index=None,
)

#Switch Statement for Image Generation Options
match imageModificationChoice:
    case "***Generate Image by Text***":
        uploadMyOwnImage = False
        image_request = streamlit.text_input("Enter text for the type of image you want","A cute white bunny with blue eyes")
        streamlit.session_state['image_request'] = image_request
    case "***Upload your own Image***":
        uploadMyOwnImage = True
        uploaded_file = streamlit.file_uploader("Choose a 1024x1024 png image",type = ['png'])
        if uploaded_file is not None:
            streamlit.session_state['image'] = uploaded_file

            #Make a temp file so we can get the path because streamlit fileuploader does not return path
            temp_dir = tempfile.mkdtemp()
            path = os.path.join(temp_dir, uploaded_file.name)
            with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())
            streamlit.session_state['uploaded_image_url'] = path

#Input Field for User to enter their request to Open AI for Text Generation
topic_request = streamlit.text_input("Enter a topic for your post","Write a post for Twitter about the history of White Bunnies with Blue Eyes")

#Dropdown to allow users to choose what language they want to translate to
translation_request = streamlit.selectbox("What Language should the post be in?", ("English","Spanish", "German"))

#When the user clicks submit add the text returned and image from Open AI to the screen, also save text for use later.
if streamlit.button("Submit", type="primary"):
    #This is how you can get params in the url!!!
    streamlit.write("We should be here")
    text_returned = sendTextToOpenAI(topic_request).choices[0].message.content

    #Localize if a language other then english is selected from the dropdown
    if translation_request != "English":
        language_input = inputDefinition(translation_request)
        streamlit.session_state['input'] = language_input
        localized_text = graniteTextLocalization(text_returned)['results'][0]['generated_text']
        language_text = streamlit.text_area("Your Localized Post", localized_text)
        streamlit.session_state['key'] = language_text
    else:
        final_post_text = streamlit.text_area("Your Post", text_returned)
        streamlit.session_state['key'] = final_post_text

    #Get image url
    imageWorkFlow()

#Display image saved on the screen
if 'image' in streamlit.session_state and 'key' in streamlit.session_state:
    streamlit.image(streamlit.session_state['image'])


#Allow the user to choose what platform they want to post to and submit!
if 'key' in streamlit.session_state and 'image' in streamlit.session_state:
    platform_request = streamlit.selectbox("Which platform do you want to post on?", ("LINKEDIN", "TWITTER"))
    if streamlit.button("Post", type="primary"):
        streamlit.write("We Posted the content on ",platform_request)
        streamlit.write(streamlit.session_state['key'])
        if(platform_request == "LINKEDIN"):
            LinkedInApi.postToLinkedIn()




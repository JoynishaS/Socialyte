import streamlit
from openai import OpenAI
import os

client = OpenAI(
    organization='org-R2DDZN0eVGgEosD61XGShpU8',
    api_key = streamlit.secrets['OPENAI_API_KEY'],
    project='proj_fqZ8kTAr98ZSgzH5cEdb8mGW'
)

image_request = streamlit.text_input("Enter text for the type of image you want","A cute white bunny with blue eyes")
topic_request = streamlit.text_input("Enter a topic for your post","How pretty white bunnies with blue eyes are")
translation_request = streamlit.selectbox("What Language should the post be in?", ("EN", "ES"))
streamlit.write(image_request)
streamlit.write(topic_request)

def sendToOpenAI(description):
    client.images.generate(
        model = "dall-e-3",
        prompt =description,
        n=1,
        size ="1024 x 1024"
    )

if streamlit.button("Submit", type="primary"):
    streamlit.write("We will send to Open AI Here and return the post in ",translation_request)
    text_returned = streamlit.text_area("This is the text OpenAI Returned","Text that was returned")
    data_response = sendToOpenAI(topic_request)
    streamlit.write(data_response["data"])
    streamlit.session_state['key'] = text_returned
    streamlit.session_state['image'] = data_response

if 'key' in streamlit.session_state:
    platform_request = streamlit.selectbox("Which platform do you want to post on?", ("LINKEDIN", "TWITTER"))
    if streamlit.button("Post", type="primary"):
        streamlit.write("We Posted the content on ",platform_request)
        streamlit.write(streamlit.session_state['key'])


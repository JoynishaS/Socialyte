import streamlit

image_request = streamlit.text_input("Enter text for the type of image you want","A cute white bunny with blue eyes")
topic_request = streamlit.text_input("Enter a topic for your post","How pretty white bunnies with blue eyes are")
translation_request = streamlit.selectbox("What Language should the post be in?", ("EN", "ES"))
streamlit.write(image_request)
streamlit.write(topic_request)
if streamlit.button("Submit", type="primary"):
    streamlit.write("We will send to Open AI Here and return the post in ",translation_request)
    platform_request = streamlit.selectbox("Which platform do you want to post on?", ("LINKEDIN", "TWITTER"))

if streamlit.button("Post", type="primary"):
    streamlit.write("We Posted the content on ",platform_request)

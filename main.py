import base64
import streamlit
from pathlib import Path


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




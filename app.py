import streamlit as st
import warnings
warnings.filterwarnings("ignore")
from authlib.integrations.requests_client import OAuth2Session
import os

# Load environment variables
CLIENT_ID = os.getenv("client_id")
CLIENT_SECRET = os.getenv("client_secret")
REDIRECT_URI = "https://smartfinanceapp.streamlit.app/oauth2callback"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

# Initialize session state for authentication
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
    st.session_state["user_name"] = None
    st.session_state["token"] = None

# Function to display the login screen
def login_screen():
    
    st.header("This app is private.")
    st.subheader("Please log in.")
    oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope="openid email profile")
    auth_url, state = oauth.create_authorization_url(AUTH_URL)
    st.session_state["oauth_state"] = state
    st.markdown(f"[Log in with Google]({auth_url})")

# Handle OAuth2 callback
def handle_callback():
    
    query_params = st.experimental_get_query_params()
    st.write("Query Params:", query_params)  # Debugging

    if "code" in query_params:
        try:
            oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URI)
            authorization_response = REDIRECT_URI + "?" + "&".join([f"{k}={v[0]}" for k, v in query_params.items()])
            st.write("Authorization Response URL:", authorization_response)  # Debugging

            token = oauth.fetch_token(
                TOKEN_URL,
                authorization_response=authorization_response,
            )
            st.session_state["token"] = token
            user_info = oauth.get(USERINFO_URL, token=token).json()
            st.session_state["is_logged_in"] = True
            st.session_state["user_name"] = user_info.get("name", "Unknown User")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error during authentication: {e}")
            st.stop()

# Main app logic
if not st.session_state["is_logged_in"]:
    st.write("Session State:", st.session_state)  # Debugging
    st.write("Query Params:", st.query_params)  # Debugging
    if "code" in st.query_params:
        handle_callback()
        st.header(f"Welcome, {st.session_state['user_name']}!")
    else:
        login_screen()
else:
    st.header(f"Welcome, {st.session_state['user_name']}!")
    if st.button("Log out"):
        st.session_state["is_logged_in"] = False
        st.session_state["user_name"] = None
        st.session_state["token"] = None
        st.experimental_rerun()

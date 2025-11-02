import streamlit as st
from authlib.integrations.requests_client import OAuth2Session

import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Load secrets
#client_id = st.secrets["CLIENT_ID"]
#client_secret = st.secrets["CLIENT_SECRET"]
redirect_uri = 'http://localhost:8501'  # Update if deploying to cloud

# OAuth endpoints
authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"
token_url = "https://oauth2.googleapis.com/token"
userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"

# Initialize session
if "token" not in st.session_state:
    oauth = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri, scope="openid email profile")
    auth_url, state = oauth.create_authorization_url(authorize_url)
    st.markdown(f"[🔐 Login with Google]({auth_url})")
    st.stop()

# Fetch user info
oauth = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)
token = st.session_state.get("token")
if not token:
    token = oauth.fetch_token(token_url, authorization_response=st.experimental_get_query_params())
    st.session_state["token"] = token

user_info = oauth.get(userinfo_url, token=token).json()
email = user_info.get("email", "unknown")

# Role-based access
roles = {
    "venkat@example.com": "admin",
    "student@example.com": "user"
}
role = roles.get(email, "guest")

# UI
st.title("🔐 Streamlit Auth App")
st.write(f"Welcome, **{email}**")
st.write(f"Your role: **{role}**")

if role == "admin":
    st.success("✅ Admin Dashboard")
    st.write("Here you can manage users, view analytics, and configure settings.")
elif role == "user":
    st.info("📊 User Dashboard")
    st.write("Access your data, reports, and personalized content.")
else:
    st.warning("🚫 Guest Access")
    st.write("Please contact admin to request access.")

import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Load credentials from Streamlit secrets
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
REDIRECT_URI = st.secrets["REDIRECT_URI"]

# Set up scope
SCOPE = "user-library-read"

# Setup SpotifyOAuth
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True,
    cache_path=".cache"
)

# Get the auth URL
auth_url = sp_oauth.get_authorize_url()

# Session state to persist token
if "token_info" not in st.session_state:
    st.session_state.token_info = None

st.title("🎵 Spotify Auth Demo")

# Display login URL
if st.session_state.token_info is None:
    st.markdown(f"[Click here to authorize Spotify]({auth_url})")
    code = st.query_params().get("code", [None])[0]

    if code:
        # Get token using the code and save in session state
        token_info = sp_oauth.get_access_token(code, as_dict=False)  # Avoid deprecation warning
        if token_info:
            st.session_state.token_info = token_info
            st.success("✅ Authentication successful!")
            st.experimental_rerun()
else:
    # Use the cached token
    sp = spotipy.Spotify(auth=st.session_state.token_info)

    # Example: Get current user's saved tracks
    results = sp.current_user_saved_tracks(limit=10)
    st.header("🎧 Your Saved Tracks")

    for idx, item in enumerate(results['items']):
        track = item['track']
        st.write(f"{idx + 1}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")

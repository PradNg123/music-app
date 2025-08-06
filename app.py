import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load credentials from Streamlit secrets
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
REDIRECT_URI = st.secrets["REDIRECT_URI"]

# Set up Spotify authentication
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-top-read"
)

st.title("🎧 Spotify Snapshot - Your Top Tracks")

# Get authorization URL
auth_url = sp_oauth.get_authorize_url()
st.markdown(f"[Click here to login with Spotify]({auth_url})")

# User enters redirected URL manually
redirect_response = st.text_input("Paste the URL you were redirected to after login:")

if redirect_response:
    code = sp_oauth.parse_response_code(redirect_response)
    token_info = sp_oauth.get_access_token(code)

    if token_info:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        results = sp.current_user_top_tracks(limit=10, time_range='short_term')

        st.subheader("🎵 Your Top Tracks:")
        for idx, item in enumerate(results['items']):
            st.write(f"{idx+1}. {item['name']} - {item['artists'][0]['name']}")

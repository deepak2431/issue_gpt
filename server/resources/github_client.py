import os
from flask_restful import Resource, reqparse, request
from flask import redirect
import requests

from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")


def get_client_access_token(client_id, client_secret, token):
    """Get client access token."""

    url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    payload = {"client_id": client_id, "client_secret": client_secret, "code": token}
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(response.status_code, response.json())
        return None

class GithubOauth(Resource):

    def get(self):

        oauth_url = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}"
        return redirect(oauth_url)

    
class GithubCallback(Resource):
    
    def get(self):

        try:
            access_code = request.args.get("code")
            access_token = get_client_access_token(CLIENT_ID, CLIENT_SECRET, access_code)
            if access_token:
                return {"message": "Access token retrieved successfully", "access_token": access_token}, 200
            else:
                return {"message": "Failed to retrieve access token"}, 400
        except Exception as e:
            # Handle general errors
            return {"message": f"Error in callback: {e}"}, 500
        



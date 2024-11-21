from flask import jsonify, request, current_app, url_for, redirect
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
from app.auth import bp

def create_flow():
    flow = Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/calendar.readonly']
    )
    flow.redirect_uri = url_for('auth.oauth2callback', _external=True)
    return flow


@bp.route('/google/authorize')
def google_authorize():
    flow = create_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent',
    )

    # return jsonify({'authorization_url': authorization_url})
    return redirect(authorization_url)

@bp.route('/google/callback')
@bp.route('/google/callback')
def oauth2callback():
    flow = create_flow()
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    
    credentials = flow.credentials
    return jsonify({
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'scopes': credentials.scopes,
    })

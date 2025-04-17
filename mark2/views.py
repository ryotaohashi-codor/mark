import os
import requests
from django.shortcuts import redirect, render
from django.http import JsonResponse
from dotenv import load_dotenv


FB_APP_ID=os.environ.get('ID')
FB_APP_SECRET=os.environ.get('SECRET')
FB_REDIRECT_URI='http://127.0.0.1:8000/facebook/callback/'


def facebook_login(request):
    auth_url = (
        f"https://www.facebook.com/v22.0/dialog/oauth"
        f"?client_id={FB_APP_ID}"
        f"&redirect_uri={FB_REDIRECT_URI}"
        f"&scope=public_profile"

    )
    return redirect(auth_url)


def facebook_callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "認証コードがありません"}, status=400)

    token_url = (
        f"https://graph.facebook.com/v22.0/oauth/access_token"
        f"?client_id={FB_APP_ID}"
        f"&redirect_uri={FB_REDIRECT_URI}"
        f"&client_secret={FB_APP_SECRET}"
        f"&code={code}"
    )

    token_response = requests.get(token_url)
    data = token_response.json()
    
    if "access_token" not in data:
        return JsonResponse({"error": "トークン取得に失敗"}, status=400)

    access_token = data["access_token"]

    # 必要ならばここでDB保存、セッション格納など
    return JsonResponse({"access_token": access_token})
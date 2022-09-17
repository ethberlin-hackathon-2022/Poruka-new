import os
import time
from flask import Flask, make_response, request
import tweepy
import requests

app = Flask(__name__)

clientT = tweepy.Client(os.getenv("TWITTER_BEARER"))

oauth1_user_handler = tweepy.OAuth1UserHandler(
        consumer_key=os.getenv("API_KEY"), consumer_secret=os.getenv("API_SEC"),
        callback="http://localhost:5000/callback"
    )

@app.route("/auth")
def twitterauth():
    oauth1_user_handler = tweepy.OAuth1UserHandler(
        consumer_key=os.getenv("API_KEY"), consumer_secret=os.getenv("API_SEC"),
        callback="http://localhost:5000/callback"
    )

    url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)

    response = make_response({"url": url}, 200)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/callback")
def test():
    access_token, access_token_secret = oauth1_user_handler.get_access_token(
        request.args['oauth_verifier']
    )
    print(access_token, access_token_secret)

    client = tweepy.Client(
        consumer_key=os.getenv("API_KEY"),
        consumer_secret=os.getenv("API_SEC"),
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    id_ = client._get_authenticating_user_id(oauth_1=True)
    user = client.get_user(id=id_, user_fields=["username", "id", "profile_image_url"])
    profile_image_url = user.data.profile_image_url
    username = user.data.username

    response = make_response({"id": id_, "username": username, "img": profile_image_url}, 200)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/v1/getTwitterIDs", methods=["GET"])
def getTwitterIDs():
    try:
        twitter_ids = clientT.get_users(usernames=",".join([x.strip("@") for x in request.args["names"].split(",")]), user_fields=["id"])
        res_ids = {u.id: u.username for u in twitter_ids.data}
    except Exception as e:
        print(str(e))
        res_ids = "No ids found"
    response = make_response({"result": res_ids}, 200)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

# library
# _library
@app.route("/v1/getTwitterNames", methods=["GET"])
def getTwitterNames():
    try:
        twitter_names = clientT.get_users(ids=",".join([str(x) for x in request.args["ids"].split(",")]), user_fields=["username"])
        res_names = {u.username: u.id for u in twitter_names.data}
    except Exception as e:
        print(str(e))
        twitter_names = "No names found"
    response = make_response({"result": twitter_names}, 200)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/getFollower', methods=["GET"])
def get_follower():
    try:
        # Warning: RateLimits 15 requests per 15 mins
        following = {}
        for response in tweepy.Paginator(clientT.get_users_following, request.args["id"], user_fields=["username", "id", "profile_image_url"], max_results=1000):
            following = {**following, **{u.username: {"id": u.id, "img": u.profile_image_url} for u in response.data}}
        response = make_response({"result": following}, 200)
    except Exception as e:
        print(e)
        following = {}
        response = make_response({"result": following}, 429)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == "__main__":
    app.run(debug=True)

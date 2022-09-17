import os
import urllib.parse
from flask import Flask, make_response, request, redirect
import tweepy

app = Flask(__name__)

twitterCounter = 0
bearerToken = [os.getenv("TWITTER_BEARER"), os.getenv("TWITTER_BEARER2")]

oauth1_user_handler = tweepy.OAuth1UserHandler(
        consumer_key=os.getenv("API_KEY"), consumer_secret=os.getenv("API_SEC"),
        callback="https://givewithporuka.pythonanywhere.com/callback"
    )

@app.route("/auth", methods=["GET"])
def twitterauth():
    """
    Start Twitter Authentication process.

    Returns:
    url (string): Twitter authorization url. Open so that user can confirm application.

    """

    global oauth1_user_handler
    oauth1_user_handler = tweepy.OAuth1UserHandler(
        consumer_key=os.getenv("API_KEY"), consumer_secret=os.getenv("API_SEC"),
        callback="https://givewithporuka.pythonanywhere.com/callback"
    )

    url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)

    response = make_response({"url": url}, 200)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/callback")
def callback():
    """
    Twitter callback handler.

    Returns:
    redirect: bring user back to index, now with Twitter account information

    """

    global oauth1_user_handler
    global twitterCounter
    access_token, access_token_secret = oauth1_user_handler.get_access_token(
        request.args['oauth_verifier']
    )

    client = tweepy.Client(
        consumer_key=os.getenv("API_KEY"),
        consumer_secret=os.getenv("API_SEC"),
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    id_ = client._get_authenticating_user_id(oauth_1=True)
    clientT = tweepy.Client(bearerToken[twitterCounter % len(bearerToken)])
    user = clientT.get_user(id=id_, user_fields=["username", "id", "profile_image_url"])
    twitterCounter += 1
    profile_image_url = user.data.profile_image_url
    username = user.data.username
    params = {"id": id_, "username": username, "img": profile_image_url}

    return redirect("https://poruka-new.vercel.app/connect?"+urllib.parse.urlencode(params))


@app.route("/v1/getTwitterIDs", methods=["GET"])
def getTwitterIDs():
    """
    Translate Twitter usernames to Twitter IDs.

    IDriss Twitter handles are translated to IDs so that a given
    link does not disappear whenever someone changes the Twitter username.

    Parameters:
    names (string): comma-separated list of Twitter usernames. Max-length: 100 names.

    Returns:
    result (dict): Key-Value pairs of Twitter usernames and Twitter IDs.

    """
    try:
        global twitterCounter
        clientT = tweepy.Client(bearerToken[twitterCounter % len(bearerToken)])
        twitter_ids = clientT.get_users(usernames=",".join([x.strip("@") for x in request.args["names"].split(",")]), user_fields=["id"])
        twitterCounter += 1
        res_ids = {u.username: u.id for u in twitter_ids.data}
    except Exception as e:
        print(str(e))
        res_ids = "No ids found"
    response = make_response({"result": res_ids}, 200)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/v1/getTwitterNames", methods=["GET"])
def getTwitterNames():
    """
    Translate Twitter IDs to Twitter usernames.

    IDriss Twitter handles are translated to IDs so that a given
    link does not disappear whenever someone changes the Twitter username.
    Translation from IDs to usernames is needed after reverse resolving.

    Parameters:
    ids (string): comma-separated list of Twitter user IDs. Max-length: 100 IDs.

    Returns:
    result (dict): Key-Value pairs of Twitter IDs and Twitter usernames.

    """
    try:
        global twitterCounter
        clientT = tweepy.Client(bearerToken[twitterCounter % len(bearerToken)])
        twitter_names = clientT.get_users(ids=",".join([str(x) for x in request.args["ids"].split(",")]), user_fields=["username"])
        twitterCounter += 1
        res_names = {u.id: u.username for u in twitter_names.data}
    except Exception as e:
        print(str(e))
        res_names = "No names found"
    response = make_response({"result": res_names}, 200)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/getFollowing', methods=["GET"])
def get_follower():
    """
    Retrieve user information of people a given user is following.

    Call after Twitter username of user is known
    (sign-in with Twitter or IDriss reverse resolving) and
    display a list of contacts.

    Parameters:
    id (string): Twitter user ID of given (verified) user.

    Returns:
    result (dict): Nested Key-Value pairs of Twitter usernames to Twitter IDs and profile picture source.
    Example:
        {
            "givewithporuka": {
                "id": "1570867755661889541",
                "img": "https://pbs.twimg.com/profile_images/1570925543473684480/GF3RTo7W_bigger.jpg"
            }
        }

    Warning: Rate limits 15 requests per 15 mins

    """
    try:
        following = {}
        global twitterCounter
        clientT = tweepy.Client(bearerToken[twitterCounter % len(bearerToken)])
        for response in tweepy.Paginator(clientT.get_users_following, request.args["id"], user_fields=["username", "id", "profile_image_url"], max_results=1000):
            if response.data:
                following = {**following, **{u.username: {"id": u.id, "img": u.profile_image_url} for u in response.data}}
        twitterCounter += 1
        response = make_response({"result": following}, 200)
    except Exception as e:
        print(e)
        following = {}
        response = make_response({"result": following}, 429)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == "__main__":
    app.run(debug=True)

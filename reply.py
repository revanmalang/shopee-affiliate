import os
import sys
import requests
import json
import time
import urllib.request
import random
from dotenv import load_dotenv
from get_product import generate_product


def option_post(querystring, payload):
    url = "https://upload.twitter.com/i/media/upload.json"

    if payload != "":
        files = {"media": open(product['image'] + '.jpeg', 'rb')}
        response = requests.request(
            "POST", url, data=payload, files=files, headers=headers, params=querystring)
        return response
    else:

        response = requests.request(
            "POST", url, data=payload, headers=headers, params=querystring)
        return json.loads(response.text)


load_dotenv()
twitter_cookie = os.getenv('TWITTER')
twitter_token = os.getenv('TOKEN')

loop = True
while (loop):
    product = json.loads(generate_product())
    get_image = urllib.request.urlretrieve(
        'https://cf.shopee.sg/file/{}'.format(product['image']), product['image'] + '.jpeg')
    # sys.exit()
    headers = {
        "cookie": twitter_cookie,
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "x-csrf-token": twitter_token,
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
        "x-twitter-auth-type": "OAuth2Session",
        "Referer": "https://twitter.com/",
    }

    get_timeline = requests.post("https://twitter.com/i/api/2/timeline/home.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_collab_control=false&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&earned=1&count=20&lca=true&ext=mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,enrichments,superFollowMetadata,unmentionInfo&browserNotificationPermission=default", headers=headers)
    timeline = json.loads(get_timeline.text)
    for tweet_id in timeline['globalObjects']['tweets']:
        if timeline['globalObjects']['tweets'][tweet_id]['retweet_count'] > 500:

            image = product['image'] + '.jpeg'
            file_name = image
            get_size = os.stat(file_name).st_size

            # init requests
            option_tweet = requests.options(
                'https://upload.twitter.com/i/media/upload.json?command=INIT&total_bytes={}&media_type=image/png&media_category=tweet_image'.format(get_size))
            if option_tweet.status_code == 200:
                # next POST requests
                querystring = {"command": "INIT", "total_bytes": get_size,
                               "media_type": "image/png", "media_category": "tweet_image"}
                payload = ""
                first_post = option_post(querystring, payload)
                if first_post['media_id'] != None:
                    append = requests.options(
                        'https://upload.twitter.com/i/media/upload.json?command=APPEND&media_id={}&segment_index=0'.format(first_post['media_id']))
                    if append.status_code == 200:

                        querystring = {"command": "APPEND",
                                       "media_id": first_post['media_id'], "segment_index": "0"}
                        payload = {"name": "media", "filename": "blob"}
                        upload_image = option_post(querystring, payload)
                        if upload_image.status_code == 204:
                            headers = {
                                "cookie": twitter_cookie,
                                "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                                "x-csrf-token": twitter_token,
                                "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
                                "x-twitter-auth-type": "OAuth2Session",
                                "Referer": "https://twitter.com/home",
                                "content-type": "application/json"
                            }
                            finalization = requests.post(
                                'https://upload.twitter.com/i/media/upload.json?command=FINALIZE&media_id={}'.format(first_post['media_id']), headers=headers)
                            if finalization.status_code == 201:
                                # Reply Payload
                                payload = {"variables": {"tweet_text": product['description'], "reply": {"in_reply_to_tweet_id": tweet_id, "exclude_reply_user_ids": []}, "media": {"media_entities": [{"media_id": first_post['media_id'], "tagged_users": []}], "possibly_sensitive": False}, "withDownvotePerspective": False, "withReactionsMetadata": False, "withReactionsPerspective": False, "withSuperFollowsTweetFields": True,
                                                         "withSuperFollowsUserFields": True, "semantic_annotation_ids": [], "dark_request": False}, "features": {"dont_mention_me_view_api_enabled": True, "interactive_text_enabled": True, "responsive_web_uc_gql_enabled": False, "vibe_tweet_context_enabled": False, "responsive_web_edit_tweet_api_enabled": False, "standardized_nudges_misinfo": False, "responsive_web_enhance_cards_enabled": False}}
                                post_tweet = requests.post(
                                    'https://twitter.com/i/api/graphql/Olwyi5wlRl8zaMAJh-GQ6Q/CreateTweet', json=payload, headers=headers)
                                result = json.loads(post_tweet.text)
                                if result['data'] != None:
                                    print("Promosi Berhasil di Tweet")
                                    os.remove(image)
                                    # sys.exit()
                                else:
                                    print("Tweet gagal")
                        else:

                            print("Gagal upload foto")
                    else:
                        print("Gagal generate id media")
            break
    time_sleep = random.randint(5, 12)
    time.sleep(60 * time_sleep)

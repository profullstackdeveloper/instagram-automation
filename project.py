import os
import signal
import time
import random
import pandas as pd
from instagrapi import Client
from constant import hashtag_list, column_names
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

username = os.environ.get("USER_NAME")
password = os.environ.get("USER_PASSWORD")

def random_delay():
    return random.uniform(10, 30)

def generate_comment():
    comments = [
        "We love supporting small businesses! Keep up the great work.",
        "Congratulations on your launch! Your hard work is inspiring.",
        "Exciting news! Wishing you all the success with your new venture.",
        "Such a fantastic initiative! We're proud to be part of this community.",
        "Incredible! Your dedication and passion shine through in everything you do."
    ]
    return random.choice(comments)

is_running = True


def signal_handler(signal, frame):
    global is_running
    is_running = not is_running
    print("Script Paused" if not is_running else "Script Resumed")


signal.signal(signal.SIGINT, signal_handler)


def run_script():
    global comments_count, likes_count, replies_count, followers_count
    comments_count = 0
    likes_count = 0
    replies_count = 0
    followers_count = 0

    while True:
        if is_running:
            for hashtag in hashtag_list:

                top_posts = cl.hashtag_medias_top(hashtag)

                for post in top_posts:
                    if not is_running:
                        break
                    post_id = post.pk
                    post_code = post.code
                    post_url = f"https://instagram.com/p/{post_code}"
                    print("Post URL:", post_url)


                    if os.path.isfile('Commented_List.csv'):
                        commented_posts = pd.read_csv('Commented_List.csv', dtype=str)
                        if not commented_posts.empty and str(post_id) in commented_posts['Post_ID'].values:
                            print("Post Already Commented\n")
                            continue

                    print("New Post Found, Commenting...\n")


                    time.sleep(random_delay())


                    comment_text = generate_comment()
                    print("Comment:", comment_text)


                    retry = 3
                    while retry > 0:
                        try:
                            comment = cl.media_comment(post_id, comment_text)
                            print("Comment posted successfully.\n")

                            comments_count += 1
                            break
                        except Exception as e:
                            print("Error:", e)
                            if "feedback_required" in str(e):
                                print("Comments disabled for this post. Skipping...")
                                break
                            print("Retrying comment...")
                            retry -= 1
                            time.sleep(60)


                    values = [hashtag, str(post_id), post_code, post_url, comments_count, likes_count, replies_count, followers_count]
                    with open('Commented_List.csv', 'a') as f:
                        if os.stat('Commented_List.csv').st_size == 0:
                            f.write(','.join(column_names) + '\n')
                        f.write(','.join(map(str, values)) + '\n')


                    print("Performance Metrics:")
                    print("No. of Comments posted:", comments_count)
                    print("No. of Likes received:", likes_count)
                    print("No. of Replies received:", replies_count)
                    print("No. of Followers gained:", followers_count)

            print("Checking for new posts in 5 seconds...")
            time.sleep(5)
        else:
            print("Script Paused. Press Ctrl+C to Resume...")
            time.sleep(5)


cl = Client()
cl.login(username, password)

if __name__ == '__main__':
    run_script()
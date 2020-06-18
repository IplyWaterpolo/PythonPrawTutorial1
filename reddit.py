import praw, requests, os, shutil, unicodedata, json
from unidecode import unidecode

path = '/Users/alist/Desktop/reddit/memes'

os.mkdir(path)

url = 'https://www.reddit.com/'

with open('/Users/alist/Desktop/reddit/credentials.json') as f:
    params = json.load(f)



reddit = praw.Reddit(
                client_id=params['client_id'],
                client_secret=params['api_key'],
                password=params['password'],
                user_agent='<reddit_top> accessAPI:v0.0.1 (by/u/redditUser)',
                username=params['username']
)


subreddit = reddit.subreddit('dankmemes')

def deEmojify(inputString):
    returnString = ""

    for character in inputString:
        try:
            character.encode("ascii")
            returnString += character
        except UnicodeEncodeError:
            replaced = unidecode(str(character))
            if replaced != '':
                returnString += replaced
    
    return " ".join(returnString.split()) #removes double spaces after replacing an emoji


name = 0

for submission in subreddit.hot(limit=100):
    name +=1

    if name == 51:
        break
    else: 
        url = (submission.url)
        file_name = str(name)
        if url.endswith(".jpg"):
            file_name += ".jpg"
            found = True
        elif url.endswith(".png"):
            file_name += ".png"
            found = True
        else:
            found = False

        if found == True:
            r = requests.get(url)
            with open(file_name, "wb") as f:
                f.write(r.content)
            
            shutil.move('/Users/alist/Desktop/reddit/'+file_name, path) 
            caption = submission.title
            title = str(name)
            title += ".txt"

            with open(title, "wt") as c:
                c.write(deEmojify(caption))
                c.close()
            shutil.move('/Users/alist/Desktop/reddit/'+title, path)
            print(file_name)
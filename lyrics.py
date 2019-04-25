import tweepy
import time
import random

class markov:

    def __init__(self,order):
        self.order = order
        self.group_size = self.order + 1
        self.text = None
        self.graph = {}
        self.result = ""
        return

    def train(self,fhandle):
        line = fhandle.read()
        line = line.lower()
        self.text = line.split()
        self.text = self.text + self.text[:self.order]

        for i in range(0,len(self.text) - self.group_size):

            key = tuple(self.text[i:i + self.order])
            value = self.text[i + self.order]

            if key in self.graph:
                self.graph[key].append(value)
            else:
                self.graph[key] = [value]

    def generate(self,length):
        index = random.randint(0,len(self.text) - self.order)
        result = self.text[index: index + self.order]
        st = ""
        count = 0

        for i in range(length):
            state = tuple(result[len(result) - self.order:])
            next_word = random.choice(self.graph[state])
            result.append(next_word)

        for i in result:
            st = st + " " + i
            count += 1
            if count > 5:
                st = st + "\n"
                count = 0


        return st




x = markov(2)

fhandle = open("alllyrics.txt","r")
#fhandle2 = open("alllyrics.txt","w")
res = ""
x.train(fhandle)




CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''
print('this is my twitter bot')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
        last_seen_id = retrieve_last_seen_id(FILE_NAME)
        mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        userMessage = mention.full_text.lower()
        if any(srchstr in userMessage for srchstr in ('sad', 'suicide', 'suicidal','ill','help','please','self-harm','cut','kill','hang','dead','mental','health','crazy','insane','mind','losing','down')):
            print("found sad human, responding back")
            api.update_status('@'+mention.user.screen_name + " " + "please give it another day, stay alive fren ||-//\n" + "here are a list of helpline if you need a human\n" + "http://ibpf.org/resource/list-international-suicide-hotlines", mention.id)

        elif any(srchstr in userMessage for srchstr in ('lyrics','song','inspiration','music')):
            print('found lyrics need, responding back with lyrics...')
            res = x.generate(45)
            api.update_status('@' + mention.user.screen_name + ' ' +
                    res, mention.id)

        else:
            print('found happy human, responding back...')
            api.update_status('@' + mention.user.screen_name + ' ' +
                    'Hello back to you! You can ask me for random lyrics!', mention.id)

    res = x.generate(45)
    api.update_status(res)

while True:
    reply_to_tweets()
    time.sleep(15)

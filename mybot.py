import praw
import pdb
import re
import os
import random
import time
import BeautifulSoup
import urllib2

reddit = praw.Reddit('bot1')
if not os.path.isfile("possible_match.txt"):
    possible_match = []
else:
    with open("possible_match.txt", "r") as f:
        possible_match = f.read()
        possible_match = possible_match.split("\n")
        
if not os.path.isfile("motd.txt"):
    motd = []
else:
    with open("motd.txt", "r") as f:
        motd = f.read()
        motd = motd.split("|")
        
if not os.path.isfile("commented.txt"):
    commented = []    
else:
    with open("commented.txt", "r") as f:
        commented = f.read()
        commented = commented.split("\n")
        f.close()
        
if not os.path.isfile("edited.txt"):
    edited = []
else:
    with open("edited.txt", "r") as f:
        edited = f.read()
        edited = edited.split("\n")
        f.close()
        
if not os.path.isfile("replied.txt"):
    replied = []
else:
    with open("replied.txt", "r") as f:
        replied = f.read()
        replied = replied.split("\n")
        f.close()
        
factoid = "*****  \nRandom fact, moment, or curious tidbit in the history of bamboozling:  \n"
addendum ="*****  \n^I'm ^a ^bot ^figthing ^for ^justice"

def searchBamboozle():
    message = "**A possible bamboozle or bamboozling in progress has been alerted. Please visit /r/NoMoreBamboozle if you wish to report or track said promise to ensure that it ends up delivering.**  \n"
    subreddit = reddit.subreddit('test')
    for submission in subreddit.hot(limit=100):
        submission.comments.replace_more(limit=0)
        author = submission.author
        for comment in submission.comments.list():
            if submission.id not in replied_to and author != "BAMBOOZLE_ALERT":
                for match in possible_match:
                    if re.search(match, comment.body, re.IGNORECASE):
                        print("match found")
                        print(comment.body)
                        reply = message + factoid + random.choice(motd) + addendum
                        submission.reply(reply)
                        replied_to.append(submission.id)
                        target = open("commented.txt", 'w')
                        target.write(submission.id)
                        target.write("\n")
                        target.close()


def alertBamboozle():
    message = "**A possible bamboozle or bamboozling in progress has been alerted. Please visit /r/NoMoreBamboozle if you wish to report or track said promise to ensure that it ends up delivering.**  \n"
    subreddit = reddit.subreddit('NoMoreBamboozles')
    for submission in subreddit.hot(limit=100):
        submission.comments.replace_more(limit=0)
        author = submission.author
        for comment in submission.comments.list():
            if comment.id not in replied:
                if re.search("!Nobamboozle", comment.body, re.IGNORECASE):
                    print("match found")
                    print(comment.body)
                    reply = message + factoid + random.choice(motd) + addendum
                    comment.reply(reply)
                    replied.append(comment.id)
                    target = open("replied.txt", 'w')
                    target.write(submission.id)
                    target.write("\n")
                    target.close()
                        
def reportBamboozle():
    subreddit = reddit.subreddit('NoMoreBamboozles')
    for report in subreddit.hot(limit=10):
        title = report.title
        post = ""
        url = report.permalink
        author = report.author
        url = str(url)
        author = str(author)
        text = report.selftext
        completeLink = re.search(r'(?:www|http).*/r/\w.*\s', text, re.I)
        #print(url)
        #print(author)        
        if completeLink:
            subredditLink = re.search(r'r/.*/comments/.*/', completeLink.group(0), re.I)
            words = subredditLink.group(0).split('/')
            #print(words)
            submissionName = words[1]
            submissionID = words[3]
            submission = reddit.submission(id=submissionID)
            message = "**BAMBOOZLE WARNING: [BAMBOOZLE REPORT LINK HERE] (" + url + ")**  \n A dutiful member of the r/NoMoreBamboozles community has reported that the OP or a user in this thread has promised to deliver a specific set of actions in return for upvotes. Be aware that such promises are always capable of bamboozling the goodwill of any redditor. Keep yourself informed on the progress of said promise by visiting the report link above.  \n"
            #comment = message + factoid + random.choice(motd) + addendum
            comment = message + addendum
            if submissionID not in commented:
                post = submission.reply(comment)
                commented.append(submissionID)
                target = open("commented.txt", 'wb')
                target.write(submissionID)
                target.write("\n")
                target.close()
            for comment in report.comments.list():
                if comment.stickied and comment.id not in edited:
                    body = comment.body
                    edit = "  \nEDIT: Report detailing progress of promise has been updated and evaluated by a moderator."
                    body += edit
                    comment.edit(body)
                    target = open("edited.txt", 'wb')
                    target.write(comment.id)
                    target.write("\n")
                    target.close()

def testEdit():
    subreddit = reddit.subreddit('test')
    postID = "5yeb9k"
    commentID = "des337r"
    submission = reddit.submission(postID)
    for comment in submission.comments.list():
        if comment.id == commentID:
            body = comment.body
            edit = "TEST EDIT 2"
            body += edit
            comment.edit(body)
    

#reportBamboozle()
#alertBamboozle()
#testEdit()

try:
    while True:
        reportBamboozle()
        
except praw.exceptions.APIException:
    print '\tSleeping for %d seconds' % error.sleep_time
    time.sleep(error.sleep_time)
    pass

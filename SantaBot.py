from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from itertools import permutations
from math import factorial
from random import randint
import smtplib, ssl

def assigner(players):
    unassigned = set(players.keys())
    for player in list(permutations(unassigned))[randint(0, factorial(len(unassigned)))]:
        # print("Assigning for %s." % player)
        giftees = unassigned.copy()
        try:
            giftees.remove(player)
        except KeyError:
            pass
        if players[player]["nogift"]:
            giftees.difference_update(players[player]["nogift"])
        giftees = list(giftees)
        players[player]["giftee"] = giftees[randint(0, len(giftees) - 1)]
        unassigned.remove(players[player]["giftee"])
        print("%s will give a gift to %s." % (players[player]["name"], players[player]["giftee"]))


# define a dict for each player with emails
players = {
    "Jonas": {"name": "Jonas",
            "email": "jonas.debeukelaer@gmail.com",
            "nogift": [],
            "giftee": None
    },
    "Jeni": {"name": "Jeni",
         "email": "jeni_pillai@hotmail.co.uk",
         "nogift": [],
         "giftee": None
    },
    "Alex": {"name": "Alex",
         "email": "a-k-c@hotmail.co.uk",
         "nogift": [],
         "giftee": None
    },
    "Margot": {"name": "Margot",
         "email": "margot.mollier@gmail.com",
         "nogift": [],
         "giftee": None
    },
    "Sophia": {"name": "Sophia",
         "email": "sophianadri@gmail.com",
         "nogift": [],
         "giftee": None
    },
    "Felix": {"name": "Felix",
         "email": "tfjoutlaw@gmail.com",
         "nogift": [],
         "giftee": None
    }
}

# assign forbidden giftees. Their names must EXACTLY match their name in players.keys()
players["Jonas"]["nogift"].append("Jeni")
players["Jeni"]["nogift"].append("Jonas")
players["Alex"]["nogift"].append("Margot")
players["Margot"]["nogift"].append("Alex")
players["Sophia"]["nogift"].append("Felix")
players["Felix"]["nogift"].append("Sophia")

# assign giftees
k = 0
while k==0:
    # assigner() will fail with a ValueError if the last person to be assigned a giftee has only themselves left to
    # choose from. So just run it repeatedly until it doesn't run into this problem.
    try:
        assigner(players)
        k += 1
    except ValueError:
        pass

# send emails
timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
port = 465  # for SSL
smtp_server = "smtp.gmail.com"
sender_email = "santabot69@gmail.com"
pw = input("Type your password and press enter:")
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, pw)
    for player in players.keys():

        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Secret Santa giftee %s." % timestamp
        message["From"] = sender_email
        message["To"] = players[player]["email"]

        # Create the plain-text and HTML version of your message
        text = """\
        Hi %s,
        You'll be giving a gift to %s!
        Santabot""" % (player, players[player]["giftee"])
        html = """\
        <html>
          <body>
            <p>Hi %s,<br>
               <br>
               You'll be giving a gift to %s!<br>
               <br>
               Santabot
            </p>
          </body>
        </html>
        """ % (player, players[player]["giftee"])

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        server.sendmail(
            sender_email, players[player]["email"], message.as_string()
        )




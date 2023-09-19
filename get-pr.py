import requests
import smtplib
from email.message import EmailMessage
from requests.exceptions import ConnectTimeout


def gh_pr_req(repo, state, token):
  auth_s = "Bearer" + token

  URL = "https://api.github.com/repos/" + repo + "/pulls"

  par = {'Accept' : 'application/vnd.github+json',
       'Authorization' : auth_s,
       'X-GitHub-Api-Version' : '2022-11-28',
       'state' : state,
       'per_page': '100' }

  try:
    r = requests.get ( url = URL, params = par, timeout=30)
  except ConnectTimeout as err:
    print("Connection to URL " + URL + " timed out")
    raise SystemExit

  data = r.json()

  return data




if __name__ == "__main__":

  repo = "pygithub/pygithub"
  token_file = "token.txt"

  draft_list = []
  open_list = []
  close_list = []

  #read token
  try:
     with open(token_file, 'r') as file:
         token = file.read().rstrip()
  except FileNotFoundError as err:
     print(err)
     raise SystemExit

  data = gh_pr_req(repo, "open", token)

  for pr in data:
     if pr['draft'] == True:
        d_str = "DRAFT: " + str(pr['number']) + ", " + pr['title']
        draft_list.append(d_str)
     else:
        if pr['state'] == "open":
           o_str = "OPEN: " + str(pr['number']) + ", " + pr['title']
           open_list.append(o_str)

  data = gh_pr_req(repo, "closed", token)

  for pr in data:
     c_str = "CLOSED: " + str(pr['number']) + ", " + pr['title']
     close_list.append(c_str)

  open_list.append("\n")
  draft_list.append("\n")
  close_list.append("\n")

  e_content = ""

  #print in console
  for l in open_list:
     print(l)
  for l in draft_list:
     print(l)
  for l in close_list:
     print(l)

  e_content = '\n'.join(open_list) + '\n'.join(draft_list) + '\n'.join(close_list) 
   



  # create email
  msg = EmailMessage()
  msg['Subject'] = "PR List"
  msg['From'] = "automated@bitbucket.local"
  msg['To'] = "person@inbucket.local"
  msg.set_content(e_content)

  # send email
  with smtplib.SMTP('127.0.0.1', 2500) as smtp:
      #smtp.login(email_address, email_password)
      smtp.send_message(msg)

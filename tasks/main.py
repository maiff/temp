import os, datetime, json
from flask import Flask, redirect, request, jsonify, render_template, abort
from google.cloud import storage
from google.cloud import datastore
import logging
from mailjet_rest import Client
import os
import requests

url = "https://api-dot-final-project-123-350902.uc.r.appspot.com/api/health"

api_key = '030561d0b18ee8414deb568c5cb08e85'
api_secret = '1f754876829407ca3e6aecdfb9410e9c'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

app = Flask(__name__)

def send_email(email, content):
  data = {
    'Messages': [
      {
        "From": {
          "Email": "xwt2101239@gmail.com",
          "Name": "test"
        },
        "To": [
          {
            "Email": email,
            "Name": "test"
          }
        ],
        "Subject": content,
        "TextPart": content,
      }
    ]
  }
  result = mailjet.send.create(data=data)
  logging.info("email send code: "+str(result.status_code))
  logging.info("email send rsp: "+str(result.json()))

@app.route("/tasks/check_health")
def check_health():
  try:
    rsp = requests.get(url)
  except:
    logging.info("check_health error")
    send_email('xwt2101239@gmail.com',  "❌ Health Error - https://photo-timeline-shared.uc.r.appspot.com/")
    return "ok", 200

  if rsp.status_code == 200:
    logging.info("check_health ok "+str(rsp.status_code))
    send_email('xwt2101239@gmail.com',  "👍 Health Check - https://photo-timeline-shared.uc.r.appspot.com/")
  else:
    logging.info("check_health error "+str(rsp.status_code))
    send_email('xwt2101239@gmail.com',  "❌ Health Error - https://photo-timeline-shared.uc.r.appspot.com/")

  return "OK", 200
  
if __name__ == '__main__':
  app.run(debug=True, port=8080)



import os, datetime, json
from functools import wraps
from flask import Flask, redirect, request, jsonify, render_template, abort
from google.cloud import storage
from google.cloud import datastore
from google.cloud import vision
import logging

app = Flask(__name__)
CLOUD_STORAGE_BUCKET = "final-project-123" 

@app.errorhandler(404)
def page_not_found(e):
    return "Cat not found.", 404
  
@app.route("/api/health")
def health():
  return "OK", 200

@app.route("/api/upload", methods=['POST'])
def upload():

  photo = request.files['file']

  storage_client = storage.Client.from_service_account_json('final-project-123-350902-5facbeacff97.json')

  bucket_name = CLOUD_STORAGE_BUCKET
  bucket = storage_client.bucket(bucket_name)

  blob = bucket.blob(photo.filename)
  blob.upload_from_string(photo.read(), content_type=photo.content_type)
  print(f"File uploaded: {photo.filename} to {blob.public_url}")

  return blob.public_url

if __name__ == '__main__':
  app.run(debug=True, port=8080)

from flask import Blueprint, render_template, send_file
import os 
import boto3
from dotenv import load_dotenv

# regiseter with blueprint
bp = Blueprint("demo", __name__)

# load dotenv
load_dotenv()

# instnatiate s3 client 
s3 = boto3.client("s3", 
                  region_name="us-east-1", 
                  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 
                  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))

# set bucket
S3_BUCKET = "pbs-passthrough"

@bp.route("/demo")
def demo():
    response = s3.get_object(Bucket=S3_BUCKET, Key="grantchester_sample.mp4")
    return send_file(response["Body"], mimetype="video/mp4")
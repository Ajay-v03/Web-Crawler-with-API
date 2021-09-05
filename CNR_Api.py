from time import gmtime, strftime

from CNR import CNR_Test
from CNR_Test import CNR_cases

import os
import PyPDF2
import secrets
from flask import jsonify, request
from flask import Flask, send_from_directory
import datetime


app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/check', methods=['GET', 'POST'])
def check_api():
    updated_part = "Hello this is check API..."
    return jsonify(
        {"statusMessage": "Successfully Completed.", "statusCode": "SRC001", "data": f"API is running, {updated_part}"})


@app.route('/time', methods=['GET', 'POST'])
def check_time():
    time_1 = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    time_2 = str(datetime.datetime.now())
    response = jsonify(
        {"time": {"local time one ": time_1, "local time two": time_2}, "statusMessage": "Successfully Completed.",
         "statusCode": "SRC001"})
    return response

'TNCB0A1234562017'


@app.route('/CNR', methods=['GET', 'POST'])
def CNR():
    # reference id
    referenceid = request.form['referenceId']
    crnnumber = request.form['crnnumber']
    if crnnumber:
        data = CNR_cases(crnnumber)
        return jsonify({"statusMessage": "Successfully Completed.", "statusCode": "SRC001","referenceId": referenceid, "data": data})
    else:
        return jsonify({"statusMessage": "CNR is Empty.", "statusCode": "EFE030", "referenceId": None, "data": {}})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
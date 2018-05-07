#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
#from azure.storage.table import TableService, Entity
from azure.cosmosdb.table import TableService, Entity
import urllib2
# If you are using Python 3+, import urllib instead of urllib2

import json 

STORAGE_ACCOUNT = 'yufengsiotoutput'
ACCOUNT_KEY = 'j4NJoY+a1i7pwY7G+RIuCQw2R0Hx7+y+JpHKULjMOVHB7+sy8hIZxvDInMypSHTbXdKwpLGDlaZKotXrlgcOzw=='

def predictResult():
    data =  {
        "Inputs": {
                "orthopedics":
                {
                    "ColumnNames": ["temperature", "pulse", "DP", "SP"],
                    "Values": [ [ "37", "90", "118", "60" ]]
                },
                "respiratory":
                {
                    "ColumnNames": ["temperature", "pulse", "DP", "SP"],
                    "Values": [ [ "37", "90", "118", "60" ]]
                },
                "cardiology":
                {
                    "ColumnNames": ["temperature", "pulse", "DP", "SP"],
                    "Values": [ [ "37", "90", "118", "60" ]]
                },
                "Sev3":
                {
                    "ColumnNames": ["temperature", "pulse", "DP", "SP"],
                    "Values": [ [ "37", "90", "118", "60" ]]
                },
                "Sev1":
                {
                    "ColumnNames": ["temperature", "pulse", "DP", "SP"],
                    "Values": [ [ "37", "90", "118", "60" ]]
                },
                "Sev2":
                {
                    "ColumnNames": ["temperature", "pulse", "DP", "SP"],
                    "Values": [ [ "37", "90", "118", "60" ]]
                },        },
        "GlobalParameters": {
        }
    }

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/a98efa3d4874420fbfcac30ee34a3252/services/34d6f8fac4c44b84903cd2e1d787ba0c/execute?api-version=2.0&details=true'
    api_key = 'gC9+E7ZkbJD0HL2gS49DIJMMZSlOKrk9H2PpopJkzvZhvxaD5QcSioNoVA8hhngnv7o/A6Ye2l0FvxA/QAb2qw==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib2.Request(url, body, headers) 
    #req = urllib.request.Request(url, body, headers)

    try:
        response = urllib2.urlopen(req)
        #response = urllib.request.urlopen(req)

        # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
        # req = urllib.request.Request(url, body, headers) 
        # response = urllib.request.urlopen(req)

        result = response.read()
        print(result) 
    except urllib2.HTTPError, error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())

        print(json.loads(error.read()))                 

def main():
    predictResult()
    table_service = TableService(account_name = STORAGE_ACCOUNT, account_key = ACCOUNT_KEY)
    task = {'PartitionKey': 'Emergency', 'RowKey': 'IoT-PI-Device','PatientID':'00000003','Severity':'2', 'Specialist':'cardiology,respiratory'}
    table_service.insert_entity('Notification',task)

if __name__ == '__main__':
    main()
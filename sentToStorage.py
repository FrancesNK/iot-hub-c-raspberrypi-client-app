#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
#from azure.storage.table import TableService, Entity
from azure.cosmosdb.table import TableService, Entity, EntityProperty, EdmType
import urllib2
# If you are using Python 3+, import urllib instead of urllib2

import json 
import random
import string

STORAGE_ACCOUNT = 'yufengsiotoutput'
ACCOUNT_KEY = 'j4NJoY+a1i7pwY7G+RIuCQw2R0Hx7+y+JpHKULjMOVHB7+sy8hIZxvDInMypSHTbXdKwpLGDlaZKotXrlgcOzw=='

rowKey = 'IoT-PI-Device-' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))
patientID = '0000000' + str(random.randint(1,4))

temperature = str(random.randint(35,42))
pulse = str(random.randint(30,200))
DP = str(random.randint(30,120))
SP = str(random.randint(50,120))

severity = ''
orthopedics = ''
cardiology = ''
respiratory = ''

def predictResult():
    data =  {
        "Inputs": {
                "orthopedics":
                {
                    "ColumnNames": ["temperature", "pulse", "DP", "SP"],
                    "Values": [ [ temperature, pulse, DP, SP ]]
                },
                "respiratory":
                {
                    "ColumnNames": ["temperature", "pulse", "DP", "SP"],
                    "Values": [ [ temperature, pulse, DP, SP ]]
                },
                "cardiology":
                {
                    "ColumnNames": ["temperature", "pulse", "DP", "SP"],
                    "Values": [ [ temperature, pulse, DP, SP ]]
                },
                "Sev3":
                {
                    "ColumnNames": ["temperature", "pulse", "DP", "SP"],
                    "Values": [ [ temperature, pulse, DP, SP ]]
                },
                "Sev1":
                {
                    "ColumnNames": ["temperature", "pulse", "DP", "SP"],
                    "Values": [ [ temperature, pulse, DP, SP ]]
                },
                "Sev2":
                {
                    "ColumnNames": ["temperature", "pulse", "DP", "SP"],
                    "Values": [ [ temperature, pulse, DP, SP ]]
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
        #print(result)
        jo = json.loads(result)
        
        global severity
        global orthopedics
        global cardiology
        global respiratory
        #print('----------------------------------------------------------')
        severity_u = jo['Results']['severity']['value']['Values']
        orthopedics_u = jo['Results']['orthopedics']['value']['Values']
        cardiology_u = jo['Results']['cardiology']['value']['Values']
        respiratory_u = jo['Results']['respiratory']['value']['Values']
        #print(ja)

        
        for line in severity_u:
            for key in line:
                severity = key
        for line in orthopedics_u:
            for key in line:
                orthopedics = key
        for line in cardiology_u:
            for key in line:
                cardiology = key
        for line in respiratory_u:
            for key in line:
                respiratory = key

    except urllib2.HTTPError, error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())

        jo = json.loads(error.read())
                        
	
def main():
    predictResult()
    table_service = TableService(account_name = STORAGE_ACCOUNT, account_key = ACCOUNT_KEY)
    
    global specialist
    global severity
    
    specialist = ''

    if orthopedics == '1':
        specialist = specialist + ' ' + 'orthopedics'
        if cardiology == '1':
            specialist = specialist + ' ' + 'cardiology'
            if respiratory == '1':
                specialist = specialist + ' ' + 'respiratory'
    
    task = Entity()
    task.PartitionKey = 'Emergency'
    task.RowKey = rowKey
    task.PatientID = patientID
    task.Temperature = temperature
    task.Pulse = pulse
    task.DP = DP
    task.SP = SP
    task.Status = 'open'

    task.Severity = EntityProperty(EdmType.STRING, severity)
    task.Specialist = EntityProperty(EdmType.STRING, specialist)

    table_service.insert_or_replace_entity('Notification',task)

if __name__ == '__main__':
    main()

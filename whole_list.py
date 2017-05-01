# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 10:28:56 2016

@author: abhishek
"""
from __future__ import print_function
import httplib2
import os
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import datetime
import bs4 as bs
import urllib.request

''' please enter the batch code here'''

batch_list={'aku':['SDTR68A7','SDTW68D1','SDPB67A2','SDPB67B1','SDIC67A1'],
            'tc':['SDTR68A5','SDTW68A9','SDPA67C6','SDSA67W1','SDTR79P1'],
            'rdk':['SDTR68A1','SDPA67G1','METAMORPHOSISSANKALP68S']
            }
date={'Monday':'2017-02-27','Tuesday':'2017-02-28','Wednesday':'2017-03-01',
      'Thursday':'2017-03-02','Friday':'2017-03-03','Saturday':'2017-03-04',
      'sunday':'2017-03-05'}  

sauce=urllib.request.urlopen('http://fiitjeesouthdelhi.co.in/time-table/?batch=100').read()
soup=bs.BeautifulSoup(sauce,'lxml')
n=[];m=[]
for z in soup.findAll('option'):
    n.append(z.get('value'))
for z in soup.findAll('option'):
    m.append(z.text)
batch_code={}
for i in range(len(n)):
    batch_code[n[i]]=m[i]
day=['Monday-box1','Tuesday-box1','Wednesday-box1','Thursday-box1',
     'Friday-box1','Saturday-box1','sunday-box1']
batch={}
for i in range(2,len(n)):
    url='http://fiitjeesouthdelhi.co.in/time-table/?batch=' +str(i)
    sauce=urllib.request.urlopen(url).read()
    soup=bs.BeautifulSoup(sauce,'lxml')
    x={}    
    for days in day:
        z=[]
        for para in soup.findAll('div',class_=eval('days')):
            z.append(para.text)
            for l in range(len(z)):
                z[l]=z[l].replace('\n',' ')
            x[days]=z
    batch[batch_code[str(i)]]=x

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'

APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials(x):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    ##home_dir = os.path.expanduser('~')
    CLIENT_SECRET_FILE = x + '.json'
    
    home_dir = os.path.join('C:\\Users\\abhishek\\fiitjee', x)
    os.chdir(home_dir)
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main(a):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials(a)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/google-apps/calendar/quickstart/python
    # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
    # stored credentials.
    x=[]
    for l in batch_list[a]:
        for i in batch[l].items():
            for j in i[1]:
                if j.find('PHY') !=-1 or j.find('P-') !=-1 :
                    x.append(i[0]+j+' '+l)
    for j in range(len(x)):
        x[j]=x[j].replace('-box1',' ')
        x[j]=x[j].replace('PHYSICS',' ')
    
    for i in x:
        s=i.split()
        s[0]=date[s[0]]
        if len(s[1]) !=5:
            s[1]='0'+s[1]
        if len(s[3]) !=5:
            s[3]='0'+s[3]
        if s[1][0]=='0':        
            s[1]=str(int(s[1][0:2])+12)+':'+s[1][3:5]
        if s[3][0]=='0':
                s[3]=str(int(s[3][0:2])+12)+':'+s[3][3:5]
        print(s)
        start=s[0]+'T'+s[1]+':00+05:30'
        end=s[0]+'T'+s[3]+':00+05:30'
        event = {
        'summary': s[5],
          'location': s[4],
          'start': {
          'dateTime': start,
          'timezone':'India/kolkata'
          },
          'end': {
          'dateTime': end,
          'timezone':'India/kolkata'
          }
          }
        try:
            event = service.events().insert(calendarId='primary', body=event).execute()
            print(i)
            print ('Event created: %s' % (event.get('htmlLink')))
        except:
            print('error')


for i in batch_list.keys():
    main(i)
    
"""
Parsing utilities for various Illiad account pages.

Parsers are separated so that they can be unit tested more easily and adjusted
without changing the application logic.
"""
import logging
import re

from pyquery import PyQuery as pq
from bs4 import BeautifulSoup

DIGITS_RE = re.compile('(\d+)')

def main_menu(content):
    out = {'authenticated': False,
           'session_id': None,
           'registered': None}
    soup = BeautifulSoup(content)
    page_title = soup.title.text
    #If the user is registered, the page title will be Illiad Main Menu.
    if page_title == 'ILLiad Main Menu':
        out['registered'] = True
    else:
        #To do - make this raise a module specific Exception that client
        #code can handle.
        out['registered'] = False
    session_id = soup.select('#SessionID')[0].attrs.get('value')
    out['session_id'] = session_id
    out['authenticated'] = True
    return out

def request_form(content):
    """
    Parse Illiad's OpenUrl request form.
    """
    submit_key = {}
    soup = BeautifulSoup(content)
    title = soup.title
    #check for blocked
    try:
        status_message = soup.select('#status')[0].text
    except IndexError:
        logging.info("Unable to parse status from ILLiad request page %s." % title)
    if status_message:
        if status_message.rfind('blocked') > 0:
            submit_key['errors'] = status_message
            submit_key['blocked'] = True
            return submit_key

    #Get all of the inputs.
    inputs = soup('input')
    
    for item in inputs:
        attrs = item.attrs
        name = attrs.get('name')
        value = attrs.get('value')
        #Skip certain values
        if value is None:
            continue
        if value.startswith('Clear'):
            continue
        if value.startswith('Cancel'):
            continue
        submit_key[name] = value
    
    #Add text areas too
    textareas = soup('textarea')
    for box in textareas:
        name = box.attrs['name']
        value = box.text
        if (value is not None) and (value != ''):
            submit_key[name] = value
        
    return submit_key

def request_submission(content):
    """
    Parse the submitted request response from Illiad.
    """
    out = {
           'transaction_number': None,
           'submitted': False,
           'error': False,
           'message': None
           }

    soup = BeautifulSoup(content)
    #Check for submission errors.
    try:
        errors = soup.select('.statusError')[0].text
    except IndexError:
        errors = None
    if errors:
        out['error'] = True
        out['message'] = errors
        return out
    
    #Get transaction number
    #Article Request Received. Transaction Number 473283
    try:
        confirm_message = soup.select('.statusInformation')[0].text
        out['message'] = confirm_message
    except IndexError:
        out['error'] = True
        out['message'] = "Unable to find confirmation message"
    match = re.search(DIGITS_RE, confirm_message)
    if match:
        number = match.groups()[0]
        out['transaction_number'] = number
        out['submitted'] = True
    return out
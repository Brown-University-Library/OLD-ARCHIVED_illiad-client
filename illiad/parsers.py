"""
Parsing utilities for various Illiad account pages.

Parsers are separated so that they can be unit tested more easily and adjusted
without changing the application logic.
"""

from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import re

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

def logout(content):
    """
    Parse the returned screen of the logout request.  This is expecting a
    Brown Illiad login/out page: https://illiad.brown.edu/illiad/illiad.dll
    
    There doesn't seem like a real way to ensure that logout has 
    happened.  
    """
    out = {'authenticated': True}
    doc = pq(content)
    #Change here if the logout page fails. 
    logon_button = doc('input[name="SubmitButton"]').attr('value')
    out['button'] = logon_button
    if logon_button:
        if logon_button.rfind('Logon') > -1:
            out['authenticated'] = False
    return out

def request_form(content):
    """
    Parse Illiad's OpenUrl request form.
    """
    submit_key = {}
    doc = pq(content)
    #check for blocked
    status_message = doc('#status').text()
    if status_message:
        if status_message.rfind('blocked') > 0:
            submit_key['errors'] = status_message
            submit_key['blocked'] = True
            return submit_key
    inputs =  doc('form').find('input')
    
    for i in inputs:
        #skip certain values
        if not i.value:
            continue
        if i.value.startswith('Clear'):
            continue
        if i.value.startswith('Cancel'):
            continue
        submit_key[i.name] = i.value
    
    #add text areas too
    texts = doc('form').find('textarea')
    for t in texts:
        submit_key[t.name] = t.value
        
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
    doc = pq(content)
    #errors
    errors = doc('.statusError').text()
    if errors:
        out['error'] = True
        out['message'] = errors
        return out
    
    #transaction number
    #Article Request Received. Transaction Number 473283
    confirm_message = doc('.statusInformation').text()
    out['message'] = confirm_message
    match = re.search('(\d+)', confirm_message)
    if match:
        number = match.groups()[0]
        out['transaction_number'] = number
        out['submitted'] = True
    return out
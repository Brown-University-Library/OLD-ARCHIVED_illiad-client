# -*- coding: utf-8 -*-

from __future__ import unicode_literals
"""
Parsing utilities for various Illiad account pages.

Parsers are separated so that they can be unit tested more easily and adjusted
without changing the application logic.
"""
import logging, re
from bs4 import BeautifulSoup


DIGITS_RE = re.compile('(\d+)')


def main_menu(content):
    out = {'authenticated': False,
           'session_id': None,
           'registered': None}
    soup = BeautifulSoup( content, 'html.parser' )
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
    """ Parses illiad's openurl request form.
        Returns dct of values which will be POSTed to submit the request.
        Called by account.py IlliadSession.get_request_key() """
    submit_key = {}
    soup = BeautifulSoup( content, 'html.parser' )
    submit_key = _check_blocked( soup, submit_key )
    submit_key = _check_inputs( soup, submit_key )
    submit_key = _check_textareas( soup, submit_key )
    return submit_key

def _check_blocked( soup, submit_key ):
    """ Checks for blocked status.
        Called by request_form() """
    try:
        title = soup.title.text
        status_message = soup.select('#status')[0].text
    except IndexError:
        logging.info("Unable to parse status from ILLiad request page %s." % title)
        status_message = None
    if status_message:
        if status_message.rfind('blocked') > 0:
            submit_key['errors'] = status_message
            submit_key['blocked'] = True
    return submit_key

def _check_inputs( soup, submit_key ):
    """ Updates key-dct with html input data.
        Called by request_form() """
    inputs = soup( 'input' )
    for item in inputs:
        attrs = item.attrs
        name = attrs.get('name')
        value = attrs.get('value')
        if (value is None) or (value == u'') or (value.startswith('Clear')) or (value.startswith('Cancel')):
            continue
        if name == 'IlliadForm':  # we're still capturing ILLiadForm (note case of 'L's)
            continue
        submit_key[name] = value
    return submit_key

def _check_textareas( soup, submit_key ):
    """ Updates key-dct with html textarea data.
        Called by request_form() """
    textareas = soup( 'textarea' )
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

    soup = BeautifulSoup( content, 'html.parser' )
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
        match = re.search(DIGITS_RE, confirm_message)
        if match:
            number = match.groups()[0]
            out['transaction_number'] = number
            out['submitted'] = True
    except IndexError:
        out['error'] = True
        out['message'] = "Unable to find confirmation message"

    return out

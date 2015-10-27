# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os, pprint, unittest
from illiad.account import IlliadSession


class AccountTest(unittest.TestCase):

    def setUp(self):
        self.ILLIAD_REMOTE_AUTH_URL = os.environ['ILLIAD_MODULE__TEST_REMOTE_AUTH_URL']
        self.ILLIAD_REMOTE_AUTH_KEY = os.environ['ILLIAD_MODULE__TEST_REMOTE_AUTH_KEY']
        self.ILLIAD_USERNAME = os.environ['ILLIAD_MODULE__TEST_USERNAME']
        self.ill = IlliadSession(
            self.ILLIAD_REMOTE_AUTH_URL, self.ILLIAD_REMOTE_AUTH_KEY, self.ILLIAD_USERNAME )

    def test_login(self):
        login = self.ill.login()
        self.assertTrue(login.has_key('session_id'))
        self.assertTrue(login.has_key('authenticated'))
        self.assertTrue(login.has_key('registered'))
        self.assertTrue(login['authenticated'])

    def test_submit_key(self):
       ill = self.ill
       ill.login()
       #Url encoded
       openurl = "rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&rft.spage=538&rft.issue=5&rft.date=2010-02-11&rft.volume=16&url_ver=Z39.88-2004&rft.atitle=Targeting+%CE%B17+Nicotinic+Acetylcholine+Receptors+in+the+Treatment+of+Schizophrenia.&rft.jtitle=Current+pharmaceutical+design&rft.issn=1381-6128&rft.genre=article"
       submit_key = ill.get_request_key(openurl)
       self.assertEqual(submit_key['ILLiadForm'],
                        'ArticleRequest')
       self.assertEqual(submit_key['PhotoJournalTitle'],
                        'Current pharmaceutical design')
       ill.logout()

    def test_book(self):
      ill = self.ill
      ill.login()
      #Url encoded
      openurl = "sid=FirstSearch:WorldCat&genre=book&isbn=9780231122375&title=Mahatma%20Gandhi%20%3A%20nonviolent%20power%20in%20action&date=2000&rft.genre=book"
      submit_key = ill.get_request_key(openurl)
      self.assertEqual(submit_key['ILLiadForm'], 'LoanRequest')
      self.assertEqual(submit_key['LoanTitle'], 'Mahatma Gandhi : nonviolent power in action')
      ill.logout()

    def test_bookitem(self):
        ill = self.ill
        ill.login()
        openurl = 'url_ver=Z39.88-2004&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&rft.genre=bookitem&rft.btitle=Current%20Protocols%20in%20Immunology&rft.atitle=Isolation%20and%20Functional%20Analysis%20of%20Neutrophils&rft.date=2001-05-01&rft.isbn=9780471142737&rfr_id=info%3Asid%2Fwiley.com%3AOnlineLibrary'
        submit_key = ill.get_request_key( openurl )
        pprint.pprint( submit_key )
        self.assertEqual(
            'foo', 'bar' )

    def test_logout(self):
        logout = self.ill.logout()
        self.assertTrue(logout.has_key('authenticated'))
        self.assertFalse(logout['authenticated'])

def suite():
    suite = unittest.makeSuite(AccountTest, 'test')
    return suite

if __name__ == '__main__':
    unittest.main()

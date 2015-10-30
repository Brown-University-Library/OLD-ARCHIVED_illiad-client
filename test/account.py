# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os, sys, pprint, unittest


class AccountTest(unittest.TestCase):

    def setUp(self):
        self.ILLIAD_REMOTE_AUTH_URL = os.environ['ILLIAD_MODULE__TEST_REMOTE_AUTH_URL']
        self.ILLIAD_REMOTE_AUTH_KEY = os.environ['ILLIAD_MODULE__TEST_REMOTE_AUTH_KEY']
        self.ILLIAD_USERNAME = os.environ['ILLIAD_MODULE__TEST_USERNAME']
        self.PROJECT_DIR_PATH = os.environ['ILLIAD_MODULE__TEST_PATH']
        self._setup_path()
        from illiad.account import IlliadSession
        self.ill = IlliadSession(
            self.ILLIAD_REMOTE_AUTH_URL, self.ILLIAD_REMOTE_AUTH_KEY, self.ILLIAD_USERNAME )

    def tearDown(self):
        self.ill.logout()

    def _setup_path(self):
        """ Adds project dir path to sys path if necessary.
            Allows `from illiad.account...` to work
            Called by setUp() """
        if self.PROJECT_DIR_PATH not in sys.path:
            sys.path.append( self.PROJECT_DIR_PATH )
        return

    def test_login(self):
        login = self.ill.login()
        self.assertTrue(login.has_key('session_id'))
        self.assertTrue(login.has_key('authenticated'))
        self.assertTrue(login.has_key('registered'))
        self.assertTrue(login['authenticated'])

    ## submit_key tests ##

    def test_submit_key(self):
        """ Tests submit_key on article openurl. """
        ill = self.ill
        ill.login()
        #Url encoded
        openurl = "rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&rft.spage=538&rft.issue=5&rft.date=2010-02-11&rft.volume=16&url_ver=Z39.88-2004&rft.atitle=Targeting+%CE%B17+Nicotinic+Acetylcholine+Receptors+in+the+Treatment+of+Schizophrenia.&rft.jtitle=Current+pharmaceutical+design&rft.issn=1381-6128&rft.genre=article"
        submit_key = ill.get_request_key(openurl)
        self.assertEqual(submit_key['ILLiadForm'],
                        'ArticleRequest')
        self.assertEqual(submit_key['PhotoJournalTitle'],
                        'Current pharmaceutical design')

    def test_book(self):
        """ Tests submit_key on simple book openurl. """
        ill = self.ill
        ill.login()
        openurl = "sid=FirstSearch:WorldCat&genre=book&isbn=9780231122375&title=Mahatma%20Gandhi%20%3A%20nonviolent%20power%20in%20action&date=2000&rft.genre=book"
        submit_key = ill.get_request_key(openurl)
        # print 'in test_book()...'; pprint.pprint( submit_key )
        self.assertEqual( 'LoanRequest', submit_key['ILLiadForm'] )
        self.assertEqual( 'Mahatma Gandhi : nonviolent power in action', submit_key['LoanTitle'] )
        self.assertEqual( 'LoanRequest', submit_key['ILLiadForm'] )
        self.assertEqual(
            ['CitedIn', 'ILLiadForm', 'ISSN', 'LoanDate', 'LoanTitle', 'NotWantedAfter', 'SearchType', 'SessionID', 'SubmitButton', 'Username', 'blocked', 'errors'],
            sorted(submit_key.keys()) )

    def test_book_with_long_openurl(self):
        """ Tests submit_key on long book openurl. """
        ill = self.ill
        ill.login()
        openurl = 'sid=FirstSearch%3AWorldCat&genre=book&isbn=9784883195732&title=Shin+kanzen+masuta%CC%84.+Nihongo+no%CC%84ryoku+shiken&date=2011&aulast=Fukuoka&aufirst=Rieko&id=doi%3A&pid=858811926%3Cfssessid%3E0%3C%2Ffssessid%3E%3Cedition%3EShohan.%3C%2Fedition%3E&url_ver=Z39.88-2004&rfr_id=info%3Asid%2Ffirstsearch.oclc.org%3AWorldCat&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&rft.genre=book&req_dat=%3Csessionid%3E0%3C%2Fsessionid%3E&rfe_dat=%3Caccessionnumber%3E858811926%3C%2Faccessionnumber%3E&rft_id=info%3Aoclcnum%2F858811926&rft_id=urn%3AISBN%3A9784883195732&rft.aulast=Fukuoka&rft.aufirst=Rieko&rft.btitle=Shin+kanzen+masuta%CC%84.+Nihongo+no%CC%84ryoku+shiken&rft.date=2011&rft.isbn=9784883195732&rft.place=To%CC%84kyo%CC%84&rft.pub=Suri%CC%84e%CC%84+Nettowa%CC%84ku&rft.edition=Shohan.&rft.genre=book'
        submit_key = ill.get_request_key( openurl )
        # print 'in test_book_returning_no_ILLiadForm()...'; pprint.pprint( submit_key )
        self.assertEqual(
            'LoanRequest', submit_key['ILLiadForm'] )
        self.assertEqual(
            ['CitedIn', 'ESPNumber', 'ILLiadForm', 'ISSN', 'LoanAuthor', 'LoanDate', 'LoanEdition', 'LoanPlace', 'LoanPublisher', 'LoanTitle', 'NotWantedAfter', 'SearchType', 'SessionID', 'SubmitButton', 'Username', 'blocked', 'errors'],
            sorted(submit_key.keys()) )

    def test_bookitem(self):
        """ Tests submit_key on genre=bookitem openurl. """
        ill = self.ill
        ill.login()
        openurl = 'url_ver=Z39.88-2004&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&rft.genre=bookitem&rft.btitle=Current%20Protocols%20in%20Immunology&rft.atitle=Isolation%20and%20Functional%20Analysis%20of%20Neutrophils&rft.date=2001-05-01&rft.isbn=9780471142737&rfr_id=info%3Asid%2Fwiley.com%3AOnlineLibrary'
        submit_key = ill.get_request_key( openurl )
        # print 'in test...'; pprint.pprint( submit_key )
        self.assertEqual(
            'BookChapterRequest', submit_key['ILLiadForm'] )
        self.assertEqual(
            ['CitedIn', 'ILLiadForm', 'ISSN', 'NotWantedAfter', 'PhotoArticleTitle', 'PhotoJournalInclusivePages', 'PhotoJournalTitle', 'PhotoJournalYear', 'SearchType', 'SessionID', 'SubmitButton', 'Username', 'blocked', 'errors'],
            sorted(submit_key.keys()) )

    def test_tiny_openurl(self):
        """ Tests submit_key on painfully minimalist openurl. """
        ill = self.ill
        ill.login()
        openurl = 'sid=Entrez:PubMed&id=pmid:23671965'
        submit_key = ill.get_request_key( openurl )
        self.assertEqual(
            'LoanRequest', submit_key['ILLiadForm'] )
        self.assertEqual(
            ['CitedIn', 'ILLiadForm', 'LoanDate', 'LoanTitle', 'NotWantedAfter', 'Notes', 'SearchType', 'SessionID', 'SubmitButton', 'Username', 'blocked', 'errors'],
            sorted(submit_key.keys()) )
        self.assertEqual(
            'entire openurl: `sid=Entrez:PubMed&id=pmid:23671965`', submit_key['Notes'] )

    def test_logout(self):
        """ Tests logout. """
        logout = self.ill.logout()
        self.assertTrue(logout.has_key('authenticated'))
        self.assertFalse(logout['authenticated'])

def suite():
    suite = unittest.makeSuite(AccountTest, 'test')
    return suite

if __name__ == '__main__':
    unittest.main()

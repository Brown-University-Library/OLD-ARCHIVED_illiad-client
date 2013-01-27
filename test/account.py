import os
import unittest

from illiad.account import IlliadSession

#This is assuming there is a local_settings file somewhere on your path
#See a sample in local_settings.tmpl
import local_settings

class AccountTest(unittest.TestCase):
    def setUp(self):
        #Replace this username with a valid usrname for your Illiad system.
        #Need to add required init args.
        self.ill = IlliadSession(local_settings.ILLIAD_URL,
                                 local_settings.ILLIAD_REMOTE_AUTH_HEADER,
                                 local_settings.ILLIAD_USERNAME)

    def test_login(self):
        login = self.ill.login()
        self.assertTrue(login.has_key('session_id'))
        self.assertTrue(login.has_key('authenticated'))
        self.assertTrue(login.has_key('registered'))
        self.assertTrue(login['authenticated'])
        
        
    def test_submit_key(self):
       ill = self.ill
       ill.login()
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
      openurl = u"sid=FirstSearch:WorldCat&genre=book&isbn=9780231122375&title=Mahatma Gandhi : nonviolent power in action&date=2000&aulast=Dalton&aufirst=Dennis&id=doi:&pid=<accession number>46863142</accession number><fssessid>0</fssessid>&url_ver=Z39.88-2004&rfr_id=info:sid/firstsearch.oclc.org:WorldCat&rft_val_fmt=info:ofi/fmt:kev:mtx:book&req_dat=<sessionid>0</sessionid>&rfe_dat=<accessionnumber>46863142</accessionnumber>&rft_id=info:oclcnum/46863142&rft_id=urn:ISBN:9780231122375&rft.aulast=Dalton&rft.aufirst=Dennis&rft.btitle=Mahatma Gandhi : nonviolent power in action&rft.date=2000&rft.isbn=9780231122375&rft.place=New York&rft.pub=Columbia University Press&rft.genre=book"
      submit_key = ill.get_request_key(openurl)
      self.assertEqual(submit_key['ILLiadForm'], 'LoanRequest')
      self.assertEqual(submit_key['LoanTitle'], 'Mahatma Gandhi : nonviolent power in action')
      ill.logout()

    def test_logout(self):
        logout = self.ill.logout()
        self.assertTrue(logout.has_key('authenticated'))
        self.assertFalse(logout['authenticated'])

def suite():
    suite = unittest.makeSuite(AccountTest, 'test')
    return suite

if __name__ == '__main__':
    unittest.main()
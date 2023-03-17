import unittest

from .context import totp
#from apass.repo import Repo
#from apass.entry import Entry


class TestUtilsTotp(unittest.TestCase):

    def test_totp_generate_simple(self):
        """ test basics """
        key = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"
        counter = 10
        res = totp.hotp(key,counter)
        self.assertEqual("403154", res, "totp should be expected value")

    def test_totp_generate_fromUri(self):
        res = totp.fromUrl("otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example", use_time=100)
        self.assertEqual((30, 20, '143627'),res,"should calculate expected totp values")
        res = totp.fromUrl("otpauth://totp/ACME%20Co:john.doe@email.com?secret=HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ&issuer=ACME%20Co&algorithm=SHA1&digits=6&period=30", use_time=121)
        self.assertEqual((30, 29, '892599'),res,"should calculate expected totp values")

    def test_totp_invalidUri(self):
        with self.assertRaises(KeyError) as ex:
             res = totp.fromUrl("otpauth://totp/Example:alice@google.com?issuer=Example",use_time=100)
        self.assertTrue("'secret'" in str(ex.exception), "should get exception for missing secret")
        
        with self.assertRaises(KeyError) as ex:
             res = totp.fromUrl("https://a-pass.de/",use_time=100)
        self.assertTrue("'secret'" in str(ex.exception), "should get exception for missing secret")

        
if __name__ == '__main__':
    unittest.main()

import unittest
from Logica.Logica import Logica

class TestLogica(unittest.TestCase):

    def setUp(self):
        '''Crea una Logica para hacer las pruebas'''
        self.logica = Logica()
    

    def test_generarCodigoOTP(self):
        otp = self.logica.generarCodigoOTP()
        self.assertGreater(otp, 0)
    

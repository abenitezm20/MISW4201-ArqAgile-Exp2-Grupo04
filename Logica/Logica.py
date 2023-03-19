

from modelos import Usuario
from faker import Faker


data_factory = Faker()

class Logica():

    @staticmethod          
    def generarCodigoOTP():
        otp = 0
        try:
            otp = data_factory.random_int(0, 999999)
            print("El codigo OTP es: " + str(otp))
            return otp
        except ValueError:
            return otp
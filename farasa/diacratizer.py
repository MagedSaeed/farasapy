from .__base import FarasaBase

class FarasaDiacritizer(FarasaBase):

    task = 'diacritize'

    def diacritize(self,text):
        return self._do_task(text=text)
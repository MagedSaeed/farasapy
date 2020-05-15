from .base import FarasaBase

class FarasaPOSTagger(FarasaBase):

    task = 'POS'

    def tag(self,text):
        return self._do_task(text=text)
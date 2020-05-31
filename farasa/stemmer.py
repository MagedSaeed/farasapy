from .__base import FarasaBase


class FarasaStemmer(FarasaBase):
    task = 'stem'

    def stem(self, text):
        return self._do_task(text=text)

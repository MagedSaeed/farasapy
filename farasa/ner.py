from .__base import FarasaBase


class FarasaNamedEntityRecognizer(FarasaBase):
    task = "NER"

    def recognize(self, text):
        return self._do_task(text=text)

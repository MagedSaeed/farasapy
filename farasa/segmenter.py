from .base import FarasaBase

class FarasaSegmenter(FarasaBase):

    task = 'segment'
    
    def segment(self, text):
        return self._do_task(text=text)
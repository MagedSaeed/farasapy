from .__base import FarasaBase


class FarasaSegmenter(FarasaBase):
    task = "segment"

    def segment(self, text):
        return self._do_task(text=text)

    def _desegment_word(self, word: str) -> str:
        desegmented_word = word.replace("ل+ال+", "لل")
        if "ال+ال" not in word:
            desegmented_word = desegmented_word.replace("ل+ال", "لل")
        desegmented_word = desegmented_word.replace("+", "")
        desegmented_word = desegmented_word.replace("للل", "لل")
        return desegmented_word

    def desegment(self, text, separator=" "):
        return " ".join(self._desegment_word(word) for word in text.split(separator))

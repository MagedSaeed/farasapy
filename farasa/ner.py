from .__base import FarasaBase


class FarasaNamedEntityRecognizer(FarasaBase):
    task = "NER"

    @property
    def command(self):
        return self.BASE_CMD + [str(self.bin_dir / "FarasaNERJar.jar")]

    def recognize(self, text):
        return self._do_task(text=text)

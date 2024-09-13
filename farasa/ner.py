from .__base import FarasaBase


class FarasaNamedEntityRecognizer(FarasaBase):
    task = "NER"

    @property
    def command(self):
        if self.bin_path is not None:
            return self.BASE_CMD + [str(self.bin_path)]
        return self.BASE_CMD + [str(self.bin_dir / "FarasaNERJar.jar")]

    def recognize(self, text):
        return self.do_task(text=text)

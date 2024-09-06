from .__base import FarasaBase


class FarasaDiacritizer(FarasaBase):
    task = "diacritize"

    @property
    def command(self):
        return self.BASE_CMD + [str(self.bin_dir / "FarasaDiacritizeJar.jar")]

    def diacritize(self, text):
        return self._do_task(text=text)

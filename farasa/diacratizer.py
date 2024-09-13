from .__base import FarasaBase


class FarasaDiacritizer(FarasaBase):
    task = "diacritize"

    @property
    def command(self):
        if self.bin_path is not None:
            return self.BASE_CMD + [str(self.bin_path)]
        return self.BASE_CMD + [str(self.bin_dir / "FarasaDiacritizeJar.jar")]

    def diacritize(self, text):
        return self.do_task(text=text)

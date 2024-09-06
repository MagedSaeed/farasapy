from .__base import FarasaBase


class FarasaStemmer(FarasaBase):
    task = "stem"

    @property
    def command(self):
        return self.BASE_CMD + [
            str(self.bin_lib_dir / "FarasaSegmenterJar.jar"),
            "-l",
            "true",
        ]

    def stem(self, text):
        return self._do_task(text=text)

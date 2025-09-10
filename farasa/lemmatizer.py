from .__base import FarasaBase


class FarasaLemmatizer(FarasaBase):
    task = "lemmatize"
    is_downloadable = False

    def __init__(self, interactive=False, logging_level="WARNING", binary_path=None):
        super().__init__(interactive, logging_level, binary_path)

    @property
    def command(self):
        if self.bin_path is not None:
            return self.BASE_CMD + [str(self.bin_path)]
        raise Exception("Binary path for lemmatizer is not provided.")

    def lemmatize(self, text):
        return self.do_task(text=text) 
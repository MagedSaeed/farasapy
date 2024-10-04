from .__base import FarasaBase


class FarasaSpellChecker(FarasaBase):
    task = "spell_check"

    @property
    def command(self):
        assert (
            not self.interactive
        ), "ERROR: Interactive mode is not supported for FarasaSpellCheck. Kindly use standalone mode."
        assert (
            self.bin_path is not None
        ), "The FarasaSpellCheck jar file is not downloadable by farasapy. Please download it from qcri first then add its path as 'binary_path=<path_to_jar>' when creating the Spellchecker object."
        if self.bin_path is not None:
            return self.BASE_CMD + [str(self.bin_path)]
        return self.BASE_CMD + [str(self.bin_dir / "FarasaSpellCheck.jar")]

    def spell_check(self, text):
        return self.do_task(text=text)

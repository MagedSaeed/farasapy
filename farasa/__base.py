import io
import logging
import os
import re
import subprocess
import sys
import tempfile
import warnings
import zipfile
from pathlib import Path

import requests
from tqdm import tqdm


class FarasaBase:
    task = None
    base_dir = Path(__file__).parent.absolute()
    bin_dir = Path(f"{base_dir}/farasa_bin")
    bin_lib_dir = Path(f"{bin_dir}/lib")

    # shlex not compatible with Windows replace it with list()
    # set java encoding with option `-Dfile.encoding=UTF-8`
    BASE_CMD = ["java", "-Dfile.encoding=UTF-8", "-jar"]
    # __APIs = {
    # "segment": __BASE_CMD + [str(__bin_lib_dir / "FarasaSegmenterJar.jar")],
    # "stem": __BASE_CMD
    # + [str(__bin_lib_dir / "FarasaSegmenterJar.jar"), "-l", "true"],
    # "NER": __BASE_CMD + [str(__bin_dir / "FarasaNERJar.jar")],
    # "POS": __BASE_CMD + [str(__bin_dir / "FarasaPOSJar.jar")],
    # "diacritize": __BASE_CMD + [str(__bin_dir / "FarasaDiacritizeJar.jar")],
    # }
    interactive = False
    task_proc = None
    logger = None

    @property
    def command(self):
        """
        This function should return the CMD command to be executed for the task.
        """
        raise NotImplemented

    def __init__(self, interactive=False, logging_level="WARNING"):
        self._config_logs(logging_level)
        self.logger.debug("perform system check...")
        self.logger.debug("check java version...")
        self.check_java_version()
        self.logger.debug("check toolkit binaries...")
        self._check_toolkit_binaries()
        Path(f"{self.base_dir}/tmp").mkdir(exist_ok=True)
        self.logger.info("Dependencies seem to be satisfied..")
        if interactive:
            self.interactive = True
            self.logger.warning(
                "Be careful with large lines as they may break on interactive mode. You may switch to Standalone mode for such cases."
            )
            self.logger.info(
                f"\033[37minitializing [{self.task.upper()}] task in \033[32mINTERACTIVE \033[37mmode..."
            )
            self.initialize_task()
            self.logger.info(
                f"task [{self.task.upper()}] is initialized interactively."
            )
        else:
            self.logger.info(
                f"task [{self.task.upper()}] is initialized in \033[34mSTANDALONE \033[37mmode..."
            )

    def _config_logs(self, logging_level):
        self.logger = logging.getLogger("farasapy_logger")
        self.logger.propagate = False
        self.logger.setLevel(getattr(logging, logging_level.upper()))
        logs_formatter = logging.Formatter(
            "[%(asctime)s - %(name)s - %(levelname)s]: %(message)s"
        )
        if not self.logger.hasHandlers():
            stream_logger = logging.StreamHandler()
            stream_logger.setFormatter(logs_formatter)
            self.logger.addHandler(stream_logger)

    def _check_toolkit_binaries(self):
        download = False
        # check in bin folder:
        for jar in ("FarasaNERJar", "FarasaPOSJar", "FarasaDiacritizeJar"):
            if not Path(f"{self.bin_dir}/{jar}.jar").is_file():
                download = True
                break

        if (
            download or not Path(f"{self.bin_lib_dir}/FarasaSegmenterJar.jar").is_file()
        ):  # last check for binaries in farasa_bin/lib
            self.logger.info("some binaries are not existed.")
            self._download_binaries()

    def _get_content_with_progressbar(self, request):
        totalsize = int(request.headers.get("content-length", 0))
        blocksize = 3413334
        bar = tqdm(
            total=totalsize,
            unit="iB",
            unit_scale=True,
            ncols=5,
            dynamic_ncols=True,
            file=sys.stdout,
        )
        content = None
        for data in request.iter_content(blocksize):
            bar.update(len(data))
            if content is None:
                content = data
            else:
                content += data
        return content

    def _download_binaries(self):
        self.logger.info("downloading zipped binaries...")
        try:
            # change download url from github releases to qcri
            # binaries_url = "https://github.com/MagedSaeed/farasapy/releases/download/toolkit-bins-released/farasa_bin.zip"
            binaries_url = "https://farasa-api.qcri.org/farasapy/releases/download/toolkit-bins-released/farasa_bin.zip"
            binaries_request = requests.get(binaries_url, stream=True, verify=False)
            # show the progress bar while getting content
            content_bytes = self._get_content_with_progressbar(binaries_request)
            self.logger.debug("extracting...")
            binzip = zipfile.ZipFile(io.BytesIO(content_bytes))
            binzip.extractall(path=self.base_dir)
            self.logger.debug("toolkit binaries are downloaded and extracted.")
        except Exception as e:
            self.logger.error("an error occured")
            self.logger.error(e)

    def initialize_task_proc(self):
        self.task_proc = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def initialize_task(self):
        word = "اختبار"
        word += "\n"
        bword = str.encode(word)
        self.initialize_task_proc()
        return self.run_task_interactive(bword)

    def check_java_version(self):
        try:
            version_proc_output = subprocess.check_output(
                ["java", "-version"], stderr=subprocess.STDOUT, encoding="utf8"
            )
            # version_pattern = r"\"(\d+\.\d+).*\""
            version_pattern = r"\"(\d+(\.\d+){0,1})"
            java_version = float(
                re.search(version_pattern, version_proc_output).groups()[0]
            )
            if java_version >= 1.7:
                self.logger.debug(
                    f"Your java version is {java_version} which is compatible with Farasa "
                )
            else:
                warnings.warn(
                    "You are using old version of java. Farasa is compatible with Java 7 and above "
                )
        except subprocess.CalledProcessError as proc_err:
            self.logger.error(f"error occurred: {proc_err}.")
            raise Exception(
                "We could not check for java version on the machine. Please make sure you have installed Java 1.7+ and add it to your PATH."
            )

    def run_task(self, btext):
        assert btext is not None
        tmpdir = str(self.base_dir / "tmp")
        # if delete=True on Windows cannot get any content
        # https://docs.python.org/3/library/tempfile.html#tempfile.NamedTemporaryFile
        itmp = tempfile.NamedTemporaryFile(dir=tmpdir, delete=False)
        otmp = tempfile.NamedTemporaryFile(dir=tmpdir, delete=False)
        try:
            itmp.write(btext)
            # https://stackoverflow.com/questions/46004774/python-namedtemporaryfile-appears-empty-even-after-data-is-written
            itmp.flush()
            proc = subprocess.run(
                self.command + ["-i", itmp.name, "-o", otmp.name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                # this only compatiple with python>3.6
                # capture_output=True,
            )
            if proc.returncode == 0:
                result = otmp.read().decode("utf8").strip()
            else:
                self.logger.critical(
                    f"error occurred! stdout: , {proc.stdout},  stderr: , {proc.stderr}"
                )
                self.logger.critical(f"return code: {proc.returncode}")
                raise Exception("Internal Error occurred!")
        finally:
            itmp.close()
            otmp.close()
            os.unlink(itmp.name)
            os.unlink(otmp.name)
        return result

    def run_task_interactive(self, btext):
        assert isinstance(btext, bytes)
        assert self.interactive
        try:
            self.task_proc.stdin.flush()
            self.task_proc.stdin.write(btext)
            self.task_proc.stdin.flush()
        except BrokenPipeError as broken_pipe:
            self.logger.error(
                f"pipe broke! error code and message: [{broken_pipe}]. reinitialize the process.., This may take sometime depending on the running task"
            )
            self.initialize_task_proc()
            self.task_proc.stdin.flush()
            self.task_proc.stdin.write(btext)
            self.task_proc.stdin.flush()

        output = self.task_proc.stdout.readline().decode("utf8").strip()
        self.task_proc.stdout.flush()
        return output

    def do_task_interactive(self, strip_text):
        outputs = []
        for line in strip_text.split("\n"):
            newlined_line = line + "\n"
            byted_newlined_line = str.encode(newlined_line)
            output = self.run_task_interactive(byted_newlined_line)
            if output:
                outputs.append(output)
        return "\n".join(outputs)

    def do_task_standalone(self, strip_text):
        byted_strip_text = str.encode(strip_text)
        return self.run_task(btext=byted_strip_text)

    def _do_task(self, text):
        strip_text = text.strip()
        if self.interactive:
            return self.do_task_interactive(strip_text)
        else:
            return self.do_task_standalone(strip_text)

    def terminate(self):
        self.task_proc.terminate()

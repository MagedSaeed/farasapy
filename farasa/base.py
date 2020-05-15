import os
import sys
import subprocess
import shlex
import warnings
import time
import re
import tempfile

class FarasaBase:
    task = None
    __APIs = {
        'segment':shlex.split('java -jar farasa/farasa_bin/lib/FarasaSegmenterJar.jar'),
        'stem' : shlex.split('java -jar farasa/farasa_bin/lib/FarasaSegmenterJar.jar -l true'),
        'NER' : shlex.split('java -jar farasa/farasa_bin/FarasaNERJar.jar'),
        'POS' : shlex.split('java -jar farasa/farasa_bin/FarasaPOSJar.jar'),
        'diacritize' : shlex.split('java -jar farasa/farasa_bin/FarasaDiacritizeJar.jar'),
    }
    __interactive = False
    __task_proc = None

    def __init__(self, interactive=False):
        print("perform system check...")
        self._check_java_version()
        if interactive:
            self.__interactive = True
            print(f"\033[37minitializing [{self.task.upper()}] task in \033[32mINTERACTIVE \033[37mmode...")
            self._initialize_task()
            print(f"task [{self.task.upper()}] is initialized interactively.")
        else:
            print(f"task [{self.task.upper()}] is initialized in \033[34mSTANDALONE \033[37mmode...")
            

    def _initialize_task(self):
        word = 'اختبار'
        word+='\n'
        bword = str.encode(word)
        self.__task_proc = subprocess.Popen(self.__APIs[self.task],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        return self._run_task_interactive(bword)

            

    def _check_java_version(self):
        try:
            version_proc_output = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT,encoding='utf8',text=True)
            version_pattern = r'\"(\d+\.\d+).*\"'
            java_version = float(re.search(version_pattern,version_proc_output).groups()[0])
            if java_version >= 1.7:
                print(f"Your java version is {java_version} which is compatiple with Farasa ")
            else:
                warnings.warn('You are using old version of java. Farasa is compatiple with Java 7 and above ')
        except subprocess.CalledProcessError as proc_err:
            print(proc_err)
            raise Exception("We could not check for java version on the machine. Please make sure you have installed Java 1.7+ and add it to your PATH.")


    def _run_task(self, btext):
        assert btext is not None
        with tempfile.NamedTemporaryFile(dir='farasa/tmp',) as itmp,\
                    tempfile.NamedTemporaryFile(dir='farasa/tmp',) as otmp:
            itmp.write(btext)
            itmp.flush() # https://stackoverflow.com/questions/46004774/python-namedtemporaryfile-appears-empty-even-after-data-is-written
            proc = subprocess.run(self.__APIs[self.task]+['-i',itmp.name,'-o',otmp.name],\
                                    capture_output=True)
            if proc.returncode == 0:
                return otmp.read().decode('utf8').strip()
            else:
                print("error occured!",otmp.read().decode('utf8').strip())
                print("return code:",proc.returncode)
                raise Exception('Internal Error occured!')

    
    def _run_task_interactive(self, btext):
        assert btext is not None and type(btext) == bytes
        assert self.__interactive == True 
        assert self.__task_proc is not None
        self.__task_proc.stdin.flush()
        self.__task_proc.stdin.write(btext)
        self.__task_proc.stdin.flush()
        output = self.__task_proc.stdout.readline().decode('utf8').strip()
        self.__task_proc.stdout.flush()
        return output
    
    def _do_task_interactive(self, strip_text):
        outputs = []
        for line in strip_text.split('\n'):
            newlined_line = line+'\n'
            byted_newlined_line = str.encode(newlined_line)
            output = self._run_task_interactive(byted_newlined_line)
            if output:
                outputs.append(output)
        return '\n'.join(outputs)
    
    def _do_task_standalone(self,strip_text):
        byted_strip_text = str.encode(strip_text)    
        return self._run_task(btext=byted_strip_text)

    def _do_task(self, text):
        strip_text = text.strip()
        if self.__interactive:
            return self._do_task_interactive(strip_text)        
        else:
            return self._do_task_standalone(strip_text)

    def terminate(self):
        self.__task_proc.terminate()
    

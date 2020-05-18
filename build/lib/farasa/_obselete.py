import os
import subprocess
import shlex
import warnings
import time
import re
import tempfile

class Farasa():
    temp_filename_in = f'.farasa.{time.time()}.in.temp'
    temp_filename_out = f'.farasa.{time.time()}.out.temp'
    interactive = None # either None or 'interactive'
    APIs_map = {
        'segment':shlex.split('java -jar ./farasa/FarasaSegmenterJar/FarasaSegmenterJar.jar'),
        'stem' : shlex.split('java -jar ./farasa/FarasaSegmenterJar/FarasaSegmenterJar.jar -l true'),
    }
    tasks = list(APIs_map.keys())
    task_proc = None

    def __init__(self, interactive_task=None):
        print("perform system check...")
        self._check_java_version()
        if interactive_task:
            if interactive_task not in self.tasks:
                raise Exception(f"task can only be one of [{', '.join(t for t in self.tasks)}]")
            self.task = interactive_task
            print(f"initialize {self.task} in interactive mode...")
            self.task_proc = subprocess.Popen(self.APIs_map[self.task],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
            


    def _check_java_version(self):
        try:
            version_proc = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT,encoding='utf8',text=True)
            version_pattern = r'\"(\d+\.\d+).*\"'
            java_version = float(re.search(version_pattern,version_proc).groups()[0])
            if java_version >= 1.7:
                print(f"Your java version is {java_version} which is compatiple with Farasa ")
            else:
                warnings.warn('You are using old version of java. Farasa is compatiple with Java 7 and above ')
        except subprocess.CalledProcessError as proc_err:
            print(proc_err)
            raise Exception("We could not check for java version on the machine. Please make sure you have installed Java 1.7+ and add it to your PATH.")

    
    def _write_to_temp_file(self, text):
        assert text
        with open(self.temp_filename_in,'w',encoding='utf-8') as tmp:
            tmp.write(text)


    def _read_from_temp_file(self):
        return open(self.temp_filename_out, 'r',encoding='utf-8').read()

    def _run_non_interactive(self,api, text):
        assert api
        assert text
        self._write_to_temp_file(text)
        proc = subprocess.run(self.APIs_map[api]+['-i',self.temp_filename_in,'-o',self.temp_filename_out],capture_output=True)
        return True if proc.returncode == 0 else False
    
    def _run_interactive(self, text):
        assert text
        assert self.interactive
        assert self.task_proc
        text+='\n'
        self.task_proc.stdin.write(str.encode(text))
        self.task_proc.stdin.flush()
        return self.task_proc.stdout.readline().decode('utf8').strip()
    
    def _do_task(self, task=None, text=None):
        if self.interactive:
            if self.task==task:
                return self._run_interactive(text)
            else:
                raise Exception("You initialized the interactive object with {self.task} task and you are asking for another task. You may create another object with {task} task.")
        
        if self._run_non_interactive(api=task, text=text):
            return self._read_from_temp_file()
        raise Exception('Internal Error occured!')

    def segment(self, text):
        return self._do_task(task='segment',text=text)

    def stem(self, text):
        return self._do_task(task='stem',text=text)

    def diacratize(self):
        pass

    def POSify(self):
        pass

    def terminate_task(self):
        self.task_proc.terminate()
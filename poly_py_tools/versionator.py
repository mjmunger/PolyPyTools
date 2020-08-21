import subprocess
import os


class Versionator(object):

    @staticmethod
    def version():
        execution_dir = os.getcwd()
        working_dir = os.path.dirname(os.readlink("/usr/local/bin/polypy")) if os.path.exists(
            "/usr/local/bin/polypy") else os.getcwd()
        os.chdir(working_dir)
        proc = subprocess.Popen(['git', 'describe', '--tags', '--long'], 1024, stdout=subprocess.PIPE)
        try:
            outs, errs = proc.communicate(1)
        except subprocess.TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate(1)
        program_version = outs.decode("utf-8").strip()
        return program_version

    @staticmethod
    def show_version():
        print("polypy version: {}".format(Versionator.version()))

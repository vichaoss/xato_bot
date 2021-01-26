import os
import signal
import subprocess
import sys
from configs.settings import Settings


class DaemonManager:

    @staticmethod
    def run_daemon():
        pid_prev_daemon = DaemonManager.read_temp_file()
        if pid_prev_daemon is not None:
            print("Ya hay un demonio en ejecución")
            return
        new_daemon = subprocess.Popen(
            "pythonw " + os.path.join(Settings.sources_folder_path, "principal.py"),
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        DaemonManager.generate_temp_file(new_daemon.pid)
        return

    @staticmethod
    def generate_temp_file(daemon_pid):
        temp_file = open("pid.tmp", "w")
        temp_file.write(str(daemon_pid))
        temp_file.close()
        return

    @staticmethod
    def kill_daemon():
        pid_to_kill = DaemonManager.read_and_flush_temp_file()
        if pid_to_kill is None:
            print("No hay un demonio por matar")
            return
        os.kill(pid_to_kill, signal.SIGTERM)
        return

    @staticmethod
    def read_temp_file():
        try:
            temp_file = open("pid.tmp", "r")
        except FileNotFoundError:
            return None
        try:
            pid = int(temp_file.readline().strip())
            temp_file.close()
            return pid
        except ValueError:
            return None
        pass

    @staticmethod
    def read_and_flush_temp_file():
        try:
            temp_file = open("pid.tmp", "r")
        except FileNotFoundError:
            return None
        try:
            pid = int(temp_file.readline().strip())
            temp_file.close()
            temp_file = open("pid.tmp", "w")
            temp_file.close()
            return pid
        except ValueError:
            return None
        pass

    pass


arg_count = len(sys.argv)

# arg_count = 2
# sys.argv = ["daemon.py", "kill"]

if arg_count == 2 and sys.argv[1] == "kill":
    DaemonManager.kill_daemon()
    exit(0)

DaemonManager.run_daemon()

import os
import subprocess
import sys
from configs.settings import Settings

arg_count = len(sys.argv)


class DaemonManager:
    pid_last_daemon = None

    @staticmethod
    def run_daemon():
        new_daemon = subprocess.Popen(
            "python " + os.path.join(Settings.sources_folder_path, "principal.py"),
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
        pid_to_kill = int(DaemonManager.read_temp_file())
        print(pid_to_kill)
        if pid_to_kill is None:
            print("No hay un demonio por matar")
            return
        os.kill(pid_to_kill, 1)
        return

    @staticmethod
    def read_temp_file():
        try:
            temp_file = open("pid.tmp", "r")
        except FileNotFoundError as e:
            print(e)
            return None
        try:
            return int(temp_file.readline().strip())
        except ValueError as e:
            print(e)
            return None
        pass

    pass


if arg_count == 2 and sys.argv[1] == "kill":
    DaemonManager.kill_daemon()
    exit(1)

DaemonManager.run_daemon()

import subprocess
import os

print(os.path.join("\\Applications", "VLC media player.app"))
subprocess.Popen(["open", "-n", os.path.join("\Applications", "VLC media player.app")], stdout=subprocess.PIPE)

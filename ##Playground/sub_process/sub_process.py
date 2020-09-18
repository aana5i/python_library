# subprocess => run command
import subprocess
import time


# shell=True is not secured
# subprocess.run("dir/s", shell=True)

# /s is the current folder where the py script is used
p1 = subprocess.run(["cmd", "/c", "dir", "/s"])

print(p1.args)  # print the passed args
print(p1.returncode)  # 0 = success


p2 = subprocess.run(["cmd", "/c", "dir", "/s"], capture_output=True)
print(p2.stdout)  #  need to add the capture_output | this command capture the result and print it
# with capture_output the result is not printed by default anymore
# its a Byte type


# here is what capture_true do
p3 = subprocess.run(["cmd", "/c", "dir", "/s"], stdout=subprocess.PIPE)
print(p3.stdout)


with open('output.txt', 'w') as f:
    subprocess.run(["cmd", "/c", "dir", "/s"], stdout=f, text=True)


proc = subprocess.Popen(["calc.exe"], stdout=subprocess.PIPE)
out = proc.communicate()[0]
pid = proc.pid
print(pid)
time.sleep(2.0)
proc.kill()

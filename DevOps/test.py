import subprocess, os, time, signal

p = subprocess.run('calc.exe')
print(p)

# Some actions
time.sleep(2)
CREATE_NO_WINDOW = 0x08000000
subprocess.call('taskkill /F /IM Calculator.exe')

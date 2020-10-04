import subprocess

sound_program = "C:/Program Files/Windows Media Player/wmplayer.exe"
sound_file = 'C:/Users/Nitze/Videos/sample_video.mp4'

# subprocess.call('python printer.py -p risa')
subprocess.call([sound_program, sound_file])
# subprocess.run('python printer.py -p risa')

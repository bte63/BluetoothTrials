from subprocess import Popen, PIPE, CalledProcessError

cmd = ["bluetoothctl", "scan", "on"]

with Popen(cmd, stdout=PIPE, universal_newlines=True) as p:
    
    for line in p.stdout:
        print(line, flush=True)
    
    if p.returncode != 0:
        raise CalledProcessError(p.returncode, p.args)
    
    
    
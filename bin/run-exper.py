import os
import signal
import sys
import time
import subprocess

user = 'yangzhou'
# the first host is the localhost
hosts = list(map(lambda x: f'apt{x}.apt.emulab.net', [137, 141, 147]))

Cmds = {
	'sync': 'cd ~/ccKVS/bin && ./copy-ccKVS-executables.sh',
	'run_local': 'cd ~/ccKVS/src/ccKVS && unbuffer ./run-ccKVS.sh &> log/{host}.log',
	# &> just does not work
	'run_remote': 'ssh -o StrictHostKeyChecking=no {user}@{host} "cd ~/ccKVS/src/ccKVS && unbuffer ./run-ccKVS.sh" > log/{host}.log 2> /dev/null',
    'kill': 'ssh -o StrictHostKeyChecking=no {user}@{host} "sudo pkill ccKVS"',
}

def signal_handler(sig, frame):
	print('kill all servers and clients')
	for h in hosts:
		print(f'kill {h}')
		ret = os.popen(Cmds['kill'].format(user=user, host=h)).read()
	sys.exit(0)

# non-blocking or blocking actually depends on whether cmd is bg or fg
def blocking_run(cmd):
    ret = subprocess.check_output(['/bin/bash', '-c', cmd])	
	return ret

# always non-blocking, as it is running in a subprocess. 
def non_blocking_run(cmd):
    subprocess.Popen(['/bin/bash', '-c', cmd])

if __name__ == "__main__":	
	signal.signal(signal.SIGINT, signal_handler)
	
	print(f'syncing')
	# blocking, as Cmds['sync'] is set to run in foreground
	ret = blocking_run(Cmds['sync'])
	print(ret)

	non_blocking_run(Cmds['run_local'].format(host=hosts[0]))

	print("waiting 2 seconds")
	time.sleep(2)

	for i, h in enumerate(hosts[1:]):
		non_blocking_run(Cmds['run_remote'].format(user=user, host=h))

	print("waiting for ctrl+c")
	signal.pause()
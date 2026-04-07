import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()

    # optional: load known hosts
    #client.load_host_keys('/home/justin/.ssh/known_hosts')

    client.set_missing_host_key_policy(paramiko.AutoAddPol>

    client.connect(ip, username=user, password=passwd)

    ssh_session = client.get_transport().open_session()
   
    if ssh_session.active:
        ssh_session.exec_command(command)
    
        # In python3, recv() returns bytes - decode to str>
        output = ssh_sessionh.recv(1024).decode('utf-8')
        print(output)
    
    client.close()
    return

ssh_command('192.168.100.131', 'justin', 'lovestheoython', 'id')

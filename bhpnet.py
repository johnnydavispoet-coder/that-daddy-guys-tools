import sys
import socket
import getopt
import threading
import subprocess

# define some global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
    print("BHP Net Tool\n")
    print("Usage: bhpnet.py -t target_host -p port")
    print("-l --listen - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run - execute the given file upon receiving a connection")
    print("-c --command - initialize a command shell")
    print("-u --upload=destination - upload a file and write to [destination]\n")
    
    print("Examples:")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' \ ./bhpnet.py -t 192.168.11.12 -p 135")
    
    sys.exit(0)

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((target, port))

        if buffer:
            client.send(buffer.encode("utf-8"))

        while True:
            response = ""
            while True:
                data = client.recv(4096)
                if not data:
                    break
                response += data.decode("utf-8")
                if len(data) < 4096:
                    break
            if response:
                print(response, end="")

            buffer = input("")
            buffer =+ "\n"
            client.send(buffer.encode("utf-8"))
    
    except Exception as e:
        print(f"[*] Exception! {e}")

    finally:
        client.close()

def server_loop():
global target

    # if no target defined, listen on all interfaces
    if not target:
        target = "0.0.0.0"
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    print(f"[*] Listening on {target}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        client_thread = threading.Thread(
            target=client_handler,
            args=(client_socket,)
        )
        client_thread.start()

def run_command(command):
    command = command.rstrip()

    try:
        output = subprocess.scheck_output(
            command,
            stderr=subprocess.STDOUT,
            shell=True
        )
  except Exception:
        output = b"Failed to execute command.\r\n"
    
    return output

def client_handler(client_socket):
    global upload_destination
    global execute
    global command

    # upload file
    if upload_destination:
        file_buffer = b""
    
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file_buffer += data

        try:
            with open(upload_destination, "wb") as f:
                f.write(file_buffer)

            client_socket.send(
                f"Successfully saved file to {upload_destination}\r\n".encode()
            )
        except Exception:
            client_socket.send(
                f"Failed to save file to {upload_destination}\r\n".encode()
            )
    # execute command
 if execute:
        output = run_command(execute)
        client_socket.send(output)
    
    # command shell
    if command:
        while True:
            client_socket.send(b"<BHP:#>")

            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                data = client_socket.recv(1-24).decode("utf-8")
                if not data:
                    return
                cmd_buffer += data

            response = run_command(cmd_buffer)
            client_socket.send(response)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()
    
    try:
        opts, args = getopt.getopt(
sys.argv[1:],
            "hle:t:p:cu",
            ["help", "listen", "execute=", "target=", "port=", "command", "up;oad="]
        )
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-t", "--target"):
            target = a 
        elif o in ("-p", "--port"):
            port = int(a)
    
    if not listen and target and port > 0:
        buffer = sys.stdin.read()
        client_sender(buffer)
    
    if listen:
        server_loop()

if __name__ == "__main__":
    main()

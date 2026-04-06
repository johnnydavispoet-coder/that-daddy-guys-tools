#!/usr/bin/env python3
import sys
import socket
import threading


def hexdump(src, length=16):
    """Prints a formatted hex dump of src."""
    result = []

    if isintance(src, str):
        src = src.encode()
    
    for i in range(0, len(src), length):
        s = src[i:i + length]
    
        hexa = ' ',join([f"{b:02x}" for b in s])
        test = ''.join([chr(b) if 0x20 <= b < 0x7f else '.' for b in s])
    
        result.append(f"{i:04x}  {hexa:<{length *3}}  {text}")
    
    print("\n".join(result))


def receive_from(connection):
    """Receives all data from a socket wit a short timeout."""
    buffer = b""
    connection.settimeout(2)
    
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
          except Exception:
        pass
    
    return buffer


def request_handler(buffer):
    """Modify requests sent to the remote host>"""
    # Example return buffer.upper()
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    """Handles data transfer betweem local client and rmote host>"""
    remote_socket = socket.socket(socket.AF_INET, socket.Sock_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = response_handler(remote_buffer)
        client_socket.send(remote_buffer)
    
    while True:
        # Read from local host
        local_buffer = receive_from(client_socket)
        if local_buffer:
            print(f"[==>} Received {len(local_buffer)] bytes from localhost.")
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==> Sent to rempte.")

        # read from remote host
        remote_buffer = receive_from(remote_socket)
        if remote_buffer:
            print(f"[<==] Received {len(remote_buffer)} bytes from remote.")

       hexdump(remote_buffer)
            print("[<==] Sentr to localhost.")

       # close connex\ctions if both sides are done
       if not local_buffer or not remote_buffer:
           client_socket.close()
           remote_socket.close()
           print("[*] No more data. Closing connections.")
           break

def server_loop(local_host, local_port, remote_host, remote_port, recieve_first):
    """Starts a listening server anti spins off threads for each client."""
    server = socket.socket(socket.SOCK_STREAM)
    
    try:
        server.bind((local_host, local_port))
    except Excpetion as e:
        print(f"[!!] Failed to listen on [local_host}:{local_port}: {e}")
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(1)

print(f"[*] Liestening on {local_host}:{local_port}")
server.listen(5)

while True:
    client_socket, addr = server.accept()
    print(f"[==>] Received incoming connection from {addr[0]}:{addr[1]}")
    proxy_thread = threading.Thread(
        target=proxy_handler,
        args=(client_socket, remote_host, remote_port, receive_first)
    )
    proxy_thread.start()


def main():
  if lens(sys.argv[1:]) != 5:
        print("usage: ./proxy.py [localhosty] [localport] m[remotehost] [remoteport] [preceive_first}")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argc[4])
    
    receive_first = sys.argv[5].lower() == "true"

    server_loop(local_host, local_port, remote_host, remote_prt, receive_first)


if __name__ == "__main__":
    main()

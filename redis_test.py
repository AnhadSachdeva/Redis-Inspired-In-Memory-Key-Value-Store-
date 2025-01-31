# import socket
# import time

# def send_command(sock, command):
#     print(f"Sending: {command}")
#     sock.sendall(f"{command}\r\n".encode())
#     # Wait for the response
#     time.sleep(0.5)
#     response = sock.recv(4096).decode().strip()
#     print(f"Received: {response}")
#     return response

# def main():
#     host, port = 'localhost', 1234
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.connect((host, port))

#     try:
#         # Test SET command
#         response = send_command(sock, "set key1 hello")
#         assert response == 'OK', "SET command did not return OK"

#         # Test GET command
#         response = send_command(sock, "get key1")
#         assert response == 'hello', "GET command did not return 'hello'"

#         # Test DEL command
#         response = send_command(sock, "del key1")
#         assert response == '1', "DEL command did not return '1'"

#         # Test GET for non-existing key (after deletion)
#         response = send_command(sock, "get key1")
#         assert response == '(nil)', "GET command for deleted key did not return '(nil)'"

#     finally:
#         sock.close()

# if __name__ == '__main__':
#     main()

import socket
import struct

def send_request(sock, *args):
    try:
        print(f"\nSending command: {args}")
        
        # First create the command portion
        cmd = struct.pack('<I', len(args))  # Number of arguments
        for arg in args:
            arg_bytes = arg.encode('utf-8')
            cmd += struct.pack('<I', len(arg_bytes))  # Length of argument
            cmd += arg_bytes  # Argument data
        
        # Now send the total message length first
        msg_len = struct.pack('<I', len(cmd))
        sock.sendall(msg_len + cmd)
        print(f"Sent message length: {len(cmd)}, total bytes: {len(msg_len) + len(cmd)}")
        
        # Read response length
        resp_len_bytes = sock.recv(4)
        if not resp_len_bytes:
            print("Error: No response length received")
            return None
            
        resp_len = struct.unpack('<I', resp_len_bytes)[0]
        print(f"Response length: {resp_len}")
        
        # Read response data
        resp_data = sock.recv(resp_len)
        if not resp_data:
            print("Error: No response data received")
            return None
            
        resp_type = resp_data[0]
        print(f"Response type: {resp_type}")
        
        if resp_type == 0:    # SER_NIL
            return None
        elif resp_type == 1:  # SER_ERR
            code = struct.unpack('<I', resp_data[1:5])[0]
            length = struct.unpack('<I', resp_data[5:9])[0]
            msg = resp_data[9:9+length].decode('utf-8')
            return f"ERR {code}: {msg}"
        elif resp_type == 2:  # SER_STR
            length = struct.unpack('<I', resp_data[1:5])[0]
            return resp_data[5:5+length].decode('utf-8')
        elif resp_type == 3:  # SER_INT
            return struct.unpack('<q', resp_data[1:9])[0]
        elif resp_type == 4:  # SER_DBL
            return struct.unpack('<d', resp_data[1:9])[0]
        
        print(f"Unknown response type: {resp_type}")
        return None
        
    except Exception as e:
        print(f"Error in send_request: {e}")
        return None

def main():
    try:
        host = 'localhost'
        port = 1234
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            print("Connected to server successfully.")
            
            # Test SET command
            print("\nTesting SET command...")
            response = send_request(sock, "set", "key1", "value1")
            print(f"SET response: {response}")
            
            # Test GET command
            print("\nTesting GET command...")
            response = send_request(sock, "get", "key1")
            print(f"GET response: {response}")
            
            # Test DEL command
            print("\nTesting DEL command...")
            response = send_request(sock, "del", "key1")
            print(f"DEL response: {response}")
            
            # Test GET after DELETE
            print("\nTesting GET after DELETE...")
            response = send_request(sock, "get", "key1")
            print(f"GET response: {response}")
            
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()

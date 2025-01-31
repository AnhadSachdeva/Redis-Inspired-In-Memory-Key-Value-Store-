import socket
import struct
import sys

def send_request(sock, command):
    try:
        # Split command into arguments
        args = command.strip().split()
        if not args:
            return None
            
        # Create the binary protocol message
        cmd = struct.pack('<I', len(args))  # Number of arguments
        for arg in args:
            arg_bytes = arg.encode('utf-8')
            cmd += struct.pack('<I', len(arg_bytes))  # Length of argument
            cmd += arg_bytes  # Argument data
        
        # Send message length and command
        msg_len = struct.pack('<I', len(cmd))
        sock.sendall(msg_len + cmd)
        
        # Read response length
        resp_len_bytes = sock.recv(4)
        if not resp_len_bytes:
            return "Error: No response"
            
        resp_len = struct.unpack('<I', resp_len_bytes)[0]
        
        # Read response data
        resp_data = sock.recv(resp_len)
        if not resp_data:
            return "Error: No data"
            
        resp_type = resp_data[0]
        
        if resp_type == 0:    # SER_NIL
            return "(nil)"
        elif resp_type == 1:  # SER_ERR
            code = struct.unpack('<I', resp_data[1:5])[0]
            length = struct.unpack('<I', resp_data[5:9])[0]
            msg = resp_data[9:9+length].decode('utf-8')
            return f"(error) {msg}"
        elif resp_type == 2:  # SER_STR
            length = struct.unpack('<I', resp_data[1:5])[0]
            return resp_data[5:5+length].decode('utf-8')
        elif resp_type == 3:  # SER_INT
            return str(struct.unpack('<q', resp_data[1:9])[0])
        elif resp_type == 4:  # SER_DBL
            return str(struct.unpack('<d', resp_data[1:9])[0])
        
        return f"Unknown response type: {resp_type}"
        
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    host = 'localhost'
    port = 1234
    
    print("Connecting to redis server...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except ConnectionRefusedError:
        print("Could not connect to server. Is it running?")
        return
        
    print("Connected! Type your commands (exit to quit):")
    
    while True:
        try:
            command = input('> ')
            if command.lower() in ('exit', 'quit'):
                break
                
            if command.strip():
                response = send_request(sock, command)
                print(response)
                
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")
            break
    
    sock.close()
    print("\nDisconnected")

if __name__ == "__main__":
    main() 
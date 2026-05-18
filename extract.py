import os
import signal


def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")

TIMEOUT = 5  

def scan_directory(directory, output_file):

    if not os.path.exists(directory):
        output_file.write(f"Directory {directory} does not exist.\n")
        return

    for root, dirs, files in os.walk(directory):

        if 'per_cpu' in root:
            output_file.write(f"Skipping entire directory: {root}\n")
            continue

        for file in files:
            file_path = os.path.join(root, file)

            if file_path == '/sys/kernel/security/apparmor/revision':
                output_file.write(f"Skipping file: {file_path}\n")
                continue

            if os.access(file_path, os.W_OK):
                # Set the signal handler for timeout
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(TIMEOUT)  # Start the timer

                try:
                    with open(file_path, 'r') as f:
                        content = f.read().strip()  # Read and strip any extra whitespace

                        # Try to convert the content to an integer
                        try:
                            int_value = int(content)
                            output_file.write(f"{file_path}: {int_value}\n\n")
                        except ValueError:
                            output_file.write(f"{file_path}: {content}\n\n")

                except TimeoutError:
                    output_file.write(f"Timeout reading file {file_path}\n")
                except Exception as e:
                    output_file.write(f"Error reading file {file_path}: {e}\n")
                finally:
                    signal.alarm(0)  # Disable the alarm

if __name__ == "__main__":

    directories = ['/proc/sys', '/sys']

    with open('output.txt', 'w') as output_file:
        for directory in directories:
            output_file.write(f"Scanning directory: {directory}\n")
            scan_directory(directory, output_file)
            output_file.write("-" * 40 + "\n")
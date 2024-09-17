import subprocess
import sys

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode('utf-8'), error.decode('utf-8')

def scale_bot(app_name, workers):
    command = f"heroku ps:scale worker={workers} -a {app_name}"
    output, error = run_command(command)
    if error:
        print(f"Error scaling {app_name}: {error}")
    else:
        print(f"Scaled {app_name} to {workers} worker(s)")

def check_status(app_name):
    command = f"heroku ps -a {app_name}"
    output, error = run_command(command)
    if error:
        print(f"Error checking status of {app_name}: {error}")
    else:
        print(f"Status of {app_name}:\n{output}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python manage_bots.py <app_name> <action> [workers]")
        print("Actions: start, stop, status")
        return

    app_name = sys.argv[1]
    action = sys.argv[2]

    if action == "start":
        scale_bot(app_name, 1)
    elif action == "stop":
        scale_bot(app_name, 0)
    elif action == "status":
        check_status(app_name)
    else:
        print("Invalid action. Use 'start', 'stop', or 'status'.")

if __name__ == "__main__":
    main()
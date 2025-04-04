import json
import paramiko

# Raspberry Pi connection details
RASPBERRY_PI_HOSTNAME = "raspberrypi.local"  # Use IP address if necessary
USERNAME = "pi"
PASSWORD = "raspberry"  # Change if needed
REMOTE_SCRIPT = "/home/pi/mlx.py"
VENV_PATH = "/home/pi/fyp/tf_venv/bin/activate"  # Virtual environment path

def send_signal_to_raspberry(selected_option):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(RASPBERRY_PI_HOSTNAME, username=USERNAME, password=PASSWORD)

        # Run the script inside the virtual environment
        command = f"source {VENV_PATH} && python3 {REMOTE_SCRIPT} {selected_option}"
        stdin, stdout, stderr = client.exec_command(command)

        output = stdout.read().decode().strip()
        errors = stderr.read().decode().strip()

        client.close()

        if errors:
            return {"error": errors}

        # Convert output to JSON format
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format received from Raspberry Pi"}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    selected_option = input("Enter body part option 1: Forehead\n 2: Wrist\n 3: Armpit\n 4: Chest\n 5: Back \n Your Option:").strip()
    print("Please wait...")

    # Send the selected option to Raspberry Pi and get temperature data
    health_data = send_signal_to_raspberry(selected_option)

    # Print the result (JSON output)
    print(json.dumps(health_data, indent=4))

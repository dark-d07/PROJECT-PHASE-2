import json
import paramiko

# Raspberry Pi connection details
RASPBERRY_PI_HOSTNAME = "raspberrypi.local"  # Use IP if needed
USERNAME = "pi"
PASSWORD = "raspberry"  # Change if necessary
REMOTE_SCRIPT = "/home/pi/data.py"
VENV_PATH = "/home/pi/fyp/tf_venv/bin/activate"  # Virtual environment path

def send_command_to_raspberry(action, selected_option=None):
    """Send a command to Raspberry Pi and retrieve sensor data."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(RASPBERRY_PI_HOSTNAME, username=USERNAME, password=PASSWORD)

        # Build command based on action
        if action == "temperature":
            command = f"source {VENV_PATH} && python3 {REMOTE_SCRIPT} temperature {selected_option}"
        elif action == "max30102":
            command = f"source {VENV_PATH} && python3 {REMOTE_SCRIPT} max30102"
        else:
            return {"error": "Invalid action"}

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
    selected_option = input("Enter body part option:\n 1: Forehead\n 2: Wrist\n 3: Armpit\n 4: Chest\n 5: Back \nYour Option: ").strip()
    print("Measuring temperature, please wait...")

    # Step 1: Get temperature from Raspberry Pi
    temp_data = send_command_to_raspberry("temperature", selected_option)
    print(json.dumps(temp_data, indent=4))

    # Step 2: Request MAX30102 (heart rate & SpO₂) data
    print("\nNow measuring heart rate & SpO₂...")
    max_data = send_command_to_raspberry("max30102")
    print(json.dumps(max_data, indent=4))

    # Combine and display results
    final_data = {**temp_data, **max_data}
    print("\nFinal Health Data:")
    print(json.dumps(final_data, indent=4))

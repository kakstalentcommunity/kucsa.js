import socket
import time
import json
import platform
import subprocess

class DeviceTracker:
    def __init__(self, log_file='device_log.txt'):
        """
        Initialize Device Tracker with logging and device tracking capabilities
        
        Args:
            log_file (str): Path to log file for storing device information
        """
        self.log_file = log_file
        self.tracked_devices = []
        self.device_logs = []

    def detect_network_devices(self):
        """
        Detect devices on the local network using different methods based on OS
        
        Returns:
            list: Discovered network devices with their details
        """
        system = platform.system().lower()
        discovered_devices = []

        try:
            if system == 'windows':
                # Windows: Use arp -a command
                output = subprocess.check_output(['arp', '-a'], 
                                                universal_newlines=True)
                lines = output.split('\n')
                for line in lines[3:]:
                    parts = line.split()
                    if len(parts) >= 3:
                        discovered_devices.append({
                            'ip': parts[0],
                            'mac': parts[1],
                            'type': parts[2] if len(parts) > 2 else 'Unknown'
                        })

            elif system in ['linux', 'darwin']:  # Linux or macOS
                # Use nmap for network discovery
                try:
                    # Scan local network (assumes 192.168.1.0/24 subnet - modify as needed)
                    output = subprocess.check_output(['nmap', '-sn', '192.168.1.0/24'], 
                                                        universal_newlines=True)
                    # Parse nmap output (this is a simplified parsing)
                    lines = output.split('\n')
                    for line in lines:
                        if 'Nmap scan report for' in line:
                            ip = line.split()[-1]
                        elif 'MAC Address:' in line:
                            mac = line.split('MAC Address: ')[1].split()[0]
                            discovered_devices.append({
                                'ip': ip,
                                'mac': mac,
                                'type': 'Unknown'
                            })
                except FileNotFoundError:
                    print("Nmap not installed. Please install nmap for network scanning.")

            else:
                print(f"Unsupported OS: {system}")
                return []

            return discovered_devices

        except Exception as e:
            print(f"Error detecting network devices: {e}")
            return []

    def add_device_to_track(self, device_identifier):
        """
        Add a specific device to track
        
        Args:
            device_identifier (str): IP address or MAC address of device
        """
        # Validate device identifier format (basic checks)
        if not device_identifier:
            print("Invalid device identifier")
            return False

        # Check if device is already being tracked
        if device_identifier in [d.get('ip') or d.get('mac') for d in self.tracked_devices]:
            print("Device is already being tracked")
            return False

        # Try to find device details in network scan
        network_devices = self.detect_network_devices()
        matching_device = next(
            (device for device in network_devices 
             if device['ip'] == device_identifier or device['mac'] == device_identifier), 
            None
        )

        if matching_device:
            self.tracked_devices.append(matching_device)
            print(f"Added device to tracking: {matching_device}")
            return True
        else:
            print(f"Could not find device {device_identifier} on network")
            return False

    def track_device(self, device, interval=60, duration=3600):
        """
        Track a specific device's network presence
        
        Args:
            device (dict): Device information
            interval (int): Time between checks in seconds
            duration (int): Total tracking time in seconds
        """
        start_time = time.time()
        print(f"Starting tracking for device: {device}")

        while time.time() - start_time < duration:
            try:
                # Ping the device to check connectivity
                param = '-n' if platform.system().lower() == 'windows' else '-c'
                output = subprocess.run(
                    ['ping', param, '4', device['ip']], 
                    capture_output=True, 
                    text=True
                )

                # Check ping result
                device_status = {
                    'timestamp': time.time(),
                    'ip': device['ip'],
                    'mac': device.get('mac', 'Unknown'),
                    'online': output.returncode == 0
                }

                # Log device status
                self.device_logs.append(device_status)
                
                # Write to log file
                with open(self.log_file, 'a') as f:
                    f.write(json.dumps(device_status) + '\n')

                print(f"Device {device['ip']} status: {'Online' if device_status['online'] else 'Offline'}")

            except Exception as e:
                print(f"Error tracking device {device['ip']}: {e}")

            # Wait before next check
            time.sleep(interval)

    def display_tracking_summary(self):
        """
        Display summary of tracked devices
        """
        if not self.device_logs:
            print("No device tracking data available.")
            return

        print("\n--- Device Tracking Summary ---")
        for log in self.device_logs:
            print(f"Time: {time.ctime(log['timestamp'])}")
            print(f"IP: {log['ip']}")
            print(f"MAC: {log['mac']}")
            print(f"Status: {'Online' if log['online'] else 'Offline'}")
            print("---")

def main():
    # Create device tracker
    tracker = DeviceTracker()

    # Detect network devices
    print("Scanning network for devices...")
    network_devices = tracker.detect_network_devices()
    
    # Print discovered devices
    print("\nDiscovered Devices:")
    for device in network_devices:
        print(f"IP: {device['ip']}, MAC: {device['mac']}")

    # Example: Track a specific device
    # Replace with the IP or MAC of the device you want to track
    target_device_ip = input("\nEnter the IP of the device you want to track: ")
    
    # Add device to track
    if tracker.add_device_to_track(target_device_ip):
        # Track the first added device
        tracker.track_device(tracker.tracked_devices[0], interval=60, duration=3600)
        
        # Display tracking summary
        tracker.display_tracking_summary()

if __name__ == "__main__":
    main()
import subprocess
from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient

# Set your Azure subscription ID and resource group name
subscription_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
resource_group_name = 'XXX-xxx'

# Create a credential object using DefaultAzureCredential
credential = DefaultAzureCredential()

# Create a MonitorManagementClient
monitor_client = MonitorManagementClient(credential, subscription_id)

# List of alert names to modify (both metric and log search alerts)
alert_names_to_modify = [
    'xxx-xxxx-xxx',
    'xxx xx xxx - xx-xx'
]

def main():
    # Ask user for action
    action = input("Do you want to disable or enable the alerts? (type 'disable' or 'enable'): ").strip().lower()
    
    if action not in ['disable', 'enable']:
        print("Invalid input. Please type 'disable' or 'enable'.")
        return

    # List and modify alerts
    print(f"Checking and {action}ing alerts:")
    
    for alert_name in alert_names_to_modify:
        metric_alert = None  # Initialize metric_alert to None
        try:
            # Check if it's a metric alert
            metric_alert = monitor_client.metric_alerts.get(resource_group_name, alert_name)
            if metric_alert:
                print(f"{action.capitalize()}ing Metric Alert: {metric_alert.name}, Status: {metric_alert.enabled}")
                metric_alert.enabled = (action == 'enable')  # Set to True if enabling, False if disabling
                monitor_client.metric_alerts.create_or_update(resource_group_name, alert_name, metric_alert)
                print(f"{action.capitalize()}d Metric Alert: {metric_alert.name}")
                continue  # Skip to the next alert name
                
        except Exception as e:
            # If not found, it may be a log search alert
            if metric_alert is None:  # Only proceed if metric_alert was not defined
                try:
                    # Disable or enable log search alert using Azure CLI command
                    print(f"{action.capitalize()}ing Log Search Alert: {alert_name}")
                    subprocess.run(
                        ["az", "monitor", "scheduled-query", "update",
                         "-g", resource_group_name,
                         "-n", alert_name,
                         "--disabled", str(action == 'disable').lower()],
                        check=True
                    )
                    print(f"{action.capitalize()}d Log Search Alert: {alert_name}")
                except subprocess.CalledProcessError as e:
                    print(f"Alert not found or could not be {action}d: {alert_name}")

if __name__ == "__main__":
    main()
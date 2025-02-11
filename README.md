# Azure Alerts Manager

🔔 A Python-based tool for managing Azure alerts at scale. Easily enable/disable both metric and log-based alerts with a single command.

## 📋 Repository Structure
```
azure-alerts-manager/
├── alert_manager.py
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/azure-alerts-manager.git
cd azure-alerts-manager
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your Azure credentials:
```bash
az login
```

4. Update the configuration:
Edit `alert_manager.py` and update your subscription ID and resource group:
```python
subscription_id = 'your-subscription-id'
resource_group_name = 'your-resource-group'

alert_names_to_modify = [
    'xxx-xxxx-xxx',
    'xxx xx xxx - xx-xx'
]
```

5. Run the script:
```bash
python alert_manager.py
```

## 📁 File Contents

### src/alert_manager.py
```python
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
```

### requirements.txt
```plaintext
azure-identity
azure-mgmt-monitor
azure-mgmt-loganalytics
```

### .gitignore
```plaintext
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# UV
#   Similar to Pipfile.lock, it is generally recommended to include uv.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#uv.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/latest/usage/project/#working-with-version-control
.pdm.toml
.pdm-python
.pdm-build/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

# PyPI configuration file
.pypirc
```

### tests/test_alert_manager.py
```python
import unittest
from unittest.mock import patch, MagicMock
from src.alert_manager import main

class TestAlertManager(unittest.TestCase):
    @patch('builtins.input', return_value='enable')
    @patch('azure.mgmt.monitor.MonitorManagementClient')
    def test_enable_alerts(self, mock_monitor_client, mock_input):
        # Add your test cases here
        pass

    @patch('builtins.input', return_value='disable')
    @patch('azure.mgmt.monitor.MonitorManagementClient')
    def test_disable_alerts(self, mock_monitor_client, mock_input):
        # Add your test cases here
        pass

if __name__ == '__main__':
    unittest.main()
```

## 🔑 Prerequisites

- Python 3.7 or higher
- Azure CLI installed and configured
- Azure subscription with appropriate permissions
- Azure Identity and Monitor Management packages

## 🛠️ Features

- Enable/disable multiple Azure alerts with a single command
- Support for both metric and log-based alerts
- Error handling and detailed feedback
- Easy to extend and customize

## 🤝 Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Azure Python SDK team for the excellent documentation
- Contributors who helped shape this tool

## 📚 Further Reading

Check out our detailed [Medium article](docs/medium-article.md) for more insights on managing Azure alerts efficiently.

---

⭐ If you find this tool useful, please consider giving it a star!
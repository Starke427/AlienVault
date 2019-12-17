# Forcibly uninstall the AlienVault agent, clear the old configuration and re-install.
# Author: Jeff Starke


# Uninstall AlienVault Agent
powershell -noninteractive -executionpolicy bypass -file "C:\Program Files\osquery\alienvault-agent.ps1" uninstall

# Remove osquery directory
Remove-Item -path "C:\Program Files\osquery" -recurse

# Install AlienVault Agent
# Insert new installation script here:

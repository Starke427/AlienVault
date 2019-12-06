# AlienVault

The following is intended to aide in the management of USM Anywhere deployments.

# USM Anywhere

USM Anywhere is a proprietary solution that centralizes security monitoring of networks and devices in the cloud, on premises, and in remote locations, helping you to detect threats virtually anywhere. USM Anywhere automatically collects and analyzes data across your attack surface, helping you to quickly gain centralized security visibility without the complexity of multiple disparate security technologies.  

The deployment revolves around sensors and agents that will be forwarding up to a cloud instance. Sensors serve as syslog collectors and can initiate a number of different API collection tasks that gather logs from cloud services. Sensors are available for Hyper-V, VMware, Azure, AWS, and GCP and can be built in under 30 minutes. On-premise sensors are even capable of providing network IDS when provided a SPAN port from a network switch. Sensor deployment resources can be accessed here:
https://www.alienvault.com/products/usm-anywhere/sensor-downloads  

Agents are installed on individual servers and workstations (64-bit only) and do not rely on the sensor for communication with the cloud instance. This is ideal for remote workers or locations that can't host a sensor due to resource limitations. Once your initial sensor is deployed and you can access your cloud instance, you'll be able to access the scripts needed for installing AlienVault Agents.

# AlienVault Agent Deployment

Deploying an agent is as simple as running a one-liner. The difficulty comes in mass-deploying in a controlled and repeatable manner. Currently, the AlienVault Agents are also unable to auto-update, meaning that a routine manual update needs to be pushed out at scheduled intervals or a schedule task needs to be incorporated into the initial deployment plan. The current Window's AlienVault Agent also does not provide PCI compliant file integrity monitoring; as such, it is recommended that you deploy NXlog with Sysmon instead (see below).

## Ansible Deployment

## Group Policy Deployment

Group Policy allows you to run various script files at a computer startup/shutdown or during user logon/logout. You can use GPOs not only to run classic batch files on a domain computers (.bat, .cmd, .vbs), but also to execute PowerShell scripts (.ps1) during Startup/Shutdown/Logon/Logoff.

Note - the GPO will only run when a computer starts. If your computers aren't restarted often, we recommended using SCCM or Ansible instead, if possible.

### Prepare the installation script

In this case, all we need is the multi-asset installation script saved as a .ps1. It will automatically download, install, and sync the Alienvault agent with your USM Anywhere deployment. Do keep in mind that the agent version is hard-coded into this script and the script should be updated on a regular, scheduled interval to ensure the latest agent versions are pushed out to your environment. Currently, the AlienVault agent does not support auto-updating.

### Create a GPO

1. Start the Active Directory Users and Computers snap-in. To do this, click Start, point to Administrative Tools, and then click Active Directory Users and Computers.
2. In the console tree, right-click your domain, and then click Properties.
3. Click the Group Policy tab, and then click New.
4. Type a name for this new policy (for example, AlienVault Agent Distribution), and then press Enter.
5. Click Properties, and then click the Security tab.
6. Clear the Apply Group Policy check box for the security groups that you don't want this policy to apply to. 
7. Select the Apply Group Policy check box for the groups that you want this policy to apply to.
8. When you are finished, click OK.

### Assign the script

1. Start the Active Directory Users and Computers snap-in. To do this, click Start, point to Administrative Tools, and then click Active Directory Users and Computers.
2. In the console tree, right-click your domain, and then click Properties.
3. Click the Group Policy tab, select the policy that you want, and then click Edit.
4. Under Computer Configuration, expand Windows Settings.

#### To run unsigned PowerShell Scripts

5. Right-click Scripts (Startup/Shutdown), select Startup policy and click on the first tab for Scripts.
6. Click Show Files and drag the script into the opened File Explorer window to copy the Powershell script to the domain controller. 
7. Now click Add and add the following for your script name and parameters:
> Script Name: %windir%\System32\WindowsPowerShell\v1.0\powershell.exe

> Script Parameters: -Noninteractive -ExecutionPolicy Bypass –Noprofile -file %~dp0MyPSScript.ps1

Note: %~dp0 references the SYSVOL directory where your script has been copied to.
8. To correctly run PowerShell scripts during computer startup, you need to configure the delay time before scripts launch using the policy in the Computer Configuration -> Administrative Templates -> System -> Group Policy section. Enable the “Configure Logon Script Delay” policy and specify a delay in minutes before starting the logon scripts (sufficient to complete the initialization and load all necessary services). It is usually enough to set up here for 1-2 minutes.
9. Close the Group Policy snap-in, click OK, and then close the Active Directory Users and Computers snap-in.
10. When the client computer starts, the managed software package is automatically installed.

#### To run signed PowerShell Scripts
5. Right-click Scripts (Startup/Shutdown), select Startup policy and click on the second tab for PowerShell Scripts.
6. Click Show Files and drag the script into the opened File Explorer window. Copy the Powershell script to the domain controller. 
7. Now click Add and add the copied PowerShell script to the list of scripts to be run by the PowerShell policy.
8. To correctly run PowerShell scripts during computer startup, you need to configure the delay time before scripts launch using the policy in the Computer Configuration -> Administrative Templates -> System -> Group Policy section. Enable the “Configure Logon Script Delay” policy and specify a delay in minutes before starting the logon scripts (sufficient to complete the initialization and load all necessary services). It is usually enough to set up here for 1-2 minutes.
9. By default, Windows security settings do not allow running PowerShell scripts. The current value of the PowerShell script execution policy setting can be obtained using the Get-ExecutionPolicy cmdlet. If the policy is not configured, the command will return Restricted (any scripts are blocked). The security settings for running the PowerShell script can be configured via the “Turn On Script Execution” policy (in the GPO Computer Configuration section -> Administrative Templates -> Windows Components -> Windows PowerShell). Set this value to: Allow only signed scripts (AllSigned).
10. Close the Group Policy snap-in, click OK, and then close the Active Directory Users and Computers snap-in.
11. When the client computer starts, the managed software package is automatically installed.


## SCCM Deployment

## PowerShell Deployment

## Bash Deployment

---

# NXlog/Sysmon Deployment

For environments that require file integrity monitoring, it is recommended that you install NXlog to serve as a syslog forwarder of Windows Eventlog, and Sysmon, to provide FIM to your Windows Eventlog. The provided nxlog.conf will configure your Windows host to forward Application, System, Security, and Sysmon eventlogs along with any IIS, SQL, Exchange and local firewall events. The sysmon deployment [here](https://github.com/Starke427/Sysmon-Configs) can be leveraged to provide file integrity, registry, and dns monitoring.

## Download NXlog CE

NXlog Community Edition can be downloaded here: https://nxlog.co/products/nxlog-community-edition/download

## Configure NXlog CE

The nxlog.conf will need to be modified; change CHANGEME to your USM Anywhere sensor's IP. Then download the configuration and place it at C:\Program Files (x86)\nxlog\conf\nxlog.conf and restart the NXlog service.

---

# Agent Troubleshooting

The following commands are useful when troubleshooting AlienVault Agent connectivity.
Note: On older Windows agents, the AlienVault Agent command script may be located under C:\Program Data\osquery.

## Restart Agent

Windows:
```
C:\Program Files\osquery\alienvault-agent.ps1 restart
```

Linux:
```
/usr/bin/alienvault-agent.sh restart
```

## Reinstall Agent

Windows:
```
C:\Program Files\osquery\alienvault-agent.ps1 force-update
```

Linux:
```
/usr/bin/alienvault-agent.sh force-update
```

## Uninstall Agent

Windows:
```
C:\Program Files\osquery\alienvault-agent.ps1 uninstall
```

Linux:
```
/usr/bin/alienvault-agent.sh force-update uninstall
```

## Gather Troubleshooting Information

Windows:
```
C:\Program Files\osquery\alienvault-agent.ps1 version
```
```
C:\Program Files\osquery\alienvault-agent.ps1 report
```
```
C:\Program Files\osquery\alienvault-agent.ps1 osqueryi
```

Linux:
```
/usr/bin/alienvault-agent.sh version
```
```
/usr/bin/alienvault-agent.sh report
```
```
/usr/bin/alienvault-agent.sh osqueryi
```

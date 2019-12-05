# AlienVault

The following is intended to aide in the management of USM Anywhere deployments.

# USM Anywhere

USM Anywhere is a proprietary solution that centralizes security monitoring of networks and devices in the cloud, on premises, and in remote locations, helping you to detect threats virtually anywhere. USM Anywhere automatically collects and analyzes data across your attack surface, helping you to quickly gain centralized security visibility without the complexity of multiple disparate security technologies.  

The deployment revolves around sensors and agents that will be forwarding up to a cloud instance. Sensors serve as syslog collectors and can initiate a number of different API collection tasks that gather logs from cloud services. Sensors are available for Hyper-V, VMware, Azure, AWS, and GCP and can be built in under 30 minutes. On-premise sensors are even capable of providing network IDS when provided a SPAN port from a network switch. Sensor deployment resources can be accessed here:
https://www.alienvault.com/products/usm-anywhere/sensor-downloads  

Agents are installed on individual servers and workstations (64-bit only) and do not rely on the sensor for communication with the cloud instance. This is ideal for remote workers or locations that can't host a sensor due to resource limitations. Once your initial sensor is deployed and you can access your cloud instance, you'll be able to access the scripts needed for installing AlienVault Agents.

# Agent Deployment

Deploying an agent is as simple as running a one-liner. The difficulty comes in mass-deploying in a controlled and repeatable manner. Currently, the AlienVault Agents are also unable to auto-update, meaning that a routine manual update needs to be pushed out at scheduled intervals or a schedule task needs to be incorporated into the initial deployment plan.

## Ansible Deployment

## Group Policy Deployment

## SCCM Deployment

## PowerShell Deployment

## Bash Deployment

# Agent Troubleshooting

The following commands are useful when troubleshooting AlienVault Agent connectivity.

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

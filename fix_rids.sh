#!/bin/bash
#
# Fix RID agent errors on USM Appliance OSSEC server.
# Author: Jeff Starke (Starke427)

### Get Agent ID associated with rids number at /var/ossec/queue/rids/<Agent-ID> ###

agentIDs=$(find /var/ossec/queue/rids/ -maxdepth 1 -type f |cut -d"/" -f6 | grep -v "sender" | sort)

### Remove rids folder ###

for agentID in $agentIDs; do
  rm -rf /var/ossec/queue/rids/$agentID
done

### Restart ossec server ###

/etc/init.d/ossec restart

### Restart agents by Agent ID ###

for agentID in $agentIDs; do
  /var/ossec/bin/agent_control -R $agentID
done

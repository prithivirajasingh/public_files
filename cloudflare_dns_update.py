#!/usr/bin/env python3

import json
import requests
import subprocess
import schedule
import time
import ipaddress
import os

# Configure which IPs should be updated
IPV4_UPDATE = True
IPV6_UPDATE = True

# 🔹 Configure your Cloudflare details
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")  # Refer python_confidential_environment/custom.env
CLOUDFLARE_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")  # Refer python_confidential_environment/custom.env
SUBDOMAIN = subprocess.getoutput("hostname").strip() + ".prithivirajasingh.com"


def get_ipv4():
    try:
        try:
            # Option 1
            output = subprocess.check_output(["curl", "-4", "--silent", "https://prithivirajasingh.com"]).decode("utf-8")
            # Convert text (JSON string) to Python dict
            data = json.loads(output)
            if isinstance(ipaddress.ip_address(data["ipv4"]), ipaddress.IPv4Address):
                return data["ipv4"]
            else:
                raise Exception("ipv4 https://prithivirajasingh.com error")
        except:
            # Option 2
            # Fetches the public IPv4 address using an external service .
            data = requests.get("https://api.ipify.org?format=text", timeout=5).text.strip()
            if isinstance(ipaddress.ip_address(data), ipaddress.IPv4Address):
                return data
            else:
                raise Exception("ipv4 https://api.ipify.org?format=text error")
    except:
        return None


def get_ipv6():
    try:
        try:
            # Option 1
            output = subprocess.check_output(["curl", "-6", "--silent", "https://prithivirajasingh.com"]).decode("utf-8")
            # Convert text (JSON string) to Python dict
            data = json.loads(output)
            if isinstance(ipaddress.ip_address(data["ipv6"]), ipaddress.IPv6Address):
                return data["ipv6"]
            else:
                raise Exception("ipv6 https://prithivirajasingh.com error")
        except:
            # Option 2
            # Gets the global IPv6 address using the ifconfig command.
            data = subprocess.getoutput("/usr/sbin/ifconfig | grep inet6 | grep global -m1 | awk '{print $2}'").strip()
            if isinstance(ipaddress.ip_address(data), ipaddress.IPv6Address):
                return data
            else:
                raise Exception("ipv6 ifconfig error")
    except:
        return None


def get_cloudflare_dns_record(record_type):
    """Fetches the existing Cloudflare DNS record for the subdomain."""
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records?type={record_type}&name={SUBDOMAIN}"
    headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}", "Content-Type": "application/json"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        records = response.json().get("result", [])
        return records[0] if records else None
    return None


def update_cloudflare_dns(record_id, record_type, new_ip):
    """Updates Cloudflare DNS record if IP is different."""
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records/{record_id}"
    headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}", "Content-Type": "application/json"}
    data = {"type": record_type, "name": SUBDOMAIN, "content": new_ip, "ttl": 1, "proxied": False}

    response = requests.put(url, headers=headers, json=data)
    return response.status_code == 200


def create_cloudflare_dns(record_type, new_ip):
    """Creates a new Cloudflare DNS record if none exists."""
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
    headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}", "Content-Type": "application/json"}
    data = {"type": record_type, "name": SUBDOMAIN, "content": new_ip, "ttl": 1, "proxied": False}

    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 200


def manage_dns(record_type, new_ip):
    """Checks existing DNS and updates it if needed."""
    if not new_ip:
        print(f"⚠️ No {record_type} detected, skipping update.")
        return

    record = get_cloudflare_dns_record(record_type)

    if record:
        record_id = record["id"]
        current_ip = record["content"]
        if current_ip != new_ip:
            print(f"🔄 Updating {record_type} from {current_ip} → {new_ip}")
            if update_cloudflare_dns(record_id, record_type, new_ip):
                print(f"✅ {record_type} updated successfully!")
            else:
                print(f"❌ Failed to update {record_type}.")
        else:
            print(f"✅ No change in {record_type}, skipping update.")
    else:
        print(f"⚠️ {record_type} record not found, creating new one...")
        if create_cloudflare_dns(record_type, new_ip):
            print(f"✅ {record_type} created successfully!")
        else:
            print(f"❌ Failed to create {record_type}.")

def update_ipv4():
    ipv4 = get_ipv4()
    print(json.dumps({"ipv4": ipv4}, indent=2))
    manage_dns("A", ipv4)

def update_ipv6():
    ipv6 = get_ipv6()
    print(json.dumps({"ipv6": ipv6}, indent=2))
    manage_dns("AAAA", ipv6)

def debugger():
    print(f"Inside debugger function")

# Schedule the function to run every 10 minutes
# print(f"Debug1")
# schedule.every(10).seconds.do(debugger)
if IPV4_UPDATE:
    schedule.every(30).minutes.do(update_ipv4)
if IPV6_UPDATE:
    schedule.every(30).minutes.do(update_ipv6)

if __name__ == "__main__":
    if IPV4_UPDATE:
        update_ipv4()
    if IPV6_UPDATE:
        update_ipv6()
    while True:
        schedule.run_pending()
        time.sleep(10)  # Sleep to avoid high CPU usage

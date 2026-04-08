#!/usr/bin/env python3
"""
verify_env.py

This script parses the `claude_desktop_master_config.json` and ensures 
that the user has replaced all placeholder tokens ("YOUR_...") with real credentials.
"""

import json
import os
import sys

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config/claude_desktop_master_config.json')

def verify_configuration(config_file):
    print("🔍 Scanning MCP Configuration for missing credentials...")
    
    if not os.path.exists(config_file):
        print(f"❌ Error: Config file not found at {config_file}")
        sys.exit(1)
        
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format. {e}")
        sys.exit(1)
        
    servers = config.get("mcpServers", {})
    issues_found = 0
    passed_servers = 0
    
    for server_name, server_config in servers.items():
        print(f"\nChecking [{server_name}]...")
        
        # Check args for placeholders
        args = server_config.get("args", [])
        for i, arg in enumerate(args):
            if "YOUR_" in arg or "username:password" in arg:
                print(f"  ❌ Placeholder found in args: '{arg}'")
                issues_found += 1
                
        # Check env for placeholders
        env = server_config.get("env", {})
        for key, value in env.items():
            if "YOUR_" in value:
                print(f"  ❌ Placeholder found in env var {key}: '{value}'")
                issues_found += 1
                
        if issues_found == 0:
            print("  ✅ Configuration valid")
            passed_servers += 1
            
    print("\n" + "="*50)
    if issues_found > 0:
        print(f"⚠️  Verification Failed. Please replace the {issues_found} placeholder(s) in your config file.")
        sys.exit(1)
    else:
        print(f"🎉 Verification Passed! All {passed_servers} servers are ready to be attached to your MCP Host.")
        sys.exit(0)

if __name__ == "__main__":
    verify_configuration(CONFIG_PATH)

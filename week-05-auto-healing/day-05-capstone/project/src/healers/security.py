# Aegis Healers: Security & Traffic

def block_ip(ip_address):
    """Simulates updating a WAF or IPTable rule."""
    print(f"  [SECURITY] Blocking suspicious IP: {ip_address}")
    # Integration point: subprocess.run(["iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"])
    return True

def rate_limit_user(user_id):
    """Simulates applying a strict rate limit to a specific user."""
    print(f"  [SECURITY] Applying 1req/min rate limit to User: {user_id}")
    return True

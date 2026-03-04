import jwt
import datetime

# --- 🔐 Enterprise Authentication Mock ---

class AuthManager:
    """
    Handles Identity Extraction and Token Validation for Enterprise AIOps.
    Simulates integration with LDAP / Active Directory / JWT Providers.
    """
    SECRET_KEY = "ENTERPRISE_SEC_KEY_999"

    def __init__(self):
        # Simulated User DB (Username: [Groups])
        self.user_directory = {
            "alice": ["SRE", "DevOps", "Admins"],
            "bob": ["Developer", "Analytics"],
            "eve": ["External_Vendor"]
        }

    def generate_token(self, username):
        """Generates a mock JWT for simulation."""
        groups = self.user_directory.get(username, ["Public"])
        payload = {
            "sub": username,
            "groups": groups,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")

    def validate_and_get_identity(self, token):
        """
        Validates the JWT and returns the User ID and their associated groups.
        Enforces token integrity and expiration.
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
            return {
                "username": payload['sub'],
                "groups": payload['groups'],
                "valid": True
            }
        except Exception as e:
            print(f"❌ Security violation: Invalid token ({str(e)})")
            return {"valid": False, "error": str(e)}

    def check_permission(self, user_groups, target_acl):
        """
        Least-Privilege Check:
        Returns True if ANY of the user's groups match the target ACL.
        """
        # "Admin" group has bypass for all internal ACLs
        if "Admins" in user_groups:
            return True
        
        # Check if user groups and target_acl (which can be a list or single string) intersect
        target_list = [target_acl] if isinstance(target_acl, str) else target_acl
        return any(group in target_list for group in user_groups)

if __name__ == "__main__":
    # Test Auth Lifecycle
    auth = AuthManager()
    
    # 🔓 Alice (SRE/Admin)
    token_alice = auth.generate_token("alice")
    ident_alice = auth.validate_and_get_identity(token_alice)
    
    # 🔒 Eve (Vendor)
    token_eve = auth.generate_token("eve")
    ident_eve = auth.validate_and_get_identity(token_eve)
    
    print(f"Alice Identity: {ident_alice['username']} with groups {ident_alice['groups']}")
    print(f"Alice allowed to see 'Prod-DB-ACL'? {auth.check_permission(ident_alice['groups'], 'Prod-DB-ACL')}")
    
    print(f"\nEve Identity: {ident_eve['username']} with groups {ident_eve['groups']}")
    print(f"Eve allowed to see 'Prod-DB-ACL'? {auth.check_permission(ident_eve['groups'], 'Prod-DB-ACL')}")

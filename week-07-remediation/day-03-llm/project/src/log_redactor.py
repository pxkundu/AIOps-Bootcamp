import re
import sys

def redact_logs(input_text):
    # Pattern for IP addresses
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    
    # Pattern for potential secret tokens/IDs (e.g., abc-123-secret-999)
    # This is a simplified example
    token_pattern = r'[a-zA-Z0-9]+-[a-zA-Z0-9]+-secret-[a-zA-Z0-9]+'
    
    # Pattern for potential credit card like numbers
    cc_pattern = r'\d{4}-\d{4}-\d{4}-\d{4}'

    redacted = re.sub(ip_pattern, '[REDACTED_IP]', input_text)
    redacted = re.sub(token_pattern, '[REDACTED_TOKEN]', redacted)
    redacted = re.sub(cc_pattern, '[REDACTED_ID]', redacted)
    
    return redacted

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 log_redactor.py <log_file>")
        sys.exit(1)
        
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        logs = f.read()
    
    clean_logs = redact_logs(logs)
    
    with open("clean_logs.txt", "w") as f:
        f.write(clean_logs)
    
    print("✅ Logs redacted and saved to clean_logs.txt")

# Exercise 1: Environment Setup

> **Duration:** 1 hour | **Difficulty:** Beginner

---

## 🎯 Objective

Set up your local development environment for the AIOps Bootcamp.

---

## 📋 Prerequisites

- Docker Desktop installed and running
- Python 3.10+ installed
- Git installed
- Text editor/IDE (VS Code recommended)

---

## 📝 Tasks

### Task 1: Verify Docker Installation

```bash
# Check Docker version
docker --version
# Expected: Docker version 24.x or higher

# Verify Docker is running
docker ps
# Should show empty table (no error)

# Test with hello-world
docker run hello-world
```

**✅ Success Criteria:** "Hello from Docker!" message appears

---

### Task 2: Set Up Python Virtual Environment

```bash
# Navigate to bootcamp directory
cd ~/AIOps-Bootcamp

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On Mac/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Verify Python version
python --version
# Expected: Python 3.10+

# Upgrade pip
pip install --upgrade pip
```

**✅ Success Criteria:** Virtual environment activated, Python 3.10+

---

### Task 3: Install Core Dependencies

Create a file `requirements.txt` in the bootcamp root:

```txt
# Observability
prometheus-client==0.19.0
opentelemetry-api==1.22.0
opentelemetry-sdk==1.22.0
opentelemetry-instrumentation==0.43b0

# Data Processing
pandas==2.1.4
numpy==1.26.3

# ML/AI
scikit-learn==1.3.2

# Utilities
requests==2.31.0
python-dotenv==1.0.0
pyyaml==6.0.1
jupyter==1.0.0
```

Install dependencies:

```bash
pip install -r requirements.txt
```

**✅ Success Criteria:** All packages installed without errors

---

### Task 4: Verify Installation

Create and run a test script `test_setup.py`:

```python
#!/usr/bin/env python3
"""Test script to verify environment setup."""

import sys

def check_python_version():
    """Check Python version is 3.10+"""
    version = sys.version_info
    assert version.major == 3 and version.minor >= 10, \
        f"Python 3.10+ required, got {version.major}.{version.minor}"
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")

def check_imports():
    """Check all required packages can be imported."""
    packages = [
        ('prometheus_client', 'Prometheus Client'),
        ('opentelemetry', 'OpenTelemetry'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('sklearn', 'scikit-learn'),
        ('requests', 'Requests'),
    ]
    
    for package, name in packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - not installed")
            return False
    return True

def main():
    print("\n🔍 Checking AIOps Bootcamp Environment\n")
    print("-" * 40)
    
    check_python_version()
    
    print("\n📦 Checking packages:\n")
    if check_imports():
        print("\n" + "-" * 40)
        print("🎉 All checks passed! Environment is ready.")
        print("-" * 40 + "\n")
    else:
        print("\n❌ Some packages are missing. Run: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
```

Run the test:

```bash
python test_setup.py
```

**✅ Success Criteria:** "All checks passed!" message

---

### Task 5: Create Your Learning Repository

```bash
# Create a personal notes directory
mkdir -p my-notes/week-01

# Create your first note
cat > my-notes/week-01/day-01.md << 'EOF'
# Day 1 Notes

## Key Takeaways
- 

## Questions
- 

## Experiments
- 
EOF

# Open in your editor
code my-notes/week-01/day-01.md  # or your preferred editor
```

**✅ Success Criteria:** Personal notes directory created

---

## 📊 Submission

Take a screenshot showing:
1. `docker --version` output
2. `python test_setup.py` output with all checks passed
3. Your notes file open in editor

Save as `exercises/exercise-01-complete.png` (or upload to the discussion).

---

## 🆘 Troubleshooting

### Docker not starting
- Mac: Ensure Docker Desktop is running (check menu bar)
- Linux: Run `sudo systemctl start docker`

### Python version too old
- Install Python 3.10+ from [python.org](https://python.org)
- Or use `pyenv` to manage versions

### Package installation fails
- Ensure you're in the virtual environment (check for `(.venv)` in prompt)
- Try: `pip install --upgrade pip setuptools wheel`

---

<p align="center">
  <a href="exercise-02-explore-data.md">Next: Exercise 2 →</a>
</p>

# Project: The Disk Doctor

In this project, you will build a mini "Self-Healing Controller" that detects disk space issues and automatically cleans them up.

## 🏃 Setup

1. Install Ansible (if not already installed):
   ```bash
   pip install ansible ansible-runner
   ```

2. Open the `src/` directory to find the starter files.

## 🎯 Tasks

1. **The Playbook (`cleanup.yml`)**: Write an Ansible playbook that:
   - Cleans up files older than 7 days in `/tmp`.
   - Compresses any large log files in `logs/` (simulated).
2. **The Controller (`remediator.py`)**: Use `ansible_runner` in Python to:
   - "Listen" for a simulated Alert (we will use a JSON file).
   - If `disk_full` alert appears, trigger the playbook.
   - Print a success report once finished.

## 📂 File Structure
- `src/remediator.py`: The Python "Brain".
- `src/cleanup.yml`: The Ansible "Hands".
- `src/alerts.json`: Your simulated input.

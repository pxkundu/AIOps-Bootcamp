# Ansible for AIOps Cheatsheet

Quick reference for essential Ansible modules and patterns used in auto-remediation.

---

## 🏃 Running Playbooks

```bash
# Run a playbook locally
ansible-playbook playbook.yml

# Run on a specific host with extra variables
ansible-playbook fix.yml -e "target=db-prod" -v

# Check syntax
ansible-playbook playbook.yml --syntax-check
```

---

## 🛠️ Essential Modules for Remediation

### 1. File Systems (`ansible.builtin.file`, `find`)
```yaml
# Delete old logs
- name: Remove logs older than 30 days
  find:
    paths: /var/log/myapp
    age: 30d
  register: files_to_delete

- name: Delete files
  file:
    path: "{{ item.path }}"
    state: absent
  with_items: "{{ files_to_delete.files }}"
```

### 2. Services (`ansible.builtin.service`)
```yaml
# Restart a crashed service
- name: Restart Nginx
  service:
    name: nginx
    state: restarted
    enabled: yes
```

### 3. Shell/Command (`ansible.builtin.shell`)
*Use sparingly! Prefer specialized modules.*
```yaml
# Clear dmesg logs
- name: Clear kernel ring buffer
  shell: dmesg -c
  become: yes
```

### 4. Package Management (`ansible.builtin.yum` / `apt`)
```yaml
# Update security patches
- name: Upgrade all packages
  yum:
    name: '*'
    state: latest
    security: yes
```

---

## 🛡️ Remediation Best Practices

1. **Check Mode (`--check`)**: Always test playbooks in dry-run mode before automating them.
2. **Limit Execution**: Use `--limit` to ensure remediation only runs on the affected node identified by your RCA engine.
3. **Wait for Health**: After a restart, use the `wait_for` module to verify the port is open before resolving the incident.
   ```yaml
   - name: Wait for port 80 to become active
     wait_for:
       port: 80
       state: started
       timeout: 30
   ```

---

<p align="center">
  <a href="../../README.md">Home</a> | <a href="../reading-list.md">Reading List</a>
</p>

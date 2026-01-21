# Exercise 3: Implementing Index Lifecycle Management (ILM)

## 🎯 Objective
Learn how to manage data costs and performance by implementing an automated storage lifecycle. You will simulate moving data from "Hot" (SSD) to "Delete" (Sunset) status.

---

## 🛠️ Step 1: The Scenario
Your company generates 1TB of logs per day. Keeping this for 90 days on high-performance storage is too expensive. 
Your goal is to:
1. Keep logs in **Hot** phase for 2 days (for active searching).
2. Move to **Delete** after 3 days (to save space in this lab environment).

---

## 📝 Step 2: Creating the ILM Policy (Elasticsearch API)

In the Kibana Dev Tools (`Management > Dev Tools`), run the following:

```json
PUT _ilm/policy/aiops_log_policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_age": "2d",
            "max_size": "50gb"
          }
        }
      },
      "delete": {
        "min_age": "3d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

---

## ⚙️ Step 3: Link Policy to Index Template

Create a template that applies this policy to any new index starting with `app-logs-`:

```json
PUT _index_template/app_logs_template
{
  "index_patterns": ["app-logs-*"],
  "template": {
    "settings": {
      "index.lifecycle.name": "aiops_log_policy",
      "index.lifecycle.rollover_alias": "app-logs"
    }
  }
}
```

---

## 🚀 Step 4: Verification

Check the status of an index to see which phase it is in:

```json
GET app-logs-*/_ilm/explain
```

---

## 🧪 Questions

1. **Wait Time:** If a log is indexed on Monday at 10 AM, and the `min_age` for delete is `3d`, exactly when will it be eligible for deletion?
2. **Rollover:** What happens if the index hits `50gb` size before the `2d` age is reached?
3. **Cold Phase:** How would you modify the policy to include a **Cold** phase at 30 days that reduces the number of replicas to 0 to save disk space?

# Guide: Building Managed Connection Points (MCP) in OpenWeb UI

This guide provides a step-by-step walkthrough for building small AIOps "Tools" that integrate into an LLM-powered workflow using **Managed Connection Points**.

---

## 🛠️ 1. What is an MCP?
A **Managed Connection Point (MCP)** is a lightweight API that allows an LLM (running in OpenWeb UI or a similar shell) to call internal corporate tools securely. It acts as the "Hands" for the "Brain" (LLM).

### Key Components:
1. **Endpoint**: A URL (`/mcp/v1/discovery`) that the LLM sends requests to.
2. **Tools Definition**: A JSON schema describing the function's arguments.
3. **Identity Layer**: Passing a `Bearer` token to identify the user.

---

## 💻 2. Building Your First MCP Tool

In this project, we've built a **Glean-Discovery-Tool**. The LLM uses it to fetch context for an incident.

### Security Implementation (Reference: `mcp_server.py`)
```python
@app.route('/mcp/v1/discovery', methods=['POST'])
def mcp_discovery_tool():
    # 🕵️ Step 1: Validate Bearer Token
    token = request.headers.get("Authorization")
    identity = auth.validate_and_get_identity(token)
    
    # 🔒 Step 2: Enforce Group-Based Filtering
    # Results are returned ONLY if user.groups intersect object.acl
    ...
```

---

## ⚙️ 3. Integrating with OpenWeb UI

To add your tool to OpenWeb UI:
1. Go to **Settings > Tools > Add New Tool**.
2. **Name**: `Glean-SEC-Discovery`.
3. **URL**: `http://localhost:5001/mcp/v1/discovery`.
4. **Auth**: Select "Token" and provide the mock Bearer token from the `/auth` endpoint.
5. **JSON Schema**: 
    ```json
    {
      "name": "search_knowledge",
      "description": "Searches enterprise docs, slack, and repos for security risks.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": { "type": "string", "description": "The security search term" }
        }
      }
    }
    ```

---

## 🛡️ 4. Advanced: Permission Re-evaluation

In a production enterprise environment, the MCP should:
- Re-query the **Glean API** for every search to ensure ACLs haven't changed.
- If a user is **Removed** from a group mid-session, the next MCP call MUST fail or redact their results.
- **Audit Logs**: Log every search query along with the user's IP and ID for compliance tracking.

---

<p align="center">
  <a href="SECURITY_ARCHITECTURE.md">⬅️ Back: Security Architecture</a> | <a href="PROJECT_SETUP.md">Next: Project Setup ➡️</a>
</p>

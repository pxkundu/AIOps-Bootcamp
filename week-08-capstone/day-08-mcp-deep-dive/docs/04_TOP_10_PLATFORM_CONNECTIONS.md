# 04. Top 10 MCP Platform Connections

Because MCP is an open standard, the community and platform providers have rapidly published open-source servers. Below are the **Top 10 most heavily utilized MCP connections**, detailing how they work and their primary enterprise use cases.

---

## 1. Local File System MCP
**Provider:** Anthropic / Open Source Community
**Use Case:** Allows an LLM running locally (e.g., Claude Desktop, VSCode) to read, search, and write files directly to your hard drive. 
**LLM Compatibility:** Works exceptionally well with Anthropic Claude and OpenAI models via local hosts.
**Architecture Context:** Extremely secure because it uses Stdio transport. The LLM only has access to the exact directories whitelisted in the MCP configuration file.
> **Configuration Detail:**
> Specify exact absolute path arrays in the arguments to sandbox the AI.
> ```json
> "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/allowed_folder"]
> ```

## 2. GitHub MCP
**Provider:** Anthropic / Open Source Community
**Use Case:** Enables the LLM to search repositories, read PRs, analyze code diffs, create issues, and even push commits.
**LLM Compatibility:** Essential for coding agents. Works seamlessly with OpenWebUI for local LLMs (like LLaMA 3) acting as codebase analyzers.
**Architecture Context:**
```mermaid
graph LR
    C[Claude Desktop] --> |MCP Stdio| S[mcp-server-github]
    S --> |REST API| GH[GitHub Cloud]
```
> **Configuration Detail:** Requires a fine-grained Personal Access Token (PAT).
> ```json
> "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..." }
> ```

## 3. PostgreSQL / SQLite MCP
**Provider:** Core Community
**Use Case:** Zero-ETL data analysis. The LLM can view the database schema (`list_resources`), structure semantic SQL queries, and execute them as Tools to retrieve live data for answering business questions.
**Architecture Context:** Bypasses the need for Vector databases in structured data workflows.
> **Configuration Detail:** Requires a database connection string.
> ```json
> "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://username:password@localhost:5432/myapp"]
> ```

## 4. Slack MCP
**Provider:** Community
**Use Case:** The LLM can read channel histories, locate specific internal expertise based on user conversations, and post formatted replies.
**LLM Compatibility:** Widely used in custom Enterprise Agents combining OpenAI's GPT-4 endpoint with internal company data.
> **Configuration Detail:** Requires a Slack Bot Token and Team ID.
> ```json
> "env": { "SLACK_BOT_TOKEN": "xoxb-YOUR-TOKEN", "SLACK_TEAM_ID": "T12345678" }
> ```

## 5. Google Drive MCP
**Provider:** Community
**Use Case:** Seamless Retrieval-Augmented Generation (RAG) over corporate documents, spreadsheets, and slide decks without syncing them locally.
**Architecture Context:** Uses OAuth 2.0. The MCP server manages the token refresh lifecycle, abstracting the complex authentication away from the LLM.
> **Configuration Detail:** Uses your local google drive auth credentials.
> ```json
> "args": ["-y", "@modelcontextprotocol/server-google-drive"]
> ```

## 6. Jira / Atlassian MCP
**Provider:** Atlassian / Community
**Use Case:** PM Copilot. The AI can analyze sprint velocity, auto-update ticket statuses based on GitHub PRs, and draft acceptance criteria for new stories.
**Architecture Context:**
```mermaid
sequenceDiagram
    participant LLM as Agent Host
    participant J as Jira MCP Server
    participant G as GitHub MCP Server
    
    LLM->>G: Check PR #104 status
    G-->>LLM: "Merged"
    LLM->>J: Transition Ticket PROJ-99 to 'Done'
    J-->>LLM: "Success"
```
> **Configuration Detail:** Requires Jira URL, Email, and API Token.
> ```json
> "env": { "JIRA_URL": "https://company.atlassian.net", "JIRA_EMAIL": "me@company.com", "JIRA_API_TOKEN": "..." }
> ```

## 7. Notion MCP
**Provider:** Community
**Use Case:** Interacting with structured corporate wikis. The LLM can query specific Notion databases, read onboarding guides, and format messy meeting notes into structured Notion pages.
> **Configuration Detail:** Requires an internal Notion Integration Token.
> ```json
> "env": { "NOTION_API_TOKEN": "secret_..." }
> ```

## 8. AWS MCP
**Provider:** AWS / Community
**Use Case:** Cloud operations automation. Allows the LLM to query `boto3` or AWS CLI resources to list EC2 instances, check S3 bucket policies, or read CloudWatch logs.
**LLM Compatibility:** Highly utilized by Site Reliability Engineers (SREs) using Claude 3 Opus to debug live cluster issues.
> **Configuration Detail:** Best run via Docker to isolate AWS CLI credentials.
> ```json
> "command": "docker", "args": ["run", "-i", "--rm", "-e", "AWS_ACCESS_KEY_ID=YOUR_AWS_KEY", "-e", "AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET", "mcp/aws"]
> ```

## 9. Linear MCP
**Provider:** Linear / Community
**Use Case:** High-speed issue tracking for modern dev teams. Similar to Jira but optimized for speed. Allows LLMs to pull context from active cycles and issues directly into the IDE context window.
> **Configuration Detail:** Requires a Linear API Key.
> ```json
> "env": { "LINEAR_API_KEY": "lin_api_..." }
> ```

## 10. Sentry / Datadog MCP
**Provider:** Community
**Use Case:** Incident response. When an alert fires, the LLM immediately queries the MCP server to pull the complete stack trace and tracing context before the on-call engineer even opens their laptop.
> **Configuration Detail:** Requires Sentry Auth Token and Org Slug.
> ```json
> "env": { "SENTRY_AUTH_TOKEN": "sntrys_...", "SENTRY_ORG_SLUG": "your-org-slug" }
> ```

---

## 🌩️ Multi-Model Provider Compatibility

The beauty of MCP is that the **Server does not care which LLM is running the Client**. 

You can configure an `npx @modelcontextprotocol/server-postgres` instance and connect it to:
1. **Claude Desktop** (Using Anthropic's Claude 3.5 Sonnet)
2. **OpenWebUI** (Using an uncensored local Ollama model like DeepSeek or Llama 3)
3. **Custom Python Frameworks** (Using OpenAI's GPT-4o API)

As long as the Host framework implements the MCP Client specification, the top 10 servers listed above will instantly function, creating truly interoperable AI ecosystems.

---

## 🛠️ Automated Setup & Master Configuration

To immediately provision all 10 of these leading integrations onto your local or enterprise machine, we have built an automated configuration package:

👉 **[View Master Configuration File](../project/config/claude_desktop_master_config.json)**
👉 **[View Installation & Verification Scripts](../project/scripts/)**

**Usage:**
1. Run `bash project/scripts/install_mcp_servers.sh` to cache the open-source Node instances.
2. Edit `project/config/claude_desktop_master_config.json` with your real tokens.
3. Run `python project/scripts/verify_env.py` to ensure you didn't leave any placeholder tokens.
4. Paste the configuration into your `claude_desktop_config.json` (or VSCode `.vscode/settings.json`) and restart your Host.

# 03. MCP Configurations & Setup

To make an MCP Host (like Claude Desktop or an AI IDE) talk to an MCP Server, you must define the connection via a configuration file. Because MCP often leverages standard I/O (Stdio) local processes, the configuration file tells the Host *how* to execute the server process.

---

## 1. Claude Desktop Configuration

Claude Desktop is currently the most robust out-of-the-box MCP Host. By editing its configuration JSON, you can attach any number of servers directly to your local Claude agent.

**File Location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

### Example `claude_desktop_config.json`

```json
{
  "mcpServers": {
    "local-filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Desktop",
        "/Users/username/codebase"
      ]
    },
    "postgres-db": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://localhost:5432/myapp"
      ]
    },
    "github-server": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_secret_token_here"
      }
    },
    "custom-python-server": {
      "command": "uvx",
      "args": [
        "markitdown-mcp"
      ]
    }
  }
}
```

### Breakdown of the Configuration

1. **`mcpServers`**: The root object containing a dictionary of all configured servers.
2. **`command`**: The executable to run (usually `npx` for Node.js servers, `uvx` or `python` for Python servers, or `docker` for containerized servers).
3. **`args`**: The arguments passed to the command. For the filesystem server, passing explicit directories restricts the LLM from accessing arbitrary files on your machine.
4. **`env`**: Environment variables (like API keys) required by the server to authenticate to the external provider.

---

## 2. Docker-based Configurations

Running MCP servers inside Docker containers is the safest approach, as it completely sandboxes the server dependencies from your local machine.

```json
{
  "mcpServers": {
    "sqlite-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "/Users/username/data:/data",
        "mcp/sqlite",
        "--db-path",
        "/data/prod.db"
      ]
    }
  }
}
```

> [!TIP]
> Notice the `-i` flag in the Docker command. This is crucial for MCP Stdio transport, as it keeps the interactive `stdin`/`stdout` pipelines open so the Host and Docker Container can communicate via JSON-RPC.

---

## 3. Cursor & VSCode Configurations

Cursor (and VSCode via extensions like `Roo-Code`) support MCP, turning the IDE into an extremely powerful Host.

Within an IDE, MCP settings are often defined in `.vscode/settings.json` or globally inside the extension settings menu. The structure is often identical to Claude Desktop, ensuring cross-compatibility of server definitions.

```jsonc
// .vscode/settings.json (Example for generic MCP extensions)
{
    "mcp.servers": {
        "jira": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-jira"],
            "env": {
                "JIRA_URL": "https://mycompany.atlassian.net",
                "JIRA_API_TOKEN": "token",
                "JIRA_EMAIL": "user@company.com"
            }
        }
    }
}
```

By connecting Jira directly to the IDE via MCP, the AI coding assistant can execute a Tool to pull the acceptance criteria of a ticket directly into the context window before it starts writing the code to solve it.

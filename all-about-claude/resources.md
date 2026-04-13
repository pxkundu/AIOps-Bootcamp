# Curated GitHub Repositories and Resources

A highly curated list of open-source repositories to accelerate your learning and enterprise integration with Claude.

### Official Anthropic Resources & Cookbooks
*   **[anthropics/anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook)**
    *   **Focus:** The definitive collection of official recipes, Jupyter notebooks, and integration guides.
    *   **Highlights:** Prompt engineering examples, Function Calling (Tool Use) patterns, RAG (Retrieval-Augmented Generation) implementations, and prompt caching.
*   **[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)**
    *   **Focus:** Official reference implementations for the Model Context Protocol (MCP).
    *   **Highlights:** Ready-to-use servers for connecting Claude to enterprise data sources like PostgreSQL, Slack, GitHub, Google Drive, and more. This is essential for building agentic enterprise workflows that interact with existing infrastructure.
*   **[anthropics/claude-code](https://github.com/anthropics/claude-code)** *(Also see community Awesome lists below)*
    *   **Focus:** Resources and configurations surrounding Anthropic's interactive CLI tool `claude-code`.

### Community "Awesome" Lists
*   **[erkcet/awesome-claude-code](https://github.com/erkcet/awesome-claude-code)**
    *   **Focus:** A community-driven index of tips, workflows, and integrations specifically tailored for the Claude CLI.
    *   **Highlights:** Excellent source for `CLAUDE.md` repository configuration templates, custom MCP server listings, and bash hook recipes.
*   **[hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)**
    *   **Focus:** Another fantastic community curation emphasizing plugins and agent orchestrators.
    *   **Highlights:** Specialized slash-commands, skills, and orchestrator scripts to expand the standard CLI desktop experience.

### Popular Framework Integrations & Enterprise RAG
*   **[langchain-ai/langchain](https://github.com/langchain-ai/langchain) (Anthropic Partner Packages)**
    *   **Focus:** The industry-standard framework for building LLM applications.
    *   **Highlights:** Look specifically for `langchain-anthropic` examples. Demonstrates how to wrap Claude with advanced memory, output parsers, and enterprise vector databases (Pinecone, Milvus, Qdrant).
*   **[run-llama/llama_index](https://github.com/run-llama/llama_index)**
    *   **Focus:** Data framework for connecting custom data sources to LLMs.
    *   **Highlights:** Excellent examples of using Claude 3 and 3.5 Sonnet for complex query engines, structured entity extraction, and handling massive enterprise document corpuses.
*   **[vercel/ai](https://github.com/vercel/ai)**
    *   **Focus:** The Vercel AI SDK.
    *   **Highlights:** If you are building an enterprise web dashboard for Claude, this repository provides production-ready React/Next.js UI components and streaming examples specifically configured for Anthropic.

### Example Project Configurations
*   **[aws-samples/amazon-bedrock-samples](https://github.com/aws-samples/amazon-bedrock-samples)**
    *   **Focus:** Enterprise architectures deployed on AWS.
    *   **Highlights:** Since Claude is heavily utilized via Amazon Bedrock in enterprise environments, this repo is a goldmine for AWS SAM templates leveraging Claude for summarization, log analysis, and chatbots using secure AWS-native services.

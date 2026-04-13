# All About skills.md (and CLAUDE.md): The Agentic Configuration Paradigm

As AI moves from acting as a passive "chat assistant" to an autonomous "agentic builder," developers face a new problem: **context alignment**. How do you ensure an autonomous AI coding agent understands a specific repository's unwritten rules, build sequences, and established architectural patterns? 

Enter the **`skills.md`** (or `CLAUDE.md`) configuration—a localized set of instructions, guardrails, and custom capabilities that act as the operating manual for AI agents operating within a specific codebase.

## 1. What is a skill.md Configuration?

A `skills.md` file is a localized markdown or YAML configuration file placed at the root of a project repository. Whenever an agentic AI tool (like Claude Code) initializes within that directory, it parses this file to understand the environment before taking any action.

It typically defines:
- **Build Commands:** The exact CLI commands to build, test, and lint the repository avoiding generic assumptions.
- **Architectural Rules:** Directives on state management, preferred libraries (e.g., "Use Tailwind over CSS modules"), and design patterns.
- **Custom Skills/Tools:** Definitions of bash hooks or MCP (Model Context Protocol) servers that the AI is permitted to invoke to gather data, talk to databases, or trigger cloud deployments.

### Why is it Important?
Without a `skills.md` file, an AI agent relies entirely on its generic pre-training. It might try to use `npm` in a strictly `yarn` project, suggest `unittest` when the team strictly uses `pytest`, or introduce vulnerable coding patterns. The `skills.md` ensures the AI is immediately productive, adhering to enterprise constraints from the very first prompt.

## 2. The Future: A Game Changer in the Agentic AI Builder Pathway

While currently used to simply "prime" isolated coding assistants, the concept of a "skill file" is evolving into the ultimate foundation of agentic software engineering. 

1. **Multi-Agent Orchestration:** In the future, large enterprises won't just have one massive AI agent. They will manage a swarm of specialized agents (a UX/UI agent, a Backend Security Agent, an Infrastructure Agent). The `skills.md` will serve as the **API Contract** that tells Agent A what capabilities Agent B possesses.
2. **Dynamic Capability Provisioning:** `skills.md` will move beyond static text rules and dynamically inject credentials, spin up ephemeral CI/CD test environments, and attach MCP servers automatically based on the branch the agent is working on.
3. **Automated Onboarding:** Instead of writing a stagnant "Developer Onboarding Guide" in Confluence, engineering teams will maintain an "Agent Onboarding Guide" (`skills.md`), which will simultaneously serve human developers, allowing them to simply type a command and let the agent navigate the complex enterprise build matrix for them.

---

## 3. Real-world Enterprise Example: Building an IDP Platform

Let's look at an enterprise scenario. You are using an AI Agent to help build an **Internal Developer Platform (IDP)** utilizing **AWS Serverless infrastructure**, **AWS CDK with Python**, and a **React.js** frontend.

The following sample `skills.md` provides strict guardrails and executable capabilities to the AI so it doesn't compromise the architecture or stray from corporate standards.

### Sample `skills.md` for Enterprise IDP

```markdown
# Agent Directives for Enterprise IDP Project

## Global Context
This repository contains the enterprise Internal Developer Platform (IDP). It is a monorepo consisting of an AWS CDK (Python) backend and a React.js (TypeScript) frontend. 
Your role as an AI agent is to assist in building, extending, debugging, and maintaining this infrastructure.

## End-to-End Build Workflow (Commands)
You are permitted to run the following commands automatically to verify your work. NEVER push code without a successful run of these checks.
*   **Compile Frontend:** `cd frontend && npm run build`
*   **Backend Testing:** `cd cdk-backend && poetry run pytest`
*   **Infrastructure Synth:** `cd cdk-backend && cdk synth --quiet`
*   **Security & Linting:** `cd frontend && npm run lint && cd ../cdk-backend && flake8 . && bandit -r src/`

## Architectural Rules & Standards

### 1. AWS Serverless CDK (Python) Constraints
- **Framework Constraint:** Use AWS CDK v2 exclusively. Do not use Serverless Framework (SLS), Terraform, or raw CloudFormation templates.
- **Dependency Management:** Use `poetry` for Python module management, NO raw `pip` or `pipenv` usage allowed.
- **Construct Abstractions:** Always prefer L3/L2 constructs. Never write an L1 (`Cfn*`) construct unless it is explicitly required because L2 is unavailable.
- **Enterprise Security Posture:** 
    - Every IAM role and policy must follow the **principle of least privilege**. NEVER use `AdministratorAccess` or wildcard `*` for resource policies. Focus the scope to specific ARNs.
    - All DynamoDB tables must have `encryption=TableEncryption.AWS_MANAGED`.
    - API Gateway endpoints must use AWS Cognito Authorizers. No open APIs are permitted.
    - Lambda functions must reside within private subnets defined in `self.vpc`.

### 2. Frontend React.js Constraints
- **Core Stack:** React 18, TypeScript, Vite, and TailwindCSS space.
- **State Management:** Use `Zustand`. Do not import or write `Redux` logic.
- **UI Components:** Use functional components exclusively. Do not write class-based components.
- **Data Fetching:** Use React Query (`@tanstack/react-query`) for all backend API interactions. Do not use raw `fetch` or `axios` instances stored in side-effect hooks (`useEffect`).

## Authorized Deployment Pathway
When asked to "build and deploy a new IDP feature end-to-end", you must implement steps in this strict chronological order:
1. **API Contract Phase:** Propose the API interface in TypeScript Interfaces and await user approval.
2. **Backend Logic Phase:** Create the Lambda function module (`cdk-backend/src/`), write accompanying unit tests (`cdk-backend/tests/`), and tie it to the API Gateway in the CDK Stack (`cdk-backend/stacks/`).
3. **Infrastructure Verification:** Run the `cdk synth` command to verify architectural compilation. Read the synthesized JSON output if necessary.
4. **Frontend Phase:** Scaffold the React components in `frontend/src/features/`, connect using React Query, and ensure it successfully compiles (`Compile Frontend`).
5. **Human Review Gate:** Once all code is written and tests pass, pause. Present a multi-file diff summary and explicitly wait for human review before proposing the execution of `cdk deploy`.
```

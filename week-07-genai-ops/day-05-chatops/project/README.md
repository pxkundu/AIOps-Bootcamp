# Project: The Slack Sentry

Build a ChatOps bot that receives an alert, enriches it with a "Self-Healing Suggestion", and provides interactive buttons for an engineer to take action.

---

## 🏃 Setup

1. (Optional) Create a Slack App at [api.slack.com](https://api.slack.com/apps).
2. Install the Slack Bolt library:
   ```bash
   pip install slack_bolt
   ```
3. If you don't have a Slack Workspace, we will use the **Simulation Mode** (Log to Console) included in the starter code.

## 🎯 Tasks

1. **The Webhook Handler (`alert_catcher.py`)**: 
   - Write a Flask/FastAPI endpoint that receives a POST request representing an alert.
   - It should parse the payload and extract the `service_name` and `severity`.
2. **The Message Formatter**:
   - Use Slack's [Block Kit Builder](https://app.slack.com/block-kit-builder) to design a card.
   - The card must have two buttons: `[Acknowledge]` and `[Remediate]`.
3. **The Logic**:
   - When `[Remediate]` is clicked, the bot should "call" the `remediator.py` logic from Day 1 to fix the issue.

## 📂 File Structure
- `src/slack_bot.py`: The main bot logic.
- `src/webhook_simulator.py`: A script to send fake alerts to your bot.
- `src/blocks.json`: Your Block Kit template.

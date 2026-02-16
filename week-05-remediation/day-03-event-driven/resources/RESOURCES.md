# Week 5 Day 3 Resources: Event-Driven Automation

> "Don't call us, we'll call you." - The Webhook Philosophy.

---

## 📚 Essential Reading

### The Standards
- **[CloudEvents Specification](https://cloudevents.io/)** - The industry standard (CNCF) for describing event data in a common way.
- **[Enterprise Integration Patterns: Message Bus](https://www.enterpriseintegrationpatterns.com/patterns/messaging/MessageBus.html)** - Why decoupling senders from receivers is scalable.

### Industry Examples
- **[GitHub Webhooks Guide](https://docs.github.com/en/developers/webhooks-and-events/webhooks/about-webhooks)** - The gold standard implementation (Events, Payloads, Security).
- **[AWS Lambda: Using Event Source Mappings](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html)** - How Cloud uses FaaS to react to streams.
- **[Slack API: Events API](https://api.slack.com/apis/connections/events-api)** - How ChatOps bots listen for mentions.

---

## 🛠️ Tools & Libraries

- **[Flask (Python)](https://flask.palletsprojects.com/)** - Micro-framework for building webhook receivers.
- **[ngrok](https://ngrok.com/)** - Expose your local `localhost:5000` to the internet (critical for testing GitHub webhooks locally).
- **[Postman](https://www.postman.com/)** - Testing your webhook receiver by mimicking events.
- **[Boto3 (AWS SDK)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)** - Managing AWS Lambda from Python.

---

## 💡 Pro Tips for SREs

1.  **Idempotency is Key:**
    - Events can be delivered **at least once** (retries).
    - If you receive the same "Deduplicate DB" event twice, don't delete data twice! Check `event_id`.

2.  **Security Measures:**
    - **Verify Signatures:** Always use HMAC (Secret Key) to ensure the request came from GitHub/AWS, not a hacker.
    - **Timeout Fast:** Webhooks expect a 200 OK within seconds. If your processing takes long, spawn a background thread or queue it (Celery).

3.  **Dead Letter Queues (DLQ):**
    - What happens if your Receiver crashes? The event is lost.
    - Use a Queue (SQS/Kafka) in front of the Receiver. If processing fails, move the event to a DLQ for manual inspection.

# Email Worker with Temporal

This project contains two workers powered by Temporal:

1. **Send Email Worker** — Sends a general email.  
2. **Verification Email Worker** — Sends a verification email.

Make sure to start the Temporal server first before running the workers.

To start the Temporal server, run:

```bash
temporal server start-dev --ui-port 8080
```

Then, start the workers by running:

```bash
python worker.py
```

To test, run the starter script with three parameters: name, email, and message.

Example:

```bash
python starter.py John john@example.com "Hello from Temporal!"
```

## Requirements

- Python 3.10+  
- Temporal SDK (`pip install temporalio`)  
- Other dependencies listed in `pyproject.toml`

## Notes

- Configure your email credentials in a `.env` file or environment variables.  
- Ensure the Temporal server is running before starting the workers.

## References

- [Temporal Python SDK Docs](https://python.temporal.io/)  
- [Temporal Docs](https://docs.temporal.io/)

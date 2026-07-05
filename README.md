# KeeperHub Execution Receipt Kit

Policy-gated execution receipts for AI agents preparing KeeperHub onchain workflow requests.

## Status

This repository candidate is a local prototype. It does not execute transactions, authenticate with KeeperHub, use a wallet, call an API, or publish anything externally.

Current honest claim:

> The kit generates KeeperHub-ready execution requests and audit-ready receipt records, then blocks unsafe requests fail-closed.

The project should only claim real KeeperHub execution after a user-approved KeeperHub run produces an actual workflow/run id and transaction hash.

## Why This Exists

AI agents can decide what to do onchain, but a submission-quality system also needs to show:

- what the agent intended
- which policy allowed or blocked it
- which KeeperHub workflow request would be made
- what evidence came back from execution
- why unsafe requests did not reach execution

KeeperHub is the execution layer. This kit is the receipt and policy layer around the delegation point.

## What The Prototype Shows

- In-policy prepared execution
- Over-cap fail-closed block
- Wrong destination fail-closed block
- Low-confidence fail-closed escalation
- Deterministic intent, policy, request, and receipt hashes
- Placeholder fields for real KeeperHub workflow/run evidence

## Run Locally

```bash
npm test
npm run demo
```

No dependencies are required beyond Node.js.

## Demo Video

Draft video:

- `media/keeperhub-execution-receipt-demo-draft.mp4`
- `media/keeperhub-execution-receipt-demo-draft-contact-sheet.jpg`

This draft is intentionally marked as pre-transaction evidence. After a user-approved KeeperHub testnet run, replace it with a final video that includes the real workflow/run id and transaction hash.

## Planned KeeperHub Integration

After explicit user approval:

1. Connect to KeeperHub through the recommended remote MCP endpoint or approved CLI/plugin path.
2. Create or select one minimal testnet workflow.
3. Execute exactly one low-risk transaction through KeeperHub.
4. Attach the resulting workflow/run id, transaction hash, chain, timestamp, gas/outcome, and audit URL to the receipt.
5. Update the README, demo output, and hackathon submission fields with exact evidence.

## Safety Boundary

This candidate intentionally excludes:

- `.env`
- secrets, credentials, tokens, private keys, seed phrases
- wallet data
- internal workspace reports
- private messaging automations
- private strategy logs
- fake transaction hashes

## License

License choice is pending user approval before public publication.

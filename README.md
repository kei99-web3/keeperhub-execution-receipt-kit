# KeeperHub Execution Receipt Kit

Policy-gated execution receipts for AI agents preparing KeeperHub onchain workflow requests.

## Status

This repository now includes one authenticated KeeperHub read workflow execution. It still does not claim a submitted transaction hash, because the captured run was a read-only Base Sepolia balance check.

Current honest claim:

> The kit generates KeeperHub-ready execution requests and audit-ready receipt records, blocks unsafe requests fail-closed, and includes one real KeeperHub read workflow run as execution evidence.

The project should only claim transaction execution after a user-approved KeeperHub write run produces an actual transaction hash. The current evidence is a real KeeperHub workflow/run id for a read-only action.

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
- Real KeeperHub read workflow evidence for Base Sepolia balance checking

## Real KeeperHub Read Evidence

Captured on 2026-07-05:

- Workflow ID: `undydd3dmaeykbzmky9ik`
- Execution ID: `bh1dkp3uur0u41ftwivft`
- Run ID: `wrun_01KWRFQK1EQG92MERS9N49G5W6`
- Workflow type: `read`
- Trigger: `manual`
- Chain: Base Sepolia (`84532`)
- Action: `web3/check-balance`
- Target wallet: `0xE2DCfA30895757BaEEFAE53568C2dc9fa422815D`
- Result: success, `0 wei`
- Transaction hashes: none, because this was read-only
- Evidence JSON: `examples/keeperhub_read_execution_evidence.json`

## Run Locally

```bash
npm test
npm run demo
```

No dependencies are required beyond Node.js.

## Demo Video

Public preview video:

- `media/keeperhub-execution-receipt-public-preview.mp4`
- `media/keeperhub-execution-receipt-public-preview-contact-sheet.jpg`

This public preview is marked as KeeperHub read-run evidence with write transaction evidence still pending. After a user-approved KeeperHub testnet write run, replace it with a final video that includes the transaction hash.

## Planned KeeperHub Integration

Completed:

1. Connected to KeeperHub through the remote MCP endpoint.
2. Created and validated one minimal read-only Base Sepolia workflow.
3. Executed the workflow manually and captured workflow/run evidence.

Still pending for transaction-hash proof:

1. Fund or select a testnet wallet path.
2. Execute exactly one low-risk KeeperHub write action with user-attended signing.
3. Attach the resulting transaction hash, chain, timestamp, gas/outcome, and audit URL to the receipt.

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

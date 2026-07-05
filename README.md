# KeeperHub Execution Receipt Kit

Policy-gated execution receipts for AI agents preparing KeeperHub onchain workflow requests.

## Status

This repository now includes one authenticated KeeperHub read workflow execution and one user-approved KeeperHub Base Sepolia write transaction.

Current honest claim:

> The kit generates KeeperHub-ready execution requests and audit-ready receipt records, blocks unsafe requests fail-closed, and includes real KeeperHub read/write evidence on Base Sepolia.

The transaction evidence is a zero-value self-transfer on Base Sepolia. It exists only to prove the KeeperHub execution path without moving value.

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
- Real KeeperHub write transaction evidence for a zero-value Base Sepolia self-transfer

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

## Real KeeperHub Write Evidence

Captured on 2026-07-05:

- Execution ID: `atjoe5a6460z2ueqm1yem`
- Chain: Base Sepolia (`84532`)
- From: `0xE2DCfA30895757BaEEFAE53568C2dc9fa422815D`
- To: `0xE2DCfA30895757BaEEFAE53568C2dc9fa422815D`
- Amount: `0 ETH`
- Transaction hash: `0x3098fabd21ec72c51d2d2aed87b7777e6fc5f15eddc423340e7ba4f802e66ac5`
- Explorer: https://sepolia.basescan.org/tx/0x3098fabd21ec72c51d2d2aed87b7777e6fc5f15eddc423340e7ba4f802e66ac5
- Gas used: `21000`
- RPC receipt status: `0x1`
- Evidence JSON: `examples/keeperhub_write_execution_evidence.json`

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

This public preview now includes both the KeeperHub read-run evidence and the user-approved Base Sepolia transaction hash.

## Planned KeeperHub Integration

Completed:

1. Connected to KeeperHub through the remote MCP endpoint.
2. Created and validated one minimal read-only Base Sepolia workflow.
3. Executed the workflow manually and captured workflow/run evidence.
4. Funded the KeeperHub wallet with Base Sepolia ETH through CDP Faucet.
5. Executed exactly one low-risk zero-value KeeperHub write action.
6. Attached the resulting transaction hash, chain, timestamp, gas/outcome, and explorer URL to the receipt.

## Safety Boundary

This candidate intentionally excludes:

- `.env`
- secrets, credentials, tokens, private keys, seed phrases
- wallet data
- internal workspace reports
- private messaging automations
- private strategy logs
- fake transaction hashes or unverified execution claims

## License

License choice is pending user approval before public publication.

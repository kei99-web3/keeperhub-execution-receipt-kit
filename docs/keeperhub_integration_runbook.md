# KeeperHub Integration Runbook

This runbook records the current KeeperHub proof path. A read-only workflow run and one user-approved Base Sepolia write transaction have been completed.

## Preferred Integration Surface

Use KeeperHub's remote MCP endpoint:

```bash
claude mcp add --transport http keeperhub https://app.keeperhub.com/mcp
```

Then the user completes browser OAuth authorization inside Claude Code. This was completed on 2026-07-05.

## Proof Run Goal

Completed read proof: execute one minimal Base Sepolia `web3/check-balance` workflow through KeeperHub and attach the returned run evidence to a receipt.

Completed write proof: execute one minimal, low-risk zero-value Base Sepolia self-transfer through KeeperHub and attach the returned transaction evidence to a receipt.

## Evidence To Save

- KeeperHub workflow/run id
- transaction hash, only for write proof
- chain and network
- timestamp
- gas or fee data, if available
- outcome
- audit/run URL or safe screenshot

## Completed Read Evidence

- Workflow ID: `undydd3dmaeykbzmky9ik`
- Execution ID: `bh1dkp3uur0u41ftwivft`
- Run ID: `wrun_01KWRFQK1EQG92MERS9N49G5W6`
- Workflow type: `read`
- Trigger: `manual`
- Chain: Base Sepolia (`84532`)
- Action: `web3/check-balance`
- Target wallet: `0xE2DCfA30895757BaEEFAE53568C2dc9fa422815D`
- Result: success, `0 wei`
- Transaction hashes: none, because the run was read-only

## Completed Write Evidence

- Execution ID: `atjoe5a6460z2ueqm1yem`
- Chain: Base Sepolia (`84532`)
- From: `0xE2DCfA30895757BaEEFAE53568C2dc9fa422815D`
- To: `0xE2DCfA30895757BaEEFAE53568C2dc9fa422815D`
- Amount: `0 ETH`
- Transaction hash: `0x3098fabd21ec72c51d2d2aed87b7777e6fc5f15eddc423340e7ba4f802e66ac5`
- Explorer: https://sepolia.basescan.org/tx/0x3098fabd21ec72c51d2d2aed87b7777e6fc5f15eddc423340e7ba4f802e66ac5
- Gas used: `21000`
- RPC receipt status: `0x1`

## Stop Conditions

Stop if:

- user approval is missing
- KeeperHub login/OAuth cannot be completed safely
- testnet transaction path is unclear
- a secret, token, key, seed phrase, or private wallet value would be exposed
- the flow asks for mainnet, payment, KYC, or unexpected funding

## Public Submission Note

Describe the current project as a KeeperHub-ready receipt kit with one real KeeperHub read workflow run and one real KeeperHub Base Sepolia transaction hash. The write transaction was a zero-value self-transfer used as low-risk proof of execution.

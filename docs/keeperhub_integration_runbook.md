# KeeperHub Integration Runbook

This runbook is for a future approved KeeperHub proof run. It is not an instruction to authenticate or transact automatically.

## Preferred Integration Surface

Use KeeperHub's remote MCP endpoint:

```bash
claude mcp add --transport http keeperhub https://app.keeperhub.com/mcp
```

Then the user completes browser OAuth authorization inside Claude Code.

## Proof Run Goal

Execute one minimal, low-risk testnet transaction through KeeperHub and attach the returned evidence to a receipt.

## Evidence To Save

- KeeperHub workflow/run id
- transaction hash
- chain and network
- timestamp
- gas or fee data, if available
- outcome
- audit/run URL or safe screenshot

## Stop Conditions

Stop if:

- user approval is missing
- KeeperHub login/OAuth cannot be completed safely
- testnet transaction path is unclear
- a secret, token, key, seed phrase, or private wallet value would be exposed
- the flow asks for mainnet, payment, KYC, or unexpected funding

## Public Submission Note

Before a real KeeperHub run exists, describe this project as a local KeeperHub-ready prototype. After a run exists, describe exactly one approved KeeperHub testnet execution and link the real transaction evidence.

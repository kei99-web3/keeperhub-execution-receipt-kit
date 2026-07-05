# Receipt Schema

Current schema: `keeperhub.execution_receipt.v0`

## Top-Level Fields

| Field | Purpose |
| --- | --- |
| `schema` | Receipt schema identifier |
| `scenario` | Demo or execution scenario name |
| `createdAt` | Receipt creation timestamp |
| `status` | `approved_for_prepared_execution` or `blocked_fail_closed` |
| `intent` | Human-readable agent intent |
| `policyId` | Policy identifier |
| `intentHash` | Deterministic hash of intent-critical inputs |
| `policyHash` | Deterministic policy hash |
| `signal` | Agent signal or market/input context |
| `policyEvaluation` | Pass/fail checks and hard failures |
| `keeperHubRequest` | KeeperHub-ready workflow request when approved |
| `keeperHubRequestHash` | Deterministic request hash |
| `executionEvidence` | Current execution state and real evidence placeholders |
| `receiptHash` | Deterministic receipt hash |

## Execution Evidence Before KeeperHub Run

```json
{
  "current": "local_mock_only",
  "nextRequired": "attach real KeeperHub run id and transaction hash after user approval",
  "txHash": null,
  "auditTrailUrl": null
}
```

## Execution Evidence After KeeperHub Run

Expected final evidence fields:

- workflow/run id
- transaction hash
- chain and network
- timestamp
- gas or fee data, if exposed
- outcome
- audit/run URL or safe screenshot reference

Do not populate these fields with fabricated values.

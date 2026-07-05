# Policy Gate

The policy gate decides whether an agent intent may be converted into a KeeperHub execution request.

## Checks

- chain is allowed
- protocol is allowed
- action is allowed
- asset is allowed
- destination is allowed
- amount is under cap
- confidence is high enough
- simulation passed
- slippage is under cap
- private routing is present when required

## Fail-Closed Behavior

If any hard check fails:

- no KeeperHub request is emitted
- the receipt status becomes `blocked_fail_closed`
- hard failures are recorded for review
- `txHash` remains `null`

This is intentional. The agent should not reach onchain execution when policy, routing, amount, or confidence constraints fail.

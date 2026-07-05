const assert = require("assert");

const {
  POLICY,
  SCENARIOS,
  digest,
  evaluatePolicy,
  runDemo
} = require("../src/keeperhub_execution_receipt_agent");

const output = runDemo();
assert.equal(output.status, "mock_only_no_wallet_no_keeperhub_api_no_network");
assert.equal(output.receipts.length, 4);

const byName = Object.fromEntries(output.receipts.map((receipt) => [receipt.scenario, receipt]));

assert.equal(byName.in_policy_yield_rebalance.status, "approved_for_prepared_execution");
assert.equal(byName.in_policy_yield_rebalance.keeperHubRequest.surface, "keeperhub-mcp-or-cli");
assert.equal(byName.in_policy_yield_rebalance.executionEvidence.txHash, null);
assert.equal(byName.in_policy_yield_rebalance.executionEvidence.nextRequired, "attach real KeeperHub run id and transaction hash after user approval");

assert.equal(byName.over_cap_rebalance_blocked.status, "blocked_fail_closed");
assert.equal(byName.over_cap_rebalance_blocked.keeperHubRequest, null);
assert(byName.over_cap_rebalance_blocked.policyEvaluation.hardFailures.some((failure) => failure.name === "amount_under_cap"));

assert.equal(byName.wrong_destination_blocked.status, "blocked_fail_closed");
assert(byName.wrong_destination_blocked.policyEvaluation.hardFailures.some((failure) => failure.name === "destination_allowed"));

assert.equal(byName.low_confidence_escalation.status, "blocked_fail_closed");
assert(byName.low_confidence_escalation.policyEvaluation.hardFailures.some((failure) => failure.name === "confidence_high_enough"));

for (const receipt of output.receipts) {
  assert.match(receipt.intentHash, /^sha256:[a-f0-9]{64}$/);
  assert.match(receipt.policyHash, /^sha256:[a-f0-9]{64}$/);
  assert.match(receipt.receiptHash, /^sha256:[a-f0-9]{64}$/);
}

const firstEvaluation = evaluatePolicy(SCENARIOS[0], POLICY);
assert.equal(firstEvaluation.hardFailures.length, 0);
assert.notEqual(digest({ a: 1 }), digest({ a: 2 }));

console.log("keeperhub_execution_receipt_agent.test.js passed");

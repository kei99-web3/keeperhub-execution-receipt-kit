const crypto = require("crypto");

const POLICY = {
  id: "policy_keeperhub_demo_v1",
  owner: "demo treasury operator",
  allowedChains: ["ethereum-sepolia", "base-sepolia"],
  allowedProtocols: ["aave-v3", "uniswap-v3"],
  allowedActions: ["supply", "rebalance", "swap"],
  allowedAssets: ["USDC", "WETH"],
  allowedDestinations: ["keeperhub-aave-v3-usdc-vault", "keeperhub-uniswap-v3-router"],
  maxUsdPerRun: 25,
  maxSlippageBps: 50,
  minConfidenceBps: 7600,
  requireSimulation: true,
  requirePrivateRouting: true,
  approvalBoundary: "real KeeperHub execution requires explicit user approval"
};

const SCENARIOS = [
  {
    name: "in_policy_yield_rebalance",
    intent: "Move 18 USDC from idle treasury balance into the approved Aave v3 USDC supply workflow if simulated APY is above 4%.",
    chain: "base-sepolia",
    protocol: "aave-v3",
    action: "supply",
    asset: "USDC",
    amountUsd: 18,
    destination: "keeperhub-aave-v3-usdc-vault",
    confidenceBps: 8420,
    signal: { apyBps: 431, liquidityUsd: 1200000, staleSeconds: 18 },
    simulation: { ok: true, gasUsd: 0.12, slippageBps: 0, estimatedOutput: "18 aUSDC" },
    route: { privateRouting: true, retryPlan: "exponential_backoff", nonceMode: "keeperhub_managed" }
  },
  {
    name: "over_cap_rebalance_blocked",
    intent: "Move 180 USDC into the approved Aave v3 USDC supply workflow.",
    chain: "base-sepolia",
    protocol: "aave-v3",
    action: "supply",
    asset: "USDC",
    amountUsd: 180,
    destination: "keeperhub-aave-v3-usdc-vault",
    confidenceBps: 8200,
    signal: { apyBps: 445, liquidityUsd: 1200000, staleSeconds: 20 },
    simulation: { ok: true, gasUsd: 0.11, slippageBps: 0, estimatedOutput: "180 aUSDC" },
    route: { privateRouting: true, retryPlan: "exponential_backoff", nonceMode: "keeperhub_managed" }
  },
  {
    name: "wrong_destination_blocked",
    intent: "Swap 12 USDC into WETH using an unknown router because it quotes a better price.",
    chain: "base-sepolia",
    protocol: "uniswap-v3",
    action: "swap",
    asset: "USDC",
    amountUsd: 12,
    destination: "unknown-router",
    confidenceBps: 8300,
    signal: { apyBps: 0, liquidityUsd: 800000, staleSeconds: 9 },
    simulation: { ok: true, gasUsd: 0.18, slippageBps: 20, estimatedOutput: "0.0038 WETH" },
    route: { privateRouting: true, retryPlan: "exponential_backoff", nonceMode: "keeperhub_managed" }
  },
  {
    name: "low_confidence_escalation",
    intent: "Rebalance 10 USDC into a new route with fresh but thin liquidity.",
    chain: "base-sepolia",
    protocol: "uniswap-v3",
    action: "swap",
    asset: "USDC",
    amountUsd: 10,
    destination: "keeperhub-uniswap-v3-router",
    confidenceBps: 6100,
    signal: { apyBps: 0, liquidityUsd: 4200, staleSeconds: 7 },
    simulation: { ok: true, gasUsd: 0.21, slippageBps: 45, estimatedOutput: "0.0031 WETH" },
    route: { privateRouting: true, retryPlan: "exponential_backoff", nonceMode: "keeperhub_managed" }
  }
];

function stableStringify(value) {
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

function digest(value) {
  return `sha256:${crypto.createHash("sha256").update(stableStringify(value)).digest("hex")}`;
}

function evaluatePolicy(scenario, policy = POLICY) {
  const checks = [
    ["chain_allowed", policy.allowedChains.includes(scenario.chain), `chain=${scenario.chain}`],
    ["protocol_allowed", policy.allowedProtocols.includes(scenario.protocol), `protocol=${scenario.protocol}`],
    ["action_allowed", policy.allowedActions.includes(scenario.action), `action=${scenario.action}`],
    ["asset_allowed", policy.allowedAssets.includes(scenario.asset), `asset=${scenario.asset}`],
    ["destination_allowed", policy.allowedDestinations.includes(scenario.destination), `destination=${scenario.destination}`],
    ["amount_under_cap", scenario.amountUsd <= policy.maxUsdPerRun, `amountUsd=${scenario.amountUsd}, max=${policy.maxUsdPerRun}`],
    ["confidence_high_enough", scenario.confidenceBps >= policy.minConfidenceBps, `confidenceBps=${scenario.confidenceBps}, min=${policy.minConfidenceBps}`],
    ["simulation_passed", !policy.requireSimulation || scenario.simulation.ok, `simulationOk=${scenario.simulation.ok}`],
    ["slippage_under_cap", scenario.simulation.slippageBps <= policy.maxSlippageBps, `slippageBps=${scenario.simulation.slippageBps}, max=${policy.maxSlippageBps}`],
    ["private_route_present", !policy.requirePrivateRouting || scenario.route.privateRouting, `privateRouting=${scenario.route.privateRouting}`]
  ].map(([name, passed, detail]) => ({ name, passed, detail }));

  const hardFailures = checks.filter((check) => !check.passed);
  const status = hardFailures.length === 0 ? "approved_for_prepared_execution" : "blocked_fail_closed";
  return { status, checks, hardFailures };
}

function buildKeeperHubRequest(scenario, policy = POLICY) {
  return {
    surface: "keeperhub-mcp-or-cli",
    proposedTool: "call_workflow",
    workflowSlug: `${scenario.protocol}-${scenario.action}-${scenario.asset.toLowerCase()}`,
    chain: scenario.chain,
    executionMode: "mock_only_pending_user_approved_keeperhub_run",
    inputs: {
      asset: scenario.asset,
      amountUsd: scenario.amountUsd,
      destination: scenario.destination,
      maxSlippageBps: policy.maxSlippageBps,
      requirePrivateRouting: policy.requirePrivateRouting
    },
    expectedKeeperHubEvidenceAfterApproval: [
      "workflow run id",
      "simulation result",
      "submitted transaction hash",
      "gas used",
      "outcome",
      "timestamp",
      "audit log export"
    ]
  };
}

function createReceipt(scenario, policy = POLICY) {
  const policyEvaluation = evaluatePolicy(scenario, policy);
  const keeperHubRequest = policyEvaluation.status === "approved_for_prepared_execution"
    ? buildKeeperHubRequest(scenario, policy)
    : null;

  const receiptBase = {
    schema: "keeperhub.execution_receipt.v0",
    scenario: scenario.name,
    createdAt: "2026-07-05T00:00:00.000Z",
    status: policyEvaluation.status,
    intent: scenario.intent,
    policyId: policy.id,
    intentHash: digest({ intent: scenario.intent, amountUsd: scenario.amountUsd, destination: scenario.destination }),
    policyHash: digest(policy),
    signal: scenario.signal,
    policyEvaluation,
    keeperHubRequest,
    keeperHubRequestHash: keeperHubRequest ? digest(keeperHubRequest) : null,
    executionEvidence: keeperHubRequest
      ? {
          current: "local_mock_only",
          nextRequired: "attach real KeeperHub run id and transaction hash after user approval",
          txHash: null,
          auditTrailUrl: null
        }
      : {
          current: "blocked_before_execution",
          nextRequired: "human review or policy change",
          txHash: null,
          auditTrailUrl: null
        }
  };

  return { ...receiptBase, receiptHash: digest(receiptBase) };
}

function runDemo() {
  const receipts = SCENARIOS.map((scenario) => createReceipt(scenario));
  return {
    project: "KeeperHub Execution Receipt Kit",
    status: "mock_only_no_wallet_no_keeperhub_api_no_network",
    approvalBoundary: POLICY.approvalBoundary,
    policy: POLICY,
    receipts
  };
}

if (require.main === module) console.log(JSON.stringify(runDemo(), null, 2));

module.exports = {
  POLICY,
  SCENARIOS,
  buildKeeperHubRequest,
  createReceipt,
  digest,
  evaluatePolicy,
  runDemo
};

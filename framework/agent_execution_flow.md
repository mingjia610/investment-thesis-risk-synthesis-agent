# Agent Execution Flow

This document describes how the Investment Thesis & Risk Synthesis Agent
runs. It focused on the practical execution flow. The design rationale is
covered in the framework document.

---

## 1. Agent Initialization

The agent is initialized via the entry script `run_agent.py`.

During initialization:
- The decision policy is loaded from an external JSON configuration file
  (`data/valuation_inputs.json`)
- The target company ticker and decision parameters are set
- No market data is retrieved at this stage

This keeps decision rules separate from the core code.

---

## 2. Market Data Retrieval

Once executed, the agent retrieves a small set of publicly available market
and financial indicators using the `yfinance` library.

These indicators include:
- Share price and market capitalization
- Trailing P/E ratio
- Revenue growth
- Free cash flow
- Debt-to-equity ratio

If certain indicators are unavailable, the agent proceeds with available data.

---

## 3. Valuation Signal Interpretation

The agent does not construct a full valuation model.

Instead, it:
- Compares the current trailing P/E ratio to a policy-defined reference
  multiple
- Translates this comparison into a rough valuation indication
  (estimated upside or downside)

This step provides context for decision-making rather than a precise estimate
of intrinsic value.

---

## 4. Risk Assessment

Key risks are approximated using simple rule-based inputs.

Specifically:
- Investment intensity risk is determined by the selected scenario
  (bull, base, or bear)
- Regulatory risk is approximated based on sector classification

These risk proxies are aggregated using explicit weights defined in the
decision policy to form an overall risk level (Low / Medium / High).

---

## 5. Decision Synthesis

Valuation signals, business support indicators, and risk assessments are
combined into a structured decision score.

Based on this score:
- The agent determines an investment recommendation
  (BUY / HOLD / SELL)
- A corresponding conviction level is assigned
- A short and clear rationale explaining the decision is generated

All decision logic is rule-based and easy to trace.

---

## 6. Investment Memo Generation

The memo includes:
- Company snapshot and key signals
- Interpretation of valuation context
- Risk assessment summary
- Investment recommendation with conviction
- Decision rationale and key drivers

The memo is printed to the terminal and saved to
`outputs/sample_investment_memo.txt`.

Each execution represents an independent assessment based on current market
data and the active decision policy.

---

## Summary

The agent follows a clear and linear process from data retrieval to
decision synthesis and memo generation.
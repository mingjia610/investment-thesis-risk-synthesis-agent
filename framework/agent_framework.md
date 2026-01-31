# Agent Framework

## 1. Role in the Investment Research Process

In a buy-side investment research workflow, quantitative analysis and
valuation models are necessary but not sufficient for making an investment
decision.

Financial outputs must be interpreted, contextualized, and translated into
a clear investment view that can be discussed and defended internally.

This agent is designed to perform **that final synthesis step**.

Rather than producing new financial models, the agent operates **after**
core analysis has been completed and focuses on:
- Interpreting valuation implications
- Balancing upside potential against downside risk
- Producing a clear and decision-oriented investment view

It mirrors what a human analyst do when preparing a recommendation for an
internal investment committee.

---

## 2. Scope and Design Intent

The scope of the agent is intentionally narrow and clearly defined.

### The agent is designed to:
- Interpret valuation indications rather than construct full valuation models
- Balance expected upside against identifiable risks
- Produce a single and coherent investment recommendation
- Communicate conclusions in analyst-style language

### The agent is **not** designed to:
- Build discounted cash flow (DCF) models or detailed forecasts
- Perform accounting or ratio analysis
- Replace qualitative analyst judgement or portfolio oversight

This scope reflects buy-side practice in the real world, where final
investment decisions are formed by combining existing analysis
rather than reproducing it.

---

## 3. Why a Rule-Based Agent Is Appropriate

At the synthesis stage of research, investment decisions are rarely driven by
statistical learning or predictive optimization.

Instead, analysts typically apply:
- Explicit judgement rules
- Valuation references
- Risk tolerances
- Scenario-based reasoning

For this reason, the agent is implemented as a **rule-based decision system**.

This design prioritizes:
- Transparency
- Interpretability
- Explainability

These properties are critical in an institutional investment setting, where
decisions must be explained and defended.

The intelligence of the agent lies in its structured reasoning process, not in
parameter estimation or model training.

---

## 4. Inputs to the Agent

The agent relies on two complementary input sources.

### 4.1 Runtime Market Data

At runtime, the agent retrieves a small set of publicly available indicators
for Microsoft using the `yfinance` library, including:
- Current share price and market capitalization
- Trailing price-to-earnings (P/E) ratio
- Revenue growth
- Free cash flow
- Debt-to-equity ratio

These headline indicators provide sufficient context for high-level
interpretation without duplicating earlier analytical work.

Because the data is retrieved dynamically, the agent’s conclusions may change
as market conditions evolve.

### 4.2 Decision Policy Configuration

In addition to market data, the agent is governed by a decision policy defined
in an external JSON configuration file.

The policy specifies:
- A reference valuation multiple
- Minimum upside thresholds for positive recommendations
- Relative weights of different risk factors
- Risk classification thresholds
- Scenario assumptions (e.g. bull, base, or bear)

The policy does **not** encode a fixed investment conclusion.

Instead, it defines **the rules the agent follows**. Changes in policy parameters
lead to systematic and transparent changes in the agent’s output.

This mirrors real investment processes, where decision rules and
risk tolerances are reviewed independently of analytical workflows.

---

## 5. Reasoning and Decision Logic

The agent follows a clear and interpretable reasoning sequence.

1. **Valuation interpretation**  
   - The current valuation multiple is compared with a policy-defined
     reference level.
   - This provides a directional indication of potential upside or downside,
     rather than a precise estimate of intrinsic value.

2. **Business support check**  
   - Revenue growth and free cash flow are evaluated to assess whether the
     valuation signal is supported by underlying performance.

3. **Risk overlay**  
   - Key risks are approximated using simple and scenario-based proxies.
   - Risks are aggregated using explicit weights to form an overall risk
     assessment.
   - These proxies are designed for interpretability rather than precision.

4. **Decision synthesis**  
   - Valuation interpretation and risk assessment are combined into a
     composite score.
   - This score determines:
     - The investment recommendation (BUY / HOLD / SELL)
     - The associated level of conviction

Because both market data and policy parameters are external inputs, changes
in either will lead to corresponding changes in the agent’s output.

---

## 6. Outputs

The primary output of the agent is a written investment memo generated at
runtime.

The memo includes:
- A concise investment thesis
- Interpretation of valuation signals
- A structured assessment of key risks
- Scenario-aware commentary
- A conviction-adjusted investment recommendation

Although the output is presented in narrative form, the underlying decision
process is fully structured and rule-based.

The memo is intended to support discussion and decision-making rather than to
serve as an independent forecast.

---

## 7. Value Added to the Investment Process

The agent adds value by standardizing how valuation implications and risk
considerations are translated into an investment view.

By applying consistent decision logic, the agent:
- Reduces reliance on ad hoc judgement
- Improves transparency at the final stage of research
- Facilitates comparison across different assumptions or scenarios

In a group research setting, the agent also provides a clear mechanism for
integrating outputs from earlier analytical components into a single and
coherent investment perspective.

---

## 8. Scalability and Reusability

While this implementation is configured specifically for Microsoft to ensure
consistency within the group project, the agent is inherently reusable.

By modifying:
- The target ticker
- The decision policy configuration

the same framework can be applied to other companies or sectors without
changing the core code structure.

This balances simplicity with extensibility and avoids unnecessary
engineering complexity.

---

## 9. Relationship to Human Judgement

This agent is designed to support, not replace, human judgement.

Its outputs should be interpreted as structured inputs into the investment
decision process rather than definitive recommendations.

Final investment decisions remain subject to analyst review, particularly in
situations involving high uncertainty or asymmetric downside risk.
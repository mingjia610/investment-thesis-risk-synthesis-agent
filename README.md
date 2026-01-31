# Investment Thesis & Risk Synthesis Agent – Microsoft (MSFT)

This project implements an independent AI Analyst Agent that performs the
final decision-synthesis step carried out by buy-side fundamental analysts.

The agent is designed to operate **after core financial analysis has been
completed**. Rather than building valuation models from scratch, it translates
valuation implications and risk considerations into a structured and decision-oriented
investment recommendation presented to an internal investment committee.

---

## 1. Purpose of the agent

In practical buy-side research, valuation models and financial metrics do not
constitute an investment decision on their own. Analysts must interpret those
outputs, assess their consistency, and balance upside potential against
downside risks.

This agent is built to cover that final step.

Specifically, the agent:
- Interprets valuation context rather than producing new models
- Applies a structured and transparent risk overlay
- Synthesizes multiple inputs into a single recommendation
- Produces a written investment memo with a BUY / HOLD / SELL recommendation
  and an explicit conviction level

The agent runs independently and generates its own conclusion based on
runtime data and predefined decision rules.

---

## 2. What the agent does (in practice)

At runtime, the agent performs the following steps:

1. Retrieves publicly available market and financial indicators for
   Microsoft (MSFT)
2. Interprets simple valuation context using a policy-defined reference
3. Approximates key risk factors under a chosen scenario
4. Combines valuation context, operating checks, and risks into a decision score
5. Generates a readable investment memo summarizing the analysis

The recommendation and language of the memo are generated automatically and
will change if market data or policy parameters change.

---

## 3. Inputs and output

### Inputs

1. **Runtime market data**
   - Share price and market capitalization
   - Trailing P/E ratio
   - Revenue growth
   - Free cash flow
   - Debt-to-equity ratio  
   (retrieved dynamically using `yfinance`)

2. **Decision policy configuration**
   - Defined in `data/valuation_inputs.json`
   - Specifies valuation references, risk weights, thresholds, and scenario
     assumptions
   - Defines *how the agent reasons*, not the final investment conclusion

### Output

After execution, the agent produces a structured investment memo:

- `outputs/sample_investment_memo.txt`

This memo reflects the agent’s interpretation of valuation and risk at the
time of execution and is intended for internal discussion purposes.

---

## 4. Project structure

```text
IFTE0001/
├── agent/
│   └── thesis_risk_agent.py
├── data/
│   └── valuation_inputs.json
├── framework/
│   ├── agent_execution_flow.md
│   ├── agent_framework.md
│   └── agent_limitations_and_reflection.md
├── outputs/
│   └── sample_investment_memo.txt
├── README.md
└── run_agent.py
```

## 5. How to Run the agent

Install the required dependency:
```bash
pip install yfinance
```

Run the agent from the project root directory:
```bash
python run_agent.py
```

The generated investment memo will be printed in the terminal and saved to:
```text
outputs/sample_investment_memo.txt
```

## 6. Design Considerations and Limitations

### Design Considerations

This agent is intentionally designed to operate at the final synthesis stage
of the fundamental investment research process. In a buy-side context, this
stage focuses on interpreting existing analytical outputs rather than
constructing new valuation models or forecasts.

Accordingly, the agent adopts a rule-based decision framework. This design
choice prioritizes transparency, interpretability, and explainability over
predictive optimization. In institutional investment settings, these
properties are critical, as investment recommendations must be clearly
explained and defended in internal discussions.

Decision rules and assumptions are externalized into a configurable policy
file rather than input directly in the code. This reflects real-world practice,
where valuation references, risk tolerances, and decision thresholds are
reviewed and adjusted independently of the analytical workflow itself.

The agent is deliberately scoped to use a small set of headline financial
indicators. This avoids duplicating earlier stages of analysis while ensuring
that valuation signals and financial quality considerations are explicitly
reflected in the final investment view.

### Limitations

The agent does not construct full valuation models such as discounted cash
flow (DCF) models, nor does it perform detailed financial statement analysis.
Its outputs therefore depend on the quality and relevance of upstream
analysis and assumptions.

Risk assessment within the agent relies on simplified and scenario-based
proxies. While this approach ensures interpretability, it does not capture
the full complexity of real-world risk dynamics, interactions between risk
factors, or sudden structural changes.

In addition, the agent does not incorporate qualitative considerations such
as management quality, competitive strategy, or regulatory negotiations
beyond high-level proxies. These factors often play a critical role in
investment decisions and must be assessed separately by human analysts.

Finally, the agent is designed as a stateless decision-support tool. Each
execution represents an independent assessment based on current data and
policy assumptions, rather than a continuous monitoring or learning system.

For these reasons, the agent is intended to support, rather than replace,
human judgement. Final investment decisions remain subject to analyst review
and professional oversight.

---

## 7. Academic context

This agent is developed for academic demonstration purposes as part of a
group-based coursework on AI agents in asset management. It represents one
independent analytical agent within a broader research workflow.

Final investment decisions would remain subject to professional oversight in
a real-world setting.
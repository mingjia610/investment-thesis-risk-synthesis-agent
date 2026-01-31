# Agent Limitations and Reflection

## 1. Scope-Related Limitations

This agent is intentionally scoped to operate at the final stage of the
fundamental research workflow. As a result, it does not construct full
valuation models such as discounted cash flow (DCF) models, nor does it
perform detailed financial statement forecasting.

This reflects how buy-side analysts typically work in practice. Valuation
outputs already exist, and the key task is interpreting their implications
for investment decisions.

---

## 2. Simplified Risk Representation

The agent approximates key risks using transparent and rule-based proxies
(e.g. scenario-driven capital intensity risk and sector-based regulatory
exposure). While this approach ensures interpretability, it necessarily
simplifies the complex and evolving nature of real-world risks.

The agent does not dynamically model second-order effects, interactions
between risk factors, or sudden structural changes. As such, its risk
assessment should be interpreted as a structured indication rather than
a precise measurement.

---

## 3. Dependence on Input Quality and Assumptions

The agent’s outputs are highly dependent on the quality of both runtime
market data and the assumptions under the decision policy framework.

Errors or biases in input data and unrealistic policy parameters can
materially affect the resulting investment recommendation. The agent
does not independently validate data accuracy or question upstream
assumptions.

---

## 4. Absence of Qualitative Judgement

Although the agent combines basic valuation context and risk considerations,
it does not incorporate qualitative factors such as management quality,
competitive strategy, or regulatory negotiations beyond simple proxies.

In a real investment setting, such qualitative insights are often critical
to final decision-making. This highlights the necessity of human oversight
when interpreting the agent’s outputs.

---

## 5. Role of Human Oversight

Given the above limitations, the agent is intended to support rather than
replace human judgement. Its primary contribution is to standardize the
reasoning process and improve transparency at the synthesis stage of research.

Final investment decisions should remain subject to analyst review,
particularly in environments characterized by high uncertainty or
asymmetric downside risks.

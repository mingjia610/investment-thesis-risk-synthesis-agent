"""
Investment Thesis & Risk Synthesis Agent – Microsoft (MSFT)

Rule-based agent that conbines basic valuation context and risk considerations
to produce an investment recommendation from public market data.
"""

import json
import os
from typing import Dict, Any, Optional

import yfinance as yf


# --------------------------------------------------
# Load decision policy
# --------------------------------------------------

def load_policy(path: str) -> Dict[str, Any]:
    """
    Read the agent's decision settings from a JSON policy file.
    The file sets out the thresholds and weights the agent will use to
    form an investment recommendation.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------
# Core Agent
# --------------------------------------------------

class InvestmentThesisRiskAgent:

    def __init__(self, policy_path: str):
        self.policy = load_policy(policy_path)
        self.ticker = self.policy.get("ticker", "MSFT")

    # ---------------- Data Collection ----------------

    def fetch_market_data(self) -> Dict[str, Any]:
        """
        Retrieve a small set of key market metrics via yfinance.
        Missing data is allowed.
        """
        ticker = yf.Ticker(self.ticker)
        info = ticker.info or {}

        return {
            "company_name": info.get("shortName", self.ticker),
            "sector": info.get("sector", "N/A"),
            "share_price": info.get("currentPrice"),
            "market_cap": info.get("marketCap"),
            "trailing_pe": info.get("trailingPE"),
            "revenue_growth": info.get("revenueGrowth"),
            "free_cash_flow": info.get("freeCashflow"),
            "debt_to_equity": info.get("debtToEquity"),
        }

    # ---------------- Valuation Interpretation ----------------

    def estimate_valuation_upside(
        self, trailing_pe: Optional[float]
    ) -> Optional[float]:
        """
        Estimate potential upside using a reference P/E multiple.
        This is a not a full valuation.
        """
        if trailing_pe is None:
            return None

        reference_pe = self.policy.get("pe_reference")

        try:
            return (float(reference_pe) / float(trailing_pe) - 1.0) * 100.0
        except (ZeroDivisionError, TypeError, ValueError):
            return None

    # ---------------- Risk Assessment ----------------

    def assess_risk(self, sector: str) -> Dict[str, float]:
        """
        Estimate key risks using simple proxies.
        Risk levels vary by scenario and sector.
        """
        scenario = str(self.policy.get("scenario", "base")).lower()

        if scenario == "bull":
            ai_capex_risk = 0.40
        elif scenario == "bear":
            ai_capex_risk = 0.70
        else:
            ai_capex_risk = 0.55

        regulatory_risk = 0.50 if str(sector).lower() == "technology" else 0.35

        return {
            "ai_capex": ai_capex_risk,
            "regulatory": regulatory_risk,
        }

    # ---------------- Decision Logic ----------------

    def make_recommendation(
        self,
        data: Dict[str, Any],
        valuation_upside: Optional[float],
        risks: Dict[str, float],
    ) -> Dict[str, Any]:
        """
        Combine valuation context and risk assessment into a final
        investment recommendation with a clear rationale.
        """
        score = 0
        driver_notes = []

        # 1) Valuation signal
        min_upside = self.policy.get("min_upside_pct_for_buy", 10)
        if valuation_upside is not None and valuation_upside >= min_upside:
            score += 2
            driver_notes.append(
                f"Valuation proxy suggests upside of roughly {valuation_upside:.1f}% "
                f"(above the {min_upside:.1f}% threshold)."
            )
        elif valuation_upside is not None:
            driver_notes.append(
                f"Valuation proxy suggests upside of roughly {valuation_upside:.1f}%, "
                f"which is below the positive threshold."
            )
        else:
            driver_notes.append("Valuation signal unavailable due to missing P/E data.")

        # 2) Operating support
        rev_g = data.get("revenue_growth")
        if rev_g is not None and rev_g >= 0.05:
            score += 1
            driver_notes.append(
                f"Revenue growth remains supportive at around {rev_g * 100:.1f}% year-on-year."
            )
        elif rev_g is not None:
            driver_notes.append(
                f"Revenue growth is modest at around {rev_g * 100:.1f}% year-on-year."
            )
        else:
            driver_notes.append("Revenue growth data is unavailable.")

        fcf = data.get("free_cash_flow")
        if fcf is not None and fcf > 0:
            score += 1
            driver_notes.append("Free cash flow is positive, supporting earnings quality.")
        elif fcf is not None:
            driver_notes.append("Free cash flow is weak, which weighs on earnings quality.")
        else:
            driver_notes.append("Free cash flow data is unavailable.")

        # 3) Balance sheet check
        dte = data.get("debt_to_equity")
        if dte is not None and dte > 150:
            score -= 1
            driver_notes.append(
                f"Leverage appears elevated with a debt-to-equity ratio of roughly {dte:.1f}."
            )
        elif dte is not None:
            driver_notes.append(
                f"Leverage appears manageable with a debt-to-equity ratio of roughly {dte:.1f}."
            )
        else:
            driver_notes.append("Debt-to-equity data is unavailable.")

        # 4) Risk overlay
        weights = self.policy.get("risk_weights", {})
        risk_score = (
            risks["ai_capex"] * float(weights.get("ai_capex", 0.5))
            + risks["regulatory"] * float(weights.get("regulatory", 0.5))
        )

        thresholds = self.policy.get("risk_thresholds", {})
        high_risk = float(thresholds.get("high_risk", 0.65))
        medium_risk = float(thresholds.get("medium_risk", 0.45))

        if risk_score >= high_risk:
            score -= 2
            risk_level = "High"
        elif risk_score >= medium_risk:
            score -= 1
            risk_level = "Medium"
        else:
            risk_level = "Low"

        driver_notes.append(
            f"Overall risk is assessed as {risk_level} based on the risk overlay."
        )

        # Map score to recommendation
        if score >= 3:
            recommendation = "BUY"
        elif score >= 1:
            recommendation = "HOLD"
        else:
            recommendation = "SELL"

        # Conviction
        if recommendation == "BUY" and risk_level == "Low":
            conviction = "High"
        elif recommendation != "SELL":
            conviction = "Moderate"
        else:
            conviction = "Low"

        # Plain-language rationale
        if recommendation == "BUY":
            rationale = (
                "Current performance supports a positive recommendation with risk limiting overall conviction."
            )
        elif recommendation == "HOLD":
            rationale = (
                "Upside and risk are fairly evenly atched,suggesting a more neutral recommendation."
            )
        else:
            rationale = (
                "Risk factors outweigh the available upside under the current assumptions."
            )

        return {
            "recommendation": recommendation,
            "conviction": conviction,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "valuation_upside_pct": valuation_upside,
            "decision_score": score,
            "rationale": rationale,
            "driver_notes": driver_notes,
        }

    # ---------------- Output Generation ----------------

    def generate_investment_memo(
        self, data: Dict[str, Any], decision: Dict[str, Any]
    ) -> str:
        """
        Generate a clear investment memo based on the agent's decision.
        """

        def fmt_pct(x: Optional[float]) -> str:
            return "N/A" if x is None else f"{x:.1f}%"

        rev_growth_pct = (
            None
            if data.get("revenue_growth") is None
            else float(data["revenue_growth"]) * 100.0
        )

        drivers_text = "\n".join(
            [f"- {note}" for note in decision.get("driver_notes", [])]
        )

        return f"""
========================================
Investment Thesis & Risk Synthesis – {data['company_name']} ({self.ticker})
========================================

Company Snapshot:
- Sector: {data['sector']}
- Share Price: {data['share_price']}
- Market Capitalization: {data['market_cap']}

Key Signals:
- Trailing P/E: {data['trailing_pe']}
- Revenue Growth (YoY): {fmt_pct(rev_growth_pct)}
- Free Cash Flow: {data['free_cash_flow']}
- Debt-to-Equity: {data['debt_to_equity']}

Valuation View:
Using a simple valuation reference, the implied upside is approximately
{fmt_pct(decision['valuation_upside_pct'])}. This provides a rough sense of
valuation rather than a precise estimate.

Risk View:
Overall risk is assessed as {decision['risk_level']}. The main risks relate 
to continued investment intensity and regulatory exposure. These risks do not
break the case, but argue against an aggressive position.

Investment View:
{decision['recommendation']} ({decision['conviction']} conviction)

What supports this view:
{decision['rationale']}

Key Drivers:
{drivers_text}

This memo is generated automatically using public market data and a transparent
set of decision rules. It is intended to support discussion rather than replace
deeper valuation work or analyst judgement.
""".strip()

    # ---------------- Run Agent ----------------

    def run(self, output_path: str) -> str:
        """
        Execute the full agent workflow and write the output memo to disk.
        """
        data = self.fetch_market_data()
        valuation_upside = self.estimate_valuation_upside(data["trailing_pe"])
        risks = self.assess_risk(data["sector"])
        decision = self.make_recommendation(data, valuation_upside, risks)

        memo = self.generate_investment_memo(data, decision)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(memo)

        return memo

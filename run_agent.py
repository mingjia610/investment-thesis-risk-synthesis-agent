from agent.thesis_risk_agent import InvestmentThesisRiskAgent


def main():
    agent = InvestmentThesisRiskAgent(
        policy_path="data/valuation_inputs.json"
    )

    memo = agent.run(
        output_path="outputs/sample_investment_memo.txt"
    )

    print(memo)


if __name__ == "__main__":
    main()

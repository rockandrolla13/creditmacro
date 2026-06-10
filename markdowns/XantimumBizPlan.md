Business Plan Details for Xantium: Systematic Spread Fixed Income Trading 

Andreas Koukorinis 

April 11, 2024 

1 

## **Contents** 

|**1**|**Introduction**|**Introduction**|**3**|
|---|---|---|---|
|**2**|**Uniqueness of the Business**||**5**|
||2.1|Why is this business unique?<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . .|5|
||2.2|What is the diferentiator versus similar businesses?<br>. . . . . . . . . . . . . . . .|5|
|**3**|**Strategy Details**||**6**|
||3.1|Questions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|6|
||3.2|Strategy signals components . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|7|
||3.3|Typical Types of Technical Signals . . . . . . . . . . . . . . . . . . . . . . . . . .|7|
|||3.3.1<br>Example of a CTL trade . . . . . . . . . . . . . . . . . . . . . . . . . . . .|9|
||3.4|Instrument Usage . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|10|
|**4**|**Trade Sizing**||**11**|
||4.1|Questions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|11|
||4.2|Criteria for Trade Construction . . . . . . . . . . . . . . . . . . . . . . . . . . . .|11|
||4.3|Sizing<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|11|
|**5**|**Risk **|**Management**|**13**|
||5.1|Questions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|13|
||5.2|Portfolio Construction Principles . . . . . . . . . . . . . . . . . . . . . . . . . . .|13|
||5.3|Liquidity<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|13|
||5.4|Risk Decomposition<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|14|
|||5.4.1<br>Structural Risk . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|14|
|||5.4.2<br>Market Risk . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|14|
||5.5|Specifc Risk Mitigation Strategies . . . . . . . . . . . . . . . . . . . . . . . . . .|14|
||5.6|Key Risks Managed<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|14|
|||5.6.1<br>Potential Adverse scenarios . . . . . . . . . . . . . . . . . . . . . . . . . .|15|
||5.7|Cutting Risk/ Stop Losses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|15|
|||5.7.1<br>Optimal Risk Retention Determination<br>. . . . . . . . . . . . . . . . . . .|15|
|||5.7.2<br>Adjustment Based on VaR-Derived Risk sizing . . . . . . . . . . . . . . .|15|
|||5.7.3<br>Dynamic Stop-Loss . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|15|
|||5.7.4<br>Correlation Stop-Loss<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . .|15|



2 

## **1 Introduction** 

This proposal outlines the creation of a systematic trading team to leverage the ETF ecosystem to trade relative value and cross-asset signals **with a primary focus on liquid credit** ( with an overlay of listed equity options and interest rate instruments). 

The create/redeem framework allows for a clear outlay of bond positions (reducing the dependency on dealers), and also expertise allows for taking advantage of episodic trades and dislocations. 

The starting point for the strategy is to define the eligible universe of instruments. The strategy is based on the following assumptions/guardrails: 

1. ETFs have volatile flows, that tend to have _memory_ in the medium term (i.e momentum). This is likely because ETFs are characterized by large differences between the clienteles trading the ETF shares vs the underlying bonds. 

2. Liquidity preservation; Binding constraints include: 

   - (a) Time to exit [50%] the position without P&L impact greater than the bid/offer spread. 

   - (b) Absolute P&L cost of exiting [50%] of the position at market levels. 

   - (c) Ability to exit minimum of [75%] of book within a predefined amount of volume traded. That translates into trading days. 

3. The ETF- eligible universe of instruments offers a layer of liquidity to the underlying securities. Even if the underlying holdings are thinly traded or relatively illiquid, the ability to transact in them indirectly through the ETF creation/redemption mechanism can make it easier to establish and unwind positions, than just directly in the market. The ETF acts as the conduit for channeling liquidity to the underlying instruments. 

ETF flows (creation and redemption activities) are symptomatic of non-fundamental demand shocks, which cause deviations in asset prices from their fundamental values. These flows are a response to violations of the law of one price between an ETF and its underlying assets, with APs playing a crucial role in correcting these discrepancies. 

The trading process, while comprehensive, aims for simplicity and liquidity: 

1. Process must be repeatable / machine-like: systematic evaluation of RV and cross asset opportunities 

2. Asymmetric risk-reward trades with pre-defined downsides 

3. Probability analysis across different states of the world 

- (a) We plan to leverage a proprietary liquidity-based framework. Liquidity playing a crucial role in determining the trading universe and trade structuring. 

- (b) The systematic algorithms for bonds will be tailored to the unique market structure of each bond asset class. 

The competitive advantage comprises three elements: 

- (a) Identifying macro bias-driven dislocations and liquidity gaps. 

- (b) Effective portfolio and position construction. 

- (c) Superior management of liquidity and risk. 

3 

We aim to implement two substrategies exploiting differing volatility profiles. 

- (a) Micro RV trades looking to exploit market dislocations and neutralise most of market risk factors, and is balance sheet intensive. 

- (b) Macro RV takes non-market-directional risk to make relative value strategies scalable or to express systematic macro signals, and is not balance sheet intensive. 

We’ll adopt a robust, top-down, algorithmic approach for medium to long-term strategies, and for the development of the tactical component. A key challenge we aim to address is defining relationships between correlated instruments, given most risk is lower-order. We acknowledge the remaining curve or basis risk after the duration and spread of the hedging, and the longer holding. 

|**Category**|**Description**|
|---|---|
|||
|Strategy|Strategy seeks to integrate actively risk management and<br>largely market neutral spread relative value and diversifed<br>global macro-thematic views into a single strategy.|
|||
|Strategy scope|Spread curve, L/S (cash vs. cash or derivs),ETF-cash basis<br>(ETF-induced statistical arbitrage), equity volatility, macro-<br>Credit relative strategies, EM sovereigns.|
|||
|Strategy<br>difer-<br>entiator|I seek to leverage technical profciency in relative value spread<br>trading, in a highly diversifed approach to alpha generation<br>that combines the understanding of global macro drives for<br>spread and yield products and a strong risk management and<br>portfolio construction approach.|



- Key Points: 

   - Appropriately aligning position, sizing, and holding periods with the risk reward of the opportunity. 

   - Managing downside risks with a strong emphasis. 

   - Utilizing approximately 3 – 4 quant themes for trading. 

   - Strategies’ holding periods ranging from intraday to multiple-week maximum. 

   - Implementation of active tail risk hedging techniques. 

   - Hard Cap on number of positions and complexity of the books. 

4 

## **2 Uniqueness of the Business** 

## **2.1 Why is this business unique?** 

The trading process aims for simplicity and liquidity, leveraging a proprietary liquidity-based framework. Liquidity plays a crucial role in determining the trading universe and trade structuring. The systematic algorithms for bonds are tailored to the unique market structure of each bond sub-class. 

The competitive advantage comprises three elements: 

- Identifying macro bias-driven dislocations and liquidity gaps. 

- Effective portfolio and position construction. 

- Superior management of liquidity and risk. 

The strategy implements three groups of strategies exploiting differing volatility profiles and has the potential for a future quant-mental overlay. 

## **2.2 What is the differentiator versus similar businesses?** 

1. _Exploiting ETF-specific inefficiencies:_ The strategy directly exploits potential mispricing between corporate bond ETFs and their underlying baskets, harnessing an additional source of alpha not accessible to cash bond-only credit strategies. 

2. _Utilizing ETF creation/redemption mechanism:_ The strategy uses the ETF create/redeem mechanism to capture pure arbitrage profits when the ETF and its basket trade out of sync. 

3. _Exploiting Non-Fundamental Demand Shocks:_ The strategy focuses on exploiting nonfundamental demand shocks, often overlooked by traditional credit strategies, by leveraging ETF flows as a novel signal to identify short-term mispricing. 

4. _Integration of sub-strategy signals:_ The strategy utilizes a diverse set of signals to identify relative mispricing, generating a novel source of alpha. 

5. _Orthogonal to credit beta:_ The core strategy is market-neutral between the ETF and its underlying basket, offering pure relative value alpha largely orthogonal to credit beta. 

6. _Liquidity and cost efficiency:_ Trading the ETF leg offers a more liquid, cost-efficient alternative to trading a full replicating basket of bonds, mitigating the largest drag on long-short credit strategies. 

7. _Explicit short option risk management:_ The strategy directly models and manages the ”short gamma” risks from APs and ETF investors via the unencumbered cash buffer, a unique aspect of the ETF structure. 

5 

## **3 Strategy Details** 

## **3.1 Questions** 

1. How many components to your main strategy? 

2. What types of signals do you use? 

3. Can you take advantage of episodic trades? 

4. What type of sub-strategies do you use? 

5. what instruments will you use and which ones are day one? 

The aim to implement sub-strategies exploiting differing profiles. 

- (a) Medium-term strategy with a potential for a future quant-mental overlay. This is an expression of directional trading combines macro fundamental views with quantitative analysis to time trends in the market, and is not balance sheet intensive. 

- (b) Micro RV trades looking to exploit market dislocations and neutralise most of market risk, factors, and is balance sheet intensive. 

   1. ETF 1 vs. ETF 2. 

   2. Bond Basket/Portfolio vs. ETF. 

   3. Bond Basket/Portfolio vs. Index/Single Name CDS/Equity Option. 

   4. Long Short Bond RV. 

Episodic Trades: Having such ETF infrastructure allows us to have access to episodic trades, such as: 

   1. _Create to Lend_ By monitoring short interest, lending fees, and supply-demand dynamics in real-time, one can identify optimal opportunities for lending and borrowing to maximize returns. Additionally, tailored lending solutions are offered based on borrowers’ specific needs and the unique attributes of ETFs. Factors such as composite borrowing costs and associated risks with borrowing ETF constituents are taken into account. 

   2. _Block Trading on ETF_ 

- (c) Macro RV takes non-market-directional risk to make relative value strategies scalable or to express macro views, and is not balance sheet. Suggested types: 

   1. Credit CDS Index vs. ETF (basis) 

   2. Credit CDS Index 1 vs. Credit CDS Index 2 (long short/ compression/decompression). 

   3. Credix Index Vol vs. ETF Vol. 

   4. Swap Spreads or EGB Spreads vs. Credit Index. 

intensive. 

We’ll adopt a robust, top-down, algorithmic approach for medium to long-term strategies, and for the development of the tactical component. A key challenge we aim to address is defining relationships between correlated instruments, given that most risk is lower-order. We acknowledge the remaining curve or basis risk after the duration and spread of the hedging and the longer hold. 

6 

- **Identify Mispricings:** Relative value is not enough! Use ETF flows (and index flows) to identify mispriced assets within the eligible universe, where **non-fundamental driven demand/supply** may have caused deviations. 

- **Optimize Create-and-Redeem Activities:** Strategically execute create-and-redeem activities to exploit the identified mispricings, adjusting the portfolio’s exposure to credit instruments accordingly. 

- **Risk Management:** Incorporate the understanding of nonfundamental demand shocks into the fund’s risk management framework, recognizing that these shocks can lead to temporary but significant price distortions. Please see section on risk management 5 

- **Return Predictability:** Leverage insights on return predictability based on ETF flow patterns to make informed decisions on the timing of entry and exit from credit positions. 

## **3.2 Strategy signals components** 

We look at the following implementations of ”sub-strategies”: 

1. Long - short. 

2. Debt vs. Equity (inclusive of Sub/SNR). 

3. Government Risk versus. Corporate Credit Risk. 

4. Cash versus Derivative. 

5. Term-Structure. 

Flexibility allows us to express these sub-strategies within the same framework. Below I provide a small sample of types of signals. 

## **3.3 Typical Types of Technical Signals** 

An indicative simple list of types of signals that will be utilised 

## **Factor- Driven Signals** 

Here is a stylized example of a signal that seeks to exploit short-term pricing inefficiencies between corporate bond ETFs and their baskets that are identified by the a subset of specified style factors, while managing risk through an ETF creation/redemption arbitrage approach. It combines elements from the ETF arbitrage, style factor investing, and risk management principles. NB: This is a stylised example, not a complete set of all the factor-signals 

1. Momentum (example): 

   - 12-month minus 1-month return for US corporate bonds. 

   - 12-month minus 1-month return for European corporate bonds. 

2. Example for Value (Composite): 

   - Book-to-Price and Earnings-to-Price ratios for US bonds (as per DBUSFVLU) 

   - Book-to-Price ratio for European bonds (as per DBCGFVLU) 

   - Residual between market spread and fair value spread estimated using distance-todefault (as per general Value factor definition) 

7 

|**Document**|**Alpha Signal Description**|**Frequency**|
|---|---|---|
|Intraday Signal<br>1|- Binary signal based on historical<br>price actions and volatility patterns.<br>- Sensitivity analysis for trading<br>costs and turnover.<br>- Frequency optimization per credit<br>asset class.|Intraday|
|Intraday Signal<br>2|- Selection of patterns based on his-<br>torical performance metrics and sta-<br>tistical testing.<br>- Aggregation of selected patterns<br>into composite daily signals.<br>- Daily signal adjustment based on<br>performance evaluation.|Daily (end of day)|
|Volatility Signal|-<br>Tracking<br>deleveraging<br>in<br>high<br>volatility periods and releveraging in<br>low volatility periods (risk budget-<br>ing).<br>- Strategies are adjusted based on a<br>volatility estimate/forecast.|Quarterly, Annual|



Table 1: Sample Alpha Signal Descriptions and Frequencies 

3. Quality/Low Risk: 

   - Distance-to-default measure, excluding financials (as a fundamental quality metric) 

   - Low Duration factor: Long 3Y CDS indices / Short 10Y CDS indices 

4. Liquidity: 

   - Bond-CDS basis as a liquidity metric (more negative basis indicates lower liquidity) 

## **Example implementation of this trade** 

- The above factor signals for US and European corporate bond ETFs and their underlying baskets are monitored. 

- When factor signals indicate a relative mispricing between ETF and its basket (e.g. high momentum, expensive valuation, low quality, or wide CDS basis in ETF vs basket), put on the arbitrage: 

   - (1) If ETF is rich vs basket, short the ETF, long the underlying corporate bonds, and create ETF shares to lock in the arbitrage. 

   - (2) If basket is rich vs ETF, buy the ETF, short the underlying corporate bonds, and redeem ETF shares. 

- Size rel-val/arb positions based on strength of factor signals, while keeping unencumbered cash above the designated risk limit. 

- Optimize leverage and risk allocation between the factor signals/arbitrage positions to maximize risk-adjusted returns. 

- Manage potential risks from factor tilts using sector-neutral positioning where needed. 

8 

- Monitor shifts in key risk measures like volatility, skew, bond-CDS basis, and ETF premium/discount to adjust leverage. 

- Unwind arbitrage positions as relative mispricing dissipates and factor spreads normalize. 

## **3.3.1 Example of a CTL trade** 

1. Utilize the ETF creation mechanism to generate new shares for lending: 

   - When an ETF’s lending fees are significantly higher than the weighted average cost of its underlying securities, use the ETF creation process to generate new ETF shares. 

   - Lend out these newly created shares to capture the higher lending fees 

2. Manage risks associated with the CTL strategy: 

   - Monitor liquidity and borrowing costs of the ETF’s underlying securities 

   - Ensure the ETF creation and redemption process is functioning efficiently to avoid getting stuck with ETF shares that can’t be redeemed. 

   - Dynamically adjust the size of CTL positions based on changes in demand and market conditions. 

   - Incorporate the CTL strategy into the overall risk management framework, considering factors like unencumbered cash, funding options, and redemption options. 

3. Exploit the structural inefficiencies in the ETF loan market: 

   - Take advantage of the regulatory restrictions on investment companies’ ownership of ETFs, which limits the supply of lendable shares. 

   - Benefit from the higher lending fees and lower price elasticity of ETFs compared to individual bonds. 

4. Complement the core ETF arbitrage strategy: 

   - Use the CTL strategy to generate additional alpha during periods of high borrowing demand and dislocations in the ETF loan market. 

   - Combine insights from the ETF arbitrage signals (e.g., flow, momentum, value) with the CTL opportunity set. 

   - Dynamically allocate risk capital between the ETF rel-val and CTL strategies based on market conditions and relative attractiveness. 

9 

## **3.4 Instrument Usage** 

Proposed list of instruments. No Level 3 instrument usage. 

|Instrument|Currency|Region|Day One Use?|
|---|---|---|---|
|CDS|EUR|EMEA|Yes|
|Bond|EUR|EMEA|Yes|
|ETF|EUR|Europe|Yes|
|CDS|USD|USA|No|
|CDS|USD|USD|No|
|Credit Index|EUR/USD|Global|Yes|
|Equity Vol|EUR/USD|Global|No|
|Futures|EUR/USD|Global|Yes|



Table 2: Instrument Usage 

10 

## **4 Trade Sizing** 

## **4.1 Questions** 

1. How do you construct positions? 

2. How do you construct the portfolio? 

3. How do you size positions? 

## **4.2 Criteria for Trade Construction** 

- Focus on structuring trades with pre-defined risks (prioritizing over the strength of conviction). 

- Determine the expected time for thesis validation (the period before the trade thesis is proven right or wrong). 

- Evaluate the base-case P&L in comparison to the expected worst-case scenario. 

- Consider liquidity costs in the event of a forced exit from a position. 

- Take into account the perceived positioning of other market participants through indexation. 

- Adhere to VaR and other risk limits as part of trade construction. 

- Analyze the relationship of the trade with the rest of the portfolio. 

- Assess mark-to-market P&L volatility associated with the trade. 

- Establish and exploit natural hedges for positions when available. 

- Consistently re-balance and re-evaluate every position in the portfolio, focusing on value extraction. 

- Utilize robust proprietary technology for comprehensive and exhaustive real time monitoring and review. 

## **4.3 Sizing** 

Broadly speaking an adapted variation of ”fractional Kelly” strategy, adjusting capital allocation to manage risk exposure effectively. 

gradient-based algorithms for optimizing the allocation of stakes across multiple simultaneous bets to maximize the expected log-utility (Kelly criterion). The algorithms can handle a large number of bets and converge quickly to the optimal solution. 

Key points on bet sizing using two specific algorithms: 

1. The algorithms optimize the trade sizes based on the expected utility, considering the probabilities and odds of each trade. 

2. The ”na¨ıve” algorithm ignores the constraint on total trades and rescales the sizes if necessary, while the ”constrained” algorithm enforces certain constraints. 

3. When the number of bets is small and the total stake is less than 100% of the allocated, the optimal stakes are closely proportional to the fractional Kelly stake for each bet individually. 

11 

4. As the number of bets increases and the total stake approaches 100% of the bankroll, the optimal stakes deviate from individual fractional Kelly stakes and are more related to the ”edge” (difference between actual and implied probabilities) of each bet. 

5. The algorithms can handle bets with multiple outcomes and can be adapted to different utility functions. 

The algorithm determines the optimal allocation of the capital across the trades, considering the probabilities, and the overall expected utility. This approach allows for the simultaneous optimization of multiple bets while managing risk through diversification and the ”fractional” Kelly criterion. 

12 

## **5 Risk Management** 

## **5.1 Questions** 

1. How do you risk manage? 

2. What scenarios can cause a draw-down in the strategy? 

3. How do you cut risk? 

4. How do you add risk? 

5. What are periods of portfolio stress/value declines that the strategy could suffer? How would you hedge them? 

I believe that the most effective way to manage risk is through trade and portfolio construction rather than relying solely on stop loss discipline. 

## **5.2 Portfolio Construction Principles** 

The distribution of risk should be explicitly tied to: 

- (a) Quantitative Conviction of views, based on ranking of themes and risk factors. 

- (b) Potential for delivering asymmetric risk/reward payoffs. 

- (c) Overall risk tolerance and profile. 

Portfolio characteristics should include: 

- Asymmetric option-like payouts. 

- Negative correlation with ”risk assets” during market declines and low correlation during market upswings. 

- Diversified expressions, providing multiple sources of alpha. 

Main considerations: 

1. Liquidity 

2. Market Risk and Structural Risk 

## **5.3 Liquidity** 

_Liquidity_ refers to the **ability of converting a position into cash efficiently and at minimal cost** . It is often determined by the level of trading activity. 

- Trade only instruments with favorable liquidity attributes, considering both cost and time factors. 

- Key characteristics of a portfolio comprising eligible instruments: 

   - Ability to exit at least 80% of the portfolio within 15-20 trading days, regardless of market conditions. 

   - Imposing a cap on the absolute P&L cost to exit half the position at prevailing market levels. 

   - Setting a maximum time limit to exit half the position while maintaining a predefined P&L impact (e.g., 1.5 times the standard bid-offer cost). 

13 

- A proprietary ranking methodology assesses the potential instrument universe based on an observable scoring mechanism. This mechanism incorporates inputs such as: 

   - Frequency of trading activity for the instrument. 

   - Trade volume associated with the instrument. 

   - Number of clearing participants involved. 

   - Associated costs related to trading the instrument. 

   - Volatility of market movements related to the instrument. 

## **5.4 Risk Decomposition** 

We break down returns into two components: Market Risk and Structural Risk. This categorization helps in understanding the multifaceted nature of risk within our strategy and guides our risk management practices. 

## **5.4.1 Structural Risk** 

In this bucket, we consider **Three** types of risk: tail risk, funding risk, and investor redemption risk. The structural obligations – redemption and funding – are viewed as two out-of-the-money options, highlighting the importance of managing mismatches between investment horizons and funding terms. Liquidity risk, a fundamental metric in our strategy, is measured by assigning a number that ties it to the cost and time of exit, with pre-set limits on both to ensure robust risk management. 

## **5.4.2 Market Risk** 

Market risk management involves maintaining a long gamma bias in the portfolio, hard capping the number of positions to ensure diversification, and structuring trades with pre-defined and limited risk. We prioritize risk containment over the strength of conviction, avoiding crowded trades through market intelligence, and sizing trades based on market impact in a ”worst-case” scenario and exit liquidity. 

## **5.5 Specific Risk Mitigation Strategies** 

- For Relative Value (RV) trades, we pay some of the carry earned in being short liquidity to buy long liquidity/long volatility positions when inexpensive. 

- Gain exposure to multiple alpha factors via a single trade where possible, understanding reasons for pricing anomalies and how they may evolve. 

- Incorporate positions with specific, structural exit points and implement specific stop-loss triggers on every trade. 

## **5.6 Key Risks Managed** 

Our strategy is tailored to manage several key risks, including: 

- Valuation risk: Mispricing between ETF and underlying bonds fails to converge. 

- Liquidity risk: Inability to unwind positions due to deteriorating market liquidity. 

- Timing risk: Profit potential eroded by cost of carry as convergence is delayed. 

- Mark-to-market risk: Adverse price moves generate losses before convergence. 

14 

- Volatility risk: Outsized price swings, especially when short gamma (from ETF options). 

By identifying the short options within the ETF structure and using risk capital without any restrictions, our strategy effectively balances risk and return. This disciplined approach to risk management, influenced by insights from ETF and credit markets, reduces left-tail liquidation risk for APs and investors while taking advantage of non-fundamental demand shocks indicated by ETF flow.s. 

## **5.6.1 Potential Adverse scenarios** 

The main two scenarios that these set of strategies can underperform are related to : 

1. Market degrossing, whereas the market is trying to actively reduce gross exposure. 

2. Funding conditions change dramatically (similar to 2008). 

Below is a more detailed scenario that is taken into consideration when managing risk. 

## **5.7 Cutting Risk/ Stop Losses** 

Individual Stop-Losses are VaR-Based Stop-Loss with an influence of the Fractional Kelly is used. **Stop-losses are implemented inclusive of liquidation cost.** 

## **5.7.1 Optimal Risk Retention Determination** 

The framework requires quantifying permissible risk exposure as a function of the Value at Risk metric. This involves calculating the maximum potential loss per a series of trades within a confidence interval, thus setting a risk threshold. This threshold defines the maximum acceptable exposure level for the algorithm and forms the basis for subsequent optimization processes within the trading strategy. 

## **5.7.2 Adjustment Based on VaR-Derived Risk sizing** 

After determining the initial allocation using the fractional Kelly criterion, an adjustment phase follows. This involves incorporating the risk parameters identified from the VaR analysis. This re-calibration ensures that the amount of capital deployed aligns with the defined risk appetite by integrating a risk management perspective into the allocation process. 

## **5.7.3 Dynamic Stop-Loss** 

A dynamic stop-loss mechanism, based on the VaR-derived risk threshold, is implemented as a key part of the strategy. This protocol involves setting an exit threshold for trades, guided by the initial risk assessment, in order to proactively limit losses by ending positions that exceed the set risk parameters. This method helps in safeguarding capital by reducing the impact of unfavorable market movements. **No position has a stop loss wider than 2x its historical VAR** 

## **5.7.4 Correlation Stop-Loss** 

Additional Sizing of the portfolio is carried out so it can withstand 10% Correlation Shock (i.e. both longs and shorts shocked in an adverse fashion and there is a cap on the sum of the losses). 

15 

|**Scenario**|**Description**|**Risk Mitigation**|
|---|---|---|
|Increased<br>Margin<br>Re-<br>quirements<br>or<br>Withdrawal<br>of<br>Credit Lines|Prime brokers might signifcantly in-<br>crease margin requirements or po-<br>tentially withdraw their credit lines<br>during crises.|Maintain<br>diversifed<br>funding<br>sources;<br>establish<br>robust<br>liquid-<br>ity bufers.|
|Large-scale<br>Redemptions by<br>Investors|Investors may withdraw capital dur-<br>ing credit crises, increasing the risk<br>of large-scale redemptions.|Implement<br>gates<br>and<br>lock-ups;<br>maintain a liquidity reserve.|
|Exercise<br>of<br>Funding<br>and<br>Redemption<br>Options|Contractual agreements with prime<br>brokers and investors may force the<br>hedge fund to reduce leverage in bad<br>states of the world.|Carefully manage leverage and un-<br>encumbered cash levels; diversifed<br>investor base.|
|Poor<br>Per-<br>formance<br>or<br>Macroeconomic<br>Developments|Either due to poor performance or<br>independent macroeconomic devel-<br>opments, there can be a high prob-<br>ability of short option exercise.|Dynamic<br>hedging<br>strategies;<br>macroeconomic sensitivity analysis.|
|Mismatch<br>between Invest-<br>ment<br>Horizon<br>and<br>Funding<br>Term|Mismatch causes signifcant risks,<br>necessitating careful management.|Align<br>investment<br>horizons<br>with<br>funding terms; continuous liquidity<br>assessment.|
|Unanticipated<br>Increase<br>in<br>Margin<br>Re-<br>quirements|A sudden increase by prime brokers<br>can result in a need for deleveraging,<br>often involuntarily.|Pre-emptive risk management; sce-<br>nario analysis and stress testing.|
|NAV<br>Trigger<br>Breaches|Major redemptions or draw-downs<br>may force the fund into involuntary<br>deleveraging.|Set conservative NAV triggers; in-<br>crease communication with prime<br>brokers.|
|Market<br>Shifts<br>Between<br>Well-<br>Understood<br>Paradigms|Best environment - volatility with<br>liquid trading.|Reduce portfolio directionality; in-<br>crease liquidity in trades.|
|Range-Trading<br>Markets|Risk of ”Whip-Saw” in markets.|Implement tight stop losses; adjust<br>trade sizes according to volatility.|
|Unexpected<br>Turn of Events|Worst-case scenario due to exoge-<br>nous developments.|Explicit focus on downside risk; re-<br>duce exposure rather than risk los-<br>ing.|



Table 3: Potential Scenarios, Descriptions, and Risk Mitigations for Hedge Fund Strategies 

16 


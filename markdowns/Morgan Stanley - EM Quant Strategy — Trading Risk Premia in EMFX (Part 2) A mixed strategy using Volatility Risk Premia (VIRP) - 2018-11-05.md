_November 5, 2018 07:00 AM GMT_ 

## **EM Quant Strategy | North America** 

## Trading Risk Premia in EMFX (Part 2): A mixed strategy using Volatility Risk Premia (VIRP) 

By complementing our two-factor model with a Vol Risk Premia approach, we manage to generate excess returns in a consistent manner (via backtesting). Our VIRP strategy beats relevant Benchmarks (EM Carry and GBI EM LC) in absolute and vol-adjusted returns and serves as a tool to detect EM trends. 

- **Our new Volatility Risk Premia model (VIRP) beats our initial two-factor model approach (IRP)** (Exhibit 1). The mixed strategy (VIRP) works as the strategies (idiosyncratic risk premia: IRP and VRP) are complementary. The IRP tends to offset VRP signals once the market has overshot/undershot, as it would detect risk premia (RP) reaching extremes on either side (cheap or expensive). In addition, it would help to time better the potential reversal in FX moves once IRP reaches extremes. The VRP strategy usually extends the signals after IRP reversals as it tends to capture trends better. IRP signals would disappear once the threshold was crossed (again), but when momentum exists, that signal would be substituted later on by VRP. The model performs particularly well for MXN, ZAR, TRY, RUB, and BRL – High Betas. 

- **VIRP consistently outperforms the relevant benchmarks** (Exhibit 2). Our backtest results show that by mixing IRP and VIRP (VIRP strategy), voladjusted returns improve materially. VIRP has a Sharpe ratio of 0.99 (transaction costs included), compared to 0.71 of VRP and 0.68 of IRP. The Sortino ratio increases to 1.1 (0.94 of IRP and 0.70 of VRP). 

- **VIRP is a useful tool to detect overall trends in EM** (Exhibit 3). By filtering signals from high beta currencies, we manage to outperform the simplest buy-and-hold strategy and most EM-dedicated funds that track the GBIEM index. The intensity of the signals clearly correlates with average returns, helping to detect trends in EM in both bull and bear markets. 

_Notes: The “buy” and “sell” signals referred to in this document are purely rulebased trading strategies and only serve as an input in our decision-making framework. The performance data provided in this document is a hypothetical illustration of mathematical principles; it does not predict or project the performance of an investment or investment strategy. Past performance is no guarantee of future results_ _**.**_ 

MORGAN STANLEY & CO. LLC 

Andres Jaime 

STRATEGIST Andres.Jaime@morganstanley.com +1 212 296-5570 

QuantWise highlights research that incorporates a robust quantitative approach in our investment analysis. 

**Exhibit 1:** VIRP consistently beats the relevant benchmarks 

**==> picture [173 x 120] intentionally omitted <==**

**----- Start of picture text -----**<br>
FX Systematic Styles<br>VIRP Carry<br>1.400<br>1.300 GBI EM VIRP HB<br>1.200<br>1.100<br>1.000<br>0.900<br>0.800<br>Source: Morgan Stanley Research<br>Jan-12 Apr-12 Jul-12 Oct-12 Jan-13 Apr-13 Jul-13 Oct-13 Jan-14 Apr-14 Jul-14 Oct-14 Jan-15 Apr-15 Jul-15 Oct-15 Jan-16 Apr-16 Jul-16 Oct-16 Jan-17 Apr-17 Jul-17 Oct-17 Jan-18 Apr-18 Jul-18 Oct-18<br>**----- End of picture text -----**<br>


**==> picture [183 x 107] intentionally omitted <==**

**----- Start of picture text -----**<br>
Exhibit 2: VIRP and benchmarks' main stats<br>VRP IRP VIRP VIRP HB Carry GBI EM (LC)<br>Average Return(annualized) 1.24% 0.70% 1.96% 4.67% 0.32% 0.15%<br>i Median 1.60% 0.00% 1.63% 1.81% 0.22% 1.43%<br>a Vol 1.75% _ 1.03% 1.98% 4.77% 4.85% 9.99%<br>Downside Vol 1.76% 0.74% 1.78% 4.01% 4.69% 10.47%<br>Upside Vol 1.74% 1.58% 2.16% 5.57% 4.98% 9.48%<br>PC Max DD le -3.84% -3.07% -3.50% -7.96% -13.69% a -31.22%<br>Sharpe Ratio 0.71 0.68 0.99 0.98 0.07 0.01<br>| Sortino Ratio 0.70 0.94 ee 1.10 1.16 0.07 0.01<br>Correlation to EM 9.36% 16.84% 17.07% 18.54% 6.69% 100.00%<br>Correlation to S&P 1.59% 17.52% 10.51% 10.78% 7.98% 38.83%<br>| Cs a<br>Source: Morgan Stanley Research<br>**----- End of picture text -----**<br>


**Exhibit 3:** VIRP is a useful tool to detect overall trends in EM 

**==> picture [160 x 109] intentionally omitted <==**

**----- Start of picture text -----**<br>
340<br>320<br>300<br>280<br>260<br>240<br>220<br>Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>Buy Signal Sell Signal GBI-EM<br>Source: Morgan Stanley Research<br>**----- End of picture text -----**<br>


Morgan Stanley does and seeks to do business with companies covered in Morgan Stanley Research. As a result, investors should be aware that the firm may have a conflict of interest that could affect the objectivity of Morgan Stanley Research. Investors should consider Morgan Stanley Research as only a single factor in making their investment decision. 

For analyst certification and other important disclosures, refer to the Disclosure Section, located at the end of this report. 

1 

## EMFX Volatility Risk Premia (VRP) 

## Definition and findings on EMFX Volatility Risk Premia 

Della Corte, Ramadorai, and Sarno (see Volatility Risk Premia and Exchange Rate Predictability, December 2013) show that **volatility risk premium (VRP)** – defined as the difference between expected future volatility and a model-free measure of implied volatility derived from currency options – **has substantial predictive power for the cross-section of currency returns** . This is in line with prior findings in equity markets. 

The currency volatility risk premium can be interpreted as the cost of insurance against volatility fluctuations in the underlying currency. As such, they find that **currencies with** 

**cheap volatility insurance (those with relatively low implied volatility vs realized) tend to appreciate** , while **currencies with relatively more expensive volatility insurance predictably depreciate.** The predictive power of VRP is specifically related to future variations in spot FX returns, not to interest rate differentials. 

In addition, they argue that a comprehensive set of standard risk factors is unable to explain VRP returns, suggesting that these returns are not generated on account of compensation for systemic risk. 

One explanation for which they manage to find evidence is that **time-variation in limits to arbitrage causes volatility insurance cost to fluctuate across time and currencies, having an impact in the spot market as risk-averse currency hedgers become reluctant to take or hold positions in expensive-to-insure currencies.** They find evidence that conditional variance in the currency options market predicts conditional variance in the underlying currency spot markets. 

## Backtesting VRP strategy in EMFX 

## Construction of VRP strategy (portfolios) 

In order to test the predictive power of VRP, we conduct a backtest for 17 EM currency pairs, all measured against the USD. Our selection encompasses the same sample utilized in EM Quant Strategy: Assessing Risk Premia in EMFX (Part 1): A Two-Factor Model Approach (5 Jun 2018). 

To construct our measure of VRP, we use 1y ATM implied volatility in options of each pair vs the USD (using Bloomberg prices) and compare it with 1y realized volatility of spot. In other words, our proxy for VRP = 1y realized vol - 1y option implied vol. 

2 

Once we have our proxy for VRP at the end of each period t (measured in weeks), we construct two portfolios: 

- **Short Portfolio.** Currencies with the highest VRP (20% percentile), i.e., Expensive volatility insurance – relatively high implied vs realized 

- **Long Portfolio.** Currencies with the lowest VRP (80% percentile), i.e., Cheap volatility insurance – relatively low implied vs realized 

We take **signals** from the model at the end of day of each Friday. We calculate **excess returns** at the maturity of each transaction by comparing prices of 1w forward at Monday's fixing vs settlement price at expiration. We assume **transaction costs** of 0.0075% per trade. 

## Backtesting Results 

In line with Della Corte et al., the strategy yields positive returns, supporting the idea that a VRP strategy provides predictive power for the cross-section of currency returns. In our out-of-sample backtest (using weekly data since January 2012), the strategy produces an average annualized return of 1.24% in USD terms and an annualized volatility of 1.75% - with similar conditional volatility on above and below average returns. This results in a Sharpe and Sortino ratio of 0.71 and 0.70 respectively. The max drawdown of the strategy is -3.84%. 

The strategy outperforms the GBI-EM index over the specified period in addition to other common strategies such as carry (see Exhibit 4). 

**Exhibit 4:** EM VRP strategy Index 

Model performance (Excess Return in USD) 

**==> picture [300 x 201] intentionally omitted <==**

**----- Start of picture text -----**<br>
1.12<br>VRP<br>1.10<br>1.08<br>1.06<br>1.04<br>1.02<br>1.00<br>0.98<br>0.96<br>Jan-12 Aug-12 Mar-13 Oct-13 May-14 Dec-14 Jul-15 Feb-16 Sep-16 Apr-17 Nov-17 Jun-18<br>**----- End of picture text -----**<br>


**Source** : Morgan Stanley Research 

3 

## VIRP Strategy: Volatility & Idiosyncratic risk premia 

## Idiosyncratic risk premia (IRP) strategy backtest 

In EM Quant Strategy: Assessing Risk Premia in EMFX (Part 1): A Two-Factor Model Approach (5 Jun 2018), we developed a framework to detect extreme pricing in EM pairs. To do so, we implied idiosyncratic risk premia (IRP) in EMFX by filtering each USDEMFX pair variance with two global factors - USD and carry (the carry factor being is voladjusted carry strategy returns, not interest differentials). 

**Exhibit 5:** IRP vs VRP Strategies 

**==> picture [221 x 122] intentionally omitted <==**

**----- Start of picture text -----**<br>
Model performance (Excess Return in USD)<br>1.11 VRP IRP<br>1.06<br>1.01<br>0.96<br>Jan- 12 Aug- 12 Mar- 13 Oct- 13 May- 14 Dec- 14 Jul- 15 Feb- 16 Sep- 16 Apr- 17 Nov- 17 Jun- 18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

The IRP strategy takes a long position vis-à-vis the USD in the underlying currency when IRP is high and a short position when IRP is low. IRP is defined as the difference between the 6m cumulative model estimated return and 6m USDEMFX pair return. In other words, the model fades extreme underperformance of EMFX vs our model on either side - long when it is "cheap", short when "expensive" 

We defined our thresholds by maximizing the Sharpe ratio of the strategy prior to 2012, which resulted in a ratio (IRP/ Std. Dev. of residuals) of 1.4 and -1.5 for short and long positions respectively. The asymmetric thresholds reflect the skew in USD/EMFX returns. 

**Our backtest suggests that the IRP strategy generates decent returns - when adjusted by vol - and does manage to correctly predict extremes.** Since 2012, it yielded a 0.70% annualized return with a volatility of 1.03%, resulting in a Sharpe ratio of 0.68. As expected, the downside volatility is much lower than the upside (as it fades extremes), generating a Sortino ratio of 0.94. The max drawdown of the strategy is -3.07% (Exhibit 7). The backtest uses the same parameters (including transaction costs) as in VRP. 

However **,** it has two main drawbacks: 

**1.** It usually fades extremes too soon, resulting in unnecessary losses. 

**2.** It fails to capture the potential trend of a subsequent correction, incurring relatively high opportunity costs. 

In other words, while the strategy does tend to correctly predict turnarounds, it fails to trade them correctly in order to generate higher returns. 

In addition, the frequency of the signals is quite low, failing to provide enough information during "normal" turnarounds in EMFX individual performance. This feature arises as, by construction, the model was designed to detect "extreme" pricing in EMFX. 

4 

## Volatility and idiosyncratic risk premia (VIRP) strategy 

The volatility and idiosyncratic risk premia strategy (VIRP) adds up the signals from VRP and IRP in order to produce a single set of signals to trade on a weekly basis. The signals are aimed to be complementary and to mitigate the drawbacks of each of the individual strategies. In order to test this, we conducted a backtest using weekly data since early 2012 (our out-of-sample dataset). The same parameters as in the prior backtests were used. 

**Exhibit 6:** VIRP Strategy outperforms the individual strategies FX Systematic Styles 

**==> picture [234 x 125] intentionally omitted <==**

**----- Start of picture text -----**<br>
VIRP Carry<br>1.400<br>1.300 GBI EM VIRP HB<br>1.200<br>1.100<br>1.000<br>0.900<br>0.800<br>Jan-12 Apr-12 Jul-12 Oct-12 Jan-13 Apr-13 Jul-13 Oct-13 Jan-14 Apr-14 Jul-14 Oct-14 Jan-15 Apr-15 Jul-15 Oct-15 Jan-16 Apr-16 Jul-16 Oct-16 Jan-17 Apr-17 Jul-17 Oct-17 Jan-18 Apr-18 Jul-18 Oct-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

**VIRP consistently outperforms the relevant benchmarks.** Our backtest results show that by mixing IRP and VIRP (VIRP strategy), the return is enhanced not only in absolute terms, but also proportionally to the increase in the volatility of the strategy. This increases the Sharpe ratio of the strategy to 0.99, compared to 0.71 of VRP and 0.68 of IRP, while the Sortino ratio increases to 1.1 (0.94 of IRP and 0.70 of VRP). 

Since 2012, VIRP yielded on average 1.96% annualized USD returns with a 1.98% volatility after including transaction costs. In line with the IRP strategy, downside vol is lower than vol at 1.78%. 

The max drawdown of the strategy, while larger than the one in the IRP model, is still lower relative to VRP which trades more 

often (3.50% vs 3.84%). **When comparing VIRP with a vol-adjusted carry strategy and one of the main EM benchmarks (GBI EM LC), the max DD looks quite small, as the latter benchmarks have a 13% and 31% max DD, respectively** Exhibit 8 

A similar result (in Sharpe ratio terms) is achieved when trading only the liquid high beta EM currencies (high sensitivity to the USD as in EM Quant Strategy: Assessing Risk Premia in EMFX (Part 1): A Two-Factor Model Approach). By taking into account just the signals for ZAR, RUB, BRL, MXN and TRY (VIRP HB), the strategy generates much higher returns (4.67% annualized), at the expense of much higher volatility (4.77%). The Sharpe ratio is almost identical to the VIRP strategy at 0.98. 

**Exhibit 7:** VIRP and VIRP HB have the higher Sharpe and Sortino ratios 

**==> picture [235 x 149] intentionally omitted <==**

**----- Start of picture text -----**<br>
1.2<br>1.0<br>0.8<br>Sharpe Ratio<br>0.6 Sortino Ratio<br>0.4<br>0.2<br>0.0<br>VRP IRP VIRP VIRP HB Carry GBI EM (LC)<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

**Exhibit 8:** IRP and VIRP have the lowest Max Drawdown of the tested strategies 

**==> picture [237 x 152] intentionally omitted <==**

**----- Start of picture text -----**<br>
0%<br>-5%<br>-10%<br>-15%<br>-20% Max DD<br>-25%<br>-30%<br>-35%<br>VRP IRP VIRP VIRP HB Carry GBI EM (LC)<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

5 

Finally, the correlation of our strategies to the the GBI-EM and S&P are relatively low, although statistically significant (Exhibit 9). 

**Why the VIRP strategy works.** The mixed strategy (VIRP) works as both strategies **(IRP and VRP) are complementary to each other.** The IRP tends to offset VRP signals once the market has overshot/undershot, as it would detect risk premia (RP) reaching extremes on either side (cheap or expensive). In addition, it would help to better time the potential reversal in FX moves once IRP reaches extremes. The VRP strategy usually extends the signals after IRP reversals as it tends to capture trends better. IRP signals would disappear once the threshold was crossed (again), but when momentum exists, that signal would be substituted later on by VRP. 

**==> picture [249 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
Exhibit 9: VIRP strategy vs relevant benchmarks<br>VRP IRP VIRP VIRP HB Carry GBI EM (LC)<br>Average Return 1.24% 0.70% 1.96% 4.67% 0.32% 0.15%<br>(annualized)<br>ai MedianVol 1.60%1.75% _ 0.00%1.03% 1.63%1.98% 1.81%4.77% 0.22%4.85% 1.43%9.99%<br>Downside Vol 1.76% 0.74% 1.78% 4.01% 4.69% 10.47%<br>Upside Vol 1.74% 1.58% 2.16% 5.57% 4.98% 9.48%<br>REE Max DD -3.84% lClC LL -3.07% -3.50% -7.96% -13.69% a -31.22%<br>Sharpe Ratio 0.71 0.68 0.99 0.98 0.07 0.01<br>Sortino Ratio 0.70 0.94 1.10 1.16 0.07 0.01<br>Ld ee<br>Correlation to EM 9.36% 16.84% 17.07% 18.54% 6.69% 100.00%<br>| Correlation to S&P 1.59% 17.52% 10.51% 10.78% a 7.98% 38.83%<br>Source: Morgan Stanley Research<br>Note: VIRP HB strategy refers to the one that only trades high Beta currencies I.e. MXN, BRL, TRY, ZAR and<br>RUB. The ranking/selection of the High Beta currencies is by using the Beta of the USD factor in EM Quant<br>Strategy: Assessing Risk Premia in EMFX (Part 1): A Two-Factor Model Approach, (5 Jun 2018).<br>**----- End of picture text -----**<br>


In order to illustrate this, we show below how the model trades on a weekly basis. As of the week ended October 26, the IRP model was signaling to buy INR, CNY and TRY. However, the VRP model complemented the IRP in two ways (Exhibit 10). 

First, it canceled the INR initial signal (resulting in a neutral signal for VIRP), and boosted the TRY signal (resulting in a VIRP signal of 2). In the case of INR, the model helps to better time the reversal, while in TRY it adds to the signal as the currency maintains momentum. 

The rest of the VIRP signals (Exhibit 11) come mainly from VRP. 

**Exhibit 10:** VIRP: adding IRP and VRP signals 

**==> picture [250 x 129] intentionally omitted <==**

**----- Start of picture text -----**<br>
IRP<br>INR CNY TRY<br>1<br>Neutralized signals Coincident signals<br>KRW<br>COP BRL<br>ZAR MXN THB CZK<br>0 PLN<br>IDR MYR HUF ILS<br>CLP<br>RUB<br>Coincident signals Neutralized signals<br>-1<br>-1 0 1<br>VRP<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

**Exhibit 11:** Model signals on Oct 26 (active trades for the following week) 

**==> picture [246 x 166] intentionally omitted <==**

**----- Start of picture text -----**<br>
VIRP signals<br>-2 -1 0 1 2<br>MXN<br>BRL<br>COP<br>CLP<br>MYR<br>KRW<br>IDR<br>INR<br>THB<br>CNY —<br>HUF<br>RUB<br>ILS<br>TRY<br>ZAR<br>CZK<br>PLN<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

6 

## Using VIRP HB (High Beta) to detect GBI EM LC index trends 

The usefulness of VIRP HB signals doesn't stop with the systematic trading strategy of EMFX. It also helps to forecast one week ahead GBI EM LC (local currency) total returns, outperforming the simplest buy-and-hold strategy and most EM-dedicated funds that track the GBI-EM index (excluding transaction costs). 

First, we construct an index that consists of the net number of Long/Short signals at the end of each week extracted from our VIRP model, but only reading signals from High Beta currencies (VIRP HB), i.e., MXN, BRL, TRY, ZAR, and RUB. The ranking/selection of the High Beta currencies set is achieved by using the Beta of the USD factor in EM Quant Strategy: Assessing Risk Premia in EMFX (Part 1): A Two-Factor Model Approach, (5 Jun 2018). We take only positive or negative signals, i.e., we do not take into account the intensity of the signal to avoid noise stemming from idiosyncratic behaviour in a particular High Beta (Exhibit 12). 

**Exhibit 13:** VIRP HB as a tool for GBI EM LC benchmarked investors 

**==> picture [509 x 160] intentionally omitted <==**

**----- Start of picture text -----**<br>
Exhibit 12: VIRP HB Index Exhibit 13: VIRP HB as a tool for GBI EM LC benchmarked investors<br>Net Long/Short High Beta<br>GBI-EM MS<br>5 1.3<br>4 1.3<br>3 1.2<br>2 1.2<br>1 1.1<br>0 1.1<br>1.0<br>-1<br>1.0<br>-2<br>0.9<br>-3<br>0.9<br>-4<br>0.8<br>Source: Morgan Stanley Research Source: Morgan Stanley Research<br>Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18 Jan-12 Apr-12 Jul-12 Oct-12 Jan-13 Apr-13 Jul-13 Oct-13 Jan-14 Apr-14 Jul-14 Oct-14 Jan-15 Apr-15 Jul-15 Oct-15 Jan-16 Apr-16 Jul-16 Oct-16 Jan-17 Apr-17 Jul-17 Oct-17 Jan-18 Apr-18 Jul-18 Oct-18<br>**----- End of picture text -----**<br>


Once we construct the Index, we take positive numbers as long signals, zero as neutral, and negative numbers as shorts. The strategy mimics the P/L of a GBI EM LC benchmarked strategy that remains neutral at zero, overweights/underweights by 25% in a +-1 signal and overweights/underweights by 50% otherwise (long/short signal with an intensity higher than 1-in absolute terms). See Exhibit 13. 

InExhibit 14, we show the distribution of the one week ahead GBI EM LC returns depending on the direction of the signal. In the case of **long signals, not only is the average GBI EM LC return higher, but the left tails (losses) are also less fat than in the case of the short signals** . In line with this, Exhibit 15 shows the one week ahead average annualized weekly GBI EM LC return bucketed by the signal. **As the signal intensifies (from lower to higher), the returns increase as well** , except for +4. It is interesting to note that neutral signals tend to yield negative returns, although that should be partially explained by the poor performance of the Benchmark in the out-of-sample time frame (since 2012). In addition, **when performing a statistical test on the correlation of the direction of our signal and the GBI EM LC return one week ahead (6.20% in a 354 sample), we find it is statistically significant with a p-value of 0.000 (threshold at 0.0001 is 1.11%).** 

7 

**Exhibit 14:** Distribution of Long and Short signals (Blue=Long, Yellow=Short) 

**==> picture [241 x 182] intentionally omitted <==**

**----- Start of picture text -----**<br>
Exhibit 15: GBI EM LC returns one week ahead after the signal was<br>produced<br>15%<br>Short Neutral Long<br>10%<br>5%<br>0%<br>-5% i<br>-10% I I<br>1 i]<br>-15%<br>-2 -1 i]a 0 i 1 2 3 4<br>Signal<br>Source: Morgan Stanley Research<br>Note: We omit -3 signals as there are very few observations in order to draw any statistically significant<br>conclusion<br>LC<br>Average weekly annualized GBI EM<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research Note: Blue line denotes are GBI Em returns one week ahead of long signals; yellow are short signals 

Finally, in order to illustrate the longer-term accuracy of the model detecting shifts in trends, we plotted in Exhibit 16 the total return GBI EM LC index with the long (green)/neutral (white)/short (red) signals overlapped. In line with what we mentioned above, the chart suggests that upward trends are detected quite nicely, while downward trends tend to be a bit more difficult for the model to trade. 

However, the model traded on the short side correctly the taper tantrum period (although a bit late) and subsequent periods of USD strength that made EM underperform. It has only a few episodes of long signals during the USD rally from mid 2014 to late 2016. More recently, it correctly traded the 2017 bull market and, at the beginning of 2018, it correctly traded ⅔ of the sell-off. 

**Exhibit 16:** GBI-EM local currency index and VIRP HB model signals (green=long, white=neutral and red=short) 

**==> picture [309 x 197] intentionally omitted <==**

**----- Start of picture text -----**<br>
340<br>320<br>300<br>280<br>260<br>240<br>220<br>Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>| | Buy Signal Ye Sell Signal —_— GBI-EM<br>Source: Morgan Stanley Research<br>**----- End of picture text -----**<br>


Note: shaded areas in green denote when the model has a long signal (1, 2 or 3), white areas are neutral (zero) and red are short signals (-1, -2 and -3). All the data used is out-of-sample. 

8 

## References and Appendix 

Jaime, Andres, EM Quant Strategy: Assessing Risk Premia in EMFX (Part 1): A TwoFactor Model Approach (5 Jun 2018) 

Della Corte, Pasquale; Ramadorai, Tarun and Sarno, Lucio, Volatility Risk Premia and Exchange Rate Predictability (July 29, 2014). Journal of Financial Economics (JFE), Forthcoming. 

Avdjiev, Stefan; Du, Wenxin; Koch, Catherine and Song Shin, BIS Working papers: The dollar, bank leverage and the deviation from covered interest parity (July 2017) 

Christiansen, Charlotte; Ranaldo, Angelo; Söderlind, The Time-Varying Systematic Risk of Carry Trade Strategies. Journal of Financial and Quantitative Analysis, Vol. 46, No. 4, 2011, p. 1107-1125. 

Verdelhan, Adrien, The Share of Systematic Variation in Bilateral Exchange Rates. The Journal of Finance (2018) 

## IRP EMFX individual pair historical signals 

Note: All charts have the y axis inverted. 

**Exhibit 17:** MXN 

**==> picture [220 x 147] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>10<br>12<br>14<br>16<br>18<br>20<br>22<br>BUY SELL MXN Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


**Exhibit 18:** BRL 

**==> picture [226 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>1.00<br>1.50<br>2.00<br>2.50<br>3.00<br>3.50<br>4.00<br>4.50<br>5.00<br>BUY SELL BRL Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


9 

**Exhibit 19:** COP 

**==> picture [223 x 134] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>1500<br>1700<br>1900<br>2100<br>2300<br>2500<br>2700<br>2900<br>3100<br>3300<br>3500<br>BUY SELL COP Curncy<br>**----- End of picture text -----**<br>


Source: Bloomberg, Morgan Stanley Research 

## **Exhibit 21:** MYR 

**==> picture [221 x 134] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>2.80<br>3.00<br>3.20<br>3.40<br>3.60<br>3.80<br>4.00<br>4.20<br>4.40<br>4.60<br>BUY SELL MYR Curncy<br>**----- End of picture text -----**<br>


Source: Bloomberg, Morgan Stanley Research 

## **Exhibit 23:** IDR 

**==> picture [226 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>8000<br>9000<br>10000<br>11000<br>12000<br>13000<br>14000<br>15000<br>16000<br>BUY SELL IDR Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


## **Exhibit 20:** CLP 

**==> picture [220 x 134] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>400<br>450<br>500<br>550<br>600<br>650<br>700<br>750<br>BUY SELL CLP Curncy<br>**----- End of picture text -----**<br>


Source: Bloomberg, Morgan Stanley Research 

## **Exhibit 22:** KRW 

**==> picture [224 x 134] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>1000<br>1050<br>1100<br>1150<br>1200<br>1250<br>1300<br>BUY SELL KRW Curncy<br>**----- End of picture text -----**<br>


Source: Bloomberg, Morgan Stanley Research 

## **Exhibit 24:** INR 

**==> picture [220 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>40<br>45<br>50<br>55<br>60<br>65<br>70<br>75<br>80<br>BUY SELL INR Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


10 

## **Exhibit 25:** THB 

**==> picture [219 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>28<br>29<br>30<br>31<br>32<br>33<br>34<br>35<br>36<br>37<br>38<br>BUY SELL THB Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


## **Exhibit 27:** HUF 

**==> picture [220 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>176<br>196<br>216<br>236<br>256<br>276<br>296<br>316<br>BUY SELL HUF Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


## **Exhibit 29:** ILS 

**==> picture [219 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>3.0<br>3.2<br>3.4<br>3.6<br>3.8<br>4.0<br>4.2<br>BUY SELL ILS Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


## **Exhibit 26:** CNY 

**==> picture [223 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>6.00<br>6.20<br>6.40<br>6.60<br>6.80<br>7.00<br>7.20<br>BUY SELL CNY Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


## **Exhibit 28:** RUB 

**==> picture [220 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>25<br>35<br>45<br>55<br>65<br>75<br>85<br>BUY SELL RUB Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


## **Exhibit 30:** TRY 

**==> picture [220 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>1.0<br>2.0<br>3.0<br>4.0<br>5.0<br>6.0<br>7.0<br>BUY SELL TRY Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


11 

**Exhibit 31:** ZAR 

**==> picture [221 x 134] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>6.0<br>8.0<br>10.0<br>12.0<br>14.0<br>16.0<br>18.0<br>BUY SELL ZAR Curncy<br>**----- End of picture text -----**<br>


**==> picture [106 x 6] intentionally omitted <==**

**----- Start of picture text -----**<br>
Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


**Exhibit 32:** CZK 

**==> picture [223 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>16.0<br>18.0<br>20.0<br>22.0<br>24.0<br>26.0<br>28.0<br>BUY SELL CZK Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


## **Exhibit 33:** PLN 

**==> picture [213 x 130] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>2.6<br>2.8<br>3.0<br>3.2<br>3.4<br>3.6<br>3.8<br>4.0<br>4.2<br>4.4<br>BUY SELL PLN Curncy<br>**----- End of picture text -----**<br>


Source: Bloomberg, Morgan Stanley Research 

## VIRP EMFX individual pair historical signals 

**Exhibit 34:** MXN 

**==> picture [219 x 134] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>10<br>12<br>14<br>16<br>18<br>20<br>22<br>BUY SELL MXN Curncy<br>**----- End of picture text -----**<br>


Source: Bloomberg, Morgan Stanley Research 

**Exhibit 35:** BRL 

**==> picture [226 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>1.00<br>1.50<br>2.00<br>2.50<br>3.00<br>3.50<br>4.00<br>4.50<br>5.00<br>BUY SELL BRL Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


12 

**Exhibit 36:** COP 

**==> picture [224 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>1500<br>1700<br>1900<br>2100<br>2300<br>2500<br>2700<br>2900<br>3100<br>3300<br>3500<br>BUY SELL COP Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


**Exhibit 38:** MYR 

**==> picture [221 x 134] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>2.80<br>3.00<br>3.20<br>3.40<br>3.60<br>3.80<br>4.00<br>4.20<br>4.40<br>4.60<br>BUY SELL MYR Curncy<br>**----- End of picture text -----**<br>


Source: Bloomberg, Morgan Stanley Research 

**Exhibit 40:** IDR 

**==> picture [226 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>8000<br>9000<br>10000<br>11000<br>12000<br>13000<br>14000<br>15000<br>16000<br>BUY SELL IDR Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


**Exhibit 37:** CLP 

**==> picture [221 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>400<br>450<br>500<br>550<br>600<br>650<br>700<br>750<br>BUY SELL CLP Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


## **Exhibit 39:** KRW 

**==> picture [225 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>1000<br>1050<br>1100<br>1150<br>1200<br>1250<br>1300<br>BUY SELL KRW Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


**Exhibit 41:** INR 

**==> picture [220 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>40<br>45<br>50<br>55<br>60<br>65<br>70<br>75<br>80<br>BUY SELL INR Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


13 

**Exhibit 42:** THB 

**Exhibit 43:** CNY 

**==> picture [507 x 134] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18 Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>28 1 6.00<br>29<br>6.20<br>30<br>31<br>6.40<br>32<br>33 6.60<br>34<br>35 6.80<br>36<br>7.00<br>37<br>38 0 7.20<br>r ie BUY SELL w THB Curncy ee AM BUY SELL CNY Curncy<br>**----- End of picture text -----**<br>


Source: Bloomberg, Morgan Stanley Research 

Source: Bloomberg, Morgan Stanley Research 

## **Exhibit 44:** HUF 

**==> picture [219 x 134] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>176<br>196<br>216<br>236<br>256<br>276<br>296<br>316<br>BUY SELL HUF Curncy<br>**----- End of picture text -----**<br>


Source: Bloomberg, Morgan Stanley Research 

## **Exhibit 45:** RUB 

**==> picture [220 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>25<br>35<br>45<br>55<br>65<br>75<br>85<br>BUY SELL RUB Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


## **Exhibit 46:** ILS 

## **Exhibit 47:** TRY 

**==> picture [490 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18 Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>3.0 1 1.0<br>3.2 2.0<br>3.4 3.0<br>3.6 4.0<br>3.8 5.0<br>4.0 6.0<br>4.2 0 7.0<br>ie BUY SELL ILS Curncy BUY SELL TRY Curncy<br>Source: Bloomberg, Morgan Stanley Research Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


14 

**Exhibit 48:** ZAR 

**==> picture [222 x 317] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>6.0<br>8.0<br>10.0<br>12.0<br>14.0<br>16.0<br>18.0 a<br>BUY SELL ZAR Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>Exhibit 50: PLN<br>Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>2.6<br>2.8<br>3.0<br>3.2<br>3.4<br>3.6<br>3.8<br>4.0<br>4.2 A.A<br>4.4<br>BUY SELL PLN Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


**Exhibit 49:** CZK 

**==> picture [223 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17 Jan-18<br>16.0<br>18.0<br>20.0<br>22.0<br>24.0<br>26.0<br>28.0<br>BUY SELL CZK Curncy<br>Source: Bloomberg, Morgan Stanley Research<br>**----- End of picture text -----**<br>


15 

## **Disclosure Section** 

The information and opinions in Morgan Stanley Research were prepared by Morgan Stanley & Co. LLC, and/or Morgan Stanley C.T.V.M. S.A., and/or Morgan Stanley Mexico, Casa de Bolsa, S.A. de C.V., and/or Morgan Stanley Canada Limited. As used in this disclosure section, "Morgan Stanley" includes Morgan Stanley & Co. LLC, Morgan Stanley C.T.V.M. S.A., Morgan Stanley Mexico, Casa de Bolsa, S.A. de C.V., Morgan Stanley Canada Limited and their affiliates as necessary. 

For important disclosures, stock price charts and equity rating histories regarding companies that are the subject of this report, please see the Morgan Stanley Research Disclosure Website at www.morganstanley.com/researchdisclosures, or contact your investment representative or Morgan Stanley Research at 1585 Broadway, (Attention: Research Management), New York, NY, 10036 USA. 

For valuation methodology and risks associated with any recommendation, rating or price target referenced in this research report, please contact the Client Support Team as follows: US/Canada +1 800 303-2495; Hong Kong +852 2848-5999; Latin America +1 718 754-5444 (U.S.); London +44 (0)20-7425-8169; Singapore +65 6834-6860; Sydney +61 (0)2-9770-1505; Tokyo +81 (0)3-6836-9000. Alternatively you may contact your investment representative or Morgan Stanley Research at 1585 Broadway, (Attention: Research Management), New York, NY 10036 USA. 

## **Analyst Certification** 

The following analysts hereby certify that their views about the companies and their securities discussed in this report are accurately expressed and that they have not received and will not receive direct or indirect compensation in exchange for expressing specific recommendations or views in this report: Andres Jaime. 

Unless otherwise stated, the individuals listed on the cover page of this report are research analysts. 

## **Global Research Conflict Management Policy** 

Morgan Stanley Research has been published in accordance with our conflict management policy, which is available at www.morganstanley.com/institutional/research/conflictpolicies. 

## **Important US Regulatory Disclosures on Subject Companies** 

The equity research analysts or strategists principally responsible for the preparation of Morgan Stanley Research have received compensation based upon various factors, including quality of research, investor client feedback, stock picking, competitive factors, firm revenues and overall investment banking revenues. Equity Research analysts' or strategists' compensation is not linked to investment banking or capital markets transactions performed by Morgan Stanley or the profitability or revenues of particular trading desks. Morgan Stanley and its affiliates do business that relates to companies/instruments covered in Morgan Stanley Research, including market making, providing liquidity, fund management, commercial banking, extension of credit, investment services and investment banking. Morgan Stanley sells to and buys from customers the securities/instruments of companies covered in Morgan Stanley Research on a principal basis. Morgan Stanley may have a position in the debt of the Company or instruments discussed in this report. Morgan Stanley trades or may trade as principal in the debt securities (or in related derivatives) that 

are the subject of the debt research report. 

Certain disclosures listed above are also for compliance with applicable regulations in non-US jurisdictions. 

## **STOCK RATINGS** 

Morgan Stanley uses a relative rating system using terms such as Overweight, Equal-weight, Not-Rated or Underweight (see definitions below). Morgan Stanley does not assign ratings of Buy, Hold or Sell to the stocks we cover. Overweight, Equal-weight, Not-Rated and Underweight are not the equivalent of buy, hold and sell. Investors should carefully read the definitions of all ratings used in Morgan Stanley Research. In addition, since Morgan Stanley Research contains more complete information concerning the analyst's views, investors should carefully read Morgan Stanley Research, in its entirety, and not infer the contents from the rating alone. In any case, ratings (or research) should not be used or relied upon as investment advice. An investor's decision to buy or sell a stock should depend on individual circumstances (such as the investor's existing holdings) and other considerations. 

## **Global Stock Ratings Distribution** 

(as of October 31, 2018) 

The Stock Ratings described below apply to Morgan Stanley's Fundamental Equity Research and do not apply to Debt Research produced by the Firm. For disclosure purposes only (in accordance with NASD and NYSE requirements), we include the category headings of Buy, Hold, and Sell alongside our ratings of Overweight, Equal-weight, Not-Rated and Underweight. Morgan Stanley does not assign ratings of Buy, Hold or Sell to the stocks we cover. Overweight, Equal-weight, Not-Rated and Underweight are not the equivalent of buy, hold, and sell but represent recommended relative weightings (see definitions below). To satisfy regulatory requirements, we correspond Overweight, our most positive stock rating, with a buy recommendation; we correspond Equal-weight and Not-Rated to hold and Underweight to sell recommendations, respectively. 

||COVERAGE UNIVERSE|COVERAGE UNIVERSE|INVESTMENT BANKING CLIENTS (IBC)|INVESTMENT BANKING CLIENTS (IBC)|INVESTMENT BANKING CLIENTS (IBC)|OTHER MATERIAL|OTHER MATERIAL|
|---|---|---|---|---|---|---|---|
|||||||INVESTMENT SERVICES||
|||||||CLIENTS(MISC)||
|STOCK RATING|COUNT|% OF|COUNT|% OF|% OF|COUNT|% OF|
|CATEGORY||TOTAL||TOTAL IBC|RATING||TOTAL|
||||||CATEGORY||OTHER|
||||||||MISC|
|**Overweight/Buy**|**1157**|**37%**|**305**|**42%**|**26%**|**544**|**39%**|
|**Equal-weight/Hold**|**1380**|**44%**|**335**|**46%**|**24%**|**632**|**45%**|
|**Not-Rated/Hold**|**47**|**1%**|**7**|**1%**|**15%**|**7**|**0%**|
|**Underweight/Sell**|**553**|**18%**|**82**|**11%**|**15%**|**220**|**16%**|
|**TOTAL**|**3,137**||**729**|||**1403**||



Data include common stock and ADRs currently assigned ratings. Investment Banking Clients are companies from whom Morgan Stanley received investment banking compensation in the last 12 months. Due to rounding off of decimals, the percentages provided in the "% of total" column may not add up to exactly 100 percent. 

16 

## **Analyst Stock Ratings** 

Overweight (O). The stock's total return is expected to exceed the average total return of the analyst's industry (or industry team's) coverage universe, on a risk-adjusted basis, over the next 12-18 months. 

Equal-weight (E). The stock's total return is expected to be in line with the average total return of the analyst's industry (or industry team's) coverage universe, on a risk-adjusted basis, over the next 12-18 months. 

Not-Rated (NR). Currently the analyst does not have adequate conviction about the stock's total return relative to the average total return of the analyst's industry (or industry team's) coverage universe, on a risk-adjusted basis, over the next 12-18 months. 

Underweight (U). The stock's total return is expected to be below the average total return of the analyst's industry (or industry team's) coverage universe, on a risk-adjusted basis, over the next 12-18 months. 

Unless otherwise specified, the time frame for price targets included in Morgan Stanley Research is 12 to 18 months. 

## **Analyst Industry Views** 

Attractive (A): The analyst expects the performance of his or her industry coverage universe over the next 12-18 months to be attractive vs. the relevant broad market benchmark, as indicated below. 

In-Line (I): The analyst expects the performance of his or her industry coverage universe over the next 12-18 months to be in line with the relevant broad market benchmark, as indicated below. 

Cautious (C): The analyst views the performance of his or her industry coverage universe over the next 12-18 months with caution vs. the relevant broad market benchmark, as indicated below. 

Benchmarks for each region are as follows: North America - S&P 500; Latin America - relevant MSCI country index or MSCI Latin America Index; Europe - MSCI Europe; Japan - TOPIX; Asia - relevant MSCI country index or MSCI sub-regional index or MSCI AC Asia Pacific ex Japan Index. 

## **Important Disclosures for Morgan Stanley Smith Barney LLC Customers** 

Important disclosures regarding the relationship between the companies that are the subject of Morgan Stanley Research and Morgan Stanley Smith Barney LLC or Morgan Stanley or any of their affiliates, are available on the Morgan Stanley Wealth Management disclosure website at www.morganstanley.com/online/researchdisclosures. For Morgan Stanley specific disclosures, you may refer to www.morganstanley.com/researchdisclosures. 

Each Morgan Stanley Equity Research report is reviewed and approved on behalf of Morgan Stanley Smith Barney LLC. This review and approval is conducted by the same person who reviews the Equity Research report on behalf of Morgan Stanley. This could create a conflict of interest. 

## **Other Important Disclosures** 

Morgan Stanley Research policy is to update research reports as and when the Research Analyst and Research Management deem appropriate, based on developments with the issuer, the sector, or the market that may have a material impact on the research views or opinions stated therein. In addition, certain Research publications are intended to be updated on a regular periodic basis (weekly/monthly/quarterly/annual) and will ordinarily be updated with that frequency, unless the Research Analyst and Research Management determine that a different publication schedule is appropriate based on current conditions. Morgan Stanley is not acting as a municipal advisor and the opinions or views contained herein are not intended to be, and do not constitute, advice within the meaning of Section 975 of the Dodd-Frank Wall Street Reform and Consumer Protection Act. 

Morgan Stanley produces an equity research product called a "Tactical Idea." Views contained in a "Tactical Idea" on a particular stock may be contrary to the recommendations or views expressed in research on the same stock. This may be the result of differing time horizons, methodologies, market events, or other factors. For all research available on a particular stock, please contact your sales representative or go to Matrix at http://www.morganstanley.com/matrix. Morgan Stanley Research is provided to our clients through our proprietary research portal on Matrix and also distributed electronically by Morgan Stanley to clients. Certain, but not all, Morgan Stanley Research products are also made available to clients through third-party vendors or redistributed to clients through alternate electronic means as a convenience. For access to all available Morgan Stanley Research, please contact your sales representative or go to Matrix at http://www.morganstanley.com/matrix. 

Any access and/or use of Morgan Stanley Research is subject to Morgan Stanley's Terms of Use (http://www.morganstanley.com/terms.html). By accessing and/or using Morgan Stanley Research, you are indicating that you have read and agree to be bound by our Terms of Use (http://www.morganstanley.com/terms.html). In addition you consent to Morgan Stanley processing your personal data and using cookies in accordance with our Privacy Policy and our Global Cookies Policy (http://www.morganstanley.com/privacy_pledge.html), including for the purposes of setting your preferences and to collect readership data so that we can deliver better and more personalized service and products to you. To find out more information about how Morgan Stanley processes personal data, how we use cookies and how to reject cookies see our Privacy Policy and our Global Cookies Policy (http://www.morganstanley.com/privacy_pledge.html). 

If you do not agree to our Terms of Use and/or if you do not wish to provide your consent to Morgan Stanley processing your personal data or using cookies please do not access our research. 

Morgan Stanley Research does not provide individually tailored investment advice. Morgan Stanley Research has been prepared without regard to the circumstances and objectives of those who receive it. Morgan Stanley recommends that investors independently evaluate particular investments and strategies, and encourages investors to seek the advice of a financial adviser. The appropriateness of an investment or strategy will depend on an investor's circumstances and objectives. The securities, instruments, or strategies discussed in Morgan Stanley Research may not be suitable for all investors, and certain investors may not be eligible to purchase or participate in some or all of them. Morgan Stanley Research is not an offer to buy or sell or the solicitation of an offer to buy or sell any security/instrument or to participate in any particular trading strategy. The value of and income from your investments may vary because of changes in interest rates, foreign exchange rates, default rates, prepayment rates, securities/instruments prices, market indexes, operational or financial conditions of companies or other factors. There may be time limitations on the exercise of options or other rights in securities/instruments transactions. Past performance is not necessarily a guide to future performance. Estimates of future performance are based on assumptions that may not be realized. If provided, and unless otherwise stated, the closing price on the cover page is that of the primary exchange for the subject company's securities/instruments. 

The fixed income research analysts, strategists or economists principally responsible for the preparation of Morgan Stanley Research have received compensation based upon various factors, including quality, accuracy and value of research, firm profitability or revenues (which include fixed income trading and capital markets profitability or revenues), client feedback and competitive factors. Fixed Income Research analysts', strategists' or economists' compensation is not linked to investment banking or capital markets transactions performed by Morgan Stanley or the profitability or revenues of particular trading desks. 

The "Important US Regulatory Disclosures on Subject Companies" section in Morgan Stanley Research lists all companies mentioned where Morgan Stanley owns 1% or more of a class of common equity securities of the companies. For all other companies mentioned in Morgan Stanley Research, Morgan Stanley may have an investment of less than 1% in securities/instruments or derivatives of securities/instruments of companies and may trade them in ways different from those discussed in Morgan Stanley Research. Employees of Morgan Stanley not involved in the preparation of Morgan Stanley Research may have investments in securities/instruments or derivatives of securities/instruments of companies mentioned and may trade them in ways different from those discussed in Morgan Stanley Research. Derivatives may be issued by Morgan Stanley or associated persons. 

With the exception of information regarding Morgan Stanley, Morgan Stanley Research is based on public information. Morgan Stanley makes every effort to use reliable, comprehensive information, but we make no representation that it is accurate or complete. We have no obligation to tell you when opinions or 

17 

information in Morgan Stanley Research change apart from when we intend to discontinue equity research coverage of a subject company. Facts and views presented in Morgan Stanley Research have not been reviewed by, and may not reflect information known to, professionals in other Morgan Stanley business areas, including investment banking personnel. 

Morgan Stanley Research personnel may participate in company events such as site visits and are generally prohibited from accepting payment by the company of associated expenses unless pre-approved by authorized members of Research management. Morgan Stanley may make investment decisions that are inconsistent with the recommendations or views in this report. 

To our readers based in Taiwan or trading in Taiwan securities/instruments: Information on securities/instruments that trade in Taiwan is distributed by Morgan Stanley Taiwan Limited ("MSTL"). Such information is for your reference only. The reader should independently evaluate the investment risks and is solely responsible for their investment decisions. Morgan Stanley Research may not be distributed to the public media or quoted or used by the public media without the express written consent of Morgan Stanley. Any non-customer reader within the scope of Article 7-1 of the Taiwan Stock Exchange Recommendation Regulations accessing and/or receiving Morgan Stanley Research is not permitted to provide Morgan Stanley Research to any third party (including but not limited to related parties, affiliated companies and any other third parties) or engage in any activities regarding Morgan Stanley Research which may create or give the appearance of creating a conflict of interest. Information on securities/instruments that do not trade in Taiwan is for informational purposes only and is not to be construed as a recommendation or a solicitation to trade in such securities/instruments. MSTL may not execute transactions for clients in these securities/instruments. 

Morgan Stanley is not incorporated under PRC law and the research in relation to this report is conducted outside the PRC. Morgan Stanley Research does not constitute an offer to sell or the solicitation of an offer to buy any securities in the PRC. PRC investors shall have the relevant qualifications to invest in such securities and shall be responsible for obtaining all relevant approvals, licenses, verifications and/or registrations from the relevant governmental authorities themselves. Neither this report nor any part of it is intended as, or shall constitute, provision of any consultancy or advisory service of securities investment as defined under PRC law. Such information is provided for your reference only. 

Morgan Stanley Research is disseminated in Brazil by Morgan Stanley C.T.V.M. S.A.; in Mexico by Morgan Stanley México, Casa de Bolsa, S.A. de C.V which is regulated by Comision Nacional Bancaria y de Valores. Paseo de los Tamarindos 90, Torre 1, Col. Bosques de las Lomas Floor 29, 05120 Mexico City; in Japan by Morgan Stanley MUFG Securities Co., Ltd. and, for Commodities related research reports only, Morgan Stanley Capital Group Japan Co., Ltd; in Hong Kong by Morgan Stanley Asia Limited (which accepts responsibility for its contents) and by Morgan Stanley Asia International Limited, Hong Kong Branch; in Singapore by Morgan Stanley Asia (Singapore) Pte. (Registration number 199206298Z) and/or Morgan Stanley Asia (Singapore) Securities Pte Ltd (Registration number 200008434H), regulated by the Monetary Authority of Singapore (which accepts legal responsibility for its contents and should be contacted with respect to any matters arising from, or in connection with, Morgan Stanley Research) and by Morgan Stanley Asia International Limited, Singapore Branch (Registration number T11FC0207F); in Australia to "wholesale clients" within the meaning of the Australian Corporations Act by Morgan Stanley Australia Limited A.B.N. 67 003 734 576, holder of Australian financial services license No. 233742, which accepts responsibility for its contents; in Australia to "wholesale clients" and "retail clients" within the meaning of the Australian Corporations Act by Morgan Stanley Wealth Management Australia Pty Ltd (A.B.N. 19 009 145 555, holder of Australian financial services license No. 240813, which accepts responsibility for its contents; in Korea by Morgan Stanley & Co International plc, Seoul Branch; in India by Morgan Stanley India Company Private Limited; in Indonesia by PT. Morgan Stanley Sekuritas Indonesia; in Canada by Morgan Stanley Canada Limited, which has approved of and takes responsibility for its contents in Canada; in Germany by Morgan Stanley Bank AG, Frankfurt am Main and Morgan Stanley Private Wealth Management Limited, Niederlassung Deutschland, regulated by Bundesanstalt fuer Finanzdienstleistungsaufsicht (BaFin); in Spain by Morgan Stanley, S.V., S.A., a Morgan Stanley group company, which is supervised by the Spanish Securities Markets Commission (CNMV) and states that Morgan Stanley Research has been written and distributed in accordance with the rules of conduct applicable to financial research as established under Spanish regulations; in the US by Morgan Stanley & Co. LLC, which accepts responsibility for its contents. Morgan Stanley & Co. International plc, authorized by the Prudential Regulatory Authority and regulated by the Financial Conduct Authority and the Prudential Regulatory Authority, disseminates in the UK research that it has prepared, and approves solely for the purposes of section 21 of the Financial Services and Markets Act 2000, research which has been prepared by any of its affiliates. RMB Morgan Stanley Proprietary Limited is a member of the JSE Limited and regulated by the Financial Services Board in South Africa. RMB Morgan Stanley Proprietary Limited is a joint venture owned equally by Morgan Stanley International Holdings Inc. and RMB Investment Advisory (Proprietary) Limited, which is wholly owned by FirstRand Limited. The information in Morgan Stanley Research is being disseminated by Morgan Stanley Saudi Arabia, regulated by the Capital Market Authority in the Kingdom of Saudi Arabia , and is directed at Sophisticated investors only. 

The information in Morgan Stanley Research is being communicated by Morgan Stanley & Co. International plc (DIFC Branch), regulated by the Dubai Financial Services Authority (the DFSA), and is directed at Professional Clients only, as defined by the DFSA. The financial products or financial services to which this research relates will only be made available to a customer who we are satisfied meets the regulatory criteria to be a Professional Client. The information in Morgan Stanley Research is being communicated by Morgan Stanley & Co. International plc (QFC Branch), regulated by the Qatar Financial Centre Regulatory Authority (the QFCRA), and is directed at business customers and market counterparties only and is not intended for Retail Customers as defined by the QFCRA. 

As required by the Capital Markets Board of Turkey, investment information, comments and recommendations stated here, are not within the scope of investment advisory activity. Investment advisory service is provided exclusively to persons based on their risk and income preferences by the authorized firms. Comments and recommendations stated here are general in nature. These opinions may not fit to your financial status, risk and return preferences. For this reason, to make an investment decision by relying solely to this information stated here may not bring about outcomes that fit your expectations. The trademarks and service marks contained in Morgan Stanley Research are the property of their respective owners. Third-party data providers make no warranties or representations relating to the accuracy, completeness, or timeliness of the data they provide and shall not have liability for any damages relating to such data. The Global Industry Classification Standard (GICS) was developed by and is the exclusive property of MSCI and S&P. Morgan Stanley Research, or any portion thereof may not be reprinted, sold or redistributed without the written consent of Morgan Stanley. © 2018 Morgan Stanley 

18 


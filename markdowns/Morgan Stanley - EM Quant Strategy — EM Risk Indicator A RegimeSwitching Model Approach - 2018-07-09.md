_July 9, 2018 10:00 AM GMT_ 

## **EM Quant Strategy** 

## EM Risk Indicator: A RegimeSwitching Model Approach 

The Morgan Stanley EM regime-shifting model serves as an early indicator to preempt stress in EM assets. Not only do we find differentiated behaviour of EM returns under the different regimes, but the shifts in the model serve as potential trading signals with high hit ratios in the sample. 

After accurately signalling a regime shift from risk-seeking to neutral and triggering an 'early' sell signal at the beginning of the year (see Global EM Strategist: Shifting Down a Gear, March 12, 2018), GBI-EM has lost 10%, the EMBI+ spread has widened by +70bp and EM equities have lost ~15%, yet the model hasn't shifted to a risk-averse regime as the risk indicator hovers around 40% (MSCEEMRI Index in Bloomberg). 

The relevance of regime shifts is twofold. 

MORGAN STANLEY & CO. LLC 

Andres Jaime STRATEGIST Andres.Jaime@morganstanley.com +1 212 296-5570 

_QuantWise highlights research that incorporates a robust quantitative approach in our investment analysis._ 

**Exhibit 1:** Morgan Stanley EM risk index 

**==> picture [176 x 101] intentionally omitted <==**

**----- Start of picture text -----**<br>
MS EM Regime Switching indicator - Contributions<br>Term Premia<br>100% Ted Spread Risk Averse<br>90% Credit Spreads (HY & IG average)<br>80% Rates Vol<br>70% Curncy VIX<br>60% VIX<br>50% Neutral<br>40%<br>30%<br>20%<br>10% Risk Appetite<br>0%<br>Jan-07 Dec-07 Nov-08 Oct-09 Sep-10 Aug-11 Jul-12 Jun-13 May-14 Apr-15 Mar-16 Feb-17 Jan-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: The thresholds for the different regimes are 22% and 55%, respectively. 

**Exhibit 2:** The volatility, skew and kurtosis of GBI-EM returns distribution tend to increase as we move away from the risk-seeking regime 

Shifts in the model proved to be good trading signals, with particular accuracy when shifting from extremes and when permanence in the new regime is persistent (more than a month). However, an additional change from neutral to risk-averse should be taken seriously, as in the past, two of the three sequential shifts detected by the model preceded major events such as the US financial crisis and the European sovereign crisis. 

- The distribution of EM returns and correlations changes materially in the different regimes, having very important ramifications for asset allocation. Volatility, kurtosis and the size of drawdowns of EM returns tend to increase out of the risk-seeking regime. 

In this vein, we expect the index to reach the 55% threshold to trigger a 'late' sell signal in the months to come as volatility is poised to increase (see EM and the New Vol Regime, February 12, 2018), credit spreads to widen (see Global Credit: Beta Watch Out, May 13, 2018) and risk appetite to remain low (see Global EM Strategist: Rallies Should Be Faded, June 25, 2018). 

Note: The thresholds determined by the model to shift regimes are 22% and 55%. We define risk- seeking regimes as those in which our EM risk indicator is below 22%, neutral is between 22% and 55%, and risk-averse is when the risk index is above 55%. The most accurate signals are usually associated with shifts from risk-seeking to neutral regimes. 

Source: Morgan Stanley Research; Note: Blue line corresponds to the riskseeking regime GBI-EM total return index USD returns distribution, yellow to riskneutral and green to risk-averse episodes. Returns are annualised. 

Due to the nature of the fixed income market, the issuers or bonds of the issuers recommended or discussed in this report may not be continuously followed. Accordingly, investors must regard this report as providing stand-alone analysis and should not expect continuing analysis or additional reports relating to such issuers or bonds of the issuers. 

Morgan Stanley does and seeks to do business with companies covered in Morgan Stanley Research. As a result, investors should be aware that the firm may have a conflict of interest that could affect the objectivity of Morgan Stanley Research. Investors should consider Morgan Stanley Research as only a single factor in making their investment decision. 

For analyst certification and other important disclosures, refer to the Disclosure Section, located at the end of this report. 

1 

## Methodology 

## Variable selection 

We calibrate a Hidden Markov Chain Model in order to detect regime shifts in global markets. We defined arbitrarily three regimes – risk-seeking, risk-neutral and risk-averse. 

The first step in the process – before calibrating any model – is to construct an observable variable that will help us to determine the regime shifts (the regimes are unobservable). In this exercise, we built an EM Risk Index (Ticker MSCEEMRI Index) comprised of different variables that we argue should be representative of changes in risk appetite. The criteria involved in the selection process of the index constituents were: 

They should include different assets classes in order to detect different triggers of risk-aversion in global markets that might affect sentiment towards EM; 

Not to include any EM variable to avoid endogeneity problems in the model; 

- High-frequency data in order to detect any potential change in regime in a timely manner. 

With these in mind, we selected six variables in order to construct our EM risk index: 

**VIX:** S&P 500 implied volatility as the most followed vol indicator. It is assumed to capture swings in risk appetite accurately. 

**CVIX:** Basket of FX-implied volatility in developed markets. Should increase as economic cycles decouple, which is usually linked with slower global growth. In addition, pricing of higher FX vol tends to disincentivise carry trades as the Sharpe ratio decreases. 

**MOVE:** Higher rates vol could be induced by higher rates or the end of forward guidance, leading to tighter financial conditions and less appetite for risky assets. 

- **US credit:** Substitute for EM credit. As US credit spreads widen, capital flow competition becomes more intense for EM, leading to wider credit spreads, higher costs of funding and slower growth. 

- **TED spread:** A measure of USD funding constraints. See USD's Relevance for EMFX, June 5, 2018. 

- **US 10y term premium:** A measure for policy mistake in developed markets. A sudden increase in term premium such as the taper tantrum period could pose serious stress to EM markets. 

As the selected variables are in different units, we normalised them in order to make them comparable and construct an index that is easy to read and goes from 0 to 100. To do this, we calculated a three-year rolling percentile for each of them. 

2 

## Parameters estimation 

In order to aggregate the normalised variables, we decided to use a Principal Component Analysis (PCA) approach while testing different samples during the past ten years. Exhibit 3 shows the loadings in the different samples we used – scaled to 100%. 

Consistently, the volatility indices and US credit get around a 20% weight, with the TED spread and US term premium having the biggest swings. We decided to assign a small percentage to US term premium despite the average being negative because we did want to incorporate a measure for policy mistake. The TED spread has a 15% weight in our index, close to the average in the different samples. **The final loadings (weights) in our** 

**index are in the last column of Exhibit 3 – VIX, CVIX, MOVE, US credit 20% each, TED spread 15% and US term premium 5%.** 

**The first principal component in all samples consistently explains more than 60% of the variance** of the six variables. 

**Exhibit 3:** EM regime-switching model parameters under different samples (past 10+ years) 

|**_Loadings (First PC)_**<br>**VIX**<br>**CVIX**<br>**MOVE**|**Complete**<br>19%<br>19%<br>19%|**Post 2009 (Ex-crisis)**<br>22%<br>24%<br>19%|**Ex-2017**<br>19%<br>19%<br>19%|**Post 2009 & Ex-2017**<br>22%<br>24%<br>18%<br>Samples|**Average**<br>21%<br>22%<br>19%|**Naïve**<br>**(Simple**<br>**average)**<br>17%<br>17%<br>17%|**MS Regime Switching**<br>**Model**<br>20%<br>20%<br>20%|
|---|---|---|---|---|---|---|---|
|**US Credit**|21%|25%|22%|27%|24%|17%|20%|
|**TED**|14%|23%|15%|25%|19%|17%|15%|
|**TP**|7%|-13%|6%|-16%|-4%|17%|5%|
|**_Thresholds_**||||||||
|**Risk On - Neutral**|22%|20%|33%|23%|24%|32%|22%|
|**Neutral - Risk Off**|55%|52%|69%|54%|58%|55%|55%|



Source: Morgan Stanley Research 

In the same vein, by using a Hidden Markov Chain Model (see Parameters and references for our regime-switching model for more details) and our EM risk index, we estimated the thresholds that signal a shift in regime, using the respective loadings in each sample. 

## **In all the samples the thresholds are very similar (which shows robustness in** 

**estimation of the parameters)** , except for the one that excludes 2017. In that instance, the thresholds are substantially higher, probably depressed in the other samples by the unusually low volatility environment we experienced last year. 

## In our model, we decided to use the **thresholds determined by the whole sample and our loadings, which are 22% and 55%, respectively.** 

In other words, when our EM risk index is below 22% the model suggests a risk-seeking regime, between 22% and 55% our model points to a risk-neutral regime, and above 55% it determines we are in a risk-averse regime (Exhibit 4). The contributions to the EM risk index are shown in Exhibit 5. 

3 

**Exhibit 4:** EM risk index 

MS EM Regime Switching indicator 

**==> picture [231 x 115] intentionally omitted <==**

**----- Start of picture text -----**<br>
100%<br>90% Risk Averse<br>80%<br>70%<br>60%<br>50%<br>Neutral<br>40%<br>30%<br>20%<br>10% eee oe) 1 eens Risk Appetite 0<br>0%<br>Jan-07 Aug-07 Mar-08 Oct-08 May-09 Dec-09 Jul-10 Feb-11 Sep-11 Apr-12 Nov-12 Jun-13 Jan-14 Aug-14 Mar-15 Oct-15 May-16 Dec-16 Jul-17 Feb-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

**Exhibit 5:** Components' contributions to our EM risk index 

**==> picture [243 x 141] intentionally omitted <==**

**----- Start of picture text -----**<br>
MS EM Regime Switching indicator - Contributions<br>Term Premia<br>100% Ted Spread Risk Averse<br>90% Credit Spreads (HY & IG average)<br>80% Rates Vol<br>70% Curncy VIX<br>60% VIX<br>50% Neutral<br>40%<br>30%<br>i ih hi | i\ { i<br>20%<br>10% Risk Appetite<br>0%<br>Jan-07 Dec-07 Nov-08 Oct-09 Sep-10 Aug-11 Jul-12 Jun-13 May-14 Apr-15 Mar-16 Feb-17 Jan-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

## Parameters assumptions and references for our regime-switching model 

## Parameters 

**Number of regimes** (hidden states): 3 

**Observed time series values:** EM risk index 

**Distribution** (Max likelihood estimation): Mixture of normals 

## **Number of distributions for the mixture:** 3 

## Model and procedures details 

Bilmes Jeff A. 1997. A Gentle Tutorial of the EM Algorithm and its Application to Parameter Estimation for Gaussian Mixture and Hidden Markov Models 

Ollivier Taramasco, Sebastian Bauer, 2012. Hidden Markov Models simulations and estimations 

Hamilton, 2005. Regime-Switching Models 

4 

## Conclusions 

## Why the regime shifts are important for EM returns 

Not only do average returns tend to be lower under the risk-averse and risk-neutral periods compared to the risk-seeking one, but the volatility, skew (in absolute terms) and kurtosis also increase substantially (Exhibit 6 and Exhibit 7). In other words, the **risk-** 

## **adjusted expected returns of EM decrease out of the risk-seeking regime as 'tail' events become more common, negative returns tend to be larger than positive ones (on average) and the return dispersion gets wider.** 

As EM shares some characteristics with a long carry trade return profile, in a highervolatility environment, the expected Sharpe and Sortino ratios diminish. For instance, the **Sharpe ratio, assuming historical volatilities and returns, more than halves when moving from a risk-seeking to a risk-neutral regime.** 

**Exhibit 6:** The volatility, skew and kurtosis of GBI-EM returns distribution tend to increase as we move away from the risk-seeking regime 

**Exhibit 7:** GBI-EM total return index USD stats under different regimes 

||**Risk seeking**|**Neutral**|**Risk averse**|
|---|---|---|---|
|Average Return|14.22%|8.20%|-2.97%|
|Median Return|13.76%|20.0%|3.9%|
|Volatility|6.98%|10.15%|13.22%|
|Skew|-0.30|-0.15|-0.25|
|Kurtosis|0.70|3.89|3.85|



Source: Morgan Stanley Research 

Source: Morgan Stanley Research; Note: Blue line corresponds to the risk-seeking regime GBI-EM total return index USD returns distribution, yellow to risk-neutral and green to risk-averse episodes. 

For EM local, USD plays an outsized role (see USD's Relevance for EMFX, June 5, 2018). Not surprisingly, most of the **risk-seeking regimes coincide with a stable and/or falling USD,** a very important anchor for EM. For instance, back in the financial crisis, the model turned risk-averse at a very early stage (Exhibit 9). While EMBI spreads widened and volatility increased, the falling USD in the early stages served as an anchor, limiting losses for EM local compared to EM credit. 

5 

**Exhibit 8:** GBI-EM total return under different regimes 

**==> picture [232 x 117] intentionally omitted <==**

**----- Start of picture text -----**<br>
GBI-EM (log)<br>2.60<br>2.55<br>2.50<br>2.45<br>2.40<br>2.35<br>2.30<br>2.25<br>2.20<br>2.15<br>Jun-07 Nov-07 Apr-08 Sep-08 Feb-09 Jul-09 Dec-09 May-10 Oct-10 Mar-11 Aug-11 Jan-12 Jun-12 Nov-12 Apr-13 Sep-13 Feb-14 Jul-14 Dec-14 May-15 Oct-15 Mar-16 Aug-16 Jan-17 Jun-17 Nov-17<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: Red shaded regions denote risk-averse regimes, white are neutral regimes while green represent risk-seeking ones. 

**Exhibit 9:** USD trade-weighted index under different regimes 

**==> picture [233 x 117] intentionally omitted <==**

**----- Start of picture text -----**<br>
USD TWI (log)<br>2.00<br>1.98<br>1.96<br>1.94<br>1.92<br>1.90<br>1.88<br>1.86<br>1.84<br>1.82<br>1.80<br>Jun-07 Nov-07 Apr-08 Sep-08 Feb-09 Jul-09 Dec-09 May-10 Oct-10 Mar-11 Aug-11 Jan-12 Jun-12 Nov-12 Apr-13 Sep-13 Feb-14 Jul-14 Dec-14 May-15 Oct-15 Mar-16 Aug-16 Jan-17 Jun-17 Nov-17<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: Red shaded regions denote risk-averse regimes, white are neutral regimes while green represent risk-seeking ones. 

## In sample backtest (EMBI spread) 

In order to assess the accuracy of the model, we decided to run a backtest using the EMBI spread as a proxy for EM risk. While an out-of-sample backtest would obviously be more suitable, the low frequency of regimes shifts – an intended feature of the model – limits the ability to perform it out of sample. 

## Signals 

## 'Sell' signal 

- Early sell: Defined as when the index changes from risk-on to neutral, using as an entry date the day when the index is already in the new regime. 

- Late sell: Defined as when the index changes from neutral to risk-off, using as an entry date the day when the index is already in the new regime. 

## 'Buy' signal 

- Early buy: Defined as when the index changes from risk-off to neutral, using as an entry date the day when the index is already in the new regime. 

- Late buy: Defined as when the index changes from neutral to risk-on, using as an entry date the day when the index is already in the new regime. 

Using data from early 2007 through the end of 2017, the model generates 35 sell signals (3.8 per year on average). 

Each time the model generated a sell signal, the EMBI widened, on average, by 11bp one month after, 16bp after three months, 37bp after six months and 64bp after a year. The hit ratio, which is defined as the percentage of instances (within the 35 signals) that the EMBI widens once a selling signal was generated, is above 44% in all the time frames defined (one month to 12 months). 

We find it interesting to note that **the accuracy of the signal increases as time goes by,** with the **maximum hit ratio at 88% after 12 months from when the signal was** 

**generated.** Although the accuracy (in sample) is relatively high, there are some instances where the EMBI actually narrows. For example, the signals that were generated in late 

6 

January 2014, October 2016 and August 2017 were wrong, but they share one feature: the persistence of the signal was very weak (on average, the index remained in one regime less than a month: 10 days, 49 days and 11 days). In other words, **as the model turns into a new regime, the signal becomes stronger after a month,** if history is a guide. 

When using only **early sell signals,** not only does the **accuracy of the model increase to 100% and 75% on a 12-month and six-month time horizon, respectively,** but the **size of the sell-off also increases.** This might be attributable to the fact that once the market is in a risk-seeking regime, valuations tend to be more expensive while positioning usually gets crowded. It is important to note that two-thirds of the time that the model shifted from risk-seeking to neutral and to risk-averse afterwards, major events unfolded (US financial crisis and European sovereign crisis, for example). 

**Exhibit 10:** EMBI change after a selling signal was triggered 

**Exhibit 11:** EMBI change after a early selling signal was triggered 

**==> picture [508 x 93] intentionally omitted <==**

**----- Start of picture text -----**<br>
|||||||||||
|---|---|---|---|---|---|---|---|---|---|
|1m|3m|6m|12m|1m|3m|6m|12m|
|Average|11|16|37|64|Average|5|10|45|79|
|Median|-2|9|38|73|Median|-3|7|53|83|
|Min|-23|-34|-87|-56|Min|-23|-34|-87|19|
|Max|81|94|153|134|Max|81|57|153|132|
|Hit Ratio|44%|81%|69%|88%|Hit Ratio|25%|75%|75%|100%|

**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

Source: Morgan Stanley Research 

In the case of the **buying signals,** the accuracy is lower over long time horizons (12 months) compared to one month to six months, with a hit ratio of only 39% in a year's time. However, as in the case of the selling signals, the **accuracy improves substantially as we restrict the buying signals to be 'early'** (Exhibit 13). In those instances, the **hit ratio is 100% on the six and 12-month time horizons while the magnitude of the rally increases as well.** These might be due to the fact that during risk-off episodes positioning is lighter and valuations becomes very cheap as markets incorporate very bad scenarios in their portfolios. 

While not tested formally in this note, we do think that valuations could play a very complementary and important role in detecting turnarounds within the different regimes. For instance, changes in regime accompanied by extreme valuations/positioning could have more predictive power as portfolio adjustments prolong and are bigger in magnitude. In addition, in high persistent regimes such as the financial crisis, it could serve as a better indicator. 

7 

**Exhibit 12:** EMBI change after a buying signal was triggered 

**Exhibit 13:** EMBI change after an early buying signal was triggered 

**==> picture [508 x 93] intentionally omitted <==**

**----- Start of picture text -----**<br>
|||||||||||
|---|---|---|---|---|---|---|---|---|---|
|1m|3m|6m|12m|1m|3m|6m|12m|
|Average|-6|-5|-8|24|Average|-10|-21|-42|-68|
|Median|-3|1|-20|16|Median|-10|-36|-30|-55|
|Min|-36|-53|-83|-142|Min|-36|-50|-83|-142|
|Max|18|36|108|181|Max|18|33|-21|-42|
|Hit Ratio|61%|50%|67%|39%|Hit Ratio|67%|67%|100%|100%|

**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

Source: Morgan Stanley Research 

_The performance data provided is a hypothetical illustration of mathematical principles; it does not predict or project the performance of an investment or investment strategy. Past performance is no guarantee of future results._ 

## **Limits and Vulnerabilities of our Regime-Switching model** 

- **Limited availability of data.** The variables we use in our EM risk index only go back to 2004. Our Index encompasses only a few months of data before the financial crisis. 

- **Low frequency of signals** makes out-of-sample back testing more challenging as there are limited data points to evaluate. While cross-validation is usually a solution, when working with time series the random selection of the samples might not be appropriate. The in-sample back test might suffer from over fitting. 

**Output of the model sensitive to including/excluding 2017 sample.** While most of the sample variation in our estimations barely change the output of the model, 2017 is an exception. 

**Back tests do not include potential carry and/or transactional costs.** This would potentially decrease the attractiveness of the model as P/L results would likely be lower. 

8 

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

(as of June 30, 2018) 

The Stock Ratings described below apply to Morgan Stanley's Fundamental Equity Research and do not apply to Debt Research produced by the Firm. For disclosure purposes only (in accordance with NASD and NYSE requirements), we include the category headings of Buy, Hold, and Sell alongside our ratings of Overweight, Equal-weight, Not-Rated and Underweight. Morgan Stanley does not assign ratings of Buy, Hold or Sell to the stocks we cover. Overweight, Equal-weight, Not-Rated and Underweight are not the equivalent of buy, hold, and sell but represent recommended relative weightings (see definitions below). To satisfy regulatory requirements, we correspond Overweight, our most positive stock rating, with a buy recommendation; we correspond Equal-weight and Not-Rated to hold and Underweight to sell recommendations, respectively. 

||COVERAGE UNIVERSE|COVERAGE UNIVERSE|INVESTMENT BANKING CLIENTS (IBC)|INVESTMENT BANKING CLIENTS (IBC)|INVESTMENT BANKING CLIENTS (IBC)|OTHER MATERIAL|OTHER MATERIAL|
|---|---|---|---|---|---|---|---|
|||||||INVESTMENT SERVICES||
|||||||CLIENTS(MISC)||
|STOCK RATING|COUNT|% OF|COUNT|% OF|% OF|COUNT|% OF|
|CATEGORY||TOTAL||TOTAL IBC|RATING||TOTAL|
||||||CATEGORY||OTHER|
||||||||MISC|
|**Overweight/Buy**|**1170**|**38%**|**292**|**39%**|**25%**|**550**|**39%**|
|**Equal-weight/Hold**|**1343**|**43%**|**363**|**49%**|**27%**|**645**|**46%**|
|**Not-Rated/Hold**|**50**|**2%**|**5**|**1%**|**10%**|**7**|**0%**|
|**Underweight/Sell**|**544**|**18%**|**81**|**11%**|**15%**|**211**|**15%**|
|**TOTAL**|**3,107**||**741**|||**1413**||



Data include common stock and ADRs currently assigned ratings. Investment Banking Clients are companies from whom Morgan Stanley received investment banking compensation in the last 12 months. Due to rounding off of decimals, the percentages provided in the "% of total" column may not add up to exactly 100 percent. 

9 

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

10 

information in Morgan Stanley Research change apart from when we intend to discontinue equity research coverage of a subject company. Facts and views presented in Morgan Stanley Research have not been reviewed by, and may not reflect information known to, professionals in other Morgan Stanley business areas, including investment banking personnel. 

Morgan Stanley Research personnel may participate in company events such as site visits and are generally prohibited from accepting payment by the company of associated expenses unless pre-approved by authorized members of Research management. Morgan Stanley may make investment decisions that are inconsistent with the recommendations or views in this report. 

To our readers based in Taiwan or trading in Taiwan securities/instruments: Information on securities/instruments that trade in Taiwan is distributed by Morgan Stanley Taiwan Limited ("MSTL"). Such information is for your reference only. The reader should independently evaluate the investment risks and is solely responsible for their investment decisions. Morgan Stanley Research may not be distributed to the public media or quoted or used by the public media without the express written consent of Morgan Stanley. Any non-customer reader within the scope of Article 7-1 of the Taiwan Stock Exchange Recommendation Regulations accessing and/or receiving Morgan Stanley Research is not permitted to provide Morgan Stanley Research to any third party (including but not limited to related parties, affiliated companies and any other third parties) or engage in any activities regarding Morgan Stanley Research which may create or give the appearance of creating a conflict of interest. Information on securities/instruments that do not trade in Taiwan is for informational purposes only and is not to be construed as a recommendation or a solicitation to trade in such securities/instruments. MSTL may not execute transactions for clients in these securities/instruments. 

Morgan Stanley is not incorporated under PRC law and the research in relation to this report is conducted outside the PRC. Morgan Stanley Research does not constitute an offer to sell or the solicitation of an offer to buy any securities in the PRC. PRC investors shall have the relevant qualifications to invest in such securities and shall be responsible for obtaining all relevant approvals, licenses, verifications and/or registrations from the relevant governmental authorities themselves. Neither this report nor any part of it is intended as, or shall constitute, provision of any consultancy or advisory service of securities investment as defined under PRC law. Such information is provided for your reference only. 

Morgan Stanley Research is disseminated in Brazil by Morgan Stanley C.T.V.M. S.A.; in Mexico by Morgan Stanley México, Casa de Bolsa, S.A. de C.V which is regulated by Comision Nacional Bancaria y de Valores. Paseo de los Tamarindos 90, Torre 1, Col. Bosques de las Lomas Floor 29, 05120 Mexico City; in Japan by Morgan Stanley MUFG Securities Co., Ltd. and, for Commodities related research reports only, Morgan Stanley Capital Group Japan Co., Ltd; in Hong Kong by Morgan Stanley Asia Limited (which accepts responsibility for its contents) and by Morgan Stanley Asia International Limited, Hong Kong Branch; in Singapore by Morgan Stanley Asia (Singapore) Pte. (Registration number 199206298Z) and/or Morgan Stanley Asia (Singapore) Securities Pte Ltd (Registration number 200008434H), regulated by the Monetary Authority of Singapore (which accepts legal responsibility for its contents and should be contacted with respect to any matters arising from, or in connection with, Morgan Stanley Research) and by Morgan Stanley Asia International Limited, Singapore Branch (Registration number T11FC0207F); in Australia to "wholesale clients" within the meaning of the Australian Corporations Act by Morgan Stanley Australia Limited A.B.N. 67 003 734 576, holder of Australian financial services license No. 233742, which accepts responsibility for its contents; in Australia to "wholesale clients" and "retail clients" within the meaning of the Australian Corporations Act by Morgan Stanley Wealth Management Australia Pty Ltd (A.B.N. 19 009 145 555, holder of Australian financial services license No. 240813, which accepts responsibility for its contents; in Korea by Morgan Stanley & Co International plc, Seoul Branch; in India by Morgan Stanley India Company Private Limited; in Indonesia by PT. Morgan Stanley Sekuritas Indonesia; in Canada by Morgan Stanley Canada Limited, which has approved of and takes responsibility for its contents in Canada; in Germany by Morgan Stanley Bank AG, Frankfurt am Main and Morgan Stanley Private Wealth Management Limited, Niederlassung Deutschland, regulated by Bundesanstalt fuer Finanzdienstleistungsaufsicht (BaFin); in Spain by Morgan Stanley, S.V., S.A., a Morgan Stanley group company, which is supervised by the Spanish Securities Markets Commission (CNMV) and states that Morgan Stanley Research has been written and distributed in accordance with the rules of conduct applicable to financial research as established under Spanish regulations; in the US by Morgan Stanley & Co. LLC, which accepts responsibility for its contents. Morgan Stanley & Co. International plc, authorized by the Prudential Regulatory Authority and regulated by the Financial Conduct Authority and the Prudential Regulatory Authority, disseminates in the UK research that it has prepared, and approves solely for the purposes of section 21 of the Financial Services and Markets Act 2000, research which has been prepared by any of its affiliates. RMB Morgan Stanley Proprietary Limited is a member of the JSE Limited and regulated by the Financial Services Board in South Africa. RMB Morgan Stanley Proprietary Limited is a joint venture owned equally by Morgan Stanley International Holdings Inc. and RMB Investment Advisory (Proprietary) Limited, which is wholly owned by FirstRand Limited. The information in Morgan Stanley Research is being disseminated by Morgan Stanley Saudi Arabia, regulated by the Capital Market Authority in the Kingdom of Saudi Arabia , and is directed at Sophisticated investors only. 

The information in Morgan Stanley Research is being communicated by Morgan Stanley & Co. International plc (DIFC Branch), regulated by the Dubai Financial Services Authority (the DFSA), and is directed at Professional Clients only, as defined by the DFSA. The financial products or financial services to which this research relates will only be made available to a customer who we are satisfied meets the regulatory criteria to be a Professional Client. The information in Morgan Stanley Research is being communicated by Morgan Stanley & Co. International plc (QFC Branch), regulated by the Qatar Financial Centre Regulatory Authority (the QFCRA), and is directed at business customers and market counterparties only and is not intended for Retail Customers as defined by the QFCRA. 

As required by the Capital Markets Board of Turkey, investment information, comments and recommendations stated here, are not within the scope of investment advisory activity. Investment advisory service is provided exclusively to persons based on their risk and income preferences by the authorized firms. Comments and recommendations stated here are general in nature. These opinions may not fit to your financial status, risk and return preferences. For this reason, to make an investment decision by relying solely to this information stated here may not bring about outcomes that fit your expectations. The trademarks and service marks contained in Morgan Stanley Research are the property of their respective owners. Third-party data providers make no warranties or representations relating to the accuracy, completeness, or timeliness of the data they provide and shall not have liability for any damages relating to such data. The Global Industry Classification Standard (GICS) was developed by and is the exclusive property of MSCI and S&P. Morgan Stanley Research, or any portion thereof may not be reprinted, sold or redistributed without the written consent of Morgan Stanley. © 2018 Morgan Stanley 

11 


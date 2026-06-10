June 5, 2018 01:00 PM GMT 

**EM Quant Strategy | North America** 

## Assessing Risk Premia in EMFX (Part 1): A Two-Factor Model Approach 

The direct and indirect implications of USD's dominance as a global funding currency are usually understated, yet they have very important ramifications for EM. Using only two factors (USD and carry), we isolate non-systemic variance in EMFX in a way to imply idiosyncratic risk premia. 

**We define systemic variation** as the change in a currency pair that can be explained by global factors (such as USD or risk appetite) and idiosyncratic variation as the change that can be explained by local factors specific to each currency pair. Once we have established each currency's relationship with the global factors, we can then assign any variation in a currency pair that is not explained by changes in the global factors to local risk premia. 

MORGAN STANLEY & CO. LLC 

Andres Jaime STRATEGIST Andres.Jaime@morganstanley.com +1 212 296-5570 

_QuantWise highlights research that incorporates a robust quantitative approach in our investment analysis._ 

**==> picture [180 x 118] intentionally omitted <==**

**----- Start of picture text -----**<br>
Exhibit 1:  EMFX performance vs two-factor model: 6-<br>month cumulative difference<br>25% Low risk-premia 01-Jun-18<br>13%<br>0%<br>-13%<br>High risk-premia<br>-25%<br>CNY ZAR THB MYR COP CLP KRW MXN IDR RUB BRL ILS INR PLN CZK HUF TRY<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: The edges of the boxplots represent the 5% and 90% percentiles assuming a normal distribution with mean zero and using standard deviation of our two-factor model. While the cumulative 6m idiosyncratic variation in EMFX does not distribute normally, it serves as a benchmark in order to assess extreme pricing. We use asymmetric percentiles in order to incorporate EMFX skew. 

**Isolating non-systemic variance** not only helps to gauge extreme pricing in EMFX pairs – serving as a potential trading signal – but could also assist as a tool to more easily assess the market impact of specific events on local assets. 

We consider **this model a complement to our current framework,** which includes other quantitative instruments and fundamental analysis. By its nature, the model was designed to have shorter time horizons compared to "fair value" models, which we plan to develop in subsequent papers. 

Within our framework, we find that **CNY, ZAR and THB are the currencies with the lowest risk premia** on a volatility-adjusted scale and **CZK, HUF and TRY are the ones with the highest.** 

While only those with low risk premia are at or above "reversal levels" (i.e., 90% and 5% percentile assuming a normal distribution and the standard deviation of our model), **we only see THB as a potential trade, although it would need to show more extreme pricing** . In the case of CNY, mean-reversion occurs extremely slowly as the renminbi remains a heavily managed currency, while ZAR tends to overshoot extremes more often amid a positive fundamental view (see Global EM Strategist: Shifting Risks, May 29, 2018). We think the currencies with high risk premia have modest room to underperform from a statistical point of view. 

Due to the nature of the fixed income market, the issuers or bonds of the issuers recommended or discussed in this report may not be continuously followed. Accordingly, investors must regard this report as providing stand-alone analysis and should not expect continuing analysis or additional reports relating to such issuers or bonds of the issuers. 

Morgan Stanley does and seeks to do business with companies covered in Morgan Stanley Research. As a result, investors should be aware that the firm may have a conflict of interest that could affect the objectivity of Morgan Stanley Research. Investors should consider Morgan Stanley Research as only a single factor in making their investment decision. 

For analyst certification and other important disclosures, refer to the Disclosure Section, located at the end of this report. 

1 

## EMFX idiosyncratic risk premia 

One of the first building blocks in order to trade EMFX is to break down the different factors that affect its variations in order to correctly understand its main drivers at different points in time. In this vein, most of the models that focus on high-frequency data – i.e., less than a month – calculate EMFX "fair value" by using a set of financial variables such as interest rate differentials, sovereign spreads, equity volatility and commodity prices, among others. Although the approach is widely used among practitioners, we do think that it has several flaws: 

It falsely treats nominal and bilateral exchange rates as stationary series; 

- Causality tests are inconclusive between EMFX and rates differentials as opposed to developed markets; 

- The high correlation between EMFX and most of the "independent" variables widely used exist mainly because of a common driver, which is arguably risk premia, i.e., risk premia are contained in most of the assets linked to a sovereign; 

- The instability of the parameters and lack of consistent data across EM make it difficult to compare risk premia. 

In our view, instead of calculating a "short-term fair value" model for each currency pair, a better approach is to separate EMFX variations into systemic and idiosyncratic variance, in a way that the idiosyncratic variation can be tracked down and accumulated in order to imply risk premia. 

To do this, we use only two factors: a **USD and a carry trade factor** (see Methodology). Although simple, these two factors not only provide a strong foundation on why they play an important role for EMFX as they have a risk-based interpretation (see USD's relevance for EMFX and Importance of the carry trade as a systemic explanatory factor), but **manage to explain close to 50% of the systemic variation of EMFX** . By using this approach, we avoid the common "overfitting" problem explained above and manage to segregate each of the EMFX idiosyncrasies in a more efficient way. In addition, it permits us to compare EMFX risk premia using a generic model while avoiding misspecifications and doubtful causalities. 

## USD's relevance for EMFX 

As we have highlighted in a few pieces before (see FX: Downward USD Trend as a Tailwind for EMFX, December 1, 2017 and Assessing EM Resilience to USD, May 29, 2018), USD has become a more relevant and key factor explaining EMFX variation. From a statistical point of view, the share of variance explained by USD in an EMFX portfolio has more than doubled after the financial crisis, reaching almost 50% before the taper tantrum and recently (past three years) while averaging above 40% post 2008 (see Results). In this vein, we do think that this increase is permanent and could be explained mainly due to three factors: 

2 

**1) USD as a proxy for the shadow price of bank leverage:** As explained in BIS Working papers: The dollar, bank leverage and the deviation from covered interest parity, a stronger USD goes hand-in-hand with bigger deviations from covered interest rate parity (CIP) and contractions in cross-border bank lending in USD. Here, **USD plays the role of a barometer of risk-taking capacity in capital markets** as CIP deviations are associated with a bank's balance sheet constraints. In turn, **a stronger USD is usually associated with tighter financial conditions, and vice versa,** mainly through the financial channel – as opposed to the classic net-export channel (see Exhibit 3 and Structural Demand for EM, November 28, 2017). 

**How does the financial channel work?** When there is the potential for valuation mismatches on borrowers' balance sheets arising from FX variations, a weaker USD tends to flatter the balance sheet of the USD borrowers as their liabilities fall relative to their assets. This usually creates spare capacity for additional credit expansion – from the standpoint of creditors – via a lower VaR as a stronger credit position of borrowers reduces the tail risks in the credit portfolio. 

**Exhibit 2:** USD's dominance as a funding currency 

**==> picture [239 x 143] intentionally omitted <==**

**----- Start of picture text -----**<br>
Global Cross-Border Liabilities<br>90<br>80<br>70<br>60<br>50<br>40<br>30<br>20 ee+eew<br>10 4f <22S=2= _ee~—- s+ =~ --<br>0 oo EEE<br>CHF EUR GBP JPY Other USD<br>Source: BIS, Macrobond, Morgan Stanley Research<br>Dec-77 Mar-80 Jun-82 Sep-84 Dec-86 Mar-89 Jun-91 Sep-93 Dec-95 Mar-98 Jun-00 Sep-02 Dec-04 Mar-07 Jun-09 Sep-11 Dec-13 Mar-16<br>**----- End of picture text -----**<br>


**Exhibit 3:** Clear relationship between exchange rates and cross-border bank lending 

Source: Bank of International Settlements, International Monetary Fund and Bank of Canada; Note: x-axis represents changes in the share of systemic exchange rate variation while y-axis shows the changes in the share of systemic variation in cross-border lending 

**2) EM local markets is now a well-established asset class:** Continued development of local currency bond markets along with better fundamentals and governance in EM have made offshore participation higher. While the generalized decrease in volatility might partially explain this trend, we think that the increase in EM holdings is due in part to more structural than cyclical factors, making them less prone to reversals. Average percentage of foreign participation in EM has increased from around 22% in 2011 to almost 30% nowadays (Exhibit 4). 

**3) USD issuance/leverage in EM:** In times of stress, a weaker currency will tighten credit conditions more when there are high FX liabilities relative to assets. Overall debt in EM has increased significantly in the past decade, although a large part of this increase has been driven by China and in local currency. Nonetheless, USD debt as a percentage of GDP has increased from an average of 30% to 40% in EM since 2009 (simple average across EM - each currency is scaled by its GDP). See Assessing EM Resilience to USD, May 29, 2018. 

3 

**Exhibit 4:** Average foreign ownership of EM local currency bonds 

**Average % of Foreign ownership** 

**==> picture [237 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
31%<br>30%<br>29%<br>28%<br>27%<br>26%<br>25%<br>24%<br>23%<br>22%<br>Oe<br>Dec-11 Mar-12 Jun-12 Sep-12 Dec-12 Mar-13 Jun-13 Sep-13 Dec-13 Mar-14 Jun-14 Sep-14 Dec-14 Mar-15 Jun-15 Sep-15 Dec-15 Mar-16 Jun-16 Sep-16 Dec-16 Mar-17 Jun-17 Sep-17 Dec-17<br>**----- End of picture text -----**<br>


Source: Haver Analytics, Morgan Stanley Research 

**Exhibit 5:** USD debt (% of GDP) 

|China<br>~~ee~~<br>~~|~~<br>~~|~~|6.7<br>~~ee~~<br>~~|~~<br>~~|~~|8.9<br>~~ee~~|11.5<br>~~ee~~<br>~~EE~~|12.2<br>~~ee~~<br>~~EE~~<br>~~pe~~|
|---|---|---|---|---|
|Korea<br>~~|~~<br>~~|~~<br>~~|~~|44.0<br>~~|~~<br>~~|~~<br>~~|~~|37.4<br>~~|~~|39.1<br>~~EE~~<br>~~|~~|36.3<br>~~EE~~<br>~~pe~~|
|Singapore<br>~~|~~<br>~~|~~<br>~~|~~|140.4<br>~~|~~<br>~~|~~<br>~~|~~|145.9<br>~~|~~|159.6<br>~~|~~<br>~~a~~|153.4<br>~~pe~~<br>~~a~~|
|Hong Kong<br>~~|~~<br>~~|~~|143.9<br>~~|~~<br>~~|~~<br>~~|~~|185.5<br>~~|~~<br>~~|~~|247.7<br>~~|~~<br>~~a~~<br>~~|~~|231.4<br>~~a~~|
|Thailand<br>~~|~~|9.6<br>~~|~~<br>~~|~~<br>~~es~~|14.1<br>~~|~~<br>~~ee~~|19.7<br>~~a~~<br>~~|~~<br>~~ee~~|17.0<br>~~a~~|
|Indonesia|13.9<br>~~|~~<br>~~es~~<br>~~a~~|14.1<br>~~|~~<br>~~ee~~<br>~~es~~|21.2<br>~~|~~<br>~~ee~~<br>~~ee~~|20.7|
|Malaysia|18.8<br>~~es~~<br>~~a~~|19.3<br>~~ee~~<br>~~es~~|30.4<br>~~ee~~<br>~~ee~~|29.0<br>~~ee~~|
|India|12.2<br>~~a~~<br>~~eee~~|15.5<br>~~es~~<br>~~eee~~|16.2<br>~~ee~~<br>~~eee~~|12.9<br>~~eee~~<br>~~ee~~|
|Russian Federation<br>~~|~~|23.5<br>~~|~~|21.9|29.9<br>~~a~~|20.1<br>~~ee~~<br>~~a~~|
|Turkey<br>~~|~~|22.7<br>~~|~~<br>~~P|~~|28.6<br>~~P|~~|39.6<br>~~a~~<br>~~a~~<br>~~|~~|43.2<br>~~a~~<br>~~a~~<br>~~|~~|
|South Africa<br>~~|~~<br>~~|~~|12.2<br>~~|~~<br>~~P|~~<br>~~|~~|14.4<br>~~P|~~<br>~~a~~|17.5<br>~~a~~<br>~~a~~<br>~~|~~<br>~~ee~~|19.8<br>~~a~~<br>~~a~~<br>~~|~~<br>~~a~~|
|Hungary<br>~~|~~|22.0<br>~~P|~~<br>~~|~~|16.6<br>~~P|~~<br>~~a~~|32.8<br>~~a~~<br>~~|~~<br>~~ee~~|30.2<br>~~a~~<br>~~|~~<br>~~a~~|
|Poland<br>~~|~~<br>~~Pe~~|4.1<br>~~|~~<br>~~Pe~~|5.7<br>~~a~~|8.0<br>~~|~~<br>~~ee~~<br>~~ee~~|8.4<br>~~|~~<br>~~a~~<br>~~ee~~|
|Czech<br>~~|~~<br>~~Pe~~|2.3<br>~~|~~<br>~~Pe~~<br>~~|~~<br>~~|~~|2.4<br>~~a~~<br>~~|~~<br>|5.0<br>~~ee ~~<br>~~ee~~<br>~~P|~~<br>~~|~~<br>|2.5<br> ~~a~~<br>~~ee~~<br>~~|~~<br>|
|Saudi Arabia<br>~~Pe~~|12.1<br>~~Pe~~<br>~~|~~<br>~~|~~|7.1<br>~~|~~<br>|10.9<br>~~ee~~<br>~~P|~~<br>~~|~~<br>|19.6<br>~~ee~~<br>~~|~~<br>|
|Israel<br>~~|~~|38.5<br>~~|~~<br>~~| ~~<br>~~|~~|34.0<br>~~|~~<br>|28.3<br>~~P|~~<br>~~|~~<br> ~~a~~|28.2<br>~~|~~<br>~~a~~|
|Brazil<br>~~|~~<br>~~|~~|16.9<br> <br>~~|~~<br>~~|~~|22.8<br>|28.7<br> ~~a~~<br>~~|~~<br>~~|~~|24.1<br>~~a~~<br>~~|~~|
|Mexico<br>~~|~~<br>~~|~~<br>~~rr~~|11.2<br> <br>~~|~~<br>~~|~~<br>~~rr~~|13.6<br> <br>~~eee~~|18.0<br> ~~a~~<br>~~|~~<br>~~|~~<br>~~eee~~|20.7<br>~~a~~<br>~~|~~<br>~~eee~~|
|Colombia<br>~~|~~<br>~~rr~~|13.5<br>~~|~~<br>~~rr~~<br>~~a~~|16.8<br>~~eee~~<br>~~es~~|30.9<br>~~|~~<br>~~|~~<br>~~eee~~<br>~~ee~~|30.2<br>~~|~~<br>~~eee~~|
|Chile<br>~~rr~~|34.2<br>~~rr ~~<br>~~a~~<br>~~7~~|35.3<br> ~~eee~~<br>~~es~~<br>~~re~~|43.0<br>~~eee~~<br>~~ee~~<br>~~en~~|43.4<br>~~eee~~|
|Argentina|46.5<br>~~a~~<br>~~7~~|25.6<br>~~es~~<br>~~re~~|30.1<br>~~ee~~<br>~~en~~|40.7|



Source: IIF, Haver Analytics, Morgan Stanley Research; Note: USD debt across sovereign, non-financial corporates, financial corporates and households 

4 

## Importance of the carry trade as a systemic explanatory factor 

It is a well-known feature of carry trade strategies to be highly dependent on risk sentiment. Christiansen, Ranaldo and Söderlind argue that carry trade returns are highly dependent on the market's risk regime, i.e., the sensitivity of carry trades strategy tends to increase in highly volatile markets compared to "normal" times. 

As we showed in EM Under a Lower Sharpe Ratio Regime (March 12, 2018), not only did EM returns tend to be lower under more risk-averse regimes, but returns drawdown tended to be steeper as the skew and kurtosis of EM returns increased. In the same vein, pure EM carry strategies possess a very similar feature. As shown in Exhibit 7, there exists a negative and nonlinear relationship between EM carry returns and risk appetite (proxied by our EM risk sentiment index we introduced in EM Under a Lower Sharpe Ratio Regime: The Model, March 12, 2018). 

In this regard, we think that the return of carry strategies provides additional information on systemic variation in risk sentiment while being "orthogonal" to the USD factor (by construction), which could explain a higher correlation of EMFX pairs which is not related to an idiosyncratic factor. 

**Exhibit 6:** Carry tends to underperform in highly volatile regimes 

**==> picture [231 x 129] intentionally omitted <==**

**----- Start of picture text -----**<br>
Carry strategy - cumulative performance<br>100%<br>80%<br>60%<br>40%<br>20%<br>0%<br>-20%<br>MS Risk-adjusted EM (Naïve) G10 (Naïve)<br>-40%<br>Feb-02 May-04 Aug-06 Nov-08 Feb-11 May-13 Aug-15 Nov-17<br>**----- End of picture text -----**<br>


Source: Bloomberg, Morgan Stanley Research; Note: A naïve carry strategy does not adjust by vol and does not target any specific level of risk 

**Exhibit 7:** EM carry is nonlinearly and negatively associated with risk sentiment 

**==> picture [239 x 128] intentionally omitted <==**

**----- Start of picture text -----**<br>
1.0<br>x-axis: MS risk index (daily change)<br>y-axis: EM carry naive (daily return)<br>0.5<br>0.0<br>-0.2 -0.1 0.0 0.1 0.2 0.3<br>-0.5<br>-1.0<br>y = -6.6205x [2] - 2.7512x + 0.0073<br>-1.5 R² = 0.0696<br>**----- End of picture text -----**<br>


Source: Bloomberg, Morgan Stanley Research; Note: The naïve EM carry strategy holds the top five yielding EM currencies by funding the position with the bottom five. It is rebalanced on a monthly basis. **A higher risk index means higher risk-aversion. 

5 

## Methodology 

## Currency selection, dollar factor and carry factor 

In order to construct our USD factor (USDF), we selected a basket of EM (2/3) and DM (1/3) currencies filtered by 1) liquidity and 2) not heavily managed by central banks. By averaging the daily change of the selected currencies vis-à-vis USD, we expect the idiosyncratic movements will be averaged out. In the same sense, we decided to use an equally weighted average in order not to over-fit the model and to avoid biasing the behaviour of the USDF by idiosyncratic events in any specific currency pair. The equally weighted USD factor has an 86% correlation with the first principal component of the same basket (see Results). 

For the carry factor, we use a risk-adjusted EM carry index comprised of 10 EM currencies (Bloomberg ticker: MSCBFCAE Index). The index selects the top and bottom five risk-adjusted yields in order to build the basket. It is rebalanced accordingly on a daily basis while targeting some specific level of volatility. For more details, see the Appendix). 

## Two-factor model 

In order to assess idiosyncratic variation in USDEMFX – i.e., variance not attributable to systemic drivers of exchange rates – we leveraged Adrien Verdelhan's approach and apply it to EM with some tweaks in the factors and methodology. 

Verdelhan argues that, as opposed to models that use lagged or contemporaneous interest rate differentials and/or macroeconomic variables at different frequencies, a model that incorporates a USD factor (USDF) and a carry factor (CF) delivers high R- squared. In other words, by using these two factors, we can explain a substantial share of EMFX variation, which helps us to isolate the fluctuations on EMFX that are explained by idiosyncratic factors. 

Originally, the specification is: 

Source: Adrien Verdelhan 

where delta-S refers to the daily change in the nominal spot USDEM exchange rate, i- star to the local EM interest rate, i to the USD interest rate, carry to the daily return of a carry-trading* strategy and dollar to the average daily change of a basket of currencies (quoted versus USD) including developed and emerging market currencies. Under this specification, the bilateral exchange rates fluctuations are explained by the CF, the USDF and the conditional carry factor (CCF), which is the interaction between the interest rate differential (lagged) and the carry trading strategy. The last element incorporates the 

6 

fact that higher yielding currencies should be more sensitive to the CF. Epsilon is regarded as the idiosyncratic variations in the EMFX pair. 

In this piece, we decided to reduce the specification to only two factors by excluding the interactive carry factor, i.e., CCF. The reasoning behind this is due to the low explanatory power of CCF, poor data quality for some EM interest rates at a high frequency and a relative short history for some others. Instead, we use: 

Source: Morgan Stanley Research 

**Exhibit 8:** Observation weight distribution (Exponentially weighted moving linear regression) 

**==> picture [232 x 110] intentionally omitted <==**

**----- Start of picture text -----**<br>
100%<br>Exponentially weighted<br>90%<br>Simple weighteed<br>80%<br>70%<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>0.0 0.5 1.0 1.4 1.9 2.4 2.9<br>Years<br>**----- End of picture text -----**<br>


To overcome this, we run a three-year exponentially weighted moving linear regression (EWMLR using 

lambda equal to 0.985) which should help twofold: 

**1.** The beta associated with the CF should change over time, partially incorporating the change in sensitivity to changes in relative monetary conditions; and 

**2.** Adjusting the relevance of USD as a global factor for EM due to liquidity/funding conditions, stage of the economic cycle and systemic risks, among others. 

Source: Morgan Stanley Research; Note: lambda=0.985 

In order to deal with potential time difference issues in the data, we use weekly data points in our calculation. 

Finally, we accumulate the weekly idiosyncratic variation in each EMFX pair over an arbitrary, although short, period of time, to build our measure for idiosyncratic risk premia (EMFXIRP). We use a six-month window to accumulate the residual of the regression. 

7 

## Results 

In our calculations, the USD factor alone explains 40-50% of the total variance in a EMFX portfolio since 2010 (Exhibit 9), substantially above the average pre-crisis. These results are in line with the increased relevance of USD as stated in USD's relevance for EMFX. 

**Exhibit 9:** Importance of the USD factor in EMFX portfolios 

**Exhibit 10:** Stretch relationship between our proxy for USD factor and first principal component of USDEMFX basket 

**==> picture [522 x 178] intentionally omitted <==**

**----- Start of picture text -----**<br>
% of variance explained by the USD factor (3y rolling window)<br>50% Y- Dollar Factor<br>3<br>45% Trend<br>2<br>40% 1<br>35% 0<br>-1<br>30%<br>Jan-05 Aug-06 Mar-08 Oct-09 May-11 Dec-12 Jul-14 Feb-16 Sep-17 -2 R² = 0.7362<br>Correlation=86%<br>Source: Morgan Stanley research -3<br>-20 -10 0 10 20<br>X-First Principal Component<br>Source: Morgan Stanley Research<br>**----- End of picture text -----**<br>


Not surprisingly, when taking the correlations of USDEMFX pairs (Exhibit 11), most of them are strongly and positively correlated (in red) with the strongest correlation vis-avis the USD factor. There are some exceptions like USDCNY due to the fact that the renminbi remains a heavily managed currency (we decided not to exclude it in our exercise due to the increasing importance of CNY in global markets). On the other hand, most of the currency pairs are negatively correlated with the carry factor as expected. 

In Exhibit 12 we show the correlation matrix of EMFX pairs once we remove the systemic variation – i.e., extracting idiosyncratic variance. As the image shows, correlations disappear as the systemic factors have been filtered out. Yet, some clusters remain. This could be explained by shared systemic variations depending on the region, commodity exposure and/or additional factors. 

For instance, the statistically significant correlation of risk premia in BRL, CLP and COP; MYR and THB; PLN, HUF and CZK could be explained on a regional basis, and/or due to an EUR factor in the case of PLN, HUF and CZK. On the other hand, RUB and COP risk premia correlation could be explained by a commodity factor (oil), as both are regarded as oil currencies. Our idiosyncratic variation measure can be adjusted by additional factors in order to consider particular cases. 

8 

**Exhibit 11:** EMFX, DF and CF correlation matrix 

**Exhibit 12:** EMFX idiosyncratic risk premia correlation matrix 

Source: Morgan Stanley Research; Note: CF refers to the carry factor while DF refers to the dollar factor. 

Source: Morgan Stanley Research; Note: CF refers to the carry factor while DF refers to the dollar factor. 

In line with this, the USD factor betas of all the currencies pairs (Exhibit 14) are positive. CEEMEA and LatAm, on average, have a higher beta than one, while Asia is the region with a lower sensitivity to the USD factor. It is important to highlight as well that the dispersion among the betas has decreased over time, being the same case for the adjusted R-squared of the complete specification. 

**Exhibit 13:** Adjusted R-squared 

**==> picture [243 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
80%<br>70% rT Average Adj R-squared iy Last 3y Adj R-squared<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Source: Morgan Stanley Research<br>IDR PLN HUF ZAR MYR CZK COP THB KRW TRY BRL INR RUB MXN CLP ILS CNY<br>**----- End of picture text -----**<br>


**Exhibit 14:** USD factor betas 

**==> picture [243 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
2.5<br>Lt Average USD Beta = Last USD Beta<br>2.0<br>1.5<br>1.0<br>0.5<br>0.0<br>Source: Morgan Stanley Research<br>ZAR COP RUB BRL MXN TRY PLN MYR HUF CLP KRW IDR CZK THB ILS INR CNY<br>**----- End of picture text -----**<br>


Regarding the idiosyncratic factor (the residual of our specification), Exhibit 16 shows the average standard deviation of the model over time. Some of the "high" betas also tend to have a high idiosyncratic risk variation, but that seems to be associated more with the intrinsic volatility properties of each EMFX pair rather than a more robust relationship as it does not hold for the "average" or "low" betas. 

The betas associated with the carry factor show the expected pattern. Those currencies with relatively low interest rates tend to have a positive beta, while the currencies with historically high interest rates show a negative sensitivity (USDEMFX goes down when carry performs well). For instance, BRL RUB and TRY are among the currencies with the highest sensitivity to the carry factor. 

9 

**Exhibit 15:** Betas associated with the carry factor 

**==> picture [238 x 115] intentionally omitted <==**

**----- Start of picture text -----**<br>
1.0<br>0.8 Average Carry Beta Last Carry Beta<br>0.6<br>0.4<br>0.2<br>0.0<br>-0.2<br>-0.4<br>-0.6<br>-0.8<br>-1.0<br>-1.2<br>Source: Morgan Stanley Research<br>HUF CZK PLN KRW ILS CNY CLP ZAR MXN THB INR COP TRY MYR RUB IDR BRL<br>**----- End of picture text -----**<br>


**Is it tradable?** While we do not perform a formal backtest of any sort of strategy related to our model, we do calculate the halflife of the cumulative six-month idiosyncratic variance in order to assess whether it reverses fast enough (less than 26 weeks). We find that the average half-life (excluding CNY) in our EMFX sample is 20, suggesting that the series tend to revert fast enough to provide us with relevant signals. LatAm tend to revert faster (14 weeks on average), followed by CEEMEA (23) and Asia (28). 

**Exhibit 16:** Average sigma of two-factor model 

**==> picture [216 x 115] intentionally omitted <==**

**----- Start of picture text -----**<br>
12%<br>10%<br>8%<br>6%<br>4%<br>2%<br>0%<br>Average sigma of regression<br>ZAR BRL COP CLP TRY HUF RUB PLN MXN KRW CZK ILS IDR INR THB MYR CNY<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

**Exhibit 17:** Mean reversion: risk-premia half-life 

**==> picture [219 x 128] intentionally omitted <==**

**----- Start of picture text -----**<br>
y-axis: # of weeks<br>50<br>40<br>30<br>20<br>10<br>0<br>Half-Life (all sample) Half-Life (post crisis)<br>Source: Morgan Stanley Research<br>MXN BRL COP CLP MYR KRW IDR INR THB CNY HUF RUB ILS TRY ZAR CZK PLN<br>**----- End of picture text -----**<br>


**What is priced in?** In Exhibit 18, we plot, ordered by "z-score", our measure of six-month cumulative risk premia. The bars denote the range between the 90% and 5% percentiles assuming a normal distribution. We use asymmetric percentiles in order to incorporate the fact that EM currencies tend to have a negative skew. 

Within our framework, the top three currencies with the lowest accumulated risk premia on a vol-scaled basis in the past six months are CNY, ZAR and THB, while the ones with the highest are TRY, HUF and CZK. Only those with low risk premia are at or above reversal levels, while the "cheap" currencies still have room to underperform before reaching "stretched" levels. In the case of CNY it is difficult to draw the same conclusions as with other currencies due to the low level of systematic variance and the fact that it is a heavily managed currency – this is why CNY is the currency that mean-reverts more slowly (Exhibit 29). 

For THB, by taking a look at Historical 6m cumulative idiosyncratic risk premia, it seems to be close to a sell signal. Historically, deviations beyond the established confidence band are limited, and usually associated with reversals in USDMYR. On ZAR, deviations beyond 90% tend to be more common than for most of the currencies, suggesting that its good performance could continue for longer despite being one of the bestperforming currencies in the past six months. 

On the other hand, with respect to TRY, HUF and CZK, although with high risk premia on a relative basis (compared to other EMs), to us the deviation seems to be quite modest and does not signal any stressed pricing in the currency pairs. In particular, TRY has not reached extreme levels despite its recent underperformance in EM. Finally, having three European currencies clustered on the "cheap" side might be associated with the EUR factor already discussed, particularly with eurozone political uncertainty. 

10 

**Exhibit 18:** EMFX idiosyncratic risk premia boxplots (cumulative 6m) 

**==> picture [350 x 217] intentionally omitted <==**

**----- Start of picture text -----**<br>
25%<br>Low risk-premia 04-Jun-18<br>13%<br>0%<br>-13%<br>High risk-premia<br>-25%<br>CNY ZAR THB MYR COP CLP KRW MXN IDR RUB BRL ILS INR PLN CZK HUF TRY<br>Source: Morgan Stanley Research; Note: The edges of the boxplots represent the 5% and 90% percentile assuming a normal distribution with mean zero<br>and using standard deviation of our two-factor model. While the cumulative 6m idiosyncratic variation in EMFX does not distribute normally, it serves as a<br>benchmark in order to assess extreme pricing.<br>**----- End of picture text -----**<br>


11 

## Appendix 

## Two-factor model stats 

**Exhibit 19:** Two-factor model stats 

|||||**Percentiles**|**Percentiles**||||**Betas**|**Betas**|
|---|---|---|---|---|---|---|---|---|---|---|
||**6m cumulative**<br>**residual***|**SD of residual**<br>**(weekly)**|**Z-Score**|**5%**|**90%**|**Half-Life**<br>**(months)**|**Adjusted R-**<br>**squared**|**USD**<br>**Factor**||**Carry**<br>**Factor**|
|**MXN**|0.52%|10.67%|0.05|-18%|14%|3.5|38%|1.20||-0.10|
|**BRL**|-5.88%|12.59%|-0.47|-21%|16%|2.9|44%|1.42||-1.03|
|**COP**|9.93%|11.94%|0.83|-20%|15%|4.4|48%|1.61||-0.49|
|**CLP**|3.22%|8.17%|0.39|-13%|10%|2.4|37%|0.91||0.06|
|**MYR**|9.41%|8.43%|1.12|-14%|11%|5.0|49%|1.09||-0.69|
|**KRW**|1.82%|7.04%|0.26|-12%|9%|2.9|44%|0.90||0.11|
|**IDR**|-1.34%|5.58%|-0.24|-9%|7%|7.1|65%|0.80||-0.98|
|**INR**|-2.47%|3.85%|-0.64|-6%|5%|4.2|41%|0.41||-0.30|
|**THB**|4.74%|4.17%|1.14|-7%|5%|5.6|47%|0.55||-0.20|
|**CNY**|4.75%|3.74%|1.27|-6%|5%|13.3|15%|0.23||0.04|
|**HUF**|-7.17%|6.98%|-1.03|-11%|9%|4.8|58%|1.02||0.76|
|**RUB**|-3.76%|13.98%|-0.27|-23%|18%|7.8|40%|1.55||-0.76|
|**ILS**|-3.78%|5.95%|-0.63|-10%|8%|3.4|29%|0.55||0.10|
|**TRY**|-10.25%|9.68%|-1.06|-16%|12%|4.8|45%|1.15||-0.70|
|**ZAR**|16.55%|13.59%|1.22|-22%|17%|5.7|55%|2.17||0.03|
|**CZK**|-6.99%|6.86%|-1.02|-11%|9%|5.6|50%|0.79||0.76|
|**PLN**|-6.25%|6.93%|-0.90|-11%|9%|4.8|60%|1.13||0.60|
|Source: Morgan Stanley Research; *A positive number relates to outperformance relative to the two-factor model. **Regression statistics are from the|||||||||Source: Morgan Stanley Research; *A positive number relates to outperformance relative to the two-factor model. **Regression statistics are from the||
|most updated regression. Percentiles are assuming a normal distribution with mean zero.|||||most updated regression. Percentiles are assuming a normal distribution with mean zero.||||||



## Historical 6m cumulative idiosyncratic risk premia 

**Exhibit 20:** MXN: 6m cumulative idiosyncratic risk premia 

**==> picture [250 x 151] intentionally omitted <==**

**----- Start of picture text -----**<br>
MXN<br>20%<br>15%<br>10%<br>5%<br>0%<br>-5%<br>-10%<br>-15%<br>-20%<br>-25%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution,<br>standard deviation of the two-factor model and a mean equal to zero.<br>**----- End of picture text -----**<br>


**Exhibit 21:** BRL: 6m cumulative idiosyncratic risk premia 

**==> picture [250 x 151] intentionally omitted <==**

**----- Start of picture text -----**<br>
BRL<br>40%<br>30%<br>20%<br>10%<br>0%<br>-10%<br>-20%<br>-30%<br>-40%<br>-50%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution,<br>standard deviation of the two-factor model and a mean equal to zero.<br>**----- End of picture text -----**<br>


12 

**Exhibit 22:** COP: 6m cumulative idiosyncratic risk premia 

**==> picture [244 x 129] intentionally omitted <==**

**----- Start of picture text -----**<br>
COP<br>30%<br>20%<br>10%<br>0%<br>-10%<br>-20%<br>-30%<br>-40%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution, standard deviation of the two-factor model and a mean equal to zero. 

**Exhibit 24:** MYR: 6m cumulative idiosyncratic risk premia 

**==> picture [244 x 128] intentionally omitted <==**

**----- Start of picture text -----**<br>
MYR<br>15%<br>10%<br>5%<br>0%<br>-5%<br>-10%<br>-15%<br>-20%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution, standard deviation of the two-factor model and a mean equal to zero. 

**==> picture [245 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Exhibit 26: IDR: 6m cumulative idiosyncratic risk premia<br>IDR<br>20%<br>15%<br>10%<br>5%<br>0%<br>-5%<br>-10%<br>-15%<br>-20%<br>-25%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution, standard deviation of the two-factor model and a mean equal to zero. 

**Exhibit 23:** CLP: 6m cumulative idiosyncratic risk premia CLP 

**==> picture [243 x 115] intentionally omitted <==**

**----- Start of picture text -----**<br>
20%<br>10%<br>0%<br>-10%<br>-20%<br>-30%<br>-40%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution, standard deviation of the two-factor model and a mean equal to zero. 

**Exhibit 25:** KRW: 6m cumulative idiosyncratic risk premia 

**==> picture [243 x 128] intentionally omitted <==**

**----- Start of picture text -----**<br>
KRW<br>25%<br>20%<br>15%<br>10%<br>5%<br>0%<br>-5%<br>-10%<br>-15%<br>-20%<br>-25%<br>-30%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution, standard deviation of the two-factor model and a mean equal to zero. 

**Exhibit 27:** INR: 6m cumulative idiosyncratic risk premia 

**==> picture [243 x 129] intentionally omitted <==**

**----- Start of picture text -----**<br>
INR<br>15%<br>10%<br>5%<br>0%<br>-5%<br>-10%<br>-15%<br>-20%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution, standard deviation of the two-factor model and a mean equal to zero. 

13 

**Exhibit 28:** THB: 6m cumulative idiosyncratic risk premia 

**==> picture [250 x 151] intentionally omitted <==**

**----- Start of picture text -----**<br>
THB<br>15%<br>10%<br>5%<br>0%<br>-5%<br>-10%<br>-15%<br>-20%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution,<br>standard deviation of the two-factor model and a mean equal to zero.<br>**----- End of picture text -----**<br>


**Exhibit 30:** HUF: 6m cumulative idiosyncratic risk premia 

**==> picture [250 x 150] intentionally omitted <==**

**----- Start of picture text -----**<br>
HUF<br>30%<br>20%<br>10%<br>0%<br>-10%<br>-20%<br>-30%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution,<br>standard deviation of the two-factor model and a mean equal to zero.<br>**----- End of picture text -----**<br>


**==> picture [245 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Exhibit 32: ILS: 6m cumulative idiosyncratic risk premia<br>ILS<br>20%<br>15%<br>10%<br>5%<br>0%<br>-5%<br>-10%<br>-15%<br>-20%<br>-25%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution, standard deviation of the two-factor model and a mean equal to zero. 

**Exhibit 29:** CNY: 6m cumulative idiosyncratic risk premia 

**==> picture [243 x 129] intentionally omitted <==**

**----- Start of picture text -----**<br>
CNY<br>8%<br>6%<br>4%<br>2%<br>0%<br>-2%<br>-4%<br>-6%<br>-8%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution, standard deviation of the two-factor model and a mean equal to zero. 

**Exhibit 31:** RUB: 6m cumulative idiosyncratic risk premia 

**==> picture [243 x 128] intentionally omitted <==**

**----- Start of picture text -----**<br>
RUB<br>40%<br>20%<br>0%<br>-20%<br>-40%<br>-60%<br>-80%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution, standard deviation of the two-factor model and a mean equal to zero. 

**Exhibit 33:** TRY: 6m cumulative idiosyncratic risk premia 

**==> picture [243 x 129] intentionally omitted <==**

**----- Start of picture text -----**<br>
TRY<br>40%<br>30%<br>20%<br>10%<br>0%<br>-10%<br>-20%<br>-30%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution, standard deviation of the two-factor model and a mean equal to zero. 

14 

**Exhibit 34:** ZAR: 6m cumulative idiosyncratic risk premia 

**==> picture [244 x 129] intentionally omitted <==**

**----- Start of picture text -----**<br>
ZAR<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>-10%<br>-20%<br>-30%<br>-40%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution, standard deviation of the two-factor model and a mean equal to zero. 

**Exhibit 35:** CZK: 6m cumulative idiosyncratic risk premia 

**==> picture [16 x 7] intentionally omitted <==**

**----- Start of picture text -----**<br>
CZK<br>**----- End of picture text -----**<br>


**==> picture [243 x 115] intentionally omitted <==**

**----- Start of picture text -----**<br>
25%<br>20%<br>15%<br>10%<br>5%<br>0%<br>-5%<br>-10%<br>-15%<br>-20%<br>-25%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution, standard deviation of the two-factor model and a mean equal to zero. 

**Exhibit 36:** PLN: 6m cumulative idiosyncratic risk premia 

**==> picture [244 x 128] intentionally omitted <==**

**----- Start of picture text -----**<br>
PLN<br>20%<br>15%<br>10%<br>5%<br>0%<br>-5%<br>-10%<br>-15%<br>-20%<br>-25%<br>Jul-05 Dec-06 May-08 Oct-09 Mar-11 Aug-12 Jan-14 Jun-15 Nov-16 Apr-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research; Note: Dashed lines represent 5% and 90% assuming a normal distribution, standard deviation of the two-factor model and a mean equal to zero. 

15 

## Historical adjusted R-squared – 3y rolling 

**Exhibit 37:** MXN: 3y rolling adjusted R-squared 

**==> picture [241 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
MXN<br>80%<br>70%<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


**Exhibit 38:** BRL: 3y rolling adjusted R-squared 

**==> picture [242 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
BRL<br>80%<br>70%<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


**Exhibit 39:** COP: 3y rolling adjusted R-squared 

**==> picture [241 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
COP<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


**Exhibit 40:** CLP: 3y rolling adjusted R-squared 

**==> picture [240 x 129] intentionally omitted <==**

**----- Start of picture text -----**<br>
CLP<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

**Exhibit 41:** MYR: 3y rolling adjusted R-squared 

**==> picture [241 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
MYR<br>70%<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


**Exhibit 42:** KRW: 3y rolling adjusted R-squared 

**==> picture [242 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
KRW<br>80%<br>70%<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


16 

**Exhibit 43:** IDR: 3y rolling adjusted R-squared 

**==> picture [241 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
IDR<br>70%<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


**Exhibit 45:** THB: 3y rolling adjusted R-squared 

**==> picture [241 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
THB<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


**Exhibit 47:** HUF: 3y rolling adjusted R-squared 

**==> picture [241 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
HUF<br>90%<br>80%<br>70%<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


**Exhibit 44:** INR: 3y rolling adjusted R-squared 

**==> picture [240 x 130] intentionally omitted <==**

**----- Start of picture text -----**<br>
INR<br>70%<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

**Exhibit 46:** CNY: 3y rolling adjusted R-squared 

**==> picture [242 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
CNY<br>20%<br>18%<br>16%<br>14%<br>12%<br>10%<br>8%<br>6%<br>4%<br>2%<br>0%<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


**Exhibit 48:** RUB: 3y rolling adjusted R-squared 

**==> picture [242 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
RUB<br>80%<br>70%<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


17 

**Exhibit 49:** ILS: 3y rolling adjusted R-squared 

**==> picture [241 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
ILS<br>70%<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


**Exhibit 51:** ZAR: 3y rolling adjusted R-squared 

**==> picture [241 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
ZAR<br>80%<br>70%<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


**Exhibit 50:** TRY: 3y rolling adjusted R-squared 

**==> picture [242 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
TRY<br>90%<br>80%<br>70%<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


**Exhibit 52:** CZK: 3y rolling adjusted R-squared 

**==> picture [240 x 130] intentionally omitted <==**

**----- Start of picture text -----**<br>
CZK<br>90%<br>80%<br>70%<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

## **Exhibit 53:** PLN: 3y rolling adjusted R-squared 

**==> picture [236 x 143] intentionally omitted <==**

**----- Start of picture text -----**<br>
PLN<br>90%<br>80%<br>70%<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


18 

## Historical beta to the USD factor 

**Exhibit 54:** MXN: Beta to the USD factor 

**==> picture [241 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
MXN<br>1.6<br>1.4<br>1.2<br>1.0<br>0.8<br>0.6<br>0.4<br>0.2<br>0.0<br>-0.2<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


**Exhibit 55:** BRL: Beta to the USD factor 

**==> picture [242 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
BRL<br>2.5<br>2.0<br>1.5<br>1.0<br>0.5<br>0.0<br>-0.5<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


## **Exhibit 56:** COP: Beta to the USD factor 

**==> picture [241 x 345] intentionally omitted <==**

**----- Start of picture text -----**<br>
COP<br>1.8<br>1.6<br>1.4<br>1.2<br>1.0<br>0.8<br>0.6<br>0.4<br>0.2<br>0.0 'Le<br>Source: Morgan Stanley Research<br>Exhibit 58: MYR: Beta to the USD factor<br>MYR<br>1.2<br>1.0<br>0.8<br>0.6<br>0.4<br>0.2<br>0.0<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


**Exhibit 57:** CLP: Beta to the USD factor 

**==> picture [242 x 345] intentionally omitted <==**

**----- Start of picture text -----**<br>
CLP<br>1.2<br>1.0<br>0.8<br>0.6<br>0.4<br>0.2<br>0.0<br>Source: Morgan Stanley Research<br>Exhibit 59: KRW: Beta to the USD factor<br>KRW<br>1.6<br>1.4<br>1.2<br>1.0<br>0.8<br>0.6<br>0.4<br>0.2<br>0.0<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


19 

**Exhibit 60:** IDR: Beta to the USD factor 

**==> picture [241 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
IDR<br>0.9<br>0.8<br>0.7<br>0.6<br>0.5<br>0.4<br>0.3<br>0.2<br>0.1<br>0.0<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


## **Exhibit 62:** THB: Beta to the USD factor 

**==> picture [241 x 345] intentionally omitted <==**

**----- Start of picture text -----**<br>
THB<br>0.7<br>0.6<br>0.5<br>0.4<br>0.3<br>0.2<br>0.1<br>0.0<br>Source: Morgan Stanley Research<br>Exhibit 64: HUF: Beta to the USD factor<br>HUF<br>2.5<br>2.0<br>1.5<br>1.0<br>0.5<br>0.0<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


**Exhibit 61:** INR: Beta to the USD factor 

**==> picture [242 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
INR<br>1.2<br>1.0<br>0.8<br>0.6<br>0.4<br>0.2<br>0.0<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


## **Exhibit 63:** CNY: Beta to the USD factor 

**==> picture [242 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
CNY<br>0.3<br>0.2<br>0.2<br>0.1<br>0.1<br>0.0<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


**Exhibit 65:** RUB: Beta to the USD factor 

**==> picture [242 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
RUB<br>2.5<br>2.0<br>1.5<br>1.0<br>0.5<br>0.0<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


20 

**Exhibit 66:** ILS: Beta to the USD factor 

**==> picture [241 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
ILS<br>1.0<br>0.9<br>0.8<br>0.7<br>0.6<br>0.5<br>0.4<br>0.3<br>0.2<br>0.1<br>0.0<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


## **Exhibit 68:** ZAR: Beta to the USD factor 

**==> picture [241 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
ZAR<br>3.5<br>3.0<br>2.5<br>2.0<br>1.5<br>1.0<br>0.5<br>0.0<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


**Exhibit 67:** TRY: Beta to the USD factor 

**==> picture [242 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
TRY<br>2.0<br>1.8<br>1.6<br>1.4<br>1.2<br>1.0<br>0.8<br>0.6<br>0.4<br>0.2<br>0.0<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


## **Exhibit 69:** CZK: Beta to the USD factor 

**==> picture [242 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
CZK<br>3.0<br>2.5<br>2.0<br>1.5<br>1.0<br>0.5<br>0.0<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


## **Exhibit 70:** PLN: Beta to the USD factor 

**==> picture [236 x 143] intentionally omitted <==**

**----- Start of picture text -----**<br>
PLN<br>2.5<br>2.0<br>1.5<br>1.0<br>0.5<br>0.0<br>Source: Morgan Stanley Research<br>Jul-05 Feb-06 Sep-06 Apr-07 Nov-07 Jun-08 Jan-09 Aug-09 Mar-10 Oct-10 May-11 Dec-11 Jul-12 Feb-13 Sep-13 Apr-14 Nov-14 Jun-15 Jan-16 Aug-16 Mar-17 Oct-17 May-18<br>**----- End of picture text -----**<br>


21 

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

(as of May 31, 2018) 

The Stock Ratings described below apply to Morgan Stanley's Fundamental Equity Research and do not apply to Debt Research produced by the Firm. For disclosure purposes only (in accordance with NASD and NYSE requirements), we include the category headings of Buy, Hold, and Sell alongside our ratings of Overweight, Equal-weight, Not-Rated and Underweight. Morgan Stanley does not assign ratings of Buy, Hold or Sell to the stocks we cover. Overweight, Equal-weight, Not-Rated and Underweight are not the equivalent of buy, hold, and sell but represent recommended relative weightings (see definitions below). To satisfy regulatory requirements, we correspond Overweight, our most positive stock rating, with a buy recommendation; we correspond Equal-weight and Not-Rated to hold and Underweight to sell recommendations, respectively. 

||COVERAGE UNIVERSE|COVERAGE UNIVERSE|INVESTMENT BANKING CLIENTS (IBC)|INVESTMENT BANKING CLIENTS (IBC)|INVESTMENT BANKING CLIENTS (IBC)|OTHER MATERIAL|OTHER MATERIAL|
|---|---|---|---|---|---|---|---|
|||||||INVESTMENT SERVICES||
|||||||CLIENTS(MISC)||
|STOCK RATING|COUNT|% OF|COUNT|% OF|% OF|COUNT|% OF|
|CATEGORY||TOTAL||TOTAL IBC|RATING||TOTAL|
||||||CATEGORY||OTHER|
||||||||MISC|
|**Overweight/Buy**|**1172**|**38%**|**289**|**40%**|**25%**|**551**|**39%**|
|**Equal-weight/Hold**|**1338**|**43%**|**354**|**49%**|**26%**|**639**|**46%**|
|**Not-Rated/Hold**|**53**|**2%**|**5**|**1%**|**9%**|**7**|**0%**|
|**Underweight/Sell**|**533**|**17%**|**77**|**11%**|**14%**|**207**|**15%**|
|**TOTAL**|**3,096**||**725**|||**1404**||



Data include common stock and ADRs currently assigned ratings. Investment Banking Clients are companies from whom Morgan Stanley received investment banking compensation in the last 12 months. Due to rounding off of decimals, the percentages provided in the "% of total" column may not add up to exactly 100 percent. 

22 

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

23 

information in Morgan Stanley Research change apart from when we intend to discontinue equity research coverage of a subject company. Facts and views presented in Morgan Stanley Research have not been reviewed by, and may not reflect information known to, professionals in other Morgan Stanley business areas, including investment banking personnel. 

Morgan Stanley Research personnel may participate in company events such as site visits and are generally prohibited from accepting payment by the company of associated expenses unless pre-approved by authorized members of Research management. Morgan Stanley may make investment decisions that are inconsistent with the recommendations or views in this report. 

To our readers based in Taiwan or trading in Taiwan securities/instruments: Information on securities/instruments that trade in Taiwan is distributed by Morgan Stanley Taiwan Limited ("MSTL"). Such information is for your reference only. The reader should independently evaluate the investment risks and is solely responsible for their investment decisions. Morgan Stanley Research may not be distributed to the public media or quoted or used by the public media without the express written consent of Morgan Stanley. Any non-customer reader within the scope of Article 7-1 of the Taiwan Stock Exchange Recommendation Regulations accessing and/or receiving Morgan Stanley Research is not permitted to provide Morgan Stanley Research to any third party (including but not limited to related parties, affiliated companies and any other third parties) or engage in any activities regarding Morgan Stanley Research which may create or give the appearance of creating a conflict of interest. Information on securities/instruments that do not trade in Taiwan is for informational purposes only and is not to be construed as a recommendation or a solicitation to trade in such securities/instruments. MSTL may not execute transactions for clients in these securities/instruments. 

Morgan Stanley is not incorporated under PRC law and the research in relation to this report is conducted outside the PRC. Morgan Stanley Research does not constitute an offer to sell or the solicitation of an offer to buy any securities in the PRC. PRC investors shall have the relevant qualifications to invest in such securities and shall be responsible for obtaining all relevant approvals, licenses, verifications and/or registrations from the relevant governmental authorities themselves. Neither this report nor any part of it is intended as, or shall constitute, provision of any consultancy or advisory service of securities investment as defined under PRC law. Such information is provided for your reference only. 

Morgan Stanley Research is disseminated in Brazil by Morgan Stanley C.T.V.M. S.A.; in Mexico by Morgan Stanley México, Casa de Bolsa, S.A. de C.V which is regulated by Comision Nacional Bancaria y de Valores. Paseo de los Tamarindos 90, Torre 1, Col. Bosques de las Lomas Floor 29, 05120 Mexico City; in Japan by Morgan Stanley MUFG Securities Co., Ltd. and, for Commodities related research reports only, Morgan Stanley Capital Group Japan Co., Ltd; in Hong Kong by Morgan Stanley Asia Limited (which accepts responsibility for its contents) and by Morgan Stanley Asia International Limited, Hong Kong Branch; in Singapore by Morgan Stanley Asia (Singapore) Pte. (Registration number 199206298Z) and/or Morgan Stanley Asia (Singapore) Securities Pte Ltd (Registration number 200008434H), regulated by the Monetary Authority of Singapore (which accepts legal responsibility for its contents and should be contacted with respect to any matters arising from, or in connection with, Morgan Stanley Research) and by Morgan Stanley Asia International Limited, Singapore Branch (Registration number T11FC0207F); in Australia to "wholesale clients" within the meaning of the Australian Corporations Act by Morgan Stanley Australia Limited A.B.N. 67 003 734 576, holder of Australian financial services license No. 233742, which accepts responsibility for its contents; in Australia to "wholesale clients" and "retail clients" within the meaning of the Australian Corporations Act by Morgan Stanley Wealth Management Australia Pty Ltd (A.B.N. 19 009 145 555, holder of Australian financial services license No. 240813, which accepts responsibility for its contents; in Korea by Morgan Stanley & Co International plc, Seoul Branch; in India by Morgan Stanley India Company Private Limited; in Indonesia by PT. Morgan Stanley Sekuritas Indonesia; in Canada by Morgan Stanley Canada Limited, which has approved of and takes responsibility for its contents in Canada; in Germany by Morgan Stanley Bank AG, Frankfurt am Main and Morgan Stanley Private Wealth Management Limited, Niederlassung Deutschland, regulated by Bundesanstalt fuer Finanzdienstleistungsaufsicht (BaFin); in Spain by Morgan Stanley, S.V., S.A., a Morgan Stanley group company, which is supervised by the Spanish Securities Markets Commission (CNMV) and states that Morgan Stanley Research has been written and distributed in accordance with the rules of conduct applicable to financial research as established under Spanish regulations; in the US by Morgan Stanley & Co. LLC, which accepts responsibility for its contents. Morgan Stanley & Co. International plc, authorized by the Prudential Regulatory Authority and regulated by the Financial Conduct Authority and the Prudential Regulatory Authority, disseminates in the UK research that it has prepared, and approves solely for the purposes of section 21 of the Financial Services and Markets Act 2000, research which has been prepared by any of its affiliates. RMB Morgan Stanley Proprietary Limited is a member of the JSE Limited and regulated by the Financial Services Board in South Africa. RMB Morgan Stanley Proprietary Limited is a joint venture owned equally by Morgan Stanley International Holdings Inc. and RMB Investment Advisory (Proprietary) Limited, which is wholly owned by FirstRand Limited. The information in Morgan Stanley Research is being disseminated by Morgan Stanley Saudi Arabia, regulated by the Capital Market Authority in the Kingdom of Saudi Arabia , and is directed at Sophisticated investors only. 

The information in Morgan Stanley Research is being communicated by Morgan Stanley & Co. International plc (DIFC Branch), regulated by the Dubai Financial Services Authority (the DFSA), and is directed at Professional Clients only, as defined by the DFSA. The financial products or financial services to which this research relates will only be made available to a customer who we are satisfied meets the regulatory criteria to be a Professional Client. The information in Morgan Stanley Research is being communicated by Morgan Stanley & Co. International plc (QFC Branch), regulated by the Qatar Financial Centre Regulatory Authority (the QFCRA), and is directed at business customers and market counterparties only and is not intended for Retail Customers as defined by the QFCRA. 

As required by the Capital Markets Board of Turkey, investment information, comments and recommendations stated here, are not within the scope of investment advisory activity. Investment advisory service is provided exclusively to persons based on their risk and income preferences by the authorized firms. Comments and recommendations stated here are general in nature. These opinions may not fit to your financial status, risk and return preferences. For this reason, to make an investment decision by relying solely to this information stated here may not bring about outcomes that fit your expectations. The trademarks and service marks contained in Morgan Stanley Research are the property of their respective owners. Third-party data providers make no warranties or representations relating to the accuracy, completeness, or timeliness of the data they provide and shall not have liability for any damages relating to such data. The Global Industry Classification Standard (GICS) was developed by and is the exclusive property of MSCI and S&P. Morgan Stanley Research, or any portion thereof may not be reprinted, sold or redistributed without the written consent of Morgan Stanley. © 2018 Morgan Stanley 

24 


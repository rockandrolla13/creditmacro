June 15, 2017 05:20 PM GMT 

## **Global Interest Rate Strategy** 

## Introducing BMI(2) and xBMI, Improving BMI(10) and iBMI 

We update our original Bond Market Indicators, henceforth BMI(10), and the iBMIs with a new bond market momentum calculation. We add BMI(2) for investors with short-end mandates and a cross-market BMI (xBMI) to aid our tactical cross market calls. FX/rate relationships now feature in our models. 

## **Improving BMI(10)** 

After more than 2 years of publishing our BMIs, we decided to update some aspects of their construction. We changed the bond market momentum factor slightly, and we introduced an FX factor with the aim of boosting cross-market performance - encapsulated in a stand-alone model we will call the xBMI. We also made a series of adjustments to the ACGB, NZGB and CAN BMIs, including a change in the cross market signal check. We explain in detail the novelties in our model and report backtest performance. 

|MORGAN STANLEY ASIA LIMITED+<br>Jesper Rooth||
|---|---|
|STRATEGIST||
|Jesper.Rooth@morganstanley.com<br>MORGAN STANLEY & CO. INTERNATIONAL PLC+|+852 3963-1519<br>MORGAN STANLEY & CO. INTERNATIONAL PLC+|
|Federico.Manicardi@morganstanley.com<br>Federico Manicardi<br>STRATEGIST|+44 20 7425-6538|
|MORGAN STANLEY & CO. LLC<br>Matthew Hornbach||
|Matthew.Hornbach@morganstanley.com<br>STRATEGIST<br>Guneet Dhingra, CFA|+1 212 761-1837|
|Guneet.Dhingra@morganstanley.com<br>STRATEGIST|+1 212 761-1445|
|MORGAN STANLEY & CO. INTERNATIONAL PLC+|MORGAN STANLEY & CO. INTERNATIONAL PLC+|
|Anton Heese||
|STRATEGIST||
|Anton.Heese@morganstanley.com|+44 20 7677-6951|
|MORGAN STANLEY MUFG SECURITIES CO., LTD.+<br>Koichi Sugisaki<br>STRATEGIST|MORGAN STANLEY MUFG SECURITIES CO., LTD.+|
|Koichi.Sugisaki@morganstanleymufg.com|+81 3 6836-8428|



## **Improving iBMI** 

We also updated the momentum factor in our iBMIs. We now use weights for the momentum signal which gives a lesser weight to the most recent observation by moving from exponential weighting scheme to logarithmic weighting scheme for older observations. This allows the signal to be less dependent on the most recent observation. Additionally, we also avoid short term reversals in returns by shifting the observation used to calculate the signal by 1 week. 

## **Introducing BMI(2)** 

We introduce a new set of indicators called BMI(2) that focus on excess returns in shorter maturity sovereigns. The structure of the model closely replicates BMI(10) with some factors recalibrated to the front end, i.e. volatility adjusted carry, momentum, and the FX factor. We illustrate how the model works and report our backtest performance. 

## **Introducing xBMI** 

We introduce a new indicator for cross market calls on 10-year maturity developed market sovereigns. Previously, we used the BMI differential alone to inform cross market tactics, but now we combine the BMI(10) signal differential with an FX factor. We explain how the signal is constructed and we show backtest performance. 

Due to the nature of the fixed income market, the issuers or bonds of the issuers recommended or discussed in this report may not be continuously followed. Accordingly, investors must regard this report as providing stand-alone analysis and should not expect continuing analysis or additional reports relating to such issuers or bonds of the issuers. 

Morgan Stanley does and seeks to do business with companies covered in Morgan Stanley Research. As a result, investors should be aware that the firm may have a conflict of interest that could affect the objectivity of Morgan Stanley Research. Investors should consider Morgan Stanley Research as only a single factor in making their investment decision. 

For analyst certification and other important disclosures, refer to the Disclosure Section, located at the end of this report. 

+= Analysts employed by non-U.S. affiliates are not registered with FINRA, may not be associated persons of the member and may not be subject to NASD/NYSE restrictions on communications with a subject company, public appearances and trading securities held by a research analyst account. 

1 

## Improving BMI(10) and iBMI 

## Current signals 

MORGAN STANLEY & CO. LLC 

## **Matthew Hornbach** 

Matthew.Hornbach@morganstanley.com 

+1 212 761-1837 

Our Bond Market Indicators (BMIs) have been a staple of our rates research effort since March 2015. Given the frequency with which we publish our BMI output (weekly), the importance the output plays in our tactical calls on bond market duration, and the interest in the models expressed by investors around the world, we updated aspects of the models we felt could be improved without giving in to the devils of data mining. 

In this report, we discuss the updates made to our original BMIs and our more recent iBMIs. We will refer to the original BMIs as BMI(10) going forward in order to differentiate them from the BMI(2) models discussed in Introducing BMI(2). But first, Exhibit 1 displays the latest BMI(10) signals including the new FX/rates relationship factor, and Exhibit 2 displays the latest iBMI signals, all updated in real time as of June 15, 2017, near time of publishing. 

Across the G7 markets, our BMI(10) models are neutral on duration, while the iBMIs are bearish on euro and UK breakevens. The most supportive factor in both models is momentum toward lower yields and lower breakevens, while most other factors are mixed. Followers of our BMI models will note a new factor in our BMI(10) table: FX/Rates, which we discuss in Introducing a 5th factor: FX markets. The FX/Rates factor also features in our new xBMI models, discussed in Introducing xBMI. 

**Exhibit 1:** Morgan Stanley Bond Market Indicators - BMI(10) signals 

|**Exhibit 1:** Morgan Stanley Bond Market Indicators - BMI(10) signals|**Exhibit 1:** Morgan Stanley Bond Market Indicators - BMI(10) signals|**Exhibit 1:** Morgan Stanley Bond Market Indicators - BMI(10) signals|**Exhibit 1:** Morgan Stanley Bond Market Indicators - BMI(10) signals|**Exhibit 1:** Morgan Stanley Bond Market Indicators - BMI(10) signals|**Exhibit 1:** Morgan Stanley Bond Market Indicators - BMI(10) signals|**Exhibit 1:** Morgan Stanley Bond Market Indicators - BMI(10) signals|**Exhibit 1:** Morgan Stanley Bond Market Indicators - BMI(10) signals|
|---|---|---|---|---|---|---|---|
|**Vol Adj. Carry**<br>**Momentum**<br>**Equity Markets**<br>**Business Cycle**<br>**FX/Rates**<br>**Average**<br>**Overall**<br>**UST**<br>-3.4 (-2.7)<br>9.1 (9.5)<br>-1.2 (-2.2)<br>6.8 (6.7)<br>-4.3 (-4.3)<br>1.4 (1.4)<br>**0.0 (0.0)**<br>~~ee~~<br>ee eee eee||||||||
|**DBR**|0.5 (1.3)|2.4 (2.4)|1.5 (-1.4)|2.5 (2.1)|-4.3 (-4.2)|0.5 (0.0)|**0.0 (0.0)**|
|**UKT**|0.8 (1.3)|6.9 (8.9)|-2.2 (-3.5)|-1.9 (2.0)|1.7 (0.6)|1.1 (1.9)|**0.0 (0.0)**|
|**JGB**|-8.9 (-9.1)|5.0 (7.6)|-2.4 (-3.6)|-5.4 (-4.2)|4.1 (4.7)|-1.5 (-0.9)|**0.0 (0.0)**|
|**ACGB**|5.7 (7.0)|7.8 (7.6)|2.1 (3.8)|-4.8 (-3.4)|-4.9 (3.0)|1.2 (3.6)|**0.0 (0.0)**|
|**NZGB**|5.2 (5.3)|8.9 (9.1)|-1.5 (-2.0)|-2.3 (-6.2)|-1.8 (-5.2)|1.7 (0.2)|**0.0 (0.0)**|
|**CAN**|-5.6 (-4.0)|9.4 (9.1)|1.8 (-0.1)|-5.3 (5.4)|7.3 (-0.2)|1.5 (2.0)|**0.0 (0.0)**|



Source: Morgan Stanley Research 

Note: Positive # = long duration; Negative # = short duration, (#) = previous week Thursday close which may differ from the post-nonfarm payroll update, Indicators bounded between -10 and +10, Overall signal set to zero if abs(Signal)<=1.5 and cross-market restriction is not satisfied 

**Exhibit 2:** Morgan Stanley Inflation Bond Market Indicators - iBMI signals 

|**Exhibit 2:** Morgan Stanley Inflation Bond Market Indicators - iBMI signals|**Exhibit 2:** Morgan Stanley Inflation Bond Market Indicators - iBMI signals|**Exhibit 2:** Morgan Stanley Inflation Bond Market Indicators - iBMI signals|**Exhibit 2:** Morgan Stanley Inflation Bond Market Indicators - iBMI signals|**Exhibit 2:** Morgan Stanley Inflation Bond Market Indicators - iBMI signals|**Exhibit 2:** Morgan Stanley Inflation Bond Market Indicators - iBMI signals|**Exhibit 2:** Morgan Stanley Inflation Bond Market Indicators - iBMI signals|
|---|---|---|---|---|---|---|
|**Market**<br>**Oil**<br>**Momentum**<br>**Equities**<br>**Value**<br>**Average**<br>**Overall**<br>TIPS<br>-0.1 (-1.5)<br>-7.2 (-7.0)<br>1.1 (1.6)<br>2.7 (1.3)<br>0.0 (-1.4)<br>**0.0 (-1.4)**<br>Tr<br>~~ee~~<br>eee|||||||
|UKTi<br>0.0 (-2.0)|0.0 (-2.0)|-3.2 (-2.0)|1.7 (2.3)|-5.6 (-5.9)|-1.7 (-1.9)|**-1.7 (-1.9)**|
|HICPxT<br>-0.7 (-2.7)|-0.7 (-2.7)|-2.6 (-2.7)|-0.1 (1.1)|-6.1 (-6.5)|-2.4 (-2.7)|**-2.4 (-2.7)**|
|JGBi<br>-0.6 (-1.9)|-0.6 (-1.9)|0.7 (0.8)|1.2 (1.8)|4.0 (3.9)|1.3 (1.2)|**0.0 (0.0)**|



Source: Morgan Stanley Research 

2 

MORGAN STANLEY ASIA LIMITED MORGAN STANLEY & CO. INTERNATION PLC MORGAN STANLEY & CO. LLC 

**Jesper Rooth** Jesper.Rooth@morganstanley.com +852 3963-1519 **Federico Manicardi** Federico.Manicardi@morganstanley.com +44 20 7425-6538 **Guneet Dhingra** Guneet.Dhingra@morganstanley.com +1 212 761-1445 

## Improving Momentum for BMI(10) 

## **Why include a momentum factor at all?** 

Trend-following investment strategies are widely employed by Commodity Trading Advisors (CTAs) within equity, commodity, rates and FX markets. Furthermore, academic literature suggests momentum strategies work in government bond markets. The inclusion of a momentum strategy in our framework, on top of diversification benefits, has the advantage of taking into account unobservable factors that cannot be modeled directly. 

For example, we argued in Global Interest Rate Strategist: Trading with Stocks that the bond market momentum factor in our JGB BMI was responsible for the successful performance of the model in 2016. The momentum factor was able to capture changes in monetary policy expectations that are not explicitly modeled otherwise. The latest bond market momentum factors are shown in Exhibit 3 and Exhibit 4. 

**Exhibit 3:** BMI10 Momentum G4 **Exhibit 4:** BMI 10 Momentum ACGB, NZGB, CAN 

**==> picture [432 x 170] intentionally omitted <==**

**----- Start of picture text -----**<br>
10 10<br>8 8<br>6 6<br>4 | 4<br>aaa ip<br>2 2<br>0 0<br>AW haf<br>-2 -2<br>-4 -4<br>-6 ( -6<br>-8 -8<br>-10 -10<br>Feb-16 May-16 Aug-16 Nov-16 Feb-17 May-17 Feb-16 May-16 Aug-16 Nov-16 Feb-17 May-17<br>Bunds UST UKT JGB ACGB NZGB CAN<br>Source: Morgan Stanley Research Source: Morgan Stanley Research<br>**----- End of picture text -----**<br>


## **How do we calculate the momentum factor?** 

We calculate the bond market momentum factor using the following formula: 

where, _ERI_ is the excess return index level on week _t_ , ∆ _ERI_ is the modulus of the 4-week change in _ERI_ , and _wi_ are the weights. 

3 

The interpretation of the above formula is straightforward. We compare the one-week lagged _ERI_ level to a weighted moving average and we divide this differential by volatility, as measured by a weighted moving average of absolute changes in the excess return index. 

After calculating momentum using the formula above, we normalize the signal to the - 10 to 10 span directly rather than calculating a full-sample z-score. We avoid a fullsample z-score in order to avoid removing the effect of longer-term trends and keep a bullish bias in the factor. Indeed, had we used a z-score, yields would have had to fall by more than their historical average for our momentum signal to produce a long signal, given the yield decline in our sample. 

## **How did we revise the momentum factor calculation?** 

We changed three major, although quite technical, aspects of the calculation. We aimed to (1) reduce factor dependence on the most recent market observation (2) reduce exposure to short-term mean reversion in returns (3) make the denominator more consistent with the numerator 

**Exhibit 5:** Exponential vs. Log function 

**Exhibit 6:** Old vs. new momentum weights 

**==> picture [421 x 171] intentionally omitted <==**

**----- Start of picture text -----**<br>
9 0.4 70%<br>8 0.2 60%<br>7<br>0<br>50%<br>6<br>-0.2<br>5 40%<br>-0.4<br>4 30%<br>-0.6<br>3<br>20%<br>-0.8<br>2<br>1 -1 10%<br>0 -1.2 0%<br>0 1 2 t-1 t-5 t-9 t-13 t-19<br>Exponential Logarithmic New Old<br>Source: Morgan Stanley Research Source: Morgan Stanley Research<br>**----- End of picture text -----**<br>


To reduce factor dependence on the most recent observations, we changed the way we calculate the momentum weights. In the original calculation, we used an exponential function to derive weights. Going forward, we will use a logarithmic function (see Exhibit 5). We show a comparison of the old and new weights in Exhibit 6. The exhibit highlights a more uniform weighting of observations in the new momentum factor. 

To reduce factor exposure to short-term reversals in returns, we follow a common practice in the academic literature by shifting the set of observations used in the calculation by 1 period. Finally, to make the denominator of the fraction consistent with the numerator, we calculate the volatility using the 4 week change in the ERI, as opposed to weekly changes. 

4 

## **New momentum factor performance** 

In Exhibit 7, we report key statistics on the new momentum factor. The figures show strong and consistent performance across sovereign rates markets as measured by information and hit ratios. As for the signal distribution, we notice a moderate skew towards long positions which we think accurately reflects the global bull bond markets of the past 20 years and our choice to not standardize the series using full-period z- scores. 

**Exhibit 7:** Key statistics for new Momentum factor (1994-2017) 

|**Exhibit 7:** Key statistics for new Momentum factor (1994-2017)|**Exhibit 7:** Key statistics for new Momentum factor (1994-2017)|**Exhibit 7:** Key statistics for new Momentum factor (1994-2017)|**Exhibit 7:** Key statistics for new Momentum factor (1994-2017)|**Exhibit 7:** Key statistics for new Momentum factor (1994-2017)|**Exhibit 7:** Key statistics for new Momentum factor (1994-2017)|**Exhibit 7:** Key statistics for new Momentum factor (1994-2017)|**Exhibit 7:** Key statistics for new Momentum factor (1994-2017)|
|---|---|---|---|---|---|---|---|
|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Info Ratio**<br>0.76<br>0.50<br>0.47<br>0.67<br>0.53<br>0.51<br>0.37<br>~~ee~~<br>ee eee eee eee eee||||||||
|**Hit Ratio**|56%|54%|53%|54%|51%|53%|52%|
|**% Long**|67%|62%|64%|69%|56%|57%|64%|
|**% Short**|33%|38%|36%|31%|44%|43%|36%|



Source: Morgan Stanley Research, Bloomberg 

## Improving Momentum for iBMIs 

In keeping with the improvements in our BMIs for nominal bonds, we also updated our inflation Bond Market Indicators (iBMIs), which we introduced 6 months ago. This allows us to keep our methodologies consistent across the suite of BMIs. The methodology change that transcends from the BMI(10) improvement is the calculation of the momentum signal with newer weights. 

As highlighted in Improving BMI(10) and iBMI, we now use weights for the momentum signal which assign a lesser weight to the most recent observation by moving from exponential weighting scheme to logarithmic weighting scheme for older observations. This allows the signal to be less dependent on the most recent observation. Additionally, we also avoid short term reversals in returns by shifting the observation used to calculate the signal by 1 week. Lastly, we also use monthly changes to calculate the volatility used in the momentum formula, instead of using weekly changes earlier. 

Exhibit 8 shows the information ratio as well as hit ratios from the new iBMIs vs. our previous version of iBMIs. We found that the new iBMIs average to a higher information ratio than the previous version, suggesting that the change in the momentum formula contributed positively to the overall model performance. 

Exhibit 9 shows the returns from the new iBMIs over the last ten years of backtesting and the results are very similar to our previous iteration of the model. 

**Exhibit 8:** Information ratio and hit-ratios for G4 regions using our new iBMIs 

|**Exhibit 8:** Information ratio and hit-ratios for G4 regions using our new iBMIs|**Exhibit 8:** Information ratio and hit-ratios for G4 regions using our new iBMIs|**Exhibit 8:** Information ratio and hit-ratios for G4 regions using our new iBMIs|**Exhibit 8:** Information ratio and hit-ratios for G4 regions using our new iBMIs|**Exhibit 8:** Information ratio and hit-ratios for G4 regions using our new iBMIs|**Exhibit 8:** Information ratio and hit-ratios for G4 regions using our new iBMIs|
|---|---|---|---|---|---|
|**Strategy Metric**<br>**TIPS**<br>**UKTi**<br>**HICPxT**<br>**JGBi**<br>New Model<br>Information Ratio (Return/Volatility)<br>1.04<br>1.22<br>1.02<br>0.86<br>~~Te~~<br>ee<br>eee<br>eee||||||
|New Model|Hit Ratio|57%|59%|57%|57%|
|Old Model|Information Ratio (Return/Volatility)|0.98|1.16|1.28|0.56|
|Old Model|Hit Ratio|56%|59%|58%|54%|



Source: Bloomberg, Morgan Stanley Research 

5 

**Exhibit 9:** Yearly returns from our inflation Bond Market Indicators (iBMIs) 

**==> picture [436 x 167] intentionally omitted <==**

**----- Start of picture text -----**<br>
% %<br>28 7<br>20 5<br>12 3<br>4 1<br>-4 -1<br>2006 2007 2009 2010 2011 2012 2013 2014 2015 2016 2017<br>— TIPS = UKTi — HICPxT JGBi i Average G4 (rhs)<br>**----- End of picture text -----**<br>


Source: Bloomberg, Morgan Stanley Research 

## **Why not include an FX/Rates factor in our iBMIs?** 

Given that we have included an FX/rates relationship factor in our BMI(10), it is relevant to ask why we did not include that factor in our iBMIs, especially because inflation expectations do respond to changes in currencies as goods prices in developed economies are largely import oriented. We have three reasons why we did not include the FX factor in our iBMIs: 

**1. Indirect inclusion** - Given that we use local currency oil price changes in our oil price signal, we explicitly account for currency driven richening and cheapening in oil and thereby the currency effect on inflation. While a theoretically better effect of changes in currencies on inflation would be captured by using trade weighted currency baskets, we believe, we capture a fair amount of the impact of currency via the oil signal. 

**2. Mixed messages in currency :** A second reason we did not include currency effects is something we alluded to in our FX factor introduction. after all, rates and FX correlations are not always positive, and movements in both may be fundamentally linked to a third factor itself. For example - after the Trump victory in the US election, inflation expectations rose even as trade weighted dollar richened - all based on the fiscal policy expectation from the new president. Prior to the election, higher currencies had been negatively correlated to inflation expectations. 

**3. Ends justifying means:** Finally, even though there are shortcomings in the FX factor (like other factors), one could still make a case for including them in the iBMIs. However, in our backttests we found that while the FX factor did comparably well to other factors on a stand-alone basis, including the FX factor actually decreased the performance of the overall signal . Thus, we finally chose to exclude the FX factor from our iBMIs. 

6 

## Introducing a 5th factor: FX/rates relationships 

We originally constructed the BMIs to generate tactical outright long/short signals in G4 government bond markets. We later extended the models to government bond markets in Australia, New Zealand, and Canada. Based on the original backtests and our experience running the models live for 2 years, we continue to believe that the BMI signals provide valuable information for tactical trading in rates markets. 

Despite our success in using the BMIs for outright duration calls, the results of using the BMI signal differentials to predict cross-market performance have been mediocre. This led us to investigate possible enhancements to the cross-market signals given by our BMIs. As a result, we introduce a 5th factor in our BMI framework that both enhances cross-market BMI performance, but also improves outright performance for the ACGB, NZGB and CAN BMIs. 

## **Using the FX/rates relationship** 

Currency strategists frequently cite interest rate differentials as drivers of foreign exchange (FX) rates. The relationship between currencies and rates is also well grounded in standard monetary economic theory. Indeed, economic theory postulates that as rates in one sovereignty rise relative to those in other sovereign countries, demand for the currency of the former sovereignty increases as investors search for yield - triggering FX appreciation. 

The theory is also well reflected in empirical correlations between daily yield spread changes and daily FX returns (see Exhibit 10). We find the positive relationship even more evident when we consider slightly longer-term changes in yield spreads and FX returns, such as 3 months, as shown in Exhibit 11. The data reveals, in line with theory, that ~70% of all correlations in the sample have been positive since 1993. 

**Exhibit 10:** Distribution of rolling 3m correlations between daily changes in 10y yield spreads and FX returns (1993-2017) 

**==> picture [440 x 174] intentionally omitted <==**

**----- Start of picture text -----**<br>
Obs. Frequency a JPY | EUR | GBP | AUD | NZD | CAD<br>16%<br>14%<br>12%<br>ii 10%<br>til<br>8%<br>PEiiii<br>Obs. Freque 6%<br>PETiiLi 4%<br>Pirriirig 35%<br>2%<br>othe hea ft 0%<br>30%<br>-1.0 -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0<br>Rates/FX correlation<br>25%<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research, Bloomberg 

Note: As an example, for JPY, the yellow line depicts the historical distribution of observed 3m correlations of daily changes in 10y UST-JGB yield spread and daily USDJPY FX returns. All rates spreads and FX pairs are against the USD. Data frequency is daily. Marker denotes most recent observation. 

7 

**Exhibit 11:** Observation frequency of rolling 3m correlations between 3m changes in 10y yield spreads and FX returns (19932017) 

**==> picture [442 x 170] intentionally omitted <==**

**----- Start of picture text -----**<br>
Obs. Frequency a JPY | EUR | GBP | AUD | NZD a CAD 20%<br>12%<br>15% 10%<br>8%<br>10%<br>6%<br>5%<br>4%<br>2%<br>0%<br>0% -1<br>-1.0 -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0<br>Rates/FX correlation<br>JP<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research, Bloomberg 

Even if we acknowledge that this strong simultaneous positive relationship _per se_ says little about its predictive power on short term government bond returns, it forms the basis for the construction of our FX factor. Indeed, we are implicitly assuming that yield spreads (and not exchange rates) ultimately revert in line with the assumed linear FX/rates relationship from temporary deviations. The performance backtests suggest that there is a rates reversion towards dynamic FX/rate relationships. 

It is also worth pointing out, as the data shows, that the correlation can also be negative. Arguably, higher currency could be seen as bad for inflation and could consequently lead to lower rates due to a reduction in expected inflation. In these respects, we try to avoid these instances by imposing a sign restriction in our factor construction. 

## **How do we calculate the factor?** 

The FX/rates relationship factor in our BMIs generates long/short duration recommendations in a given rate market when the yield spread of that market to others deviates significantly from the yield spread suggested by the historical FX/rates relationship. We construct separate FX/rates relationship factors for two separate BMI blocks: (1) UST, DBR, UKT, JGB, and (2) ACGB, NZGB, and CAN. 

- For each rates market, we consider 1y rolling regressions between 3m changes in 10y yield spreads over 3m changes in the spot FX rate. We run this regression and calculate a residual against all countries in the specified BMI block. 

- For each regression, we impose a sign constraint (>0) on the beta and an R-squared threshold (>5%) to determine if the corresponding residual will be used as input in the factor calculation. 

- If a residual satisfies both conditions, we use it to calculate an average residual, which attempts to represent the deviation from the FX/rates relationship against all sovereigns in the block. On the contrary, if a residual does not satisfy both constraints, we do not include it the factor calculation. 

8 

We then calculate the z score for the average residual, which we normalize by using a cumulative distribution function (from 0 to 1) and convert on a scale from -10 to +10. Our rationale for putting a cap and a floor to the factor is simple: mitigate the impact on the overall BMI(10) of an individual factor growing ‘too strong’ (the cap/floor applies to all 5 individual factors within the model). The sign of the factor will be determined by the sign of the z score or put differently: if the average residual is below average the factor will be short while it will be long otherwise. 

Importantly, if no residual passes both the R-squared and sign requirements, we exclude the FX/rates relationship factor from BMI(10) combined signal calculation, which will be based only on the original 4 factors in that case. Our rationale behind the sign and R- squared constraints is to exclude the FX/rates relationship that display a negative and/or a particularly weak correlation from the combined and overall BMI factor calculation. 

To offer more clarity on the factor construction, we consider, in Exhibit 12, the relationship between 3m changes in 10y ACGB vs NZGB yield spreads and 3m changes in the AUD/NZD FX rate over the past 52 weeks. As shown in the exhibit, the coefficient (1.95) and the R-squared (16%) satisfy both required conditions, which means that the current residual obtained from the regression will be included in the factor construction. Assuming that the analogous regressions against CAN and UST do not satisfy the R- squared and sign constraints, we calculate the average residual for ACGB, which we then signalize, only on the basis of the above regression. 

In particular, under the these assumptions and given the magnitude and sign of the deviation of the current 3m change in yield spreads relative to the predicted change (i.e. the fitted line shown in the exhibit), the resulting FX/rates relationship factor will only be moderately bullish. 

**Exhibit 12:** AUD vs NZD FX/Rates relationship 

**==> picture [436 x 166] intentionally omitted <==**

**----- Start of picture text -----**<br>
ACGB 10y - NZGB 10y 3m changes y = 1.95x - 0.05<br>R² = 0.16<br>0.3<br>0.2<br>0.1<br>0.0<br>-0.1<br>-0.2 a .<br>-0.3<br>-0.4<br>-0.10 -0.08 -0.06 -0.04 -0.02 0.00 0.02 0.04 0.06<br>AUD/NZD 3m changes<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research, Bloomberg 

## **FX/rates relationship performance** 

Exhibit 13 shows key performance measures for our FX/rates relationship factor together with the empirical distribution of the factor sign. Overall, as stand-alone strategy, we notice that the FX/rates factor produces lackluster information and hit ratios across sovereign rates markets. 

9 

So why include it? We find the FX/rates factor improves the overall BMI(10) performance (see Exhibit 14) and, more importantly, benefits our xBMI model that we introduce later (see the Introducing xBMI section). 

Regarding the distribution of the FX/rates factor sign, we notice that it is similar across rates markets, balanced across long and short positions, and it takes a neutral sign about 10% of the time. 

**Exhibit 13:** Key statistics for the FX factor (1994-2017) 

|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Information Ratio**<br>0.12<br>0.55<br>0.09<br>0.22<br>0.46<br>-0.43<br>0.82<br>~~ee~~<br>ee eee|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Information Ratio**<br>0.12<br>0.55<br>0.09<br>0.22<br>0.46<br>-0.43<br>0.82<br>~~ee~~<br>ee eee|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Information Ratio**<br>0.12<br>0.55<br>0.09<br>0.22<br>0.46<br>-0.43<br>0.82<br>~~ee~~<br>ee eee|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Information Ratio**<br>0.12<br>0.55<br>0.09<br>0.22<br>0.46<br>-0.43<br>0.82<br>~~ee~~<br>ee eee|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Information Ratio**<br>0.12<br>0.55<br>0.09<br>0.22<br>0.46<br>-0.43<br>0.82<br>~~ee~~<br>ee eee|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Information Ratio**<br>0.12<br>0.55<br>0.09<br>0.22<br>0.46<br>-0.43<br>0.82<br>~~ee~~<br>ee eee|
|---|---|---|---|---|---|
|**Hit Ratio**|50%|50%|49%|53%<br>52%|50%<br>52%|
|**% Long**|47%|44%|53%|44%<br>44%|40%<br>44%|
|**% Short**|48%|43%|44%|41%<br>48%|48%<br>39%|
|**% Neutral**|5%|13%|3%|16%<br>8%|12%<br>17%|



Source: Morgan Stanley Research, Bloomberg 

**Exhibit 14:** Improvement attributable to the introduction of the FX Factor 

|**Info Ratio**<br>a|**Info Ratio**<br>a|**DBR**<br>-0.02<br>a|**UST**<br>0.18<br>a|**UKT**<br>-0.02<br>es|**JGB**<br>0.19|**ACGB**<br>0.23|**NZGB**<br>0.05|**CAN**<br>0.29|
|---|---|---|---|---|---|---|---|---|
||**Hit Ratio**|1%|0%|0%|2%|1%|0%|1%|
||**% Long**|-3.5%|-5.4%|-2.0%|-4.3%|-2.2%|-3.6%|-2.0%|
||**% Short**|-3.8%|-2.9%|-2.4%|-3.1%|-2.1%|-0.2%|-3.4%|
||**% Neutral**|7.3%|8.3%|4.4%|7.4%|4.3%|3.7%|5.4%|



Source: Morgan Stanley Research, Bloomberg 

## Improving ACGB, NZGB, and CAN BMIs 

## **We other changes did we make?** 

We made a few, relatively small technical changes exclusively to our ACGB, NZGB and CAN BMI(10) models. We changed the input for the volatility-adjusted carry and business cycle factors, as well as modified the cross-market restriction: 

- **Volatility-adjusted carry:** We switch from the 2y to the 3y point in the calculation of the factor (i.e., we use the 3s10s curve rather than 2s10s) for ACGB and NZGB markets. The change is motivated by performance enhancements and by more liquidity at the 3y point of the curve in the ACGB and NZGB markets. For instance, government bonds futures contracts are traded at the 3y point of the ACGB yield curve. 

- **Business cycle surprises:** We replace two local economic time series for both ACGB and NZGB markets with China PPI inflation and the official manufacturing PMI. The change is motivated by performance enhancements and by the close ties between Australia and New Zealand to China given the importance of China as an export market. 

10 

**Cross-market signal check:** Previously for the ACGB, NZGB, and CAN block, the cross-market restriction required that one other combined signal within the block, including the UST combined signal, have the same sign. Going forward, the new cross market restriction will look at all G4 BMI overall signals. This means that at least two G4 BMI combined signals must have the same sign for trading to take place in ACGB, NZGB, and CAN markets. 

## Backtest results 

After incorporating all changes, we display key performance measures and the distribution of signals for our new BMI(10) models in Exhibit 15. Across sovereign markets, our BMIs would have delivered impressive combinations of risk-reward and accuracy in the 1993-2017 YTD period, as measured respectively by the information and hit ratios. 

Furthermore, we also note the balanced distribution of trading signals, with about 50% of the weeks in the sample with a neutral position, and more positions long duration than short, which reflects partially the global bull bond market of the past 20 years. 

**Exhibit 15:** New BMI(10) performance and signal distribution (1993-2017 YTD) 

|**Exhibit 15:** New BMI(10) performance and signal distribution (1993-2017 YTD)|**Exhibit 15:** New BMI(10) performance and signal distribution (1993-2017 YTD)|**Exhibit 15:** New BMI(10) performance and signal distribution (1993-2017 YTD)|**Exhibit 15:** New BMI(10) performance and signal distribution (1993-2017 YTD)|**Exhibit 15:** New BMI(10) performance and signal distribution (1993-2017 YTD)|**Exhibit 15:** New BMI(10) performance and signal distribution (1993-2017 YTD)|**Exhibit 15:** New BMI(10) performance and signal distribution (1993-2017 YTD)|**Exhibit 15:** New BMI(10) performance and signal distribution (1993-2017 YTD)|
|---|---|---|---|---|---|---|---|
|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Info Ratio**<br>1.74<br>1.16<br>1.14<br>1.66<br>1.18<br>1.03<br>1.14<br>~~ee~~<br>eee<br>eee eee||||||||
|**Hit Ratio**|63%|57%|58%|59%|55%|57%|55%|
|**% Long**|39%|34%|37%|39%|24%|34%|33%|
|**% Short**|14%|16%|18%|13%|15%|10%|15%|
|**% Neutral**|46%|50%|45%|48%|61%|57%|52%|



Source: Morgan Stanley Research, Bloomberg. The performance data provided is a hypothetical illustration of mathematical principles, it does not predict or project the performance of an investment or investment strategy. Past performance is no guarantee of future results. 

We also explore wether the accuracy of our model is comparable across long and short positions, by showing, in Exhibit 16, some performance measures separately for long and short signals. 

By and large, we make two important observations: 

## **Long positions tend to have higher information and hit ratios than short positions:** 

which we think primarily reflects that bonds have been in a bull market over the period we have back-tested the strategies. Indeed,using a trading strategy of being long or short the market on a completely random basis over the last 30 years, one would have got a lot more long calls right than short ones. Or put differently, as performance of a passive long only strategies suggests, the unconditional probability of entering a long position is higher than the one of entering a short position. 

**The information ratios for the short positions is positive, suggesting the BMIs can generate positive returns in both bull and bear markets** : If the indicators were not successful in making short calls, then one would have to worry that the backtest results were just a reflection of the bond bull market of the past 20 years. 

11 

**Exhibit 16:** New BMI(10) performance of long vs short positions (1993-2017 YTD) 

|||**DBR**|||**UST**|||**UKT**|||**JGB**||**ACGB**|**ACGB**|**NZGB**|**NZGB**|**CAN**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**S**||**L**|**S**||**L**|**S**||**L**|**S**||**L**|**S**|**L**|**S**|**L**|**S**|**L**|
|**Info Ratio**|1.11||1.83|0.70||1.43|0.27||1.27|0.54||2.03|0.61|1.55|1.16|0.96|0.46|1.30|
|**Hit Ratio**|59%||64%|51%||60%|53%||59%|48%||63%|48%|59%|53%|57%|48%|57%|



Source: Morgan Stanley Research, Bloomberg. The performance data provided is a hypothetical illustration of mathematical principles, it does not predict or project the performance of an investment or investment strategy. Past performance is no guarantee of future results. Note: S= Short position, L= Long position 

Finally, in Exhibit 17, given the alpha-generating objective of our systematic strategies, we think it is important to compare them with passive long-only benchmark strategies on the corresponding rates market. Overall, the result suggests that our BMIs significantly outperformed long-only benchmarks in the backtest period (1993-2017 YTD), both in terms of accuracy and risk-reward. 

**Exhibit 17:** BMI10s vs long-only strategy 

|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Change in info Ratio**<br>0.91<br>0.61<br>0.60<br>0.85<br>0.83<br>0.73<br>0.48<br>~~a~~<br>esee|
|---|
|**Change in hit Ratio**<br>6%<br>3%<br>5%<br>1%<br>1%<br>5%<br>1%|



Source: Morgan Stanley Research, Bloomberg.The performance data provided is a hypothetical illustration of mathematical principles, it does not predict or project the performance of an investment or investment strategy. Past performance is no guarantee of future results. 

12 

## Introducing BMI(2) 

MORGAN STANLEY & CO. LLC 

## **Matthew Hornbach** 

Matthew.Hornbach@morganstanley.com +1 212 761-1837 

## Current signals 

We designed our BMI(10) models to guide our calls on duration near the 10-year maturity point on sovereign yield curves. But many investors do not, or cannot, invest beyond maturities shorter down the curve. In an effort to cater to investors with shorter-duration mandates, or those who trade central bank policy expectations in futures markets, we created the BMI(2) suite of models. 

The out-of-sample backtest performance of the BMI(2) models for both short-duration indexes and Libor futures encouraged us to introduce these models to the public and use them in our research. We plan on using the BMI(2) models to guide our short-end calls in the way in which we use the BMI(10) models to guide our views on duration further out the curve. We will update our BMI(2) signals each Friday with the previous day's (Thursday) closing market levels. 

Exhibit 18 displays the latest BMI(2) signals updated in real time as of June 15, 2017, near time of publishing. In contrast to BMI(10) in Exhibit 1, bond market momentum in the short end of G7 curves is less uniformly bullish. In fact, momentum in the short end of the gilt and JGB curves is quite negative on our new models. And it's this factor that has led the BMI(2) model to suggest short positions in the short-end UK and Japan curves. 

We've been bullish on 2y JGBs outright since the end of March (see Steep on Steepenin' On), and bullish 2y JGBs on asset swap since November 2016. But, respecting the bearish output from our new BMI(2) model means we turn neutral on short-end JGBs now. 

In the UK, the short reading from our BMI(2) is in line with our current suggestion to be in volatility-weighted 2s10s gilt flatteners (see Toward Smaller Balance Sheets). Given the surprise 5-3 vote from the MPC to keep rates on hold versus the previous 7-1 vote, we continue to suggest underweighting the UK front end. 

**Exhibit 18:** Morgan Stanley Bond Market Indicators - BMI(2) signals 

|**Exhibit 18:** Morgan Stanley Bond Market Indicators - BMI(2) signals|**Exhibit 18:** Morgan Stanley Bond Market Indicators - BMI(2) signals|**Exhibit 18:** Morgan Stanley Bond Market Indicators - BMI(2) signals|**Exhibit 18:** Morgan Stanley Bond Market Indicators - BMI(2) signals|**Exhibit 18:** Morgan Stanley Bond Market Indicators - BMI(2) signals|**Exhibit 18:** Morgan Stanley Bond Market Indicators - BMI(2) signals|**Exhibit 18:** Morgan Stanley Bond Market Indicators - BMI(2) signals|**Exhibit 18:** Morgan Stanley Bond Market Indicators - BMI(2) signals|
|---|---|---|---|---|---|---|---|
|**Vol Adj. Carry**<br>**Momentum**<br>**Equity Markets**<br>**Business Cycle**<br>**FX/Rates**<br>**Average**<br>**Overall**<br>**UST**<br>-1.1 (-2.5)<br>3.8 (6.2)<br>-1.7 (-2.2)<br>6.8 (6.7)<br>-1.4 (-4.4)<br>1.3 (0.8)<br>**0.0 (0.0)**<br>~~ee~~<br>eee||||||||
|**DBR**|-1.9 (-7.0)|-0.6 (-2.6)|1.7 (-1.4)|2.5 (2.1)|0.1 (0.5)|0.4 (-1.7)|**0.0 (-1.7)**|
|**UKT**|-0.1 (-1.1)|-6.6 (-6.4)|-2.0 (-3.5)|-1.9 (2.0)|-1.9 (0.1)|-2.5 (-1.8)|**-2.5 (-1.8)**|
|**JGB**|-8.9 (-8.7)|-9.9 (-8.4)|-2.4 (-3.6)|-5.4 (-4.2)|4.3 (5.3)|-4.4 (-3.9)|**-4.4 (-3.9)**|
|**ACGB**|-0.3 (-3.6)|8.3 (8.0)|2.1 (3.8)|-4.8 (-3.4)|2.7 (1.5)|1.6 (1.3)|**0.0 (0.0)**|
|**NZGB**|4.1 (4.8)|9.4 (9.5)|-1.5 (-2.0)|-2.3 (-6.2)|-2.9 (-2.0)|1.4 (0.8)|**0.0 (0.0)**|
|**CAN**|-0.5 (-7.6)|3.6 (4.0)|1.4 (-0.1)|-5.3 (5.4)|3.2 (-0.6)|0.5 (0.2)|**0.0 (0.0)**|



Source: Morgan Stanley Research 

Note: Positive # = long duration; Negative # = short duration, (#) = previous week Thursday close which may differ from the post-nonfarm payroll update, Indicators bounded between -10 and +10, Overall signal set to zero if abs(Signal)<=1.5 

13 

MORGAN STANLEY & CO. INTERNATION PLC **Federico Manicardi** Federico.Manicardi@morganstanley.com +44 20 7425-6538 MORGAN STANLEY ASIA LIMITED **Jesper Rooth** Jesper.Rooth@morganstanley.com +852 3963-1519 

## Why BMI(2)? 

Over the past 2 years, we used our Bond Market Indicators (BMIs) to aid our tactical calls on duration, targeting the 10-year sector of sovereign yield curves. During that time, we extended our framework to include inflation breakevens and euro sovereign spreads (see BMI Foundations). The backtest returns and historical hit ratios were encouraging, and we have been pleased that the indicators performed well after initial publication by outperforming passive long-only strategies. 

Given the success of these strategies, we created a new set of indicators that we call BMI(2). With this set of models, we aim to improve the quality of our short end calls as well as cater to investors with shorter duration mandates or who trade central bank policy expectations in futures markets. Benefits of extending our BMI framework to the short end include: 

The intuitive appeal of the input signals. 

- Converting multiple inputs into one coherent directional view which takes into account the main drivers of bond markets. 

- A high frequency of signal evaluation – useful for higher frequency trading strategies. 

## **Our philosophy** 

As is our practice, we will use BMI(2) to inform our tactical views. We do not suggest blindly following the output. Indeed, systematic strategies like the BMIs do not capture event risks as well as idiosyncratic market moves and turning points (like the US election results in November or the French election in April). Thus, the BMIs themselves cannot be taken as the complete set of information needed to call market direction. 

Moreover, given the nature of the short maturity bond returns, i.e., sensitive to safe haven behavior and monetary policy expectations, which are difficult to model, we feel that these concerns are more relevant for BMI(2) than for our BMI(10) models. Nevertheless, with these issues in mind, BMI(2) will feature in our calls on short-end G4 rates markets. Experience has taught us that the model outputs provide more signal than noise. 

## How does BMI(2) work? 

Our goal was to create indicators targeted to the short-end while keeping our framework intact. This explains why we constructed the BMI(2) models with the same structure as our BMI(10) models. In particular, we include the following factors in our BMI(2) models: 

14 

## **Volatility-adjusted carry** 

## **Bond market momentum** 

## **Equity market performance** 

## **Business cycle surprises** 

## **FX/rates relationship** 

We calculate the factors identically to BMI(10), with the exception of the inputs for factor construction. The rationale behind the factors is identical and is grounded in academic research. In these respects, we point readers to our BMI foundational work for further details (see BMI Foundations). As with BMI(10), all factors in the BMI(2) models are bounded between +10 and -10, with -10 representing max short/underweight and +10 representing max long/overweight. 

We use a simple average of the 5 factors to arrive at a "combined" signal. The reason for using a simple average is to avoid data mining to the extent possible. We chose not to optimize the model to generate better backtest results by overweighting factors that have worked best historically. The simple average approach also leads to encouraging results, though we believe that further optimization of the weighting scheme (especially if dynamic) is likely to lead to improvements in performance. We prefer to keep our model simple and less exposed to data mining threats. 

Finally, as with our BMI(10) models, we also use 2 'sanity checks' for the combined signal, to arrive at an 'overall signal' – i.e. the final signal that we use for our backtests. 

**1. Signal quality** – we eliminate any signal between -1.5 and +1.5 to avoid whipsaws and remove weak which result from opposing signals within a market. 

**2. Cross-market –** within the G4 markets, we look for at least 2 'combined' signals in the same direction (either long or short). Within the ACGB, NZGB, and CAN block, we require at least 2 'overall' signals among the G4 to be in the same direction. If none of these conditions is met, we ignore a long (short) 'combined' signal. 

**Exhibit 19:** Impact of signal quality check 

|**Change in Info Ratio**<br>TT|**Change in Info Ratio**<br>TT|**DBR**<br>**UST**<br>0.32<br>0.18<br>ee|**UKT**<br>0.09<br> ee|**JGB**<br>0.13<br> ee|**ACGB**<br>0.19<br> eee|**NZGB**<br>**CAN**<br>0.12<br>-0.10<br> eee|
|---|---|---|---|---|---|---|
||**Change in Hit Ratio**|2%<br>2%|1%|1%|2%|2%<br>2%|



Source: Morgan Stanley Research Bloomberg 

**Exhibit 20:** Impact of cross-market check 

||**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Change in Info Ratio**<br>0.07<br>0.16<br>0.33<br>0.10<br>0.17<br>0.10<br>-0.05<br>~~ee~~<br>ee eee eee|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Change in Info Ratio**<br>0.07<br>0.16<br>0.33<br>0.10<br>0.17<br>0.10<br>-0.05<br>~~ee~~<br>ee eee eee|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Change in Info Ratio**<br>0.07<br>0.16<br>0.33<br>0.10<br>0.17<br>0.10<br>-0.05<br>~~ee~~<br>ee eee eee|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Change in Info Ratio**<br>0.07<br>0.16<br>0.33<br>0.10<br>0.17<br>0.10<br>-0.05<br>~~ee~~<br>ee eee eee|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Change in Info Ratio**<br>0.07<br>0.16<br>0.33<br>0.10<br>0.17<br>0.10<br>-0.05<br>~~ee~~<br>ee eee eee|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Change in Info Ratio**<br>0.07<br>0.16<br>0.33<br>0.10<br>0.17<br>0.10<br>-0.05<br>~~ee~~<br>ee eee eee|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Change in Info Ratio**<br>0.07<br>0.16<br>0.33<br>0.10<br>0.17<br>0.10<br>-0.05<br>~~ee~~<br>ee eee eee|
|---|---|---|---|---|---|---|---|
||**Change in Hit Ratio**|1%|2%|3%|-1%|3%|2%<br>1%|
|Source: Morgan Stanley Research Bloomberg||||||||



15 

## **What signals did we recalibrate?** 

BMI(2) has exactly the same factors and structure of our BMI(10), so what is different? The main difference is in the inputs that we use for the calculation of the factors. Our aim is to recalibrate the BMI(10) for short end trading and, at least for now, not to develop a completely different model. Of course, we did not change the equity market performance and business cycle surprise factors because they do not depend directly on a specific sector of the yield curve. 

We recalibrated the following factors as follows: 

- **Volatility-adjusted carry:** will be based on the 3m2y slope adjusted by 2y yield volatility. 

**Bond market momentum:** will be based on the 1y-3y excess return index. 

- **FX/rates relationship:** will be based on the 2y yield 

## **Why these variables and not others?** 

In the process of developing the BMI(2), we used our BMI(10) as a natural starting point and we also tried, like we did for our BMI(10) different factor combinations and structures. By and large, our decision not to include different factors can be summarized as follows: 

- **Excluded variables had little predictive power in their own right.** This includes valuation metrics, mean reversion strategies, and many economic data releases such as GDP, industrial production, and inflation prints. It is possible that we have not found the correct way to construct variables from these data sources to turn them into useful tactical indicators. But we fear too much manipulation of the data may amount to data mining. 

- **Excluded variables were very similar to existing ones within the model.** For example, we have found changes in credit spreads, implied and realized volatility, and changes in commodity prices can be used to predict short-term bond returns. However, they are also highly correlated with variables already included in the model, and hence tend not to improve overall performance. 

- **Data limitations prevent us from using excluded variables.** For example, inflation surprises, as calculated from the difference in reported consensus expectations and realized prints, sound like a promising variable to include, given the importance of inflation to the central bank response function and the bond market. However, the available time series is short and the lag with which some figures are updated means the estimated ‘surprise’ can be a poor proxy for actual market expectations. 

In the end, we decided to keep the same structure as our BMI(10) models and simply recalibrated some of the factors to short end trading. Importantly, we do not claim we constructed the definitive BMI(2) with the variables we chose to include. Indeed, we will continue to examine potential variables for inclusion in the model and keep readers informed with future updates. 

16 

## BMI(2) performance 

In Exhibit 21 we display key performance metrics together with the distribution of signals for our BMI(2) models. Hit ratios and informations ratios are encouraging, especially for trading in such a low risk and low volatility asset class, and highlight the historical ability of our models to generate excess returns. Looking at the distribution of trading signals, we note that the BMI(2) models take positions with a similar frequency to our BMI(10) models. The BMI(2) models take a neutral position on average about 60% of the time and positions are slightly skewed to longs. 

**Exhibit 21:** Key performance metrics and statistics (1994-2017) 

|**Exhibit 21:** Key performance metrics and statistics (1994-2017)|**Exhibit 21:** Key performance metrics and statistics (1994-2017)|**Exhibit 21:** Key performance metrics and statistics (1994-2017)|**Exhibit 21:** Key performance metrics and statistics (1994-2017)|**Exhibit 21:** Key performance metrics and statistics (1994-2017)|**Exhibit 21:** Key performance metrics and statistics (1994-2017)|
|---|---|---|---|---|---|
|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>**Info Ratio**<br>1.42<br>1.25<br>0.61<br>0.92<br>0.82<br>0.75<br>0.53<br>~~rr~~<br>ee<br>eee eee||||||
|**Hit Ratio**|59%|58%|57%<br>56%|57%|55%<br>56%|
|**% Long**|26%|28%|23%<br>31%|10%|24%<br>19%|
|**% Short**|13%|15%|20%<br>11%|17%|11%<br>15%|
|**% Neutral**|61%|57%|57%<br>58%|73%|65%<br>65%|



Source: Morgan Stanley Research, Bloomberg 

While the excess return averages and standard deviations are informative, we think annual excess returns provides another interesting perspective (see Exhibit 22 and Exhibit 23) as well as the excess return indices (see Exhibit 24 and Exhibit 25). Overall, annual returns shows that: 

- Both the G4 and ACGB, NZGB and CAN blocks rarely earned negative returns on aggregate and the distribution of annual excess returns has a clear positive skew. 

- The strategies excluding the high returns earned in 2001, 2002 and 2008, display moderate volatility and a high degree of consistency. 

DBR is the top performing strategy. 

We arrive at similar conclusions by looking at the excess return indices. They also highlight the few number of moderate drawdowns that the indicators experienced since 2000. While we don't expect our indicators to easily replicate the performance achieve in 2008, we think that the similarity between BMI(2) and BMI(10) and the minimum adjustments made to recalibrate our models corroborate the success and robustness of our framework. 

Importantly, we note that, in the past 5 years, the frequency of signals and the absolute performance of our strategies has diminished. We think the low level and volatility of short term interest rates across G4 and ACGB, NZGB, and CAN markets is to blame. 

17 

**Exhibit 22:** Annual excess returns for the G4 markets 

**==> picture [198 x 169] intentionally omitted <==**

**----- Start of picture text -----**<br>
50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>thle<br>-10%<br>Jan-00 Jan-03 Jan-06 Jan-09 Jan-12 Jan-15<br>DBR UST UKT JGB<br>Source: Morgan Stanley Research, Bloomberg<br>**----- End of picture text -----**<br>


**Exhibit 23:** Annual excess returns for ACGB, NZGB and CAN markets 

**==> picture [198 x 170] intentionally omitted <==**

**----- Start of picture text -----**<br>
25%<br>20%<br>15%<br>10%<br>5%<br>0%<br>-5% A alll,<br>-10%<br>Jan-00 Jan-03 Jan-06 Jan-09 Jan-12 Jan-15<br>ACGB NZGB CAN<br>Source: Morgan Stanley Research, Bloomberg<br>**----- End of picture text -----**<br>


**Exhibit 24:** Excess return indexes for G4 markets 

**==> picture [198 x 169] intentionally omitted <==**

**----- Start of picture text -----**<br>
160<br>150<br>140<br>130<br>120<br>110<br>100<br>90<br>Feb-00 Feb-03 Feb-06 Feb-09 Feb-12 Feb-15<br>DBR UST UKT JGB<br>Source: Morgan Stanley Research, Bloomberg<br>**----- End of picture text -----**<br>


**Exhibit 25:** Excess return indexes for ACGB, NZGB, and CAN markets 

**==> picture [189 x 170] intentionally omitted <==**

**----- Start of picture text -----**<br>
160<br>150<br>140<br>130<br>120<br>110<br>100<br>90<br>Feb-00 Feb-03 Feb-06 Feb-09 Feb-12 Feb-15<br>ACGB NZGB CAN<br>Source: Morgan Stanley Research, Bloomberg<br>**----- End of picture text -----**<br>


## **BMI(2) vs. short term interest rates futures** 

Monetary policy and, more generally, short term interest rate expectations are an important, if not the most important, drivers of short end sovereign yields. Therefore, given the common driver behind short term yields and short term interest rates, we ran an additional out-of-sample backtest of our BMI(2) models on short term Libor futures. 

In particular, we use our BMI(2) overall signal to take long/short positions on the 6th 3m Libor future contract in the G4 and ACGB, NZGB and CAN blocks. We display the results in Exhibit 26, where the performance denoted under "F" is the futures performance and the performance denoted under "C" is the index performance, or cash performance. Given the BMI(2) has been calibrated against the BBG/EFFA indices, we are pleased with its past ability to predict excess returns in Libor futures, as suggested by the historical hit ratios and information ratios. 

18 

**Exhibit 26:** BMI(2) trading on 6th 3m Libor contract vs bond indices 

|||**DBR**|||**UST**|||**UKT**|||**JGB**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**F**||**C**|**F**||**C**|**F**||**C**|**F**||**C**|
|**Sharpe**|1.47||1.50|1.26||1.25|0.46||0.61|1.27||0.92|
|**Hit**|59%||57%|60%||58%|57%||57%|57%||56%|
|||**AUD**|||**NZD**|||**CAN**|||||
||**F**||**C**|**F**||**C**|**F**||**C**||||
|**Sharpe**|0.59||0.82|1.01||0.89|0.78||0.53||||
|**Hit**|57%||57%|61%||56%|56%||56%||||



Source: Morgan Stanley Research, Bloomberg Note: due to unavailable data for NZD and DBR, the sample we are using starts in 1994 and 1998 respectively. F and C columns, refers to backtest being performed on futures and bond indices respectively 

## **BMI(2) versus passive strategies** 

As the aim of our indicators is to outperform passive strategies, in Exhibit 27 , we compare 2 performance metrics of our BMIs against the corresponding long-only benchmark strategies. By and large, results are impressive and show a significant improvement in both hit and information ratios. The only exception is the JGB BMI(2) with a hit ratio about 3% lower than the benchmark strategy. 

**Exhibit 27:** BMI(2) vs. long-only strategies (1994-2017) 

|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>~~|~~|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>~~|~~|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>~~|~~|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>~~|~~|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>~~|~~|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>~~|~~|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>~~|~~|**DBR**<br>**UST**<br>**UKT**<br>**JGB**<br>**ACGB**<br>**NZGB**<br>**CAN**<br>~~|~~|
|---|---|---|---|---|---|---|---|
|**Change in info Ratio**|0.39|0.46|0.07|0.24|0.57|0.69|-0.09|
|**Change in hit Ratio**|1%|3%|4%|-3%|3%|7%|3%|



Source: Morgan Stanley Research, Bloomberg 

19 

## Introducing xBMI 

MORGAN STANLEY & CO. LLC 

## **Matthew Hornbach** 

Matthew.Hornbach@morganstanley.com 

+1 212 761-1837 

## Current signals 

We originally constructed our Bond Market Indicators (BMIs) with the goal of improving the quality of our short term tactical duration calls in 10-year nominal sovereign bonds. Given the global set of indicators we constructed, which sometimes offered opposing views of duration, we wondered if those opposing views could produce profitable trading signals themselves for cross market yields spreads. The mediocre results from that exercise led us to develop a related cross-market BMI, or xBMI. 

Exhibit 28 displays the output from the xBMI model, updated in real time as of June 15, 2017, near time of publishing. We will update our xBMI signals each Friday with the previous day's (Thursday) closing market levels. Before we explain how we built the xBMI, we should explain the current readings and how investors should interpret these numbers for trading opportunities. One of the xBMIs with a non-zero reading is ACGB/CAN. The -4.0 reading out of a possible -10.0 to +10.0 scale means investors should consider selling 10y ACGBs vs. buying 10y CAN. 

Exhibit 28 displays 4 rows for each cross-market pair. The "FX/Rates" row displays the FX/rates relationship signal, discussed in The FX/rates relationship factor. The "BMI differential" row displays the difference between the relevant BMI(10) signals after having applied the signal strength check, i.e., abs(signal) >= 1.5. The "Average xBMI combined" row displays the average of the "FX/Rates" and "BMI differential" rows. And the "Overall" row display the final output of the model, which requires that the sign of the "Average xBMI combined" signal match the sign of the "BMI differential" signal and be >=2. 

**Exhibit 28:** Morgan Stanley Cross-Market Bond Market Indicators (xBMIs) 

|**Overall**<br>rr|**Overall**<br>rr|**DBR/UKT**<br>**0.0 (0.0)**<br>ee|**DBR/JGB**<br>**0.0 (0.0)**<br>eee|**DBR/UST**<br>**0.0 (0.0)**<br>eee|**UKT/JGB**<br>**0.0 (0.0)**<br> eee|**UKT/UST**<br>**JGB/UST**<br>**0.0 (3.9)**<br>**0.0 (0.0)**<br> eee|
|---|---|---|---|---|---|---|
||**Average xBMI**|-1.4 (-1.4)|-0.9 (-2.0)|-1.1 (-1.4)|-0.6 (-1.0)|2.8 (3.9)<br>1.7 (2.5)|
||**Combined BMI differential**|0.0 (-1.9)|1.5 (0.0)|0.0 (0.0)|1.5 (1.9)|0.0 (1.9)<br>-1.5 (0.0)|
||**FX/Rates**|-2.7 (-1.0)|-3.4 (-4.1)|-2.3 (-2.8)|-2.7 (-3.9)|5.6 (6.0)<br>5.0 (5.0)|
|**ACGB/NZGB**<br>**ACGB/CAN**<br>**ACGB/UST**<br>**NZGB/CAN**<br>**NZGB/UST**<br>**CAN/UST**<br>**Overall**<br>**0.0 (4.4)**<br>**-4.0 (0.0)**<br>**0.0 (2.2)**<br>**0.0 (0.0)**<br>**0.0 (0.0)**<br>**3.5 (0.0)**<br>~~ee~~<br>~~eee~~|||||||
||**Average xBMI**|1.2 (4.4)|-4.0 (0.8)|-1.0 (2.2)|-4.0 (-1.6)|-0.7 (-0.7)<br>3.5 (1.8)|
||**Combined BMI differential**|-1.7 (3.6)|-1.5 (1.5)|0.0 (3.6)|0.2 (-2.0)|1.7 (0.0)<br>1.5 (2.0)|
||**FX/Rates**|4.1 (5.3)|-6.4 (0.2)|-1.9 (0.7)|-8.2 (-1.1)|-3.1 (-1.3)<br>5.4 (1.6)|



Source: Morgan Stanley Research Note: Positive # = long cross market spreads; Negative # = short cross market spread, (#) = previous week Thursday close which may differ from the post-nonfarm payroll update, Indicators bounded between -10 and +10, Signal is calculated as the average of Combined BMI differential and the FX component. Signal is set to zero if abs(Signal)<=2 and/or its has a sign different from the Combined BMI differential. 

20 

MORGAN STANLEY & CO. INTERNATION PLC 

MORGAN STANLEY & CO. INTERNATIONAL PLC 

**Jesper Rooth** Jesper.Rooth@morganstanley.com +852 3963-1519 **Federico Manicardi** Federico.Manicardi@morganstanley.com +44 20 7425-6538 

## What is the xBMI? 

Given the success of our BMI models with outright long/short calls, we saw crossmarket yield spread indicators as a natural addition to our portfolio of strategies. In particular, we sought to build cross-market indicators that are integrated with our existing strategies in order to leave the key benefits our framework unaltered: 

The intuitive appeal of the input signals. 

- Converting multiple inputs into one coherent duration view which takes into account the main driver of bond markets. 

A high frequency of signal evaluation – useful for tactical trading strategies. 

In these respects, our first attempt was to construct a a series of systematic crossmarket strategies simply based on the combined BMI(10) signal differentials. We show performance backtests of this simple framework in Exhibit 29. While the results for all spread models were positive, the relatively modest performance ratios suggested room for improvement. 

**Exhibit 29:** Performance backtest of BMI combined signal differential strategy 

|**Exhibit 29:** Performance backtest of BMI combined signal differential strategy|**Exhibit 29:** Performance backtest of BMI combined signal differential strategy|**Exhibit 29:** Performance backtest of BMI combined signal differential strategy|**Exhibit 29:** Performance backtest of BMI combined signal differential strategy|**Exhibit 29:** Performance backtest of BMI combined signal differential strategy|**Exhibit 29:** Performance backtest of BMI combined signal differential strategy|**Exhibit 29:** Performance backtest of BMI combined signal differential strategy|
|---|---|---|---|---|---|---|
|**DBR/UKT**<br>**DBR/JGB**<br>**DBR/UST**<br>**UKT/JGB**<br>**UKT/UST**<br>**JGB/UST**<br>**Sum**<br>**Info ratio**<br>0.12<br>0.41<br>0.75<br>0.32<br>0.64<br>0.71<br>0.77<br>~~eee~~<br>eee|||||||
|**Hit ratio**|51%|52%|52%|51%|56%|53%<br>54%|
|**Non-Zero**|83%|85%|85%|86%|84%|90%<br>97%|
|**ACGB/NZGB**<br>**ACGB/CAN**<br>**ACGB/UST**<br>**NZGB/CAN**<br>**NZGB/UST**<br>**CAN/UST**<br>**Sum**<br>**Info ratio**<br>0.23<br>0.74<br>0.94<br>0.41<br>0.49<br>0.53<br>0.92<br>a a<br>a<br>~~ee~~<br>ee ee|||||||
|**Hit ratio**|52%|56%|56%|52%|54%|51%<br>57%|
|**Non-Zero**|85%|87%|86%|87%|85%|86%<br>96%|



Source: Morgan Stanley Research 

Our efforts culminated in the development of a new set of models, which we call the xBMIs, for cross-market tactical trading. The xBMIs effectively extend the breath of our systematic framework to include cross-market calls across nominal rates markets. In Exhibit 30 and Exhibit 31, we show the recent history for these indicators. 

## **Our philosophy** 

We will apply the xBMI output in a similar fashion to our current approach with the BMI(10) models. The signals will be an important input to our cross-market calls, but will not determine our trade recommendations at all times. Indeed, like all our BMIs, xBMIs are not able to capture event risks as well as idiosyncratic market moves and turning points and, as such, we will continue to overlay the quantitative output with qualitative judgement. 

21 

**Exhibit 30:** G4 xBMI signal history 

**Exhibit 31:** ACGB, NZGB, and CAN xBMI signal history 

**==> picture [433 x 170] intentionally omitted <==**

**----- Start of picture text -----**<br>
10 10<br>8 8<br>6 6<br>4 | iY V \ s<br>4<br>2<br>AVA NAY 2 yf<br>0 PAW Waa ni)<br>IY VV PY UAT WAV \<br>0<br>-2 OA ANTWAT ee||ee 0<br>-4 Nam WV -2 TV UL<br>-6-8 WN Vg An Pa| Ni ',.A d -4-6 IAWLeadNANAVi,WAAL,vi a /V<br>-10 -8<br>Feb-16 May-16 Aug-16 Nov-16 Feb-17 May-17 Feb-16 May-16 Aug-16 Nov-16 Feb-17 May-17<br>Bunds/UKTs Bunds/JGBs Bunds/UST ACGB/NZGB ACGB/CAN ACGB/UST<br>UKTs/JGBs UKTs/UST JGBs/UST NZGB/CAN NZGB/UST CAN/UST<br>Source: Morgan Stanley Research Source: Morgan Stanley Research<br>**----- End of picture text -----**<br>


## How do we calculate the xBMI signal? 

The FX/rates relationship, which is described in Introducing a 5th factor: FX/rates relationships, is assigned a disproportionately large weight in the xBMI, given its specific usefulness guiding cross-market calls. Our inclusion of the FX/rates relationship within the BMI(10) framework, i.e. as a 5th factor alongside the original 4 factors, primarily stems from its cross-market features. 

The two key inputs in our xBMIs are the BMI(10) 'combined' signals for each market, i.e., the average of the 5 BMI(10) factors (including only the signal magnitude check, but not the cross-market check) as well as the previously described FX/rates relationship factor. 

Specifically, we use an average of the BMI(10) cross-market signal differential with the additional, FX/rates relationship factor. We apply two sanity checks to arrive at an 'overall xBMI signal', i.e., the final signal that we use for our backtests: 

- **Sign check** : we require the xBMI 'combined' signal differential and the simple BMI(10) 'combined' signal differential to have the same sign. We do this because we want to limit contradictions between the BMI(10) models and the xBMIs. We limit situations where the xBMI would suggest going short Bunds vs. gilts, while the BMI(10) would suggest going long Bunds vs. gilts. 

- **Quality check:** we require the xBMI 'combined' signal differential to be greater than 2. 

If both checks are satisfied, we calculate the xBMI as the average of xBMI 'combined' signal differential and the FX/rates relationship factor. If not, we restrict our model from trading by making the signal neutral. 

22 

## The FX/rates relationship factor 

We calculate the FX/rates relationship factor, against which we equally weight the BMI(10) 'combined' signal differential, by using the same procedure as the FX/rates relationship factor in the BMI(10). Hence, for a detailed discussion on the factor construction and rationale, please see Introducing a 5th factor: FX/rates relationships. 

The only difference between the FX/rates relationship factor in the BMI(10) and the xBMI is that, in the BMI(10), we use the average residual against all sovereign bonds in the same block, but for the xBMI we use only the residual from the sovereign pair that the model is trading. 

We end up overweighting the FX/rates relationship factor for the xBMI because it improves the performance of our strategy. Indeed, as shown in Exhibit 32, both the accuracy and the risk-reward of our strategies, increase significantly with the introduction of the FX/rates relationship factor. 

**Exhibit 32:** Performance improvement attributable to FX/rates relationship factor 

|**DBR/UKT**<br>**DBR/JGB**<br>**DBR/UST**<br>**UKT/JGB**<br>**UKT/UST**<br>**JGB/UST**<br>**Sum**<br>**Info ratio**<br>0.35<br>0.16<br>0.63<br>-0.11<br>0.21<br>0.38<br>0.12<br>~~ee~~<br>eee eee|
|---|
|**Hit ratio**<br>0.00<br>-0.01<br>0.05<br>0.00<br>0.01<br>0.01<br>0.01|
|**ACGB/NZGB**<br>**ACGB/CAN**<br>**ACGB/UST**<br>**NZGB/CAN**<br>**NZGB/UST**<br>**CAN/UST**<br>**Sum**<br>**Info ratio**<br>0.37<br>0.32<br>0.55<br>0.63<br>0.91<br>0.71<br>0.47<br>~~ee~~<br>eee eee|
|**Hit ratio**<br>0.01<br>0.02<br>0.06<br>0.05<br>0.04<br>0.06<br>0.02|



Source: Morgan Stanley Research, Bloomberg Note: Include also the quality check 

## xBMI performance 

Finally, in Exhibit 33, we look at xBMI performance across the different combination of countries and note that: 

In the G4 block, hit ratios and information ratios are sizeable except for the DBR/UKT and UKT/JGB pairs. 

All combinations in the ACGB, NZGB, and CAN and UST block has impressive information and hit ratios. 

**Exhibit 33:** Performance summary 

|**Exhibit 33:** Performance summary|**Exhibit 33:** Performance summary|**Exhibit 33:** Performance summary|**Exhibit 33:** Performance summary|**Exhibit 33:** Performance summary|**Exhibit 33:** Performance summary|**Exhibit 33:** Performance summary|
|---|---|---|---|---|---|---|
|**DBR/UKT**<br>**DBR/JGB**<br>**DBR/UST**<br>**UKT/JGB**<br>**UKT/UST**<br>**JGB/UST**<br>**Sum**<br>**Info ratio**<br>0.49<br>0.70<br>1.39<br>0.21<br>0.83<br>1.10<br>0.92<br>Tr<br>~~eee~~<br>eee|||||||
|**Hit ratio**<br>52%|53%|57%|51%|56%|54%|56%|
|**Non-Zero**<br>35%|39%|43%|49%|39%|54%|87%|
|**ACGB/NZGB**<br>**ACGB/CAN**<br>**ACGB/UST**<br>**NZGB/CAN**<br>**NZGB/UST**<br>**CAN/UST**<br>**Sum**<br>**Info ratio**<br>0.63<br>1.04<br>1.48<br>1.05<br>1.41<br>1.24<br>1.39<br>a a<br>ee<br>ee<br>~~ee~~<br>ee|||||||
|**Hit ratio**<br>53%|58%|62%|57%|59%|58%|58%|
|**Non-Zero**<br>40%|46%|38%|41%|33%|26%|85%|



Source: Morgan Stanley Research, Bloomberg 

23 

In Exhibit 34, we show the distribution of xBMI trading signals. By and large, we notice that the model trades about 40% of the time with a balanced composition of long and short signals. 

**Exhibit 34:** Distribution of trading signals 

|**Exhibit 34:** Distribution of trading signals|**Exhibit 34:** Distribution of trading signals|**Exhibit 34:** Distribution of trading signals|**Exhibit 34:** Distribution of trading signals|**Exhibit 34:** Distribution of trading signals|**Exhibit 34:** Distribution of trading signals|**Exhibit 34:** Distribution of trading signals|
|---|---|---|---|---|---|---|
|**DBR/UKT**<br>**DBR/JGB**<br>**DBR/UST**<br>**UKT/JGB**<br>**UKT/UST**<br>**JGB/UST**<br>**% Long**<br>14%<br>17%<br>16%<br>22%<br>17%<br>25%<br>~~ee~~<br>eee<br>eee eee|||||||
|**% Short**|19%|22%|24%|26%|18%|25%|
|**% Neutral**|67%|62%|60%|52%|65%|50%|
|**ACGB/NZGB**<br>**ACGB/CAN**<br>**ACGB/UST**<br>**NZGB/CAN**<br>**NZGB/UST**<br>**CAN/UST**<br>**% Long**<br>14%<br>18%<br>13%<br>20%<br>16%<br>13%<br>~~Tr~~<br>ee<br>eee eee eee|||||||
|**% Short**|28%|35%|30%|21%|14%|13%|
|**% Neutral**|58%|47%|57%|59%|69%|73%|



Source: Morgan Stanley Research, Bloomberg 

24 

## BMI Signals 

**Exhibit 35:** Morgan Stanley Bond Market Indicators - BMI(10) 

|**UST**<br>a|**UST**<br>a|**Vol Adj. Carry**<br>-3.4 (-2.7)<br> a|**Momentum**<br>9.1 (9.5)<br>a|**Equity Markets**<br>-1.2 (-2.2)<br>ee|**Business Cycle**<br>6.8 (6.7)<br> ee|**FX/Rates**<br>-4.3 (-4.3)<br>ee|**Average**<br>1.4 (1.4)|**Overall**<br>**0.0 (0.0)**|
|---|---|---|---|---|---|---|---|---|
||**DBR**|0.5 (1.3)|2.4 (2.4)|1.5 (-1.4)|2.5 (2.1)|-4.3 (-4.2)|0.5 (0.0)|**0.0 (0.0)**|
||**UKT**|0.8 (1.3)|6.9 (8.9)|-2.2 (-3.5)|-1.9 (2.0)|1.7 (0.6)|1.1 (1.9)|**0.0 (0.0)**|
||**JGB**|-8.9 (-9.1)|5.0 (7.6)|-2.4 (-3.6)|-5.4 (-4.2)|4.1 (4.7)|-1.5 (-0.9)|**0.0 (0.0)**|
||**ACGB**|5.7 (7.0)|7.8 (7.6)|2.1 (3.8)|-4.8 (-3.4)|-4.9 (3.0)|1.2 (3.6)|**0.0 (0.0)**|
||**NZGB**|5.2 (5.3)|8.9 (9.1)|-1.5 (-2.0)|-2.3 (-6.2)|-1.8 (-5.2)|1.7 (0.2)|**0.0 (0.0)**|
||**CAN**|-5.6 (-4.0)|9.4 (9.1)|1.8 (-0.1)|-5.3 (5.4)|7.3 (-0.2)|1.5 (2.0)|**0.0 (0.0)**|



Source: Morgan Stanley Research 

Note: Positive # = long duration; Negative # = short duration, (#) = previous week Thursday close which may differ from the post-nonfarm payroll update, Indicators bounded between -10 and +10, Overall signal set to zero if abs(Signal)<=1.5 and cross-market restriction is not satisfied 

**Exhibit 36:** Morgan Stanley Bond Market Indicators - BMI(2) 

|**Vol Adj. Carry**<br>**Momentum Equity Markets Business Cycle**<br>**FX/Rates**<br>**Average**<br>**Overall**<br>**UST**<br>-1.1 (-2.5)<br>3.8 (6.2)<br>-1.7 (-2.2)<br>6.8 (6.7)<br>-1.4 (-4.4)<br>1.3 (0.8)<br>**0.0 (0.0)**<br>~~ee~~<br>ee ee<br>eee eee|**Vol Adj. Carry**<br>**Momentum Equity Markets Business Cycle**<br>**FX/Rates**<br>**Average**<br>**Overall**<br>**UST**<br>-1.1 (-2.5)<br>3.8 (6.2)<br>-1.7 (-2.2)<br>6.8 (6.7)<br>-1.4 (-4.4)<br>1.3 (0.8)<br>**0.0 (0.0)**<br>~~ee~~<br>ee ee<br>eee eee|**Vol Adj. Carry**<br>**Momentum Equity Markets Business Cycle**<br>**FX/Rates**<br>**Average**<br>**Overall**<br>**UST**<br>-1.1 (-2.5)<br>3.8 (6.2)<br>-1.7 (-2.2)<br>6.8 (6.7)<br>-1.4 (-4.4)<br>1.3 (0.8)<br>**0.0 (0.0)**<br>~~ee~~<br>ee ee<br>eee eee|**Vol Adj. Carry**<br>**Momentum Equity Markets Business Cycle**<br>**FX/Rates**<br>**Average**<br>**Overall**<br>**UST**<br>-1.1 (-2.5)<br>3.8 (6.2)<br>-1.7 (-2.2)<br>6.8 (6.7)<br>-1.4 (-4.4)<br>1.3 (0.8)<br>**0.0 (0.0)**<br>~~ee~~<br>ee ee<br>eee eee|**Vol Adj. Carry**<br>**Momentum Equity Markets Business Cycle**<br>**FX/Rates**<br>**Average**<br>**Overall**<br>**UST**<br>-1.1 (-2.5)<br>3.8 (6.2)<br>-1.7 (-2.2)<br>6.8 (6.7)<br>-1.4 (-4.4)<br>1.3 (0.8)<br>**0.0 (0.0)**<br>~~ee~~<br>ee ee<br>eee eee|**Vol Adj. Carry**<br>**Momentum Equity Markets Business Cycle**<br>**FX/Rates**<br>**Average**<br>**Overall**<br>**UST**<br>-1.1 (-2.5)<br>3.8 (6.2)<br>-1.7 (-2.2)<br>6.8 (6.7)<br>-1.4 (-4.4)<br>1.3 (0.8)<br>**0.0 (0.0)**<br>~~ee~~<br>ee ee<br>eee eee|**Vol Adj. Carry**<br>**Momentum Equity Markets Business Cycle**<br>**FX/Rates**<br>**Average**<br>**Overall**<br>**UST**<br>-1.1 (-2.5)<br>3.8 (6.2)<br>-1.7 (-2.2)<br>6.8 (6.7)<br>-1.4 (-4.4)<br>1.3 (0.8)<br>**0.0 (0.0)**<br>~~ee~~<br>ee ee<br>eee eee|**Vol Adj. Carry**<br>**Momentum Equity Markets Business Cycle**<br>**FX/Rates**<br>**Average**<br>**Overall**<br>**UST**<br>-1.1 (-2.5)<br>3.8 (6.2)<br>-1.7 (-2.2)<br>6.8 (6.7)<br>-1.4 (-4.4)<br>1.3 (0.8)<br>**0.0 (0.0)**<br>~~ee~~<br>ee ee<br>eee eee|
|---|---|---|---|---|---|---|---|
|**DBR**|-1.9 (-7.0)|-0.6 (-2.6)|1.7 (-1.4)|2.5 (2.1)|0.1 (0.5)|0.4 (-1.7)|**0.0 (-1.7)**|
|**UKT**|-0.1 (-1.1)|-6.6 (-6.4)|-2.0 (-3.5)|-1.9 (2.0)|-1.9 (0.1)|-2.5 (-1.8)|**-2.5 (-1.8)**|
|**JGB**|-8.9 (-8.7)|-9.9 (-8.4)|-2.4 (-3.6)|-5.4 (-4.2)|4.3 (5.3)|-4.4 (-3.9)|**-4.4 (-3.9)**|
|**ACGB**|-0.3 (-3.6)|8.3 (8.0)|2.1 (3.8)|-4.8 (-3.4)|2.7 (1.5)|1.6 (1.3)|**0.0 (0.0)**|
|**NZGB**|4.1 (4.8)|9.4 (9.5)|-1.5 (-2.0)|-2.3 (-6.2)|-2.9 (-2.0)|1.4 (0.8)|**0.0 (0.0)**|
|**CAN**|-0.5 (-7.6)|3.6 (4.0)|1.4 (-0.1)|-5.3 (5.4)|3.2 (-0.6)|0.5 (0.2)|**0.0 (0.0)**|



Source: Morgan Stanley Research 

Note: Positive # = long duration; Negative # = short duration, (#) = previous week Thursday close which may differ from the post-nonfarm payroll update, Indicators bounded between -10 and +10, Overall signal set to zero if abs(Signal)<=1.5 and cross-market restriction is not satisfied 

**Exhibit 37:** Morgan Stanley Bond Market Indicators - xBMIs 

|**Overall**<br>rr|**Overall**<br>rr|**DBR/UKT**<br>**0.0 (0.0)**<br>ee|**DBR/JGB**<br>**0.0 (0.0)**<br> eee|**DBR/UST**<br>**0.0 (0.0)**<br> eee|**UKT/JGB**<br>**0.0 (0.0)**<br>eee|**UKT/UST**<br>**JGB/UST**<br>**0.0 (3.9)**<br>**0.0 (0.0)**<br> eee|**UKT/UST**<br>**JGB/UST**<br>**0.0 (3.9)**<br>**0.0 (0.0)**<br> eee|
|---|---|---|---|---|---|---|---|
||**Average xBMI**|-1.4 (-1.4)|-0.9 (-2.0)|-1.1 (-1.4)|-0.6 (-1.0)|2.8 (3.9)|1.7 (2.5)|
||**Combined BMI differential**|0.0 (-1.9)|1.5 (0.0)|0.0 (0.0)|1.5 (1.9)|0.0 (1.9)|-1.5 (0.0)|
||**FX/Rates**|-2.7 (-1.0)|-3.4 (-4.1)|-2.3 (-2.8)|-2.7 (-3.9)|5.6 (6.0)|5.0 (5.0)|
|**Overall**<br>rr||**ACGB/NZGB**<br>**0.0 (4.4)**<br>ee|**ACGB/CAN**<br>**-4.0 (0.0)**<br>eee|**ACGB/UST**<br>**0.0 (2.2)**<br>eee|**NZGB/CAN**<br>**0.0 (0.0)**<br> eee|**NZGB/UST**<br>**CAN/UST**<br>**0.0 (0.0)**<br>**3.5 (0.0)**<br> eee||
||**Average xBMI**|1.2 (4.4)|-4.0 (0.8)|-1.0 (2.2)|-4.0 (-1.6)|-0.7 (-0.7)|3.5 (1.8)|
||**Combined BMI differential**|-1.7 (3.6)|-1.5 (1.5)|0.0 (3.6)|0.2 (-2.0)|1.7 (0.0)|1.5 (2.0)|
||**FX/Rates**|4.1 (5.3)|-6.4 (0.2)|-1.9 (0.7)|-8.2 (-1.1)|-3.1 (-1.3)|5.4 (1.6)|



Source: Morgan Stanley Research 

Note: Positive # = long cross market spreads; Negative # = short cross market spread, (#) = previous week Thursday close which may differ from the post-nonfarm payroll update, Indicators bounded between -10 and +10, Signal is calculated as the average of Combined BMI differential and the FX component. Signal is set to zero if abs(Signal)<=2 and/or its has a sign different from the Combined BMI differential 

25 

**Exhibit 38:** Morgan Stanley Euro Sovereign Bond Market Indicators - eBMI 

|**Periphery vs. Core**<br>a|**Periphery vs. Core**<br>a|**Business Cycle Surprises**<br>a|**Business Cycle Surprises**<br>1.1 (2.4)|**Momentum**<br>-6.4 (-2.7)<br>ee|**Vol. Adj. Carry**<br>7.4 (9.2)|**Supply**<br>5.3 (-6.5)|**Risky Assets**<br>6.7 (4.5)|**Overall**<br>**2.8 (1.4)**|
|---|---|---|---|---|---|---|---|---|
||**Semi-Core vs. Core**||0.7 (0.5)|-9.0 (-8.3)|-6.5 (-5.8)|-6.2 (-3.0)|-0.1 (-5.7)|**-4.2 (-4.5)**|
||**Periphery vs. Semi-Core**||0.2 (0.9)|1.3 (2.8)|7.0 (7.5)|5.8 (-1.7)|3.4 (5.1)|**7.1 (5.8)**|



Source: Morgan Stanley Research 

**Exhibit 39:** Morgan Stanley Inflation Bond Market Indicators - iBMI 

|**Exhibit 39:** Morgan Stanley Inflation Bond Market Indicators - iBMI|**Exhibit 39:** Morgan Stanley Inflation Bond Market Indicators - iBMI|**Exhibit 39:** Morgan Stanley Inflation Bond Market Indicators - iBMI|**Exhibit 39:** Morgan Stanley Inflation Bond Market Indicators - iBMI|**Exhibit 39:** Morgan Stanley Inflation Bond Market Indicators - iBMI|**Exhibit 39:** Morgan Stanley Inflation Bond Market Indicators - iBMI|**Exhibit 39:** Morgan Stanley Inflation Bond Market Indicators - iBMI|
|---|---|---|---|---|---|---|
|**Market**<br>**Oil**<br>**Momentum**<br>**Equities**<br>**Value**<br>**Average**<br>**Overall**<br>**TIPS**<br>-0.1 (-1.5)<br>-7.2 (-7.0)<br>1.1 (1.6)<br>2.7 (1.3)<br>0.0 (-1.4)<br>**0.0 (-1.4)**<br>Tr<br>~~ee~~<br>eee|||||||
|**UKTi**<br>0.0 (-2.0)|0.0 (-2.0)|-3.2 (-2.0)|1.7 (2.3)|-5.6 (-5.9)|-1.7 (-1.9)|**-1.7 (-1.9)**|
|**HICPxT**<br>-0.7 (-2.7)|-0.7 (-2.7)|-2.6 (-2.7)|-0.1 (1.1)|-6.1 (-6.5)|-2.4 (-2.7)|**-2.4 (-2.7)**|
|**JGBi**<br>-0.6 (-1.9)|-0.6 (-1.9)|0.7 (0.8)|1.2 (1.8)|4.0 (3.9)|1.3 (1.2)|**0.0 (0.0)**|



Source: Morgan Stanley Research 

Note: Positive # = long inflation breakeven; Negative # = short inflation breakeven, (#) = previous week Thursday close which may differ from the post-nonfarm payroll update, Indicators bounded between -10 and +10, Overall signal set to zero if abs(Signal)<=1.0 and cross-market restriction is not satisfied 

## BMI Foundations 

Our Bond Market Indicators: A Powerful Systematic Approach _6 Mar 2015_ 

We introduce a suite of Bond Market Indicators, which we believe are very effective tools for guiding and framing the debate on duration. We will use the output from these models to guide our tactical interest rate market views, as well as our cross-market calls. For now, our models focus on the US, the UK, Germany and Japan. 

Bond Market Indicators: Reviewing Performance and Adding ACGB, NZGB, and CAN _27 Oct 2015_ 

We review the performance of our BMIs during its first six months ‘live’ in our research. Overall, we are pleased with the positioning signals, particularly for the US Treasury, German Bund, and UK gilt markets. We also introduce BMIs for the Australian, New Zealand, and Canadian government bond markets. We find the models would have performed well on a historical basis, using the same methodology that we developed previously for G4 markets. 

Euro Sovereign Bond Market Indicators (eBMIs) 

## _13 Apr 2016_ 

We extend our suite of Bond Market Indicators to include euro sovereign spreads. The eBMIs will guide our tactical calls on the direction of semi-core and peripheral spreads to the core, as well as semi-core vs. periphery. We also review the performance of our BMIs on their one-year anniversary. 

## Introducing Our Inflation Bond Market Indicators (iBMIs) 

## _16 Dec 2016_ 

We introduce our inflation Bond Market Indicators to guide our tactical views on G4 inflation markets. We discuss signal construction, theory, and historical performance of the iBMIs. We also review performance of the BMIs and eBMIs, and make some minor adjustments to the BMIs for next year. 

26 

27 

## **Disclosure Section** 

The information and opinions in Morgan Stanley Research were prepared or are disseminated by Morgan Stanley & Co. LLC and/or Morgan Stanley C.T.V.M. S.A. and/or Morgan Stanley México, Casa de Bolsa, S.A. de C.V. and/or Morgan Stanley Canada Limited and/or Morgan Stanley & Co. International plc and/or RMB Morgan Stanley Proprietary Limited and/or Morgan Stanley MUFG Securities Co., Ltd. and/or Morgan Stanley Capital Group Japan Co., Ltd. and/or Morgan Stanley Asia Limited and/or Morgan Stanley Asia (Singapore) Pte. (Registration number 199206298Z) and/or Morgan Stanley Asia (Singapore) Securities Pte Ltd (Registration number 200008434H), regulated by the Monetary Authority of Singapore (which accepts legal responsibility for its contents and should be contacted with respect to any matters arising from, or in connection with, Morgan Stanley Research) and/or Morgan Stanley Taiwan Limited and/or Morgan Stanley & Co International plc, Seoul Branch, and/or Morgan Stanley Australia Limited (A.B.N. 67 003 734 576, holder of Australian financial services license No. 233742, which accepts responsibility for its contents), and/or Morgan Stanley Wealth Management Australia Pty Ltd (A.B.N. 19 009 145 555, holder of Australian financial services license No. 240813, which accepts responsibility for its contents), and/or Morgan Stanley India Company Private Limited, regulated by the Securities and Exchange Board of India (“SEBI”) and holder of licenses as a Research Analyst (SEBI Registration No. INH000001105), Stock Broker (BSE Registration No. INB011054237 and NSE Registration No. INB/INF231054231), Merchant Banker (SEBI Registration No. INM000011203), and depository participant with National Securities Depository Limited (SEBI Registration No. IN-DP-NSDL-372-2014) which accepts the responsibility for its contents and should be contacted with respect to any matters arising from, or in connection with, Morgan Stanley Research, and/or PT. Morgan Stanley Sekuritas Indonesia and their affiliates (collectively, "Morgan Stanley"). 

For important disclosures, stock price charts and equity rating histories regarding companies that are the subject of this report, please see the Morgan Stanley Research Disclosure Website at www.morganstanley.com/researchdisclosures, or contact your investment representative or Morgan Stanley Research at 1585 Broadway, (Attention: Research Management), New York, NY, 10036 USA. 

For valuation methodology and risks associated with any recommendation, rating or price target referenced in this research report, please contact the Client Support Team as follows: US/Canada +1 800 303-2495; Hong Kong +852 2848-5999; Latin America +1 718 754-5444 (U.S.); London +44 (0)20-7425-8169; Singapore +65 6834-6860; Sydney +61 (0)2-9770-1505; Tokyo +81 (0)3-6836-9000. Alternatively you may contact your investment representative or Morgan Stanley Research at 1585 Broadway, (Attention: Research Management), New York, NY 10036 USA. 

## **Analyst Certification** 

The following analysts hereby certify that their views about the companies and their securities discussed in this report are accurately expressed and that they have not received and will not receive direct or indirect compensation in exchange for expressing specific recommendations or views in this report: Guneet Dhingra, CFA; Anton Heese; Matthew Hornbach; Federico Manicardi; Jesper Rooth; Koichi Sugisaki. 

Unless otherwise stated, the individuals listed on the cover page of this report are research analysts. 

## **Global Research Conflict Management Policy** 

Morgan Stanley Research has been published in accordance with our conflict management policy, which is available at www.morganstanley.com/institutional/research/conflictpolicies. 

## **Important US Regulatory Disclosures on Subject Companies** 

The equity research analysts or strategists principally responsible for the preparation of Morgan Stanley Research have received compensation based upon various factors, including quality of research, investor client feedback, stock picking, competitive factors, firm revenues and overall investment banking revenues. Equity Research analysts' or strategists' compensation is not linked to investment banking or capital markets transactions performed by Morgan Stanley or the profitability or revenues of particular trading desks. 

Morgan Stanley and its affiliates do business that relates to companies/instruments covered in Morgan Stanley Research, including market making, providing liquidity, fund management, commercial banking, extension of credit, investment services and investment banking. Morgan Stanley sells to and buys from customers the securities/instruments of companies covered in Morgan Stanley Research on a principal basis. Morgan Stanley may have a position in the debt of the Company or instruments discussed in this report. Morgan Stanley trades or may trade as principal in the debt securities (or in related derivatives) that are the subject of the debt research report. 

Certain disclosures listed above are also for compliance with applicable regulations in non-US jurisdictions. 

## **STOCK RATINGS** 

Morgan Stanley uses a relative rating system using terms such as Overweight, Equal-weight, Not-Rated or Underweight (see definitions below). Morgan Stanley does not assign ratings of Buy, Hold or Sell to the stocks we cover. Overweight, Equal-weight, Not-Rated and Underweight are not the equivalent of buy, hold and sell. Investors should carefully read the definitions of all ratings used in Morgan Stanley Research. In addition, since Morgan Stanley Research contains more complete information concerning the analyst's views, investors should carefully read Morgan Stanley Research, in its entirety, and not infer the contents from the rating alone. In any case, ratings (or research) should not be used or relied upon as investment advice. An investor's decision to buy or sell a stock should depend on individual circumstances (such as the investor's existing holdings) and other considerations. 

## **Global Stock Ratings Distribution** 

(as of May 31, 2017) 

The Stock Ratings described below apply to Morgan Stanley's Fundamental Equity Research and do not apply to Debt Research produced by the Firm. For disclosure purposes only (in accordance with NASD and NYSE requirements), we include the category headings of Buy, Hold, and Sell alongside our ratings of Overweight, Equal-weight, Not-Rated and Underweight. Morgan Stanley does not assign ratings of Buy, Hold or Sell to the stocks we cover. Overweight, Equal-weight, Not-Rated and Underweight are not the equivalent of buy, hold, and sell but represent recommended relative weightings (see definitions below). To satisfy regulatory requirements, we correspond Overweight, our most positive stock rating, with a buy recommendation; we correspond Equal-weight and Not-Rated to hold and Underweight to sell recommendations, respectively. 

28 

||COVERAGE UNIVERSE|COVERAGE UNIVERSE|INVESTMENT BANKING CLIENTS (IBC)|INVESTMENT BANKING CLIENTS (IBC)|INVESTMENT BANKING CLIENTS (IBC)|OTHER MATERIAL|OTHER MATERIAL|
|---|---|---|---|---|---|---|---|
|||||||INVESTMENT SERVICES||
|||||||CLIENTS(MISC)||
|STOCK RATING|COUNT|% OF|COUNT|% OF|% OF|COUNT|% OF|
|CATEGORY||TOTAL||TOTAL IBC|RATING||TOTAL|
||||||CATEGORY||OTHER|
||||||||MISC|
|**Overweight/Buy**|**1146**|**35%**|**298**|**41%**|**26%**|**560**|**37%**|
|**Equal-weight/Hold**|**1411**|**44%**|**333**|**46%**|**24%**|**679**|**45%**|
|**Not-Rated/Hold**|**59**|**2%**|**8**|**1%**|**14%**|**8**|**1%**|
|**Underweight/Sell**|**616**|**19%**|**87**|**12%**|**14%**|**262**|**17%**|
|**TOTAL**|**3,232**||**726**|||**1509**||



Data include common stock and ADRs currently assigned ratings. Investment Banking Clients are companies from whom Morgan Stanley received investment banking compensation in the last 12 months. 

## **Analyst Stock Ratings** 

Overweight (O or Over) - The stock's total return is expected to exceed the total return of the relevant country MSCI Index or the average total return of the analyst's industry (or industry team's) coverage universe, on a risk-adjusted basis over the next 12-18 months. Equal-weight (E or Equal) - The stock's total return is expected to be in line with the total return of the relevant country MSCI Index or the average total return of the analyst's industry (or industry team's) coverage universe, on a risk-adjusted basis over the next 12-18 months. 

Not-Rated (NR) - Currently the analyst does not have adequate conviction about the stock's total return relative to the relevant country MSCI Index or the average total return of the analyst's industry (or industry team's) coverage universe, on a risk-adjusted basis, over the next 12-18 months. Underweight (U or Under) - The stock's total return is expected to be below the total return of the relevant country MSCI Index or the average total return of the analyst's industry (or industry team's) coverage universe, on a risk-adjusted basis, over the next 12-18 months. Unless otherwise specified, the time frame for price targets included in Morgan Stanley Research is 12 to 18 months. 

## **Analyst Industry Views** 

Attractive (A): The analyst expects the performance of his or her industry coverage universe over the next 12-18 months to be attractive vs. the relevant broad market benchmark, as indicated below. 

In-Line (I): The analyst expects the performance of his or her industry coverage universe over the next 12-18 months to be in line with the relevant broad market benchmark, as indicated below. Cautious (C): The analyst views the performance of his or her industry coverage universe over the next 12-18 months with caution vs. the relevant broad market benchmark, as indicated below. 

Benchmarks for each region are as follows: North America - S&P 500; Latin America - relevant MSCI country index or MSCI Latin America Index; Europe - MSCI Europe; Japan - TOPIX; Asia - relevant MSCI country index or MSCI sub-regional index or MSCI AC Asia Pacific ex Japan Index. 

## **Important Disclosures for Morgan Stanley Smith Barney LLC Customers** 

Important disclosures regarding the relationship between the companies that are the subject of Morgan Stanley Research and Morgan Stanley Smith Barney LLC or Morgan Stanley or any of their affiliates, are available on the Morgan Stanley Wealth Management disclosure website at www.morganstanley.com/online/researchdisclosures. For Morgan Stanley specific disclosures, you may refer to www.morganstanley.com/researchdisclosures. 

Each Morgan Stanley Equity Research report is reviewed and approved on behalf of Morgan Stanley Smith Barney LLC. This review and approval is conducted by the same person who reviews the Equity Research report on behalf of Morgan Stanley. This could create a conflict of interest. 

## **Other Important Disclosures** 

Morgan Stanley Research policy is to update research reports as and when the Research Analyst and Research Management deem appropriate, based on developments with the issuer, the sector, or the market that may have a material impact on the research views or opinions stated therein. In addition, certain Research publications are intended to be updated on a regular periodic basis (weekly/monthly/quarterly/annual) and will ordinarily be updated with that frequency, unless the Research Analyst and Research Management determine that a different publication schedule is appropriate based on current conditions. Morgan Stanley is not acting as a municipal advisor and the opinions or views contained herein are not intended to be, and do not constitute, advice within the meaning of Section 975 of the Dodd-Frank Wall Street Reform and Consumer Protection Act. 

Morgan Stanley produces an equity research product called a "Tactical Idea." Views contained in a "Tactical Idea" on a particular stock may be contrary to the recommendations or views expressed in research on the same stock. This may be the result of differing time horizons, methodologies, market events, or other factors. For all research available on a particular stock, please contact your sales representative or go to Matrix at http://www.morganstanley.com/matrix. Morgan Stanley Research is provided to our clients through our proprietary research portal on Matrix and also distributed electronically by Morgan Stanley to clients. Certain, but not all, Morgan Stanley Research products are also made available to clients through third-party vendors or redistributed to clients through alternate electronic means as a convenience. For access to all available Morgan Stanley Research, please contact your sales representative or go to Matrix at http://www.morganstanley.com/matrix. 

Any access and/or use of Morgan Stanley Research is subject to Morgan Stanley's Terms of Use (http://www.morganstanley.com/terms.html). By accessing and/or using Morgan Stanley Research, you are indicating that you have read and agree to be bound by our Terms of Use (http://www.morganstanley.com/terms.html). In addition you consent to Morgan Stanley processing your personal data and using cookies in accordance with our Privacy Policy and our Global Cookies Policy (http://www.morganstanley.com/privacy_pledge.html), including for the purposes of setting your preferences and to collect readership data so that we can deliver better and more personalized service and products to you. To find out more information about how Morgan Stanley processes personal data, how we use cookies and how to reject cookies see our Privacy Policy and our Global Cookies Policy (http://www.morganstanley.com/privacy_pledge.html). 

If you do not agree to our Terms of Use and/or if you do not wish to provide your consent to Morgan Stanley processing your personal data or using cookies please do not access our research. 

Morgan Stanley Research does not provide individually tailored investment advice. Morgan Stanley Research has been prepared without regard to the circumstances and objectives of those who receive it. Morgan Stanley recommends that investors independently evaluate particular investments and 

29 

strategies, and encourages investors to seek the advice of a financial adviser. The appropriateness of an investment or strategy will depend on an investor's circumstances and objectives. The securities, instruments, or strategies discussed in Morgan Stanley Research may not be suitable for all investors, and certain investors may not be eligible to purchase or participate in some or all of them. Morgan Stanley Research is not an offer to buy or sell or the solicitation of an offer to buy or sell any security/instrument or to participate in any particular trading strategy. The value of and income from your investments may vary because of changes in interest rates, foreign exchange rates, default rates, prepayment rates, securities/instruments prices, market indexes, operational or financial conditions of companies or other factors. There may be time limitations on the exercise of options or other rights in securities/instruments transactions. Past performance is not necessarily a guide to future performance. Estimates of future performance are based on assumptions that may not be realized. If provided, and unless otherwise stated, the closing price on the cover page is that of the primary exchange for the subject company's securities/instruments. The fixed income research analysts, strategists or economists principally responsible for the preparation of Morgan Stanley Research have received compensation based upon various factors, including quality, accuracy and value of research, firm profitability or revenues (which include fixed income trading and capital markets profitability or revenues), client feedback and competitive factors. Fixed Income Research analysts', strategists' or economists' compensation is not linked to investment banking or capital markets transactions performed by Morgan Stanley or the profitability or revenues of particular trading desks. The "Important US Regulatory Disclosures on Subject Companies" section in Morgan Stanley Research lists all companies mentioned where Morgan Stanley owns 1% or more of a class of common equity securities of the companies. For all other companies mentioned in Morgan Stanley Research, Morgan Stanley may have an investment of less than 1% in securities/instruments or derivatives of securities/instruments of companies and may trade them in ways different from those discussed in Morgan Stanley Research. Employees of Morgan Stanley not involved in the preparation of Morgan Stanley Research may have investments in securities/instruments or derivatives of securities/instruments of companies mentioned and may trade them in ways different from those discussed in Morgan Stanley Research. Derivatives may be issued by Morgan Stanley or associated persons. 

With the exception of information regarding Morgan Stanley, Morgan Stanley Research is based on public information. Morgan Stanley makes every effort to use reliable, comprehensive information, but we make no representation that it is accurate or complete. We have no obligation to tell you when opinions or information in Morgan Stanley Research change apart from when we intend to discontinue equity research coverage of a subject company. Facts and views presented in Morgan Stanley Research have not been reviewed by, and may not reflect information known to, professionals in other Morgan Stanley business areas, including investment banking personnel. Morgan Stanley Research personnel may participate in company events such as site visits and are generally prohibited from accepting payment by the company of associated expenses unless pre-approved by authorized members of Research management. Morgan Stanley may make investment decisions that are inconsistent with the recommendations or views in this report. 

To our readers based in Taiwan or trading in Taiwan securities/instruments: Information on securities/instruments that trade in Taiwan is distributed by Morgan Stanley Taiwan Limited ("MSTL"). Such information is for your reference only. The reader should independently evaluate the investment risks and is solely responsible for their investment decisions. Morgan Stanley Research may not be distributed to the public media or quoted or used by the public media without the express written consent of Morgan Stanley. Any non-customer reader within the scope of Article 7-1 of the Taiwan Stock Exchange Recommendation Regulations accessing and/or receiving Morgan Stanley Research is not permitted to provide Morgan Stanley Research to any third party (including but not limited to related parties, affiliated companies and any other third parties) or engage in any activities regarding Morgan Stanley Research which may create or give the appearance of creating a conflict of interest. Information on securities/instruments that do not trade in Taiwan is for informational purposes only and is not to be construed as a recommendation or a solicitation to trade in such securities/instruments. MSTL may not execute transactions for clients in these securities/instruments. Certain information in Morgan Stanley Research was sourced by employees of the Shanghai Representative Office of Morgan Stanley Asia Limited for the use of Morgan Stanley Asia Limited. 

Morgan Stanley is not incorporated under PRC law and the research in relation to this report is conducted outside the PRC. Morgan Stanley Research does not constitute an offer to sell or the solicitation of an offer to buy any securities in the PRC. PRC investors shall have the relevant qualifications to invest in such securities and shall be responsible for obtaining all relevant approvals, licenses, verifications and/or registrations from the relevant governmental authorities themselves. Neither this report nor any part of it is intended as, or shall constitute, provision of any consultancy or advisory service of securities investment as defined under PRC law. Such information is provided for your reference only. 

Morgan Stanley Research is disseminated in Brazil by Morgan Stanley C.T.V.M. S.A.; in Mexico by Morgan Stanley México, Casa de Bolsa, S.A. de C.V which is regulated by Comision Nacional Bancaria y de Valores. Paseo de los Tamarindos 90, Torre 1, Col. Bosques de las Lomas Floor 29, 05120 Mexico City; in Japan by Morgan Stanley MUFG Securities Co., Ltd. and, for Commodities related research reports only, Morgan Stanley Capital Group Japan Co., Ltd; in Hong Kong by Morgan Stanley Asia Limited (which accepts responsibility for its contents) and by Morgan Stanley Asia International Limited, Hong Kong Branch; in Singapore by Morgan Stanley Asia (Singapore) Pte. (Registration number 199206298Z) and/or Morgan Stanley Asia (Singapore) Securities Pte Ltd (Registration number 200008434H), regulated by the Monetary Authority of Singapore (which accepts legal responsibility for its contents and should be contacted with respect to any matters arising from, or in connection with, Morgan Stanley Research) and by Morgan Stanley Asia International Limited, Singapore Branch (Registration number T11FC0207F); in Australia to "wholesale clients" within the meaning of the Australian Corporations Act by Morgan Stanley Australia Limited A.B.N. 67 003 734 576, holder of Australian financial services license No. 233742, which accepts responsibility for its contents; in Australia to "wholesale clients" and "retail clients" within the meaning of the Australian Corporations Act by Morgan Stanley Wealth Management Australia Pty Ltd (A.B.N. 19 009 145 555, holder of Australian financial services license No. 240813, which accepts responsibility for its contents; in Korea by Morgan Stanley & Co International plc, Seoul Branch; in India by Morgan Stanley India Company Private Limited; in Indonesia by PT. Morgan Stanley Sekuritas Indonesia; in Canada by Morgan Stanley Canada Limited, which has approved of and takes responsibility for its contents in Canada; in Germany by Morgan Stanley Bank AG, Frankfurt am Main and Morgan Stanley Private Wealth Management Limited, Niederlassung Deutschland, regulated by Bundesanstalt fuer Finanzdienstleistungsaufsicht (BaFin); in Spain by Morgan Stanley, S.V., S.A., a Morgan Stanley group company, which is supervised by the Spanish Securities Markets Commission (CNMV) and states that Morgan Stanley Research has been written and distributed in accordance with the rules of conduct applicable to financial research as established under Spanish regulations; in the US by Morgan Stanley & Co. LLC, which accepts responsibility for its contents. Morgan Stanley & Co. International plc, authorized by the Prudential Regulatory Authority and regulated by the Financial Conduct Authority and the Prudential Regulatory Authority, disseminates in the UK research that it has prepared, and approves solely for the purposes of section 21 of the Financial Services and Markets Act 2000, research which has been prepared by any of its affiliates. RMB Morgan Stanley Proprietary Limited is a member of the JSE Limited and regulated by the Financial Services Board in South Africa. RMB Morgan Stanley Proprietary Limited is a joint venture owned equally by Morgan Stanley International Holdings Inc. and RMB Investment Advisory (Proprietary) Limited, which is wholly owned by FirstRand Limited. The information in Morgan Stanley Research is being disseminated by Morgan Stanley Saudi Arabia, regulated by the Capital Market Authority in the Kingdom of Saudi Arabia , and is directed at Sophisticated investors only. 

The information in Morgan Stanley Research is being communicated by Morgan Stanley & Co. International plc (DIFC Branch), regulated by the Dubai Financial Services Authority (the DFSA), and is directed at Professional Clients only, as defined by the DFSA. The financial products or financial services to which this research relates will only be made available to a customer who we are satisfied meets the regulatory criteria to be a Professional Client. The information in Morgan Stanley Research is being communicated by Morgan Stanley & Co. International plc (QFC Branch), regulated by the Qatar Financial Centre Regulatory Authority (the QFCRA), and is directed at business customers and market counterparties only and is not intended for Retail Customers as defined by the QFCRA. 

As required by the Capital Markets Board of Turkey, investment information, comments and recommendations stated here, are not within the scope of 

30 

investment advisory activity. Investment advisory service is provided exclusively to persons based on their risk and income preferences by the authorized firms. Comments and recommendations stated here are general in nature. These opinions may not fit to your financial status, risk and return preferences. For this reason, to make an investment decision by relying solely to this information stated here may not bring about outcomes that fit your expectations. The trademarks and service marks contained in Morgan Stanley Research are the property of their respective owners. Third-party data providers make no warranties or representations relating to the accuracy, completeness, or timeliness of the data they provide and shall not have liability for any damages relating to such data. The Global Industry Classification Standard (GICS) was developed by and is the exclusive property of MSCI and S&P. Morgan Stanley Research, or any portion thereof may not be reprinted, sold or redistributed without the written consent of Morgan Stanley. 

© 2017 Morgan Stanley 

31 


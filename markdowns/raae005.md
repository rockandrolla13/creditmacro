# **Contingent Claims and Hedging of Credit Risk with Equity Options** 

## **Davide E. Avino** 

Management School, University of Liverpool, United Kingdom 

## **Enrique Salvador** 

Jaume I University, Spain 

Using contingent-claims valuation, we introduce novel hedge ratios for credit exposures using put options. Option hedge ratios are generally in line with the empirical sensitivities of credit spread changes to put option returns and, relative to stock hedge ratios, produce further reductions in volatility for a portfolio of North American firms. We show that option hedge ratios capture option-specific credit exposure related to the VIX index and the default spread, which is unaccounted for by Merton’s (1974) equity hedge ratios alone. Combining stocks and put options for credit risk hedging can be done effectively using the volatility smirk. ( _JEL_ E43, E44, G10) 

Received: 8 October 2021; Editorial decision: 5 January 2024 Editor: Hui Chen 

Authors have furnished an Internet Appendix, which is available on the Oxford University Press Web site next to the link to the final published paper online. 

Since the publication of the seminal paper by Modigliani and Miller (1958) on the theory of optimal capital structure, extensive attention has been drawn to the relationship between debt and equity values. Based on the option pricing theory developed by Black and Scholes (1973) and Merton (1973), Merton (1974) introduced the first structural model of credit risk building on the notion that equity and debt can be valued as options on the firm value.[1 ] A few years later, Geske (1979) 

We are grateful to Hui Chen (the editor), an anonymous referee, Antonello Avino, Periklis Boumparis, Han-Sheng Chen, Adnan Gazi, Dale Gray, Andreas Kaeck, Alex Kostakis, Alex Michaelides, Manuel Moreno, Chardin Wese Simen and seminar and conference participants at the 2019 OptionMetrics Research Conference, the 13th NUS-RMI Annual Risk Management Conference, the 2019 IRMC, the 2019 Northfield’s Investment Seminar, the 26th Finance Forum, the 2018 C.R.E.D.I.T. Conference, the 2018 FMA meeting in San Diego, the 13th INQUIRE-UK Business School seminar, the University of Reading, the University of Sussex, and the University of Liverpool for helpful comments and discussions. D. E. Avino acknowledges a research grant from Cardiff University for partial support and a mobility grant from Banco Santander. The paper received the Best Conference Paper Award at the 2019 International Risk Management Conference. Send correspondence to Davide E. Avino, d.avino@liverpool.ac.uk. 

- 1 Since Merton (1974), structural models of credit risk have evolved to include stochastic interest rates (Longstaff and Schwartz 1995), stochastic jump-diffusion process for the firm value (Zhou 2001; Cremers, Driessen, and Maenhout 2008; Huang and Huang 2012), dynamic capital structure (Leland and Toft 1996), stationary leverage ratios (Collin- 

_The Review of Asset Pricing Studies_ 14 (2024) 310–347 

# The Author(s) 2024. Published by Oxford University Press on behalf of The Society for Financial Studies. This is an Open Access article distributed under the terms of the Creative Commons Attribution License (https:// creativecommons.org/licenses/by/4.0/), which permits unrestricted reuse, distribution, and reproduction in any medium, provided the original work is properly cited. 

https://doi.org/10.1093/rapstu/raae005 Advance Access publication 8 March 2024 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

developed a structural model to price options on options (or compound options). If a stock can be regarded as a call option on the value of the firm, an option on the stock is equivalent to an option on an option. 

In this paper, we use contingent-claims valuation to introduce novel hedge ratios that can be used to neutralize market value changes of credit exposures using equity put options. This is an important topic for practitioners who are mainly interested in developing their hedging techniques and cross-market arbitrage as well as economists who are concerned about the accuracy of the models. Specifically, we derive theoretical hedge ratios of bond credit spreads to equity options by combining the structural models of Merton (1974) and Geske (1979) in order to study the sensitivities of credit spreads to equity options. To this end, we analytically solve the partial derivative of the bond credit spread with respect to the option price using the credit spread implied by the Merton (1974) model as well as the option price implied by the Geske (1979) model. While previous studies have analyzed the ability of the Merton (1974) model to generate accurate sensitivities of debt-to-equity values (Schaefer and Strebulaev 2008; Che and Kapadia 2012; Bao and Hou 2017; Huang, Shi, and Zhou 2020; Huang and Shi 2021), we are the first to test whether the compound option model of Geske (1979) produces accurate sensitivities of credit spreads to option values.[2] 

Two main theoretical ideas justify an investigation of credit hedging strategies based on the use of options rather than stocks. First, out-of-the-money (OTM) put options can help insure against large price shocks (jumps), which are potentially more clearly associated with credit risk. Particularly, it is the price of deep OTM puts which should reflect more accurately information on credit risk, rather than stock price fluctuations, which can instead be affected by many other factors (Carr and Wu 2011). Second, in a more realistic world of incomplete capital markets characterized by limits-to-arbitrage and information asymmetry, option payoffs cannot be perfectly replicated by underlying assets, and hence options are not redundant assets (Ross 1976; Back 1993). An informed investor may strategically choose to trade in the option market, if it is sufficiently liquid, to exploit the higher leverage embedded in options (Black 1975; Easley, O’Hara, and Srinivas 1998), or to disguise her information signal in the presence of noise traders (An et al. 2014). As a potential consequence and consistent with these two theoretical reasons, option prices may reflect information about volatility or jumps that is not reflected in stocks or, more generally, information that is not already 

> Dufresne and Goldstein 2001), and strategic default (Anderson and Sundaresan 1996; Mella-Barral and Perraudin 1997). More recent models have attempted to incorporate macroeconomic conditions to explain credit spreads (Chen, Collin-Dufresne, and Goldstein 2009; Chen 2010; Bhamra, Kuehn, and Strebulaev 2010). 

> 2 In a recent paper, Geske, Subrahmanyam, and Zhou (2016) study the pricing performance of the compound option model and find that, relative to the model of Black and Scholes (1973), pricing errors of individual stock options can be reduced across all strikes and maturity dates and that greater improvements are achieved for long-term options and for firms with higher levels of market leverage. On the other hand, structural models of credit risk are generally unable to accurately replicate corporate bond prices, and most of them underestimate credit spreads (Jones, Mason, and Rosenfeld 1984; Eom, Helwege, and Huang 2004; Huang and Huang 2012). 

311 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

incorporated into the price of the underlying asset and, therefore, improve hedging effectiveness.[3] 

We test the empirical validity of our option-based hedge ratios on a sample of 230 firms for which data on both American put options on stocks and CDS spreads on corporate bonds are available during the period August 2001 to December 2021. We find that the sensitivities of CDS spread changes to option returns are generally in line with the models using both model-free calibration of the parameters and their maximum likelihood estimation in an internally consistent manner. Differently from the case of stocks, we find that hedge ratio regressions can improve adjusted _R_ -squared values (up to 5–8 percentage points for BBB-rated and A-rated firms, respectively) relative to empirical regressions of credit spread changes on option returns and interest rate changes. This improvement in the ability of the regression model to explain more of the variability of the credit spread changes is corroborated by a comparative analysis of hedging effectiveness between model-based equity hedge ratios and model-based option hedge ratios. In an out-of-sample analysis, the latter reduce volatility by an additional 5% for the full portfolio of firms (reducing the root mean square error of the CDS portfolio by 22%). The empirical counterparts of both stock and put hedge ratios deliver a similar reduction in root mean square error (of about 25% relative to an unhedged CDS portfolio including the entire sample of firms), with stock empirical hedge ratios delivering the best hedging performance particularly when based on a sample of long-term options. 

Our empirical findings suggest that both stock and option markets can be useful for hedging credit risk. More importantly, options may contain information that doesn’t overlap with equity markets and thus makes it particularly suitable to learn about credit risk. We investigate this point further with additional empirical tests and find that option returns can explain an additional 5% of the variations in CDS spread changes that are left unexplained by firm-specific stock market variables. More importantly, we find that the source underlying the variation in the option hedge ratios that contribute to this additional explanatory power is due to the option-only component of the hedge ratios, that is the reciprocal of the put option delta (or stock-option hedge ratio) implied by the compound option model of Geske (1979). This component, that captures leverage effects introduced by the strike price of the first option (the stock) and directly transmitted to option prices (the option on the stock), is related to credit risk factors including the VIX index and the default spread, consistent with the ability of the compound option model to generate a stock stochastic volatility process induced by these leverage effects. 

> 3 If options were really redundant assets, the introduction of option trading should not produce any statistically significant effects on returns and volatility of the underlying stocks. However, Conrad (1989) and Skinner (1989) document significant price effects on the underlying stock associated with option introduction. Evidence on the presence of informed trading in the option market is mixed: while a growing body of evidence indicates that various optionbased variables can predict future stock returns (Ofek, Richardson, and Whitelaw 2004; Cao, Chen, and Griffin 2005; Pan and Poteshman 2006; Cremers and Weinbaum 2010; Xing et al. 2010; Bali and Hovakimian 2009; Johnson and So 2012; Stilger, Kostakis, and Poon 2017), a few studies show that no informed trading seems to be present in the option market (Muravyev, Pearson, and Broussard 2013; Collin-Dufresne, Fos, and Muravyev 2021). 

312 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

Having ascertained that options are useful for hedging credit risk, we then strategically combine them with stocks in the hedging portfolios and find that the best hedging performance is obtained when the trading decisions on both instruments are made based on changes in the volatility smirk. We find that the latter can positively predict the gap in hedging errors between stocks and options in the time series. Based on this, a market timing strategy that buys (shorts) puts (stocks) when the changes in the volatility skew in a given month are above (below) their 75th (25th) percentile, and that otherwise invests 50% in puts and 50% in stocks, produces further reductions in portfolio volatility for both model hedge ratios and empirical hedge ratios relative to a strategy that, each month, is 100% invested in either stocks or options. 

More generally, our hedge ratios are fundamentally different from what has been suggested by past studies (Carr and Wu 2011; JPMorgan 2006), according to which the composition of the replicating option portfolio is determined ex ante by the loss expected at default, which is uncertain due to recovery risk.[4 ] Rather than hedging the default loss, we instead propose hedging changes in the market value of a long credit risk position.[5,6 ] Our empirical analysis suggests that adopting this mark-to-market hedging approach would involve a reduction in hedging costs of almost 90% for a portfolio of short CDS positions (which includes our sample of firms) on a notional amount of $10 million per contract.[7] 

Our work is most germane to the studies of Schaefer and Strebulaev (2008), Huang and Shi (2021), Che and Kapadia (2012) and Huang et al. (2020) who analyze the empirical sensitivities of debt-to-equity values finding that they are in line with the sensitivities implied by the Merton (1974) model. Schaefer and Strebulaev (2008) and Huang and Shi (2021) show that the Merton (1974) model provides accurate predictions of the sensitivity of both corporate bond returns and credit spread changes to changes in equity values. Che and Kapadia (2012) and Huang et al. (2020) confirm the ability of the Merton model to explain also the sensitivities of CDS spreads to equity returns. In addition, Huang et al. (2020) propose a new approach for estimating the main parameters and conduct 

> 4 In particular, the number of put options to buy depends on the assumptions related to the recovery rate on the underlying corporate bond in the occurrence of a default event. 

> 5 The mark-to-market hedging approach we propose acknowledges the possibility that credit risk comes in different forms that may not necessarily be linked to the occurrence of a credit event but simply to the increased collateral requirements due to adverse market value changes and rating migration risk. See, for instance, Stulz (2010) for a detailed description of the events surrounding the Fed bailout of the American International Group in 2008. 

> 6 Using the risk-neutral measure of the credit loss from the implicit put option (required to compute the firm’s debt value based on Merton 1974) allows us to avoid using simplistic assumptions on the bond recovery rates of defaulting firms. These can be hard to identify given their systematic time variations over the business cycle and across seniority levels (Altman et al. 2005), and across industries (Acharya et al. 2007) often ignored in risk management models. 

> 7 From a practitioner’s perspective, hedging corporate credit risk could be achieved by simply buying CDS contracts. However, this would not allow traders to arbitrage between credit and equity and/or equity option markets. Our theoretical hedge ratios enable innovative capital structure arbitrage trades between credit instruments and equity options. In particular, market credit spreads could be compared to option-implied credit spreads and the amount of options to be traded could be based on our theoretical hedge ratios. Culp et al. (2018) discuss a recent example of how to obtain option-implied credit spreads. Capital structure arbitrage is traditionally implemented trading CDS and equities using Merton-based equity hedge ratios as detailed, for instance, by Yu (2006) and Duarte et al. (2007). 

313 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

specification tests of five different structural credit risk models based on the use of generalized method of moments. They find that the Merton model fares better than more sophisticated credit risk models in terms of hedging effectiveness as measured by reduced hedging errors. Differently from these papers, our focus is on hedging credit spreads with equity options by introducing novel hedge ratios, which blend together the structural credit risk model of Merton (1974) with the compound option pricing model of Geske (1979). Hence, we contribute to the structural credit risk modeling literature by investigating the sensitivity of debt-toequity option values. Our paper is also different from Schaefer and Strebulaev (2008) and Huang and Shi (2021) because we consider, similarly to Huang et al. (2020), hedging CDS spread changes (rather than corporate bond returns or credit spread changes) and provide direct evidence on hedging effectiveness. However, differently from Huang et al. (2020), we adopt an alternative consistent estimation technique for the Merton (1974) model parameters based on maximum likelihood estimation and we extend their analysis on the hedging effectiveness by comparing the hedging performance of both stocks and options. Unlike the papers above, we propose an effective way to combine equities and options for credit risk hedging based on the use of the volatility smirk. 

## **1. Literature on Credit and Option Markets** 

Academic studies on the relationship between credit markets and equity options are limited. Carr and Wu (2010) introduce a methodology that allows joint valuation of CDS and equity options. In another related paper, Carr and Wu (2011) also establish a robust theoretical link between deep OTM American put options and CDS. In particular, under the assumption that the stock price drops to zero at default, a long position in a put option (scaled by its strike) replicates the payoff of a standardized credit contract. Empirical tests also show that estimates of optionimplied and CDS-implied unit recovery claims (or URC) are not statistically different from each other, confirming that the two markets strongly comove. Berndt and Ostrovnaya (2014) examine CDS spreads and option prices and show that both markets react faster than the equity market prior to the release of negative credit news. Collin-Dufresne et al. (2012) use index option prices and corporate bond credit spreads to infer market and firm-level dynamics, respectively. Then they use these to jointly price S&P 500 index options and CDO tranches of corporate debt. Seo and Wachter (2018) build a mathematical model based on time-varying probabilities of economic catastrophe to price CDX index senior tranches before and during the 2008-2009 financial crisis. They show that these instruments are extremely deep OTM put options on the U.S. economy. Culp et al. (2018) compare credit spreads based on traded corporate bonds with credit spreads based on pseudo bonds computed from equity options. The latter are based on the Merton (1974) insight that the value of risky debt is equivalent to a riskless bond minus the value of a put option on the firm’s assets. They show that observed credit spreads and pseudo credit spreads share common time-series characteristics 

314 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

documenting a high degree of integration between the corporate bond and equity option markets. Kuehn et al. (2017) show how to retrieve the default probabilities and loss rates from CDS spreads and equity put option prices. Similar to the Black and Scholes (1973) option-implied volatility surface, Kelly et al. (2016) construct a credit-implied volatility surface from observable CDS spreads using the Merton (1974) model formula for credit spreads. Reindl et al. (2017) infer bankruptcy costs from equity and equity put option prices during the 2008–2010 period for a sample of S&P 500 firms. 

A number of empirical studies on the determinants of credit spreads have documented a positive incremental effect of option-implied volatilities and jump risk measures on credit spread levels (Cremers et al. 2008; Cao et al. 2010) as well as changes (Collin-Dufresne et al. 2001). In particular, Cremers et al. (2008) use panel regressions of credit spreads on both historical and optionimplied proxies of return volatility and volatility skew. They find that both implied volatility and (to a lesser extent) implied volatility skew dominate their historical counterparts for long-maturity bonds and lower-rated debt. Similarly, Cao, Yu, and Zhong (2010) find that option-implied volatilities dominate historical volatility in firm-by-firm time-series regressions of CDS spread levels and that this finding is particularly strong for lower-rated firms. Further investigation of their results reveals that the explanatory power of the implied volatility derives from its greater ability to forecast future volatility and to capture a time-varying volatility risk premium. Collin-Dufresne et al. (2001) confirm the importance of optionimplied volatility (proxied for by changes in the VIX index) and jump risk (proxied for by the change in the slope of the “smirk” of implied volatilities of S&P 500 futures options) for explaining credit spread changes. Related to these papers, Cao, Yu, and Zhong (2011) and Cremers, Driessen, and Maenhout (2008) also show that credit spread levels’ pricing errors of structural models of credit risk can be reduced by calibrating them with measures of option-implied volatility and option-implied risk premiums, respectively.[8] 

## **2. Hedging Credit with Puts Using Structural Models** 

This section describes how we derive theoretical hedge ratios of bond credit spreads to put options using the structural models of Merton (1974) and Geske (1979). According to these models, the firm value _V_ represents the underlying state variable required to specify the models’ main outputs. In particular, the bond credit spread and the option value are both a function of the variable _V_ , which is assumed to follow a diffusion-type stochastic process. In Merton’s model, _V_ determines a firm’s default, which occurs whenever its value falls below the face value of debt. In Geske’s model, _V_ determines whether the option should be exercised when it 

> 8 Other papers investigating the determinants of credit (or CDS) spreads are by Elton et al. (2001), Campbell and Taksler (2003), Longstaff et al. (2005), Das and Hanouna (2009), Ericsson et al. (2009) and Zhang et al. (2009). These studies also include firm leverage, interest rates, the slope of the term structure of interest rates, and the return on the S&P 500 index as additional state variables to explain variations in spreads. 

315 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

expires or it should remain unexercised. As the firm value represents the only driving stochastic factor of these two models, the elasticity of the bond credit spread ( _CS_ ) to the value of the option ( _P_ ) is related to the sensitivity of both the spread and the option price to _V_ by the following relation: 

**==> picture [220 x 24] intentionally omitted <==**

where _@_ represents the partial derivative symbol. 

As they define the weights in the hedging portfolio, we refer to these sensitivities as hedge ratios. While these sensitivities can be estimated by a linear regression of bond credit spread changes on the returns of a put option on the firm’s stock, time variation in the elasticity can only be captured by the theoretical hedge ratios based on structural models. In Appendix A, we show the steps taken to solve the two partial derivatives in Equation (1), which provides the following solution for the theoretical hedge ratios ( _hrP_ ): 

**==> picture [311 x 100] intentionally omitted <==**

where 

**==> picture [145 x 141] intentionally omitted <==**

_V_ ¼ current value of the firm’s assets, 

� _V_ ¼ value of _V_ such that 

**==> picture [262 x 17] intentionally omitted <==**

_D_ ¼ face value of the debt, 

316 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

_r_ ¼ the risk-free rate of interest, 

- s ¼ maturity date of the debt, 

s1 ¼ maturity date of the put option, 

r[2] _V_[¼][ the instantaneous variance of the return on the assets of the firm,] 

- _K_ ¼ strike price of the put option, 

- /½��¼ univariate normal density function, 

- U½��¼ univariate cumulative normal distribution function, 

- H½��¼ bivariate cumulative normal distribution function. 

As _@@CSV[<]_[ 0 and ] _@@VP[<]_[ 0, hedge ratios implied by the theory predict a positive ] relationship between changes in option values and bond credit spread changes ~~(~~ _@@CSP[>]_[ 0).] 

## **3. Sample Selection and Data Construction** 

We obtain our data on U.S. dollar-denominated CDS spreads from Bloomberg. Our sample consists of monthly observations from August 2001 to December 2021. The information about CDS spreads is extracted using 5-year maturity contracts (as they are the most actively traded) on senior unsecured debt. We start with an initial sample of 1,476 corporate reference entities with CDS contracts traded. From these, we were able to identify 503 North American firms with available Standard & Poor’s credit rating, having at least 24 months of CDS spreads as well as equity market data (stock prices, trading volumes and outstanding number of shares adjusted for stock dividends and splits) in the Center for Research on Security Prices (CRSP) database based on their Committee on Uniform Security Identification Procedures (CUSIP) number. After removing firms with no accounting data on company debt from Compustat, we are left with 379 firms. 

Using the CUSIP identifier, we match CDS data with option data from OptionMetrics using the Security file, the Security Price file, the Distribution file and the Option Price file all available in the database. As we want to focus on highly liquid contracts, we select put options with short maturities that either expire the next month or 2 months after the trading date. Then we use the selected put contract to create a monthly time series of option returns matched with the monthly time series of CDS spread changes. In particular, the options are purchased the first day after the expiration of the previous month’s option, which is usually on the next Monday following the third Friday of each month. We get information about the following characteristics of the put options: strike price, maturity, moneyness, open interest, traded volume, implied volatility and delta. 

We follow previous papers (Goyal and Saretto 2009) and apply the following filters to the option data: the bid price is positive and strictly smaller than the ask price, the traded volume and the open interest are both positive and the bid-ask spread is lower than the minimum tick size (which is equal to $0.05 for options trading below $3 and $0.10 in any other case). We also eliminate prices violating 

317 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

arbitrage bounds. To construct our time series of options we need to choose only one put option contract among all those traded on the day when we purchase the option. In selecting the options, we prefer those with a 2-month maturity (rather than the 1-month contracts) in order to avoid the use of holding-to-maturity option returns that have been shown to be affected by biases at expiration (Ni et al. 2005).[9 ] Whenever a 2-month maturity option that meets our filtering criteria is not available in a given month, we select a 1-month contract that does meet the same criteria. Given the established link between CDS contracts and OTM put options (Carr and Wu 2011), we build a monthly time series of put options which are, on average, OTM.[10 ] We start by selecting put options with moneyness (defined as the ratio of strike to stock price) lower than 0.90. In the eventuality that no option is traded on a given day with such moneyness levels, we replace it with an option with moneyness lower than 0.925. If there is still no option available, we select one with moneyness lower than 0.95. If there are no options available with this moneyness level, we select one with moneyness lower than 0.975. If still we cannot find options, we select one put option with moneyness lower than 1. This algorithm allows us to create, for each firm in our sample, a continuous monthly time series of option returns based on a sample of put options that are, on average, OTM. 

Hence, each month, we select one put option with the highest open interest that meets all the above characteristics. After applying the previous option filters, we lose an additional 149 firms, leaving us with a final sample of 230 firms.[11 ] Given that the traded equity option contracts are American while our theoretical hedge ratios are derived for European options, we convert American option prices into European prices by following the procedure adopted by Trolle and Schwartz (2009). 

From Table 1 we can observe that most firms in our final sample are rated BBB (118 firms) and A (70 firms). The remaining firms are AAA-rated (only 1 firm), 

- 9 Selecting 2-month maturity options to compute 1-month holding-period returns also allows us to mitigate the incidence of many repeated values of -100% returns that particularly affect OTM expirations. 

> 10 Our focus on short-maturity OTM puts also mitigates any issue related to the possibility of early exercise (Barraclough and Whaley 2012). For these contracts, both the probability of early exercise and the forgone net interest income from failure to exercise before the expiration would be smaller. Furthermore, the main parameter in our analysis that could be affected by early exercise of put options is the firm’s asset volatility, which depends on the option-implied volatility. The fact that this is computed by OptionMetrics using binomial trees that account for dividend payments also alleviates our concerns on this issue. While other papers did not directly address the early exercise issue of put options (Hu and Jacobs 2020; Goyal and Saretto 2009), the papers that attempted to deal with it have found that adjusting for early exercise has minor empirical consequences (Broadie et al. 2007; Boyer and Vorkink 2014). 

- 11 Our final sample of 230 firms over 20 years compares favorably with other studies that have jointly analyzed CDS and equity options: for example, Kuehn et al. (2017) and Berndt and Ostrovnaya (2014) use data on 106 and 144 firms for a much shorter sample period, respectively. Carr and Wu (2010) collect data for eight reference firms during a 4-year period, while the Carr and Wu (2011) sample includes 121 firms for a period of 3.5 years. Differently from ours, the latter study focuses on deep OTM puts and long maturity contracts (with a time-to-maturity of at least 360 days) in order to minimize the maturity mismatch with the corresponding CDS contract. This comes at the expense of liquidity as the authors are not able to observe a continuous time series of put prices for most of the 121 firms in their sample (the average number of firms they can observe each week is 28). Furthermore, the maturity mismatch between puts and CDS is not really a concern for our empirical analysis as the compound option model we use allows for the existence of a mismatch between a shorter maturity put option and a longer debt maturity that we set equal to the maturity of the CDS contract. 

318 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

**Table 1** 

**Summary statistics for the final sample of put options** 

||All|AAA-AA|A|BBB|BB-B|
|---|---|---|---|---|---|
|No. frms|230|11|70|118|31|
|Nobs|24,249|1,327|8,332|12,248|2,342|
|Mean maturity|42.979|48.254|44.908|41.860|41.009|
|Median maturity|41.715|53.636|46.164|38.894|38.177|
|Mean moneyness|0.946|0.951|0.946|0.947|0.939|
|Median moneyness|0.951|0.955|0.952|0.952|0.942|
|Mean open interest|4,135|9,036|5,696|2,691|4,367|
|Median open interest|2,541|5,733|3,732|1,546|2,505|
|Mean delta|−0.300|−0.272|−0.284|−0.308|−0.316|
|Median delta|−0.284|−0.260|−0.270|−0.292|−0.293|



_This table reports summary statistics for the final sample of put options obtained from OptionMetrics during the period August 2001 to December 2021. In particular, mean and median values are reported for option maturity (on the trading date), moneyness (defined as the ratio of strike to stock price), open interest, and delta. The statistics are first computed for each firm using the time series of each variable and then averaged across firms. Each firm is assigned a credit rating based on its average rating across years for which both CDS and option data are available. Nobs is the number of observations._ 

AA-rated (10 firms), BB-rated (26), and B-rated (5 firms).[12 ] Credit ratings are from Bloomberg and are based on the Standard & Poor’s credit rating agency. To assign credit ratings to each firm, we transform them into numerical values, take an average over the period for which CDS and put option data are available, and convert the number back into a rating.[13 ] Table 1 also reports summary statistics on our sample of put options. The mean maturity and moneyness of the put contracts are 43 calendar days and 0.946, respectively. The mean delta and open interest are − 0.30 and 4,135, respectively. The mean open interest varies considerably across rating categories: it is the highest for the best-rated firms (and equal to 9,036) and the lowest for BBB-rated firms (equal to 2,691). 

We compute monthly put option returns by dividing the change in option price (or the difference between the option payoff at maturity and the option price if a 1- month contract is selected in a given month) by the option price on the trading date. To mitigate the influence of outliers in the regressions, we winsorize CDS spread changes at the 1% and 99% levels and put returns at the 99% level. 

Table 2 describes the main summary statistics for both CDS and option data in panels A and B, respectively. The average CDS spread change for the entire portfolio of firms is negative and ranges from about zero basis points for the 

> 12 The subsample of firms rated AAA-AA is very small. This is due to (1) our definition of rating portfolios that rely on the average rating of the issuer over the sample period and (2) the application of the option filtering criteria required to produce a homogeneous sample of put options. Previous papers on the hedging performance of the Merton (1974) model have instead used stocks that do not undergo a similar strict filtering procedure as options and define rating portfolios based on the first date when a bond is present in the data set (Schaefer and Strebulaev 2008; Huang and Shi 2021), based on the last available rating (Huang et al. 2020) or based, as we do, on the average rating over time (Che and Kapadia 2012). Despite these differences, our sample size compares favorably with studies that also used CDS data: for instance, Huang et al. (2020) have a total of 93 firms (7 of which are rated AAA-AA), while Che and Kapadia (2012) use a sample of 207 firms with 33 firms rated A or higher. 

> 13 The main empirical findings of this paper are based on the use of average ratings. However, as a robustness, we repeat the empirical analysis using the rating available at the end of the sample period for each firm and obtain very similar results. These results are available on request from the authors. 

319 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

**Table 2** 

**Summary statistics on monthly returns and liquidity proxies for CDS and options** 

||All|AAA-AA|A|BBB|BB-B|
|---|---|---|---|---|---|
|_A. CDS data_||||||
|_CDS spread changes (in_|_basis points)_|||||
|Mean|−0.547|0.032|−0.097|−0.222|−4.718|
|Standard deviation|12.627|4.163|8.002|12.428|33.139|
|Skewness|1.400|2.130|1.305|1.507|0.372|
|Kurtosis|8.635|16.054|5.865|8.627|1.191|
|5% quantile|−17.321|−4.499|−11.906|−16.122|−49.065|
|95% quantile|18.048|5.237|14.327|18.726|61.223|
|_CDS bid-ask spread_||||||
|Mean|0.126|0.226|0.138|0.110|0.073|
|Standard deviation|0.047|0.122|0.050|0.038|0.026|
|Skewness|1.163|1.082|0.754|0.914|1.092|
|Kurtosis|2.187|0.803|−0.126|1.673|0.978|
|5% quantile|0.066|0.090|0.077|0.059|0.043|
|95% quantile|0.205|0.462|0.235|0.175|0.126|
|_CDS-bond basis (in basis points)_||||||
|Mean|−88.667|−70.060|−71.200|−88.673|−91.614|
|Standard deviation|104.515|178.792|94.036|101.814|159.621|
|Skewness|−2.250|−4.130|−2.927|−2.375|−4.147|
|Kurtosis|4.221|17.623|8.529|5.879|18.805|
|5% quantile|−374.964|−520.408|−315.044|−312.463|−378.266|
|95% quantile|−16.370|5.725|−15.741|−17.012|17.896|
|_B. Option data_||||||
|_Option returns_||||||
|Mean|−0.167|−0.234|−0.246|−0.169|−0.169|
|Standard deviation|0.950|0.873|0.782|0.765|0.943|
|Skewness|3.746|2.512|2.559|2.529|2.374|
|Kurtosis|20.276|7.147|7.595|8.259|6.714|
|5% quantile|−0.867|−0.950|−0.889|−0.860|−0.914|
|95% quantile|1.631|1.599|1.500|1.376|1.993|
|_Option bid-ask spread_||||||
|Mean|0.133|0.084|0.104|0.161|0.156|
|Standard deviation|0.035|0.051|0.037|0.031|0.051|
|Skewness|0.757|1.400|0.650|0.602|0.836|
|Kurtosis|5.335|2.442|−0.171|1.250|2.171|
|5% quantile|0.077|0.030|0.052|0.117|0.081|
|95% quantile|0.187|0.184|0.170|0.209|0.241|
|_Option expensiveness_||||||
|Mean|−0.036|0.072|−0.008|−0.041|−0.175|
|Standard deviation|0.139|0.055|0.145|0.121|0.239|
|Skewness|−2.376|−1.159|−3.540|−2.542|−2.814|
|Kurtosis|9.957|4.964|17.877|11.009|11.408|
|5% quantile|−0.260|−0.011|−0.222|−0.206|−0.603|
|95% quantile|0.111|0.148|0.118|0.094|0.053|
|Firms|230|11|70|118|31|



_This table reports summary statistics on the monthly time series of CDS spread changes and CDS liquidity proxies (panel A), as well as put option returns and option liquidity proxies (panel B) for the final sample of firms over the period August 2001 to December 2021. The CDS-bond basis is defined as the difference between the CDS spread and the spread of the underlying bond over the risk-free rate. The option expensiveness is measured as the difference between the implied volatility of the put option and the GARCH(1,1) expected volatility. The bid-ask spreads for both options and CDS are computed as the ratio of the difference between ask and bid quotes to the midpoint of the bid and ask quotes. The statistics are given for the time series of the variables of each portfolio after averaging their values across firms in each month. Each firm is assigned a credit rating based on its average rating across years for which both CDS and option data are available. Firms is the number of firms in each portfolio. The statistics for each rating group exclude months for which observations are not available for at least one of the rating portfolios._ 

320 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

AAA-AA companies to -4.718 basis points for BB-rated and B-rated companies. The standard deviation of CDS spread changes is 12.6 basis points for the whole sample of firms and increases as the credit rating deteriorates. The probability distribution of CDS spread changes is nonnormal as shown by the positive values of skewness and high levels of kurtosis. Similar to CDS spread changes, mean put option returns are negative and range from about -24% for the highest-rated firms to -17% for worst-rated firms. Similar to CDS spread changes, option returns are also positively skewed with positive kurtosis confirming that option returns are highly nonnormal. The average returns’ patterns of put options in our study are in line with the work by Hu and Jacobs (2020), who find a strong positive relationship between average put option returns and underlying volatility. 

Previous papers have shown that OTM put option prices can be affected by liquidity conditions, customer demand and intermediary constraints (G^arleanu et al. 2009; Chen et al. 2019). Similarly, CDS spreads can be affected by illiquidity of the underlying bonds (Chen et al. 2018). These liquidity effects could affect the hedging performance of put options for CDS portfolios. For these reasons, we also compute some liquidity measures for both the CDS and put options used in our sample. In particular, we report summary statistics on the bid-ask spreads (computed as the ratio of the difference between the ask and bid quotes to the midpoint of the bid and ask quotes), the CDS-bond basis (defined as the CDS spread minus the spread of the underlying bond over the risk-free rate)[14 ] and the put option excess implied volatility computed similar to G^arleanu et al. (2009) by taking the difference between the put implied volatility and the GARCH(1,1) expected volatility estimated from 5 years of daily underlying stock returns leading up to the option trading date. Table 2 shows that lower-rated firms have narrower mean CDS bid-ask spreads but a wider CDS-bond basis consistent with Acharya and Johnson (2007) and Bai and Collin-Dufresne (2019), respectively. Put options of lower-rated firms are less liquid than higher-rated firms as shown by higher mean bid-ask spreads and are affected by a more negative net demand as proxied for by the excess implied volatility. These demand patterns are consistent with those described by G^arleanu et al. (2009) and according to which equity options do not appear to be expensive on average like index options. 

## **4. Empirical Analysis** 

This section includes the main empirical results of this paper. We compare the empirical sensitivities of CDS spreads to put option values with the sensitivities implied by the structural models of Merton (1974) and Geske (1979). We also analyze hedging of CDS spread changes with equities. The hedging effectiveness of both empirical as well as model hedge ratios are assessed. Finally, we examine 

> 14 We match the bond yield to the 5-year CDS maturity by interpolating the 5-year maturity whenever sufficient bond data from Refinitiv Eikon is available in a given month for each issuer. We use the 5-year Treasury zero rates as a proxy for the risk-free rate. 

321 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

the incremental role of options over equities and the relationship between informed trading proxies and the hedging error gap between stocks and options. 

**4.1 Contingent claims approach and sensitivities of debt-to-equity options 4.1.1 Empirical sensitivities of credit spreads to put options.** We start by estimating the sensitivity of CDS spreads to changes in the value of the firm by regressing, for each firm _j_ , CDS spread changes (D _CDSj;t_ ) on the returns on options on stocks issued by the firm ( _retoptionj;t_ ). Similar to Schaefer and Strebulaev (2008), our regressions also control for changes in the riskless interest rate by including the change in the 10-year constant maturity Treasury-bond rate (D _rt_[10][). In particular, we estimate the following time-series regression model for ] each firm in our sample: 

**==> picture [247 x 13] intentionally omitted <==**

Panel A of Table 5 reports average estimated coefficients and their _t_ -statistics, which are computed in the same way as in Schaefer and Strebulaev (2008). These _t_ -statistics account for the cross-sectional variation in the time-series regression coefficient estimates and correct for potential correlations between estimates of hedge ratios for different issuers. The estimated coefficients for option returns and the change in the riskless rate are highly significant for the whole sample and for all rating categories. Interestingly, the estimated coefficients for both explanatory variables become larger for lower credit rating categories. These results are economically significant: focusing on the whole sample of firms, a 1% increase in the riskless rate reduces CDS spreads by 12 basis points, whereas a 100% increase in option returns increases CDS spreads by about 5 basis points. The two factors explain approximately 16% of the variation in the spreads, with higher adjusted _R_[2 ] for the lowest-rated firms. The negative correlation between CDS spreads and the risk-free rate is in line with the findings by Ericsson et al. (2009) and Longstaff and Schwartz (1995). 

**4.1.2 Analyzing theoretical hedge ratios.** To study the ability of structural models to provide good predictions of hedge ratios, we estimate the following regression model: 

**==> picture [257 x 13] intentionally omitted <==**

where _hrPjt_ is the theoretical hedge ratio for firm _j_ at time _t_ that we defined in Equation (2). If the combined models of Merton (1974) and Geske (1979) were accurate, a _j;O_ would not be statistically different from one. Before estimating the regression model in Equation (4), a number of parameters have to be estimated for each firm including: the market leverage ( _D=V_ ), the asset volatility (r _V_ ), the timeto-maturity of the debt (s), the time-to-maturity of the put option (s1), the strike price of the option ( _K_ ) and the risk-free rate of interest ( _r_ ). 

322 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

We estimate _D=V_ by taking the ratio of the book value of debt (the sum of Compustat quarterly items for long-term debt and debt in current liabilities)[15 ] to the market value of assets (the product between the number of shares outstanding and the stock price taken from CRSP plus the book value of debt). The Compustat data refer to the most recent quarterly accounting report, whereas the CRSP data are obtained on the observation date. 

As our main objective is to assess the ability of both the Merton (1974) and Geske (1979) models to generate accurate sensitivities of credit spreads to put option values, we need to take special care to avoid that our results are somehow contaminated by the fact that we use these same models to estimate the main inputs required to determine the theoretical hedge ratios. For example, because these sensitivities also depend on the estimated asset volatility, we are careful not to use any of these models for the purpose of generating the asset volatility input. Instead, we follow a model-free approach similar to Schaefer and Strebulaev (2008) that captures debt risk as well as the covariation between equity and debt. Specifically, we compute a firm’s asset volatility from the following formula: 

**==> picture [295 x 27] intentionally omitted <==**

where r _Ej;t_ and r _Dj;t_ represent the time _t_ volatility of firm _j_ ’s equity and debt returns, respectively. r _EDj;t_ is the time _t_ covariance between the returns on firm _j_ ’s debt and equity. 

In our main analysis, we use the option-implied volatility (provided by OptionMetrics) as a proxy for the equity volatility because it has been shown to dominate its historical counterpart in explaining bond yield spreads and CDS spreads (Cremers et al. 2008; Cao et al. 2010). To estimate the debt return volatility, we collect, for each firm, the following bond data from Refinitiv Eikon: dealer quotes, outstanding amounts, coupon and accrued interest. To mitigate the effect of stale prices, we use end-of-month quotes and compute debt returns by value-weighting individual bond returns, where the market values of bonds are determined using bond quoted prices and the face values of bond amounts (Choi 2013; Choi and Richardson 2016).[16 ] We first calculate the time-series volatility of debt returns for each firm if at least 15 monthly observations are available. We then average these volatilities across all firms with the same credit rating, so that the volatility of firm _j_ ’s debt at month _t_ is equal to the average volatility for the rating category of firm _j_ . The covariance between equity and debt returns, r _EDj;t_ , is estimated in a similar way to r _Dj;t_ . 

> 15 We use items 45 and 51 for debt in current liabilities and long-term debt, respectively. 

> 16 We apply the following filtering criteria when collecting bond data: only SEC-registered dollar-denominated and fixedcoupon issues are included; issues with total notional amount less than $10 million are excluded and bonds with optionlike features and floating-rate coupons are also removed. We then calculate individual bond returns between months _t_ -1 and _t_ as follows: _rt_ ¼ _Pt_ þ _PAIt_ − _t_ 1þþ _IAIt_ � _t_ − _C=_ 1 _FR_ − 1 where _Pt_ is the quoted price of each bond at the end of month _t_ , _AIt_ is the accrued interest accumulated in month _t_ , _C_ is the annual coupon rate, and _FR_ is the coupon frequency per year. _It_ is an indicator variable taking the value of one if the coupon is due between _t_ -1 and _t_ , and zero otherwise. 

323 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

We use 5-year as the time-to-maturity of the debt as this is the most liquid segment of the term structure of CDS spreads and the most widely used in previous empirical studies on CDS. The time-to-maturity of the option is either 1 or 2 months depending on the traded option contract selected in a given month. The strike price of the option is that of the put contract selected each month and is needed to estimate _V_[�] , which is a required input in Equation (2). We use historical Treasury zero yields with a time to maturity of 5 years as a proxy for the risk-free rate of interest. 

Table 3 reports estimates of leverage ratios, volatilities and other firm characteristics. Equity volatilities (implied from put options) and asset volatilities increase for lower-rated firms. The relatively higher value of leverage for the A-rated portfolio (relative to BBB firms) reflects the effect of including financial firms in our sample.[17 ] Lower-rated firms have generally lower market capitalization, higher stock turnover and higher book-to-market ratios.[18 ] These patterns are consistent with those shown by Schaefer and Strebulaev (2008) and Bao and Hou (2017). 

Panel A of Table 4 shows summary statistics for estimated hedge ratios based on Equation (2) using option-implied volatility ( _hrP_ ðr _[A] IMP_[Þ][) as an input for the ] estimation of a firm’s asset volatility (computed as from Equation (5)). Hedge ratios increase monotonically as the credit rating declines from about 0.3 basis points for AAA-AA category to 8.6 basis points for the BB-B category. A timeseries plot of these hedge ratios is shown in Figure 1, panel A, for a portfolio including the whole sample of firms. From the plot, it can be observed that hedge ratios increase during periods of market turbulence: for example, they rise to almost 10 basis points around the dot-com bubble and the stock market crash of August 2011; they reach their highest levels (of over 40 basis points) during the financial crisis of 2007–2009 and the COVID-19 outbreak of March 2020. Panel B of Table 4 presents summary statistics for hedge ratios estimated using the optionimplied volatility as a proxy for a firm’s asset volatility: they present the same monotonic pattern but are higher than hedge ratios that are based on Equation (5) across all rating categories. 

**4.1.3 Testing structural models predictions of hedge ratios.** Next, we directly test whether the theoretical hedge ratios of bond credit spreads are consistent with the empirical sensitivities of CDS spreads to equity puts. To this end, we estimate the regression model in Equation (4) for each firm _j_ using the hedge ratio based on our estimate of asset volatility, _hrP_ ¼ _hrP_ ðr _[A] IMP_[Þ][. If the structural ] models of Merton (1974) and Geske (1979) produce accurate predictions of these sensitivities, then the estimated coefficient a _j;O_ should not be statistically different from one. 

> 17 Excluding these financial firms from our sample results in leverage ratios monotonically increasing as the credit rating deteriorates, which is in line with past studies. 

> 18 Book-to-market ratios for each firm are obtained directly from Compustat. 

324 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

## **Table 3** 

## **Summary statistics on firm characteristics** 

||All|AAA-AA|A|BBB|BB-B|
|---|---|---|---|---|---|
|_Leverage_||||||
|Mean|0.342|0.123|0.321|0.302|0.467|
|Standard deviation|0.098|0.021|0.059|0.052|0.136|
|5% quantile|0.256|0.092|0.249|0.241|0.320|
|95% quantile|0.540|0.157|0.460|0.423|0.759|
|_Size_||||||
|Mean|24.586|25.853|24.925|23.781|22.902|
|Standard deviation|0.446|0.335|0.411|0.374|0.618|
|5% quantile|24.044|25.438|24.315|23.142|21.927|
|95% quantile|25.458|26.455|25.653|24.360|23.792|
|_Turnover_||||||
|Mean|0.009|0.004|0.007|0.009|0.017|
|Standard deviation|0.003|0.002|0.003|0.003|0.007|
|5% quantile|0.005|0.002|0.004|0.006|0.007|
|95% quantile|0.015|0.007|0.014|0.014|0.030|
|_Book-to-market_||||||
|Mean|0.546|0.308|0.464|0.579|0.726|
|Standard deviation|0.117|0.104|0.080|0.099|0.358|
|5% quantile|0.425|0.149|0.353|0.454|0.365|
|95% quantile|0.819|0.404|0.638|0.786|1.541|
|r_E_<br>_IMP_||||||
|Mean|0.324|0.223|0.291|0.325|0.456|
|Standard deviation|0.117|0.074|0.111|0.105|0.183|
|5% quantile|0.224|0.153|0.202|0.232|0.297|
|95% quantile|0.557|0.371|0.507|0.516|0.811|
|r_A_<br>_IMP_||||||
|Mean|0.211|0.197|0.195|0.228|0.261|
|Standard deviation|0.065|0.065|0.060|0.060|0.066|
|5% quantile|0.135|0.134|0.143|0.170|0.187|
|95% quantile|0.325|0.314|0.300|0.334|0.375|
|Firms|230|11|70|118|31|



_This table reports the summary statistics on estimates of leverage, size, turnover, book-to-market ratio and volatilities for the final sample of firms over the period August 2001 to December 2021. Leverage is defined as the ratio between the book value of liabilities and the market value of assets. Size is proxied for by the natural logarithm of the firm’s market capitalization. Turnover is the ratio of the stock’s monthly trading volume to the number of shares outstanding. Book-toMarket is the book-to-market ratio._ r _[E] IMP[is the equity volatility implied from the put option as provided from ] OptionMetrics._ r _[A] IMP[is the estimated asset volatility computed using the implied equity volatility (]_[r] _[E] IMP[) as a proxy ] for_ r _Ej;t in Equation (5). We first compute the mean leverage, size, turnover, book-to-market ratio, and volatilities across firms included in a given portfolio in each month, and then provide the statistics for the time series of the variables of each portfolio. Each firm is assigned a credit rating based on its average rating across years for which both CDS and option data are available. Firms is the number of firms in each portfolio. The statistics for each rating group exclude months for which observations are not available for at least one of the rating portfolios._ 

We follow Schaefer and Strebulaev (2008) and use average hedge ratios for each rating class as an estimate of _hrPj;t_ in order to mitigate the noise that may affect the firm-specific estimates of asset volatility. In particular, we start by estimating the theoretical hedge ratios for each firm _j_ from the asset volatility estimate. We then compute, for each month, the hedge ratio averaged across firms 

325 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

**Table 4** 

**Hedge ratios** 

|**Table 4**<br>**Hedge ratios**||||||
|---|---|---|---|---|---|
||All|AAA-AA|A|BBB|BB-B|
|_A. hrP_ ¼_hrP_ðr_A_<br>_IMP_Þ||||||
|Mean|2.940|0.263|1.624|3.162|8.558|
|Standard deviation|5.692|1.338|4.037|5.765|9.195|
|5% quantile|0.133|0.000|0.011|0.095|0.755|
|95% quantile|10.831|1.086|6.735|11.949|25.529|
|_B. hrP_ ¼_hrP_ðr_E_<br>_IMP_Þ||||||
|Mean|12.548|0.689|8.652|12.459|31.196|
|Standard deviation|14.751|2.853|11.788|14.882|26.454|
|5% quantile|2.375|0.000|1.356|1.947|8.330|
|95% quantile|38.674|2.809|33.215|40.401|75.500|
|Firms|230|11|70|118|31|



_This table reports the summary statistics on estimated hedge ratios using the combined models of_ Merton (1974) _and_ Geske (1979) _and computed as in Equation (2). Hedge ratios are estimated assuming two alternative methods to compute asset volatility. In panel A, we use_ r _[A] IMP[as the estimated asset volatility computed using the implied equity ] volatility (_ r _[E] IMP[) as a proxy for ]_[r] _[E] j;t[in ][Equation (5)][. In panel B]_[, ][r] _[A] IMP[is set equal to ]_[r] _[E] IMP[. We first compute the mean ] hedge ratios across firms included in a given portfolio in each month, and then provide the statistics for the time series of each portfolio’s hedge ratios. Each firm is assigned a credit rating based on its average rating across years for which both CDS and option data are available. Firms is the number of firms in each portfolio. Hedge ratios are given in basis points. The statistics for each rating group exclude months for which observations are not available for at least one of the rating portfolios._ 

that are in the same rating portfolio as firm _j_ .[19 ] This average hedge ratio is used for the regression model in Equation (4). 

Panel B of Table 5 provides the results of the hedge ratio regressions. In the case of the whole sample, the mean estimate of a _j;O_ is not statistically different from one (1.02 with _t_ -statistic against unity of 0.24). A more careful examination of the results reveals that the combined structural models of Merton (1974) and Geske (1979) provide accurate predictions of put option sensitivity of CDS spreads for all rating categories. The mean estimate of a _j;O_ varies between 0.94 (for BBB-rated firms) and 1.12 (for BB-B-rated firms). An interesting observation to make relates to the adjusted _R_[2 ] of the regressions. In particular, for the whole sample, they can be up to 5 percentage points higher than the adjusted _R_[2 ] obtained for the empirical sensitivity regressions shown in panel A of the same table. This increase in explanatory power is attributable to hedge ratios of A-rated and BBB-rated firms, and is interesting as it is specific of option sensitivities and less evident when predicting the equity sensitivity using the Merton (1974) model as shown below in Section 4.2 and as already documented for bond returns and bond spread changes by Schaefer and Strebulaev (2008) and Huang and Shi (2021). This difference suggests that nonlinearities play a more significant role when put options are used in place of equities to hedge credit exposures, and capturing these nonlinearities 

> 19 Subrating categories are ignored in our analysis. This means that, for example, both AA- or AAþ would be classed as AA. We treat the remaining subratings in a similar manner. 

326 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

**==> picture [226 x 400] intentionally omitted <==**

**----- Start of picture text -----**<br>
A 50<br>45<br>40<br>35<br>30<br>25<br>20<br>15<br>10<br>5<br>0<br>07/2002 01/2005 07/2007 01/2010 07/2012 01/2015 07/2017 01/2020<br>Date<br>Hedge ratios of credit spreads to put options<br>10 [4]<br>B 8<br>6<br>4<br>2<br>0<br>-2<br>-4<br>-6<br>-8<br>-10<br>07/2002 01/2005 07/2007 01/2010 07/2012 01/2015 07/2017 01/2020<br>Date<br>model hedge ratio (in basis points)<br>hedging error gap (in $ amount)<br>**----- End of picture text -----**<br>


Hedging error gap between stocks and put options 

## **Figure 1** 

## **Time series of hedge ratios and hedging error gap** 

This figure plots average put option hedge ratios (in basis points) for our model and the gap in hedging errors (in U.S. dollars) related to hedging a short position in a portfolio of CDS contracts using either stocks or put options. The top panel shows the time series of average theoretical hedge ratios of credit spreads to put options computed using Equation (2) for the whole sample of 230 firms. The bottom panel displays the time series of the hedging error gap defined as the difference in the absolute values between stock hedging errors and option hedging errors, namely, j _eSt;EMP_ − _eSt;MODEL_ j − j _ePt;EMP_ − _ePt;MODEL_ j. Stock/put hedging errors are computed according to Equation (8) as the absolute value of the difference between the empirical and model hedging errors, namely, j _eSt;EMP_ − _eSt;MODEL_ j for stocks and based on estimated coefficients from monthly rolling regressions using a rolling window of 4 years of monthly data. j _ePt;EMP_ − _ePt;MODEL_ j for puts. Hedging errors are computed in an out-of-sample fashion where empirical hedge ratios are The sample period is from August 2001 to December 2021. 

327 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

**Table 5** 

**Regression of CDS changes on put option returns** 

||All|AAA-AA|A|BBB|BB-B|
|---|---|---|---|---|---|
|_A. Empirical sensitivities_||||||
|Intercept|−0.12|0.14|0.44|0.01|−1.99|
||(−0.68)|(0.91)|(2.47)|(0.05)|(−2.39)|
|_retoption_|5.14|1.30|2.85|5.08|11.90|
||(38.17)|(9.78)|(19.70)|(26.98)|(19.45)|
|D_r_10|−12.16|−4.92|−5.44|−13.26|−25.68|
||(−17.01)|(−8.19)|(−7.42)|(−14.15)|(−7.24)|
|Adj_R_2|.16|.12|.13|.16|.24|
|_B. Hedge ratio regressions_||||||
|Intercept|−0.24|−0.12|0.35|−0.27|−1.51|
||(−1.33)|(−0.78)|(2.02)|(−1.10)|(−1.72)|
|_retoption_|1.02|1.00|1.10|0.94|1.12|
||(0.24)|(−0.00)|(0.50)|(−1.27)|(1.75)|
|D_r_10|−16.67|−5.98|−9.46|−17.86|−32.22|
||(−23.35)|(−10.00)|(−13.12)|(−19.45)|(−8.89)|
|Adj_R_2|.21|.12|.21|.21|.23|
|Nobs|105.43|120.64|119.03|103.80|75.55|



_This table reports the results of regressing CDS spread changes on put option returns and Treasury rate changes during the period August 2001 to December 2021. In panel A, we estimate the following time-series regression for each firm j:_ 

D _CDSj;t_ ¼ a _j_ þ b _j;Oretoptionj;t_ þ b _j;r_ D _rt_[10][þ] _[ �][j][;][t][:]_ 

_In panel B, we estimate the following time-series regression for each firm j:_ 

**==> picture [180 x 11] intentionally omitted <==**

_where hrPs;t is the mean theoretical hedge ratio at time t for all reference entities in rating s and_ r _[A] IMP[is estimated ] according to Equation (5). If the combined models of Merton (1974) and Geske (1979) were accurate_ , a _j;O would not be statistically different from one. The average regression coefficients from the time-series regressions are reported. t- statistics are provided in parentheses and calculated in the same way as in_ Schaefer and Strebulaev (2008).D _rt_[10] _[is the ] change in the 10-year constant maturity U.S. Treasury-bond rate. retoptionj;t is the return on the put option. t-statistics for_ a _j;O are with respect to the difference from unity. All coefficients are in basis points. Nobs is the average of the number of observations per firm in each portfolio._ 

produces an increase in the explanatory power for CDS spread changes. More than for stocks, this pattern also reveals the importance of using appropriate models that are able to capture these nonlinearities. The Geske (1979) model (combined with the Merton model) is able to achieve this by introducing leverage effects that produce a stochastic volatility process for the return on the firm’s stock and, in turn, affect the price of the put option on the stock. 

## **4.2 Hedging credit with stocks** 

Past papers have investigated the ability of the Merton (1974) model to generate accurate sensitivities of corporate bond returns to equity (Schaefer and Strebulaev 2008), corporate bond credit spread changes to equity (Huang and Shi 2021) or CDS spread changes to equity (Che and Kapadia 2012; Huang et al. 2020). We carry out a similar analysis using our sample of CDS firms. We start by defining 

328 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

the model hedge ratios ( _hrS_ ) exploiting the dependence of debt to the firm value _V_ , which is the only stochastic variable in Merton (1974): 

**==> picture [313 x 75] intentionally omitted <==**

where all variables are as previously defined and derivation details can be found in Appendix B. The parameters required to estimate these hedge ratios are the same as those discussed in Section 4.4.1.2. 

Empirical sensitivities of CDS spreads to stock returns are computed using the same approach adopted in Section 4.4.1.1. Panel A of Table 6 reports average coefficient estimates (and their _t_ -statistics) from time-series regressions of CDS spread changes on a constant, stock returns and changes in the riskless interest rate. We find that the coefficients for both stock returns and the riskless rate are highly significant for the whole sample and for each rating category. In particular, for the whole sample, a 1% increase in stock returns decreases CDS spreads by almost 1 basis point. The magnitude of this negative relationship increases as the company rating deteriorates. Similarly, a 1% increase in the risk-free rate produces a reduction in CDS spreads of about 12 basis points and the impact of this effect is greater for lower-rated firms. 

We use Equation (6) to compute the sensitivity of CDS spread changes to changes in the value of a firm’s equity. We then test the accuracy of these sensitivities based on Merton (1974) by running the following regression model: 

**==> picture [266 x 13] intentionally omitted <==**

where _retstockj;t_ and _hrSs;t_ are the stock log-return (in percentage) and the mean theoretical hedge ratio for all firms in rating _s_ at time _t_ , respectively. 

If the Merton (1974) model hedge ratios are accurate, we would expect to estimate a value of a _j;S_ not statistically different from one. 

Panel B of Table 6 shows that the estimated coefficient a _j;S_ is not statistically different from one for the whole sample as well as for each rating group. The alignment between the empirical sensitivities and those based on Merton (1974) is also confirmed by similar adjusted _R_[2 ] values obtained from the regression models in both panels A and B of the table, with the exception of the lowest-rated firms for which empirical regressions show a much higher adjusted _R_[2] . 

Our findings confirm for our sample of firms that the Merton (1974) model is able to generate accurate predictions of the debt-to-equity sensitivity in line with previous studies (Schaefer and Strebulaev 2008; Che and Kapadia 2012; Huang et al. 2020; Huang and Shi 2021). 

329 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

**Table 6** 

**Regression of CDS changes on stock returns** 

||All|AAA-AA|A|BBB|BB-B|
|---|---|---|---|---|---|
|_A. Empirical sensitivities_||||||
|Intercept|−0.63|−0.07|0.08|−0.52|−2.83|
||(−3.79)|(−0.49)|(0.47)|(−2.23)|(−3.75)|
|_retstock_|−0.86|−0.28|−0.54|−0.89|−1.67|
||(−51.65)|(−10.11)|(−25.65)|(−34.97)|(−28.36)|
|D_r_10|−11.63|−5.10|−5.08|−13.69|−20.93|
||(−17.34)|(−8.55)|(−7.14)|(−15.34)|(−6.43)|
|Adj._R_2|.22|.13|.18|.23|.34|
|_B. Hedge ratio regressions_||||||
|Intercept|−0.79|−0.23|−0.10|−0.67|−3.03|
||(−4.56)|(−1.53)|(−0.58)|(−2.79)|(−3.68)|
|_retstock_|1.00|1.47|0.98|0.95|1.08|
||(0.00)|(0.89)|(−0.14)|(−1.01)|(1.41)|
|D_r_10|−16.89|−5.47|−9.08|−19.05|−30.33|
||(−23.96)|(−9.01)|(−12.84)|(−20.76)|(−8.57)|
|Adj._R_2|.21|.11|.21|.21|.25|
|Nobs|105.43|120.64|119.03|103.80|75.55|



_This table reports the results of regressing CDS spread changes on stock returns and Treasury rate changes during the period August 2001 to December 2021. In panel A, we estimate the following time-series regression for each firm j:_ 

D _CDSj;t_ ¼ a _j_ þ b _j;Sretstockj;t_ þ b _j;r_ D _rt_[10][þ] _[ �][j][;][t][:]_ 

_In panel B, we estimate the following time-series regression for each firm j:_ 

**==> picture [176 x 11] intentionally omitted <==**

_where hraccording to Ss;t is the mean theoretical hedge ratio at time t for all reference entities in rating s and Equation (5). If the_ Merton (1974) _model hedge ratios are accurate, we would expect to estimate a value of_ r _[A] IMP[is estimated ]_ a _j;S not statistically different from one. The average regression coefficients from the time-series regressions are reported. t-statistics are provided in parentheses and calculated in the same way as in_ Schaefer and Strebulaev (2008). D _rt_[10] _[is the change in the 10-year constant maturity U.S. Treasury-bond rate. ret][stock] j;t[is the stock log-return ] (in percentage). t-statistics for_ a _j;S are with respect to the difference from unity. All coefficients are in basis points. Nobs is the average of the number of observations per firm in each portfolio._ 

## **4.3 Hedging effectiveness** 

The significant increase in explanatory power for CDS spread changes attributable to the option model hedge ratios and not similarly observed for stock model hedge ratios (as documented from the adjusted _R_[2 ] in Tables 5 and 6) prompts us to investigate further whether the hedging effectiveness of a short position in a portfolio of CDS contracts improves when the replicating portfolio is constructed using the option model hedge ratios rather than the stock model hedge ratios. 

To perform this analysis, we assume that the main aim of a CDS dealer is to minimize the monthly volatility of a hedged short CDS portfolio position including _N_ reference entities. Each of the _N_ contracts is for a notional amount of $10 million and is hedged with d _j;t_ put option contracts. We compute the mean portfolio hedging error ( _et_ ) on each month _t_ as follows: 

**==> picture [285 x 29] intentionally omitted <==**

330 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

where d _j;t_ represents the number of put option contracts on firm _j_ ’s stock that are required to hedge a short position in one CDS contract at time _t_ ,[20 ] _CV_ ð _CDSj;t_ Þ is the mark-to-market value of the CDS contract and D _Poptionj;t_ þ1 is the change in option price (or the difference between the option payoff at maturity and the option price on the trading date if a 1-month contract is selected in a given month). If CDS contracts are hedged using stocks instead of options, in Equation (8) we replace D _Poptionj;t_ þ1 with _retstockj;t_ þ1 (the net stock return on firm _j_ over period _t_ þ1) and d _j;t_ would instead represent the dollar amount of equity of firm _j_ required to hedge a short position in one CDS contract at time _t_ .[21 ] Once the trading positions are opened each month, we do not rebalance them until the next-month expiration date.[22] 

The two main challenges we now face relate to the computation of both _CV_ ð _CDSj;t_ Þ and d _j;t_ . The former requires the use of a CDS pricing model. The latter is complicated by the fact that our theoretical hedge ratios (as well as the empirical hedge ratios) are expressed in basis points. Hence, they cannot directly tell us the number of options or shares of the stock required for hedging a short CDS position. 

We address the first challenge by using the ISDA CDS standard model that can be implemented on Bloomberg’s ”CDSW” function. We use this model to compute the CDS duration ( _D_ ), which we define as the average change in the mark-tomarket value for a plus/minus 1-basis-point change in the CDS spread:[23 ] 

**==> picture [312 x 35] intentionally omitted <==**

According to this pricing model, a change in the value of the CDS contract will depend on the current level of the spread. For each CDS portfolio and each month, we then compute the mark-to-market value of the CDS portfolio by multiplying the average CDS spread by the average duration of the portfolio. 

We use the duration of a CDS contract also to deal with our second challenge. In particular, we compute the total dollar amount to be invested in put options (or of stock shares to be shorted) by multiplying the model (or empirical) hedge ratio (expressed in basis points) by the CDS duration computed as in Equation (9). In 

> 20 Clearly, in case of no hedging, we have that d _j;t_ ¼ 0. 

> 21 The value of d _j;t_ is computed either from empirically observed sensitivities or from the structural models using Equation (2) for options or Equation (6) for stocks. 

> 22 Our choice of a monthly rebalancing frequency is the result of a trade-off between hedging accuracy and trading costs. In particular, Boyer and Vorkink (2014) show that average option bid-ask spreads are wide and are especially so for shortterm OTM options providing investors with substantial skewness. As wide bid-ask spreads would make the hedging strategy overly expensive, we refrain from implementing it using higher rebalancing frequencies. 

> 23 More detailed information on the ISDA pricing model (including documentation and source code) can be found at www.cdsmodel.com. The same model has been previously used in a similar way by Kapadia and Pu (2012), Che and Kapadia (2012), and Huang et al. (2020) to study the Merton (1974) hedge ratios of CDS spreads to equity. 

331 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

the case of puts, we can obtain the total number of put options to buy (d _j;t_ ) by simply dividing this total dollar amount by the put option price.[24] 

We finally examine the magnitude of hedging errors by computing the RMSE as follows: 

**==> picture [199 x 38] intentionally omitted <==**

where _T_ is the number of months for which hedging errors can be computed. 

Table 7 reports the RMSE of the monthly hedging errors for the unhedged case, hedging using theoretical hedge ratios based on stocks (Model-S) and put options (Model-P) and hedging using empirical sensitivities based on stocks (Empirical-S) and put options (Empirical-P). Panel A is based on the whole sample period, whereas panel B produces out-of-sample empirical hedge ratios using timevarying estimated coefficients b _j;O_ from the regression model in Equation (3), where option returns are replaced with stock returns for the case of equity hedging. Time variation in coefficient estimates is obtained by estimating the regression model each month using a rolling window of 4 years of monthly data.[25] 

The first interesting thing to notice is that hedging credit risk with both put options or stocks allows to reduce the RMSE of the CDS portfolio. Second, option model hedge ratios are more effective than equity model hedge ratios at reducing hedging errors: in particular, for the entire portfolio of firms, RMSE values are 19% (14%) lower than the unhedged case if put options (equities) are used for hedging credit exposures. Hence, option-based hedging allows a further 5% reduction in RMSE relative to equity-based hedging. Thirdly, empirical hedge ratios based on either equity or options generally produce a similar reduction in RMSE values of about 25% even though for the lowest rating portfolios, equity-based hedging can reduce RMSE values up to a further 10% relative to option-based hedging. These findings are confirmed for both the in-sample (panel A) and out-ofsample (panel B) analyses. 

Our baseline results rely on short-dated options and longer-term 5-year CDS contracts. One may wonder whether potential longer-term factors affecting CDS spread changes could distort their relationship with put option returns. We investigate this possibility in panel C of Table 7, where we reduce the gap in maturities between CDS contracts and put options by using a sample of longer-dated options. Overall, the results on the hedging effectiveness are consistent with those based on the short-dated options but show a better performance of option model hedge ratios as well as empirical stock hedge ratios, suggesting that nonlinearities of 

> 24 The average duration for our sample of firms is 4,699. The average durations for each rating categories are 4,890, 4781, 4,675 and 4,378 for AAA-AA, A, BBB, and BB-B, respectively. 

> 25 By creating time variation in the empirical hedge ratios, we insure a fair race between the latter and the model hedge ratios that are time-varying by construction. The results in panel A of Table 7 are instead based on fixed empirical hedge ratios that are constant throughout the sample period. 

332 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

**Table 7** 

|**Table 7**|||||
|---|---|---|---|---|
|**Hedging effectiveness**<br>Unhedged<br>_RMSEu_|Model-P<br>_RMSEh_<br>_RMSEh_<br>_RMSEu_ −1|Empirical-P<br>_RMSEh_<br>_RMSEh_<br>_RMSEu_ −1|Model-S<br>_RMSEh_<br>_RMSEh_<br>_RMSEu_ −1|Empirical-S|
|||||_RMSEh_<br>_RMSEh_<br>_RMSEu_ −1|
|_A. In-sample analysis_<br>All<br>57,996<br>47,099<br>−0.19<br>43,775<br>−0.25<br>AAA-AA<br>19,577<br>19,071<br>−0.03<br>18,500<br>−0.06<br>A<br>47,878<br>40,908<br>−0.15<br>37,661<br>−0.21<br>BBB<br>58,449<br>45,215<br>−0.23<br>50,989<br>−0.13<br>BB-B<br>126,723<br>112,132<br>−0.12<br>107,725<br>−0.15<br>_B. Out-of-sample analysis_<br>All<br>59,528<br>46,196<br>−0.22<br>44,850<br>−0.25<br>AAA-AA<br>21,222<br>20,360<br>−0.04<br>20,476<br>−0.04<br>A<br>49,736<br>41,152<br>−0.17<br>36,525<br>−0.27<br>BBB<br>59,709<br>43,908<br>−0.26<br>47,460<br>−0.21<br>BB-B<br>121,555<br>102,601<br>−0.16<br>87,663<br>−0.28<br>_C. Out-of-sample analysis based on long-term options_<br>All<br>59,350<br>45,161<br>−0.24<br>44,532<br>−0.25<br>AAA-AA<br>21,222<br>21,133<br>−0.00<br>21,687<br>0.02<br>A<br>49,614<br>40,189<br>−0.19<br>37,706<br>−0.24<br>BBB<br>59,118<br>44,672<br>−0.24<br>46,574<br>−0.21<br>BB-B<br>120,968<br>100,681<br>−0.17<br>83,809<br>−0.31|||49,731<br>−0.14<br>19,644<br>0.00<br>41,925<br>−0.12<br>48,830<br>−0.16<br>110,952<br>−0.12<br>49,136<br>−0.17<br>20,596<br>−0.03<br>42,136<br>−0.15<br>47,772<br>−0.20<br>103,302<br>−0.15<br>48,717<br>−0.18<br>20,906<br>−0.01<br>42,266<br>−0.15<br>47,155<br>−0.20<br>103,296<br>−0.15|42,996<br>−0.26<br>18,179<br>−0.07<br>38,494<br>−0.20<br>45,068<br>−0.23<br>97,263<br>−0.23<br>44,864<br>−0.25<br>19,868<br>−0.06<br>37,673<br>−0.24<br>46,243<br>−0.23<br>74,839<br>−0.38<br>42,407<br>−0.29<br>19,761<br>−0.07<br>35,059<br>−0.29<br>43,614<br>−0.26<br>84,124<br>−0.30|



_This table reports the root mean square error (RMSE) in U.S. dollars of the hedging error for an equally weighted portfolio of CDS contracts across each rating category and for the whole sample of firms. Each CDS portfolio is hedged dynamically using both equity put options and the equity market. Option hedging is based on empirical hedge ratios (Empirical-P) as from Equation (3) as well as theoretical hedge ratios (Model-P) computed as from Equation (2). Equity hedging is based on empirical hedge ratios (Empirical-S) as from Equation (3), where option returns are replaced by stock returns, as well as theoretical hedge ratios (Model-S) computed as from Equation (6). Positions are rebalanced each month. We also report the RMSE of an unhedged CDS portfolio. Panel A reports RMSE values for the full sample period. Panel B shows results for an out-of-sample analysis where empirical hedge ratios are based on estimated coefficients from monthly rolling regressions using a rolling window of 4 years of monthly data. Panel C performs a similar out-of-sample analysis but using long-term equity put options._ 

option hedging can be better captured by using the models rather than empirical regressions. 

## **4.4 Do options have incremental explanatory power for CDS spread changes?** 

Option valuation models are derived under assumptions that render options redundant securities. However, a number of empirical studies have shown that option trading affects returns and the volatility of the underlying stocks highlighting that options are not merely redundant assets (Conrad 1989; Skinner 1989). Furthermore, the empirical results discussed in previous sections suggest that there might be something unique about the equity option market that makes it particularly suitable to learn about credit risk on top of equity prices. 

To disentangle the incremental information content of options relative to stocks, we estimate the following time-series regression for each firm _j_ : 

**==> picture [237 x 13] intentionally omitted <==**

333 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

where _�j;t_ are the residuals from Equation (7) that are orthogonal to the returns on the issuing firm’s equity, _retoptionj;t_ are the put option returns and _hrPs;t_ are the mean theoretical hedge ratios at time _t_ for all reference entities in rating _s_ . We employ three different specifications of this regression model: one that assumes constant hedge ratios ( _hrPs;t_ ¼ 1); a second specification that captures time variation in hedge ratios ( _hrPs;t_ ¼ _hrPs;t_ ) as defined in Equation (2); and a final specification that uses the option-only component of the theoretical hedge ratios ( _hrPs;t_ ¼ _hrPs;t_ − _@@CSV @@VE_ ~~[)]~~[ as the explanatory variable of the regression model. ] The latter test is made possible because the theoretical hedge ratios we defined in Equations (1) and (2) allow us to isolate the option hedging component from the equity hedging component.[26] 

Panel A of Table 8 shows the estimated coefficients, their corresponding _t_ - statistics and the adjusted _R_ -squared values from the regressions estimated for our sample of firms. We can clearly notice that, for all specifications, the option returns are highly significant and the adjusted _R_[2 ] values suggest that the option market is able to explain up to an additional 5% of the variations in CDS spread changes that the stock market is unable to explain. Furthermore, the option-only component of the theoretical hedge ratios, that is the product between the reciprocal of the put option delta implied by the compound option model of Geske (1979) and the model-based option price, accounts for the entire additional explanatory power (of 2%) of the model hedge ratios.[27 ] To further understand the sources of this additional explanatory power attributable to the option market, we augment the regression model in Equation (11) with the following credit-related and noncredit-related variables as suggested by previous studies (Collin-Dufresne et al. 2001; Schaefer and Strebulaev 2008): the change in the bond market illiquidity measure of Hu et al. (2013) (D _NOISE_ ), the Fama-French Small minus Big ( _SMB_ ) and High Minus Low ( _HML_ ) factors, the change in Moody’s BAA-AAA yield spread (D _DEF_ ), the change in the difference between the 3-month LIBOR rate and the 3-month Treasury-bill rate (D _TED_ ), the change in the difference between the 3-month LIBOR rate and the 3-month overnight index swap rate (D _LIBOR_ − _OIS_ ), the return on the S&P 500 index ( _S_ & _P_ ), the change in the VIX index of implied volatility of options on the S&P 100 index (D _VIX_ ), the change in the slope of the term structure (D _Slope_ ), the change in the difference between the 3-month repo rate and the 3-month Treasury-bill rate (D _REPO_ − _TBILL_ ), the return on an equally weighted stock index of prime dealers 

> 26 The theoretical hedge ratios in Equation (2) can be computed as the product of three partial derivatives ~~(~~ _@@CSV @@VE @@EP_ ~~[)]~~[ after ] inverting Equation () of Appendix A for _V_ ð _P_ Þ and substituting this into Equation (B.2) of Appendix B. As such, they incorporate the first two partial derivatives used to compute the equity hedge ratios (as defined in Equation (6)). Hence, by simply taking the difference between the total hedge ratios from Equation (2) and the product of the first two partial derivatives ~~(~~ _@@CSV @@VE_ ~~[)]~~[, we can retrieve the option-only component of the theoretical hedge ratios (or the reciprocal of the ] stock-option hedge ratio multiplied by the model put price). 

> 27 In unreported results, we also estimated a multivariate model including both stock returns and option returns (together with the change in the riskless rate) to explain CDS spread changes and found that the adjusted _R_ -squared values increase by a few percentage points relative to regression specifications, which separately consider option and stock hedge ratios. These results confirm that options reflect credit-related information that is additional to that contained in equity prices. 

334 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

**Table 8** 

**Regression of unexplained CDS spread changes on option returns** 

_A. Univariate regressions_ 

|||_hrPs;t_|_hrPs;t_|¼1||_hrPs;t_ ¼_hrPs;t_|_hrPs;t_ ¼_hrPs;t_|_hrPs;t_ ¼_hrPs;t_||_hrPs;t_|¼_hrPs;t_ −<br>_@CS_<br>_@V_|¼_hrPs;t_ −<br>_@CS_<br>_@V_|¼_hrPs;t_ −<br>_@CS_<br>_@V_|_@V_<br>_@E_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Intercept||||0.46|||0.24|||||0.28|||
||||(2.70)||||(1.36)|||||(1.59)|||
|_hrP_�_retoption_||||2.75|||0.26|||||0.21|||
||||(22.41)||||(3.75)|||||(4.58)|||
|Adj_R_2||||.05|||.02|||||.02|||
|_B. Multivariate regressions_|||_based on hrPs;t_ ¼_hrPs;t_||||||||||||
|Intercept|0.14|0.21||0.23|0.27|−0.00|0.20|0.66|0.01|0.18|0.23|0.27||0.50|
||(0.80)|(1.23)||(1.33)|(1.59) (−0.01)(1.15)|||(3.85)|(0.06)|(1.01)(1.26)||(1.56)||(2.97)|
|_hrP_�|0.15|0.26||0.26|0.02|0.17|0.17|−0.11|−0.07|0.27|0.29|0.24||−0.20|
|_retoption_|(1.97)|(3.75)||(3.80)|(0.23)|(2.40)|(2.38)|(−1.43)|(−0.88)(3.89)(4.64)|||(3.50)||(−2.50)|
|D_NOISE_|3.48||||||||||||||
||(12.05)||||||||||||||
|_SMB_||−0.15|||||||||||||
|||(−3.04)|||||||||||||
|_HML_||||−0.10|||||||||||
|||||(−1.86)|||||||||||
|D_DEF_|||||22.77|||||||||16.94|
||||||(22.98)|||||||||(16.25)|
|D_TED_||||||14.70|||||||||
|||||||(6.38)|||||||||
|D_LIBOR_−_OIS_|||||||12.01||||||||
||||||||(3.40)||||||||
|_S_&_P_||||||||−1.03||||||−0.55|
|||||||||(−23.74)||||||(−8.40)|
|D_VIX_|||||||||0.67|||||0.15|
||||||||||(19.01)|||||(2.95)|
|D_Slope_||||||||||5.05|||||
|||||||||||(5.20)|||||
|D_REPO_−|||||||||||1.34||||
|_TBILL_|||||||||||(0.53)||||
|_PBI_||||||||||||−0.09|||
|||||||||||||(−4.75)|||
|Adj_R_2|.05|.02||.03|.11|.05|.07|.09|.08|.02|.03|.02||.15|



_Panel A of this table shows the results of regressing the residuals CDS spread changes (obtained from Equation (7)) on option returns during the period August 2001 to December 2021. We estimate the following time-series regression for each firm j:_ 

_�j;t_ ¼ a _j_ þ a _j;OhrPs;t_ ðr _[A] IMP_[Þ] _[ret][option] j;t_[þ] _[ v][j][;][t  ]_ 

_where hrPs;t is the mean theoretical hedge ratio at time t for all reference entities in rating s_ , r _[A] IMP[is estimated according ] to Equation (5) and retoptionj;t is the put option return. Panel B reports results for multivariate regressions, which also consider other possible credit-related and non-credit-related spread determinants including the change in the bond market illiquidity measure of_ Hu et al. (2013) (D _NOISE), the Fama-French Small minus Big (SMB) and High Minus Low (HML) factors, the change in Moody’s BAA-AAA yield spread (_ D _DEF), the change in the difference between the 3- month LIBOR rate and the 3-month Treasury-bill rate (_ D _TED), the change in the difference between the 3-month LIBOR rate and the 3-month overnight index swap rate (_ D _LIBOR_ − _OIS), the return on the S&P 500 index (S&P), the change in the VIX index of implied volatility of options on the S&P 100 index (_ D _VIX), the change in the slope of the term structure (_ D _Slope), the change in the difference between the 3-month repo rate and the 3-month Treasury-bill rate (_ D _REPO_ − _TBILL), and the return on an equally weighted stock index of prime dealers (PBI). The average regression coefficients from the time-series regressions are reported. t-statistics are provided in parentheses and calculated in the same way as in_ Schaefer and Strebulaev (2008). 

335 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

identified by a list compiled by the Federal Reserve Bank of New York ( _PBI_ ). Panel B of Table 8 shows that option returns become insignificant in bivariate regressions when D _DEF_ , _S_ & _P_ , and D _VIX_ are included. When all these variables are added together (as shown in the last column of panel B) in a multivariate regression, they remain significant while the option returns flip the sign.[28 ] We then conclude that considering options in addition to equities when hedging credit risk allows us to learn more about credit risk by capturing additional structural factors that can be used to enhance the risk management of credit exposures. This finding may also provide further evidence that capturing stochastic asset volatility is important consistent with Huang and Huang (2012), Du et al. (2019), and Kita and Tortorice (2021). 

## **4.5 Economic reasoning for the use of options versus stocks** 

As discussed in the introduction, one of the reasons for choosing to hedge credit exposures with options (rather than stocks) relates to the possibility that informed traders may prefer to trade first in the option market if sufficiently liquid (Easley et al. 1998) and depending on the size of noise trading present in this market relative to the equity market (An et al. 2014). In this eventuality, option prices would provide additional information that is not yet reflected in stock prices and may improve hedging effectiveness. To test this prediction, we compute two measures that have been related to informed trading activity in the option market, namely, the volatility spread ( _VSpread_ ) and the volatility smirk or skew ( _VSkew_ ) investigated by Cremers and Weinbaum (2010) and Xing et al. (2010), respectively. We compute these variables following Andreou et al. (2023): in particular, _VSpread_ is computed as the difference in at-the-money (ATM) implied volatilities between a call and a put option with 30 days to maturity and an absolute value of delta equal to 0.50. _VSkew_ is computed as the difference between the implied volatility of a put option with 30 days to maturity and a delta of -0.20 and the ATM implied volatility, where the latter is computed as the average implied volatility of a call and a put option with an absolute value of delta equal to 0.50 and 30 days to maturity. The data used to compute the two measures are based on the Volatility Surface file from OptionMetrics. 

Each month we compute a cross-sectional average of these variables and, from the resultant time series, then use the changes in these variables to predict next month’s hedging error gap between the stock and option market. We define the hedging error gap as the difference in the absolute values between stock hedging errors and option hedging errors, where hedging errors are defined in two alternative ways. First, we compute them as the absolute value of the difference between empirical hedge ratios ( _hrSs;t;EMP_ for stocks and _hrPs;t;EMP_ for puts) and theoretical hedge ratios ( _hrSs;t;MODEL_ for stocks and _hrPs;t;MODEL_ for puts). Second, we compute them as the absolute value of the difference between the empirical 

> 28 We obtain similar results if we replace _hrPs;t_ ¼ _hrPs;t_ with _hrPs;t_ ¼ _hrPs;t_ − _@@CSV @@VE_[in ][Equation (11)][.] 

336 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

and model hedging errors according to Equation (8), namely, j _eSt;EMP_ − _eSt;MODEL_ j for stocks and j _ePt;EMP_ − _ePt;MODEL_ j for puts. Furthermore, the hedging errors are computed in an out-of-sample fashion where empirical hedge ratios are based on estimated coefficients from monthly rolling regressions using a rolling window of 4 years of monthly data. Hence, based on these alternative definitions of hedging errors, the hedging error gap (representing the dependent variable of the timeseries predictive regression) is defined as either j _hrSs;t;EMP_ − _hrSs;t;MODEL_ j − j _hrPs;t;EMP_ 

− _hrPs;t;MODEL_ j or j _eSt;EMP_ − _eSt;MODEL_ j − j _ePt;EMP_ − _ePt;MODEL_ j. 

Figure 1, panel B, shows the time-series pattern of the hedging error gap. While on average the gap is very close to zero (its sample median is only $61), it becomes very negative (of at least $70,000) around the Lehman collapse in October 2008, the stock market crash of August 2011 and the COVID-19 outbreak of March 2020. The highest gap level of almost $73,000 occurs on the month following the COVID-19 outbreak. The time-series regression estimates are reported in Table 9 and show that skew changes predict an increase in hedging errors between stocks and options, regardless of the way hedging errors are computed. For instance, from panel A, a 1% increase in skew increases by about 3 basis points the gap in hedge ratio difference between stocks and options. Similarly, from panel B, a 1% increase in skew increases by almost $2,000 the gap in hedging errors’ difference between stocks and options. Changes in the volatility spread are significant for the full sample of firms at the 10% level if hedging errors are computed as from Equation (8). The predictive power derives from the largest portfolios, namely, the A-rated and BBB-rated firms.[29] 

Next, we repeat the hedging effectiveness analysis implementing market timing strategies based on the changes in informed trading proxies. In particular, we buy (short) puts (stocks) if volatility skew or volatility spread changes in a given month are higher (lower) than their mean change up to that month. Comparing panel B of Table 7 with panels A and C of Table 10 shows that, based on the use of model hedge ratios, the RMSE values of this timing strategy are reduced by a further 4%– 5% relative to a strategy that shorts stocks each month to hedge CDS spread changes regardless of the informed trading environment. The same strategy would generate similar RMSE values to a strategy that buys puts each month to hedge CDS spread changes. If we instead use empirical hedge ratios to implement the same strategies, we would obtain reduced RMSE values of about 3% relative to a strategy that either buys puts or shorts stocks each month of the sample period. 

We also implement an alternative market timing strategy that buys (shorts) puts (stocks) when volatility skew or volatility spread changes in a given month are above (below) their 75th (25th) percentile using information up to that month. Otherwise, for volatility skew or volatility spread changes that lie between the 

> 29 We also estimated a multivariate regression to control for additional factors that could affect the hedging error gap including S&P 500 returns, a change in the default spread, excess implied volatility, and a change in VIX. While no major differences are observed on the predictive power of the volatility spread, unreported results show that the skew change is the most powerful predictor together with the VIX change with significant estimates at the 1% and 5% levels, respectively. 

337 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

## **Table 9** 

**Informed trading and hedging error gap between stocks and options** 

||All|AAA-AA|A|BBB|BB-B|
|---|---|---|---|---|---|
|_A._j_hrSs;t;EMP_ −_hrSs;t;MODEL_j−j_hrPs;t;EMP_ −_hrPs;t;MODEL_j||||||
|D_VSkew_||||||
|Slope|2.71|0.13|2.53|2.64|−1.49|
|_t_-stat|(2.23)|(0.25)|(2.30)|(1.74)|(−3.26)|
|Adj_R_2|.04|−.01|.06|.03|.01|
|D_VSpread_||||||
|Slope|0.19|0.56|3.48|−3.74|−2.52|
|_t_-stat|(0.10)|(0.88)|(1.58)|(−1.64)|(−1.36)|
|Adj._R_2|−.01|−.00|.02|.02|.00|
|_B._j_eSt;EMP_ −_eSt;MODEL_j−j_ePt;EMP_ −_ePt;MODEL_j||||||
|D_VSkew_||||||
|Slope|1,789.19|−94.26|1,255.37|1,916.30|−860.25|
|_t_-stat|(1.88)|(−0.32)|(1.25)|(1.67)|(−1.54)|
|Adj._R_2|.08|−.00|.06|.07|.01|
|D_VSpread_||||||
|Slope|3,034.50|−418.42|2,464.44|640.80|46.91|
|_t_-stat|(1.67)|(−1.21)|(1.60)|(0.63)|(0.05)|
|Adj._R_2|.05|.00|.05|−.00|−.01|



_This table reports estimation results of univariate time-series regressions that use informed trading proxies (observed on option trading dates) to predict the hedging error gap between stocks and put options for an equally weighted portfolio of CDS contracts across each rating category and for the whole sample of firms. We use two main informed trading proxies, namely, the changes in volatility skew (VSkew) and volatility spread (VSpread) computed as in_ Andreou et al. (2023). _In particular, we compute changes in VSkew (_ D _VSkew) and VSpread (_ D _VSpread) as the difference between the value of each informed trading proxy on the current month’s option expiration date and its value on the previous month’s trading date. We use these changes to predict next month’s gap in hedging errors between stocks and put options. Stock/put hedging errors are defined in two alternative ways. First, we compute them as the absolute value of the difference between empirical hedge ratios (hrSs;t;EMP for stocks and hrPs;t;EMP for puts) and theoretical hedge ratios (hrSs;t;MODEL for stocks and hrPs;t;MODEL for puts). Second, we compute them as the absolute value of the difference between the empirical and model hedging errors according to Equation (8), namely_ , j _eSt;EMP_ − _eSt;MODEL_ j _for stocks and stock hedging errors and option hedging errors. We report estimation results using two definitions of the hedging error_ j _ePt;EMP_ − _ePt;MODEL_ j _for puts. The hedging error gap is then defined as the difference in the absolute values between gap, based on our definitions of hedging errors: panel A uses_ j _hrSs;t;EMP_ − _hrSs;t;MODEL_ j − j _hrPs;t;EMP_ − _hrPs;t;MODEL_ j _as the options, empirical hedge ratios are based on dependent variable, while panel B uses_ j _eSt;EMPEquation (3)_ − _eSt;MODEL_ j − _and theoretical hedge ratios are computed according to_ j _ePt;EMP_ − _ePt;MODEL_ j _as the dependent variable. For put Equation (2). For stocks, empirical hedge ratios are based on Equation (3), where option returns are replaced by stock returns, and theoretical hedge ratios are computed as from Equation (6). The hedging errors in the panels are computed in an out-of-sample fashion where empirical hedge ratios are based on estimated coefficients from monthly rolling regressions using a rolling window of 4 years of monthly data. The t-statistics provided in parentheses are based on_ Newey and West (1987) _standard errors with seven lags._ 

percentiles, the CDS portfolio is hedged by investing both in puts and stocks using constant 50% weights. Comparing again panel B of Table 7 with panels B and D of Table 10, in addition to improvements in the performance of empirical hedge ratios, we also obtain slightly better results in model hedging when using skew changes for market timing relative to strategies that either buy puts or short stocks on each month of the sample period. 

While the results in Table 7 are based on 100% investments in either puts or stocks, the last three panels of Table 10 explore combined portfolios of stocks and puts using constant weights in each month of the sample period: we can observe that increasing the option weight in the combined portfolio delivers a reduction in 

338 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

## **Table 10** 

**Hedging effectiveness of portfolios combining stocks and options** 

||All|AAA-AA|A|BBB|BB-B|
|---|---|---|---|---|---|
|Unhedged|59,528|21,222|49,736|59,709|121,555|
|_A. Buy (short) puts_|_(stocks) when_|D_Skew is above (below)_|_mean_|||
|Model|46,282|20,739|40,689|44,107|102,463|
||[−0.22]|[−0.02]|[−0.18]|[−0.26]|[−0.16]|
|Empirical|42,816|20,230|34,634|45,330|83,052|
||[−0.28]|[−0.05]|[−0.30]|[−0.24]|[−0.32]|
|_B. Buy (short) puts_|_(stocks) when_|D_Skew is high (low)_||||
|Model|45,985|20,651|40,548|43,644|102,762|
||[−0.23]|[−0.03]|[−0.18]|[−0.27]|[−0.15]|
|Empirical|42,613|20,000|34,500|45,084|83,504|
||[−0.28]|[−0.06]|[−0.31]|[−0.24]|[−0.31]|
|_C. Buy (short) puts_|_(stocks) when_|D_VSpread is above (below) mean_||||
|Model|46,764|20,629|40,926|44,755|103,391|
||[−0.21]|[−0.03]|[−0.18]|[−0.25]|[−0.15]|
|Empirical|43,016|19,946|34,932|45,305|84,230|
||[−0.28]|[−0.06]|[−0.30]|[−0.24]|[−0.31]|
|_D. Buy (short) puts_|_(stocks) when_|D_VSpread is high (low)_||||
|Model|47,167|20,687|41,054|45,429|102,655|
||[−0.21]|[−0.03]|[−0.17]|[−0.24]|[−0.16]|
|Empirical|42,587|19,889|34,627|44,819|82,082|
||[−0.28]|[−0.06]|[−0.30]|[−0.25]|[−0.32]|
|_E. Constant weights_|_- 75_%_puts, 25_%_stocks_|||||
|Model|46,650|20,331|41,146|44,489|102,108|
||[−0.22]|[−0.04]|[−0.17]|[−0.25]|[−0.16]|
|Empirical|44,308|20,144|36,220|46,592|82,208|
||[−0.26]|[−0.05]|[−0.27]|[−0.22]|[−0.32]|
|_F. Constant weights_|_- 50_%_puts, 50_%_stocks_|||||
|Model|47,297|20,361|41,310|45,338|102,060|
||[−0.21]|[−0.04]|[−0.17]|[−0.24]|[−0.16]|
|Empirical|44,128|19,929|36,313|46,093|78,115|
||[−0.26]|[−0.06]|[−0.27]|[−0.23]|[−0.36]|
|_G. Constant weights - 25_%_puts, 75_%_stocks_||||||
|Model|48,128|20,450|41,641|46,438|102,460|
||[−0.19]|[−0.04]|[−0.16]|[−0.22]|[−0.16]|
|Empirical|44,315|19,837|36,803|45,976|75,606|
||[−0.26]|[−0.07]|[−0.26]|[−0.23]|[−0.38]|



_This table reports the root mean square error (RMSE) in U.S. dollars of the hedging error for an equally weighted portfolio of CDS contracts across each rating category and for the whole sample of firms. Each CDS portfolio is hedged dynamically using a portfolio including both put options and stocks. In addition to creating hedging portfolios that use constant weights for puts and stocks, we also implement market timing strategies based on two informed trading proxies, namely, the changes in volatility skew (VSkew) and volatility spread (VSpread) computed as in_ Andreou et al. (2023). _Option hedging is based on empirical hedge ratios as from Equation (3) as well as model hedge ratios computed as from Equation (2). Equity hedging is based on empirical hedge ratios as from Equation (3), where option returns are replaced by stock returns, as well as model hedge ratios computed as from Equation (6). Panel A reports results for a market timing strategy that buys (shorts) puts (stocks) if skew changes in a given month are above (below) their mean. Panel B reports results for a market timing strategy that buys (shorts) puts (stocks) if skew changes in a given month are above (below) their 75th (25th) percentile. Otherwise, for skew changes that lie between the percentiles, the CDS portfolio is hedged by investing both in puts and stocks using constant 50_ % _weights. Panels C and D also report results for similar market timing strategies that are instead based on VSpread changes. The remaining panels show results for hedging portfolios that invest, each month, in both puts and stocks applying different combinations of constant weights. Positions are rebalanced each month. We also report the root mean square error (RMSE) of an unhedged CDS portfolio. All RMSE values are based on an out-of-sample analysis where empirical hedge ratios are estimated from monthly rolling regressions using a rolling window of 4 years of monthly data. The mean and percentiles of the informed trading proxies used as signals for the market timing strategies are computed each month in a recursive fashion using information up to the trading date. In parentheses, we report the percentage change in the RMSE from an exposure that RMSEh is unhedged (RMSEu) to one that is hedged (RMSEh), namely_ , _RMSEu_[−][1.] 

339 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

RMSE values particularly if model hedge ratios are used. In other words, increasing the stock weight is detrimental to the performance of model hedge ratios. However, we instead observe reductions in RMSE values when adding stocks to the portfolio based on the market timing strategies relying on skew changes: for instance, the strategy used in panel B of Table 10 would use stocks to hedge CDS exposures 72% of the months in the out-of-sample period (using a weight of either 100% or 50%). This finding suggests that the volatility smirk can be used to hedge credit exposures more effectively capturing valuable informed trading information. Also, in line with the predictive regressions results, the largest improvements in hedging effectiveness are observed for the largest portfolios, namely, A-rated and BBB-rated portfolios. 

## **5. Robustness Checks and Further Analyses** 

This section provides a brief description of the robustness checks and additional analyses we performed. The results are discussed in more detail in the Internet Appendix. 

**Additional descriptive statistics** . Our sample of CDS firms is limited by the availability of put option data. In Section 1.1 of the Internet Appendix, we provide summary statistics for an extended sample of CDS firms, which confirm patterns similar to those observed for our final sample of firms matched to option data. We also provide summary statistics for the corporate bond sample, the alternative option samples and informed trading proxies we used in our analysis. 

**Robustness on hedging errors** . In Section 1.2 of the Internet Appendix, we report additional out-of-sample RMSE estimates of hedging credit based on the use of stocks and put options using alternative estimation windows. We confirm our main findings on hedging effectiveness documented in Section 4.4.3 We also provide additional evidence on the relationship between informed trading and the hedging error gap between stocks and options, which become much stronger for the volatility skew when excluding the observations on the Lehman collapse. 

**Other determinants of credit spreads** . In Section 1.3 of the Internet Appendix, we confirm the importance of some additional determinants of credit spreads documented by past papers (Collin-Dufresne et al. 2001; Ericsson et al. 2009). Their addition to our baseline regression model does not affect the role of option returns that remain highly significant. We also study the differential impact that these other determinants of credit spreads have on residual CDS changes, that is, residuals, which are orthogonal to either the returns on the issuing firm’s equity or put option returns. 

**Dealing with noise in calibration and estimation** . We relied on model-free calibration choices for the main parameters of the structural models of Merton (1974) and Geske (1979). To mitigate concerns about noisy hedge ratios due to our 

340 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

“ _ad hoc_ ” modeling choices, we confirm our main findings by estimating the models’ parameters consistently using the maximum likelihood estimation (MLE) adopted by Duan (1994) and Ericsson and Reneby (2005). Furthermore, Broadie et al. (2009) showed that standard statistical tests that involve option returns are noisy. To alleviate this concern and the effect of nonlinearities of option payoffs on our empirical estimates, we use the structural models to simulate monthly CDS spread changes and option returns. We find that the estimates of hedge ratios obtained from regressing simulated CDS spread changes on simulated put returns are in line with those obtained from the regressions based on the original sample of data. We report these additional results in Section 1.4 of the Internet Appendix. 

**Default-loss hedging** . In Section 1.5 of the Internet Appendix, we compare the mark-to-market hedging approach with the more standard and applied default-loss hedging method described in JPMorgan (2006) and based on the theoretical work by Carr and Wu (2011). We show that these two approaches are substantially different as the former aims to neutralize losses in market values of a short position in a CDS contract, while the latter aims to neutralize the loss at default. 

**The costs of hedging** . In Section 1.6 of the Internet Appendix, we analyze hedging costs of three alternative strategies: stock hedging based on the Merton (1974) model hedge ratios, put hedging based on our model hedge ratios combining Merton (1974) and Geske (1979) and put hedging based on JPMorgan (2006). We show that mark-to-market put option hedging based on our model hedge ratios represents the cheapest way of hedging credit exposures. 

**Excluding financial firms** . Our main results are confirmed when we exclude financial firms from our sample of firms as discussed in Section 1.7 of the Internet Appendix. This exclusion can be justified by their peculiar capital structure (Adrian and Shin 2014) and is consistent with previous studies on the hedging performance of structural models (Eom et al. 2004; Huang and Huang 2012; Geske et al. 2016; Schaefer and Strebulaev 2008; Huang et al. 2020; Huang and Shi 2021). 

**Holding-to-maturity returns** . In Section 1.8 of the Internet Appendix, we confirm our main results when we use holding-to-maturity returns (rather than holding period returns) that are typically used by academic studies on options. 

## **6. Conclusion** 

We introduce novel hedge ratios that determine the sensitivities of corporate bond credit spreads to put option values by combining the structural credit risk model of Merton (1974) and the compound option pricing model of Geske (1979). Adopting two alternative calibration approaches, we show that these sensitivities are generally consistent with the empirical sensitivities obtained from regressing CDS spread changes on put option returns. Relative to model-based equity hedge 

341 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

ratios, model-based option hedge ratios decrease portfolio volatility by a further 5% for our sample of firms. We also document the ability of the option market to explain an additional 5% of the variation in the CDS spread changes that is left unexplained by the equity market. The source of this additional explanatory power is linked to the option-only component of the hedge ratios, namely, the reciprocal of the put option delta (or stock-option hedge ratio), which is related to aggregate credit factors, such as the VIX index and the default spread. Overall, our findings suggest that the structural credit risk model of Merton (1974) can be improved in terms of its ability to capture additional credit exposure if option-specific information is combined with equity-specific information. We also show that the choice between equity hedging and option hedging of credit risk exposures can be made effectively based on the changes in the volatility smirk that are shown to predict the gap in hedging errors between stocks and equity options in the time series. 

## **Appendix** 

## **A Deriving Hedge Ratios of Credit Spreads to Equity Options** 

In this section we show how to derive theoretical hedge ratios of corporate bond credit spreads to equity options. First, we define the hedge ratio based on put options, _hrP_ : 

**==> picture [180 x 17] intentionally omitted <==**

where _CS_ and _P_ represent the bond credit spread and the put option price, respectively. _@_ is the partial derivative symbol. 

Merton (1974) and Geske (1979) express corporate debt prices and equity option prices as a function of a firm’s asset value, respectively. 

In particular, Merton (1974) shows that corporate debt of face value _D_ is equal to risk-free debt discounted at the risk-free rate _r_ minus a European put option on the firm’s asset value _V_ with asset returns’ volatility r _V_ . The corporate bond yield spread of maturity s can be expressed as 

**==> picture [239 x 17] intentionally omitted <==**

where U½�� is the univariate cumulative normal distribution function and 

**==> picture [108 x 68] intentionally omitted <==**

Geske (1979) shows that an equity option can be regarded as an option on an option on the firm’s asset value (compound option). For the case of a put option of maturity s1 with strike price _K_ , _P_ would be equal to the following expression: 

**==> picture [314 x 32] intentionally omitted <==**

342 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

where H½�� is the bivariate cumulative normal distribution function and 

**==> picture [116 x 44] intentionally omitted <==**

_V_ � is the value of _V_ , where the option is just at the money at time s1 and is the solution to the following equation: 

**==> picture [210 x 14] intentionally omitted <==**

Given the dependence of both the credit spread and the put option price on the firm’s asset value _V_ , we can now rewrite Equation (A.1) as a function of two partial derivatives: 

**==> picture [209 x 21] intentionally omitted <==**

We first derive the first partial derivative of the credit spread with respect to _V_ . This gives: 

**==> picture [270 x 39] intentionally omitted <==**

where /½�� is the univariate normal density function. Next, we compute the second partial derivative and obtain the following: 

**==> picture [256 x 20] intentionally omitted <==**

We can now group the solutions to the two partial derivatives as from Equations (A.5) and (A.6) to compute the final hedge ratio: 

**==> picture [272 x 65] intentionally omitted <==**

## **B Deriving Hedge Ratios of Credit Spreads to Equity** 

In this section we show how to derive theoretical hedge ratios of corporate bond credit spreads to equity. The hedge ratio based on stocks, _hrS_ , is given by the following expression: 

**==> picture [180 x 18] intentionally omitted <==**

where _CS_ and _E_ represent the bond credit spread and the stock price, respectively. Under Merton (1974), the equity value of a firm is a European call option on the asset value _V_ : 

**==> picture [228 x 10] intentionally omitted <==**

343 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

We can exploit the equity’s dependence on _V_ and write Equation (B.1) as a function of two partial derivatives: 

**==> picture [209 x 20] intentionally omitted <==**

The solution to the partial derivative of the credit spread with respect to _V_ is given in Equation (A.5) of Appendix A. 

We compute the partial derivative of the firm’s equity with respect to _V_ and obtain the following: 

**==> picture [192 x 18] intentionally omitted <==**

Combining Equations (A.5) and (B.4), we obtain the following final hedge ratio: 

**==> picture [301 x 39] intentionally omitted <==**

## **References** 

Acharya, V. V., S. T. Bharath, and A. Srinivasan. 2007. Does industry-wide distress affect defaulted firms? Evidence from creditor recoveries. _Journal of Financial Economics_ 85:787–821. 

Acharya, V. V. and T. C. Johnson. 2007. Insider trading in credit derivatives. _Journal of Financial Economics_ 84:110–41. 

Adrian, T. and H. S. Shin. 2014. Procyclical leverage and value-at-risk. _Review of Financial Studies_ 27:373–403. 

Altman, E. I., B. Brady, A. Resti, and A. Sironi. 2005. The link between default and recovery rates: Theory, empirical evidence, and implications. _Journal of Business_ 78:2203–28. 

An, B., A. Ang, T. G. Bali, and N. Cakici. 2014. The joint cross section of stocks and options. _Journal of Finance_ 69:2279–337. 

Anderson, R. W. and S. Sundaresan. 1996. Design and valuation of debt contracts. _Review of Financial Studies_ 9:37–68. 

Andreou, P. C., T. G. Bali, A. Kagkadis, and N. Lambertides. 2023. Firm growth potential and option returns. _Georgetown University_ . 

Back, K.. 1993. Asymmetric information and options. _Review of Financial Studies_ 6:435–72. 

Bai, J. and P. Collin-Dufresne. 2019. The CDS-bond basis. _Financial Management_ 48:417–39. 

Bali, T. G. and A. Hovakimian. 2009. Volatility spreads and expected stock returns. _Management Science_ 55:1797–812. 

Bao, J. and K. Hou. 2017. De facto seniority, credit risk, and corporate bond prices. _Review of Financial Studies_ 30:4038–80. 

Barraclough, K. and R. E. Whaley. 2012. Early exercise of put options on stocks. _Journal of Finance_ 67:1423–56. 

Berndt, A. and A. Ostrovnaya. 2014. Do equity markets favor credit market news over options market news? _Quarterly Journal of Finance_ 4:1450006. 

Bhamra, H. S., L.-A. Kuehn, and I. A. Strebulaev. 2010. The levered equity risk premium and credit spreads: A unified framework. _Review of Financial Studies_ 23:645–703. 

Black, F.. 1975. Fact and fantasy in the use of options. _Financial Analysts Journal_ 31:36–41. 

Black, F. and M. Scholes. 1973. The pricing of options and corporate liabilities. _Journal of Political Economy_ 81:637–59. 

Boyer, B. H. and K. Vorkink. 2014. Stock options as lotteries. _Journal of Finance_ 69:1485–527. 

344 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

Broadie, M., M. Chernov, and M. Johannes. 2007. Model specification and risk premia: Evidence from futures options. _Journal of Finance_ 62:1453–90. 

——— 2009. Understanding index option returns. _Review of Financial Studies_ 22:4493–529. 

Campbell, J. T. and G. B. Taksler. 2003. Equity volatility and corporate bond yields. _Journal of Finance_ 58:2321–49. 

Cao, C., Z. Chen, and J. Griffin. 2005. Informational content of option volume prior to takeovers. _Journal of Business_ 78:1073–109. 

Cao, C., F. Yu, and Z. Zhong. 2010. The information content of option-implied volatility for credit default swap valuation. _Journal of Financial Markets_ 13:321–43. 

——— 2011. Pricing credit default swaps with option-implied volatility. _Financial Analysts Journal_ 67:67–76. 

Carr, P. and L. Wu. 2010. Stock options and credit default swaps: A joint framework for valuation and estimation. _Journal of Financial Econometrics_ 8:409–49. 

——— 2011. A simple robust link between American puts and credit protection. _Review of Financial Studies_ 24:473–505. 

Che, X. and N. Kapadia. 2012. Can credit risk be hedged in equity markets? _University of Massachusetts_ . 

Chen, H.. 2010. Macroeconomic conditions and the puzzles of credit spreads and capital structure. _Journal of Finance_ 65:2171–212. 

Chen, H., R. Cui, Z. He, and K. Milbradt. 2018. Quantifying liquidity and default risks of corporate bonds over the business cycle. _Review of Financial Studies_ 31:852–97. 

Chen, H., S. Joslin, and S. X. Ni. 2019. Demand for crash insurance, intermediary constraints, and risk premia in financial markets. _Review of Financial Studies_ 32:228–65. 

Chen, L., P. Collin-Dufresne, and R. Goldstein. 2009. On the relation between the credit spread puzzle and the equity premium puzzle. _Review of Financial Studies_ 22:3367–409. 

Choi, J.. 2013. What drives the value premium?: The role of asset risk and leverage. _Review of Financial Studies_ 26:2845–75. 

Choi, J. and M. Richardson. 2016. The volatility of a firm’s assets and the leverage effect. _Journal of Financial Economics_ 121:254–77. 

Collin-Dufresne, P., V. Fos, and D. Muravyev. 2021. Informed trading in the stock market and option-price discovery. _Journal of Financial and Quantitative Analysis_ 56:1945–84. 

Collin-Dufresne, P. and R. Goldstein. 2001. Do credit spreads reflect stationary leverage ratios? _Journal of Finance_ 56:1929–57. 

Collin-Dufresne, P., R. S. Goldstein, and S. J. Martin. 2001. The determinants of credit spread changes. _Journal of Finance_ 56:2177–207. 

Collin-Dufresne, P., R. S. Goldstein, and F. Yang. 2012. On the relative pricing of long-maturity index options and collateralized debt obligations. _Journal of Finance_ 67:1983–2014. 

Conrad, J.. 1989. The price effect of option introduction. _Journal of Finance_ 44:487–98. 

Cremers, M., J. Driessen, and P. Maenhout. 2008. Explaining the level of credit spreads: Option-implied jump risk premia in a firm value model. _Review of Financial Studies_ 21:2209–42. 

Cremers, M., J. Driessen, P. Maenhout, and D. Weinbaum. 2008. Individual stock-option prices and credit spreads. _Journal of Banking and Finance_ 32:2706–15. 

Cremers, M. and D. Weinbaum. 2010. Deviations from put-call parity and stock return predictability. _Journal of Financial and Quantitative Analysis_ 45:335–67. 

Culp, C. L., Y. Nozawa, and P. Veronesi. 2018. Option-based credit spreads. _American Economic Review_ 108:454–88. 

345 

_Review of Asset Pricing Studies / v 14 n 2 2024_ 

Das, S. R. and P. Hanouna. 2009. Hedging credit: Equity liquidity matters. _Journal of Financial Intermediation_ 18:112–23. 

Du, D., R. Elkamhi, and J. Ericsson. 2019. Time-varying asset volatility and the credit spread puzzle. _Journal of Finance_ 74:1841–85. 

Duan, J.-C.. 1994. Maximum likelihood estimation using price data of the derivative contract. _Mathematical Finance_ 4:155–67. 

Duarte, J., F. Longstaff, and F. Yu. 2007. Risk and return in fixed-income arbitrage: Nickels in front of a steamroller? _Review of Financial Studies_ 20:769–811. 

Easley, D., M. O’Hara, and P. Srinivas. 1998. Option volume and stock prices: Evidence on where informed traders trade. _Journal of Finance_ 53:431–65. 

Elton, E. J., M. J. Gruber, D. Agrawal, and C. Mann. 2001. Explaining the rate spread on corporate bonds. _Journal of Finance_ 56:247–77. 

Eom, Y. H., J. Helwege, and J. Z. Huang. 2004. Structural models of corporate bond pricing: An empirical analysis. _Review of Financial Studies_ 17:499–544. 

Ericsson, J., K. Jacobs, and R. Oviedo. 2009. The determinants of credit default swap premia. _Journal of Financial and Quantitative Analysis_ 44:109–32. 

Ericsson, J. and J. Reneby. 2005. Estimating structural bond pricing models. _Journal of Business_ 78:707–35. 

G^arleanu, N., L. H. Pedersen, and A. M. Poteshman. 2009. Demand-based option pricing. _Review of Financial Studies_ 22:4259–99. 

Geske, R.. 1979. The valuation of compound options. _Journal of Financial Economics_ 7:63–81. 

Geske, R., A. Subrahmanyam, and Y. Zhou. 2016. Capital structure effects on the prices of equity call options. _Journal of Financial Economics_ 121:231–53. 

Goyal, A. and A. Saretto. 2009. Cross-section of option returns and volatility. _Journal of Financial Economics_ 94:310–26. 

Hu, G. and K. Jacobs. 2020. Volatility and expected option returns. _Journal of Financial and Quantitative Analysis_ 55:1025–60. 

Hu, G. X., J. Pan, and J. Wang. 2013. Noise as information for illiquidity. _Journal of Finance_ 68:2341–82. 

Huang, J.-Z. and M. Huang. 2012. How much of the corporate-treasury yield spread is due to credit risk? _Review of Asset Pricing Studies_ 2:153–202. 

Huang, J.-Z. and Z. Shi. 2021. What do we know about corporate bond returns? _Annual Review of Financial Economics_ 13:363–99. 

Huang, J.-Z., Z. Shi, and H. Zhou. 2020. Specification analysis of structural credit risk models. _Review of Finance_ 24:45–98. 

Johnson, T. L. and E. C. So. 2012. The option to stock volume ratio and future returns. _Journal of Financial Economics_ 106:262–86. 

Jones, E. P., S. P. Mason, and E. Rosenfeld. 1984. Contingent claims analysis of corporate capital structures: An empirical investigation. _Journal of Finance_ 39:611–27. 

JPMorgan. 2006. Credit derivatives handbook. _Corporate Quantitative Research_ . 

Kapadia, N. and X. Pu. 2012. Limited arbitrage between equity and credit markets. _Journal of Financial Economics_ 105:542–64. 

Kelly, B., G. Manzo, and D. Palhares. 2016. Credit-implied volatility. _University of Chicago_ . 

Kita, A. and D. L. Tortorice. 2021. Same firm, two volatilities: How variance risk is priced in credit and equity markets. _Journal of Corporate Finance_ 69:101885. 

346 

_Contingent Claims and Hedging of Credit Risk with Equity Options_ 

Kuehn, L., D. Schreindorfer, and F. Schulz. 2017. Credit and option risk premia. _Carnegie Mellon University_ . 

Leland, H. E. and K. B. Toft. 1996. Optimal capital structure, endogenous bankruptcy and the term structure of credit spreads. _Journal of Finance_ 51:987–1019. 

Longstaff, F. A., S. Mithal, and E. Neis. 2005. Corporate yield spreads: Default risk or liquidity? New evidence from the credit default swap market. _Journal of Finance_ 60:2213–53. 

Longstaff, F. A. and E. S. Schwartz. 1995. A simple approach to valuing risky fixed and floating rate debt. _Journal of Finance_ 50:789–819. 

Mella-Barral, P. and W. Perraudin. 1997. Strategic debt service. _Journal of Finance_ 52:531–56. 

Merton, R. C.. 1973. Theory of rational option pricing. _Bell Journal of Economics and Management Science_ 4:141–83. 

———1974. On the pricing of corporate debt: The risk structure of interest rates. _Journal of Finance_ 29:449–70. 

Modigliani, F. and M. Miller. 1958. The cost of capital, corporate finance and the theory of investment. _American Economic Review_ 48:267–97. 

Muravyev, D., N. D. Pearson, and J. P. Broussard. 2013. Is there price discovery in equity options? _Journal of Financial Economics_ 107:259–83. 

Newey, W. K. and K. D. West. 1987. A simple positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix estimator. _Econometrica_ 55:703–08. 

Ni, S. X., N. Pearson, and A. Poteshman. 2005. Stock price clustering on option expiration dates. _Journal of Financial Economics_ 78:49–87. 

Ofek, E., M. Richardson, and R. F. Whitelaw. 2004. Limited arbitrage and short sale constraints: Evidence from the option markets. _Journal of Financial Economics_ 74:305–42. 

Pan, J. and A. Poteshman. 2006. The information in option volume for future stock prices. _Review of Financial Studies_ 19:871–908. 

Reindl, J., N. Stoughton, and J. Zechner. 2017. Market implied costs of bankruptcy. _BI Norwegian Business School_ . 

Ross, S. A.. 1976. Options and efficiency. _Quarterly Journal of Economics_ 90:75–89. 

Schaefer, S. M. and I. A. Strebulaev. 2008. Structural models of credit risk are useful: Evidence from hedge ratios on corporate bonds. _Journal of Financial Economics_ 90:1–19. 

Seo, S. B. and J. A. Wachter. 2018. Do rare events explain CDX tranche spreads? _Journal of Finance_ 73:2343–83. 

Skinner, D. J.. 1989. Options market and stock return volatility. _Journal of Financial Economics_ 23:61–78. 

Stilger, P. S., A. Kostakis, and S.-H. Poon. 2017. What does risk-neutral skewness tell us about future stock returns? _Management Science_ 63:1814–34. 

Stulz, R. M.. 2010. Credit default swaps and the credit crisis. _Journal of Economic Perspectives_ 24:73–92. 

Trolle, A. B. and E. S. Schwartz. 2009. Unspanned stochastic volatility and the pricing of commodity derivatives. _Review of Financial Studies_ 22:4423–61. 

Xing, Y., X. Zhang, and R. Zhao. 2010. What does the individual option volatility smirk tell us about future equity returns? _Journal of Financial and Quantitative Analysis_ 45:641–62. 

Yu, F.. 2006. How profitable is capital structure arbitrage? _Financial Analysts Journal_ 62:47–62. 

Zhang, B. Y., H. Zhou, and H. Zhu. 2009. Explaining credit default swap spreads with the equity volatility and jump risks of individual firms. _Review of Financial Studies_ 22:5099–131. 

Zhou, C.. 2001. The term structure of credit spreads with jump risk. _Journal of Banking and Finance_ 25:2015–40. 

347 

# The Author(s) 2024. Published by Oxford University Press on behalf of The Society for Financial Studies. This is an Open Access article distributed under the terms of the Creative Commons Attribution License (https:// creativecommons.org/licenses/by/4.0/), which permits unrestricted reuse, distribution, and reproduction in any medium, provided the original work is properly cited. Review of Asset Pricing Studies, 2024, 14, 310–347 https://doi.org/10.1093/rapstu/raae005 Article 


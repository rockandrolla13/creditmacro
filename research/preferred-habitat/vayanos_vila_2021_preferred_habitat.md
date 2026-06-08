_Submitted to Econometrica_ 

## A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES[1] 

## Dimitri Vayanos and Jean-Luc Vila 

We model the term structure of interest rates that results from the interaction between investors with preferences for specific maturities and risk-averse arbitrageurs. Shocks to the short rate are transmitted to long rates through arbitrageurs’ carry trades. Arbitrageurs earn rents from transmitting the shocks, through bond risk premia that relate positively to the slope of the term structure. When the short rate is the only risk factor, changes in investor demand have the same relative effect on interest rates across maturities regardless of the maturities where they originate. When investor demand is also stochastic, demand effects become more localized. A calibration indicates that long rates under-react to forward-guidance announcements about short rates. Large-scale asset purchases can be more effective in moving long rates, especially if they are concentrated at long maturities. 

Keywords: Interest rates, bond risk premia, limited arbitrage, government debt, monetary policy. 

## 1. INTRODUCTION 

What determines the term structure of interest rates? In most macro-finance models, the interest rate for a given maturity depends on the willingness of a representative agent to substitute consumption from today towards that maturity. The consumption-based view of the term structure contrasts with a more informal preferred-habitat view, which has been proposed by Culbertson (1957) and Modigliani and Sutch (1966), and is popular within central banks and the financial industry. According to that view, there are investor clienteles for specific maturity segments, and the interest rate for a given maturity is mainly driven by shocks affecting 

Department of Finance, London School of Economics, Houghton Street, London WC2A 2AE, United Kingdom, CEPR and NBER. `d.vayanos@lse.ac.uk` 

> Capula Investment Management, 7 Clarges Street, London W1J 8AE, United Kingdom. `JVila@capulaglobal.com` 

> 1We thank Ravi Bansal, Markus Brunnermeier, Andrea Buraschi, Stefania D’Amico, Greg Duffee, Pierre Collin-Dufresne, Peter DeMarzo, Michael Fleming, Giorgio Fossi, Xavier Gabaix, Ken Garbade, Robin Greenwood, Sam Hanson, Moyeen Islam, Mike Joyce, Thomas King, Ralph Koijen, Arvind Krishnamurthy, Jun Liu, Vasant Naik, Anna Pavlova, Monika Piazzesi, Ricardo Reis, Ishita Sen, Jeremy Stein, Michael Woodford, seminar participants at the Bank of England, Chicago Fed, ECB, Fed Board, LSE, Manchester, New York Fed, Tilburg, Toulouse and UCLA, and participants at the American Finance Association, Adam Smith Asset Pricing, Brazilian Finance Association, Chicago, CRETE, Gerzensee, Imperial, NBER Asset Pricing, SITE and York conferences, for helpful comments. We are especially grateful to John Cochrane and four anonymous referees for extensive and valuable comments. We thank Noah Schmeiders, Ran Shi and Jingtong Zhang for research assistance, and the LSE Paul Woolley Centre for financial support. The views expressed in this paper are those of the authors and not of Capula Investment Management. Please address correspondence to Dimitri Vayanos, `d.vayanos@lse.ac.uk` . 

1 

2 

D. VAYANOS AND J.-L. VILA 

the demand of the corresponding clientele. The term structure thus exhibits a degree of segmentation. 

The preferred-habitat view has been used to interpret numerous market episodes. The 2004 U.K. pension reform is one example. The reform required pension funds to evaluate their pension liabilities using the yields of long-maturity bonds. To hedge against drops in long rates, which would raise the value of pension liabilities and trigger regulatory scrutiny, pension funds bought long-maturity bonds in large quantities. This drove long rates to record low levels. A flat term structure in early 2004 became downward-sloping in subsequent years, with the 30-year bond yielding as much as 0.80% (80 basis points, bps) below its 10-year counterpart.[1] More recently, the preferred-habitat view informed decisions by major central banks to engage in Quantitative Easing (QE). A stated goal of QE programmes was that large-scale purchases of long-maturity bonds would drive long rates down, stimulating corporate investment.[2] 

The preferred-habitat view cannot be correct in its most extreme form, namely, the interest rate for a given maturity cannot be driven _only_ by shocks affecting the demand of the corresponding clientele. Indeed, if that were the case, interest rates for nearby maturities could be very different, generating large profits for termstructure arbitrageurs. At the same time, shocks to clientele demands can affect interest rates. Indeed, because absorbing the shocks exposes arbitrageurs to interest-rate risk, bond prices must change to compensate them for the risk. 

How do shocks to clientele demands affect the term structure? What are the effects of large-scale bond purchases by central banks? What are the implications of the preferred-habitat view for the dynamics of interest rates, for bond risk premia, and for the transmission of monetary policy from short to long rates? In this paper we develop a model to answer these questions both qualitatively as well as quantitatively through a calibration exercise. Our model formalizes the preferred-habitat view and embeds it into a modern no-arbitrage term-structure framework. We describe our model in Section 2. The short rate follows an exogenous mean-reverting process. An exogenous short rate can be interpreted as the return of a linear and instantaneously riskless production technology, or as the instantaneous rate that a (non-modelled) central bank pays on reserves. Bond yields are determined endogenously through trading between preferred-habitat investors and arbitrageurs. Preferredhabitat investors demand zero-coupon bonds with specific maturities, and their demand can be price-elastic. 

> 1For accounts of the 2004 U.K. pension reform and other related episodes, see Tzucker and Islam (2005), Garbade and Rutherford (2007), Islam (2007), and Greenwood and Vayanos (2010). 

> 2See, for example, the 2011 speeches on large-scale asset purchases by Janet Yellen, the then Vice-Chair of the U.S. Federal Reserve (Yellen (2011)), and John Williams, the then President of the San Francisco Fed (Wiliams (2011)). 

3 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

We provide an optimizing foundation for that demand in a setting where investors form overlapping generations consuming at the end of their life, are infinitely risk averse, and can invest in bonds and in a private opportunity with exogenous return (e.g., real estate). Arbitrageurs are competitive and maximize a meanvariance objective over instantaneous changes in wealth. We fix their aggregate risk aversion and do not study entry into the arbitrage business. 

In Section 3 we solve for equilibrium when the demand of preferred-habitat investors is constant over time and the only risk factor is the short rate. We address three main questions: how shocks to the short rate are transmitted to long rates, how bond risk premia depend on the shape of the term structure, and how changes in preferred-habitat demand affect the term structure. Since demand is constant over time, we take demand changes to be unanticipated and permanent. 

Shocks to the short rate are transmitted to bond yields through the trades of arbitrageurs. Suppose that the short rate drops. Since investing in bonds becomes more attractive than investing in the short rate, arbitrageurs buy bonds by borrowing short-term. That trade causes bond prices to rise and yields to drop. Because, however, arbitrageurs become exposed to the risk that the short rate will increase, they do not scale up their trade to the point where it earns zero expected profit. Hence, the drop in bond yields does not fully reflect the drop in the short rate, which means that forward rates under-react to expected future short rates. The under-reaction disappears when arbitrageurs are risk-neutral, or when preferred-habitat demand is price-inelastic since in that case arbitrageurs cause bond prices to rise without actually buying the bonds. 

Bond risk premia (expected returns in excess of the short rate) are positively related to the slope of the term structure, consistent with the empirical findings of Fama and Bliss (FB 1987) and Campbell and Shiller (CS 1991). When the short rate is low, the term structure slopes up, and bonds earn positive risk premia so that arbitrageurs are induced to buy them. The risk premia accrue to arbitrageurs as a rent for transmitting short-rate shocks to long rates. Monetary-policy actions by central banks affecting the short rate can hence be viewed as a source of arbitrageur rent.[3] That rent is higher when arbitrageurs are more risk-averse and when preferred-habitat demand is more price-elastic. 

When the short rate is the only risk factor, changes in preferred-habitat demand have global effects: the effects depend on how the arbitrageurs’ overall exposure to the short rate (“duration risk”) changes, and not on the specific maturities where the demand changes originate. To illustrate this result’s surprising implications, suppose that the demand for short-maturity bonds increases and the demand for long-maturity 

> 3We thank John Cochrane for suggesting this idea (Cochrane (2008)). 

4 

D. VAYANOS AND J.-L. VILA 

bonds decreases by the same amount in present-value terms. Since arbitrageurs buy long-maturity bonds, and these are more sensitive to short-rate changes than short-maturity bonds, all yields rise—including those of short-maturity bonds for which demand _increases_ . The same logic implies that all demand changes have the same relative effect across maturities regardless of where they originate. Moreover, the effect is largest at the longest maturity. Indeed, since the longest-maturity bonds are the most sensitive to short-rate changes, their risk premia are also the most sensitive to changes in the arbitrageurs’ exposure to the short rate. In Section 4 we allow the demand of preferred-habitat investors to vary over time. We maintain a stochastic short rate; with a constant short rate, arbitrageur activity would render all yields equal to the short rate. We mainly focus on the case where demand has a one-factor structure and that factor is independent of the short rate, but we also consider multiple demand factors and correlation. Within the two-factor model, we revisit the same three questions as in Section 3. 

Demand risk weakens and can even reverse the transmission of short-rate shocks to long rates. Suppose that the short rate drops, in which case arbitrageurs buy bonds. Arbitrageurs become exposed to the risk that the short rate will increase _and_ that preferred-habitat demand will decrease. Because demand risk becomes dominant for long-maturity bonds, arbitrageurs buy them in small quantities and may even sell them short to hedge the demand risk of their long positions in intermediate maturities. Long-maturity yields may thus _rise_ in response to a short-rate drop. 

Demand risk strengthens the positive relationship between bond risk premia and term-structure slope. Indeed, when preferred-habitat demand is low, risk premia are high so that arbitrageurs are induced to buy bonds to make up for the low demand. Because of the high premia, bond yields are high and the term structure slopes up. As a result of the stronger premia-slope relationship, the model-generated coefficients in the FB and CS regressions have properties closer to their empirical counterparts. For example, the FB coefficient can be larger than one and increasing with maturity, rather than only positive and constant as in the one-factor model. 

With multiple risk factors, demand effects become more localized. Changes in the demand for short- (long-) maturity bonds have more pronounced effects on short- (long-) maturity yields. As in the one-factor model, the effects arise through the arbitrageurs’ exposure to the risk factors. They become more localized because demand changes originating at different maturities affect the exposure to each factor differently, and because changes in each factor exposure have a different relative effect across maturities. 

In Section 5 we calibrate the two-factor model and analyze central-bank policies such as forward guidance 

5 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

and QE. We choose the model parameters to match the volatility of U.S. government bond yields and yield changes, the correlation between yield changes at the short and the long end of the term structure, and the composition of bond trading volume across maturities. Since the model can be given both a nominal and a real interpretation, we calibrate it using nominal yields and then again using real yields. The nominal and real calibrations generate remarkably similar results. 

Forward guidance about short rates is effective in moving yields of short-maturity bonds, but becomes less effective for long maturities. Lowering the average expected short rate over the next ten years by 100 bps (and holding preferred-habitat demand constant) causes the ten-year yield to drop by 35-50 bps. The same change to the expected short rate over thirty years has almost no effect on the thirty-year yield. QE can be more effective in changing long rates, provided that bond purchases are concentrated at long maturities. Purchases amounting to 12% of GDP and conforming to the maturity distribution used by the Fed during QE1 lower the ten-year yield by 25-30bps and the thirty-year yield by 30-35bps. Tilting purchases towards long maturities, while keeping the fraction of available supply purchased in each maturity bucket within observed ceilings, increases the effects by 10 and 30bps, respectively. 

Our model formalizes the preferred-habitat theory of the term structure, proposed by Culbertson (1957) and Modigliani and Sutch (1966). Related to preferred habitat is Tobin’s (1958,1969) portfolio-balance theory, in which financial assets are imperfect substitutes, and investors require a rise in interest rates to absorb an increased supply of government bonds. The portfolio-balance channel is present in our model, with Tobin’s investors being our arbitrageurs. It is the only channel present in the special case of our model where preferredhabitat demand is price-inelastic. 

Andres, Lopez-Salido, and Nelson (2004) study demand effects and the portfolio-balance channel in a calibrated macroeconomic model with trading frictions. Greenwood and Vayanos (2014) use our model’s special case with a price-inelastic demand to test for a positive relationship between the maturity of government debt and future bond returns. Other empirical studies of demand effects in the bond market that build on our model include Hamilton and Wu (2012) and Li and Wei (2013) on QE purchases and the zero lower bound (ZLB);[4] Hanson (2014) and Malkhozov, Mueller, Vedolin, and Venter (2016) on mortgage-backed securities; Gorodnichenko and Ray (2018) on Treasury auctions; Kaminska and Zinna (2019) on purchases by foreign 

> 4For empirical estimates of the effects of QE, see also Gagnon, Raskin, Remache, and Sack (2011), Joyce, Lasaosa, Stevens, and Tong (2011), Krishnamurthy and Vissing-Jorgensen (2011), Swanson (2011), Christensen and Rudebusch (2012), D’Amico and King (2013), Swanson and Williams (2014), and the survey by Wiliams (2014). Some of these papers emphasize the duration-risk channel. That channel describes demand effects in the one-factor version of our model but not with multiple factors. 

6 

## D. VAYANOS AND J.-L. VILA 

central banks; and King (2019) on non-linearities induced by the ZLB. Hayashi (2018) develops numerical algorithms to solve our model with a general number of risk factors. 

The notion that demand shocks can drive asset prices away from fundamental values is emphasized in the literature on the limits of arbitrage, surveyed in Gromb and Vayanos (2010). Closest to our paper is the strand of the literature on price distortions across an asset class. See, for example, Barberis and Shleifer (2003) and Vayanos and Woolley (2013) on style investing, momentum and reversal; Greenwood (2005) and Hau (2011) on index redefinitions; Gabaix, Krishnamurthy, and Vigneron (2007) on mortgage-backed securities; Garleanu, Pedersen, and Poteshman (2009) on options; and Gabaix and Maggiori (2015) on foreign exchange. 

Preferred habitats in our model concern maturities. They could alternatively concern bonds that differ in liquidity or in the type of issuer, e.g., government versus corporate. Preferences for liquidity have been used to explain the on-the-run phenomenon, whereby just-issued government bonds are more expensive than previously-issued bonds maturing on nearby dates.[5] Preferences for government bonds over corporate bonds could be arising because the former are safer and more widely acceptable as collateral. Krishnamurthy and Vissing-Jorgensen (2012) provide evidence consistent with the existence of an investor clientele pricing those attributes. 

Our model belongs to the class of affine no-arbitrage term-structure models (Duffie and Kan (1996)) because yields are affine in the risk factors. Dai and Singleton (2002) and Duffee (2002) develop models within that class that embody the positive relationship between bond risk premia and term-structure slope. We derive such a relationship in an equilibrium model.[6] Our model can address questions that reduced-form models cannot such as how demand shocks affect the term structure and how the effects depend on arbitrageur risk aversion and investor price-elasticity. 

## 2. MODEL 

Time is continuous and goes from zero to infinity. The term structure at time _t_ consists of a continuum of zero-coupon government bonds. The maturities of the bonds lie in the interval (0 _, ∞_ ). Assuming that the interval of bond maturities is infinite is without loss of generality because we can specify preferred-habitat 

> 5For evidence on the on-the-run phenomenon, see Amihud and Mendelson (1991), Warga (1992) and Krishnamurthy (2002). For theoretical explanations, see Duffie (1996), Vayanos and Weill (2008) and Banerjee and Graveline (2013). 

> 6Other equilibrium models that generate a positive premia-slope relationship include Wachter (2006), Buraschi and Jiltsov (2007) and Lettau and Wachter (2011) who assume habit formation; Xiong and Yan (2010) who assume heterogeneous beliefs; and Gabaix (2012) who assumes rare disasters with time-varying severity. 

7 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

demand to be zero for bonds with sufficiently long maturities. The bond with maturity _τ_ has face value one, hence paying one unit of the numeraire at time _t_ + _τ_ . We denote by _Pt_[(] _[τ]_[)] and _yt_[(] _[τ]_[)] , respectively the time- _t_ price and yield of the bond with maturity _τ_ . The yield is the spot rate for maturity _τ_ , and is related to the price through 

**==> picture [125 x 25] intentionally omitted <==**

We denote by _ft_[(] _[τ][−]_[∆] _[τ,τ]_[)] the time- _t_ forward rate between maturities _τ −_ ∆ _τ_ and _τ_ . The forward rate is related to the price through 

**==> picture [173 x 36] intentionally omitted <==**

The short rate _rt_ is the limit of the yield _yt_[(] _[τ]_[)] when _τ_ goes to zero. We take _rt_ as exogenous, and describe its dynamics later in this section (Equation (7)). An exogenous _rt_ can be interpreted as the return of a linear and instantaneously riskless production technology. Alternatively, _rt_ can be determined by the central bank in response to exogenous shocks. We sketch the central-bank interpretation in Section 3.3, where we derive some of our model’s implications for monetary policy. 

Agents are of two types: arbitrageurs and preferred-habitat investors. Arbitrageurs can invest in the bonds and in the short rate. We denote their time- _t_ wealth by _Wt_ and their time- _t_ position, expressed in presentvalue terms, in the bonds with maturities in [ _τ, τ_ + _dτ_ ] by _Xt_[(] _[τ]_[)] _dτ_ . The arbitrageurs’ budget constraint is 

**==> picture [276 x 30] intentionally omitted <==**

where the instantaneous change _dPt_[(] _[τ]_[)] is computed by changing the time subscript _t_ to _t_ + _dt_ and the maturity superscript _τ_ to _τ − dt_ .[7] Arbitrageurs maximize a mean-variance objective over instantaneous changes in 

> 7Implicit in our notation is that the arbitrageurs’ position in the bonds with maturities in [ _τ, τ_ + _dτ_ ] is of order _dτ_ . Arbitrageurs hold such a position in equilibrium because preferred-habitat demand for the bonds with maturities in [ _τ, τ_ + _dτ_ ] is assumed to be of order _dτ_ . 

8 

D. VAYANOS AND J.-L. VILA 

wealth. Their optimization problem is 

**==> picture [212 x 24] intentionally omitted <==**

where _a ≥_ 0 is a risk-aversion coefficient that characterizes the trade-off between mean and variance. Arbitrageurs with the objective (4) can be interpreted as overlapping generations living over infinitesimal periods. The generation born at time _t_ is endowed with wealth _W_ , invests from _t_ to _t_ + _dt_ , consumes at _t_ + _dt_ and then dies. If preferences over consumption are described by the Von Neumann-Morgenstern (VNM) utility function _U_ , and if all uncertainty is Brownian as is the case in equilibrium, utility maximization yields the[)] objective (4) with the risk-aversion coefficient _a_ = _−[U][ ′′][′]_[(] _[W]_[[.]] 

_U[[′]]_ ( _W_ )[[.]] 

Preferred-habitat investors have preferences for specific maturities. For example, pension funds prefer longmaturity bonds because their duration matches that of pension liabilities. Insurance companies likewise prefer long- and intermediate-maturity bonds because their duration matches that of liabilities associated to retirement and insurance products that they offer. At the other end of the maturity spectrum, money-market funds are required by their mandates to hold short-maturity bonds. We model the demand of preferred-habitat investors in reduced form and provide an optimizing foundation in Appendix B. 

Investors’ maturity habitats cover the interval (0 _, ∞_ ), and investors with habitats in [ _τ, τ_ + _dτ_ ] are in measure _dτ_ . Investors with habitat _τ_ at time _t_ hold a position 

**==> picture [176 x 14] intentionally omitted <==**

expressed in present-value terms, in the bond with maturity _τ_ and hold no other bonds. Equation (5) is a demand function linear and decreasing in the logarithm of the bond price. The slope coefficient _α_ ( _τ_ ) _≥_ 0 is constant over time but can depend on maturity _τ_ . The intercept coefficient _βt_[(] _[τ]_[)] can depend on both _t_ and _τ_ . For simplicity, we refer to _α_ ( _τ_ ) and _βt_[(] _[τ]_[)] as demand slope and demand intercept, respectively. The actual intercept is _−βt_[(] _[τ]_[)] . By setting _α_ ( _τ_ ) = _βt_[(] _[τ]_[)] = 0 for _τ_ larger than a finite threshold _T_ , we can take the interval of bond maturities to be finite and equal to (0 _, T_ ). 

The demand intercept _βt_[(] _[τ]_[)] takes the form 

**==> picture [166 x 30] intentionally omitted <==**

9 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

where _{θk_ ( _τ_ ) _}k_ =0 _,..,K_ are constant over time but can depend on maturity _τ_ , and _{βk,t}k_ =1 _,..,K_ are timevarying but independent of _τ_ . We refer to _{βk,t}k_ =1 _,..,K_ as demand risk factors. The functions _{θk_ ( _τ_ ) _}k_ =1 _,..,K_ characterize the maturities where demand changes originate. If, for example, _θk_ ( _τ_ ) is independent of _τ_ , then a change in _βk,t_ impacts demand for all maturities equally, and can be interpreted as a global demand shock. If instead _θk_ ( _τ_ ) peaks at a specific maturity, then a change in _βk,t_ impacts demand for that maturity the most, and can be interpreted as a local demand shock. To ensure that integrals involving ( _α_ ( _τ_ ) _, {θk_ ( _τ_ ) _}k_ =1 _,..,K_ ) are well-defined, we assume that either (i) ( _α_ ( _τ_ ) _, {θk_ ( _τ_ ) _}k_ =1 _,..,K_ ) become zero for _τ_ larger than a finite threshold _T_ , are are continuous in (0 _, T_ ], or (ii) ( _α_ ( _τ_ ) _, {θk_ ( _τ_ ) _}k_ =1 _,..,K_ ) converge to zero at exponential rates when _τ_ goes to infinity, with the rate for _α_ ( _τ_ ) not exceeding those for _{θk_ ( _τ_ ) _}k_ =1 _,..,K_ , and are continuous in (0 _, ∞_ ). The ( _K_ + 1) _×_ 1 vector _qt ≡_ ( _rt, β_ 1 _,t, .., βK,t_ ) _[⊤]_ follows the process 

(7) _dqt_ = _−_ Γ( _qt − r_ ~~E~~ ) _dt_ + Σ _dBt,_ 

where _r_ is a constant, E is the ( _K_ + 1) _×_ 1 vector (1 _,_ 0 _, ..,_ 0) _[⊤]_ , (Γ _,_ Σ) are constant ( _K_ + 1) _×_ ( _K_ + 1) matrices, _dBt_ is a ( _K_ + 1) _×_ 1 vector ( _dBr,t, dBβ,_ 1 _,t, .., dBβ,K,t_ ) _[⊤]_ of independent Brownian motions, and _⊤_ denotes transpose. Equation (7) nests the case where the short rate _rt_ and the _K_ demand factors _{βk,t}k_ =1 _,..,K_ are mutually independent, and the case where they are correlated. Independence arises when the matrices (Γ _,_ Σ) are diagonal. When instead Σ is non-diagonal, shocks to the factors _rt_ and _{βk,t}k_ =1 _,..,K_ are correlated, and when Γ is non-diagonal, the drift (instantaneous expected change) of each factor depends on all other factors. We assume that the eigenvalues of Γ have positive real parts. Hence, _qt_ is stationary, and (7) implies that the long-run means of _rt_ and _{βk,t}k_ =1 _,..,K_ are _r_ and zero, respectively. Setting the long-run mean of _{βk,t}k_ =1 _,..,K_ to zero is without loss of generality since we can redefine the function _θ_ 0( _τ_ ) to include a non-zero long-run mean. 

We assume that government bonds are in zero supply. This is without loss of generality because we can redefine the demand function (5) as a net demand: the demand by preferred-habitat investors for the bond with maturity _τ_ , net of the government supply of that bond. 

Under the assumed demand function (5), the demand by preferred-habitat investors for the bond with maturity _τ_ depends only on that bond’s price and not on the prices of other bonds. This begs the question why rational investors buy the bond with maturity _τ_ if a bond with maturity close to _τ_ is much cheaper. Appendix B shows that the demand function (5), together with the specification (6) and (7) for the demand 

10 

D. VAYANOS AND J.-L. VILA 

intercept _βt_[(] _[τ]_[)] , can be given an optimizing foundation when bond maturities belong to a finite interval (0 _, T_ ) and the matrix Σ has full rank. The optimizing foundation requires that the term structure satisfies noarbitrage, which is the case for the equilibrium derived in Sections 3 and 4. 

The preferred-habitat investors in Appendix B form overlapping generations living over a period equal to the maximum bond maturity _T_ . The generation born at time _t_ consumes only at _t_ + _T_ and then dies. Investors are infinitely risk-averse over consumption. They derive consumption by investing in bonds and in a private opportunity whose return at time _t[′] ≥ t_ is exogenous and increasing in _βt_[(] _[T]_[ +] _[t][−][t][′]_[)] . Infinite risk aversion ensures that investors’ optimal bond portfolio yields a riskless payoff at the time _t_ + _T_ when they consume. That portfolio consists only of the bond maturing at _t_ + _T_ . No-arbitrage ensures that investors cannot achieve a higher payoff with certainty by investing in bonds with maturities other than _t_ + _T_ : if the payoff is higher with positive probability, then it must also be lower with positive probability. 

The elasticity of preferred-habitat demand in Appendix B arises because investors substitute between the bond that matures at the time _t_ + _T_ when they consume, and the private opportunity. When the bond’s price decreases, the bond’s return from _t_ to _t_ + _T_ increases. Hence, the bond becomes more attractive relative to the private opportunity, and bond demand increases.[8] Conversely, when the return on the private opportunity increases, it becomes more attractive relative to the bond, and bond demand decreases. The private opportunity could represent, for example, an investment in real estate.[9] 

Stepping outside of the optimizing foundation in Appendix B, _βt_[(] _[τ]_[)] could vary because of shocks to the supply of bonds issued by the government and shocks to the composition of the preferred-habitat investor pool. The demand specification (5)-(7) can capture these shocks if the maturities affected by the shocks remain fixed as time passes. Suppose, for example, that there is a sudden increase at time _t_ in the demand for the bond with maturity _τ_ . The specification (5)-(7) requires that this increase translates to an increase at time _t[′] > t_ in the demand for the bond with maturity _τ_ rather than _τ_ + _t − t[′]_ . That is, the shock does not “roll down” over time in the maturity space. 

Some shocks roll down in the maturity space. For example, an increase at time _t_ in the government supply of the bond with maturity _τ_ translates to an increase at time _t[′] > t_ in the supply of the bond with maturity 

> 8Since investors in Appendix B choose their portfolio based on its return at the time _t_ + _T_ when they consume, their demand for the bond that matures at _t_ + _T_ depends on the bond’s return to maturity rather than on the return over the next instant. 

> 9An example of preferred-habitat investors substituting from government bonds into real estate comes from the UK’s pension reform of 2004, mentioned in the Introduction. The drop in long rates induced pension funds to substitute towards non-bond investments, including real estate. For example, Marks & Spencer arranged for their pension fund to receive payments based on the leases of their property portfolio (Islam (2007), p.61). 

11 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

_τ_ + _t−t[′]_ rather than _τ_ . For such shocks, the specification (5)-(7) can be viewed as an approximation. Modifying that specification to allow roll down would render the analysis more complicated because bond demand at time _t_ would depend on the entire history of shocks up to time _t − T_ . (The shocks up to time _t − T_ + _τ_ would affect demand for bonds with maturities up to _τ_ .) 

Our model makes a stark distinction between arbitrageurs, who can substitute across maturities, and preferred-habitat investors, who invest only in their maturity habitat. Suppressing this distinction (by making the risk aversion of preferred-habitat investors finite in Appendix B), would complicate the model without changing the basic mechanisms. Preferred-habitat investors would substitute across maturities, acting partly as arbitrageurs, and arbitrage capacity would increase. The analysis would become more complicated because it would involve a continuum of portfolios rather than only the portfolio of arbitrageurs. 

An additional distinction between arbitrageurs and preferred-habitat investors, which is implicit in the demand specification (5) and explicit in the optimizing foundation in Appendix B, is that the latter can access investment opportunities outside of the bond market while the former cannot. If arbitrageurs could access investment opportunities outside the government bond market, then shocks to the returns of their opportunities would affect bond prices as well. We suppress that effect by assuming that arbitrageurs specialize in trading only government bonds. 

Our model can be given both a nominal and a real interpretation. Under the nominal interpretation, the numeraire is money, arbitrageurs’ preferences concern their wealth evaluated in nominal terms, and preferences of preferred-habitat investors (in the optimizing foundation in Appendix B) concern their consumption in nominal terms. Under the real interpretation, the numeraire consists of goods, and preferences concern wealth and consumption in real terms. A short rate determined by the central bank fits better the nominal interpretation, while a short rate determined by a production technology fits better the real interpretation. 

The arbitrageurs’ optimization problem yields the same solution regardless of whether preferences concern nominal or real wealth. This is because the arbitrageurs’ objective involves changes in wealth over an infinitesimal interval, during which inflation is constant.[10] Hence, the assumption under the nominal interpretation that arbitrageurs’ preferences concern nominal wealth is innocuous. 

Whether preferences concern nominal or real consumption matters for preferred-habitat investors, who have 

> 10Denoting by _dWt_ = _Wt_ + _dt − Wt_ the instantaneous change in arbitrageur nominal wealth, the change in real wealth is _dWt[R]_ = 1+ _[W][t] π_[+] _t[dt] dt[−][W][t]_[=] _[ dW][t][ −][W][t][π][t][dt]_[,][where] _[π][t]_[is][inflation][between] _[t]_[and] _[t]_[ +] _[ dt]_[.][Since][E] _[t]_[(] _[dW][ R] t_[)] _[ −][a]_ 2[V][ar] _[t]_[(] _[dW][ R] t_[) =][ E] _[t]_[(] _[dW][t]_[)] _[ −] a_ 2[V][ar] _[t]_[(] _[dW][t]_[)] _[ −][π][t][dt]_[,][maximizing][E] _[t]_[(] _[dW][ R] t_[)] _[ −][a]_ 2[V][ar] _[t]_[(] _[dW][ R] t_[)][yields][the][same][solution][as][maximizing][E] _[t]_[(] _[dW][t]_[)] _[ −][a]_ 2[V][ar] _[t]_[(] _[dW][t]_[).] 

12 

## D. VAYANOS AND J.-L. VILA 

a longer horizon. Preferences over nominal consumption describe, for example, life-insurance companies that offer insurance or retirement products with guaranteed minimum returns typically not indexed to inflation.[11] Preferences over real consumption describe, for example, pension funds that offer pensions rising with, or explicitly indexed to, inflation.[12] Payouts from property and casualty insurance rise with inflation as well. Hence, both nominal and real preferred habitats arise in practice. 

Under the nominal interpretation, inflation could affect both the short rate and the intercept _βt_[(] _[τ]_[)] of preferred-habitat demand. Indeed, high inflation could be associated with high nominal returns throughout the economy, and hence with both a high nominal short rate and a high nominal return _βt_[(] _[τ]_[)] on investment opportunities other than government bonds. Inflation could thus generate a positive correlation between the short rate and the demand factors. Because of that correlation, inflation could have only a weak effect on bond demand by preferred-habitat investors: high bond yields raise demand, and high _βt_[(] _[τ]_[)] lowers it. 

## 3. NO DEMAND RISK 

In this section we study the case where there are no demand risk factors ( _K_ = 0). Time-variation in yields arises because of the short rate _rt_ , which is the only risk factor. For _K_ = 0, (7) reduces to 

**==> picture [168 x 11] intentionally omitted <==**

where _κr ≡_ Γ1 _,_ 1 _>_ 0 and _σr ≡_ Σ1 _,_ 1. 

## 3.1. _Equilibrium without Arbitrageurs_ 

We first derive, as a benchmark, the equilibrium that would prevail in the arbitrageurs’ absence. We refer to it as the _segmentation equilibrium_ because the yield for each maturity is determined solely by the demand of the investors with that maturity habitat. The yield _yt_[(] _[τ]_[)] for maturity _τ_ is determined by setting the net demand (5) by preferred-habitat investors to zero. Since (1) implies log( _Pt_[(] _[τ]_[)] ) = _−τyt_[(] _[τ]_[)] , _yt_[(] _[τ]_[)] is given by 

**==> picture [144 x 28] intentionally omitted <==**

> 11For a description of the products offered by life-insurance companies see, for example, Berends, McMenamin, Plestis, and Rosen (2013) and Sen (2019). Table 1 of Berends, McMenamin, Plestis, and Rosen (2013) indicates that guaranteed minimum returns not indexed to inflation are a common feature of life-insurance products. 

> 12Indexation of pensions to inflation was accounted for in the 2004 U.K. pension reform, which required pension funds to evaluate their pension liabilities using the yields of long-maturity _inflation-indexed_ bonds. 

13 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

where the second equality follows by setting _K_ = 0 in (6). The yield _yt_[(] _[τ]_[)] for maturity _τ_ is constant over time and is disconnected from the time-varying short rate _rt_ . It depends only on the demand intercept _βt_[(] _[τ]_[)] = _θ_ 0( _τ_ ) and demand slope _α_ ( _τ_ ) for maturity _τ_ . An increase in _θ_ 0( _τ_ ) lowers the demand by preferred-habitat investors for the bond with maturity _τ_ , and hence raises _yt_[(] _[τ]_[)] . The effect is weaker the larger _α_ ( _τ_ ) is because the demand by preferred-habitat investors is more price-elastic. The segmentation equilibrium corresponds to an extreme form of the preferred-habitat view (Culbertson (1957), Modigliani and Sutch (1966)). 

## 3.2. _Equilibrium with Arbitrageurs_ 

We next derive the equilibrium when arbitrageurs are present. We proceed in three steps: (i) conjecture a functional form for equilibrium yields, (ii) derive the arbitrageurs’ first-order condition given the conjectured yields, and (iii) combine the arbitrageurs’ first-order condition with market clearing, and confirm that yields are as conjectured. 

We conjecture that equilibrium yields are affine in the single risk factor _rt_ . That is, there exist two functions ( _Ar_ ( _τ_ ) _, C_ ( _τ_ )) that depend only on _τ_ such that the time- _t_ price of the bond with maturity _τ_ is 

**==> picture [145 x 14] intentionally omitted <==**

Applying Ito’s Lemma to (10), recalling that _dPt_[(] _[τ]_[)] is computed by changing the time subscript _t_ to _t_ + _dt_ and the maturity superscript _τ_ to _τ − dt_ , and using the dynamics (8) of _rt_ , we find that the time- _t_ instantaneous return on the bond with maturity _τ_ is 

**==> picture [181 x 30] intentionally omitted <==**

where 

**==> picture [282 x 21] intentionally omitted <==**

is the instantaneous expected return. 

To derive the arbitrageurs’ first-order condition, we substitute the bond return (11) into the the arbi- 

14 

D. VAYANOS AND J.-L. VILA 

trageurs’ budget constraint (3) and optimization problem (4). This yields 

**==> picture [315 x 25] intentionally omitted <==**

and 

**==> picture [337 x 31] intentionally omitted <==**

respectively. Point-wise maximization of (13) yields the arbitrageurs’ first-order condition. 

Lemma 1 _The arbitrageurs’ first-order condition is_ 

**==> picture [145 x 14] intentionally omitted <==**

_where_ 

**==> picture [175 x 25] intentionally omitted <==**

The arbitrageurs’ first-order condition (14) balances risk and return. The left-hand side is the increase in the expected return on the arbitrageurs’ portfolio if they shift one unit of the numeraire from the short rate _rt_ to the bond with maturity _τ_ . Portfolio expected return increases by the difference between the bond’s expected return _µ_[(] _t[τ]_[)] and the short rate _rt_ . The right-hand side is the increase in the risk of the arbitrageurs’ portfolio, times the arbitrageurs’ risk-aversion coefficient _a_ . Portfolio risk increases by the covariance between the return on the additional investment in the bond and the return on the portfolio. With one risk factor, the covariance is the product of the sensitivities of the two returns to the factor, times the factor’s variance. The risk factor is the short rate, and its variance is _σr_[2][.][Moreover,][(][11][)][implies][that][the][sensitivity][of][the][bond’s] _∞_ return to the short rate is _−Ar_ ( _τ_ ), and the sensitivity of the portfolio’s return is _−_ �0 _Xt_[(] _[τ]_[)] _Ar_ ( _τ_ ) _dτ_ . 

The first-order condition (14) can alternatively be interpreted in the context of no-arbitrage models of the term structure.[13] No-arbitrage in continuous time requires that there exist prices specific to each risk 

> 13See, for example, Vasicek (1977) and Cox, Ingersoll, and Ross (1985) for early contributions, and Veronesi (2010) for a textbook treatment. 

15 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

factor and common across assets, such that the expected return of any asset in excess of the short rate is equal to the sum across factors of the asset’s sensitivity to each factor times the factor’s price. With one factor, the no-arbitrage condition boils down to requiring that the factor’s price is equal to the ratio of any asset’s expected excess return to the asset’s factor sensitivity. The no-arbitrage condition in our model is the arbitrageurs’ first-order condition (14), and the price of the short-rate factor is _λr,t_ . 

Absence of arbitrage is mute on what the prices of the risk factors are. These prices are instead determined by equilibrium arguments. Equation (15) shows that _λr,t_ is proportional to the factor sensitivity 

_∞ −_ �0 _Xt_[(] _[τ]_[)] _Ar_ ( _τ_ ) _dτ_ of the arbitrageurs’ portfolio. To determine that portfolio, we use market clearing. 

Market clearing requires that the time- _t_ positions of arbitrageurs and preferred-habitat investors in the bond with maturity _τ_ sum to zero: 

**==> picture [115 x 14] intentionally omitted <==**

Substituting _Xt_[(] _[τ]_[)] from (16) into (15), we find 

**==> picture [282 x 94] intentionally omitted <==**

where the second equality follows by substituting _Zt_[(] _[τ]_[)] from (5), and the third equality follows by substituting _Pt_[(] _[τ]_[)] from (10) and using _βt_[(] _[τ]_[)] = _θ_ 0( _τ_ ) (which follows by setting _K_ = 0 in (6)). Equation (17) shows that the price _λr,t_ of the short-rate risk factor depends on the short rate _rt_ and on the demand intercept _θ_ 0( _τ_ ) and demand slope _α_ ( _τ_ ) of preferred-habitat investors. We return to these effects and their economic implications in Sections 3.3-3.5. 

Substituting _λr,t_ and _µ_[(] _t[τ]_[)] from (17) and (12), respectively, into (14), we find 

**==> picture [292 x 56] intentionally omitted <==**

16 

D. VAYANOS AND J.-L. VILA 

Equation (18) must hold for all values of _rt_ . Hence, the linear terms in _rt_ on both sides must be equal, and the same is true for the terms that are independent of _rt_ . This yields the two first-order linear ordinary differential equations (ODEs) 

**==> picture [375 x 59] intentionally omitted <==**

in the functions ( _Ar_ ( _τ_ ) _, C_ ( _τ_ )). Equations (19) and (20) must be solved with the initial conditions _Ar_ (0) = _C_ (0) = 0, which follow from (10) because a bond with zero maturity trades at its face value of one. A complicating feature of (19) and (20) is that the coefficient of _Ar_ ( _τ_ ) in each equation depends on an integral involving the functions ( _Ar_ ( _τ_ ) _, C_ ( _τ_ )). To solve (19) and (20), we proceed in two steps. First, we take the integrals as given and solve (19) and (20) as linear ODEs with constant coefficients. Second, we require that the solution is consistent with the value of the integrals. 

The first step yields 

**==> picture [242 x 62] intentionally omitted <==**

where the scalars ( _κ[∗] r[,] r[∗]_ ) are defined by 

**==> picture [261 x 59] intentionally omitted <==**

We use the star subscript because ( _κ[∗] r[,] r_ ~~_[∗]_~~ ) are the counterparts of ( _κr, r_ ) under the risk-neutral measure. The second step requires that ( _κ[∗] r[,] r[∗]_ ) solve (23) and (24) when ( _Ar_ ( _τ_ ) _, C_ ( _τ_ )) are substituted in from (21) and (22). Proposition 1 shows that this requirement determines ( _κ[∗] r[,] r_ ~~_[∗]_~~ ) uniquely. 

Proposition 1 _The functions_ ( _Ar_ ( _τ_ ) _, C_ ( _τ_ )) _are given by (21) and (22), respectively, where κ[∗] r[is the unique]_ 

17 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

_solution to_ 

**==> picture [226 x 28] intentionally omitted <==**

_and r_ ~~_[∗]_~~ _is given by_ 

**==> picture [435 x 46] intentionally omitted <==**

We next explore the economic implications of the equilibrium derived in Proposition 1. Section 3.3 examines how shocks to the short rate are transmitted to longer maturities. Section 3.4 examines how bond expected excess returns depend on the short rate and on the shape of the term structure. Section 3.5 examines how changes in bond demand affect the term structure. 

## 3.3. _Monetary Policy Transmission and Carry Trades_ 

In the segmentation equilibrium, in which there are no arbitrageurs, bond yields _yt_[(] _[τ]_[)] are disconnected from the short rate _rt_ . By contrast, when arbitrageurs are present, they transmit short-rate shocks to bond yields, ensuring that yields are informative about the current and expected future short rates. 

Arbitrageurs transmit short-rate shocks to bond yields through their _carry trades_ . Suppose that a shock causes the short rate to drop below the value that bond yields would take in the segmentation equilibrium. To benefit from the discrepancy between bond yields and the short rate, arbitrageurs buy bonds and finance their position by borrowing short-term. Their activity causes bond prices to rise and yields to drop, thus reflecting the drop in the short rate. Conversely, following a shock that causes the short rate to exceed the value that bond yields would take under segmentation, arbitrageurs short-sell bonds and invest short-term. Their activity causes bond prices to drop and yields to rise, thus reflecting the rise in the short rate. In both cases, arbitrageurs engage in carry trades—trades that are profitable when prices do not move. For example, buying a bond and financing that position by short-term borrowing is profitable when the short rate remains below the bond’s yield until the bond’s maturity. 

The extent to which arbitrageurs transmit short-rate shocks to bond yields depends on three main parameters of our model: the arbitrageurs’ risk-aversion coefficient _a_ , the volatility _σr_ of the short rate, and 

18 

D. VAYANOS AND J.-L. VILA 

the slope _α_ ( _τ_ ) of the demand by preferred-habitat investors. When _a_ = 0, arbitrageurs are not averse to the risk that carry trades entail, namely, that the short rate can rise when they borrow short-term to buy bonds, and that the short rate can drop when they short-sell bonds and invest short-term. Hence, arbitrageurs engage in carry trades that are sufficiently large to transmit short-rate shocks fully to bond yields. When _α_ ( _τ_ ) = 0 for all _τ ∈_ (0 _, T_ ), shocks are again transmitted fully, but for a different reason. Since the demand of preferred-habitat investors is independent of bond prices, short-rate shocks do not trigger carry trades by arbitrageurs in equilibrium, even though bond yields change. Hence, arbitrageurs impact bond yields without bearing carry-trade risk, in effect having infinite price impact. The transmission of shocks becomes weaker when _a_ , _σr_[2][and] _[α]_[(] _[τ]_[)][increase.] 

We measure the extent to which arbitrageurs transmit short-rate shocks to bond yields by comparing the reaction of forward rates to that of expected future short rates. We evaluate how a time- _t_ shock to the short rate _rt_ affects the expected short rate _Et_ ( _rt_ + _τ_ ) at time _t_ + _τ_ and the instantaneous forward rate _ft_[(] _[τ]_[)] for maturity _τ_ . The latter rate is defined as the limit of the forward rate _ft_[(] _[τ][−]_[∆] _[τ,τ]_[)] between maturities _τ −_ ∆ _τ_ and _τ_ when ∆ _τ_ goes to zero: 

**==> picture [295 x 25] intentionally omitted <==**

where the second step follows from (2), and the third from (10). When the expectations hypothesis (EH) of the term structure holds, forward rates move one-to-one with expected future short rates. Proposition 2 shows that when _a >_ 0 and _α_ ( _τ_ ) _>_ 0, forward rates under-react and hence arbitrageurs transmit short-rate shocks to bond yields only partially. 

Formally, a unit shock to _rt_ raises _Et_ ( _rt_ + _τ_ ) by _e[−][κ][r][τ]_ because the short rate mean-reverts at rate _κr_ . Equation (27) implies that _ft_[(] _[τ]_[)] rises by _A[′] r_[(] _[τ]_[) =] _[ e][−][κ] r[∗][τ]_ , where the equality follows from (21). Under-reaction occurs because the short rate’s mean-reversion parameter _κ[∗] r_[under][the][risk-neutral][measure][exceeds][its] counterpart _κr_ under the physical measure. Equation (25) implies that the difference _κ[∗] r[−][κ][r]_[,][and][hence][the] extent of under-reaction, increases in _a_ , _σr_[2][and] _[α]_[(] _[τ]_[).] 

Proposition 2 ( **Under-Reaction of Forward Rates** ) _A unit shock to the short rate rt:_ 

>  _Raises the expected short rate Et_ ( _rt_ + _τ_ ) _at time t_ + _τ by[∂E][t] ∂r_[(] _[r] t[t]_[+] _[τ]_[ )] = _e[−][κ][r][τ] ._ 

19 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

 _Raises the instantaneous forward rate ft_[(] _[τ]_[)] _for maturity τ by[∂] ∂r[f] t_[ (] _[τ] t_[)] = _e[−][κ] r[∗][τ] . The forward rate under-reacts (κ[∗] r[> κ][r][)][if][arbitrageurs][are][risk-averse][(][a >]_[ 0] _[)][and][the][demand][by][preferred-] habitat investors is price-elastic (α_ ( _τ_ ) _>_ 0 _in a positive-measure subset of_ (0 _, ∞_ ) _). The extent of underreaction κ[∗] r[−][κ][r][increases][in][a][,][σ] r_[2] _[and][α]_[(] _[τ]_[)] _[.]_ 

Our results have implications for the transmission of monetary policy. Suppose that the central bank conducts monetary policy by changing the rate that it pays on bank reserves. Suppose also that arbitrageurs are banks, in which case the short rate _rt_ that they earn on their wealth is the rate paid on reserves. Our model implies that the transmission of monetary-policy shocks to the yields of long-maturity bonds is done by arbitrageurs. Moreover, the transmission mechanism is weaker when arbitrageurs are more risk-averse, central bank actions are more uncertain (the short rate is more volatile), or the demand by preferred-habitat investors is more price-elastic. An additional implication is that in transmitting monetary-policy shocks, arbitrageurs earn a rent. That rent arises from the returns on the carry trades, and reflects bond risk premia, as we explain in Section 3.4. In that section we also show that bond risk premia are larger, resulting in a larger rent for arbitrageurs, under the same conditions that generate a weaker transmission mechanism. 

## 3.4. _Bond Risk Premia_ 

Under the EH, bond expected returns are equal to the riskless rate. When instead _a >_ 0 and _α_ ( _τ_ ) _>_ 0, they differ from the riskless rate and mirror the carry trades of arbitrageurs. This is because risk-averse arbitrageurs enter into carry trades only if they expect to earn high returns as compensation for the risk they take. Suppose that the short rate drops, in which case bond yields drop and price-elastic preferredhabitat investors sell bonds. Bonds earn then positive expected returns in excess of the riskless rate so that arbitrageurs are induced to buy them. When instead the short rate rises, bonds earn negative expected excess returns so that arbitrageurs are induced to sell them short. We refer to expected excess returns as risk premia because they compensate arbitrageurs for risk. 

Since in the absence of demand risk factors, the short rate is the only source of time-variation, bond risk premia are positively related to the slope of the term structure: a low (high) short rate implies both a term structure with slope higher (lower) than average and positive (negative) bond risk premia. The positive premia-slope relationship is a widely documented empirical fact in the term-structure literature, starting with 

20 

D. VAYANOS AND J.-L. VILA 

Fama and Bliss (FB, 1987). FB perform the regression 

**==> picture [349 x 31] intentionally omitted <==**

The dependent variable is the return on a zero-coupon bond with maturity _τ_ held over a period ∆ _τ_ , in excess of the spot rate for maturity ∆ _τ_ . The independent variable is the slope of the term structure as measured by the difference between the forward rate between maturities _τ −_ ∆ _τ_ and _τ_ , and the spot rate for maturity ∆ _τ_ . FB find that _b_ FB is positive, larger than one for most _τ_ , and increasing in _τ_ . The implied time-variation of risk premia is economically significant: predicted premia have a standard deviation of about 1-1.5% per year, while average premia are about 0.5% per year. 

The behavior of bond risk premia is related to the predictability of changes to long rates. Campbell and Shiller (CS 1991) find that the slope of the term structure predicts changes in long rates, but to a weaker and typically opposite extent than implied by the EH. CS perform the regression 

**==> picture [298 x 21] intentionally omitted <==**

The dependent variable is the change, between times _t_ and _t_ + ∆ _τ_ , in the yield of a zero-coupon bond that has maturity _τ_ at time _t_ . The independent variable is the difference between the spot rates for maturities _τ_ and ∆ _τ_ , normalized so that the regression coefficient _b_ CS is equal to one under the EH. CS find that _b_ CS is smaller than one, negative for most _τ_ , and decreasing in _τ_ . This finding is related to the positive premiaslope relationship. Indeed, suppose that the term structure has slope higher than average. Because bonds earn positive expected excess returns, their yields increase by less than under the EH, implying a regression coefficient _b_ CS smaller than one.[14] 

Proposition 3 computes the FB and CS regression coefficients _b_ FB and _b_ CS in the analytically convenient case where ∆ _τ_ is small. The proposition confirms that when _a >_ 0 and _α_ ( _τ_ ) _>_ 0, _b_ FB is positive and _b_ CS is smaller than one. It also shows that _b_ FB increases in the arbitrageurs’ risk-aversion coefficient _a_ , the volatility _σr_ of the short rate, and the slope _α_ ( _τ_ ) of the demand by preferred-habitat investors. 

Additional implications of Proposition 3 are that _b_ FB is independent of _τ_ and is smaller than one, and that 

> _b_ CS increases in _τ_ . In the data, by contrast, _b_ FB increases in _τ_ and exceeds one for most maturities, and _b_ CS 

> 14For more material and references on bond return predictability, see the survey by Cochrane (1999). See also Cochrane and Piazzesi (2005) who find that a tent-shaped factor of yields explains bond risk premia even better than the slope of the term structure does. 

21 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

decreases in _τ_ . Our model can match these empirical properties in the presence of demand risk, as we show in Sections 4 and 5. 

- Proposition 3 ( **Positive Premia-Slope Relationship** ) _For_ ∆ _τ →_ 0 _and for all τ :_ 

   -  _The FB regression coefficient in (28) is bFB_ = _[κ] r[∗] κ[−][∗] r[κ][r] . It is positive if arbitrageurs are risk-averse (a >_ 0 _) and the demand by preferred-habitat investors is price-elastic (α_ ( _τ_ ) _>_ 0 _in a positive-measure subset of_ (0 _, ∞_ ) _). It increases in a, σr_[2] _[and][α]_[(] _[τ]_[)] _[.]_ 

   -  _The CS regression coefficient in (29) is bCS_ = 1 _−_[(] _[κ] r[∗] τ[−] −[κ] A[r]_[)] _r[A]_ ( _τ[r]_[(] ) _[τ]_[)] _[τ] . It is smaller than one under the same condition that ensures bFB >_ 0 _, and it increases in τ ._ 

## 3.5. _Demand Effects_ 

In the segmentation equilibrium, in which there are no arbitrageurs, the yield _yt_[(] _[τ]_[)] for maturity _τ_ depends only on the demand intercept _βt_[(] _[τ]_[)] = _θ_ 0( _τ_ ) and demand slope _α_ ( _τ_ ) for that maturity. The presence of arbitrageurs changes that aspect of the equilibrium dramatically. The yield _yt_[(] _[τ]_[)] depends on the demand intercept and slope for all maturities. Moreover, a change in the demand intercept for maturity _τ_ can have its largest effects for maturities other than _τ_ . 

Suppose that the demand intercept _θ_ 0( _τ_ ) changes to _θ_ 0( _τ_ ) + ∆ _θ_ 0( _τ_ ), where ∆ _θ_ 0( _τ_ ) is a general function of _τ_ and represents an unanticipated and permanent change. Maturities for which ∆ _θ_ 0( _τ_ ) _>_ 0 experience a drop in demand because (5) defines the demand intercept with a negative sign. Proposition 1 implies that _κ[∗] r_[and] _Ar_ ( _τ_ ) do not change, that the change ∆ _r_ ~~_[∗]_~~ in _r[∗]_ has the same sign as _aσr_[2] �0 _∞_ ∆ _θ_ 0( _τ_ ) _Ar_ ( _τ_ ) _dτ_ , and that _C_ ( _τ_ ) changes by _κ[∗] r_[∆] _r[∗]_[�] 0 _[τ][A][r]_[(] _[u]_[)] _[du]_[.][Hence,][the][yield] _[y] t_[(] _[τ]_[)] for maturity _τ_ changes by ∆ _yt_[(] _[τ]_[)] _≡ κ[∗] r_[∆] _r_ ~~_[∗]_~~ �0 _τ[A][r] τ_[(] _[u]_[)] _[du]_ . Proposition 4 follows from these observations. 

Proposition 4 ( **Global Demand Effects** ) _A change in the demand intercept from θ_ 0( _τ_ ) _to θ_ 0( _τ_ )+∆ _θ_ 0( _τ_ ) _affects yields if arbitrageurs are risk-averse (a >_ 0 _). Spot rates for all maturities rise if_ �0 _∞_ ∆ _θ_ 0( _τ_ ) _Ar_ ( _τ_ ) _dτ >_ 0 _and drop otherwise. The relative effect across maturities is independent of the maturities where the demand t t change originates (_[∆] _[y]_[(] _[τ]_[2)] _is independent of_ ∆ _θ_ 0( _τ_ ) _). Yields for longer maturities are more affected (_[∆] _[y]_[(] _[τ]_[2)] _>_ 1 ∆ _yt_[(] _[τ]_[1)] ∆ _yt_[(] _[τ]_[1)] _for τ_ 1 _< τ_ 2 _)._ 

## 22 

## D. VAYANOS AND J.-L. VILA 

Proposition 4 shows that the effects of the change ∆ _θ_ 0( _τ_ ) are characterized fully by the integral �0 _∞_ ∆ _θ_ 0( _τ_ ) _Ar_ ( _τ_ ) _dτ_ . If that integral is positive, then yields for all maturities rise—even for maturities for which demand increases because ∆ _θ_ 0( _τ_ ) _<_ 0. Thus, demand effects are global: demand intercepts across all maturities are aggregated into the one-dimensional index �0 _∞ θ_ 0( _τ_ ) _Ar_ ( _τ_ ) _dτ_ , and changes to that index move all yields in the same direction. These global effects are the polar opposite of the local effects derived in the segmentation equilibrium. 

Demand effects are represented by a one-dimensional index because there is only one risk factor, the short rate. The index relates to the sensitivity of arbitrageurs’ portfolio to that factor. Suppose that following a change in preferred-habitat demand, arbitrageurs are induced to hold a portfolio that realizes more losses when the short rate increases. Arbitrageurs then view bonds as riskier and require higher expected excess returns to hold them, causing yields to increase for all maturities. 

The index is derived by multiplying the demand intercept _θ_ 0( _τ_ ) for maturity _τ_ by the function _Ar_ ( _τ_ ) = 1 _−e[−][κ] r[∗][τ] κ[∗] r_ that characterizes the sensitivity of the _τ_ -maturity bond to the short rate, and integrating across maturities. If a change in the demand intercept raises that integral, then the sensitivity-weighted demand for bonds by preferred-habitat investors declines and the sensitivity of arbitrageurs’ portfolio increases. Since _Ar_ ( _τ_ ) increases in _τ_ , demand intercepts for longer-maturity bonds receive a larger weight in the index. Hence, changes to the demand for these bonds have a larger effect on the term structure. 

While changes to the demand for longer-maturity bonds have a larger effect on yields, the _relative_ effect across maturities is the same as when the demand for shorter-maturity bonds changes. Moreover, yields for longer maturities are more affected (by any demand change). Intuitively, a decrease in demand raises the instantaneous expected returns of long-maturity bonds more than of short-maturity bonds. This is because expected excess returns compensate arbitrageurs for risk, and long-maturity bonds are riskier ( _Ar_ ( _τ_ ) increases in _τ_ ). The increase in expected returns causes yields to increase: the yield for maturity _τ_ involves an average of instantaneous expected returns that the bond with maturity _τ_ earns during its life [ _t, t_ + _τ_ ]. Since demand changes are permanent, the average of instantaneous expected returns increases more for longer-maturity bonds. Hence, yields for longer maturities are more affected by demand changes. 

23 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

**==> picture [76 x 8] intentionally omitted <==**

In this section we generalize our analysis to the case where demand is time-varying. Since demand affects yields only when arbitrageurs are risk-averse, we assume _a >_ 0. Time-variation in yields arises because of the short rate _rt_ and the _K_ demand factors _{βk,t}k_ =1 _,..,K_ . 

## 4.1. _Equilibrium_ 

We derive the equilibrium following the same three steps as in Section 3.2. We conjecture that there exist _K_ +2 functions ( _Ar_ ( _τ_ ) _, {Aβ,k_ ( _τ_ ) _}k_ =1 _,..,K, C_ ( _τ_ )) that depend only on _τ_ such that the time- _t_ price of the bond with maturity _τ_ is 

**==> picture [148 x 15] intentionally omitted <==**

where _A_ ( _τ_ ) is the ( _K_ + 1) _×_ 1 vector ( _Ar_ ( _τ_ ) _, Aβ,_ 1( _τ_ ) _, .., Aβ,K_ ( _τ_ )) _[⊤]_ . Applying Ito’s Lemma to (10), using the dynamics (7) of _qt_ , and noting that _t_ + _τ_ stays constant when taking the derivative, we find that the time- _t_ instantaneous return on the bond with maturity _τ_ is 

**==> picture [175 x 30] intentionally omitted <==**

where 

**==> picture [321 x 21] intentionally omitted <==**

is the instantaneous expected return. Substituting the bond return (31) into the the arbitrageurs’ optimization problem (4) yields 

**==> picture [429 x 31] intentionally omitted <==**

Point-wise maximization of (33) yields the arbitrageurs’ first-order condition. 

Lemma 2 _The arbitrageurs’ first-order condition is_ 

**==> picture [236 x 25] intentionally omitted <==**

24 

## D. VAYANOS AND J.-L. VILA 

Equation (34) is the multi-factor counterpart of (14). The left-hand side is the increase in portfolio expected return if arbitrageurs shift one unit of the numeraire from the short rate _rt_ to the bond with maturity _τ_ . The right-hand side is the increase in portfolio risk, times the arbitrageurs’ risk aversion coefficient _a_ . The increase in portfolio risk is equal to the covariance between the return on the additional investment in the bond and the return on the arbitrageurs’ portfolio. With multiple risk factors, the covariance is the product _∞_ of the sensitivity vectors _−A_ ( _τ_ ) and _−_ �0 _Xt_[(] _[τ]_[)] _A_ ( _τ_ ) _dτ_ of the two returns to the factors, times the factors’ covariance matrix ΣΣ _[⊤]_ . To show the full analogy between (34) and (14), we can write (34) in terms of factor prices. Denoting the ( _K_ + 1) _×_ 1 vector of factor prices by _λt ≡_ ( _λr,t, λβ,_ 1 _,t, .., λβ,K,t_ ) _[⊤]_ , we can write (34) as _µ_[(] _t[τ]_[)] _− rt_ = _−aA_ ( _τ_ ) _[⊤] λt_ and deduce that factor prices are _λt_ = _−_ ΣΣ _[⊤]_[��] 0 _[∞] Xt_[(] _[τ]_[)] _A_ ( _τ_ ) _dτ_ �. 

Substituting _Xt_[(] _[τ]_[)] from the market-clearing equation (16) into (34), using (5), (6), (30) and (32), and denoting by Θ( _τ_ ) the 1 _×_ ( _K_ + 1) vector (0 _, θ_ 1( _τ_ ) _, .., θK_ ( _τ_ )), we find the following counterpart of (18): 

**==> picture [268 x 21] intentionally omitted <==**

**==> picture [350 x 25] intentionally omitted <==**

Setting the linear terms in _qt_ on both sides of (35) to be equal yields the system of _K_ + 1 first-order linear ODEs 

**==> picture [150 x 11] intentionally omitted <==**

where _M_ is the ( _K_ + 1) _×_ ( _K_ + 1) matrix 

**==> picture [299 x 24] intentionally omitted <==**

Setting the terms that are independent of _qt_ on both sides of (35) to be equal yields the first-order linear ODE 

**==> picture [417 x 24] intentionally omitted <==**

Equations (36) and (38) must be solved with the initial conditions _A_ (0) = _C_ (0) = 0. To solve (36) and (38), 

25 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

we follow the same two steps as in Section 3. The first step is to take the integrals in (36) and (38) as given and solve these equations as linear ODEs with constant coefficients. The solution is in Lemma 3. 

Lemma 3 _Suppose that the matrix M defined in (37) has K_ + 1 _distinct eigenvalues_ ( _ν_ 1 _, .., νK_ +1) _. The function A_ ( _τ_ ) = ( _Ar_ ( _τ_ ) _, Aβ,_ 1( _τ_ ) _, .., Aβ,K_ ( _τ_ )) _[⊤] is given by_ 

**==> picture [314 x 73] intentionally omitted <==**

_where_ ( _{ϕr,k′}k′_ =1 _,..,K, {ϕβ,k,k′}k,k′_ =1 _,..,K_ ) _are scalars derived from the eigenvectors of M . The function C_ ( _τ_ ) _is given by_ 

**==> picture [272 x 25] intentionally omitted <==**

_where χ ≡_ ( _χr, χβ,_ 1 _, .., χβ,K_ ) _[⊤] is the_ ( _K_ + 1) _×_ 1 _vector_ 

**==> picture [253 x 24] intentionally omitted <==**

The second step is to ensure that the solution derived in Lemma 3 is consistent with the value of the integrals. There are ( _K_ +1)[2] integrals in (36). These integrals involve the _K_ +1 functions ( _Ar_ ( _τ_ ) _, {Aβ,k_ ( _τ_ ) _}k_ =1 _,..K_ ), and determine the elements of the ( _K_ + 1) _×_ ( _K_ + 1) matrix _M_ defined in (37). In turn, the eigenvalues and eigenvectors of _M_ determine the solution for ( _Ar_ ( _τ_ ) _, {Aβ,k_ ( _τ_ ) _}k_ =1 _,..K_ ) in Lemma 3, and that solution determines the value of the integrals. This yields a nonlinear system of ( _K_ + 1)[2] equations in the ( _K_ + 1)[2] integrals. Given a solution to that system, the elements ( _χr, χβ,_ 1 _, .., χβ,K_ ) of the vector _χ_ in the solution for _C_ ( _τ_ ) in Lemma 3 can be derived from a linear system of _K_ + 1 equations. 

In the remainder of this section, we show analytically general properties of the model. We focus on the case where there is one demand factor ( _K_ = 1, four nonlinear equations) and omit the subscript _k_ from that factor. We additionally assume that the short rate and the demand factor are independent. This corresponds to the 

26 

D. VAYANOS AND J.-L. VILA 

matrices (Γ _,_ Σ) being diagonal. We denote their diagonal elements by ( _κr, κβ, σr, σβ_ ) _≡_ (Γ1 _,_ 1 _,_ Γ2 _,_ 2 _,_ Σ1 _,_ 1 _,_ Σ2 _,_ 2). The case with one independent demand factor is a natural first case to analyze, and it yields a rich set of results. We analyze the same case numerically in Section 5, where we perform a calibration exercise.[15] We discuss the general case briefly at the end of Section 4.4. 

Two useful assumptions for deriving some of our analytical results are that the functions ( _α_ ( _τ_ ) _, {θk_ ( _τ_ ) _}k_ =1 _,..,K_ ) are exponentials or linear combinations of exponentials. Under these assumptions, the integrals in (36) involve Laplace transforms of the functions ( _Ar_ ( _τ_ ) _, {Aβ,k_ ( _τ_ ) _}k_ =1 _,..K_ ) and of those functions’ pairwise products. Moreover, by multiplying the ODE system (36) by the exponentials in ( _α_ ( _τ_ ) _, {θk_ ( _τ_ ) _}k_ =1 _,..,K_ ) and by the products of these exponentials with the functions ( _Ar_ ( _τ_ ) _, {Aβ,k_ ( _τ_ ) _}k_ =1 _,..K_ ), we find equations that involve the same Laplace transforms. This yields a system of equations in the Laplace transforms, derived in Appendix A for the general case (Lemma A.1). While that system remains nonlinear, a key advantage of the Laplacetransform approach is that we do not need to compute the eigenvalues and eigenvectors of _M_ , which can be real or complex. 

We begin our analytical investigation by showing existence of equilibrium. We take the demand elasticity _α_ ( _τ_ ) to be the declining exponential _α_ ( _τ_ ) = _αe[−][δ][α][τ]_ , where ( _α, δα_ ) are positive constants. We take the impact _θ_ ( _τ_ ) of the single demand factor on the demand intercept to be a difference between two exponentials _θ_ ( _τ_ ) = _θ_ � _e[−][δ][α][τ] − e[−][δ][θ][τ]_[�] , where ( _θ, δθ_ ) are positive constants and _δα < δθ_ . A unit increase in the demand factor _βt_ raises the spot rate for maturity _τ_ in the segmentation equilibrium by 

**==> picture [123 x 26] intentionally omitted <==**

This function has a positive limit at _τ_ = 0 and decreases in _τ_ . 

Theorem 1 ( **Equilibrium Existence** ) _Suppose that there is one demand factor, the matrices_ (Γ _,_ Σ) _are diagonal, α_ ( _τ_ ) = _αe[−][δ][α][τ] and θ_ ( _τ_ ) = _θ_ � _e[−][δ][α][τ] − e[−][δ][θ][τ]_[�] _, where_ ( _α, θ, δα, δθ_ ) _are positive constants and δθ is large. An equilibrium exists under either of the following sufficient conditions:_  _κβ is close to zero._ 

> 15Hayashi (2018) derives two alternative numerical algorithms for solving our model in the case _α_ ( _τ_ ) = 0. Both algorithms discretize the functions ( _Ar_ ( _τ_ ) _, {Aβ,k_ ( _τ_ ) _}k_ =1 _,..K_ ), without imposing the structure derived in Lemma 3. They have the advantage of handling large values of _K_ as easily as small values. 

27 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

 _δα_ ( _δα_ + _κr_ )( _δα_ + _κβ_ ) _>_ 2 _aθσrσβ._ 

_In equilibrium, M_ 1 _,_ 1 _> κr, M_ 1 _,_ 2 _>_ 0 _, M_ 2 _,_ 1 _<_ 0 _and M_ 2 _,_ 2 _>[κ][β][−]_ 2 _[δ][α] ._ 

We complement the existence result in Theorem 1 by computing in Appendix A (Lemma A.2) the equilibrium in closed form when the arbitrageurs’ risk-aversion coefficient _a_ is close to zero or to infinity and other parameters can take any values. For our analysis of _a ≈_ 0 and _a ≈∞_ , we require that _α_ ( _τ_ ) and _[θ]_[(] _τ[τ]_[)] have a positive and a finite limit, respectively, at _τ_ = 0. That restriction is satisfied by the specification in Theorem 1.[16] We next examine how the results of Sections 3.3-3.5 are modified in the presence of demand risk. 

## 4.2. _Carry Trades and Hedging_ 

Demand risk weakens the transmission of short-rate shocks to bond yields. This is because the carry trades through which arbitrageurs transmit the shocks become riskier. To hedge against demand risk, arbitrageurs scale down their carry trades or even convert them into _butterfly trades,_ reversing the sign of their positions for long maturities. Because of hedging, short-rate shocks can move yields for long maturities in the direction opposite to the shocks. 

To explain hedging in our model, suppose as in Section 3.3 that a shock causes the short rate to drop below the value that bond yields would take in the segmentation equilibrium. Arbitrageurs can benefit from the discrepancy between bond yields and the short rate by buying bonds and borrowing short-term. This carry trade leaves them exposed to a rise in the short rate, as in Section 3.3, and to a drop in bond demand by preferred-habitat investors. The importance of demand risk relative to short-rate risk rises with maturity. This is shown in Proposition 5, and can be partly anticipated from the one-factor model, in which short-rate shocks have an effect on yields that declines with maturity, while permanent demand changes have an increasing effect. Because long-maturity bonds are highly exposed to demand risk, arbitrageurs can short-sell them to hedge the demand risk of their aggregate position. Such short-selling occurs when arbitrageurs are sufficiently risk-averse, and causes yields for long maturities to rise despite the drop in current and expected future short rates. Buying intermediate-maturity bonds and short-selling long-maturity ones and very short-maturity ones 

> 16For _a ≈_ 0, our model becomes approximately a one-factor one, with the factor being the short rate. This is because shocks to the demand factors have small effects on bond yields. The effects of demand shocks are characterized by the one-dimensional index derived in Proposition 4, with _κ[∗] r_[=] _[κ][r]_[.][The][only][difference][relative][to][Proposition][4][is][that][yields][for][longer][maturities] may not be the most affected. This is because Proposition 4 assumes permanent demand changes, while shocks to the demand factors mean-revert. 

28 

D. VAYANOS AND J.-L. VILA 

(i.e., borrowing short-term) is a butterfly trade, common in term-structure arbitrage.[17] 

Proposition 5 characterizes the response of yields to short-rate and demand shocks. The proposition assumes _M_ 2 _,_ 1 _<_ 0, a property shown to hold for the equilibrium derived in Theorem 1. The assumptions of Theorem 1 are not needed as long as that property holds. 

The characterization is simple when the two eigenvalues of _M_ are real. The function _Aβ_ ( _τ_ ) is positive, which implies that a drop in demand causes yields for all maturities to rise, and increases in _τ_ . The function _Ar_ ( _τ_ ) is either positive, or switches sign from positive to negative when _τ_ crosses a threshold _τ_ ¯. In the latter case, a drop in the short rate causes yields for maturities _τ > τ_ ¯ to rise. The ratio _A[A] β[r]_[(] ( _[τ] τ_[)] )[decreases][in] _[τ]_[,][which] implies that the effect of demand shocks relative to short-rate shocks rises with maturity. 

When the two eigenvalues of _M_ are complex, the functions ( _Ar_ ( _τ_ ) _, Aβ_ ( _τ_ )) exhibit an oscillating pattern driven by the arbitrageurs’ hedging activity. Following a rise in the short rate, prices of short-maturity bonds drop. Prices of long-maturity bonds can instead rise because arbitrageurs can buy them to hedge demand risk. Long-maturity bonds can thus hedge the short-rate risk of a portfolio with long positions in bonds, and earn negative expected excess returns when arbitrageurs hold such a portfolio in equilibrium. Since arbitrageurs hold long positions when demand by preferred-habitat investors is low, low demand can cause, through the cumulation of negative expected returns, the prices of bonds of even longer (“very long”) maturities to rise. In that case, arbitrageurs do not use the very-long-maturity bonds to hedge demand risk, and those bonds’ prices rise following a drop in the short rate. This yields an oscillating pattern of price sensitivity to the short rate as a function of maturity. The properties shown for real eigenvalues carry through to complex ones for the first half-cycle of the oscillation (which can be longer than the maximum maturity _T_ ). The functions ( _Ar_ ( _τ_ ) _, Aβ_ ( _τ_ )) begin by being increasing in _τ_ . The function _Ar_ ( _τ_ ) eventually reaches a maximum, and the ˆ ˆ function _Aβ_ ( _τ_ ) does so at a larger value _τ_ which marks the end of the first half-cycle. We set _τ_ = _∞_ when the 

> 17An example of a butterfly trade comes from the 2007-2008 financial crisis. Short-rate cuts triggered by the crisis rendered the US term structure steeply upward sloping. Term structure arbitrageurs took the view that forward rates did not drop enough to reflect the low expected future spot rates—the under-reaction result of Proposition 2. For example, a Barclays Capital report by Pradhan (2009), p.2., points out that while the two-year spot rate was 258 bps lower than the ten-year spot rate, the difference between their two-year forward counterparts was only 93bps. The report goes on to advise lending at the two-year rate two years forward and borrowing at the ten-year rate two years forward. Lending at the two-year rate two years forward is a carry trade: it amounts to shorting two-year bonds and buying four-year bonds. Borrowing at the ten-year rate two years forward amounts to buying two-year bonds and shorting twelve-year bonds. That position is layered to the carry trade to hedge term-structure movements at intermediate maturities, and is for a smaller notional amount since the twelve-year bond is more sensitive to such movements than the four-year bond. The overall trade is a butterfly: a short position in two-year bonds, a long position in four-year bonds, and a short position in twelve-year bonds. It exerts upward pressure on the twelve-year spot rate, even though it is triggered by a drop in the short rate. 

29 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

two eigenvalues of _M_ are real. We refer to the largest interval of the form (0 _, τ_ ) over which a given property holds as a maximal interval. 

Proposition 5 ( **Effect of Short-Rate and Demand Shocks** ) _Suppose that there is one demand factor, the matrices_ (Γ _,_ Σ) _are diagonal, and M_ 2 _,_ 1 _<_ 0 _._ 

- _′_ 

-  _If the two eigenvalues of M are real, then Aβ_ ( _τ_ ) _>_ 0 _, A[′] β_[(] _[τ]_[)] _[ >]_[ 0] _[ and]_ � _AAβr_ (( _ττ_ )) � _<_ 0 _. Moreover, Ar_ ( _τ_ ) _>_ 0 _for τ ∈_ (0 _,_ ¯ _τ_ ) _and Ar_ ( _τ_ ) _<_ 0 _for τ ∈_ (¯ _τ, ∞_ ) _, where τ_ ¯ = _∞ when a ≈_ 0 _or α_ ( _τ_ ) = 0 _, and τ_ ¯ _< ∞ when a ≈∞._ 

-  _If the two eigenvalues of M are complex, then Aβ_ ( _τ_ ) _>_ 0 _for τ in a maximal interval_ (0 _, τ_ ¯[¯] ) _, A[′] β_[(] _[τ]_[)] _[ >]_[ 0] _′_ 

- _Ar_ ( _τ_ ) ¯ ˆ ¯ 

- _for τ in a maximal interval_ (0 _,_ ˆ _τ_ ) _, and_ � _Aβ_ ( _τ_ ) � _<_ 0 _for τ ∈_ (0 _,_ ˆ _τ_ ) _, where τ_[¯] _> τ >_ 0 _. If τ_[¯] _< ∞, then Ar_ ( _τ_ ) _>_ 0 _for τ in a maximal interval_ (0 _,_ ¯ _τ_ ) _, where τ_ ¯ _∈_ (0 _, τ_ ¯[¯] ) _._ 

## 4.3. _Bond Risk Premia_ 

Demand risk strengthens the positive premia-slope relationship derived in Section 3.4. Indeed, low demand by preferred-habitat investors implies positive bond risk premia because arbitrageurs must be induced to buy the bonds to make up for the low investor demand. Because of the positive premia, yields are high and the term structure is upward-sloping. 

Proposition 6 computes the FB and CS coefficients _b_ FB and _b_ CS. It shows that _b_ FB is positive and _b_ CS is smaller than one for at least all maturities such that the functions ( _Ar_ ( _τ_ ) _, Aβ_ ( _τ_ )) are positive and _Aβ_ ( _τ_ ) increases in _τ_ , and for all maturities when _a_ is close to zero or to infinity. Moreover, when _a ≈∞_ and the average maturity where demand shocks originate is sufficiently long, _b_ FB exceeds one and increases in _τ_ , while _b_ CS is negative and decreases in _τ_ . 

Proposition 6 ( **Demand Risk Strengthens Positive Premia-Slope Relationship** ) _Suppose that there is one demand factor, the matrices_ (Γ _,_ Σ) _are diagonal, M_ 1 _,_ 2 _≥_ 0 _, M_ 2 _,_ 1 _<_ 0 _and_ ∆ _τ →_ 0 _._ 

-  _The FB regression coefficient in (28) is positive for τ <_ min _{τ,_ ¯ ˆ _τ }, and for all τ when a ≈_ 0 _or a ≈∞. When a ≈∞ and_ 

**==> picture [172 x 28] intentionally omitted <==**

30 

D. VAYANOS AND J.-L. VILA 

_bFB exceeds one and increases in τ ._ 

-  _The CS regression coefficient in (29) is smaller than one for τ <_ min _{τ,_ ¯ ˆ _τ }, and for all τ when a ≈_ 0 _or a ≈∞. When a ≈_ 0 _, bCS is close to one and increases in τ . When a ≈∞ and (43) holds, bCS is negative and decreases in τ ._ 

## 4.4. _Demand Effects_ 

Suppose, as in Section 3.5, that the demand intercept _θ_ 0( _τ_ ) changes to _θ_ 0( _τ_ ) + ∆ _θ_ 0( _τ_ ), where ∆ _θ_ 0( _τ_ ) is a general function of _τ_ . The functions ( _Ar_ ( _τ_ ) _, Aβ_ ( _τ_ )) do not change, and the effects on yields are entirely through _C_ ( _τ_ ). Because there are two risk factors, the effects are represented by two one-dimensional indices. The indices are �0 _∞ θ_ 0( _τ_ ) _Ar_ ( _τ_ ) _dτ_ and �0 _∞ θ_ 0( _τ_ ) _Aβ_ ( _τ_ ) _dτ_ , and relate to the sensitivity of arbitrageurs’ portfolio to the short-rate and the demand factor, respectively. 

While demand effects retain a global flavor because they are represented by only two indices across a continuum of maturities, they become more localized relative to the one-factor case. Recall from Section 3.5 that with one factor, demand changes have the same relative effect across maturities regardless of the maturities where they originate. This independence result does not extend to two factors. The maturities where demand shocks originate matter because they influence how the shocks affect one index relative to the other, and because changes to each index have a different relative effect across maturities. Changes to the demand for long-maturity bonds have a large effect on �0 _∞ θ_ 0( _τ_ ) _Aβ_ ( _τ_ ) _dτ_ relative to �0 _∞ θ_ 0( _τ_ ) _Ar_ ( _τ_ ) _dτ_ , and changes to �0 _∞ θ_ 0( _τ_ ) _Aβ_ ( _τ_ ) _dτ_ have a large effect on long rates relative to short rates. Hence, the effects of long-maturity bond demand are more pronounced at the long end of the term structure. In comparison, changes to the demand for short-maturity bonds have a large relative effect on �0 _∞ θ_ 0( _τ_ ) _Ar_ ( _τ_ ) _dτ_ , and changes to that index have a large relative effect on short rates. Hence, the effects of short-maturity bond demand are more pronounced at the short end. 

The economic intuition is as follows. Suppose that the demand by preferred-habitat investors for longmaturity bonds declines, in which case arbitrageurs take up the slack by purchasing those bonds. Since bonds’ sensitivity to demand shocks relative to short-rate shocks rises with maturity, arbitrageurs’ exposure to demand risk increases significantly, while their exposure to short-rate risk increases more mildly. The expected excess returns that arbitrageurs require to bear demand risk increase significantly as well. Since bonds’ sensitivity to demand shocks rises faster with maturity than their sensitivity to short-rate shocks, 

31 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

long-maturity bonds experience a sharp increase in their expected excess returns relative to short-maturity bonds. Hence, long rates increase sharply. By contrast, when the demand by preferred-habitat investors for short-maturity bonds declines, long rates increase less than short rates. 

To show a formal result on localization, we consider the simple case where the change ∆ _θ_ 0( _τ_ ) represents a decrease in demand for a specific short maturity _τ_ 1 or a specific long maturity _τ_ 2 _> τ_ 1. We denote the resulting changes in the yield _yt_[(] _[τ]_[)] by ∆ _yt,τ_[(] _[τ]_[)] 1[and][∆] _[y] t,τ_[(] _[τ]_[)] 2[,][respectively.] 

Proposition 7 ( **Localization of Demand Effects** ) _When there is one demand factor, a change in the demand intercept from θ_ 0( _τ_ ) _to θ_ 0( _τ_ )+∆ _θ_ 0( _τ_ ) _affects yields only through_ �0 _∞_ ∆ _θ_ 0( _τ_ ) _Ar_ ( _τ_ ) _dτ and_ �0 _∞_ ∆ _θ_ 0( _τ_ ) _Aβ_ ( _τ_ ) _dτ . When additionally the matrices_ (Γ _,_ Σ) _are diagonal, M_ 2 _,_ 1 _<_ 0 _, α_ ( _τ_ ) _is non-increasing, and the change_ ∆ _θ_ 0( _τ_ ) _is a Dirac function with point mass at τ_ 1 _< τ_ ˆ _or at τ_ 2 _∈_ ( _τ_ 1 _,_ ˆ _τ_ ) _,_ 

**==> picture [170 x 15] intentionally omitted <==**

Equation (44) states that the product of the “local” effects that the changes have on the maturity where they originate exceeds the product of the “cross” effects on the other maturity. Local effects are thus stronger than cross effects. 

We expect full localization when there is a large number of demand factors and arbitrageurs are highly risk-averse. Indeed, suppose that a demand shock originating at maturity _τ_ 1 has its largest effect at maturity _τ_ 2 = _τ_ 1. For this to happen, arbitrageurs must hold non-zero positions in at least the bonds of one of the two maturities. Highly risk-averse arbitrageurs, however, hold non-zero positions only if their exposure to all risk factors is zero, which is infeasible with a large number of factors. Proposition 1 implies a full localization result for the effects of short-rate shocks: since the function _Ar_ ( _τ_ ) converges to zero when the arbitrageurs’ riskaversion coefficient _a_ goes to infinity, the effects of short-rate shocks become localized at the zero maturity. We can derive the same localization result with one and two demand factors, using closed-form solutions for the large _a_ limit. Extending the full localization result for the effects of demand shocks requires extending our solutions to a large number of demand factors and is left for future work. 

## 5. CALIBRATION AND POLICY ANALYSIS 

In this section we calibrate our model and analyze the effects of different policies by central banks. Since the model can be given both a nominal and a real interpretation, we calibrate it using nominal yields and then 

32 

D. VAYANOS AND J.-L. VILA 

again using real yields. In all calibrations we assume that there is one demand factor which is independent of the short rate. We leave the correlated case, which seems more relevant for the nominal calibration, for future work. The independent case is a natural first case to investigate, and it yields a remarkably similar analysis of central-bank policies across the nominal and real calibrations. 

## 5.1. _Calibration_ 

The equilibrium term structure is determined by the parameters ( _r, κr, σr_ ) of the short-rate process, the parameters ( _κβ, σβ_ ) of the demand-factor process, the risk-aversion coefficient _a_ of arbitrageurs, and the functions ( _α_ ( _τ_ ) _, θ_ 0( _τ_ ) _, θ_ ( _τ_ )) that describe the demand slope and intercept of preferred-habitat investors. 

The values of ( _r, θ_ 0( _τ_ )) affect only the long-run averages of yields and of agents’ positions. They do not matter for our policy analysis, which concerns how yields and positions respond to shocks. We sketch a calibration of these parameters in Section 5.3, where we compute unconditional moments of bond returns. 

We set _α_ ( _τ_ ) = _αe[−][δ][α][τ]_ and _θ_ ( _τ_ ) = _θ_ ( _e[−][δ][α][τ] − e[−][δ][θ][τ]_ ) for _τ < T_ , and _α_ ( _τ_ ) = _θ_ ( _τ_ ) = 0 for _τ > T_ . This is the same exponential specification as in Theorem 1, except that we take the maximum bond maturity _T_ to be finite. We set _T_ = 30 years, the maximum maturity for U.S. government bonds. 

The values of ( _θ_ ( _τ_ ) _, σβ_ ) matter only through their product because ( _θ_ ( _τ_ ) _, βt_ ) affect the demand of preferredhabitat investors only through their product as well. We can hence normalize _σβ_ to an arbitrary value, and we set it equal to _σr_ . 

We calibrate the remaining eight parameters ( _κr, σr, κβ, a, α, θ, δα, δθ_ ) using U.S. data on bond yields and trading volume, as well as estimates of demand elasticity from the literature. For bond yields, we use the Gurkaynak, Sack and Wright (GKS) datasets, which report daily spot rates extracted from government bond prices. The dataset on nominal yields goes from June 1961 to the present. We start our main sample of nominal yields in November 1985, because this is the earliest when all maturities from one to 30 years are included, and end it in January 2020. The dataset on real yields goes from January 1999 to the present, and includes all maturities from two to 20 years. We start our sample of real yields in January 1999 and end it in January 2020. In addition to our main sample of nominal yields, we consider a sub-sample covering the same period as the sample of real yields. We source nominal and real yields at the end of each month. For bond trading volume, we use the FR 2004 dataset, which reports daily volume by primary dealers in the Treasury market, split into buckets based on the bonds’ remaining time to maturity. Volume on real bonds 

33 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

(TIPS) is approximately 3% of total volume, and is not split into maturity buckets until March 2020. For that reason, we use the volume split for nominal bonds in all calibrations. We do not include T-bills in our volume calculations because of their special features (e.g., extensive use as collateral). T-bills are also not included in the GKS datasets. The dataset on volume goes from April 2013 to the present. We end it in January 2020, and use averages within that period in all calibrations. For demand elasticity, we use estimates from Krishnamurthy and Vissing-Jorgensen (KVJ 2012).[18] 

Table I reports the calibrated parameters and the empirical moments used to determine them, for the main sample of nominal yields. Tables C.I and C.II in Appendix C report the same information for the subsample of nominal yields and the sample of real yields, respectively. We express yields and their volatilities in percentage terms throughout this section, e.g., a yield of 0.02 is expressed as 2. 

We determine the first seven parameters in Table I by equating the first seven empirical moments to their model-generated counterparts. This requires solving a seven-equation non-linear system. The formulas for the seven model-generated moments are in Appendix C. The seven moments concern volatilities and correlations of yields and yield changes, and fractions of volume at different maturity buckets. Data on yields and relative volume cannot identify the arbitrageurs’ risk-aversion coefficient _a_ separately from the parameters ( _α, θ_ ) that characterize the slope of preferred-habitat demand and the magnitude of demand shocks, respectively. Only the products ( _aα, aθ_ ) can be identified. Intuitively, yields can be volatile because arbitrageurs are highly risk-averse (high _a_ ) and demand shocks are small (low _θ_ ), or because arbitrageurs are less risk-averse and demand shocks are larger.[19] We determine _α_ , the eighth parameter in Table I, based on KVJ’s estimates, and deduce ( _a, θ_ ) from the products ( _aα, aθ_ ). 

The empirical moment next to each parameter in Table I is the one identifying that parameter. We address identification formally in Appendix C, where we compute a seven-by-seven table of elasticities of the first seven moments with respect to the first seven parameters. The elasticity table validates the mapping in Table I except for the fourth and fifth moments, for which cross-effects from the fifth and fourth parameter, respectively, are important. 

> 18The dataset of nominal yields is available at `https://www.federalreserve.gov/pubs/feds/2006/200628/200628abs.html` and is described in Gurkaynak, Sack, and Wright (2007). The dataset of real yields is available at `https://www.federalreserve.gov/pubs/feds/2008/200805/200805abs.html` . The FR 2004 dataset (which reports additional information to volume) is available at `https://www.newyorkfed.org/markets/gsds/search` . 

> 19Formally, (37) shows that the matrix _M_ that determines ( _Ar_ ( _τ_ ) _, Aβ_ ( _τ_ )) through the ODE (36) depends on ( _a, α, θ_ ) only through the products ( _aα, aθ_ ). Hence, ( _Ar_ ( _τ_ ) _, Aβ_ ( _τ_ )) have that property as well, and so do the moments of returns and volume computed in Appendix C. 

34 

D. VAYANOS AND J.-L. VILA 

TABLE I 

Calibration of model parameters for the main sample of nominal yields. 

|**Parameter**|**Value**||**Empirical moment**|**Empirical moment**|**Value**|
|---|---|---|---|---|---|
|||||||
|_κr_<br>Mean-reversion of _rt_<br>_σr_<br>Difusion of _rt_<br>_κβ_<br>Mean-reversion of _βt_<br>_aθ_<br>Arb. risk-aversion<br>_×_ PH demand shock<br>_aα_<br>Arb. risk-aversion<br>_×_ PH demand slope<br>_δα_<br>PH demand shock<br>– short maturities<br>_δθ_<br>PH demand shock<br>– long maturities<br>_α_<br>PH demand slope|0.125<br>0.0146<br>0.053<br>3155<br>35.3<br>0.297<br>0.307<br>5.21||�<br>Var<br>�<br>_y_(1)<br>_t_<br>�<br>Volatility 1-year yield<br>– Levels<br>�<br>Var<br>�<br>_y_(1)<br>_t_+1 _−y_(1)<br>_t_<br>�<br>Volatility 1-year yield<br>– Annual changes<br>1<br>30<br>�30<br>_τ_=1<br>�<br>Var<br>�<br>_y_(_τ_)<br>_t_<br>�<br>Volatility _τ_-year yield<br>– Levels, average over _τ_<br>1<br>30<br>�30<br>_τ_=1<br>�<br>Var<br>�<br>_y_(_τ_)<br>_t_+1 _−y_(_τ_)<br>_t_<br>�<br>Volatility _τ_-year yield<br>– Annual changes, average over _τ_<br>1<br>30<br>�30<br>_τ_=1 Corr<br>�<br>_y_(1)<br>_t_+1 _−y_(1)<br>_t_<br>_, y_(_τ_)<br>_t_+1 _−y_(_τ_)<br>_t_<br>�<br>Correlation 1-year yield with _τ_-year yield<br>– Annual changes, average over _τ_<br>�<br>0_<τ≤_2 Volume(_τ_)<br>�<br>0_<τ≤_30 Volume(_τ_)<br>Relative volume for maturities _τ ∈_(0_,_2]<br>�<br>11_<τ≤_30 Volume(_τ_)<br>�<br>0_<τ≤_30 Volume(_τ_)<br>Relative volume for maturities _τ ∈_(11_,_30]<br>Estimate in KVJ 2012||2.62<br>1.27<br>2.20<br>0.796<br>0.504<br>0.199<br>0.094<br>-0.746|



35 

## A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

The mean-reversion _κr_ and diffusion _σr_ of the short rate _rt_ have their largest effect on the one-year yield _yt_[(1)] . An increase in _σr_ raises the volatility of that yield and the volatility of yield changes. A decrease in _κr_ raises the yield’s volatility, but has a weaker effect on the volatility of yield changes because it implies that the short rate mean-reverts more slowly. Since shocks to the demand factor have a weak effect on the one-year yield, the volatility of that yield identifies _κr_ , and the volatility of annual changes to that yield identifies _σr_ . 

The mean-reversion _κβ_ of the demand factor _βt_ and the magnitude parameter _θ_ of demand shocks have their largest effect on long-maturity yields. As with ( _κr, σr_ ), the volatility of yields identifies _κβ_ and the volatility of annual changes to yields identifies _aθ_ . We average volatilities across all maturities. Using volatilities at long maturities only does not sharpen the identification. 

The slope parameter _α_ of preferred-habitat demand affects how shocks to the short rate are transmitted to longer maturities. An increase in _α_ weakens the transmission (Proposition 2), and this makes yield changes at short and long maturities less correlated. Hence, the correlation between annual changes to the one-year yield and to other yields identifies _aα_ . (As we explain in Appendix C, however, there are important crosseffects from _aθ_ to correlation and from _aα_ to volatility.) As with ( _κβ, θ_ ), we average the correlation across all maturities 

The parameters ( _δα, δθ_ ) control the maturities where demand shocks originate, via the specification _θ_ ( _τ_ ) = _θ_ ( _e[−][δ][α][τ] −e[−][δ][θ][τ]_ ). Hence, they affect how volume is split across maturities. An increase in _δα_ raises the relative volume for short maturities and lowers that for long maturities. An increase in _δθ_ has the same effects, with the decline in long-maturity volume being relatively more pronounced. Hence, the relative volume for maturities two years and below identifies _δα_ , and the relative volume for maturities eleven years and above identifies _δθ_ . 

Our moment-matching exercise indicates slow mean-reversion for the short rate ( _κr_ = 0 _._ 125, half-life of shocks 5.55 years) and even slower mean-reversion for the demand factor ( _κβ_ = 0 _._ 053, half-life of shocks 13.1 years). The corresponding parameters for the sub-sample of nominal yields and the sample of real yields are two to three times larger, implying faster mean-reversion. In all samples, demand shocks originate at short and intermediate maturities, consistent with the fact that only 9.4% of volume concerns bonds with remaining time to maturity longer than 11 years. 

Figure 1 compares the empirical moments, represented by the black crosses, to the model-generated ones, represented by the red solid lines, for the main sample of nominal yields. Figures C.1 and C.2 in Appendix C show the same comparisons for the sub-sample of nominal yields and the sample of real yields, respectively. 

36 

D. VAYANOS AND J.-L. VILA 

**==> picture [386 x 464] intentionally omitted <==**

**----- Start of picture text -----**<br>
3 1.5<br>2.5<br>2 1<br>1.5<br>1 0.5<br>0.5<br>0 0<br>0 5 10 15 20 25 30 0 5 10 15 20 25 30<br>Maturity (years) Maturity (years)<br>1 1.5<br>0.8<br>1<br>0.6<br>0.4<br>0.5<br>0.2<br>0 0<br>0 5 10 15 20 25 30 0 5 10 15 20 25 30<br>Maturity (years) Maturity (years)<br>3.5 1<br>3 0.5<br>2.5 0<br>2 -0.5<br>1.5 -1<br>1 -1.5<br>0.5 -2<br>0 -2.5<br>0 5 10 15 20 25 30 0 5 10 15 20 25 30<br>Maturity (years) Maturity (years)<br>Volatility of yield -- Levels<br>Volatility of yield -- Annual changes<br>Correlation with one-year yield -- Annual changes First principal component -- Annual yield changes<br>Fama-Bliss regression coefficient<br>Campbell-Shiller regression coefficient<br>**----- End of picture text -----**<br>


Figure 1.— Model-generated and empirical moments for the main sample of nominal yields. 

37 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

The comparisons are remarkably similar across the three figures. The figures depend only on the first seven parameters in Table I, and not on the separate values of _a_ and ( _α, θ_ ). 

The top two panels in Figure 1 report the volatility of yields and the volatility of annual yield changes, as functions of maturity. The model-generated moments coincide with the empirical ones for the one-year maturity and on average, by construction. While the empirical moments are decreasing functions of maturity, the model-generated ones are inverse hump-shaped. The inverse hump shape seems to be driven by the independence between the short rate and the demand factor, as these factors have their largest effects at different ends of the term structure. The middle-left panel reports the correlation between annual changes to the one-year yield and to other yields, as function of maturity. The model-generated moments coincide with the empirical ones on average, by construction. 

The remaining panels in Figure 1 report moments not used in the calibration. The middle-right panel reports the first principal component of annual yield changes as function of maturity, scaled to one for the one-year maturity. The model-generated moments are close to the empirical ones, and so is the fraction of variation explained by the first principal component (76.5% in the model and 81.3% in the data). Hence, our calibration captures closely the empirical factor structure of yields. 

The bottom two panels in Figure 1 report the coefficients of the FB and CS regressions (28) and (29), respectively, with ∆ _τ_ = 1 (returns and yield changes are evaluated over one year). The model generates less predictability than is found in the data, especially for long maturities. For those maturities, the modelgenerated predictability, as measured by the deviation between the FB/CS coefficients and their EH value, is about 60% of its empirical counterpart. The model-generated coefficients have the same monotonicity as in the data. If the model is calibrated to match the FB/CS coefficients instead of the volatility of annual yield changes, then it overshoots that volatility for long maturities, because _aθ_ must take a larger value. 

To determine the slope parameter _α_ of preferred-habitat demand, we use KVJ’s estimates of the elasticity of the demand for government debt. KVJ regress the yield spread between long-maturity AAA-rated corporate bonds and government bonds on the logarithm of government debt to GDP, and find a coefficient of -0.746 (Table 1, Panel A). Hence, a 0.01 (1 bp) drop in the yield spread is associated with a 0.0134 (= 00 _.._ 74601[) increase] in the logarithm of debt to GDP. Assuming that debt to GDP takes originally its average value, which is 43.9% in KVJ’s sample (1919-2008), it increases by 0.0059 (= 43 _._ 9% _×_ ( _e_[0] _[.]_[0134] _−_ 1)). To map this estimate into our model, we interpret the increase in debt to GDP as the slope of preferred-habitat demand for government 

38 

D. VAYANOS AND J.-L. VILA 

debt. We also assume that the drop in the yield spread results from an increase in government bond yields across all maturities, and use GDP as the unit of account. KVJ’s estimate implies _α_ = 5 _._ 21. 

The value _α_ = 5 _._ 21 is an upper bound for two reasons. First, instrumental-variables estimation of the KVJ regression generates a more negative coefficient and hence a smaller slope for preferred-habitat demand. Second, our model takes as given the returns that preferred-habitat investors earn outside the government bond market (Appendix B). These returns, however, could change in equilibrium when government bond yields change, resulting in a lower effective demand elasticity. In the extreme case where returns outside the government bond market move one-to-one with government bond yields, a change in these yields should not affect preferred-habitat demand, resulting in an effective slope of zero. In the intermediate case where returns outside the government bond market adjust by _x ∈_ (0 _,_ 1), the effective slope is _α_ (1 _− x_ ). 

For _α_ = 5 _._ 21 and _aα_ = 35 _._ 3, the coefficient of arbitrageur risk aversion is _a_ = 6 _._ 78. To map _a_ into a coefficient of relative risk aversion (RRA), we recall that if arbitrageurs have wealth _W_ and a VNM utility function _U_ , then _a_ = _−[U] U[ ′′][′]_ ([(] _W[W]_ )[)][.][Hence,][the][coefficient][of][RRA][is] _[γ]_[=] _[−][U] U[ ′′]_[(] _[′][W]_ ( _W_[)] ) _[W]_ = _aW_ . The macro-finance literature generally assumes that _γ_ is larger than one and does not exceed ten. For _γ_ = 2 and _a_ = 6 _._ 78, arbitrageur wealth is _W_ = 29 _._ 5%, which is 29.5% of GDP since we are using GDP as the unit of account. Such a value seems large. Suppose that we identify arbitrageurs with hedge funds, which are sophisticated investors with relatively broad mandates. The assets of hedge funds in the fixed-income, macro and balanced categories in the last quarter of 2019 added up to $ 1.2 trillion, which was 5.6% (= 211 _.._ 422[) of U.S. GDP in that] year.[20] Smaller values of _W_ correspond to smaller values of _α_ since _W_ is proportional to _α_ holding ( _aα, γ_ ) fixed. Since smaller values seem plausible for both _W_ and _α_ , for separate reasons for each parameter, we use a parameter range. We use _α_ = 5 _._ 21 as the upper bound of the range for _α_ , and _α_ = 1 _._ 04 as the lower bound. The lower bound corresponds to an _x_ = 80% adjustment of returns outside the government-bond market to government-bond yields.[21] The upper bound _α_ = 5 _._ 21 corresponds to an upper bound 29.5% for _W_ and a lower bound 6.78 for _a_ . The lower bound _α_ = 1 _._ 04 corresponds to a lower bound 5.9% for _W_ and an upper bound 33.9 for _a_ . 

> 20See `https://www.barclayhedge.com/solutions/assets-under-management/hedge-fund-assets-under-management/` . 

> 21Duffee (1998) finds that a unit drop in the Treasury bill rate causes the spread between corporate and government bonds to rise by values ranging from 0.02 for intermediate-term AAA-rated corporate bonds to 0.42 for long-term BBB-rated bonds. An 80% adjustment of corporate bond yields to government bond yields (i.e., a rise in the spread by 0.2) lies within these estimates. 

**==> picture [436 x 167] intentionally omitted <==**

**----- Start of picture text -----**<br>
A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 39<br>0.5 0.5<br>Forward guidance Forward guidance<br>Forward guidance EH Forward guidance EH<br>0 0<br>-0.5 -0.5<br>-1 -1<br>-1.5 -1.5<br>-2 -2<br>0 5 10 15 20 25 30 0 5 10 15 20 25 30<br>Maturity (years) Maturity (years)<br>Yield change Yield change<br>**----- End of picture text -----**<br>


Figure 2.— Effect of a forward-guidance announcement about the path of short rates, for the calibration based on the main sample of nominal yields. 

## 5.2. _Policy Analysis_ 

The first policy that we analyze is a forward-guidance announcement about the path of short rates. We model this announcement as a change ∆ _r_ in the long-run mean _r_ of the short rate _rt_ . We assume that the change is unanticipated, takes place at time zero, and reverts deterministically to zero at a rate _κr_ ~~[.]~~ 

Figure 2 shows the announcement’s effect on the term structure at time zero, for the calibration based on the main sample of nominal yields. The figures for the other two calibrations, and the equations describing the announcement’s effect, are in Appendix C. In each panel of Figure 2, the red solid line represents the announcement’s effect, and the red dashed line represents the same effect when arbitrageurs are risk-neutral and the EH holds. The change ∆ _r_ is negative, i.e., the announcement is that future short rates will be lower, and is set to -4 (-400 bps). The change reverts to zero at the rate _κr_[=][0] _[.]_[1][(half-life][6.93][years)][in][the][left] panel and _κr_[= 0] _[.]_[2][(half-life][3.47][years)][in][the][right][panel.][When] _[κ] r_[= 0] _[.]_[1,][yields][are][more][affected][because] the same is true for expected future short rates. 

For both values of _κr_ ~~[,]~~[ yields under-react relative to their EH counterparts. This reflects the under-reaction] result of Proposition 2. The extent of under-reaction increases with maturity. When _κr_[= 0] _[.]_[1,][under-reaction] is 25.6% for the two-year yield, 35.1% for the five-year yield, 49.6% for the ten-year yield, 76.1% for the twenty-year yield, and 102.6% for the thirty-year yield. When _κr_[= 0] _[.]_[2,][these][numbers][rise][to][25.7%,][35.7%,] 51.6%, 81.6%, and 111.4%, respectively. Thus, forward guidance is effective in changing yields for short maturities, but less so for longer maturities. To engineer a decline in the ten-year yield by 0.5 (50 bps), for 

40 

**==> picture [119 x 6] intentionally omitted <==**

**----- Start of picture text -----**<br>
D. VAYANOS AND J.-L. VILA<br>**----- End of picture text -----**<br>


**==> picture [400 x 147] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 0<br>-0.5 -0.5<br>-1 -1<br>-1.5 -1.5<br>2-yr 2-yr<br>5-yr 5-yr<br>-2 10-yr -2 10-yr<br>20-yr 20-yr<br>30-yr 30-yr<br>QE mix QE mix<br>-2.5 -2.5<br>0 5 10 15 20 25 30 0 5 10 15 20 25 30<br>Maturity (years) Maturity (years)<br>Yield change Yield change<br>**----- End of picture text -----**<br>


Figure 3.— Effect of QE, for the calibration based on the main sample of nominal yields. 

example, central banks need to lower the average of expected short rates over the next ten years by about twice as much (100 bps). The calibration based on the sample of real yields generates a similar number. The calibration based on the sub-sample of nominal yields implies instead that the average of expected short rates must drop by about three times as much (150 bps). 

The second policy that we analyze is QE. We assume that QE purchases concern government bonds only, and we model them as a decrease ∆ _θ_ 0( _τ_ ) in the intercept of preferred-habitat demand. (Equation (5) defines the demand intercept with a negative sign.) We assume that the decrease is unanticipated, takes place at time zero, and reverts deterministically to zero at a rate _κθ_ . 

Figure 3 shows the effect of QE on the term structure at time zero, for the calibration based on the main sample of nominal yields. The figures for the other two calibrations, and the equations describing the effect of QE, are in Appendix C. In each panel of Figure 3, the red, green, light blue (cyan), blue and black solid lines represent the effect of QE purchases of two-, five-, ten-, twenty- and thirty-year bonds, respectively. The black dashed line represents the effect of QE purchases that conform to the maturity distribution used by the Fed during QE1, as reported in D’Amico and King (2013). All lines are drawn for a change ∆ _θ_ 0( _τ_ ) in _∞_ the intercept of preferred-habitat demand that satisfies �0 ∆ _θ_ 0( _τ_ ) _dτ_ = _−_ 0 _._ 12, i.e., QE purchases are 12% of GDP. This is approximately the value of government bonds purchased by the Fed during QE1, QE2 and QE3. The demand change mean-reverts to zero at the rate _κr_[= 0] _[.]_[1 (half-life 6.93 years) in the left panel and] _κr_[= 0] _[.]_[2][(half-life][3.47][years)][in][the][right][panel.] 

41 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

Figure 3 is the only one in this section that depends on the separate values of _a_ and ( _α, θ_ ) rather than only on the products ( _aθ, aα_ ). An increase in the coefficient of arbitrageur risk aversion _a_ holding ( _aθ, aα_ ) constant results in a proportionate increase in the effects of QE. Relative effects across maturities do not change, i.e., Figure 3 looks the same after rescaling the _y_ -axis. We use the value of _a_ that generates the average effect across the lower bound _a_ = 6 _._ 78 and the upper bound _a_ = 33 _._ 9. 

The effects of QE on the term structure are larger when _κθ_ = 0 _._ 1, i.e., when QE is unwound over a longer period. Intuitively, QE lowers the yield of a bond because it lowers the risk premia that arbitrageurs require to hold the bond. Moreover, the yield depends not only on the risk premium that arbitrageurs require in the current instant but on an average of risk premia during the bond’s life. When QE is expected to be unwound more slowly, risk premia in that average are impacted more. 

The effects of QE have a global flavor as in Proposition 4, with some localization as in Proposition 7. Consistent with Proposition 4, an increase in demand for bonds with longer maturities generates a larger downward shift in the term structure. For example, the term structure shifts downward more when QE purchases concern thirty-year bonds than when they concern two-year bonds. That downward shift, however, is not larger across all maturities: yields for maturities ranging from one to three years are more sensitive to purchases of two-year bonds than of thirty-year bonds. More generally, and consistent with Proposition 7, an increase in demand for bonds with short (long) maturities has more pronounced effects at the short (long) end of the term structure. For example, purchases of two- and five-year bonds have an effect that peaks at short and intermediate maturities, while purchases of twenty- and thirty-year bonds have an effect that peaks at long maturities. These features are robust to different values of _κθ_ . 

The effects of QE in Figure 3 are somewhat smaller than in the literature. Wiliams (2014) summarizes a number of QE studies in the U.S. as suggesting that bond purchases of $ 600 billion by the Fed reduced the ten-year yield by 0.15-0.25 (15-25 bps). Taking U.S. GDP at that time to be $ 15 trillion, the $ 600 billion purchases are 4% of GDP. Hence, QE purchases of 12% of GDP should reduce the ten-year yield by 0.450.75. The corresponding effect in Figure 3, in the case where the maturities of QE purchases conform to the distribution used by the Fed during QE1, is 0.24 when _κθ_ = 0 _._ 1 and 0.19 when _κθ_ = 0 _._ 2. When _κθ_ = 0 _._ 1, the range of the effect between the upper and lower bound of _α_ is 0.08-0.39. The calibration based on the subsample of nominal yields generates the range 0.11-0.54, and that based on the sample of real yields generates 0.09-0.44. 

The discrepancy between our calibrations and the estimates from QE studies could arise because some of 

D. VAYANOS AND J.-L. VILA 

## 42 

the observed effect of QE was due to forward guidance about the path of short rates. Additionally, arbitrageur risk aversion during the QE period could have been larger than average because of capital losses and tighter regulation. The latter explanation is consistent with the calibration based on the sub-sample of nominal yields generating larger effects than the one based on the main sample. 

Figure 3 suggests that central banks seeking to maximize the effects on QE on yields should concentrate their purchases at long maturities. Moreover, such purchases have particularly large effects on long-maturity yields. In the extreme case where QE purchases of 12% of GDP are concentrated at the thirty-year maturity, and where _κθ_ = 0 _._ 1, the ten-year yield drops by 0.66 (instead of 0.24, under the maturity distribution used by the Fed during QE1) and the thirty-year yield drops by 2.51 (instead of 0.29). Of course, it is not possible to buy 12% of GDP worth of thirty-year bonds because their supply is below that amount. 

Even less extreme tilts towards long maturities, in a way consistent with available supply, can generate sizeable effects. The Fed’s purchases during QE1 incorporated a mild tilt: the average maturity of purchased bonds was 6.5 years, while that of all available coupon bonds was 5.7 years. To evaluate the effects of a stronger tilt, suppose that the Fed did not change the total value of its purchases during QE1 but bought 15% of all available supply in any given maturity before moving to a shorter maturity (hence not buying at all short maturities). The ceiling of 15% is not overly high: D’Amico and King (2013) report that it was exceeded for the 6-8 and 10-12 maturity buckets. Under the modified maturity distribution, QE purchases of 12% of GDP lower the 10-year yield by 0.33 (instead of 0.24) and the thirty-year yield by 0.59 (instead of 0.29). 

## 5.3. _Unconditional Moments_ 

To compute unconditional moments of bond returns, we must choose values for ( _r, θ_ 0( _τ_ )). We assume that _θ_ 0( _τ_ ) is proportional to _θ_ ( _τ_ ), thus setting _θ_ 0( _τ_ ) = _θ_ 0( _e[−][δ][α][τ] − e[−][δ][θ][τ]_ ) for _τ < T_ , and _θ_ 0( _τ_ ) = 0 for _τ > T_ . We determine ( _r, θ_ 0) by equating empirical averages of yields to their model-generated counterparts. Since the estimation concerns first moments, we use the longest period available in the GKS dataset: we focus on nominal yields and start the sample from June 1961. The empirical average of the one-year yield is 5.01. The empirical average of the seven-year yield, which is the longest maturity covered during the entire sample period, is 5.90. Our model matches these moments when ( _r, aθ_ 0) = (4 _._ 80 _,_ 289). 

The model-generated average yield rises with maturity, from 5.01 for the one-year bond to 6.99 for the 

43 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

thirty-year bond. The unconditional expected excess return rises with maturity as well, from 0.40% for the one-year bond to 5.08% for the thirty-year bond. The unconditional Sharpe ratio drops from 0.320 for the one-year bond to 0.206 for the thirty-year bond, but does so non-monotonically, by first rising until the seven-year maturity to 0.365. The rise in expected return with maturity reflects the rise in the yield, and is consistent with the empirical evidence. Empirical Sharpe ratios, by contrast, decline with maturity across the entire maturity range.[22] The increase in the Sharpe ratio that our model generates for short maturities reflects the inverse hump shape of volatility shown in Figure 1, and seems to be driven by the independence between the short rate and the demand factor. The unconditional correlation between bond returns and the stochastic discount factor rises from 0.842 for the one-year bond to one for the seven-year bond, and subsequently drops to 0.563 for the thirty-year bond. The formulas for the model-generated moments are in Appendix C. 

## 6. CONCLUSION 

We model the term structure of interest rates that results from the interaction between investors with preferences for specific maturities and risk-averse arbitrageurs. Our model formalizes the preferred-habitat view of the term structure and embeds it into a modern no-arbitrage framework. We use our model to study three main questions: how shocks to the short rate, including monetary-policy actions by central banks, are transmitted to long rates; how bond risk premia depend on the shape of the term structure; and how changes in preferred-habitat demand, including large-scale bond purchases by central banks, affect the term structure. We provide qualitative answers as well as quantitative ones through a calibration exercise. Our approach can be extended in a number of directions. One direction is to derive optimal debt issuance by governments or corporations when investors have preferences for specific maturities. Work along these lines includes Greenwood, Hanson, and Stein (2010), Guibaud, Nosbusch, and Vayanos (2013) and Bigio, Nuno, and Passadore (2019). Another direction is to broaden the asset-pricing implications by allowing arbitrageurs to trade additional assets. Work along these lines includes Gourinchas, Ray, and Vayanos (2020) and Greenwood, Hanson, Stein, and Sunderam (2020), who study the joint determination of bond prices and exchange rates. A third direction is to analyze broader macro-economic settings, in which term-structure shifts affect investment and output. Work along these lines includes Ray (2019), who embeds our model within a New Keynesian 

> 22For evidence on how bond expected returns and Sharpe ratios vary with maturity see, for example, Duffee (2010) and Frazzini and Pedersen (2014). 

44 

## D. VAYANOS AND J.-L. VILA 

framework. 

## REFERENCES 

- Amihud, Y., and H. Mendelson (1991): “Liquidity, Maturity, and the Yield on US Treasury Securities,” _Journal of Finance_ , 46, 479–486. 

- Andres, J., D. Lopez-Salido, and E. Nelson (2004): “Tobin’s Imperfect Asset Substitution in Optimizing General Equilibrium,” _Journal of Money, Credit and Banking_ , 36(4), 665–690. 

- Banerjee, S., and J. Graveline (2013): “The Cost of Short-Selling Liquid Securities,” _Journal of Finance_ , 68(2), 637–664. 

- Barberis, N., and A. Shleifer (2003): “Style Investing,” _Journal of Financial Economics_ , 68, 261–199. 

- Berends, K., R. McMenamin, T. Plestis, and R. Rosen (2013): “The Sensitivity of Life Insurance Firms to Interest Rate Changes,” _Economic Perspectives_ , 37(Q II), 47–78. 

- Bigio, S., G. Nuno, and J. Passadore (2019): “A Framework for Debt-Maturity Management,” Working paper, UCLA. 

- Buraschi, A., and A. Jiltsov (2007): “Habit Formation and Macroeconomic Models of the Term Structure of Interest Rates,” _Journal of Finance_ , 62, 3009–3063. 

- Campbell, J., and R. Shiller (1991): “Yield Spreads and Interest Rate Movements: A Bird’s Eye View,” _Review of Economic Studies_ , 58, 495–514. 

- Christensen, J., and G. Rudebusch (2012): “The Response of Interest Rates to US and UK Quantitative Easing,” _Economic Journal_ , 122(564), F385–F414. 

- Cochrane, J. (1999): “New facts in finance,” _Economic Perspectives_ , (Q III), 36–58. 

- (2008): “Comments on ‘Bond Supply and Excess Bond Returns’ by Robin Greenwood and Dimitri Vayanos,” Working 

- paper, University of Chicago. 

- Cochrane, J., and M. Piazzesi (2005): “Bond Risk Premia,” _American Economic Review_ , 91, 138–160. 

- Cox, J., J. Ingersoll, and S. Ross (1985): “A Theory of the Term Structure of Interest Rates,” _Econometrica_ , 53, 385–408. 

- Culbertson, J. (1957): “The Term Structure of Interest Rates,” _Quarterly Journal of Economics_ , 71, 485–517. 

- Dai, Q., and K. Singleton (2002): “Expectations Puzzles, Time-Varying Risk Premia, and Affine Models of the Term Structure,” _Journal of Financial Economics_ , 63(3), 415–441. 

- D’Amico, S., and T. King (2013): “Flow and Stock Effects of Large-Scale Treasury Purchases: Evidence on the Importance of Local Supply,” _Journal of Financial Economics_ , 108(2), 425–448. 

- Duffee, G. (1998): “The Relation Between Treasury Yields and Corporate Bond Yield Spreads,” _Journal of Finance_ , 53, 2225–2241. 

   - (2002): “Term Premia and Interest Rate Forecasts in Affine Models,” _Journal of Finance_ , 57, 405–443. 

45 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

   - (2010): “Sharpe Ratios in Term Structure Models,” Working paper, Johns Hopkins University. 

- Duffie, D. (1996): “Special Repo Rates,” _Journal of Finance_ , 51, 493–526. 

- Duffie, D., and R. Kan (1996): “A Yield-Factor Model of Interest Rates,” _Mathematical Finance_ , 6(4), 379–406. 

- Fama, E., and R. Bliss (1987): “The Information in Long-Maturity Forward Rates,” _American Economic Review_ , 77(4), 680–692. 

- Frazzini, A., and L. H. Pedersen (2014): “Betting Against Beta,” _Journal of Financial Economics_ , 111(1), 1–25. 

- Gabaix, X. (2012): “Variable Rare Disasters: An Exactly Solved Framework for Ten Puzzles in Macro-Finance,” _Quarterly Journal of Economics_ , 127(2), 645–700. 

- Gabaix, X., A. Krishnamurthy, and O. Vigneron (2007): “Limits of Arbitrage: Theory and Evidence from the MortgageBacked Securities Market,” _Journal of Finance_ , 62(2), 557–595. 

- Gabaix, X., and M. Maggiori (2015): “International Liquidity and Exchange Rate Dynamics,” _Quarterly Journal of Economics_ , 130(3), 1369–1420. 

- Gagnon, J., M. Raskin, J. Remache, and B. Sack (2011): “The Financial Market Effects of the Federal Reserve’s Large-Scale 

- Asset Purchases,” _International Journal of Central Banking_ , 7(1), 3–43. 

- Garbade, K., and M. Rutherford (2007): “Buybacks in Treasury Cash and Debt Management,” Staff report 304,, Federal Reserve Bank of New York. 

- Garleanu, N., L. Pedersen, and A. Poteshman (2009): “Demand-Based Option Pricing,” _Review of Financial Studies_ , 22(10), 4259–4299. 

- Gorodnichenko, Y., and W. Ray (2018): “Unbundling Quantitative Easing: Taking a Cue from Treasury Auctions,” Working paper, UC Berkeley. 

- Gourinchas, P.-O., W. Ray, and D. Vayanos (2020): “A Preferred-Habitat Model of Term Premia and Currency Risk,” Working paper, UC Berkeley. 

- Greenwood, R. (2005): “Short- and Long-term Demand Curves for Stocks: Theory and Evidence on the Dynamics of Arbitrage,” _Journal of Financial Economics_ , 75, 607–649. 

- Greenwood, R., S. Hanson, and J. Stein (2010): “A Gap-Filling Theory of Corporate Debt Maturity Choice,” _Journal of Finance_ , 65(3), 993–1028. 

- Greenwood, R., S. Hanson, J. Stein, and A. Sunderam (2020): “A Quantity-Driven Theory of Term Premiums and Exchange Rates,” Working paper, Harvard Business School. 

- Greenwood, R., and D. Vayanos (2010): “Price Pressure in the Government Bond Market,” _American Economic Review, Papers and Proceedings_ , 100(2), 585–590. 

   - (2014): “Bond Supply and Excess Bond Returns,” _Review of Financial Studies_ , 27(3), 663–713. 

- Gromb, D., and D. Vayanos (2010): “Limits of Arbitrage,” _Annual Review of Financial Economics_ , 2, 251–275. 

46 

D. VAYANOS AND J.-L. VILA 

- Guibaud, S., Y. Nosbusch, and D. Vayanos (2013): “Bond Market Clienteles, the Yield Curve, and the Optimal Maturity Structure of Government Debt,” _Review of Financial Studies_ , 26, 1914–1961. 

- Gurkaynak, R., B. Sack, and J. Wright (2007): “The US Treasury Yield Curve: 1961 to the Present,” _Journal of Monetary Economics_ , 54(8), 2291–2304. 

- Hamilton, J., and C. Wu (2012): “The Effectiveness of Alternative Monetary Policy Tools in a Zero Lower Bound Environment,” _Journal of Money, Credit and Banking_ , 44, 3–46. 

- Hanson, S. (2014): “Mortgage convexity,” _Journal of Financial Economics_ , 113(2), 270–299. 

- Hau, H. (2011): “Global versus Local Asset Pricing: A New Test of Market Integration,” _Review of Financial Studies_ , 24(12), 3891–3940. 

- Hayashi, F. (2018): “Computing Equilibrium Bond Prices in the Vayanos-Vila Model,” _Research in Economics_ , 72(2), 181–195. 

- Islam, M. (2007): “The State that I am in...,” Equity gilt study 2007,, Barclays Capital. 

- Joyce, M., A. Lasaosa, I. Stevens, and M. Tong (2011): “The Financial Market Impact of Quantitative Easing in the United Kingdom,” _International Journal of Central Banking_ , 7(3), 113–161. 

- Kaminska, I., and G. Zinna (2019): “Official Demand for US Debt: Implications for US Real Rates,” _Journal of Money, Credit, and Banking_ , forthcoming. 

- King, T. (2019): “Expectation and Duration at the Effective Lower Bound,” _Journal of Financial Economics_ , forthcoming. 

- Krishnamurthy, A. (2002): “The Bond/Old-Bond Spread,” _Journal of Financial Economics_ , 66, 463–506. 

- Krishnamurthy, A., and A. Vissing-Jorgensen (2011): “The Effects of Quantitative Easing on Interest Rates: Channels and Implications for Policy,” _Brookings Papers on Economic Activity_ , 42(2 (Fall)), 215–287. 

   - (2012): “The Aggregate Demand for Treasury Debt,” _Journal of Political Economy_ , 120(2), 233 – 267. 

- Lettau, M., and J. Wachter (2011): “The Term Structures of Equity and Interest Rates,” _Journal of Financial Economics_ , 101(1), 90–113. 

- Li, C., and M. Wei (2013): “Term Structure Modeling with Supply Factors and the Federal Reserve’s Large-Scale Asset Purchase Programs,” _International Journal of Central Banking_ , 9(1), 3–39. 

- Malkhozov, A., P. Mueller, A. Vedolin, and G. Venter (2016): “Mortgage Risk and the Yield Curve,” _Review of Financial Studies_ , 29(5), 1220–1253. 

- Modigliani, F., and R. Sutch (1966): “Innovations in Interest-Rate Policy,” _American Economic Review_ , 56, 178–197. 

- Pradhan, A. (2009): “Forward Steepeners Still Offer Value,” Global rates strategy, Barclays Capital. 

- Ray, W. (2019): “Monetary Policy and the Limits to Arbitrage: Insights from a New Keynesian Preferred Habitat Model,” Working paper, UC Berkeley. 

- Sen, I. (2019): “Regulatory Limits to Risk Management,” Working paper, Harvard Business School. 

- Swanson, E. (2011): “Let’s Twist Again: A High-Frequency Event-study Analysis of Operation Twist and Its Implications for 

47 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

QE2,” _Brookings Papers on Economic Activity_ , 42(1 (Spring)), 151–207. 

Swanson, E., and J. Williams (2014): “Measuring the Effect of the Zero Lower Bound on Medium- and Longer-Term Interest Rates,” _American Economic Review_ , 104(10), 3154–3185. 

Tobin, J. (1958): “Liquidity Preference as Behavior Towards Risk,” _Review of Economic Studies_ , 25, 124–131. 

(1969): “A General Equilibrium Approach to Monetary Theory,” _Journal of Money, Credit, and Banking_ , 1, 15–29. 

Tzucker, R., and M. Islam (2005): “A Pension Reform Primer,” Fixed income rates strategy,, Barclays Capital. 

Vasicek, O. (1977): “An Equilibrium Characterization of the Term Structure,” _Journal of Financial Economics_ , 5, 177–188. 

Vayanos, D., and P.-O. Weill (2008): “A Search-based Theory of the On-the-run Phenomenon,” _Journal of Finance_ , 63, 1361–1398. 

Vayanos, D., and P. Woolley (2013): “An Institutional Theory of Momentum and Reversal,” _Review of Financial Studies_ , 26, 1087–1145. 

Veronesi, P. (2010): _Fixed-Income Securities: Valuation, Risk, and Risk Management_ . John Wiley & Sons, Hoboken, New Jersey. 

- Wachter, J. (2006): “A Consumption-Based Model of the Term Structure of Interest Rates,” _Journal of Financial Economics_ , 79(2), 365–399. 

Warga, A. (1992): “Bond Returns, Liquidity, and Missing Data,” _Journal of Financial and Quantitative Analysis_ , 27, 605–617. 

Wiliams, J. (2011): “Unconventional Monetary Policy: Lessons from the Past Three Years,” Presentation to the Swiss National Bank Research Conference,, http://www.frbsf.org/news/speeches/2011/john-williams-0923.html. 

- (2014): “Monetary Policy at the Zero Lower Bound: Putting Theory into Practice,” in _Hutchins Center on Fiscal and_ 

- _Monetary Policy_ . Brookings Institution. 

Xiong, W., and H. Yan (2010): “Heterogeneous Expectations and Bond Markets,” _Review of Financial Studies_ , 23, 1405–1432. 

Yellen, J. (2011): “The Federal Reserve’s Asset Purchase Program,” Speech at the Brimmer Policy Forum, Allied Social Science Associations Annual Meeting,, https://www.federalreserve.gov/newsevents/speech/files/yellen20110108a.pdf. 

## APPENDIX A: PROOFS 

## **Proof of Lemma 1:** The proof is in the text. 

## _Q.E.D._ 

**Proof of Proposition 1:** Equations (21) and (22) follow from integrating the linear ODEs (19) and (20) with the initial conditions _Ar_ (0) = _C_ (0) = 0. Substituting _Ar_ ( _τ_ ) from (21) into (23), we find (25). The left-hand side of (25) is increasing in _κ[∗] r_[,][is][zero][for] _[κ][∗] r_[= 0,][and][converges][to][infinity][when] _[κ][∗] r_[goes][to][infinity.][The][right-hand][side][of][(][25][)][is][decreasing][in] _[κ][∗] r_[,][exceeds] _κr >_ 0 for _κ[∗] r_[= 0,][and][converges][to] _[κ][r]_[when] _[κ][∗] r_[goes][to][infinity.][Therefore,][(][25][)][has][a][unique][solution][for] _[κ][∗] r_[,][which][is][positive.] 

48 

D. VAYANOS AND J.-L. VILA 

Substituting _C_ ( _τ_ ) from (22) into (24), we find 

**==> picture [318 x 260] intentionally omitted <==**

where the first step follows from (21) and (25), and the third step follows from integrating (19) from zero to _τ_ and using (21) and (25), we can write (A.1) as 

**==> picture [472 x 103] intentionally omitted <==**

Equations (21) and (A.2) imply (26). 

**Proof of Proposition 2:** Taking expectations conditional on time _t_ in (8), we find 

**==> picture [121 x 9] intentionally omitted <==**

(A.3) _⇒ Et_ ( _rt_ + _τ_ ) = (1 _− e[−][κ][r][τ]_ ) _r_ + _e[−][κ][r][τ] rt._ 

Equation (A.3) implies 

**==> picture [120 x 19] intentionally omitted <==**

49 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

Equation (27) likewise implies 

**==> picture [135 x 22] intentionally omitted <==**

where the second step follows from (21). 

Equation (25) implies that if _a >_ 0 and _α_ ( _τ_ ) _>_ 0 in a positive-measure subset of (0 _, T_ ), then _κ[∗] r[>][κ][r]_[.][Since][the][right-hand] side of (25) increases in _a_ , _σr_[2][and] _[α]_[(] _[τ]_[),][and][the][difference][between][the][left-hand][side][and][the][right-hand][side][increases][in] _[κ][∗] r_[,] _κ[∗] r_[increases][in] _[a]_[,] _[σ] r_[2][and] _[α]_[(] _[τ]_[).] _Q.E.D._ 

**Proof of Proposition 3:** Equations (1), (2) and (10) imply that the dependent variable in (28) is 

1 _[−]_[∆] _[τ]_[)] _[r][t]_[+∆] _[τ]_[+] _[ C]_[(] _[τ][−]_[∆] _[τ]_[)]] _[ −]_[[] _[A][r]_[(∆] _[τ]_[)] _[r][t]_[ +] _[ C]_[(∆] _[τ]_[)]] _[}]_ ∆ _τ[{][A][r]_[(] _[τ]_[)] _[r][t]_[ +] _[ C]_[(] _[τ]_[)] _[ −]_[[] _[A][r]_[(] _[τ]_ 

and the independent variable is 

1 ∆ _τ[{][A][r]_[(] _[τ]_[)] _[r][t]_[ +] _[ C]_[(] _[τ]_[)] _[ −]_[[] _[A][r]_[(] _[τ][−]_[∆] _[τ]_[)] _[r][t]_[ +] _[ C]_[(] _[τ][−]_[∆] _[τ]_[)]] _[ −]_[[] _[A][r]_[(∆] _[τ]_[)] _[r][t]_[ +] _[ C]_[(∆] _[τ]_[)]] _[}][ .]_ 

Therefore, the FB regression coefficient is 

> _[{]_[[] _[A][r]_[(] _[τ]_[)] _[ −][A][r]_[(][∆] _[τ]_[)]] _[r][t][ −][A][r]_[(] _[τ][−]_[∆] _[τ]_[)] _[r][t]_[+][∆] _[τ][,]_[[] _[A][r]_[(] _[τ]_[)] _[ −][A][r]_[(] _[τ][−]_[∆] _[τ]_[)] _[ −][A][r]_[(][∆] _[τ]_[)]] _[r][t][}] b_ FB =[C][ov] Var _{_ [ _Ar_ ( _τ_ ) _− Ar_ ( _τ −_ ∆ _τ_ ) _− Ar_ (∆ _τ_ )] _rt}_ 

> _[−]_[∆] _[τ]_[)][C][ov][(] _[r][t]_[+][∆] _[τ][, r][t]_[)] (A.6) =[[] _[A][r]_[(] _[τ]_[)] _[ −]_ [ _A[A] r_ ( _[r] τ_[(] )[∆] _−[τ]_[)]] _A_[V] _r_[ar] ( _τ_[(] _−[r][t]_[)] ∆ _[ −] τ_ ) _[A] −[r]_[(] _A[τ] r_ (∆ _τ_ )]Var( _rt_ ) _._ 

Since (A.3) implies 

(A.7) Cov( _rt_ +∆ _τ , rt_ ) = Var( _rt_ ) _e[−][κ][r]_[∆] _[τ] ,_ 

we can write (A.6) as 

**==> picture [174 x 22] intentionally omitted <==**

Taking the limit ∆ _τ →_ 0 and noting from (21) that _[A][r]_ ∆[(][∆] _τ[τ]_[)] _→_ 1, we find 

**==> picture [264 x 21] intentionally omitted <==**

where the second step follows from (19) and (25). Since _κ[∗] r[> κ][r]_[when] _[a >]_[ 0][and] _[α]_[(] _[τ]_[)] _[ >]_[ 0][in][a][positive-measure][subset][of][(0] _[, T]_[),] 

(A.8) implies _b_ FB _>_ 0. Since _κ[∗] r_[increases][in] _[a]_[,] _[σ] r_[2][and] _[α]_[(] _[τ]_[),][(][A.8][)][implies][that] _[b]_[FB][increases][in][the][same][variables.] Equations (1) and (10) imply that the dependent variable in (29) is 

**==> picture [188 x 18] intentionally omitted <==**

50 

D. VAYANOS AND J.-L. VILA 

and the independent variable is 

**==> picture [187 x 20] intentionally omitted <==**

Therefore, the CS regression coefficient is 

**==> picture [300 x 73] intentionally omitted <==**

Using (A.7), we can write (A.9) as 

**==> picture [128 x 31] intentionally omitted <==**

Taking the limit ∆ _τ →_ 0, we find 

**==> picture [369 x 27] intentionally omitted <==**

where the third step follows from (19) and (25). Since _κ[∗] r[> κ][r]_[when] _[a >]_[ 0][and] _[α]_[(] _[τ]_[)] _[ >]_[ 0][in][a][positive-measure][subset][of][(0] _[, T]_[),] 

(A.10) implies _b_ CS _<_ 1. Since 

**==> picture [124 x 29] intentionally omitted <==**

(A.10) implies that _b_ CS increases in _τ_ if the function 

**==> picture [133 x 21] intentionally omitted <==**

is increasing for _x >_ 0. The derivative _K[′]_ ( _x_ ) has the same sign as the function 

**==> picture [94 x 11] intentionally omitted <==**

The function _K_[ˆ] ( _x_ ) is equal to zero for _x_ = 0, and its derivative _K_[ˆ] _[′]_ ( _x_ ) has the same sign as _e[−][x]_ 2 _−_ 1 + _[x]_ 2[which][is][positive][for] all _x_ . Therefore, _K_[ˆ] ( _x_ ) _>_ 0 for _x >_ 0, and _K_ ( _x_ ) is increasing. _Q.E.D._ 

_Q.E.D._ 

51 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

**Proof of Proposition 4:** The argument in the text shows that ∆ _yt_[(] _[τ]_[)] = _κ[∗] r_[∆] _r_ ~~_[∗]_~~ �0 _τ[A][r] τ_[(] _[u]_[)] _[du]_ and ∆ _r_ ~~_[∗]_~~ has the same sign as _aσr_[2] �0 _∞_ ∆ _θ_ 0( _τ_ ) _Ar_ ( _τ_ ) _dτ_ . Hence, when _a >_ 0, the change ∆ _θ_ 0( _τ_ ) raises all yields if �0 _∞_ ∆ _θ_ 0( _τ_ ) _Ar_ ( _τ_ ) _dτ >_ 0 and lowers them otherwise. The relative effect across maturities is 

**==> picture [88 x 34] intentionally omitted <==**

**==> picture [472 x 14] intentionally omitted <==**

relative effect across maturities is larger than one for _τ_ 1 _< τ_ 2. **Proof of Lemma 2:** The proof is in the text. 

_Q.E.D. Q.E.D._ 

**Proof of Lemma 3:** Using the diagonalization 

**==> picture [124 x 11] intentionally omitted <==**

where _Diag_ ( _z_ 1 _, z_ 2 _, .., zN_ ) is the _N × N_ diagonal matrix with elements ( _z_ 1 _, z_ 2 _, .., zN_ ), and multiplying the ODE system (36) from the left by _P_ , we can write it as 

(A.11) _PA[′]_ ( _τ_ ) + _Diag_ ( _ν_ 1 _, ν_ 2 _, .., νK_ +1) _PA_ ( _τ_ ) _− P_ E = 0 _._ 

Integrating (A.11) with the initial condition _A_ (0) = 0 yields 

**==> picture [270 x 21] intentionally omitted <==**

Using 

**==> picture [396 x 199] intentionally omitted <==**

52 

## D. VAYANOS AND J.-L. VILA 

Equation (A.13) implies (39) and (40). Integrating (38) with the initial condition _C_ (0) = 0 yields (41). 

_Q.E.D._ 

We next derive the system of equations in the Laplace transforms. We consider the general case where there are _K_ demand factors. We assume _α_ ( _τ_ ) = _αe[−][δ][α][τ]_ and _θk_ ( _τ_ ) =[�] _[N] n_ =1 _[θ][k,n][e][−][δ][θn][τ]_[, where] _[ N][≥]_[1, (] _[α, δ][α][,][ {][θ][k,n][}][k]_[=1] _[,..,K,][n]_[=1] _[,..,N][,][ {][δ][θ] n[}][n]_[=1] _[,..,N]_[)] are scalars and ( _α, δα, {δθn }n_ =1 _,..,N_ ) are positive. We set 

**==> picture [105 x 49] intentionally omitted <==**

For _n_ = 1 _, .., N_ , we set 

**==> picture [94 x 20] intentionally omitted <==**

and denote by Θ _n_ the 1 _×_ ( _K_ + 1) vector (0 _, θ_ 1 _,n, .., θK,n_ ). Since the vectors ( _I, I_ 1 _, .., IN_ ) are ( _K_ + 1) _×_ 1, and since the matrix _J_ is ( _K_ + 1) _×_ ( _K_ + 1) and symmetric, there are a total of 

**==> picture [237 x 21] intentionally omitted <==**

distinct elements. These elements are Laplace transforms of the functions ( _Ar_ ( _τ_ ) _, {Aβ,k_ ( _τ_ ) _}k_ =1 _,..K_ ) and of those functions’ pairwise products. Using ( _J, {In}n_ =1 _,..,N , {_ Θ _n}n_ =1 _,..,N_ ), we can write the matrix _M_ defined in (37) as 

**==> picture [181 x 25] intentionally omitted <==**

Lemma A.1 _Suppose that α_ ( _τ_ ) = _αe[−][δ][α][τ] and θk_ ( _τ_ ) = � _Nj_ =1 _[θ][k,n][e][−][δ][θn][τ][,] where N ≥_ 1 _,_ ( _α, δα, {θk,n}k_ =1 _,..,K, n_ =1 _,..,N , {δθn }n_ =1 _,..,N_ ) _are scalars and_ ( _α, δα, {δθn }n_ =1 _,..,N_ ) _are positive. The_ ( _K_ + 1) � _K_ 2[+] _[ N]_[+ 2] � _elements of_ ( _I, J, {In}n_ =1 _,..,N_ ) _solve the system of_ 

**==> picture [134 x 17] intentionally omitted <==**

**==> picture [145 x 20] intentionally omitted <==**

_for n_ = 1 _, .., N , and_ 

**==> picture [191 x 10] intentionally omitted <==**

53 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

**Proof of Lemma A.1:** To derive (A.15), we multiply the ODE system (36) by _α_ ( _τ_ ) and integrate from zero to infinity. This yields 

**==> picture [217 x 20] intentionally omitted <==**

Integration by parts implies 

**==> picture [255 x 49] intentionally omitted <==**

**==> picture [148 x 19] intentionally omitted <==**

where the second step follows from _α[′]_ ( _τ_ ) = _−δαα_ ( _τ_ ) and the third step from _A_ (0) = 0. Assuming lim _τ →∞ α_ ( _τ_ ) _A_ ( _τ_ ) = 0, a property that is required for the matrix _M_ to be finite (and that holds for the solution in Theorem 1, as we show at the end of that theorem’s proof), we find 

**==> picture [217 x 20] intentionally omitted <==**

Using (A.18), (A.19) and _a_ ( _τ_ ) = _αe[−][δ][α][τ]_ , we find (A.15). 

To derive (A.16), we likewise multiply the ODE system (36) by _e[−][δ][θn][τ]_ and integrate from zero to infinity. This yields 

**==> picture [241 x 20] intentionally omitted <==**

Integration by parts and a zero limit at infinity imply 

**==> picture [248 x 19] intentionally omitted <==**

Using (A.20) and (A.21), we find (A.16). 

To derive (A.17), we multiply the ODE system (36) from the left by _α_ ( _τ_ ) _A_ ( _τ_ ) _[⊤]_ , add to the resulting ( _K_ +1) _×_ ( _K_ +1) matrix its transpose, and integrate from zero to infinity. This yields 

**==> picture [321 x 20] intentionally omitted <==**

Integration by parts and a zero limit at infinity imply 

**==> picture [330 x 19] intentionally omitted <==**

54 

D. VAYANOS AND J.-L. VILA 

Using (A.22) and (A.23), we find (A.17). 

The total number of equations is ( _K_ + 1) � _K_ 2[+] _[ N]_[+ 2] �, same as the number of unknown Laplace transforms: the vector equation (A.15) yields _K_ + 1 scalar equations, the vector equations (A.16) for _n_ = 1 _, .., N_ yield ( _K_ + 1) _N_ scalar equations, and the matrix equation (A.17) yields[(] _[K]_[+][1][)(] 2 _[K]_[+][2][)] scalar equations because the matrices in it are symmetric. _Q.E.D._ **Proof of Theorem 1:** The theorem specializes Lemma A.1 to the case _K_ = 1, _N_ = 2, _θ_ 11 = _−θ_ 12 = _θ_ , _δθ_ 1 = _δα_ , _δθ_ 2 = _δθ_ , Γ = _Diag_ ( _κr, κβ_ ) and Σ = _Diag_ ( _σr, σβ_ ). Since _K_ = 1 and _N_ = 2, there are nine unknown Laplace transforms, which reduce to seven because _δθ_ 1 = _δα_ implies _I_ 1 = _α[I]_[.][Setting] _[I][≡]_[(] _[I][r][, I][β]_[)] _[⊤]_[,] _[I]_[2] _[≡]_[(] _[I][r,]_[2] _[, I][β,]_[2][)] _[⊤]_[and] 

**==> picture [80 x 20] intentionally omitted <==**

the seven unknown Laplace transforms are ( _Ir, Iβ , Ir,_ 2 _, Iβ,_ 2 _, Ir,r, Ir,β , Iβ,β_ ). Setting 

**==> picture [155 x 20] intentionally omitted <==**

**==> picture [158 x 20] intentionally omitted <==**

we can write the matrix _M_ given by (A.14) as 

**==> picture [178 x 22] intentionally omitted <==**

The vector equation (A.15) yields the two scalar equations 

**==> picture [200 x 17] intentionally omitted <==**

**==> picture [220 x 15] intentionally omitted <==**

The vector equation (A.16) yields the two scalar equations 

**==> picture [209 x 19] intentionally omitted <==**

**==> picture [230 x 15] intentionally omitted <==**

The matrix equation (A.17) yields the three scalar equations 

- (A.31) 

**==> picture [156 x 20] intentionally omitted <==**

**==> picture [337 x 46] intentionally omitted <==**

55 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

Equations (A.27)-(A.32) constitute a system of seven equations in the seven unknowns ( _Ir, Iβ , Ir,r, Ir,β , Iβ,β , Ir,_ 2 _, Iβ,_ 2). We next reduce this system into one of four equations in the four unknowns ( _Ir,r, Ir,β ,_ ∆ _Ir,θ,_ ∆ _Iβ,θ_ ). 

The system of (A.27) and (A.28) is linear in ( _Ir, Iβ_ ) and its solution is 

**==> picture [300 x 32] intentionally omitted <==**

**==> picture [300 x 28] intentionally omitted <==**

Likewise, the system of (A.29) and (A.30) is linear in ( _Ir,_ 2 _, Iβ,_ 2) and its solution is 

**==> picture [304 x 32] intentionally omitted <==**

**==> picture [304 x 29] intentionally omitted <==**

Equation (A.33) is linear in _Iβ,β_ and its solution is 

**==> picture [152 x 25] intentionally omitted <==**

Substituting _Ir_ from (A.34), we can write (A.31) as 

**==> picture [134 x 20] intentionally omitted <==**

**==> picture [306 x 32] intentionally omitted <==**

Substituting ( _Ir, Ir,_ 2) from (A.34) and (A.36), respectively, into the definition (A.24) of ∆ _Ir,θ_ , we find 

**==> picture [266 x 33] intentionally omitted <==**

**==> picture [329 x 32] intentionally omitted <==**

56 

D. VAYANOS AND J.-L. VILA 

Substituting ( _Iβ , Iβ,_ 2 _, Iβ,β_ ) from (A.34), (A.36) and (A.38), respectively, into the definition (A.25) of ∆ _Iβ,θ_ , we find 

**==> picture [267 x 29] intentionally omitted <==**

**==> picture [394 x 30] intentionally omitted <==**

Substituting ( _Iβ , Iβ,β_ ) from (A.34) and (A.38), respectively, we can write (A.31) as 

**==> picture [324 x 26] intentionally omitted <==**

**==> picture [306 x 29] intentionally omitted <==**

Equations (A.39)-(A.42) form the system of four equations in the four unknowns ( _Ir,r,_ ∆ _Ir,θ,_ ∆ _Iβ,θ, Ir,β_ ). Given a solution to that system, we can determine ( _Ir, Iβ , Ir,_ 2 _, Iβ,_ 2 _, Iβ,β_ ) from (A.34)-(A.38). 

To show that the system (A.39)-(A.42) has a solution, we proceed in two steps. In Step 1 we take _Ir,β >_ 0 as given, and construct _Ir,r >_ 0, ∆ _Ir,θ >_ 0 and ∆ _Iβ,θ < δ_ 2 _αaσ_ + _κ_[2] _β_ uniquely from (A.39)-(A.41). In Step 2 we treat ( _Ir,r,_ ∆ _Ir,θ,_ ∆ _Iβ,θ_ ) as implicit _β_ functions of _Ir,β_ , and show that (A.42) has a solution _Ir,β >_ 0. We denote the left-hand sides of (A.39), (A.40), (A.41) and (A.42) by _Lr,r_ , _Lr,θ_ , _Lβ,θ_ and _Lr,β_ , respectively, and set 

**==> picture [253 x 15] intentionally omitted <==**

for _j_ = _α, θ_ . For _Ir,r ≥_ 0, ∆ _Ir,θ ≥_ 0, ∆ _Iβ,θ < δ_ 2 _αaσ_ + _κ_[2] _β_ and _Ir,β >_ 0, _Dθ > Dα >_ 0, and hence ( _Lr,r, Lr,θ, Lβ,θ, Lr,β_ ) are _β_ continuous functions of ( _Ir,r,_ ∆ _Ir,θ,_ ∆ _Iβ,θ, Ir,β_ ). 

**Step 1:** We first take ∆ _Ir,θ ≥_ 0, ∆ _Iβ,θ < δ_ 2 _αaσ_ + _κ_[2] _β_ and _Ir,β >_ 0 as given, and construct _Ir,r >_ 0 from (A.39). Equation (A.39) _β_ 

implies 

**==> picture [281 x 28] intentionally omitted <==**

which in turn implies _[∂L] ∂Ir,r[r][,][r][>]_[ 0][for] _[I][r,r][≥]_[0.][Hence,][if] _[L][r,r][<]_[ 0][for] _[I][r,r]_[= 0,][and] _[L][r,r][>]_[ 0][for] _[I][r,r]_[large][enough,][then][(][A.39][)][has] a unique positive solution for _Ir,r_ . Equation (A.39) implies that _Lr,r_ converges to infinity when _Ir,r_ goes to infinity. We assume that (∆ _Ir,θ,_ ∆ _Iβ,θ, Ir,β_ ) are such that _Lr,r <_ 0 for _Ir,r_ = 0, and return to this issue in Step 2. 

57 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

We next take ∆ _Iβ,θ < δ_ 2 _αaσ_ + _κ_[2] _β_ and _Ir,β >_ 0 as given, treat _Ir,r >_ 0 as an implicit function of (∆ _Ir,θ,_ ∆ _Iβ,θ, Ir,β_ ), and construct _β_ ∆ _Ir,θ >_ 0 from (A.40). Equation (A.40) implies that the partial derivative of _Lr,θ_ with respect to ∆ _Ir,θ_ when the variation of _Ir,r_ is taken into account is 

**==> picture [119 x 21] intentionally omitted <==**

We show that if _Lr,θ_ = 0 for a value ∆ _Ir,θ >_ 0, then _L_[ˆ] _r,θ >_ 0 for the same value. Equation (A.40) implies 

**==> picture [366 x 76] intentionally omitted <==**

Equation (A.39) implies 

**==> picture [227 x 28] intentionally omitted <==**

Since ∆ _Iβ,θ < δ_ 2 _αaσ_ + _κβ_[2] _β_ and _Ir,β >_ 0, (A.46) implies _∂∂L_ ∆ _Irr,θ,r[>]_[ 0][and][hence] 

**==> picture [135 x 32] intentionally omitted <==**

Combining (A.44) and (A.45) with 

**==> picture [306 x 69] intentionally omitted <==**

for _j_ = _α, θ_ , 

**==> picture [376 x 21] intentionally omitted <==**

58 

D. VAYANOS AND J.-L. VILA 

**==> picture [330 x 149] intentionally omitted <==**

which follows from (A.43), (A.46) and (A.47), _Dθ > Dα >_ 0, and 

**==> picture [283 x 26] intentionally omitted <==**

which follows from _Lr,θ_ = 0 (i.e., (A.40)), we find 

**==> picture [192 x 21] intentionally omitted <==**

Since _L_[ˆ] _r,θ >_ 0 at any point where _Lr,θ_ = 0, _Lr,θ_ can be equal to zero only once. Hence, if _Lr,θ <_ 0 for ∆ _Ir,θ_ = 0, and _Lr,θ >_ 0 for ∆ _Ir,θ_ = ∆ _I r,θ_ sufficiently large, and if all values of ∆ _Ir,θ ∈_ (0 _,_ ∆ _I r,θ_ ) yield _Ir,r >_ 0, then (A.40) yields a unique solution for ∆ _Ir,θ ∈_ (0 _,_ ∆ _I r,θ_ ). We assume that (∆ _Iβ,θ, Ir,β_ ) are such that these conditions hold, and return to this issue in Step 2. We finally take _Ir,β >_ 0 as given, treat _Ir,r >_ 0 and ∆ _Ir,θ >_ 0 as implicit functions of (∆ _Iβ,θ, Ir,β_ ), and construct ∆ _Iβ,θ <_ 

_δ_ 2 _αaσ_ + _κ_[2] _β_ from (A.41). Equation (A.41) implies that the partial derivative of _Lβ,θ_ with respect to ∆ _Iβ,θ_ when the variation of _β_ 

( _Ir,r,_ ∆ _Ir,θ_ ) is taken into account is 

**==> picture [233 x 21] intentionally omitted <==**

We show that if _Lβ,θ_ = 0 for a value ∆ _Iβ,θ < δ_ 2 _αaσ_ + _κβ_[2] _β_[,][then] _[L]_[ˆ] _[β,θ][>]_[0][for][the][same][value.][Differentiating][(][A.39][)][and][(][A.40][)][at] 

the values of ( _Ir,r,_ ∆ _Ir,θ_ ) that render ( _Lr,r, Lr,θ_ ) equal to zero, we find 

**==> picture [219 x 52] intentionally omitted <==**

59 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

respectively. Equations (A.50) and (A.51) form a linear system in the unknowns � _∂∂I_ ∆ _Irβ,θ,r[,] ∂∂_ ∆∆ _IIβ,θr,θ_ �. The determinant of that 

system is 

**==> picture [251 x 93] intentionally omitted <==**

and is positive because _[∂L] ∂Ir,r[r][,][r][>]_[ 0][and] _[L]_[ˆ] _[r,θ][>]_[ 0.][Substituting][the][solution][of][the][system][(][A.50][)-(][A.51][)][into][(][A.49][),][we][find][that] (A.49) has the same sign as the Jacobian determinant 

**==> picture [157 x 44] intentionally omitted <==**

The partial derivatives ( _[∂L] ∂Ir,r[r][,][r][,] ∂[∂L]_ ∆ _I[r] r,θ[,][r][,] ∂L∂Ir,rr,θ[,] ∂∂L_ ∆ _Irr,θ,θ_[)][are][given][by][(][A.43][),][(][A.46][),][(][A.44][)][and][(][A.45][),][respectively.][Equations] 

(A.39), (A.40) and (A.41) imply that the remaining partial derivatives are 

**==> picture [376 x 215] intentionally omitted <==**

The sign of the Jacobian determinant (A.52) does not change if we multiply the last row by � _δα_ + _κβ − aσβ_[2][∆] _[I][β,θ]_ �. The resulting determinant does not change if we subtract the middle row times _aσr_[2][∆] _[I] r,θ_[from][the][last][row,][and][then][the][first][row] 

60 

D. VAYANOS AND J.-L. VILA 

times _α[θ]_ �1 _−[δ] δ[α] θ D[D] θα_[2][2] � from the middle row. In the resulting determinant, the elements (1,1), (1,2) and (1,3) are given by (A.43), (A.46) and (A.53), respectively, the element (2,1) is given by 

**==> picture [352 x 119] intentionally omitted <==**

the element (2,2) by 

**==> picture [332 x 70] intentionally omitted <==**

the element (2,3) by 

**==> picture [285 x 26] intentionally omitted <==**

the element (3,1) by 

**==> picture [355 x 118] intentionally omitted <==**

61 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

the element (3,2) by 

**==> picture [388 x 104] intentionally omitted <==**

where we use _Lβ,θ_ = 0 (i.e., (A.41)), and the element (3,3) by 

**==> picture [376 x 189] intentionally omitted <==**

where the last step follows from _Lβ,θ_ = 0. 

For large _δθ_ , all the terms with _Dθ_ in the denominator are close to zero, and the determinant obtained by multiplying (A.52) 

62 

D. VAYANOS AND J.-L. VILA 

**==> picture [433 x 238] intentionally omitted <==**

To show that (A.58) is positive, and hence _L_[ˆ] _β,θ >_ 0, we distinguish cases. When ∆ _Iβ,θ <_ 0, the only negative term in (A.58) is the one generated by ∆∆ _IIβ,r,θθ_ � _δα_ + _κβ − aσβ_[2][∆] _[I][β,θ]_ �. We group it together with the term generated by one of the two _−aσβ_[2][∆] _[I][β,θ]_ in � _δα_ + _κβ −_ 2 _aσβ_[2][∆] _[I][β,θ]_ � and note that (A.58) exceeds 

**==> picture [330 x 111] intentionally omitted <==**

which is positive. When instead ∆ _Iβ,θ ∈_ �0 _, δ_ 2 _αaσ_ + _κβ_[2] _β_ �, all the terms in (A.58), with � _δα_ + _κβ −_ 2 _aσβ_[2][∆] _[I][β,θ]_ � counted as a single term, are positive. Hence, _L_[ˆ] _β,θ >_ 0 at any point ∆ _Iβ,θ < δ_ 2 _αaσ_ + _κ_[2] _β_ where _Lβ,θ_ = 0, which implies that _Lβ,θ_ can be equal to zero _β_ only once. Moreover, if _Lβ,θ <_ 0 for ∆ _Iβ,θ_ = ∆ _I_ ~~_β_~~ _,θ_[sufficiently][negative,][and] _[L][β,θ][>]_[0][for][∆] _[I][β,θ]_[=] _δ_ 2 _αaσ_ + _κ_[2] _β_ , and if all values of _β_ ∆ _Iβ,θ ∈_ ∆ _I_ ~~_β_~~ _,θ[,] δ_ 2 _αaσ_ + _κ_[2] _β_ yield _Ir,r >_ 0 and ∆ _Ir,θ >_ 0, then (A.40) yields a unique solution for ∆ _Iβ,θ ∈_ ∆ _I_ ~~_β_~~ _,θ[,] δ_ 2 _αaσ_ + _κ_[2] _β_ . We � _β_ � � _β_ � 

63 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

assume that _Ir,β_ is such that these conditions hold, and return to this issue in Step 2. 

**Step 2:** Suppose that _Ir,β >_ 0 satisfies 

**==> picture [113 x 21] intentionally omitted <==**

and define _I_[¯] _r,r >_ 0 by 

**==> picture [274 x 22] intentionally omitted <==**

Equation (A.60) defines _I_[¯] _r,r >_ 0 uniquely because the left-hand side increases for _Ir,r ≥_ 0, converges to infinity when _I_[¯] _r,r_ goes 

to infinity, and is negative for _I_[¯] _r,r_ = 0 because of (A.59). Suppose that _Ir,β_ satisfies additionally 

**==> picture [217 x 51] intentionally omitted <==**

**==> picture [472 x 17] intentionally omitted <==**

assumes some of the boundary conditions, which we next prove using (A.59), (A.61) and (A.62). 

Take first ∆ _Ir,θ ∈_ (0 _,_ ∆ _I r,θ_ ), ∆ _Iβ,θ < δ_ 2 _αaσ_ + _κ_[2] _β_ and _Ir,β >_ 0 as given, where ∆ _I r,θ >_ 0 is defined by _β_ 

**==> picture [280 x 32] intentionally omitted <==**

and is positive because of (A.59). Equation (A.39) implies that for _Ir,r_ = 0, 

**==> picture [282 x 32] intentionally omitted <==**

where the inequality follows from ∆ _Ir,θ ∈_ (0 _,_ ∆ _I r,θ_ ) and (A.63). Equation (A.39) and (A.60) imply that for _Ir,r_ = _I_[¯] _r,r_ , 

**==> picture [161 x 20] intentionally omitted <==**

**==> picture [245 x 33] intentionally omitted <==**

**==> picture [342 x 32] intentionally omitted <==**

64 

D. VAYANOS AND J.-L. VILA 

Hence (A.39) has a unique positive solution for _Ir,r ∈_ (0 _, I_[¯] _r,r_ ). 

Take next ∆ _Iβ,θ < δ_ 2 _αaσ_ + _κ_[2] _β_ and _Ir,β >_ 0 as given, and treat _Ir,r ∈_ (0 _, I_[¯] _r,r_ ) as an implicit function of (∆ _Ir,θ,_ ∆ _Iβ,θ, Ir,β_ ). For _β_ 

∆ _Ir,θ_ = 0, (A.39) and (A.60) imply _Ir,r_ = _I_[¯] _r,r_ , and (A.40) implies 

**==> picture [223 x 25] intentionally omitted <==**

where the inequality follows from (A.61). For ∆ _Ir,θ_ = ∆ _I r,θ_ , (A.39) and (A.63) imply _Ir,r_ = 0, and (A.40) implies 

**==> picture [256 x 32] intentionally omitted <==**

**==> picture [368 x 106] intentionally omitted <==**

where the second step follows from (A.63) and the fourth from (A.62). Hence, (A.40) has a unique solution for ∆ _Ir,θ ∈_ (0 _,_ ∆ _I r,θ_ ). Take finally _Ir,β >_ 0 as given, and treat _Ir,r ∈_ (0 _, I_[¯] _r,r_ ) and ∆ _Ir,θ ∈_ (0 _,_ ∆ _I r,θ_ ) as implicit functions of (∆ _Iβ,θ, Ir,β_ ). When ∆ _Iβ,θ_ goes to minus infinity, (A.63) implies that _δα_ + _κβ_ ∆ _−Iaσr,θβ_[2][∆] _[I][β,θ]_[converges][to][a][positive][limit.][Since,][in][addition,] _[I]_[¯] _[r,r]_[is] independent of ∆ _Iβ,θ_ , _Ir,r ∈_ (0 _, I_[¯] _r,r_ ) and ∆ _Ir,θ ∈_ (0 _,_ ∆ _I r,θ_ ), (A.41) implies that _Lβ,θ_ converges to minus infinity. We next determine conditions so that _Lβ,θ >_ 0 for ∆ _Iβ,θ_ = _δ_ 2 _αaσ_ + _κβ_[2] _β_[.][Equations][(][A.40][)][and][(][A.41][)][imply] 

**==> picture [362 x 144] intentionally omitted <==**

65 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

Hence, _Lβ,θ >_ 0 for large _δθ_ if 

**==> picture [357 x 29] intentionally omitted <==**

Setting ∆ _Iβ,θ_ = _δ_ 2 _αaσ_ + _κ_[2] _β_ in (A.65), we can write it as _β_ 

**==> picture [212 x 27] intentionally omitted <==**

Equation (A.66) is satisfied for _κβ ≈_ 0. It is also satisfied for a general value of _κβ_ if 

**==> picture [298 x 41] intentionally omitted <==**

_θ_ which follows from (A.66) by noting that (A.40) implies ∆ _Ir,θ < δθδ_ + _θκr_[. Under either] _[ κ][β][≈]_[0 or] _[ δ][α]_[(] _[δ][α]_[+] _[κ][r]_[)(] _[δ][α]_[+] _[κ][β]_[)] _[ >]_[ 2] _[aθσ][r][σ][β]_[,] 

_Lβ,θ >_ 0 for ∆ _Iβ,θ_ = _δ_ 2 _αaσ_ + _κ_[2] _β_ , and hence (A.41) has a unique solution for ∆ _Iβ,θ < δ_ 2 _αaσ_ + _κ_[2] _β_ . _β β_ 

Inequalities (A.59), (A.61) and (A.62) hold for _Ir,β_ close to zero. Consider the largest value _I_[¯] _r,β_ such that (A.59), (A.61) and (A.62) hold for all _Ir,β < I_[¯] _r,β_ . The implicit function theorem ensures that the functions ( _Ir,r,_ ∆ _Ir,θ,_ ∆ _Iβ,θ_ ) are continuous in _Ir,β ≤ I_[¯] _r,β_ . For _Ir,β_ close to zero, (A.39) and (A.40) imply that _Ir,r_ and ∆ _Ir,θ_ are bounded away from zero. Since, in addition, ∆ _Iβ,θ_ is bounded above by _δ_ 2 _αaσ_ + _κβ_[2] _β_[,][(][A.42][)][implies] _[L][r,β][<]_[0.][We][next][determine][a][value] _[I] r,β[∗][≥][I]_[¯] _[r,β]_[such][that] _[L][r,β][>]_[0][(and] such that ( _Ir,r,_ ∆ _Ir,θ,_ ∆ _Iβ,θ_ ) are well-defined and continuous in _Ir,β ∈_ ( _I_[¯] _r,β , Ir,β[∗]_[]).][Continuity][then][ensures][that][a][solution] _Ir,β < Ir,β[∗]_[to][(][A.42][)][exists,][and][hence][a][solution][(] _[I][r,r][,]_[ ∆] _[I][r,θ][,]_[ ∆] _[I][β,θ][, I][r,β]_[)][to][the][system][(][A.39][)-(][A.42][)][also][exists.] 

The inequality among (A.59), (A.61) and (A.62) that switches to an equality at _I_[¯] _r,β_ cannot be (A.59). Indeed, if (A.59) switches to an equality at _I_[¯] _r,β_ , then (A.60) implies _I_[¯] _r,r_ = 0, and (A.61) becomes 

**==> picture [142 x 23] intentionally omitted <==**

Multiplying (A.62) by (A.68), we find 

**==> picture [156 x 22] intentionally omitted <==**

which implies that (A.59) holds, a contradiction. 

66 

D. VAYANOS AND J.-L. VILA 

If (A.61) switches to an equality at _I_[¯] _r,β_ , then _Lr,θ_ = 0 for ∆ _Ir,θ_ = 0, and hence the solution to (A.40) is ∆ _Ir,θ_ = 0. Equation (A.42) then implies _Lr,β >_ 0 for _Ir,β_ = _I_[¯] _r,β_ = _I_[¯] _r,β[∗]_[.] 

Suppose instead that (A.62) switches to an equality at _I_[¯] _r,β_ . Consider a value of _Ir,β > I_[¯] _r,β_ = _θaσα β_[2][such][that][(][A.59][)][and] (A.61) hold. Define ∆ _I r,θ >_ 0 by (A.63) and consider the set of ∆ _Iβ,θ < δ_ 2 _αaσ_ + _κ_[2] _β_ such that _Lr,θ >_ 0 for ∆ _Ir,θ_ = ∆ _I r,θ_ . _β_ 

Proceeding as in (A.64) and substituting ∆ _I r,θ_ from (A.63), we can write the condition defining that set as 

**==> picture [365 x 72] intentionally omitted <==**

If (A.69) holds for all ∆ _Iβ,θ < δ_ 2 _αaσ_ + _κβ_[2] _β_[,][then][we][can][proceed][as][in][the][case][where][(][A.59][),][(][A.61][)][and][(][A.62][)][hold,][and][construct] 

_Ir,r >_ 0, ∆ _Ir,θ >_ 0 and ∆ _Iβ,θ < δ_ 2 _αaσ_ + _κ_[2] _β_ uniquely. Denote by _I_[¯] _r,β[′][>][I]_[¯] _[r,β]_[the][maximum][value][of] _[I][r,β]_[such][that][(][A.69][)][holds][for] _β_ all ∆ _Iβ,θ < δ_ 2 _αaσ_ + _κ_[2] _β_ and for all _Ir,β ∈_ [ _I_[¯] _r,β , I_[¯] _r,β[′]_[).] _β_ 

If (A.61) switches to an equality at _I_[¯] _r,β[′′][∈]_[(¯] _[I][r,β][,]_[ ¯] _[I] r,β[′]_[]][and][(][A.59][)][holds][for][all] _[I][r,β][∈]_[[¯] _[I][r,β][,]_[ ¯] _[I] r,β[′′]_[],][then][(] _[I][r,r][,]_[ ∆] _[I][r,θ][,]_[ ∆] _[I][β,θ]_[)][are] 

well-defined and continuous in _Ir,β ∈_ [ _I_[¯] _r,β , I_[¯] _r,β[′′]_[]][and] _[L][r,β][>]_[ 0][for] _[I][r,β]_[=] _[I]_[¯] _r,β[′′]_[=] _[ I] r,β[∗]_[.] 

Suppose instead that (A.61) holds for all _Ir,β ∈_ [ _I_[¯] _r,β , I_[¯] _r,β[′]_[].][Then][(][A.59][)][also][holds][for][all] _[I][r,β][∈]_[[¯] _[I][r,β][,]_[ ¯] _[I] r,β[′]_[].][Indeed,][if][(][A.59][)] switches to an equality at _I_[¯] _r,β[′′][∈]_[(¯] _[I][r,β][,]_[ ¯] _[I] r,β[′]_[],][then][(][A.60][)][implies] _[I]_[¯] _[r,r]_[= 0,][and][(][A.64][)][implies] 

**==> picture [189 x 95] intentionally omitted <==**

where the first and third steps follow from (A.59) switching to an equality at _I_[¯] _r,β[′′]_[.][Hence,][(][A.61][)][holds][in][the][opposite][direction,] a contradiction. Since (A.59) and (A.61) hold for all _Ir,β ∈_ [ _I_[¯] _r,β , I_[¯] _r,β[′]_[],][(] _[I][r,r][,]_[ ∆] _[I][r,θ][,]_[ ∆] _[I][β,θ]_[)][are][well-defined][and][continuous][in] _Ir,β ∈_ [ _I_[¯] _r,β , I_[¯] _r,β[′]_[].][For] _[I][r,β]_[=] _[I]_[¯] _r,β[′]_[,][(][A.64][)][switches][to][an][equality][for][a][single][value][∆] _[I]_ ~~_β_~~ _,θ_[.][(Since][the][left-hand][side][is][convex][in] ∆ _Iβ,θ_ , if (A.64) switches to an equality for two values of ∆ _Iβ,θ_ , then it switches to an inequality in the opposite direction for values of ∆ _Iβ,θ_ in-between, which contradicts the definition of _I_[¯] _r,β[′]_[.)][Suppose][without][loss][of][generality][that][the][solution][∆] _[I][β,θ]_ 

67 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

is to the right of ∆ _I_ ~~_β_~~ _,θ_[,][in][which][case] _[L][β,θ][<]_[ 0][for][∆] _[I][β,θ]_[= ][∆] _[I]_ ~~_β_~~ _,θ_[.][Consider][a][value][of] _[I][r,β][>][I]_[¯] _r,β[′]_[such][that][(][A.59][)][and][(][A.61][)] hold, and denote by ∆ _I_ ~~_β_~~ _,θ_[the][minimum][value][of][∆] _[I][β,θ]_[such][that][(][A.69][)][holds][for][all][∆] _[I][β,θ][∈]_ ∆ _I_ ~~_β_~~ _,θ[,] δ_ 2 _αaσ_ + _κ_[2] _β_ . Proceeding � _β_ � as in the case where (A.59), (A.61) and (A.62) hold, we can construct _Ir,r >_ 0, ∆ _Ir,θ >_ 0 and ∆ _Iβ,θ ∈_ ∆ _I_ ~~_β_~~ _,θ[,] δ_ 2 _αaσ_ + _κ_[2] _β_ � _β_ � uniquely. Consider the largest value _I_[¯] _r,β[′′′][>][I]_[¯] _r,β[′]_[such][that][for][all] _[I][r,β][∈]_[[¯] _[I] r,β[′][,]_[ ¯] _[I] r,β[′′′]_[),][(][A.59][)][and][(][A.61][)][hold][and] _[L][β,θ][<]_[0][for] ∆ _Iβ,θ_ = ∆ _I_ ~~_β_~~ _,θ_[.][The][functions][(] _[I][r,r][,]_[ ∆] _[I][r,θ][,]_[ ∆] _[I][β,θ]_[)][are][well-defined][and][continuous][in] _[I][r,β][∈]_[(¯] _[I] r,β[′][,]_[ ¯] _[I] r,β[′′′]_[].][The][same][argument][as] in (A.70) implies that the inequality among (A.59), (A.61) and _Lβ,θ <_ 0 for ∆ _Iβ,θ_ = ∆ _I_ ~~_β_~~ _,θ_[that][switches][to][an][equality][at] _I_ ¯ _r,β[′′′]_[cannot][be][(][A.59][).][If][(][A.61][)][switches][to][an][equality][at] _[I]_[¯] _r,β[′′′]_[,][then] _[L][r,β][>]_[0][for] _[I][r,β]_[=] _[I]_[¯] _r,β[′′′]_[=] _[I] r,β[∗]_[.][If][instead,] _[L][β,θ]_[=][0][for] ∆ _Iβ,θ_ = ∆ _I_ ~~_β_~~ _,θ_[,][then][(] _[I][r,r][,]_[ ∆] _[I][r,θ][,]_[ ∆] _[I][β,θ]_[) = (0] _[,]_ ∆ _I r,θ,_ ∆ _I_ ~~_β_~~ _,θ_[).][Hence,] 

**==> picture [258 x 141] intentionally omitted <==**

**==> picture [339 x 30] intentionally omitted <==**

where the first step follows from _Ir,β[′′′][>][I]_[¯] _[r,β]_[=] _θaσα β_[2][and][the][second][step][from][(][A.41][).][For][large] _[δ][θ]_[,] _[L][r,β][>]_[ 0][if] 

**==> picture [161 x 12] intentionally omitted <==**

which holds because ∆ _Iβ,θ < δ_ 2 _αaσ_ + _κβ_[2] _β_[.][Hence,] _[I][r,β]_[=] _[I]_[¯] _r,β[′′′]_[=] _[I] r,β[∗]_[.][The][solution][satisfies] _[I][r,r][>]_[0,][∆] _[I][r,θ][>]_[0,][∆] _[I][β,θ][<] δ_ 2 _αaσ_ + _κβ_[2] _β_ and 

_Ir,β >_ 0. Combining these inequalities with (A.26), we find _M_ 1 _,_ 1 _> κr_ , _M_ 1 _,_ 2 _>_ 0, _M_ 2 _,_ 1 _<_ 0 and _M_ 2 _,_ 2 _> κβ −_ 2 _δα_ . 

To complete the existence proof, we show that the integrals in the Laplace transforms ( _Ir, Iβ , Ir,r, Ir,β , Iβ,β , Ir,_ 2 _, Iβ,_ 2) converge. That property is assumed when performing the integration by parts in Lemma A.1. Since _δθ > δα_ , the Laplace-transform integrals converge if the real parts of the eigenvalues of _M_ exceed _−[δ]_ 2 _[α]_[.][Using][(][A.26][),][we][find][that][the][characteristic][polynomial] 

68 

D. VAYANOS AND J.-L. VILA 

of _M_ is 

**==> picture [300 x 16] intentionally omitted <==**

Since _Ir,r >_ 0, ∆ _Ir,θ >_ 0, ∆ _Iβ,θ < δ_ 2 _aaσ_ + _κ_[2] _β_ and _Ir,β >_ 0, _P_ ( _λ_ ) _>_ 0 for all _λ < −[δ]_ 2 _[α]_[.][Hence,][if][the][eigenvalues][are][real,][they][must] _β_ 

exceed _−[δ][α]_[If][the][eigenvalues][are][complex,][their][real][part][is] 2[.] 

**==> picture [115 x 21] intentionally omitted <==**

**==> picture [209 x 17] intentionally omitted <==**

**==> picture [28 x 8] intentionally omitted <==**

**Proof of Proposition 5:** Using _K_ = 1 and (A.26), we can write the system (36) as 

**==> picture [247 x 12] intentionally omitted <==**

**==> picture [251 x 16] intentionally omitted <==**

and the solution to that system, given in Lemma 3, as 

**==> picture [241 x 52] intentionally omitted <==**

Equations (A.73) and (A.74), together with the initial conditions _Ar_ (0) = _Aβ_ (0) = 0, imply _A[′] r_[(0)][=][1][and] _[A][′] β_[(0)][=][0.] Differentiating (A.74) at zero and using ∆ _Ir,θ >_ 0, which follows from _M_ 2 _,_ 1 _<_ 0 and (A.26), we find _A[′′] β_[(0)] _[>]_[0.][Hence,] _Ar_ ( _τ_ ) _>_ 0, _A[′] β_[(] _[τ]_[)] _[ >]_[ 0][and] _[A][β]_[(] _[τ]_[)] _[ >]_[ 0][for][small] _[τ]_[.] 

Suppose that the two eigenvalues of _M_ are real, and without loss of generality set _ν_ 1 _> ν_ 2. Since the function ( _ν, τ_ ) _−→_[1] _[−][e] ν[−][ντ]_ decreases in _ν_ , the term in parenthesis in (A.76) is positive. Since, in addition, _Aβ_ ( _τ_ ) _>_ 0 for small _τ_ , _ϕβ >_ 0 and hence _Aβ_ ( _τ_ ) _>_ 0 for all _τ_ . Since 

**==> picture [108 x 11] intentionally omitted <==**

and _ϕβ >_ 0, _A[′] β_[(] _[τ]_[)] _[ >]_[ 0.][Since] 

**==> picture [276 x 30] intentionally omitted <==**

**==> picture [472 x 17] intentionally omitted <==**

Since 

**==> picture [143 x 11] intentionally omitted <==**

69 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

the sign of _A[′] r_[(] _[τ]_[)][can][change][at][most][once.][Hence,] _[A][′] r_[(] _[τ]_[)] _[>]_[0][for] _[τ][∈]_[(0] _[,]_[ ¯] _[τ][ ′]_[)][and] _[A][′] r_[(] _[τ]_[)] _[<]_[0][for] _[τ][∈]_[(¯] _[τ][ ′][,][ ∞]_[),][where] _[τ]_[¯] _[ ′]_[is][a] threshold in (0 _, ∞_ ]. The function _Ar_ ( _τ_ ) has the same behavior for a different threshold _τ_ ¯. 

When _a ≈_ 0, _Ar_ ( _τ_ ) _>_ 0 because Lemma A.2 implies _ϕr ≈_ 0, _ν_ 1 _≈ κr >_ 0 and _ν_ 2 _≈ κβ >_ 0. When _α_ ( _τ_ ) = 0, _Ir,r_ = _Ir,β_ = 0, and hence (A.73) implies _Ar_ ( _τ_ ) =[1] _[−][e] κ[−] r[κrτ] >_ 0. In both cases, _τ_ ¯ = _∞_ . When _a ≈∞_ , Lemma A.2 implies that for _τ_ bounded away from zero 

**==> picture [228 x 102] intentionally omitted <==**

¯ Since this is negative for _τ_ close to _∞_ , _τ < ∞_ . 

Suppose that the two eigenvalues of _M_ are complex. Since they are conjugates, we set _ν_ 1 = _µ_ + _iξ_ and _ν_ 2 = _µ − iξ_ for real numbers ( _µ, ξ_ ). Equations (A.75) and (A.76) imply that ( _Ar_ ( _τ_ ) _, Aβ_ ( _τ_ )) take the form 

(A.77) _Ar_ ( _τ_ ) = _ϕr,_ 0 + _ϕr,_ 1 _e[−][µτ]_ cos( _ξτ_ ) + _ϕr,_ 2 _e[−][µτ]_ sin( _ξτ_ ) _,_ 

(A.78) _Aβ_ ( _τ_ ) = _ϕβ,_ 0 + _ϕβ,_ 1 _e[−][µτ]_ cos( _ξτ_ ) + _ϕβ,_ 2 _e[−][µτ]_ sin( _ξτ_ ) _,_ 

for real numbers _{ϕj,n}j_ = _r,β, n_ =0 _,_ 1 _,_ 2. Since the initial conditions _Ar_ (0) = _Aβ_ (0) = 0 imply _ϕj,_ 0 + _ϕj,_ 1 = 0 for _j_ = _r, β_ , condition 

_A[′] r_[(0) = 1][implies] _[−][ϕ][r,]_[1] _[µ]_[ +] _[ ϕ][r,]_[2] _[ξ]_[= 1,][and][condition] _[A][′] β_[(0) = 0][implies] _[−][ϕ][β,]_[1] _[µ]_[ +] _[ ϕ][β,]_[2] _[ξ]_[= 0,][we][can][write][(][A.77][)][and][(][A.78][)][as] 

**==> picture [293 x 50] intentionally omitted <==**

Differentiating (A.79) and (A.80), we find 

**==> picture [283 x 52] intentionally omitted <==**

70 

D. VAYANOS AND J.-L. VILA 

Since _A[′] β_[(] _[τ]_[)] _[ >]_[ 0][for][small] _[τ]_[,] _[ϕ][β,]_[0] _[>]_[ 0,][and][hence] _[A][′] β_[(] _[τ]_[)] _[ >]_[ 0][for] _[τ][∈]_[(0] _[,] |[π] ξ|_[).][The][derivative] � _AAβr_ (( _ττ_ )) � _′_ has the same sign as 

**==> picture [100 x 11] intentionally omitted <==**

**==> picture [308 x 82] intentionally omitted <==**

where the second step follows from (A.79)-(A.82) and the third by rearranging. Since _ϕβ,_ 0 _>_ 0, � _AAβr_ (( _ττ_ )) � _′_ is negative if the term 

in brackets in (A.83) is negative. That term is concave in _µ_ and is maximized for _µ_ given by 

**==> picture [165 x 20] intentionally omitted <==**

The maximum is 

**==> picture [251 x 20] intentionally omitted <==**

where 

**==> picture [140 x 20] intentionally omitted <==**

The function _H_ ( _x_ ) is equal to zero for _x_ = 0, and its derivative is 

**==> picture [304 x 27] intentionally omitted <==**

Since 

_x_[2] _−_ 2 _x_ cos( _x_ ) sin( _x_ ) + sin[2] ( _x_ ) _> x_[2] _−_ 2 _|x_ sin( _x_ ) _|_ + sin[2] ( _x_ ) = ( _|x| −|_ sin( _x_ ) _|_ )[2] _>_ 0 

for _x_ = 0, _H[′]_ ( _x_ ) _>_ 0 for _x <_ 0, and _H[′]_ ( _x_ ) _<_ 0 for _x >_ 0. Since, in addition, _H_ (0) = 0, _H_ ( _x_ ) _<_ 0. Hence, the maximum (A.84) is negative for _τ ∈_ (0 _, |[π] ξ|_[),][and][so][is] � _AAβr_ (( _ττ_ )) � _′_ . This establishes the results in the proposition for _A[′] β_[(] _[τ]_[)][and] _A[A] β[r]_[(] ( _[τ] τ_[)] )[and][for][the] threshold _τ_ ˆ = _|πξ|_[.][The][result][for] _[A][β]_[(] _[τ]_[)][and][for][a][threshold] _[τ]_[¯¯] _[>][τ]_[ˆ][follows][because] _[A][β]_[(0) = 0][and] _[A][′] β_[(] _[τ]_[)] _[ >]_[ 0][for] _[τ][∈]_[(0] _[,]_[ ˆ] _[τ]_[)][imply] _Aβ_ ( _τ_ ) _>_ 0 for _τ ∈_ (0 _,_ ˆ _τ_ ]. 

If _τ_ ¯[¯] _< ∞_ , then _Aβ_ ( _τ_ ¯[¯] ) = 0 and _A[′] β_[(¯¯] _[τ]_[)] _[≤]_[0.][If] _[A][′] β_[(¯¯] _[τ]_[)] _[<]_[0,][then][∆] _[I][r,θ][>]_[0][and][(][A.74][)][imply] _[A][r]_[(¯¯] _[τ]_[)] _[<]_[0.][If] _[A][′] β_[(¯¯] _[τ]_[)][=][0,][then] ∆ _Ir,θ >_ 0 and (A.74) imply _Ar_ ( _τ_ ¯[¯] ) = 0, and (A.74) implies _A[′] r_[(¯¯] _[τ]_[)][=][1.][Hence,][in][both][cases,] _[A][r]_[(] _[τ]_[)] _[<]_[0][for] _[τ]_[smaller][than][and] close to _τ_ ¯[¯] . This yields the result in the proposition for _Ar_ ( _τ_ ) and for a threshold _τ_ ¯ _< τ_ ¯[¯] . _Q.E.D._ 

71 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

Lemma A.2 derives the asymptotic behavior of ( _ν_ 1 _, ν_ 2 _, ϕr, ϕβ_ ) when _a ≈_ 0 and _a ≈∞_ . To state and prove the lemma, we define the functions 

**==> picture [160 x 43] intentionally omitted <==**

**==> picture [154 x 13] intentionally omitted <==**

**==> picture [110 x 20] intentionally omitted <==**

**==> picture [92 x 11] intentionally omitted <==**

We also note that the definitions of ( _J, Ir,r, Ir,β_ ) imply 

**==> picture [158 x 50] intentionally omitted <==**

Lemma A.2 _Suppose that there is one demand factor, the matrices_ (Γ _,_ Σ) _are diagonal, and α_ ( _τ_ ) _and[θ]_[(] _τ[τ]_[)] _have a positive and a finite limit, respectively, at τ_ = 0 _. The asymptotic behavior of_ ( _ν_ 1 _, ν_ 2 _, ϕr, ϕβ_ ) _when a ≈_ 0 _and a ≈∞ is as follows:_ 

**==> picture [219 x 11] intentionally omitted <==**

**==> picture [129 x 57] intentionally omitted <==**

**==> picture [268 x 144] intentionally omitted <==**

72 

## D. VAYANOS AND J.-L. VILA 

_and ν_ 2 _solves_ 

**==> picture [224 x 32] intentionally omitted <==**

**Proof:** Substituting (A.75) and (A.76) into (A.73) and identifying terms in[1] _[−][e] ν[−]_ 1 _[ν]_[1] _[τ]_ and � 1 _−eν[−]_ 2 _[ν]_[2] _[τ] −_[1] _[−][e] ν[−]_ 1 _[ν]_[1] _[τ]_ �, we find 

(A.93) _ϕr_ ( _ν_ 1 _− ν_ 2) _− ν_ 1 + _κr_ + _aσr_[2] _[I][r,r]_[= 0] _[,]_ 

**==> picture [213 x 12] intentionally omitted <==**

respectively. Using (A.93), we can write (A.94) as 

- (A.95) _ϕr_ (1 _− ϕr_ )( _ν_ 1 _− ν_ 2) + _ϕβ aσβ_[2] _[I][r,β]_[= 0] _[.]_ 

Substituting (A.75) and (A.76) into (A.74) and identifying terms, we find 

- (A.96) _ϕβ_ ( _ν_ 1 _− ν_ 2) _− aσr_[2][∆] _[I] r,θ_[= 0] _[,]_ 

- (A.97) _− ϕβ ν_ 2 _− ϕr_ ∆ _Ir,θ_ + _ϕβ_ � _κβ − aσβ_[2][∆] _[I][β,θ]_ � = 0 _,_ 

respectively. Using (A.96), we can write (A.97) as 

- (A.98) _−ν_ 2 _− ϕr_ ( _ν_ 1 _− ν_ 2) + _κβ − aσβ_[2][∆] _[I][β,θ]_[= 0] _[.]_ 

Equations (A.93), (A.95), (A.96) and (A.98) constitute a system of four equations in the four unknowns ( _ν_ 1 _, ν_ 2 _, ϕr, ϕβ_ ). Substituting (A.75) and (A.76) into the definitions (A.85), (A.86), (A.24) and (A.25) of ( _Ir,r, Ir,β ,_ ∆ _Ir,θ,_ ∆ _Iβ,θ_ ), we can write that system as 

- (A.99) _ϕr_ ( _ν_ 1 _− ν_ 2) _− ν_ 1 + _κr_ + _aσr_[2] _F_ ( _ν_ 1 _, ν_ 1) + 2 _ϕrF_[ˆ] ( _ν_ 1 _, ν_ 2) + _ϕ_[2] _r[F]_[ˆˆ][(] _[ν]_[1] _[, ν]_[2][)] = 0 _,_ � � 

- ˆ ˆ 

- (A.100) _ϕr_ (1 _− ϕr_ )( _ν_ 1 _− ν_ 2) + _ϕ_[2] _β[aσ] β_[2] � _F_ ( _ν_ 1 _, ν_ 2) + _ϕrF_[ˆ] ( _ν_ 1 _, ν_ 2)� = 0 _,_ 

**==> picture [328 x 16] intentionally omitted <==**

**==> picture [284 x 16] intentionally omitted <==**

Suppose that _a ≈_ 0. Setting ( _ϕr, ϕβ_ ) = ( _a_[3] _cr, acβ_ ), we can write (A.99)-(A.102) as 

- (A.103) _a_[3] _cr_ ( _ν_ 1 _− ν_ 2) _− ν_ 1 + _κr_ + _aσr_[2] _F_ ( _ν_ 1 _, ν_ 1) + 2 _a_[3] _crF_[ˆ] ( _ν_ 1 _, ν_ 2) + _a_[6] _c_[2] _r[F]_[ˆˆ][(] _[ν]_[1] _[, ν]_[2][)] = 0 _,_ � � 

- ˆ ˆ 

- (A.104) _cr_ (1 _− a_[3] _cr_ )( _ν_ 1 _− ν_ 2) + _c_[2] _β[σ] β_[2] � _F_ ( _ν_ 1 _, ν_ 2) + _a_[3] _crF_[ˆ] ( _ν_ 1 _, ν_ 2)� = 0 _,_ 

- ˆ ˆ 

- (A.105) _cβ_ ( _ν_ 1 _− ν_ 2) _− σr_[2] � _G_ ( _ν_ 1) + _a_[3] _crG_[ˆ] ( _ν_ 1 _, ν_ 2) _− acβ_ � _F_ ( _ν_ 1 _, ν_ 2) + _a_[3] _crF_[ˆ] ( _ν_ 1 _, ν_ 2)�� = 0 _,_ 

- ˆ ˆ 

- (A.106) _− ν_ 2 _− a_[3] _cr_ ( _ν_ 1 _− ν_ 2) + _κβ − a_[2] _cβ σβ_[2] � _G_ ( _ν_ 1 _, ν_ 2) _− acβ F_[ˆ] ( _ν_ 1 _, ν_ 2)� = 0 _._ 

73 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

The asymptotic behavior of ( _ν_ 1 _, ν_ 2 _, ϕr, ϕβ_ ) is as in the lemma if (A.103)-(A.106) has a non-zero solution ( _ν_ 1 _, ν_ 2 _, cr, cβ_ ) for _a_ = 0. For _a_ = 0, (A.103) implies _ν_ 1 = _κr_ , (A.106) implies _ν_ 2 = _κβ_ , (A.105) implies _cβ_ = _c_ ~~_β_~~[and][(][A.104][)][implies] _[c][r]_[=] _[c]_ ~~_r_~~[.] 

1 Suppose that _a ≈∞_ . Setting ( _ν_ 1 _, ϕr_ ) = ( _a_ 3 _n_ 1 _, a[−]_[1] 3 _cr_ ), we can write (A.99)-(A.102) as 

**==> picture [467 x 95] intentionally omitted <==**

The asymptotic behavior of ( _ν_ 1 _, ν_ 2 _, ϕr, ϕβ_ ) is as in the lemma if (A.107)-(A.110) has a non-zero solution ( _n_ 1 _, ν_ 2 _, cr, ϕβ_ ) for _a_ = _∞_ . Noting that 

**==> picture [190 x 82] intentionally omitted <==**

we can write (A.107)-(A.110) for _a_ = _∞_ as 

**==> picture [465 x 125] intentionally omitted <==**

Equations (A.112) and (A.113) imply (A.92). Equation (A.92) has a solution _ν_ 2. Indeed, when _ν_ 2 goes to infinity, the left-hand side is 

**==> picture [176 x 25] intentionally omitted <==**

74 

D. VAYANOS AND J.-L. VILA 

because _[θ]_[(] _τ[τ]_[)] has a finite limit at zero, and the right-hand side is 

**==> picture [284 x 25] intentionally omitted <==**

because _α_ ( _τ_ ) has a positive limit at zero. Hence, the left-hand side exceeds the right-hand side. When ( _α_ ( _τ_ ) _, {θk_ ( _τ_ ) _}k_ =1 _,..,K_ ) 

become zero for _τ_ larger than a finite threshold _T_ , and _ν_ 2 goes to minus infinity, the left-hand side is 

**==> picture [260 x 23] intentionally omitted <==**

and is smaller than the right-hand side, which is 

**==> picture [223 x 26] intentionally omitted <==**

Hence, a solution _ν_ 2 _∈_ ( _−∞, ∞_ ) to (A.92) exists. When _T_ = _∞_ , ( _α_ ( _τ_ ) _, θ_ ( _τ_ )) _≈_ ( _αe[−][δ][α][τ] , θe[−][δ] α[′][τ]_ ) for _τ_ large and for 0 _< δα ≤ δα[′]_[.][When] _[ν]_[2][goes][to] _[−][δ]_ 2 _[α]_[,][the][right-hand][side][goes][to][infinity,][while][the][left-hand][side][remains][finite.][Hence,][a][solution] _ν_ 2 _∈_ � _−[δ]_ 2 _[α][,][ ∞]_ � to (A.92) exists. 

Using (A.112) to eliminate _cr_ in (A.111), we find _n_ 1 = _n_ 1. Equations (A.112) and (A.114) imply _cr_ = _cr_ and _ϕβ_ = _ϕβ_ , respectively. The Cauchy-Schwarz inequality implies _n_ 1 _>_ 0, and hence _cr <_ 0. _Q.E.D._ **Proof of Proposition 6:** Proceeding as in the proof of Proposition 3, we find that the FB regression coefficient is 

**==> picture [350 x 71] intentionally omitted <==**

where 

**==> picture [306 x 15] intentionally omitted <==**

for _j_ = _r, β_ . Taking the limit in (A.115) when ∆ _τ →_ 0, and noting from (A.75) and (A.76) that _[A][r]_ ∆[(][∆] _τ[τ]_[)] _→_ 1 and _Aβ_ ∆(∆ _τ τ_ ) _→_ 0, we find 

**==> picture [328 x 37] intentionally omitted <==**

75 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

For _τ <_ min _{τ,_ ¯ ˆ _τ }_ , _Ar_ ( _τ_ ) _>_ 0, _Aβ_ ( _τ_ ) _>_ 0 and _A[′] β_[(] _[τ]_[)] _[ >]_[ 0.][Moreover,][(][A.73][)][implies] 

(A.117) _A[′] r_[(] _[τ]_[) +] _[ κ][r][A][r]_[(] _[τ]_[)] _[ −]_[1 =] _[ −][aσ] r_[2] _[I][r,r][A][r]_[(] _[τ]_[)] _[ −][aσ] β_[2] _[I][r,β][A][β]_[(] _[τ]_[)] _[ ≤]_[0] _[,]_ 

**==> picture [256 x 12] intentionally omitted <==**

where the inequalities follow from _Ar_ ( _τ_ ) _>_ 0, _Aβ_ ( _τ_ ) _>_ 0, _Ir,r ≥_ 0 and _Ir,β ≥_ 0, which in turn follows from _M_ 1 _,_ 2 _≥_ 0 and (A.26). 

Equations (A.116), _Aβ_ ( _τ_ ) _>_ 0, _A[′] β_[(] _[τ]_[)] _[ >]_[ 0,][(][A.117][)][and][(][A.118][)][imply] _[b]_[FB] _[>]_[ 0.] 

When _a ≈_ 0, (A.75), (A.76) and ( _ν_ 1 _, ν_ 2 _, ϕr, ϕβ_ ) _≈_ ( _κr, κβ , a_[3] _c_ ~~_r_~~ _[, a][c]_ ~~_β_~~[)][(Lemma][A.2][)][imply] 

**==> picture [279 x 38] intentionally omitted <==**

where 

**==> picture [127 x 21] intentionally omitted <==**

Since _Lβ_ ( _τ_ ) _L[′] β_[(] _[τ]_[)] _[ >]_[ 0,][and][(][A.85][)][and][(][A.93][)][imply] 

**==> picture [232 x 23] intentionally omitted <==**

_b_ FB _>_ 0. 

1 When _a ≈∞_ , (A.75), (A.76) and ( _ν_ 1 _, ν_ 2 _, ϕr, ϕβ_ ) _≈_ ( _a_ 3 _n_ 1 _, ν_ 2 _, a[−]_ 3[1] _cr, ϕβ_ ) (Lemma A.2) imply that for _τ_ bounded away from 

zero 

**==> picture [380 x 37] intentionally omitted <==**

Hence, _b_ FB _>_ 1. We next show that _b_ FB increases in _τ_ if (43) holds. Equation (43) implies that the left-hand side of (A.92) exceeds the right-hand side for _ν_ 2 = 0, and hence (A.92) has a solution _ν_ 2 _<_ 0. We write (A.120) as 

**==> picture [182 x 33] intentionally omitted <==**

where 

**==> picture [84 x 40] intentionally omitted <==**

76 

D. VAYANOS AND J.-L. VILA 

and _z ≡−ν_ 2 _>_ 0, and consider the derivative 

**==> picture [320 x 41] intentionally omitted <==**

Since 

**==> picture [148 x 22] intentionally omitted <==**

_N_ FB _[′]_[(] _[τ]_[)] _[D]_[FB][(] _[τ]_[)] _[ −][N]_[FB][(] _[τ]_[)] _[D]_ FB _[′]_[(] _[τ]_[)] _[ >]_[ 0.][Since,][in][addition,] 

**==> picture [101 x 10] intentionally omitted <==**

_b_ FB increases in _τ_ . 

Proceeding as in the proof of Proposition 3, we find that the CS regression coefficient is 

**==> picture [396 x 238] intentionally omitted <==**

For _τ <_ min _{τ,_ ¯ ˆ _τ }_ , _Aβ_ ( _τ_ ) _>_ 0, _A[′] β_[(] _[τ]_[)] _[ >]_[ 0,][and][(][A.117][)][and][(][A.118][)][hold.][Equation][(][A.118][)][and][the][initial][condition] _[A][r]_[(0) = 0] imply _Ar_ ( _τ_ ) _− τ <_ 0. Equations (A.9), _Aβ_ ( _τ_ ) _>_ 0, _A[′] β_[(] _[τ]_[)] _[ >]_[ 0,][(][A.117][)][and] _[A][r]_[(] _[τ]_[)] _[ −][τ][<]_[ 0][imply] _[b]_[CS] _[<]_[ 1.] 

When _a ≈_ 0, (A.75), (A.76), ( _ν_ 1 _, ν_ 2 _, ϕr, ϕβ_ ) _≈_ ( _κr, κβ , a_[3] _c_ ~~_r_~~ _[, a][c] β_[)][(Lemma][A.2][)][and][(][A.119][)][imply] 

**==> picture [247 x 28] intentionally omitted <==**

77 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

Hence, _b_ CS is smaller than and close to one. Moreover, _b_ CS increases in _τ_ because the function _K_ ( _x_ ) defined in Proposition 3 is increasing for _x >_ 0. 

1 When _a ≈∞_ , (A.75), (A.76) and ( _ν_ 1 _, ν_ 2 _, ϕr, ϕβ_ ) _≈_ ( _a_ 3 _n_ 1 _, ν_ 2 _, a[−]_ 3[1] _cr, ϕβ_ ) (Lemma A.2) imply that for _τ_ bounded away from zero 

**==> picture [276 x 37] intentionally omitted <==**

Hence, _b_ CS _<_ 1. We next show that _b_ CS is negative and decreasing in _τ_ if (43) holds. We write (A.124) as 

**==> picture [181 x 38] intentionally omitted <==**

where 

**==> picture [147 x 52] intentionally omitted <==**

and _z ≡−ν_ 2 _>_ 0. Equation (A.125) implies 

**==> picture [197 x 37] intentionally omitted <==**

Since 

**==> picture [270 x 51] intentionally omitted <==**

and _xe[x] − e[x]_ + 1 _>_ 0 for all _x_ , (A.126) implies _b_ CS _<_ 0. Consider next the derivative 

**==> picture [363 x 43] intentionally omitted <==**

78 

D. VAYANOS AND J.-L. VILA 

Since 

**==> picture [339 x 81] intentionally omitted <==**

and _x_[2] _e[x] − xe[x]_ + _e[x] −_ 1 _>_ 0 for all _x_ , _N_ CS _[′]_[(] _[τ]_[)] _[ −][D]_ CS _[′]_[(] _[τ]_[)] _[ >]_[ 0.][Since] 

**==> picture [297 x 22] intentionally omitted <==**

and _e[x] −_ 1 _− x >_ 0 for all _x_ , _N_ CS _[′]_[(] _[τ]_[)] _[D]_[CS][(] _[τ]_[)] _[ −][N]_[CS][(] _[τ]_[)] _[D]_ CS _[′]_[(] _[τ]_[)] _[ >]_[ 0.][Hence,] _[b]_[CS][decreases][in] _[τ]_[.] 

**==> picture [28 x 8] intentionally omitted <==**

**Proof of Proposition 7:** Substituting _C_ ( _τ_ ) from (41) into (42), using Γ = _Diag_ ( _κr, κβ_ ) and Σ = _Diag_ ( _σr_[2] _[, σ] β_[2][),][and][dropping] the subscript 1 from functions of the single demand factor, we find 

**==> picture [384 x 183] intentionally omitted <==**

The system of (A.127) and (A.128) is linear in ( _χr, χβ_ ) and its solution is 

**==> picture [387 x 112] intentionally omitted <==**

79 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

where 

and 

**==> picture [353 x 100] intentionally omitted <==**

for _j_ = _r, β_ . The effect of a change in the demand intercept from _θ_ 0( _τ_ ) to _θ_ 0( _τ_ ) + ∆ _θ_ 0( _τ_ ) on the yield _yt_[(] _[τ]_[)] for maturity _τ_ is ∆ _yt_[(] _[τ]_[)] _≡_[∆] _[C] τ_[(] _[τ]_[)] , which from (41), (A.129) and (A.130) is 

**==> picture [29 x 9] intentionally omitted <==**

**==> picture [354 x 114] intentionally omitted <==**

Hence, the change ∆ _θ_ 0( _τ_ ) affects yields only through �0 _∞_ ∆ _θ_ 0( _τ_ ) _Ar_ ( _τ_ ) _dτ_ and �0 _∞_ ∆ _θ_ 0( _τ_ ) _Aβ_ ( _τ_ ) _dτ_ . When the change ∆ _θ_ 0( _τ_ ) is a Dirac function with point mass at _τ[∗]_ , 

**==> picture [113 x 20] intentionally omitted <==**

for _j_ = _r, β_ , and (A.131) becomes 

**==> picture [289 x 156] intentionally omitted <==**

80 

D. VAYANOS AND J.-L. VILA 

Using (A.132), we can write (44) in the equivalent form 

**==> picture [409 x 95] intentionally omitted <==**

To show that (A.133) holds, we show that each of the two terms in brackets is positive. The second term is positive because it has the same sign as 

**==> picture [318 x 81] intentionally omitted <==**

where the second step follows because _Aβ_ ( _τ_ ) _>_ 0 and � _AAβr_ (( _ττ_ )) � _′ <_ 0 for _τ ∈_ (0 _,_ ˆ _τ_ ). The first term is equal to 

� _Ar_ ( _τ_ 1) _Aβ_ ( _τ_ 2) _− Ar_ ( _τ_ 2) _Aβ_ ( _τ_ 1)� _D,_ 

**==> picture [440 x 79] intentionally omitted <==**

where _dα_ ˆ( _τ_ ) denotes the measure generated by the non-decreasing function _−α_ ( _τ_ ) (which is possibly discontinuous at a finite threshold _T_ ). Since 

**==> picture [239 x 25] intentionally omitted <==**

where the second step follows because _M_ is finite, (A.134) implies 

**==> picture [292 x 23] intentionally omitted <==**

81 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

Likewise, 

**==> picture [389 x 214] intentionally omitted <==**

Equations (A.135) and (A.136) imply that _D >_ 0 if 

**==> picture [228 x 57] intentionally omitted <==**

which holds because of the Cauchy-Schwarz inequality. 

_Q.E.D._ 

## APPENDIX B: DEMAND OF PREFERRED-HABITAT INVESTORS 

There are overlapping generations of preferred-habitat investors living for a period of length _T < ∞_ , and of arbitrageurs living for a period of length _dt_ . Thus, at each point in time there is a continuum of investor generations and one arbitrageur generation. Arbitrageurs and investors receive endowment _W_ at the beginning of their life and consume at the end of their life. Arbitrageurs use their endowment to buy bonds. Investors use their endowment to buy bonds and to invest in a private opportunity (“real estate”) that pays at the end of their life. To ensure that the slope of the investors’ demand for bonds is finite, we require that substitution between bonds and the private opportunity is imperfect. We model imperfect substitution by assuming that bonds pay in a good 1 (“money”) and the private opportunity pays in a different good 2 (“real estate services”). The endowment _W_ is in good 1. Arbitrageurs and investors can use good 1 to invest in bonds and in the private opportunity. 

Consider the optimization problem of an investor _n_ born at time 0. We denote by _Z_[ˆ] _n,t_[(] _[τ]_[)][the][number][of][units][of][the][bond] with maturity _τ_ that the investor holds at time _t ∈_ [0 _, T_ ], where one unit of the bond is an investment in the bond with face 

82 

D. VAYANOS AND J.-L. VILA 

value one. We denote by _Wn,t_ the value of the investor’s bond portfolio at time _t_ and by _dcn,t_ the investment in the private opportunity between _t_ and _t_ + _dt_ , both expressed in units of good 1. We denote by ( _W_[ˆ] _n,t, dc_ ˆ _n,t_ ) the counterparts of ( _Wn,t, dcn,t_ ) when expressed in units of the bond maturing at time _T_ : 

**==> picture [62 x 22] intentionally omitted <==**

**==> picture [62 x 22] intentionally omitted <==**

We finally denote by _β_[ˆ] _n,t_[(] _[T][ −][t]_[)] _>_ 0 the number of units of good 2 that an investment of one unit of good 1 at time _t_ yields at time 

_T_ . The investor’s budget constraint is 

**==> picture [199 x 26] intentionally omitted <==**

The investor’s utility at time _T_ is 

**==> picture [172 x 21] intentionally omitted <==**

and consists of two parts: a utility _u_ ( _Cn,T_ ) that is an increasing and concave function of the consumption _Cn,T_ of good 1 at time _T_ , and a utility �0 _T β_ ˆ _n,t_[(] _[T][ −][t]_[)] _Pt_[(] _[T][ −][t]_[)] _dc_ ˆ _n,t_ that is equal to the consumption of good 2 at time _T_ and is derived from the accumulated investment in the private opportunity between times 0 and _T_ . The marginal utility _u[′]_ ( _Cn,T_ ) converges to infinity when _Cn,T_ goes to a lower bound _C_ and to zero when _Cn,T_ goes to infinity. The investor has max-min preferences. At each time _t ∈_ [0 _, T_ ], the investor chooses ( _Z_[ˆ] _n,t_[(] _[τ]_[)] _[,]_[ ˆ] _[c][n,t]_[)][to][maximize][the][minimum][of][(][B.2][)][over][sample][paths][of] _[q][t]_[=][(] _[r][t][, β]_[1] _[,t][, .., β][K,t]_[)] _[⊤]_[and] _[β]_[ˆ] _n,t_[(] _[T][ −][t]_[)] , subject to the budget constraint (B.1) and the terminal condition _Cn,T_ = _W_[ˆ] _n,T_ . 

Proposition B.1 _Assume that_ Σ _has full rank, K ≥_ 1 _, β_[ˆ] _n,t_[(] _[T][ −][t]_[)] _is a function of_ ( _β_ 1 _,t, .., βK,t_ ) _, and the term structure involves no arbitrage, i.e., (34) holds. At time t, the investor holds only the bond maturing at time T and no other bonds. The number Z_ ˆ _n,t_[(] _[T][ −][t]_[)] _of units of the bond held by the investor solves_ 

**==> picture [154 x 16] intentionally omitted <==**

**Proof:** Defining ( _µ_ ˆ _Z,n,t[, σ]_[ ˆ] _Z,n,t_[)][by] 

**==> picture [184 x 26] intentionally omitted <==**

83 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

where _dBt_ = ( _dBr,t, dBβ,_ 1 _,t, .., dBβ,K,t_ ) _[⊤]_ , we write the budget constraint (B.1) as 

**==> picture [186 x 13] intentionally omitted <==**

Integrating (B.4) from 0 to _T_ and using the terminal condition _Cn,T_ = _W_[ˆ] _n,T_ , we write the investor’s optimization problem at _t_ = 0 as 

(B.5) 

**==> picture [339 x 57] intentionally omitted <==**

where we allow for the possibility that _c_ ˆ _n,t_ has a discrete change ∆ˆ _cn,_ 0 at _t_ = 0. Since Σ has full rank and _K ≥_ 1, _rt_ is not perfectly correlated with ( _β_ 1 _,t, .., βK,t_ ). Since, in addition, _β_[ˆ] _n,t_[(] _[T][ −][t]_[)] is a function of ( _β_ 1 _,t, .., βK,t_ ), sample paths of _qt_ and _β_[ˆ] _n,t_[(] _[T][ −][t]_[)] ˆ exist such that _β_[ˆ] _n,t_[(] _[T][ −][t]_[)] _Pt_[(] _[T][ −][t]_[)] = _u[′]_[ �] _Wn,_ 0 _−_ ∆ˆ _cn,_ 0� for _t > ϵ_ and for any _ϵ >_ 0. Hence, the minimum in (B.5) is smaller than 

**==> picture [273 x 57] intentionally omitted <==**

which in turn is smaller than 

**==> picture [424 x 25] intentionally omitted <==**

because _u_ is concave. If _σ_ ˆ _Z,n,t_[= 0][for][any][interval][in][(0] _[, T]_[),][then][the][minimum][in][(][B.6][)][is][minus][infinity][because][the][Brownian] motion has infinite variation. Therefore, _σ_ ˆ _Z,n,t_[=][0,][i.e.,][the][investor][holds][the][bond][maturing][at][time] _[T]_[and][zero][units][of][all] other bonds. Since absence of arbitrage requires _µ_ ˆ _Z,n,t_[= 0,][(][B.6][)][is][smaller][than] 

**==> picture [138 x 15] intentionally omitted <==**

and hence 

**==> picture [383 x 85] intentionally omitted <==**

84 

D. VAYANOS AND J.-L. VILA 

Setting _Z_[ˆ] _n,t_[(] _[τ]_[)][=][0][for] _[t][≥]_[0][and] _[τ]_[=] _[T][−][t]_[,][and] _[d][c]_[ˆ] _[n,t]_[=][0][for] _[t][>]_[0,][in][(][B.5][),][we][find][that][(][B.7][)][holds][also][in][the][reverse][sense,] and is therefore an equality. The optimal ∆ˆ _cn,_ 0 thus satisfies 

**==> picture [162 x 15] intentionally omitted <==**

Since _W_[ˆ] _n,_ 0 _−_ ∆ˆ _cn,_ 0 represents units of the bond maturing at time _T_ that the investor holds at time 0, (B.8) yields (B.3) for _t_ = 0. The same argument yields (B.3) for _t >_ 0. _Q.E.D._ 

Proposition B.1 implies that preferred-habitat investors demand only the bond whose maturity coincides with the time when they consume. To ensure that the demand by preferred-habitat investors takes the specific functional form (5)-(7), we assume specific functions for the utility _u_ and the return _β_[ˆ] _n,t_[(] _[τ]_[)][on][the][private][opportunity.] 

Suppose _C_ = _−∞_ , _u_ ( _Cn,T_ ) = _−e[−][C][n,T]_ and _β_[ˆ] _n,t_[(] _[τ]_[)][=] _[e][β] t_[(] _[τ]_[)] , where _βt_[(] _[τ]_[)] is given by (6) and (7). Proposition B.1 implies that the number _Z_[ˆ] _n,t_[(] _[T][ −][t]_[)] of units of the bond maturing at time _T_ and held at time _t_ by an investor _n_ born at time 0 is given by 

**==> picture [245 x 17] intentionally omitted <==**

This coincides with the demand (5)-(7) with _α_ ( _τ_ ) = 1, except that (5)-(7) concern the present value of the bond rather than its face value, i.e., the units of the bond. To derive the demand (5)-(7) expressed in present-value terms, we modify the assumed functions for _u_ and _β_[ˆ] _n,t_[(] _[τ]_[)][.][We][can][obtain][the][demand][(][5][)-(][7][)][for][a][set][of][values][of] _[q][t]_[whose][probability][can][be][made][arbitrarily] close to one. 

Suppose that there are two types of preferred-habitat investors born at each time _t_ , in equal measure. For type 1 investors, _C_ = 0, _u_ ( _Cn,t_ + _T_ ) = log( _Cn,t_ + _T_ ) and _β_[ˆ] _n,t_[(] _[T]_[ +] _[′][t][−][t][′]_[)] = _−_ min _{βt_[(] _[′][T]_[ +] 1 _[t][−][t][′]_[)] _,−ϵ}_[,][where] _[β] t_[(] _[τ]_[)] is given by (6) and (7), and _ϵ_ is positive and small. For type 2 investors, _C_ = _−∞_ and _β_[ˆ] _n,t_[(] _[T]_[ +] _[′][t][−][t][′]_[)] = 1. To define _u_ ( _Cn,t_ + _T_ ) for type 2 investors, we start with the function 

**==> picture [65 x 19] intentionally omitted <==**

defined for _x >_ 0. The function _N_ ( _x_ ) converges to infinity when _x_ goes to zero, and to zero when _x_ goes to infinity. It decreases for _x ∈_ (0 _, e_ ), and increases for _x ∈_ ( _e, T_ ). Its minimum value, obtained for _x_ = _e_ , is _−_[1] _e_[.][We][take] _[x]_[to][represent][marginal] utility _u[′]_ ( _Cn,t_ + _T_ ), and _N_ ( _x_ ) to represent _Cn,t_ + _T_ . This defines _u_ ( _Cn,t_ + _T_ ) for _Cn,t_ + _T > −_[1] _e_[and] _[u][′]_[(] _[C][n,t]_[+] _[T]_[ )] _[ ∈]_[(0] _[, e]_[).][To][define] _u_ ( _Cn,t_ + _T_ ) for _Cn,t_ + _T < −_[1] _e_[and] _[u][′]_[(] _[C][n,t]_[+] _[T]_[ )] _[>][e]_[,][we][extend] _[u][′]_[(] _[C][n,t]_[+] _[T]_[ )][as][a][linear][function][of] _[C][n,T]_[ .][(Other][extensions][are] possible as well.) We set the derivative of the linear function so that _u[′]_ ( _Cn,t_ + _T_ ) is continuously differentiable at the extension point, and take the extension point to be _u[′]_ ( _Cn,t_ + _T_ ) = _e_ (1 _− ϵ_ ) (rather than _u[′]_ ( _Cn,t_ + _T_ ) = _e_ ) so that the derivative is finite. 

85 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

We thus set 

**==> picture [208 x 11] intentionally omitted <==**

**==> picture [318 x 21] intentionally omitted <==**

Since _u[′]_ ( _Cn,t_ + _T_ ) is positive and decreasing, _u_ ( _Cn,t_ + _T_ ) is increasing and concave. 

Proposition B.1 implies that the number _Z_[ˆ] _n,t_[(] _[T][ −][t]_[)] of units of the bond maturing at time _T_ and held at time _t_ by a type 1 

investor born at time 0 is given by 

**==> picture [95 x 23] intentionally omitted <==**

This yields the demand 

**==> picture [139 x 23] intentionally omitted <==**

expressed in present-value terms, when _βt_[(] _[T][ −][t]_[)] _< −ϵ_ . Proposition B.1 implies that the number _Z_[ˆ] _n,t_[(] _[T][ −][t]_[)] of units of the bond 

maturing at time _T_ and held at time _t_ by a type 2 investor born at time 0 is given by 

**==> picture [94 x 15] intentionally omitted <==**

when _Pt_[(] _[T][ −][t]_[)] _< e_ (1 _− ϵ_ ). This yields the demand 

**==> picture [210 x 15] intentionally omitted <==**

expressed in present-value terms. The aggregate demand, expressed in present-value terms, across type 1 and type 2 investors 

when _βt_[(] _[T][ −][t]_[)] _< −ϵ_ and _Pt_[(] _[T][ −][t]_[)] _< e_ (1 _− ϵ_ ) is 

**==> picture [94 x 15] intentionally omitted <==**

and coincides with the demand (5)-(7) with _α_ ( _τ_ ) = 1. Condition _βt_[(] _[T][ −][t]_[)] _< −ϵ_ requires that the demand intercept in (5) is negative (smaller than _−ϵ_ ). Condition _Pt_[(] _[T][ −][t]_[)] _< e_ (1 _− ϵ_ ) requires that zero-coupon bonds trade below _e_ (1 _− ϵ_ ) and hence below par value. The probability of the set of values of _qt_ such that the two conditions hold simultaneously can be made arbitrarily close to one if _r_ is sufficiently large and _θ_ 0( _τ_ ) sufficiently small. 

Proposition B.1 and the subsequent analysis require _K ≥_ 1. To extend them to _K_ = 0, we assume that _β_[ˆ] _n,t_[(] _[T][ −][t]_[)] is equal to a deterministic function of _T − t_ plus random noise that is independent across investors _n_ in the same generation. Because of the random noise, _β_[ˆ] _n,t_[(] _[T][ −][t]_[)] is not perfectly correlated with _rt_ , and the proof of Proposition B.1 goes through. Because the random 

noise is independent across investors in the same generation, _β_[ˆ] _n,t_[(] _[T][ −][t]_[)] averages to a deterministic function of _T − t_ . 

86 

## D. VAYANOS AND J.-L. VILA 

## APPENDIX C: CALIBRATION 

## C.1. _Model-Generated Moments_ 

Equations (1) and (30) imply that when there is one demand factor, the yield for maturity _τ_ is 

**==> picture [130 x 19] intentionally omitted <==**

When, in addition, the demand factor is independent of the short rate, the volatility of the yield is 

**==> picture [348 x 114] intentionally omitted <==**

where the second step follows from (A.7) and its counterpart equation for _βt_ . The covariance of yield changes is 

**==> picture [294 x 82] intentionally omitted <==**

The correlation of yield changes can be computed from (C.2) and (C.3). The principal components can be computed from the 

covariance matrix of yield changes, with element ( _τ_ 1 _, τ_ 2) given by (C.3). The FB and CS regression coefficients are given by (A.115) and (A.122), respectively. 

The volume during an infinitesimal interval [ _t, t_ + _dt_ ] for the bond with maturity _τ ∈_ (0 _, T_ ) is the absolute value of the change 

**==> picture [268 x 31] intentionally omitted <==**

**==> picture [286 x 11] intentionally omitted <==**

where the first step follows from (5), and the second from (6) and (30) written for one demand factor. Equation (C.4) implies that expected volume is 

**==> picture [334 x 25] intentionally omitted <==**

87 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

where independence between the short rate and demand implies 

**==> picture [184 x 13] intentionally omitted <==**

**==> picture [244 x 17] intentionally omitted <==**

In our calculations of relative volume we use ~~�~~ _V_ ( _τ_ ), which is proportional to expected volume. 

When yields across all maturities change by ∆ _y_ , (1) and (5) imply that the demand of preferred-habitat investors changes by 

**==> picture [267 x 22] intentionally omitted <==**

Setting ( _T, δα,_ ∆ _y_ ) = (30 _,_ 0 _._ 297 _,_ 0 _._ 0001) and the demand change to 0.0059, we find _α_ = 5 _._ 21. 

## C.2. _Calibrated Parameters_ 

Tables C.I and C.II report the calibrated parameters and the empirical moments used to determine them, for the sub-sample of nominal yields and the sample of real yields, respectively. 

## C.3. _Elasticities_ 

The matrix in the top panel of Table C.III reports the elasticities of the first seven model-generated moments in Table I with respect to the first seven parameters, for the main sample of nominal yields. The elasticities are computed by varying each parameter from its value in Table I times 1 _._ 001 to its value in Table I times 0 _._ 999, computing the change in the corresponding model-generated moment, dividing by the value of that moment in the base case, and multiplying by 500. 

The elasticities involving ( _δα, δθ_ ) are hard to interpret because they combine multiple effects. For example, an increase in _δθ_ lowers the relative volume for long maturities. It also strengthens the effect of demand shocks on yields, since the shocks’ magnitude is _θ_ ( _τ_ ) = _θ_ � _e[−][δ][α][τ] − e[−][δ][θ][τ]_[�] , which increases in _δθ_ . This raises the volatility of yields and lowers the correlation between yield changes at short and long maturities. 

To disentangle the effects and facilitate the interpretation of the elasticities, we modify the matrix in the top panel of Table C.III by subtracting columns _i_ = 4 _,_ 5 from columns _j_ = 6 _,_ 7, after multiplying each time column _i_ by the scalar needed to make element ( _i, j_ ) equal to zero. For _i_ = 4, this amounts to keeping the volatility of annual yield changes constant when changing ( _δα, δθ_ ), through a compensating change in _aθ_ . For _i_ = 5, this amounts to keeping the correlation between annual changes to the one-year yield and to other yields constant when changing ( _δα, δθ_ ), through a compensating change in _aα_ . Eliminating the effects of ( _δα, δθ_ ) on the volatility of yields and on the correlation between them results in the simpler matrix of modified elasticities in the bottom panel of Table C.III. We focus on that matrix from now on. 

The parameter _κr_ has its strongest, negative, effect on the volatility of the one-year yield. The parameter _σr_ has its strongest, positive, effect on the volatility of the one-year yield and on the volatility of annual changes to that yield. Other parameters 

88 

D. VAYANOS AND J.-L. VILA 

TABLE C.I 

Calibration of model parameters for the sub-sample of nominal yields. 

|**Parameter**|**Value**||**Empirical moment**|**Empirical moment**|**Value**|
|---|---|---|---|---|---|
|||||||
|_κr_<br>Mean-reversion of _rt_<br>_σr_<br>Difusion of _rt_<br>_κβ_<br>Mean-reversion of _βt_<br>_aθ_<br>Arb. risk-aversion<br>_×_ PH demand shock<br>_aα_<br>Arb. risk-aversion<br>_×_ PH demand slope<br>_δα_<br>PH demand shock<br>– short maturities<br>_δθ_<br>PH demand shock<br>– long maturities<br>_α_<br>PH demand slope|0.240<br>0.0159<br>0.127<br>5305<br>80.3<br>0.269<br>0.279<br>4.28||�<br>Var<br>�<br>_y_(1)<br>_t_<br>�<br>Volatility 1-year yield<br>– Levels<br>�<br>Var<br>�<br>_y_(1)<br>_t_+1 _−y_(1)<br>_t_<br>�<br>Volatility 1-year yield<br>– Annual changes<br>1<br>30<br>�30<br>_τ_=1<br>�<br>Var<br>�<br>_y_(_τ_)<br>_t_<br>�<br>Volatility _τ_-year yield<br>– Levels, average over _τ_<br>1<br>30<br>�30<br>_τ_=1<br>�<br>Var<br>�<br>_y_(_τ_)<br>_t_+1 _−y_(_τ_)<br>_t_<br>�<br>Volatility _τ_-year yield<br>– Annual changes, average over _τ_<br>1<br>30<br>�30<br>_τ_=1 Corr<br>�<br>_y_(1)<br>_t_+1 _−y_(1)<br>_t_<br>_, y_(_τ_)<br>_t_+1 _−y_(_τ_)<br>_t_<br>�<br>Correlation 1-year yield with _τ_-year yield<br>– Annual changes, average over _τ_<br>�<br>0_<τ≤_2 Volume(_τ_)<br>�<br>0_<τ≤_30 Volume(_τ_)<br>Relative volume for maturities _τ ∈_(0_,_2]<br>�<br>11_<τ≤_30 Volume(_τ_)<br>�<br>0_<τ≤_30 Volume(_τ_)<br>Relative volume for maturities _τ ∈_(11_,_30]<br>Estimate in KVJ 2012||1.89<br>1.24<br>1.36<br>0.705<br>0.369<br>0.199<br>0.094<br>-0.746|



89 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

TABLE C.II 

Calibration of model parameters for the sample of real yields. 

|**Parameter**|**Value**||**Empirical moment**|**Empirical moment**|**Value**|
|---|---|---|---|---|---|
|||||||
|_κr_<br>Mean-reversion of _rt_<br>_σr_<br>Difusion of _rt_<br>_κβ_<br>Mean-reversion of _βt_<br>_aθ_<br>Arb. risk-aversion<br>_×_ PH demand shock<br>_aα_<br>Arb. risk-aversion<br>_×_ PH demand slope<br>_δα_<br>PH demand shock<br>– short maturities<br>_δθ_<br>PH demand shock<br>– long maturities<br>_α_<br>PH demand slope|0.395<br>0.0216<br>0.098<br>643<br>44.5<br>0.265<br>0.308<br>4.16||�<br>Var<br>�<br>_y_(2)<br>_t_<br>�<br>Volatility 2-year yield<br>– Levels<br>�<br>Var<br>�<br>_y_(2)<br>_t_+1 _−y_(2)<br>_t_<br>�<br>Volatility 2-year yield<br>– Annual changes<br>1<br>19<br>�20<br>_τ_=2<br>�<br>Var<br>�<br>_y_(_τ_)<br>_t_<br>�<br>Volatility _τ_-year yield<br>– Levels, average over _τ_<br>1<br>19<br>�20<br>_τ_=2<br>�<br>Var<br>�<br>_y_(_τ_)<br>_t_+1 _−y_(_τ_)<br>_t_<br>�<br>Volatility _τ_-year yield<br>– Annual changes, average over _τ_<br>1<br>19<br>�20<br>_τ_=2 Corr<br>�<br>_y_(2)<br>_t_+1 _−y_(2)<br>_t_<br>_, y_(_τ_)<br>_t_+1 _−y_(_τ_)<br>_t_<br>�<br>Correlation 2-year yield with _τ_-year yield<br>– Annual changes, average over _τ_<br>�<br>0_<τ≤_2 Volume(_τ_)<br>�<br>0_<τ≤_30 Volume(_τ_)<br>Relative volume for maturities _τ ∈_(0_,_2]<br>�<br>11_<τ≤_30 Volume(_τ_)<br>�<br>0_<τ≤_30 Volume(_τ_)<br>Relative volume for maturities _τ ∈_(11_,_30]<br>Estimate in KVJ 2012||1.59<br>1.23<br>1.30<br>0.674<br>0.660<br>0.199<br>0.094<br>-0.746|



90 

## D. VAYANOS AND J.-L. VILA 

TABLE C.III 

Elasticities and modified elasticities of model-generated moments with respect to model parameters for the main sample of nominal yields. 

||**Parameter**|**Parameter**|_κr_|_κr_|_σr_|_σr_|_κβ_|_κβ_|_aθ_|_aθ_|_aα_|_aα_|_δα_|_δα_|_δθ_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||||
|�<br>Var<br>�<br>_y_(1)<br>_t_<br>�<br>�<br>Var<br>�<br>_y_(1)<br>_t_+1 _−y_(1)<br>_t_<br>�<br>1<br>19<br>�30<br>_τ_=1<br>~~�~~<br>Var<br>�<br>_y_(_τ_)<br>_t_<br>�<br>1<br>19<br>�30<br>_τ_=1<br>~~�~~<br>Var<br>�<br>_y_(_τ_)<br>_t_+1 _−y_(_τ_)<br>_t_<br>�<br>1<br>19<br>�30<br>_τ_=1 Corr<br>�<br>_y_(2)<br>_t_+1 _−y_(2)<br>_t_<br>_, y_(_τ_)<br>_t_+1 _−y_(_τ_)<br>_t_<br>�<br>�<br>0_<τ≤_2 Volume(_τ_)<br>�<br>0_<τ≤_30 Volume(_τ_)<br>�<br>11_<τ≤_30 Volume(_τ_)<br>�<br>0_<τ≤_30 Volume(_τ_)|||-0.538<br>-0.074<br>-0.318<br>-0.202<br>0.083<br>-0.019<br>0.189||0.468<br>0.467<br>0.344<br>0.330<br>-0.207<br>0.179<br>-0.365||-0.006<br>-0.001<br>-0.672<br>-0.256<br>0.225<br>-0.036<br>0.236||0.017<br>0.012<br>1.493<br>1.243<br>-1.443<br>0.028<br>-0.519||-0.041<br>-0.039<br>-0.903<br>-0.791<br>0.514<br>0.165<br>-0.106||-0.448<br>-0.315<br>-43.873<br>-36.446<br>43.209<br>-0.379<br>15.304||0.500<br>0.009<br>43.661<br>36.340<br>-42.273<br>1.192<br>-16.877|
|||||||||||||||||
|||||||||||||||||
||**Parameter**|||_κr_||_σr_||_κβ_||_aθ_||_aα_||_δα_|_δθ_|
|||||||||||||||||
|~~�~~<br>Var<br>�<br>_y_(1)<br>_t_<br>�<br>~~�~~<br>Var<br>�<br>_y_(1)<br>_t_+1 _−y_(1)<br>_t_<br>�<br>1<br>19<br>�30<br>_τ_=1<br>�<br>Var<br>�<br>_y_(_τ_)<br>_t_<br>�<br>1<br>19<br>�30<br>_τ_=1<br>�<br>Var<br>�<br>_y_(_τ_)<br>_t_+1 _−y_(_τ_)<br>_t_<br>�<br>1<br>19<br>�30<br>_τ_=1 Corr<br>�<br>_y_(2)<br>_t_+1 _−y_(2)<br>_t_<br>_, y_(_τ_)<br>_t_+1 _−y_(_τ_)<br>_t_<br>�<br>�<br>0_<τ≤_2 Volume(_τ_)<br>�<br>0_<τ≤_30 Volume(_τ_)<br>�<br>11_<τ≤_30 Volume(_τ_)<br>�<br>0_<τ≤_30 Volume(_τ_)||||-0.538<br>-0.074<br>-0.318<br>-0.202<br>0.083<br>-0.019<br>0.189||0.468<br>0.467<br>0.344<br>0.330<br>-0.207<br>0.179<br>-0.365||-0.006<br>-0.001<br>-0.672<br>-0.256<br>0.225<br>-0.036<br>0.236||0.017<br>0.012<br>1.493<br>1.243<br>-1.443<br>0.028<br>-0.519||-0.041<br>-0.039<br>-0.903<br>-0.791<br>0.514<br>0.165<br>-0.106||-0.017<br>-0.018<br>0.008<br>0<br>0<br>0.856<br>-0.875|0.011<br>0.009<br>0.003<br>0<br>0<br>0.327<br>-1.617|



91 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

have much weaker effects on these volatilities. Hence, the volatility of the one-year yield identifies _κr_ , and the volatility of annual changes to that yield identifies _σr_ . 

The parameter _κβ_ has its strongest, negative, effect on the average volatility of yields. The parameters ( _aθ, aα_ ) have their strongest effects on the average volatility of yields, on the average volatility of annual yield changes, and on the average correlation between annual changes to the one-year yield and to other yields. Hence, the average volatility of yields identifies _κβ_ , and the other two moments identify ( _aθ, aα_ ).[23] 

The parameters ( _δα, δθ_ ) have their strongest effect on relative volume, positive for short maturities and negative for long maturities. The effect of _δθ_ on short-maturity volume is weaker. Hence, the relative volume for maturities two years and below identifies _δα_ , and the relative volume for maturities eleven years and above identifies _δθ_ . 

Tables C.IV and C.V provide counterpart matrices to that in the bottom panel of Table C.III, for the sub-sample of nominal yields and the sample of real yields, respectively. The modified elasticities for these samples have similar magnitudes and signs to those for the main sample of nominal yields. 

## C.4. _Figures_ 

Figures C.1 and C.2 compare the empirical moments to the model-generated ones, for the sub-sample of nominal yields and the sample of real yields, respectively. For the sub-sample of nominal yields, the fraction of variation of annual yield changes explained by the first principal component is 74% in the model and 73.8% in the data. For the sample of real yields, maturities range from two to twenty. The one-year yield needed to compute the empirical FB and CS coefficients is obtained by spline interpolation. The first principal component of annual yield changes is scaled to one for the two-year maturity. The fraction of variation of annual yield changes explained by the first principal component is 83.6% in the model and 85.2% in the data. 

## C.5. _Policy Analysis_ 

Consider an unanticipated change ∆ _r_ in the long-run mean _r_ of the short rate _rt_ at time zero that reverts deterministically to zero at the rate _κr_ ~~[.]~~[Writing][bond][prices][at][time] _[t]_[as] 

**==> picture [179 x 13] intentionally omitted <==**

> 23Table C.III shows that an increase in _aα raises_ the correlation between yield changes at short and long maturities (element (5,5) is positive). Intuitively, an increase in _α_ , holding ( _a, θ_ ) constant, weakens the transmission of short-rate shocks to longer maturities, and this lowers correlation. At the same time, demand shocks have weaker effects on yields because shocks are better absorbed when preferred-habitat demand has higher slope. The latter effect lowers volatility and raises correlation. The latter effect also makes the mapping between _aθ_ and volatility, and between _aα_ and correlation, less clear-cut. To isolate the former effect, we consider an increase in _aα_ accompanied by an increase in _aθ_ such that the volatility of annual yield changes remains constant. (This amounts to subtracting column 4 from column 5, after multiplying column 4 by the scalar needed to make element (4 _,_ 5) equal to zero.) Element (5 _,_ 5) then turns negative, capturing only the former effect. 

92 

D. VAYANOS AND J.-L. VILA 

TABLE C.IV 

Modified elasticities of model-generated moments with respect to model parameters for the sub-sample of nominal yields. 

||**Parameter**|**Parameter**|_κr_|_σr_|_κβ_|_aθ_|_aα_|_δα_|_δθ_|
|---|---|---|---|---|---|---|---|---|---|
|||||||||||
|~~�~~<br>Var<br>�<br>_y_(1)<br>_t_<br>�<br>~~�~~<br>Var<br>�<br>_y_(1)<br>_t_+1 _−y_(1)<br>_t_<br>�<br>1<br>19<br>�30<br>_τ_=1<br>�<br>Var<br>�<br>_y_(_τ_)<br>_t_<br>�<br>1<br>19<br>�30<br>_τ_=1<br>�<br>Var<br>�<br>_y_(_τ_)<br>_t_+1 _−y_(_τ_)<br>_t_<br>�<br>1<br>19<br>�30<br>_τ_=1 Corr<br>�<br>_y_(2)<br>_t_+1 _−y_(2)<br>_t_<br>_, y_(_τ_)<br>_t_+1 _−y_(_τ_)<br>_t_<br>�<br>�<br>0_<τ≤_2 Volume(_τ_)<br>�<br>0_<τ≤_30 Volume(_τ_)<br>�<br>11_<τ≤_30 Volume(_τ_)<br>�<br>0_<τ≤_30 Volume(_τ_)|||-0.572<br>-0.137<br>-0.195<br>-0.122<br>0.157<br>-0.045<br>0.269|0.454<br>0.454<br>0.191<br>0.198<br>-0.142<br>0.225<br>-0.362|-0.007<br>-0.001<br>-0.924<br>-0.507<br>0.406<br>-0.107<br>0.767|0.025<br>0.021<br>2.054<br>1.898<br>-2.145<br>0.134<br>-1.626|-0.058<br>-0.057<br>-1.335<br>-1.251<br>0.930<br>0.158<br>0.451|-0.063<br>-0.062<br>0.009<br>0<br>0<br>0.938<br>-0.724|0.065<br>0.061<br>-0.001<br>0<br>0<br>-0.008<br>-1.143|



TABLE C.V 

Modified elasticities of model-generated moments with respect to model parameters for the sample of real yields. 

||**Parameter**|**Parameter**|_κr_|_σr_|_κβ_|_aθ_|_aα_|_δα_|_δθ_|
|---|---|---|---|---|---|---|---|---|---|
|||||||||||
|~~�~~<br>Var<br>�<br>_y_(2)<br>_t_<br>�<br>~~�~~<br>Var<br>�<br>_y_(2)<br>_t_+1 _−y_(2)<br>_t_<br>�<br>1<br>19<br>�20<br>_τ_=2<br>�<br>Var<br>�<br>_y_(_τ_)<br>_t_<br>�<br>1<br>19<br>�20<br>_τ_=2<br>�<br>Var<br>�<br>_y_(_τ_)<br>_t_+1 _−y_(_τ_)<br>_t_<br>�<br>1<br>19<br>�20<br>_τ_=2 Corr<br>�<br>_y_(2)<br>_t_+1 _−y_(2)<br>_t_<br>_, y_(_τ_)<br>_t_+1 _−y_(_τ_)<br>_t_<br>�<br>�<br>0_<τ≤_2 Volume(_τ_)<br>�<br>0_<τ≤_30 Volume(_τ_)<br>�<br>11_<τ≤_30 Volume(_τ_)<br>�<br>0_<τ≤_30 Volume(_τ_)|||-0.627<br>-0.230<br>-0.455<br>-0.386<br>0.129<br>-0.094<br>0.457|0.460<br>0.459<br>0.362<br>0.352<br>-0.153<br>0.241<br>-0.422|-0.012<br>-0.001<br>-0.911<br>-0.427<br>0.377<br>-0.084<br>0.514|0.028<br>0.016<br>1.903<br>1.536<br>-1.671<br>0.022<br>-0.945|-0.054<br>-0.049<br>-1.090<br>-0.916<br>0.683<br>0.230<br>0.051|-0.027<br>-0.028<br>0.012<br>0<br>0<br>0.838<br>-0.823|0.026<br>0.020<br>0.003<br>0<br>0<br>0.176<br>-1.458|



93 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

**==> picture [400 x 482] intentionally omitted <==**

**----- Start of picture text -----**<br>
3 1.5<br>2.5<br>2 1<br>1.5<br>1 0.5<br>0.5<br>0 0<br>0 5 10 15 20 25 30 0 5 10 15 20 25 30<br>Maturity (years) Maturity (years)<br>1 1.5<br>0.8<br>1<br>0.6<br>0.4<br>0.5<br>0.2<br>0 0<br>0 5 10 15 20 25 30 0 5 10 15 20 25 30<br>Maturity (years) Maturity (years)<br>3.5<br>1<br>3<br>0.5<br>2.5<br>0<br>2<br>-0.5<br>1.5<br>-1<br>1<br>-1.5<br>0.5<br>-2<br>0<br>-2.5<br>0 5 10 15 20 25 30 0 5 10 15 20 25 30<br>Maturity (years) Maturity (years)<br>Volatility of yield -- Levels<br>Volatility of yield -- Annual changes<br>Correlation with one-year yield -- Annual changes First principal component -- Annual yield changes<br>Fama-Bliss regression coefficient<br>Campbell-Shiller regression coefficient<br>**----- End of picture text -----**<br>


Figure C.1.— Model-generated and empirical moments for the sub-sample of nominal yields. 

94 

## D. VAYANOS AND J.-L. VILA 

**==> picture [400 x 482] intentionally omitted <==**

**----- Start of picture text -----**<br>
3 1.5<br>2.5<br>2 1<br>1.5<br>1 0.5<br>0.5<br>0 0<br>0 5 10 15 20 0 5 10 15 20<br>Maturity (years) Maturity (years)<br>1 1.5<br>0.8<br>1<br>0.6<br>0.4<br>0.5<br>0.2<br>0 0<br>0 5 10 15 20 0 5 10 15 20<br>Maturity (years) Maturity (years)<br>3.5 1<br>3 0.5<br>2.5 0<br>2 -0.5<br>1.5 -1<br>1 -1.5<br>0.5 -2<br>0 -2.5<br>0 5 10 15 20 0 5 10 15 20<br>Maturity (years) Maturity (years)<br>Volatility of yield -- Levels<br>Volatility of yield -- Annual changes<br>Correlation with two-year yield -- Annual changes First principal component -- Annual yield changes<br>Fama-Bliss regression coefficient<br>Campbell-Shiller regression coefficient<br>**----- End of picture text -----**<br>


Figure C.2.— Model-generated and empirical moments for the sample of real yields. 

95 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

and proceeding as in Sections 3 and 4, we find that ~~_A_~~ _r_ ~~[(]~~ _[τ]_[)][solves][the][ODE] 

**==> picture [385 x 20] intentionally omitted <==**

Proceeding as in the proofs of Lemma 3 and Proposition 7, we find that the solution to the ODE is 

**==> picture [239 x 20] intentionally omitted <==**

where 

**==> picture [245 x 51] intentionally omitted <==**

and 

**==> picture [236 x 111] intentionally omitted <==**

When _a_ = 0, ( _χr, χβ , Ar_ ( _τ_ ) _, Aβ_ ( _τ_ )) = ( _κr,_ 0 _,_[1] _[−][e] κ[−] r[κrτ] ,_ 0) and 

**==> picture [146 x 20] intentionally omitted <==**

Figures C.3 and C.4 show the effects of a forward-guidance announcement about the path of short rates, for the calibrations based on the sub-sample of nominal yields and the sample of real yields, respectively. In each panel, the red solid line represents the announcement’s effect on the term structure, and the red dashed line represents the same effect when arbitrageurs are risk-neutral and the EH holds. The change ∆ _r_ in the long-run mean _r_ of the short rate _rt_ is set to -4 (-400 bps). It reverts to zero at the rate _κr_[= 0] _[.]_[1][in][the][left][panel][and] _[κ] r_[= 0] _[.]_[2][in][the][right][panel.] 

Consider next an unanticipated change ∆ _θ_ 0( _τ_ ) in the intercept of preferred-habitat demand at time zero that reverts deterministically to zero at the rate _κθ_ . Writing bond prices at time _t_ as 

> _Pt_[(] _[τ]_[)] = _e[−]_[[] _[A][r]_[(] _[τ]_[)] _[r][t]_[+] _[A][β]_[(] _[τ]_[)] _[β][t]_[+] _[A][θ]_[(] _[τ]_[)∆] _[θ]_[0][(] _[τ]_[)] _[e][−][κθt]_[+] _[C]_[(] _[τ]_[)]] 

96 

D. VAYANOS AND J.-L. VILA 

**==> picture [400 x 413] intentionally omitted <==**

**----- Start of picture text -----**<br>
Forward guidance Forward guidance<br>0.5 0.5<br>Forward guidance EH Forward guidance EH<br>0 0<br>-0.5 -0.5<br>-1 -1<br>-1.5 -1.5<br>-2 -2<br>0 5 10 15 20 25 30 0 5 10 15 20 25 30<br>Maturity (years) Maturity (years)<br>.— Effect of a forward-guidance announcement about the path of short rates, for the calibration<br>the sub-sample of nominal yields.<br>0.5 0.5<br>Forward guidance Forward guidance<br>Forward guidance EH Forward guidance EH<br>0 0<br>-0.5 -0.5<br>-1 -1<br>-1.5 -1.5<br>-2 -2<br>0 5 10 15 20 25 30 0 5 10 15 20 25 30<br>Maturity (years) Maturity (years)<br>Yield change Yield change<br>Yield change Yield change<br>**----- End of picture text -----**<br>


Figure C.3.— Effect of a forward-guidance announcement about the path of short rates, for the calibration based on the sub-sample of nominal yields. 

Figure C.4.— Effect of a forward-guidance announcement about the path of short rates, for the calibration based on the sample of real yields. 

97 

A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 

and proceeding as in Sections 3 and 4, we find that _Aθ_ ( _τ_ ) solves the ODE 

**==> picture [418 x 20] intentionally omitted <==**

Proceeding as in the proofs of Lemma 3 and Proposition 7, we find that the solution to the ODE is 

where 

**==> picture [346 x 164] intentionally omitted <==**

and 

**==> picture [236 x 112] intentionally omitted <==**

When the change ∆ _θ_ 0( _τ_ ) is a Dirac function with point mass at _τ[∗]_ , 

**==> picture [113 x 19] intentionally omitted <==**

for _j_ = _r, β_ . Hence, the time-zero change in the yield for maturity _τ_ is 

**==> picture [335 x 25] intentionally omitted <==**

98 

**==> picture [119 x 6] intentionally omitted <==**

**----- Start of picture text -----**<br>
D. VAYANOS AND J.-L. VILA<br>**----- End of picture text -----**<br>


**==> picture [400 x 147] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 0<br>-0.5 -0.5<br>-1 -1<br>-1.5 -1.5<br>-2 -2<br>-2.5 -2.5<br>2-yr 2-yr<br>-3 -3<br>5-yr 5-yr<br>-3.5 10-yr -3.5 10-yr<br>20-yr 20-yr<br>-4 30-yr -4 30-yr<br>QE mix QE mix<br>-4.5 -4.5<br>0 5 10 15 20 25 30 0 5 10 15 20 25 30<br>Maturity (years) Maturity (years)<br>Yield change Yield change<br>**----- End of picture text -----**<br>


Figure C.5.— Effect of QE, for the calibration based on the sub-sample of nominal yields. 

where 

**==> picture [286 x 112] intentionally omitted <==**

Figures C.5 and C.6 show the effects of QE for the calibrations based on the sub-sample of nominal yields and the sample of real yields, respectively. In each panel, the red, green, light blue (cyan), blue and black solid lines represent the effect of QE purchases of two-, five-, ten-, twenty- and thirty-year bonds, respectively. The black dashed line represents the effect of QE purchases that conform to the maturity distribution used by the Fed during QE1, as reported in D’Amico and King (2013). In all cases, the change ∆ _θ_ 0( _τ_ ) in the intercept of preferred-habitat demand is such that �0 _∞_ ∆ _θ_ 0( _τ_ ) _dτ_ = _−_ 0 _._ 12, i.e., QE purchases are 12% of GDP. QE is unwound at the rate _κr_[=][0] _[.]_[1][in][the][left][panel][and] _[κ] r_[=][0] _[.]_[2][in][the][right][panel.][We][use][the][value][of] _[a]_ that generates the average effect across the lower and the upper bound. These bounds are _a_ = 18 _._ 8 and _a_ = 93 _._ 8, respectively, in Figure C.5, and _a_ = 10 _._ 7 and _a_ = 53 _._ 5, respectively, in Figure C.6. 

**==> picture [436 x 167] intentionally omitted <==**

**----- Start of picture text -----**<br>
A PREFERRED-HABITAT MODEL OF THE TERM STRUCTURE OF INTEREST RATES 99<br>0 0<br>-0.5 -0.5<br>-1 -1<br>-1.5 -1.5<br>2-yr 2-yr<br>5-yr 5-yr<br>-2 10-yr -2 10-yr<br>20-yr 20-yr<br>30-yr 30-yr<br>QE mix QE mix<br>-2.5 -2.5<br>0 5 10 15 20 25 30 0 5 10 15 20 25 30<br>Maturity (years) Maturity (years)<br>Yield change Yield change<br>**----- End of picture text -----**<br>


Figure C.6.— Effect of QE, for the calibration based on the sample of real yields. 

C.6. _Unconditional Moments_ 

The expected excess return of the bond with maturity _τ_ is equal to the right-hand side of (35). When there is one demand factor which is independent of the short rate, the right-hand side of (35) becomes 

**==> picture [297 x 49] intentionally omitted <==**

Taking expectations with respect to ( _rt, βt_ ), we find that the unconditional expected excess return is 

**==> picture [153 x 12] intentionally omitted <==**

where 

**==> picture [191 x 49] intentionally omitted <==**

The Sharpe ratio of the bond with maturity _τ_ is 

**==> picture [112 x 29] intentionally omitted <==**

The correlation between the return on the bond with maturity _τ_ and the stochastic discount factor is 

**==> picture [158 x 29] intentionally omitted <==**

## 100 

**==> picture [119 x 6] intentionally omitted <==**

The stochastic discount factor parameters (M _r,_ M _β_ ) depend on _C_ ( _τ_ ). When there is one demand factor which is independent of the short rate, (41) becomes 

**==> picture [323 x 20] intentionally omitted <==**

The constants ( _χr, χβ_ ) are given by (A.129) and (A.130). 


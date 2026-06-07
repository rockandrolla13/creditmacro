## **Finance and Economics Discussion Series Divisions of Research & Statistics and Monetary Affairs Federal Reserve Board, Washington, D.C.** 

# **Nowcasting GDP and Inflation:  The Real-Time Informational Content of Macroeconomic Data Releases** 

## **Domenico Giannone, Lucrezia Reichlin, and David Small** 

## **2005-42** 

NOTE:  Staff working papers in the Finance and Economics Discussion Series (FEDS) are preliminary materials circulated to stimulate discussion and critical comment.  The analysis and conclusions set forth are those of the authors and do not indicate concurrence by other members of the research staff or the Board of Governors. References in publications to the Finance and Economics Discussion Series (other than acknowledgement) should be cleared with the author(s) to protect the tentative character of these papers. 

## Nowcasting GDP and Inflation: The Real-Time Informational Content of Macroeconomic Data Releases _[∗]_ 

Domenico Giannone, ECARES and European Central Bank, Lucrezia Reichlin, European Central Bank and CEPR David Small, Board of Governors, Federal Reserve 

This version: September 2005 

## **Abstract** 

This paper formalizes the process of updating the nowcast and forecast on output and inflation as new releases of data become available. The marginal contribution of a particular release for the value of the signal and its precision is evaluated by computing “news” on the basis of an evolving conditioning information set. The marginal contribution is then split into what is due to timeliness of information and what is due to economic content. We find that the Federal Reserve Bank of Philadelphia surveys have a large marginal impact on the nowcast of both inflation variables and real variables and this effect is larger than that of the Employment Report. When we control for timeliness of the releases, the effect of hard data becomes sizeable. Prices and quantities affect the precision of the estimates of inflation while GDP is only affected by real variables and interest rates. 

## **JEL Classification** : E52, C33, C53 

**Keywords** : Forecasting, Monetary Policy, Factor Model, Real Time Data, Large Data Sets, News 

> _∗_ We would like to thank the Division of Monetary Affairs of the Board of Governors of the Federal Reserve System for encouragement to pursue this project and providing financial support to Lucrezia Reichlin. We thank our research assistants at the Fed, Ryan Michaels and Claire Hausman, and Michele Modugno at ECARES, Univeriste Libre de Bruxelles. Thanks are also due to David Wilcox and William Wascher for their comments, to seminar participants at the Fed in April 2004 and to our discussant Athanasios Orphanides at the EABCN conference in Brussels in June 2005. The opinions in this paper are those of the authors and do not necessarily reflect the views of the European Central Bank or the Federal Reserve System. Please address any comments to Domenico Giannone dgiannon@ulb.ac.be; Lucrezia Reichlin lucrezia.reichlin@ecb.int; or David Small, dsmall@frb.gov. 

## **1 Introduction** 

Monetary policy decisions in real time are based on assessments of current and future economic conditions using incomplete data. Since most data are released with a lag and are subsequently revised, the reconstruction of current-quarter GDP, inflation and other key variables is an important task for central banks and one to which they devote a considerable amount of resources. Current-quarter numbers are also important because, in the short-run, there is a greater degree of forecastability than in the long run. For example, Giannone, Reichlin, and Sala (2004) (GRS from now on) document that, in forecasting GDP beyond the first quarter, the forecasts of the Federal Reserve staff and of standard statistical models do not perform better than that of a constant growth rate. Current-quarter estimates are particularly relevant because they are inputs for model-based longer term forecasting exercises. 

Nowcasts are constructed at central banks using both simple models and qualitative judgment. Those exercises involve the analysis of a large amount of information and a judgment on the relative weight to attribute to various data series. As new information becomes available throughout the month, the nowcasts and forecasts may be adjusted in response to changes in both the values of the data series and the implicit relative weights applied to those series. Typically, central banks and markets pay particular attention to certain data releases either because they arrive earlier, and can therefore convey news on key variables such as GDP, or because they are inputs in their estimates (e.g. industrial production or the Employment Report for GDP). In principle, however, any release, no matter at what frequency, may potentially affect current-quarter estimates and their precision. From the point of view of the short-term forecaster, there is no reason to throw away any information. 

This paper provides a framework that formalizes the updating of the nowcast and forecast of output and inflation as data are released throughout the month and that can be used to evaluate the marginal impact of new data releases on the precision of the now/forecast as well as the marginal contribution of different groups of variables. In the empirics, we focus on the nowcast and we use intra-month releases of monthly time series to construct (possibly) progressively more accurate current-quarter estimates. Our approach allows us to consider a large number of monthly time series (in principle all the potentially relevant ones) within the same forecasting model. Moreover, the model takes into account the non-synchronicity of the releases by exploiting vintages of panel data which are unbalanced at the end of the sample. 

The framework we propose is adapted from the parametric dynamic factor model proposed by Doz, Giannone, and Reichlin (2005) and applied by GRS to the same variables we are using here. It is similar in spirit to Evans (2005), but our focus is different since we exploit a large number of data series rather than just financial variables and we don’t consider information at frequencies lower than the month. 

Using this framework, we ask three specific empirical questions. The first is whether a large information set really helps to obtain an early and accurate estimate of current inflation and output. Several papers have made the point that a large information set helps in forecasting (cfr. Boivin and Ng (2005), Forni, Hallin, Lippi, and Reichlin (2003), Giannone, Reichlin, and Sala (2004), Marcellino, Stock, and Watson (2003), 

1 

Stock and Watson (2002)). This literature proposes and applies factor models adapted to handle large panels of time series. On the basis of such models, Bernanke and Boivin (2003) and GRS formalize the real-time application of large datasets to nowcasting and forecasting inflation and output in the United States. GRS in particular show that a specification of the model with two dynamic factors has a forecasting performance comparable to that of the Federal Reserve’s Greenbook. 

This paper builds on this literature, but instead of performing an out-of sample forecasting exercise, we compute measures of news and uncertainty and study their evolution as new information becomes available within the month. This is achieved by deriving explicitly the standard error of the nowcast or forecast as a function of the size of the information set. Changes in this standard error allow us to track the evolution of the uncertainty of the forecast and nowcast as the flow of information evolves within a month. 

The second question is the assessment of the marginal contribution of particular sets of variables in constructing the nowcasts. What kind of information really matters? To provide an answer, we update our nowcasts and forecasts following each data release within the month and construct empirical measures of the “news” in each data block by conditioning on the data that was available in real time when the data was released and that is evolving within the month. Because the data are released in blocks and the releases follow a relatively stable calendar, each month the updates and news for each type of data release are conditional on the same (updated) set of data releases. Since blocks of releases typically correspond to an economic classification: money indicators, prices, industrial production series, labor market variables etc., our measure of news refers to aggregates of variables in a certain category rather than to a single indicator. The third question is whether the marginal contribution of a block of releases is due to its “timeliness” or to its “quality.” The distinction between timeliness and quality arises because the marginal value of a data release depends on the new information in the release; i.e. it depends on the difference between the data that are released and the values that were predicted by the model just before the release. The earlier a given series is released (timeliness), the smaller the information set for its predicted value and the greater, ceteris paribus, is the news in the release. Its “quality” depends on the predictive power of an information block given the same conditioning information set as for other information blocks. Since data are very collinear, the order of the release matters and we may have a situation where high quality data such as GDP, have no marginal impact on GDP itself since they are released with a long lag. 

The paper is organized as follows. In Section 2, we describe the problem and the structure of the staggered releases in the United States. In Section 3 we introduce the model, our estimation technique, the computation of the standard errors, and the method for examining the “timeliness” of data. Section 4 describes the empirical analysis and comments on the results. Section 5 concludes. 

2 

## **2 The Problem and the Structure of the Data Sets** 

## **2.1 The Problem** 

We will first describe the problem we are analyzing in a very stylized way. Our aim is to evaluate the current quarter nowcast of key indicators of real economic activity and price dynamics on the basis of the flow of information that becomes available during the quarter. 

Within each quarter, contemporaneous values of key macroeconomic variables like GDP are not available, but they can be estimated using higher frequencies variables which are recorded and published more timely. At month _v_ we can define the relevant information set Ω _[n] v_[which][includes][the][relevant] _[n]_[monthly][time][series][and][the][relevant] sample up to month _v_ and compute the following projection: 

**==> picture [82 x 12] intentionally omitted <==**

Let us assume that Ω _[n] v_[is][composed][of][two][blocks][[Ω] _[n] v_[1] Ω _[n] v_[2][]][and][that][the][variables] in Ω _[n] v_[2][,][say][production,][are][released][a][month][later][than][those][in][Ω] _[n] v_[1][,][say][surveys.] This implies that, in month _v_ , variables in Ω _[n] v_[1] are available up to month _v_ , while variables in Ω _[n] v_[2] are available up to month _v −_ 1. In order not to lose the information in Ω _[n] v_[2] available up to the previous month, we will have to project on the basis of a dataset which is unbalanced at the end of the month. Our forecasting problem is the generalization of this simple case. 

The conditioning set in the projection is a large panel of monthly time series, consisting of about 200 series for the US economy, broadly those examined closely by the staff of the Federal Reserve when making the forecasts. 

The data considered are published in thirty six releases per month. The blocks contain direct measures both of real economic activity and prices, and of aggregate and sectoral variables. Moreover, they include indirect measures of economic developments, such as surveys, financial prices that may reflect current and expected future economic developments and measures of money and credit. 

To set the notation, we will denote the information set by: 

**==> picture [200 x 19] intentionally omitted <==**

where _v_ denotes the month of the release, and _vj_ the date of the _j_ th data release within the month. At each point in time _vj_ , we will refer to the information set as vintage. The latter is composed _n_ variables, _Yit|vj_ , where _i_ = 1 _, ..., n_ identifies the individual time series and _t_ = 1 _, ..., Tivj_ denotes time in months. Here, _Tivj_ indicates the last period for which series _i_ in vintage _vj_ has an observed value. For example, when industrial production is released in month _v_ , the last available observation refers to the previous month _Tivj_ = _v −_ 1, while when surveys are released, the last values refer to the month of the releases _Tivj_ = _v_ . 

Let us now track the flow of information within the quarter of interest. We will follow the convention that a quarter _k_ is dated by its last month (for example, the first quarter of 2005, is dated by _k_ =March05). Release _j_ within each quarter _k_ is given 

3 

by Ω _vj_ where _v_ = _k −_ 2 _, k −_ 1 _, k,_ are, respectively, the first, the second and the third month of quarter _k_ . 

At _vj_ , a set of variables _Yi,t, i ∈ Ivj_ is released and the information set expands from Ω _vj−_ 1 to Ω _vj_ . The new information set differs from the preceding one for two reasons. First, there are new, more recent, observations: _Tivj ≥ Tivj−_ 1 _, i ∈ Ivj_ , while _Tivj_ = _Tivj−_ 1 _, i ∈/ Ivj_ . Second, old data are revised, and data revisions are given by _Yit|vj − Yit|vj−_ 1 _, i ∈ Ivj_ . Notice that in absence of data revisions Ω _vj−_ 1 _⊆_ Ω _vj_ , i.e. the information set is expanding as time passes by. 

The timing and the order of data releases can vary from month to month, i.e. _Ivj_ can ˜ be different from _Iv_ ˜ _j_ , for _v_ = _v_ . However, releases typically correspond to an economic classification: money indicators, prices, industrial productions, labor market variables etc. and with few exceptions, the differences in the chronological order of the releases are limited. This allows us to construct a stylized calendar in which we combine the series into fifteen data blocks so that, in most cases, they consist of roughly homogeneous variables, containing data released at roughly the same time in the month, roughly preserving the chronological order in which the data are released. We call pseudo vintages the releases which refer to our stylized calendar. We have: _Ivj_ = _Ij, j_ = 0 _,_ 1 _, · · · , J_ . 

We want to stress here that, abstracting from data revisions, due to the non synchronicity of data releases, the intra month flow of data is mainly reflected in the increase of cross-sectional information. In particular, at each release date _vj_ the information set expands because of the inclusion of new information about a group of variables that corresponds to a particular economic classification. 

For each information set within the quarter of interest, we compute the nowcast for the variables of interest by simple projection. For a generic variable _zk[q]_[,][e.g.][GDP] growth rate, where the superscript _q_ indicates that the variables is measured at quarterly frequency, we have: 

**==> picture [260 x 19] intentionally omitted <==**

Once we have obtained the projections, we can compute the news in block _j_ as the change that the release of block _j_ induces in the current estimates of the variable of interest: 

**==> picture [282 x 16] intentionally omitted <==**

Notice that NEWS is not a standard Wold forecast error. First of all, the structure of the unbalancedeness changes with time so that the number of variables within the month is different from month to month. Second, it is affected by the order in which data arrive. 

The uncertainty associated with this projection, is estimated by 

**==> picture [215 x 17] intentionally omitted <==**

Since the dataset is expanding, _V zk[q] |vj[≤][V z] k[q] |vj−_ 1[and][the][uncertainty][is][expected] to decrease as time passes by. The evolution of this quantity across data releases 

4 

measures the extent to which each block of releases helps reduce uncertainty of the nowcast of the variables of interest: more informative releases are expected to produce larger reductions in uncertainty. The reduction of uncertainty provides a measure of the marginal information content of the _j_ th data release and, in general, of the value of an increasingly larger information set. 

From the practical point of view, the computation of this projection is not simple. Due to the large number of data we are considering, Ω _vj_ is very large. The basic idea of this paper is to exploit the collinearity of the series in our panel to summarize the information in Ωin a smaller space generated by the span of few common factors _Ft_ . A projection on the space of the common factors _Ft_ is able to capture the bulk of the covariance of the data and provides a parsimonious well performing forecast. Our problem is split in two steps. First, estimate the factors from the panel, _F_[ˆ] _t|vj_ = Proj � _Ft|_ Ω _vj_ �. Second, project on the span of the estimated factors. Uncertainty of the nowcast can hence be attributed to two components 

**==> picture [134 x 16] intentionally omitted <==**

The first component reflects uncertainty on the common component, i.e. the uncertainty arising from the estimation of the common factors; the second component reflects uncertainty on the idiosyncratic, i.e. the variance of that part of the variable not explained by the common factors. 

On the basis of the framework outlined here we will also study whether the impact of a release depends on the fact that it is published early (timeliness) or by its economic content (quality). Quality of a block of release is defined as its marginal impact, controlling for the date of the release. 

To summarize, our objectives are: 

1. Update the current quarter estimate and the forecast of the variables of interest, conditioning on a large set of information. 

2. Update on the basis of a panel which at the end of the month is unbalanced. 

3. Evaluate “news” in relation to the publication of data releases. 

4. Evaluate uncertainty in relation to the flow of information. 

5. Evaluate the impact of a release by distinguishing the effect due to timing and that due to quality. 

On the basis of this information, we want to evaluate the marginal contribution of different blocks of variables to the forecast and assess whether the latter is due of to the timeliness of the release or to its intrinsic quality. 

A model that is suitable to our objectives is defined in the next Section. 

5 

## **3 The Econometric Methodology** 

The methodology we will propose here is the parametric dynamic factor model proposed by Doz, Giannone, and Reichlin (2005) and applied by GRS to the same variables we are using here. In this framework, once the parameters of the model are estimated consistently through principal components, the Kalman filter is used to update the estimates of the signal and the forecast on the basis of the unbalanced panels. 

This parametric version of the factor model can also be used to derive explicit measures of data uncertainty across the vintages. 

The Kalman filter allows us to extract the innovation content of each data release (composed of several individual data series) and to identify the news – splitting it from the noise. The underlying signal is computed by the Kalman filter by weighting the innovation content of each variable according to its news to noise ratio. 

## **3.1 The Model** 

While in Section 2 we defined the problem for a generic quarterly variable _zk[q] |vj_[,][in] describing the model, for simplicity, we will refer to monthly stationary variables. The appendix describes data transformation and the relation between quarterly and monthly quantities in detail. Here let us just say that the variable of interest, _yit|vj_ is the corresponding monthly series to _zk[q] |vj_[,][transformed][so][as][to][induce][stationarity.][Obviously] different transformations will be required depending on the nature of the variable in question. 

We have: 

**==> picture [115 x 13] intentionally omitted <==**

where _µi_ is a constant and _χit ≡ λiFt_ and _ξit|vj_ are two orthogonal unobserved stochastic processes.[1] In matrix notation we can write: 

**==> picture [180 x 13] intentionally omitted <==**

where _yt|vj_ = ( _y_ 1 _t|vj , ..., ynt|vj_ ) _[′]_ , _ξt|vj_ = ( _ξ_ 1 _t|vj , ..., ξnt|vj_ ) _[′]_ , Λ = ( _λ[′]_ 1 _[, ..., λ] n[′]_[)] _[′]_[.][We][assume] that the _n ×_ 1 process _χt_ (the common component) is a linear function of a few unobserved common factors _Ft_ that capture “almost all” comovements in the economy, while the _n ×_ 1 stationary linear process _ξt|vj_ (the idiosyncratic component) is driven by _n_ variable-specific shocks. Since data revision errors are typically series specific, we incorporate them in the idiosyncratic component. Additionally, the common factors are supposed to be the same across releases because they summarize the fundamental state of the economy underlying all data releases. 

The common and idiosyncratic components are identified under the methodology and assumptions used in estimating the model, as described in section A.3 of the Appendix. The common factors can be consistently estimated by principal components (See Forni, Hallin, Lippi, and Reichlin (2000) and Stock and Watson (2002)) provided that the idiosyncratic shocks exhibit, at most, “weak” cross-correlations. 

> 1The particular transformations that we use are discussed in Section C of the Appendix. 

6 

Our approach is to specify the the dynamics of the common factors as follows:[2] 

**==> picture [250 x 33] intentionally omitted <==**

where _B_ is a _r×q_ matrix of full rank _q_ , _A_ is a _r×r_ matrix and all roots of det(Ir _−_ Az) lie outside the unit circle, and _ut_ is the shock to the common factor and is a white-noise process. In such a model, a number of common factors ( _r_ ) that is large relative to the number of common shocks ( _q_ ) aims at capturing the lead and lag relations among variables along the business cycle (cfr. Forni, Giannone, Lippi, and Reichlin (2005) for details). 

In the empirical estimates, _r_ and _q_ will be set equal to ten and two, respectively. These choices are based on findings in GRS and correspond to the idea that the economy can be described as being driven by _q_ = 2 large pervasive shocks with heterogeneous dynamics captured by the parameter _r_ . 

To estimate the factors on the basis of an unbalanced data set, for the idiosyncratic shock we assume: 

**==> picture [327 x 31] intentionally omitted <==**

The data generating process of the idiosyncratic components is parameterized by specifying, for available vintages, the following conditions: 

**==> picture [277 x 17] intentionally omitted <==**

**==> picture [265 x 16] intentionally omitted <==**

We also assume that _ξit|vj_ is orthogonal to the common shocks _ut_ : 

**==> picture [272 x 16] intentionally omitted <==**

Our model consists of equations 3.2 through 3.7, and we can use the Kalman filter to estimate the common factors _Ft_ by assuming that errors are Gaussian. If we replace the parameters of the model above by their consistent estimates (see section A.3 of the Appendix for details), we can estimate the common factors as: 

**==> picture [284 x 16] intentionally omitted <==**

In particular, imposing _ψ_[˜] _it|vj_ = _∞_ when _yit|vj_ is missing (see equation 3.4) implies that the filter, through its implicit signal extraction process, will put no weight on the missing variable in the computation of the factors at time _t_ . 

> 2The relation of our model to that used in estimating principal components is discussed in Section A.4 of the Appendix. 

7 

The Kalman filter is also used to evaluate the degree of precision of the factor estimates given the consistent parameter estimates, with the degree of precision reflecting that of the signal extraction process for estimating the factor: 

**==> picture [216 x 16] intentionally omitted <==**

Our estimates of the signal and their degree of precision are given by: 

**==> picture [203 x 16] intentionally omitted <==**

**==> picture [129 x 16] intentionally omitted <==**

A discussion of the assumptions is in the appendix. 

## **3.2 Forecasts and Uncertainty** 

Turning to the nowcast, notice that in the state space representation we assume that only the common component of each series is forecastable. Empirically, this restriction does not create any relevant loss of information because the common factors are able to capture not only most of the cross-sectional correlation, but also the bulk of the dynamics of the key aggregates (for evidence on this point, see GRS). 

Hence, if _yit|vj_ is not available, because _yit_ has not been releasedˆ yet at ˆvintageˆ _v_ , (this is always the case if _t > v_ ), then our estimates are given by _yit|vj_ = _µi_ + _χit|vj_ . On the other hand we assume that if an ˆofficial estimate for _yit|vj_ is available, so that _yit_ has been released at vintage _vj_ , then _yit|vj_ = _yit|vj_ . More precisely: 

**==> picture [289 x 16] intentionally omitted <==**

**==> picture [184 x 14] intentionally omitted <==**

where: 

**==> picture [186 x 31] intentionally omitted <==**

From these equations, as indicated in Section 1, we can compute the news induced by the release of block _j_ to the nowcast of _yit_ : 

**==> picture [279 x 14] intentionally omitted <==**

Because the projections by which these forecasts are calculated assume that the parameters are given, and thus the relative weights in the signal extraction process are unchanged, this measure of news reflects the updating of the factors due only to the new information in vintage _vj_ , conditional on the information in vintage _vj−_ 1. This measure of the news allows us to determine whether particular releases contain relevant 

8 

information in a real-time setting and thus whether it is worthwhile to estimate the signal at each intra-month data release. 

Also, for each vintage, the confidence bands for the forecast can be easily computed from the state space representation. Let us consider the difference between the expected value computed at vintage _w_ and the official realized released in the future at date _w_ ˜ ( ˜ _w > w_ ). Our measure of uncertainty about this realized value is defined as: 

**==> picture [297 x 17] intentionally omitted <==**

Alternatively, if _yit_ has not been released yet at vintage _w_ , we have: 

**==> picture [236 x 32] intentionally omitted <==**

whereindependentV[ˆ] _χjt|w_ of= _w_ ˜Λ[ˆ] _[′] i_ by _[V]_[ˆ] 0 _|_ assumption _w_[ˆΛ] _[i]_[and] V[�] _ξ_ (cfr. _jt|w_ =section _ψ_[ˆ] _j_ . Notice3). that this measure of uncertainty is 

On the other hand, if there is an official release of _yit_ at vintage _w_ , we have 

**==> picture [337 x 16] intentionally omitted <==**

where there is no covariance term due to the orthogonality of the factor and the idiosyncratic term. 

This quantity measures the size of the revision error between vintage _w_ and vin˜ tage _w_ . To estimate it, it is necessary to have an assessment on the evolution of the idiosyncratic component at each release E( _ξ_[ˆ] _it|w − ξit|w_ ˜)[2] . In addition, notice that E(ˆ _χit|w − χit_ )[2] will provide a lower bound for the variance of the revisions. For simplicity, we will not measure uncertainty due to revision errors, hence we will assume that E[ˆ _yit|w − yit|w_ ˜][2] = 0 if there is an official release of _yit_ at vintage _w_ .[3] In summary, we have: 

**==> picture [285 x 19] intentionally omitted <==**

Notice that there are two sources of uncertainty, one associated with the signal extraction problem (extraction of _χt_ ), the other due to the presence of idiosyncratic components ( _ξt_ ). 

The appendix detail how to adapt these measures of news and uncertainty to obtain the statistics described in Section 2.1 for the data of interest transformed in quarterly rates. 

> 3An analysis of the data revision process will require a separate discussion, and is beyond the scope of the paper. 

9 

## **4 Empirics** 

The measures of news and uncertainty introduced in Section 2 will now be applied to the real-time vintages of data sets from June 2003 through March 2004 and to the pseudo real-time vintages we have constructed for each of those months, capturing the actual chronological order of the data releases (see again Section 2). We also present these measures in a way that controls for the timeliness of the data releases. 

## **4.1 Data** 

The dataset is described in Table 1. As anticipated in Section 2.1, it consists of about 200 macroeconomic indicators and the sample, in each vintage, starts in 1982. 

All variables are monthly, except for GDP and GDP deflator for which monthly measures are derived from linear interpolation.[4] Details on data transformation are reported in Appendix C. Let us here stress that price variables are treated as _I_ (2) in estimation, but results will be reported for the level of inflation. 

Table 1 describes the structure of the information within the quarter. Variables (releases) are indicated in Column 2 while Column 1 indicates the associated block. As described in Section 2, we have 15 blocks of releases.[5] Different blocks of releases are published at different dates throughout a month (column 3) and may refer to different dates (column 4). Typically, surveys have very short publishing lags and often are forecasts for future months or quarters, while GDP, for example, is released with a relatively long delay.[6] Industrial production, price variables and others are intermediate cases. 

In column 3, we start our “data month” with the Consumer Credit release on the 5th business day of the month and end it with the Employment Situation release on the first Friday of the following month. With this convention, the data set that we label as June, for example, only includes values for June and earlier, although the data in the latest Labor and Wages block contained in that data set were released in the first week of July. After the release of the Labor and Wages block, we track the flow of information within each month by exploiting the fact that our information blocks preserve the chronological ordering of the releases. 

As indicated in the third column of Table 1 and anticipated in the discussion of Section 2, the timing of releases varies somewhat from month to month. To overcome this problem, we construct pseudo intra-month vintages according to a stylized data release calendar, by assigning to the vintages the most common timing pattern and keeping that timing fixed across our 21 monthly data sets. The construction of the 

> 4Although very simple, this transformation works because it is applied to only a small number of series and the distortion is expected to go into the idiosyncratic factor (See Altissimo, Bassanetti, Cristadoro, Forni, Hallin, and Lippi (2001)). In fact, the results in GRS show that the model performs quite well even with such a simple transformation. The procedure might be improved using more sophisticated types of interpolation, that is beyond the scope of the paper. 

> 5Appendix C reports the source of each data release. The individual series in each release (and block) are reported in Appendix B. 

> 6The releases of the GDP and Income block for the first, second and third months of the quarter contain the GDP and Income data from the “advance”, “preliminary” and “final” releases, respectively. 

10 

|Frequency<br>of data (5)|Monthly<br>Monthly<br>Monthly<br>Monthly<br>Monthly<br>Monthly<br>Monthly<br>Monthly<br>Monthly<br>Monthly<br>Quarterly<br>Monthly<br>Monthly<br>Monthly<br>Monthly<br>Monthly<br>Monthly<br>Weekly<br>Weekly<br>Daily<br>Daily<br>Daily<br>Daily<br>Daily<br>Daily<br>Monthly<br>Monthly<br>Monthly<br>Monthly<br>Monthly<br>Monthly<br>Monthly<br>Monthly<br>Monthly<br>Monthly|
|---|---|
|Publishing<br>Lag (4)|two months<br>one month<br>one month<br>two months<br>one month<br>one month<br>current month<br>one month<br>one month<br>two months<br>one quarter<br>one month<br>one month<br>one month<br>one month<br>current month<br>current month<br>current month<br>current month<br>current month<br>current month<br>current month<br>current month<br>current month<br>current month<br>current month<br>current month<br>one month<br>one month<br>one month<br>two quarters<br>current month<br>one month<br>one month<br>current month|
|Timing<br>(approx.) (3)|5th business day of month<br>11-15th of month<br>Middle of month<br>2nd full week of month<br>15th to 17th of month<br>16th to the 20th of month<br>3rd Thursday of month<br>Middle of month<br>Middle of month<br>Day after GDP - release<br>Last week of month<br>Day after GDP - release<br>3rd to last bus. day of month<br>Last week of month<br>Last week of month<br>Last Tues. of month<br>Last Fri. of the month<br>Last Thurs. of month: Monthly ave.<br>Last Wed. of month: Monthly ave.<br>Last day of month: Monthly ave.<br>Last day of month: Monthly ave.<br>Last day of month: Monthly ave.<br>Last day of month: Monthly ave.<br>Last day of month: Monthly ave.<br>Last day of month: Monthly ave.<br>1st business day of month<br>1st bus. day of month<br>1st bus. day of month<br>23rd - 29th / 30th - 6th<br>5 days after Advance Durables<br>Quarterly (series is monthly)<br>1st Thurs. of month<br>2nd Thurs. of month<br>1st Fri. of month<br>1st Fri. of month|
|Release (2)|G.19 Consumer Credit<br>Advance Monthly Sales For Retail and Food Services<br>Monthly Treasury Statement of Receipts and Outlays of the U.S. Government<br>FT900 U.S. International Trade in Goods and Services: Exhibit 5<br>G.17 Industrial Production and Capacity Utilization<br>New Residential Construction<br>Federal Reserve Bank of Philadelphia Business Outlook Survey<br>Producer Prices<br>Consumer Prices<br>GDP - detail: inventories and sales<br>GDP - release: GDP and GDP defator<br>Personal Income and Outlays<br>Manufactured Homes Survey<br>New Residential Sales<br>Chicago Fed MMI Survey<br>Consumer Confdence Index<br>Michigan Survey of Consumers<br>Claims, Unemployment Insurance Weekly Claims Report<br>Freddie Mac Primary Mortgage Survey<br>H.15 Selected Interest Rates<br>H.10 Foreign Exchange Rates<br>Price of gold<br>NYSE<br>S&P (wkly)<br>Wilshire<br>PMGR-Manufacturing<br>Commercial Paper<br>Construction Put in Place<br>M3: Advance Report on Durable Goods Manufacturers Shipments, Inventories and Orders<br>M3: Full Report on Durable Goods Manufacturers Shipments, Inventories and Orders<br>Consumer Delinq. Bulletin<br>H.3 Aggregate Reserves of Depository Institutions and the Monetary Base<br>H.6 Money Stock Measures<br>H.8 Assets and Liabilities of Commercial Banks in the United States<br>Employment Situation|
|Block Name (1)|Mixed 1<br>Mixed 1<br>Mixed 1<br>Mixed 1<br>IP<br>Mixed 2<br>Mixed 2<br>PPI<br>CPI<br>GDP & Income<br>GDP & Income<br>GDP & Income<br>Housing<br>Housing<br>Surveys 1<br>Surveys 1<br>Surveys 1<br>Initial Claims<br>Interest Rates<br>Interest Rates<br>Financial<br>Financial<br>Financial<br>Financial<br>Financial<br>Surveys 2<br>Mixed 3<br>Mixed 3<br>Mixed 3<br>Mixed 3<br>Money & Credit<br>Money & Credit<br>Money & Credit<br>Money & Credit<br>Labor & Wages|



11 

vintages is discussed in more detail in Section A.1 of the Appendix. 

Following the notation introduced in Section 2, _v_ 0 indexes the vintage just before the release of the first block (Mixed 1), while _v_ 1 indexes the vintage after the release of Mixed 1 and before the release of the second block (IP). Just after the Labor and Wages release, we have the last vintage of the month, indexed by _v_ 15. 

With this convention, the starting vintage in each month is equal to the last vintage of the subsequent month: so the vintages indexed by _v_ 15 and ( _v_ + 1)0 are the same. Because the data blocks defining the vintages are in the same order each month, we use _vj_ to index both the vintages and the time at which they are released. So, we will say variables in the first block (Mixed 1) are updated in vintage _v_ 1 and are released at time _v_ 1. 

The way we treat financial variables deserves a comment. Financial variables and interest rates are the most timely since they are available on a daily basis. In principle daily information could be used to update the estimates of GDP and inflation as, for example, in Evans (2005). Our approach is different. Since the bulk of our data is monthly, we disregard information from financial variables at frequencies lower than the month and let them enter the model as monthly averages. We make the arbitrary assumption that they become available only at the end of the month which implies that their effect is underestimated. 

## **4.2 News and Uncertainty in Real-Time** 

In this section we report summary statistics evaluated using real time vintages from July 2003 to March 2005. These measures are derived using the “real-time” and “pseudo realtime” vintages in their natural chronological order and thus correspond to the exercise in which the forecaster updates her nowcasts after the release of each information block. 

We report statistics on uncertainty around the current quarter nowcast of key variables and on the size of the news derived using real time vintages. For real variables, measures of news and uncertainty are constructed for quarterly quantities derived from monthly data. For inflation variables they are reported for annual inflation. The statistics used are based on formulas (3.10) and (3.12), modified so as to track the quarterly aggregates of interest. 

The measure of uncertainty in formula (3.12) depends on the estimated parameters, which change over time because they are recomputed after each vintage of data. Below we report averages of the uncertainty measures across all the quarters considered in the real time exercise. We will refer to this measure as average uncertainty. Similarly, we measure the size of the news as the absolute value of the news measure (3.10) averaged across all the quarters considered in the real time exercise. 

Because the impact of the release of block _j_ may differ according to whether the release is in the first, second or third month of the quarter, the average for both uncertainty and news is taken over the seven vintages in our sample and correspond to either to the first, second, or third months of the quarter. 

Chart 1, 2 and 3 focus on two key variables: quarterly growth of GDP (Charts 1a, 2a and 3a) and annual growth of GDP deflator (Charts 1b, 2b and 3b) while Charts 

12 

4a and 4b consider, respectively, additional real and nominal indicators.[7] 

Measures of news for real growth and inflation are shown in Charts 1a and 1b, respectively. Charts 2a-2b, 3a-3b and 4a-4b report the evolution of the uncertainty on the signal (common) and the uncertainty on the variable itself (total). These charts complement the information in Chart 1a-1b by providing a systematic measure of how the accuracy of the nowcast evolves. Chart 2a-2b shows the evolution of the standard errors over the quarter: by understanding whether the marginal impact of a given release has a different effect in the first month than in later months, we can assess the importance of timing in explaining the impact of a particular release. Chart 3a-3b, on the other hand, overlays the three months of the quarter to allow for an easier comparison of the effects of a given block across the three months. Chart 4a-4b reports the same information as Chart 2a-2b, but for additional real and nominal series. These series are: employment on nonfarm payroll (NFP), unemployment rate (UR), personal consumption expenditure price index excluding food and energy (PCEX). 

Let us first concentrate on GDP growth. From Charts 1a, 2a and 3a we have three results: 

1. Intra-month information matters. Data releases throughout the quarter convey news as can be seen by the fact that the estimates are generally updated as new releases are published (Chart 1a). Moreover, uncertainty decreases uniformly through the quarter (Chart 2a). 

2. The release that has the largest impact on the nowcast and its precision in the first month is the “Mixed 2” block. Mixed 2 is composed of two series from the New Residential Construction Release and nine series from the Philadelphia Business Outlook Survey. By way of the Philadelphia survey, Mixed 2 is the most timely release since it is the first block to contain data or forecasts on the current quarter. The two preceding releases in the month (Mixed 1 and Industrial Production) convey information about earlier months only and have almost no impact since they are published relatively late. 

3. Other important news for the nowcast of real GDP growth is contained in the blocks of Labor and Wages (which includes the release of the Employment Report) and interest rates (the components of the block compose the yield curve). This emerges from both Chart 1a and 2a. 

In general, the striking result is that the surveys (Mixed 2) have a larger impact than the Employment Report (Labor and Wages) which is the news to which financial markets react more strongly. The reason is that, by the time the labor block is released, the information conveyed by the surveys has already been taken into account. This highlights the importance of timing. 

Noticeable is also the large effect of the interest rate block on both the nowcast and its uncertainty. The Interest Rate block is the end-of-month average of the weekly 30-year mortgage rate from Freddie Mac and of daily observations of nine interest rates 

> 7All statistics are presented numerically in Section D of the Appendix. 

13 

from the Federal Reserve’s H.15 Release. The later include short and longer-term U.S. Treasury rates and AAA and BAA corporate bond yields. Likewise, the Financial block is composed of end-of-month averages of daily observations on foreign exchange rates, the price of gold, and U.S. stock prices. 

**Chart 1a** _Average Size of News: Nowcasts of Real Growth_ 

**==> picture [335 x 465] intentionally omitted <==**

**----- Start of picture text -----**<br>
 first month (m=1)   second month (m=2)  third month (m=3)<br>0.2<br>0.18<br>0.16<br>0.14<br>0.12<br>0.1<br>0.08<br>0.06<br>0.04<br>0.02<br>0<br>Chart 2a Average Uncertainty: Nowcast of Real Growth<br> total   common<br>1.4<br>First Month Second Month Third Month<br>1.2<br>1<br>0.8<br>0.6<br>0.4<br>0.2<br>0<br>Mixed 1  Ind. Production Mixed 2  PPI CPI GDP & Income  Housing Surveys 1  Initial Claims  Interest Rates  Financial Surveys 2  Mixed 3  Money & Credit Labor & Wages<br>Labor and Wages Mixed 1  Ind. Production Mixed 2  PPI CPI GDP & Income Housing Surveys 1  Initial Claims  Interest Rates  Financial Surveys 2  Mixed 3  Money & Credit Labor & Wages Labor and Wages Mixed 1  Ind. Production Mixed 2  PPI CPI GDP & Income Housing Surveys 1  Initial Claims  Interest Rates  Financial Surveys 2  Mixed 3  Money & Credit Labor & Wages Labor and Wages Mixed 1  Ind. Production Mixed 2  PPI CPI GDP & Income Housing Surveys 1  Initial Claims  Interest Rates  Financial Surveys 2  Mixed 3  Money & Credit Labor & Wages<br>**----- End of picture text -----**<br>


14 

**Chart 3a** _Average Uncertainty: Nowcast of Real Growth (Common Component)_ 

**==> picture [335 x 185] intentionally omitted <==**

**----- Start of picture text -----**<br>
 first month (m=1)   second month (m=2)  third month (m=3)<br>1.2<br>1.0<br>0.8<br>0.6<br>0.4<br>0.2<br>0.0<br>PPI  CPI<br>Labor and Wages Mixed 1  Ind. Production Mixed 2  GDP & Income Housing Surveys 1  Initial Claims  Interest Rates  Financial Surveys 2  Mixed 3  Money & Credit Labor & Wages<br>**----- End of picture text -----**<br>


**Chart 4a** _Average Uncertainty: Nowcast of Alternative Real Variables (Common Component)_ 

**==> picture [334 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
GDP NFP UR<br>1<br>First Month Second Month Third Month<br>0.9<br>0.8<br>0.7<br>0.6<br>0.5<br>0.4<br>0.3<br>0.2<br>0.1<br>0<br>Mixed 1  Ind. Production Mixed 2  PPI  CPI  GDP & Income Housing  Surveys 1  Initial Claims  Interest Rates  Financial  Surveys 2  Mixed 3  Money & Credit Labor & Wages Mixed 1  Ind. Production Mixed 2  PPI  CPI  GDP & Income Housing  Surveys 1  Initial Claims  Interest Rates  Financial  Surveys 2  Mixed 3  Money & Credit Labor & Wages Mixed 1  Ind. Production Mixed 2  PPI  CPI  GDP & Income Housing  Surveys 1  Initial Claims  Interest Rates  Financial  Surveys 2  Mixed 3  Money & Credit Labor & Wages<br>**----- End of picture text -----**<br>


15 

We now turn to inflation. Let us first remark that, as mentioned, we focus on quarterly growth rate for GDP and on annual rate for what concerns price inflation. The latter is therefore smoother and less sensitive to the news by construction. This feature is evident from Chart 1b. From Chart 2b and 3b we can see that, as in the case of GDP, uncertainty decreases monotonically within the quarter as new information arrives. As for the importance of different blocks, two features are noticeable. First, looking at the evolution of the updates of the estimates (Chart 2a), we can see that a big jump occurs with the release of the GDP and Income block in the first month of the quarter. This release (the “advance” release) contains the first observation for the GDP deflator (and GDP) for the previous quarter and, thus, reveals information about the value of the idiosyncratic shock to the deflator in the previous quarter. This effect, however, is much less pronounced on the common component (the signal) and mainly affects the idiosyncratic component of inflation. This is explained by the fact that, since we have modelled inflation in first differences, the idiosyncratic component has a unit root (empirically it turns out to be well captured by a random walk) so that the nowcast reacts strongly to the information revealed about the idiosyncratic shock in the previous quarter. 

More interestingly, an important impact on the precision of the estimates (Chart 2b) is due to the financial block release, containing data on exchange rates and the nominal prices of gold and equities, whereas, unlike in the case of GDP the interest rate block, has no effect. The Financial block, as we have seen, contributes to a noticeable decline in the uncertainty associated to GDP inflation but not for that associated to real GDP. Conversely, the Interest Rate block has an effect that is much more pronounced for real GDP than for inflation. Notice that the role of financial variables and interest rates is likely to be underevaluated since they are available from the markets on a daily basis but we assume that they become available only at the end of the month. 

To check for the robustness of these results for the Interest Rate and Financial blocks, we perform the same analysis as in Chart 3 but invert the order of these two blocks. This exercise is motivated by the fact that the order of these two blocks is arbitrary because we constructed them as month-end averages of weekly and daily observations which implies that they become available contemporaneously at the end of the calendar month. As shown in Chart 5, the relative impact of these two blocks are not sensitive to their ordering. 

While we have focused on GDP inflation and growth, central bankers and economists at large are also interested in other aggregate measures of inflation and real activity. Measures of uncertainty for the common factor of the nowcast for inflation based on the core deflator for personal consumption expenditures and for the growth rate of employment in nonfarm payrolls and the unemployment rate are presented in Chart 4a and 4b. Notice that the two measures for inflation move closely together, as do the three measures for real activity. Thus below we will continue to focus on the common factor for real GDP and for GDP inflation. 

Finally, let us remark that the size of news, unlike the measure of uncertainty, depends on the particular realization over the sample period we use for the out-ofsample exercise. This explains why results on the size of the news are some time different than results on average uncertainty. 

16 

**Chart 1b** _Average Size of News: Nowcasts of Inflation_ 

**==> picture [357 x 207] intentionally omitted <==**

**----- Start of picture text -----**<br>
 first month (m=1)   second month (m=2)  third month (m=3)<br>0.08<br>0.07<br>0.06<br>0.05<br>0.04<br>0.03<br>0.02<br>0.01<br>0<br>Mixed 1  Ind. Production Mixed 2  PPI CPI GDP & Income  Housing Surveys 1  Initial Claims  Interest Rates  Financial Surveys 2  Mixed 3  Money & Credit Labor & Wages<br>**----- End of picture text -----**<br>


**Chart 2b** _Average Uncertainty: Nowcast of Inflation_ 

**==> picture [354 x 209] intentionally omitted <==**

**----- Start of picture text -----**<br>
 total   common<br>0.18<br>First Month Second Month Third Month<br>0.16<br>0.14<br>0.12<br>0.1<br>0.08<br>0.06<br>0.04<br>0.02<br>0<br>Labor and Wages Mixed 1  Ind. Production Mixed 2  PPI  CPI  GDP & Income Housing  Surveys 1  Initial Claims  Interest Rates  Financial  Surveys 2  Mixed 3  Money & Credit Labor & Wages Labor and Wages Mixed 1  Ind. Production Mixed 2  PPI  CPI  GDP & Income Housing  Surveys 1  Initial Claims  Interest Rates  Financial  Surveys 2  Mixed 3  Money & Credit Labor & Wages Labor and Wages Mixed 1  Ind. Production Mixed 2  PPI  CPI  GDP & Income Housing  Surveys 1  Initial Claims  Interest Rates  Financial  Surveys 2  Mixed 3  Money & Credit Labor & Wages<br>**----- End of picture text -----**<br>


17 

**Chart 3b** _Average Uncertainty: Nowcast of Inflation (Common Component)_ 

**==> picture [357 x 185] intentionally omitted <==**

**----- Start of picture text -----**<br>
 first month (m=1)   second month (m=2)  third month (m=3)<br>0.07<br>0.06<br>0.05<br>0.04<br>0.03<br>0.02<br>0.01<br>0<br>Labor & Wages Mixed 1  Ind. Production Mixed 2  PPI  CPI GDP & Income Housing Surveys 1  Initial Claims  Interest Rates  Financial Surveys 2  Mixed 3  Money & Credit Labor & Wages<br>**----- End of picture text -----**<br>


**Chart 4b** _Average Uncertainty: Nowcast of Alternative Inflation Measures (Common Component)_ 

**==> picture [354 x 208] intentionally omitted <==**

**----- Start of picture text -----**<br>
Deflator PCEX<br>1<br>First Month Second Month Third Month<br>0.9<br>0.8<br>0.7<br>0.6<br>0.5<br>0.4<br>0.3<br>0.2<br>0.1<br>0<br>Mixed 1  Ind. Production Mixed 2  PPI  CPI  GDP & Income Housing  Surveys 1  Initial Claims  Interest Rates  Financial  Surveys 2  Mixed 3  Money & Credit Labor & Wages Mixed 1  Ind. Production Mixed 2  PPI  CPI  GDP & Income Housing  Surveys 1  Initial Claims  Interest Rates  Financial  Surveys 2  Mixed 3  Money & Credit Labor & Wages Mixed 1  Ind. Production Mixed 2  PPI  CPI  GDP & Income Housing  Surveys 1  Initial Claims  Interest Rates  Financial  Surveys 2  Mixed 3  Money & Credit Labor & Wages<br>**----- End of picture text -----**<br>


18 

**Chart 5a** _Average Uncertainty Under Alternative Ordering: Real Growth (Common Component)_ 

**==> picture [357 x 185] intentionally omitted <==**

**----- Start of picture text -----**<br>
 first month (m=1)   second month (m=2)  third month (m=3)<br>1.2<br>1.0<br>0.8<br>0.6<br>0.4<br>0.2<br>0.0<br>Labor & Wages Mixed 1  Ind. Production Mixed 2  PPI  CPI GDP & Income Housing Surveys 1  Initial Claims  Financial Interest Rates  Surveys 2  Mixed 3  Money & Credit Labor & Wages<br>**----- End of picture text -----**<br>


**Chart 5b** _Average Uncertainty Under Alternative Ordering: Inflation (Common Component)_ 

**==> picture [354 x 208] intentionally omitted <==**

**----- Start of picture text -----**<br>
 first month (m=1)   second month (m=2)  third month (m=3)<br>0.07<br>0.06<br>0.05<br>0.04<br>0.03<br>0.02<br>0.01<br>0.00<br>Labor & Wages Mixed 1  Ind. Production Mixed 2  PPI  CPI GDP & Income Housing Surveys 1  Initial Claims  Financial Interest Rates  Surveys 2  Mixed 3  Money & Credit Labor & Wages<br>**----- End of picture text -----**<br>


19 

## **4.3 The Information Content of the Blocks Conditional on Timeliness** 

The marginal impact of a block is conditional on the set of previously released data. To control for the effect due to timeliness, we construct a counterfactual series of vintage data sets in which data don’t differ in their timing or lags of releases. In this way we can construct a measure of “quality” of the data independent of timeliness. 

For each of the first three months of 2004, we construct 16 vintages with each vintage corresponding˜ to one of the information blocks. These 48 vintages are denoted by _yt|v_ ˜ _j v_ = 04 _m_ 1 _, ...,_ 04 _m_ 3; _j_ = 0 _, ...,_ 15. In contrast to the real-time vintages, each of these counterfactual vintages is constructed from data in a single real-time vintage (which we choose to be _yt|v_ 0 _, v_ = 05 _m_ 3). We then truncate this data set at December 2003, thereby producing a data set that is balanced because the truncation deletes periods which may have had missing observations due to lags in releasing data. We denote the series in this data set as _yt,v_ ˜0 _, t_ = 83 _m_ 1 _, ...,_ 03 _m_ 11 _,_ ˜ _v_ = 04 _m_ 1 and refer to measures of uncertainty constructed from these series as “no release” measures. 

Starting with this balanced dataset, we construct pseudo panels in which each block is the most timely. For the data set in which the Mixed 1 block is most timely, we add data for January 2004 but only for variables belonging to Mixed 1, obtaining the counterfactual vintage _yt|v_ ˜1.[8] Similarly, we start anew with the balanced data set and add data for January 2004 but only for variables belonging to the second block (IP), obtaining the counterfactual vintage _yt|v_ ˜2. In the end, we obtain the counterfactual ˜ vintages _ytv_ ˜ _j_ , for _j_ = 0 _, ...,_ 15 and _v_ = 03 _m_ 1. 

Then we do the same exercise with the balanced panel truncated at January 2004, ˜ _yt|v_ ˜0 _, v_ = 04 _m_ 2, and add February 2004 data for each block one by one to construct ˜ _ytv_ ˜ _j_ , for _j_ = 0 _, ...,_ 15 and _v_ = 05 _m_ 2 and so on, up through March. In the end, we obtain ˜ _yt|v_ ˜ _j_ , for _v_ = 04 _m_ 1 _, ...,_ 04 _m_ 3, _j_ = 0 _, ...,_ 15. 

Using these vintages, we construct measures of common-factor uncertainty for the nowcasts. They are reported in Chart 6a and 6b.[9] The horizontal dashed lines are drawn at the level of the “no release” uncertainty. As it was expected, in each month, each block of information either leaves the average uncertainty of the nowcast unchanged, or reduces it, relatively to the “no release” value. 

In Chart 6a we report results for GDP. Industrial production has now become an important block and so has GDP & Income and Labor and Wages. The importance of surveys and interest rates is now reduced. 

In Chart 6b we report results for inflation. Compared with Chart 2b, where the main effect was due to surveys, GDP and income and financial variables, we now have a clear effect of the price blocks and of industrial production. The effect of financial variables remain sizeable while that of surveys is reduced. 

In general, hard data become important while they were not in the real time exercise, while soft data have a lower impact which reflects the fact that part of their contribution is mainly due to timeliness. 

> 8The values for January 2004 that we use here, we use values for this month form the vintage, _v_ = 05 _m_ 3. 

> 9In computing these results, we run the Kalman filter over the various datasets but estimate the model parameters only once on the basis of the balanced panel (up to September 2004, in this case). Numerical details of these exercises are reported in Tables 4a and 4b. 

20 

We should stress, however, that the effect of financial variables on inflation uncertainty remains large and it is therefore independent of timeliness. 

**Chart 6a** _Counterfactual Average Uncertainty : Real Growth 2004-Q1 (Common Component)_ 

**==> picture [335 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-04 Feb-04 Mar-04<br>1<br>0.9<br>0.8<br>0.7<br>0.6<br>0.5<br>0.4<br>0.3<br>0.2<br>0.1<br>0<br>no release  Mixed 1  Ind. Production Mixed 2  PPI  CPI GDP & Income  Housing Surveys 1  Initial Claims  Interest Rates  Financial Surveys 2  Mixed 3  Money & Credit Labor & Wages<br>**----- End of picture text -----**<br>


**Chart 6b** _Counterfactual Average Uncertainty: Inflation 2004-Q1 (Common Component)_ 

**==> picture [334 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
Jan-04 Feb-04 Mar-04<br>0.06<br>0.05<br>0.04<br>0.03<br>0.02<br>0.01<br>0.00<br>no release  Mixed 1  Ind. Production Mixed 2  PPI  CPI GDP and Income Housing Surveys 1  Initial Claims  Interest Rates  Financial Surveys 2  Mixed 3  Money & Credit Labor & Wages<br>**----- End of picture text -----**<br>


21 

## **5 Summary and Conclusion** 

This paper has analysed the impact of the flow of information within the month on the estimate of current quarter GDP growth and inflation before these variables are published. We considered the unsynchronous release of about 200 monthly time series where releases are organized in groups of homogeneous variables. To this end, we have proposed a framework which is an adaptation of the parametric version of the large dynamic factor model proposed by GRS and Doz, Giannone, and Reichlin (2005). 

This model allows to analyze the flow of a large number of time series and update the signal on the basis of a panel which, due to the unsynchronous release of data, is unbalanced at the end of the sample. 

We find that information matters in the sense that the precision of the signal increases monotonically within the month as new data are released. We also find that both timeliness of the release and quality matter for decreasing uncertainty. Surveys have a large impact on both inflation and output in real time and their effect is larger than the Employment Report. Hard data such as price and real variables have no effect since they are released relatively late. When we control for timeliness, the contribution of hard data increases and we find a sizeable effect of both nominal and real variables on inflation while for GDP only real variables matter. Another finding is that interest rates affect the precision of the estimates of GDP, but not that of inflation while asset prices affect the precision of the nowcast of inflation, but not that of GDP. 

22 

## **References** 

- Altissimo, F., A. Bassanetti, R. Cristadoro, M. Forni, M. Hallin, and Lippi (2001): “EuroCOIN: A Real Time Coincident Indicator of the Euro Area Business Cycle,” CEPR Discussion Papers 3108. 

- Bai, J. (2003): “Inferential Theory for Factor Models of Large Dimensions,” _Econometrica_ , 71(1), 135–171. 

- Bernanke, B., and J. Boivin (2003): “Monetary Policy in a Data-Rich Environment,” _Journal of Monetary Economics_ , 50, 525–546. 

- Boivin, J., and S. Ng (2003): “Are More Data Always Better for Factor Analysis?,” NBER Working Paper 9829, _Journal of Econometrics_ , forthcoming. (2005): “Understanding and Comparing Factor-Based Forecasts,” NBER 

- Working Paper 11285. 

- Doz, C., D. Giannone, and L. Reichlin (2005): “A Maximum Likelihood Approach for Large Approximate Dynamic Factor Models,” Unpublished manuscript. 

- Engle, R. F., and M. Watson (1981): “A one-factor multivariate time series model of metropolitan wage rates,” _Journal of the American Statistical Association_ , 76, 774–781. 

- Evans, M. D. (2005): “Where Are We Now? Real-Time Estimates of the Macro Economy,” NBER Working Paper 11064, _Internationa Journal of Central Banking_ , forthcoming. 

- Forni, M., D. Giannone, M. Lippi, and L. Reichlin (2005): “Opening the Black Box: Structural Factor Models with large cross-sections,” Manuscript, (www.dynfactors.org). 

- Forni, M., M. Hallin, M. Lippi, and L. Reichlin (2000): “The Generalized Dynamic Factor Model: identification and estimation,” _Review of Economics and Statistics_ , 82, 540–554. 

   - (2003): “The Generalized Dynamic Factor Model: one-sided estimtion and 

   - forecasting,” CEPR Working Paper 9829, _Journal of the American Statistical Association_ , forthcoming. 

- Forni, M., and L. Reichlin (2001): “Federal Policies and Local Economies: Europe and the US,” _European Economic Review_ , 45, 109–134. 

- Giannone, D., L. Reichlin, and L. Sala (2004): “Monetary Policy in Real Time,” in _NBER Macroeconomics Annual_ , ed. by M. Gertler, and K. Rogoff, pp. 161–200. MIT Press. 

- Marcellino, M., J. H. Stock, and M. W. Watson (2003): “Macroeconomic Forecasting in the Euro Area: Country Specific versus Area-Wide Information,” _European Economic Review_ , 47, 1–18. 

23 

- Quah, D., and T. J. Sargent (2004): “A Dynamic Index Model for Large CrossSection,” in _Business Cycle_ , ed. by J. Stock, and M. Watson, pp. 161–200. Univeristy of Chicago Press. 

- Stock, J. H., and M. W. Watson (1989): “New Indexes of Coincident and Leading Economic Indicators,” in _NBER Macroeconomics Annual_ , ed. by O. J. Blanchard, and S. Fischer, pp. 351–393. MIT Press. 

(2002): “Macroeconomic Forecasting Using Diffusion Indexes,” _Journal of Business and Economics Statistics_ , 20, 147–162. 

24 

## **A Appendix** 

## **A.1 Construction of the Vintage Data Sets** 

We construct the sequence of vintages _v_ 1 _, ..., v_ 15 for a given month _v_ from two data sets: the ones containing all data collected for months _v−_ 1 and _v_ (including the Employment Report early in the following month). Because these data sets contain the releases of all 15 information blocks, they are denoted as ( _v −_ 1)15 and _v_ 15, respectively. The data set ( _v −_ 1)15 is also the initial data set for month v, so ( _v −_ 1)15 = _v_ 0. 

Starting with _v_ 0 for month _v_ , the data series in that data set are replaced and updated recursively block-by-block with blocks that were released in month v (and that are contained in the data set indexed by _v_ 15). For example, _v_ 1 is constructed by identifying the series in Block 1 (Mixed 1) and replacing its values in _v_ 0 with those from _v_ 15, while leaving the values for series in all other blocks unchanged. When making such replacements, each series in the block is replaced by the new readings on its current and past values because new releases contain new values not only for the most recent dates, but also for past dates. We call _v_ 1 a “pseudo vintage”, because the data series in it were not literally constructed in real time, they are constructed from information blocks that generally preserve the chronological order of the data releases. The pseudo vintage _v_ 2 is constructed from _v_ 1 by identifying all series in Block 2, taking their values from _v_ 15 and using them to replace the values for the series reported in _v_ 1 for Block 2. The pseudo vintages _v_ 3 _, v_ 4 _, ..., v_ 15 are constructed in the analogous manner. 

In sum, for each month (v= June, 2003; ... ; March 2005), we have 16 vintages indexed by ( _v −_ 1)15 = _v_ 0 _, v_ 1 _, ..., v_ 15 = ( _v_ + 1)0. 

## **A.2 Transformations of the Data Series** 

The transformations we apply to the raw data ( _Yit_ ) so that the model estimation uses data series that are stationary ( _yit_ ) are: 

## **Data transformations** 

|**code**<br>0<br>1<br>2<br>3<br>4|**transformation**<br>_yit_ =_Yit_<br>_yit_ = log_Yit_<br>_yit_ = (1_−L_3) _Yit_<br>_yit_ = (1_−L_3) log_Yit ×_100<br>_yit_ = (1_−L_3)(1_−L_12) log_Yit ×_100|**Description**<br>no transformation<br>log<br>three-month diference<br>three-month growth rate<br>three-month diference of yearly growth rate|
|---|---|---|



The particular transformation that we apply to a series is reported in column 4 of the table in Section C of the Appendix. 

## **A.3 Estimation of Parameters** 

In this section we do not consider the dependence of data on the vintage but instead work under the assumption that the data generating process of the idiosyncratic component is the same across different releases. In particular, we assume homoscedasticity 

25 

of the idiosyncratic component across vintages, E _ξt|vj ξt[′] |vj_[= Ψ][for][all] _[v][j]_[.][However,][re-] laxing this assumption does not have major consequences for the results below because the principal component estimator is robust to a limited amount of heteroscedasticity, which could be induced by the data revision process (see e.g. Bai (2003)). 

The assumptions that allow us to identify the common and idiosyncratic components of the model are: 

A1. Common factors are pervasive 

**==> picture [98 x 25] intentionally omitted <==**

and 

A2. Idiosyncratic factors are non-pervasive 

**==> picture [120 x 25] intentionally omitted <==**

Assumption A1 implies that the common factors must be understood as sources of variation that remain pervasive as we increase the number of series in the dataset. In that sense, the common factors correspond to the notion of macroeconomic shocks. Assumption A.2 implies that idiosyncratic factors may affect more than one particular series (Ψ need not be diagonal, however the idiosyncratic shocks are assumed to be stationary), but the effects of an idiosyncratic shock are limited to a particular cluster and do not propagate throughout the macroeconomy. 

Next, we define: 

**==> picture [63 x 11] intentionally omitted <==**

**==> picture [88 x 25] intentionally omitted <==**

where _µ_ ˆ _it_ = _T_[1] � _Tt_ =1 _[y][it]_[and] _[σ]_[ˆ] _[i]_[=] � _T_ 1 ~~�~~ _Tt_ =1[(] _[y][it][ −][µ]_[ˆ] _[i]_[)][2] _[.]_ Consider the following estimator of the common factors: 

**==> picture [175 x 31] intentionally omitted <==**

To derive these estimators, define the sample correlation matrix of the observables ( _zt_ ): 

**==> picture [68 x 31] intentionally omitted <==**

Denote by _D_ the _r × r_ diagonal matrix with diagonal elements given the largest _r_ eigenvalues of _S_ and denote by _V_ the _n × r_ matrix of the corresponding eigenvectors subject to the normalization _V[′] V_ = _Ir_ . We estimate the factors as: 

26 

**==> picture [46 x 13] intentionally omitted <==**

The factor loadings, Λ,[ˆ] and the covariance matrix of the idiosyncratic components, ˆΨ, are estimated by regressing the variables on the estimated factors: 

**==> picture [149 x 34] intentionally omitted <==**

and 

**==> picture [108 x 14] intentionally omitted <==**

The other parameters are estimated by running a VAR on the estimated factors, precisely: 

**==> picture [233 x 75] intentionally omitted <==**

Define _P_ as the _q × q_ diagonal matrix with the entries given by the largest _q_ eigenvalues of Σ[ˆ] and by _M_ the _r × q_ matrix of the corresponding eigenvectors, then: 

**==> picture [57 x 11] intentionally omitted <==**

The estimates _µ_ ˆ, Λ,[ˆ] Ψ,[ˆ] _A_[ˆ] , _B_[ˆ] can be shown to be consistent as _n, T →∞._ Under assumptions A1 and A2 this is proven in Forni et al. 2005 and, under slightly different assumptions by Stock and Watson(2002), Bai and Ng(2003) and Giannone, Reichlin and Sala(2003). 

For unbalanced panels the parameters of the model, _µ,_ Λ _, A, B,_ Ψ are estimated using data up to the last date when the balanced panel is available. 

Then we reestimate the factors through the Kalman filter as outlined above in section 3.1.[11] Loosely speaking, the Kalman filter, computes the factors by weighting the innovation content of each variable ( _xi,t_ +1 _−_ E[ _xi,t_ +1 _|x_ 1 _, ..., xt_ ; Λ[ˆ] _, A,_[ˆ] _B,_[ˆ] Ψ])[ˆ] accordingly to its news (the part driven by common shocks _ut_ ) to noise (the part driven by components _ξit_ ) ratio. 

> 10For any square matrix _A_ , diag( _A_ ) is the matrix _A_ with off-diagonal elements set equal to zero. In estimating Ψ, we estimate only the diagonal elements and set the off-diagonal elements to zero. 

> 11Notice that the parameters Λ _, A,_ Ψ _, B_ can reestimated by OLS on the new factors _F_ ˆ _t_ using the implied second order moments which can be computed by running the Kalman smoother. This is one step of the EM algorithm, hence by iterating until convergence, we obtain Maximum Likelihood estimates under Gaussian assumptions. Such a procedure has been used by Engle and Watson (1981) and Stock and Watson (1989) with an handful of time series to compute coincident and lagging indicators, and by Quah and Sargent (2004) with a larger panel of time series. On the development of this idea and some theoretical results, see Doz, Giannone, and Reichlin (2005). 

27 

## **A.4 Estimation of the common factors: relation to Principal Components and Weighted Principal Components** 

Notice that principal components and weighted principal components are a particular case _A_ ˆ = 0 andof theˆΨ =estimates _n_[1] � _ni_ =1of _[ψ]_[ˆ] _[i]_ the _[I][n]_[=] common _[ψI]_[¯] _[n]_[, then the Kalman filter is redundant since the factor] factors derived above. In fact, if we constrain estimated with the Kalman filter step will be proportional to the principal components estimates: 

**==> picture [173 x 14] intentionally omitted <==**

However, if only _A_[ˆ] = 0 is imposed, then 

**==> picture [150 x 14] intentionally omitted <==**

so the estimated factors are proportional to the weighted principal components, i.e. principal components on the weighted data Ψ _[−]_[1] _[/]_[2] _xt._[12] 

With both principal components and generalized principal components, the estimates of the factors are computed by projecting only on the present observations and, thus, the dynamic properties of the factors are not taken into account. In our case, the Kalman filter performs the projection on present and past observations and, thus, takes into consideration the dynamics of the factors and the degree of commonality of each time series. However, when running the Kalman filter, we do not exploit the time series and cross-sectional correlations of the idiosyncratic shocks which are treated as uncorrelated both in time and in the cross section. Estimates are, however, still consistent under the approximate factor structure (Assumption A1 and A2), as shown in Doz, Giannone, and Reichlin (2005). 

## **A.5 Statistics for the Untransformed Data** 

In general, the measures of news and uncertainty in equations 3.10 and 3.12 apply to measures of our data over which the model has been estimated: that is, they apply to monthly data and to data that has been transformed so as to be stationary. Here we derive such measures that apply to data expressed in ways more commonly used by economists. 

Series with native frequencies higher than monthly, such as financial and interest rates, are aggregated to monthly frequencies by taking simple within-month averages. And in general, to derive such measures from monthly variables, one or both of two adjustments need to be made to the measures: 1) to adjust from the model’s monthly forecasts to quarterly forecasts and 2) to adjust from stationary series to non-stationary series. This issues are discussed below. 

**Case 1: Interpolations** All the variables in our model are expressed as monthly series; for example monthly growth rates and monthly inflation. Accordingly, the measures of NEWS and uncertainty derived above in the text apply to series of this frequency. With most practitioners of monetary policy commonly interested in inflation 

> 12Different versions of such an estimator were proposed by Boivin and Ng (2003), Forni and Reichlin (2001), Forni, Hallin, Lippi, and Reichlin (2003). 

28 

and growth at the quarterly frequency (in part because this is the highest frequency at which real GDP and the GDP deflator are published), we transform our measures of News and uncertainty to the quarterly frequency. 

To set notation, the quarterly measure of variable _z_ will be denoted, as in section, 2.1, by: 

**==> picture [46 x 14] intentionally omitted <==**

As an example, consider the case of real GDP. Its quarterly growth rate, defined in the first equation below, can be expressed in terms of the measure _yzt_ , over which the model was estimated: 

**==> picture [338 x 14] intentionally omitted <==**

Since variables enter our model as three-month annualized growth rates, 

**==> picture [176 x 12] intentionally omitted <==**

Hence, we have: 

**==> picture [145 x 13] intentionally omitted <==**

where, as stressed above, we have defined the quarter by its last month We aggregate the forecast accordingly: 

**==> picture [170 x 16] intentionally omitted <==**

and derive the measure of “NEWS” in a analogous manner to that of equation 3.10. 

For the construction of the corresponding uncertainty, we have to take into account the autocorrelation between the extracted factors, which is summarized in the following matrix: 

**==> picture [161 x 52] intentionally omitted <==**

Hence, uncertainty is given by: 

**==> picture [374 x 50] intentionally omitted <==**

where 

**==> picture [165 x 14] intentionally omitted <==**

**Case 2: Going from Stationary to Non-Stationary Data** For some variables, economists are interested in measures of them that are not stationary. For example, 

29 

the measure of GDP inflation used in this model is not stationary and was differenced to yield a stationary series with which the model could be estimated. In particular, GDP inflation enters the model as: 

**==> picture [121 x 14] intentionally omitted <==**

where _πt_ = (log _Pt −_ log _Pt−_ 12) _×_ 100 and _Pt_ is the level of the GDP deflator. We are interested in forecasting annual inflation at a quarterly frequency: 

**==> picture [178 x 13] intentionally omitted <==**

As described above in Generic Case 1, we can first change from monthly to quarterly forecasts of the change of inflation: 

**==> picture [247 x 15] intentionally omitted <==**

Denoting the by ∆[�] _πk[q] |vj_[the][estimates][made][at][time] _[v][j]_[,][our][estimates][for][the][level][of] inflation are given by: 

**==> picture [122 x 33] intentionally omitted <==**

Uncertainty will be measured accordingly as: 

**==> picture [378 x 51] intentionally omitted <==**

where 

**==> picture [182 x 14] intentionally omitted <==**

and _s_ = _k−vj −l_ where _l_ is the maximum delay for the release of _πt_ , as defined in section 2. A similar treatment has been applied to recover the statistics for the unemployment rate which is treated as non stationary and hence enter our model in differences. 

30 

## 

|**Block Name**<br>**Release Name**<br>**Website**|Mixed 1<br>G.19 Consumer Credit<br>http://www.federalreserve.gov/releases/g19/<br>Mixed 1<br>Advance Monthly Sales For Retail and Food Services<br>http://www.census.gov/svsd/www/fullpub.pdf<br>Mixed 1<br>Monthly Treasury Statement of the U.S. Government<br>http://www.fms.treas.gov/mts/<br>Mixed 1<br>FT900 U.S. International Trade<br>http://www.census.gov/foreign-trade/Press-Release/<br>IP<br>G.17 Industrial Production and Capacity Utilization<br>http://www.federalreserve.gov/releases/G17/<br>Mixed 2<br>New Residential Construction<br>http://www.census.gov/indicator/www/newresconst.pdf<br>Mixed 2<br>Business Outlook Survey<br>http://www.phil.frb.org/econ/bos/index.html<br>PPI<br>Producer Price Indexes<br>http://www.bls.gov/news.release/pdf/ppi.pdf<br>CPI<br>Consumer Price Index<br>http://www.bls.gov/news.release/pdf/cpi.pdf<br>GDP & Income<br>Selected series from underlying detail tables<br>http://www.bea.gov/bea/dn/nipaweb/nipa<br>underlying/Index.asp<br>GDP & Income<br>Gross Domestic Product<br>http://www.bea.gov/bea/dn1.htm<br>GDP & Income<br>Personal Income and Outlays<br>http://www.bea.gov/bea/newsrel/pinewsrelease.htm<br>Housing<br>Manufactured Homes Survey<br>http://www.census.gov/const/www/mhsindex.html<br>Housing<br>New Residential Sales<br>http://www.census.gov/const/newressales.pdf<br>Surveys 1<br>Chicago Fed Midwest Manufacturing Index<br>http://www.chicagofed.org/economic<br>research<br>and<br>data/cfmmi.cfm<br>Surveys 1<br>Consumer Confdence Index<br>http://www.pollingreport.com/consumer.htm<br>Surveys 1<br>Survey of Consumers<br>http://www.sca.isr.umich.edu/main.php<br>Initial Claims<br>Unemployment Insurance Weekly Claims Report<br>http://ows.doleta.gov/unemploy/claims<br>arch.asp<br>Interest Rates<br>Freddie Mac Primary Mortgage Survey<br>http://federalreserve.gov/releases/h15/data/wr/cm.txt<br>Interest Rates<br>H.15 Selected Interest Rates<br>http://www.federalreserve.gov/releases/h15/update/<br>Financial<br>Wilshire Index<br>http://www.wilshire.com/Indexes/calculator/<br>Financial<br>S&P Indices<br>http://www.economy.com/freelunch/<br>Financial<br>Exchange rates<br>http://www.federalreserve.gov/releases/h10/update/<br>Financial<br>London Gold PM Fix<br>http://www.kitco.com/charts/historicalgold.html<br>Financial<br>New York Stock Exchange<br>http://www.economy.com/freelunch/<br>Surveys 2<br>The Chicago Report<br>http://www.napm-chicago.org/current.pdf<br>Mixed 3<br>Advance Report on Durable Goods Manufacturers<br>http://www.census.gov/indicator/www/m3/adv/pdf/durgd.pdf<br>Mixed 3<br>Full Report on Durable Goods Manufacturers<br>http://www.census.gov/indicator/www/m3/prel/pdf/s-i-o.pdf<br>Mixed 3<br>Commercial Paper: Commercial Paper Outstanding<br>http://www.federalreserve.gov/releases/cp/table1.htm<br>Mixed 3<br>Construction Spending<br>http://www.census.gov/const/C30/release.pdf<br>Money & Credit<br>American Bankers Association<br>http://www.aba.com/Surveys+and+Statistics/ss<br>delinquency.htm<br>Money & Credit<br>H.3 Aggregate Reserves<br>http://www.federalreserve.gov/releases/h3/<br>Money & Credit<br>H.6 Money Stock Measures<br>http://www.federalreserve.gov/releases/h6/<br>Money & Credit<br>H.8 Assets and Liabilities of U.S. Commercial Banks<br>http://www.federalreserve.gov/releases/h8/<br>Labor & Wages<br>The Employment Situation<br>http://www.bls.gov/news.release/pdf/empsit.pdf|
|---|---|



31 

|**Block Name**<br>**Release**<br>**Series**<br>**Transformation**|Mixed 1<br>Consumer Credit<br>New car loans at auto fnance companies (NSA): loan to value ratio<br>3<br>Mixed 1<br>Consumer Credit<br>New car loans at auto fnance companies (NSA): Amount fnanced ($)<br>3<br>Mixed 1<br>Retail Sales<br>Sales: Retail & food services, total (mil of $)<br>3<br>Mixed 1<br>Treasury Statement<br>Federal govt defcit or surplus (bil of $) (NSA)<br>3<br>Mixed 1<br>U.S. Merchandise Trade<br>Total merchandise exports, total census basis (mil of $)<br>3<br>Mixed 1<br>U.S. Merchandise Trade<br>Total merchandise imports, total census basis (mil of $)<br>3<br>Mixed 1<br>U.S. Merchandise Trade<br>Total merchandise imports (CIF value) (mil of $) (NSA)<br>3<br>IP<br>IP Release<br>Total<br>3<br>IP<br>IP Release<br>Final Products and non-industrial supplies<br>3<br>IP<br>IP Release<br>Final products<br>3<br>IP<br>IP Release<br>Consumer goods<br>3<br>IP<br>IP Release<br>Durable consumer goods<br>3<br>IP<br>IP Release<br>Nondurable consumer goods<br>3<br>IP<br>IP Release<br>Business equipment<br>3<br>IP<br>IP Release<br>Materials<br>3<br>IP<br>IP Release<br>Materials, nonenergy, durables<br>3<br>IP<br>IP Release<br>Materials, nonenergy, nondurables<br>3<br>IP<br>IP Release<br>Mfg (NAICS)<br>3<br>IP<br>IP Release<br>Mfg, durables (NAICS)<br>3<br>IP<br>IP Release<br>Mfg, nondurables (NAICS)<br>3<br>IP<br>IP Release<br>Mining (NAICS)<br>3<br>IP<br>IP Release<br>Utilities (NAICS)<br>3<br>IP<br>IP Release<br>Energy, total (NAICS)<br>3<br>IP<br>IP Release<br>Non-energy, total (NAICS)<br>3<br>IP<br>IP Release<br>Motor vehicles and parts (MVP) (NAICS)<br>3<br>IP<br>IP Release<br>Computers, comm. equip., semiconductors (CCS) (NAICS)<br>3<br>IP<br>IP Release<br>Non-energy excl CCS (NAICS)<br>3<br>IP<br>IP Release<br>Non-energy excl CCS and MVP (NAICS)<br>3<br>IP<br>IP Release<br>Capacity Utilization: Total (NAICS)<br>2<br>IP<br>IP Release<br>Capacity Utilization: Mfg (NAICS)<br>2<br>IP<br>IP Release<br>Capacity Utilization: Mfg, durables (NAICS)<br>2<br>IP<br>IP Release<br>Capacity Utilization: Mfg, nondurables (NAICS)<br>2<br>IP<br>IP Release<br>Capacity Utilization: Mining<br>2<br>IP<br>IP Release<br>Capacity Utilization: Utilities<br>2<br>IP<br>IP Release<br>Capacity Utilization: Computers, comm. equip., semiconductors<br>2<br>IP<br>IP Release<br>Capacity Utilization: Mfg excl CCS<br>2<br>Mixed 2<br>New Residential Construction<br>Privately-owned housing, started: Total (thous)<br>3<br>Mixed 2<br>New Residential Construction<br>New privately-owned housing authorized: Total (thous)<br>3<br>Mixed 2<br>Philadelphia BOS<br>Outlook: General activity<br>2|
|---|---|



32 

33 

|**Block Name**<br>**Release**<br>**Series**<br>**Transformation**|GDP & Income<br>GDP - detail<br>Inventories: Mfg & Trade, Mfg, nondurables (mil of chained 96$)<br>3<br>GDP & Income<br>GDP - detail<br>Inventories: Mfg & Trade, Merchant wholesale (mil of chained 96$)<br>3<br>GDP & Income<br>GDP - detail<br>Inventories: Mfg & Trade, Retail trade (mil of chained 96$)<br>3<br>GDP & Income<br>Personal Income<br>Real disposable personal income<br>3<br>GDP & Income<br>Personal Income<br>PCE: Total (bil of chained 96$)<br>3<br>GDP & Income<br>Personal Income<br>PCE: Durables (bil of chained 96$)<br>3<br>GDP & Income<br>Personal Income<br>PCE: Nondurables (bil of chained 96$)<br>3<br>GDP & Income<br>Personal Income<br>PCE: Services (bil of chained 96$)<br>3<br>GDP & Income<br>Personal Income<br>PCE: Durables - MVP - New autos (bil of chained 96$)<br>3<br>GDP & Income<br>Personal Income<br>PCE chain weight price index: Total<br>4<br>GDP & Income<br>Personal Income<br>PCE prices: total excl food and energy<br>4<br>GDP & Income<br>Personal Income<br>PCE prices: durables<br>4<br>GDP & Income<br>Personal Income<br>PCE prices: nondurables<br>4<br>GDP & Income<br>Personal Income<br>PCE prices: services<br>4<br>Housing<br>Manufactured Homes<br>Mobile homes – mfg shipments (thous)(SA)<br>3<br>Housing<br>New Residential Sales<br>New 1-family houses sold: Total (thous)<br>3<br>Housing<br>New Residential Sales<br>New 1-family houses – months supply @ current rate<br>3<br>Housing<br>New Residential Sales<br>New 1-family houses for sale at end of period (thous)<br>3<br>Surveys 1<br>Chicago Fed MMI Survey<br>Chicago Fed Midwest Mfg Survey: General activity<br>3<br>Surveys 1<br>Consumer Confdence Index<br>Index of consumer confdence<br>2<br>Surveys 1<br>Michigan Survey<br>Michigan Survey: Index of consumer sentiment<br>2<br>Initial Claims<br>Claims (wkly Thurs.)<br>Avg weekly initial claims<br>3<br>Interest Rates<br>Freddie Mac (wkly Wed.)<br>Primary market yield on 30-year fxed mortgage<br>2<br>Interest Rates<br>H.15 (daily)<br>Interest rate: federal funds rate<br>2<br>Interest Rates<br>H.15 (daily)<br>Interest rate: U.S. 3-mo Treasury (sec. Market)<br>2<br>Interest Rates<br>H.15 (daily)<br>Interest rate: U.S. 6-mo Treasury (sec. Market)<br>2<br>Interest Rates<br>H.15 (daily)<br>Interest rate: 1-year Treasury (constant maturity)<br>2<br>Interest Rates<br>H.15 (daily)<br>Interest rate: 5-year Treasury (constant maturity)<br>2<br>Interest Rates<br>H.15 (daily)<br>Interest rate: 7-year Treasury (constant maturity)<br>2<br>Interest Rates<br>H.15 (daily)<br>Interest rate: 10-year Treasury (constant maturity)<br>2<br>Interest Rates<br>H.15 (daily)<br>Bond yield: Moodys AAA corporate<br>2<br>Interest Rates<br>H.15 (daily)<br>Bond yield: Moodys BAA corporate<br>2<br>Financial<br>H.10<br>Nominal efective exchange rate<br>3<br>Financial<br>H.10<br>Spot Euro/US (2)<br>3<br>Financial<br>H.10<br>Spot SZ/US<br>3<br>Financial<br>H.10<br>Spot Japan/US<br>3<br>Financial<br>H.10<br>Spot UK/US<br>3<br>Financial<br>H.10<br>Spot CA/US<br>3<br>Financial<br>London PM Fix (daily)<br>Price of gold ($/oz) on the London market (recorded in the p.m.)<br>4<br>Financial<br>NYSE<br>NYSE composite index<br>3<br>Financial<br>NYSE<br>NYSE : industrial<br>3<br>Financial<br>NYSE<br>NYSE: utilities<br>3|
|---|---|



34 

|**Block Name**<br>**Release**<br>**Series**<br>**Transformation**|Financial<br>S&P<br>S&P composite<br>3<br>Financial<br>S&P (wkly)<br>S&P dividend yield<br>3<br>Financial<br>S&P (wkly)<br>S&P P/E ratio<br>3<br>Financial<br>Wilshire (daily)<br>Wilshire composite index<br>3<br>Surveys 2<br>PMGR-Manufacturing<br>Purchasing Managers Index (PMI)<br>2<br>Surveys 2<br>PMGR-Manufacturing<br>ISM mfg index: production (Institute for Supply Management)<br>2<br>Surveys 2<br>PMGR-Manufacturing<br>ISM mfg index: Employment<br>2<br>Surveys 2<br>PMGR-Manufacturing<br>ISM mfg index: inventories<br>2<br>Surveys 2<br>PMGR-Manufacturing<br>ISM mfg index: new orders<br>2<br>Surveys 2<br>PMGR-Manufacturing<br>ISM mfg index: suppliers deliveries<br>2<br>Mixed 3<br>Commercial Paper<br>Commercial paper month-end outstanding: Total (mil of $)<br>3<br>Mixed 3<br>Construction Put in Place<br>Construction put in place: Total (mil of current $)<br>3<br>Mixed 3<br>Construction Put in Place<br>Construction put in place: Private (mil of current $)<br>3<br>Mixed 3<br>Advance Durables / M3<br>New Orders: Durable goods industries (mil of $)<br>3<br>Mixed 3<br>Advance Durables / M3<br>New Orders: Nondefense capital goods (mil of $)<br>3<br>Mixed 3<br>M3<br>New Orders: All manufacturing industries (mil of $)<br>3<br>Mixed 3<br>M3<br>New Orders: All manuracturing industries w/unflled orders (mil of $)<br>3<br>Mixed 3<br>M3<br>New Orders: Nondurable goods industries (mil of $)<br>3<br>Mixed 3<br>M3<br>Unflled Orders: All manufacturing industries (mil of $)<br>3<br>Money & Credit<br>Consumer Delinq. Bulletin<br>Delinquency rate on bank-held consumer installment loans<br>3<br>Money & Credit<br>H.3<br>Monetary base (mil of $)<br>3<br>Money & Credit<br>H.3<br>Depository institutions reserves: Total (mil of $)<br>3<br>Money & Credit<br>H.3<br>Depository institutions: nonborrowed (mil of $)<br>3<br>Money & Credit<br>H.6<br>M1 (mil of $)<br>3<br>Money & Credit<br>H.6<br>M2 (mil of $)<br>3<br>Money & Credit<br>H.6<br>M3 (mil of $)<br>3<br>Money & Credit<br>H.8<br>Loans and Securities @ all commercial banks: Total (mil of $)<br>3<br>Money & Credit<br>H.8<br>Loans and Securities @ all comm banks: Securities, total (mil of $)<br>3<br>Money & Credit<br>H.8<br>Loans and Securities @ all comm banks: Securities, U.S. govt (mil of $)<br>3<br>Money & Credit<br>H.8<br>Loans and Securities @ all comm banks: Real estate loans (mil of $)<br>3<br>Money & Credit<br>H.8<br>Loans and Securities @ all comm banks: Comm and Indus loans (mil of $)<br>3<br>Money & Credit<br>H.8<br>Loans and Securities @ all comm banks: Consumer loans (mil of $)<br>3<br>Labor & Wages<br>Employment Situation<br>Unemployment rate<br>2<br>Labor & Wages<br>Employment Situation<br>Participation rate<br>2<br>Labor & Wages<br>Employment Situation<br>Mean duration of unemployment<br>3<br>Labor & Wages<br>Employment Situation<br>Persons unemployed less than 5 weeks<br>3<br>Labor & Wages<br>Employment Situation<br>Persons unemployed 5 to 14 weeks<br>3<br>Labor & Wages<br>Employment Situation<br>Persons unemployed 15 to 26 weeks<br>3<br>Labor & Wages<br>Employment Situation<br>Persons unemployed 15+ weeks<br>3<br>Labor & Wages<br>Employment Situation<br>Employment on nonag payrolls: Total<br>3<br>Labor & Wages<br>Employment Situation<br>Employment on nonag payrolls: Total private<br>3<br>Labor & Wages<br>Employment Situation<br>Employment on nonag payrolls: Goods-producing<br>3|
|---|---|



35 

36 

## **D Tables** 

**Table 2a** : Average Size of the news for GDP growth rate 

|Blocks _vb_|frst month (m=1)|second month (m=2)|third month (m=3)|
|---|---|---|---|
|Mixed 1<br>Industrial Production<br>Mixed 2<br>PPI<br>CPI<br>GDP and Income<br>Housing<br>Surveys 1<br>Initial Claims<br>Interest Rates<br>Financial<br>Surveys 2<br>Mixed 3<br>Money & Credit<br>Labor and Wages|0.104<br>0.527<br>0.676<br>0.073<br>0.100<br>0.042<br>0.006<br>0.414<br>0.087<br>0.489<br>0.166<br>0.256<br>0.007<br>0.040<br>0.362|0.081<br>0.427<br>0.179<br>0.038<br>0.064<br>0.030<br>0.006<br>0.205<br>0.136<br>0.764<br>0.067<br>0.167<br>0.010<br>0.040<br>0.241|0.081<br>0.531<br>0.127<br>0.050<br>0.056<br>0.071<br>0.009<br>0.135<br>0.058<br>0.583<br>0.076<br>0.112<br>0.004<br>0.037<br>0.244|



**Table 2b** : Average Size of the news for GDP Deflator inflation 

|Blocks _vb_|frst month (m=1)|second month (m=2)|third month (m=3)|
|---|---|---|---|
|Mixed 1<br>Industrial Production<br>Mixed 2<br>PPI<br>CPI<br>GDP and Income<br>Housing<br>Surveys 1<br>Initial Claims<br>Interest Rates<br>Financial<br>Surveys 2<br>Mixed 3<br>Money & Credit<br>Labor and Wages|0.002<br>0.029<br>0.033<br>0.032<br>0.040<br>0.160<br>0.001<br>0.028<br>0.002<br>0.003<br>0.035<br>0.008<br>0.000<br>0.002<br>0.006|0.001<br>0.027<br>0.009<br>0.016<br>0.017<br>0.015<br>0.001<br>0.016<br>0.003<br>0.014<br>0.031<br>0.008<br>0.001<br>0.001<br>0.010|0.001<br>0.023<br>0.015<br>0.018<br>0.017<br>0.032<br>0.001<br>0.012<br>0.002<br>0.019<br>0.021<br>0.006<br>0.000<br>0.001<br>0.009|



37 

**Table 3a** : Average uncertainty for GDP growth rate 

||frst month (m=1)|second month (m=2)|third month (m=3)|
|---|---|---|---|
|Blocks|total<br>common|total<br>common|total<br>common|
|Labor and Wages<br>Mixed 1<br>Industrial Production<br>Mixed 2<br>PPI<br>CPI<br>GDP and Income<br>Housing<br>Surveys 1<br>Initial Claims<br>Interest Rates<br>Financial<br>Surveys 2<br>Mixed 3<br>Money & Credit<br>Labor and Wages|1.305<br>1.004<br>(0.027)<br>(0.027)<br>1.303<br>1.002<br>(0.027)<br>(0.027)<br>1.290<br>0.985<br>(0.028)<br>(0.028)<br>1.219<br>0.890<br>(0.024)<br>(0.025)<br>1.219<br>0.889<br>(0.024)<br>(0.026)<br>1.219<br>0.889<br>(0.025)<br>(0.026)<br>1.218<br>0.889<br>(0.025)<br>(0.026)<br>1.218<br>0.889<br>(0.025)<br>(0.026)<br>1.196<br>0.858<br>(0.024)<br>(0.024)<br>1.179<br>0.834<br>(0.028)<br>(0.030)<br>1.110<br>0.733<br>(0.022)<br>(0.022)<br>1.106<br>0.727<br>(0.023)<br>(0.023)<br>1.096<br>0.712<br>(0.021)<br>(0.021)<br>1.096<br>0.712<br>(0.021)<br>(0.021)<br>1.095<br>0.711<br>(0.021)<br>(0.021)<br>1.072<br>0.675<br>(0.020)<br>(0.019)|1.067<br>0.669<br>(0.019)<br>(0.018)<br>1.064<br>0.665<br>(0.019)<br>(0.019)<br>1.043<br>0.631<br>(0.018)<br>(0.017)<br>0.997<br>0.550<br>(0.016)<br>(0.016)<br>0.996<br>0.550<br>(0.016)<br>(0.016)<br>0.996<br>0.549<br>(0.017)<br>(0.017)<br>0.995<br>0.548<br>(0.016)<br>(0.016)<br>0.995<br>0.548<br>(0.016)<br>(0.016)<br>0.982<br>0.523<br>(0.016)<br>(0.015)<br>0.969<br>0.499<br>(0.016)<br>(0.014)<br>0.925<br>0.406<br>(0.013)<br>(0.016)<br>0.922<br>0.400<br>(0.014)<br>(0.015)<br>0.916<br>0.387<br>(0.013)<br>(0.012)<br>0.916<br>0.386<br>(0.013)<br>(0.012)<br>0.916<br>0.386<br>(0.013)<br>(0.012)<br>0.902<br>0.351<br>(0.012)<br>(0.009)|0.902<br>0.351<br>(0.013)<br>(0.010)<br>0.901<br>0.347<br>(0.013)<br>(0.011)<br>0.888<br>0.311<br>(0.012)<br>(0.009)<br>0.873<br>0.265<br>(0.010)<br>(0.007)<br>0.873<br>0.265<br>(0.010)<br>(0.007)<br>0.872<br>0.264<br>(0.011)<br>(0.007)<br>0.872<br>0.263<br>(0.011)<br>(0.007)<br>0.872<br>0.263<br>(0.011<br>(0.007)<br>0.868<br>0.248<br>(0.011)<br>(0.006)<br>0.863<br>0.232<br>(0.011)<br>(0.006)<br>0.847<br>0.159<br>(0.011)<br>(0.009)<br>0.846<br>0.156<br>(0.011)<br>(0.009)<br>0.844<br>0.147<br>(0.010)<br>(0.006)<br>0.844<br>0.147<br>(0.010)<br>(0.006)<br>0.844<br>0.146<br>(0.010)<br>(0.006)<br>0.840<br>0.121<br>(0.009)<br>(0.012)|



38 

**Table 3b** : Average uncertainty for GDP deflators 

||frst month (m=1)|second month (m=2)|third month (m=3)|
|---|---|---|---|
|Blocks|total<br>common|total<br>common|total<br>common|
|Labor and Wages<br>Mixed 1<br>Industrial Production<br>Mixed 2<br>PPI<br>CPI<br>GDP and Income<br>Housing<br>Surveys 1<br>Initial Claims<br>Interest Rates<br>Financial<br>Surveys 2<br>Mixed 3<br>Money & Credit<br>Labor and Wages|0.156<br>0.062<br>(0.007)<br>(0.009)<br>0.156<br>0.062<br>(0.007)<br>(0.009)<br>0.155<br>0.061<br>(0.007)<br>(0.009)<br>0.154<br>0.056<br>(0.007)<br>(0.008)<br>0.153<br>0.055<br>(0.007)<br>(0.008)<br>0.153<br>0.055<br>(0.007)<br>(0.008)<br>0.115<br>0.054<br>(0.006)<br>(0.008)<br>0.115<br>0.054<br>(0.006)<br>(0.008)<br>0.113<br>0.051<br>(0.006)<br>(0.007)<br>0.113<br>0.051<br>(0.006)<br>(0.007)<br>0.113<br>0.050<br>(0.005)<br>(0.007)<br>0.109<br>0.042<br>(0.005)<br>(0.006)<br>0.109<br>0.041<br>(0.005)<br>(0.006)<br>0.109<br>0.041<br>(0.005)<br>(0.006)<br>0.109<br>0.041<br>(0.005)<br>(0.006)<br>0.109<br>0.041<br>(0.005)<br>(0.006)|0.110<br>0.042<br>(0.005)<br>(0.006)<br>0.110<br>0.042<br>(0.005)<br>(0.006)<br>0.109<br>0.041<br>(0.005)<br>(0.006)<br>0.108<br>0.037<br>(0.004)<br>(0.005)<br>0.107<br>0.036<br>(0.004)<br>(0.005)<br>0.107<br>0.035<br>(0.004)<br>(0.005)<br>0.107<br>0.035<br>(0.004)<br>(0.005)<br>0.107<br>0.035<br>(0.004)<br>(0.005)<br>0.106<br>0.033<br>(0.004)<br>(0.005)<br>0.106<br>0.032<br>(0.004)<br>(0.004)<br>0.106<br>0.031<br>(0.004)<br>(0.004)<br>0.104<br>0.024<br>(0.004)<br>(0.003)<br>0.104<br>0.024<br>(0.004)<br>(0.003)<br>0.104<br>0.024<br>(0.004)<br>(0.003)<br>0.104<br>0.024<br>(0.004)<br>(0.003)<br>0.104<br>0.023<br>(0.004)<br>(0.003)|0.105<br>0.024<br>(0.004)<br>(0.004)<br>0.105<br>0.024<br>(0.004)<br>(0.004)<br>0.104<br>0.023<br>(0.004)<br>(0.004)<br>0.104<br>0.019<br>(0.004)<br>(0.003)<br>0.104<br>0.019<br>(0.004)<br>(0.003)<br>0.103<br>0.018<br>(0.004)<br>(0.003)<br>0.103<br>0.018<br>(0.004)<br>(0.003)<br>0.103<br>0.018<br>(0.004)<br>(0.003)<br>0.103<br>0.016<br>(0.004)<br>(0.003)<br>0.103<br>0.015<br>(0.003)<br>(0.002)<br>0.103<br>0.014<br>(0.003)<br>(0.002)<br>0.102<br>0.010<br>(0.003)<br>(0.001)<br>0.102<br>0.010<br>(0.003)<br>(0.001)<br>0.102<br>0.010<br>(0.003)<br>(0.001)<br>0.102<br>0.010<br>(0.003)<br>(0.001)<br>0.102<br>0.009<br>(0.003)<br>(0.001)|



39 

**Table 4a:** Uncertainty for GDP growth rate (04 _Q_ 1) (counterfactual) 

||˜_v_ = 04_m_1|˜_v_ = 04_m_2|˜_v_ = 04_m_3|
|---|---|---|---|
|Blocks|common<br>total|common<br>total|common<br>total|
|no release<br>Mixed 1<br>Industrial Production<br>Mixed 2<br>PPI<br>CPI<br>GDP and Income<br>Housing<br>Surveys 1<br>Initial Claims<br>Financial<br>Interest Rates<br>Surveys 2<br>Mixed 3<br>Money & Credit<br>Labor and Wages|0.861<br>1.189<br>0.784<br>1.135<br>0.570<br>0.998<br>0.733<br>1.100<br>0.837<br>1.172<br>0.820<br>1.159<br>0.608<br>1.021<br>0.825<br>1.163<br>0.734<br>1.101<br>0.803<br>1.148<br>0.837<br>1.171<br>0.715<br>1.088<br>0.736<br>1.102<br>0.750<br>1.111<br>0.835<br>1.170<br>0.641<br>1.041|0.554<br>0.990<br>0.488<br>0.954<br>0.285<br>0.868<br>0.446<br>0.933<br>0.536<br>0.980<br>0.522<br>0.972<br>0.331<br>0.884<br>0.525<br>0.973<br>0.446<br>0.934<br>0.505<br>0.963<br>0.535<br>0.979<br>0.422<br>0.922<br>0.449<br>0.935<br>0.456<br>0.938<br>0.532<br>0.977<br>0.357<br>0.894|0.271<br>0.864<br>0.230<br>0.852<br>0.079<br>0.824<br>0.205<br>0.845<br>0.261<br>0.860<br>0.253<br>0.858<br>0.000<br>0.000<br>0.254<br>0.858<br>0.204<br>0.845<br>0.241<br>0.855<br>0.260<br>0.860<br>0.184<br>0.840<br>0.207<br>0.846<br>0.209<br>0.846<br>0.258<br>0.860<br>0.140<br>0.832|



**Table 4b:** Uncertainty for GDP deflators (04 _Q_ 1) (counterfactual) 

||˜_v_ = 04_m_1|˜_v_ = 04_m_2|˜_v_ = 04_m_3|
|---|---|---|---|
|Blocks|common<br>total|common<br>total|common<br>total|
|no release<br>Mixed 1<br>Industrial Production<br>Mixed 2<br>PPI<br>CPI<br>GDP and Income<br>Housing<br>Surveys 1<br>Initial Claims<br>Financial<br>Interest Rates<br>Surveys 2<br>Mixed 3<br>Money & Credit<br>Labor and Wages|0.055<br>0.110<br>0.054<br>0.109<br>0.043<br>0.104<br>0.052<br>0.108<br>0.039<br>0.103<br>0.036<br>0.102<br>0.040<br>0.103<br>0.053<br>0.109<br>0.052<br>0.108<br>0.055<br>0.109<br>0.041<br>0.103<br>0.053<br>0.109<br>0.052<br>0.108<br>0.052<br>0.108<br>0.054<br>0.109<br>0.049<br>0.107|0.035<br>0.101<br>0.035<br>0.101<br>0.025<br>0.098<br>0.032<br>0.100<br>0.022<br>0.097<br>0.020<br>0.097<br>0.023<br>0.098<br>0.034<br>0.101<br>0.032<br>0.100<br>0.035<br>0.101<br>0.024<br>0.098<br>0.034<br>0.101<br>0.032<br>0.100<br>0.033<br>0.101<br>0.034<br>0.101<br>0.030<br>0.100|0.018<br>0.097<br>0.017<br>0.096<br>0.011<br>0.096<br>0.015<br>0.096<br>0.011<br>0.096<br>0.009<br>0.095<br>0.000<br>0.000<br>0.017<br>0.096<br>0.016<br>0.096<br>0.017<br>0.096<br>0.012<br>0.096<br>0.017<br>0.096<br>0.015<br>0.096<br>0.017<br>0.096<br>0.017<br>0.096<br>0.014<br>0.096|



40 


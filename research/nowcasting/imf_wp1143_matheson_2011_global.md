WP/11/43 

**==> picture [478 x 91] intentionally omitted <==**

## New Indicators for Tracking Growth in Real Time 

_Troy Matheson_ 

**==> picture [450 x 43] intentionally omitted <==**

© 2011 International Monetary Fund 

WP/11/43 

## **IMF Working Paper** 

Research Department 

**New Indicators for Tracking Growth in Real Time** 

Prepared by Troy Matheson[*] 

Authorized for distribution by Krishna Srinivasan 

February 2011 

## **This Working Paper should not be reported as representing the views of the IMF.** 

The views expressed in this Working Paper are those of the author(s) and do not necessarily represent those of the IMF or IMF policy. Working Papers describe research in progress by the author(s) and are published to elicit comments and to further debate. 

## **Abstract** 

We develop monthly indicators for tracking growth in 32 advanced and emerging-market economies. We test the historical performance of our indicators and find that they do a good job at describing the business cycle. In a recursive out-of-sample forecasting exercise, we find that the indicators generally produce good GDP growth forecasts relative to a range of time series models. 

JEL Classification Numbers: C51, C53, E17 

Keywords: Nowcasting, Short-term forecasting, Real-time data 

Author’s E-Mail Address: tmatheson@imf.org. 

> * The author would like to acknowledge comments from Jörg Decressin, Emil Stavrev, and Krishna Srinivasan. The paper outlines the methodology behind the ‘Growth Tracker’, which appears in the World Economic Outlook. 

## Contents 

|||Page|
|---|---|---|
|I|Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|3|
|II|Methodology<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|4|
||A<br>Dynamic factor model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|4|
||B<br>Estimation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|5|
|III|Data . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|6|
|IV|Specifcation and historical ft . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|7|
||A<br>Smoothed indicators for tracking growth . . . . . . . . . . . . . . . . . . . .|9|
|V|Real-time forecast evaluation . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|11|
||A<br>The real-time problem . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|12|
||B<br>Real-time experiment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|12|
||C<br>Forecasting results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|16|
|VI|Revision properties . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|16|
|VIIConcluding Remarks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .||19|
|References . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .||20|
|Appendices . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .||22|
|I|Data transformation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|22|
|Tables|||
|1|Data description . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|7|
|2|Factor model parameters and historical ft<br>. . . . . . . . . . . . . . . . . . . . .|8|
|3|Stylized data panel for different classes of variable<br>. . . . . . . . . . . . . . . .|12|
|4|Forecast accuracy: Nowcast . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|18|
|Figures|||
|1|Interpolated GDP growth and growth indicators (% at an annual rate) . . . . . . .|10|
|2|Growth Tracker . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|11|
|3|Interpolated GDP growth and smoothed indicators in real time (% at an annual rate) 17||



3 

## **I. INTRODUCTION** 

Evaluating the current state of the business cycle is of crucial importance to policy makers and the general public alike. However, economic data are often noisy and available with a substantial lag. Determining the underlying state of an economy is thus very difficult in practice, requiring a mix of information gleaned from economic and statistical models and – perhaps most importantly – the expertise of economists. The importance of the real-time measurement of economic activity is reflected in the significant resources devoted to macroeconomic monitoring by policy-making institutions, and the large number of private firms providing economic analyses to clients eager to get a fix on the current state of the economy. Against this backdrop, we develop monthly growth indicators for 32 advanced and emerging-market economies that can utilize a wide range of economic information in real time. These indicators are currently used for tracking short-term trends in global growth in the World Economic Outlook. 

The OECD and the Conference Board have a long history of publishing composite indicators,[2] while more sophisticated attempts to capture the U.S. business cycle using dynamic factor models have been provided by Stock and Watson (1989), Mariano and Murasawa (2003), Aruoba and others (2009), and Boragan and Diebold (2010). Mariano and Murasawa (2003), Aruoba and others (2009), and Boragan and Diebold (2010), extend the dynamic factor model to incorporate data measured at different frequencies. Similarly, Camacho and Perez-Quiros (2010) aim to estimate real GDP growth at the monthly frequency for the euro area by incorporating data on preliminary, advanced, and final GDP releases; Evans (2005) estimates real GDP at the daily frequency for the U.S. using different vintages of GDP but without using a dynamic factor model. 

The most recent literature tends to use a relatively limited number of economic indicators and the Kalman filter to estimate in the presence of missing data at the end of the sample due to publication lags, the so-called “jagged edge”. We use an approach that is similar in spirit, but focus on estimating indicators using a large number of economic time series for a large number of countries. 

The EuroCoin indicator represents one of the first serious attempts to publish an economic indicator that utilizes a large panel of data in real time.[3] However, the EuroCoin indicator uses an approach to handle missing observations at the end of the sample that changes with the pattern of available data making the underlying model change over time. In contrast, the approach proposed by Giannone and others (2008) and followed, for example, by Barhoumi and others (2008), and Matheson (2010), gets around this problem by using the Kalman filter to estimate in the presence of missing data at the end of the sample. This paper follows this approach. 

> 2See http:www.oecd.org/std/cli and http://www.conference-board.org/data/bci.cfm. 

> 3See Altissimo and others (2007). 

4 

The primary objective of this paper is to produce growth indicators that describe the behavior of economic activity for a large number of countries at the monthly frequency, while utilizing a wide range of economic time series in a timely fashion. Our approach does not explicitly model high-frequency data in the statistically optimal way, as suggested Boragan and Diebold (2010). This choice was made to facilitate the use of the model in real time across a wide range of countries, where some countries have limited data of sufficient quality to produce reliable estimates of economic activity at higher frequencies. Moreover, we consider the computational cost of estimating a high-frequency model with a large number of economic indicators as currently being too high for our purposes. 

We find that our indicators generally do a good job at describing the behavior of real GDP growth for most countries considered. In a real-time forecasting experiment, we also find that the indicators produce good forecasting performance relative to a range of time series models. The indicators generally have good revision properties when applied in real time and, for those countries where historical revisions are particularly large, there is some hope for efficiency improvements with time. 

The paper proceeds as follows. Section (II) outlines the methodology. Section (III) describes the data. Section (IV) discusses the specification of the dynamic factor model and the historical fit of our growth indicators. Section (V) discusses a real-time forecasting exercise and presents the results. Section (VI) evaluates the revision properties of the indicators and section (VII) concludes. 

## **II. METHODOLOGY** 

## **A. Dynamic factor model** 

The growth indicators are estimated using the dynamic factor model (DFM). The DFM is particularly useful in this context, because it can utilize a large number of economic time series in a timely fashion and it has been shown to produce reliable short-term forecasts. See, for example, Giannone and others (2008), Barhoumi and others (2008), and Matheson (2010). 

The DFM assumes that real GDP growth _yt_ can be decomposed into a common component _χt_ and an idiosyncratic component _εt_ . The common component captures the bulk of the covariation between growth and a wide range of economic indicators, while the idiosyncratic component is assumed to mainly only affect growth: 

**==> picture [307 x 13] intentionally omitted <==**

where _µ_ is a constant and _χt_ = Λ _Ft_ , with _Ft_ = ( _F_ 1 _t, . . . , Frt_ ) _[′]_ and Λ = ( _λ_ 1 _, . . . , λr_ ). The common component is thus related to growth through a linear combination of a small handful of _r_ static factors. The static factors themselves are, in turn, estimated using information 

5 

from a potentially large panel of _n_ economic indicators, _Xt_ = ( _x_ 1 _,t, . . . , xn,t_ ), where each indicator in _Xt_ has a factor representation analogous to that of real GDP growth (1). 

The dynamics of the static factors are captured by the following vector autoregressive (VAR) process: 

**==> picture [323 x 34] intentionally omitted <==**

where the _βi_ s are _r × r_ matrices, _p_ is the lag length of the process, _B_ is an _r × q_ matrix, and _q_ is the number of underlying common shocks driving the economy. The number of static factors _r_ is generally assumed to be large relative to the number of common shocks _q_ in order to capture the dynamics of the economy. 

For the purposes of this paper, our indicator for growth _yt[∗]_[is simply the component of growth] estimated in equation 1 (including the constant), after excluding the idiosyncratic component: 

**==> picture [254 x 13] intentionally omitted <==**

One of the key advantages of this framework is that the common component of growth can be estimated when some of the economic indicators have missing values at the end of the sample due to publication lags. This effectively means that the model can utilize all available information in real time. 

## **B. Estimation** 

The estimation procedure begins with the panel of data _Xt_ up to the last date when the balanced panel is available. The common factors _Ft_ are then estimated from this balanced panel using principal components, and the factor loadings and the covariance matrix of the idiosyncratic components are estimated by regressing the variables on the estimated factors. The other parameters of the model are estimated by running a VAR on the estimated factors. All parameters are then re-estimated using the Kalman filter by assuming that the errors are Gaussian, where, for the unbalanced part of the panel, restrictions are imposed on the idiosyncratic components. These restrictions mean that the signal extraction process implicit in the Kalman filter will put no weight on the missing variables while computing the common factors at time _t_ .[4] See Giannone and others (2008) for a more detailed description of how the procedure deals with missing observations. 

This two-step estimation procedure (estimating the factors and parameters using principal components and OLS, and then re-estimating them using the Kalman filter) is simply the first step of the EM algorithm, and has been shown to produce consistent estimates by Doz and others (2007). The procedure is also discussed in Doz and others (2007), along with principal components and a quasi-maximum likelihood estimator. 

> 4Effectively, the Kalman filter computes the factors by weighting the innovation content of each variable by its signal to noise ratio. The restrictions state that this will go to zero when the data are unobserved. 

6 

## **III. DATA** 

Data selection is a crucial step in developing our growth indicators. Choosing series that are too focused on particular sectors of the economy will bias the estimates, deteriorating the effectiveness of the DFM in estimating the underlying factors driving growth. Thus, for each country, we pay close attention to choosing data from a broad cross section of the economy. 

Given poor data quality, particularly for some emerging countries, we employ a multi-step procedure for cleaning the data of outliers and missing observations. The vast majority of the series are measured at the monthly frequency, with the remaining series measured at the daily, weekly, quarterly, and annual frequencies.[5] All series are converted to the monthly frequency and, where required, they are transformed to be devoid of long-run trends (non-stationarity) prior to estimation of the DFM. The data pre-filtering procedure is detailed in appendix I. 

Broadly speaking, the data were chosen to cover the following categories: 

- Activity (surveys) - includes PMIs, consumer and business confidence etc. 

- Activity (hard data) - includes retail sales, industrial production etc. 

- Trade - includes exports, imports, exchange rates etc. 

- Financial Conditions - includes interest rates, equity prices, credit conditions etc. 

- Employment and Income - includes employment, wages etc. 

- Prices and Costs - includes PPIs, CPIs, inflation expectations etc. 

The implications of developments in key trading partners will be implicitly captured by the trade and survey data included for each country. However, each country’s data set also includes 8 key series for the U.S, which are assumed to capture elements of the global business cycle not captured by the domestic indicators.[6] 

Some information about the series used and their classifications can be found in table 1. For most of the advanced economies the sample period begins in 1994, while the samples for many of the emerging-market economies begin later, due to a lack of available data and the presence of structural breaks. The number of series used also varies across countries depending on available data, ranging from 97 series for Kazakhstan to 290 for Sweden. 

> 5Real GDP for Saudi Arabia is the only series that is initially measured at the annual frequency. 

> 6We include industrial production, 3 retail sales series, the ISM survey for manufacturing, the unemployment rate, employment, and consumer confidence (Conference Board). 

7 

Table 1. Data description 

||||||_Number of Series in Each Category_|_Number of Series in Each Category_|_Number of Series in Each Category_|||
|---|---|---|---|---|---|---|---|---|---|
||||Activity|Activity|Trade|Financial|Employment|Prices||
|Country|Sample begins|Evaluation begins|(surveys)|(hard data)||Conditions|and Income|and Costs|Total|
|United States|1994M01|2000M01|15|41|15|15|21|24|131|
|Canada|1994M01|2000M01|19|57|38|12|17|18|161|
|Mexico|2000M01|2005M01|20|33|33|10|17|16|129|
|Brazil|1996M01|2001M01|17|31|56|22|10|12|148|
|Argentina|2003M01|2008M01|0|16|46|16|10|15|103|
|Chile|2000M01|2005M01|9|29|53|30|12|17|150|
|Columbia|2000M01|2005M01|0|44|39|19|21|18|141|
|Peru|2000M01|2005M01|0|48|24|18|14|20|124|
|Ecuador|2000M01|2005M01|0|31|56|1|4|20|112|
|Venezuela|2004M04|2008M01|0|26|22|41|3|30|122|
|Domenican Republic|2000M01|2005M01|0|1|96|11|30|11|149|
|Uruguay|2001M01|2006M01|0|22|39|9|29|35|134|
|Japan|1994M01|2000M01|30|39|22|9|7|6|113|
|Australia|1994M01|2000M01|32|37|42|8|20|32|171|
|Korea|2000M01|2005M01|37|49|42|22|20|30|200|
|China|2000M01|2006M01|23|82|29|7|34|17|192|
|Indonesia|2004M01|2008M01|3|24|41|12|3|24|107|
|India|2000M01|2007M01|32|25|36|18|4|12|127|
|Euro Area|1994M01|2000M01|20|27|17|17|6|29|116|
|Germany|1994M01|2000M01|58|31|39|18|26|15|187|
|France|1994M01|2000M01|60|28|20|17|24|39|188|
|Italy|1994M01|2000M01|55|32|23|22|12|29|173|
|United Kingdom|1994M01|2000M01|63|58|34|22|29|36|242|
|Russia|2000M01|2005M01|32|40|31|17|17|39|176|
|Turkey|2002M01|2007M01|52|46|38|17|15|19|187|
|Sweden|1994M01|2000M01|59|60|66|14|42|49|290|
|Spain|1994M01|2000M01|44|68|33|17|40|59|261|
|Portugal|2000M01|2005M01|26|44|37|26|30|38|201|
|Greece|2000M01|2005M01|33|41|26|19|19|32|170|
|South Africa|1994M01|2000M01|24|58|45|23|14|27|191|
|Kazakhstan|2000M01|2005M01|0|10|51|12|5|19|97|
|Saudi Arabia|2000M01|2005M01|0|2|28|119|0|27|176|



* Sample begins is the start of the sample period. Evaluation begins is the start of the out-of-sample evaluation period. 

## **IV. SPECIFICATION AND HISTORICAL FIT** 

Bai and Ng (2007) suggest a two-step procedure for determining the number of dynamic factors in factor models. The procedure relies on the fact that the _r × r_ matrix of innovations to the static factors ( _But_ in equation 2) has rank equal to the number of dynamic factors _q_ . The first step of the procedure requires the number of static factors _r_ to be determined using information criteria described in Bai and Ng (2002). Then, once the number of static factors _r_ is set, the rank of spectrum of the _q_ dynamic factors is estimated using the eigenvalues of the residual covariance (or correlation matrix) of the VAR in the _r_ static factors. 

Unfortunately, we found that the Bai and Ng (2002) criteria generally produced too many factors, deteriorating the forecasting performance of the DFM. Likewise, the more ad-hoc approach used by Giannone and others (2005) and Matheson (2010), where the number of factors is chosen to explain a certain percentage of the variation in a few key series, was not well suited to our multi-country setting, because there is significant variation in the explanatory power of the factor model across countries. Instead, following Stock and Watson (2002), we choose the number of factors by minimizing Schwarz’s Bayesian information criterion (SBC). 

Specifically, the number of common factors _r_ is chosen by regressing quarterly real GDP growth on the common factors for _r_ = 1 _, ...,_ 8; the number of factors is then that which minimizes the SBC. The number of common shocks _q_ is then chosen using information 

8 

Table 2. Factor model parameters and historical fit 

|Country|r|q|p|R-squared(%)|Concordance(%)|
|---|---|---|---|---|---|
|United States|4|3|1|72|66|
|Canada|2|2|1|71|61|
|Mexico|1|1|3|60|54|
|Brazil|4|2|1|62|66|
|Argentina|6|4|1|88|64|
|Chile|1|1|3|49|68|
|Columbia|1|1|2|58|69|
|Peru|5|3|1|70|63|
|Ecuador|2|2|1|26|58|
|Venezuela|4|3|1|80|75|
|Domenican Republic|3|3|1|50|75|
|Uruguay|4|2|1|67|78|
|Japan|4|3|3|67|72|
|Australia|6|4|1|59|81|
|Korea|4|3|2|85|78|
|China|3|3|3|42|76|
|Indonesia|1|1|3|34|60|
|India|6|4|2|69|85|
|Euro Area|3|1|1|65|57|
|Germany|4|3|2|86|85|
|France|4|3|2|82|80|
|Italy|3|3|1|79|69|
|United Kingdom|5|3|1|87|75|
|Russia|2|2|2|84|73|
|Turkey|5|3|1|77|66|
|Sweden|2|2|2|56|58|
|Spain|3|2|2|90|69|
|Portugal|5|2|1|73|80|
|Greece|5|3|1|55|61|
|South Africa|1|1|3|63|66|
|Kazakhstan|6|4|1|59|68|
|Saudi Arabia|3|3|1|50|67|
|Average|4|3|2|67|69|



criteria described in Bai and Ng (2007).[7] The number of lags of the factors _p_ included in the model is determined using the SBC. 

The specifications of the DFMs are displayed in table 2. To get an idea of the quality of the growth indicators in describing the behavior of real quarterly GDP growth over history, the table also shows the percentage of the variation of growth explained by the indicators, R-squared, and the proportion of time the indicators move in the same direction as real quarterly GDP growth, concordance. 

The indicators generally explain a sizable proportion of growth for the majority of countries, particularly for advanced countries. Because the growth indicators are estimates of the underlying, pervasive component of growth, their explanatory power tends not to be as great for emerging economies, where growth is generally more volatile and subject to larger idiosyncratic shocks. Nevertheless, the indicators do a good job at predicting the direction of real GDP growth over history, with all concordance statistics being above 50% – the proportion of time a coin toss would accurately predict the direction of a change in growth. 

Some of the growth indicators are subject to more short-run volatility than others. By construction, this volatility is pervasive across the series that went into constructing each indicator. It is also useful, however, to consider an indicator that is both pervasive in the cross section and persistent over time. We thus introduce a smoothed indicator _yt[∗∗]_[that removes the] 

> 7 We use _δ_ = 0 _._ 1 and _m_ = 1 for _q_ 3 and _q_ 4 (the covariance matrix of the VAR residuals is used, rather than the correlation matrix). We take _q_ as being the (rounded) average of _q_ 3 and _q_ 4. 

9 

short-run volatility from the indicator estimated with the DFM. These smoothed indicators are simply centered 7-month-moving averages of the estimated indicators _yt[∗]_[:] 

**==> picture [257 x 13] intentionally omitted <==**

where _ϵt_ captures the short-run noise in the common component of growth. The monthly growth indicators are displayed in figure 1 along with interpolated real GDP growth: dates beyond the collapse of Lehman Brothers near the beginning of the global financial crisis are shaded. 

The indicators generally do a good job at tracking trends in GDP growth over time. All countries’ indicators fell markedly with the onset of the global financial crisis and have since recovered to around pre-crisis levels. As mentioned above, the indicators for the emerging economies produce reasonable estimates of the underlying trends in real GDP growth, despite the volatility inherent in these countries. Even for Saudi Arabia, where GDP is measured at the annual frequency, the growth indicators produce reasonable estimates of growth at the monthly frequency. 

## **A. Smoothed indicators for tracking growth** 

By incorporating estimates of potential output growth, the behavior of the smoothed growth indicators can provide a great deal of information about the current state of the business cycle and the evolution of growth over time. 

The heat map in figure 2 displays information about growth for all of the countries for which we have indicators. The trends referred to in the heat map are the interpolated growth rates of potential output taken from World Economic Outlook (WEO) projections. The colors are based on the behavior of the smoothed indicators relative to trend: a yellow color indicates growth below trend and falling; red and pink indicate contraction at increasing and decreasing rates, respectively; the two lightest shades of green represent rising growth rates, with the lightest green indicating growth is below trend; the darkest green represents that growth is moderating but remains above trend. 

The heat map clearly shows the implications of the global financial crisis for growth. The effects of the crisis were seen across all 32 countries, but differed across regions. A contraction was evident in late 2007 in the U.S, before spreading to most other countries by the beginning of 2008. The growth indicators suggest the U.S economy contracted from late 2007 to early 2009, a longer period than all other countries apart from Greece, where the effects of a sovereign debt crisis perpetuated the decline in activity. 

The economies in the Western Hemisphere generally suffered a shorter contraction than the U.S, likewise for Japan, Korea and Australia. Meanwhile, activity in the Chinese, Indonesian and Indian economies slowed somewhat but growth remained positive throughout the crisis. The crisis was perhaps most keenly felt in Europe, with all major countries contracting from the middle of 2008 to the middle of 2009. 

10 

Figure 1. Interpolated GDP growth and growth indicators (% at an annual rate) 

**==> picture [421 x 592] intentionally omitted <==**

**----- Start of picture text -----**<br>
United States Canada Mexico Brazil<br>5 5 10<br>0<br>−50 GDPIndicatorSmoothed −50 −10 −100<br>−20<br>2002:01 2007:01 2002:01 2007:01 2002:01 2007:01 2002:01 2007:01<br>Argentina Chile Columbia Peru<br>10<br>10 5 10 10<br>5 0 5 5<br>0 0 0<br>−5<br>−5<br>−5 −5<br>2002:01 2007:01 2002:01 2007:01 2002:01 2007:01 2002:01 2007:01<br>Ecuador Venezuela Domenican Republic Uruguay<br>15 20 15<br>10 10 10 10<br>5 5<br>0 0 0 0<br>−5 −5<br>−10 −10<br>2002:01 2007:01 2002:01 2007:01 2002:01 2007:01 2002:01 2007:01<br>Japan Australia Korea China<br>5 6 10<br>4 15<br>0<br>−5 2 0 10<br>−10 0 −10<br>−15 −2 5<br>2002:01 2007:01 2002:01 2007:01 2002:01 2007:01 2002:01 2007:01<br>Indonesia India Euro Area Germany<br>15 4 5<br>8 2<br>10 0 0<br>6 −2<br>4 5 −4 −5<br>2 0 −6−8 −10<br>2002:01 2007:01 2002:01 2007:01 2002:01 2007:01 2002:01 2007:01<br>France Italy United Kingdom Russia<br>4 4 10<br>20 0 20 0<br>−2 −5 −2 −10<br>−4<br>−4 −10 −6 −20<br>−6<br>2002:01 2007:01 2002:01 2007:01 2002:01 2007:01 2002:01 2007:01<br>Turkey Sweden Spain Portugal<br>20 5 4 5<br>2<br>0 0 −20 0<br>−4<br>−5 −6 −5<br>−20<br>−8<br>2002:01 2007:01 2002:01 2007:01 2002:01 2007:01 2002:01 2007:01<br>Greece South Africa Kazakhstan Saudi Arabia<br>10<br>5 6<br>20<br>5 4<br>0<br>0 0 2<br>−5 0<br>−20<br>2002:01 2007:01 2002:01 2007:01 2002:01 2007:01 2002:01 2007:01<br>**----- End of picture text -----**<br>


11 

## Figure 2. Growth Tracker 

**==> picture [406 x 298] intentionally omitted <==**

**----- Start of picture text -----**<br>
Western Hemisphere<br>United States 4 4 4 4 4 4 6 6 6 6 6 6 6 6 6 6 6 6 6 5 5 5 5 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1<br>Canada  4 4 4 4 4 3 4 3 4 4 4 4 4 4 6 6 6 6 6 6 6 5 5 5 3 3 2 2 2 2 2 2 2 2 1 1 1 1<br>Mexico  4 3 3 3 4 3 2 4 4 4 4 4 6 6 6 6 6 6 6 5 5 5 5 5 3 2 2 2 2 2 2 2 1 1 1 1 4 4<br>Brazil  1 2 2 2 2 2 2 1 1 1 1 1 4 4 6 6 6 6 6 5 5 3 3 3 2 2 2 2 2 2 2 1 1 1 1 4 4 4<br>Argentina  1 1 1 2 1 1 1 1 1 1 1 1 1 4 4 4 6 6 6 6 5 5 3 3 3 2 2 2 2 2 2 2 2 2 1 1 1 1<br>Chile   4 4 2 2 2 2 2 2 1 1 4 4 4 6 6 6 6 6 6 5 5 5 3 3 2 2 2 2 2 1 1 1 1 1 1 1 1 2<br>Colombia   4 2 3 2 4 4 4 4 3 4 4 4 4 4 4 4 4 4 3 3 3 3 3 2 2 2 2 2 2 2 2 2 2 1 1 1 1 4<br>Peru 2 2 2 2 2 2 2 2 1 1 1 1 1 4 4 4 6 6 6 6 5 3 3 3 3 3 2 2 2 2 2 2 2 1 1 1 1 1<br>Ecuador 2 2 2 2 2 2 1 1 1 1 1 1 4 4 4 4 6 6 6 3 3 3 2 2 2 2 2 2 2 2 2 1 1 1 1 1 1 1<br>Venezuela  2 2 1 1 1 4 4 4 1 4 4 4 4 4 4 6 6 6 6 6 6 6 6 6 6 6 5 5 5 5 5 3 3 2 2 2 2 1<br>Domanican Republic 2 1 1 2 2 2 1 1 1 1 4 4 4 4 4 6 6 6 6 5 5 3 3 2 2 2 2 2 2 2 2 2 1 1 1 1 1 1<br>Uruguay   1 1 4 4 4 4 4 3 3 4 4 4 4 4 4 4 6 6 6 6 5 3 3 3 3 2 2 2 2 1 1 2 2 2 1 1 1 1<br>Asia Pacific<br>Japan  1 4 4 4 4 4 6 6 6 6 6 6 6 6 6 6 6 6 6 5 5 5 5 2 2 2 2 2 2 2 2 2 1 1 1 1 1 1<br>Australia 4 4 4 4 3 3 3 3 4 4 4 4 4 4 6 4 3 3 3 3 3 2 2 3 2 2 2 2 2 1 1 1 1 4 4 4 4 4<br>Korea  1 2 2 2 1 1 1 1 4 4 4 4 6 6 6 6 6 6 5 5 3 2 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1<br>China   2 2 2 2 1 1 1 1 1 4 4 4 4 4 4 4 4 4 3 3 3 2 2 2 2 1 2 2 2 1 1 1 1 4 4 4 4 4<br>Indonesia 3 2 2 2 2 2 2 2 1 4 4 4 4 4 4 4 4 4 4 3 3 3 3 3 2 2 2 2 2 1 1 4 4 4 4 4 4 3<br>India  2 2 2 2 1 1 1 1 4 4 4 4 3 3 3 2 2 2 2 2 2 2 1 1 4 4 4 4 4 3 3 2 2 2 2 2 1 1<br>Europe<br>Euro Area 1 1 1 1 1 1 1 4 4 4 4 6 6 6 6 6 6 6 6 6 5 5 5 5 2 2 2 2 2 2 2 2 2 2 1 1 1 1<br>Germany  1 1 4 2 2 2 1 4 4 4 6 6 6 6 6 6 6 6 6 6 5 5 5 3 2 2 2 2 1 1 2 2 2 2 2 2 2 1<br>France  1 1 1 4 4 4 4 4 4 4 6 6 6 6 6 6 6 6 6 6 5 5 5 5 3 2 2 2 2 2 2 2 2 2 2 2 2 2<br>Italy  4 4 4 4 4 3 6 6 6 6 6 6 6 6 6 6 6 6 6 6 5 5 5 5 2 2 2 2 2 2 2 2 2 2 1 1 1 1<br>United Kingdom 2 2 1 1 1 1 1 1 1 6 6 6 6 6 6 6 6 6 6 6 5 5 5 5 5 2 2 2 2 2 2 2 2 2 2 2 2 2<br>Russia  1 1 2 2 2 2 2 2 1 1 1 1 4 6 6 6 6 6 6 6 5 5 5 5 3 2 2 2 2 2 2 2 1 1 1 1 1 4<br>Turkey  1 2 2 2 2 2 1 1 4 4 4 6 6 6 6 6 6 6 6 5 5 5 3 3 2 2 2 2 2 2 2 2 2 1 1 1 1 1<br>Sw eden  1 1 2 2 1 1 1 1 1 1 1 4 6 6 6 6 6 6 6 5 5 5 5 3 2 2 2 2 2 2 2 2 2 2 2 1 1 1<br>Spain  1 1 4 4 4 4 4 4 4 6 6 6 6 6 6 6 6 6 6 6 5 5 5 5 5 5 5 5 5 3 2 2 2 2 2 2 2 2<br>Portugal 1 1 2 2 1 1 1 4 4 6 6 6 6 6 6 6 6 6 6 5 5 5 5 2 2 2 2 2 2 2 2 2 1 1 1 1 1 1<br>Greece 1 2 2 2 1 1 1 1 1 1 1 1 1 1 4 6 6 6 6 6 6 6 5 5 5 5 5 5 5 5 6 6 6 6 6 5 5 5<br>Africa<br>South Africa 1 1 1 1 2 2 2 1 1 1 1 4 4 4 6 6 6 6 6 6 6 5 5 5 5 3 3 3 2 2 2 2 1 1 4 4 4 4<br>Middle East & Central Asia<br>Kazakhstan 1 2 2 2 2 2 2 2 1 1 1 1 1 4 4 4 6 6 6 3 3 3 2 2 2 2 2 2 2 2 1 1 1 1 1 1 1 1<br>Saudi Arabia 4 4 4 4 4 4 3 3 2 2 2 2 2 2 2 1 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 3 3 3 4 4 4 4<br>*Source: Haver and IMF Staff estimates. 1 Grow th above trend and moderating<br>2 Grow th above trend and rising<br>The grow th trackers are constructed using a large number of daily, monthly, and quarterly  indicators 3 Grow th below  trend and rising<br>and a dynamic factor model that incorporates all available data. The trackers are estimated and forecast at the  4 Grow th below  trend and moderating<br>monthly frequency. The classifications represented in the table are based on the behavior of a centered 7-month-moving average.  5 Contraction at a moderating rate<br>The most recent estimates implicity include forecasts and can change w ith the arrival of more data. 6 Contraction at an increasing rate<br>Jul-07Aug-07Sep-07Oct-07Nov-07Dec-07Jan-08Feb-08Mar-08Apr-08May-08Jun-08Jul-08Aug-08Sep-08Oct-08Nov-08Dec-08Jan-09Feb-09Mar-09Apr-09May-09Jun-09Jul-09Aug-09Sep-09Oct-09Nov-09Dec-09Jan-10Feb-10Mar-10Apr-10May-10Jun-10Jul-10Aug-10<br>**----- End of picture text -----**<br>


**==> picture [71 x 4] intentionally omitted <==**

**----- Start of picture text -----**<br>
Estimates based on data available on:<br>**----- End of picture text -----**<br>


**==> picture [19 x 4] intentionally omitted <==**

**----- Start of picture text -----**<br>
9/20/2010<br>**----- End of picture text -----**<br>


- trend is potential output grow th taken  from 'live' WEO database. 

Following the downturn, growth recovered strongly for a period several months or more across most countries. Growth has since begun to moderate, first in the parts of the Western Hemisphere and Asia, then in parts of Europe. 

## **V. REAL-TIME FORECAST EVALUATION** 

Assessing the underlying state of the economy is contingent on the behavior of the data at hand and the model used to analyze the data. As such, to the extent new data differ from previous estimates produced by the indicators, they can be revised over both the historical and forecast periods. This may cause the indicators to produce some false signals in real time. Thus, to evaluate how well the indicators perform in real time, we conduct a simulated real-time forecasting experiment. 

12 

## **A. The real-time problem** 

Within each quarter, contemporaneous values of key macroeconomic variables such as GDP are not available. Specifically, at an arbitrary point in each quarter _ν_ , the data available is represented by the information set Ω _[n] ν_[, which includes the most recent data for] _[ n]_[ monthly] time series. The forecaster’s task is to project GDP growth _yν_ + _h_ for _h_ = 0 _, . . . , H_ based on the information set available at _ν_ : 

**==> picture [314 x 13] intentionally omitted <==**

Assume that Ω _[n] ν_[composes of two blocks][ [Ω] _[n] ν_[1][Ω] _[n] ν_[2][]][.][The variables in][ Ω] _[n] ν_[2][, say industrial] production, are released a month later than those in Ω _[n] ν_[1][, say asset prices.][This implies that] variables in Ω _[n] ν_[1][are available up to month] _[ ν]_[, while variables in][ Ω] _[n] ν_[2][is only available up] month _ν −_ 1. Table 3 illustrates a stylized panel of data for different classes of variables. The forecaster needs to project on the basis of this unbalanced panel of data. 

Table 3. Stylized data panel for different classes of variable 

|Month|Activity|Surveys|Assetprices|Foreign|GDP|
|---|---|---|---|---|---|
|_ν −_2|X|X|X|X|O|
|_ν −_1|O|X|X|X|O|
|_ν_|O|O|X|O|O|



X indicates data is available at the end of the month, and O indicates data that is missing from the panel. 

## **B. Real-time experiment** 

In our forecasting experiment, we aim to replicate the real-time application of the growth indicators as closely as possible. However, we do not have the vintages of data as they would have existed in real time. Instead, we rely on data release dates recorded by Haver Analytics to compile quasi-real-time data sets; we manipulate the most recent vintage of data to match the publication lags that would have been seen in real time. These data sets mimic the data available at the beginning of the first month of each quarter of out-of-sample evaluation periods displayed in table 1. For comparison, we also include a range of other forecasting models in the forecasting experiment, described below. In the experiment, we re-specify and re-estimate the models each time a forecast is made. 

## **Baseline quarterly autoregressive model (AR)** 

As a benchmark, we use an univariate AR model of order _p_ for quarterly GDP growth ( _yt[Q]_[):] 

**==> picture [286 x 34] intentionally omitted <==**

13 

where _c_ is a constant, _ϵ[Q] t_[is a quarterly white noise term such that] _[ ϵ][Q] t[∼][N]_[(0] _[, σ]_[2] _ϵ_[)][, and the lag] length _p_ is selected using the SBC. 

## **Pooled bridge equations (BE)** 

The bridge equation is perhaps the most widely used method for forecasting quarterly GDP using monthly indicators.[8] Our bridge equation forecasts are constructed using the following four steps: 

1. We consider the set of monthly indicators _Xt_ and forecast the individual indicators _xi,k_ over the relevant horizon using a univariate AR( _p_ ) model: 

**==> picture [315 x 34] intentionally omitted <==**

2. Each indicator (including forecasts) is converted to the quarterly frequency, _x[Q] i,t_[=] _[ x][i,t]_[ +] _[ x][i,t][−]_[1][ +] _[ x][i,t][−]_[2][, and we estimate the following bridge equation:] 

**==> picture [279 x 33] intentionally omitted <==**

which relates quarterly GDP growth to the quarterly aggregate of the monthly indicator.[9] The lag lengths _pi_ and _qi_ are determined using the SBC. The forecast of GDP growth is obtained by inserting the monthly indicator forecast from equation 7 into 8. 

3. We choose to select the set of 10 monthly indicators that have the highest contemporaneous correlation with quarterly GDP growth. 

4. The forecast for GDP growth is a weighted average of the 10 forecasts from the individual indicators, with the weights based on the inverse of the root mean squared errors (RMSE) of the individual indicators. 

Note that the pooled bivariate VAR model described below also uses the 10 indicators selected in step 3 above. In preliminary work, we experimented with choosing the 5, 20, and 50 indicators most correlated with quarterly real GDP growth and found that forecasting performance generally deteriorated relative to the forecast based on 10 indicators. Choosing all of the available indicators for each country also deteriorated forecasting accuracy. 

> 8See, for example, Kitchen and Monaco (2003) and Baffigi and others, (2004). 

> 9Note that a more general specification would allow for lags of _yi,t[Q]_[on the right hand side of this equation.][In] our application, however, we found that allowing for such lags generally led to a deterioration in forecast accuracy. 

14 

## **Pooled bivariate VARs (BV)** 

Similar to the bridge equation, the bivariate VAR model exploits the information content of monthly indicators. However, while the bridge equation relies on the autoregressive forecasts in step 1, it may be that information in real GDP growth itself can produce more efficient forecasts of the indicators and better forecasts of real GDP growth. 

To capture some of the dynamics between each of the indicators and GDP, we estimate the following monthly bivariate VAR model on GDP growth and each of the 10 indicators used in the bridge equations: 

**==> picture [295 x 34] intentionally omitted <==**

where _Zi,t_ = [ _yt, xi,t_ ] _[′]_ . Prior to estimation of each VAR, we interpolate all indicators measured at frequencies higher than monthly using the Chow and Lin (1971) procedure; we follow Angelini and others (2006) and use the monthly factors estimated using the DFM as regressors in the procedure. As with the other forecasting methods discussed, the lag length _pi_ of the VAR is determined using the SBC. 

Relative to the bridge equations, this methodology loses some information by using interpolated GDP, but it also may produce some efficiency gains by better capturing the dynamics between GDP growth and each indicator. We use the estimated VAR in equation 9 to forecast the monthly GDP growth rates, conditional on the latest monthly indicators available using the Kalman filter. The forecast for GDP growth is formed by weighting together the 10 bivariate VAR forecasts in the same way as the bridge equation forecast. 

## **Bayesian VAR (BVAR)** 

One extension of the bivariate VAR is to include selection of potentially useful monthly indicators. Using the same notation as above, _Zt_ now includes a set of monthly indicators, as well as the GDP growth:[10] 

**==> picture [286 x 34] intentionally omitted <==**

where the constant term _c_ is a _k ×_ 1 vector, _βs_ is a _k × k_ autoregressive matrix, and _ϵt_ is a _k ×_ 1 white noise process with covariance matrix Ψ. To overcome the “curse of dimensionality” problem, we estimate the VAR using Bayesian shrinkage methods by imposing prior beliefs on the parameters. In setting the prior distributions, we follow the procedure developed by Doan and others (1984) and Litterman (1986). 

> 10All indicators initially measured at frequencies higher than monthly are interpolated in the same way as those used in the bivariate VARs described above. 

15 

The basic principle of the Litterman (1986) prior (often referred to as the Minnesota prior) is that all equations are “centered” around a random walk with drift. This amounts to shrinking the diagonal elements of _β_ 1 towards one and all other coefficients in _β_ 1 _, . . . , βp_ towards zero: 

**==> picture [270 x 12] intentionally omitted <==**

This embodies the belief that the more recent lags provide more useful information than the more distant ones. More formally, these priors can be imposed by setting the following moments for the prior distribution of the coefficients: 

**==> picture [412 x 44] intentionally omitted <==**

where _δi_ = 1 _, ∀i_ reflects the random walk prior. The researcher can also incorporate priors where some variables are characterized by a degree of mean-reversion, 0 _≤ δi <_ 1. In our application, we estimate BVARs on stationary data, so we set _δi_ = 0 _, ∀i_ . The hyper-parameter _µ_ 1 controls the overall tightness of the prior distribution around _δi_ , and the factor 1 _/k[λ]_ is the rate at which the prior standard deviation decreases with the lag length of the VAR. See Banbura and others (2010) for more details. 

The BVAR contains real GDP growth, industrial production, inflation, a real exchange rate, a short-term interest rate, and equity prices.[11] Following Banbura and others (2010) , the overall tightness of the prior _µ_ 1 is set such that the average _R_[2] across all equations is fixed at 60% to avoid the problem of “over-fitting”. The BVAR contains 6 lags with _λ_ set to 1, and the standard deviations of the parameters are taken from the estimated residuals of AR(6) processes. As with the bivariate VAR forecasts, the BVAR forecasts are made conditional on all available monthly data using the Kalman filter. 

## **Pooled forecasts** 

There is a large literature showing that model combination tends to improve forecasting accuracy. As such, we also compute two pooled forecasts based on the forecasts described above. The first pooled forecast uses the recursively computed inverse RMSEs of each forecast as weights (INVMSE) and the second is based on a simple average across forecasts (MEAN). 

11For some countries, due to a lack of available data, we replaced one or more of these series with series that have a similar economic interpretation. 

16 

## **C. Forecasting results** 

The forecasting results for predicting the next GDP release – the nowcast – are displayed in table 4.[12] The panel on the right of the table contains the RMSEs of the AR benchmark in predicting annualized real GDP growth and the RMSEs of the competing models relative to RMSEs of the AR, where a ratio less than one indicates that the model in question outperforms the AR. The panel on the left ranks the 7 competing models on the basis of RMSEs. 

The more sophisticated models outperform the AR for all countries except Australia, Argentina, and India, and, of these models, the DFM generally produces the most accurate forecasts. The average RMSE ratio for the DFM across countries is 0.81, the lowest of the competing models. The forecasts based on model averages, INVMSE and MEAN, are the next most accurate, with average RMSE ratios of 0.84 and 0.83, respectively. 

The DFM ranks as the best model for just over half of the countries, with the model averages also generally ranking highly. Across all countries, the DFM ranks as the best forecasting model, followed by the simple average of the forecasts and the inverse-MSE-weighted average. It is noteworthy that the DFM generally outperforms the model combination methods presented here, given the relatively good performance of these types of forecasts shown in previous studies. 

Overall, our growth indicators generally show good forecasting performance relative to a range of models. This, combined with the usefulness of the indicators in describing the behavior of economic activity over history, makes them a useful tool for evaluating growth in real time. 

## **VI. REVISION PROPERTIES** 

In the previous section, we evaluated how well our growth indicators predict GDP growth in real time. It is also worthwhile to consider the revision properties of the monthly smoothed indicators discussed in section IV. Figure 3 displays the recursively estimated smoothed indicators (red), along with interpolated real GDP growth and the smoothed indicators estimated with all available data. For each country, the recursively estimated indicators are estimated using the data that would have been available at the beginning of every month of the out-of-sample period. The 7-month-moving averages are centered on the months in which the forecasts are made and implicity include forecasts. The deviations in the red lines from the blue lines represent the extent of the revisions to the real-time estimates of the smoothed indicators. As with figure 1, the dates beyond the collapse of Lehman Brothers near the beginning of the global financial crisis are shaded. 

> 12The results for the one-step-ahead forecasts are qualitatively very similar to the nowcasting results, and are available from the author on request. 

17 

Figure 3. Interpolated GDP growth and smoothed indicators in real time (% at an annual rate) 

**==> picture [421 x 592] intentionally omitted <==**

**----- Start of picture text -----**<br>
United States Canada Mexico Brazil<br>5 5 10<br>0<br>0 0 0<br>−10<br>−5 −5 −10<br>−20<br>2002:01 2007:01 2002:01 2007:01 2002:01 2007:01 2002:01 2007:01<br>Argentina Chile Columbia Peru<br>10<br>10 10<br>10 5<br>5 5<br>5 0<br>0 0<br>0 −5 −5 −5<br>2002:01 2007:01 2002:01 2007:01 2002:01 2007:01 2002:01 2007:01<br>Ecuador Venezuela Domenican Republic Uruguay<br>15 20 15<br>15<br>10 10<br>10 10<br>5 5<br>5<br>0 0 0 0<br>−5 −5 −5<br>−10<br>2002:01 2007:01 2002:01 2007:01 2002:01 2007:01 2002:01 2007:01<br>Japan Australia Korea China<br>5 6 10<br>4 15<br>0<br>−5 2 0 10<br>−10 0 −10<br>−15 −2 5<br>2002:01 2007:01 2002:01 2007:01 2002:01 2007:01 2002:01 2007:01<br>Indonesia India Euro Area Germany<br>15 4 5<br>8 2<br>10 0 0<br>6<br>−2<br>4 5 −4 −5<br>2 0 −6−8 −10<br>2002:01 2007:01 2002:01 2007:01 2002:01 2007:01 2002:01 2007:01<br>France Italy United Kingdom Russia<br>4 4 10<br>2 0 2<br>0 0 0<br>−2 −5 −2 −10<br>−4 −10 −4−6 −20<br>−6<br>2002:01 2007:01 2002:01 2007:01 2002:01 2007:01 2002:01 2007:01<br>Turkey Sweden Spain Portugal<br>20 5 5 5<br>0 0 0 0<br>−5 −5 −5<br>−20<br>2002:01 2007:01 2002:01 2007:01 2002:01 2007:01 2002:01 2007:01<br>Greece South Africa Kazakhstan Saudi Arabia<br>10 5 10<br>20<br>5<br>0 5<br>0<br>0<br>−5<br>−20 0<br>2002:01 2007:01 2002:01 2007:01 2002:01 2007:01 2002:01 2007:01<br>**----- End of picture text -----**<br>


18 

Table 4. Forecast accuracy: Nowcast 

|||Table 4. Forecast accuracy: Nowcast|
|---|---|---|
|Country|AR(RMSE)|_RMSE relative to AR_<br>_Rank of forecasts according to RMSE_<br>DFM<br>BE<br>BV<br>BVAR<br>INVMSE<br>MEAN<br>AR<br>DFM<br>BE<br>BV<br>BVAR<br>INVMSE<br>MEAN|
|United States<br>Canada<br>Mexico<br>Brazil<br>Argentina<br>Chile<br>Columbia<br>Peru<br>Ecuador<br>Venezuela<br>Domenican Republic<br>Uruguay<br>Japan<br>Australia<br>Korea<br>China<br>Indonesia<br>India<br>Euro Area<br>Germany<br>France<br>Italy<br>United Kingdom<br>Russia<br>Turkey<br>Sweden<br>Spain<br>Portugal<br>Greece<br>South Africa<br>Kazakhstan<br>Saudi Arabia<br>Average|2.79<br>1.99<br>8.25<br>5.20<br>4.79<br>5.10<br>5.18<br>4.20<br>4.75<br>11.46<br>7.55<br>6.03<br>4.64<br>2.43<br>5.93<br>3.65<br>1.92<br>3.03<br>2.15<br>3.79<br>2.27<br>2.87<br>2.17<br>9.41<br>15.19<br>4.62<br>1.82<br>3.64<br>3.86<br>2.17<br>8.02<br>2.09|0.69<br>0.79<br>0.89<br>0.73<br>0.73<br>0.76<br>7<br>1<br>5<br>6<br>2<br>3<br>4<br>0.85<br>0.77<br>0.87<br>0.85<br>0.78<br>0.78<br>7<br>5<br>1<br>6<br>4<br>3<br>2<br>0.72<br>0.72<br>0.86<br>0.78<br>0.80<br>0.79<br>7<br>2<br>1<br>6<br>3<br>5<br>4<br>0.74<br>1.24<br>0.91<br>0.84<br>0.86<br>0.84<br>6<br>1<br>7<br>5<br>2<br>4<br>3<br>1.05<br>1.18<br>0.90<br>1.01<br>1.01<br>0.97<br>3<br>6<br>7<br>1<br>5<br>4<br>2<br>0.92<br>0.87<br>0.89<br>0.88<br>0.88<br>0.86<br>7<br>6<br>2<br>5<br>4<br>3<br>1<br>0.87<br>0.80<br>0.95<br>1.03<br>0.83<br>0.81<br>6<br>4<br>1<br>5<br>7<br>3<br>2<br>0.83<br>1.05<br>0.87<br>0.84<br>0.76<br>0.76<br>6<br>3<br>7<br>5<br>4<br>1<br>2<br>0.95<br>0.95<br>0.95<br>0.99<br>0.92<br>0.89<br>7<br>5<br>3<br>4<br>6<br>2<br>1<br>0.66<br>0.75<br>0.83<br>0.99<br>0.80<br>0.76<br>7<br>1<br>2<br>5<br>6<br>4<br>3<br>0.81<br>0.96<br>0.95<br>0.91<br>0.89<br>0.88<br>7<br>1<br>6<br>5<br>4<br>3<br>2<br>0.72<br>0.81<br>0.88<br>0.86<br>0.84<br>0.82<br>7<br>1<br>2<br>6<br>5<br>4<br>3<br>0.68<br>0.77<br>0.86<br>0.72<br>0.74<br>0.76<br>7<br>1<br>5<br>6<br>2<br>3<br>4<br>1.19<br>0.94<br>1.08<br>1.15<br>1.01<br>0.99<br>3<br>7<br>1<br>5<br>6<br>4<br>2<br>0.52<br>0.80<br>0.91<br>0.86<br>0.78<br>0.75<br>7<br>1<br>4<br>6<br>5<br>3<br>2<br>0.86<br>1.02<br>1.05<br>0.69<br>0.86<br>0.83<br>5<br>3<br>6<br>7<br>1<br>4<br>2<br>0.80<br>0.91<br>0.80<br>0.85<br>0.84<br>0.81<br>7<br>1<br>6<br>2<br>5<br>4<br>3<br>1.52<br>0.88<br>0.83<br>1.15<br>0.82<br>0.84<br>5<br>7<br>4<br>2<br>6<br>1<br>3<br>0.66<br>0.79<br>0.83<br>0.69<br>0.72<br>0.72<br>7<br>1<br>5<br>6<br>2<br>4<br>3<br>0.84<br>0.77<br>0.89<br>0.98<br>0.83<br>0.82<br>7<br>4<br>1<br>5<br>6<br>3<br>2<br>0.66<br>0.68<br>0.81<br>0.93<br>0.75<br>0.76<br>7<br>1<br>2<br>5<br>6<br>3<br>4<br>0.55<br>0.75<br>0.86<br>0.91<br>0.74<br>0.77<br>7<br>1<br>3<br>5<br>6<br>2<br>4<br>0.81<br>0.95<br>0.85<br>0.99<br>0.89<br>0.87<br>7<br>1<br>5<br>2<br>6<br>4<br>3<br>0.39<br>1.37<br>0.80<br>0.78<br>0.54<br>0.59<br>6<br>1<br>7<br>5<br>4<br>2<br>3<br>0.70<br>0.82<br>0.81<br>0.73<br>0.79<br>0.77<br>7<br>1<br>6<br>5<br>2<br>4<br>3<br>0.76<br>0.77<br>0.83<br>0.84<br>0.81<br>0.80<br>7<br>1<br>2<br>5<br>6<br>4<br>3<br>0.85<br>1.10<br>1.20<br>1.63<br>1.44<br>1.10<br>2<br>1<br>3<br>7<br>6<br>5<br>3<br>0.81<br>0.62<br>0.85<br>1.15<br>0.80<br>0.81<br>6<br>4<br>1<br>5<br>7<br>2<br>3<br>0.99<br>0.89<br>0.88<br>1.06<br>0.80<br>0.93<br>6<br>5<br>3<br>2<br>7<br>1<br>4<br>0.82<br>0.90<br>0.96<br>0.87<br>0.86<br>0.84<br>7<br>1<br>5<br>6<br>4<br>3<br>2<br>0.85<br>0.98<br>0.87<br>0.89<br>0.91<br>0.89<br>7<br>1<br>6<br>2<br>4<br>5<br>3<br>0.98<br>1.15<br>1.36<br>0.81<br>0.85<br>0.85<br>5<br>4<br>6<br>7<br>1<br>2<br>3<br>0.81<br>0.90<br>0.91<br>0.92<br>0.84<br>0.83<br>6.2<br>2.6<br>3.9<br>4.8<br>4.5<br>3.2<br>2.8|



For most countries, the revisions to the indicators are small relative to the variance of GDP, and they do not show a marked deterioration since the global financial crisis. However, the revisions to the indicators for some countries – particularly Australia, India and Saudi Arabia – are large and warrant further discussion. 

Recall that the relative forecasting performance of the DFM for Australia and India was not as good as for other countries. This accounts from some of the large revisions associated with these countries. But short sample periods and instabilities in the specifications of the DFM over time are perhaps more important. 

In each month of the out-of-sample period, all DFM parameters are re-selected on the basis of the criteria described in section II. In fact, we find that the specifications tend to change more for India and Saudi Arabia than for most other countries in the recursive experiment, introducing volatility into the estimates of the indicators. While the recursively estimated indicators for Australia are not subject to this small sample problem, a relatively low R-squared in explaining quarterly real GDP growth for an advanced economy of 58%, even after including 6 factors, suggests a relatively weak factor structure in the Australian data. 

Fortunately, the revision properties of the indicators seem to have improved over the past couple of years, suggesting that any inefficiencies in estimation seen over history may well become less important with time. 

19 

## **VII. CONCLUDING REMARKS** 

We developed monthly growth indicators for 32 advanced and emerging-market economies. For each country, the indicators were estimated using a dynamic factor model and a large number of economic time series. We find that our growth indicators did a good job at describing the business cycle, and they produced reliable short-term forecasts relative to a range of time series models in a simulated real-time forecasting experiment. The revision properties of the indicators were shown to be good for most of the countries and, for the countries where revisions were large historically, there was some evidence that the properties of the indicators may well improve with time. 

The indicators will be used to evaluate the state of the business cycle in the future, and it is hoped that applying the indicator in real time will prompt further refinements to the framework over time. The list of countries for which indicators are estimated is also likely to be expanded in the future. 

20 

## **REFERENCES** 

- Altissimo, Filippo, Riccardo Cristadoro, Mario Forni, Marco Lippi, and Giovanni Veronese, 2007, “New Eurocoin: Tracking Economic Growth in Real Time,” _Bank of Italy Working Papers_ , No. 631 (June). 

- Angelini, Elena, Jerome Henry, and Massimiliano Marcellino, 2006, “Interpolation and backdating with a large information set,” _Journal of Economic Dynamics and Control_ , Vol. 30, No. 12, pp. 2693-2724. 

- Baffigi, Alberto, Roberto Golinelli, and Giuseppe Parigi, 2004, “Bridge models to forecast the euro area GDP,” _International Journal of Forecasting_ , Vol. 20, pp. 447–460. 

- Bai, Jushan, and Serena Ng, 2002, “Determining the number of factors in approximate factor models,” _Econometrica_ , Vol. 70, No. 1, pp. 135–172. 

   - , and , 2007, “Determining the number of primitive shocks in factor models,” 

   - _Journal of Business and Economic Statistics_ , Vol. 25, No. 1, pp. 52-60. 

- Banbura, Marta, Domenico Giannone, and Lucrezia Reichlin, 2010, “Large Bayesian vector auto regressions,” _Journal of Applied Econometrics_ , Vol. 25, No. 1, pp. 71-92. 

- Barhoumi, Karim, Szilard Benk, Riccardo Cristadoro, Ard Den Reijer, Audrone Jakaitiene, Piotr Jelonek, Antonio Rua, Gerhard Runstler, Karsten Ruth, and Christophe Van Nieuwenhuyze, 2008, “Short-term forecasting of GDP using large monthly datasets: a pseudo real-time forecast evaluation exercise,” _European Central Bank Occasional Paper_ , No. 84. 

- Boragan, Aruoba S., and Francis X. Diebold, 2010, “Real-Time Macroeconomic Monitoring: Real Activity, Inflation, and Interactions,” _American Economic Review_ , Vol. 100, No. 2 (May), pp. 20-24. 

   - , , and Chiara Scotti, 2009, “Real-Time Measurement of Business 

   - Conditions,” _Journal of Business & Economic Statistics_ , Vol. 27, No. 4, pp. 417-427. 

- Camacho, Maximo, and Gabriel Perez-Quiros, 2010, “Introducing the euro-sting: Short-term indicator of euro area growth,” _Journal of Applied Econometrics_ , Vol. 25, No. 4, pp. 663-694. 

- Chow, Gregory C., and An loh Lin, 1971, “Best Linear Unbiased Interpolation, Distribution, and Extrapolation of Time Series by Related Series,” _Review of Economics and Statistics_ , Vol. 53, No. 4, pp. 372–375. 

- Doan, Tom, Richard Litterman, and Chris Sims, 1984, “Forecasting and conditional projections using realistic prior distributions,” _Econometric Reviews_ , Vol. 3, pp. 1-100. 

- Doz, Catherine, Domenico Giannone, and Lucrezia Reichlin, 2007, “A two-step estimator for large approximate dynamic factor models based on Kalman filtering,” Discussion paper 6043, Centre for Economic Policy Research (CEPR), ). 

21 

- Evans, Martin D. D., 2005, “Where Are We Now? Real-Time Estimates of the Macroeconomy,” _International Journal of Central Banking_ , Vol. 1, No. 2 (September). 

- Giannone, Domenico, Lucrezia Reichlin, and David Small, 2008, “Nowcasting: The real-time informational content of macroeconomic data,” _Journal of Monetary Economics_ , Vol. 55, No. 4, pp. 665 – 676. 

   - , , and Luca Sala, “Monetary policy in real time,” 2005, in Mark Gertler, and 

   - Kenneth Rogoff, eds., _NBER Macroeconomics Annual 2004_ , (Cambridge, Mass.: MIT Press). 

- Kitchen, John, and Ralph Monaco, 2003, “Real-time forecasting in practice: The U.S Treasury Staff’s real-time GDP forecast system,” _Business Economics_ , Vol. 38, pp. 10-28. 

- Litterman, Richard, 1986, “Forecasting with Bayesian Vector Autoregressions - Five Years of Experience,” _Journal of Business and Economic Statistics_ , Vol. 4, pp. 25-38. 

- Mariano, Roberto S., and Yasutomo Murasawa, 2003, “A new coincident index of business cycles based on monthly and quarterly series,” _Journal of Applied Econometrics_ , Vol. 18, No. 4, pp. 427-443. 

- Matheson, Troy D., 2010, “An analysis of the informational content of New Zealand data releases: The importance of business opinion surveys,” _Economic Modelling_ , Vol. 27, pp. 304-314. 

- Stock, James H., and Mark W. Watson, “New Indexes of Coincident and Leading Economic Indicators,” 1989, in “NBER Macroeconomics Annual 1989, Volume 4” NBER Chapters (National Bureau of Economic Research), pp. 351–409. 

   - , and , 2002, “Macroeconomic Forecasting Using Diffusion Indexes,” _Journal_ 

   - _of Business and Economic Statistics_ , Vol. 20, No. 2, pp. 147-62. 

22 

APPENDIX I 

## **APPENDIX I. DATA TRANSFORMATION** 

We apply the following to each country’s data set prior to estimation: 

1. Missing values within the sample are linearly interpolated. 

2. The seasonal series are adjusted using X11. 

3. Quarterly and annual series are interpolated to the monthly frequency using linear interpolation; the daily and weekly series are converted into monthly averages. 

4. Log quarterly differences are taken of the non-stationary series, ln( _xi,t_ ) _−_ ln( _xi,t−_ 3), except those that are measured in percentages or can take negative values, in which case quarterly differences are taken, _xi,t − xi,t−_ 3. The remaining series are left as levels. 

5. The series that only change 10 percent of the time are discarded. 

6. The series with less than 3 years worth of data are discarded. 

7. The series not released in the past year are discarded (to avoid discontinued data). 

8. Outliers are removed, where observations greater/less than 6 times the interquintile range are replaced with the next highest/lowest admissible value. 

9. Missing observations at the beginning of the sample are backdated using the DFM, with the number factors set to explain 60 percent of the variation in the data. 


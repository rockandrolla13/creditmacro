_October 13, 2017 05:33 PM GMT_ 

## **Morgan Stanley Resi Credit Insights** 

## MODs: Machine Learning on Drivers 

|QUANTWI~~SE~~<br>[~~EA~~]||
|---|---|
|MORGAN STANLEY & CO. LLC<br>Jeen Ng||
|STRATEGIST||
|Jeen.Ng@morganstanley.com<br>James Egan<br>STRATEGIST|+1 212 296-8773|
|James.F.Egan@MorganStanley.com<br>Vishwanath Tirupattur|+1 212 761-4715|
|STRATEGIST||
|Vishwanath.Tirupattur@morganstanley.com|+1 212 761-1043|



Given how pervasive loan modifications are in legacy nonagency RMBS pools, understanding the factors that determine their performance is crucial in evaluating relative value. We apply machine learning techniques to determine the features that drive re-defaults in modifications over time. 

**Prevalence of modifications:** It has been almost a decade since modifications entered the vocabulary of the legacy non-agency market and, over that time, their share has grown steadily from 6% in January 2009 to 54% today. While modified loans make up 68% of Subprime and 52% of Option ARM deals, they also make up a growing proportion of Alt-A and Prime Jumbo pools. 

- **Constants and change:** There have been significant changes in the broader macroeconomic environment since modifications first started becoming more prevalent; coincidentally, we have seen shifts in the importance of different features that determine post-modification performance within legacy nonagency pools. 

- **What matters more?** Features measured at the time of modification are more important than those measured at loan origination. While borrowers' credit scores are still indicative, the percentage by which the payment is changed upon modification is the most informative feature, and its importance has remained stable over time. 

**What changes?** Bucketing the modification data by the year they were implemented, we observe that features such as MTMLTV, loan factor at modification, changes from original LTV, original FICO and geography have become progressively less important while other features such as the number of months spent in delinquency prior to modification and rate incentive upon modification have become more important. 

**Application of predictive model algorithms:** Among the tested models we have, regularized logistic models and linear discriminant analysis have the lowest predictive power. Performance improves as we move on to more complex models such as multi-layer neural networks, gradient boosting and random forest. Aggregating these individuals learners with a combiner algorithm, we can further improve the performance in both absolute and stability terms. 

QuantWise highlights research that incorporates a robust quantitative approach in our investment analysis. Due to the nature of the fixed income market, the issuers or bonds of the issuers recommended or discussed in this report may not be continuously followed. Accordingly, investors must regard this report as providing stand-alone analysis and should not expect continuing analysis or additional reports relating to such issuers or bonds of the issuers. 

Morgan Stanley does and seeks to do business with companies covered in Morgan Stanley Research. As a result, investors should be aware that the firm may have a conflict of interest that could affect the objectivity of Morgan Stanley Research. Investors should consider Morgan Stanley Research as only a single factor in making their investment decision. 

For analyst certification and other important disclosures, refer to the Disclosure Section, located at the end of this report. 

1 

## Mental mastication of modifications 

The long and storied history of negative net issuance in the non-agency RMBS universe has been a pervasive technical tailwind for the market. In addition to creating an environment where there has been more money looking to reinvest in fewer and fewer bonds each month, this dynamic has left the legacy resi credit market with a large concentration of modified loans. In fact, the share of modifications as a percentage of outstanding unpaid principal balance (UPB) has grown from **6% in January 2009 to 54% today** (Exhibit 1). It is no exaggeration to say that the performance of modified loans and therefore understanding the factors that determine their performance is probably among the most important (if not the most important) determinants of relative value in legacy non-agency RMBS deals. 

While modifications are more prevalent in Subprime and Option ARM deals – where they make up 68% and 52% of the outstanding balance of the market, respectively – they also make up a growing proportion of Alt-A and Prime Jumbo pools. Today almost one in three Prime Jumbo loans originated between 2004 and 2007 has been modified at least once (Exhibit 2). The incidence rate of higher-iteration modifications is increasing as well, with over half of all modifications completed so far this year being the second, third or even fourth+ modification on that particular mortgage (Exhibit 3). 

**Exhibit 1:** Breakdown of legacy resi credit by modification status 

**Exhibit 2:** % of modification loans by collateral type 

**==> picture [492 x 143] intentionally omitted <==**

**----- Start of picture text -----**<br>
1800 Le Non Modified | 1st Mod 60% —_ Alt-A —_ Subprime<br>1600 Le 2nd Mod Le 3+ Mod 80% — Prime Jumbo — Option Arm<br>Mod (%, RHS) 50% 70%<br>1400<br>60%<br>1200 40%<br>50%<br>1000<br>30% 40%<br>800<br>600 20% 30%<br>400 20%<br>10%<br>200 10%<br>0 0% 0%<br>eS Serv PrP Vv © Ss PF SP SKY Dr PK KP VP KS<br>Fe oe eK we F FV SS we Fe ow & we F FV & S<br>Source: Loan Performance, Morgan Stanley Research Source: Loan Performance, Morgan Stanley Research<br>Legacy Universe ($bn) % of Modified Loans (%)<br>**----- End of picture text -----**<br>


**==> picture [124 x 7] intentionally omitted <==**

**----- Start of picture text -----**<br>
Source: Loan Performance, Morgan Stanley Research<br>**----- End of picture text -----**<br>


As modifications become a growing proportion of the outstanding population, it should come as no surprise that they are becoming a larger share of monthly default and prepayment volumes. This past month, re-defaulted modifications accounted for 53% of all liquidations and, perhaps more surprisingly, 21% of all voluntary prepayments (Exhibit 4). 

This growing role that modifications play in monthly cash flows to non-agency trusts makes it imperative for investors to learn more about a mortgage's behavior postmodification. Modifications come in all shapes and sizes, but they are not all equally effective. 

2 

**Exhibit 3:** % of completed modifications over the past three years that are 1st, 2nd and 3+ modifications 

**Exhibit 4:** % of liquidations and voluntary prepayments that have been modifications 

**==> picture [190 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
100%<br>80%<br>60%<br>40%<br>20%<br>0%<br>Jan-14 Jan-15 Jan-16 Jan-17<br>| 3+ | 2nd | 1st<br>Source: Loan Performance, Morgan Stanley Research<br>**----- End of picture text -----**<br>


**==> picture [203 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>Jan-12 Jan-13 Jan-14 Jan-15 Jan-16 Jan-17<br>Liquidated Prepaid<br>**----- End of picture text -----**<br>


Source: Loan Performance, Morgan Stanley Research 

Additionally, and perhaps more importantly, modification rates began picking up in earnest in 2010 in what was a very different economic environment to today (Exhibit 5). Home prices had yet to hit rock bottom and the national unemployment rate was more than double where it stands as of right now (Exhibit 6). Therefore, it follows that what drove performance (or led to re-defaults) four or five years ago is different than what drives post-modification performance today. The question really is what characteristics have become more or less influential in determining post-modification performance of these loans and which factors remain as important as they have been. 

**Exhibit 5:** Number of modifications and modification rate by month or year 

**Exhibit 6:** HPA and the unemployment rate 

**==> picture [493 x 195] intentionally omitted <==**

**----- Start of picture text -----**<br>
Unemployment Rate (%)<br>12.0% 250<br>4% 70 Case Shiller HPI (NSA)<br>60 10.0% 200<br>3%<br>50<br>8.0%<br>150<br>40<br>2% 6.0%<br>30<br>100<br>4.0%<br>20<br>1%<br>10 2.0% 50<br>0% 0<br>eo Sy XT VP - Y © 0.0% 0<br>Ss x Number of Mod ('000) SS SK KK S K Mod Rate (%) aeoeOR ee<br>Source: Case Shiller, Bureau of Labor Statistics, Morgan Stanley Research<br>Modification Rate (%)<br>Number of Modifications ('000)<br>**----- End of picture text -----**<br>


Source: Loan Performance, Morgan Stanley Research 

In this report, we leverage techniques developed within the machine learning space to take a deep dive into the drivers behind re-default rates in modified loans and identify which features have become more or less important over time. In our view, this analysis provides a key insight into evaluating the relative value across the legacy non-agency RMBS universe, given the importance of the performance of modified loans. 

3 

## How do we start? Laying out the framework 

## **Framework set-up/objective** 

For the purpose of this report, our scope of analysis includes only Subprime loans originated between 2004 and 2007 that were modified between January 2012 and June 2016. Our objective is to determine the main attributes responsible for re-performing loans defaulting (defined as 90+ delinquent/re-modified) within the first 12 months post modification. 

For ease of understanding our analytical approach, we explain the subsequent sections in the same order as the following machine learning roadmap. 

Roadmap of building machine learning systems 

Python Machine Learning, Sebastian Raschika 

## **Data preprocessing** 

First, we create an initial set of attributes and categorize them into smaller subgroups: 

- **Property type:** Single Family Residence (SFR), Planned Unit Development (PUD), Manufactured Housing, Condominium, Town House, 2 - 4 Units Housing, Other 

- **Occupancy:** Owner Occupied, Investor Occupied, Other 

- **Loan product:** Fixed, ARM, Other 

- **Loan purpose:** Purchase, Cash Out Refinance, Noncash Out Refinance, Other 

- **Other loan properties:** Term, Closing Rate, Fixed/Floating, Rate Incentive at origination (Initial Rate - Mortgage Rate at origination), First Lien, Penalty Term, PMI status (mortgage insurance), Full Documentation, Origination Amount, Ratio of Closing Value to Origination Amount 

4 

- **Geography:** Northeast, Midwest, South, West, Other NAR, Judicial/Non Judicial 

- **Borrower credit characteristic:** Original LTV, Original DTI, Original FICO, Mark-tomarket LTV (MTMLTV), Vantage Score at Modification, Beacon Score at Modification, Income at Modification, Change from Original LTV at Modification 

- **Loan properties at modification:** Loan Balance, Loss To-date, Delinquency Timeline, Loan Seasoning, Previous Loan Balance 

- **Modification characteristics:** Rate Modification, Loss Modification, Balance Up Modification, Balance Down Modification, Modification Iteration, Change in Payment, Loan Factor at Modification, Rate Incentive at Modification, Change in Rate Incentive, Modified within Prior 6 months, Modified within Prior 12 months. 

- **Regional characteristics:** County Level Unemployment rate, County Level Unemployment rate MoM, County Level Unemployment YoY 

- **Servicer characteristics:** Servicer, Change from Servicer at Origination, % of serviceable months being serviced (over last 12 months), % of serviceable months being serviced (over last 24 months) 

Next, we implement feature selection algorithms to identify attributes that are more influential in predicting modified loans' default probability. 

## **Feature selection** 

Feature selection is an integral part of machine learning preprocessing as it often helps to (1) simplify models to make them more interpretable, (2) shorten training times, (3) avoid the curse of dimensionality – where feature relation breaks down in a highdimensional space, and (4) improve generalizability of the model. 

Within feature selection, there are three main methods that are commonly used: 

- **Filter method:** Uses a proxy measure to assess the importance of features from the data. This method ignores the interaction with the classifier and all features are considered separately, thereby ignoring feature dependencies. Relative to the wrapper method below, it is easily scaled to high-dimensional datasets, more computationally simple and efficient, doesn’t contain assumptions of a prediction model and is more useful to rank individual features. 

- **Wrapper method:** Uses a predictive model to score each possible combination of feature subsets. It usually produces the best feature set but it is very computationally intensive. 

- **Embedded method:** Perform variable selection as part of the learning algorithm and is usually specific to a given machine learning technique (e.g., lasso, decision tree). 

Given the number of features (>65) and data points (>700K) we have, we use the filter method as an initial screening process prior to training our model. 

5 

## **Feature analysis – filter method** 

The three proxies we are using to evaluate the importance of individual features are: (1) Information gain, (2) Gain ratio and (3) Chi-square. We explain each of the metrics in the following subsection (a more visual explanation of each metric is in Appendix III: Visual explanations of machine learning terminologies): 

## **Information gain** 

A good classification model splits data samples into groups of asymmetrical data subsets. The better the model, the lower the entropy (a measure of data symmetry). Information gain measures the reduction of entropy caused by the inclusion of the additional feature. 

## **Gain ratio** 

One shortcoming of using the information gain metric is that it is biased towards multivalued attributes, resulting in an over-fitted model. Gain ratio (defined as ratio of information gain to intrinsic information) is often used to reduce the bias by taking the number and size of branches into account when choosing an attribute. 

## **Chi-square** 

A chi-square test is used to examine the independence of two events (e.g. Event 1: Higher FICO distribution, Event 2: Lower default rate). Given a dataset about two events, we can get the observed count (O) and the expected count (E). The chi-square score measures the deviation between these two counts. If the events are independent, the deviation between the two counts will be small. Likewise, if the feature is important, the expected value and the observed value conditioning on the new feature will be very different. 

6 

## Which features matter? 

In this analysis, we incorporate insights from all three metrics to reduce the likelihood of the analysis being distorted by one particular biased metric. For instance. we see that information gain metrics tend to favor features with continuous values (e.g. payment change, rate incentive at modification) while gain ratio metrics reduce that bias, placing more weight on attributes with less discrete values (e.g. loss modification, modification iteration). Having the same feature score low across all three metrics provides us with more conviction that the feature is indeed irrelevant. 

**Exhibit 7:** Feature importance – scaled information gain, scaled gain ratio, scaled chi-square 

Source: Loan Performance, Morgan Stanley Research; *Note: A bigger, clearer version is available in Appendix III: Visual explanations of machine learning terminologies. 

Exhibit 7 shows the scaled feature importance score for each individual attribute across all three metrics in descending order. There are a few interesting observations worth highlighting: 

- In general, features measured upon modification have more implications for default likelihood than features measured at origination. This makes sense as origination data are more dated and therefore could be less of an effective indicator of postmodification performance. 

While borrowers' credit scores are still indicative, other attributes such as 

7 

percentage of payment change, rate incentive upon modification, modification iteration, loss amount to date, or the presence of a principal modification are ranked higher. 

- Features such as loan purpose, housing type, or the identity of the servicer provide us with less information on modified loans' propensity to re-default. 

In Exhibit 8, we illustrate the difference in classification ability (degree of outcome separability) between higher-ranked features and lower-ranked features. For example, the top left chart shows the density distribution across percentage payment change by default outcome. We can see that once the payment percentage decrease is more than 10%, the probability of not defaulting increases. On the other hand, if we look at origination balance (top right), the density distribution for both default classes almost overlap with one another, making the feature less relevant. 

A similar argument can be made for discrete independent variables. If a loan receives a principal modification (bottom-left chart, higher-ranked variable), the chance of it going delinquent increases from 60% to 78%. Meanwhile, lower-ranked discrete features such as purchase mortgages have almost no effect on the final outcome. 

**Exhibit 8:** Comparison between a higher-ranked feature and a lower-ranked feature 

Source: Loan Performance, Morgan Stanley Research 

8 

## Correlation test 

In addition to identifying irrelevant features, attributes can also be redundant if they are strongly correlated with other attributes and can be removed without incurring much loss of information. In Exhibit 9, we plot the correlation between each feature pair, and the strength of correlation is proportional to the intensity of the color (dark blue: high positive correlation, dark red: high negative correlation, white: uncorrelated). 

**Exhibit 9:** Correlation plot between feature pair 

Source: Loan Performance, Morgan Stanley Research 

For convenience, we arrange features that are strongly correlated with one another in clusters. For example, we have clusters of features that represent loan size (current loan balance, previous loan balance), loan-to-value (MTMLTV, LTV at origination) and loan type (fixed rate, product – fixed). The removal of these features can make the training phase more computationally efficient and the model performance more stable. 

9 

## Feature analysis over time 

One criticism of machine learning is that the models are only as good as the data you feed them. Indeed, non-stationarity within the data will lead to model performance decay. Therefore, we want to analyze whether the attributes we identified as relevant are important throughout the passage of time. Our next step involves breaking the same modification data we have into their respective modification vintage year and repeating the analysis. 

**Exhibit 10:** Feature importance – scaled information gain, scaled gain ratio, scaled chi-square by modification year 

|**FeatureName**<br>~~SS~~|**Scaled Information Gain**<br>~~————~~|**Scaled Gain Ratio**|**Scaled Chi Square**|
|---|---|---|---|
||**2012**<br>**2013**<br>**2014**<br>**2015**<br>**2016**<br>~~————~~|**2012**<br>**2013**<br>**2014**<br>**2015**<br>**2016**|**2012**<br>**2013**<br>**2014**<br>**2015**<br>**2016**|
|Payment Chg (M)<br>Mod Loan Factor (M)<br>Mod Rate Incentive (M)<br>Mod Iteration (M)<br>MTMLTV (M)<br>Beacon (M)<br>Chg LTV (M)<br>Loss Mod (M)<br>Balance Down Mod (M)<br>Vantage (M)<br>Loss To-date (M)<br>DTI (M)<br>Servicing % - Last 24 mths (M)<br>Servicing % - Last 12 mths (M)<br>Adj. Rate Incentive (M)<br>Servicer - Ocwen (M)<br>FICO (O)<br>Income (M)<br>Servicer - American Housing (M)<br>Prev Balance (M)<br>Loan Balance (M)<br>Delinq Timeline (M)<br>Init Rate Incentive (O)<br>Last Mod withn 12 mths (M)<br>No PMI (O)<br>Closing Rate (O)<br>Servicer - Litton (M)<br>Last Mod withn 6 mths (M)<br>Product - ARM (O)<br>West (O)<br>Orig DTI (O)<br>Full Doc (O)<br>Fixed Rate (O)<br>Servicer - JP Morgan (M)<br>Penalty (O)<br>Chg Serv (M)<br>Seasoning (M)<br>Product - Other (O)<br>Orig Amt (O)<br>Close Value To Orig Amt (O)<br>Northeast (O)<br>County Unemployment rate YoY (M)<br>Servicer - Nationstar (M)<br>Term (O)<br>Servicer - Wells Fargo (M)<br>Product - Fixed (O)<br>Servicer - Bank of America (M)<br>Judicial State (O)<br>Orig LTV (O)<br>2 - 4 Units (O)<br>Condo (O)<br>County Unemployment rate (M)<br>SFR (O)<br>Purpose - Refi Cashout (O)<br>Purpose - Purchase (O)<br>South (O)<br>First Lien (O)<br>Midwest (O)<br>Owner Occ (O)<br>Investor Occ (O)<br>Manufactured Housing (O)<br>Balance Up Mod (M)<br>PUD (O)<br>Purpose - Other (O)<br>Town House (O)<br>Purpose - Refi Cashout (O)<br>Single Units (O)<br>Other Occ (O)<br>Other Property (O)<br>County Unemployment rate MoM (M)<br>~~SS ~~|20.3%<br>18.1%<br>22.7%<br>27.7%<br>26.1%<br>10.3%<br>9.0%<br>5.6%<br>0.8%<br>0.5%<br>6.0%<br>5.9%<br>8.6%<br>23.1%<br>22.3%<br>5.4%<br>5.4%<br>6.8%<br>5.0%<br>4.8%<br>5.2%<br>5.3%<br>3.2%<br>0.5%<br>0.1%<br>5.2%<br>5.7%<br>5.1%<br>1.1%<br>0.7%<br>5.1%<br>4.8%<br>3.2%<br>0.5%<br>0.0%<br>4.9%<br>5.4%<br>7.8%<br>9.4%<br>7.6%<br>4.2%<br>2.9%<br>4.4%<br>5.4%<br>3.6%<br>4.2%<br>6.2%<br>6.4%<br>1.3%<br>0.7%<br>3.9%<br>2.7%<br>5.0%<br>5.4%<br>4.5%<br>3.6%<br>2.9%<br>2.0%<br>0.9%<br>1.3%<br>2.0%<br>3.4%<br>4.3%<br>2.2%<br>2.5%<br>2.0%<br>3.7%<br>4.1%<br>2.5%<br>2.8%<br>1.9%<br>1.5%<br>0.7%<br>0.9%<br>1.3%<br>1.7%<br>0.2%<br>0.0%<br>0.4%<br>0.2%<br>1.6%<br>2.2%<br>1.4%<br>0.1%<br>0.0%<br>1.3%<br>1.4%<br>1.0%<br>0.1%<br>0.0%<br>1.0%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.9%<br>0.6%<br>0.5%<br>0.6%<br>0.4%<br>0.9%<br>0.6%<br>0.5%<br>0.6%<br>0.4%<br>0.9%<br>2.3%<br>1.0%<br>4.6%<br>5.2%<br>0.7%<br>1.4%<br>0.8%<br>0.2%<br>0.6%<br>0.6%<br>0.2%<br>0.9%<br>0.1%<br>4.3%<br>0.6%<br>0.1%<br>0.0%<br>0.1%<br>0.1%<br>0.6%<br>1.3%<br>0.7%<br>0.0%<br>0.6%<br>0.6%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.4%<br>0.6%<br>0.1%<br>0.2%<br>0.1%<br>0.4%<br>0.4%<br>0.3%<br>0.2%<br>0.3%<br>0.4%<br>0.8%<br>0.2%<br>0.1%<br>0.1%<br>0.3%<br>0.2%<br>0.1%<br>0.1%<br>0.1%<br>0.2%<br>0.3%<br>0.0%<br>0.0%<br>0.1%<br>0.2%<br>0.4%<br>0.2%<br>0.3%<br>0.5%<br>0.2%<br>0.1%<br>0.1%<br>0.1%<br>0.2%<br>0.2%<br>0.2%<br>0.1%<br>0.1%<br>0.1%<br>0.2%<br>0.0%<br>0.0%<br>0.1%<br>0.1%<br>0.2%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.2%<br>0.0%<br>0.1%<br>0.0%<br>0.0%<br>0.2%<br>0.3%<br>0.0%<br>0.4%<br>0.6%<br>0.2%<br>0.3%<br>0.3%<br>0.2%<br>0.5%<br>0.1%<br>0.2%<br>0.0%<br>0.0%<br>0.0%<br>0.1%<br>0.4%<br>0.0%<br>0.0%<br>0.1%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.1%<br>0.1%<br>0.4%<br>0.1%<br>0.1%<br>0.1%<br>0.5%<br>0.4%<br>0.0%<br>0.0%<br>0.1%<br>0.3%<br>0.1%<br>0.2%<br>0.3%<br>0.1%<br>0.1%<br>0.0%<br>0.0%<br>0.1%<br>0.1%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.1%<br>0.3%<br>0.1%<br>0.3%<br>0.2%<br>0.1%<br>0.1%<br>0.1%<br>0.0%<br>0.0%<br>0.1%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.1%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.1%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.2%<br>0.1%<br>0.1%<br>0.1%<br>0.0%<br>0.2%<br>0.1%<br>0.1%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.1%<br>0.0%<br>0.0%<br>0.1%<br>0.2%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.1%<br>0.0%<br>0.0%<br>0.2%<br>3.5%<br>5.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.1%<br>0.1%<br>0.0%<br>0.0%<br> ~~————~~<br>~~ee~~<br>~~— ~~<br>~~—-~~|7.9%<br>9.9%<br>11.1%<br>13.1%<br>10.9%<br>4.8%<br>6.1%<br>3.9%<br>0.6%<br>0.4%<br>3.2%<br>3.4%<br>5.2%<br>8.6%<br>10.1%<br>3.8%<br>4.4%<br>4.8%<br>4.7%<br>4.5%<br>2.6%<br>3.7%<br>2.7%<br>0.4%<br>0.4%<br>3.7%<br>3.6%<br>3.6%<br>1.0%<br>0.5%<br>2.6%<br>3.4%<br>2.2%<br>0.6%<br>0.0%<br>7.7%<br>10.1%<br>13.7%<br>18.7%<br>15.9%<br>6.9%<br>5.6%<br>8.3%<br>12.0%<br>8.6%<br>2.0%<br>4.2%<br>4.5%<br>1.0%<br>0.6%<br>3.1%<br>2.4%<br>4.0%<br>3.7%<br>2.7%<br>1.8%<br>2.2%<br>1.6%<br>0.6%<br>0.9%<br>1.2%<br>2.4%<br>2.9%<br>3.1%<br>2.2%<br>1.3%<br>2.9%<br>3.3%<br>3.4%<br>2.6%<br>1.3%<br>1.4%<br>0.9%<br>0.8%<br>1.0%<br>3.3%<br>0.3%<br>0.1%<br>0.6%<br>0.3%<br>1.1%<br>1.7%<br>1.2%<br>0.2%<br>0.0%<br>0.8%<br>1.3%<br>0.9%<br>0.2%<br>0.1%<br>4.0%<br>0.4%<br>0.2%<br>0.3%<br>0.4%<br>0.7%<br>0.6%<br>0.6%<br>0.5%<br>0.3%<br>0.7%<br>0.6%<br>0.6%<br>0.5%<br>0.3%<br>0.8%<br>2.1%<br>0.8%<br>3.1%<br>4.0%<br>0.6%<br>1.1%<br>0.8%<br>1.3%<br>0.6%<br>1.4%<br>0.6%<br>2.5%<br>0.2%<br>7.6%<br>1.5%<br>0.2%<br>0.1%<br>0.2%<br>0.2%<br>0.5%<br>1.1%<br>0.7%<br>0.0%<br>1.5%<br>3.1%<br>3.4%<br>0.4%<br>1.4%<br>0.2%<br>1.1%<br>2.3%<br>0.3%<br>0.8%<br>0.6%<br>0.5%<br>0.8%<br>0.4%<br>0.3%<br>0.5%<br>0.6%<br>1.7%<br>0.5%<br>0.1%<br>0.2%<br>0.3%<br>0.2%<br>0.2%<br>0.1%<br>0.2%<br>0.4%<br>0.6%<br>0.0%<br>0.0%<br>0.2%<br>0.3%<br>0.8%<br>0.3%<br>0.5%<br>0.7%<br>1.0%<br>0.3%<br>0.6%<br>0.3%<br>0.9%<br>0.3%<br>0.5%<br>0.2%<br>0.1%<br>0.2%<br>0.3%<br>0.0%<br>0.0%<br>0.1%<br>0.2%<br>0.1%<br>0.4%<br>0.0%<br>0.0%<br>0.0%<br>0.3%<br>0.1%<br>0.1%<br>0.0%<br>0.0%<br>0.3%<br>0.5%<br>0.0%<br>0.4%<br>0.4%<br>0.3%<br>0.5%<br>0.5%<br>2.0%<br>1.8%<br>0.3%<br>0.6%<br>0.1%<br>0.0%<br>0.1%<br>0.1%<br>0.5%<br>0.0%<br>0.1%<br>0.1%<br>0.8%<br>0.0%<br>0.1%<br>0.1%<br>0.1%<br>0.3%<br>1.2%<br>2.5%<br>0.5%<br>1.4%<br>1.0%<br>3.6%<br>3.5%<br>0.1%<br>0.0%<br>0.2%<br>0.6%<br>0.2%<br>0.4%<br>0.4%<br>0.6%<br>0.3%<br>0.0%<br>0.1%<br>0.2%<br>0.1%<br>0.2%<br>0.0%<br>0.0%<br>0.0%<br>16.3%<br>0.4%<br>4.8%<br>0.2%<br>0.6%<br>0.3%<br>0.6%<br>0.5%<br>0.0%<br>0.1%<br>0.3%<br>0.4%<br>0.2%<br>0.0%<br>0.0%<br>0.1%<br>0.4%<br>0.1%<br>0.0%<br>0.0%<br>0.1%<br>0.1%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.4%<br>0.1%<br>0.1%<br>0.2%<br>0.0%<br>0.5%<br>0.2%<br>0.1%<br>0.2%<br>0.0%<br>0.1%<br>0.0%<br>0.1%<br>0.1%<br>0.1%<br>0.0%<br>0.5%<br>1.3%<br>0.5%<br>0.0%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.1%<br>0.1%<br>0.1%<br>0.7%<br>0.3%<br>0.1%<br>0.1%<br>0.1%<br>0.7%<br>0.3%<br>0.4%<br>0.0%<br>0.0%<br>1.0%<br>1.5%<br>0.0%<br>0.0%<br>0.4%<br>6.7%<br>8.4%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.3%<br>1.1%<br>0.0%<br>1.4%<br>2.5%<br>0.1%<br>0.2%<br>0.2%<br>0.0%<br>0.1%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.0%<br>0.1%<br>0.2%<br>0.0%<br>0.4%<br>1.1%<br>0.1%<br>0.2%<br>0.0%<br>0.1%<br>0.0%<br>0.4%<br>0.0%<br>0.0%<br>0.4%<br>0.1%<br>0.1%<br>0.1%<br>~~eee~~<br> ~~i~~<br>~~—-~~|8.0%<br>7.4%<br>9.3%<br>11.2%<br>10.4%<br>5.7%<br>5.3%<br>4.6%<br>2.0%<br>1.5%<br>4.3%<br>4.2%<br>5.7%<br>10.3%<br>9.6%<br>4.2%<br>4.1%<br>5.0%<br>4.7%<br>4.5%<br>4.0%<br>4.0%<br>3.5%<br>1.6%<br>0.8%<br>4.1%<br>4.2%<br>4.4%<br>2.3%<br>1.8%<br>4.0%<br>3.8%<br>3.5%<br>1.6%<br>0.0%<br>3.8%<br>4.0%<br>5.2%<br>6.5%<br>5.6%<br>3.5%<br>2.9%<br>3.9%<br>4.9%<br>3.9%<br>3.6%<br>4.4%<br>4.9%<br>2.4%<br>1.7%<br>3.4%<br>2.8%<br>4.3%<br>5.0%<br>4.4%<br>3.3%<br>3.0%<br>2.7%<br>2.0%<br>2.4%<br>2.6%<br>3.3%<br>4.1%<br>3.2%<br>3.3%<br>2.5%<br>3.5%<br>4.0%<br>3.4%<br>3.5%<br>2.4%<br>2.1%<br>1.6%<br>2.1%<br>2.4%<br>2.3%<br>0.7%<br>0.3%<br>1.3%<br>1.0%<br>2.2%<br>2.5%<br>2.3%<br>0.7%<br>0.0%<br>2.0%<br>2.1%<br>2.0%<br>0.7%<br>0.5%<br>1.8%<br>0.5%<br>0.1%<br>0.1%<br>0.1%<br>1.7%<br>1.3%<br>1.3%<br>1.7%<br>1.2%<br>1.7%<br>1.3%<br>1.3%<br>1.7%<br>1.2%<br>1.6%<br>2.6%<br>2.0%<br>4.6%<br>4.7%<br>1.5%<br>2.0%<br>1.7%<br>1.0%<br>1.6%<br>1.4%<br>0.8%<br>1.8%<br>0.5%<br>4.3%<br>1.4%<br>0.4%<br>0.3%<br>0.6%<br>0.6%<br>1.4%<br>1.9%<br>1.6%<br>0.0%<br>1.5%<br>1.3%<br>0.5%<br>0.1%<br>0.3%<br>0.1%<br>1.1%<br>1.3%<br>0.5%<br>0.8%<br>0.8%<br>1.1%<br>1.1%<br>1.0%<br>0.9%<br>1.2%<br>1.1%<br>1.5%<br>0.9%<br>0.5%<br>0.6%<br>1.2%<br>1.0%<br>0.8%<br>0.8%<br>0.9%<br>0.8%<br>0.9%<br>0.3%<br>0.3%<br>0.7%<br>0.8%<br>1.1%<br>0.8%<br>1.2%<br>1.4%<br>0.8%<br>0.5%<br>0.7%<br>0.6%<br>1.0%<br>0.7%<br>0.8%<br>0.6%<br>0.5%<br>0.7%<br>0.7%<br>0.0%<br>0.2%<br>0.5%<br>0.7%<br>0.7%<br>0.6%<br>0.0%<br>0.0%<br>0.0%<br>0.7%<br>0.4%<br>0.5%<br>0.2%<br>0.1%<br>0.7%<br>0.9%<br>0.0%<br>1.4%<br>1.6%<br>0.7%<br>1.0%<br>1.1%<br>1.0%<br>1.5%<br>0.7%<br>0.8%<br>0.4%<br>0.2%<br>0.4%<br>0.7%<br>1.1%<br>0.0%<br>0.4%<br>0.6%<br>0.6%<br>0.0%<br>0.4%<br>0.3%<br>0.3%<br>0.6%<br>0.6%<br>1.2%<br>0.6%<br>0.6%<br>0.5%<br>1.2%<br>1.2%<br>0.2%<br>0.1%<br>0.5%<br>0.9%<br>0.6%<br>1.0%<br>1.1%<br>0.5%<br>0.6%<br>0.2%<br>0.4%<br>0.6%<br>0.5%<br>0.6%<br>0.0%<br>0.0%<br>0.0%<br>0.5%<br>0.9%<br>0.5%<br>1.1%<br>0.8%<br>0.4%<br>0.6%<br>0.6%<br>0.0%<br>0.3%<br>0.4%<br>0.4%<br>0.3%<br>0.2%<br>0.0%<br>0.3%<br>0.6%<br>0.5%<br>0.0%<br>0.0%<br>0.3%<br>0.4%<br>0.5%<br>0.3%<br>0.2%<br>0.3%<br>0.8%<br>0.5%<br>0.6%<br>0.7%<br>0.3%<br>0.8%<br>0.6%<br>0.5%<br>0.6%<br>0.2%<br>0.4%<br>0.2%<br>0.5%<br>0.6%<br>0.2%<br>0.0%<br>0.6%<br>0.9%<br>0.6%<br>0.2%<br>0.3%<br>0.2%<br>0.2%<br>0.3%<br>0.2%<br>0.2%<br>0.2%<br>0.6%<br>0.4%<br>0.2%<br>0.2%<br>0.2%<br>0.6%<br>0.4%<br>0.2%<br>0.0%<br>0.0%<br>0.4%<br>0.5%<br>0.1%<br>0.1%<br>0.9%<br>4.0%<br>4.6%<br>0.1%<br>0.1%<br>0.0%<br>0.1%<br>0.1%<br>0.1%<br>0.2%<br>0.0%<br>0.4%<br>0.6%<br>0.1%<br>0.1%<br>0.2%<br>0.0%<br>0.1%<br>0.0%<br>0.0%<br>0.1%<br>0.1%<br>0.0%<br>0.0%<br>0.2%<br>0.1%<br>0.4%<br>0.6%<br>0.0%<br>0.1%<br>0.2%<br>0.1%<br>0.1%<br>0.0%<br>0.1%<br>0.0%<br>0.2%<br>0.0%<br>0.0%<br>0.5%<br>0.5%<br>0.5%<br>0.5%<br>~~LS~~|



A few interesting observations can be made from Exhibit 10: 

For most features, their relative importance/rankings remain stable over time (e.g., percentage payment change upon modification remains the most informative feature across vintages). 

As we move into the recent cohorts, features such as MTMLTV, loan factor at 

10 

modification, and change from original LTV become less relevant. One possible explanation is that most modified loans from recent cohorts have a higher chance of being above water than the more seasoned ones. Since January 2009, the share of modified loans with MTMLTV post-modification below 100% has grown from 55% to 90% today. Once the borrowers enter positive home equity territory, the effect on them going delinquent become less distinguishable. 

## Features trending less important 

The number of months spent in the delinquency queue prior to modification, presence of balance down/up modification and rate incentive (mortgage rate - prevailing 30-year mortgage rate) upon modification have become increasingly important in predicting modified borrowers' ability to repay. Exhibit 11 and Exhibit 12 show the difference in default distribution by balance up modification status from 2012 and 2015. 

## Features trending more important 

We also identified other fallen angels (features) such as original FICO and NAR geographical location that have seen their relevance trend lower over time. 

**Exhibit 11:** Default distribution by balance up modification status (2012) 

**Exhibit 12:** Default distribution by balance up modification status (2015) 

**==> picture [523 x 143] intentionally omitted <==**

**----- Start of picture text -----**<br>
80% No Balance Up Mod 80% No Balance Up Mod<br>69% 69% Balance Up Mod 71% Balance Up Mod<br>60% 60%<br>53%<br>47%<br>40% 40%<br>31% 31% 29%<br>20% 20%<br>0% ea da 0%<br>% Not Default % Default % Not Default % Default<br>Source: Loan Performance, Morgan Stanley Research Source: Loan Performance, Morgan Stanley Research<br>**----- End of picture text -----**<br>


As modifications become a more pervasive part of the non-agency universe, it is important to understand what characteristics leave a particular modification more or less susceptible to default, and how these characteristics have changed over time. Some modification characteristics – such as the percentage by which a borrower's payment is 

11 

reduced – have remained of paramount importance throught the years. Others such as loan factor upon modification and MTMLTV have become less important while delinquency timeline and balance up modification have become more important. If we look at the borrower being modified instead of the modification itself, characteristics such as their FICO score no longer matter as much as they used to, but the length of time they have been delinquent before being modified has taken on an ever more important role. 

In Appendix IV - Machine learning algorithms, we illustrate various machine learning algorithms that can take the variables we've identified in this report, and in Appendix II: Model performance evaluation results, we project default rates on various pools of modifications. While data limitations currently leave us focusing on modifications within the legacy non-agency universe, we hope to be able to extend this analysis to other reperforming loan pools and deals in the future. 

12 

## Appendix I: Applications of predictive model algorithms 

Roadmap of building machine learning systems 

Python Machine Learning, Sebastian Raschika 

Based on the results we gathered from our feature selection methods and correlation tests, we reduced the number of features from 72 to 35. Our next step involves feeding the preprocessed data we have into various machine learning algorithms to evaluate the best prediction models for the datasets we have. 

Within the supervised learning (labeled outcome) branch of the machine learning space, there are various prediction models being used in performing regression/classification tasks. For example, we have linear based models (e.g., linear regression), tree-based models, support vector machines, multi-layer neural networks and linear discriminant analysis. Each algorithm has its own merits and limitations and its performance is dependent on the inherent structures within the data distribution. The objective of the machine learning process is to choose the most suitable learner to provide us with the best trade-off between bias (ability to learn from the given data – low in-sampling error) and variance (ability to generalize over unseen data points – low out-sampling error). 

In this exercise, the algorithms that we use are (1) Regularized Logistic Regression, (2) Gradient Boosting, (3) Random Forest, (4) Linear Discriminant Analysis, (5) Multi-layer Neural Network (Deep Learning), and (6) Ensemble Learning (Stacking); see Appendix IV - Machine learning algorithms. Each algorithm's hyper-parameters (e.g. depth of decision trees, size of penalty term in regularized model) are tuned using the grid search method – look for the best combination of parameters that gives us the lowest out-out-sample error. 

## **Performance measurement** 

In order to evaluate the effectiveness of each model, we need to have a consistent measurable performance metric for all tested algorithms, While accuracy (defined as percentage of cases evaluated where the outcome is predicted accurately) is easily 

13 

interpretable and often used to analyze the quality of the predictive model, it relies on a single threshold value (usually 0.5) to determine the classification output. However, for different types of problem, objective and data distribution, the optimal classifier thresholds could differ. Area under receiver operating curve (AUC ROC) measures the trade-off between true positive rates and false positive rates under various threshold levels. It serves as a more objective comparison metric between two or more classifiers. An AUC of a random model with zero predictive power will have an area = 0.5, while a perfect model will have an area under curve = 1. In short, the higher the AUC, the better the model performs. We can also measure the performance using another alternative metric – area under precision recall curve, which often gives us consistent results, given that the data sets are not heavily imbalanced (see Appendix III: Visual explanations of machine learning terminologies). 

For consistency, each model is trained with the same training and validation data sets using five-fold cross validation, and we measure the performance of the model using out-of-sample testing data sets. We split the analysis into four different datasets based on the modification year (2012-15) to ensure the performance of the algorithms are consistent over time. 

## Appendix II: Model performance evaluation results 

Based on the result summary, we can see that regularized logistic regression models and linear discriminant analysis have the lowest predictive power among the tested models, averaging 70-72% AUC over time. As we move on to more complex models such as multi-layer neural network (four hidden layers) and gradient boosting, the performance (in terms of AUC) improves by another 5-6%. Random forest (parallel boosting model) outperforms the previous two marginally by another 1-2% on average. As we combine these individual learners and form a combined classifier (stacking-based ensemble learning), the performance improves by another 1%. In addition to measuring absolute performance, we split the testing datasets into 50 smaller partitions and measure the standard deviation of the algorithm's performance on each data partition. While the improvement from combining classifiers seems marginal, it also helps to reduce the variance of the classifier performance over different datasets. At the very least, the combined learner outperforms each individual base learner it learns from and it can further improve as we include more uncorrelated learners to its base level. 

14 

**Exhibit 13:** Area under curve across various algorithms (out-of-sample result) 

Source: Loan Performance, Morgan Stanley Research 

**Exhibit 14:** Standard deviation of performance across different data partitions (by algorithm) 

**==> picture [486 x 170] intentionally omitted <==**

**----- Start of picture text -----**<br>
2.4%<br>2.3%<br>2.2%<br>2.1%<br>2.0%<br>1.9%<br>1.8%<br>1.7%<br>Ridge Lasso Elastic LDA Deep Gradient Random Ensemble<br>Net Learning Boosting Forest Learning<br>**----- End of picture text -----**<br>


Source: Loan Performance, Morgan Stanley Research 

15 

**Exhibit 15: Model evaluation (rolling test) – comparison between predicted values and actual value** 

Source: Loan Performance, Morgan Stanley Research 

16 

## Appendix III: Visual explanations of machine learning terminologies 

Entropy and information gain explanation 

17 

Gain ratio explanation 

Chi-square explanation 

18 

## Scaled information gain by selected features 

19 

## Scaled gain ratio by selected features 

20 

## Scaled chi-square by selected features 

21 

Simplified explanation of performance metrics 

22 

## Appendix IV - Machine learning algorithms 

## **Regularized logistic regression** 

Logistic regression is a regression model where dependent variables are discrete and it is used to estimate the probability of a categorical response based on linear combination of predictors. In order to prevent models from over-fitting, given data samples, we include a regularization term to impose a penalty on the complexity of the model to improve the generalizability of the learned model. There are three main types of regularization: ridge, lasso and elastic net (each differs by penalty term, which will be evaluated separately). 

## **Linear discriminant analysis** 

Linear discriminant analysis aims to find a linear combination of features that separates two or more classes of outcomes. It is similar to principal component analysis, which aims to find the principal components that explain the variance within the independent variables but differ by taking the differences in dependent variable into account. 

## **Random forest** 

Decision tree works by asking a series of questions that have binary outcomes – 'Yes' or 'No'. The questions/thresholds are chosen at any point of time to create the most asymmetrical data split. The decision tree does not stop splitting the data until each leaf of the tree has a smaller number of data points than a preset threshold. The mean (regression) or the mode (classification) of the leaves is then used as the final outcome. A decision tree model has the advantage of not assuming any inherent data distribution. However, it easily runs into over-fitting problems by having one data point per leaf. Random forest algorithm was devised to minimize the variance of the model by creating hundreds of decision trees in parallel and predict the final outcome based on the aggregate decision. In order to improve the overall predictive power, we aim to reduce the correlation between each tree by providing each of them with a different subset of sample data and features. 

23 

Simplified random forest model 

## **Gradient boosting** 

Similar to random forest, gradient boosting is an ensemble algorithm. One key difference between these two is that instead of building different weak learners (models with low predictive ability) in parallel, we create them in stagewise fashion. At each iteration, we assume there is some imperfect model and we add an additional imperfect model to learn from the residual values (difference between actual outcomes and predicted outcomes). The residual value decreases with each iteration and the learning process continues until it is less than a preset threshold value (determined by the user). 

Simplified gradient boosting model 

## **Multilayer neural network/deep learning** 

Artificial neurons (basic building blocks of a neural network) are inspired by biological neural networks that constitute human brains. Each neuron receives one or more inputs (separately weighted) and the sum is passed through a non-linear activation function (e.g., sigmoid , tanh, RELU). An artificial neural network is a collection of neurons and is typically organized in layers where the output of each layer serves as the input of the 

24 

subsequent layer. The hierarchical architecture of the network helps the model to learn the abstraction representation of the underlying data. 

Simplified neural network model 

## **Ensemble algorithm – stacking** 

Stacked algorithm involves training a learning algorithm to combine information from multiple predictive models to generate a new model. First, it trains individual algorithms (e.g., linear regression, neural network, random forest) using available datasets. Subsequently, we train a combiner algorithm to make the final prediction using all the predictions from the individual algorithms as additional inputs. In practice, we often use a simple logistic regression model as the combiner (to prevent over-fitting). The stacked algorithm usually outperforms its base learners and the outperformance increases as the correlation between base learners decreases. 

Simplified stacking algorithm model 

25 

## **Disclosure Section** 

Mortgage Backed Securities (MBS) and Collateralized Mortgage Obligations (CMO) 

Principal is returned on a monthly basis over the life of the security. Principal prepayment can significantly affect the monthly income stream and the maturity of any type of MBS, including standard MBS, CMOs and Lottery Bonds. Yields and average lives are estimated based on prepayment assumptions and are subject to change based on actual prepayment of the mortgages in the underlying pools. The level of predictability of an MBS/CMO's average life, and its market price, depends on the type of MBS/CMO class purchased and interest rate movements. In general, as interest rates fall, prepayment speeds are likely to increase, thus shortening the MBS/CMO's average life and likely causing its market price to rise. Conversely, as interest rates rise, prepayment speeds are likely to decrease, thus lengthening average life and likely causing the MBS/CMO's market price to fall. Some MBS/CMOs may have “original issue discount” (OID). OID occurs if the MBS/CMO’s original issue price is below its stated redemption price at maturity, and results in “imputed interest” that must be reported annually for tax purposes, resulting in a tax liability even though interest was not received. Investors are urged to consult their tax advisors for more information. Government agency backing applies only to the face value of the CMO and not to any premium paid. 

The information and opinions in Morgan Stanley Research were prepared by Morgan Stanley & Co. LLC, and/or Morgan Stanley C.T.V.M. S.A., and/or Morgan Stanley Mexico, Casa de Bolsa, S.A. de C.V., and/or Morgan Stanley Canada Limited. As used in this disclosure section, "Morgan Stanley" includes Morgan Stanley & Co. LLC, Morgan Stanley C.T.V.M. S.A., Morgan Stanley Mexico, Casa de Bolsa, S.A. de C.V., Morgan Stanley Canada Limited and their affiliates as necessary. 

For important disclosures, stock price charts and equity rating histories regarding companies that are the subject of this report, please see the Morgan Stanley Research Disclosure Website at www.morganstanley.com/researchdisclosures, or contact your investment representative or Morgan Stanley Research at 1585 Broadway, (Attention: Research Management), New York, NY, 10036 USA. 

For valuation methodology and risks associated with any recommendation, rating or price target referenced in this research report, please contact the Client Support Team as follows: US/Canada +1 800 303-2495; Hong Kong +852 2848-5999; Latin America +1 718 754-5444 (U.S.); London +44 (0)20-7425-8169; Singapore +65 6834-6860; Sydney +61 (0)2-9770-1505; Tokyo +81 (0)3-6836-9000. Alternatively you may contact your investment representative or Morgan Stanley Research at 1585 Broadway, (Attention: Research Management), New York, NY 10036 USA. 

## **Analyst Certification** 

The following analysts hereby certify that their views about the companies and their securities discussed in this report are accurately expressed and that they have not received and will not receive direct or indirect compensation in exchange for expressing specific recommendations or views in this report: James Egan; Jeen Ng; Vishwanath Tirupattur. 

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

(as of September 30, 2017) 

The Stock Ratings described below apply to Morgan Stanley's Fundamental Equity Research and do not apply to Debt Research produced by the Firm. For disclosure purposes only (in accordance with NASD and NYSE requirements), we include the category headings of Buy, Hold, and Sell alongside our ratings of Overweight, Equal-weight, Not-Rated and Underweight. Morgan Stanley does not assign ratings of Buy, Hold or Sell to the stocks we cover. Overweight, Equal-weight, Not-Rated and Underweight are not the equivalent of buy, hold, and sell but represent recommended relative weightings (see definitions below). To satisfy regulatory requirements, we correspond Overweight, our most positive stock rating, with a buy recommendation; we correspond Equal-weight and Not-Rated to hold and Underweight to sell recommendations, respectively. 

26 

||COVERAGE UNIVERSE|COVERAGE UNIVERSE|INVESTMENT BANKING CLIENTS (IBC)|INVESTMENT BANKING CLIENTS (IBC)|INVESTMENT BANKING CLIENTS (IBC)|OTHER MATERIAL|OTHER MATERIAL|
|---|---|---|---|---|---|---|---|
|||||||INVESTMENT SERVICES||
|||||||CLIENTS(MISC)||
|STOCK RATING|COUNT|% OF|COUNT|% OF|% OF|COUNT|% OF|
|CATEGORY||TOTAL||TOTAL IBC|RATING||TOTAL|
||||||CATEGORY||OTHER|
||||||||MISC|
|**Overweight/Buy**|**1162**|**36%**|**304**|**40%**|**26%**|**560**|**37%**|
|**Equal-weight/Hold**|**1420**|**44%**|**363**|**48%**|**26%**|**697**|**46%**|
|**Not-Rated/Hold**|**58**|**2%**|**6**|**1%**|**10%**|**9**|**1%**|
|**Underweight/Sell**|**612**|**19%**|**91**|**12%**|**15%**|**242**|**16%**|
|**TOTAL**|**3,252**||**764**|||**1508**||



Data include common stock and ADRs currently assigned ratings. Investment Banking Clients are companies from whom Morgan Stanley received investment banking compensation in the last 12 months. Due to rounding off of decimals, the percentages provided in the "% of total" column may not add up to exactly 100 percent. 

## **Analyst Stock Ratings** 

Overweight (O). The stock's total return is expected to exceed the average total return of the analyst's industry (or industry team's) coverage universe, on a risk-adjusted basis, over the next 12-18 months. 

Equal-weight (E). The stock's total return is expected to be in line with the average total return of the analyst's industry (or industry team's) coverage universe, on a risk-adjusted basis, over the next 12-18 months. 

Not-Rated (NR). Currently the analyst does not have adequate conviction about the stock's total return relative to the average total return of the analyst's industry (or industry team's) coverage universe, on a risk-adjusted basis, over the next 12-18 months. 

Underweight (U). The stock's total return is expected to be below the average total return of the analyst's industry (or industry team's) coverage universe, on a risk-adjusted basis, over the next 12-18 months. 

Unless otherwise specified, the time frame for price targets included in Morgan Stanley Research is 12 to 18 months. 

## **Analyst Industry Views** 

Attractive (A): The analyst expects the performance of his or her industry coverage universe over the next 12-18 months to be attractive vs. the relevant broad market benchmark, as indicated below. In-Line (I): The analyst expects the performance of his or her industry coverage universe over the next 12-18 months to be in line with the relevant broad market benchmark, as indicated below. Cautious (C): The analyst views the performance of his or her industry coverage universe over the next 12-18 months with caution vs. the relevant broad market benchmark, as indicated below. 

Benchmarks for each region are as follows: North America - S&P 500; Latin America - relevant MSCI country index or MSCI Latin America Index; Europe - MSCI Europe; Japan - TOPIX; Asia - relevant MSCI country index or MSCI sub-regional index or MSCI AC Asia Pacific ex Japan Index. 

## **Important Disclosures for Morgan Stanley Smith Barney LLC Customers** 

Important disclosures regarding the relationship between the companies that are the subject of Morgan Stanley Research and Morgan Stanley Smith Barney LLC or Morgan Stanley or any of their affiliates, are available on the Morgan Stanley Wealth Management disclosure website at www.morganstanley.com/online/researchdisclosures. For Morgan Stanley specific disclosures, you may refer to www.morganstanley.com/researchdisclosures. 

Each Morgan Stanley Equity Research report is reviewed and approved on behalf of Morgan Stanley Smith Barney LLC. This review and approval is conducted by the same person who reviews the Equity Research report on behalf of Morgan Stanley. This could create a conflict of interest. 

## **Other Important Disclosures** 

Morgan Stanley Research policy is to update research reports as and when the Research Analyst and Research Management deem appropriate, based on developments with the issuer, the sector, or the market that may have a material impact on the research views or opinions stated therein. In addition, certain Research publications are intended to be updated on a regular periodic basis (weekly/monthly/quarterly/annual) and will ordinarily be updated with that frequency, unless the Research Analyst and Research Management determine that a different publication schedule is appropriate based on current conditions. Morgan Stanley is not acting as a municipal advisor and the opinions or views contained herein are not intended to be, and do not constitute, advice within the meaning of Section 975 of the Dodd-Frank Wall Street Reform and Consumer Protection Act. 

Morgan Stanley produces an equity research product called a "Tactical Idea." Views contained in a "Tactical Idea" on a particular stock may be contrary to the recommendations or views expressed in research on the same stock. This may be the result of differing time horizons, methodologies, market events, or other factors. For all research available on a particular stock, please contact your sales representative or go to Matrix at http://www.morganstanley.com/matrix. Morgan Stanley Research is provided to our clients through our proprietary research portal on Matrix and also distributed electronically by Morgan Stanley to clients. Certain, but not all, Morgan Stanley Research products are also made available to clients through third-party vendors or redistributed to clients through alternate electronic means as a convenience. For access to all available Morgan Stanley Research, please contact your sales representative or go to Matrix at http://www.morganstanley.com/matrix. 

Any access and/or use of Morgan Stanley Research is subject to Morgan Stanley's Terms of Use (http://www.morganstanley.com/terms.html). By accessing and/or using Morgan Stanley Research, you are indicating that you have read and agree to be bound by our Terms of Use (http://www.morganstanley.com/terms.html). In addition you consent to Morgan Stanley processing your personal data and using cookies in accordance with our Privacy Policy and our Global Cookies Policy (http://www.morganstanley.com/privacy_pledge.html), including for the purposes of setting your preferences and to collect readership data so that we can deliver better and more personalized service and products to you. To find out more information about how Morgan Stanley processes personal data, how we use cookies and how to reject cookies see our Privacy Policy and our Global Cookies Policy (http://www.morganstanley.com/privacy_pledge.html). 

If you do not agree to our Terms of Use and/or if you do not wish to provide your consent to Morgan Stanley processing your personal data or using cookies please do not access our research. 

Morgan Stanley Research does not provide individually tailored investment advice. Morgan Stanley Research has been prepared without regard to the 

27 

circumstances and objectives of those who receive it. Morgan Stanley recommends that investors independently evaluate particular investments and strategies, and encourages investors to seek the advice of a financial adviser. The appropriateness of an investment or strategy will depend on an investor's circumstances and objectives. The securities, instruments, or strategies discussed in Morgan Stanley Research may not be suitable for all investors, and certain investors may not be eligible to purchase or participate in some or all of them. Morgan Stanley Research is not an offer to buy or sell or the solicitation of an offer to buy or sell any security/instrument or to participate in any particular trading strategy. The value of and income from your investments may vary because of changes in interest rates, foreign exchange rates, default rates, prepayment rates, securities/instruments prices, market indexes, operational or financial conditions of companies or other factors. There may be time limitations on the exercise of options or other rights in securities/instruments transactions. Past performance is not necessarily a guide to future performance. Estimates of future performance are based on assumptions that may not be realized. If provided, and unless otherwise stated, the closing price on the cover page is that of the primary exchange for the subject company's securities/instruments. The fixed income research analysts, strategists or economists principally responsible for the preparation of Morgan Stanley Research have received compensation based upon various factors, including quality, accuracy and value of research, firm profitability or revenues (which include fixed income trading and capital markets profitability or revenues), client feedback and competitive factors. Fixed Income Research analysts', strategists' or economists' compensation is not linked to investment banking or capital markets transactions performed by Morgan Stanley or the profitability or revenues of particular trading desks. The "Important US Regulatory Disclosures on Subject Companies" section in Morgan Stanley Research lists all companies mentioned where Morgan Stanley owns 1% or more of a class of common equity securities of the companies. For all other companies mentioned in Morgan Stanley Research, Morgan Stanley may have an investment of less than 1% in securities/instruments or derivatives of securities/instruments of companies and may trade them in ways different from those discussed in Morgan Stanley Research. Employees of Morgan Stanley not involved in the preparation of Morgan Stanley Research may have investments in securities/instruments or derivatives of securities/instruments of companies mentioned and may trade them in ways different from those discussed in Morgan Stanley Research. Derivatives may be issued by Morgan Stanley or associated persons. 

With the exception of information regarding Morgan Stanley, Morgan Stanley Research is based on public information. Morgan Stanley makes every effort to use reliable, comprehensive information, but we make no representation that it is accurate or complete. We have no obligation to tell you when opinions or information in Morgan Stanley Research change apart from when we intend to discontinue equity research coverage of a subject company. Facts and views presented in Morgan Stanley Research have not been reviewed by, and may not reflect information known to, professionals in other Morgan Stanley business areas, including investment banking personnel. Morgan Stanley Research personnel may participate in company events such as site visits and are generally prohibited from accepting payment by the company of associated expenses unless pre-approved by authorized members of Research management. Morgan Stanley may make investment decisions that are inconsistent with the recommendations or views in this report. 

To our readers based in Taiwan or trading in Taiwan securities/instruments: Information on securities/instruments that trade in Taiwan is distributed by Morgan Stanley Taiwan Limited ("MSTL"). Such information is for your reference only. The reader should independently evaluate the investment risks and is solely responsible for their investment decisions. Morgan Stanley Research may not be distributed to the public media or quoted or used by the public media without the express written consent of Morgan Stanley. Any non-customer reader within the scope of Article 7-1 of the Taiwan Stock Exchange Recommendation Regulations accessing and/or receiving Morgan Stanley Research is not permitted to provide Morgan Stanley Research to any third party (including but not limited to related parties, affiliated companies and any other third parties) or engage in any activities regarding Morgan Stanley Research which may create or give the appearance of creating a conflict of interest. Information on securities/instruments that do not trade in Taiwan is for informational purposes only and is not to be construed as a recommendation or a solicitation to trade in such securities/instruments. MSTL may not execute transactions for clients in these securities/instruments. 

Morgan Stanley is not incorporated under PRC law and the research in relation to this report is conducted outside the PRC. Morgan Stanley Research does not constitute an offer to sell or the solicitation of an offer to buy any securities in the PRC. PRC investors shall have the relevant qualifications to invest in such securities and shall be responsible for obtaining all relevant approvals, licenses, verifications and/or registrations from the relevant governmental authorities themselves. Neither this report nor any part of it is intended as, or shall constitute, provision of any consultancy or advisory service of securities investment as defined under PRC law. Such information is provided for your reference only. 

Morgan Stanley Research is disseminated in Brazil by Morgan Stanley C.T.V.M. S.A.; in Mexico by Morgan Stanley México, Casa de Bolsa, S.A. de C.V which is regulated by Comision Nacional Bancaria y de Valores. Paseo de los Tamarindos 90, Torre 1, Col. Bosques de las Lomas Floor 29, 05120 Mexico City; in Japan by Morgan Stanley MUFG Securities Co., Ltd. and, for Commodities related research reports only, Morgan Stanley Capital Group Japan Co., Ltd; in Hong Kong by Morgan Stanley Asia Limited (which accepts responsibility for its contents) and by Morgan Stanley Asia International Limited, Hong Kong Branch; in Singapore by Morgan Stanley Asia (Singapore) Pte. (Registration number 199206298Z) and/or Morgan Stanley Asia (Singapore) Securities Pte Ltd (Registration number 200008434H), regulated by the Monetary Authority of Singapore (which accepts legal responsibility for its contents and should be contacted with respect to any matters arising from, or in connection with, Morgan Stanley Research) and by Morgan Stanley Asia International Limited, Singapore Branch (Registration number T11FC0207F); in Australia to "wholesale clients" within the meaning of the Australian Corporations Act by Morgan Stanley Australia Limited A.B.N. 67 003 734 576, holder of Australian financial services license No. 233742, which accepts responsibility for its contents; in Australia to "wholesale clients" and "retail clients" within the meaning of the Australian Corporations Act by Morgan Stanley Wealth Management Australia Pty Ltd (A.B.N. 19 009 145 555, holder of Australian financial services license No. 240813, which accepts responsibility for its contents; in Korea by Morgan Stanley & Co International plc, Seoul Branch; in India by Morgan Stanley India Company Private Limited; in Indonesia by PT. Morgan Stanley Sekuritas Indonesia; in Canada by Morgan Stanley Canada Limited, which has approved of and takes responsibility for its contents in Canada; in Germany by Morgan Stanley Bank AG, Frankfurt am Main and Morgan Stanley Private Wealth Management Limited, Niederlassung Deutschland, regulated by Bundesanstalt fuer Finanzdienstleistungsaufsicht (BaFin); in Spain by Morgan Stanley, S.V., S.A., a Morgan Stanley group company, which is supervised by the Spanish Securities Markets Commission (CNMV) and states that Morgan Stanley Research has been written and distributed in accordance with the rules of conduct applicable to financial research as established under Spanish regulations; in the US by Morgan Stanley & Co. LLC, which accepts responsibility for its contents. Morgan Stanley & Co. International plc, authorized by the Prudential Regulatory Authority and regulated by the Financial Conduct Authority and the Prudential Regulatory Authority, disseminates in the UK research that it has prepared, and approves solely for the purposes of section 21 of the Financial Services and Markets Act 2000, research which has been prepared by any of its affiliates. RMB Morgan Stanley Proprietary Limited is a member of the JSE Limited and regulated by the Financial Services Board in South Africa. RMB Morgan Stanley Proprietary Limited is a joint venture owned equally by Morgan Stanley International Holdings Inc. and RMB Investment Advisory (Proprietary) Limited, which is wholly owned by FirstRand Limited. The information in Morgan Stanley Research is being disseminated by Morgan Stanley Saudi Arabia, regulated by the Capital Market Authority in the Kingdom of Saudi Arabia , and is directed at Sophisticated investors only. 

The information in Morgan Stanley Research is being communicated by Morgan Stanley & Co. International plc (DIFC Branch), regulated by the Dubai Financial Services Authority (the DFSA), and is directed at Professional Clients only, as defined by the DFSA. The financial products or financial services to which this research relates will only be made available to a customer who we are satisfied meets the regulatory criteria to be a Professional Client. The information in Morgan Stanley Research is being communicated by Morgan Stanley & Co. International plc (QFC Branch), regulated by the Qatar Financial Centre Regulatory Authority (the QFCRA), and is directed at business customers and market counterparties only and is not intended for Retail Customers as defined by the QFCRA. 

As required by the Capital Markets Board of Turkey, investment information, comments and recommendations stated here, are not within the scope of investment advisory activity. Investment advisory service is provided exclusively to persons based on their risk and income preferences by the authorized firms. 

28 

Comments and recommendations stated here are general in nature. These opinions may not fit to your financial status, risk and return preferences. For this reason, to make an investment decision by relying solely to this information stated here may not bring about outcomes that fit your expectations. The trademarks and service marks contained in Morgan Stanley Research are the property of their respective owners. Third-party data providers make no warranties or representations relating to the accuracy, completeness, or timeliness of the data they provide and shall not have liability for any damages relating to such data. The Global Industry Classification Standard (GICS) was developed by and is the exclusive property of MSCI and S&P. Morgan Stanley Research, or any portion thereof may not be reprinted, sold or redistributed without the written consent of Morgan Stanley. 

© 2017 Morgan Stanley 

29 


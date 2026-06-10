## **Global Interest Rate Strategy** 

March 2016 M O R G A N   S T A N L E Y   R E S E A R C H **XCCY Basis Primer** Morgan Stanley & Co. International plc+ **Alexander Wojt** alexander.wojt@morganstanley.com +44 20 7425 3976 Morgan Stanley MUFG Securities Co., Ltd.+ **Koichi Sugisaki** koichi.sugisaki@morganstanley.com +81 3 6836 8428 _Due to the nature of the fixed income market, the issuers or bonds of the issuers recommended or discussed in this report may not be continuously followed. Accordingly, investors must regard this report as providing standalone analysis and should not expect continuing analysis or additional reports relating to such issuers or bonds of the issuers._ 

## Note: Information as of Match 22, 2016, unless otherwise indicated. 

Morgan Stanley does and seeks to do business with companies covered in Morgan Stanley Research. As a result, investors should be aware that the firm may have a conflict of interest that could affect the objectivity of Morgan Stanley Research. Investors should consider Morgan Stanley Research as only a single factor in making their investment decision. 

## **For analyst certification and other important disclosures, refer to the Disclosure Section, located at the end of this report.** 

+= Analysts employed by non-U.S. affiliates are not registered with FINRA, may not be associated persons of the member and may not be subject to NASD/NYSE restrictions on communications with a subject company, public appearances and trading securities held by a research analyst account. 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Content** 

## **Section 1. The Mechanics of XCCY Basis Swaps** 

- Quotation, definition and terminology 

- Cash flows of XCCY basis swaps 

- Calculation of the basis 

## **Section 2. The Drivers and Risks** 

- Foreign currency issuance 

- Foreign currency asset purchases 

- FX 

- Rates 

- Liquidity 

- Regulation 

## **Section 3. Additional Material** 

- Decomposing the basis 

- FX forwards vs. XCCY basis 

- MtM vs. non-MtM XCCY swaps 

2 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Section 1 – The Mechanics of XCCY Basis Swaps** 

3 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Quotation, Definition and Terminology** 

**Definition:** _A cross-currency basis swap (XCCY swap) is a floating/floating swap where two parties simultaneously borrow from and lend to each other in two different currencies for a predefined period of time._ 

**Intuition:** The XCCY basis gives an indication of the price for liquidity in one currency vs. another. 

**Quotation:** The basis is usually quoted on the non-USD leg. For example, if one party is receiving the EURUSD XCCY basis at -40bp, that party will be receiving Euribor -40bp and paying USD Libor. The currency on which the basis is added is typically written first, e.g., in a JPYUSD XCCY, the spread is on the JPY leg (even though it can occasionally be seen written the other way round). 

**Non-USD XCCY:** Due to liquidity reasons, non-USD XCCY is often traded through USD. The SEKEUR basis is traded through EURUSD & SEKUSD. 

**Liquidity:** XCCY basis swaps are typically liquid beyond the 1y point. In the front end, the FX basis is traded. 

**Reference rates:** Interemediate payments typically occur every quarter and the reference rate is 3m xIbor. 

**Common uses:** Hedging of foreign currency assets or liabilities. Optimizing funding decisions. Liquidity management. Macro trading. 

**Market participants:** Bank treasurys, corporate treasurys, asset managers, hedge funds 

4 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Cash Flows of XCCY Basis Swaps** 

**At the start:** A is lending B an amount of X (EUR) while borrowing X*S USD, where S is the current spot rate. 

**Intermediate payments:** During the life of the swap, A will be paying 3m USD Libor (as USD was borrowed) while receiving 3m Euribor + x (as EUR was lent). 

**At maturity:** A will be repaid X (EUR) while paying back X*S (USD) to B. The last floating payments will also be made at maturity. 

**==> picture [669 x 191] intentionally omitted <==**

**----- Start of picture text -----**<br>
At start  Intermediate  At maturity<br>A  A  A<br>JT oO CT<br>3m USD  3m   X   X*S   3m   3m<br>X (EUR)  X*S (USD)<br>Libor  Euribor + x  (EUR)  (USD)  USD Libor  Euribor + x<br>en<br>B  B  B<br>ne ee<br>**----- End of picture text -----**<br>


5 

Source: Morgan Stanley Research 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Calculation of the Basis** 

The most intuitive way to calculate the basis is by looking at FX forwards, which constitutes the front end of the XCCY curve. The formula is: 

**==> picture [131 x 30] intentionally omitted <==**

We can also use this formula the other way round. Taking forward data from the market, we can solve for, for example, the European rate. Doing that, using 12m US Ois rates, we realize that the resulting 12m EONIA rate that we solve for will differ from the market rate (see Exhibit 1). The difference is the basis, denoted x below. 

**==> picture [443 x 43] intentionally omitted <==**

Doing the calculations above, we see that our calculated basis equals the 1y fed funds/EONIA basis quoted on BBG (Exhibit 2) 

## **Exhibit 1. 12m EONIA Implied from FX Fwds** 

**==> picture [215 x 218] intentionally omitted <==**

**----- Start of picture text -----**<br>
%<br>EONIA 12m<br>6.0<br>EONIA 12m implied from FX fwds<br>4.8<br>3.6<br>2.4<br>1.2<br>0.0<br>-1.2<br>2005 2007 2010 2013 2015<br>Source: Morgan Stanley Research, Bloomberg<br>**----- End of picture text -----**<br>


## **Exhibit 2. ’Calculated’ vs. BBG Quoted 1y Basis** 

**==> picture [219 x 206] intentionally omitted <==**

**----- Start of picture text -----**<br>
Basis points<br>0<br>-5<br>-10<br>-15<br>-20<br>-25<br>-30<br>-35<br>-40<br>-45<br>-50<br>1y EURUSD basis (EOUSFF1 Curncy)<br>-55<br>1y EURUSD basis (implied from FX fwds)<br>-60<br>Jul-12 Aug-13 Sep-14 Oct-15<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research, Bloomberg 

6 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Section 2 – The Drivers and Risks** 

7 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Drivers of XCCY – A Constantly Evolving Landscape** 

## Basis points 

Source: Morgan Stanley Research, Bloomberg, Macrobond 

8 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Drivers of XCCY (1) – Issuance** 

Issuance is probably one of the most important drivers of the basis, as issuance data are available and we tend to have an idea of what corporate issuance is being swapped. 

When issuance is done in foreign currency, and swapped back to domestic currency, the domestic currency becomes ’richer’. 

The XCCY makes it possible to transform issuance in one currency into another. Thus, issuers typically assess in what currency and on what part of the curve it is optimal to fund. 

**Exhibit 3. Optimal Funding Segments** 

**==> picture [232 x 213] intentionally omitted <==**

**----- Start of picture text -----**<br>
Basis points<br>20<br>Cheaper to<br>fund in USD<br>0<br>Cheaper to<br>fund in EUR<br>-20<br>-40<br>-60<br>-80<br>AA & A non-financials (current)<br>-100 O O<br>1 2 3 4 5 6 7 8 9 10 12<br>Maturity<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research, Bloomberg 

## **Exhibit 4. Historically Prefered Issuance Currency** 

**==> picture [230 x 198] intentionally omitted <==**

**----- Start of picture text -----**<br>
Basis points<br>100<br>Favourable to fund in USD<br>60<br>uf<br>20<br>-20<br>Wh Ay Min AN<br>-60<br>Favourable to<br>fund in EUR<br>-100<br>-140 5-10y A/BBB Corp Spreads<br>5-10y A/BBB Corp Spreads (incl. XCCY)<br>-180 —<br>2007 2009 2011 2014 2016<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research, Bloomberg 

9 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Drivers of XCCY (1) – Issuance (Example of Swapped EUR Issuance)** 

The more EUR issuance by US corporates that is swapped back to USD, the more receiving pressure on the XCCY basis 

**==> picture [540 x 347] intentionally omitted <==**

**----- Start of picture text -----**<br>
EUR<br>.  .  .  US corporate issues EUR bond  A US corporate issues a EUR bond, receives the<br>.  .  .  notional and pays the fixed coupons.<br>EUR<br>.  .  .  Receive fixed rate in swap<br>A received position in swaps is entered to transform<br>.  .  .  the fixed intermediate payments into floating rates.<br>3m Euribor<br>Receive EURUSD XCCY<br>USD EUR<br>.  .  .  3m Euribor+x By receiving (Euribor – x) in a XCCY, the corporate<br>lends EUR, borrows USD, and thereby receives<br>Euribor + x and pays Libor.<br>.  .  .  3m Libor<br>EUR USD<br>Netting out the cash flows – USD bond issuance<br>USD .  .  .  x Netting out the cash flows, we end up with the profile of a USD bond issuance with floating payments (i.e.,<br>issued fixed vs. swaps). Thus, the initial EUR bond<br>.  .  .  3m Libor issue has been transformed into a USD bond issue.<br>USD<br>**----- End of picture text -----**<br>


10 

Source: Morgan Stanley Research 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Drivers of XCCY (2) – Foreign Asset Purchases** 

FX-hedged purchases of foreign currency securities will push the basis in the other direction compared to issuance. 

There is, however, less transparancy about who is trading the XCCY, rolling FX forwards or is unhedged. 

Bank treasurys tend to actively look for opportunities across markets and are typically frequent users of basis swaps. 

**Exhibit 5. Assessing Value across Currencies** 

## **Exhibit 6. Eurozone Debt Outflows** 

**==> picture [612 x 228] intentionally omitted <==**

**----- Start of picture text -----**<br>
Basis points EUR bn, 12m sum<br>200 Net Debt Flows<br>600<br>ASWs swapped back to EUR (vs 3s)* Net Equity Flows<br>150<br>400<br>Outflows from<br>100 Eurozone<br>200<br>50<br>0<br>0<br>-200<br>-50<br>ECB<br>— DE SP US JP -400 vy!<br>introduces<br>Inflows to<br>-100<br>neg rates<br>Eurozone<br>2 7 12 17 22 -600<br>*Constant maturity  Maturity 2007 2009 2011 2013 2015<br>Source: Morgan Stanley Research, Bloomberg  Source: Morgan Stanley Research, Bloomberg<br>**----- End of picture text -----**<br>


11 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Drivers of XCCY (2) – Foreign Asset Purchases (Example of FX-hedged Purchase)** 

EUR **.  .  . US treasury buys EUR bond** ...and receives the intermediate fixed coupons. EUR 3m Euribor **.  .  . Pay fixed rate in swap** A paid position in swaps is entered to transform the **.  .  .** fixed intermediate payments into floating rates. EUR USD **.  .  .** 3m Libor **Pay EURUSD XCCY** By paying (Euribor – x) in a XCCY, the treasury **.  .  .** 3m Euribor+x lends USD, borrows EUR, and thereby pays Euribor USD EUR + x and receives Libor. The more EUR assets bought by US corporates TS] and swapped back to USD, the more paying pressure on the **.  .  .** 3m Libor USD **Netting out the cash flows – USD bond purchase** XCCY basis Netting out the cash flows, we end up with the profile of a USD bond purchase with floating payments (i.e., x bought on ASW). Thus, the initial EUR bond USD purchase has been transformed into a USD bond purchase. 

12 

Source: Morgan Stanley Research 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Drivers of XCCY (3) – FX** 

There is not a direct link between the currency pair and a XCCY basis. 

However, both indicate a need for one currency (over another), which can often be seen both in the FX forward market and the spot market. 

The relation between the two were stronger in 2008-12; the correlation has lately weakened, as the XCCY has been moving somewhat less with general risk-on/risk-off during the last couple of years. 

## **Exhibit 7. EURUSD & XCCY** 

**==> picture [240 x 211] intentionally omitted <==**

**----- Start of picture text -----**<br>
Basis points<br>EURUSD, lhs<br>1.7 20<br>2y EURUSD XCCY basis, rhs<br>0<br>1.6<br>-20<br>1.4<br>-40<br>1.3 SWE Nae<br>-60<br>yr<br>1.1<br>| -80<br>1.0 -100<br>2008 2010 2011 2013 2014 2016<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research, Bloomberg 

## **Exhibit 8. FX Options and XCCY** 

**==> picture [240 x 210] intentionally omitted <==**

**----- Start of picture text -----**<br>
Basis points<br>2.0 20<br>3m EURUSD 25d risk reversal, lhs<br>2y EURUSD XCCY basis, rhs<br>1.0<br>0<br>0.0<br>-20<br>-1.0<br>-40<br>-2.0 i nae<br>-60<br>-3.0<br>YOUU -80<br>-4.0<br>-5.0 -100<br>2008 2010 2011 2013 2014 2016<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research, Bloomberg 

13 

**M O R G A N   S T A N L E Y   R E S E A R C H** March 2016 

## **Drivers of XCCY (4) – Rates** 

As with FX, there is no direct link between the rate levels or curves in between two markets and the XCCY. 

However, as the level of rates and the slope of the yield curve give an indication of future monetary policy and thereby also issuance activity, there will be an indirect link between the shape of the yield curve and the XCCY. 

Typically, jurisdictions with higher rates (ZAR, AUD, NZD, etc.) have a basis that is positive (vs. USD) while low rate environment which works as funding markets (JPY, EUR, CHF) usually have a negative basis. 

**Exhibit 9. XCCY in Different Markets** 

Source: Morgan Stanley Research, Bloomberg. Macrobond 

14 

**M O R G A N   S T A N L E Y   R E S E A R C H** March 2016 

## **Drivers of XCCY (5) – Liquidity** 

Liquidity was a key driver of the XCCY basis in particular in the beginning of the financial crisis, before QE was launched and when swap lines had not been established. Liquidity tended to be related to dollar scarcity, which caused the EURUSD basis to widen. 

More recently, the draining of the 3y LTROs helped tighten the basis, which traded above zero for a brief period. 

In order to limit the severity of liquidity stress in the market, the major central banks have swap lines with the Fed (for a cost of Ois+50bp). These have never been intensely used, not even during the crisis, but do provide a theoretical backstop, even if there is some stigma attached. 

**Exhibit 10. Limited Usage of USD Swap Lines These Days** 

## **Exhibit 11. Relative Balance Sheets and XCCY** 

**==> picture [290 x 188] intentionally omitted <==**

**----- Start of picture text -----**<br>
1.80<br>Usage of USD swap lines (bn USD)<br>1.60<br>| ECB<br>1.40<br>7 Bank of Japan<br>1.20 Quarter-ends<br>1.00 SS<br>0.80<br>Lo \<br>0.60<br>0.40<br>0.20<br>0.00<br>Nov 2014 Feb 2015 May 2015 Aug 2015 Nov 2015<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research, Bloomberg 

Source: Morgan Stanley Research, Bloomberg 

15 

**M O R G A N   S T A N L E Y   R E S E A R C H** March 2016 

## **Drivers of XCCY (6) – Regulation** 

A range of new regulation has changed the XCCY landscape over the past few years. Some of these regulations may have contributed to the surprisingly large widening in EURUSD XCCY during the 2015 yearend. 

**SLR (Supplementary Liquidity Ratio):** The ratio is designed to make sure banks have adequate capital relative to total exposure. In brief, it means that low-risk repo positions will impact total exposure a lot. This has tended to drive up the cost of USD funding in the repo market, increasing the need to fund through currency swaps. 

**US MMF:** The US money market fund regulation (coming in October 2016) will likely also make commercial paper funding more costly, contributing to the increased pressure on FX forwards. MMFs will be pushed away from CPs and into USTs. 

**Solvency II (UK):** Insurance companies are suggested to use XCCY basis swaps when hedging foreign currency purchases instead of rolling FX forwards. The XCCY is seen as a better hedge but also more balance sheet intensive. 

**UK bank levy:** This will add another cost for banks trading XCCY over year-end. 

**Local regulators:** This year, mandatory margining will be rolled out, impacting all OTC derivatives. 

**Basel III:** As a result of Basel III and the credit value adjustment, trading XCCY has become more costly. 

16 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Section 3 – Additional Material** 

17 

**M O R G A N   S T A N L E Y   R E S E A R C H** March 2016 

## **Decomposing the Basis** 

The regular Libor XCCY basis swap can be decomposed into a Ois/Ois XCCY and Libor vs. Ois spreads. 

## **EURUSD (Libor) XCCY = EURUSD (Ois) XCCY + (USD Libor – USD Ois) – (Euribor – EONIA)** 

Thus, the Ois/Ois basis is the ‘purest’ one to trade when it comes to liquidity and credit risk, and is typically traded in the short end, while the Libor/Libor basis is traded beyond 1y. 

## **Exhibit 12. Ois/Ois vs. Libor/Libor XCCY** 

**==> picture [345 x 202] intentionally omitted <==**

**----- Start of picture text -----**<br>
3m FF  3m USD Libor<br>Ois/Ois   Libor/Libor<br>basis  basis<br>| —L_<br>3m EONIA  3m Euribor<br>I<br>JomL_ |}<br>**----- End of picture text -----**<br>


**==> picture [208 x 202] intentionally omitted <==**

**----- Start of picture text -----**<br>
Basis points<br>14<br>0<br>-14<br>-28<br>-42<br>1y EURUSD basis<br>a 1y FF/EONIA basis<br>-56<br>Apr-12 OF Aug-13 Dec-14 May-16<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

Source: Morgan Stanley Research, Bloomberg 

18 

**M O R G A N   S T A N L E Y   R E S E A R C H** March 2016 

## **FX Forwards vs. XCCY Basis** 

Instead of trading XCCY basis that provides a hedge for the full period, one could simply roll FX forwards. Each comes with its advantages/disadvantages. FX forwards are less balance sheet intensive but may be seen as less optimal from a regulatory perspective, as it’s not certain at what rate future rolls will be done. 

Using XCCY, the basis will be fixed throughout the whole period. When rolling FX forwards, the basis will change each time the roll occurs. 

**==> picture [85 x 102] intentionally omitted <==**

**----- Start of picture text -----**<br>
Rolling FX<br>forwards<br>XCCY Basis<br>**----- End of picture text -----**<br>


19 

Source: Morgan Stanley Research 

**M O R G A N   S T A N L E Y   R E S E A R C H** March 2016 

## **MtM vs. non-MtM XCCY Swaps** 

In a Mark-to-Market XCCY basis, the notional amount on one of the legs will be adjusted on each intermediate payment with the FX rate. 

The idea is to reduce credit risk due to changes in the collateral value caused by FX moves. 

Standard XCCY are typically Mark-to-Market. 

## **non-Mark-to-Market** 

**==> picture [76 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
Mark-to-Market<br>**----- End of picture text -----**<br>


**==> picture [628 x 277] intentionally omitted <==**

**----- Start of picture text -----**<br>
€ X<br>€ X<br>At start  A  B  A  B<br>$ X*S0  $ X*S0<br>PJ=LJ LILI<br>MtM adjustment<br>3m$L*X*St-1+(X*St-X*St-1)<br>3m$L*X*S0<br>Intermediate  A  B  A  B<br>(3m€L+x)*X<br>(3m€L+x)*X<br>3m$L*X*S0 3m$L*X*St-1<br>$ X*S0 $ X*St-1<br>At maturity  A  B  A  B<br>€ X<br>€ X<br>Source: Morgan   (3m€L+x)*X  (3m€L+x)*X<br>…  …  …  …<br>…  …  …  …<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

20 

**M O R G A N   S T A N L E Y   R E S E A R C H** March 2016 

## **Answering Three Common Questions** 

**Does a XCCY have FX risk?** In brief, not directly, and limited. But some FX risk exists both in MtM and nonMtM XCCY swaps as FX moves in-between cash-flows will lead to changes in the value of the collateral. Thus, this could be a potential issue in case one counterparty would default. However, this is usually seen as a relatively small risk in the XCCY basis. 

**Does a XCCY have rate risk?** A XCCY basis can be decomposed into two FRNs, in different currencies. A FRN has little interest rate risk as the duration will be between zero and the frequency of payments. In a XCCY, i.e. a long and short position in a FRN, the rate risk will thus be very close to zero. If the structure of the standard floating/floating XCCY would change however, and you for example would have one fixed leg, duration risk would exist. 

**Selling a USD floater…                     + buying a EUR floater…                    equals receiving EURUSD XCCY** 

**==> picture [641 x 93] intentionally omitted <==**

**----- Start of picture text -----**<br>
3m Euribor<br>USD 3m Euribor EUR USD EUR<br>+ =<br>3m Libor<br>USD EUR EUR USD<br>3m  Libor<br>**----- End of picture text -----**<br>


Source: Morgan Stanley Research 

**Why does the basis exist?** One way to understand why a basis exists in a product which is simply created by two floating rate notes is that both legs of the XCCY are discounted with the same curve (so fed funds or EONIA in a EURUSD XCCY). In two separate FRNs however, two discount curves will be used. This can also be seen as the reason for the existence of the basis. 

21 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Disclosure Section** 

The information and opinions in Morgan Stanley Research were prepared or are disseminated by Morgan Stanley & Co. LLC and/or Morgan Stanley C.T.V.M. S.A. and/or Morgan Stanley México, Casa de Bolsa, S.A. de C.V. and/or Morgan Stanley Canada Limited and/or Morgan Stanley & Co. International plc and/or RMB Morgan Stanley (Proprietary) Limited and/or Morgan Stanley MUFG Securities Co., Ltd. and/or Morgan Stanley Capital Group Japan Co., Ltd. and/or Morgan Stanley Asia Limited and/or Morgan Stanley Asia (Singapore) Pte. (Registration number 199206298Z) and/or Morgan Stanley Asia (Singapore) Securities Pte Ltd (Registration number 200008434H), regulated by the Monetary Authority of Singapore (which accepts legal responsibility for its contents and should be contacted with respect to any matters arising from, or in connection with, Morgan Stanley Research) and/or Morgan Stanley Taiwan Limited and/or Morgan Stanley & Co International plc, Seoul Branch, and/or Morgan Stanley Australia Limited (A.B.N. 67 003 734 576, holder of Australian financial services license No. 233742, which accepts responsibility for its contents), and/or Morgan Stanley Wealth Management Australia Pty Ltd (A.B.N. 19 009 145 555, holder of Australian financial services license No. 240813, which accepts responsibility for its contents), and/or Morgan Stanley India Company Private Limited, regulated by the Securities and Exchange Board of India (“SEBI”) and holder of licenses as a Research Analyst (SEBI Registration No. INH000001105), Stock Broker (BSE Registration No. INB011054237 and NSE Registration No. INB/INF231054231), Merchant Banker (SEBI Registration No. INM000011203), and depository participant with National Securities Depository Limited (SEBI Registration No. IN-DP-NSDL-372-2014) which accepts the responsibility for its contents and should be contacted with respect to any matters arising from, or in connection with, Morgan Stanley Research, and/or PT Morgan Stanley Asia Indonesia and their affiliates (collectively, "Morgan Stanley"). 

For important disclosures, stock price charts and equity rating histories regarding companies that are the subject of this report, please see the Morgan Stanley Research Disclosure Website at www.morganstanley.com/researchdisclosures, or contact your investment representative or Morgan Stanley Research at 1585 Broadway, (Attention: Research Management), New York, NY, 10036 USA. 

For valuation methodology and risks associated with any price targets referenced in this research report, please contact the Client Support Team as follows: US/Canada +1 800 303-2495; Hong Kong +852 2848-5999; Latin America +1 718 754-5444 (U.S.); London +44 (0)20-7425-8169; Singapore +65 6834-6860; Sydney +61 (0)2-9770-1505; Tokyo +81 (0)3-6836-9000. Alternatively you may contact your investment representative or Morgan Stanley Research at 1585 Broadway, (Attention: Research Management), New York, NY 10036 USA. 

## **Analyst Certification** 

The following analysts hereby certify that their views about the companies and their securities discussed in this report are accurately expressed and that they have not received and will not receive direct or indirect compensation in exchange for expressing specific recommendations or views in this report: Alexander Wojt 

Unless otherwise stated, the individuals listed on the cover page of this report are research analysts. 

## **Global Research Conflict Management Policy** 

Morgan Stanley Research has been published in accordance with our conflict management policy, which is available at www.morganstanley.com/institutional/research/conflictpolicies. 

## **Important US Regulatory Disclosures on Subject Companies** 

The equity research analysts or strategists principally responsible for the preparation of Morgan Stanley Research have received compensation based upon various factors, including quality of research, investor client feedback, stock picking, competitive factors, firm revenues and overall investment banking revenues. 

Morgan Stanley and its affiliates do business that relates to companies/instruments covered in Morgan Stanley Research, including market making, providing liquidity, fund management, commercial banking, extension of credit, investment services and investment banking. Morgan Stanley sells to and buys from customers the securities/instruments of companies covered in Morgan Stanley Research on a principal basis. Morgan Stanley may have a position in the debt of the Company or instruments discussed in this report. Certain disclosures listed above are also for compliance with applicable regulations in non-US jurisdictions. 

## **STOCK RATINGS** 

Morgan Stanley uses a relative rating system using terms such as Overweight, Equal-weight, Not-Rated or Underweight (see definitions below). Morgan Stanley does not assign ratings of Buy, Hold or Sell to the stocks we cover. Overweight, Equal-weight, Not-Rated and Underweight are not the equivalent of buy, hold and sell. Investors should carefully read the definitions of all ratings used in Morgan Stanley Research. In addition, since Morgan Stanley Research contains more complete information concerning the analyst's views, investors should carefully read Morgan Stanley Research, in its entirety, and not infer the contents from the rating alone. In any case, ratings (or research) should not be used or relied upon as investment advice. An investor's decision to buy or sell a stock should depend on individual circumstances (such as the investor's existing holdings) and other considerations. 

22 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Disclosure Section (Cont.)** 

## **Global Stock Ratings Distribution** 

## _(as of February 29, 2016)_ 

For disclosure purposes only (in accordance with NASD and NYSE requirements), we include the category headings of Buy, Hold, and Sell alongside our ratings of Overweight, Equalweight, Not-Rated and Underweight. Morgan Stanley does not assign ratings of Buy, Hold or Sell to the stocks we cover. Overweight, Equal-weight, Not-Rated and Underweight are not the equivalent of buy, hold, and sell but represent recommended relative weightings (see definitions below). To satisfy regulatory requirements, we correspond Overweight, our most positive stock rating, with a buy recommendation; we correspond Equal-weight and Not-Rated to hold and Underweight to sell recommendations, respectively. 

||Coverage Universe|e Universe|Investment Bankin|Investment BankingClients(IBC)|Investment BankingClients(IBC)|
|---|---|---|---|---|---|
|||% of|% of|% of|% of<br>% of Rating|
|Stock Rating Category|Count|Count<br>Total|Total<br>Count|Count<br>Total IBC|Total IBC<br>Category|
|**Overweight/Buy**|**1216**|<br>**36** **%**|**320**|<br>**44** **%**|**26** **%**|
|**Equal** **-** **weight/Hold**|**1399**|<br>**4** **2** **%**|**320**|<br>**4** **4** **%**|**23** **%**|
|**Not** **-** **Rated/Hold**|**69**|<br>**2%**|**3**|<br>**0%**|**4** **%**|
|**Underweight/Sell**|**671**|<br>**20** **%**|**89**|<br>**12** **%**|**13%**|
|**Total**|**3,355**|<br>|**732**|<br>|<br>|



Data include common stock and ADRs currently assigned ratings. Investment Banking Clients are companies from whom Morgan Stanley received investment banking compensation in the last 12 months. 

## **Analyst Stock Ratings** 

Overweight (O or Over) - The stock's total return is expected to exceed the total return of the relevant country MSCI Index or the average total return of the analyst's industry (or industry team's) coverage universe, on a risk-adjusted basis over the next 12-18 months. 

Equal-weight (E or Equal) - The stock's total return is expected to be in line with the total return of the relevant country MSCI Index or the average total return of the analyst's industry (or industry team's) coverage universe, on a risk-adjusted basis over the next 12-18 months. 

Not-Rated (NR) - Currently the analyst does not have adequate conviction about the stock's total return relative to the relevant country MSCI Index or the average total return of the analyst's industry (or industry team's) coverage universe, on a risk-adjusted basis, over the next 12-18 months. 

Underweight (U or Under) - The stock's total return is expected to be below the total return of the relevant country MSCI Index or the average total return of the analyst's industry (or industry team's) coverage universe, on a risk-adjusted basis, over the next 12-18 months. 

Unless otherwise specified, the time frame for price targets included in Morgan Stanley Research is 12 to 18 months. 

## **Analyst Industry Views** 

Attractive (A): The analyst expects the performance of his or her industry coverage universe over the next 12-18 months to be attractive vs. the relevant broad market benchmark, as indicated below. 

In-Line (I): The analyst expects the performance of his or her industry coverage universe over the next 12-18 months to be in line with the relevant broad market benchmark, as indicated below. 

Cautious (C): The analyst views the performance of his or her industry coverage universe over the next 12-18 months with caution vs. the relevant broad market benchmark, as indicated below. 

Benchmarks for each region are as follows: North America - S&P 500; Latin America - relevant MSCI country index or MSCI Latin America Index; Europe - MSCI Europe; Japan - TOPIX; Asia - relevant MSCI country index or MSCI sub-regional index or MSCI AC Asia Pacific ex Japan Index. 

23 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Disclosure Section (Cont.)** 

## **Important Disclosures for Morgan Stanley Smith Barney LLC Customers** 

Important disclosures regarding the relationship between the companies that are the subject of Morgan Stanley Research and Morgan Stanley Smith Barney LLC or Morgan Stanley or any of their affiliates, are available on the Morgan Stanley Wealth Management disclosure website at www.morganstanley.com/online/researchdisclosures. For Morgan Stanley specific disclosures, you may refer to www.morganstanley.com/researchdisclosures. 

Each Morgan Stanley Equity Research report is reviewed and approved on behalf of Morgan Stanley Smith Barney LLC. This review and approval is conducted by the same person who reviews the Equity Research report on behalf of Morgan Stanley. This could create a conflict of interest. 

## **Other Important Disclosures** 

Morgan Stanley is not acting as a municipal advisor and the opinions or views contained herein are not intended to be, and do not constitute, advice within the meaning of Section 975 of the Dodd-Frank Wall Street Reform and Consumer Protection Act. 

Morgan Stanley produces an equity research product called a "Tactical Idea." Views contained in a "Tactical Idea" on a particular stock may be contrary to the recommendations or views expressed in research on the same stock. This may be the result of differing time horizons, methodologies, market events, or other factors. For all research available on a particular stock, please contact your sales representative or go to Matrix at http://www.morganstanley.com/matrix. 

Morgan Stanley Research is provided to our clients through our proprietary research portal on Matrix and also distributed electronically by Morgan Stanley to clients. Certain, but not all, Morgan Stanley Research products are also made available to clients through third-party vendors or redistributed to clients through alternate electronic means as a convenience. For access to all available Morgan Stanley Research, please contact your sales representative or go to Matrix at http://www.morganstanley.com/matrix. 

Any access and/or use of Morgan Stanley Research is subject to Morgan Stanley's Terms of Use (http://www.morganstanley.com/terms.html). By accessing and/or using Morgan Stanley Research, you are indicating that you have read and agree to be bound by our Terms of Use (http://www.morganstanley.com/terms.html). In addition you consent to Morgan Stanley processing your personal data and using cookies in accordance with our Privacy Policy and our Global Cookies Policy (http://www.morganstanley.com/privacy_pledge.html), including for the purposes of setting your preferences and to collect readership data so that we can deliver better and more personalized service and products to you. To find out more information about how Morgan Stanley processes personal data, how we use cookies and how to reject cookies see our Privacy Policy and our Global Cookies Policy (http://www.morganstanley.com/privacy_pledge.html). 

If you do not agree to our Terms of Use and/or if you do not wish to provide your consent to Morgan Stanley processing your personal data or using cookies please do not access our research. 

Morgan Stanley Research does not provide individually tailored investment advice. Morgan Stanley Research has been prepared without regard to the circumstances and objectives of those who receive it. Morgan Stanley recommends that investors independently evaluate particular investments and strategies, and encourages investors to seek the advice of a financial adviser. The appropriateness of an investment or strategy will depend on an investor's circumstances and objectives. The securities, instruments, or strategies discussed in Morgan Stanley Research may not be suitable for all investors, and certain investors may not be eligible to purchase or participate in some or all of them. Morgan Stanley Research is not an offer to buy or sell or the solicitation of an offer to buy or sell any security/instrument or to participate in any particular trading strategy. The value of and income from your investments may vary because of changes in interest rates, foreign exchange rates, default rates, prepayment rates, securities/instruments prices, market indexes, operational or financial conditions of companies or other factors. There may be time limitations on the exercise of options or other rights in securities/instruments transactions. Past performance is not necessarily a guide to future performance. Estimates of future performance are based on assumptions that may not be realized. If provided, and unless otherwise stated, the closing price on the cover page is that of the primary exchange for the subject company's securities/instruments. 

The fixed income research analysts, strategists or economists principally responsible for the preparation of Morgan Stanley Research have received compensation based upon various factors, including quality, accuracy and value of research, firm profitability or revenues (which include fixed income trading and capital markets profitability or revenues), client feedback and competitive factors. Fixed Income Research analysts', strategists' or economists' compensation is not linked to investment banking or capital markets transactions performed by Morgan Stanley or the profitability or revenues of particular trading desks. 

The "Important US Regulatory Disclosures on Subject Companies" section in Morgan Stanley Research lists all companies mentioned where Morgan Stanley owns 1% or more of a class of common equity securities of the companies. For all other companies mentioned in Morgan Stanley Research, Morgan Stanley may have an investment of less than 1% in securities/instruments or derivatives of securities/instruments of companies and may trade them in ways different from those discussed in Morgan Stanley Research. Employees of Morgan Stanley not involved in the preparation of Morgan Stanley Research may have investments in securities/instruments or derivatives of securities/instruments of companies mentioned and may trade them in ways different from those discussed in Morgan Stanley Research. Derivatives may be issued by Morgan Stanley or associated persons. 

24 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Disclosure Section (Cont.)** 

With the exception of information regarding Morgan Stanley, Morgan Stanley Research is based on public information. Morgan Stanley makes every effort to use reliable, comprehensive information, but we make no representation that it is accurate or complete. We have no obligation to tell you when opinions or information in Morgan Stanley Research change apart from when we intend to discontinue equity research coverage of a subject company. Facts and views presented in Morgan Stanley Research have not been reviewed by, and may not reflect information known to, professionals in other Morgan Stanley business areas, including investment banking personnel. 

Morgan Stanley Research personnel may participate in company events such as site visits and are generally prohibited from accepting payment by the company of associated expenses unless pre-approved by authorized members of Research management. 

Morgan Stanley may make investment decisions that are inconsistent with the recommendations or views in this report. 

To our readers in Taiwan: Information on securities/instruments that trade in Taiwan is distributed by Morgan Stanley Taiwan Limited ("MSTL"). Such information is for your reference only. The reader should independently evaluate the investment risks and is solely responsible for their investment decisions. Morgan Stanley Research may not be distributed to the public media or quoted or used by the public media without the express written consent of Morgan Stanley. Information on securities/instruments that do not trade in Taiwan is for informational purposes only and is not to be construed as a recommendation or a solicitation to trade in such securities/instruments. MSTL may not execute transactions for clients in these securities/instruments. To our readers in Hong Kong: Information is distributed in Hong Kong by and on behalf of, and is attributable to, Morgan Stanley Asia Limited as part of its regulated activities in Hong Kong. If you have any queries concerning Morgan Stanley Research, please contact our Hong Kong sales representatives. 

Certain information in Morgan Stanley Research was sourced by employees of the Shanghai Representative Office of Morgan Stanley Asia Limited for the use of Morgan Stanley Asia Limited. 

Morgan Stanley is not incorporated under PRC law and the research in relation to this report is conducted outside the PRC. Morgan Stanley Research does not constitute an offer to sell or the solicitation of an offer to buy any securities in the PRC. PRC investors shall have the relevant qualifications to invest in such securities and shall be responsible for obtaining all relevant approvals, licenses, verifications and/or registrations from the relevant governmental authorities themselves. 

Morgan Stanley Research is disseminated in Brazil by Morgan Stanley C.T.V.M. S.A.; in Mexico by Morgan Stanley México, Casa de Bolsa, S.A. de C.V which is regulated by Comision Nacional Bancaria y de Valores. Paseo de los Tamarindos 90, Torre 1, Col. Bosques de las Lomas Floor 29, 05120 Mexico City; in Japan by Morgan Stanley MUFG Securities Co., Ltd. and, for Commodities related research reports only, Morgan Stanley Capital Group Japan Co., Ltd; in Hong Kong by Morgan Stanley Asia Limited (which accepts responsibility for its contents) and by Bank Morgan Stanley AG, Hong Kong Branch; in Singapore by Morgan Stanley Asia (Singapore) Pte. (Registration number 199206298Z) and/or Morgan Stanley Asia (Singapore) Securities Pte Ltd (Registration number 200008434H), regulated by the Monetary Authority of Singapore (which accepts legal responsibility for its contents and should be contacted with respect to any matters arising from, or in connection with, Morgan Stanley Research) and by Bank Morgan Stanley AG, Singapore Branch (Registration number T11FC0207F); in Australia to "wholesale clients" within the meaning of the Australian Corporations Act by Morgan Stanley Australia Limited A.B.N. 67 003 734 576, holder of Australian financial services license No. 233742, which accepts responsibility for its contents; in Australia to "wholesale clients" and "retail clients" within the meaning of the Australian Corporations Act by Morgan Stanley Wealth Management Australia Pty Ltd (A.B.N. 19 009 145 555, holder of Australian financial services license No. 240813, which accepts responsibility for its contents; in Korea by Morgan Stanley & Co International plc, Seoul Branch; in India by Morgan Stanley India Company Private Limited; in Indonesia by PT Morgan Stanley Asia Indonesia; in Canada by Morgan Stanley Canada Limited, which has approved of and takes responsibility for its contents in Canada; in Germany by Morgan Stanley Bank AG, Frankfurt am Main and Morgan Stanley Private Wealth Management Limited, Niederlassung Deutschland, regulated by Bundesanstalt fuer Finanzdienstleistungsaufsicht (BaFin); in Spain by Morgan Stanley, S.V., S.A., a Morgan Stanley group company, which is supervised by the Spanish Securities Markets Commission (CNMV) and states that Morgan Stanley Research has been written and distributed in accordance with the rules of conduct applicable to financial research as established under Spanish regulations; in the US by Morgan Stanley & Co. LLC, which accepts responsibility for its contents. Morgan Stanley & Co. International plc, authorized by the Prudential Regulatory Authority and regulated by the Financial Conduct Authority and the Prudential Regulatory Authority, disseminates in the UK research that it has prepared, and approves solely for the purposes of section 21 of the Financial Services and Markets Act 2000, research which has been prepared by any of its affiliates. RMB Morgan Stanley (Proprietary) Limited is a member of the JSE Limited and regulated by the Financial Services Board in South Africa. RMB Morgan Stanley (Proprietary) Limited is a joint venture owned equally by Morgan Stanley International Holdings Inc. and RMB Investment Advisory (Proprietary) Limited, which is wholly owned by FirstRand Limited. The information in Morgan Stanley Research is being disseminated by Morgan Stanley Saudi Arabia, regulated by the Capital Market Authority in the Kingdom of Saudi Arabia , and is directed at Sophisticated investors only. 

The information in Morgan Stanley Research is being communicated by Morgan Stanley & Co. International plc (DIFC Branch), regulated by the Dubai Financial Services Authority (the DFSA), and is directed at Professional Clients only, as defined by the DFSA. The financial products or financial services to which this research relates will only be made available to a customer who we are satisfied meets the regulatory criteria to be a Professional Client. 

25 

**M O R G A N   S T A N L E Y   R E S E A R C H** 

March 2016 

## **Disclosure Section (Cont.)** 

The information in Morgan Stanley Research is being communicated by Morgan Stanley & Co. International plc (QFC Branch), regulated by the Qatar Financial Centre Regulatory Authority (the QFCRA), and is directed at business customers and market counterparties only and is not intended for Retail Customers as defined by the QFCRA. 

As required by the Capital Markets Board of Turkey, investment information, comments and recommendations stated here, are not within the scope of investment advisory activity. Investment advisory service is provided exclusively to persons based on their risk and income preferences by the authorized firms. Comments and recommendations stated here are general in nature. These opinions may not fit to your financial status, risk and return preferences. For this reason, to make an investment decision by relying solely to this information stated here may not bring about outcomes that fit your expectations. 

The trademarks and service marks contained in Morgan Stanley Research are the property of their respective owners. Third-party data providers make no warranties or representations relating to the accuracy, completeness, or timeliness of the data they provide and shall not have liability for any damages relating to such data. The Global Industry Classification Standard (GICS) was developed by and is the exclusive property of MSCI and S&P. 

Morgan Stanley Research, or any portion thereof may not be reprinted, sold or redistributed without the written consent of Morgan Stanley. 23/03/16 jf 

26 

**The Americas Europe Japan Asia/Pacific** 1585 Broadway 20 Bank Street, Canary Wharf 1-9-7 Otemachi, Chiyoda-ku 1 Austin Road West New York, NY 10036-8293 London E14 4AD Tokyo 100-8104 Kowloon United States United Kingdom Japan Hong Kong +1 212 761 4000 +44 (0)20 7425 8000 +81 (0) 3 6836 5000 +852 2848 5200 

©2016 Morgan Stanley 


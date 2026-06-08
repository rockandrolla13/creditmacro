                                     Forecasting Using Principal Components
                                          From a Large Number of Predictors
James H. STOCKand Mark W. WATSON

          This article considers forecasting a single time series when there are many predictors (N) and time series observations (T). When the
          data follow an approximate factor model, the predictors can be summarized by a small number of indexes, which we estimate using
          principal components. Feasible forecasts are shown to be asymptotically efficient in the sense that the difference between the feasible
          forecasts and the infeasible forecasts constructed using the actual values of the factors converges in probability to 0 as both N and T
          grow large. The estimated factors are shown to be consistent, even in the presence of time variation in the factor model.
          KEY WORDS:        Factor models; Forecasting; Principal components.



                        1. INTRODUCTION                                         classic factor analysis model. In our macroeconomic forecast-
                                                                                ing application, these assumptions are unlikely to be satisfied,
   This article considers forecasting one series using a large
                                                                                and so we allow the error terms to be both serially corre-
number of predictor series. In macroeconomic forecasting, for
                                                                                lated and (weakly) cross-sectionally correlated. In this sense,
example, the number of candidate predictor series (N) can be
very large, often larger than the number of time series obser-                  (1) is a serially correlated version of the approximate factor
vations (T) available for model fitting. This high-dimensional                  model introduced by Chamberlain and Rothschild (1983) for
problem is simplified by modeling the covariability of the                      the study of asset prices. To construct forecasts of y,,,, we
series in terms of a relatively few number of unobserved latent                 form principal components of {X,}T=, to serve as estimates of
factors. Forecasting can then be carried out in a two-step pro-                 the factors. These estimated factors, together with w,, are then
cess. First, a time series of the factors is estimated from the                 used in (2) to estimate the regression coefficients. The fore-
predictors; second, the relationship between the variable to be                 cast is constructed as j,,, = &PT +F,w,, where                      p,, p,,
forecast and the factors is estimated by a linear regression. If                and pT are the estimated coefficients and factors.
the number of predictors is large, then precise estimates of the                   This article makes three contributions. First, under general
latent factors can be constructed using simple methods even                     conditions on the errors discussed in Section 2, we show that
under fairly general assumptions about the cross-sectional and                  the principal components of Xi are consistent estimators of
temporal dependence in the variables. We estimate the factors                   the true latent factors (subject to a normalization discussed
using principal components, and show that these estimates are                   in Sec. 2). Consistency requires that both N and T + co,
consistent in an approximate factor model with idiosyncratic                    although there are no restrictions on their relative rates of
errors that are serially and cross-sectionally correlated.                      increase. Second, we show that the feasible forecast, j,,,,
   To be specific, let y, be the scalar time series variable to be              constructed from the estimated factors together with the esti-
forecast and let Xi be a N-dimensional multiple time series                     mated coefficients converge to the infeasible forecast that
of candidate predictors. It is assumed that (Xi, y,,,) admit a                  would be obtained if the factors and coefficients were known.
factor model representation with r common latent factors F,,                    Again, this result holds as N , T + co. Thus the feasible fore-
                                                                                cast is first-order asymptotically efficient. Finally, motivated
                             X, = AF,     + e,                           (1)    by the problem of temporal instability in macroeconomic fore-
and                                                                             casting models, we study the robustness of the consistency
                     Yr+h   = PkFr +PLwt + Et+h                          (2)    results to time variation in the factor model. We show that
                                                                                these results continue to hold when the temporal instability
where e, is a N x 1 vector idiosyncratic disturbances, h is the                 is small (as suggested by empirical work in macroeconomics)
forecast horizon, w, is a m x 1 vector of observed variables                    and weakly cross-sectionally dependent, in a sense that is
(e.g., lags of y,), that together with F, are useful for forecasting
                                                                                made precise in Section 3.
y,+,, and st+,is the resulting forecast error. Data are available
                                                                                   This article is related to a large literature on factor anal-
for {y,, X,, w,}:,,   and the goal is to forecast y,+,.
                                                                                ysis and a much smaller literature on forecasting. The liter-
   If the idiosyncratic disturbances e, in (1) were cross-
                                                                                ature on principal components and classical factor models is
sectionally independent and temporally iid, then (1) is the
                                                                                large and well known (Lawley and Maxwell 1971). Sargent
                                                                                and Sims (1977) and Geweke (1977) extended the classical
   James H. Stock is Professor, Kennedy School of Government, Harvard           factor model to dynamic models, and several researchers have
University, Cambridge, MA 02138, and the National Bureau of Economic            applied versions of their dynamic factor model. In most appli-
Research (E-mail: james-stock@harvard.edu). Mark W. Watson is Profes-           cations of the classic factor model and its dynamic general-
sor, Department of Economics and Woodrow Wilson School, Princeton
University, Princeton, NJ 08540, and the National Bureau of Economic            ization, the dimension of X is small, and so the question of
Research (E-mail: mwatson@princeton.edu). The results in this article origi-
nally appeared in the paper titled "Diffusion Indexes" (NBER Working Paper
6702, August 1998). The authors thank the associate editor and referees,
Jushan Bai, Michael Boldin, Frank Diebold, Gregory Chow, Andrew Harvey,                                  O 2002 American Statistical Association
Lucrezia Reichlin, Ken Wallis, and Charles Whiteman for helpful discussions                        Journal of the American Statistical Association
and/or comments, and Lewis Chan, Piotr Eliasz, and Alexei Onatski for skilled                December 2002, Vol. 97, No. 460, Theory and Methods
research assistance. This research was supported in part by National Science                                    DO1 10.1 1981016214502388618960
Foundation grants SBR-9409629 and SBR-9730489.
1168                                                                     Journal of the American Statistical Association, December 2002

consistent estimation of the factors is not relevant. However,     by associating A with the ordered orthonormal eigenvectors of
several authors have noted that with large N, consistent esti-     (NT)-I xT=, AF,F:A' and {F,}~=,with the principal compo-
mation is possible. Connor and Korajczyk (1986, 1988, 1993)        nents of {AF,}:=,. The diagonal elements of ZFF correspond
discussed the problem in a static model and argue that the fac-    to the limiting eigenvalues of (NT)-I    cT=,  AF,F,'A1. For con-
tors can be consistently estimated by principle components as      venience, these eigenvalues are assumed to be distinct. If they
N -t co even if the errors terms are weakly cross-sectionally      were not distinct, then the factors could only be consistently
correlated. Forni and Reichlin (1996, 1998) and Forni, Hallin,     estimated up to an orthonormal transformation.
Lippi, and Reichlin (1999) discussed consistent (N, T + co)           Assumption Fl(b) allows the factors to be serially corre-
estimation of factors in a dynamic version of the approximate      lated, although it does rule out stochastic trends and other pro-
model. Finally, in a prediction problem similar to the one con-    cesses with nonconstant uncondititional second moments. The
sidered here, Ding and Hwang (1999) analyzed the properties        assumption also allows lags of the factors to enter the equa-
of forecasts constructed from principal components in a set-       tions for x,, and y,+, . A leading example of this occurs in the
ting with large N and T. Their analysis is conducted under         dynamic factor model
the assumption that error process {e,,      is cross-sectionally
and temporally iid, an assumption that is inappropriate for
economic models and when interest focuses on multiperiod
                                                                   and
forecasts. We highlight the differences between our results and
those of others later in the article.                                              Yt+h   = Ps(L)'fr + P:.wI + &i+h,               (4)
   The article is organized as follows. Section 2 presents the     where A,(L) and P f ( L ) are lag polynomials is nonnegative
model in more detail, discusses the assumptions, and presents      powers of the lag operator L. If the lag polynomials have
the main consistency results. Section 3 generalizes the model      finite order q, then (3)-(4) can be rewritten as (1)-(2) with
to allow temporal instability in the factor model. Section 4       F, = (f( fk, . . . f(-,)', and Assumption Fl(b) will be satisfied
examines the finite-sample performance of these methods in a       if the f, process is covariance stationary.
Monte Carlo study, and Section 5 discusses an application to          In the classical model, the errors or "uniquenesses" are
macroeconomic forecasting.                                         assumed to be iid and normally distributed. This assumption is
           2.   THE MODEL AND ESTIMATION                           clearly inappropriate in the macroeconomic forecasting appli-
                                                                   cation, because the variables are serially correlated, and many
2.1 Assumptions                                                    or the variables (e.g., alternative measures of the money sup-
   As described in Section 1, we focus on a forecasting sit-       ply) may be cross-correlated even after the aggregate factors
uation in which N and T are both large. This motivates our         are controlled for. We therefore modify the classic assump-
asymptotic results requiring that N , T + co jointly or, equiv-    tions to accommodate these complications.
alently, that N = N(T) with lim,,,     N(T) + co. No restric-        Assumption M I (Moments of the Errors e,)
tions on the relative rates of N and T are required.
   The assumptions about the model are grouped into assump-
tions about the factors and factor loading, assumptions about
the errors in the (I), and assumptions about the regressors and         Let e,, denote the zth element of e,; then
errors in (2).                                                       b. E(e,telr) = rll,r , limN+, SUP, N-' CLl C,N_lI riJ 1 l <   "9

                                                                        and
  Assumption Fl (Factors and Factor Loading).
                                                                     C. 1lmN-m SUP, 5 N-I    EL1 Ey=1   lcov(e,sei,, e,seJ,)l < CQ.
  a. (A'AIN) -+I,.                                                    Assumption Ml(a) allows for serial correlation in the el,
  b. E(F,FI1)= C,,, where Z F F is a diagonal matrix with          processes. As in the approximate factor model of Chamber-
     elements a,,> a, > 0 for i < j .                              lain and Rothschild (1983) and Connor and Korajczyk (1986,
  C. Ihi,,,l 5 h < M.
                                                                   1993), Assumption Ml(b) allows (e,,} to be weakly corre-
  d. T-I C ,F,F; i;X F F .                                         lated across series. Forni et al. (1999) also allowed for serial
   Assumption F1 serves to identify the factors. The nonsin-       correlation and cross-correlation with assumptions similar to
gular limiting values of (A'AlN) and ZFFimply that each of         Ml(a)-(b). Normality is not assumed, but Ml(c) limits the
the factors provides a nonnegligible contribution to the aver-     size of fourth moments.
age variance of x,,, where x,,is the ith element of X, and            It is assumed that the forecasting equation (2) is well
the average is taken over both i and t. Moreover, because          behaved in the sense that if {F,} were observed, then ordi-
AF, = ARR-'F, for any nonsingular matrix R, a normaliza-           nary least squares (OLS) would provide a consistent estimator
tion is required to uniquely define the factors. Said differ-      of the regression coefficients. The specific assumption is as
ently, the model with factor loadings AR and factors R-IF,         follows.
is observationally equivalent to the model with factor load-         Assumption YI (Forecasting Equation). Let z, = (F: w:)'
ings A and factors F,. Assumption Fl(a) restricts R to be          and p = (pk PL,)'. Then the following hold:
orthonormal, and this together with Assumption Fl(b) restricts
R to be a diagonal matrix with diagonal elements of * I . This       a. E(z,zi) = X I = ['FF   ' ~ ~ a' positive
                                                                                          x w ~xu,io    1        definite matrix.
identifies the factors up to a change of sign. Equivalently,
Assumption F l provides this normalization (asymptotically)
Stock and Watson: Forecasting From Many Predictors                                                                                    1169

                                                                       that converges in probability to 0. Because Assumption F1
                                                                       does not identify the sign of the factors, the theorem is stated
                                                                       in terms of sign-adjusted estimators.

Assumptions Yl(a)-(c) are a standard set of conditions that               Theorem 1. Let Si denote a variable with value of f1, let
imply consistency of OLS from the regression of y,+, onto              N , T + co, and suppose that F1 and MI hold. Suppose that
(Fi wi). Here F, is not observed, and the additional assump-           k factors are estimated, where k may be 5 or > r, the true
tions are useful for showing consistency of the OLS regres-            number of factors. Then Si can be chosen so that the following
sion coefficients in the regression of y,,, onto
resulting forecast of y,+,.
                                                   (e
                                                  w:) and the          hold:
                                                                                                                            P


2.2 Estimation                                                                                       -
                                                                         a. For i = 1 , 2 , . . . , r, T-' C L , ( S ~ E ,-
                                                                                                              P
                                                                         b. For i = 1 , 2 , . . . , r , SiFl,-+ Fir.
                                                                                                                            -+ 0.



   In "small-N" dynamic factor models, forecasts are gener-              c. F o r i = r + l , . . . , k, T - ' C ~ ~ ~ $ O .
ally constructed using a three-step process (see, e.g., Stock
                                                                          The details of the proof are provided in the Appendix;
and Watson 1989). First, parametric models are postulated for
                                                                       here we offer only a few remarks to provide some insight
the joint stochastic process {y,,,, X,, w,, e,}, and the sample
                                                                       into problem and the need for the assumptions given in
data {y,,,, X,, w,}:_;~ are used to estimate the parameters of
                                                                       the preceding section. The estimation problem would be
this process, typically using a Gaussian Maximum likelihood
estimator (MLE). Next, these estimated parameters are used             considerably simplified if it happened that A were known,
in signal extraction algorithms to estimate the unknown value          because then F, could be estimated by the least squares
of F,. Finally, the forecast of y,,, is constructed using this         regression of {xit)El onto {Ai)E1.Consistency of the result-
                                                                                                                                 A


estimated value of the factor and the estimated parameters.            ing estimator would then be studied by analyzing F, - F, =
When N is large, this process requires estimating many param-          (A'A/N)-' (N-' Elhie,,). Because N -+ oo,(AfA/N) -+ I,
eters using iterative nonlinear methods, which can be compu-           [by Fl(a)], and N-'   xi   hiei, 5 0 [by Ml(a) and Fl(c)], the
tationally prohibitive. We therefore take a different approach         consistency of       would follow directly. Alternatively, if F
and estimate the dynamic factors nonparametrically using the           were known, then A, could be estimated by regression {xit}~=,
method of principal components.                                        onto {F,}:, , and consistency would be studied analyzing
   Consider the nonlinear least squares objective function,            (T-' C ,F,F:)-'T-' ErFreir,as T + oo in a similar fashion.
                                                                       Because both F and A are unknown, both N and T + co are
                                                                       needed, and as it turns out, the proof is more complicated than
                                                                       these two simple steps suggest. The strategy that we have used
                      -
written as a function of hypothetical values of the factors (F)
and factor loadings (A), where F= ( 4 F 2 . . . FT)' and Xi is the
                                                                       is to show that the first r eigenvectors of (NT)-'X'X behave
                                                                       like the first r eigenvectors of (NT)-'A'F'FA (Assumption
ith row of X. Let FI and ;  idenote the minimizers of v(F, X).         M1 is critical in this regard), and then show that these eigen-
After concentrating out F, minimizing (5) is equivalent to             vectors can be used to construct a consistent estimator of F
maximizing ~ ~ [ X ' X ' X Xsubject
                             ]       to A'A/N = I,, where X is         (Assumption F1 is critical in this regard).
the T x N data matrix with tth row Xi and tr(.) denotes the               The next result shows that the feasible forecast (constructed
matrix trace. This is the classical principal components prob-         using the estimated factors and estimated parameters) con-
lem, which is solved by setting ;   iequal to the eigenvectors of      verges to the optimal infeasible forecast and thus is asymptoti-
X'X corresponding to its r largest eigenvalues. The resulting          cally efficient. In addition, it shows that the feasible regression
principal components estimator of F is then                            coefficient estimators are consistent.
                                                                          The result assumes that the forecasting equation is estimated
                                                                       using the k = r factors. This is with little loss of generality,
                                                                       because there are several methods for consistently estimating
   Computation of F requires the eigenvectors of the N x N             the number of factors. For example, using analysis similar to
matrix X'X; when N > T, a computationally simp@ approach               that in Theorem 1, Bai and Ng (2001) constructed estimators
uses the T x T matrix XX'. By concentrating ou@, minimiz-              of r based on penalized versions of the minimized value of
ing (5) is equivalent to maximizing ~ ~ [ F ( x x ' ) F ] subject
                                                          ,       to   (5), and in an earlier version of this article (Stock and Watson
FFIT= I, which yields the estimator, say ?, which is the                1998a), we developed a consistent estimator of r based on the
            -
matrix of the first r eigenvectors of XX'. The column spaces
of F^ and F are equivalent, and so for forecasting purposes
                                                                       fit of the forecasting equation (2).

they can be used interchangeably, depending on computational              Theorem 2. Suppose that Y1 and the conditions of The-
                                                                       orem 1 hold. Let @, and       fi,
                                                                                                      denote the OLS estimates of
convenience.

2.3   Consistent Estimation of Factors
                                                                       @, and @, from the regression of { y , , , } ~ . onto
                                                                       Then the following conditions hold:
                                                                                                                                {c,
                                                                                                                             w,}Y_;h.

      and Forecasts (1) and (2)
   The first result presented in this section shows that the prin-
                                                                                    +
                                                                         a. (fi>F^, fiU,wT> - (P>FT +@mwT) + 0.
                                                                                                                   P


cipal component estimator is pointwise (for any date t) con-             b.  p,,
                                                                               - @,     0 and Si (defined in Theorem 1) can be cho-
sistent and has limiting mean squared error (MSE) over all t                sen so that SipiF- Pi,     0 for i = I , . . . , r.
1170                                                                          Journal of the American Statistical Association, December 2002

  The theorem follows directly from Theorem 1 together with               b. The initial values of the values loadings satisfy
Assumption Y1. The details of the proof are given in the                     N-I CiA:,Aio= AbA,,/N 4 I, and sup,,, IAij,,\ <                         A,
Appendix.                                                                    where Aij,, is the jth element of A,.
         3. TIME-VARYING FACTOR LOADINGS                                  As discussed earlier, Assumption F2(a) makes the amount
                                                                       of time variation small. Assumption F2(b) means that the ini-
   In practice, when macroeconomic forecasts are constructed
                                                                       tial value of the factor loadings satisfy the same assumptions
using many variables over a long period, some degree of tem-
                                                                       as the time-invariant factor loading of the preceding section.
poral instability is inevitable. In this section we model this
                                                                          The next assumption limits the dependence in i f , . This
instability as stochastic drift in the factor loadings, and show
that if this drift is not too large and not too dependent across       assumption is written in fairly general form, allowing for some
series (in a sense made precise later), then the results of Theo-      dependence in the random variables in the model.
rems 1 and 2 continue to hold. Thus the principal components             Assumption M2. Let l,,,,denote the mth element of lit.
estimator and forecast are robust to small and idiosynchratic          Then the following hold:
shifts in the factor loadings.
   Specifically, replace the time-invariant factor model (1) with



and
                        'it   = 'it-1    +gi~lir                @I
for i = 1, . . . , N and t = 1, . . . , T, where g,, is a scalar and
Lit is an r x 1 vector of random variables. This formulation
implies that factor loadings for the ith variable shift by an
amount, giTli,,in time period t. The assumptions given in this
section limit this time variation in two ways. First, the scalar
                                        --
giTis assumed to be small [g,, Op(T-I)] which is consistent
with the empirical literature in macroeconomics that estimates
the degree of temporal instability in macroeconomic relations

means that A,, -Aio    -
(Stock and Watson 1996, 1998b). This nesting implies that
                           O,(T-'/~). Second, litis assumed to
have weak cross-sectional dependence. That is, whereas some
of the x variables may undergo related shifts in a given period,       This assumption essentially repeats Assumption M1 for
wholesale shifts involving a large number of the x's are ruled         the components of the composite error term a,, in (9).
out. Presumably such wholesale shifts could be better repre-           To interpret the assumption, consider the leading case in
sented by shifts in the factors rather than in the factor load-        which the various components { E , } , {F,}, {ei,}, and {lit}
ings. In any event, this section shows that when these assump-         are independent and have mean 0. Then, assuming that
tions hold (along with technical assumptions given later), then        the F, have finite fourth moments, and given the assump-
the instability does not affect the consistency of the principal       tions made in the last section, Assumption M2 is satis-
                                                                                                     T-s
components estimator of F,.                                            fied if (a) limT+m         Cu=l-ss u ~ i , mIE(lis,/lis+u,m)l < ~ 2 3 ;
   To motivate the additional assumptions used in this section,        (b) lim~,m N-' Ci Cj s'JPi.s,uIE(lis,/lju.m)I <                            and (c)
rewrite (7) as                                                                                       m. {tkl;=, I ~ ~ ~ ( l il i tt2 .,i Z, ' il j ~
                                                                       l i m ~ + mN-' Ci Cj SUP(ikl;=,.                                            tj,
                                                                       l,,,lA)l< co, which are the analogs of the assumptions in M1
                                                                       applied to the [ error terms.
                                                                           These two new assumptions yield the main result of this
                +                            +
where a i r= eit (A,, - Aio)F, = eit giTC:=, lL!sF,.  This equa-       section, which follows.
tion has the same general form of the time-invariant factor
model studied in the last section, with A, and a,, in (9) replac-         Theorem 3. Given Fl(b), Fl(d), F2, M I , and M2, the
ing A, and e,, in the time-invariant model. This section intro-        results of Theorems 1 and 2 continue to hold.
duces two new sets of assumptions that imply that Aio and a,,
                                                                          The proof is given in the Appendix.
in (9) satisfy the assumptions concerning hi and e,, from the
preceding section. This means that the conclusions of Theo-
                                                                                         4.    MONTE CARL0 ANALYSIS
rems 1 and 2 will continue to hold for the time-varying factor
model of this section.                                                    In this section we study some of the finite-sample proper-
   The first new assumption is as follows.                             ties of the principal components estimator and forecast using
                                                                       a small Monte Carlo experiment. The framework used in the
  Assumption F2.
                                                                       preceding two sections was quite rich, allowing for distributed
  a. g,, is independent of F,, ej,, and lj,for all i, j, and t         lags of potentially serially correlated factors to enter the x and
     and supi,j.k.m T[E(lgrTgjTgkTgmT1)1141< < co            i,        y equations, error terms that were conditionally heteroscedas-
     j , k, and m.                                                     tic and serially and cross-correlated, and factor loadings that
Stock and Watson: Forecasting From Many Predictors                                                                                   1171


evolved through time. The design used here incorporates all             the Monte Carlo experiment are N, T, ?, q, k, T, a, b, c, S,,
of these features, and the data are generated according to              and 6,.
                                                                           The results are summarized by two statistics. The first statis-
                                                                        tic is a trace R2 of the multivariate regression of FI onto F ,



                                                                        where 2 denotes the expectation estimated by averaging the
                                                                        relevant statistic over the Monte Carlo repetitions and PF =
                                                                                                                        P
                                                                        F(F'F)-IF'. According to Theorem 1, R;, -+1.
                                                                           The second statistic measures how close the forecast based
                                                                        on the estimated factors is to the infeasible forecast based on
and
                                                                        the true factors,
                   a: = So+S,U:~, +Slv;,-l,                     (15)
where i = 1, . . . , N, t = 1, . . . , T, f, and A:,, are J x 1, and
the variables {Jijt}, {uj,}, and {77il}are mutually independent                                     P
iid N(0, 1) random variables. Equation (10) is dynamic factor           Because jT+llT   - jT+,/,  -+ 0 when k = r from Theorem 1,

model with q lags of J factors that, as shown in Section 2, can         S;,j, should be close to 1 for appropriately large N and T. S;,?
be represented as the static factor model (1) with r = J ( l q) +       is computed for several choices of i . First, as a benchmark,
                                                                        results are shown for i = r . Second, F is formed using three
factors. From (12), the factors evolve as a vector autoregres-
sive [VAR(l)] model with common scalar autoregressive (AR)              of the information criteria suggested by Bai and Ng (2001).
parameter a. From (13), the error terms in the factor equation                                                              +
                                                                        These criteria have the form ICp(k) = l n ( c ) kg(T, N),
are serially correlated, with an AR(1) coefficient of a, and            where f;, is the minimized value of the objective function (5)
cross-correlated, [with spatial moving average [MA(1)] coeffi-          for a model with k factors and gj(T, N) is a penalty function.
cient b]. The innovations wit are conditionally heteroscedastic         Three of the penalty functions suggested by Bai and Ng are
and follow a GARCH(1, 1) process with parameters So, S,,                used:
and 6, [see (14) and (15)l. Finally, from (1 I), the factor load-
ings evolve as random walk, with innovation standard devia-
tion proportional to c.
   The scalar variable to be forecast is generated as

                                                                        and


                                              -
where L is an J x 1 vector of 1s and E,+, iid N(0, 1) and is
independent of the other errors in (10)-(15).
   The other design details are as follows. The initial factor          where C;, = min(N, T), resulting in criteria labeled IC,,,
loading matrix, A,, was chosen as a function of RZ, the frac-           IC,,, and ICp3. The minimizers of these criteria yield a con-
tion of the variance of xio explained by Fo.The value of R?             sistent estimator of r, and interest here focuses on their rela-
was chosen as an iid random variable equal to 0 with proba-             tive small-sample accuracy. Finally, results are shown with i
bility T and drawn from a uniform distribution on [.1, .8] with         computed using the conventional Akaike information criterion
probability 1 - T. A nonzero value of .rr allows for the inclu-         (AIC) and Bayes information criterion (BIC) applied to the
sion of x's unrelated to the factors. Given this value of R;, the       forecasting equation (2).
initial factor loading was computed as Aijo = A* (R;) hijo, where
                               -
A*(R;) is a scalar and hijo iid N(O,1) and independent of
{qi,, lij, u,}. The initial values of the factors were drawn from
                                                                           The results are summarized in Table 1. Panel A presents
                                                                        results for the static factor model with iid errors and factors
                                                                        and with large N and T(N, T > 100). Panel B gives corre-
their stationary distribution. The parameter So was chosen so           sponding results for small values of N and T(N, T 1 50).
that the unconditional variance of vi, was unity.                       Panel C adds irrelevant xi,'s to the model (T > 0). Panel D
   Principal components were used to estimate k factors, as             extends the model to idiosyncratic errors that are serially
discussed in Section 2.2. These k estimated factors were                correlated, cross-correlated, conditionally heteroscedastic, or
used to estimate r (the true number of factors) using meth-             some combination of these. Panel E considers the dynamic
ods described later, and the coefficients P in the forecasting          factor model with serially correlated factors and/or lags of the
regression (2) were estimated by the OLS coefficients in the6           factors entering' X,. Finally, panel F gives time-varying factor
regression of y,+, onto F,,, j = 1, . . . , i , t = 1, . . . , T - 1,
                           A

                                                                        loadings.
where F is the estimated ntm_ber of factors. The out-of-sample             First, consider the results for the static factor model shown
forecast is jT+,/,  = c:=, PjFjT. For comparison purposes, the
                                                -                       in panel A. The values of R;, exceed .85 except when many
infeasible out-of-sample forecast jT+,/,     = PIFTwas also com-        redundant factors are estimated. The smallest value of R;,~
               p
puted, where is the OLS estimator obtained from regress-                is .69, which obtains when N and T are relatively small
ing y,,, onto F,, t = 1, . . . , T - 1. The free parameters in          (N = T = 100) and there are 10 redundant factors ( r = 5 and
Stock and Watson: Forecasting From Many Predictors                                                                      1173

                                                           section we describe a forecasting experiment for the Federal
k = 15). The values of s:,? generally exceed .9, and this is
true for all methods used to estimate the number of fac-   Reserve Board's Index of Industrial Production, an important
tors. The only important exception is when k = r = 10 and  monthly indicator of macroeconomic activity. The variables
                                                           making up X, are 149 monthly macroeconomic variables rep-
N = T = 100; in this case, IC,, and IC,, perform poorly. The
                                                           resenting several different facets of the macroeconomy (e.g.,
penalty factors for IC,, and ICPz are larger than for IC,, [e.g.,
when T = N, g,(N, T ) = 2g3(N, T ) ] , and apparently theseproduction, consumption, employment, price inflation, inter-
large penalties lead to serious underfitting.              est rates). We have described the variables in detail in earlier
    Performance deteriorates somewhat is small samples, as work (Stock and Watson 2002). The sample period is January
shown in panel B. With only two factors, Si. is near .9 for1959-December 1998. Principal components of X, were used
                                                           to construct forecasts of y,+,, = ln(lP,+,,/IP,), where IP, is
k = r, so that the forecasts perform nearly as well as the infea-
sible forecasts. When k is much larger than r (k = 10 and  the index of industrial production for date t . These 12-month-
r = 2), IC,, performs poorly because of overfitting. particu-
                                                           ahead forecasts were constructed in each month starting in
larly when T is very small ( T = 25). All of the methods dete-
                                                           1970:l and extending through 1997:12, using previously avail-
                                                           able data to estimate unknown parameters and factors.
riorate when there are five factors; for example, when T = 25,
the values of S,'2,j are closer to .6.                         To simulate real-time forecasting, we used data dated T and
                                                           earlier in all calculations for constructing forecasts at time T.
     Panel C suggests that including irrelevant series has little
                                                           Thus for example, to compute the forecast in T = 1970: 1, the
effect on the estimators and forecasts when N and T are large.
                                                           variables making up X , were standardized using data from
Results are shown for n- = .25 (so that 25% of the series are
unrelated to the factors) and N = 333. The results for the t = 1959: 1-1970: 1, and principal components were computed.
                                                           These estimated values of F, were used together with Y , + , ~ for
models with five factors are nearly identical to the results in
panel A with the same number of relevant series (N = 250). t = 1959: 1-1969: 1 to estimate P in (2). Model selection with
The results for 10 factors are also similar to those in panel
                                                           k = 10 based on IC,,, IC,,, IC,,, AIC, and BIC were used
 A, although panel C shows some deterioration of the forecasts
                                                           to determine the number of factors to include in the regres-
 using IC,, and IC,, .                                     sion. Finally, the forecasts constructed in T = 1970: 1 were
                                                           formed as ~,+,,,,
     From panel D, moderate amounts of serial or spatial cor-                   =BE. This process was repeated for 1970:2-
 relation in the errors have little effect on the estimators and
                                                            1997: 12.
 forecasts. For example, on the one hand, when moderate serial We also computed forecasts using four other methods: a
 correlation is introduced by setting a = .5, the results in the
                                                           univariate autogression in which y,+,, was regressed on lags
 table are very similar to the results with a = 0; similarly, there
                                                           of ln(lP,/IP,-,), a vector autoregression that included the
 is little change when spatial correlation is introduced by sett-
                                                           rate of price inflation and short-term interest rates in addi-
 ting b = 1.0. On the other hand, some deterioration in perfor-
                                                            tion to the rate of growth of the industrial production index,
 mance occurs when the degree of serial correlation is largea leading-indicator model in which y,,,, was regressed on
 (compare the entries with a = .9 to those with a = .5). Condi-
                                                            11 leading indicators chosen by Stock and Watson (1989)
 tional heteroscedasticity has no apparent effect on the perfor-
                                                            as good predictors of aggregate macroeconomic activity; and
 mance of the estimator and forecasts.                      an autoregressive-augmented principal components model in
     From panel E, introducing lags of the factors has little effect
                                                            which y,,,, was regressed on the estimated factors and lags
 on the quality of the estimators and forecasts: the results with
                                                            of ln(lP,/IP,-,). We gave details of the specification, includ-
 ? = 5 and q = 1 (so that r = 10) are essentially identical to the
                                                            ing lag length choice and exact description of the variables, in
 static factor model with 10 factors. However, a high degree of
                                                            earlier work (Stock and Watson 2002).
 serial correlation in the factor process ( a = .9) does result in
                                                               Table 2 shows the MSE of the resulting forecasts, where
 some deterioration of performance. For example, when T =   we have shown each MSE relative to the MSE for the univari-
  100, N = 250, and r = 5, R2^ = .97 in the static factor model
                                                            ate autoregression. The first three rows show results from the
                                F,F
  ( a = O), and this falls to .89 when a = .9.              benchmark AR, VAR, and leading indicator models. The next
     Finally, panel F shows the effect of time variation on the
                                                            row shows the results for the principal components forecasts,
 factor loadings in isolation and together with other compli-
                                                            with the number of factors determined by IC,,. (The results
 cations. There appears to be only moderate deterioration offor the other selection procedures are similar and thus are not
 the forecast performance even for reasonably large amount of
                                                            reported.) This is followed by principal components forecasts
 temporal instability (e.g., S;, remains high even as the param-
                                                            using a fixed number of factors (k = 1-k = 4). Finally, the last
 eter governing time-variation increases from 0 to 10). How-row shows the principal components forecasting model (with
 ever, when all of the complications are present (i.e., serially
                                                             r estimated by IC,,) augmented with BIC-selected lags of the
 correlated dynamic factors, k > r, serial and cross-correlated
                                                            growth rate of industrial production. (Again, results for other
 heteroscedastic errors, time-varying factor loading, and a large
                                                            selection procedures are very similar and are not reported.)
 number of unrelated x's), forecast performance deteriorates   Both the leading indicator and VAR models perform slightly
  significantly, as shown in the last few entries in panel F.
                                                            better than the univariate AR in this simulated out-of-sample
                                                            experiment. However, the gains are not large. The factor mod-
              5. AN EMPIRICAL EXAMPLE
                                                            els offer substantial improvement. The results suggest that
   In related empirical work we have applied factor mod- nearly all of the forecasting gain comes from the first two
els and principal components to forecast several macroeco- or three factors and that once these factors are included, no
nomic variables (see Stock and Watson 1999, 2002). In this additional gain is realized from including lagged values of IP
1174                                                                                                    Journal of the American Statistical Association, December 2002

                                                                                                The term N-'              xi
                                                                                                                    rli,, is O(1) from Assumption M l ( b ) (because
    Table 2. Simulated Out-of-Sample Forecasting Results Industrial
                    Production, 12-Month Horizon                                                N-'   xi
                                                                                                       rii,,5 N - I             x,                          -
                                                                                                                         El 1ri1,,l O ( 1 ) ) . SO it suffices that the sec-
                                                                                                ond term converges to 0 in probability. Now
Forecast method                                                          Relative MSE

Univariate autoregression
Vector autogression
Leading indicators
Principal components
Principal components, k = 1
Principal components, k = 2
Principal components, k = 3
Principal components, k = 4
Principal components, AR
Root MSE, AR model

NOTE: For each forecast method, this table shows the ratio of the MSE of the forecast made
by the method for that row to the MSE of a univariate autoregresslve forecast with lag length
selected by the BIC. The final line presents the root MSE for the autoregressive model in       by Assumption Ml(c). Thus N-' x , ( e f , - r,,, ,) 4 0.
native (decimal growth rate) units at an annual rate.




                                                                                                   Proof.
growth. We have already reported similar results for other real
macroeconomic variables (Stock and Watson 2002).
                                                                                                           ( N 2 T ) - ' y'e'ey = (N2T)-I
                                                                                                                                                                    l
                                                                                                                                                                                x yi yjerrejr
                                                                                                                                                                                 j

                               6.     DISCUSSION
   This article has shown that forecasts of a single series
                                                                                                                                         =     N - ~ EyiYj
                                                                                                                                                      C T-I Cei,ejt
                                                                                                                                                        i       I
based on principal components of a large number of predic-                                                                                                                               112
tors are first-order asymptotically efficient as N, T +        for
general relationships between N and T in the context of an                                                                                                  i       I

approximate factor model with dynamics. The Monte Carlo
results suggest that these theoretical implications provide a
useful guide to empirical work in datasets of the size typi-
cally encountered in macroeconomic forecasting. The empiri-
cal results summarized here and reported in more detail else-
                                                                                                but N - 2                  Y;Y; = ( Y , Y I N ) 2 ,and for all                                         E   r, ( y , y l N ) = I.
                                                                                                Thus
where suggest that these methods can contribute to substantial
improvement in forecasts beyond conventional models using
                                                                                                            sup(N2T)-If e ' e y 5
a small number of variables.                                                                                YE,
   Several methodologic issues remain. One issue is to explore
estimation methods that might be more efficient in the pres-                                    NOW
ence of heteroscedastic and serially correlated uniquenesses.
Another is to develop a distribution theory for the estimated
factors that goes beyond the consistency results shown here
                                                                                                      N-2    xx   i   j
                                                                                                                          ( ~ - 1   x1
                                                                                                                                             e i r e l r ) 2= N - Z T - ~            xxxx
                                                                                                                                                                                     i         j       r   s
                                                                                                                                                                                                               eileiselrelx


and provides measures of the sampling uncertainty of the esti-
mated factors. A third theoretical extension is to move beyond                                  and
the I ( 0 ) framework of this article and to introduce strong per-
sistence into the series; for example, by letting some of the
factors have a unit autoregressive root, which would permit
                                                                                                      E[N-'T-Z ~ ~ ~ ~ e i r e t x ' j r e l s
                                                                                                                            I   J        '      S                           I
some of the observed series to contain a common stochastic                                                 = N - ~ Ti -j ~r Cs C C C Y ~ . ~ , ~ Y , , ~ , ~
trend.
                                                                                                                 fW2T2
                                                                                                                     i
                                                                                                                                    C Cj Cr Cs E [ ( e i l e t s Yi,t,s)(ejtejs- Yj.r.s)I>
                                                                                                                                                                                 -
               APPENDIX: PROOFS OF THEOREMS
   W e begin with some notation.                                                                where Yi,r,s = E(eiretx).
   Define 1,= ELl and          = CT=I.                                                          The first term is
   Let y denote an N x 1 vector and let r = { y l y l y / N= I } , R ( y ) =
N-~T-I  y' CrX,X; y, and R * ( y ) = N - ~ T - Iy' C ,AFtF;A1y.
   W e begin by collecting a set o f results used in the proof.                                        f     U
                                                                                                                                Yi,r,                (N-I           x Yj,r,r+u) T - ~ x YN,l(u)2>
                                                                                                                                                                        I
                                                                                                                                                                                                   =
                                                                                                                                                                                                               f   U



Results (R1)-(R19) Hold Under Assumptions F1 and M I                                            because (N-I X i y ,,,,,+,) = N-'E     ei,e,,,+, = y,,,(u) defined in   xi
             xief, - 0,(1).
    ( R l ) N-'                                                                                 MI (a). Now the absolute summability o f 1 y,, ,( u )1 in Ml(a) implies
                                                                                                square summability, so that lim,,,      sup, 1,y , , , ( ~ ) <
                                                                                                                                                             ~ co. This
   Proof. N - ' xi e: = N - ' x, rli,,+ N-I x , ( e ? ,- rii,,).                                implies that N - ' T - ~ El E j El yi,r,sY , , , , ~-+ 0.   xs
Stock and Watson: Forecasting From Many Predictors                                                                                                                             1175

The second term is                                                                          Proof. I s u ~ , , r R ( ~ ) - s u ~ , , r R * ( ~ )~l s u p , , r I R ( Y ) - R * ( Y ) I ~ O .
                                                                                          where the first inequality follows by the definition of the sup and the
                                                                                          convergence follows from (R6).


                                                                                             Proof. Write A'AIN = (A'A/N)'/~(A'A/N)'/~'to denote the
                                                                                          Choleski factorization of A'AIN. Let y be represented as y =
by Assumption MI (c).                                                                                           +
                                                                                          A ( A ' A / N ) - ' / ~ ~ V, where V'A = 0. Note that y'y/N = 6'6                          +
                                                                                          V'VIN, so that for all y G r, 6'6 5 1. Thus we can write
   (R3) Let q, denote a sequence of random variables with
        T-' C, q: -- OP(1). Then                                                                                                       = B11
                                                                                              sup R*(y) = sup ~'(A'A/N)'/~'(F'F/T)(A'A/N)'/~~                                    3

                                                                                              YE,        6.6'651

                                                                                          where &,, is the largest eigenvalue of (A'A/N)'/~'(F'F/T)(A'
                                                                                                                               ~ I by Fl(i) and F'F/T$z,, by Fl(d),
                                                                                          A / N ) ' / ~ .But ( A ' A / N ) ~ /-+
   Proof. sup,,, IT-' C, q,(N-' Ciyiei,)l                 I      (T-I C, q:)'l2x          so that (A'A/N)'/~'(F'F/T)(A'A/N)'/~~z~~                 and (by continuity of
(sup,,, T-I C,(N-' Ci ~ i e i r ) ~ ) " ~ .                                               eigenvalues)          4 ul
The first term is 0,(1) by assumption, and so the result follows from
                                                                                              Proof. This follows from (R7) and (R8).
                                                                                              (R10) Let i,= argsup,,, R(y); then R * ( ~ , ) ~ u , , .
                                                                                              Proof. This follows from (R6) and (R9).
                                                                                              (R11) Let %I denote the first column of        and let S, =        x
                                                                                                    sign($, A,), meaning S, = 1 if AIAl > 0 and S, = -1 if
                                                                                                                                                    A,


where the limit follows from (R2).
                                                                                                        A',
                                                                                                       4' < 0.
      (R4) sup,,,   IT-' C, Fl,(N-' C , y,e,,)l$0 for j = 1 , 2 , . . . , r.
                                                                                          Then (S,$;A/N)$C',,             where el = (100.. . 0)'.
   Proof. Because T-' 1,  F jr4ulj [from Assumption Fl(d)], the
result follows from (R3).                                                                    Proof. For particular values of 8 and p, we can write    =
                                                                                          A(A%/N)-'/~~+  p, where ?A=O and 6'8 5 1. (Note that 6 is
                                                                                          r x 1.) Let CNrA= (A'A/N)'/~'(F'F/T)(A'A/N)~/~   and note that
                                                                                          R*($,) = 6'cNT6.Thus
   Proof.     (N2T)-' y'AF'ey = C j ( y ' A j / N ) T - ' C , F , , ( N - ' C , yiei,),
so that




Thus.                                                                                     Because     c,,~c,,  and i is bounded, the first term on the right side
                                                                                          of this expression is op(l). This result together with (R10) implies
      sup l(N2T)-' y'AF'eyl
      YE,
                                                                                                                 +                  P
                                                                                          that (6: - I)(+,, C:=, Sfuii-+O. Because uii > 0, i = 1, . . . , r
                                                                                                                            A




                                                                                          [Assumption Fl(b)], this implies that 6 i s l and if40for i >
                                                                                          1. Note that this result, together with A ' , ~ , / N= 1, implies that
                                                                                          A

                                                                                          V'VIN~O.
                                                                                             The result then follows from the assumption that A'AIN -+ I,
                                                                                          [Assumption F l (a)].
                                                                                                                                                x
                                                                                              (R12) Suppose that the N x r matrix is fop,ed as the r ordered
                                                                                                    eigenvectors of X'X normalized as AfA/N = I (with the
                                                                                                    first column corresponding the largest eigenvalue, etc.) Let
                                                                                                    S denote S = diag(sign(;"l'A)). Then s ; ~ ' A / NI.~
where the last line follows from (yly/N) = 1, Fl(a), and (R4).
                                                                                             Proof. The result for the first column of S ~ ' A / Nis given in
      (R6) sup,,,   IR(y)-~*(y)l$0.                                                       (RI 1). The results for the other columns mimic the steps in (R8)-
  Proof.      R(y) - R*(y) = (N2T)-' y'e'ey               + 2(N2T)-'y'AF'ey               (R1 I), for the other principal components, that is, by maximizing
and                                                                                       R(.) and R*(.) sequentially using orthonormal subspaces of r. For
                                                                                          later reference, we-note that this process yields a representation of
sup IR(y) - R*(y)l Isup(N2T)-'ly'e'eyl +sup(N2T)-'ly1AF'eyl,                              the jth column of A as
YE,                        YE,                          YE,

where the two terms on the rhs of the inequality converge to 0 in
probability by (R2) and (R5).                                                             where PA= 0, ??/N<O,                    and $$SO             P
                                                                                                                                         for i # j and 6;,-+1.
                                                                                                                                                             P
                                                                                               (R13) For j = 1 , . . . , r, T-' C,? = R(A,)-+ujj.
                                                                                                                                                         A
1176                                                                                     Journal of the American Statistical Association, December 2002

  Proof. T-' C,        = R ( i j ) by the definitions of and R ( . ) . The        Because ( s ~ ' A / N ) <I by (R12) and T-' C ,F , ~ , ~ zby, assump-
convergence result follows from (R9) for j = 1 and from the steps                 tion,
outlined in (R12) for j = 2 , . . . , r.                                                               T-' ~ ( s ~ ' A / N ) F , ~ , ~ z , ~ .
   (R14) For i > r , T-' C ,    E~o.
                                                                                     Now the jth element of T - ' N - ' C , S ~ ' e , q satisfies
                                                                                                                                        ,
   Proof. Let .i, denote the ith ordered eigenvector of X ' X , i > r ,
normalized so that ??IN = 1 . Then T - ' C, = R ( f ) follows from
the definition of R(.) and    E,.
   Now, for particular values of & and p, we can write

                                                                                                                         I , ( C )Ip
                                                                                                                5 sup T-' C q , N-'
                                                                                                                  ysl-                    ,
                                                                                                                                              yiei, +O,

where Vl' A = 0 , &'& 5 1, and           5 1. Now, by construction,               where the final inequality follows because i,E l- and the limit fol-
?'Aj = O for j = 1, . . . , r. Using the representation for +A given              lows from (R3).
                                              A


                                                   +   A -




               --
from (R12), V,'V,+O
                     P                        --
in (R12), we can write N-' ?'A, = 2 8 , V I V j / N= 0. Because
                                                       P
                         and Vl'p/N 5 1 . VIVj+O. Thus & ' $ , ~ oso
                                                                   ,
                                                                                     (R17) T-' C ,sEF,-!+z,,.

&'[$,. . . i,]40.
                          A      ^       P
                     But [ a 1 . . 8,]+1,, so &-%0.                                         Proof. This follows from (R16) with q, = F,,, j = 1 , . . . , r.
                                                                                         Assumption Fl(d) shows that this choice of q, satisfies the restriction
    Thus R * ( f ) = & 1 ( ~ ' ~ / ~ ) ' ~ 2 ' ( ~ ' ~ / ~ )The                    (~'~/~)'~2&~0.
                                                                                         in (R16.)
result then follows from (R6).
              A
                                                                                                       --         P
                                                                                             (R18) T - ' C ,F,F,'+Z,,.
     (R15) SjF,, - F,,-%o for j = 1, . . . , r
                                     I                         ^ I                          Proof. This follows from (R16) and (R17). Set q, =      ~~5,.   (R13)
                                                                            +
                                 A


    Proof. S,F,, - F,, = SjA,X,/N - F,, = (SjA,A,/N - l ) F j ,                          shows that q, satisfies the conditions of (R16).
~ , ~ ~ ( s ~ i+       i s~j Li ; /e r~/ ~). ~ t r
                                                                                             (R19) For i = 1,2, . . . , r , T - ' c,(S,E, - F , , ) ~ ~ o .
    Because s ( ~ ' A / NI )from       ~     (R12), ( s , ~ : A , / N - 1):0       and
                    o i # j . Because IFTI is O P ( 1 ) [which follows
s , ~ ~ A , / N - %for
from E(FTF;) = Z,,], ( s , ~ ~ A , /-        N ~)F,,-%oand c , , ~ ( s , ~ ; A , / N ) x
                                                             r i

F,,<o. The result then follows by showing that s , ~ , ~ , / N > o .                     (R20)-(R23) Hold Given F1, M I , and Y1
   Now
                                                                                     (R20) T-' C , Scw;<Z,,.
                                                                                    Proof. This follows from (R16), with q, equal to w,,. Y l ( b )
                                                                                  shows that this definition of q, satisfies the conditions of (R16).
Also,
                                                                                     (R21) T-' C ,s E E , + , ~ o .
                                                                                      Proof. This follows from (R16) and Y l ( c )with q, equal to E,,,.
                                                                                  Y l ( d ) shows that this definition of q, satisfies the conditions of
                                                                                  (R16).
and
                                                                                     (R22) With      p partitioned as p = (pip',)', flu, - pu,<O and
                                                                                              s,P,~-P,~-%ofor i = 1 , . . . r .
                                 -
by (R12). Finally, N-' C ,ef, O p ( l )by ( R l ) .Thus IN-' -     c,(s,~,
                                                                                     Proof. Write

A,,)e,, 140 by Slutsky's theorem. T h ~ smeans that S,iie,/N =
               +
N ' C ,A,,e,, o P ( l ) .Now




                                                                                                      --
                                                                                  Because T-' C ,F,F;+Z,,
                                                                                                            P
                                                                                                                     (R18), T - ' S C ,E w i < ~ , , (R20),
where the final inequality uses the bound on A,j given in Fl(c) and               T-' C ,w,w;-%Z,, [ Y l ( b ) ] ,T - ' S C , EE,+,~o   ( R21), and T - ' x
the limit uses Ml(b). Thus S j L ; e , / N s O .                                  C , w,E,+,-%o [ Y l ( c ) ] ;and because ZZ: is nonsingular [ Y l ( a ) ] ,the
                                                                                  result follows by Slutsky's theorem.
   (R16) Let q, denote a sequence of random variables with
         T-' ~   ,       ~ T-'~ 1,
                     q and       uF , ~~, ~ z , , . Then T-' 1,S                     (R23) Let      I , = (c,g,.  .: F),w;)' and         p = (I:,;"Z,:^;)-'
            E~,$Z~,.                                                                          (~:_;h i , ~ , +  ~ P)';i , - P'zT$0.
                                                                                                             then
   Proof.                                                                           Proof. Let R =       [i ,: 1, where n,, denotes the number of ele-
                                                                                  ments in w,.
Stock and Watson: Forecasting From Many Predictors

Because zT is 0,(1) [because E(zTz;) = 2:: by Yl(a)], and
~ f i
    - ~ $ 0(R22), the first term vanishes in probability by Slut-
sky's theorem. Similarly, because P is finite [Assumption Yl(e)] and
Ri, - z T 4 0 (R15), the second term vanishes in probability by Slut-
sky's theorem.
Proof of Theorem 1
  Part a is proved by (R19); part b, by (R15); and part c, by (R14).

Proof of Theorem 2
  Part a is proved by (R23); part b, by (R22).

Proof of Theorem 3
  The model can be written as



               +
where ail = e,, JiT&',Fr, Ji, = TgiT, ti,= T-' Z:=, lis, and where        where the first line follows from the definition of 6, the next line
(from Assumption F2) A,, satisfies the same conditions as A in            follows from independence of J,, and the bound given in SO, the
Assumption Fl. Thus the results follows if the error terms a, satisfy     next line redefines the index of summation, the next line follows from
the assumptions in M 1.                                                   definition of the sup, the next line follows because the summand in
   We prove a set of set of results (SO-S5) that yields the results. SO   the summation over s does not depend on s, the next line follows from
is a preliminary result. S1-S3 show that a , satisfies the assumption     the definition of the sup, the next line follows because the summand
in MI.                                                                    in the summation over u does not depend on u, and the final line
                                                                          follows from Assumption M2(a).
SO.
  Let J,, = Tg,,. Then constants K , - K, can be chosen so that
                                                                             Proof. JtTeirF:+u6ir+u  = J i ~Em Frn~+u6t~+~i,
                                                                                                                       m and we                      the
                                                                          result for each term in the sum:




and
                   SUP;, ]. k,   ,El   J,T J,T J ~ TJLT   I < K4.
This follows from F2(a).


   The error term a satisfies Assumption Ml(a). That is,
lim,,,,, sup, C:;-, IE(N-~C, ai,att+u)l < 00.



  We consider each part in turn.

  Sl(a). limN,,    sup, C, IE(N-' C, ei,ei,+u)l< m.
  Proof.   This is Assumption Ml(a).
                                                                 where the first line follows from the definition of 6, the next line
                                                                 follows from independence of J,, and the bound given in SO, the
  Proof. J,',(F: 6i1)(Fi+uti,+,) = J$CIE m F/tFmr+u6zr,l6ir+u.m, next line follows definition of the sup, the next line follows from
and we show the result for each term in the sum:                 the definition of the sup, the next line follows because the summand
                                                                 in the summation over u does not depend on u, and the final line
                                                                 follows from Assumption M2(b).


                                                                            Proof.    The proof parallels Sl(c).


                                                                            The error terms a, satisfy Ml(b); that is, lim,,,                sup, N-'
                                                                          Xi"=)C,N_IIE(airaji)l < 00.
                                                                                                                                   +: ~Jj,e,rF;Sjr
                                                                             Proof. aa,,ajt = cite], + J , T J ~ T ( F : ~ ~ ~ ) ( F     ~I)          +
                                                                          Ji~ejfF:ti~.
1178                                                                                           Journal of the American Statistical Association, December 2002

   We consider each part in turn.
  S2(a). lim,,,       sup, N-' EL,I
                                  :,          I E(ellejl)1 < m.
   Proof.    This is Assumption Ml(a).

                                                                                         We consider each of these terms in turn.

  Proof. JiTJjT(F:t1l)(Fl'tjt) = 11   Ern J ~ ~ J j ~ F l lfFtmi ~~t .~ f , m ,and
                                                                                         S3(a). lim,,,         sup,,, N-'   cL, c:=, I c o ~ ( e ~ , eejsejl)I
                                                                                                                                                       ,~, <     03.

we show the required result for each term in the sum:                                    Proof.        This is Assumption Ml(c).



                                                                                         Proof. cov(ei,e,,>JJ,(F:tjl)(F,'tjS)) = C,C,, cov(eiseil> JJ7Fll
                                                                                       ~jl,lFm,~j,,m
                                                                                                   and
                                                                                                     ) , it suffices to show the result for each term in the
                                                                                       sum:




where the first line follows from the definition of 5, the next line
follows from the independence of J and the bound in SO, the next
line follows from the definition of the sup and the fact that there are t
terms in the summations involving s and q, and the final line follows
from M2c.
   S2(c). limN+, sup1 N-I CEl C,N_,IE(Ji7ejrF;trOl < 00.
   Proof. J,,e,, F:[,, = JITe,,1,Frnltil,
                                       , and we show the required                      where the last line follows from M2(e)(l).
result for each term in the sum:


                                                                                         Proof. cov(eiseir, JITel,Fjtjx) = Crncov(etXetr,     JjTelrFn,rt,x,rn),
                                                                                       and it suffices to show the result for each term in the sum:




where the first line follows from the definition of 5, the next line
follows from the independence of J and the bound in SO, the next
line follows from the definition of the sup and the fact that there are
tterms in the summations involving s, and the final line follows from
M2(d).                                                                                 where the last line follows from M2(e)(2).
   S2(d). lim,,,      sup, N-' CElCg1 IE(JjTeitFltjl)l < CO.                                                        - ' E ~ =I cI ov(J$(F:t,~)(Fjh),
                                                                                         S3(d). lim~,, s u ~ ~ , , NCEI
   Proof.    The results is implied by S2(c).                                                   J?,(F~tjO(F:tjr))I < w .
                                                                                         Proof. cov(J;',(F:t,r)(F,15,,), J$(F:tjr)(F,/tjs))           =    CIIC12x
   The error terms a satisfy Ml(c); that is                                            El, El4cov(J,',Fll,ti,, 1, F1,StiS. l2 ' J/21Fl31tjl,13F14StlS.
                                                                                                                                                    14)' and it suf-
                                                                                       fices to show the result for each term in the sum:

               lim sup N-'
              N+-   1.5    ,=I
                                  x
                               C I cov(ai,a,,,ajsall)1 <          CO.
                                                                                         supN-'
                                                                                                       N
                                                                                                       C
                                                                                                           N
                                                                                                           C I cov(~,',~l~lt,l,l,~l,,t,,.l,~
                                                                                                                                      ~,',~l~,t~l.l~~,~~t~~.l~)
                                                                                         1.5           i=l ,=l
   Proof. aa,lais = eileir + J?T(F:tir)(F,'tis) + J I T e t ~ F ~ t , x+ J i ~ e l x
F:til, and so cov(aiSa,,,ajsajl) is made of 16 terms, which have
                                                                                                 1,s
6 possible forms:
Stock and Watson: Forecasting From Many Predictors




                                                                                    where the last line follows from M2(e)(5).

where the last line follows from M2(e)(3).                                                          [Received April 2000, Revised September 20011

                                                                                                                   REFERENCES
   Proof. ~ O V ( J : ~ ( F ~ S ~ , ) ( FJiTejrFiSjx)
                                         ,'~~~),        =     ClIC1, Ci, x                Bai, J., and Ng, S. (2001), "Determining the Number of Factors in Approxi-
                                                                                             mate Factor Models," Econometrica, 70, 191-221.
COV(J:~FlltSif,llFlzsSrs.  l 2 JjTejfFi3s~js,l,),   and it suffices to show               Chamberlain, G., and Rothschild, M. (1983), "Arbitrage Factor Structure, and
the result for each term in the sum:                                                         Mean-Variance Analysis of Large Asset Markets." Econometrica, 51, 1281-
                                                                                             1304.
                                                                                          Connor, G., and Korajczyk, R. A. (1986), "Performance Measurement With
                                                                                             the Arbitrage Pricing Theory," Journal of Financial Economics, 15, 373-
                                                                                             394.
                                                                                          -(1988), "Risk and Return in an Equilibrium APT: Application of a
                                                                                             New Test Methodology," Journal of Financial Economics, 21, 255-289.
                                                                                          -(1993), "A Test for the Number of Factors in an Approximate Factor
                                                                                             Model," Journal of Finance, XLVIII, 1263-1291.
                                                                                          Ding, A. A,, and Hwang, J. T. (1999), "Prediction Intervals, Factor Analysis
                                                                                             Models, and High-Dimensional Empirical Linear Prediction," Journal of
                                                                                             the American Statistical Association, 94, 446455.
                                                                                          Forni, M., Hallin, M., Lippi, M., and Reichlin, L. (2000), "The General-
                                                                                             ized Dynamnic Factor Model: Identification and Estimation," The Review
                                                                                             of Economics and Statistics, 82, 540-552.
                                                                                          Forni, M., and Reichlin, L. (1996), "Dynamic Common Factors in Large
                                                                                             Cross-Sections," Empirical Economics, 21, 27-42.
                                                                                          -(1998), "Lets Get Real: A Dynamic Factor Analytical Approach
                                                                                             to Disaggregated Business Cycle," Review of Economic Studies, 65,
                                                                                             453474.
              N N                                                                          Geweke, J. (1977), "The Dynamic Factor Analysis of Economic Time Series,"
    < K ~ N - ' C C SUP
    -                                      ~ c o v ( F ~ ~ ~ ~ ~ ~ ~ . ~in Latent                ~ F Variables
                                                                                                         I ~ ~ in~Socio-Economic
                                                                                                                      ~ ~ ~ . /Models,  ~ ~ eds.  ~ J.~ Aigner
                                                                                                                                                ~ D.     ~ I and
                                                                                                                                                               ~ A.
                                                                                                                                                                  s S.~   ~ ~ ~
             i=l j=I f , s, { l k , qk]2=l                                                   Goldberger, Amsterdam: North-Holland, Ch. 19.
                                                                                           Lawley, D. N., and Maxwell, A. E. (1971), Factor Analysis as a Statistical
    < CO.                                                                                    Method, New York: American Elsevier Publishing.
                                                                                           Sargent, T. J,. and Sims, C. A. (1977), "Business Cycle Modeling Without
where the last line follows from M2(e)(4).                                                   Pretending to Have Too Much A Priori Economic Theory," in New Meth-
                                                                                             ods in Business Cycle Research, eds. C . Sims et al., Minneapolis: Federal
                                                                                             Reserve Bank of Minneapolis.
                                                                                           Stock, J. H., and Watson, M. W. (1989), "New Indexes of Coincident and
                                                                                             Leading Economic Indicators," NBER Macroeconomics Annual, 351-393.
   Proof. cov(Jr~ei~(F,'lis)>                               s ) Ci Crn cov(J,~e/tF/sSts,~, -(1996), "Evidence on Structural Instability in Macroeconomic Time
                                         J j ~ e j ~ F i l j=
JlTejfFrnSljs,,),and it suffices to show the result for each term in                          Series Relations," Journal of Business and Economic Statistics, 14,
                                                                                              11-30.
the sum:
                                                                                           -(1998a), "Diffusion Indexes," Working Paper 6702, NBER.
                                                                                           -(1998b), "Median Unbiased Estimation of Coefficient Variance in a
                                                                                             Time-Varying Parameter Model," Journal of the American Statistical Asso-
                                                                                              ciation, 93, 349-358.
                                                                                                    (1999), "Forecasting Inflation," Journal of Monetaiy Economics, 44,
                                                                                              293-335.
                                                                                                    (2002), "Macroeconomic Forecasting Using Diffusion Indexes," Jour-
                                                                                              nal of Business and Economic Statistics, 20, 147-162.
http://www.jstor.org


                        LINKED CITATIONS
                                  - Page 1 of 2 -



You have printed the following article:
       Forecasting Using Principal Components from a Large Number of Predictors
       James H. Stock; Mark W. Watson
       Journal of the American Statistical Association, Vol. 97, No. 460. (Dec., 2002), pp. 1167-1179.
       Stable URL:
       http://links.jstor.org/sici?sici=0162-1459%28200212%2997%3A460%3C1167%3AFUPCFA%3E2.0.CO%3B2-U



This article references the following linked citations. If you are trying to access articles from an
off-campus location, you may be required to first logon via your library web site to access JSTOR. Please
visit your library's website or contact a librarian to learn about options for remote access to JSTOR.

References

    Determining the Number of Factors in Approximate Factor Models
    Jushan Bai; Serena Ng
    Econometrica, Vol. 70, No. 1. (Jan., 2002), pp. 191-221.
    Stable URL:
    http://links.jstor.org/sici?sici=0012-9682%28200201%2970%3A1%3C191%3ADTNOFI%3E2.0.CO%3B2-7


    Arbitrage, Factor Structure, and Mean-Variance Analysis on Large Asset Markets
    Gary Chamberlain; Michael Rothschild
    Econometrica, Vol. 51, No. 5. (Sep., 1983), pp. 1281-1304.
    Stable URL:
    http://links.jstor.org/sici?sici=0012-9682%28198309%2951%3A5%3C1281%3AAFSAMA%3E2.0.CO%3B2-B


    A Test for the Number of Factors in an Approximate Factor Model
    Gregory Connor; Robert A. Korajczyk
    The Journal of Finance, Vol. 48, No. 4. (Sep., 1993), pp. 1263-1291.
    Stable URL:
    http://links.jstor.org/sici?sici=0022-1082%28199309%2948%3A4%3C1263%3AATFTNO%3E2.0.CO%3B2-0


    Prediction Intervals, Factor Analysis Models, and High-Dimensional Empirical Linear
    Prediction
    A. Adam Ding; J. T. Gene Hwang
    Journal of the American Statistical Association, Vol. 94, No. 446. (Jun., 1999), pp. 446-455.
    Stable URL:
    http://links.jstor.org/sici?sici=0162-1459%28199906%2994%3A446%3C446%3APIFAMA%3E2.0.CO%3B2-K
http://www.jstor.org


                        LINKED CITATIONS
                                  - Page 2 of 2 -



    The Generalized Dynamic-Factor Model: Identification and Estimation
    Mario Forni; Marc Hallin; Marco Lippi; Lucrezia Reichlin
    The Review of Economics and Statistics, Vol. 82, No. 4. (Nov., 2000), pp. 540-554.
    Stable URL:
    http://links.jstor.org/sici?sici=0034-6535%28200011%2982%3A4%3C540%3ATGDMIA%3E2.0.CO%3B2-G


    Let's Get Real: A Factor Analytical Approach to Disaggregated Business Cycle Dynamics
    Mario Forni; Lucrezia Reichlin
    The Review of Economic Studies, Vol. 65, No. 3. (Jul., 1998), pp. 453-473.
    Stable URL:
    http://links.jstor.org/sici?sici=0034-6527%28199807%2965%3A3%3C453%3ALGRAFA%3E2.0.CO%3B2-A


    Evidence on Structural Instability in Macroeconomic Time Series Relations
    James H. Stock; Mark W. Watson
    Journal of Business & Economic Statistics, Vol. 14, No. 1. (Jan., 1996), pp. 11-30.
    Stable URL:
    http://links.jstor.org/sici?sici=0735-0015%28199601%2914%3A1%3C11%3AEOSIIM%3E2.0.CO%3B2-5

    Median Unbiased Estimation of Coefficient Variance in a Time-Varying Parameter Model
    James H. Stock; Mark W. Watson
    Journal of the American Statistical Association, Vol. 93, No. 441. (Mar., 1998), pp. 349-358.
    Stable URL:
    http://links.jstor.org/sici?sici=0162-1459%28199803%2993%3A441%3C349%3AMUEOCV%3E2.0.CO%3B2-K


    Macroeconomic Forecasting Using Diffusion Indexes
    James H. Stock; Mark W. Watson
    Journal of Business & Economic Statistics, Vol. 20, No. 2. (Apr., 2002), pp. 147-162.
    Stable URL:
    http://links.jstor.org/sici?sici=0735-0015%28200204%2920%3A2%3C147%3AMFUDI%3E2.0.CO%3B2-Z

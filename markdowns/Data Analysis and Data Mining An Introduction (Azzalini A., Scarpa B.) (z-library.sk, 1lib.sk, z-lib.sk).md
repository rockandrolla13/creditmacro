Data Analysis and Data Mining 

_This page intentionally left blank_ 

Data Analysis and Data Mining _An Introduction_ 

A D E L C H I A Z Z A L I N I AND 

B R U N O S C A R PA 

3 

## 3 

Oxford University Press, Inc., publishes works that further Oxford University’s objective of excellence in research, scholarship, and education. 

Oxford New York Auckland Cape Town Dar es Salaam Hong Kong Karachi Kuala Lumpur Madrid Melbourne Mexico City Nairobi New Delhi Shanghai Taipei Toronto With offices in Argentina Austria Brazil Chile Czech Republic France Greece Guatemala Hungary Italy Japan Poland Portugal Singapore South Korea Switzerland Thailand Turkey Ukraine Vietnam 

Copyright © 2012 by Oxford University Press 

Published by Oxford University Press, Inc. 198 Madison Avenue, New York, New York 10016 www.oup.com 

Oxford is a registered trademark of Oxford University Press 

All rights reserved. No part of this publication may be reproduced, stored in a retrieval system, or transmitted, in any form or by any means, electronic, mechanical, photocopying, recording, or otherwise, without the prior permission of Oxford University Press. 

Library of Congress Cataloging-in-Publication Data Azzalini, Adelchi. [Analisi dei dati e “data mining”. English] Data analysis and data mining : an Introduction / Adelchi Azzalini, Bruno Scarpa; [text revised by Gabriel Walton]. p. cm. Includes bibliographical references and index. ISBN 978-0-19-976710-6 1. Data mining. I. Scarpa, Bruno. II. Walton, Gabriel. III. Title. QA76.9.D343A9913 2012 006.3’12—dc23 2011026997 9780199767106 

English translation by Adelchi Azzalini, Bruno Scarpa and Anne Coghlan. Text revised by Gabriel Walton. 

First published in Italian as Analisi dei dati e “data mining”, 2004, Springer-Verlag Italia (ITALY) 

9 8 7 6 5 4 3 2 1 

Printed in the United States of America on acid-free paper 

## CONTENTS 

Preface vii Preface to the English Edition ix 

1. Introduction 1 

   - 1.1. New problems and new opportunities 1 

   - 1.2. All models are wrong 9 

   - 1.3. A matter of style 12 

2. A–B–C 15 

   - 2.1. Old friends: Linear models 15 

   - 2.2. Computational aspects 30 

   - 2.3. Likelihood 33 

   - 2.4. Logistic regression and GLM 40 

   - Exercises 44 

3. Optimism, Conflicts, and Trade-offs 45 

   - 3.1. Matching the conceptual frame and real life 45 

   - 3.2. A simple prototype problem 46 

   - 3.3. If we knew _f_ ( _x_ ) _. . ._ 47 

   - 3.4. But as we do not know _f_ ( _x_ ) _. . ._ 51 

   - 3.5. Methods for model selection 52 

3.6. Reduction of dimensions and selection of most appropriate model 58 Exercises 66 

4. Prediction of Quantitative Variables 68 

   - 4.1. Nonparametric estimation: Why? 68 

   - 4.2. Local regression 69 

   - 4.3. The curse of dimensionality 78 

   - 4.4. Splines 79 

   - 4.5. Additive models and GAM 89 

   - 4.6. Projection pursuit 93 

   - 4.7. Inferential aspects 94 

   - 4.8. Regression trees 98 

   - 4.9. Neural networks 106 

   - 4.10. Case studies 111 

Exercises 132 

C O N T E N T S 

vi 

5. 134 

   - 5.1. Prediction of categorical variables 134 

   - 5.2. An introduction based on a marketing problem 135 

   - 5.3. Extension to several categories 142 

   - 5.4. Classification via linear regression 149 

   - 5.5. Discriminant analysis 154 

   - 5.6. Some nonparametric methods 159 

   - 5.7. 164 

   - 5.8. Some other topics 168 

   - 5.9. 176 

   - 5.10. Case studies 183 Exercises 210 

6. Methods of Internal Analysis 212 

   - 6.1. Cluster analysis 212 

   - 6.2. Associations among variables 222 

   - 6.3. Case study: Web usage mining 232 

Appendix A Complements of Mathematics and Statistics 240 

- A.1. Concepts on linear algebra 240 

- A.2. Concepts of probability theory 241 

- A.3. Concepts of linear models 246 

Appendix B Data Sets 254 

- B.1. Simulated data 254 

- B.2. Car data 254 

- B.3. Brazilian bank data 255 

- B.4. Data for telephone company customers 256 

- B.5. Insurance data 257 

- B.6. Choice of fruit juice data 258 

- B.7. Customer satisfaction 259 

- B.8. Web usage data 261 

AppendixC Symbols and Acronyms 263 

References 265 Author Index 269 Subject Index 271 

PREFACE 

When well-meaning university professors start out with the laudable aim of writing up their lecture notes for their students, they run the risk of embarking on a whole volume. 

We followed this classic pattern when we started jointly to teach a course entitled ‘Data analysis and data mining’ at the School of Statistical Sciences, University of Padua, Italy. 

Our interest in this field had started long before the course was launched, while both of us were following different professional paths: academia for one of us (A. A.) and the business and professional fields for the other (B. S.). In these two environments, we faced the rapid development of a field connected with data analysis according to at least two features: the size of available data sets, as both number of units and number of variables recorded; and the problem that data are often collected without respect for the procedures required by statistical science. Thanks to the growing popularity of large databases with low marginal costs for additional data, one of the most common areas in which this situation is encountered is that of data analysis as a decision-support tool for business management. At the same time, the two problems call for a somewhat different methodology with respect to more classical statistical applications, thus giving this area its own specific nature. This is the setting usually called _data mining_ . 

Located at the point where statistics, computer science, and machine learning intersect, this broad field is attracting increasing interest from scientists and practitioners eager to apply the new methods to real-life problems. This interest is emerging even in areas such as business management, which are traditionally less directly connected to scientific developments. 

Within this context, there are few works available if the methodology for data analysis must be inspired by and not simply illustrated with the aid of real-life problems. This limited availability of suitable teaching materials was an important reason for writing this work. Following this primary idea, methodological tools are illustrated with the aid of real data, accompanied wherever possible by some motivating background. 

Because many of the topics presented here only appeared relatively recently, many professionals who gained university qualifications some years ago did not have the opportunity to study them. We therefore hope this work will be useful for these readers as well. 

P R E F A C E 

viii 

Although not directly linked to a specific computer package, the approach adopted here moves naturally toward a flexible computational environment, in which data analysis is not driven by an “intelligent” program but lies in the hands of a human being. The specific tool for actual computation is the R environment. 

All that remains is to thank our colleagues Antonella Capitanio, Gianfranco Galmacci, Elena Stanghellini, and Nicola Torelli, for their comments on the manuscript. We also thank our students, some for their stimulating remarks and discussions and others for having led us to make an extra effort for clarity and simplicity of exposition. 

Padua, April 2004 

Adelchi Azzalini and Bruno Scarpa 

## PREFACE TO THE ENGLISH EDITION 

This work, now translated into English, is the updated version of the first edition, which appeared in Italian (Azzalini & Scarpa 2004). 

The new material is of two types. First, we present some new concepts and methods aimed at improving the coverage of the field, without attempting to be exhaustive in an area that is becoming increasingly vast. Second, we add more case studies. The work maintains its character as a first course in data analysis, and we assume standard knowledge of statistics at graduate level. 

Complementary materials (data sets, R scripts) are available at: http:// azzalini.stat.unipd.it/Book-DM/. 

A major effort in this project was its translation into English, and we are very grateful to Gabriel Walton for her invaluable help in the revision stage. 

Padua, April 2011 

Adelchi Azzalini and Bruno Scarpa 

_This page intentionally left blank_ 

1 

## Introduction 

He who loves practice without theory is like the sailor who boards ship without a rudder and compass and never knows where he may cast. 

—LEONARDO DA VINCI 

## 1.1 NEW PROBLEMS AND NEW OPPORTUNITIES 

## 1.1.1 Data, More Data, and Data Mines 

An important phase of technological innovation associated with the rise and rapid development of computer technology came into existence only a few decades ago. It brought about a revolution in the way people work, first in the field of science and then in many others, from technology to business, as well as in day-to-day life. For several years another aspect of technological innovation also developed, and, although not independent of the development of computers, it was given its own autonomy: large, sometimes enormous, masses of information on a whole range of subjects suddenly became available simply and cheaply. This was due first to the development of automatic methods for collecting data and then to improvements in electronic systems of information storage and major reductions in their costs. 

This evolution was not specifically related to one invention but was the consequence of many innovative elements which have jointly contributed to the 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

2 

creation of what is sometimes called the _information society_ . In this context, new avenues of opportunity and ways of working have been opened up that are very different from those used in the past. To illustrate the nature of this phenomenon, we list a few typical examples. 

- Every month, a supermarket chain issues millions of receipts, one for every shopping cart that arrives at the checkout. The contents of one of these carts reflect the demand for goods, an individual’s preferences and, in general, the economic behavior of the customer who filled that cart. Clearly, the set of all shopping lists gives us an important information base on which to direct policies of purchases and sales on the part of the supermarket. This operation becomes even more interesting when individual shopping lists are combined with customers’ “loyalty cards,” becausewecanthenfollowtheirbehaviorthroughasequenceofpurchases. 

- A similar situation arises with credit cards, with the important difference that all customers can be precisely identified; there is no need to introduce anything like loyalty cards. Another point is that credit card companies do not sell anything directly to their customers, although they may offer other businesses the opportunity of making special offers to selected customers, at least in conditions that allow them to do so legally. 

- Every day, telephone companies generate data from millions of telephone calls and other services they provide. The collection of these services becomes more highly structured as advanced technology, such as UMTS (Universal Mobile Telecommunications System), becomes established. Telephone companies are interested in analyzing customer behavior, both to identify opportunities for increasing the services customers use and to ascertain as soon as possible when customers are likely to terminate their contracts and change companies. The danger of a customer terminating a contract is a problem in all service-providing sectors, but it is especially critical in subsectors characterized by rapid transfers of the customer base, for example, telecommunications. Study of this danger is complicated by the fact that, for instance, for prepaid telephone cards, there can be no formal termination of service (except for number portability), but merely the fact that the credit on the card is exhausted, is not recharged after its expiration date, and the card itself can no longer be used. 

- Service companies, such as telecommunications operators, credit card companies, and banks, are obviously interested in identifying cases of fraud, for example, customers who use services without paying for them. Physical intrusion, subscriptions with the intention of selling services at low cost, and subverting regulatory restrictions are only some examples of fraud-implemented methods. There is a need for tools to design accurate systems capable of predicting fraud, and they must work in an adaptive way according to the changing behavior of both legitimate customers and fraudsters. The problem is particularly challenging because only a very small percentage of the customer base will actually be fraudulently inclined, which makes this problem more difficult than finding a needle 

Introduction 

3 

in a haystack. Fraudulent behavior may be rare, and behavior that looks like an attempt at fraud in one account may appear normal and indeed expected in another. 

- The Worldwide Web is an enormous store of information, a tiny fraction of which responds to a specific query posted to a search engine. Selecting the relevant documents, the operation that must be carried out by the search engine, is complicated by various factors: (a) the size of the overall set of documents is immense; (b) compared with the examples quoted previously, the set of documents is not in a structured form, as in a wellordered database; (c) within a single document, the aspects that determine its pertinence, or lack thereof, with respect to the given query, are not placed in a predetermined position, either with respect to the overall document or compared with others. 

- Also, in scientific research, there are many areas of expertise in which modern methods produce impressive quantities of data. One of the most recent active fields of research is microbiology, with particular reference to the structure of DNA. Analyses of sequences of portions of DNA allow the construction of huge tables, called DNA microarrays, in which every column is a sequence of thousands of numerical values corresponding to the genetic code of an individual, and one of these sequences can be constructed for every individual. The aim— in the case of microbiology—is to establish a connection between the patterns of these sequences and, for instance, the occurrence of certain pathologies. 

- The biological context is certainly not the only one in science where massive amounts of data are generated: geophysics, astronomy, and climatology are only a few of the possible examples. The basic organization of the resulting data in a structured way poses significant problems, and the analysis required to extract meaningful information from them poses even greater ones. 

Clearly, the contexts in which data proliferation manifests itself are numerous and made up of greatly differing elements. One of the most important, to which we often refer, is the business sector, which has recently invested significantly in this process with often substantial effects on the organization of marketing. Related to this phenomenon is the use of the phrase _Customer Relationship Management_ (CRM),whichreferstothestructuringof“customer-oriented”marketingbehavior. CRM aims at differentiating the promotional actions of a company in a way that distinguishesonecustomerfromanother,searchingforspecificofferssuitedtoeach individualaccordingtohisorherinterestsandhabits,andatthesametimeavoiding waste in promotional initiatives aimed at customers who are not interested in certain offers. The focus is therefore on identifying those customer characteristics that are relevant to specific commercial goals, and then drawing information from data about them and what is relevant to other customers with similar profiles. Crucially, the whole CRM system clearly rests on both the availability of reliable 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

4 

quantitative information and the capacity to process it usefully, transforming raw data into knowledge. 

## 1.1.2 Problems in Mining 

Data mining, this new technological reality, requires proper tools to exploit the mass elements of information, that is, _data_ . At first glance, this may seem paradoxical, but in fact, more often than not, it tells us that we cannot obtain significant information from such an abundance of data. 

In practical terms, examining the data of two characteristics of 100 individuals is very different from examining the results of 10[2] characteristics of 10[6] individuals. In the first case, simple data-analytical tools may result in important information at the end of the process: often an elementary scatterplot can offer useful indications, although formal analysis may be much more sophisticated. In the second case, the picture changes dramatically: many of the simple tools used in the previous case lose their effectiveness. For example, the scatterplot of 10[6] points may become a single formless ink spot, and 10[2] characteristics may produce 100 × 99 _/_ 2 of these forms, which are both too many and at the same time useless. 

This simple example highlights two aspects that complicate data analysis of the type mentioned. One regards the _size_ of the data, that is, the number of _cases_ or _statistical units_ from which information is drawn; the other regards the _dimensionality_ of the data, that is, the number of features or _variables_ of the data collected on a certain unit. 

The effects of these components on the complexity of the problem are very different from each other, but they are not completely independent. With simplification that might be considered coarse but does help understand the problem, we may say that _size_ brings about an increase primarily in computational aspects, whereas _dimensionality_ has a complex effect, which involves both a computational increase similar to that of size and a rapid increase in the conceptual complexity of the models used, and consequently of their interpretation and operative usage. 

Not all problems emerging from the context described can be ascribed to a structure in which it is easy to define a concept of size and, to an even lesser extent, of dimensionality. A typical counterexample of this kind is extracting those pages of the Web that are relevant to a query posted to a specific search engine: not only is it difficult to define the size of the set of cases of interest, but the concept of dimensionality itself is vague. Otherwise, the most classic and common situation is that in which statistical units are identified, each characterized by a certain predetermined number of variables: we focus on this family of situations in this volume. However, this is the structure in which each of the tables composing a database is conceptually organized; physical organization is not important here. 

We must also consider the possibility that the data has ‘infinite’ size, in the sense that we sometimes have a _continuous stream_ of data. A good example is the stream of financial transactions of a large stock exchange. 

In the past few years, exploration and data analysis of the type mentioned in section 1.1.1 has come to be called _data mining_ . We can therefore say that: 

Introduction 

5 

data mining represents the work of processing, graphically or numerically, large amounts or continuous streams of data, with the aim of extracting information useful to those who possess them. 

The expression “useful information” is deliberately general: in many cases, the point of interest is not specified a priori at all and we often search for it by mining the data. This aspect distinguishes between data mining and other searches related to data analysis. In particular, the approach is diametrically opposed, for example, to clinical studies, in which it is essential to specify very precisely a priori the aims for which data are collected and analyzed. 

What might constitute useful information varies considerably and depends on the context in which we operate and on the objectives we set. This observation is clearly also true in many other contexts, but in the area of data mining it has additional value. We can make a distinction between two situations: (a) in one, the interesting aspect is the global behavior of the phenomenon examined, and the aim istheconstructionofits _global model_ ,takenfromtheavailabledata;(b)intheother, it is characterization of detail or the _pattern structures_ of the data, as we are only interestedincasesoutsidestandardbehavior.Intheexampleoftelephonecompany customers, we can examine phone traffic data to identify trends that allow us to forecast customers’ behavior according to their price plans, geographical position, and other known elements. However, we can also examine the data with the aim of identifying behavioral anomalies in telephone usage with respect to the behavior of the same customer in the past—perhaps to detect a fraudulent situation created by a third party to a customer’s detriment. 

Data mining is a recent discipline, lying at the intersection of various scientific sectors, especially statistics, _machine learning_ , and _database_ management. 

The connection with database management is implicit in that the operations of data cleaning, the selection of portions of data, and so on, also drawn from distributed databases, require competences and contributions from that sector. The link with artificial intelligence reflects the intense activity in that field to make machines “learn” how to calculate general rules originating from a series of specific examples: this is very like the aim of extracting the laws that regulate a phenomenon from sampled observations. This, among the methods that are presented later, explains why some of them originate from the field of artificial intelligence or similar ones. 

In light of the foregoing, the statements of Hand et al. (2001) become clear: 

Data mining is fundamentally an applied discipline … data mining requires an understanding of both statistical and computational issues. (p. xxviii) 

The most fundamental difference between classical statistical applications and data mining is the size of the data. (p. 19) 

The computational cost connected with large data sizes and dimensions obviously has repercussions on the method of working with these data: as they increase, 

6 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

methods with high computational cost become less feasible. Clearly, in such cases, we cannot identify an exact rule, because various factors other than those already mentioned come into play, such as available resources for calculation and the time needed for results. However, the effect unquestionably exists, and it prevents the use of some tools, or at least renders them less practical, while favoring others of lower computational cost. 

It is also true that there are situations in which these aspects are of only marginal importance, because the amount of data is not enough to influence the computing element; this is partly thanks to the enormous increase in the power of computers. We often see this situation with a large-scale problem, if it can be broken down into subproblems, which make portions of the data more manageable. More traditional methods of venerable age have not yet been put to rest. On the contrary, many of them, which developed in a period of limited computing resources, are much less demanding in terms of computational effort and are still valid if suitably applied. 

## 1.1.3 SQL, OLTP, OLAP, DWH, and KDD 

We have repeatedly mentioned the great availability of data, now collected in an increasingly systematic and thorough way, as the starting point for processing. However, the conversion of raw data to “clean” data is time-consuming and sometimes very demanding. 

We cannot presume that all the data of a complex organization can fit into a single database on which we can simply draw and develop. In the business world, even medium-sized companies are equipped with complex IT systems made up of various databases designed for various aims (customers and their invoices, employees’ careers and wages, suppliers, etc.). These databases are used by various operators, both to insert data (e.g., from outlying sales offices) and to answer _queries_ about single entries, necessary for daily activities—for example, to know whether and when customer _X_ has paid invoice _Y_ issued on day Z. The phrase referring to methods of querying specific information in various databases, called _operational_ , is _OnLine Transaction Processing_ (OLTP). Typically, these tools are based on _Structured Query Language_ (SQL), the standard tool for database queries. 

For _decision support_ , in particular analysis of data for CRM, these operational databases are not the proper sources on which to work. They were all designed for different goals, both in the sense that they were usually created for administrative and accounting purposes and not for data analysis, and that those goals differ. This means that their structures are heterogeneous and very often contain inconsistent data, sometimes even structurally, because the definitions of the recorded variables may be similar but are not identical. Nor is it appropriate for the strategic activities of decision support to interfere with daily work on systems designed to work on operational databases. 

For these reasons, it is appropriate to develop focused databases and tools. We thus construct a _strategic_ database or Data WareHouse (DWH), in which data from different database systems merge, are “cleaned” as much as possible, and are organized round the postprocessing phase. 

The development of a DWH is complex, and it must be carefully designed for its future aims. From a functional point of view, the most common method of 

Introduction 

7 

construction is progressive aggregation of various data marts—that is, of finalized _databases_ . For example, a data mart may contain all the relevant information for a certain marketing division. After the DWH has been constructed, the later aggregation must achieve a coherent, homogenous structure, and the DWH must be periodically updated with new data from various operational databases. 

After completing all these programming processes (which can then progress by means of continual maintenance), a DWH can be used in at least two ways, which are not mutually exclusive. The first recomposes data from the various original data marts to create new ones: for example, if we have created a DWH by aggregating data mart for several lines of products, we can create a new one for selling all those products in a certain geographical area. A new data mart is therefore created for every problem for which we want to develop quantitative analysis. 

A second way of using a DWH, which flanks the first, directly generates processing (albeit simplified) to extract certain information about the data summary. This is called _OnLine Analytical Processing_ (OLAP) and, as indicated by its name, is made up of querying and processing designed in a certain way to be a form of data analysis, although it is still raw and primarily descriptive. 

For OLAP, the general support is a structure of intermediate processing, called a _hypercube_ . In statistical terms, this is a _multiway table_ , in which every dimension corresponds to a variable, and every cell at the intersection of different levels contains a synthetic indicator, often a frequency. To give an example of this, let us presume that the statistical units are university students. One variable could be constructed by place of residence, another by department or university membership, gender, and so on, and the individual cells of the crosstable (hypercube) contain the frequencies for the various intersecting levels. This table can be used for several forms of processing: marginalization or conditioning with respect to one or more variables, level aggregation, and so on. They are described in introductory statistical texts and need no mention here. Note that in the field of computer science, the foregoing operations have different names. 

As already noted, OLAP is an initial form of the extraction of information from the data—relatively simple, at least from a conceptual point of view— operating from a table with predefined variables and a scope of operations limited to them. Therefore, strictly speaking, OLAP returns to data mining as defined in section 1.1.2, but limited to a form that is conceptually a very simple way of processing. Instead, “data mining” commonly refers to the inspection of a strategic database and is characteristically more investigative in nature, typically involving the identification of relations in certain significant ways among variables or making specific and interesting patterns of the data. The distinction between OLAP and data mining is therefore not completely clear, but essentially—as already noted—the former involves inspecting a small number of prespecified variables and has a limited number of operations, and the latter refers to a more open and more clearly focused study on extracting knowledge from the data. For the latter type of processing, much more computational than simple management, it is not convenient to use SQL, because SQL does not provide simple commands for intensive statistical processing. Alternatives are discussed later. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

8 

We can now think of a chain of phases, starting as follows: 

- one or more operational databases to construct a strategic database (DWH): this also involves an operation in which we homogenize the definition of variables and data cleaning operations; 

- we apply OLAP tools to this new database, to highlight points of interest on variables singled out previously; 

- data mining is the most specific phase of data analysis, and aims at finding interesting elements in specific data marts extracted from the DWH. 

The term _Knowledge Discovery in Databases_ (KDD) is used to refer to this complex chain, but this terminology is not unanimously accepted and _data mining_ is sometimes used as a synonym. In this work, data mining is intended in the more restricted sense, which regards only the final phases of those described. 

## 1.1.4 Complications 

We have already touched on some aspects that differentiate data mining from other areas of data analysis. We now elaborate this point. 

In many cases, data were collected for reasons other than statistical analysis. In particular, in the business sector, data are compiled primarily for accounting purposes. This administrative requirement led to ways of organizing these data becomingmorecomplex;therealizationthattheycouldbeusedforotherpurposes, that is, marketing analysis and CRM, came later. 

Data, therefore, do not correspond to any sampling plan or experimental design: they simply ‘exist’. The lack of canonical conditions for proper data collection initially kept many statisticians away from the field of data mining, whereas information technology (IT) experts were more prompt in exploiting this challenge. 

Even without these problems, we must also consider data collected in spurious forms. This naturally entails greater difficulties and corresponding attention to other applicative contexts. 

The first extremely simple but useful observation in this sense has to do with the validity of our conclusions. Because a company’s customer database does not represent a random sample of the total population, the conclusions we may draw from it cover at most already acquired customers, not prospective ones. 

Another reason for the initial reluctance of statisticians to enter the field of data mining was a second element, already mentioned in section 1.1.2—that is, research sometimes focuses on an objective that was not declared a priori. When we research ‘anything’, we end up finding ‘something’ _. . ._ even if it is not there. To illustrate this idea intuitively, assume that we are examining a sequence of random numbers: ultimately, it seems that there is some regularity, at least if we examine a sequence that is not too long. At this point, we must recall an aphorism coined by an economist, which is very fashionable among applied statisticians: “If you torture the data long enough, Nature will always confess” (Ronald H. Coase, 1991 Nobel Prize for Economics). 

Introduction 

9 

This practice of “looking for something” (when we do not know exactly what it is) is therefore misleading, and thus the associated terms _data snooping_ or _data dredging_ have negative connotations. When confronted with a considerable amount of data, the danger of false findings decreases but is not eliminated altogether. There are, however, techniques to counter this, as we shall see in chapter 3. 

One particularity, which seems trivial, regards the so-called leaker variables, which are essentially surrogates of the variables of interest. For example, if the variable of interest is the amount of money spent on telephone traffic by one customer in one month, a leaker variable is given by the number of phone calls made in that same month, as the first variable is recorded at the same moment as the second variable. Conceptually, the situation is trivial, but when hundreds of variables, often of different origin, are manipulated, this eventuality is not as remote as it may appear. It at least signals the danger of using technology blindly, inserting whole lists of variables without worrying about what they represent. We return to this point in section 1.3.1. 

## _Bibliographical notes_ 

Hand et al. (2001) depict a broad picture of data mining, its connections with other disciplines, and its general principles, although they do not enter into detailed technical aspects. In particular, their chapter 12 contains a more highly developed explanation of our section 1.1.3 about relationships between data management and some techniques, like OLAP, closer to that context. 

For descriptive statistics regarding tables of frequency and their handling, there is a vast amount of literature, which started in the early stages of statistics and is still developing. Some classical texts are Kendall & Stuart (1969, sections 1.30–1.34), Bishop et al. (1975), and Agresti (2002). 

For a more detailed description of the role of data mining in the corporate context, in particular its connections with business promotion, see the first chapters of Berry & Linoff (1997). 

## 1.2 ALL MODELS ARE WRONG 

All models are wrong but some are useful. 

—GEORGE E. P. BOX 

## 1.2.1 What is a Model? 

The term _model_ is very fashionable in many contexts, mainly in the fields of science and technology and also business management. Because the important attributes of this term (which are often implicit) are so varied and often blurred, let us clarify at once what we mean by it: 

A model is a simplified representation of the phenomenon of interest, functional for a specific objective. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

10 

In addition, certain aspects of this definition must be noted: 

- We must deal with a _simplified representation_ : an identical or almost identical copy would not be of use, because it would maintain all the complexity of the initial phenomenon. What we need is to reduce it and eliminate aspects that are not essential to the aim and still maintain important aspects. 

- If the model is to be _functional for a specific objective_ , we may easily have different models for the same phenomenon according to our aims. For example, the design of a new car may include the development of a mechanical or mathematical model, as the construction of a physical model (a real object) is required to study aerodynamic characteristics in a wind tunnel. Each of these models—obviously very different from each other—has a specific function and is not completely replaceable by the other. 

- Once the aspect of the phenomenon we want to describe is established, there are still wide margins of choice for the way we explain relationships between components. 

- Therefore, this construction of a “simplified representation” may occupy various dimensions: level of simplification, choice of real-life elements to be reproduced, and the nature of the relationships between the components. It therefore follows that a “true model” does not exist. 

- Inevitably, the model will be “wrong”—but it must be “wrong” to be useful. 

We can apply these comments to the idea of a model defined in general terms, and therefore also to the specific case of mathematical models. This term refers to any conceptual representation in which relations between the entities involved are explained by mathematical relationships, both written in mathematical notation and translated into a computer program. 

In some fields, generally those connected with the exact sciences, we can think of the concept of a “true” model as describing the precise mechanics that regulate the phenomenon of interest. In this sense, a classical example is that of the kinematic laws regulating the fall of a mass in a vacuum; here, it is justifiable to think of these laws as quite faithfully describing mechanisms that regulate reality. 

It is not our purpose to enter into a detailed discussion arguing that in reality, even in this case, we are effectively completing an operation of simplification. However, it is obvious that outside the so-called exact sciences, the picture changes radically, and the construction of a “true” model describing the exact mechanisms that regulate the phenomenon of interest is impossible. 

There are extensive areas—mainly but not only in scientific research—in which, although there is no available theory that is complete and acquired from the phenomenon, we can use an at least partially accredited theoretical formulation by means of controlled experimentation of important factors. 

In other fields, mostly outside the sciences, models have purely operative functions, often regulated only by the criterion “all it has to do is work,” that is, without the pretext of reproducing even partially the mechanism that regulates 

Introduction 

11 

the functioning of the phenomenon in question. This approach to formulation is often associated with the phrase “black-box model,” borrowed from the field of control engineering. 

## 1.2.2 From Data to Model 

Since we are working in empirical contexts and not solely speculatively, the data collected from a phenomenon constitutes the base on which to construct a model. How we proceed varies radically, depending on the problems and the context in which we are required to operate. 

The most favorable context is certainly that of experimentation, in which we control experimental factors and observe the behavior of the variables of interest as those factors change. 

In this context, we have a wide range of methods available. In particular, there is an enormous repertoire of statistical techniques for planning experiments, analyzing the results, and interpreting the outcomes. 

It should be noted that “experimenting” does not signify that we imagine ourselves inside a scientific laboratory. To give a simple example: to analyze the effect of a publicity campaign in a local newspaper, a company selects two cities with similar socioeconomic structure, and applies the treatment (that is, it begins the publicity campaign) to only one of them. In all other aspects (existence of other promotional actions, etc.), the two cities may be considered equivalent. At a certain moment after the campaign, data on the sales of goods in the two cities become available. The results may be configured as an experiment on the effects of the publicity campaign, if all the factors required for determining sales levels have been carefully controlled, in the sense that they are maintained at an essentially equivalent level in both cities. One example in which factors are not controlled may arise from the unfortunate case of promotional actions by competitors that take place at the same time but are not the same in the two cities. 

However, clearly an experiment is generally difficult in real-world environment, so it is much more common to conduct observational studies. These are characterized by the fact that because we cannot control all the factors relative to the phenomenon, we limit ourselves merely to observing them. This type of study also gives important and reliable information, again supported by a wide range of statistical techniques. However, there are considerable differences, the greatest of which is the difficulty of identifying causal links among the variables. In an experimental study in which the remaining experimental factors are controlled, we can say that any change in variable of interest _Y_ as variable _X_ (which we regulate) changes involves a causal relationship between _X_ and _Y_ . This is not true in an observational study, because both may vary due to the effect of an external (not controlled) factor _Z_ , which influences both _X_ and _Y_ . 

However, this is not the place to examine the organization and planning of experimental or observational studies. Rather, we are concerned with problems arising in the analysis and interpretation of this kind of data. 

There are common cases in which the data do not fallwithinanyofthepreceding types. We often find ourselves dealing with situations in which the data were collected for different aims than those we intend to work on now. A common 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

12 

case occurs in business, when the data were gathered for contact or management purposes but are then used for marketing. Here, it is necessary to ask whether they can be recycled for an aim that is different from the original one and whether statistical analysis of data of this type can maintain its validity. A typical critical aspect is that the data may create a sample that is not representative of the new phenomenon of interest. 

Therefore, before beginning data analysis, we must have a clear idea of the nature and validity of the data and how they represent the phenomenon of interest to avoid the risk of making disastrous choices in later analysis. 

Bibliographic notes Two interesting works that clearly illustrate opposing styles of conducting real data analysis are those by Cox (1997) and Breiman (2001b). The latter is followed by a lively discussion in which, among others, David Cox participated, with a rejoinder by Breiman. 

## 1.3 A MATTER OF STYLE 

## 1.3.1 Press the Button? 

The previous considerations, particularly those concluding the section, show how important it is to reflect carefully on the nature of the problem facing us: how to collect data, and above all how to exploit them. These issues certainly cannot be resolved by computer. 

However, this need to understand the problem does not stop at the preliminary phase of planning but underlies every phase of the analysis itself, ending with interpretation of results. Although we tend to proceed according to a logic that is much more practical than in other environments, often resulting in black-box models, this does not mean we can handle every problem by using a large program (software, package, tool, system, etc.) in a large computer and pushing a button. 

Although many methods and algorithms have been developed, becoming increasingly more refined and flexible and able to adapt ever more closely to the data even in a computerized way, we cannot completely discard the contribution of the analyst. We must bear in mind that “pressing the button” means starting an algorithm, based on a method and an objective function of which we may or may not be aware. Those who choose to ‘press the button’ without this knowledge simply do not know which method is used, or only know the name of the method they are using, but are not aware of its advantages and disadvantages. 

More or less advanced knowledge of the nature and function of methods is essential for at least three reasons: 

1. An understanding of tool characteristics is vital in order to choose the most suitable method. 

2. The same type of control is required for correct interpretation of the results produced by the algorithms. 

3. Acertaincompetenceincomputationalandalgorithmicalaspectsishelpful to better evaluate the _output_ of the computer, also in terms of its reliability. 

Introduction 

13 

The third point requires clarification, as computer output is often perceived as secure and indisputable information. Many of the techniques currently applied involve nontrival computational aspects and the use of iterative algorithms. The convergence of these algorithms on the solution defined by the method is seldom guaranteed by its theoretical basis. The most common version of this problem occurs when a specific method is defined as the optimal solution of a certain objective function that is minimized (or maximized), but the algorithm may converge on a optimal point which is local and not global, thus generating incorrect computer output without the user realizing it. However, these problemsarenotuniformamongdifferentmethods;therefore,knowingthevarious characteristics of the methods, even from this aspect, has important applicative value. 

The choice of style to be accomplished here, corroborated by practical experience, is that of combining up-to-date methods with an understanding of the problems inherent in the subject matter. 

This point of view explains why, in the following chapters, various techniques are presented from the viewpoints not only of their operative aspects but also (albeit concisely) of their statistical and mathematical features. 

Our presentation of the techniques is accompanied by examples of real-life problems, simplified for the sake of clarity. This involves the use of a software tool of reference. There are many such products, and in recent years software manufacturers have developed impressive and often valuable products. 

## 1.3.2 Tools for Computation and Graphics 

In this work, we adopt R (R Development Core Team, 2011) as the software of choice, because it constitutes a language and an environment for statistical calculations and graphical representation of data, available free at http://www.r-project.org/ in _open-source_ form. The reasons for this choice are numerous. 

- In terms of quality, R is one of the best products currently available, inspired by the environment and language S, developed in the laboratories of AT&T. 

- The fact that R is free is an obvious advantage, which becomes even more significant in the teaching context, in which—because it is easily accessible to all—it has an ideal property on which to construct a common working basis. 

- However, the fact that it is free does not mean that it is of little value: R is developed and constantly updated by the R Development Core Team, composed of a group of experts at the highest scientific level. 

- Because R is a language, it lends itself easily to programming of variants of existing methods, or the formulation of new ones. 

- In addition to the wide range of methods in the basic installation of R, additional packages are available. The set of techniques thus covers the whole spectrum of the existing methods. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

14 

- R can interact in close synergy with other programs designed for different or collateral aims. In particular, cooperation between R and a relational database or tools of dynamic graphic representation may exist. 

- This extendibility of R is facilitated by the fact that we are dealing with an _open-source_ environment and the consequent transparency of the algorithms. This means that anyone can contribute to the project, both with additional packages for specific methods and for reporting and correcting errors. 

- The syntax of R is such that users are easily made aware of the way the methods work. 

The set of exploitable data mining methods by means of R are the same as those that underlie commercial products and constitute their engine. The choice of R as our working environment signifies that although we forgo the ease and simplicity of a graphic interface, we gain in knowledge and in control of what we are doing. 

2 

## A–B–C 

Everything should be made as simple as possible, but not simpler. 

—Attributed to ALBERT EINSTEIN 

## 2.1 OLD FRIENDS: LINEAR MODELS 

## 2.1.1 Basic Concepts 

Let us start with a simple practical problem: we have to identify a relationship that allows us to predict the consumption of fuel or, equivalently, the distance covered per unit of fuel as a function of certain characteristics of a car. We consider data for 203 models of cars in circulation in 1985 in the United States, but produced elsewhere. Twenty-seven of their characteristics are available, four of which are shown in figure 2.1: city distance (km/L), engine size (L), number of cylinders, and curb weight (kg). The data are marked in different ways according to fuel type (gasoline or diesel). 

Some of the available characteristics are numerical: city distance, engine size, and curb weight are quantitative and continuous, and number of cylinders is quantitative and discrete. However, fuel type is qualitative; equivalent terms are _categorical variable_ and _factor_ . 

16 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

**==> picture [328 x 328] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 2 3 4 5 800 1200 1600<br>City<br>distance<br>Engine<br>size<br>Number of<br>cylinders<br>Curb<br>weight<br>5 10 15 20 2 4 6 8 10 12<br>20<br>15<br>10<br>5<br>5<br>4<br>3<br>2<br>1<br>12<br>10<br>8<br>6<br>4<br>2<br>1600<br>1200<br>800<br>**----- End of picture text -----**<br>


Figure 2.1 Matrix of scatterplots of some variables of car data, stratified by fuel type. Circles: gasoline; triangles: diesel. 

In this case, when we are dealing with few data, we can represent them as a _scatterplot_ , as in figure 2.1; in other cases, we would have to think of more elaborate representations. 

In the first phase, for simplicity, we consider only two explanatory variables: engine size and fuel type, of which the former is quantitative and the latter qualitative. To study the relationship between quantitative variables, the first thing to make is a graphic representation, as in figure 2.2. 

To study the relationship between two variables (for the moment leaving aside fuel type, which acts as a qualitative _stratification_ variable), any statistics primer would first suggest a simple linear regression line, of the type 

**==> picture [204 x 12] intentionally omitted <==**

where _y_ represents city distance, _x_ fuel type, and _ε_ is a nonobservable random ‘error’ term, which we assume to be of zero mean and constant but unknown variance _σ_[2] . We also assume lack of correlation among error terms and 

A–B–C 

17 

**==> picture [273 x 270] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gasoline<br>Diesel<br>1 2 3 4 5<br>Engine size (L)<br>20<br>15<br>Urban distance (km/L)<br>10<br>5<br>**----- End of picture text -----**<br>


Figure 2.2 Car data, scatterplot of engine size and city distance, stratified by fuel type. 

therefore also among observations _y_ for differing units. This set of hypothesis is called ‘of the second-order’ because it involves mean, variance, and covariance, which are second-order moments. 

We are looking for an estimate of unknown _regression parameters β_ 0 and _β_ 1 using _n_ (in this case _n_ = 203) pairs of observations, denoted by ( _xi, yi_ ), for _i_ = 1 _, . . . , n_ . Equation (2.1) is the simplest case for a more general formulation of the type 

**==> picture [201 x 12] intentionally omitted <==**

which becomes (2.1) when _f_ is the expression of the straight line and _β_ = ( _β_ 0 _, β_ 1)[⊤] . 

To estimate _β_ , the _least squares criterion_ leads us to identify the values for which we obtain the minimum, with respect to _β_ , of the _objective function_ 

**==> picture [263 x 31] intentionally omitted <==**

where the last expression uses matrix notation to represent vector _y_ = ( _y_ 1 _, . . . , yn_ )[⊤] ; _f_ ( _x_ ; _β_ ) = ( _f_ ( _x_ 1; _β_ ) _, . . . , f_ ( _xn_ ; _β_ ))[⊤] ; and ∥· ∥ indicates the _Euclidean norm_ of the vector, that is, the square root of the sum of squares of the elements. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

18 

The solution to this minimization problem is shown by _β_[ˆ] , and we indicate the corresponding _fitted values_ 

**==> picture [138 x 13] intentionally omitted <==**

which, in the linear case (2.1), are of the type 

**==> picture [99 x 14] intentionally omitted <==**

where ˜ _xi_[⊤][=][ (1] _[,][ x][i]_[).] 

From the same formula, we can also write the expression of the _predicted value_ 

**==> picture [68 x 14] intentionally omitted <==**

for a value _x_ 0 of the explanatory variable, which does not necessarily correspond to any observation. 

Clearly, however, the trend of the relationship in figure 2.2 does not lend itself to being expressed by a straight line. At this point, we can move in several alternative directions. The most immediate one is probably to consider a more elaborate form of function _f_ ( _x_ ; _β_ ), for instance, a polynomial form 

**==> picture [250 x 14] intentionally omitted <==**

where _β_ is now a vector with _p_ components, _β_ = ( _β_ 0 _, β_ 1 _, . . . , βp_ −1)[⊤] . Using a polynomial function has the double advantage of (1) being conceptually and mathematically simple, and (2) offering simple treatment regarding the use of the least squares criterion. 

Because (2.4) is _linear in the parameters_ , it can be rewritten as 

**==> picture [196 x 12] intentionally omitted <==**

where _X_ is an _n_ × _p_ matrix, called the _design matrix_ , defined by 

**==> picture [92 x 13] intentionally omitted <==**

where _x_ is the vector of the observations of the explanatory variable, and the various columns of _X_ contain powers of order from 0 to _p_ − 1 of elements of _x_ . The complete entry is therefore a particular case of a _linear model_ 

**==> picture [191 x 12] intentionally omitted <==**

in which _X_ refers to a polynomial regression, corresponding to (2.4). 

A–B–C 

19 

In this formulation, the explicit solution to the minimization problem of (2.3) is 

**==> picture [206 x 14] intentionally omitted <==**

**==> picture [194 x 13] intentionally omitted <==**

where 

**==> picture [207 x 13] intentionally omitted <==**

is an _n_ × _n_ matrix, called the _projection matrix_ . Properties _P_[⊤] = _P_ , _P P_ = _P_ hold, as does tr( _P_ ) = rk( _P_ ) = _p_ . 

The minimum value of (2.3) may be written in various equivalent forms 

**==> picture [269 x 14] intentionally omitted <==**

where _In_ denotes the identity matrix of order _n_ . Quantity _D_ = _D_ ( _β_[ˆ] ) is called _deviance_ , in that it is a quantification of the discrepancy between fitted and observed values. 

From here, we also obtain the estimate of _σ_[2] , usually given by 

**==> picture [189 x 29] intentionally omitted <==**

and this allows us to assess the variance of the estimates of _β_ through 

**==> picture [213 x 13] intentionally omitted <==**

The square root of the diagonal elements of (2.12) yields the _standard errors_ of the components of _β_[ˆ] —essential for inferential procedures, as we shall see shortly. 

A somewhat more detailed explanation of linear model concepts and least squares is given in Appendix A.3. 

In the case of the data in figure 2.2, it is plausible to use _p_ = 3 or even _p_ = 4. In any case, we still need one more element to treat the data effectively, and this is the qualitative variable fuel type. A nonnumerical variable must be conveniently encoded by _indicator variables_ ; if the possible _levels_ assumed by the variable are _k_ , then the number of required indicator variables is _k_ − 1. In this case, we need a single indicator variable, because fuel type may have two levels, diesel and gasoline. There is an infinite number of choices, provided that each is associated with a single value of the indicator variable. One particularly simple choice is to assign value 1 to the level diesel and value 0 to the level gasoline; we indicate this new variable with _IA_ . 

The simplest way to insert _IA_ into the model is additive, which is equivalent to presuming that the average difference of the distance covered by two 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

20 

_Table 2.1._ CAR DATA: ESTIMATES AND ASSOCIATED QUANTITIES FOR MODEL (2.14) 

||Estimate|SE|_t_-value|_p_-value|
|---|---|---|---|---|
|(intercept)|24_._832|3_._02|8_._21|0.000|
|(engine size)|−10_._980|3_._53|−3_._11|0.002|
|(engine size)2|2_._098|1_._27|1_._65|0.100|
|(engine size)3|−0_._131|0_._14|−0_._94|0.349|
|fuel.diesel|3_._214|0_._43|7_._52|0.000|



groups of diesel and gasoline cars is constant for any engine size. This simplified hypothesis is called the _additive hypothesis_ of the effects. Also, if the additive hypothesis is not completely valid, this formulation constitutes a first approximation, which is often the most important part of the influence of the factor. This component, entered in an additive form, is therefore called the _main effect_ of the factor. 

This choice means that matrix _X_ of (2.5) is now extended with the addition of a new column containing _IA_ . Function _f_ ( _x_ ; _β_ ) and matrix _X_ are therefore substituted by the new expressions 

**==> picture [330 x 26] intentionally omitted <==**

Correspondingly, we add a new component to vector _β_ , which, given the specific form adopted by the dummy variable, represents the average deviation of the distance covered between diesel or gasoline cars. 

Adopting this scheme for the data in figure 2.2, with _p_ = 4, means that the linear model is specified in the form 

**==> picture [248 x 13] intentionally omitted <==**

of which the estimates and _standard errors_ are listed in table 2.1, together with the normalized value of estimate _t_ = estimate _/_ (standard error) and the corresponding _p_ -value, or _observed significance level_ , which we obtain if we can introduce the additional hypothesis of _normal or Gaussian distribution_ for the error terms _ε_ of (2.2). The estimated curves identified by these parameters are shown in figure 2.3. 

To evaluate the goodness of fit, we need to calculate the _coefficient of determination_ 

**==> picture [307 x 29] intentionally omitted <==**

where _D_ ( _β_[ˆ] ) is calculated by (2.10) using _X_ , the matrix corresponding to model ¯ (2.14); and _y_ =[�] _i[y][i][/][n]_[indicates][the][arithmetic][mean][or] _[average]_[of] _[y][i]_[.][In][this] specific case, we obtain _R_[2] = 0 _._ 60, which indicates a fair degree of correlation between observed and interpolated data. 

A–B–C 

21 

**==> picture [236 x 234] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gasoline<br>Diesel<br>1 2 3 4 5<br>Engine size<br>20<br>15<br>City distance<br>10<br>5<br>**----- End of picture text -----**<br>


Figure 2.3 Car data: fitted curves relative to model (2.14). 

However, we cannot reduce evaluation of the adequacy of a model to consideration of a single indicator. Other indications are provided by _graphical diagnostics_ . There are several of these, and they all bring us back more or less explicitly to examination of the behavior of the _residuals_ 

**==> picture [231 x 12] intentionally omitted <==**

which serve as surrogates of errors _εi_ , which are not observable. The residuals have various aspects that we must evaluate according to various assumptions. Among the many diagnostic tools, two of the most frequently used are shown in figure 2.4. 

Figure 2.4 (left) shows the _Anscombe plot_ of the residuals with respect to the interpolated values, which would ideally have to present random scattering of all points if the selected model is to be deemed valid. In our case, it is evident that the variability of the residuals increases from left to right, signaling a probable violation of _homoscedasticity_ —that is, var { _εi_ } must be a constant, say, _σ_[2] , independent of index _i_ —whereas here the graphic indicates something very different. 

Figure 2.4 (right) shows the _quantile-quantile plot_ for verification of the normality assumption for the distribution of _εi_ . The _y_ -axis gives the values of _ε_ ˆ _i_ , conveniently standardized and ordered in increasing terms, and the _x_ -axis shows the corresponding expected values under the normality hypothesis, approximated (if necessary) for simplicity of calculation. 

If the normal hypothesis is valid, we expect the observed points to lie along the bisector of the first and third quadrants. In this case, the data behave differently and do not conform to the normal hypothesis. In more detail, the central part of 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

22 

**==> picture [329 x 171] intentionally omitted <==**

**----- Start of picture text -----**<br>
Residuals vs fitted Normal Q−Q<br>31 31<br>5 67<br>56 57<br>6 8 10 12 14 16 −3 −2 −1 0 1 2 3<br>Fitted values Theoretical quantiles<br>10<br>4<br>5<br>2<br>0<br>0<br>Residuals<br>Standardized residuals −2<br>−5<br>−4<br>**----- End of picture text -----**<br>


Figure 2.4 Car data: graphical diagnostics for model (2.14). 

the diagram shows a trend that is quite satisfactory, although not ideal. The part of the graph that conforms least to expectations lies in the _tails_ of the distribution, the portion outside interval (−2 _,_ 2). Specifically, the observed residuals are of much larger absolute value than the expected ones, indicating _heavy tails_ with respect to the normal curve. 

Thus, using a simple linear model (2.14) suggests the following points, some of which, with necessary modifications, we find in other applications of linear models. 

- The goodness of fit of the linear model of figure 2.3 is satisfactory on first analysis, especially if we want to use it to predict the city distance covered by a car of average engine size (i.e., between 1.5 and 3 L). 

- The construction of the model is so simple, both conceptually and computationally, that in some cases, these methods can be applied automatically. 

- Despite the superficially satisfactory trend of figure 2.3, the graphical diagnostics of figure 2.4 reveal aspects that are not satisfied. 

- The model is not suitable for _extrapolation_ , that is, for predicting the value of the variable outside the interval of observed values for the explanatory variables. This is seen in the example of the set of diesel cars with engines larger than 3 L, when the predicted values become completely unrealistic. 

- The model has no grounding in physics or engineering, which leads to interpretive difficulties and adds paradoxical elements to the expected trend. For example, the curve of the set of gasoline cars shows a local minimum around 4.6 L, and then rises again! 

This type of evaluation of a model’s critical elements is not confined to linear models (see chapter 4). 

A–B–C 

23 

## 2.1.2 Variable Transformations 

We must explain what we mean by ‘linear’: these are models which are linear with respect to _parameters_ , but we can use nonlinear variable transformations of both _y_ and _xi_ , which may be different for different variables. In addition, we can use as many transformations as we need, for example, _x_ 1 and _x_ 2 can give place to _X_ = (1 _, x_ 1 _, x_ 2 _, x_ 1 _/x_ 2 _, e[x]_ 2[2][+] _[x]_[1] ). This flexibility of use, with respect to the basic formulation, is one of the successful features of linear models. 

We already used this possibility in formulating polynomial model (2.14), which is a common variant, but we can also use many others, including transformations of the response variable. The theoretical structure remains unchanged, although in this case the objective function (2.3), and therefore the optimality criterion, work on the transformed scale. 

In the foregoing examples, it is reasonable to consider fuel consumption per km as a response variable instead of distance covered. Hence, we can write 

**==> picture [300 x 12] intentionally omitted <==**

where consumption = 1/(distance covered). Obviously, here, error term _ε_ and parameters _βj_ are not the same as those in (2.14), but the same hypotheses on the nature of the error component are retained. Figure 2.5 shows the scatterplot of the new variables, with two regression lines, the coefficients of which are listed in table 2.2. 

Some simple observations may be made: (1) the trend of the points in figure 2.5 shows good alignment; (2) this is reinforced by the value of _R_[2] , which is 0 _._ 64; (3) therefore, it is not necessary to draw on polynomials of higher order. However, it is useful to report the trend of the new estimated function on the original scale, which also allows comparisons with the previous estimate. The new estimated function is shown in figure 2.6, and is much more convincing, particularly in the edges of the explanatory variable engine size. To be comparable with model (2.14), _R_[2] is now recalculated to its original scale, giving a value of 0 _._ 56. The corresponding graphical diagnostics are shown in figure 2.7. Although the fit of figure 2.5 appears to be acceptable, the graphical diagnostics continue to be unsatisfactory. 

Another type of transformation often used is the logarithm. In this case, it is also reasonable to transform both the explanatory variable and the response variable, 

_Table 2.2._ CAR DATA: ESTIMATES AND ASSOCIATED QUANTITIES OF MODEL (2.17) 

||Estimate|SE|_t_-value|_p_-value|
|---|---|---|---|---|
|(intercept)|0_._042|0.0035|11_._94|0.000|
|(engine size)|0_._029|0.0016|17_._94|0.000|
|fuel.diesel|−0_._025|0.0037|−6_._78|0.000|



D A T A A N A L Y S I S A N D D A T A M I N I N G 

24 

**==> picture [258 x 255] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 2 3 4 5<br>Engine size<br>0.18<br>0.16<br>0.14<br>0.12<br>Consumption<br>0.10<br>0.08<br>0.06<br>**----- End of picture text -----**<br>


Figure 2.5 Car data: scatterplot of engine size and consumption, with regression lines of model (2.17). 

## aiming for the formulation 

## log(distance covered) = _β_ 0 + _β_ 1 log(engine size) + _β_ 2 _IA_ + _ε._ 

(2.18) 

Logarithmictransformationsareoftenusedwhenintrinsicallypositivequantities are involved, such as distance covered and engine size. They have the advantage of allowing us to operate on variables that vary in (−∞ _,_ ∞), that is, the “right” support for linear models. In turn, this fact means that once the transformation is inverted, we are certain of obtaining positive quantities for the predicted values of the response variable. An additional advantage of logarithmic transformations is that they often correct the heteroscedasticity of the residuals. 

Table 2.3 summarizes the fitted model, figure 2.8 shows the fitted curves on both transformed and original scales, and figure 2.9 shows the graphical diagnostics for the linear model. We can now deduce that model (2.18) is preferable to (2.14), but the graphical diagnostics remain substantially unsatisfactory. 

Much of the inadequacy of model (2.18) is due to the persistence of heteroscedasticity in the residuals, as clearly shown in the left side of figure 2.9, as in figures 2.4 and 2.7. In turn, this heteroscedasticity is probably due to a _heterogeneity_ in observed cases that is not adequately ‘explained’ by the explanatory variables. 

To remedy this inconvenience, we have many other variables at our disposal. In particular, basic evaluations lead us to consider the curb weight of the car 

A–B–C 

25 

**==> picture [256 x 254] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gasoline<br>Diesel<br>1 2 3 4 5<br>Engine size<br>20<br>15<br>City distance<br>10<br>5<br>**----- End of picture text -----**<br>


Figure 2.6 Car data: scatterplot of engine size and distance covered with curves fitted to model (2.17). 

**==> picture [325 x 164] intentionally omitted <==**

**----- Start of picture text -----**<br>
Residuals vs fitted Normal Q−Q<br>59 59<br>5 67 5657<br>0.06 0.08 0.10 0.12 0.14 0.16 0.18 0.20 −3 −2 −1 0 1 2 3<br>Fitted values Theoretical quantiles<br>0.08<br>4<br>0.06<br>0.04<br>2<br>0.02<br>Residuals<br>0.00 0<br>Standardized residuals<br>−0.02<br>−2<br>−0.04<br>**----- End of picture text -----**<br>


Figure 2.7 Car data: graphical diagnostics of model (2.17). 

as an important variable. For reasons already mentioned with respect to the other two continuous variables, it makes sense to consider curb weight through its logarithmic transformation. 

Another feature to take into account is the anomalous position of the two points in the bottom left corner of figure 2.2, which are never interpolated appropriately 

26 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

_Table 2.3._ CAR DATA: ESTIMATES AND ASSOCIATED QUANTITIES OF MODEL (2.18) 

||Estimate|SE|_t_-value|_p_-value|
|---|---|---|---|---|
|(intercept)|2_._782|0.0295|94_._30|0.000|
|log(engine size)|−0_._682|0.0398|−17_._13|0.000|
|fuel.diesel|0_._278|0.0379|7_._34|0.000|



**==> picture [330 x 163] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gasoline<br>Diesel<br>0.0 0.5 1.0 1.5 1 2 3 4 5<br>Log (engine size) Engine size (L)<br>3.0 20<br>2.8<br>2.6<br>15<br>2.4<br>2.2<br>Log (city distance) City distance (km/L) 10<br>2.0<br>1.8<br>5<br>**----- End of picture text -----**<br>


Figure 2.8 Car data: scatterplots and fitted curves of model (2.18) on transformed (left) and natural scales (right). 

by any of the regression curves. They turn out to correspond to four cars, all with two-cylinder engines, and they are the only ones to have this characteristic. We must therefore add a new indicator variable, _ID_ , to the model, with a value of 1 if the engine has two cylinders and 0 otherwise. 

Combining the considerations of the last two paragraphs, we can formulate the new model 

log(distance covered) = _β_ 0 + _β_ 1 log(engine size) 

**==> picture [200 x 25] intentionally omitted <==**

for which table 2.4 lists the summary outcome of the estimation process. The value of _R_[2] is 0 _._ 88, and the corresponding value on the original scale is 0 _._ 87. These values are evidently much more convincing than the previous ones, even though the number of parameters has not been increased to any great extent. In addition, the graphical diagnostics of the residuals of figure 2.10 give a much better picture, although the residual distribution is slightly _skewed_ , highlighted by the mild convexity of the trend of the the quantile-quantile plot in the top right panel. 

In this case, we have added two extra graphic panels, containing the scatterplots of the residuals (transformed into the square roots of their absolute values) with 

A–B–C 

27 

**==> picture [330 x 170] intentionally omitted <==**

**----- Start of picture text -----**<br>
Residuals vs fitted Normal Q−Q<br>5 678<br>5657 58<br>1.6 1.8 2.0 2.2 2.4 2.6 2.8 −3 −2 −1 0 1 2 3<br>Fitted values Theoretical quantiles<br>4<br>0.5<br>2<br>0.0 0<br>Residuals<br>−2<br>Standardized residuals<br>−0.5<br>−4<br>**----- End of picture text -----**<br>


Figure 2.9 Car data: graphical diagnostics for model (2.18). 

_Table 2.4._ CAR DATA: ESTIMATES AND QUANTITIES FOR MODEL (2.19) 

||Estimate|SE|_t_-value|_p_-value|
|---|---|---|---|---|
|(intercept)|9_._07|0.475|19_._08|0.000|
|log(engine size)|−0_._18|0.051|−3_._50|0.001|
|fuel.diesel|0_._35|0.022|15_._93|0.000|
|cylinders.2|−0_._48|0.052|−9_._30|0.000|
|log(curb weight)|−0_._94|0.072|−13_._07|0.000|



respect to the estimated values, and the _Cook distance_ for every observation. The _Cook distance_ allows us to evaluate the effect on _β_[ˆ] produced by removing ( _xi, yi_ ) from the set of observations, and this perturbation of _β_[ˆ] is linked to a corresponding ˆ perturbation of _y_ . Therefore, the Cook distance provides an indicator of the _influence_ of this observation on the fitted model. Both diagrams are entirely satisfactory in that they show neither heteroscedasticity of residuals nor _influential observations_ . 

The meaning and interpretation of the numerical values in table 2.4 are largely according to expectations, in the sense that curb weight, engine size, and fuel type all correspond to common knowledge of the distance covered by a car, or rather, its logarithmic transformation, as examined here. 

However, a specific comment must be made regarding factor _ID_ , the coefficient of which has a negative sign and is of considerable statistical significance—in outstanding contrast with intuitive expectations, as a car with two cylinders should in fact consume less than the others, that is, it should have a positive _β_ 4 coefficient in the prediction of log(distance covered). 

The explanation of this apparently paradoxical behavior is due to the structure of the relationships between _all_ the variables involved, not only between the response and explanatory variables. In particular, figure 2.1 shows that the 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

28 

**==> picture [324 x 328] intentionally omitted <==**

**----- Start of picture text -----**<br>
Residuals vs fitted Normal Q−Q<br>31<br>31<br>154 154<br>159 159<br>1.8 2.0 2.2 2.4 2.6 2.8 −3 −2 −1 0 1 2 3<br>Fitted values Theoretical quantiles<br>Scale−location Cook's distance<br>31<br>154 154<br>159<br>31<br>173<br>1.8 2.0 2.2 2.4 2.6 2.8 0 50 100 150 200<br>Fitted values Obs. number<br>4<br>0.3<br>3<br>0.2<br>2<br>0.1<br>1<br>Residuals 0.0 0<br>Standardized residuals<br>−0.1 −1<br>−0.2 −2<br>0.30<br>1.5 0.25<br>0.20<br>1.0 0.15<br>Cook's distance<br>0.10<br>Standardized residuals 0.5<br>0.05<br>0.0 0.00<br>**----- End of picture text -----**<br>


Figure 2.10 Car data: graphical diagnostics for model (2.19). 

curb weight of the two-cylinder cars is similar to that of four-cylinder ones and much higher than those of three-cylinder cars, and this group of cars also behaves anomalously with respect to the general trend in the scatterplots for other variables. 

There are many ways of dealing with this type of situation. The simplest is adopted here: the indicator variable _ID_ of the anomalous group is inserted among the explanatory variables. Thus, the value of the estimate −0.48 for _β_ 4 is not interpreted in the sense that two-cylinder cars generally have a log(distance covered) that is 0.48 lower than that of the others: this is due to the particular way the fact of having two cylinders links up with the other explanatory variables, mainly curb weight. 

## 2.1.3 Multivariate Responses 

In some cases, there are several response variables of interest, for the same sets of units and explanatory variables. An immediate example comes from the car data themselves, and here it is interesting to consider not only city distance but 

A–B–C 

29 

also highway distance, so we examine the same set of explanatory variables in both responses. 

If there are _q_ response variables, we can construct a matrix _Y_ , the columns of which contain these _q_ variables. In our car example, _q_ = 2 and 

**==> picture [232 x 11] intentionally omitted <==**

If we create _q_ models of linear regression, each of type (2.6), using the same regression matrix _X_ for each, we obtain 

**==> picture [192 x 12] intentionally omitted <==**

where _B_ is the matrix formed of _q_ columns of dimension _p_ , each representing the regression parameters for the corresponding column of _Y_ , and matrix _E_ is made up of error terms. Here, too, each of its columns refers to the corresponding column of _Y_ , with the condition that 

**==> picture [55 x 14] intentionally omitted <==**

where _E_[˜] _i_[⊤][represents the] _[ i]_[th row] _[ E]_[, for] _[ i]_[=][1] _[, . . . ,][ n]_[, and] _[ �]_[is a variance matrix] of dimensions _q_ × _q_ independent of _i_ , which expresses the correlation structure between the error components and therefore also between the response variables. Equation (2.20) constitutes a model of _multivariate multiple linear regression_ , where the term ‘multivariate’ refers to _q_ response variables and ‘multiple’ to _p_ explanatory variables. 

The natural extension of the least squares criterion to the case of _q_ response variables is given by the sum of _q_ terms of type (2.3). Because this sum is minimal when each additive term is minimal, the solution to the multivariate least squares problem is 

**==> picture [207 x 14] intentionally omitted <==**

which is simply the juxtaposition of _q_ vectors estimated for each response variable. The corresponding estimate of _�_ is 

**==> picture [77 x 25] intentionally omitted <==**

of which the diagonal gives the terms equivalent to _s_[2] of (2.11), yielding standard errors, as in the scalar case, from (2.12). 

## _Bibliographical notes_ 

The treatment of linear models appears in a variety of styles and levels; we only mention a few references. For an introduction focusing on applicative use, see Weisberg (2005) and Cook & Weisberg (1999), who deal with extended aspects of graphical representation and the use of graphical diagnostics. A more formal treatment of linear models is in chapter 4 of Rao (1973). For the operational aspects, we refer to Venables & Ripley (2002, ch. 6). Classical methods 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

30 

for analysing multivariate response variables are provided by Mardia et al. (1979). 

## 2.2 COMPUTATIONAL ASPECTS 

Computational aspects take on a very important role in data mining. Let us start by referring to the linear models that represent their most simple algebraic formulation. 

The main element to be calculated is the estimate of _β_ in (2.7), and then the other quantities associated with it—in particular, estimate _s_[2] of _σ_[2] given by (2.11) and the relative standard errors of the components of _β_[ˆ] . 

## 2.2.1 Least Squares Estimation by Successive Orthogonalization 

As we saw in section 2.1.1, the solutions to least squares problems (2.7) and related quantities are all based on inversion of the ( _X_[⊤] _X_ ) matrix, and the most frequently used method of inverting symmetric matrices is based on Cholesky factorization. The solutions to least squares problems by this method has a computational cost of _p_[3] + _np_[2] _/_ 2 elementary operations (see, e.g., Trefethen & Bau, 1997, Lecture 11). 

However, a matrix can be inverted only if all its rows and columns are linearly independent—that is, in this case, if there is no linear dependence between the columns of _X_ . Clearly, if some columns of _X_ are almost linearly dependent, the solution of ( _X_[⊤] _X_ )[−][1] will probably be computationally unstable. The best situation is when all the columns of _X_ are orthogonal to each other, so that the inverse is obtained very efficiently. The Gram-Schmidt procedure, shown in algorithm 2.1, transforms the original variables sequentially, by successive orthogonalization yielding a new formulation of _X_ with orthogonal columns, so that the inverse of _X_[⊤] _X_ is easily obtained. 

The algorithm may be written in matrix form by considering the _QR_ decomposition of _X_ as the product of an _n_ × _p_ orthogonal matrix _Q_ , usually normalized so that _Q_[⊤] _Q_ = _I_ , and a _p_ × _p_ , upper triangular matrix _R_ . The least squares solution is therefore 

**==> picture [168 x 14] intentionally omitted <==**

where the inversion of _R_ is easy because it is a upper triangular matrix. 

The computational cost of least squares fitting by _QR_ decomposition requires approximately 2 _np_[2] operations, about twice that of direct inversion by Cholesky decomposition when _n_ ≫ _p_ and about the same when _p_ = _n_ . Depending on the number of variables and records available, we choose the most appropriate algorithm. 

## 2.2.2 When _n_ is Large 

However, when _n_ is large, the solutions presented in the last section become difficult to ascertain, because they involve handling matrices of dimensions _n_ × _p_ , which is time consuming. When _n_ is really very large, even simply loading _X_ into memory may be problematic. 

A–B–C 

31 

**Algorithm 2.1** Gram-Schmidt algorithm for least squares estimates 

**==> picture [133 x 10] intentionally omitted <==**

2. Cycle for _j_ = 1 _,_ 2 _, . . . , p_ − 1: regress _xj_ on _z_ 0, _z_ 1, …, _zj_ −1, to produce 

**==> picture [49 x 31] intentionally omitted <==**

**==> picture [233 x 34] intentionally omitted <==**

3. Regress _y_ on residual vector _zp_ −1 to give estimate _β_[ˆ] _p_ −1. 

A simple method of overcoming this problem is as follows. The elements necessary for calculating (2.7) are only 

**==> picture [114 x 14] intentionally omitted <==**

of dimensions _p_ × _p_ and _p_ × 1, respectively, where _W_ is the symmetric matrix, so we can write 

**==> picture [192 x 14] intentionally omitted <==**

Also, putting 

**==> picture [52 x 66] intentionally omitted <==**

where ˜ _xi_[⊤][is the] _[ i]_[th row of] _[ X]_[, we obtain] 

**==> picture [146 x 31] intentionally omitted <==**

We can also write 

**==> picture [312 x 16] intentionally omitted <==**

where _W_ ( _j_ ) is the matrix formed by the first _j_ summands of _W_ , and _u_ ( _j_ ) is defined analogously, starting from 

**==> picture [140 x 15] intentionally omitted <==**

It is now clear that _W_ and _u_ can be calculated by reading the data of a single _record_ at a time and increasing the sums gradually as the data are read, with a 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

32 

construction involving memory use independent of _n_ . At this point, _β_[ˆ] can be calculated by exploiting an algorithm for the inversion of symmetric matrices. The most frequently used method is based on Cholesky decomposition. If some of the columns of _X_ are made up at least partially of variables obtained by transforming the original data, such transformations can be performed progressively as the data are read. 

The previous procedure may also be extended to calculate _s_[2] and the standard errors of _β_ with a memory use independent of _n_ . 

## 2.2.3 Recursive Estimation 

When the data flow continuously (i.e., are a _data stream_ ) and we must update the estimates in real time, we need an algorithm that updates them recursively. 

The previous setting allows us to solve this problem, as there are no restrictions on _n_ . However, it does behave in a way that for every data read cycle, we must reinvert matrix _W_ , of dimensions _p_ × _p_ , and this may be problematic if _p_ is not small and the data flow fast. We can also improve our procedure by suitably manipulating the formulas. 

Let us presume that we have calculated the least squares estimates for the set of _n_ observations and that we have 

**==> picture [166 x 17] intentionally omitted <==**

where _n_ as a subscript reminds us that the quantities refer to the first _n_ observations. On reading the ( _n_ + 1)th observation, formed by _yn_ +1 and ˜ _xn_ +1, we must update the estimates and other connected quantities. We write 

**==> picture [316 x 33] intentionally omitted <==**

and use the Sherman-Morrison formula (A.2) to invert _W_ ( _n_ +1), obtaining 

**==> picture [153 x 15] intentionally omitted <==**

where _h_ = 1 _/_ (1 + ˜ _xn_[⊤] +1 _[V]_ ( _n_ ) _[x]_[˜] _[n]_[+][1][). After due substitutions in (2.22), we obtain the] recursive expression 

**==> picture [264 x 76] intentionally omitted <==**

where _en_ +1 represents the _prediction error_ of _yn_ +1 based on the estimate of _β_ obtained from the first _n_ observations. We thus have the new quantities _β_[ˆ] ( _n_ +1) and 

A–B–C 

33 

_V_ ( _n_ +1) = ( _X_ ([⊤] _n_ +1) _[X]_[(] _[n]_[+][1)][)][−][1][, with which we can resume the updating cycle from] the beginning. 

Making use of (A.2) in a similar fashion, we can also obtain a corresponding recursive form to calculate the sum of the squares of the residuals (2.10), that is, 

**==> picture [239 x 15] intentionally omitted <==**

where _Qn_ +1(·) is calculated with matrix _X_ ( _n_ +1) and response vector _y_ ( _n_ +1), and, analogously, _Qn_ (·) refers to the first _n_ observations. Equations (2.24) and (2.11) giveestimate _sn_[2] +1[,which,multipliedby] _[V]_ ( _n_ +1)[,yieldsthestandarderrorsof] _[β]_[ˆ] ( _n_ +1)[.] _β_ ˆ( _n_ The updating rule (2.23) takes the form of a+1) is obtained by modifying old estimate _β linear filter_ ˆ( _n_ ) according to prediction error, in which new estimate _en_ +1, weighted with the _gain kn_ of the filter. Using the terminology typical of the field of _machine learning_ , we say that the estimator “learns from its errors” by adjusting the current estimate each time, according to error _en_ +1. 

This scheme therefore calculates only a single inversion of the _p_ × _p_ matrix at first, and then we simply have to update the estimates and related quantities. When _n_ is very large, as when we work with a continuous data stream, we can further simplify the procedure, introducing an approximation that becomes negligible as _n_ increases. As in this case, the first _p_ observations have little influence on the total, and we can begin in whatever way we like—for example, with _β_[ˆ] ( _p_ ) equal to the zero vector and _V_ ( _p_ ) to the identity matrix of order _p_ , which essentially corresponds to following only step 6 of algorithm 2.2. In this way, the values of _β_[ˆ] are not the correct ones, but they tend to became so gradually as _n_ increases. 

This sequence of previous operations is shown schematically in algorithm 2.2. · The Diag( ) notation is used to indicate the diagonal elements of a general square matrix. 

## _Bibliographical notes_ 

An authoritative coverage of the computational aspects of least squares estimation is given by Golub & Van Loan (1983). The algorithm of recursive least squares was presented by Plackett (1950), who also refers to the original work of Gauss of 1821. 

## 2.3 LIKELIHOOD 

## 2.3.1 General Concepts 

Up to now we have reviewed cases in which the variable of interest ( _y_ ) was continuousandtheproblemofstudyingtherelationshipbetween _y_ andexplanatory variables ( _x_ 1 _, . . . , xp_ −1) could be managed through the least squares criterion. The latter finds its field of application more appropriate when the range of _y_ is (−∞ _,_ ∞). The most correct usage of associated inferential techniques is possible if the distribution of error terms _ε_ , and thus also of _y_ , is normal or Gaussian, at least approximately. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

34 

**Algorithm 2.2** Recursive linear least squares 

1. Let _W_ ( _p_ × _p_ ) ← 0, _u_ ( _p_ ×1) ← 0, Q ←0. 2. Cycle for _n_ = 1 _, . . . , p_ : a. read _n_ th record: _x_ ←˜ _xn_ , _y_ ← _yn_ , b. _W_ ← _W_ + _x x_[⊤] , c. _u_ ← _u_ + _x y_ . 3. _V_ ← _W_[−][1] . 4. _β_[ˆ] ← _V u_ . 5. Cycle for _n_ = _p_ + 1 _, p_ + 2 _, . . ._ : a. read _n_ th record: _x_ ←˜ _xn_ , _y_ ← _yn_ , b. _h_ ← 1 _/_ (1 + _x_[⊤] _V x_ ), c. _e_ ← _y_ − _x_[⊤] _β_[ˆ] , d. _β_[ˆ] ← _β_[ˆ] + _h V x e_ , e. _V_ ← _V_ − _h V x x_[⊤] _V_ , f. _Q_ ← _Q_ + _h e_[2] , g. _s_[2] ← _Q /_ ( _n_ − _p_ ), h. std.err( _β_[ˆ] ) ← _s_ Diag( _V_ )[1] _[/]_[2] . 

For many other cases, to fit a model to data, we need a more general criterion than that of least squares. From both theoretical and practical points of view, the preferred criterion for statistical estimation of model parameters is that of _maximum likelihood_ , which substantially comprises least squares as a special case. 

This criterion requires specification of a parametric family of probability distributions, dependent on a parameter _θ_ (possibly _p_ -dimensional) that must be estimated from available data. This probability distribution represents the law governing random variable _Y_ from which empirical value _y_ was observed. The distributionisidentifiedbyitsprobabilitydensityfunctioninthecaseofcontinuous variables, or by the probability function for discrete variables. We usually use the notation _p_ ( _t_ ; _θ_ ) to indicate this probability or density function, where _t_ varies in the set of possible values of _Y_ . 

With these hypotheses, we define the _likelihood function_ as 

**==> picture [200 x 12] intentionally omitted <==**

where _c_ is an arbitrary positive constant, but fixed once and for all. Because _p_ ( _t_ ; _θ_ ) is evaluated in observed value _y_ , the term on the left-hand side is a function only of _θ_ ; however, in some cases we use the notation _L_ ( _θ_ ; _y_ ) to show that it depends on observations. 

Equation (2.25) therefore constitutes a family of functions, indexed by _c_ . As _c_ plays a significant role only for the development of theoretical results but has no 

A–B–C 

35 

effect either on the use of _L_ ( _θ_ ) or on the properties of the associated inferential techniques, in the following we keep _c_ = 1. 

Because _p_ ( _y_ ; _θ_ ) is essentially positive, it makes sense to define the _log-likelihood function_ as 

**==> picture [212 x 12] intentionally omitted <==**

setting log _L_ ( _θ_ ) = −∞ if _p_ ( _y_ ; _θ_ ) = 0. 

We obtain the estimate of _θ_ according to the _maximum likelihood criterion_ by maximizing (2.25) or, equivalently, (2.26). We can also write 

**==> picture [244 x 18] intentionally omitted <==**

although this notation is not completely rigorous, because the existence and uniqueness of the maximum of L are not guaranteed. However, in the regular cases used in practice, this ambiguity does not occur because a unique global maximum exists. 

The actual maximization of _L_ can be explicitly obtained only in simple cases. In many others, we have to return to _numerical analysis_ methods to identify it. In regular cases, we have to resolve the system of _likelihood equations_ 

**==> picture [200 x 24] intentionally omitted <==**

and then verify that the resulting solution corresponds to a maximum point. It is, in fact, quite simple to check whether we have a local maximum, but its definition (2.27) requires selection of the _global_ maximum point. This can sometimes (but not always) be resolved by exploiting the mathematical properties of _p_ ( _y_ ; _θ_ ). We therefore see that this method can cause computational problems, at least in the case of complex models. 

Every estimate must be accompanied by quantification of its precision, and this requires evaluation of its variance. One of the advantages of the maximum likelihood method is that we have a general scheme available for it, starting from _Fisher’s observed information matrix_ 

**==> picture [234 x 28] intentionally omitted <==**

of which the inverse gives an approximation to var { _θ_[ˆ] }, in conditions that can be verified in most practical cases. We can therefore obtain standard errors for _θ_[ˆ] through 

**==> picture [129 x 14] intentionally omitted <==**

· where the Diag( ) notation indicates the diagonal elements of a square matrix. 

36 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

Combining these facts with the additional property of estimates of maximum likelihood, that is, they have an approximately normal distribution when sample size is sufficiently high, we obtain 

**==> picture [210 x 15] intentionally omitted <==**

to construct _confidence intervals_ of at least approximate level 1 − _α_ for the _r_ th component _θr_ of _θ_ ; here, _zα/_ 2 indicates the quantile of level 1 − _α/_ 2 of distribution N(0,1). 

This construction of a confidence interval for _θr_ is associated with the construction of a procedure for testing the _hypothesis_ 

**==> picture [50 x 11] intentionally omitted <==**

for a specified value _a_ . For fixed _statistical significance level α_ , _Wald’s test_ criterion leads to rejection of hypothesis _H_ 0 when | _t_ | _> zα/_ 2, because we put 

**==> picture [199 x 30] intentionally omitted <==**

and (2.30) is consequently called a Wald-type confidence interval. 

Equivalently, we can calculate the _p-value_ , or _observed significance level_ , approximated by 2 _�_ (−| _t_ |), which is compared with _α_ . 

Whenweareinterestedintestingahypothesisonthecomponentsof _θ_ expressed by _q_ constraints of the type 

**==> picture [237 x 13] intentionally omitted <==**

where _gj_ are differentiable functions, against the alternativethatatleastoneequality is false, the foregoing method cannot be used. Instead, we use the criterion of the _likelihood ratio_ , defined by the test function 

**==> picture [227 x 14] intentionally omitted <==**

where _θ_[ˆ] 0 indicatesthemaximumlikelihoodestimatesubjectto _q_ constraints(2.32). 

For a fixed significance level _α_ , the criterion leads to rejection of hypothesis _H_ 0[′] when observed value _w_ is greater than the 1 − _α_ quantile of distribution _χq_[2] . Here again, we can calculate the _p_ -value, now expressed by 

**==> picture [70 x 15] intentionally omitted <==**

where _X_[2] ∼ _χq_[2] , at least approximately and compare _p_ with _α_ . The distributive propertiesassociatedwiththeprocedureareexactinthecaseofnormaldistribution of observations and hypothesis _H_ 0[′][expressed by linear constraints; in other cases,] these properties are approximate. 

A–B–C 

37 

Note that the two testing procedures based on (2.31) and (2.33) are connected. When they are both applicable, they give identical (or at least approximately equal) results. This is because hypothesis _H_ 0 corresponding to a single linear constraint may be expressed as _H_ 0[′][=] _[θ][r]_[−] _[a]_[=][0,][and][2] _[�]_[(][−|] _[t]_[|][)][is][at][least][approximately] equal to P� _X_ 2 _> w_ �, where _w_ = _t_ 2 and _X_ 2 ∼ _χ_ 12[.] 

## 2.3.2 Linear Models with Gaussian Error Terms 

Discussion of the regression models of section 2.1 was based on specifying for error term _ε_ only hypotheses up to second-order moments (i.e., mean, variance, and covariance), but without formulating a complete hypothesis on the nature of the distribution of _ε_ , and therefore of the response variable. 

As already mentioned, the distributive hypothesis that assumes normal or Gaussian distribution for _ε_ , with independence between components for separate observations, is by far the most common and historically consolidated. Combining this fact with the contents of section 2.1.1 gives us _ε_ ∼ _N_ (0 _, σ_[2] ). Therefore, regarding random variable _Yi_ , which generates the _i_ th observation of model (2.2), we write 

**==> picture [194 x 13] intentionally omitted <==**

and the corresponding log-likelihood function is 

**==> picture [166 x 23] intentionally omitted <==**

where _D_ ( _β_ ) = ∥ _y_ − _f_ ( _x_ ; _β_ )∥[2] is defined as in (2.3). This means that the maximization of likelihood with respect to _β_ corresponds to the minimization of _D_ ( _β_ ), and therefore the estimates of maximum likelihood coincide with those of least squares. To estimate _σ_[2] , the maximum likelihood estimate, 

**==> picture [60 x 14] intentionally omitted <==**

is similar to _s_[2] of (2.11); the difference in the denominator tends to be relatively negligible as _n_ gradually increases. It also follows that 

**==> picture [166 x 14] intentionally omitted <==**

The new estimates are thus effectively the same as the least square ones, but the new formulation means that we have access to all the inferential apparatus mentioned in section 2.3.1. 

The principal type of regression model is linear, which may be expressed as (2.6). In this framework, one common practical problem is testing the significance of regression parameters _β_ ; in particular, hypotheses of the type _H_ 0 : _βr_ = 0 are commonly involved. In this case, the distribution of test function (2.31) can be calculated exactly, by Student’s _t_ distribution, like the _p_ -value in the tables of section 2.1. The approximation error caused by avoiding the exact calculation of the _p_ -value is not important for sample sizes larger than a few dozen. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

38 

If the _q_ constraints (2.32) are expressed by linear relations on parameters, quantity (2.33) takes the form: 

**==> picture [253 x 26] intentionally omitted <==**

where ˆ _y_ 0 is the vector of interpolated values under the _q_ constraints. Each of the terms 

**==> picture [251 x 14] intentionally omitted <==**

in (2.34) represent a deviance, respectively, of the unconstrained model and that with _q_ constraints. 

The approximated distribution of reference for _w_ is _χq_[2] , according to the general results of section 2.3.1. In the specific case of Gaussian error terms, we can also obtain the exact distribution, which is usually expressed in terms of the transformation 

**==> picture [227 x 28] intentionally omitted <==**

which, as null distribution, is Snedecor’s _F_ with ( _q, n_ − _p_ ) degrees of freedom, if _p_ is the number of parameters in the nonconstrained model. Also in this case, the approximation error due to the asymptotic distribution for calculating the _p_ -value is not important for sample sizes exceeding a few dozen. 

## 2.3.3 Binary Variables with Binomial Distribution 

In the case of binary response variables, let us denote one possible outcome as “success” and the other as “failure.” When _π_ denotes the probability of success in a single observation, the probability distribution of the total number of successes _Y_ out of _n_ independent observations in constant conditions is given by the binomial distribution of index _n_ and probability parameter _π_ . If _y_ denotes the observed value of _Y_ , the corresponding log-likelihood function is 

**==> picture [314 x 12] intentionally omitted <==**

The estimate of maximum likelihood and its standard error are, respectively, 

**==> picture [184 x 14] intentionally omitted <==**

and the corresponding maximum of the log-likelihood function is 

**==> picture [226 x 12] intentionally omitted <==**

where we mean that 0 log 0 = 0, for continuity. 

A–B–C 

39 

One frequent practical problem arises when we wish to examine a population stratified into two groups, say, 1 and 2, and denote the probability of success in a single observation from each group by _π_ 1 and _π_ 2, respectively. In this case, the log-likelihood function depends on two parameters and is 

**==> picture [269 x 30] intentionally omitted <==**

where _y_ 1 and _y_ 2 denote the number of successes and _n_ 1 and _n_ 2 the sizes of two samples from the subpopulations. 

In the previous notation, the test hypothesis was _H_ 0 : _π_ 1 − _π_ 2 = 0, and the null hypothesis thus imposes _q_ = 1 constraints of type (2.32) on the parameters. The likelihood ratio test statistic is therefore 

**==> picture [154 x 12] intentionally omitted <==**

ˆ ˆ where _πj_ = _yj/nj_ , for _j_ = 1 _,_ 2, and _π_ = ( _y_ 1 + _y_ 2) _/_ ( _n_ 1 + _n_ 2) is the estimate of common values of _π_ . Observed value _w_ is compared with approximate reference distribution _χ_ 1[2][.] 

By analogy with the framework of section 2.3.2, quantity _w_ is also described as _deviance_ , because here too it expresses the discrepancy between the formulated hypothesis and the general case and is usually indicated by the same symbol, _D_ , of (2.10). We bear in mind here the fact that there is no parameter of scale _σ_[2] . The same applies to the likelihood test: the concept of deviance has a much more general value than in the given example, because it may also refer to cases with _J_ groups and the formulated hypothesis may not be that of equality of _π_ for all groups, but corresponds to _q_ constraints. Under this assumption _π_ is estimated by ˆ _π_ =[�] _yj/_[�] _nj_ . Some simple manipulations yield 

**==> picture [264 x 32] intentionally omitted <==**

where 

**==> picture [321 x 48] intentionally omitted <==**

ˆ ˆ and _D_ 0 is similarly obtained when all _πj_ = _π_ . Obviously, if the number of subgroups of which we want to test the equality of probability of success is _q_ + 1, and correspondingly the number of constraints imposed on _π_ is _q_ , the number of degrees of freedom changes, and the approximate reference distribution is _χq_[2] . 

For a numerical illustration, we consider the data of the Brazilian bank (described in Appendix B.3) and split the degree of satisfaction into two levels, high and low, stratified into two subpopulations of old people and young 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

40 

people, according to age (over and under 45). The observed frequencies are shown below. 

|satisfaction<br>low<br>high<br>total|young<br>old<br>total|
|---|---|
||84<br>34<br>118<br>225<br>157<br>382|
||309<br>191<br>500|



ˆ This gives us the estimates of the probability of high satisfaction, _π_ 1 = ˆ 225 _/_ 309 = 0 _._ 728 (SE = 0.025) for the young group, and _π_ 2 = 157 _/_ 191 = 0 _._ 822 (SE = 0.028) for the old group, and the estimate without age stratification is ˆ _π_ = 382 _/_ 500 = 0 _._ 764 (SE = 0.019). The corresponding calculation of the likelihood ratio test, that is, of deviance, gives _D_ = 2 (273 _._ 21 − 270 _._ 25) = 5 _._ 96, _p_ -value 0.015, indicating the influence of age class on the degree of satisfaction. 

## _Bibliographic notes_ 

For a general treatment of statistical inference, at various levels, see Cox & Hinkley (1979), Casella & Berger (2002), or Wasserman (2004). For treatment of likelihood-based inference, see Azzalini (1996). 

## 2.4 LOGISTIC REGRESSION AND GLM 

In the previous numerical example, we concluded that the young customers of the bank are significantly less satisfied than the older ones. Because the variable age can be used in numerical form, it seems preferable to use it in a nondichotomized way. To do this, we need a tool that allows us to study the relation between a quantitative variable and a dichotomous one, like satisfaction. 

This situation is still a study of the relation between variables, but in this case the dichotomous nature of the response variable advises against the use of linear regression. A simple extension of the idea of linear regression to the new problem is logistic regression, which connects probability _π_ of the event of interest to a set _x_ = ( _x_ 1 _, x_ 2 _, . . . , xp_ −1) of explanatory variables in the following form. Response variable _Y_ for any given subject is now a Bernoulli random variable, whose probability of success _π_ ( _x_ ) depends on the covariates. If we indicate by _η_ ( _x_ ) a combination of covariates, linear on the parameters, of the type 

**==> picture [243 x 13] intentionally omitted <==**

similar to those used in § 2.1, and define the _logistic function_ : 

**==> picture [197 x 25] intentionally omitted <==**

the model of logistic regression is given by 

**==> picture [227 x 29] intentionally omitted <==**

A–B–C 

41 

**==> picture [236 x 232] intentionally omitted <==**

**----- Start of picture text -----**<br>
(a=2, b=−2) (a=2, b=3)<br>(a=0, b=1)<br>−3 −2 −1 0 1 2 3<br>x<br>1.0<br>0.8<br>0.6<br>0.4<br>Logistic function<br>0.2<br>0.0<br>**----- End of picture text -----**<br>


Figure 2.11 Logistic function for some choices of pair ( _β_ 0 _, β_ 1) when _η_ ( _x_ ) = _β_ 0 + _β_ 1 _x_ . 

where we note that the probability of the event of interest depends on _x_ , through _linear predictor η_ ( _x_ ) = _x_[⊤] _β_ . 

Figure 2.11 shows some examples of the behavior obtainable in this way when we have only one explanatory variable and _η_ ( _x_ ) = _β_ 0 + _β_ 1 _x_ , for some choices of pair ( _β_ 0 _, β_ 1). The specific pair (0, 1) corresponds to _ℓ_ ( _x_ ) defined by (2.40). 

The scheme of logistic regression is one of the family of _generalized linear models_ (GLM) in which the relationship between the explanatory variables and the response variable may be expressed as 

**==> picture [251 x 27] intentionally omitted <==**

for an appropriate choice of _link function g_ (·). The notation E� _Y_ | _x_ 1 _, . . . , xp_ −1� used here indicates that the values of variables _xj_ are predetermined or that we operate conditionally on the assumed values of the variables. 

For this family of models, the probability distribution of _Y_ conditional on covariates _x_ 1 _, . . . , xp_ −1 must belong to a specific set of distributions. Although, mathematically speaking, this set is quite narrow, in practical terms it covers all the commonly employed families of distributions—Gaussian, gamma, binomial, Poisson, inverse Gaussian, and negative binomial. For this form, there is a clearly structured inference theory based on likelihood and deviance that, in this framework, plays an important role. 

In general, we cannot express the maximum likelihood estimate of a GLM explicitly as a function of the observed data, and we must therefore use an iterative 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

42 

**==> picture [328 x 158] intentionally omitted <==**

**----- Start of picture text -----**<br>
Linear model Linear model<br>Quadratic model Quadratic model<br>20 30 40 50 60 70 20 30 40 50 60 70<br>Age Age<br>1.0 1.0<br>0.8 0.8<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>Pr{ satisfied customers | age } Pr{ satisfied customers | age }<br>0.0 0.0<br>**----- End of picture text -----**<br>


Figure 2.12 Bank data: frequencies of satisfied customers according to age and estimated curves of logistic regression. Left: circles have same diameter; right: circles have areas proportional to size of group. 

numerical procedure. However, there is a very efficient and reliable iterative algorithm to obtain the estimates, through an appropriate sequence of estimates called _iterated weighted least squares_ . 

· The case of logistic regression obtains when _g_ ( ) in (2.42) is 

**==> picture [226 x 21] intentionally omitted <==**

that is, the inverse function of (2.40), and _Y_ has Bernoulli distribution of parameter _π_ , which is a function of the explanatory variables, that is, _π_ ( _x_ ) = _ℓ_ ( _η_ ( _x_ )). In the previous example, in which the response variable was dichotomous, the index of the binomial distribution was 1, but extension to the case of _m_ observations made at value _x_ is immediate, and therefore _Y_ is a binomial with index _m_ and parameter _π_ ( _x_ ). It is common to use the quantity 

**==> picture [63 x 21] intentionally omitted <==**

with inverse function 

**==> picture [66 x 24] intentionally omitted <==**

If we examine the Brazilian bank data in greater detail, without aggregating the age values, the picture emerging from section 2.3.3 changes considerably. Figure 2.12 shows the fitted curve of the relative frequencies of satisfied customers according to age; the two panels are equal, except for the different way of representing the observed values. Figure 2.12 shows that customers’ behavior does vary appreciably with age, in the sense that younger customers behave more like older ones than customers in the intermediate age classes. 

A–B–C 

43 

_Table 2.5._ BANK DATA: SUMMARY OF LOGISTIC REGRESSION MODEL, QUADRATIC (UPPER) AND LINEAR (LOWER) 

||MODEL WITH QUADRATIC COMPONENT|MODEL WITH QUADRATIC COMPONENT|MODEL WITH QUADRATIC COMPONENT||
|---|---|---|---|---|
||Estimate|SE|_t_-value|_p_-value|
|(intercept)|2_._0356|1.2734|1_._60|0.110|
|age|−0_._0700|0.0602|−1_._16|0.245|
|age2|0_._0011|0.0007|1_._56|0.120|
|_D_=0.795 with 3 d.f.|||||
||MODEL WITHOUT|QUADRATIC|COMPONENT||
||Estimate|SE|_t_-value|_p_-value|
|(intercept)|0_._1490|0.3829|0_._39|0.697|
|age|0_._0230|0.0084|2_._73|0.006|



_D_ = 3.302 with 4 d.f. 

We can now apply this method to study of the relationship between the probability of high satisfaction and the age of the bank’s customers. The latter variable is available in the form of a central value of the respective age class, which we now indicate by _x_ , of which possible values are (20, 25, 35, 45, 55, 65). The points in figure 2.12 represent the observed relative frequencies at the values of _x_ , and the dotted curve is obtained by adapting model (2.40) as follows: 

**==> picture [107 x 13] intentionally omitted <==**

where selection is based on preliminary inspection of the data. Note that for the class of the youngest customers, the trend is opposite that of intermediate classes. Table 2.5 lists the estimate operations, which also show that the quadratic component has a Wald test _p_ -value of 0.12, which is not significant. 

We can also evaluate the importance of component _β_ 2 by comparing the two deviances of the model with and without a quadratic component. The difference between them is _D_ = _D_ 1 − _D_ 2 = 3.302 − 0.795 = 2.507, a value that is exceeded with a probability of 0.11 by variable _χ_ 1[2][,][where][the][degrees][of][freedom][are] calculated by the difference 4 − 3 between the degrees of freedom of the two ingredients. This value is not perfectly identical, but is basically equivalent, to that obtained by the Wald test. 

Removing the quadratic component yields a model the relevant values of which are shown in the lower part of table 2.5, and the estimated curve is that which is continuous in figure 2.12. 

It is initially surprising that the quadratic component is not necessary for a proper description of the relationship, in view of the very high frequency of the younger group. In fact, this deceptive impression comes from the type of graphical representation used, which does not consider group size. The right panel of figure 2.12 uses a more appropriate representation, in that the areas of the points are proportional to the size of the various groups, providing a visual impression that 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

44 

includes information. The choice of the model without a quadratic component no longer seems surprising, as the first group is of negligible size. 

## _Bibliographic notes_ 

A classical reference for these models is given in McCullagh & Nelder (1989). The work of Azzalini (1996) includes a shorter treatment of generalized linear models. Specific coverage of logistic regression, with particular attention to applicative aspects, is given by Hosmer & Lemeshow (1989). 

## EXERCISES 

- 2.1 In model (2.14), applied to car data, remove the cubic term and estimate the new model. Observe that the quadratic term becomes significant. Explain this result. 

- 2.2 Use the estimate of linear model (2.14) and extrapolate predicted values for gasoline cars with engine size in the interval (1 _,_ 7). Comment on the results. 

- 2.3 For model (2.17), value _R_[2] ranges from 0.64 to 0.56 when calculated from the original data instead of the transformed data, falling below value 0.60 of the model (2.14). Explain and comment on these differences. 

- 2.4 Extend model (2.17), inserting variables curb weight and _ID_ , and compare the result of the fit of the new model with that of (2.19). 

- 2.5 For model (2.18), reproduce the two graphs of figure 2.8. 

- 2.6 For model (2.18), give a critical analysis of the elements in table 2.3 and associated graphs along the lines of the discussion at the end of section 2.1.1. 

- 2.7 Fit an appropriate linear model to predict highway distance for car data, in two ways: (a) using the variables described in this chapter; (b) using any variables listed in Appendix B.2. 

- 2.8 Complete the details of the statements at the end of section 2.2.2 by calculating _s_[2] and standard errors, using (2.10) or any other method. 

- 2.9 Check the correctness of the Sherman-Morrison formula (A.2). 

- 2.10 Check the correctness of the formulas provided by recursive updating of the least squares estimates. 

- 2.11 Prove (2.24). 

- 2.12 What is the difference between the confidence interval of the value of the function and the prediction interval, both relative to the next observation? 

- 2.13 The curves of figure 2.11 are all monotone, whereas one of those in figure 2.12 is not. Explain this discrepancy. 

3 

Optimism, Conflicts, and Trade-offs 

Pluralitas non est ponenda sine necessitate. 

—WILLIAM OF OCKHAM 

## 3.1 MATCHING THE CONCEPTUAL FRAME AND REAL LIFE 

A solidly based and rich theory of statistical inference, of which we have only mentioned a few key components, underlies the methods described in chapter 2. This theory is characterized by a number of properties that hold only if the model is chosen according to a conceptual foundation that must preexist the availability of the data, and the model itself is appropriate, at least for the purposes of the analysis in question. The related inferential paradigm was developed within a specific research context, with important connections with the foregoing experimental and scientific settings. 

However, certain applied problems, which are often encountered, do not fit this scheme very well. A particularly common critical point is the absence of an adequate background theory, which prevents us from formulating a reliable model before inspecting the data. Preliminary exploration of the data is therefore often required to identify the most suitable model; this approach is even adopted as a general course of action. Chapter 2 describes some examples. 

In our areas of application, the inferential paradigm must be adapted to some extent, because no proper sampling design exists. 

46 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

Similar to the procedure described in chapter 2—that is, exploratory inspection of the data to choose the most suitable models—we consider diagnostic methods to at least partially verify the appropriateness of the choice of model. These diagnostics cover one aspect of the problem, but the issue of assessing the validity of a model is much broader. We explore this topic in the next sections. 

## 3.2 A SIMPLE PROTOTYPE PROBLEM 

We consider here a very simple example serving as the prototype for much more complex and realistic circumstances. Let us presume that yesterday we observed _n_ = 30 pairs of data ( _xi, yi_ ), for _i_ = 1 _, . . . , n_ , shown in the scatterplot of figure 3.1. The data were generated artificially by an equation such as 

**==> picture [193 x 12] intentionally omitted <==**

where _ε_ is an error component with distribution _N_ (0 _, σ_[2] ) and _σ_ = 10[−][2] ; _f_ ( _x_ ) is a function which we leave unspecified—the only requirement is that this function should follow an essentially regular trend. Clearly, to generate the data, we had to choose a specific function (not a polynomial), but we do not disclose our choice. 

Say we wish to obtain an estimate of _f_ ( _x_ ) today that allows us to predict _y_ as new observations of _x_ become available. A reasonable choice consists of using the techniques mentioned in chapter 2, particularly the polynomial regression in (2.4). 

If we have no information to guide us in choosing the degree of the polynomial, we first consider all possible degrees from 0 to _n_ − 1, thereby introducing _p_ 

**==> picture [257 x 254] intentionally omitted <==**

**----- Start of picture text -----**<br>
0.5 1.0 1.5 2.0 2.5 3.0<br>x<br>0.54<br>0.52<br>0.50<br>y<br>0.48<br>0.46<br>0.44<br>**----- End of picture text -----**<br>


Figure 3.1 Yesterday’s data: scatterplot. 

Optimism, Conflicts, and Trade-offs 

47 

parameters ranging from 1 to _n_ , in addition to _σ_ . For brevity, figure 3.2 only shows the fitted curves for only some values of _p_ . Obviously, the polynomial fit improves as _p_ increases, as shown in figure 3.3, in which the residual deviance (2.10) and coefficient of determination _R_[2] (2.15) are plotted as functions of _p_ . 

A special case exists when _p_ = _n_ , corresponding to a polynomial that exactly interpolates the observed data, with residual deviance 0 and _R_[2] = 1. Such a case is apparently ideal, but it corresponds to the unacceptable situation shown in the last plot of figure 3.2. The nearly vertical lines are simply the visualized portions of the very large fluctuations the 29-degree polynomial must follow to interpolate all the observed points exactly. 

As already mentioned, we need to use an estimate of _f_ ( _x_ ) to predict values of _y_ for new data { _yi, i_ = 1 _, . . . , n_ } produced by the same generating mechanism, but these will become available tomorrow. To simplify the process, we assume that these _yi_ are associated with the same _xi_ used for yesterday’s data. We now evaluate the quality of the prediction using yesterday’s fit of the polynomials for the new _yi_ , as if we could obtain tomorrow’s data today. Figure 3.4 shows tomorrow’s data with the predictions from the previously fitted polynomials. It is noteworthy that the higher-degree polynomials fluctuate and no longer fit the new points, whereas for smaller values of _p_ , an increase in the degree of the polynomial improves the fit of the general trend. This improvement gradually ceases as the increase in degree causes the polynomial to follow random fluctuations in yesterday’s data, not observed in the new sample. Figure 3.5 summarizes and quantifies this information by showing that the residual deviance decreases to a certain point and then increases, whereas index _R_[2] peaks and then falls. 

The concepts of deviance and _R_[2] are used here in a way that extends beyond their common definitions, since the sum of the squares of the quantities involved are computed by using data other than those used for the fit. 

## 3.3 IF WE KNEW _f_ ( _x_ ) _. . ._ 

In a general sense, when we formalize the observations of section 3.2, we can say ˆ that we want to estimate _f_ ( _x_ ) using a generic estimator _y_ = _f_[ˆ] ( _x_ ), which, in our example, can be provided by one of the 30 fitted polynomials. 

We start by considering a specific value _x_[′] for _x_ . If we knew the mechanism used to generate the data precisely, that is, _f_ ( _x_[′] ), we could calculate a few quantities of interest for the quality of estimator ˆ _y_ . An important goodness-of-fit index is given by the _mean squared error_ 

**==> picture [270 x 28] intentionally omitted <==**

where _Y_[ˆ] denotes the parent random variable of ˆ _y_ . When _f_ (·) is a polynomial with fixed degree _p_ , (3.2) can be explicitly obtained; see exercise 3.2. 

Because we are interested in more than one single point _x_[′] , we consider the sum of the mean squared errors for all the _n_ values of _x_ . Representing the resulting value as a function of _p_ , which is an indicator of _model complexity_ , we obtain the 

**==> picture [328 x 499] intentionally omitted <==**

**----- Start of picture text -----**<br>
Data and 3rd-degree polynomial Data and 6th-degree polynomial<br>0.5 1.0 1.5 2.0 2.5 3.0 0.5 1.0 1.5 2.0 2.5 3.0<br>Data and 12th-degree polynomial Data and 18th-degree polynomial<br>0.5 1.0 1.5 2.0 2.5 3.0 0.5 1.0 1.5 2.0 2.5 3.0<br>Data and 24th-degree polynomial Data and (n−1)th-degree polynomial<br>0.5 1.0 1.5 2.0 2.5 3.0 0.5 1.0 1.5 2.0 2.5 3.0<br>x x<br>0.54 0.54<br>0.52 0.52<br>0.50 0.50<br>y y<br>0.48 0.48<br>0.46 0.46<br>0.44 0.44<br>0.54 0.54<br>0.52 0.52<br>0.50 0.50<br>y y<br>0.48 0.48<br>0.46 0.46<br>0.44 0.44<br>0.54 0.54<br>0.52 0.52<br>0.50 0.50<br>y y<br>0.48 0.48<br>0.46 0.46<br>0.44 0.44<br>**----- End of picture text -----**<br>


Figure 3.2 Yesterday’s data: interpolations with polynomials of various degrees. 

Optimism, Conflicts, and Trade-offs 

49 

**==> picture [330 x 158] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 5 10 15 20 25 30 0 5 10 15 20 25 30<br>p p<br>1.0<br>0.015<br>0.8<br>0.6<br>0.010 2<br>R<br>Deviance 0.4<br>0.005<br>0.2<br>0.0<br>0.000<br>**----- End of picture text -----**<br>


Figure 3.3 Yesterday’s data: deviance and _R_[2] coefficient when _p_ varies. 

plot shown in figure 3.6. Note that when _p_ increases, the mean squared error first decreasesandthenincreases,thusprovidingthelevelof‘complexity’corresponding to a minimum mean squared error—in this case, for _p_ = 5. 

In the foregoing treatment, we used the family of polynomials as a set of models in which complexity was controlled by a certain parameter _p_ , which was precisely the polynomial degree. Polynomials are not the only possible choice; the Fourier series is another that comes to mind. In any case, the final message remains unaltered, even when the family of models chosen is changed. When complexity increases, there is usually an initial gain followed by a loss. 

When we further consider (3.2), the components of which are such that 

**==> picture [243 x 15] intentionally omitted <==**

we see that this decomposition applies not only in the case of polynomial regression, but also in general. Figure 3.7 shows how these two components contribute to the mean squared error for this example. When model complexity, quantified by _p_ , is low, bias is high and variance is moderate; when _p_ increases, bias decreases but variance increases. As mentioned in section 3.2, when _p_ increases, the polynomials fit the data better, but when _p_ becomes too large, they follow random fluctuations in the data. In this case, variance increases without any important gain in bias. In these situations, the model _overfits_ the data and involves an excess of _optimism_ in evaluating the prediction error. 

This behavior is found in much more general situations involving models with increasing complexity. Bias and variance are conflicting entities, and we cannot minimize both simultaneously. We must therefore choose a _trade-off between bias and variance_ . This situation guides the developments that follow. 

A bias component is essentially due to lack of knowledge of the data-generating mechanism. If this mechanism were known, we could set up an appropriate parametric model, such as a polynomial of specified degree, and the bias would be null or at most negligible. This is typical of parametric models when they are 

**==> picture [329 x 496] intentionally omitted <==**

**----- Start of picture text -----**<br>
Data and 3rd-degree polynomial Data and 6th-degree polynomial<br>0.5 1.0 1.5 2.0 2.5 3.0 0.5 1.0 1.5 2.0 2.5 3.0<br>Data and 12th-degree polynomial Data and 18th-degree polynomial<br>0.5 1.0 1.5 2.0 2.5 3.0 0.5 1.0 1.5 2.0 2.5 3.0<br>Data and 24th-degree polynomial Data and (n−1)th-degree polynomial<br>0.5 1.0 1.5 2.0 2.5 3.0 0.5 1.0 1.5 2.0 2.5 3.0<br>x x<br>0.54 0.54<br>0.52 0.52<br>0.50 0.50<br>y.test y.test<br>0.48 0.48<br>0.46 0.46<br>0.44 0.44<br>0.54 0.54<br>0.52 0.52<br>0.50 0.50<br>y.test y.test<br>0.48 0.48<br>0.46 0.46<br>0.44 0.44<br>0.54 0.54<br>0.52 0.52<br>0.50 0.50<br>y.test y.test<br>0.48 0.48<br>0.46 0.46<br>0.44 0.44<br>**----- End of picture text -----**<br>


Figure 3.4 Tomorrow’s data: interpolation with polynomials obtained by fitting yesterday’s data. 

Optimism, Conflicts, and Trade-offs 

51 

**==> picture [328 x 156] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 5 10 15 20 25 30 0 5 10 15 20 25 30<br>p p<br>1.0<br>0.015<br>0.8<br>0.6<br>0.010 2<br>R<br>Deviance 0.4<br>0.005<br>0.2<br>0.0<br>0.000<br>**----- End of picture text -----**<br>


Figure 3.5 Tomorrow’s data: deviance and _R_[2] coefficient as a function of _p_ . 

**==> picture [258 x 255] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 5 10 15 20 25 30<br>Model complexity<br>4e−04<br>3e−04<br>Error<br>2e−04<br>1e−04<br>0e+00<br>**----- End of picture text -----**<br>


Figure 3.6 Yesterday’s data: mean squared error as a function of _p_ . 

correctly specified. Instead, the context in which we are working obliges us to use an essentially _nonparametric approach_ , although we used parametric tools (polynomials) as building materials for the sake of simplicity. 

## 3.4 BUT AS WE DO NOT KNOW _f_ ( _x_ ) _. . ._ 

We just concluded that we must expect a trade-off between error and variance components. In practice, however, we cannot do this because, of course, _f_ ( _x_ ) is unknown. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

52 

**==> picture [257 x 254] intentionally omitted <==**

**----- Start of picture text -----**<br>
Bias [2]<br>Variance<br>Total<br>0 5 10 15 20 25 30<br>Model complexity<br>4e−04<br>3e−04<br>Error<br>2e−04<br>1e−04<br>0e+00<br>**----- End of picture text -----**<br>


Figure 3.7 Yesterday’s data: mean squared error as a function of _p_ , decomposed into bias and variance. 

We have seen that overfitting is a trap that must be avoided. Overfitting occurs when a model closely fits some nonessential features of the observed sample. If these characteristics are not structural to the phenomenon under study, they will not recur in a new sample. As this problem originates because we calculate deviance with the same data with which we fitted the model, one way of avoiding this trap is to evaluate the model with other data. 

In our example, the models fitted to “yesterday’s” data can be compared with those of “tomorrow,” yielding the plot of figure 3.8, which shows the residual deviance for various polynomials fitted to yesterday’s data. Clearly, the deviance calculated for tomorrow’s data provides a reasonable indication of the complexity of the model, essentially analogous to that given in figure 3.6; equally clearly, the two figures do not have the same nature: one is an approximation of the other, and the curve obtained with tomorrow’s data is also affected by the variability of the new data. Nevertheless, the indication provided by the deviance of tomorrow’s data does not suffer from the drawback we wished to avoid, and its message is essentially valid, with a minimum point at _p_ = 4. 

## 3.5 METHODS FOR MODEL SELECTION 

We must confess here that we cheated. We do not in fact have two sets of data, one for yesterday and one for tomorrow. We have 60 observations, randomly divided into two groups of 30 observations each, but we acted as we did to illustrate 

Optimism, Conflicts, and Trade-offs 

53 

**==> picture [254 x 250] intentionally omitted <==**

**----- Start of picture text -----**<br>
Tomorrow data<br>Yesterday data<br>0 5 10 15 20 25 30<br>Model complexity<br>0.015<br>0.010<br>Deviance<br>0.005<br>0.000<br>**----- End of picture text -----**<br>


Figure 3.8 Yesterday’s and tomorrow’s data: residual deviance as a function of degree _p_ of polynomials fitted to yesterday’s data. 

the problem. We now consider the principal tools used in model selection by identifying the trade-off between bias and variance. 

## 3.5.1 Training Sets and Test Sets 

Dividing the data into two groups circumvents the overfitting problem and allows us to reach a plausible solution for choosing _p_ . 

This approach is not our invention but is a common procedure in this kind of context. A randomly selected portion of data, called _training set_ , is used to fit the various candidate models. The remaining portion, the _test set_ , is used to evaluate the performance of the available models and choose the most accurate one. 

Clearly, this scheme reduces the sample size used for fitting the model, which may be inadvisable when sample sizes are already small. Having too few data is not a concern in the context of data mining; having too many might be the problem. Instead, in the current context, it is more important to neutralize or at least diminish any estimation bias, as already noted. 

Because the same test set can be used to evaluate many different models, there is a risk that the final assessment, obtained at the end of the entire process, is still somewhat biased and too optimistic, because of the same mechanism that acts when we use the training set. For this reason, and because the data are abundant, a third set, called the _validation set_ , is often created for use at the end of analysis for final evaluation of the prediction error. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

54 

There is no precise rule on how to select the size of these sets, but the table that follows gives some commonly used reference values for proportions with two or three subsets. 

|Portion of data for:|training|test|validation|
|---|---|---|---|
||50%|25%|25%|
||75%|25%|0|
||67%|33%|0|



## 3.5.2 Cross-validation 

Recall the procedure described in section 3.5.1 and presume that we use 75% of the data for training and 25% for testing the models. However, for greater accuracy, we do not want to assign only _that_ specific 25% of the data to the role of test set. In addition, if _n_ is not very large and we only use 75% of the data to fit the model, the estimate will be further impoverished, whereas we would like to take better advantage of available information. 

One way of partially overcoming this arbitrariness is to split the data into four equal parts and use three portions _in rotation_ for training the model and the remaining portion for testing it. We then _cross_ the role of the data sets: one of the portions used as the training set is now used as a test set, and the test set is incorporated into the training set with the other two portions. Obviously, this scheme requires four iterations of the training and testing procedures. 

Because this scheme results in four different estimates, which probably do not differ by much, an average or some other combination of them can be used. Analogously, we have four different figures similar to figure 3.8, and use these to obtain an “average curve,” from which we can determine the minimum point. 

It is intuitive that the procedure becomes progressively more accurate if, instead of 4 parts sized _n/_ 4, we use _k_ portions of size _n/k_ and repeat the operations _k_ times. This is more effective when large values of _k_ are used. 

The maximum possible value for _k_ is _n_ . To fit the model, _n_ − 1 observations are used, and the remaining observation is used for testing. This procedure is known as _leave-one-out_ cross-validation and is described in detail in algorithm 3.1. Once we have rotated the only datum serving as test set, we must perform a total of _n_ fitting operations. Clearly, the computational burden of this procedure increases considerably as _n_ increases. 

Fortunately, in many cases, it is possible to obtain estimates of a model using data deprived of a single observation, by means of simple operations based on estimates obtained from the complete data set. In particular, in the case of a linear model such as (2.6), in which the fitted values are given by (2.8), the following relationship holds 

**==> picture [231 x 12] intentionally omitted <==**

so that we can obtain interpolated value ˆ _y_ − _i_ for the _i_ th observation without using theobservationitself,butonlyusingvalue(orvalues) _xi_ .Here, _Pii_ isthe _i_ thdiagonal element of projection matrix (2.9). In this way, we obtain all the interpolated 

Optimism, Conflicts, and Trade-offs 

55 

**Algorithm 3.1** Cross-validation ( _leave-one-out_ ) 

1. Read _n_ records of _x_ and _y_ . 

2. Cycle for _p_ = 0 _,_ 1 _, . . . ,_ max _p_ : 

a. cycle for _i_ = 1 _, . . . , n_ : 

- i. fit the model of degree _p_ by eliminating the _i_ th observation, 

- ii. obtain prediction ˆ _y_ − _i_ for _yi_ corresponding to point _xi_ , 

- iii. obtain residual _ei_ ← ( _yi_ −ˆ _y_ − _i_ ), 

**==> picture [122 x 31] intentionally omitted <==**

3. Choose _p_ so that _D_[∗] ( _p_ ) is minimum. 

values for the _n_ possible subsets of training data by a simple modification of interpolated value ˆ _yi_ and using matrix _P_ , which needs to be calculated in any case. 

Algorithm 3.1 for the 60 observations considered so far and the simplified formula (3.4) produces figure 3.9, which indicates _p_ = 4 is the preferred value. 

We introduced the cross-validation criterion on a purely intuitive basis. There are theoretical results guaranteeing that when _n_ diverges, this procedure certainly leads us to select the most appropriate model. However, we should add that for small sample sizes, this method often gives a very variable choice for _p_ . 

## 3.5.3 Criteria Based on Information 

The main statistical method applied for estimating the unknown parameters of a model is to maximize the log-likelihood. However, when the model itself is not fixed in advance and is chosen from a sometimes large set of alternative models, we cannot simply proceed by maximizing the likelihood function for each alternative model; we must also take into account the different number of parameters, introducing a suitable penalty. Criteria that follow this logic can be traced back to objective functions such as 

**==> picture [234 x 14] intentionally omitted <==**

where penalty( _p_ ) quantifies the penalty assigned to a model incorporating _p_ parameters. 

The choice of the specific penalty function identifies a particular criterion. Clearly, this function must be positive and must increase with _p_ . A more specific indication is supplied by the following considerations. When we compare two nested models by test function (2.33) when the restricted model has one parameter 

56 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

**==> picture [253 x 257] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 5 10 15 20 25 30<br>Model complexity<br>0.035<br>0.030<br>0.025<br>Error 0.020<br>0.015<br>0.010<br>0.005<br>**----- End of picture text -----**<br>


Figure 3.9 Yesterday’s and tomorrow’s data: cross-validation model selection. 

less than does the other—that is, the nested model specifies one variance on the _p_ + 1 parameters of the larger model—we know that asymptotically 

**==> picture [120 x 15] intentionally omitted <==**

when the ( _p_ + 1)th parameter is actually redundant. Here, we denote the maximum achieved by the likelihood of the two compared models as _Lp_ +1 and _Lp_ . Thus, the insertion of an unnecessary parameter leads the mean of −2 log _L_ to decrease by one unit, so that the penalty for _p_ parameters must be strictly greater than _p_ . 

This approach to model selection was introduced by Akaike (1973), who proposed the now famous Akaike information criterion (AIC). Akaike suggested minimizing the _Kullback-Leibler divergence_ : 

**==> picture [330 x 27] intentionally omitted <==**

between true distribution _p_ ∗( _y_ ) and fitted model _p_ ( _y_ ; _θ_ ). This quantity may be interpreted as a measure of the divergence between the distribution of future data generated by random variable _Y_ and that predicted by the model. It is clear that to minimize _KL_ , we can only act on the second term of the last expression and must therefore consider a value that maximizes log _p_ ( _Y_ ; _θ_ ), that is, the maximum likelihood estimate. As this estimate _θ_[ˆ] _y_ is a function of past observations, say, _y_ , 

Optimism, Conflicts, and Trade-offs 

57 

and as we want to use _p_ (·; _θ_[ˆ] _y_ ) to predict the behavior of the model on future data generated from random variable _Y_ , we also need to take into account the variability connected with the estimating procedure. This leads us to consider the quantity 

**==> picture [102 x 21] intentionally omitted <==**

Calculation of this expression requires some assumptions, as well as analytic approximations. According to Akaike’s initial formulation, after appropriate analytical developments, we obtain 

**==> picture [85 x 14] intentionally omitted <==**

as an estimate of the quantity of interest E _p_ ∗�log _p_ ( _Y_ ; _θ_ )�, multiplied by the conventional factor −2, which is inserted by alignment with the consolidated notations related to likelihood, in particular (2.33). 

Akaike’s original work was followed by several other proposals, differing in their assumptions and the way they approximate certain quantities. Some of them are shown in the table that follows, which provides some alternative penalties to be included in (3.5). 

|Criterion|Author|Penalty(_p_)|
|---|---|---|
|AIC|Akaike|2_p_|
|AIC_c_|Sugiura, Hurvich-Tsay|2_p_+ 2_p_ (_p_+1)<br>_n_−(_p_+1)|
|BIC/SIC|Akaike, Schwarz|_p_ log_n_|
|HQ|Hannan-Quinn|_c p_ log log_n,_<br>(_c >_2)|



Note that the difference between AIC and AIC _c_ tends to be negligible when _n_ is large, because AIC _c_ is a corrected AIC for small sample sizes. The last two criteria use a penalty that increases with increasing _n_ and were generated by theoretical considerations quite different from the first two criteria. Although the logical framework of these information-based criteria and the procedures for hypothesis testing is not really the same, in practice they are often employed as if they were competing on the same ground. 

An important advantage of information-based criteria with respect to the likelihood ratio test is that they can also be applied to families of unnested models, provided that the arbitrary constant in likelihood function (2.25) is set at 1. The disadvantage is that any evaluation of the probability of error of the procedure is not available. 

Figure 3.10 illustrates the results obtained with these criteria for the data used so far. In this case, all four criteria suggest the same choice: _p_ = 4. Obviously, there is no need to split the data into two sets, hence we use all 60 observations. 

To conclude this short review of methods for model selection, figure 3.11 plots the fitted curve, which in this case is the same for all methods, with _p_ = 4. This represents the basic trend of the phenomenon in a plausible fashion. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

58 

**==> picture [258 x 254] intentionally omitted <==**

**----- Start of picture text -----**<br>
AIC<br>AIC.c<br>BIC<br>HQ (c=3)<br>0 5 10 15 20 25 30<br>Model complexity<br>−450<br>AIC and BIC criterion −500<br>−550<br>−600<br>**----- End of picture text -----**<br>


Figure 3.10 Yesterday’s and tomorrow’s data: various information criteria as a function of model complexity. 

## _Bibliographical notes_ 

Although the first examples of the use of cross-validation methods are quite old, the introduction and systematic study of this criterion are attributed to Stone (1974). The AIC appeared for the first time in Akaike (1973). An extended discussion of AIC-related criteria is given in Burnham & Anderson (2002). Recent specific coverage of model selection is to be found in Claeskens & Hjort (2008). 

## 3.6 REDUCTION OF DIMENSIONS AND SELECTION OF MOST APPROPRIATE MODEL 

We can now devise automatic procedures for model selection by examining a set of alternative models fitted to a certain data set. Implementation of these procedures is made easier, and for this reason is particularly widespread, when various models are all of the same type, differing only in their set of explanatory variables. Therefore, in practice, these are _variable selection_ procedures. 

## 3.6.1 Automatic Selection of Variables 

For the sake of simplicity, we refer to the problem discussed in section 3.2 and to model (3.1). The set of models competing for _f_ ( _x_ ) consists of a family of polynomial functions. The explanatory variables are the powers of _x_ , so that the generic covariate, say, _xj_ , is such that _xj_ = _x[j]_ , with a degree ranging from 0 to a fixed maximum _q_ (e.g., _q_ = _n_ − 1). In previous sections, we argued on the assumption that when we use a polynomial of a certain degree, all the terms of lower degree are 

Optimism, Conflicts, and Trade-offs 

59 

**==> picture [256 x 252] intentionally omitted <==**

**----- Start of picture text -----**<br>
Training set<br>Test set<br>0.5 1.0 1.5 2.0 2.5 3.0<br>x<br>0.54<br>0.52<br>0.50<br>y<br>0.48<br>0.46<br>0.44<br>**----- End of picture text -----**<br>


Figure 3.11 Yesterday’s and tomorrow’s data: fitted curve with _p_ = 4. 

inserted in the regression curve. However, this requirement is not necessary in the following. 

In a generic regression context, we consider a set of explanatory variables such as 

**==> picture [220 x 13] intentionally omitted <==**

where the inclusion of constant 1 is not a formal need but is in fact almost universally applied. For each choice of a subset of _S_ , it is straightforward to obtain estimates for regression coefficients _β_[ˆ] _j_ , other connected quantities such as deviance, and if we assume Gaussian errors, log-likelihood, and AIC. However, the regression model is not the only one available: GLM linear or other parametric models can also be used, despite the possible greater computational burden. 

An automatic procedure for variable selection aims at identifying the subset of _S_ that minimizes the AIC or a similar criterion. Obviously, this operation requires fitting many models and must be done by computer. Even so, the related computational burden is huge if _q_ is not small and we have to go through all the possible subsets and look for the _optimal subset_ . 

Thus, if _q_ is not small, it is more common to use a simplified procedure known as _stepwise selection_ , or some variant of this name. We begin with a certain model, identified by a certain subset _S_ 0 of _S_ , and then add the member of _S_ not included in _S_ 0. Alternatively, we eliminate the member of _S_ 0, which gives the lower value of 

60 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

AIC of all the operations of this type. We thus obtain a subset, _S_ 1, which contains one element more or one element less than _S_ 0. This operation is repeated, this time starting from _S_ 1, looking for the optimal variation. The result is subset _S_ 2, and the procedure is repeated until we reach a set, _S_ ∗, which cannot be improved by either reduction or enlargement. This is the selected subset. 

When starting, subset _S_ 0 is the minimum size that we want to consider with respect to _S_ , for example, _S_ 0 = {1}, the final outcome will obviously be a subset _S_ ∗ ⊇ _S_ 0, and the procedure is called _forward selection_ . However, when _S_ 0 = _S_ , the final selection will be _S_ ∗ ⊆ _S_ 0 and the procedure is called _backward selection_ . 

The use of these automatic selection techniques is particularly justified when a large number of the explanatory variables is available and detailed analysis of all of them is not feasible. Another reason is the lack of suggestions and guidelines provided by the original applied problem. Both of these conditions often occur in the context of data mining. 

However, it should be noted that these procedures, although they use inferential tools with well-known probabilistic characteristics as functioning ingredients, are out of that context in practice. For example, it is very difficult to establish which properties (in terms of actual precision of standard errors) are associated with the various estimates. This is because they do not refer to a predetermined model with respect to data, which is the basic condition for evaluating standard errors. Obviously, these observations also apply to other situations where the model is selected using the same data, but they are more relevant in cases when multiple individual models are evaluated. 

## _Bibliographical notes_ 

Stepwise regression is described and discussed, for example, in Weisberg (2005, section 10.3), Miller (2002, chapter 3), and Izenman (2008, section 5.7). Chapter 8 of Afifi & Clark (1990) gives a detailed presentation of automatic selection procedures. 

## 3.6.2 Principal Component Analysis 

Another strategy for selecting a model is based on reducing the dimension of the explanatory variables, transforming them in some way into a set of new variables of smaller number, but at the same time trying to lose only information that is not important in predicting the response variable. 

The simplest possibility is to consider linear transformations of explanatory variables that have some sort of optimality property. _Principal component analysis_ (PCA) is probably the most frequently used technique for deriving a reduced set of new variables by linear combination of the original variables that explains most of the variability of those variables. 

We consider matrix _X_ , obtained from the set of explanatory variables in (3.6), as the sampling determination of a multivariate random variable and, for ease of explanation, assume that it has mean 0 and covariance matrix _�_ . If the variables are not centered around 0, it is always possible to calculate deviations from the mean and obtain zero mean variables. The variance of linear combination _Z_ = _Xα_ is 

Optimism, Conflicts, and Trade-offs 

61 

var{ _Z_ } = _α_[⊤] _�α_ . We must find a vector of weights _α_ , so that var{ _Z_ } is the largest among all normalized linear combinations of the columns of _X_ , by imposing a scale restriction on _α_ . This leads to the principal component criterion 

**==> picture [221 x 37] intentionally omitted <==**

Once the first component has been selected, with coefficients _α_ 1, we look for another linear combination, orthogonal to the first one, maximizing the variance 

**==> picture [244 x 38] intentionally omitted <==**

The other components are defined in a similar fashion by requiring orthogonality with all the previous components. 

The mathematical solution of this problem is given by the spectral decomposition of _�_ : var{ _Z_ 1} = var{ _Xα_ 1} = _λ_ 1 is the largest eigenvalue of _�_ and _α_ 1 is the corresponding eigenvector; var{ _Z_ 2} = _λ_ 2 and _α_ 2 correspond to the second-largest eigenvalue and the related eigenvector, and so on. Solution _α_ 1 is called the _first vector of principal loadings_ , combination _Z_ 1 = _Xα_ 1 is the _first principal component_ , and so on for _α_ 2, _Z_ 2, and so on. 

Because _�_ is not usually known, in practice spectral decomposition is obtained on estimate _�_[ˆ] . We denote by _zj_ the observed value of _Zj_ . Principal components have a simple geometrical interpretation, because _Z_ 1 is the projection of the data on the longest observed direction—that is, the direction having the largest variance among all such normalized projections— _Z_ 2 is the projection on the second longest direction orthogonal to the first one, and so on. This is illustrated in figure 3.12 for the two-dimensional case. 

The sum of the eigenvalues is equal to the trace of the covariance matrix, so that the sum of the variances of the components is the same as that of the original variables, and[�] _[k] i_ =1 _[λ][i][/]_[ �] _i[p]_ =[+] 1[1] _[λ][i]_[ is the fraction of total variance explained] by the first _k_ components, and fraction _λi/_[�] _i[p]_ =[+] 1[1] _[λ][i]_[measures][the][importance] of the _i_ th component in explaining total variability. If the percentage of total variance explained by the first _k_ components is large enough, we can eliminate the remaining components and take only the first _k_ to describe variability among explanatory variables, using them as new independent variables of the model. PCA for dimension reduction in prediction problems is often used to solve the problem of multicollinearity among explanatory variables. This technique is also used when there are more independent variables than observations, a typical problem found in some data mining applications such as gene expression problems, where a large number of genes (variables) is typically observed for a small number of samples (observations). 

Despite the considerable merit of this technique (reducing the number of variables used), it suffers from the fact that the new variables are often not as 

62 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

**==> picture [257 x 254] intentionally omitted <==**

**----- Start of picture text -----**<br>
Smallest principal<br>Largest principal component<br>component<br>−4 −2 0 2<br>x1<br>2<br>0<br>2<br>x<br>−2<br>−4<br>**----- End of picture text -----**<br>


Figure 3.12 Principal components for a set of simulated data in two dimensions. Length of each solid segment is proportional to variance _λi_ explained by each component. Dashed segments: perpendicular distances from first component for some observations. 

easy to interpret as the original ones. However, suitable modifications of PCA are often used as tools to identify latent but interpretable data structures. The methods used to find unobservable but interpretable variables, based on principal components or not, are usually grouped under the name of _factor analysis_ . 

A substantial body of literature proposes many other types of combinations of variables. Some of these maintain their linear structure and change the optimization criteria (3.7), (3.8), and so on; of these, _canonical correlation analysis_ maximizes the correlation between two groups of variables, and _independent component analysis_ requires the components to be statistically independent instead of orthogonal. However, the linearity required is a limitation to the procedure, because it does not allow for different combinations and reductions of data. Other methods have been proposed to allow for nonlinear transformations. For example, _principal curves and surfaces_ provide smooth one- and two-dimensional curved approximations to a set of data points. 

## _Bibliographical notes_ 

PCA was introduced by Pearson (1901) and developed by Hotelling (1933). It is now one of the most frequently used techniques in exploratory multivariate analysis. Depending on the field of application, it is also called the discrete Karhunen-Loève transform, the Hotelling transform, or proper orthogonal decomposition. Detailed presentations are discussed in all works on multivariate 

Optimism, Conflicts, and Trade-offs 

63 

analysis, for example, Mardia et al. (1979) or Johnson & Wichern (1998). A standard account of PCA is the work of Jolliffe (2002). Generalizations of PCA, such as independent component analysis (ICA) and principal curves and surfaces, are discussed in many data mining and multivariate analysis works, such as Hastie et al. (2009, sections 14.5 and 14.7) and Izenman (2008, sections 15.3 and 16.3). 

## 3.6.3 Methods of Regularization 

When a large number of covariates is available, least squares estimates of a linear model often have low bias but high variance when compared with models with a smaller number of variables. As we have seen, methods of variable selection and dimension reduction may help improve prediction accuracy by allowing for larger bias but smaller variance. 

These methods may be unattractive for reasons of computational burden (variable selection) or interpretation (dimension reduction), as discussed in the previous sections. A different approach is to modify the estimation method by abandoning the requirement of an unbiased estimator of the parameters, and instead considering the possibility of using a biased estimator, which may have smaller variance. There are several such estimators, most based on regularization: all the variables are left in the model, but when the model is fitted, their 

The idea is to obtain a shrinkage toward the mean, so that usually the intercept is not penalized. We can therefore operate in two steps: first, we obtain the average of _y_ as estimate for the intercept; then we replace each _yi_ with _yi_ −¯ _y_ , and the _xij_ with centered variables _xij_ −¯ _xj_ (for _j_ = 1 _, . . . , p_ − 1). For the rest of this section, without loss of generality, _X_ is the new matrix with _p_ − 1 columns, the first constant column 1 _n_ having been eliminated, and there is no longer any intercept to be estimated. 

_Ridge regression_ is probably the most common shrinkage method. Consider linear model (2.6), _y_ = _Xβ_ + _ε_ , for which ridge regression coefficients minimize a constrained form of (2.3) 

**==> picture [265 x 36] intentionally omitted <==**

An equivalent formulation of this problem can be obtained with the Lagrange form, so that the ridge regression coefficients minimize the penalized residual sum of squares 

**==> picture [323 x 36] intentionally omitted <==**

where _λ_ is uniquely determined by _s_ . The solution is _β_[ˆ] _λ_ = ( _X_[⊤] _X_ + _λI_ )[−][1] _X_[⊤] _y_ , where _I_ is the identity matrix. Estimator _β_[ˆ] _λ_ is biased but for some values of _λ >_ 0 may have a smaller mean squared error than the least squares estimator. 

64 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

Note that _λ_ = 0 gives the least squares estimator and, if _λ_ →∞, then _β_[ˆ] → 0. Ridge regression is particularly useful when explanatory variables are collinear, as even a small _λ >_ 0 makes solution _β_[ˆ] _λ_ numerically and statistically stable. Parameter _λ_ should be adaptively chosen, for example, by cross-validation or the other methods discussed in section 3.5. 

Ridge regression has a simple geometrical interpretation according to PCA, because it projects response variable _y_ on the principal components and then shrinks the coefficients of low-variance components by more than those of highvariance components. It is, in fact, often (although not always) reasonable to expect that the response variable will vary more in the direction of high variance of explanatory variables. Therefore, when compared with principal component transformation of explanatory variables, ridge regression shrinks the coefficients of the principal components, relatively more shrinkage being applied to the smaller components than the larger ones, whereas principal component regression discards the components with smaller eigenvalues (see, for example, Hastie et al., 2009, section 3.4.1). 

The choice of an alternative penalty to be added to the sum of squares (2.3) may provide a shrinkage method that, in addition to parameter restriction, requires some coefficients to be zero. When the quadratic constraint in (3.9) is replaced by absolute value constraint[�] _[p] j_ =[–1] 1[|] _[β][j]_[|][≤] _[s]_[and][a][sufficiently][small] _[s]_[is][chosen,] constrained minimization of the sum of squares sets some coefficients exactly at 0, by performing a kind of continuous model selection. This shrinkage method is called _lasso_ and minimizes 

**==> picture [267 x 35] intentionally omitted <==**

or, in Lagrange form: 

**==> picture [296 x 35] intentionally omitted <==**

The solutions are nonlinear in _y_ and, because of the nature of the constraint, they may be solved by quadratic programming. As for ridge regression, regularization parameter _s_ (or _λ_ ) should also be adaptively chosen, according to the methods discussed in section 3.5. 

When we compare the coefficient estimates obtained by ridge regression and lasso, we observe that if inputs are orthogonal, ridge regression coefficients are obtained from multiplication of least squares coefficients by a constant between 0 and 1, whereas lasso translates them toward 0 by a constant, as shown in figure 3.13 for the simple case when the columns of the _X_ matrix are orthonormal; note that stepwise regression truncates small estimated coefficients at 0. 

The appealing characteristics of lasso are offset by the complicated quadratic programming algorithm required to estimate the coefficients. In recent years, 

Optimism, Conflicts, and Trade-offs 

65 

**==> picture [222 x 215] intentionally omitted <==**

**----- Start of picture text -----**<br>
Lasso<br>Ridge regression<br>Least<br>squares<br>Stepwise regression<br>Least squares coefficient<br>Shrinkage coefficient<br>**----- End of picture text -----**<br>


Figure 3.13 Transformed coefficient with respect with least squares coefficient for ridge regression, lasso, and stepwise regression for orthonormal case. 

several faster algorithms have been proposed, one based on pathwise coordinate descent. The most elegant and efficient algorithm is based on least-angle regression (LAR), a modification of the Gram-Schmidt algorithm to estimate least squares coefficients of model (2.6) by successive orthogonalization; see algorithm 2.1. 

As we saw in section 3.6.1, forward stepwise regression adds one variable at a time to the model by identifying the variable to be included in that model at each step. LAR uses a similar strategy, but adds to the model only that portion of information included in a variable which is needed, as we show in algorithm 3.2. LAR starts by adding to the model the variable most correlated with the response and, rather than fit this variable by least squares, chooses the coefficient by moving its value continuously between 0 and the least squares value. As the estimated coefficient moves between them, the correlation between the variable and the residuals decreases in absolute value. At some point in this evolution of the first coefficient, the correlation between the variable and the residuals becomes equal to the correlation between another variable and the same residuals. This second variable is then included in the model, and its coefficient is chosen together with the first one, by moving them in the direction of their least squares coefficient, until some other variable has as much correlation with the current residuals. The process continues until all the variables are included in the model and we obtain the least squares coefficients. 

The LAR algorithm is of comparable computational complexity to the least squares fit, which can be computed in _p_[3] + _np_[2] operations. 

The interesting aspect of LAR is its simple relationship with lasso: a modification of the algorithm can generate its entire sequence path. In fact, it is enough to add 

66 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

**Algorithm 3.2** Least-angle regression with lasso modification 

Let _A_ be the set of active covariates indices, _XA_ the matrix with the active covariates, and _βA_ the coefficients vector for these variables. 

1. Start: _r_ ← _y_ , _β_[ˆ] _j_ ← 0 _, j_ = 1 _. . . , p_ . Assume _xj_ standardized. _A_ ←∅. 

2. Find predictor, say, _xj_ 1 most correlated with _r_ . Update _A_ ← _A_ ∪{ _j_ 1}. 3. Increase _βj_ 1 in the direction of sign(corr { _r, xj_ 1}) until some other competitor _xj_ 2 has as much correlation with current residual as _xj_ 1 does. Update _A_ ← _A_ ∪{ _j_ 2}. 

4. Cycle for _k_ = 3 _, . . . , p_ ; 

   - a. Update residuals _r_ ← _y_ − _XAβ_[ˆ] _A_ . 

   - b. Move _β_[ˆ] _A_ in the joint least squares direction for the regression of _r_ on _XA_ (i.e., equiangular between the variables already in _XA_ ) until some other competitor _xjk_ has as much correlation with the current residual. Update _A_ ← _A_ ∪{ _jk_ }. 

   - c. [lasso modification:] If a nonzero coefficient reaches 0 (e.g., changes its sign), remove that variable from set _A_ and recompute the current equiangular (joint least squares) direction. 

5. Stop when corr { _r, xj_ } = 0, for all _j_ , that is, least squares solution. 

a new step to the algorithm by indicating that if a nonzero coefficient becomes 0, the corresponding variable must be removed from the model. The best joint least squares direction is then recomputed, requiring the algorithm to start again from this new best direction. Clearly, the number of steps in the lasso-modified LAR algorithm (which is called LARS) may be larger than that of the LAR algorithm itself, but the order of magnitude of computations remains the same. 

## _Bibliographical notes_ 

Hoerl & Kennard (1970) proposed ridge regression to solve the problem of the instability of the least squares estimator in linear models, and since then the method hasbeenpresentedanddiscussedinmanyworks.LassowasproposedbyTibshirani (1996) and the LAR procedure by Efron et al. (2004). They are also presented in detail in Hastie et al. (2009, section 3.4), Miller (2002, sections 3.10–3.11) and Izenman (2008, sections 5.5–5.9). 

## EXERCISES 

3.1 Prove (3.2). 

- ˆ 

- 3.2 Write (3.2) in explicit form when _y_ is a polynomial of degree _p_ (for _p_ = 0 _,_ 1 _, . . . , n_ − 1), and _x_[′] = 2. 

Optimism, Conflicts, and Trade-offs 

67 

- 3.3 Consider a linear regression model with _p_ parameters fitted to a training set ( _x_ 1 _, y_ 1) _, . . . ,_ ( _xn, yn_ ) randomly selected from the available data, in which _β_ are linear regression coefficients. The mean squared error on this set is _n_ 

- _Rtrain_ ( _β_ ) =[1] _n_ � _i_ =1[(] _[y][i]_[ −] _[β]_[⊤] _[x][i]_[)][2][. A test set (] _[x][m]_[+][1] _[,][ y][m]_[+][1][)] _[, . . . ,]_[ (] _[x][m]_[+] _[n][,][ y][m]_[+] _[n]_[)] 1 _m_ 

- is also available with mean squared error _Rtest_ ( _β_ ) = _m_ � _i_ =1[(] _[y][n]_[+] _[i]_[−] _β_[⊤] _xn_ + _i_ )[2] . Show that E _Rtrain_ ( _β_[ˆ] ) ≤ E _Rtest_ ( _β_[ˆ] ) , in which expectations � � � � 

- are taken with respect to all the random elements in each expression. 

- 3.4 Obtain (3.4) by applying the results of section 2.2.3. 

- 3.5 If _q_ in (3.6) is 9, what is the size of the set of all possible models that can be 

4 

## Prediction of Quantitative Variables 

## 4.1 NONPARAMETRIC ESTIMATION: WHY? 

Let us go back to the car data used in chapter 2 and examine the problem of predicting city distance by making use of the other available variables, in particular, engine size and weight. The method used in section 2.1 was parametric, in that we have assumed that function _f_ of (2.2), which expresses the relationship between the response and the covariates, is a member of a parametric class of functions and that the parameter estimate _β_[ˆ] denotes the chosen member of the class. 

The simplest example of this approach is by use of the regression line specified in (2.1) in the case of a single covariate. However, we saw that this formulation is not sufficient—for instance, for the data shown in figure 2.2—and this requires more elaborate formulations, that is, polynomials, transformations of response variables, nonlinear transformations of covariates, and so on. 

An alternative route is to make no reference to either the framework of linear models or any other parametric formulation for _f_ , but to estimate _f_ in a nonparametric way—that is, without assuming that _f_ belongs to a specific parametric class of functions and assuming only some mathematical regularity conditions. Consequently, there is no longer any need to transform the variables in a nonlinear way. 

The nonparametric approach to regression turns out to be particularly effective, mainly (but certainly not only) when there is a considerable amount of data, as is often the case in our type of applications. In fact, with a large amount of data, we always have enough empirical evidence to “falsify” any parametric model, except 

Prediction of Quantitative Variables 

69 

when dealing with the “true” model and, as mentioned in section 1.2.1, this very rarely occurs. The reason for this failure lies in the attempt to summarize all the data in a limited number of parameters, but this difficulty can be overcome with tools that offer great flexibility. 

The main aim of this chapter is to explore these tools. Because the approach lends itself to several very different formulations, we only select the main ones here. We also note that the existence of diverse formulations signifies that the “free” expression of the data just mentioned is not in fact completely free: there are various methods available, and using one rather than another may produce different results, at least partially or in certain circumstances. Again, it is up to us to choose the tool best adapted to the specific problem. 

## 4.2 LOCAL REGRESSION 

## 4.2.1 Basic Formulation 

We are interested in examining the relationship that links two quantities, represented by variables _x_ and _y_ , using a formula of the type 

**==> picture [193 x 11] intentionally omitted <==**

where _ε_ is a random, nonobserved error term. Without loss of generality, we can assume that E{ _ε_ } = 0 because a possible nonzero value can be included in _f_ ( _x_ ). This formulation is similar to that of (2.2), but we do not presume that _f_ is a member of a specific parametric class. We limit ourselves to looking for an estimate of _f_ ( _x_ ), presuming only some regularity conditions. 

Consider a general but fixed point _x_ 0 of real numbers. We want to estimate _f_ ( _x_ ) of (4.1) at point _x_ 0. 

If _f_ ( _x_ ) is a derivable function with a continuous derivative at _x_ 0, then, based on development of the Taylor series, _f_ ( _x_ ) is locally approximated by a line passing through ( _x_ 0 _, f_ ( _x_ 0)), that is, 

**==> picture [186 x 29] intentionally omitted <==**

where the remainder is a quantity with an order of magnitude less than | _x_ − _x_ 0|. 

Transferring this idea to the context of statistical estimation, we estimate _f_ ( _x_ ) in a neighborhood _x_ 0 by means of a criterion that takes advantage of this fact, according to _n_ observation pairs ( _xi, yi_ ) for _i_ = 1 _, . . . , n_ . The remainder term is incorporated in _ε_ . 

Let us therefore introduce a criterion analogous to (2.3), but we now weigh observations based on their distance from _x_ 0, which is 

**==> picture [245 x 31] intentionally omitted <==**

where weights _wi_ are chosen so that they are largest when | _xi_ − _x_ 0| is smallest. Formula (4.2) is a particular form of the _weighted least squares criterion_ , 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

70 

_Table 4.1._ SOME COMMON CHOICES FOR KERNELS 

|_Table 4.1._ SOME|OMMONCHOICES FORKERNELS|
|---|---|
|Nucleus|_w_(_z_)<br>Support|
|Normal<br>Rectangular<br>Epanechnikov<br>Biquadratic<br>Tricubic|1<br>~~√~~<br>2_π_<br>exp<br>�<br>−1<br>2_z_2�<br>R<br>1<br>2<br>(−1_,_1)<br>3<br>4(1−_z_2)<br>(−1_,_1)<br>15<br>16 (1−_z_2)2<br>(−1_,_1)<br>70<br>81 (1−|_z_|3)3<br>(−1_,_1)|



a generalization of least squares when a set of weights is available. Following this criterion, the estimates of the parameters _β_ = ( _β_ 0 _, β_ 1)[⊤] are 

**==> picture [102 x 14] intentionally omitted <==**

where _X_ is a _n_ × 2 matrix whose _i_ th row is (1 _,_ ( _xi_ − _x_ 0)), and _W_ is the _n_ × _n_ diagonal matrix with _wi_ as diagonal elements. Because weights _wi_ are constructed with a “local” perspective around _x_ 0, the resulting estimation method is called _local regression_ . Minimization problem (4.2) is resolved by _β_[ˆ] and the estimate of _f_ ( _x_ 0) is _f_[ˆ] ( _x_ 0) = _β_[ˆ] 0. 

One way to select the weights is to set 

**==> picture [88 x 26] intentionally omitted <==**

where _w_ (·) is a symmetric density function around the origin, which in this context, is called a _kernel_ , and _h_ (with _h >_ 0) represents a scale factor, which is called _bandwidth_ or _smoothing parameter_ . Some of the more common choices for kernel _w_ (·) are listed in table 4.1. It is convenient to think of the normal kernel, corresponding to density _N_ (0 _,_ 1), which we use from now on. 

Figure 4.1 exemplifies the result of nonparametric estimation in the case of data for distance covered in relation to car engine size. The top-left panel presents the data, already seen in chapter 2. The top-right panel illustrates how the estimate works, highlighting the system of weights relative to specific point _x_ 0 = 3, for the particular choice _h_ = 0 _._ 5 with normal kernel, as indicated by the dashed curve. The shaded area distinguishes the _smoothing window_ on the _x_ -axis, whose points have an overall relative weight of 95% in (4.2). The other points on the continuous curve were obtained by shifting the weights indicated by the dashed curve along the _x_ -axis and reapplying (4.2). 

Expression (4.2) depends on weights _wi_ , which in turn depend on elements _h_ , _w_ (·), and _x_ 0. Even with _h_ and kernel _w_ (·) fixed, the minimization problem depends on _x_ 0, and estimating _f_ ( _x_ ) for different choices of _x_ requires many minimization operations. Repeating the minimization operation is not a problem, as we can 

Prediction of Quantitative Variables 

71 

**==> picture [330 x 330] intentionally omitted <==**

**----- Start of picture text -----**<br>
h = 0.5<br>1 2 3 4 5 1 2 3 4 5<br>Engine size (L) Engine size (L)<br>h = 0.15 h = 1<br>1 2 3 4 5 1 2 3 4 5<br>Engine size (L) Engine size (L)<br>20 20<br>15 15<br>10 10<br>City distance (km/L) City distance (km/L)<br>5 5<br>20 20<br>15 15<br>10 10<br>City distance (km/L) City distance (km/L)<br>5 5<br>**----- End of picture text -----**<br>


Figure 4.1 Car data: estimates with local regression of relationship between engine size and city distance for some choices of _h_ . 

show that the estimate relative to a general point _x_ can be obtained from the explicit formula: 

**==> picture [269 x 31] intentionally omitted <==**

where _ar_ ( _x_ ; _h_ ) = {[�] ( _xi_ − _x_ ) _[r] wi_ } _/n_ , for _r_ = 0 _,_ 1 _,_ 2. We are therefore dealing with an estimate that is noniterative and linear in the _yi_ , and can therefore write 

**==> picture [50 x 15] intentionally omitted <==**

for a suitable vector _sh_ ∈ R _[n]_ depending on _h_ , _x_ and _x_ 1 _, . . . , xn_ . 

We do not usually estimate _f_ ( _x_ ) at a single point, but on a whole set of _m_ values (generally equally spaced) that span the interval of interest for variable _x_ . We can 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

72 

calculate each of the _m_ estimates by a single matrix operation of the type 

**==> picture [189 x 14] intentionally omitted <==**

where _Sh_ is an _m_ × _n_ matrix, called _smoothing matrix_ ; _x_ is now the vector (in R _[m]_ ) of the _x_ -axis where we estimate function _f_ ; and _f_[ˆ] ( _x_ ) is the corresponding estimation vector. 

If _n_ is very large, we can reduce the size of matrix _Sh_ by regrouping variable _x_ into classes, and therefore use an _m_ × _n_[′] matrix, with _n_[′] ≪ _n_ . 

The choice to approximate a function _f_ ( _x_ ) locally by a straight line may be relaxed by fitting a polynomial locally. Degree 0 and degree 2 are the alternatives in actual use. When a polynomial of degree 0 is used, the estimate of each point is a weighted mean of the data in a neighborhood of that point. However, a modification of this procedure with degree 0, called _k_ -nearest-neighbor and described later (section 4.2.4), is typically preferred. A polynomial of degree 2 is an appropriate choice when the data show sharp peaks and troughs, because this variant is more suitable for producing steep curves. 

## 4.2.2 Choice of Smoothing Parameters 

The problem of the choice of _h_ and _w_ (·) remains. The latter is not critical, as many studies on the subject have shown, and we can use any kernel listed in table 4.1. At most, there is a slight benefit in using continuous functions and some computational advantages in the choice of kernels with limited support. 

The truly important aspect is the choice of smoothing parameter _h_ . One direct indication of the effect of the choice of _h_ is provided by the last two panels in figure 4.1. Lowering value _h_ clearly produces curve _f_[ˆ] , which is closer to the local behavior of the data and is therefore rougher, because the allocated weights system works on a smaller window and is more affected by local data variability. In the other direction, the increase in _h_ produces the opposite effect: the window on which the weights operate widens and the curve becomes smoother. 

To understand which ingredients regulate the behavior of _f_[ˆ] , particularly in relation to _h_ , we must study the formal properties of _f_[ˆ] . Limiting ourselves to quite simple working hypotheses, let us assume that var { _εi_ } = _σ_[2] is a positive constant common to all observations and that the observations are not correlated. Under suitable regularity conditions for _f_ , we can prove that for _h_ sufficiently close to 0 and _n_ sufficiently large, the approximations 

**==> picture [305 x 28] intentionally omitted <==**

hold, where _σw_[2] = � _z_[2] _w_ ( _z_ ) d _z_ , _α_ ( _w_ ) = � _w_ ( _z_ )[2] d _z_ , and _g_ ( _x_ ) indicates the density from which the _xi_ were sampled. 

These expressions show that bias is a multiple of _h_[2] and the variable is a multiple of 1 _/_ ( _n h_ ). Therefore, although we would like to choose _h_ → 0 to bring down the bias, this makes the variance of the estimate diverge. For _h_ →∞, the opposite 

Prediction of Quantitative Variables 

73 

occurs: the variance is reduced, but the bias diverges. Relations (4.5) are valid in the somewhat restrictive hypotheses previously mentioned, but the same type of indication is essentially valid with weaker hypotheses: the resulting formulas are more complex, but the qualitative indication is similar. 

At this point, we can also verify the same contrast between the bias and variance of the estimate already seen in chapter 3, in another context. As in that case, we must adopt a trade-off solution, balancing bias and variance in some way. 

In a certain sense, the optimal solution is implicit in relations (4.5). That is, minimizing the sum of the variance and the square of the bias, as indicated in (3.3), the asymptotically best choice for _h_ is 

**==> picture [232 x 30] intentionally omitted <==**

However, this expression is not directly useful because it involves unknown terms _f_[′′] ( _x_ ) and _g_ ( _x_ ), although it does supply at least two important elements: 

- it tells us that _h_ must tend to 0 as _n_[−][1] _[/]_[5] , and therefore that it decreases very slowly; 

- if we substitute this _h_ opt into the mean and variance expressions (4.5), it tells us that the mean squared error tends to 0 at a rate of _n_[−][4] _[/]_[5] ; therefore this method of nonparametric estimation is intrinsically less efficient than a parametric one with a rate of decrease of _n_[−][1] , when the parametric model is satisfactory. 

This last remark has much broader validity than is apparent here, in the sense that the basic indication is also valid for other methods of nonparametric estimation (see later). 

Operatively, to choose _h_ , we therefore take different routes to those in (4.6), or at least we do not use it directly. A somewhat rudimentary but effective method is to try some values and select by eye which seem most appropriate, as we did for figure 4.1. There are, however, more formal processes, which follow lines similar to those of section 3.5. 

In particular, the methods of cross-validation and AIC _c_ (section 3.5) are in current use, having been suitably adapted to the problem. Specifically, the AIC _c_ variant 

**==> picture [156 x 27] intentionally omitted <==**

is proposed, inspired by section 3.5.3; see Hurvich et al. (1998). Here 

**==> picture [233 x 29] intentionally omitted <==**

**==> picture [331 x 178] intentionally omitted <==**

**----- Start of picture text -----**<br>
74 D A T A A N A L Y S I S A N D D A T A M I N I N G<br>1 2 3 4 5 1 2 3 4 5<br>Engine size (L) Engine size (L)<br>20 20<br>15 15<br>10 10<br>City distance (km/L) City distance (km/L)<br>5 5<br>**----- End of picture text -----**<br>


Figure 4.2 Car data: estimation by local regression with _h_ chosen by AIC _c_ (left) and by loess method (right). 

is the estimate of residual variance _σ_[2] , and tr( _Sh_ ) indicates the trace of matrix _Sh_ in (4.4). This trace is a substitutive measure of the number of parameters involved, 

The first panel in figure 4.2 presents the result of local regression with _h_ = 0 _._ 21, chosen by the AIC _c_ criterion represented by the continuous curve, but removing the values corresponding to the four anomalous points (shown as two single points bottom-left). The meaning of the dotted curves will be explained shortly. 

To conclude, we note that the linearity of the estimation process with respect to _yi_ , established at the end of section 4.2.1, is valid when _h_ is fixed independently of the data. However, if _h_ is chosen on the basis of the same data, as commonly occurs, then the method is no longer linear. 

## 4.2.3 Variability Bands 

To make inferences, it is useful to develop a tool that is similar to the confidence interval, to give the estimate of _f_ ( _x_ ) an indicator of its reliability. To construct such an interval, we must refer to a pivotal quantity, at least approximately, of the type 

**==> picture [230 x 44] intentionally omitted <==**

where _b_ ( _x_ ) indicates the bias of the estimate, of which the main term is approximated by the final term of the first expression of (4.5); analogously, the variance in the denominator is approximated by the second expression of (4.5). Note that for the asymptotically optimal bandwidth (4.6), the bias has the same order of magnitude as the denominator of (4.7). Therefore, the bias term cannot be neglected in this framework, in contrast with what happens in a parametric context. 

Prediction of Quantitative Variables 

75 

Of the various quantities in play, all, in some way, can be computed at least approximately, except term _f_[′′] ( _x_ ), which is included in bias _b_ ( _x_ ). This means that constructing a confidence interval is not feasible, even in an approximate form. 

Instead of looking for extremely complicated corrections to remedy the problem, a current solution is to construct _variability bands_ of the type 

**==> picture [231 x 20] intentionally omitted <==**

where _zα/_ 2 is the 1 − _α/_ 2 quantile of distribution _N_ (0 _,_ 1) and std.err( _f_[ˆ] ( _x_ )) the denominator of (4.7). Strictly speaking, the previous expression is clearly that of an interval, but once the expression is applied to every point on the _x_ -axis, it gives rise to two bands. The result is shown by the dotted curves in the left panel of figure 4.2. 

Two observations are necessary: (1) for every fixed _x_ , the previous interval does not constitute a confidence interval, for the reasons already mentioned, but only provides an indication of the local variability of the estimate; (2) even if bias _b_ ( _x_ ) were not present, the interval thus constructed would have a confidence level of approximately 1 − _α_ for _f_ ( _x_ ) to _each_ fixed value of _x_ , but not globally for the entire curve. 

## 4.2.4 Variable Bandwidths and loess 

There are several variations to the basic method of local regression as described up to now. The most common variation regards the use of a nonconstant bandwidth along the _x_ -axis, but according to the level of sparseness of observed points. If again we look at figure 4.1, it is reasonable to use larger values of _h_ when _xi_ are more scattered (mainly for _x >_ 3). 

These intuitive considerations are confirmed by expression (4.6), in which the presence of _g_ ( _x_ ) in the denominator shows that when density _g_ ( _x_ ) is low, that is, when observations _xi_ are sparse, we must use a larger value of _h_ to keep var _f_ ˆ ( _x_ ) � � the same. 

One technique, which arose from these considerations, is loess, which is very similar to the local regression in section 4.2.1. A distinctive feature of loess is that it expresses the smoothing parameter by means of the fraction of effective observations for estimating _f_ ( _x_ ) at a certain point on the _x_ -axis; this fraction is kept constant. To understand how this works, let us look at the top-right panel in figure 4.1. When we estimate _f_ ( _x_ ) at another point on the _x_ -axis, with local regression the weights system and associated colored area are shifted horizontally, and we do not take into account the level of local sparseness of points on the _x_ -axis. Instead, loess widens or narrows the window, so that the fraction of observations involved remains constant. 

We can now see that the degree of smoothing is regulated by the fraction of points used, just like the bandwidth. Therefore, this fraction constitutes the smoothing parameter in loess. 

Another typical aspect of loess is that it combines the ideas of local regression and _robust estimation_ , which means that we substitute the quadratic function 

**==> picture [331 x 177] intentionally omitted <==**

**----- Start of picture text -----**<br>
76 D A T A A N A L Y S I S A N D D A T A M I N I N G<br>1 2 3 4 5 1 2 3 4 5<br>Engine size (L) Engine size (L)<br>20 20<br>15 15<br>10 10<br>City distance (km/L) City distance (km/L)<br>5 5<br>**----- End of picture text -----**<br>


Figure 4.3 Car data: estimation by _k_ -nearest-neighbor with _k_ = 10 (left) and _k_ = 60 (right). 

of (4.2) with another objective function that limits the effect of _anomalous observations_ , commonly called _outliers_ . 

Again according to the _robustness_ considerations of the procedure, loess uses a limited support kernel, generally tricubic (see table 4.1), which also has the advantage of more clearly distinguishing between used and unused points in the estimate. 

The second panel of figure 4.2 shows the result of the estimate and relative variability bands obtained through loess for the car data, with a fraction of 75% of the observations and a quadratic objective function such as (4.2) as smoothing parameter. The same panel also shows the estimated curve when the robust variant is used: this is the dashed curve that goes beyond the variability bands of the nonrobust method. 

The local regression of degree 0, when a nonconstant bandwidth along the _x_ -axis is chosen, is very simple and quite commonly used. The estimate of the function at each point is obtained as the average of a fixed number of closest observations around that point. This method is called _k–nearest–neighbor_ , where _k_ denotes the number of observations averaged by the estimate. We use _k_ to indicate the decreasing complexity of the procedure because, when _k_ = _n_ , the estimate is simply the average of all available observations, giving a constant fit over the entire _x_ -axis. Instead, when _k_ = 1, the value of _y_ of the closest observation is used at every single point as an estimate of the function, producing a very rough curve. 

As an example, figure 4.3 displays the _k_ -nearest-neighbor predicting function of city distance with engine size at _k_ = 10 and _k_ = 60. 

## 4.2.5 Extension to Several Dimensions 

The formulation of section 4.2.1 may also be applied when two or more covariates, say, _p_ , are used. Let us begin with the simplest case of two variables, _x_ 1 and _x_ 2, and 

Prediction of Quantitative Variables 

77 

presume that a relationship of the type 

**==> picture [75 x 12] intentionally omitted <==**

holds, where _f_ ( _x_ 1 _, x_ 2) is now a function from R[2] to R. 

The available data are now made up of the same _yi_ as previously and of points _xi_ = ( _xi_ 1 _, xi_ 2) ∈ R[2] , for _i_ = 1 _, . . . , n_ . To estimate _f_ corresponding to a specific point, _x_ 0 = ( _x_ 01 _, x_ 02), a natural extension of the criterion (4.2) takes the form 

**==> picture [301 x 31] intentionally omitted <==**

where weights _wi_ are now to be determined as a function of a suitable distance between _xi_ and _x_ 0. A common way of choosing _wi_ is to set 

**==> picture [179 x 26] intentionally omitted <==**

which is a simple extension of what we saw in section 4.2.1. Clearly, this expression involves two smoothing parameters, _h_ 1 and _h_ 2, to take into account the different variability of _x_ 1 and _x_ 2. 

From a computational point of view, we can also tackle this problem as a variation of weighted least squares. If we indicate by _X_ the _n_ × 3 matrix of which the _i_ th row is 

**==> picture [109 x 11] intentionally omitted <==**

_y_ = ( _y_ 1 _, . . . , yn_ )[⊤] and _W_ = diag( _w_ 1 _, . . . , wn_ ), then the solution of the previous minimum problem is the first element, which corresponds to _β_ 0, of ( _X_[⊤] _WX_ )[−][1] _X_[⊤] _Wy_ . Obviously, this calculation is repeated for every choice of point _x_ 0, and tendentially the number of these points is now higher than in the scalar case of section 4.2.1. 

Figure 4.4 shows the results obtained for the car data with _x_ 1 = engine size, _x_ 2 = curb weight, and _y_ = city distance, in two forms of representation: perspective and level curves. To avoid extrapolating the estimate where we have no observations, it is limited to the convex hull of the observed points of ( _x_ 1 _, x_ 2). 

Formally, most of the results can be easily extended to the multivariate case, where the formulation is of the type 

**==> picture [239 x 13] intentionally omitted <==**

Definition of the estimation method seen for _p_ = 1 and _p_ = 2 extends naturally to the case of general _p_ , meaning that there is no need to repeat the discussion of various connected aspects, such as the choice of _h_ , and so on. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

78 

**==> picture [327 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
15<br>10<br>1<br>2<br>3<br>8001000 4<br>1200<br>1400<br>1600 5<br>1800 1 2 3 4 5<br>Engine size (L)<br>Curb weight (kg)<br>Engine size (L)<br>City distance (km/L)<br>1800<br>1600<br>1400<br>1200<br>Curb weight (kg)<br>1000<br>800<br>**----- End of picture text -----**<br>


Figure 4.4 Car data: estimation of city distance by local regression with two covariates, engine size and curb weight. 

## _Bibliographical notes_ 

A more detailed but still fairly informal presentation of the nonparametric approach through local regression is given in Bowman & Azzalini (1997). The book is associated with the R package, an evolution from an earlier version of software written in S-plus and with a set of additional scripts. These tools have been used extensively here; specifically figure 4.1 is based on one of the scripts associated with the book. For more advanced mathematical coverage of the subject, see Fan & Gijbels (1996) and Wand & Jones (1995). Loader (1999) extends the local regression approach by combining it with the likelihood concept, particularly within generalized linear models, and supplies other software tools for the S-plus and R environments. Loess was originally proposed by Cleveland (1979) and further developed by Cleveland & Devlin (1988) and is described in Cleveland et al. (1992). 

## 4.3 THE CURSE OF DIMENSIONALITY 

In practice, we rarely go much beyond two dimensions in nonparametric regression. The first reason is the poor conceptual manageability of the resulting object: although the idea of a function with 6 or 26 variables is not conceptually different from one with 2 variables, it is actually difficult to visualize mentally and graphically. Interpreting the results is also difficult. 

A second and perhaps more important aspect is that with increasing dimension _p_ of the space in which the covariates are placed, the observed points scatter very quickly. To understand the essence of the problem intuitively, think of _n_ = 500 points on the _x_ -axis, randomly set over an interval that, without loss of generality we may presume to be unit interval (0 _,_ 1). If we use these _n_ points to estimate function _f_ ( _x_ ), we obtain a reliable estimate, thanks to the small average distance that separates them. If the same number _n_ of points is then distributed in square (0 _,_ 1)[2] of plane ( _x_ 1 _, x_ 2), they are much less close to each other. If we then move to higher dimensions, say, _p_ , the dispersion of _n_ points in space R _[p]_ 

Prediction of Quantitative Variables 

79 

increases very rapidly, and the quality of the obtainable estimate correspondingly worsens. 

To compensate for the increased space between the points, we need a number of points of the order of magnitude _n[p]_ . However, although it is common to use a sample of size _n_ = 500, it is much more uncommon to have 500[5] units available, and practically impossible to have 500[10] , even in a data mining context. These are the sizes that are in some way equivalent to estimating function _f_ nonparametrically when the number of covariates is 5 or, respectively, 10. 

This situation of substantial impossibility in estimating function _f_ accurately when _p_ is large is called the _curse of dimensionality_ . For a more detailed explanation of how the scatter of the points increases with _p_ , and for other similar issues, see Hastie et al. (2009; section 2.5). 

A further critical aspect with increasing _p_ is the increased computational cost, at least when a substantial increase in _n_ also occurs. 

These problems are not confined to the specific technique of local regression, but they are substantially valid for all nonparametric estimation techniques, as they are due to the dimension and dispersed nature of the data with respect to the number of points from which we wish to estimate the function and not so much to the method chosen for data processing. 

To overcome the problem of the curse of dimensionality, one strategy is to carry out a preliminary operation to reduce the number _p_ of the covariates, transforming them into a reduced set of new variables but at the same time losing as little of their informative content as possible. 

The simplest and probably most frequent way of achieving this is to extract some of the _principal components_ of the original covariates. Therefore, once the complete set of principal components has been constructed, a suitable number of them are chosen, keeping a sufficient proportion of the original variability and the number of new variables low. For a discussion of the advantages and disadvantages of PCA, see section 3.6.2. 

Therefore, in the following section, what we indicate as covariates may not represent the original variables but those constructed through principal components or other methods of dimensionality reduction (see section 3.6.2). 

## _Bibliographical notes_ 

The concept of the curse of dimensionality was introduced by Bellman (1961). Hastie et al. (2009; section 2.5) give a very detailed description of it in the context of data mining and also discuss a number of additional issues. 

## 4.4 SPLINES 

The term _spline_ originally meant the flexible strips of wood used to shape ships’ hulls. Some points on the cross-section of the hull were chosen, and the rest of the curve of the hull was derived by forcing the wooden strips to pass through such points, leaving them free to fit into the rest of desired curve according to their natural tendency. This gave rise to a regular curve with preassigned behavior in certain positions. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

80 

## 4.4.1 Spline Functions 

The term _spline_ is used in mathematics to construct piecewise polynomial functions, according to a logic that partly replicates the mechanism just described, to approximate functions of which we know the value only at certain points. 

We choose _K_ points _ξ_ 1 _< ξ_ 2 _<_ · · · _< ξK_ , called _knots_ , along the _x_ -axis. A function _f_ ( _x_ ) is constructed so that it passes exactly through the knots and is free at the other points, with the constraint that it presents regular overall behavior. In this sense, the function behaves like splines used in shipyards. 

The following strategy is followed: between two successive knots, say, in the interval ( _ξi, ξi_ +1), curve _f_ ( _x_ ) coincides with a suitable polynomial, of prefixed degree _d_ , and these sections of polynomials meet at point _ξi_ ( _i_ = 2 _, . . . , K_ − 1), in the sense that the resulting function _f_ ( _x_ ) has a continuous derivative from degree 0 to degree _d_ − 1 in each of the _ξi_ . 

The degree that is almost universally used is _d_ = 3, and we therefore speak of cubic splines. The reason for this is that the human eye cannot perceive discontinuity in the third derivative. The foregoing conditions are therefore written as 

**==> picture [288 x 50] intentionally omitted <==**

where _g_ ( _x_[−] ) and _g_ ( _x_[+] ) indicate the left and right limits of a function _g_ (·) at point _x_ . 

The framework of the problem requires the following set of conditions: each of the _K_ − 1 cubic components requires four parameters; there are _K_ constraints of the type _f_ ( _ξi_ ) = _yi_ , and 3 ( _K_ − 2) continuity constraints of the function and the 

As the difference between coefficients and constraints is 2 units, the system of conditions does not univocally identify a function. We must therefore introduce two additional constraints. 

Many proposals have been made to define these additional constraints, most of which concern the outmost interval or the extreme points of the function. A particularly simple choice consists of constraining the second derivatives of the polynomials in the two extreme intervals to 0, _f_[′′] ( _ξ_ 1) = _f_[′′] ( _ξK_ ) = 0, which means that the two extreme polynomials are straight lines. The resulting function _f_ ( _x_ ) is called the _natural cubic spline_ . 

## 4.4.2 Regression Splines 

The previous tool is also useful in statistics, in various forms, in the study of relations between a covariate _x_ and a response _y_ , for which we use _n_ pairs of observations ( _xi, yi_ ) for _i_ = 1 _, . . . , n_ . 

Let us begin by applying these ideas to parametric regression. We return to model (2.2), where _f_ ( _x_ ; _β_ ) is hypothesized to be a spline function. Then we divide the _x_ -axis into _K_ + 1 intervals separated by _K_ knots, _ξ_ 1 _, . . . , ξK_ , and interpolate 

Prediction of Quantitative Variables 

81 

the _n_ points with criterion (2.3), where the _β_ coefficients are now the nonconstrained parameters of the _K_ + 1 constituent polynomials. 

With respect to section 4.4.1, there is a certain difference in that the spline function coefficients can no longer be chosen according to constraints of the type _f_ ( _ξj_ ) = _yj_ , because _K_ and _n_ are no longer linked and _K_ ≪ _n_ . This means that we have to use a fitting criterion between the data and the interpolated function, for example, the least squares criterion or a similar one. 

If we use cubic splines, the total number of cubic parameters is 4( _K_ + 1) subject to 3 _K_ continuity constraints, and therefore _β_ has _K_ + 4 components. The solution to the minimum problem (2.3) may be rewritten in the equivalent form 

**==> picture [213 x 34] intentionally omitted <==**

where 

**==> picture [175 x 35] intentionally omitted <==**

and _a_ + = max( _a,_ 0). The solution is thus represented by a suitable linear combination of _basis functions_ { _hj_ ( _x_ ) _, j_ = 1 _, . . . , K_ + 4}, composed partly of low-order powers of _x_ and partly of functions of the type max(0 _,_ ( _x_ − _ξ_ )[3] ). 

The number _K_ of knots and their position along the _x_ -axis need to be chosen. Because _K_ is viewed as a tuning parameter, regulating the complexity of the model, the strategies proposed in section 3.5 apply. Once _K_ has been set, when no information is available about the shape of the function to be estimated, a reasonable choice for knot positions is uniformly along the _xi_ range. Alternatively, the quantiles of the empirical distribution of the _xi_ are chosen as knots. 

Figure 4.5, which concerns our yesterday’s data, illustrate regression splines. We used _K_ = 2 knots, marked by vertical dotted lines. As well as the standard solution for the degree _d_ = 3, we also constructed those for _d_ = 1 and _d_ = 2 for purposes of illustration only. Obviously, in the last two cases, the basis function changes: in particular, for _d_ = 1, the basis is represented by 

**==> picture [285 x 13] intentionally omitted <==**

The right panel of figure 4.5 shows function ( _x_ − _ξ_ 1)+ as an example of the characteristic component of this approach. 

## 4.4.3 Smoothing Splines 

Another way of using spline functions in studying the relationship between variables is to introduce an approach to nonparametric estimation as an alternative to local regression. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

**==> picture [331 x 175] intentionally omitted <==**

**----- Start of picture text -----**<br>
82 D A T A A N A L Y S I S A N D D A T A M I N I N G<br>3 2 1<br>0.5 1.0 1.5 2.0 2.5 3.0 0.5 1.0 1.5 2.0 2.5 3.0<br>x x<br>2.0<br>0.54<br>0.52 1.5<br>0.50<br>y<br>1.0<br>0.48<br>Max(0,x−1.333)<br>0.46 0.5<br>0.44<br>0.0<br>**----- End of picture text -----**<br>


Figure 4.5 Yesterday’s day: interpolated functions for _d_ = 1 _,_ 2 _,_ 3 (left) and the component function ( _x_ − _ξ_ 1)+ (right). 

Let us consider the penalized least squares criterion 

**==> picture [269 x 31] intentionally omitted <==**

where _λ_ is a positive penalization parameter of the roughness degree of curve _f_ , quantified by the integral of _f_[′′] ( _x_ )[2] , and therefore acts as a smoothing parameter. 

If _λ_ → 0, there is no penalization for the roughness of _f_ ( _x_ ), so the previous criterion is not influenced by _f_ ( _x_ ) outside points _x_ 1 _, . . . , xn_ , and the optimal solution _f_[ˆ] ( _xi_ ) is the arithmetic mean of the _yi_ corresponding to each fixed _x_ for each of the observed _xi_ but is not determined for other values of _x_ . If _λ_ →∞, the penalty is maximal and means adapting a line imposing _f_[′′] ( _x_ ) ≡ 0. The overall result is the least squares line. Therefore, the role of _λ_ is qualitatively similar to that of _h_ in the case of local regression. 

A noteworthy mathematical result (Green & Silverman 1994) shows that the solution to the minimization problem (4.11) is represented by a _natural cubic spline_ , whose knots are distinct points _xi_ . The solution may be written as 

**==> picture [84 x 33] intentionally omitted <==**

where _n_ 0 is the number of distinct _xi_ and the _Nj_ ( _x_ ) are natural cubic splines basis functions. 

We can rewrite 

**==> picture [181 x 13] intentionally omitted <==**

where _N_ is the matrix in which the _j_ th column contains the values of _Nj_ corresponding to the _n_ 0 distinct values of _x_ , and _�_ is the matrix of which the 

Prediction of Quantitative Variables 

83 

**==> picture [258 x 255] intentionally omitted <==**

**----- Start of picture text -----**<br>
λ = 0.00071<br>λ = 0.01971<br>λ = 2.89867<br>1 2 3 4 5<br>Engine size (L)<br>20<br>15<br>City distance (km/L)<br>10<br>5<br>**----- End of picture text -----**<br>


Figure 4.6 Car data: Estimate of city distance according to engine size by a smoothing spline for three choices of _λ_ . 

generic element is � _Nj_[′′][(] _[t]_[)] _[ N] k_[′′][(] _[t]_[)][d] _[t]_[. The solution of the optimization problem is] given by 

**==> picture [221 x 14] intentionally omitted <==**

which clearly depends on the choice of smoothing parameter _λ_ . 

ˆ If this expression of _θ_[ˆ] is substituted into that of _f_ ( _x_ ), we have _y_ = _S_[˜] _λ y_ for a certain matrix _S_[˜] _λ_ of dimension _n_ 0 × _n_ 0, that is, we are dealing with another _linear smoother_ . In this case, we speak of _smoothing splines_ . 

However, from a computational point of view, we do not proceed with (4.12), which involves a matrix of order _n_ 0. There are much more efficient algorithms, for which we refer readers to the specialized literature (see the bibliographical notes). In addition, when the quantity of data is very large, we can reduce the number of knots used, without loss of accuracy, as we did for local regression at the end of section 4.2.1. 

Again, figure 4.6 shows what is obtained when this procedure is applied to the car data for three choices of parameter _λ_ . We can also use the criteria discussed earlier for the choice of smoothing parameter _λ_ (in sections 3.5 and 4.2.2), but here we choose three values that highlight the effect of variations in parameter _λ_ . 

## 4.4.4 Multidimensional Splines 

Extending splines to cases with two or more covariates is not as automatic as for the other smoothing techniques presented in this chapter. Extension of cubic 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

84 

smoothing splines, for example, are _thin-plate splines_ , obtained by a generalization of (4.11) in which, in the penalty function, the second derivative of function _f_ is substituted by the Laplacian. Due to the elevated computational complexity involved, thin-plate splines are hard to use with more than two covariates. In the simple case when we have a pair of covariates _x_ = ( _x_ 1 _, x_ 2)[⊤] ∈ R[2] , the roughness penalty function in (4.11) becomes 

**==> picture [268 x 33] intentionally omitted <==**

The solution to optimization problem (4.11) with this penalty function can be proved to have the form 

**==> picture [136 x 33] intentionally omitted <==**

ˆ where _hj_ ( _x_ ) = _η_ (∥ _x_ − _xj_ ∥), _η_ ( _z_ ) = _z_[2] log _z_[2] , and estimates _αj_ , _β_[ˆ] 0, and _β_[ˆ] are determined by substituting _f_ ( _x_ ) in (4.11) and minimizing with respect to the parameters. 

Figure 4.7 presents the results obtained for car data, again with _x_ 1 = engine size, _x_ 2 = curb weight, and _y_ = city distance, with two forms of graphical representation: perspective and level curves. 

Another type of generalization particularly useful for regression splines is based on _tensor products of splines_ . The extension to multiple dimensions is obtained by constructing a set of basis functions in R _[p]_ , multiplying together the basis of one-dimensional functions for each covariate. If, for example, we consider the two-dimensional case of cubic splines, where _x_ = ( _x_ 1 _, x_ 2)[⊤] ∈ R[2] and we have a basis of functions _h_ 1 _k_ ( _x_ 1) with _k_ = 1 _, . . . , K_ 1 + 4, relative to the first covariate 

**==> picture [329 x 163] intentionally omitted <==**

**----- Start of picture text -----**<br>
15<br>10<br>1<br>2<br>3<br>8001000 4<br>1200<br>1400<br>1600 5<br>1800 1 2 3 4 5<br>Engine size<br>Curb weight<br>Engine size<br>City distance<br>1800<br>1600<br>1400<br>1200<br>Curb weight<br>1000<br>800<br>**----- End of picture text -----**<br>


Figure 4.7 Car data: estimation of city distance according to engine size and curb weight by smoothing splines. 

Prediction of Quantitative Variables 

85 

**==> picture [204 x 156] intentionally omitted <==**

**----- Start of picture text -----**<br>
y<br>x<br>g(x)<br>**----- End of picture text -----**<br>


Figure 4.8 Tensor product basis functions, obtained as product of scalar basis functions of type ( _x_ − _ξ_ )+, as in figure 4.5. 

_x_ 1 and a basis of functions _h_ 2 _k_ ( _x_ 2) with _k_ = 1 _, . . . K_ 2 + 4, relative to the second explanatory variable _x_ 2, the _tensor product basis_ of dimension ( _K_ 1 + 4) × ( _K_ 2 + 4) is defined by 

**==> picture [298 x 13] intentionally omitted <==**

and can be used to represent a two-dimensional function 

**==> picture [114 x 35] intentionally omitted <==**

Parameters _θjk_ can be estimated by the penalized least squares criterion. 

Figure 4.8 is an example of tensor product basis functions obtained with onedimensional components of the type ( _x_ − _ξ_ )+ = max( _x_ − _ξ,_ 0); see figure 4.5. 

## 4.4.5 MARS 

When the number of covariates is high, extension of the previous approach is not easy, due to computational and interpretive difficulties. It is therefore important to use a process that, starting from the information present in the data, allows us to select variables reasonably and provides criteria for the choice of the number of knots necessary for each variable. 

_Multivariate adaptive regression splines_ (MARS) represent a particular iterative specification of regression splines (see section 4.4.2), the aim of which is to model problems with many explanatory variables. The basis functions used are pairs of piecewise linear functions, of the type ( _x_ − _ξ_ )+ and ( _ξ_ − _x_ )+, with a single knot at point _ξ_ , like those of section 4.4.2. 

86 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

The aim is to find the relationship between a dependent variable _y_ and the _p_ covariates _x_ = ( _x_ 1 _, . . . , xp_ ) _[T]_ . For every explanatory variable _xj_ , we determine a pair of basis functions with the knot in each observed value _xij_ , for _i_ = 1 _, . . . , n_ in addition to the linear one. This gives the set of basis functions that are considered as functions on whole space R _[p]_ : 

**==> picture [243 x 34] intentionally omitted <==**

We must select a subset of basis functions in _C_ to combine in a model suitable for fitting the data. Piecewise basis functions are included in the model in pairs of the form {( _xj_ − _ξ_ )+ _,_ ( _ξ_ − _xj_ )+}. The MARS model is therefore of the type: 

**==> picture [219 x 33] intentionally omitted <==**

where _hk_ ( _x_ ) are either functions belonging to _C_ or products of two or more such functions, and _K_ is the number of pairs of basis functions to be included in the model. 

To select the _hk_ functions and estimate parameters _β_ , we follow a recursive process. 

- Start with _K_ = 0. We first introduce constant function _h_ 0( _x_ ) = 1. 

- Generic step _K_ . We presume that the model already has 2( _K_ − 1) terms. We consider, as a new pair of basis functions, each of the possible pairs of products of a function _hk, k_ ∈{1 _, . . . , K_ }, already included in the model, with another pair of functions in _C_ . We then choose the pair of basis functions that adds to (4.13) the terms 

**==> picture [201 x 15] intentionally omitted <==**

which minimize the least squares criterion. Here, _hm_ indicates a function that is already included in the model, and _β_[ˆ] 2 _K_ −1 and _β_[ˆ] 2 _K_ are parameters that are estimated by least squares together with all the other _β_ parameters of the model. 

- The process continues until a predefined maximum _K_ is reached. 

This model is generally very large and may overfit the data. It may be appropriate to formulate a backward procedure in which we iteratively select and remove the terms from the model one by one, at each step deleting the terms that make minor contributions to the residual sum of squares. In this backward procedure, single terms are usually deleted, so the final model is not necessarily characterized by a pair of basis functions for each knot. 

Model subsets are then compared by means of some fitting criterion. When many data are available, we choose the best model subset by using a different test 

Prediction of Quantitative Variables 

87 

set, as in section 3.5.1. Alternatively, we can use cross-validation (see section 3.5.2), which, however, requires a considerable computational load. 

Another alternative is to use _generalized cross-validation_ (GCV). For each model to be compared, GCV is defined as 

**==> picture [116 x 29] intentionally omitted <==**

where _d_ is an indicator of the effective number of parameters in the model. For the MARS context, _d_ is the sum of the number of terms in the model and the number of knots defined in the basis selection process weighted by a penalty that, after some theoretical and simulation results, is usually fixed at 2 or 3. Another frequently used approximation chooses _d_ proportional to the number of terms in the model. Note that the formula used by GCV approximates the error, based on (3.4), which would be determined by _leave one out_ cross-validation for a linear model: this is why it is called _generalized_ cross-validation. 

The pairs of linear functions chosen as basis functions for MARS have the advantage of operating locally. When these basis functions are multiplied together, they are different from 0 only in that part of the space where all the univariate functions are positive (see figure 4.8), and this allows the model to be fitted to the data with a relatively small number of parameters. These functions also have the advantage that they can be multiplied together simply, with greatly reduced computational complexity. 

The constructional logic of the model is clearly hierarchical, in the sense that we can multiply new basis functions that involve new variables only to the basis functions already in the model; therefore, an interaction of a higher order can only be introduced when interactions of a lower order are present. This constraint, introduced for computational reasons, does not necessarily reflect the real behavior of the data, but it often helps in interpreting the results. However, for easier interpretation, we often constrain the model to have only first- or at most secondorder interactions. 

So far, we have considered the case in which explanatory variables are quantitative, but it is also easy to introduce qualitative predictors in the MARS model. If we consider all the possible binary partitions of the levels of a qualitative explanatory variable, each partition generates a pair of basis step functions that indicates membership to one of the two groups of levels. These basis functions can be inserted into _C_ and used like all the others, to obtain products with functions already included in the model. 

For a simple explanation, we again use the car data, this time with only the two covariates engine size and curb weight. The surface obtained with the MARS model is shown in figure 4.9. 

To build a slightly more realistic example, still based on car data, let us now consider as covariates the variables fuel type, intake, bodywork type, traction, motor position, width, height, and length in addition to engine size and curb weight. Table 4.2 lists the relevant information used by the final model at the end of the MARS process. Only pairs of basis functions 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

88 

**==> picture [226 x 220] intentionally omitted <==**

**----- Start of picture text -----**<br>
25<br>20<br>15<br>10<br>1<br>5 2<br>3<br>800<br>1000<br>1200 4<br>1400<br>1600 5<br>1800<br>Curb weight<br>Engine size<br>City distance<br>**----- End of picture text -----**<br>


Figure 4.9 Car data: MARS surface, fitted with two quantitative variables. 

_Table 4.2._ CAR DATA: PARAMETER ESTIMATES OF MARS MODEL 

|Variable|Node|Levels|Parameters|SE|
|---|---|---|---|---|
|constant|||57_._0798|4.4884|
|fuel type||1|−4_._0680|0.2768|
|intake||1|1_._3412|0.2287|
|curb weight|||−0_._0639|0.0063|
|curb weight|861_._84||0_._0510|0.0067|
|curb weight|1149_._88||0_._0069|0.0013|
|engine size|||11_._6215|1.7015|
|engine size|1_._47||−12_._1585|1.7581|



based on single variables occur in the final model, so it has no interactions. The table has a line for each pair of basis functions in the final model: the first column shows the explanatory variable linked to the basis, and for basis functions with piecewise linear components, the second column specifies the point at which the knot for that variable is fixed; otherwise, the basis is linear. For qualitative variables, the third column shows the number of levels into which the factor was divided to determine the relative basis. The fourth column lists parameter estimations _β_[ˆ] _k_ relative to each basis, and the last column shows the estimated standard errors of each parameter. 

Figure 4.10 shows the one-dimensional plots of the estimates of the response variable for each covariate, where the other explanatory variables are kept constant and equal to their median value in each panel. Figure 4.11 displays a similar plot of 

Prediction of Quantitative Variables 

89 

**==> picture [330 x 331] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 2 3 4 5 800 1000 1200 1400 1600 1800<br>Predictor  1 Predictor  2<br>1.0 1.2 1.4 1.6 1.8 2.0 1.0 1.2 1.4 1.6 1.8 2.0<br>Predictor  3 Predictor  4<br>11 25<br>10<br>20<br>9<br>8 15<br>Response Response<br>7<br>10<br>6<br>10.6<br>14 10.4<br>10.2<br>13<br>Response Response 10.0<br>12<br>9.8<br>11 9.6<br>**----- End of picture text -----**<br>


Figure 4.10 Car data: estimates of one-dimensional relationships in MARS model. Other 

the regression function, estimated according to the two variables engine size and curb weight at the same time. 

## _Bibliographical notes_ 

There are very many other aspects concerning spline functions, for which we refer readers to specialized texts. General coverage of splines and their mathematical properties can be found in the works of de Boor (1978) and Atkinson (1989; section 3.7). Green & Silverman (1994) were among the first to use splines and their variations as thin-plate splines in a statistical environment and were responsible for the spread of this tool in the statistical community. MARS was introduced by Friedman (1991) and is found in many works on data mining (e.g., Hastie et al. 2009; section 9.4). GCV was introduced by Craven & Wahba (1978) and extended to MARS by Friedman (1991). 

## 4.5 ADDITIVE MODELS AND GAM 

Up to now, we have examined various methods of nonparametric regression estimation, each of which allows us to examine the relationship between a response 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

90 

**==> picture [236 x 232] intentionally omitted <==**

**----- Start of picture text -----**<br>
25<br>20<br>15<br>10<br>1<br>5<br>2<br>3<br>800<br>1000<br>1200 4<br>1400<br>1600 5<br>1800<br>Curb weight<br>Engine size<br>City distance<br>**----- End of picture text -----**<br>


Figure 4.11 Car data: estimates of double relationship in MARS model. Other variables 

variable _y_ and a certain number _p_ of explanatory variables. All these techniques are valid for the aim, but they also come up against the same problems when _p_ is high: the curse of dimensionality and the other aspects discussed in section 4.2.5. 

To overcome this, on one hand we have to introduce some form of “structure,” that is, a model of the form of regression function _f_ ( _x_ ) _, x_ = ( _x_ 1 _, . . . , xp_ ) ∈ R _[p]_ . On the other hand, for reasons already discussed, we do not want a rigid structure but must maintain ample flexibility. 

One option that has been greatly appreciated for its practical usefulness and logical simplicity is the following. Let us presume that a representation of the type 

**==> picture [248 x 35] intentionally omitted <==**

holds for _f_ ( _x_ ), where _f_ 1 _, . . . , fp_ are functions of one variable, each having smooth behavior, and _β_ 0 is a constant. We say that formulation (4.9) with representation (4.14) of _f_ ( _x_ ) is an _additive model_ . 

Note that to avoid what is essentially a problem of model _identifiability_ , it is necessary for the various _fj_ to be centred around 0, that is, 

**==> picture [154 x 31] intentionally omitted <==**

where _xij_ is the _j_ th variable for unit _i_ . 

Prediction of Quantitative Variables 

91 

**Algorithm 4.1** Backfitting 

**==> picture [208 x 112] intentionally omitted <==**

until functions _f_[ˆ] _j_ stabilize. 

To fit (4.14) to the data, there is an iterative process based on a nonparametric estimation method of one-variable functions to estimate _fj_ . This procedure, shown inalgorithm4.1,iscalled _backfitting_ andisessentiallyavariationoftheGauss-Seidel algorithm. 

The specific method for nonparametric estimation is not crucial, and we can even choose different methods for different _fj_ , but we usually apply a single one, generically indicated by _S_ in algorithm 4.1, in the sense that _S_ ( _y_ ) constitutes the nonparametric estimate, calculated on the observed values _y_ = ( _y_ 1 _, . . . , yn_ )[⊤] , of a scalar function. In many cases, _S_ is a linear estimator, of type _Sy_ , where _S_ is a suitable smoothing matrix. 

A generalization of model (4.14) is of the type 

**==> picture [222 x 78] intentionally omitted <==**

which allows us to bear in mind the _interaction effect_ between pairs of variables, triplets, or other interactions of a higher order. 

Figures 4.12 and 4.13 illustrate how additive models work with reference to the car data, in which the response variable is city distance and the covariates are engine size and curb weight. Figure 4.12 shows the functions indicated in (4.14) by _f_ 1 and _f_ 2, both of which are accompanied by their respective variability bands. Note that the trend of the engine size regression function is noticeably modified when the curb weight component is introduced with respect to similar graphs in figures 4.1, 4.2, and 4.6, which consider engine size alone. 

The left panel of figure 4.13 presents the fitted regression surface under the additive hypothesis, combining the two functions shown in figure 4.12; the right 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

92 

**==> picture [328 x 359] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 2 3 4 5 800 1000 1200 1400 1600 1800<br>Engine size Curb weight<br>Figure 4.12 Car data: estimate of city distance according to engine size and<br>curb weight by an additive model with a spline smoother. by an additive model with a spline smoother.<br>20<br>15<br>15<br>10<br>10<br>1 1<br>2 2<br>5<br>3 3<br>800 800<br>10001200 4 10001200 4<br>1400 1400<br>1600 5 1600 5<br>1800 1800<br>Curb weight Curb weight<br>Engine size Engine size<br>City distance<br>City distance<br>10<br>10<br>5 5<br>0 0<br>s(engine size) s(curb weight)<br>−5 −5<br>**----- End of picture text -----**<br>


Figure 4.12 Car data: estimate of city distance according to engine size and curb weight by an additive model with a spline smoother. by an additive model with a spline smoother. 

Figure 4.13 Car data: estimate of city distance according to engine size and curb weight by an additive model with a spline smoother (left), and without additive hypothesis by local regression (right). 

panel shows the unconstrained estimate, free of the additive hypothesis (see figure 4.4). Comparison between the two plots shows the effect of the additive hypothesis or, rather, the effect of interaction between the variables that cannot be removed from the additive model, which, however, is greatly limited in this example. 

Another direction in which model (4.14) is frequently generalized is of the type 

**==> picture [164 x 34] intentionally omitted <==**

which follows (2.42), and is called _generalized additive model_ (GAM). As in the standard GLM, link function _g_ must be specified. For example, in the case of 

Prediction of Quantitative Variables 

93 

binomial _Y_ , _g_ is commonly assumed to be logit function (2.43). Instead, the term on the right-hand side is now expressed by an additive form, and consequently the contribution of general variable _xj_ is no longer linear _βj xj_ but is of the more general type _fj_ ( _xj_ ). 

To estimate functions for a GAM-type model, we use a suitable combination of algorithm 4.1 with that of iterative weighted least squares, applied in the case of GLM. 

## _Bibliographical notes_ 

For complete coverage of additive models and GAM, see Hastie & Tibshirani (1990) and Hastie et al. (2009; section 9.1). 

## 4.6 PROJECTION PURSUIT 

Additive model (4.14) can also be applied to transformed variables in particular, to projected variables in carefully chosen directions. The model may be written as 

**==> picture [146 x 33] intentionally omitted <==**

and is called the _projection pursuit_ regression model, where _K_ is the number of projections that must be chosen, and _βk_ ∈ R _[p]_ are projection vectors, which must be estimated. Functions _fk_ (·) are called _ridge functions_ , because they are constant in all directions except that defined by vector _βk_ . Note that unlike additive models, number _K_ of ridge functions does not coincide with number _p_ of variables in the model. 

The fitting procedure is based on the least squares criterion, leading to an expression to be minimized by selecting _β_ 1 _, . . . , βK_ and functions _f_ 1 _, . . . , fK_ . The algorithm follows a forward or backward stepwise strategy to select the number of terms _K_ . At each step, it alternates between a Gauss-Newton method to estimate _βk_ , given _fk_ s, and a one-dimensional smoothing regression for the _fk_ , given _βk_ . After each step, the _fk_ s from previous steps can be readjusted by backfitting (algorithm 4.1). In a forward stepwise procedure, the number of terms _K_ is selected by stopping the procedure when the next term does not appreciably improve the model fit, but cross-validation can also be used to choose _K_ . 

The model is very general, and for large enough _K_ and appropriate choice of _fk_ , it can arbitrarily approximate any continuous function of the covariates. A class of models with this property is called a _universal approximator_ . Note that, for example, additive models do not share this property. Projection pursuit regression is also invariant to nonsingular transformations of covariates, but interpretation of results is usually difficult, because each variable enters the model in different projections. 

We illustrate the method by considering the car data, with city distance as the response variable and engine size and curb weight as explanatory variables. We use smoothing splines as smoothing functions and select _K_ = 3. Direction vectors _βk_ are shown in table 4.3 and fitted functions _fk_ are plotted in figure 4.14. The surface of the fitted city distance is shown in figure 4.15. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

94 

_Table 4.3._ CAR DATA: DIRECTION VECTORS FOR THREE-TERM PROJECTION PURSUIT REGRESSION WITH SPLINE SMOOTHER 

||Term 1|Term 2|Term 3|
|---|---|---|---|
|engine size(rescaled)|0_._114|−0_._782|0_._980|
|curb weight(rescaled)|−0_._993|0_._623|−0_._198|



**==> picture [329 x 116] intentionally omitted <==**

**----- Start of picture text -----**<br>
−0.9 −0.8 −0.7 −0.6 −0.5 −0.4 −0.1 0.0 0.1 0.2 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8<br>Term 1 Term 2 Term 3<br>4<br>3<br>2 3<br>2 2<br>0<br>1<br>1<br>0<br>0 −2 −1<br>−1 −4 −2<br>**----- End of picture text -----**<br>


Figure 4.14 Car data: plots of ridge functions for three-term projection pursuit regression with spline smoother. 

## _Bibliographical notes_ 

Projection pursuit was introduced by Friedman & Tukey (1974). A detailed overview is given in Huber (1985), and an introductory account is provided by Hastie et al. (2009; section 11.2). Proof that the projection pursuit model is a universal approximator derives from Kolmogorov’s universal approximation theorem (Kolmogorov 1957) and is discussed, for example, by Jones (1992). 

## 4.7 INFERENTIAL ASPECTS 

The contents of this chapter so far mostly concern nonparametric estimation of a regression, and we have only marginally considered a statistical inference step, which we now examine in greater depth. In particular, we want to introduce a formulation of _analysis of variance_ adapted to the present context to test the hypothesis that a certain covariate does not affect the response variable. 

## 4.7.1 Effective Degrees of Freedom 

Let us refer to the general framework (4.9) and to relative estimator _f_[ˆ] . We consider the problem of establishing whether a certain explanatory variable, let us call it _xr_ , is unnecessary and can be removed from the model. 

The fact that most of the nonparametric methods described so far are linear forms of the response variable (once the smoothing parameter has been fixed) plays an important role. We can therefore write the vector of fitted values ˆ _y_ in the form ˆ _y_ = _S y_ , with _S_ as the _n_ × _n_ smoothing matrix; the corresponding vector of the residuals is given by ˆ _ε_ = ( _In_ − _S_ ) _y_ . 

Prediction of Quantitative Variables 

95 

**==> picture [236 x 233] intentionally omitted <==**

**----- Start of picture text -----**<br>
15<br>10<br>1<br>2<br>3<br>800<br>1000<br>1200 4<br>1400<br>1600 5<br>1800<br>Curb weight<br>Engine size<br>City distance<br>**----- End of picture text -----**<br>


Figure 4.15 Car data: estimate of city distance according to engine size and curb weight through projection pursuit regression with spline smoothers. 

To construct a table of analysis of variance, we must introduce some type of “degrees of freedom,” even approximately, associated with the quadratic forms connected to an estimator. Consider the residual sum of squares 

**==> picture [188 x 24] intentionally omitted <==**

of which we wish to determine the probability distribution and, in particular, calculate the expected value. Hence, we now consider _y_ as a vector sampled from a multivariate random variable _Y_ . 

We take the case of the classic linear model ˆ _ε_ = ( _In_ − _P_ ) _y_ , where _P_ is projection matrix (2.9) and it is known that E{ _Q_ } = _σ_[2] ( _n_ − _p_ ), where _n_ − _p_ are the degrees of freedom of the error component. With the addition of the hypothesis _ε_ ∼ _Nn_ (0 _, σ_[2] _In_ ), we can conclude that _Q_ ∼ _σ_[2] _χn_[2] − _p_[.] 

In our case, the residuals are obtained with a formula similar to that of linear models, apart from the fact that projection matrix _P_ is substituted by smoothing matrix _S_ , which does not enjoy the same formal properties. Consequently, even if we assume the normality of _ε_ , the probability distribution of _Q_ is no longer _χ_[2] . 

However, we have empirical evidence based on simulations indicating that the shape of the probability density for _Q_ is similar to that of _χ_[2] . The problem now is to find an expression that plays the role of degrees of freedom, and this requires determination of an approximation to E{ _Q_ }, in view of the correspondence 

96 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

between the average value and degrees of freedom for a _χ_[2] variable. For this, we write 

**==> picture [252 x 39] intentionally omitted <==**

where _μ_ = E{ _Y_ }, and we used lemma A.2.4. If we introduce the approximations 

**==> picture [218 x 13] intentionally omitted <==**

we can then write 

**==> picture [98 x 13] intentionally omitted <==**

and _n_ − tr( _S_ ) are called _effective_ or _equivalent degrees of freedom_ for the error term; correspondingly, tr( _S_ ) are the effective degrees of freedom for the smoother. 

Because the foregoing expressions are based on approximations, one implication is that we can introduce slightly different expressions for the same degrees of freedom, based on alternative approximations. For example, forms tr( _SS_[⊤] ) or even tr(2 _S_ − _S S_[⊤] ) have been proposed instead of tr( _S_ ). Dealing with approximations among which there is no clear reason to prefer one form over another, we tend to use the simplest form, tr( _S_ ); in any case, the results do not change radically. 

In addition to the role of numerical approximation, it is useful to identify the basic meaning of the idea of effective degrees of freedom. We bear in mind that depending on the choice of smoothing parameter, ˆ _y_ = _S y_ lies between the linear parametric interpolation and a “totally irregular” fit, which presumes no regularity whatsoever for the underlying function _f_ ( _x_ ). Choosing the smoothing parameter, and therefore _S_ , between these two extremes corresponds to a form of “partial regularity” of _f_ ( _x_ ), which is quantified by the degrees of freedom corresponding to the choice of smoothing parameter. In other words, tr( _S_ ) represents the number of effective parameters implied by the model; conversely, _n_ − tr( _S_ ) represents the component of nonregularity and quantifies which fraction of the data is allocated to estimating the error component. 

One role played by effective degrees of freedom is that of introducing a uniformly valid smoothing indicator across different types of smoothers. 

## 4.7.2 Analysis of Variance 

We now return to the question of evaluating the significance of the individual variables that enter model (4.9). 

Like the scheme of analysis of variance for linear models with Gaussian errors, we can establish an extended form of analysis of variance in which total variability is broken down into components that represent the contribution of each covariate. 

We can now reproduce (2.35) using two nonparametric estimates for _y_ ˆ0 and _y_ ˆ, where _y_ ˆ0 represents the restricted model. Recalling the discussion in the last 

Prediction of Quantitative Variables 

97 

subsection, we approximate the distribution of test _F_ with a Snedecor _F_ with (tr( _S_ ) − tr( _S_ 0) _, n_ − tr( _S_ )) degrees of freedom. 

As an illustration, reconsider the car city distance data and examine the effect of engine size and curb weight using local regression, as in section 4.2, with values of 0 _._ 3 and 300 for the smoothing parameters of the two variables, respectively. 

As usual, we summarize the essential ingredients in a _table of analysis of variance_ . 

|Component|Deviance|d.f.|_p_-value|
|---|---|---|---|
|engine size|1169618|12.07|0.000|
|curb weight|729.0|5.40|0.094|
|(engine size,curb weight)|410.2|13.08||



To interpret the elements of this table, we bear in mind that the row headed, for example, curb weight, provides the difference of deviance between the complete model, with both terms, engine size and curb weight, and the restricted model, without the variable curb weight—that is, the row reports the contribution made to lowering the deviance due to the variable curb weight. In the same way, the row shows the effective degrees of freedom for this component — that is, the difference between the degrees of freedom of the complete model and that without the variable curb weight. Last, the _p_ -value is calculated as the complement of the distribution function at the point 

**==> picture [146 x 25] intentionally omitted <==**

of Snedecor’s distribution with 5 _._ 40 and 203 − 13 _._ 08 degrees of freedom, since the sample size is 203. 

The values obtained depend to some extent on the choice of smoothing parameters, for example, _h_ . However, we note empirically that the _p_ -values, and therefore the inferential conclusions, are not heavily influenced if the variation of _h_ occurs within a reasonably chosen area. Consequently, the choice of smoothing parameter is not as critical here as we saw in the estimation problem. 

Clearly, this form of analysis of variance is used in a particularly natural way within the field of additive models, where the idea of the increase in fit made by each variable is implicit, retracing the logic of classical analysis of variance. 

## _Bibliographical notes_ 

Inferential methods in the context of nonparametric regression are discussed in Bowman & Azzalini (1997; ch. 4). For the introduction of effective degrees of freedom and their various definitions, see, for example, Hastie & Tibshirani (1990; pp. 128–129, and appendix B) and Green & Silverman (1994; pp. 37–38). 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

98 

## 4.8 REGRESSION TREES 

## 4.8.1 Approximations via Step Functions 

In one sense, the simplest way to approximate a generic function _y_ = _f_ ( _x_ ), with _x_ ∈ R, is to use a step function, that is, a piecewise constant function (see figure 4.16). 

However, there are various choices to be made: (a) how many subdivisions of the _x_ -axis must be considered? (b) where are the subdivision points to be placed? (c) which value of _y_ must be assigned to each interval? 

Of these questions, the easiest to answer is the last one, because it is completely natural to choose value � _Rj[f]_[ (] _[x]_[) d] _[x][/]_[|] _[R][j]_[|][ for any interval] _[ R][j]_[, having indicated the] length of that interval by | _Rj_ |. Regarding positioning the subdivision points of R, and therefore defining the intervals, it is better to choose small intervals where _f_ ( _x_ ) is steeper. The choice of the number of subdivisions is the most subjective of the three points: intuitively, any increase in the number of steps increases the quality of the approximation, and therefore, in a certain sense, we are led to think of infinite subdivisions. However, this is counter to the requirement to use 

**==> picture [329 x 317] intentionally omitted <==**

**----- Start of picture text -----**<br>
0.5 1.0 1.5 2.0 2.5 3.0 0.5 1.0 1.5 2.0 2.5 3.0<br>x x<br>0.5 1.0 1.5 2.0 2.5 3.0 0.5 1.0 1.5 2.0 2.5 3.0<br>x x<br>0.54 0.54<br>0.52 0.52<br>0.50 0.50<br>f (x) f (x)<br>0.48 0.48<br>0.46 0.46<br>0.44 0.44<br>0.54 0.54<br>0.52 0.52<br>0.50 0.50<br>f (x) f (x)<br>0.48 0.48<br>0.46 0.46<br>0.44 0.44<br>**----- End of picture text -----**<br>


Figure 4.16 A continuous function and some approximations by step functions. 

Prediction of Quantitative Variables 

99 

**==> picture [317 x 144] intentionally omitted <==**

**----- Start of picture text -----**<br>
x1 x1<br>x2 x2<br>y<br>y<br>**----- End of picture text -----**<br>


Figure 4.17 A continuous function in R[2] and an approximation via a step function. 

a “sparing” approximate representation, and therefore to adopt a finite number of subdivisions. 

The scheme can be extended to the case of functions of _p_ variables: we thus write _y_ = _f_ ( _x_ ) where _x_ ∈ R _[p]_ . There are many ways of extending the idea from the _p_ = 1 case to the general _p_ case. Figure 4.17 shows a function in R[2] and its approximation by a step function: the regions with constant values are thus rectangles, the sides of which are parallel to the coordinate axes. 

These characteristics of an approximate function, with some additional specifications to be described later, allow it to be represented as a _binary tree_ , shown in the top panel of figure 4.18; the bottom panel shows the corresponding partition of the domain of function _f_ ( _x_ ) and the values of the approximating function in each rectangle. 

The components of the tree are inequalities, called _nodes_ , relative to any component _x_ of type _x_ 2 _<_ 1 _._ 725. We begin by examining the inequality of the node at the _root of the tree_ , which is at the top. We follow the left branch if the inequality is true and the right branch if it is not. We proceed in the same way, sequentially examining all the inequalities until we reach the terminal nodes, called _leaves_ , which give the values of the approximating function. 

Graphical representation as a tree is not as visually attractive as that of figure 4.17, but it has important advantages: as the tree is identified by a few numerical elements, it can easily be stored. A second important advantage is that we can move from one approximation to a more accurate one by subdividing one of the components into two subrectangles with the same characteristics as the original. This corresponds to extending a branch of the tree to a further branch level. This characteristic immediately allows us to recursively construct a sequence of approximations that are increasingly accurate, each obtained by refining the previous one, as illustrated in the sequence of three step functions in figure 4.16. 

## 4.8.2 Regression Trees: Growth 

We want to use the idea of approximation with a step function to approximate our functions of interest, which are regression functions. Obviously, in our context, 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

100 

**==> picture [215 x 415] intentionally omitted <==**

**----- Start of picture text -----**<br>
x2 < 1.725<br>|<br>x1 < 1.525 x2 < 2.325<br>x1 < 0.925 x2 < 1.125 x1 < 2.275 x1 < 0.475<br>x2 < 0.875 x1 < 2.025 x1 < 2.225<br>0.37 0.34 0.60 0.37 0.22<br>0.64 0.45 0.81 0.95 0.60 0.84<br>0.839 0.598<br>0.954<br>0.597<br>0.810 0.217<br>0.640 0.448<br>0.336<br>0.370<br>0.370<br>0.0 0.5 1.0 1.5 2.0 2.5 3.0<br>x2<br>3.0<br>2.5<br>2.0<br>x1 1.5<br>1.0<br>0.5<br>0.0<br>**----- End of picture text -----**<br>


Figure 4.18 Tree corresponding to approximation of bottom panel of figure 4.17 (top), and partition of domain of _f_ ( _x_ ) induced by tree (bottom). 

regression function _f_ ( _x_ ) is not known, but we can observe it indirectly through _n_ sample observations, generated by model (4.9). 

For simplicity, we begin from the case where _p_ = 1 and consider the data of figure 4.19, which represents the 60 pieces of data already seen in chapter 2, subdivided into two groups: ‘yesterday’ and ‘tomorrow’. Wecanestimate regression curve _f_ ( _x_ ) underlying the data by a step function of the type just described, that is 

**==> picture [216 x 34] intentionally omitted <==**

Prediction of Quantitative Variables 

101 

**==> picture [256 x 251] intentionally omitted <==**

**----- Start of picture text -----**<br>
Yesterday<br>Tomorrow<br>0.5 1.0 1.5 2.0 2.5 3.0<br>x<br>0.54<br>0.52<br>0.50<br>y<br>0.48<br>0.46<br>0.44<br>**----- End of picture text -----**<br>


Figure 4.19 Scatterplot with 60 pairs of values. 

where _c_ 1 _, . . . , cJ_ are constants and _I_ ( _z_ ) is the _indicator function_ 0 − 1 of logical predicate _z_ . In general, sets _R_ 1 _, . . . , RJ_ are rectangles, in the _p_ -dimensional sense, with their edges parallel to the coordinate axes. In the specific case where _p_ = 1, obviously _Rh_ are reduced to line segments. 

We need an objective function to choose _Rh_ and _ch_ . The reference criterion is deviance, but its minimization, even if we fix step number _J_ , involves very complex computation. Therefore, operatively we follow a suboptimal approach of _step-bystep optimization_ , in the sense that we construct a sequence of gradually more refined approximations and to each of these we minimize the deviance relative to the passage from the current approximation to the previous one. 

The algorithm starts by splitting the real line associated with one of the variables, for example, _xj_ , into two parts; which variable is to be considered is discussed later. Each of the subintervals is assigned a value, _ch_ , given by the arithmetic mean of the observed _yi_ having component _xj_ falling in this subinterval, irrespective of the other covariates. Note that this step divides the R _[p]_ space into two regions via a hyperplane parallel to the _j_ th coordinate axis. The subsequent steps of the algorithm proceed similarly, each time splitting one of the existing regions of R _[p]_ into two further regions, again with a split parallel to one of the coordinate axes. 

The right panel of figure 4.18 illustrates the outcome of this process in a simple instance with _p_ = 2. Figure 4.20 shows three instances of portions that are not compatible with the foregoing process; the fourth one is admissible. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

102 

**==> picture [319 x 313] intentionally omitted <==**

Figure 4.20 Three partitions of domain of _f_ ( _x_ ), not consistent with a tree, and one partition induced by a tree (lower right). 

A crucial aspect is the fact that at each step, one of the already constructed rectangles is divided into two, and so is the portion of data belonging to it; we optimize deviance with respect to this operation. Therefore, this is a _myopic optimization_ procedure. Although it does not guarantee global minimization of deviance, it does provide acceptable solutions, maintaining limited _computational complexity_ . 

At least in principle, this procedure can be applied iteratively through successive subdivisions of R _[p]_ until we can no longer distinguish sets containing a single sampled observation and thus obtain a tree with _n_ leaves. To be useful, the number of leaves must be less than _n_ , preferably much less. Therefore, after the stage of _tree growth_ , with the complete or almost complete development of all the leaves, we move to a stage of _tree pruning_ . We describe the growth algorithm now and return to the pruning phase later. 

To develop the growth algorithm, first note that whatever the division of R _[p]_ into hyper-rectangles, we can break down the deviance as follows 

**==> picture [300 x 40] intentionally omitted <==**

Prediction of Quantitative Variables 

103 

We also bear in mind the general property that the minimum of[�] _[n] i_ =1[(] _[z][i]_[−] _[a]_[)][2] with respect to _a_ is obtained for _a_ = _M_ ( _z_ ), where _M_ (·) is the average operator of the vector. 

The growth process starts with _J_ = 1, _RJ_ = R _[p]_ , _D_ =[�] _i_[(] _[y][i]_[−] _[M]_[(] _[y]_[))][2][,][and] proceeds iteratively for a number of cycles, according to the following scheme: 

- once a rectangle _Rh_ is chosen, the appropriate value _ch_ is the average of the corresponding values 

**==> picture [87 x 12] intentionally omitted <==**

- if we subdivide region _Rh_ into two parts, _Rh_[′][and] _[ R] h_[′′][(therefore moving to] _J_ + 1 leaves), summand _Dh_ of _D_ is replaced by 

**==> picture [154 x 29] intentionally omitted <==**

with a “gain” of 

**==> picture [60 x 13] intentionally omitted <==**

- we can inspect all _p_ explanatory variables and, for each of them, all the possible points of subdivision, selecting the variable and its point of subdivision that maximize _gh_ . 

We stop when _J_ = _n_ , at least conceptually. Mainly, if _n_ is enormous, we stop earlier — for example, when all the leaves contain a number of sample elements that is less than a preassigned value, or when the relative fall of deviance is less than a prefixed threshold. 

## 4.8.3 Regression Trees: Pruning 

A large tree with _n_ leaves is conceptually equivalent to interpolation through a polynomial of order _n_ − 1, which passes exactly through all the points; hence, it is not very useful. We have to prune the tree by removing branches of little or no use. 

Let us therefore introduce an objective function that incorporates a penalty for the _cost-complexity_ of the tree which we assess by dimension _J_ . This objective function is given by 

**==> picture [213 x 34] intentionally omitted <==**

where _α_ is a nonnegative penalty parameter. Breiman et al. (1984) showed that the set of rooted subtrees that minimize the cost-complexity measure is nested. That is, as we increase _α_ we can find the optimal trees by a sequences of pruning operations on the current tree. So for each _α_ , there is a unique smallest tree minimizing _Cα_ ( _J_ ) (Breiman et al. 1984; proposition 3.7) and we select the tree that minimizes _Cα_ ( _J_ ) for a fixed _α_ . 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

104 

To minimize (4.17), we proceed by sequentially eliminating one leaf at a time. At each step, we select the leaf for which elimination causes the smallest increase in � _h[D][h]_[. The question is therefore reduced to choosing] _[ α]_[, and for this we can use] one of the methods described in section 3.5. We can show that suitable adaptation ˆ ˆ of the AIC gives _α_ = 2 _σ_[2] , where _σ_[2] is the estimate of residual error variance, but how this can be estimated reliably is not very clear. However, the widespread opinion is that AIC tends to overfit the data in this area. Therefore, the methods of cross-validation and simple subdivision of data into a training set and a test set, as seen in sections 3.5.1–3.5.2, are more widely used. 

Predicting _f_ ( _x_ ) on a new piece of data _x_ 0 is done by allowing the observation to descend from the root of the available tree. Datum _x_ 0 follows one of the branches, according to the components of _x_ 0, which describe it, until it reaches a leaf with a value of _f_[ˆ] ( _x_ 0). We repeat this process for the _n_[′] components of the test set, ( _xi, yi_ ) for _i_ = 1 _, . . . , n_[′] . Comparing _f_[ˆ] ( _xi_ ) with observed class _yi_ , we compute the contribution from the _i_ th unit to deviance (4.16), and the sum over the _n_[′] terms provides the observed value of the deviance. 

For illustration, let us consider the data in figure 4.19, using the subgroups of yesterday’s data for growth and tomorrow’s data for pruning. The tree developed to fullness using only yesterday’s data is shown in the first panel of figure 4.21, where the length of the vertical lines is proportional to the reduction of the deviance obtained by subdividing the node. Clearly, after some ramifications, there is no substantial gain due to the lower branches. 

The top-right panel represents function[�] _h[D][h]_[calculated][from][tomorrow’s] data. The graph indicates choice _J_ = 4, associated with _α_ = 4 _._ 33 × 10[−][4] . The suitably pruned tree appears in the lower-left panel, and function _f_[ˆ] ( _x_ ) is found lower-right, overlapping the points. 

In this case, the small sample size allows us to use cross-validation. 

Note that pruning is often very radical and can easily lead to a tree with a small number of nodes with respect to the numbers of variables and their levels, if they are categorical. This fact automatically leads to a choice of the useful variables, regarding the variables that remain excluded. In reverse, it is not easy to rank importance for those that remain in the tree, as the reduction in deviance associated with each node is not directly interpretable. This difficulty is due to at least three aspects: (a) the reduction of the deviance due to the node quantifies the gain of that particular dichotomization of the variable and not the whole variable; (b) the logic of myopic optimization used to make the tree grow makes it difficult to attribute global significance a posteriori to local aspects and (c) each variable may be included in more than one node. 

To overcome these problems, specific measures of the relative importance of each covariate in predicting the response have been proposed. For example, a simple measure of the contribution of a variable, like _xk_ , is based on improvements _gh_ in lowering the deviance at each step, involving _xk_ as splitting variable. The sum of squared _gh_[2][over][all][the][internal][nodes][for][which] _[x][k]_[was][chosen] as splitting variable is a squared relative measure of the importance of that variable. 

Prediction of Quantitative Variables 

**==> picture [333 x 353] intentionally omitted <==**

**----- Start of picture text -----**<br>
Quantitative 105<br>8.1e−03 4.3e−04 2.1e−05 −Inf<br>|<br>5 10 15<br>Size<br>x0 < 0.543103|<br>x0 < 1.57759<br>0.4270<br>x0 < 0.715517<br>0.5097<br>Yesterday<br>Tomorrow<br>0.4900 0.5395<br>0.5 1.0 1.5 2.0 2.5 3.0<br>x<br>0.014<br>0.012<br>Deviance 0.010<br>0.008<br>0.006<br>0.54<br>0.52<br>0.50<br>y<br>0.48<br>0.46<br>0.44<br>**----- End of picture text -----**<br>


Figure 4.21 For data of figure 4.19, top-left panel displays a nearly fully grown tree. Top-right panel: deviance function from tomorrow’s data, which selects four-node tree in lower-left panel. Lower-right panel: data with overlapping selected four-level function. 

## 4.8.4 Discussion 

Because trees are very frequently used in practice, we note their advantages and disadvantages. 

## _Advantages_ 

- Logical simplicity and ease of “communication,” above all with those who have a nonquantitative background. Trees are logical structures usually used by many people in decision-making processes, for example, by physicians and businesspeople, perhaps not consciously. 

- The step function has a simple, compact mathematical formulation in terms of information to be stored. 

- Speed of computation: the process is not very taxing from this point of view, and it can also take advantage of the potential of _parallel calculation_ . 

106 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

- Use of discrete and categorical variables: although the previous description referred to continuous covariates, there is no specific reason to limit oneself to them, and the method can proceed in the same way if some of the variables are discrete or qualitative. 

- Robust forms of deviance: clearly, having seen the construction, we immediately can substitute deviance with another criterion and the average with the corresponding operator, thus allowing the use of criteria based on robustness considerations. 

- Missing data: not particularly complicated variations can be introduced, which allow for missing values, in both tree construction and prediction. 

- Variable selection: the method automatically selects the important variables. 

## _Disadvantages_ 

- Instability of results: a tree is often very sensitive to the insertion of new data or changes in existing data. 

- Difficulty in upgrading: if more data arrive, they cannot be added to the already constructed tree; it is necessary to start again from the beginning. 

- Difficulty of approximating some mathematically simple functions, particularly if they are steep, and a straight line or other simple function would approximate them very well. 

- Statistical inference: formal procedures of statistical inference such as hypothesis testing, confidence intervals, and others are not available. 

- Selection of variables: it is not simple to evaluate the order of importance of variables remaining in the pruned tree. 

## _Bibliographical notes_ 

Breiman et al. (1984) introduced not only the idea of regression trees and classification trees (see later discussion) but also the acronym CART, which then became synonymous with the same method. This work was among the first to promote a particular philosophy of data analysis and examine issues that later to became the characteristic elements of data mining. Venables & Ripley (2002) describe the practical usage of trees. 

## 4.9 NEURAL NETWORKS 

The term _neural network_ encompasses a wide family of techniques developed in _machine learning_ . We describe only the simplest version here. 

Figure 4.22 shows _p_ explanatory variables ( _input_ ) in a relationship with _q_ response variables, or _output_ . The most characteristic aspect is the _layer_ of _r latent variables_ , which is not observable (hidden) and comes between the two previous groups in the sense that the covariates influence the latent variables; these in turn influence the response variables. The number of _input_ and _output_ variables is determined by the problem, but the number _r_ of latent variables is something we can choose, because they are only conceptual entities. In figure 4.22, we have _p_ = 4, _r_ = 3, and _q_ = 2, and some additional “constant variables,” identical to 1, are also shown. 

Prediction of Quantitative Variables 

107 

**==> picture [252 x 251] intentionally omitted <==**

**----- Start of picture text -----**<br>
+1<br>+1<br>X1<br>Z1<br>Y1<br>X2<br>Z2<br>X3 Y2<br>Z3<br>X4<br>Input Hidden Output<br>variables  layer variables<br>**----- End of picture text -----**<br>


Figure 4.22 A simple neural network. 

The term _neural network_ originated as a mathematical model that in the past was believed to be the mechanism controlling the working of the animal brain: every node of the graph represented a neuron, and the arcs represented the synapses. We now know that the animal brain is much more complex, but the term _neural network_ survives. 

A neural network is essentially a two-stage regression scheme, generally of nonlinear or at least partially nonlinear type. We indicate the generic _input_ , latent, and _output_ variables by _xh_ , _zj_ , and _yk_ , respectively, and add constant variables _x_ 0 and _z_ 0 equal to 1. The previous scheme can now be expressed as 

**==> picture [271 x 39] intentionally omitted <==**

where _αhj_ and _βjk_ are parameters to be estimated, and the sums are over the indices of the variables for which a dependence relation is predicted. Figure 4.22 shows these dependencies by arrows and involves all the compatible variables, although this is not necessarily the case. We can therefore see that the resulting structure is an acyclic _graph_ with directed edges and _weights_ associated with coefficients _α_ and _β_ . 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

108 

To complete the picture, we must specify _activation functions f_ 0 and _f_ 1. In regression problems, where the _yk_ are generally nonlimited, we presume 

**==> picture [233 x 25] intentionally omitted <==**

where the choice of _f_ 0 is the logistic function, as seen in section 2.4. We note, however, that at least one of the two functions _f_ 0 and _f_ 1 must be nonlinear to avoid reducing the whole network to a set of linear relations, effectively eliminating the latent layer. 

There are mathematical results that give rise to interesting properties for the framework. In particular, we can show that a neural network with linear _output_ units can approximate any continuous function _f_ uniformly on compact sets, by appropriately increasing the number of units of the latent layer; see Ripley (1996; p. 147 and 174). 

Extensions are possible in various directions. One of the most common is to consider several layers of latent variables. Another is to introduce edges that skip a layer: in the case of the single latent layer considered here, this means inserting an edge directly between some variables of the _input_ layer and some of the _output_ . Two elements must be specified: the number _r_ of units in the hidden layer and the set of coefficients _α_ and _β_ of (4.18). For the choice of _r_ , there are no criteria that are easy to use in practice, apart from experimenting with various ones and comparing the results. 

Therefore assume that _r_ has been fixed and we want to estimate coefficients _α_ and _β_ according to sample observations. This is done by minimizing the usual objective function 

**==> picture [95 x 25] intentionally omitted <==**

where _yi_ now indicates the _q_ -dimensional vector of the response variables of the _i_ th observation. Analogously, _xi_ is the corresponding _p_ -dimensional vector of the covariates, and _f_ ( _x_ ) is the vector, whose _k_ th component is 

**==> picture [256 x 40] intentionally omitted <==**

More elaborate versions of this objective function can be obtained by including a penalty term to avoid overfitting problems, for example, functions of the type 

**==> picture [210 x 12] intentionally omitted <==**

Here _λ_ is a positive tuning parameter and _J_ ( _α, β_ ) is a penalty function, according to a path already seen previously, for example in section 4.4.3. Among the most common penalty forms there are 

**==> picture [330 x 45] intentionally omitted <==**

Prediction of Quantitative Variables 

109 

of which the first form penalizes the amplitude of the second derivative, and the second tends to shrink the parameters toward 0; the latter is called _weight decay_ . Here _yki_ denotes the _k_ th component of _yi_ . 

These formulations, both _D_ and penalty function _J_ , make sense if the variables are measured on the same scale. As a preliminary operation, it is therefore better to normalize them—for example, by rescaling all the variables between 0 and 1 (at least approximately). For regulation parameter _λ_ , Venables & Ripley (2002; p. 339) advise choosing a value between 10[−][4] and 10[−][2] . 

Clearly, minimization of _D_ 0 requires a numerical optimization process. Much effort has been invested in developing such algorithms. The most common method is called _back-propagation_ , which has interesting properties. One of the most important aspects in this context is that there exists a variant of the back-propagation algorithm, which allows for later updating of parameter estimates in an incremental way as new data become available. 

It must be stressed that practical experience has provided extensive evidence that objective function _D_ 0 often has many points of local minima, and it is therefore wise to start the optimization algorithm from several initial points. This difficulty in turn affects something else: in choosing _λ_ it is difficult to take advantage of techniques like cross-validation, as the algorithm varies widely in locating the minimum. 

To illustrate the method, let us consider the engine size and curb weight from our car data to predict city distance. We consider a neural network with _f_ 0 and _f_ 1 as in (4.19) and one latent layer with _r_ = 3 nodes. We minimize function _D_ 0 with penalty _J_ ( _α, β_ ) in the second form, and _λ_ = 10[−][3] . After various executions of the minimization algorithm, starting from different initial points of the parameters, we reach what would seem to be an acceptable minimum point. The results are shown in figure 4.23, in which the top diagram is a graph of the neural network with estimated weights and the lower one is a prospective representation of _f_ ( _x_ ). 

In conclusion, we review of the advantages and disadvantages of this approach. 

## _Advantages_ 

- Flexibility: the method allows for good approximation of practically any regression function _f_ ( _x_ ), that is, the model is a _universal approximator_ . 

- Compactness of representation: the estimated regression function is identified by a limited number of components. 

- Sequential upgrading: coefficients _α_ and _β_ can be updated sequentially as new data arrive by means of a suitable variation of the back-propagation algorithm. 

## _Disadvantages_ 

- Arbitrariness: there are no strong criteria with which to choose the number _r_ of latent nodes; in addition, we only have rough indications for the choice of _λ_ . 

- Instability in the estimation stage: the nature of objective function _D_ , or its variations, implies that its properties are difficult to identify, especially the existence of a single minimum point. Instead, there is empirical evidence 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

110 

**==> picture [325 x 453] intentionally omitted <==**

**----- Start of picture text -----**<br>
+1 +1<br>1.21<br>0.64<br>Z1<br>0.52 3.68<br>Engine size<br>–2.02 1.59<br>–5.6 –4.01 City<br>Z2 distance<br>–4.9<br>Curb weight –1.08 2.3 1.97<br>1.22<br>Z3<br>Input Hidden Output<br>variables  layer variables<br>0.8<br>0.6<br>0.4<br>1<br>2<br>3<br>800<br>1000<br>1200 4<br>1400<br>1600 5<br>1800<br>Curb weight<br>Engine size<br>City distance<br>**----- End of picture text -----**<br>


Figure 4.23 Car data. Top: neural network 2–3–1 with engine size and curb weight to predict city distance, bottom: surface of estimated function. 

of the frequent presence of local minima, and different results may be obtained if the optimization algorithm is started from different points. 

- Inference: there are no standard errors associated with the coefficients or other inferential procedures—for example, to reduce the number of 

Prediction of Quantitative Variables 

111 

- Interpretation: there are major problems in interpreting results, particularly when _r_ increases. 

## _Bibliographical notes_ 

The literature on neural networks is extremely ample, and ranges from very technical presentations to very informal ones. Among the latter, from the viewpoint of readers with a statistical background, we mention the works by Ripley (1996; ch. 5) and Hastie et al. (2009; ch. 11). Fine (1999) provides a more mathematical account. 

## 4.10 CASE STUDIES 

The data used up to now to illustrate the various methods, although obtained from real cases, were suitably simplified to avoid over-specific details in applied problems that interfere with presentation. Here we focus on operational aspects and treat a couple of real cases in their original complexity. 

## 4.10.1 

The first problem presented here was handled by a group of marketing analysts in a telecommunications company. Our aim is not to analyze the associated marketing themes in detail but to present the use of data mining methods as a tool for business choices. 

## _The data and the background problem_ 

The group within the marketing section of a telecommunications company managing customer relationships ( _customer base management_ ) is interested in analyzing customer behavior regarding telephone traffic. Of the many types of analysis the group uses to study customer traffic characteristics, identifying a tool to predict the traffic of every single customer in the coming months is often extremely useful. Not only can appropriate estimations of overall traffic provide necessary elements for predicting the company’s budget, but tools can be supplied to evaluate each client’s _value_ to the company. Marketing actions can be organized to incentivize the use of company services to those whose traffic could potentially increase and to avoid doing the same to those who do not need them. Traffic predictions are also used to note possibly anomalous behavior by customers, particularly those who are more valuable to the company, for early identification of possible dissatisfaction, problems in using the main services the company offers, or even fraudulent situations. 

In this context, let us consider a set of customers who possess a SIM (subscriber identity module) card with a call plan that is of particular interest to the company. We tackle the problem of predicting traffic for the coming month using data available so far. Therefore, as response variable, we choose the total number of seconds of outgoing calls made in a given month. 

A typical way of proceeding in these cases is based on the idea that in essence, customers’ traffic behavior can be considered as stable in time if reduced time intervals are considered. Under such a hypothesis, traffic in month _t_ using data for months _t_ − 1 _, t_ − 2 _, . . . , t_ − _k_ , can be predicted as a first approximation, 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

112 

irrespective of specific month _t_ . Therefore, in the first search we do not keep count of seasonal components or cycles in the model, but, following common usage in this field, we consider a model constructed with data for month _t_ as a good prediction tool for each successive month. 

The approximation thus introduced may seem excessive, and it is in fact possible to consider components that gather effects due to the specific months in constructing the model itself. Or, in contexts in which prediction models are often updated, we can validate the model on the basis of test sets extracted from data that refer to _t_ months differing from those used for the estimate. For the sake of simplicity, we concentrate only on the stable hypothesis. 

We must now choose our covariates. First, we determine for how many months it would be useful and suitable to “go backwards” in time to continue to find meaningful relationships with the response variable and then identify the variables to be observed for each customer. Some of these are observed for all months, for example, the number of text messages (SMS) sent or the number of calls to the customer services helpline ( _customer care_ ), but others do not depend on the time interval in question, for example, gender or the day of activation of the service. The company’s DWH (see section 1.1.3) yields a data mart for 30,619 customers, for whom information on a total of 99 variables is available. Some of these are intrinsic customer characteristics (e.g., gender and age) or have to do with the specific relationship between customer and company (e.g., activation data or any value-added services), and some have to do with information on traffic in each of the consecutive nine months previous to the month of interest. Last, there is the variable relative to the total duration of outgoing calls in the tenth month, which is our response variable. The data are presented in greater detail in section B.4. 

The high number of customers allows us to divide the data set into two parts, one for the estimate and the other for validation of results and comparisons. We subdivide the available data into two equal sets, composed of 15,310 and 15,309 customers, respectively. 

We now examine the training set. An initial descriptive graphical analysis shows that the distribution of the response variable is highly asymmetric and concentrated around 0. In particular, the training set contains 5,131 customers who have not made outgoing calls. This data characteristic involves some difficulty in automatically using the models proposed here. Clearly, the response variable cannot be treated as a continuous variable, because it has the characteristics of a mixed variable: it is the combination of a continuous component for some of the observations and a discrete, binary component for the other group of customers who did not make calls in that month. 

It is therefore reasonable to take advantage of this information to construct our prediction model of the duration of outgoing calls. One possibility is to organize the process into two stages. First, we fit a model for the probability that the duration is not 0, and, conditionally on this event, we then construct a model for positive duration values. 

To construct a model that predicts an indicator variable, we still need to introduce more elements (see chapter 5 for the analysis of this aspect). In the 

Prediction of Quantitative Variables 

113 

**==> picture [330 x 166] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 1000 2000 3000 4000 5000 6000 −20000 −10000 0 10000 20000<br>Minutes Residuals<br>0.0015<br>4e−04<br>3e−04<br>0.0010<br>Density Density 2e−04<br>0.0005<br>1e−04<br>0.0000 0e+00<br>**----- End of picture text -----**<br>


Figure 4.24 Telecommunications customers. Left: distributions of outgoing call duration for month of interest; right: residuals of stepwise linear model with density of Gaussian distribution of average 0 and variance equal to variance of residuals. 

next section, we describe some models to predict the total duration of calls on condition that they were made. 

## _Some prediction models_ 

We now consider, among the customers selected for the estimate, the set containing the 10,179 customers who had positive total call durations in the month of interest. The left part of figure 4.24 is a histogram of the response variable for this set. 

Thefirstpredictionmethodisalinearmodelobtainedwithallavailablevariables. The fitted model with 98 covariates gives _R_[2] = 0 _._ 613. Clearly the estimate of many parameters indicates that the variables in question do not significantly influence the response variable. Therefore, a _stepwise_ procedure is formulated to select the relevant variables. After much computer work, the final model contains 56 covariates and gives _R_[2] = 0 _._ 612. Note that in situations like these, in which we have an extremely high number of observations, it is not useful to carry out formal hypothesis testing with test _F_ to verify the combined influence of all the eliminated variables on the response variable. 

The histogram of the residuals of the model with 56 variables appears in the right part of figure 4.24. The quantities, obtained by estimating the parameters in R, are listed below: 

## Residuals: 

|Residuals:||||||
|---|---|---|---|---|---|
|Min|1Q|Median|3Q|Max||
|-69152.5<br>-790.7||66.8|663.4 148323.2|||
|Coefficients:||||||
|||Estimate|Std. Error|t value|Pr(>|t|)|
|(Intercept)||4.04e+03|2.97e+02|13.64|< 2e-16 ***|
|tariff.plan4||1.50e+04|4.92e+02|30.57|< 2e-16 ***|



## D A T A A N A L Y S I S A N D D A T A M I N I N G 

|114||D|A T A A N A L|S I S A N D D A T A|
|---|---|---|---|---|
|tariff.plan6|-3.78e+03|2.52e+02|-15.00|< 2e-16 ***|
|tariff.plan7|-4.02e+03|1.99e+02|-20.24|< 2e-16 ***|
|tariff.plan8|-3.78e+03|1.97e+02|-19.21|< 2e-16 ***|
|etacl|-2.92e+01|6.24e+00|-4.68|2.9e-06 ***|
|activ.zone2|-4.64e+01|1.24e+02|-0.37|0.70829|
|activ.zone3|4.87e+02|1.32e+02|3.70|0.00022 ***|
|activ.zone4|-2.87e+01|1.92e+02|-0.15|0.88146|
|vas1Y|3.93e+02|1.13e+02|3.46|0.00053 ***|
|q01.out.ch.peak|-4.26e+00|1.58e+00|-2.70|0.00698 **|
|q01.out.dur.peak|3.01e-02|1.26e-02|2.40|0.01635 *|
|q01.out.ch.offpeak|1.67e+01|5.91e+00|2.82|0.00481 **|
|q01.out.dur.offpeak|1.92e-01|4.45e-02|4.31|1.7e-05 ***|
|q01.out.val.offpeak|-6.45e+01|1.30e+01|-4.98|6.4e-07 ***|
|q01.in.ch.tot|3.85e+00|1.33e+00|2.90|0.00370 **|
|q01.ch.cc|-6.54e+01|4.16e+01|-1.57|0.11609|
|q02.out.dur.peak|-4.37e-02|2.04e-02|-2.15|0.03180 *|
|q02.out.val.peak|1.81e+01|4.47e+00|4.05|5.1e-05 ***|
|q02.out.ch.offpeak|1.11e+01|6.85e+00|1.62|0.10539|
|q02.out.dur.offpeak|-2.13e-01|4.24e-02|-5.03|5.1e-07 ***|
|q02.out.val.offpeak|-1.28e+01|6.91e+00|-1.85|0.06398 .|
|q02.in.ch.tot|-3.82e+00|1.37e+00|-2.79|0.00525 **|
|q02.ch.cc|-1.08e+02|4.03e+01|-2.68|0.00736 **|
|q03.out.val.peak|4.94e+00|1.62e+00|3.05|0.00232 **|
|q03.out.dur.offpeak|1.20e-01|3.70e-02|3.25|0.00115 **|
|q03.out.val.offpeak|2.03e+01|8.81e+00|2.30|0.02129 *|
|q03.in.dur.tot|-3.06e-02|8.19e-03|-3.73|0.00019 ***|
|q04.out.ch.peak|-3.59e+00|1.27e+00|-2.82|0.00485 **|
|q04.out.dur.peak|-3.62e-02|1.90e-02|-1.90|0.05713 .|
|q04.out.val.peak|1.19e+01|4.29e+00|2.77|0.00568 **|
|q04.out.ch.offpeak|-3.71e+01|5.00e+00|-7.42|1.3e-13 ***|
|q04.in.dur.tot|2.60e-02|9.58e-03|2.71|0.00678 **|
|q05.out.dur.peak|5.44e-02|1.66e-02|3.27|0.00108 **|
|q05.out.val.peak|-1.46e+01|3.37e+00|-4.34|1.4e-05 ***|
|q05.out.ch.offpeak|3.35e+01|6.69e+00|5.00|5.9e-07 ***|
|q05.out.val.offpeak|1.46e+01|9.44e+00|1.55|0.12220|
|q05.ch.cc|6.74e+01|3.93e+01|1.72|0.08637 .|
|q06.out.dur.peak|-4.48e-02|1.77e-02|-2.53|0.01134 *|
|q06.out.val.peak|1.14e+01|3.88e+00|2.93|0.00342 **|
|q06.out.ch.offpeak|-5.43e+01|8.54e+00|-6.35|2.2e-10 ***|
|q06.out.dur.offpeak|-1.11e-01|7.23e-02|-1.54|0.12357|
|q06.out.val.offpeak|2.04e+02|2.61e+01|7.82|5.8e-15 ***|
|q06.in.dur.tot|1.59e-02|9.45e-03|1.68|0.09219 .|
|q06.ch.sms|-4.29e+00|1.86e+00|-2.30|0.02139 *|
|q07.out.dur.peak|-3.59e-02|1.37e-02|-2.62|0.00893 **|
|q07.out.val.peak|1.26e+01|3.06e+00|4.12|3.8e-05 ***|
|q07.out.ch.offpeak|-2.34e+01|8.74e+00|-2.68|0.00728 **|
|q07.out.dur.offpeak|-1.12e-01|7.72e-02|-1.45|0.14819|
|q07.out.val.offpeak|4.01e+01|2.66e+01|1.51|0.13233|
|q07.in.dur.tot|-1.86e-02|9.48e-03|-1.96|0.04975 *|
|q07.ch.cc|-3.23e+01|1.84e+01|-1.76|0.07900 .|
|q08.out.ch.peak|-2.71e+00|1.34e+00|-2.03|0.04280 *|
|q08.out.dur.peak|4.69e-02|1.36e-02|3.46|0.00055 ***|
|q08.out.val.peak|-1.37e+01|3.11e+00|-4.41|1.1e-05 ***|



Prediction of Quantitative Variables 

115 

q08.out.ch.offpeak -2.18e+01 9.03e+00 -2.42 0.01569 * q08.out.dur.offpeak 2.48e-01 6.35e-02 3.90 9.5e-05 *** q08.in.ch.tot 3.43e+00 1.19e+00 2.89 0.00389 ** q09.out.val.peak 1.34e+01 9.95e-01 13.51 < 2e-16 *** q09.out.ch.offpeak 1.27e+02 8.67e+00 14.63 < 2e-16 *** q09.out.dur.offpeak 1.47e+00 6.31e-02 23.35 < 2e-16 *** q09.out.val.offpeak -1.99e+02 1.88e+01 -10.53 < 2e-16 *** --Signif. codes: 0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1 

Residual standard error: 5020 on 10117 degrees of freedom Multiple R-Squared: 0.612, Adjusted R-squared: 0.61 F-statistic: 262 on 61 and 10117 DF, p-value: <2e-16 

Did you stop to look at the individual numbers in the list? They seem to be useless and too many. In fact, they contain much useful information for analysts looking for reasons customers increase their traffic. So if we analyze the parameter values in more detail, we see that they offer interesting suggestions for marketing choices. 

Let us make a single example of simple interpretation: the high value of the parameter of the first value-added service (vas1) tells us that, taking into account the linear effect of all the other variables in the model, subscription to such a service is a strong incentive to use the phone. This result may give rise to marketing choices aimed at increasing the use of this value-added service— for example, a targeted marketing campaign or sending personalized letters presenting the service to customers who have not yet subscribed to it. 

However, predictions obtained by applying this model to new data may also give rise to negative values for total call duration. To avoid this annoying problem, the prediction for all these customers to whom the model would assign negative duration at 0.5 was fixed. The choice of 0.5 is reasonable here because it is lower than any other value in the training set for total call duration, but it is not too small to have any great influence on the results of the following analysis. 

To evaluate the quality of these two prediction models more completely, we measure performance on the test set. The resulting squared prediction errors are 257 _._ 74 × 10[9] and 258 _._ 52 × 10[9] for the complete and restricted models, respectively. 

The models minimize objective function (2.3), which assigns the same importance to each observed entity. However, as we note that total monthly call duration (the variable we are predicting) is certainly a positive quantity and we expect that it frequently has low or medium values and only rarely high ones, we also expect that it will have a skew shape. This consideration, also corroborated by the right panel of figure 4.24, which clearly shows that the residuals of the linear model do not have Gaussian distribution, leads us to consider different objective functions for estimate evaluation. 

A simple, widespread choice in these cases is to consider as new output the logarithmic transform of the response variable, leading to a deviance on the 

116 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

logarithmic scale: 

**==> picture [236 x 24] intentionally omitted <==**

where, as usual, _yi_ indicates the response variable observations, _xi_ the corresponding covariate observations, _β_ the vector of the unknown parameters to be estimated, and _f_ the function identified by the model. 

To evaluate these two linear models in terms of this new loss function, we can calculate the prediction error on a logarithmic scale on the test set, calculating the function 

**==> picture [124 x 25] intentionally omitted <==**

where _g_ is the linear predictor on the original scale. On the logarithmic scale, deviance is 113,472 for the complete model and 112,061 for the restricted one, respectively, confirming that the model with fewer covariates produces a slightly better prediction. 

The linear model can also be directly fitted so as to minimize (4.22). This time, too, we fit the model with all the covariates to the data and then select the most important ones with a stepwise procedure. The prediction errors on the validation set of all the models fitted using the original and logarithmic scales are listed in table 4.5. 

In figure 4.25, the left panel shows the histogram of the logarithm of the outgoing call duration in the month of interest; the right panel shows the histogram of the model residuals on the logarithmic scale obtained by stepwise selection of the variables. These histograms support the hypothesis that the loss function on the logarithmic scale is a reasonable choice for the problem in question. 

**==> picture [329 x 166] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 2 4 6 8 10 12 −6 −4 −2 0 2 4 6<br>Log (minutes) Residuals<br>0.4 0.4<br>0.3 0.3<br>0.2 0.2<br>Density Density<br>0.1 0.1<br>0.0 0.0<br>**----- End of picture text -----**<br>


Figure 4.25 Telecommunications customers. Left: distribution of logarithms of outgoing call duration for month of interest; right: histogram of residuals of linear model on logarithmic scale with stepwise selection of variables with Gaussian distribution density (average 0 and variance equal to variance of residuals). 

Prediction of Quantitative Variables 

117 

A second group of models fitted to these data is based on GAM models (see section 4.5). In this case, a first model with all available variables was fitted and then a second, with only the variables resulting significant in the first model, determined through analysis of variance (section 4.7.2). A GAM model was also fitted, with only those variables for the last observed month, as well as customer characteristics, which do not vary in time. Also in this case, to estimate the functions of the additive models, both logarithmic and original scales were used. Table 4.5 lists the prediction errors of the six additive models obtained by selecting the covariates (all of them, only significant ones, only those relative to the last month) and using the two estimation criteria (original and logarithmic scales). 

For all continuous variables, smoothing splines (see section 4.4.3) were used as nonparametric estimators, and the number of effective degrees of freedom was fixed at 4 for each univariate function as a choice of spline smoothing parameter. The estimates of the functions of variables significant for the model on the logarithmic scale are shown in figure 4.26. 

Looking at all the coefficients of the linear model may give rise to feelings of confusion or uselessness. However, also in this case, each figure may have useful consequences for company policy. Simple examples are that value-added services (vas1 and vas2) cause an increase in net traffic, other estimated elements being fixed. Regarding traffic variables, note the narrowness of the variability bands of the function for off-peak call duration in the ninth month, identified as a very important predictor for increased traffic in the tenth month, and the nonmonotone trend of the curve for the same variable in the sixth month. 

The other family of models based on splines used here is MARS (see section 4.4.5). In this case, because the procedure automatically chooses variables useful for predictions, one model was used for the original scale and one for the logarithmic scale. Table 4.4 lists the information used by the final model on the original scale. The prediction errors of these models are also listed in table 4.5 to aid comparison with other predictions. 

A neural network (see section 4.9) was also fitted on both original and logarithmic scales. Three nodes were used for the hidden layer and to control overfitting. We selected _λ_ = 10[−][3] as the _weight decay_ parameter. Prediction errors are listed in table 4.5. 

Last, two regression trees (see section 4.8) were “grown” on the two scales. The trees, like MARS, automatically select the variables that most influence the response variable, taking advantage of pruning phases; it is not necessary here to carry out any preliminary operations to reduce the models. The training set was divided into two parts: one of 5,089 customers, used to grow the tree, and the other of 5,090 customers, for pruning. Figure 4.27 shows the deviance plot versus number of tree nodes for the two models on the original and logarithmic scales, respectively, and figure 4.28 shows the two final trees. 

For the first tree, the function that describes deviance with respect to number of nodes (top panel, figure 4.27) shows two local minima, and the absolute minimum attained with deviance on the pruning set of 119 _._ 52 × 10[9] refers to the tree with 44 leaves, which is obviously a tree with many branches. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

118 

**==> picture [315 x 430] intentionally omitted <==**

**----- Start of picture text -----**<br>
3 7 8 1 2 3 4 PO CC DD 2 5 6 N Y N Y<br>tariff.plan activ.zone payment.method activ.chan vas1 vas2<br>0 40000 80000 0 50 150 250 0 100000 250000 0 200 400 0 100 300 0 40000 100000<br>q01.out.dur.offpeak q01.out.val.offpeak q01.in.dur.tot q02.out.val.offpeak q03.out.ch.offpeak q03.out.dur.offpeak<br>0 200 400 600 0 50 150 250 0 500 1500 0 400 800 1200 0 100 300 0 20000 50000<br>q03.out.val.offpeak q04.out.val.offpeak q06.out.ch.peak q06.out.val.peak q06.out.ch.offpeak q06.out.dur.offpeak<br>0 50 150 250 0 500 1500 0 100000 250000 0 400 800 1200 0 100 300 0 20000 50000<br>q06.out.val.offpeak q07.out.ch.peak q07.out.dur.peak q07.out.val.peak q07.out.ch.offpeak q07.out.dur.offpeak<br>0 50 150 250 0 50000 150000 0 500 1000 0 400 800 0 100 300 500 0 20000 50000<br>q07.out.val.offpeak q07.in.dur.tot q08.out.ch.peak q08.out.val.peak q08.out.ch.offpeak q08.out.dur.offpeak<br>0 100 200 300 0 400 800 1200 0 500 1500 0 100000 250000 0 400 800 0 100 200 300<br>q08.out.val.offpeak q08.in.ch.tot q09.out.ch.peak q09.out.dur.peak q09.out.val.peak q09.out.ch.offpeak<br>0 20000 50000 0 100 200 300 0 40000 100000 20 30 40 50<br>q09.out.dur.offpeak q09.out.val.offpeak q09.in.dur.tot age<br>1.5 0.00 0.05 0.2 0.08 0.20<br>0.5 −0.2 0.02 0.10<br>−0.5 −0.10 −0.05 −0.6 −0.04 0.00<br>1 1 2 3<br>10 0−1 0−1 10 1.00.0 210<br>−1 −2 −1<br>−2 −3 −3 −2 −1.0 −2<br>20 0−1−2 1.00.0 1.50.5 10−1 10−1<br>−2 −3 −0.5 −2<br>−4 −4 −1.0 −1.5 −3<br>420 0.5−0.5 1.00.0 321 10−1 43215<br>−2 −2.0 −1.5 0 −3 0<br>2 2 0 2 1<br>0 0.5 1 −1 1 0<br>−2−4 −0.5 0−1 −2−3 −1 −2<br>−6 −1.5 −3 −4<br>6 1.5 4<br>420−2 0.5−0.5−2.0 0.5−0.5−1.5 3210 1.50.5−0.5 43210<br>4 2 0.3<br>32 0 0.5 0.1<br>1 −2<br>0−1 −4 −0.5 −0.1<br>**----- End of picture text -----**<br>


Figure 4.26 Telecommunications customers: GAM model on logarithmic scale, with significant covariates only. 

It seems unreasonable in this case to apply the algorithm automatically, which suggests choosing the tree that minimizes deviance on the pruning set. A more careful analysis indicates we should consider both models proposed by the deviance curve, which therefore also correspond to the local minimum of 121 _._ 32 × 10[9] —a tree with seven leaves. In fact, as well as finding the optimal prediction criterion, it is always useful to look for a model which also responds to simplicity criteria. If, as in this case, deviance on the pruning set is very similar in the two models, we often prefer the simpler one, apart from other considerations regarding 

Prediction of Quantitative Variables 

119 

_Table 4.4._ TELECOMMUNICATIONS CUSTOMERS: ESTIMATES FOR MARS MODEL 

|First Variable|First|Second Variable|Second|Parameters|SE|
|---|---|---|---|---|---|
||Node||Node|||
|constant||||988_._29|251_._77|
|q09.out.dur.offpeak||||−2_._84|0_._85|
|q09.out.dur.offpeak|365_._00|||4_._42|0_._85|
|q09.out.val.peak||||40_._80|3_._27|
|q09.out.val.peak||q09.out.dur.offpeak||0_._34|0_._01|
|q09.out.val.peak||q09.out.dur.offpeak|365_._00|−0_._34|0_._01|
|plan.tariff||||−119_._08|56_._43|
|plan.tariff||q09.out.val.peak||−8_._77|0_._78|
|q09.out.val.offpeak||||−48_._60|39_._37|
|q05.out.val.offpeak||||342_._32|25_._45|
|plan.tariff||q05.out.val.offpeak||−70_._93|4_._92|
|q05.out.val.offpeak||q09.out.val.peak||−0_._44|0_._13|
|q05.out.val.offpeak|48_._07|||−396_._81|32_._59|
|plan.tariff||q05.out.val.offpeak|48_._07|183_._68|12_._05|
|q05.out.val.offpeak|48_._07|q09.out.val.peak||−3_._13|0_._18|
|q05.out.val.offpeak||q09.out.val.offpeak||−2_._53|1_._03|
|q05.out.val.offpeak||q09.out.dur.offpeak||−0_._001|0_._01|
|q09.out.val.offpeak|29_._22|||−515_._14|46_._37|
|q09.out.val.peak|189_._57|||4_._91|1_._47|
|q05.out.val.offpeak||q09.out.val.peak|189_._57|3_._35|0_._25|
|q05.out.val.offpeak||q09.out.val.offpeak|29_._22|11_._44|1_._30|



model interpretation. It was for this reason that in figure 4.28 we preferred to design the final tree with seven leaves. Table 4.5 lists the prediction errors of the trees with both 7 and 44 leaves, so as to highlight the real differences between the models on the test set. 

## _Comparisons and discussion_ 

Examination of table 4.5 and other elements prompt some reflections on both models and estimates. 

The choice of the objective function is obviously linked to the marketing problem in question. In our case requests vary; on one hand the most precise prediction possible of the traffic of every customer for the month of interest is required—to be able, for example, to run budget predictions, measure the value of each customer, or redesign the network. On the other hand, we can study which operative tools can incentivize customers with medium or low traffic to increase their use of company services. Both objective functions are therefore used to provide useful suggestions for these types of requirements. 

After choosing one of the two objective functions, the optimized models are clearly better than those obtained by minimizing the other function. Table 4.5 shows that similar models obtained with different optimizations can also differ greately from each other (see, for example, results on linear models). In the following, therefore, we compare the models obtained by maximizing each of the two objective functions separately. 

Regarding the original scale—that is, analysis of the measure of total traffic, and therefore of the gain obtained by the company—we focus on the fact that 

**==> picture [257 x 488] intentionally omitted <==**

**----- Start of picture text -----**<br>
1.1e+11 9.3e+08 4.0e+08 2.0e+08 1.2e+08 7.5e+07 4.8e+07 3.5e+07 2.7e+07<br>1 50 100 150 200<br>Size<br>4000 350 90 52 42 30 23 23 21 18 17 −Inf<br>1 10 20 30 40<br>Size<br>2.0e+11<br>1.8e+11<br>Deviance 1.6e+11<br>1.4e+11<br>1.2e+11<br>16000<br>14000<br>12000<br>Deviance<br>10000<br>8000<br>**----- End of picture text -----**<br>


Figure 4.27 Telecommunications customers. Deviance of two regression trees with call duration on original scale (top) and logarithmic scale (bottom). 

**==> picture [238 x 570] intentionally omitted <==**

**----- Start of picture text -----**<br>
|<br>|<br>q09.out.dur.offpeak < 3254<br>q09.out.dur.offpeak < 489 q09.out.dur.peak < 43005.5<br>q09.out.val.peak < 81.2521<br>  1065<br>  5955  19440 q07.out.val.peak < 94.5273 q01.out.val.peak < 401.715<br> 15390  33680  72230 163700<br>q09.out.dur.offpeak < 193<br>q09.out.dur.peak < 15241.5 q07.out.dur.peak < 11346.5<br>piano.tariff: 7,8 q09.out.val.peak < 16.4365q04.out.dur.peak < 4941.5 q09.out.ch.offpeak < 36.5 q09.out.ch.offpeak < 38.5<br> 7.225  7.682  8.461  8.682  9.207  9.244 10.290<br>piano.tariff: 6,7,8 q09.out.dur.peak < 22868.5 q09.out.dur.peak < 46008 q09.out.val.peak < 303.243<br>q09.out.dur.peak < 6111 q09.out.dur.peak < 502<br>canale.attivaz: 6,9 q09.out.ch.peak < 1.5 q09.out.dur.peak < 1669 q08.in.dur.tot < 186 q09.out.dur.peak < 9587<br> 6.373  6.983  7.563  8.270<br> 6.093  7.799<br> 4.029  5.770  4.300  4.942  6.361  5.370  5.887<br>**----- End of picture text -----**<br>


Figure 4.28 Telecommunications customers. Final regression trees, fitted to data with call duration on original scale (top) and logarithmic scale (bottom). 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

122 

_Table 4.5._ TELECOMMUNICATIONS CUSTOMERS: PREDICTION ERRORS IN ORIGINAL AND LOGARITHMIC SCALES FOR MODELS FITTED TO DATA 

|Model|Variables|Optimization|Squared Error|Squared Error|
|---|---|---|---|---|
|||Scale|Original Scale|Logarithmic Scale|
|Linear|all|original|257,736,193,454|113_,_472|
|Linear|only signif.|original|258,524,520,314|112_,_061|
|Linear|all|logarithmic|79,407,475,570,006,224|15_,_838|
|Linear|only signif.|logarithmic|41,140,000,000,000,000|15_,_853|
|GAM|all|original|392,419,005,268|94_,_137|
|GAM|only signif.|original|391,286,779,004|98_,_628|
|GAM|prev. month|original|299,872,658,074|109_,_552|
|GAM|all|logarithmic|666,446,084,652|229_,_497|
|GAM|only signif.|logarithmic|1,190,485,331,659|13_,_989|
|GAM|prev. month|logarithmic|1,668,869,970,637|13_,_779|
|MARS||original|211,786,338,287|35_,_151|
|MARS||logarithmic|276,868,390,512|13_,_317|
|Neural network||original|604,876,539,104|35_,_151|
|Neural network||logarithmic|601,084,507,392|36_,_875|
|Tree|44 leaves|original|324,547,309,675|20_,_252|
|Tree|7 leaves|original|252,187,094,517|32_,_852|
|Tree||logarithmic|344,247,954,167|13_,_796|



customers with high traffic are special and are considered much more important than customers with medium or low traffic. We therefore note the following. 

- All the models are essentially equivalent as for prediction error with the only exception of the neural network. 

- The tree that the pruning set suggested was “optimal” (i.e., 44 final nodes) performs worse than the tree selected as “sub-optimal,” with 7 leaves, which combines simplicity and precision. This example indicates that trees may provide very interesting results if they are studied with care and evaluated in all their relevant aspects. 

- The preferable model in terms of prediction error is MARS, which is used to make a precise prediction of total call duration in the following month. 

- After precise prediction of total call duration, it is very important for marketing experts to have a precise description of the characteristics of those customers who make large numbers of calls with respect to those who do not. 

   - Table 4.4 gives us a first, albeit preliminary, idea of the mechanism that allows MARS to predict total duration. 

   - Other models are of more help in interpreting results. In this case, the regression tree does not only perform well in terms of 

Prediction of Quantitative Variables 

123 

prediction error, but is also extremely easy to interpret and, as seen in figure 4.28, offers simple but useful cues for marketing actions. 

- Other than trees, linear models and GAM are also simple to interpret, through the table of coefficients presented at the beginning of this section for the former, and graphs like those of figure 4.26 for the latter. 

- Neural networks present greater difficulties in interpreting relationships. In this specific case, they also appear to perform worse than the other models. 

Similar reasoning can be made for the last column of table 4.5, showing the squared errors on the logarithmic scale. In this case, the objective is to reduce the effect on estimates of best customers and search for the levers on which the company’s marketing department can act to increase the traffic of customers with low value. 

Again, the best model seems to be MARS, followed by GAM and the regression tree. The linear model behaves slightly worse than the others, probably due to the nonlinearity induced by the logarithmic transformation, which the other, 

When working on the logarithmic scale, the need to interpret the results is greater than that of simply being able to suggest actions to carry out on the customer base. It therefore favors a GAM-type model, which, as we have seen, offers not only good performance in terms of prediction error but also easy interpretation (see figure 4.26). 

## _Summary_ 

- We need a model to predict the traffic of each customer in a fixed month, using information on customers and services to them in the previous months. 

- There are at least two types of aims: (1) to predict total traffic in the month of interest with the greatest possible precision, (2) to identify lines of action to persuade customers with less traffic to increase it. 

- The model chosen for the first aim was MARS, with the smallest prediction on the original scale, which is appropriate for problems of type (1). 

- The model chosen for the second aim, for which we used the logarithmic transform, was GAM, which, although not having the best prediction error on the logarithmic scale, is appropriate for problems of type (2). It also makes quite good predictions, offers easy interpretation of the model, and indicates possible up-sell actions. 

## 4.10.2 Insurance Pricing 

The problem described next was handled by the _nonlife_ actuarial office of an insurance company. However, our objective is not to analyze actuarial issues in detail but to present data mining methods as tools for business choices. Much literature is available on statistical models for insurance pricing problems 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

124 

(e.g., Ohlsson & Johansson 2010; Tse 2009). A specific characteristic of this type of problem is that the value of the _premium_ must be defined before a _claim_ is made, that is, before its cost is known. Large numbers of predictive actuarial models have been developed to price different types of insurance. 

The marketing managers of insurance companies are also interested in the combinations of products customers have. They want to “segment” the base by grouping customers with similar behavior and identify the characteristics of customers having similar premium value for some specific product. In this section, we examine the problem of predicting the amount of the _pure premium_ (the total claim amount, divided by the duration of exposure to risk) for private car third-party liability insurance by considering subscription to other products offered by the same company, as well as other policyholder variables such as age, gender, and residential area. In particular, the company is interested in which insurance products are bought by customers who buy third-party liability insurance. 

## _The data_ 

The data are described in detail in section B.5 and refer to a random sample of 5 _,_ 000 policyholders in a given year. Available variables include the number and total amount of premiums paid in the current year. It is easy to obtain the average pure premium for third-party liability policies, which is the response variable in our analysis. Clearly, a different strategy would be to predict the single variables, number of policies, and total sum paid for premiums by using two different models and then obtain the predicted ratio of the single-model predictions. There are circumstances in which either of these strategies is preferable (see exercise 4.10). Data on other customer policies are also available and are used as covariates. 

We divide the original data set into two parts: 4 _,_ 000 policyholders are used for training the models and the remaining 1 _,_ 000 are reserved to validate results. 

Simple descriptive analysis of the training set shows that 26 _._ 70% of customers do not hold any third-party liability insurance, and only 12 _._ 12% subscribe to more than one policy. 

The first four panels of figure 4.29 show some characteristics of customers in the training set. The marginal distribution of the average pure premium paid by customers holding at least one policy is quite skewed, as shown by the bottomleft panel of figure 4.29. The last panel of figure 4.29 shows the histogram of the logarithm of the average pure premium added to 1, so that customers not subscribing to third-party liability policies are all included in the bar at 0. 

Table 4.6 shows the probabilities that in the year considered, a customer subscribes to products of one or two types, usually called “lines,” at the same time. The diagonal elements represent the probabilities of subscribing to a product of every single line, and all other elements represent the probabilities that a customer subscribes both to a product of the type indicated by the row and to one of a type indicated by the column in the same year, so that the matrix is symmetric. 

The probability of subscribing to a third-party liability policy and a policy of type 1 at the same time is clearly higher than in other groups. Policy type 4 also shows a relatively high association with the policy of interest. 

Prediction of Quantitative Variables 

125 

**==> picture [330 x 296] intentionally omitted <==**

**----- Start of picture text -----**<br>
Not available Female Male 20 40 60 80<br>Gender Age<br>0 1 2 3 4 5 6 7 8 9 City Country<br>Region Area<br>0 1000 2000 3000 4000 0 2 4 6 8<br>Average pure premium Log (average pure premium + 1)<br>0.6<br>0.020<br>Frequency 0.40.2 Density 0.010<br>0.0 0.000<br>0.20<br>0.6<br>0.10 0.4<br>Frequency Frequency 0.2<br>0.00 0.0<br>0.0030<br>0.4<br>Density 0.0015 Density 0.2<br>0.0<br>0.0000<br>**----- End of picture text -----**<br>


Figure 4.29 Insurance customers: Plots of distribution of a few selected variables. 

## _Some prediction models_ 

To better understand the characteristics of third-party liability customers, we formulate a number of regression models by considering either the original average pure premium or its logarithm. 

We can organize the analysis into two phases, as we did for telecommunications customer prediction (section 4.10.1): first fitting a model for the probability that the premium is not 0, and then, conditionally on this event, fitting a model for the amount of the premium when it assumes positive values. We leave this implementation as an exercise (exercise 4.11), and prefer here to predict the average pure premium directly, including customers with 0 amount paid in the response variable. 

A linear model to predict the average pure premium with all available covariates gives _R_[2] = 0 _._ 27. The same value is obtained by selecting the most important 30 variables in a stepwise procedure based on AIC. We also fit a linear model with lasso. The LARS algorithm allows us to estimate the entire set of models. We then select the one producing the smallest squared error on the evaluation set. Figure 4.30 shows the whole path of the coefficients for all lasso models obtained by changing the value of _s_ in (3.11). Coefficients are plotted versus _t_ = _s/_[�] _[p] j_ =1[| ˆ] _[β][j]_[|][.] A vertical line is drawn at _t_ = 0 _._ 14, the value chosen according to the test set. 

126 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

_Table 4.6._ INSURANCE CUSTOMERS. CUSTOMERS SUBSCRIBE TO PRODUCTS OF ONE OR TWO GROUPS AT THE SAME TIME: OBSERVED FREQUENCIES 

|Policy|Third-Party|Policy|Policy|Policy|Policy|Policy|Policy|Policy|Policy|Policy|
|---|---|---|---|---|---|---|---|---|---|---|
||Liability|1|2|3|4|5|6|7|9|10|
|Third-party<br>liability|0_._7330|0_._1137|0_._0130|0_._0027|0_._0515|0_._0065|0_._0160|0_._0022|0_._0002|0_._0065|
|1|0_._1137|0_._1867|0_._0287|0_._0012|0_._0245|0_._0045|0_._0072|0_._0017|0_._0000|0_._0027|
|2|0_._0130|0_._0287|0_._0455|0_._0005|0_._0080|0_._0020|0_._0032|0_._0002|0_._0000|0_._0015|
|3|0_._0027|0_._0012|0_._0005|0_._0165|0_._0030|0_._0010|0_._0017|0_._0000|0_._0000|0_._0002|
|4|0_._0515|0_._0245|0_._0080|0_._0030|0_._1340|0_._0130|0_._0050|0_._0007|0_._0000|0_._0027|
|5|0_._0065|0_._0045|0_._0020|0_._0010|0_._0130|0_._0165|0_._0015|0_._0000|0_._0000|0_._0005|
|6|0_._0160|0_._0072|0_._0032|0_._0017|0_._0050|0_._0015|0_._0372|0_._0002|0_._0000|0_._0002|
|7|0_._0022|0_._0017|0_._0002|0_._0000|0_._0007|0_._0000|0_._0001|0_._0047|0_._0000|0_._0000|
|9|0_._0002|0_._0000|0_._0000|0_._0000|0_._0000|0_._0000|0_._0000|0_._0000|0_._0002|0_._0002|
|10|0_._0065|0_._0027|0_._0015|0_._0002|0_._0027|0_._0005|0_._0002|0_._0000|0_._0002|0_._0120|



**==> picture [233 x 208] intentionally omitted <==**

**----- Start of picture text -----**<br>
LASSO<br>0.0 0.2 0.4 0.6 0.8 1.0<br>| b |/max| b |<br>60000 198<br>40000<br>20000<br>171<br>0 4<br>212<br>Standardized coefficients –20000<br>–40000<br>–60000 197<br>**----- End of picture text -----**<br>


Figure 4.30 Insurance customers: profiles of lasso coefficients as tuning parameter _s_ is varied. Standardized coefficients plotted versus _t_ = _s/_[�] _[p]_ 1[| ˆ] _[β][j]_[|][.] 

Lasso shrinks parameters and gives a model with only 9 variables (15 parameters). The estimated coefficients obtained by lasso with R are listed in table 4.7. 

We also fit some nonlinear models to the data. To choose a suitable neural network for our problem, we divide the training set into two subsets of equal size and fit a number of different networks on the first subset by modifying the number of nodes in the hidden layer and the weight decay. Networks with 10 to 19 hidden nodes and 10 values for weight decay between 0 _._ 001 and 0 _._ 1 are evaluated, and we select the one with the smallest squared prediction error on the second subset of the training set. The best model has 12 nodes and weight decay of 0 _._ 1. 

Prediction of Quantitative Variables 

127 

_Table 4.7._ INSURANCE CUSTOMERS: ESTIMATE OF COEFFICIENTS FOR BEST LASSO NONZERO ESTIMATE OF LINEAR MODEL 

|Variable|Level|Coeff.|
|---|---|---|
|occupation.1|9|6_._94|
||99|26_._57|
||5|25_._54|
|occupation.2|12|7_._63|
||13|20_._47|
||1082|73_._15|
|area|1191|17_._27|
||1542|94_._19|
|number.claims.3||100_._18|
|amount.claims.last||0_._0041|
|prem.non-life.5||0_._1098|
|prem.payed.life.1b||0_._00007|
|number.life.2b||102_._57|
|region|2<br>8|61_._84<br>10_._24|



A regression tree is also fitted to data. We let the tree grow by using data on the first subset of the training set and then prune it by using the second subset. The top panel of figure 4.31 shows deviance versus number of nodes. The global minimum is observed for size 2 and the pruned tree splits the pure premium once: if there were no claims in the last three years, the predicted pure premium is €306 _._ 00; otherwise, it is €497 _._ 50. However, this tree cannot describe the various characteristics of customers, particularly if we are interested in connections with other lines of products. Thus, we consider a second tree, the one corresponding to the local minimum for size equal 11, plotted in the bottom panel of the same figure 4.31. 

Last, we fit a MARS model, a projection pursuit regression model, and an additive model by selecting variables by a stepwise procedure based on AIC. 

We then consider the logarithm of the average pure premium and fit different models predicting this transformed variable. Linear models with different selection strategies, GAM, MARS, projection pursuit, neural network, and trees are fittedtothedatatopredictthetransformedresponsevariable,choosingappropriate tuning parameters. 

The top part of figure 4.32 shows the pruned tree resulting from prediction of the transformed variable with the same growing and pruning subsets as for the original-scale tree. 

Table 4.8 shows the prediction errors obtained on the validation set of some of the models used (the better-fitting ones). For each, we present the squared prediction error on original and logarithmic scales. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

128 

**==> picture [250 x 443] intentionally omitted <==**

**----- Start of picture text -----**<br>
1.3e+07 9.7e+05 5.3e+05 3.7e+05 3.0e+05 2.2e+05 1.7e+05    −Inf<br>1 50 100 150 200 250 300<br>Size<br>n.claims.3 < 0.5<br>|<br>n.life.1a < 0.5 prem.nonlife.1 < 1330<br>n.nonlife.4 < 0.5 area:adghjlortuvwxyz}..<br>91.92<br>3833.00<br>occupation.2:achiklopq<br>448.30<br>occupation.2:fhijoq<br>124.10 598.30 1090.00<br>prem.nonlife.1 < 100.5<br>226.70<br>area:abhijlmnqstuvw}..<br>99.43<br>prem.nonlife.3 < 26.5<br>627.80<br>408.60 0.00<br>3.4e+08<br>3.0e+08<br>Deviance<br>2.6e+08<br>2.2e+08<br>**----- End of picture text -----**<br>


Figure 4.31 Insurance customers. Top: deviance of regression tree with pure premium on original scale; bottom: second-best regression tree fitted to data with average pure premium on original scale. 

## _Comparisons and discussion_ 

Analysis of table 4.8 provides ingredients for comparing the various models and allows for different choices according to marketing managers’ aims. 

In the original scale, the best prediction is that obtained by lasso estimates of the linear model, and GAM and MARS predictions give a squared error on the original 

**==> picture [289 x 252] intentionally omitted <==**

**----- Start of picture text -----**<br>
pret.life.1a < 96<br>|<br>i.nonlife.4:a n.claims.3 < 0.5<br>1.0630 5.3040<br>prem.nonlife.1 < 100.5 n.claims.3 < 0.5<br>n.nonlife.1 < 0.5 occupation.2:cdefhjq<br>occupation.2:fjq area:adelpqtvz{}•..4.7680 [2.5220] [5.4370]<br>2.2470<br>0.9992 6.0530<br>n.claims.3 < 0.5 prem.nonlife.3 < 16.5<br>2.0090 5.6320<br>prem.nonlife.6 < 14<br>0.7642<br>n.nonlife.2 < 0.5<br>2.5810<br>prem.nonlife.1 < 30.5<br>1.6430<br>5.8080 4.7230<br>**----- End of picture text -----**<br>


Figure 4.32 Insurance customers. Regression tree with pure premium on logarithmic scale. 

**==> picture [299 x 284] intentionally omitted <==**

**----- Start of picture text -----**<br>
occupation.2<br>prem.nonlife.1<br>age<br>region<br>zip<br>n.claims.3<br>prem.nonlife.4<br>prem.life.1a<br>pret.life.1a<br>i.nonlife.4<br>n.nonlife.4<br>occupation.1<br>amount.claims.3<br>i.life.1a<br>prem.nonlife.6<br>n.life.1a<br>n.nonlife.1<br>prem.nonlife.2<br>prem.nonlife.3<br>i.nonlife.3<br>i.nonlife.2<br>sex<br>i.nonlife.1<br>n.nonlife.3<br>n.nonlife.6<br>n.nonlife.2<br>prem.life.3b<br>i.nonlife.6<br>pret.life.3b<br>country<br>0 500 1000 1500 2000 2500<br>IncNodePurity<br>**----- End of picture text -----**<br>


Figure 4.33 Insurance customers. Measure of importance of each variable of random forest for pure premium on same scale. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

130 

_Table 4.8._ INSURANCE CUSTOMERS: PREDICTION ERRORS IN ORIGINAL AND LOGARITHMIC SCALES FOR MODELS FITTED TO DATA 

|Model|Optimization|Squared Error|Squared Error|
|---|---|---|---|
||Scale|Original Scale|Logarithmic Scale|
|Linear (all variables)|original|1,924,095,198|7,918|
|Linear (lasso)|original|74,270,206|7,967|
|Linear (stepwise)|original|1,870,139,302|7,744|
|GAM (stepwise)|original|73,171,214|7,622|
|Neural network|original|94,077,740|9,002|
|Neural network|logarithmic|192,971,718|4,483|
|Tree (2 leaves)|original|92,697,508|9,503|
|Tree (9 leaves)|original|94,077,740|7,795|
|Tree|logarithmic|94,425,522|4,036|
|Projection pursuit|original|85,829,668|7,454|
|Projection pursuit|logarithmic|3,607,884,000,000|4,258|
|MARS|original|74,288,572|6,732|
|MARS|logarithmic|620,993,900,000,000|4,201|



scale that is only slightly larger. These models, in addition to good predictions, allow easier interpretation of the characteristics of various types of customers. 

For example, from table 4.7 it is clear that customers paying large premiums for third-party liability insurance live in certain regions (in particular region 2 and, to a limited extent, region 8) and geographic areas (area 1542 shows premium increases of about €94, area 1082 about €73, and area 1191 about €17, when compared with other regions) and they work in specific sectors. In addition, there are some characteristics more related to customer behavior: subscription to one or more life insurance policies of type 2b and the total amount of the premium paid for type 1b life insurance policies both increase the level of the pure premium for third-party liability. Moreover, the amount of premiums paid for nonlife insurance of type 5 increases the pure premium, and customers who made claims in the past three years, particularly those who spent more in the last year, have larger premiums. 

The model that best predicts the squared prediction error on the logarithmic scale is the tree. Looking at figure 4.32, we see that the regression tree for the logarithm of the average pure premium mainly contains splits related to nonlife products. 

## _Summary_ 

- We want a model to predict the average pure premium of customers for private car third-party liability insurance, using information on the number of policies and amount of premiums paid by customers for other lines of business of the same insurance company, in addition to some sociodemographic data. 

Prediction of Quantitative Variables 

131 

_Table 4.9._ INSURANCE CUSTOMERS: PREDICTION ERRORS IN ORIGINAL AND LOGARITHMIC SCALES FOR SOME MODELS DESCRIBED IN CHAPTER 5 FITTED TO DATA 

|Model|Optimization|Squared Error|Squared Error|
|---|---|---|---|
||Scale|Original Scale|Logarithmic Scale|
|SVM (radial kernel)|original|68,795,451|5,790|
|Random forest<br>(40 variables for each split)|original|76,643,407|6,820|
|Random forest<br>(40 variables for each split)|logarithm|88,553,872|3,599|



- There are two objectives: (1) to predict the average pure premium with the greatest possible precision; (2) to predict low and medium levels of premiums more carefully, for the moment neglecting precision for high premiums. 

- Forthefirsttarget,ourchoiceisalinearmodelfittedwithalassoprocedure, which shows good prediction error on the original scale, is appropriate for problems of type (1), and has an easily interpretable output in terms of characteristics of customers profiled with respect to the average pure premium. 

- For the second objective, we choose a regression tree, which presents the best prediction error on the logarithmic scale. 

## _Back from the future_ 

Some methods, which are modifications of classification methods discussed in the next chapter, that is, support vector machines (SVM), bagging, boosting, and randomforests,arealsofittedtothisdata,consideringbothoriginalandlogarithmic scales. Table 4.9 shows the prediction errors obtained on the validation set of some of these models (the better-fitting ones). 

In the original scale, SVM shows better prediction than the lasso linear model, but as we see in section 5.8.2, it does not allow for easy interpretation of results. 

In logarithmic scale the random forest (see section 5.9.3) over-perform the previously chosen tree. In this case, although easy interpretation of the tree is lost, a useful plot can give some information about the importance of the variables. Figure 4.33 shows an importance measure of each variable for random forests. As discussed in section 5.9.3, this measure is the average over all the trees in the forest of the measures of importance of a variable for each single tree, introduced at the end of section 4.8.3. This plot shows that when we consider logarithmic scale errors (that is, when we want to limit the effect of errors for very large premiums) sociodemographic characteristics such as age, occupation, and region of residence are still relevant variables, and important variables regarding customer behavior are more related to nonlife products: policies of types 1 and 4 are more important than life products, which were more important in predicting the original scale. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

132 

## EXERCISES 

- 4.1 Prove (4.3). 

- 4.2 Prove (4.5). 

- 4.3 Every nonparametric regression model involves a smoothing parameter. For example, consider parameter _h_ of local regression. Why is it not estimated by a standard method such as maximum likelihood? 

- 4.4 Given _n_ points ( _x_ 1 _, y_ 1) _, . . . ,_ ( _xn, yn_ ), with all _xi_ distinct and increasing, show that the function that minimizes 

**==> picture [64 x 27] intentionally omitted <==**

under the constraint that _f_ ( _xi_ ) = _yi_ ( _i_ = 1 _, . . . , n_ ) is a natural cubic spline with nodes at points _x_ 1 _, . . . , xn_ . This function is called an _interpolation spline_ . 

- 4.5 Show that function (4.10) satisfies the following three conditions, which characterize cubic splines 

   1. _f_ is a cubic function in each subinterval [ _ξj, ξj_ +1), for _j_ = 1 _, . . . , K_ − 1; 

   2. _f_ has two continuous derivatives; 

   3. _f_ has a third derivative that is a step function with jumps at points _ξ_ 1 _, . . . , ξK_ . 

- 4.6 Prove (4.12). 

- 4.7 Consider non-parametric model _Yi_ = _f_ ( _xi_ 1 _, . . . , f_ ( _xip_ ) + _εi_ , where E{ _εi_ } = 0, var( _εi_ ) = _σ_[2] , for _i_ = 1 _, . . . , n_ , and assume that all error terms _εi_ are independent of each other. Under the assumption of smoothness of _f_ , consider linear smoother _Y_[ˆ] = _SY_ evaluated at the observed covariate points, i.e., _S_ is a _n_ × _n_ smoothing matrix and _Y_ = ( _Y_ 1 _, . . . , Yn_ )[⊤] . Prove that: 

**==> picture [108 x 31] intentionally omitted <==**

- 4.8 In the tree growth algorithm, show that _Dj_ − _D_[∗] _j[>]_[ 0, apart from a degenerate] case (which one?). 

- 4.9 Consider the step of the tree growth algorithm when examining a generic variable _xr_ . How can the value of the point of subdivision of its range be determined efficiently? 

- 4.10 In the case study on prediction of third-party liability insurance premiums in section 4.10.2, we directly predicted the average pure premium per customer. A different strategy would be to predict, separately with two different models, the number of policies per customer and the total amount of 

Prediction of Quantitative Variables 

133 

premiums paid by each customer, and then obtain the ratio between the two predictions. Follow this strategy and compare results with those presented in section 4.10.2. 

- 4.11 Analyze the insurance data in two steps: first fit a model for the probability that the premium is not 0, and then, conditionally on this, fit a model for the amount of the premium when it assumes positive values. Compare the results with those presented in section 4.10.2 and those obtained in this exercise. 

5 

## Methods of Classification 

## 5.1 PREDICTION OF CATEGORICAL VARIABLES 

One of the most frequent practical problems in statistics is allocating a unit to a _category_ or a _class_ among _K_ possible alternatives, using observations about its variables. The examples that follow illustrate various situations of this type, focusing on a business context, an area where this kind of problem arises. 

- A bank must decide on the degree of solvency of a customer who is asking for a loan. The problem is to assign the customer to the category of “solvent” or “insolvent” borrowers, which are two mutually exclusive and exhaustive categories—presuming, that is, the bank conventionally allocates its customers to one of the two categories. To make such a classification, various pieces of information, both personal and historical, about the customer are available to the bank. In the credit sector, this type of problem is associated with the terms _credit scoring_ and _credit rating_ . 

- An insurance company must evaluate whether a motorist who takes out a third-party liability policy will have 0, 1, 2, or more accidents in the next year. The available information here is customer’s personal information, vehicle characteristics, and data on insurance history. In the business sector, this type of problem is associated (indirectly) with _pricing_ . 

- An airline wants to predict which of its customers, among those in possession of a loyalty card, will make an intercontinental flight to a holiday destination within the next 12 months. To avoid contacting people who 

Methods of Classification 

135 

   - are not interested, the airline sends a catalog of promotional deals to those customers with a high inclination to do so. In this case, customers are divided into two groups: those who will and those who will not make holiday flights, and the available information for predictions is recorded in the airline loyalty card database. In the business sector, this type of problem is associated with terms like _up-sell_ and _cross-sell_ . 

- A car company wants to identify customers who, within the next six months, intend to purchase a new car of the type “luxury car,” so that a presentation brochure of the latest model can be sent to them. It therefore needs to turn to a specialized company for lists of potential customers. These are created from extremely large collections of data from diverse sources, which all contribute toward the formation of individual economic behavior profiles . In the business sector, this type of problem is associated with the management of _prospects_ . 

The number _K_ and the nature of the classes in each problem are well defined, in the sense that the allocation criterion must be able to decide the membership of each unit to one and only one class in a nonambiguous way. In all the previous examples, we had _K_ = 2 (apart from the second example, where _K_ = 3). The predominance of examples with _K_ = 2 corresponds to a predominance in real situations. 

The objective, therefore, is to construct a rule to arrange available observations on the variables relative to an individual and allocate that person to one of the classes. The following is based on the hypothesis that we use a certain set of _n_ cases for which membership class is known, in addition to observed variables. In this case, we use this information to construct the classification rule. 

The problem is similar to that considered in chapter 4, with the difference that response variable _y_ is categorical with _K_ levels, which represent membership class. We indicate by _y_ 1 _, . . . , yn_ the membership classes of elements in the sample, and by _nk_ the number of units belonging to the _k_ th class, for _k_ = 0 _, . . . , K_ − 1. We denote by _Y_ the parent random variable from which the _yi_ are sampled. 

Therefore, apart from methods specifically developed in this context, many of the techniques presented here go back to the contents of chapter 4. However, there are some necessary adaptations, one of which concerns the usual discrepancy measure (2.10) between observed values and estimates, which is not adequate here. Another aspect is that we have _K_ ( _K_ − 1) possible forms of _misclassification error_ , and the adequacy measures of various methods are constructed in this context. 

## 5.2 AN INTRODUCTION BASED ON A MARKETING PROBLEM 

## 5.2.1 Prediction via Logistic Regression 

We have already seen one of the methods used to overcome classification problems when _K_ = 2, that is, logistic regression (section 2.4). This model predicts a categorical response variable with two levels, usually indicated by 0 and 1 so that an appropriate transformation of the probability of result 1 is expressed as a linear 

136 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

combination of the covariates. We can use this tool to face a first example of classification and examine further aspects of the problem in greater detail. 

Consider data on the preferences of consumers of two brands of fruit juice in some American supermarkets, considering _n_ = 1070 purchases that included fruit juice. The source and other information on the same data are reported in section B.6. To predict the customer choice between the two brands, CH and MM, other available variables are used: the prices of the two brands, priceCH and price MM; the discounts applied, discountCH and discountMM; a loyalty indicator for MM, loyaltyMM; an identifier of the week, and the store where the purchase was made. Indicator loyaltyMM reflects the fraction of preference given in previous purchases to brand MM; the similar indicator loyaltyCH is also available, so that their sum is constantly 1, and therefore only one of the two needs to be considered. 

According to the procedure already introduced in section 3.5.1, we select a random portion of 75% of the total set, to be used for fitting and other operations. The remaining 25% is then used to evaluate the results. 

Figure 5.1 shows the behavior of the variables, taken individually. The first six panels are box-plots of the continuous variables, stratified with respect to the response variable. The last panel shows a bar plot of the percentage of cases in which MM was preferred, stratified by store. 

As a first classification tool of customers with respect to their purchase preferences, we fit a logistic regression model for probability _π_ of choosing MM, using the covariates indicated above. The model takes the form 

**==> picture [285 x 52] intentionally omitted <==**

where the notation _I_ factor represents a set of indicator variables equal in number to the levels of the qualitative variable factor, decreased by 1; in this case, the corresponding parameter _βj_ is a vector with a matching dimension. Here we adopt the so-called _corner-parameterization_ for the qualitative variable, for which the first level is taken as reference and the parameters for other levels represent deviation from it. The parameter estimates and related quantities are listed in table 5.1. 

We remove the term week from (5.1) in light of the _p_ -values of table 5.1. After refitting the model, the parameter estimates and other relevant quantities are as listed in table 5.2. The appropriateness of the reduction is confirmed by the likelihood ratio test _D_ 2 − _D_ 1, which is virtually 0 on the scale of reference distribution _χ_ 1[2][, bearing in mind (2.33).] 

## 5.2.2 Misclassification Tables and Adequacy Measures 

We now apply the fitted model to the portion of data not yet used to classify the remaining units and examine the prediction ability of the identified model. To allocate a new unit, we evaluate the probability of choosing MM according to the chosen model and assign the customer to one category or the other, according to 

**==> picture [328 x 521] intentionally omitted <==**

**----- Start of picture text -----**<br>
CH MM CH MM CH MM<br>CH MM CH MM CH MM<br>0 1 2 3 4<br>Shop<br>280 2.1 2.3<br>270 2.2<br>2.0<br>2.1<br>260<br>Week 1.9 2.0<br>250 PriceCH PriceMM<br>1.9<br>240 1.8<br>1.8<br>230<br>1.7 1.7<br>0.5 0.8 1.0<br>0.4 0.8<br>0.6<br>0.3 0.6<br>0.4<br>DiscountCH 0.2 DiscountMM LoyaltyMM 0.4<br>0.2<br>0.1 0.2<br>0.0 0.0 0.0<br>100<br>80<br>60<br>40<br>Percentage of choosing MM<br>20<br>0<br>**----- End of picture text -----**<br>


Figure 5.1 Fruit juice data: Preliminary graphical representations. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

138 

_Table 5.1._ FRUIT JUICE DATA: SUMMARY OF FITTED LOGISTIC REGRESSION MODEL (5.1) 

||Estimate|SE|_t_-value|_p_-value|
|---|---|---|---|---|
|(intercept)|−3_._816|2.059|−1_._85|0.064|
|week|−0_._002|0.013|−0_._13|0.895|
|priceCH|4_._435|2.114|2_._10|0.036|
|priceMM|−3_._706|1.006|−3_._68|0.000|
|discountCH|−3_._648|1.140|−3_._20|0.001|
|discountMM|2_._095|0.500|4_._18|0.000|
|loyaltyMM|5_._864|0.448|13_._09|0.000|
|store1|0_._551|0.315|1_._75|0.080|
|store2|0_._656|0.285|2_._30|0.021|
|store3|0_._574|0.368|1_._56|0.119|
|store4|0_._039|0.419|0_._09|0.927|



_D_ = 631 _._ 63 with 791 d.f. 

_Table 5.2._ FRUIT JUICE DATA: SUMMARY OF FITTED LOGISTIC REGRESSION MODEL WITHOUT TERM week 

||Estimate|SE|_t_-value|_p_-value|
|---|---|---|---|---|
|(intercept)|2_._056|2.015|1_._02|0.308|
|priceCH|4_._241|1.520|2_._79|0.005|
|priceMM|−3_._744|0.963|−3_._89|0.000|
|discountCH|−3_._695|1.084|−3_._41|0.001|
|discountMM|2_._082|0.491|4_._24|0.000|
|loyaltyMM|5_._868|0.447|13_._12|0.000|
|store1|0_._543|0.309|1_._76|0.079|
|store2|0_._651|0.283|2_._30|0.021|
|store3|0_._593|0.338|1_._75|0.079|
|store4|0_._055|0.401|0_._14|0.892|



_D_ = 631 _._ 64 with 792 d.f. 

whether this probability is greater or less than[1] 2[. We thus construct a cross-table] that counts the number of correctly or incorrectly predicted cases, for each of the two levels (table 5.3). This is called a _misclassification table_ or a _confusion matrix_ . 

Because we want to compare various classification procedures, we look for a summarizing index of the quality of the result, and therefore introduce some _adequacy measures_ of prediction. The first of these is simply constructed from the fraction of cases correctly classified or, conversely, those wrongly classified. In this case, we obtain 

**==> picture [264 x 11] intentionally omitted <==**

Because these two quantities provide equivalent information, one of them suffices and, by convention, we call this error frequency _misclassification error_ . 

Methods of Classification 

139 

_Table 5.3._ FRUIT JUICE DATA: MISCLASSIFICATION TABLE OF MODEL WITHOUT TERM week IN TEST SET 

|Prediction<br>CH<br>MM<br>Total|Actual response<br>CH<br>MM<br>Total<br>150<br>23<br>173<br>19<br>76<br>95<br>169<br>99<br>268|
|---|---|



_Table 5.4._ CONFUSION MATRIX AND TABLE OF PROBABILITY ERRORS 

|_Ta_|_ble 5.4._ CONFUSIONMATRIX ANDTABLE OFPROBAB|ILITYERRORS|
|---|---|---|
|Prediction<br>**−**<br>**+**<br>Total|Actual response<br>**−**<br>**+**<br>Total<br>_n_00<br>_n_01<br>_n_0·<br>_n_10<br>_n_11<br>_n_1·<br>_n_·0<br>_n_·1<br>_n_<br>Prediction<br>**−**<br>**+**<br>Total|Actual response<br>**−**<br>**+**|
|||1−_α_<br>_β_<br>_α_<br>1−_β_|
|||1<br>1|



However, this method of proceeding is somewhat simplistic: there are various reasons to be aware of the two separate types of error. If the “positive” event is the purchase of MM, MM customers classified as CH purchasers are called _false negatives_ , taking a term originally used in medical context. In reverse, CH customers classified as MM purchasers are called _false positives_ . The situation is shown in table 5.4, where the terms _nij_ on the left correspond to the absolute frequencies of the four possible results; therefore, _n_ 01 is the count of the false negatives and _n_ 10 that of false positives. 

There is a similarity between this set-up and that of hypothesis testing in the sense that false positives are analoguous to type I error and false negatives to type II error, as listed in the right side of table 5.4. According to the terminology of hypothesis testing, 

**==> picture [216 x 14] intentionally omitted <==**

These two probabilities are unknown and not fixed by us, but they can be estimated by 

**==> picture [132 x 13] intentionally omitted <==**

A first remark in this regard is that the _cost_ of a classification error—that is, damage caused by an error—is not the same in the two situations. Depending on the problem, we can give more weight to one type of error or the other. For example, if we are interested in identifying customers who choose MM, we want to minimize the error in identifying them. 

We therefore consider the error fractions for each observed subpopulation, thus distinguishing between false positives and false negatives. Recalling the previous 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

140 

comments, we use the selected model in a slightly different way: the logistic model itself provides a set of probabilities, and 2[1][need not be used as the threshold value] to allocate the units. We can grade the weight assigned to each category by moving the threshold value. 

## 5.2.3 ROC Curve 

Although from some points of view it is convenient to use very concise and comprehensive indicators of the performance of a classification procedure, such as the simple fractions just considered, it is useful to evaluate the predictive ability of various models more analytically. 

One tool to evaluate the adequacy of a classification criterion is provided by the _ROC curve_ (receiver operating characteristic). This was introduced during World War II in the context of communication theory, specifically radar signal detection, and was then extensively used elsewere, especially in quality control and medical statistics. 

We return to table 5.3 to quantify the proportion of false positives with respect to the total of positive individuals, here 19/169, and the proportion of false negatives, here 23/99. However, these values are linked by the threshold value, which is 2[1][for][this][table.][We][now][move][this][threshold][between][0][and][1,][and] calculate the corresponding proportion of false positives and negatives. We call these proportions: 

- _specificity_ for the proportion of predicted negatives with respect to the number of actual negatives, that is, 1 − _α_ . 

- _sensitivity_ for the proportion of predicted positives with respect to the number of actual positives, that is, 1 − _β_ . 

These quantities are naturally estimated by 

**==> picture [224 x 23] intentionally omitted <==**

The ROC curve is made up of the coordinate points (1 − specificity _,_ sensitivity) from these fractions for each of the possible threshold values. 

For the fruit juice data, the results, are shown in the left panel of figure 5.2; the right panel shows a smooth version of the same points. This smoothing was done by regrouping the data into portions with one-tenth of the points each. 

To interpret this curve, we bear in mind that the bisector of the origin corresponds to random classification of subjects. We are searching for a classification rule in which the ROC curve is as high as possible above the diagonal. 

## 5.2.4 Lift Curve 

Another frequently used tool to evaluate the performance of a classification procedure more analytically is the _lift function_ , which provides a measure of the improvement gained by the model with respect to random classification, with uniform probability equal to the observed fraction in the test set. 

Methods of Classification 

141 

**==> picture [329 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
Threshold=0.5<br>0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0<br>1−specificity 1−specificity<br>1.0 1.0<br>0.8 0.8<br>Sensibility 0.60.4 Sensibility 0.60.4<br>0.2 0.2<br>0.0 0.0<br>**----- End of picture text -----**<br>


Figure 5.2 Fruit juice data: ROC curve for logistic model. Vertical dotted line in left panel: threshold 2[1][in allocation rule.] 

One way of introducing this tool refers to the previous question on the threshold at which to discriminate customers. Let us imagine that company CH wants to acquire new customers, and a prediction error of MM customers is very worrying; we want to highlight the predictive ability of this set. We return to the response provided by the model in terms of the values of estimated probability. These fall in the interval (0 _,_ 1), and we simplify it by dichotomizing it with respect to a threshold. One way of scaling such a threshold is to order units according to the probability assigned by the model and then verify whether the parts of the units with a greater predicted probability are those that do correspond to greater frequency of events—in this example, by choosing MM. 

Figure 5.3 shows the results of such an operation, with two variants. In both panels, the left-most points of the line correspond to sets of customers for whom the estimated probability is higher, and the _y_ -axis represents the proportion of observed purchasers of MM of those customers, divided by the average proportion calculated on all the data. The left panel shows the calculation made for every possible fraction of subjects, ordered according to estimated probabilities; the right panel shows a smooth form of the same curve, in which the calculated points refer to fractions of 10%, 20%, …, 100% of the data. The smooth variant is more commonly used, both to obtain a more regular trend and for computational simplicity. 

Both panels of figure 5.3 also show a vertical dotted line, which corresponds to the classification of subjects with the probability of the indicated value as a threshold. For every fixed value of this threshold, a misclassification table is identified, of the type presented in table 5.4, from which, we can extract the _y_ -axis of the lift curve for event +, represented by 

**==> picture [32 x 26] intentionally omitted <==**

In table 5.3 constructed with threshold[1] 2[, the] _[ y]_[-axis of the lift curve for “purchase] of MM” is (76 _/_ 95) _/_ (99 _/_ 268) = 2 _._ 17, which is the observed value on figure 5.3 

**==> picture [331 x 179] intentionally omitted <==**

**----- Start of picture text -----**<br>
142 D A T A A N A L Y S I S A N D D A T A M I N I N G<br>Threshold=0.5 Threshold=0.5<br>0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0<br>Fraction of predicted subjects Fraction of predicted subjects<br>2.5 2.5<br>2.0 2.0<br>Improvement factor 1.5 Improvement factor 1.5<br>1.0 1.0<br>**----- End of picture text -----**<br>


Figure 5.3 Fruit juice data. Lift curve for logistic model. Left: curve calculated for every fraction of subjects; right: curve calculated for grouped data. 

where the vertical dotted line crosses the lift curve. In the right panel, the value of the _y_ -axis is subject to approximation because we constructed the lift curve by reorganizing the data into 10 groups. 

To better appreciate the value of the information in this type of graph, and also the reason for the term _lift_ , we refer to an example of a different type. Imagine that a company wants to promote a product to already known customers who are contacted individually—for example, by mail. For cost reasons, the company decides to send a limited number _N_ of letters, and therefore the problem arises of which customers to send them to. 

The trivial option, without taking advantage of any information about customers, is to send letters to _N_ customers chosen at random. Instead, let us use a logistic regression model for the probability of responding positively to the promotion, constructed according to available data, following analogous promotional actions in the past. Clearly, if we take advantage of the indications of the model, we send letters to those _N_ subjects who have a higher probability of responding positively. 

The lift curve of this model allows us to quantify the _expected improvement_ of the logistic model with respect to random choice. At _x_ , that is, the proportion between _N_ and the size of the customer base, point _y_ of the lift curve represents the ratio between the probability of success in reaching the customers selected by the model and a randomly chosen set. 

A further observation regarding the asymmetry of the behavior of lift with respect to the choice of “favorable” or “unfavorable” events: different graphs are obtained if we invert the choice of the event in question. 

## 5.3 EXTENSION TO SEVERAL CATEGORIES 

## 5.3.1 Multivariate Logit and Multinomial Regression 

The case _K >_ 2 may be treated by extending the previous method as follows. If we call the _K_ classes 0 _,_ 1 _, . . . , K_ − 1, and denote by _πk_ ( _x_ ) the probability that 

Methods of Classification 

143 

_Y_ = _k_ by the fixed value of _x_ , with[�] _k[K]_ =[−] 0[1] _[π][k]_[(] _[x]_[)][ =][ 1, we assume that] 

**==> picture [205 x 27] intentionally omitted <==**

holds, where _ηk_ ( _x_ ) is a linear combination of the covariates, of type _β_ 0 + _x_[⊤] _β_ , where the components of vector _β_ vary with _k_ , for _k_ = 1 _, . . . , K_ − 1. A simple algebraic manipulation leads us to write 

**==> picture [128 x 33] intentionally omitted <==**

and, therefore, adding 1 to both sides, 

**==> picture [275 x 71] intentionally omitted <==**

These relations extend (2.41), and the derived model is called a _multivariate logistic regression model_ . In principle, each of functions _ηk_ ( _x_ ) may use different covariates, but conceptually the substance does not change. 

The _p_ ( _K_ − 1) parameters of this model may be estimated by fitting _K_ − 1 logistic regression models. Each of these is applied to compare classes 0 and _k_ , conditional on the fact that the subject belongs to one of these two classes. Because 

**==> picture [297 x 27] intentionally omitted <==**

it is immediately verified that the parameters estimated in this way are those of interest for the multivariate model. 

A different estimation strategy is based on the assumption that _π_ 0( _x_ ) _, π_ 1( _x_ ) _, . . . , πK_ −1( _x_ ) in (5.3) are the parameters of _multinomial_ distribution, which specifies the probability of each way of allocating _n_ observations in _K_ categories. The estimates are obtained by numerically maximizing the log-likelihood function, which is proportional to 

**==> picture [201 x 33] intentionally omitted <==**

where _y_ 0 _, . . . , yK_ −1 represent the number of observed events for each category. In this case, the model is called _multinomial_ (or _polytomous_ ) _logit_ . 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

144 

_Table 5.5._ BANK DATA: SUMMARY OF MULTINOMIAL LOGIT MODEL, WITH LINEAR (TOP) AND QUADRATIC (BOTTOM) EFFECTS OF AGE. STANDARD ERROR VALUES IN BRACKETS 

Model with linear age effect 

|Logit|(Intercept)|Age|Car possession|
|---|---|---|---|
|log(_π_1_/π_0)|−0.973 (0.744)|0.0358 (0.0153)|−0.916 (0.483)|
|log(_π_2_/π_0)|0.373 (0.617)|0.0099 (0.0124)|0.047 (0.439)|
|log(_π_3_/π_0)|−0.737 (0.597)|0.0510 (0.0122)|−0.795 (0.406)|



_D_ = 1164 _._ 493 with 9 d.f. 

Model with quadratic age effect 

|Logit|(Intercept)|Age|Age2|Car possession|
|---|---|---|---|---|
|log(_π_1_/π_0)|3.07 (0.0009)|−0.171 (0.0198)|0.0024 (0.0004)|−0.8939 (0.043)|
|log(_π_2_/π_0)|2.97 (0.0031)|−0.125 (0.0170)|0.0016 (0.0003)|0.0523 (0.110)|
|log(_π_3_/π_0)|3.98 (0.0030)|−0.177 (0.0169)|0.0027 (0.0003)|−0.7620 (0.168)|



_D_ = 1156 _._ 30 with 12 d.f. 

Note that in (5.2) the choice of 0 as reference class, called baseline category, is arbitrary but irrelevant in that we could use any other class for this aim, and the probabilities resulting from (5.3) would remain unchanged. 

For a numerical illustration, we analyze the Brazilian bank data (described in section B.3 and already used in section 2.3.3), examining the satisfaction of the bank’s customers as a categorical variable with four categories, modeled as a function of customer age and an indicator of car ownership. Table 5.5 lists the estimate operations of a multinomial logit model, with satisfaction level 4 as baseline category. 

For a given age, the estimated odds that customers not possessing a car have a satisfaction level of 1 instead of 4 are exp(−0 _._ 92) = 0 _._ 40 times the estimated odds for customers possessing a car; the Wald 90% confidence interval is exp(−0 _._ 92 ± 1 _._ 64 × 0 _._ 483) = (0 _._ 18 _,_ 0 _._ 88). For example, the age effect indicates that the estimated odds that satisfaction level is 1 instead of 4 are relatively higher for older customers. The left part of figure 5.4 plots the estimated probabilities that satisfaction level is 1, 2, 3, or 4 as a function of age, for customers owning a car. 

We also consider a model in which a quadratic component for age is added. The lower part of table 5.5 lists these estimates and the right part of figure 5.4 plots the estimated probabilities for the four satisfaction levels as a function of age. Figure 5.5 plots the distributions of the predicted probabilities that the response variable falls in each category with the model that includes the quadratic component of age. 

## 5.3.2 Ordinal Categorical Variables and Cumulative Logit Models 

Sometimes, as in the case of customer satisfaction in the Brazilian bank example, the categorical response variable is ordinal but the multinomial logit model does 

**==> picture [330 x 160] intentionally omitted <==**

**----- Start of picture text -----**<br>
Satisfaction level 4<br>Satisfaction level 4<br>Satisfaction level 3<br>Satisfaction level 3<br>Satisfaction<br>level 1<br>Satisfaction level 1<br>Satisfaction level 2 Satisfaction level 2<br>20 30 40 50 60 70 20 30 40 50 60 70<br>Age Age<br>1.0 1.0<br>0.8 0.8<br>0.6 0.6<br>0.4 0.4<br>Predicted probabilities Predicted probabilities<br>0.2 0.2<br>0.0 0.0<br>**----- End of picture text -----**<br>


Figure 5.4 Bank data: Estimated probabilities with a multilnomial logit model. Left: satisfaction levels with linear age effect; right: with quadratic effect. 

**==> picture [307 x 322] intentionally omitted <==**

**----- Start of picture text -----**<br>
Level 1<br>0.0 0.2 0.4 0.6 0.8 1.0<br>Level 2<br>0.0 0.2 0.4 0.6 0.8 1.0<br>Level 3<br>0.0 0.2 0.4 0.6 0.8 1.0<br>Level 4<br>0.0 0.2 0.4 0.6 0.8 1.0<br>Predicted probability<br>6<br>5<br>4<br>3<br>2<br>Density<br>1<br>0<br>8<br>6<br>4<br>Density 2<br>0<br>5<br>4<br>3<br>2<br>Density 1<br>0<br>5<br>4<br>3<br>2<br>Density<br>1<br>0<br>**----- End of picture text -----**<br>


Figure 5.5 Bank data: Distribution of predicted probabilities for each satisfaction level with a multinomial logit model with quadratic age effect. 

146 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

not take this information into account. Models for ordinal responses may be introduced for simpler interpretation and potentially greater precision. 

Considering an ordered response variable, for each category we define as _cumulative probabilities_ the probabilities that response variable _Y_ belongs to a class not higher than the nominated category 

**==> picture [226 x 10] intentionally omitted <==**

A model for cumulative logits 

**==> picture [194 x 27] intentionally omitted <==**

automatically incorporates category order. The simplest model of this type is the _proportional odds model_ , in which an identical effect of the explanatory variable is assumed for all _K_ − 1 cumulative probabilities 

**==> picture [287 x 43] intentionally omitted <==**

where _η_ ( _x, k_ ) = _β_ 0 _k_ − _β_ 1 _x_ 1 − _. . ._ − _βpxp_ . The choice of the negative sign preceding _βj_ is conventional and is adopted for easier interpretation of the parameters, as will be made clear shortly. Here, each cumulative logit has its own intercept _β_ 0 _k_ , but effects _βj_ of the _j_ th covariate, for _j_ = 1 _, . . . , p_ , are the same for all categories. 

Model (5.5) satisfies the property 

**==> picture [197 x 70] intentionally omitted <==**

where _x_[′] = ( _x_ 1[′] _[, . . . ,][ x][p]_[′][)][and] _[x]_[′′][=][(] _[x]_ 1[′′] _[, . . . ,][ x][p]_[′′][)][are][two][points][of][covariate] space and, in this case, a notation of the type P� _Y_ ≤ _k_ | _x_ ′�) makes explicit the dependence on _x_ that was implicit previously. This means that the odds of making response _Y_ ≤ _k_ when the covariates assume value _x_[′] are exp{ _β_ 1( _x_ 1[′′][−] _[x]_ 1[′][)][ +] _[ . . .]_[ +] _βp_ ( _xp_[′′] − _xp_[′] )} times the odds at _x_ = _x_[′′] . The log cumulative odds ratio is therefore proportional to the distance between the two points _x_[′] and _x_[′′] . This is why the model is called _proportional odds model_ . 

The equivalent model expression for cumulative probabilities is 

**==> picture [240 x 27] intentionally omitted <==**

Methods of Classification 

147 

**==> picture [237 x 202] intentionally omitted <==**

**----- Start of picture text -----**<br>
P  ( y  ≤ 3)<br>P  ( y ≤ 2)<br>P  ( y  ≤1)<br>x<br>1.0<br>0.8<br>k ) 0.6<br> ≤<br>P  ( y<br>0.4<br>0.2<br>0.0<br>**----- End of picture text -----**<br>


Figure 5.6 Cumulative probabilities in a proportional odds model. Each curve corresponds to a category. 

and the single category probabilities are 

**==> picture [244 x 27] intentionally omitted <==**

Figure 5.6 shows an example of the trend of P{ _Y_ ≤ _k_ } for a proportional odds model versus one covariate, all other explanatory variables being given. 

By hypothesizing multinomial distribution for independent observations, estimates are obtained by maximizing the log-likelihood 

**==> picture [297 x 53] intentionally omitted <==**

Note that models based on cumulative probabilities can use a link function other than a logit. Models belonging to this broad family are usually called “cumulative link models.” They are characterized by an interesting interpretation, which considers the response categorical variable as a discretization of an underlying continuous variable. If _Y_[∗] denotes such a latent variable, we consider the model for _Y_[∗] as a function of _x_ 

**==> picture [228 x 14] intentionally omitted <==**

where we assume that _ε_ has a distribution function _G_ (·), with E{ _ε_ } = 0. If −∞= _β_ 00 _< β_ 01 _<_ · · · _< β_ 0 _K_ −1 _< β_ 0 _K_ = ∞ are _cut-points_ or _thresholds_ on 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

148 

a continuous scale, we assume that 

**==> picture [250 x 12] intentionally omitted <==**

This means that 

**==> picture [266 x 14] intentionally omitted <==**

and, equivalently, 

**==> picture [198 x 14] intentionally omitted <==**

It is now clear why we adopted the negative sign for the _βj_ in (5.5). Negative signs in (5.5) correspond to positive signs in (5.6), so that the parameters have the usual directional interpretation—that is, if _βj_ is positive, then _Y_ is more likely to assume high values as _xj_ increases. 

If _G_ ( _ε_ ) = e _[ε] /_ (1 + e _[ε]_ ) = _ℓ_ ( _ε_ )—that is, if _G_ is the standard logistic distribution— _G_[−][1] is the logit link function and the model is a proportional odds model (5.5). Other latent distributions are implied by different link functions: for example, if _ε_ is Gaussian, _G_[−][1] is the _probit_ link function, the inverse of the normal distribution function. 

To illustrate the proportional odds model, we analyze the Brazilian bank data. We consider the simple model with only age and car possession as predictors. Table 5.6 lists the estimates for the proportional odds model. For each parameter, the 95% level Wald confidence interval is adopted. Analyzing these confidence intervals, we observe that the interval for car possession includes 0, so we are led to test the hypothesis that this parameter is null. The likelihood ratio test statistic is 2(log _L_ 1 − log _L_ 0), where _L_ 0 is the maximized log-likelihood function under the null hypothesis constraint that _β_ car = 0, and _L_ 1 is the maximized log-likelihood function without that constraint. The observed test statistic, 1185 _._ 64 − 1182 _._ 31 = 3 _._ 33 on 1 degree of freedom, leads to an observed significance level of 0 _._ 068, suggesting that we could eliminate the variable car possession from the model. 

The lower part of table 5.6 lists the proportional odds model with only age as a covariate. The top part of figure 5.7 plots the estimated probabilities for the 4 satisfaction levels as functions of age, and the bottom part shows the distributions of predicted probabilities for each category. 

## _Bibliographical notes_ 

Fahrmeir & Tutz (2001) deal with GLM in the multidimensional case, including extension of logistic regression to the multivariate case, totreatcategoricalvariables with more than two levels. 

Multinomial classification models and cumulative odds models are also discussed in many works on categorical data analysis, for example, Agresti (2002) and, specifically for ordinal categorical data, Agresti (2010). For a discussion of GLM, including a presentation of proportional odds models, see McCullagh & Nelder (1989). 

Methods of Classification 

149 

_Table 5.6._ BANK DATA: PROPORTIONAL ODDS VERSION OF CUMULATIVE LOGIT MODEL WITH LINEAR EFFECT OF AGE. Intercept 1|2, Intercept 2|3, Intercept 3|4: PARAMETERS _β_ 01 _, β_ 02 _, β_ 03 

|||||Wald 95%|Wald 95%|
|---|---|---|---|---|---|
||Estimate|SE|_t_-value|conf. limits||
|Model with age and||||||
|car possession||||||
|(Intercept 1|2)|−0.5803|0.3569|−1.6256|−1.2798|0.1193|
|(Intercept 2|3)|0.1778|0.3499|0.5081|−0.5080|0.8636|
|(Intercept 3|4)|1.5289|0.3560|4.2951|0.8312|2.2265|
|age|0.0386|0.0068|5.6450|0.0252|0.0519|
|car possession|−0.4080|0.2259|−1.8060|−0.8508|0.0348|
|_D_=1182.31 with 5 d.f.||||||
|Model with age only||||||
|(Intercept 1|2)|−0.2901|0.3187|−0.9105|−0.9147|0.3344|
|(Intercept 2|3)|0.4678|0.3110|1.5041|−0.1418|1.0774|
|(Intercept 3|4)|1.8137|0.3198|5.6719|1.1870|2.4405|
|age|0.0374|0.0068|5.5240|0.0242|0.0573|



_D_ = 1185.64 with 4 d.f. 

## 5.4 CLASSIFICATION VIA LINEAR REGRESSION 

We tackled our first problem of classification with a fairly simple and familiar method: logistic regression. There are more sophisticated methods, but we now move on to another, which is even simpler and more familiar: linear regression. After all, simple methods often give very good results. 

## 5.4.1 Case with Two Categories 

We start by considering the case with _K_ = 2 classes, 0 and 1. We introduce a linear regression model in which response variable _y_ is formed exactly of labels ˆ 0 and 1 of the two classes, and value _y_ = 2[1][is][the][discriminatory][threshold][for] predicting the two categories. 

To illustrate the method, consider the artificial data of the two parts of figure 5.8. Here, we have two continuous covariates _z_ 1 and _z_ 2, and membership of the points to the two groups is distinguished by the symbol used. There are 120 points in one category and 80 in the other. 

The simplest form of linear regression we can consider is 

**==> picture [225 x 12] intentionally omitted <==**

It is important to note that the nature of _ε_ as implied here is truly original, in the sense that it must be a random variable, so that its value added to the deterministic part gives 0 or 1. However, the really crucial assumption for the least squares criterion to provide reasonable results is that E{ _ε_ } = 0, but in fact 

**==> picture [226 x 477] intentionally omitted <==**

**----- Start of picture text -----**<br>
Satisfaction level 4<br>Satisfaction level 3<br>Satisfaction level 1<br>Satisfaction level 2<br>20 30 40 50 60 70<br>Age<br>Level 1<br>0.0 0.2 0.4 0.6 0.8 1.0<br>Level 2<br>0.0 0.2 0.4 0.6 0.8 1.0<br>Level 3<br>0.0 0.2 0.4 0.6 0.8 1.0<br>Level 4<br>0.0 0.2 0.4 0.6 0.8 1.0<br>Predicted probability<br>1.0<br>0.8<br>0.6<br>0.4<br>Predicted probabilities<br>0.2<br>0.0<br>6<br>4<br>2<br>Density<br>0<br>8 10<br>6<br>4<br>Density 2<br>0<br>12<br>Density 2 4 6 8<br>0<br>5<br>4<br>3<br>2<br>Density 1<br>0<br>**----- End of picture text -----**<br>


Figure 5.7 Bank data: Proportional odds version of cumulative logit model. Top: estimated probabilities of satisfaction levels with linear effect of age; bottom: distributions of predicted probabilities for each satisfaction level. 

Methods of Classification 

151 

**==> picture [328 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
−4 −2 0 2 −4 −2 0 2<br>z 1 z 1<br>2 2<br>0 0<br>2 2<br>z z<br>−2 −2<br>−4 −4<br>**----- End of picture text -----**<br>


Figure 5.8 Simulated data with two groups. Left: classification with simple regression; right: classification with quadratic regression. 

this requirement is automatically satisfied when the model includes an intercept, because any nonzero value can be included in _β_ 0. 

After least squares estimation, the R[2] plane is divided into two parts by the line 

**==> picture [225 x 14] intentionally omitted <==**

where self-explanatory notation is used. This is the line plotted in the left part of figure 5.8. 

Elaborating on this formulation, we can extend the process by inserting nonlinear functions of _z_ 1 and _z_ 2 into the linear predictor. The simplest choice is that of polynomial functions—for example, the quadratic form 

**==> picture [197 x 13] intentionally omitted <==**

After estimation of the parameters, equating the resulting function to[1] 2[leads to] subdivision of R[2] , indicated by the separation curve in the right part of figure 5.8. 

We now apply this procedure to the fruit juice data, using the variables already shown in figure 5.1. Obviously, with many variables in play, it is not possible to produce a plot like that of figure 5.8. The misclassification table in the test sample is identical to that in table 5.3, and so are the error percentages. The lift and ROC curves are practically indistinguishable from those of the logistic model and are therefore not shown. However, figure 5.9 shows the scatterplot of logit( ˆ _π_ ) of the fitted logistic model, with respect to the predicted values according to the linear model. This reveals astonishing agreement between the two classification rules, at least for threshold value[1] 2[,][which][corresponds][to][0][on][the][logit][scale.] The essential equivalence of the two methods is quite common, although not an absolute rule. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

152 

**==> picture [258 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>
−4 −2 0 2<br>Logit (probability) predicted by logistic model<br>1.0<br>0.8<br>0.6<br>0.4<br>0.2<br>Predicted values with linear model<br>0.0<br>−0.2<br>**----- End of picture text -----**<br>


Figure 5.9 Fruit juice data: Scatterplot of logit( _π_ ˆ ) predicted by fitted logistic model and values predicted by linear model. 

## 5.4.2 Case with Several Categories 

The case of _K >_ 2 can be tackled with an extension of the previous process combined with the multivariate linear model described in section 2.1.3. We construct the _n_ × _K_ dimension matrix _Y_ made by the indicator variables of the levels of _y_ . The columns of _Y_ are linearly dependent, in the sense that the sums of each row are identically equal to 1, but in this case it is convenient not to eliminate a column. We can therefore arrange multivariate multiple linear regression of the type (2.20), 

_Y_ = _X B_ + _E,_ 

where _X_ represents design matrix _n_ × _p_ and _B_ the _p_ × _K_ of the parameters. For the columns of error matrix _E_ , the comments made for _ε_ in (5.7) hold. 

Once matrix _B_ has been estimated by (2.21), we can allocate a new point _x_ 0 ( _x_ 0 ∈ R _[p]_ ) to one of the classes, calculating 

**==> picture [45 x 14] intentionally omitted <==**

and assigning _x_ 0 to the class for which component ˆ _y_ 0 is greater ( _y_ ˆ0 ∈ R _[K]_ ). 

For numerical illustration, we can refer to figure 5.10, showing three groups of simulated data, of which two coincide with those in figure 5.8 and the new set has 100 points. The two panels of figure 5.10 correspond to those of figure 5.8 in the 

Methods of Classification 

153 

**==> picture [326 x 158] intentionally omitted <==**

**----- Start of picture text -----**<br>
−4 −2 0 2 −4 −2 0 2<br>z 1 z 1<br>2 2<br>0 0<br>2 2<br>z z<br>−2 −2<br>−4 −4<br>**----- End of picture text -----**<br>


Figure 5.10 Simulated data with three groups. Left: classification with linear regression; right: classification with quadratic regression. 

sense that a regression plan is used for the former and a second-degree polynomial for the latter. 

## 5.4.3 Discussion 

Using linear models for classification purposes is somewhat unnatural. The domain of _y_ is {0 _,_ 1}, which does not fit the logical set-up of least squares because a linear regression function does not remain constrained within this set. One consequence of this was already mentioned when the nature of error term _ε_ of (5.7) was discussed. In turn, this nature causes difficulty in using inferential methods: the usual hypothesis of homoscedasticity is not guaranteed in this case. Therefore, the usual standard errors and other inferential procedures are not fully sustained by a fixed theory, although some numerical tests give comforting indications in the sense that approximate standard errors are essentially valid. 

It is appropriate here to remark on the interpretation of the model parameters. Because labels 0 and 1 are conventional, parameters vary if we choose other labels. As for the nonconstant terms of the linear predictor, the estimate of the parameter and the corresponding standard error vary in proportion, so the overall interpretation is not modified. However, the intercept has a purely arbitrary value: it changes simply if other values are used for the classes, for example, −1 and 1, the associated standard errors change appreciably, and so do the observed significance levels of the parameters. However, the constant term in the linear model is needed to guarantee that E{ _ε_ } = 0 for every label choice, and it must therefore be maintained. 

A particular problem of this approach comes from the possible “masking” of a class, in the sense that we can construct a classification rule for which a new individual will never be allocated to a certain class: this class is masked by the others. For a more detailed illustration of the problem, see Hastie et al. (2009, p. 105). The remedy is to consider polynomial expressions of the explanatory variables in the linear predictor up to order _K_ − 1, which involves _O_ ( _p[K]_[−][1] ) terms. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

154 

To conclude, we list the advantages and disadvantages of this approach. 

## _Advantages_ 

- Familiarity of the method: linear regression is one of the most widespread and familiar statistical tools. 

- Computational simplicity: the computational side is noniterative, with minimal computational complexity. The recursive updating formulas of algorithm 2.2 can be used, thus allowing real-time applications. 

- Effectiveness: in spite of its simplicity, the method produces satisfactory results, competitive with more sophisticated ones. 

## _Disadvantages_ 

- Improper use of the linear model: the domain of _y_ is in no way similar to the set of values of a linear function. 

- Masking problems: if we are not careful, we risk masking a class. 

- Difficulties with inferential aspects: there is no completely satisfactory theoretical basis to support inferential processes. 

Apart from these aspects, there are the standard considerations about using a parametric method, in both positive and negative senses. 

## 5.5 DISCRIMINANT ANALYSIS 

## 5.5.1 General Remarks 

Linear regression and logistic regression are not really tools specifically designed for classification. “Proper” treatment of the problem follows the procedure shown next, in which we refer to a _p_ -dimensional random variable _X_ , assumed for the moment to be continuous, and a random categorical variable _Y_ , which represents the class to which a subject belongs. 

The total population is made up of _K_ subpopulations (classes), having probability density functions _p_ 0( _x_ ) _, . . . , pK_ −1( _x_ ) for the conditional distribution of _X_ , and weights _π_ 0 _, . . . , πK_ −1 with respect to the total population ([�] _k[π][k]_[=][ 1).] Therefore, marginal density in the total population is 

**==> picture [211 x 33] intentionally omitted <==**

For the moment, we argue as if the various ingredients of _p_ ( _x_ ) were known. A priori, the probability that a still unclassified subject belongs to the _k_ th subpopulation is given by _πk_ . For this subject, if the observed value of _X_ is _x_ 0, then by Bayes theorem the a posteriori probability that this subject belongs to group _k_ is given by 

**==> picture [129 x 27] intentionally omitted <==**

Methods of Classification 

155 

or, equivalently, comparison of probability between class _k_ and class _m_ takes place according to 

**==> picture [202 x 27] intentionally omitted <==**

We therefore compare the various classes through the _discriminant function_ 

**==> picture [123 x 12] intentionally omitted <==**

linked to the posterior probability of the classes. The value of _k_ that maximizes the discriminant function selects the group to which we assign the new subject. 

This constitutes the framework of _discriminant analysis_ . However, to make the process operative, we must know and therefore estimate from the data the ˆ ingredients of (5.9). Regarding _πk_ , it is natural to estimate it as _πk_ = _nk/n_ , unless wehave further information. However, there are variousapproacheswecantakefor _pk_ ( _x_ ):parametricornonparametric;theformerincludesvariousoptionsrelatingto the family of density functions to be considered, and the latter various alternatives among estimation methods. 

From now on, we develop the more classical procedure, that of Fisher (1936), which are placed within the parametric environment. We do not deal with the nonparametric approach, as it has not yet found widespread application, both because it does not lend itself easily to combining quantitative and qualitative variables and because it falls quite rapidly into the curse of dimensionality, and therefore is not suitable for dealing with the problems that interest us here. 

## 5.5.2 Linear Discriminant Analysis 

For discriminant analysis, the simplest parametric hypothesis is that in which each density _pk_ ( _x_ ) is multivariate normal with parameters dependent on _k_ , say, _Np_ ( _μk, �k_ ), which results in 

**==> picture [315 x 25] intentionally omitted <==**

for _k_ = 0 _, . . . , K_ − 1. For a brief recap of multivariate normal distribution, see appendix A.2.3. 

In the simplified case, in which all the variance matrices are equal to the same _�_ , the discriminant function takes the form 

**==> picture [183 x 14] intentionally omitted <==**

which is a linear function of _x_ , leading to its name, _linear discriminant analysis_ (LDA). 

156 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

**==> picture [318 x 156] intentionally omitted <==**

**----- Start of picture text -----**<br>
−4 −2 0 2 −4 −2 0 2<br>z 1 z 1<br>2 2<br>0 0<br>2 2<br>z z<br>−2 −2<br>−4 −4<br>**----- End of picture text -----**<br>


Figure 5.11 Simulated data with three groups: Classification with linear discriminant analysis for two sets of variables given in (5.11). 

Parameter estimation poses no difficulties because it is immediate to set 

**==> picture [285 x 35] intentionally omitted <==**

where denominator _n_ − _K_ follows from the same logic of the denominator of (2.11), and _xi_ denotes the value of _X_ taken on the _i_ th sample unit. Therefore, the total number of estimated parameters is _p K_ + _p_ ( _p_ + 1) _/_ 2. 

Consider the simulated data of figure 5.10 and use them as in section 5.4 adopting the same linear predictor. Figure 5.11 was made with the general term _xi_ of the type 

**==> picture [293 x 14] intentionally omitted <==**

for the left and right panels, respectively, and therefore they have _p_ = 2 and _p_ = 5 components. Here, _zi_ 1 indicates the _i_ th observation of _z_ 1, and analogously for _zi_ 2. 

However, we can reach the linear discriminant function just indicated without the multivariate normality assumption simply by using second-order assumptions. This justifies using the technique even when _X_ is not a multivariate normal variable, and it may in fact have noncontinuous components. The development of LDA through the second-order hypothesis was the original path followed by Fisher (1936), but for simplicity of explanation, it is easier to follow the framework based on normal distribution. 

## 5.5.3 Quadratic Discriminant Analysis 

If we remove the condition that the _K_ variance matrices in (5.10) are equal, we obtain the discriminant function 

**==> picture [240 x 15] intentionally omitted <==**

Methods of Classification 

157 

**==> picture [329 x 159] intentionally omitted <==**

**----- Start of picture text -----**<br>
−4 −2 0 2 −4 −2 0 2<br>z 1 z 1<br>2 2<br>0 0<br>2 2<br>z z<br>−2 −2<br>−4 −4<br>**----- End of picture text -----**<br>


Figure 5.12 Simulated data with three groups: classification with quadratic discriminant analysis for two sets of variables given in (5.11). 

which is a quadratic function in _x_ , and the corresponding procedure is therefore called _quadratic discriminant analysis_ (QDA). 

The estimate of average vectors _μk_ is the same as that given in the previous section, whereas the estimate of _�k_ is given by 

**==> picture [173 x 31] intentionally omitted <==**

and there are therefore a total of _K p_ + _K p_ ( _p_ + 1) _/_ 2 distinct estimated parameters. 

Applying this procedure to the data used earlier and employing the same transformations of variables _z_ 1 and _z_ 2 in the components of _x_ , we obtain the classification regions shown in figure 5.12. Figure 5.13 displays the lift and ROC curves of the LDA and QDA. 

It is important to emphasize that unlike LDA, QDA is closely linked to the Gaussian distributive hypothesis. However, the second diagram was produced by violating this assumption, as it cannot be true that _z_ 1[2][and] _[z]_ 2[2][have][normal] distribution, not even approximately, because _z_ 1 and _z_ 2 assume values around 0. In spite of this, the regions have reasonable shapes. 

Let us now apply these two variants of discriminant analysis to the fruit juice data, in both cases using the linear predictor of (5.1). From table 5.7 we obtain the total misclassification percentages, which are 42 _/_ 268 = 0 _._ 157 and 46 _/_ 268 = 0 _._ 172, for the linear and quadratic variants, respectively. Note that in this case, the misclassification error of QDA is larger than that of LDA, highlighting the fact that a more complicated model does not always give better results. 

## 5.5.4 Discussion 

_Advantages_ 

- Appropriateness of the method: the method was specifically developed for the classification problem; it is not an adaptation of a procedure designed for a different aim. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

158 

_Table 5.7._ FRUIT JUICE DATA: MISCLASSIFICATION TABLE OF LINEAR AND QUADRATIC DISCRIMINANT ANALYSIS ON TEST SET 

|Prediction with LDA<br>CH<br>MM<br>Total|Actual response<br>CH<br>MM<br>Total<br>147<br>20<br>167<br>2<br>79<br>101<br>169<br>99<br>268|
|---|---|
|Prediction with QDA<br>CH<br>MM<br>Total|145<br>22<br>167<br>24<br>77<br>101<br>169<br>99<br>268|



**==> picture [330 x 163] intentionally omitted <==**

**----- Start of picture text -----**<br>
LDA LDA<br>QDA QDA<br>0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0<br>Fraction of predicted subjects 1−specificity<br>1.0<br>2.5<br>0.8<br>2.0 Sensibility 0.60.4<br>Improvement factor 1.5<br>0.2<br>1.0 0.0<br>**----- End of picture text -----**<br>


Figure 5.13 Fruit juice data. Left: lift curve; right: ROC curve for discriminant analysis. 

- A priori information: if available, this can easily be included in the prior probability of the subpopulation. 

- Simplicity of calculation: both parameter estimates and calculation of discriminant functions are extremely simple from a computational viewpoint, and the procedure lends itself well to real-time applications. 

- Quality and stability of results: years of accumulated experience on discriminant analysis have shown that the method is highly reliable and produces results that are valid in a large number of cases and stable with respect to new data inputs. 

- Robustness with respect to the hypotheses: even when the assumptions of the method are not satisfied, the method tends to produce valid results. 

Methods of Classification 

159 

## _Disadvantages_ 

- Restrictive hypotheses: the method is constructed under quite detailed hypotheses. 

- Selection and grading of variables: there are no simple techniques to examine whether a certain variable can be removed without much loss, apart from the universal method of testing on a test set. The same applies to the similar problem of identifying an order of importance among variables. 

- Number of parameters: when _p_ and/or _K_ are not small, QDA brings about a rapid increase in the number of parameters. In particular, when _nk_ is small, some covariance matrices _�k_ may not be identifiable—that is, their estimates may turn out to be singular. 

- Nonrobustness of estimates: the estimates of the required parameters are very quickly calculated with the method of moments, but for this very reason they are not robust when outlying observations occur. However, forms of robust estimates exist. 

## _Bibliographical notes_ 

Discriminant analysis was introduced by Fisher (1936). Classic works on classification problems, with a presentation of discriminant analysis, are those of Mardia et al. (1979, ch. 11), Hand (1981, 1982), and McLachlan (1992). A work with a statistical approach but with emphasis on the area of machine learning is that of Ripley (1996). 

## 5.6 SOME NONPARAMETRIC METHODS 

Up to now, we have only dealt with parametric methods, but it is also worth exploring nonparametric ones. In the remaining part of this chapter, we consider some of the options, which mainly consist of adapting the matching procedures discussed in chapter 4 to classification problem. 

The _k_ -nearest-neighbor estimator (section 4.2.4) is easily generalized to the classification framework by considering, for every fixed point _x_ 0, neighborhood _Nk_ ( _x_ 0), including the _k_ points closest in distance to _x_ 0 and classifying _x_ 0 according to a majority vote among _k_ neighbors. 

As in the case of regression, number _k_ is a tuning parameter related to the “complexity” of the model. Figure 5.14 shows the classification results obtained by applying _k_ -nearest-neighbors with _k_ = 1 and _k_ = 50 to the simulated data already used in figure 5.8. 

Several nonparametric regression techniques can be adapted to the classification problem, considering the indicator variable that identifies the membership class of each unit as a response variable. To relate this response variable to covariates, exactly as in GLM, we use a link function that transforms the scale of the nonparametric predictor into that of the response variable. For example, where _K_ = 2, the link function is again logit function (2.43), and the nonparametric predictor is an unknown function _f_ yielding 

**==> picture [141 x 27] intentionally omitted <==**

160 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

**==> picture [327 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
−4 −2 0 2 −4 −2 0 2<br>z 1 z 1<br>2 2<br>0 0<br>2 2<br>z z<br>−2 −2<br>−4 −4<br>**----- End of picture text -----**<br>


Figure 5.14 Simulated data with two groups classification with _k_ -nearest-neighbors. Left: _k_ = 1; right: _k_ = 50. 

**==> picture [328 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
−4 −2 0 2 −4 −2 0 2<br>z 1 z 1<br>2 2<br>0 0<br>2 2<br>z z<br>−2 −2<br>−4 −4<br>**----- End of picture text -----**<br>


Figure 5.15 Simulated data with two groups: Classification with loess and a thin plate spline. 

If one or two covariates are available, then the regression function can be estimated in a nonparametric way by one of the techniques described in section 4.2 and section 4.4. Figure 5.15 shows the classification results applying loess and a thin plate spline to the simulated data of figure 5.8. 

Extension to the case of _K_ categories is possible, following the scheme of section 5.3 and using the multilogit function (5.3) as the link function. 

When many covariates are available, as in the regression case, the models must have an albeit weak structure to reduce both conceptual and computational complexity. The generalized additive models, introduced in section 4.5, can be used for classification, with a suitable distribution of the response variable and an appropriate link function. In the case of _K_ = 2, we also use the logit function, 

Methods of Classification 

161 

**Algorithm 5.1** Local scoring for additive logistic model. 

1. Initialization: 

**==> picture [111 x 15] intentionally omitted <==**

- a. if the _yi_ are all 0 or 1, put _β_[ˆ] 0 ← 0 or 1, and the algorithm terminates; 

- b. otherwise, set 

**==> picture [96 x 88] intentionally omitted <==**

where ¯ _y_ is the average of _yi_ . 

**==> picture [208 x 11] intentionally omitted <==**

a. set: 

**==> picture [97 x 46] intentionally omitted <==**

- b. fit an additive model to variable _zi_ with weights _wi_ , using the weighted backfitting algorithm and obtaining new estimates for _β_ ˆ0 and ˆ _fj_ , 

until functions _f_[ˆ] _j_ stabilize. 

which yields 

**==> picture [221 x 34] intentionally omitted <==**

where _π_ is the probability of belonging to class 1. To obtain nonparametric estimates of _fj_ ( _xj_ ), we use a modification of the backfitting algorithm, which in this context is called _local scoring_ and is shown in algorithm 5.1. 

The result of applying the GAM model to the fruit juice data is shown in figure 5.16, where the estimated functions are represented with the smoothing 

**==> picture [303 x 525] intentionally omitted <==**

**----- Start of picture text -----**<br>
230 240 250 260 270 280 1.7 1.8 1.9 2.0 2.1<br>Week PriceCH<br>1.7 1.8 1.9 2.0 2.1 2.2 2.3 0.0 0.1 0.2 0.3 0.4 0.5<br>PriceMM DiscountCH<br>0.0 0.2 0.4 0.6 0.8 0.0 0.2 0.4 0.6 0.8 1.0<br>DiscountMM LoyaltyMM<br>0 1 2 3 4<br>Shop<br>2<br>0.5<br>1<br>0.0 0<br>−0.5 −1<br>−2<br>2 0.0<br>−0.5<br>1 −1.0<br>0 −1.5<br>−2.0<br>−1 −2.5<br>4<br>2.5<br>2.0<br>2<br>1.5<br>1.0 0<br>0.5<br>0.0 −2<br>−0.5<br>0.5<br>0.0<br>−0.5<br>−1.0<br>**----- End of picture text -----**<br>


Figure 5.16 Fruit juice data: Effect of variables on classification with GAM model. For continuous variables, functions _fj_ are estimated by smoothing splines and yield partial effect of each covariate on the response; partial effect of qualitative variable is represented by estimated value for each level. Approximate 95% confidence bands for each function are also shown in different ways for continuous and discrete explanatory variables. 

Methods of Classification 

163 

_Table 5.8._ FRUIT JUICE DATA: TABLE OF ANALYSIS OF VARIANCE FOR GAM MODEL 

|Component|Deviance|d.f.|_p_-value|
|---|---|---|---|
|s(week)|0.20|1.0|0.65|
|s(priceCH)|4.50|3.0|0.21|
|s(priceMM)|0.29|1.0|0.59|
|s(discountCH)|0.85|1.0|0.36|
|s(discountMM)|8.19|3.0|0.04|
|s(loyaltyMM)|0.52|1.1|0.52|
|store|7.44|4.0|0.11|



_Table 5.9._ FRUIT JUICE DATA: CONFUSION MATRIX OF VERIFICATION SAMPLE WITH GAM MODEL 

|Prediction<br>CH<br>MM<br>Total|Actual response<br>CH<br>MM<br>Total<br>147<br>24<br>171<br>22<br>75<br>97<br>169<br>99<br>268|
|---|---|



spline model on the model components. Table 5.8 lists the essential elements of the analysis of variance of the GAM model. Table 5.9 lists the confusion matrix for the resulting classifier, to predict classification on the test set, which gives a global 

Also for MARS (see section 4.4.5), generalizations have been proposed to tackle the classification problem. In the case of _K_ = 2, the simplest route consists of considering the classification variable as a quantitative variable that takes values 0 and 1 and uses the MARS algorithm for the regression. If _K >_ 2, we can recode the response variable into _K_ binary variables and apply the multivariate adaptive regression spline algorithm to each of them, as already seen in the linear model. We then assign each unit to the class that has the highest predicted value for the response variable associated with it. 

Another way of generalizing MARS to the classification problem is PolyMARS, based on the multilogit model. As in the case of regression, the model grows when new basis functions are included, but in this case, a quadratic approximation of the multinomial log-likelihood is used to decide which basis function is to be included at each step. The expanded model is fitted to the data by maximum likelihood. 

The confusion matrix for a PolyMARS model estimated on the fruit juice data is shown in table 5.10. The global misclassification error of this prediction method is 16.4%. Figure 5.17 shows the lift and ROC curves of the same model. 

164 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

_Table 5.10._ FRUIT JUICE DATA: CONFUSION MATRIX OF TEST SET WITH POLYMARS MODEL 

|Prediction<br>CH<br>MM<br>Total|Actual response<br>CH<br>MM<br>Total<br>149<br>24<br>173<br>20<br>75<br>95<br>169<br>99<br>268|
|---|---|



**==> picture [329 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0<br>Fraction of predicted subjects 1−specificity<br>1.0<br>2.5<br>0.8<br>2.0 Sensibility 0.60.4<br>Improvement factor 1.5<br>0.2<br>1.0 0.0<br>**----- End of picture text -----**<br>


Figure 5.17 Fruit juice data: Lift and ROC curves for PolyMARS model. 

## _Bibliographical notes_ 

The reference base for GAM is the work by Hastie & Tibshirani (1990) in which the additive version of the proportional odds model is also discussed. PolyMARS was introduced by Stone et al. (1997). 

## 5.7 CLASSIFICATION TREES 

Let us adapt the idea of regression trees, presented in section 4.8, to the case in which the response variable is _qualitative_ (categorical), with _K_ levels. Figure 5.18 shows a simple case with _p_ = 1 explanatory variables and _K_ = 2. In real operations, we use this approach with larger _p_ (and sometimes larger _K_ ). 

Indicating the two classes by 0 and 1 and the probability that an individual with characteristics _x_ belongs to class 1 by _p_ ( _x_ ) = P{ _Y_ = 1| _x_ }, we approximate _p_ ( _x_ ) by means of a step function of the type 

**==> picture [215 x 35] intentionally omitted <==**

as in (4.15), where _Pj_ now represents the probability that _Y_ = 1 in region _Rj_ . 

Methods of Classification 

165 

**==> picture [244 x 242] intentionally omitted <==**

**----- Start of picture text -----**<br>
0.5 1.0 1.5 2.0 2.5 3.0<br>x<br>1.0<br>0.8<br>0.6<br>y<br>0.4<br>0.2<br>0.0<br>**----- End of picture text -----**<br>


Figure 5.18 Simulated data of a categorical response with two levels and one explanatory variable. 

**==> picture [331 x 169] intentionally omitted <==**

**----- Start of picture text -----**<br>
x < 0.866162<br>|<br>x < 0.714646 x < 2.81061<br>1 1<br>x < 1.04293<br>1<br>x < 2.58333<br>0<br>0 0<br>0.5 1.0 1.5 2.0 2.5 3.0<br>x<br>1.0<br>0.8<br>0.6<br>y<br>0.4<br>0.2<br>0.0<br>**----- End of picture text -----**<br>


Figure 5.19 Simulated data of a categorical response variable with two levels and one covariate: Tree and estimate of _p_ ( _x_ ). 

The resulting tree is of the type shown in figure 5.19 (left) and the estimate of _p_ ( _x_ ) (right). The only difference with respect to figure 4.21 is that a class indicator, which is 0 or 1, is associated with the leaves, instead of the values of function _p_ ( _x_ ). In other words, when we drop a new observation _x_ from the root of the tree to reach a leaf with associated probability _p_ ˆ( _x_ ), this observation is allocated to ˆ class _C_ ( _p_ ( _x_ )), in which _C_ ( _p_ ) = 0 if _p_ ≤[1] 2[, and] _[ C]_[(] _[p]_[)][ =][ 1 if] _[ p][ >]_ 2[1][.] 

166 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

To estimate the _Pj_ of (5.13), we use the arithmetic mean 

**==> picture [174 x 30] intentionally omitted <==**

which is the relative frequency of elements 1 in region _Rj_ . 

Given the binary nature of _y_ , the deviance function as used for the linear model is not the most suitable. A more appropriate choice is the deviance of the binomial distribution 

**==> picture [188 x 31] intentionally omitted <==**

as given in (2.38). The deviance may be rewritten by pooling all units _i_ belonging to region _Rj_ , where the probability is constantly _Pj_ , so that 

**==> picture [244 x 36] intentionally omitted <==**

We reach an interesting interpretation by rewriting the deviance as 

**==> picture [212 x 29] intentionally omitted <==**

which, without constant 2 _n_ , is an average of _entropies_ : 

**==> picture [240 x 47] intentionally omitted <==**

weighted with the relative size of leaves; here, _Pjk_ is the probability of outcome _k_ , which is _Pj_ 1 = _Pj_ and _Pj_ 0 = 1 − _Pj_ . Terms _Q_ (·) are called _impurity_ measures because they indicate that the elements of a certain leaf are nonhomogenous with respect to the response variable. Clearly, _Q_ ( _p_ ) = 0 if _p_ = 0 or _p_ = 1, and increases gradually from the extremes of interval (0 _,_ 1) toward[1] 2[,][which][corresponds][to] maximum heterogeneity. 

Expression (5.14) suggests that we can substitute the entropy with other impurity measures. Of the possible alternatives, one common variant is the _Gini index_ 

**==> picture [225 x 26] intentionally omitted <==**

Another simple index of misclassification error, often used as an alternative to the sum of impurities, is 

**==> picture [130 x 37] intentionally omitted <==**

that is, the sum of the relative frequencies of errors. 

Methods of Classification 

167 

**==> picture [329 x 166] intentionally omitted <==**

**----- Start of picture text -----**<br>
220.0  6.7  5.1  5.0  3.9  3.4  2.9  2.7  1.9  1.6 −Inf loyaltyMM < 0.530711<br>|<br>loyaltyMM < 0.294301 loyaltyMM < 0.964358<br>discountCH < 0.115 MM MM<br>CH discountMM < 0.15<br>CH<br>CH MM<br>1 20 40 60 80 100 120<br>Size<br>500<br>450<br>400<br>350<br>Deviance<br>300<br>250<br>200<br>**----- End of picture text -----**<br>


Figure 5.20 Fruit juice data: Classification tree. 

_Table 5.11._ FRUIT JUICE DATA: CONFUSION MATRIX OF TEST SET WITH A CLASSIFICATION TREE MATRIX 

|Prediction<br>CH<br>MM<br>Total|Actual response<br>CH<br>MM<br>Total<br>135<br>18<br>153<br>34<br>81<br>115<br>169<br>99<br>268|
|---|---|



We now use these tools for the fruit juice data. In the growth phase of the tree, we adopt entropy as impurity index and base the fit on a sample of 600 elements, taken from 802 observations of the training set. For pruning, we use the remaining 202 observations, for which we again use entropy as the adequacy measure. The corresponding deviance is shown in the left panel of figure 5.20, from which we select dimension _J_ = 6 for the tree, shown in the right panel. 

The resulting tree demonstrates the importance of loyaltyMM and the discount variables. We also note that the two leaves on the extreme right could be pruned, if we are merely focusing on classification, because their distinction deals with the associated probability value, which is 0 _._ 72 for the left leaf and 1 for the other leaf. 

The confusion matrix is shown in table 5.11 and indicates a global error of 19.4%. Figure 5.21 shows the lift and ROC curves. 

The adaption for the case of _K >_ 2 is as follows. Function _p_ ( _x_ ) takes values in the _K_ -dimensional simplex—that is, its values are probabilities _p_ 0( _x_ ) _, . . . , pK_ −1( _x_ ), which total 1. The impurity indices used earlier take the form 

**==> picture [248 x 33] intentionally omitted <==**

168 

**==> picture [330 x 179] intentionally omitted <==**

**----- Start of picture text -----**<br>
168 D A T A A N A L Y S I S A N D D A T A M I N I N G<br>0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0<br>Fraction of predicted subjects 1−specificity<br>1.0<br>2.5<br>0.8<br>2.0 Sensibility 0.60.4<br>Improvement factor 1.5<br>0.2<br>1.0 0.0<br>**----- End of picture text -----**<br>


Figure 5.21 Fruit juice data. Left: lift curve; right: ROC curve for classification tree. 

each one of which can be inserted into objective function (5.14) where _P_[ˆ] _j_ is now a _K_ -dimensional vector of estimates of _p_ 0( _x_ ) _, . . . , pK_ −1( _x_ ). 

For a numerical illustration, consider the data of figure 5.10, where _K_ = 3. The fitting process gives the plots in figure 5.22, where the top-left plot shows the completely developed tree with entropy as an impurity measure, and the topright plot shows the deviance obtained by cross-validation, dividing the set into 10 portions, leading to _J_ = 9. The bottom plots refer to the pruned tree and the corresponding graphical representation in R[2] . 

For a discussion of the pros and cons of classification trees, the remarks already made in section 4.8.4 for regression trees apply. 

## _Bibliographical notes_ 

The references provided at the end of section 4.8 are pertinent also here. In addition, the basic methodology described in CART is also used in C4.5 developed by Quinlan (1993) and the commercial version C5.0. Small differences with respect to CART are in tree structure (C4.5 may have multiway splits), splitting criteria (only entropy is allowed by C4.5), pruning method (C4.5 uses an errorbased pruning, see, for example Ripley 1996, p. 227) and the way missing values are handled. 

## 5.8 SOME OTHER TOPICS 

The set of classification techniques is vast. We have only presented some here; there are many others. In this section, we give a brief description of a few of them without attempting to cover the complete list. 

## 5.8.1 Neural Networks 

The extension of neural networks (section 4.9) to this context is immediate. Starting as usual from the case of _K_ = 2, where class indicator _y_ takes the value 0 or 1, the only important adaptation to be introduced is that in (4.18): activation 

Methods of Classification 

169 

**==> picture [329 x 326] intentionally omitted <==**

**----- Start of picture text -----**<br>
240.0  20.0  9.0  5.7  4.9   4.6  3.0   2.7   2.1  −Inf<br>|<br>1 10 20 30 40<br>Size<br>x2 < −1.2524<br>|<br>1<br>2<br>x1 < −0.783075 x1 < 0.319662<br>x2 < 0.520249 x2 < −0.740155<br>x1 < −0.763861 x2 < 1.99623<br>x2 < −3.97048 2 1 3<br>3 2 1 1 2<br>3 2<br>−4 −2 0 2<br>x 1<br>650<br>600<br>550<br>Deviance 500<br>450<br>400<br>350<br>2<br>0<br>x 2<br>−2<br>−4<br>**----- End of picture text -----**<br>


Figure 5.22 Simulated data with three groups: Classification by tree. 

function _f_ 1 must have interval (0 _,_ 1) as a codomain; the most commonly used function is logistic function _ℓ_ ( _x_ ), defined in (2.40). When the two classes are encoded −1 and 1, we use the function 

**==> picture [148 x 24] intentionally omitted <==**

If _K >_ 2, we proceed as in section 5.4.2, in the sense that we create _K_ response variables with values 0 or 1. The new ingredient is the choice of the activation function. Putting 

**==> picture [65 x 26] intentionally omitted <==**

the activation functions between the hidden layer and the output layer in (4.18) are 

**==> picture [196 x 29] intentionally omitted <==**

D A T A A N A L Y S I S A N D D A T A M I N I N G 

**==> picture [330 x 177] intentionally omitted <==**

**----- Start of picture text -----**<br>
170 D A T A A N A L Y S I S A N D D A T A M I N I N G<br>2<br>1<br>2<br>3<br>1<br>3<br>−4 −2 0 2 −4 −2 0 2<br>z 1 z 1<br>2 2<br>0 0<br>2 2<br>z z<br>−2 −2<br>−4 −4<br>**----- End of picture text -----**<br>


Figure 5.23 Simulated data with three classes: Classification with neural networks. 

In this context, this type of function is called _softmax_ , but it is essentially the same as (5.3). Term _D_ in objective function (4.20) is no longer the Euclidean distance but rather entropy, as in many other classification methods. Correspondingly, the suggested choice of Ripley (1996, p. 163) for regulation parameter _λ_ also changes: it must now be between 10[−][3] and 10[−][1] , referring to the second form of (4.21) for _J_ . 

Figure 5.23 shows the results of classifying the simulated data of three classes, varying the number of hidden nodes _r_ : in the first panel _r_ = 4 and in the second _r_ = 12; in both cases regulation parameter _λ_ in (4.20) is 10[−][2] . The second panel shows an overfit effect, indicated by the zones without or almost without any point within a zone that is well characterized by points in another class and also by the irregular form of the borders between the classes in some cases. This clearcut overfit effect stresses the need for care in choosing regulation parameter _λ_ and the number of hidden nodes. 

## 5.8.2 Support Vector Machines 

Figure 5.24 shows two sets of points in R[2] , whose elements are distinguished by different symbols, and many straight lines cut the plane, perfectly separating the two classes. As one line must be chosen, it is obvious that the line giving the cleanest separation is the best, in the sense of maximizing its distance from the closest point. Intuitively, this line will have the same distance _m_ from the closest representative of each of the two classes. There are two other lines associated with it and parallel to it, which pass through the closest point of each of the classes. 

This example is a simple illustration of the more general case of two sets of points in R _[p]_ that are _linearly separable_ —that is, perfectly separable by a hyperplane. For these situations, there is an algorithm to determine the optimal separation hyperplane, that is, with maximum value _m_ , in a finite number of operations. This algorithm and its connected aspects go back to the work of Frank Rosenblatt in the late 1950s on the _perceptron_ , on which the development of neural networks was based. 

Methods of Classification 

171 

**==> picture [217 x 218] intentionally omitted <==**

**----- Start of picture text -----**<br>
m<br>m<br>**----- End of picture text -----**<br>


Figure 5.24 Maximum separation margin between two classes: Points belonging to different classes are marked by different symbols. 

It is convenient to recall some geometric concepts. For a hyperplane in R _[p]_ with equation 

**==> picture [120 x 13] intentionally omitted <==**

identified by coefficients _a_ ( _a_ ∈ R) and _b_ ( _b_ ∈ R _[p]_ ), each of the following hold: 

- for every point _x_[′] on the hyperplane, it follows that _b_[⊤] _x_[′] = − _a_ ; 

- if _x_[′] and _x_[′′] are any two points on the hyperplane, _b_[⊤] ( _x_[′] − _x_[′′] ) = 0; 

- it follows that vector _b_ is orthogonal to the hyperplane, and _b_[ˆ] = _b/_ ∥ _b_ ∥ is the corresponding unit-norm vector; 

- the signed distance from a point _x_ ∈ R _[p]_ to the hyperplane, that is, to projection _x_ 0 of _x_ on the hyperplane, is given by 

**==> picture [125 x 24] intentionally omitted <==**

We now examine the optimization problem more closely. We consider the case of _K_ = 2 classes to which this time we assign the conventional values _y_ = −1 and _y_ = 1, and denote by 

**==> picture [237 x 13] intentionally omitted <==**

the equation that identifies a general hyperplane candidate to separate the two classes. Note that without loss of generality, we can let ∥ _β_ ∥= 1. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

172 

˜ For a fixed choice of (5.16), unit ( _x, y_ ) is classified either correctly or incorrectly, depending on 

**==> picture [188 x 13] intentionally omitted <==**

Therefore, the optimization problem may be formulated as 

**==> picture [317 x 33] intentionally omitted <==**

where 2 _m_ is called the _margin_ , and it represents the width of the free band of points in figure 5.24. Problem (5.17) can then be conveniently rewritten as follows. To free ourselves from condition ∥ _β_ ∥= 1, we rewrite the constraints in the form 

**==> picture [105 x 25] intentionally omitted <==**

which implies a redefinition of _β_ 0 or, equivalently, 

**==> picture [104 x 14] intentionally omitted <==**

Because multiplication of _β_ and _β_ 0 by a arbitrary positive constant does not change the constraints, we also presume condition ∥ _β_ ∥= 1 _/m_ , and rewrite (5.17) in the equivalent form 

**==> picture [308 x 20] intentionally omitted <==**

Now the half-width _m_ of the free band of points in figure 5.24. is given by 1 _/_ ∥ _β_ ∥. Optimization problem (5.18) becomes a minimization problem of a quadratic function with linear constraints, which can be solved by known techniques. 

A situation in which a hyperplane achieves perfect separation between the two classes is of course rare in practice. However, we can take the previous example to extend the criterion to more realistic cases. We do not treat it in detail but only outline the basic idea. In a case like that of figure 5.25, there is no straight line that perfectly separates the two classes, and we must therefore select the line using a less stringent requirement. 

Because in this new case we have to accept the fact that some points will be wrongly classified, we introduce auxiliary nonnegative variables _ξ_ 1 _, . . . , ξn_ , which express how far the points are on the wrong side of the margin of their class; when = a point is within its margin, _ξi_ 0. In figure 5.25, the _ξi_ are represented by the length of the line segments connecting the margin of each class with those points 

Methods of Classification 

173 

**==> picture [217 x 218] intentionally omitted <==**

Figure 5.25 An example of two classes of points that cannot be separated by a straight line. Membership of points is distinguished by triangles and circles. Line segments between some points and dotted lines show auxiliary variables _ξi_ . 

that violate the margin of their membership class. So optimization problem (5.17) can be adapted, replacing constraints _yi_ ( _β_ 0 + ˜ _xi_[⊤] _[β]_[)][ ≥] _[m]_[ with the form] 

**==> picture [198 x 14] intentionally omitted <==**

Reformulating the problem in a way similar to the linearly separable case, we reach the form 

**==> picture [313 x 33] intentionally omitted <==**

where _γ_ represents a positive constant that plays the role of the regulation parameter and represents the cost of violating the barriers. It can be shown that the solution for _β_ to the optimality problem is of the form 

**==> picture [197 x 31] intentionally omitted <==**

where only some of the _ai_ are nonzero. Therefore, the solution can be expressed through only some of the observations, which are called _support vectors_ . 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

174 

As in many other techniques, it is convenient to consider transforming the explanatory variables, as in 

**==> picture [186 x 15] intentionally omitted <==**

where the number of components _q_ may be less than, equal to, or greater than _p_ . Correspondingly, (5.16) is substituted by the separation curve 

**==> picture [108 x 14] intentionally omitted <==**

which, in light of (5.20), becomes 

**==> picture [264 x 31] intentionally omitted <==**

In the second expression, we used the most commonly adopted notation in the machine learning literature for the inner product. The resulting method takes the name _support vector machines_ (SVM). 

Note that the observations enter these formulas only through the inner products of the form ⟨ _h_ ( _x_ ) _, h_ ( _x_ ˜ _i_ )⟩ and the products between these and the _yi_ . Specification of the functions that form _h_ ( _x_ ) can therefore occur through the _kernel function_ 

**==> picture [104 x 12] intentionally omitted <==**

which calculates the inner products in the space of the transformed variables. The most commonly used kernel functions are the following: 

|Kernel|_K_(_x_,_x_′)|
|---|---|
|polynomial|(1+ ⟨_x, x_′⟩)_d_|
|radial basis|exp(−_d_∥_x_−_x_′∥2)|
|sigmoidal|tanh(_d_1⟨_x, x_′⟩+_d_2)|



where _d, d_ 1 _, d_ 2 are quantities that must be specified a priori. 

For example, if _p_ = 2 with _x_ = ( _x_ 1 _, x_ 2) and we adopt the polynomial kernel of order _d_ = 2, we have 

**==> picture [107 x 13] intentionally omitted <==**

**==> picture [253 x 33] intentionally omitted <==**

for which _q_ = 6. The corresponding functions _hj_ ( _x_ ) are 

**==> picture [204 x 35] intentionally omitted <==**

Methods of Classification 

175 

**==> picture [328 x 325] intentionally omitted <==**

**----- Start of picture text -----**<br>
−4 −2 0 2 −4 −2 0 2<br>z 1 z 1<br>−4 −2 0 2 −4 −2 0 2<br>z 1 z 1<br>2 2<br>0 0<br>2 2<br>z z<br>−2 −2<br>−4 −4<br>2 2<br>0 0<br>2 2<br>z z<br>−2 −2<br>−4 −4<br>**----- End of picture text -----**<br>


Figure 5.26 Simulated data with two groups. Left: classification by SVM with a polynomial kernel; right: a radial basis kernel. Top plots: _γ_ = 1; bottom plots: values chosen by cross-validation. 

To illustrate the results of the method, examine figure 5.26, in which the data points are the same as those in figure 5.8. A polynomial of order 3 is used in the two left panels, and the radial basis kernel with _d_ =[1] 2[in those on the right. In the] two top panels, value _γ_ = 1 is fixed, whereas the two bottom panels show a scan of 25 values of _γ_ , logarithmically equally spaced between 10[−][2] and 10[4] . For each value, we proceed to evaluate the total misclassification error by cross-validation by rotating 10 data subgroups; the resulting optimal values are _γ_ = 70 for the polynomial and _γ_ = 7 _._ 39 for the radial basis. 

## _Bibliographical notes_ 

Hastie et al. (2009, ch. 12) provide more details of the foregoing discussion. Cristianini & Shawe-Taylor (2000) offer a systematic description of SVM, although they define it as an “introduction.” Another authoritative text, by one of the main craftsmen of the approach, is that of Vapnik (1998). 

176 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

## 5.9 COMBINATION OF CLASSIFIERS 

In many real-life cases, several models fit the data equally well and none appear to be preferable to another. For example, in a problem with 50 explanatory variables, if we construct a logistic regression model with, say, five covariates, there are more than 2 million possible groups of five variables from which we can choose. If we calculate the prediction error on a test set to measure the adequacy of the model, we generally find several sets of five variables with very similar error rates. These models are essentially equivalent from the viewpoint of their prediction error, but they may be quite different when we consider the actual classification of the units in the two groups. 

In a similar and perhaps even more obvious way, classification by more unstable methods—for example, trees or neural networks—is greatly influenced by the specific choice of the data set used by the estimate. If this set is modified slightly— for instance, by eliminating a small percentage (2–3%) of data—we can obtain a model that is markedly different from the original one with about the same prediction error. That is, many different models can give similar results for the prediction error. 

To improve the predictive ability of each model, one possibility is to combine predictions obtained from various methods, and various paths have been proposed. Each of them produces a model that in some way gathers all the qualities of the single components and thus often gives more accurate predictions. This section presents the main features of the most popular methods. 

## 5.9.1 Bagging 

Let _Z_ = {( _x_ ˜1 _, y_ 1) _,_ ( _x_ ˜2 _, y_ 2) _, . . . ,_ ( _x_ ˜ _n, yn_ )} be the training set and _C_ ( _x_ ) a classifier obtained with one of the methods presented earlier. In the following, the model associated with _C_ ( _x_ ) is called the base model. For the sake of simplicity, we consider the case with _K_ = 2. 

Adopting a bootstrap procedure, examine sample _Z_ 1[∗][obtained by extracting] _[ n]_ elements from training set _Z_ with replacement. We obtain a new classifier _C_ 1[∗][(] _[x]_[),] by fitting to _Z_ 1[∗][one of the models presented earlier in this chapter, for example, a] classification tree. In general, for a fixed _x_ , the new fitted model is different from the original one. Repeated application of this step, say, _B_ times, produces a set of samples _Zb_[∗][(] _[b]_[=][1] _[, . . . ,][ B]_[),][each][of][size] _[n]_[,][and][they][in][turn][produce] _[B]_[new] classifiers _Cb_[∗][(] _[x]_[),] _[ b]_[ =][ 1] _[, . . . ,][ B]_[.] 

A new classifier that is an average of the results from each of the _Cb_[∗][(] _[x]_[) on the] given _x_ can be introduced. The most natural form of averaging is the arithmetic mean 

**==> picture [100 x 33] intentionally omitted <==**

which allocates the unit with explanatory variables _x_ to _y_ = 1 if _Cbag_ ( _x_ ) _>_[1] 2 and to _y_ = 0 otherwise. As discussed for logistic regression, the choice of[1] 2[is] not mandatory, and the method seen in section 5.2.2 still applies. If we think of every single classifier _Cb_[∗][(] _[x]_[)][as][a][voter][who][assigns][a][vote][to][one][class][or][the] 

Methods of Classification 

177 

other, we choose the class corresponding to the largest number of votes, so that this criterion is indicated as a _majority vote_ . This classification procedure is called bootstrap aggregating, from which the abbreviated the term _bagging_ is derived. The classification error of the new procedure is often lower than that of the base models. 

Many classification procedures also yield a function _p_ ˆ( _x_ ), which gives the probability that a unit with explanatory variables _x_ belongs to each class. A variation of bagging works by averaging the _p_ ˆ[∗] _b_[(] _[x]_[),][which][estimate][the][class][probabilities] forˆ the model fitted to each of the _B_ bootstrap samples _Zb_[∗][and][using][this][new] _pbag_ ( _x_ ) =[�] _b[p]_[ˆ][∗] _b_[(] _[x]_[)] _[/][B]_[ as a probability indicator of class membership.] The bagging strategy can easily be adapted to the regression context, where in place of classifiers _C_ ( _x_ ) we use the predictions derived from the models discussed in chapter 4. In this case, it is not necessary to return to the majority vote criterion, because we can directly use the average of the predictors obtained by bootstrap resampling as a new predictor. The new prediction may have variance smaller than that of the original model. 

Bagging procedures often greatly improve predictive ability, particularly when the classifiers used are very unstable, for example, trees or neural networks. However, with more stable procedures, bagging can somewhat worsen prediction quality. It is also obvious that the operation of combining the results of the single models by way of the arithmetic mean involves losing whatever simple structure existed in the base model, leading to greater difficulty in interpreting the results. 

A variant, called _bumping_ , or _stochastic search of the model_ , picks out, as a new classifier, the model with the smallest prediction error among all the models obtained in bootstrap resampling. 

To illustrate how the method works, a bagging procedure with majority vote was applied to the classification tree fitted to the fruit juice data (see table 5.11). Table 5.12 shows the confusion matrix obtained from the test set after bagging based on 300 bootstrap samples taken from the training set and, for every sample, fitting a tree with growth and pruning carried out on two random subsets of each bootstrap sample. 

The model obtained with this procedure is better than the original one, as shown by figure 5.27, which compares the error rates of the base model and the bagging procedure when the number of bootstrap samples used grows. Figure 5.28 shows 

_Table 5.12._ FRUIT JUICE DATA: CONFUSION MATRIX OF BAGGING PROCEDURE BASED ON CLASSIFICATION TREE ON TEST SET 

|Prediction<br>with bagging<br>CH<br>MM<br>Total|Actual response<br>CH<br>MM<br>Total<br>143<br>24<br>167<br>26<br>75<br>101<br>169<br>99<br>268|
|---|---|



D A T A A N A L Y S I S A N D D A T A M I N I N G 

178 

**==> picture [260 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>
Original tree<br>Bagging procedure<br>0 50 100 150 200 250 300<br>Number of bootstrap samples<br>0.195<br>0.190<br>0.185<br>Misclassification error − Test set<br>0.180<br>**----- End of picture text -----**<br>


Figure 5.27 Fruit juice data: Estimation errors for bagging on a classification tree. 

**==> picture [330 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
Original tree<br>Bagging<br>Original tree<br>Bagging<br>0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0<br>Fraction of predicted subjects 1−specificity<br>1.0<br>2.5<br>0.8<br>2.0 Sensibility 0.60.4<br>Improvement factor 1.5<br>0.2<br>1.0 0.0<br>**----- End of picture text -----**<br>


Figure 5.28 Fruit juice data: Lift (left) and ROC (right) curves of classification tree and classifier obtained by bagging a tree. 

the lift and ROC curves for the bagging model, compared with similar curves for the initial classification tree, and _B_ = 300. 

Using random samples of observations allows the use of a technique called _outof-bag_ for easy estimation of prediction errors. In fact, in each bootstrap sample, some of the data of the original training set are excluded. Consequently, for each classifier _Cb_[∗][(] _[x]_[), the data of training set] _[ Z]_[that are not in sample] _[ Z] b_[∗][can be used] 

Methods of Classification 

179 

as a test set. We can therefore estimate, for instance, the misclassification error on these data outside the sample used for the fit (out-of-bag), without requiring a test set or having to choose computing-intensive solutions, such as cross-validation. 

## 5.9.2 Boosting 

The idea underlying bagging is to combine results from different data sets, extracted through equal-weight random sampling of available units, and fit them with the same type of model. 

Analogously, _boosting_ consists of combining the results of a model fitted from several data sets, but we assign a different probability of entering the sample to each unit. Specifically, we assign greater weight to observations classified poorly in the early stage. We thus aim at improving model performance, acting mostly on those subsets in which the original classifier had more problems. 

The procedure is iterative. We start by choosing a base model among the classifiers discussed earlier. In the first step, the base classifier is fitted to the data by assigning the same weight to each observation. In the following iterations, the weight assigned to each observation is modified, depending on the classification error. A new classifier is then fitted at each iteration from the modified set of weights. At the end of the process, a new classifier is identified through a weighted majority vote among the classifiers fitted in all the iterations. 

This logic has been implemented in many different ways. The most frequent procedure, also the original one, is called _AdaBoost_ , presented in algorithm 5.2. 

As the number of iterations increases, the importance of the choice of base classifier tends to fall, as the classification choice is more and more closely linked to iteration, that is, it concentrates on badly classified units. This explains the common choice of a tree grown with one or at most two levels, without pruning, as a base classifier. Because their error rate is only slightly better than random guessing, in this context they are usually called _weak classifiers_ . When the weak classifier is a tree, the number of levels is connected to the order of interactions allowed by the final model. For example, if only one level of trees is included, only main effects are allowed. 

Note that when a tree is fully grown, all its leaves are pure, the classifier makes no errors on the training data, and its error rate is therefore 0. This means that boosting will stop because there are no wrongly classified training units to be boosted. Clearly, the same thing occurs if the tree is just very large, without being fully grown, so that it probably overfits the data. For this reason, it is usually better not to use very large trees for boosting. 

Boosting has shown a remarkable ability to produce accurate classifiers in a wide range of situations. They have also been studied theoretically, proving statistical properties that justify their excellent empirical performance; see Friedman et al. (2000). 

To illustrate the method, we again use the fruit juice data and choose a tree with two levels as a weak classifier, corresponding to four final leaves. Boosting is stopped after 200 iterations. Figure 5.29 shows the error rate obtained in the test set as iterations increase, clearly demonstrating the improvement up a certain number of iterations, at which point the error stabilizes. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

180 

**Algorithm 5.2** Boosting (AdaBoost) 

1. Initialize weights _wi_ = 1 _/n, i_ = 1 _,_ 2 _, . . . , n_ . 2. Cycle for _b_ = 1 _, . . . , B_ : 

   - a. Fit a classification model _Cb_ ( _x_ ) to the training set, with target values 0 or 1, by weighting the observations by _wi_ . 

   - b. Obtain: 

**==> picture [139 x 61] intentionally omitted <==**

- c. Assign the new weights: 

**==> picture [229 x 11] intentionally omitted <==**

3. 

**==> picture [167 x 53] intentionally omitted <==**

Table 5.13 shows the confusion matrix on the test set for the classifier obtained by boosting; the misclassification error is 16%. Figure 5.30 plots lift and ROC 

## 5.9.3 Random Forests 

Both bagging and boosting construct different models they then combine by changing at each iteration the set of units or the weight assigned to each unit on which to fit the model, using all available _p_ explanatory variables at each iteration. Another way of obtaining combinations of models consists of considering several subsets of the explanatory variables, instead of considering subsets of the units. 

One strategy of this type has been proposed with trees as base classifiers, choosing the variables to put into each model by random selection: this procedure is called _random forest_ . Note that this term is sometimes used with a more general meaning, referring to any classifier obtained as a combination of a set of classification trees. For example, in this interpretation of the term, bagging and boosting also belong to random forests when applied to trees. 

The procedure consists of selecting at random, at every tree node, a small group of covariates, which are examined to find their best point of subdivision, according 

Methods of Classification 

181 

**==> picture [238 x 233] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 50 100 150 200 250 300<br>Iterations<br>0.19<br>0.18<br>0.17<br>0.16<br>Misclassification error − Test set<br>0.15<br>**----- End of picture text -----**<br>


Figure 5.29 Fruit juice data: Estimated error for boosting on a classification tree. 

_Table 5.13._ FRUIT JUICE DATA: CONFUSION MATRIX ON TEST SET OF BOOSTING CLASSIFIER, BASED ON A CLASSIFICATION TREE WITH FOUR LEAVES 

|Prediction<br>with boosting<br>C<br>CH<br>1<br>MM<br>Total<br>1|Actual response<br>H<br>MM<br>Total<br>48<br>22<br>170<br>21<br>77<br>98<br>69<br>99<br>268|
|---|---|



to the splitting criterion described in section 5.7. Therefore, rather than exploring all the possible variable in each node, only _q_ ( _q_ ≪ _p_ ) randomly chosen variables are examined. The tree grows to maximum size but is not pruned. In fact, the resulting combination of various trees avoids overfitting. 

The number _q_ of variables to be selected in each node is a tuning parameter to be determined and is generally kept constant on all nodes. The number is often chosen considering forests constructed with different values of _q_ and determining the value that minimizes the error on a test set. 

The other tuning parameter is the number of trees, let’s say _B_ , that make up the forest. It can be shown that the global error converges to a lower bound when _B_ increases and that it does not cause overfitting problems when additional trees are added. If, therefore, a sufficiently large value is chosen for _B_ , we can be confident that the prediction error obtained will not be very far from its minimum. 

182 

**==> picture [329 x 177] intentionally omitted <==**

**----- Start of picture text -----**<br>
182 D A T A A N A L Y S I S A N D D A T A M I N I N G<br>Original tree<br>Boosting<br>Original tree<br>Boosting<br>0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0<br>Fraction of predicted subjects 1−specificity<br>1.0<br>2.5<br>0.8<br>2.0 Sensibility 0.60.4<br>Improvement factor 1.5<br>0.2<br>1.0 0.0<br>**----- End of picture text -----**<br>


Figure 5.30 Fruit juice data. Left: lift curve; right: ROC curve of classification tree and classifier obtained by boosting on a tree with four leaves. 

When constructing a forest, a bagging procedure is usually also associated with random selection of variables. Each tree is made to grow on a different bootstrap sample with a number _q_ of randomly selected variables for each node. Here, bagging, for which the main aim is to improve prediction accuracy, also allows us to use the out-of-bag technique to choose regulation parameter _q_ and obtain the importance measures of the covariates. We can use the prediction error obtained from the out-of-bag data when determining _q_ , instead of the error on a test set. 

To obtain a measure of the importance of each explanatory variable in predicting the response, we can proceed using out-of-bag data in the following way. For each tree, the misclassification error on the out-of-bag portion of the data is obtained. The same is done after randomly permuting the values of each explanatory variable. The average of the difference between the two misclassification errors is computed and divided by the standard deviation of the differences, providing an indicator of how that variable influences predictions. 

Another indicator of the relevance of variables is based on the importance measure for a single tree,[�] _h[g] h_[2][,][introduced][at][the][end][of][section][4.8.3.][This][is] obtained as the average over all the trees in the forest of that importance measure, calculated separately for each variable. 

With respect to other methods of model combination, random forests have some interesting advantages. The accuracy of their predictions is comparable to that of boosting and in some cases is better, but they are much faster because every single tree is based on fewer variables and the computational burden is therefore lower. It is also relatively simple to build an algorithm that, taking advantage of parallel computing, can further accelerate the random forest procedure. 

For illustration, we present the result of a random forest obtained for the fruit juice data. Note, however, that the presence of only eight covariates would not justify using this strategy, which really only produces interesting results when some hundreds of variables are involved. 

Methods of Classification 

183 

_Table 5.14._ FRUIT JUICE DATA: CONFUSION MATRIX OF RANDOM FOREST USING TEST SET AND OUT-OF-BAG SAMPLES 

||SET ANDOUT-OF|-BAGSAMPLES|-BAGSAMPLES|
|---|---|---|---|
||Test set<br>Actual response<br>CH<br>MM<br>Total<br>145<br>21<br>166<br>24<br>78<br>102<br>169<br>99<br>268|Out-of-bag samples||
|Prediction<br>random forest<br>CH<br>MM<br>Total||Prediction<br>random forest<br>CH<br>MM<br>Total|Actual response<br>CH<br>MM<br>Total<br>414<br>77<br>491<br>70<br>241<br>311<br>484<br>318<br>802|



In this example, we constructed a forest of 500 trees, and every tree was made to grow through the Gini index as an impurity measure, with _q_ = 2 variables randomly chosen for each node of every tree. The left part of table 5.14 shows the confusion matrix for the forest with the test set; the total classification error is 16.79%. The right side shows the confusion matrix resulting from out-of-bag samples, with a classification error of 18.33%. 

The top panel of figure 5.31 plots the error rates obtained on the test set and the out-of-bag samples when the number of iterations increases. The bottom panel plots the importance measures based on the out-of-bag data of the variables in predicting purchases of MM. In this case, loyaltyMM is by far the most important variable for predicting MM purchases; discountMM and store are less important. 

## _Bibliographical notes_ 

Combination methods of classifiers have been proposed by many authors in both statistical and machine learning literature. Bagging was introduced by Breiman (1996), taking advantage of the statistical results on bootstrap. For a presentation of the bootstrap method, see, for example, Efron & Tibshirani (1993) and Davison & Hinkley (1997). The out-of-bag technique was introduced by Wolpert & MacReady (1999) and later exploited by Breiman (2001a). Boosting was initially introduced in the machine learning environment as AdaBoost by Freund & Schapire (1996), and its statistical properties were examined by Hastie et al. (2009). Random forests have been introduced and discussed by Breiman (2001b). 

## 5.10 CASE STUDIES 

We now present some real-life cases in which some of the tools described in this chapter are applied to resolve business problems. Because the method follows the lines expressed in section 4.10, we simply outline the problems, list the models used, and present the results and the choice of the final models. 

## 5.10.1 The Traffic of a Telephone Company 

We return to the real-life case analyzed in section 4.10.1 and concentrate on identifying the customers who used services offered by the telephone company. If we refer to the variable total duration of outgoing calls in a certain 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

184 

**==> picture [190 x 363] intentionally omitted <==**

**----- Start of picture text -----**<br>
Out−of−bag sample<br>Test set<br>0 100 200 300 400 500<br>Iterations<br>LoyaltyMM<br>DiscountMM<br>Shop<br>DiscountCH<br>Week<br>PriceCH<br>PriceMM<br>0.6 0.7 0.8 0.9 1.0 1.1 1.2<br>Mean decrease accuracy<br>0.26<br>0.24<br>0.22<br>Misclassification error<br>0.20<br>0.18<br>**----- End of picture text -----**<br>


Figure 5.31 Fruit juice data: Estimation errors and importance measures of variables for random forests. 

month for a certain population of interest (see section 4.10.1), we must subdivide customers into two classes: those with 0 or positive call durations. 

We use as the response variable a new binary variable with value 1 for customers who made calls lasting at least 1 second in the month of interest, and value 0 for customers with no traffic. The following models were fitted to the data: 

- linear regression model (see section 5.4), with threshold[1] 2[, in two variant] forms: (i) with all 98 available explanatory variables; (ii) with only the 55 most significant variables ( _p_ -value lower than 0.1); 

- logistic regression model (see section 2.4), again using all 98 available explanatory variables and only the 55 most significant ones ( _p_ -value lower than 0.1); 

- linear discriminant analysis (see section 5.5.2); 

Methods of Classification 

185 

- logistic additive model (see section 5.6), with smoothing splines with 4 effective degrees of freedom as smoothers for each variable; this model was also fitted to the data with all 98 variables and only the 29 most significant ones ( _p_ -value lower than 0.1); 

- MARS (see section 5.6), with linear regression splines with single nodes as elements; 

- a classification tree (see section 5.7), with entropy as an impurity index and the number of leaves for the final tree selected by growing and pruning that tree on two separate sets of equal size, randomly chosen from the training set; 

- neural networks, with five nodes in the hidden layer and with weight decay parameter _λ_ = 10[−][2] ; 

- support vector machine, with radial kernel and tuning parameter ( _γ_ = 4) selected on the test set; 

- randomforestwith500trees;thenumberofvariablessampledascandidate at each split (60) was selected on the test set; 

- bagging with 500 trees; 

- boosting with 50 trees; to include higher order interactions, each tree was grown up to 8 leaves (a test set was used to select it). 

We compared the various models according to the percentages of misclassification error, false positives and false negatives, listed in table 5.15. The models were also compared with the lift and ROC curves of figure 5.32. 

Comparison of error rates and curves shows that the classifier that predicts best is bagging, because it has the lowest total error rate and the lowest percentage 

_Table 5.15._ TELECOMMUNICATIONS CUSTOMER DATA: PREDICTION ERRORS (%) FOR MODELS DESCRIBED IN SECTION 5.10.1. WHERE NECESSARY THRESHOLDS WERE SET AT[1] 2 

|Model|Total|False|False|
|---|---|---|---|
||error|negatives|positives|
|Linear model|22.56|29.69|19.92|
|Linear model – selected variables|22.61|29.64|20.04|
|Logistic regression model|17.58|27.10|12.50|
|Logistic regression model – selected variables|20.20|34.87|8.69|
|Discriminant analysis|22.30|30.25|19.16|
|GAM|16.06|23.37|12.49|
|GAM – selected variables|16.13|23.75|12.36|
|MARS|15.61|18.75|14.34|
|Classifcation tree|15.79|21.95|12.95|
|Neural network|21.39|21.59|21.33|
|SVM|16.72|24.41|12.96|
|Random forest|15.40|18.69|14.07|
|Bagging|15.04|18.51|13.60|
|Boosting|15.59|19.48|13.98|



**==> picture [284 x 579] intentionally omitted <==**

**----- Start of picture text -----**<br>
Linear model<br>Reduced linear model<br>Logistic regression<br>Reduced logistic model<br>Discriminant analysis<br>GAM<br>Reduced GAM<br>MARS<br>Classification tree<br>Neural network<br>SVM<br>Random forest<br>Bagging<br>Boosting<br>0.0 0.2 0.4 0.6 0.8 1.0<br>Fraction of predicted subjects<br>Linear model<br>Reduced linear model<br>Logistic regression<br>Reduced logistic model<br>Discriminant analysis<br>GAM<br>Reduced GAM<br>MARS<br>Classification tree<br>Neural network<br>SVM<br>Random forest<br>Bagging<br>Boosting<br>0.0 0.2 0.4 0.6 0.8 1.0<br>1−specificity<br>1.5<br>1.4<br>1.3<br>Improvement factor 1.2<br>1.1<br>1.0<br>1.0<br>0.8<br>0.6<br>Sensibility<br>0.4<br>0.2<br>0.0<br>**----- End of picture text -----**<br>


Figure 5.32 Telecommunications data: Comparison of lift (top) and ROC (bottom) curves for various models. 

Methods of Classification 

187 

**==> picture [331 x 173] intentionally omitted <==**

**----- Start of picture text -----**<br>
q09.out.ch.peak < 27.5<br>|<br>q09.out.dur.peak < 148.5 q09.out.ch.peak < 99.5<br>age < 16.735 q08.out.dur.offpeak < 10.5 q09.out.dur.offpeak < 20.5 q09.out.ch.peak < 136.5<br>q09.out.dur.offpeak < 9.5 q09.out.ch.peak < 12.5 q09.out.ch.peak < 61.5<br>0 1 1 1 1<br>age < 16.795 age < 17.025 q09.out.ch.peak < 41.5<br>1 0 1<br>tariff.plan: 6,7,8<br>1 0 1 1 1<br>0 1<br>**----- End of picture text -----**<br>


Figure 5.33 Telecommunications customer data: Final classification tree. 

of false negatives. Although its percentage of false positives is not the lowest, it has an acceptable value. However, the classification tree has not only a low misclassification error rate and a percentage of false positives lower than that obtained by bagging, but also a ROC curve that is essentially equal to that of bagging and is easier to interpret. We therefore chose the tree to predict customers who do not generate telephone traffic. 

Figure 5.33 shows the final version of the tree. To predict which customers will have traffic in the next month, predictive variables are customer’s age, phone tariff plan, and several variables linked to traffic in the current and previous months. One interpretation of this evidence is that a customer does not suddenly stop using a telephone but generally reduces traffic slowly until it stops completely. 

## 5.10.2 Churn Analysis 

A typical CRM problem for many companies with a large customer base is how to evaluate customer loyalty and, in particular, how to predict which customers are most likely to abandon the company and transfer to another supplier. These customers are often described as being _churners_ . This problem is prominent in sectors where customers have ongoing relationships with companies, such as banks, insurance companies, telecommunications services, and services companies in general. Companies of this type must have good models for predicting deactivation by their customers to be able to carry out appropriate retention actions later on. 

It is also very useful to understand what reasons customers have for leaving the company. Constructing a model is therefore inspired not only by the need to fit the data but also by the need for that model to indicate _marketing actions_ , for example, customer retention strategies, because this obviously translates into profit. 

To handle a real-life case in which this problem was tackled, the same data analyzed in sections 4.10.1 and 5.10.1 were used for the customers of a 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

188 

telecommunications operator. The aim of the analysis was to predict deactivation by a customer in a given month with at least 2 months’ notice. This requirement is used to plan and implement loyalty actions toward this customer in those 2 months. In other words, we search for the indicator preluding the decision to abandon the company, using information on the structural characteristics of customers, their behavior in terms of use of services offered by the company (if any), their change in usage style, and any other information available in the data mart. 

Our data mart contains a status variable (not used in the previous analyses) that indicates customer status in terms of deactivation 2 months after the last month of available traffic (indicated in the data by the number 10). This variable takes value 1 if a customer has deactivated and 0 if the customer remains active. Our objective is therefore to predict this indicator variable by using the other 108 available variables. 

A simple inspection reveals that the percentage of customers who deactivate is about 13.8% in the training set. In this case, the percentage of events in the population is fairly small—lower than the total prediction rate reasonably envisioned for this problem. This fact causes problems: if we classify all cases as nonevents, irrespective of their individual features, this strategy would appear to be acceptable or possibly even superior to methods that use customer information. This sort of problem is exacerbated in cases in which the percentage of events is even smaller and becomes extreme in cases of rare events: if the percentage of nonevents is 1%, a flat classification scheme of all customers as nonevents has a total error rate of 1%. All this requires us to change our strategy with respect to the previous problems. 

Clearly, a prediction of this type, although it minimizes misclassification errors, is not useful for those who want to identify customers who intend to abandon the operator, together with their characteristics. Instead, we need a strategy allowing us to fit a model that can identify customers as accurately as possible, even at the expense of a relatively bad classification of loyal customers, which therefore translates into an increase in the global misclassification error. 

The strategy applied here, commonly used in data mining, consists of using a sample stratified by the values of the response variable in the training stage. We thus select all “rare event” customers, that is, all the deactivators or “churners,” and a random sample with a similar number of customers with the more common event, that is, customers who are still active. 

In this strategy, most of the data are discarded and not used for the estimate. There are alternative proposals for using all the available data, based on evaluation of various costs involved in various types of misclassification. In the present case, for example, we could decide to assign a higher cost to misclassifying a deactivated customer as active, compared with that of an active customer classified as nonactive. These costs may be included as weights of the terms composing the objective function of most of the models discussed in this chapter. 

In this analysis, considering the abundance of available data, we preferred to carry out balanced sampling from the original data mart, to obtain the set to be 

Methods of Classification 

189 

used for the estimate. Obviously, the test set must retain its original proportion of units, so we can evaluate and compare the results of the various models correctly. The following models were fitted to the new balanced training set: 

- linear regression model, with threshold[1] 2[;] 

- logistic regression model; 

- linear discriminant analysis; 

- logistic additive model, with smoothing splines with 4 effective degrees of freedom as smoother for each variable; this model was also fitted to the data with all 108 variables and also the 36 variables that turned out to be the most significant in the previous model; 

- MARS, with linear regression splines with singles node as elements; 

- classification tree, with entropy as an impurity index and number of leaves for the final tree selected by growing and pruning two separate sets of equal size, randomly selected from the training set; 

- neural networks, with five nodes in the hidden layer and with weight decay parameter _λ_ = 2 × 10[−][2] ; 

- support vector machine, with radial kernel and tuning parameter ( _γ_ = 4 _._ 5) selected on the test set; 

- randomforestwith500trees;thenumberofvariablessampledascandidate at each split (50) was selected on the test set; 

- bagging with 500 trees; 

- boosting with 50 trees; to include higher order interactions, each tree was grown up to 16 leaves (a test set was used to select it). 

Table 5.16 lists the percentages of total misclassification errors, false positives and false negatives obtained on the test set. To further appreciate the usefulness of balanced samples, the error rates for a linear model, a logistic regression model and a classification tree fitted to the original nonbalanced sample are also listed. 

As expected, the models fitted to the nonbalanced training set all have a lower total error than the other models, but they are all around the percentage obtainable by classifying all customers as active, which is 13 _._ 9% in the test set. However, these predictions have a higher percentage of false negatives with respect to other models fitted on balanced samples. 

Comparing the percentages of false positives and false negatives shows that bagging classification is preferable. The percentages in table 5.16 show that the logistic additive model, which is easier to interpret than bagging, gives slightly worse predictions for all three three indicators, so it seems reasonable to consider this simpler model. 

Figure 5.34 shows the lift curves of some models. The bottom panel enlarges the low fractions of predicted customers, which is the important part of the curve, because it is the portion with the greatest differences among models. 

As the fraction of predicted subjects varies, the classifier with the highest lift is almost always bagging. Only for the first percentile does boosting have a higher lift. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

190 

_Table 5.16._ CHURN PREDICTION: ERRORS (%) FOR MODELS DESCRIBED IN SECTION 5.10.2. WHERE NECESSARY THRESHOLDS WERE SET AT[1] 

2 

|Model|Balance|Total|False|False|
|---|---|---|---|---|
|||error|negatives|positives|
|Linear model|yes|33.97|9_._02|77.59|
|Logistic regression|yes|34.46|9_._08|77.87|
|Discriminant analysis|yes|33.97|9_._02|77.59|
|GAM|yes|31.75|8_._49|75.86|
|Restricted GAM|yes|32.16|8_._07|75.60|
|MARS|yes|31.84|8_._45|75.86|
|Classifcation tree|yes|24.94|9_._55|72.64|
|Neural network|yes|40.32|10_._90|81.88|
|Support vector machine|yes|33.69|8_._28|76.62|
|Random forest|yes|31.78|8_._02|75.34|
|Bagging|yes|30.24|7_._81|74.19|
|Boosting|yes|31.43|8_._46|75.64|
|Linear model|no|13.94|13_._75|54.93|
|Logistic regression|no|13.86|13_._41|48.73|
|Classifcation tree|no|14.13|12_._32|52.62|



With this model, at its first percentile, we can choose customers who have almost five times the probability of deactivating with respect to average customers. A fraction of 1% of customers may not seem much, but if—for example—we have a customer base of 1,000,000, this 1% corresponds to 10,000 customers, which already means a nontrivial cost for retention actions on all selected customers. The lift curve can be used to select these 10,000 customers to whom retention action (for example, sending a letter or a gift) will be more profitable, because it indicates those customers most likely to churn. 

Among the easily interpretable models, the classification tree has the highest lift curve (about 4 at the first percentile) and falls more slowly than the other models until the first decile of predicted units. The corresponding tree of figure 5.35 shows that the traffic of the last and previous months and customer age are the variables most closely linked to churning. Less important but still relevant are the sales activation channel and the chosen method of payment. These are _actionable variables_ , in the sense that the telecommunications operator can act directly on them. For example, the company can try to dissuade customers from paying bills by mail (the tree in figure 5.35 shows that the probability of churning is higher for such customers) or have greater control over those sales channels that provide potential churner customers. 

This last remark empirically highlights the important fact that the final model should also suggest commercial actions. In our case, for example, models with actionable variables are preferable to ones in which prediction variables are not easily translatable into actions, for example, gender. If we were to discover that 

**==> picture [274 x 559] intentionally omitted <==**

**----- Start of picture text -----**<br>
Balanced logistic model<br>Not balanced logistic model<br>Balanced linear model<br>Not balanced linear model<br>Discriminant analysis<br>Classification tree<br>MARS<br>GAM<br>SVM<br>Random forest<br>Bagging<br>Boosting<br>0.0 0.2 0.4 0.6 0.8 1.0<br>Fraction of predicted subjects<br>Balanced logistic model<br>Not balanced logistic model<br>Balanced linear model<br>Not balanced linear model<br>Discriminant analysis<br>Classification tree<br>MARS<br>GAM<br>SVM<br>Random forest<br>Bagging<br>Boosting<br>0.00 0.05 0.10 0.15 0.20<br>Fraction of predicted subjects<br>5<br>4<br>3<br>Improvement factor<br>2<br>1<br>5<br>4<br>3<br>Improvement factor<br>2<br>1<br>**----- End of picture text -----**<br>


Figure 5.34 Churn prediction: Lift curves. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

192 

**==> picture [324 x 206] intentionally omitted <==**

**----- Start of picture text -----**<br>
payment.method: CdC,DB<br>|<br>age < 23.195 q10.in.dur.tot < 262<br>q08.out.ch.peak < 65.5<br>1 q10.out.val.peak < 0.4233<br>1<br>activ.chan: 8,9 q10.in.dur.tot < 35.5 1 1<br>q10.in.dur.tot < 200.5<br>0<br>1 0<br>q04.in.ch.tot < 14.5 q05.out.dur.peak < 3335.5<br>q09.out.dur.peak < 613<br>1 1 0<br>1 0<br>**----- End of picture text -----**<br>


Figure 5.35 Churn prediction: Classification tree. 

men churn more easily, we certainly cannot decide to stipulate fewer contracts with men, as they make up about half the population of interest. 

In cases like these, the importance of choosing classifiers that are easily translatable into actions emphasizes the essential fact that a human being carries out the analysis and selects models that are easy to interpret and not based on _black-box_ procedures or ones of the type “press a button and the computer will do it for you.” 

## 5.10.3 Customer Satisfaction 

Quantitative measurement of customer satisfaction is one of the most important key performance indicators for companies in many business sectors. 

Customer satisfaction surveys are typically implemented by questionnaires containing many items detailing various aspects of customers’ feelings toward the company and of their expectations regarding services offered by that company. 

## _Data and background problem_ 

The data analyzed here are described in detail in section B.7 and represent a random sample of 4 _,_ 000 questionnaires submitted to the customers of an IT (information technology) company producing software and offering consulting services. Opinions about a large number of items are collected by asking customers to score the importance attributed to every aspect characterizing the relationship between customers and company and their actual degree of satisfaction. 

Overall satisfaction was investigated by a single question at the end of the questionnaire: “Recalling all the aspects analyzed in this questionnaire, how 

Methods of Classification 

193 

satisfied are you with the company, overall?” The answer was coded in six levels: 

|Level|Description|
|---|---|
|1|Extremely satisfed|
|2|Very satisfed|
|3|Quite satisfed|
|4|Quite dissatisfed|
|5|Very dissatisfed|
|6|Extremely dissatisfed|



Theanswersclearlyshowthatoverallsatisfactionisaordinalcategoricalvariable. Marketing managers are interested in identifying the specific aspects most closely connected with answers to this question. We describe and predict such a variable by fitting models according to three strategies: 

- a. the response variable considered as ordinal categorical, as seen in section 5.3.2; 

- b. the response variable considered as categorical by ignoring level order and setting a classification problem with six classes; 

- c. the response variable considered as quantitative discrete by assigning to each level of overall satisfaction a numeric mark and applying the methods introduced in chapter 4. 

As usual, when data are collected by questionnaire, the number of units is not as enormous as may occur in other contexts of data mining. In our case, we decided to set aside one-quarter of the observations (1 _,_ 000 customers) in the validation set for the final operation of comparing different models. To tune and test models, we preferred not to divide the training set into two parts but to apply fivefold cross-validation to the entire training set of 3 _,_ 000 customers (see section 3.5.2). 

Figure 5.36 shows the percentage of customers by satisfaction level in the training set. About 69% of them were “quite satisfied,” and only 0 _._ 47% were “extremely satisfied.” The overall percentage of dissatisfied customers was 14 _._ 93%, of which only 2 _._ 93% are very or extremely dissatisfied. 

## _Some prediction models_ 

As discussed in section 5.3.2, the simplest model allowing for the ordinal nature of the response variable is the proportional odds version of the cumulative logit model. We fitted such a model to the data by selecting important variables with a stepwise procedure (see section 3.6.1) based on AIC (see section 3.5.3). Table 5.17 shows the final fitted proportional odds model. 

A useful feature of this model is its interpretability. The categories of response variables are in inverse order with respect to common sense—that is, 1 for the most satisfied and 6 for the least satisfied, so the parameter signs must be interpreted inversely. For example, table 5.17 shows that given all other 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

194 

**==> picture [237 x 220] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 2 3 4 5 6<br>Overall satisfaction<br>0.6<br>0.5<br>0.4<br>0.3<br>Relative frequency 0.2<br>0.1<br>0.0<br>**----- End of picture text -----**<br>


Figure 5.36 Customer satisfaction: Bar graph of overall satisfaction on training set. 

variables, customers who often had direct contacts with company personnel (question V11) were less satisfied, and older customers were more likely to be less satisfied than younger ones. The importance attributed to product quality and flexibility (questions V33 and V35), efficiency, and the capacity to understand customers’ needs (questions V37 and V39) were negatively related with satisfaction; satisfaction about single aspects such as efficiency, speed of problem solving (questions V45, V47, and V48), and the capacity to understand and respond to customers’ needs (questions V44, V52, and V54) were positively related with overall satisfaction. Using some specific products/services (the numbers 5 and “others”—variables V6 and V9) were positively related with satisfaction, whereas product 6 (variable V7) was sometimes a cause of dissatisfaction. 

The first part of table 5.18 lists the confusion matrix of the linear proportional odds model in the validation set with classification errors for each predicted level. The overall classification error was 26 _._ 3%. This is a weighted average of the specific classification errors of each predicted level. Marketing managers, in addition to receiving good predictions for each category of satisfaction, are particularly interested in reducing the classification error in one of the “satisfaction” categories (1, 2, and 3) of customers who express some level of dissatisfaction (3, 4, and 6). Using the proportional odds model, among the “very dissatisfied” we can predict 1 customer as “very satisfied” and 5 as “quite satisfied,” and we can classify 62 customers as “quite satisfied” among the “quite dissatisfied.” The total of all these particular misclassification errors was 6 _._ 8% in the validation set. 

Methods of Classification 

195 

_Table 5.17._ CUSTOMER SATISFACTION: SUMMARY OF PROPORTIONAL ODDS VERSION OF CUMULATIVE LOGIT MODEL. VARIABLES ARE DESCRIBED IN SECTION B.7 

|||Estimate|SE|Wald|95%|
|---|---|---|---|---|---|
|||||conf. limits||
|(Intercept|1|2)|−15_._83|0.65|−17_._10|−14_._56|
|(Intercept|2|3)|−11_._26|0.56|−12_._36|−10_._17|
|(Intercept|3|4)|−4_._85|0.50|−5_._83|−3_._86|
|(Intercept|4|5)|−1_._19|0.51|−2_._18|−0_._20|
|(Intercept|5|6)|1_._36|0.56|0_._25|2_._46|
|V6||−0_._24|0.11|−0_._44|−0_._03|
|V7||0_._23|0.10|0_._03|0_._43|
|V9||−0_._16|0.10|−0_._36|0_._05|
|V11-2||0_._33|0.20|−0_._06|0_._72|
|V11-3||0_._27|0.11|0_._06|0_._48|
|V11-4||0_._50|0.19|0_._13|0_._88|
|V25||−0_._20|0.05|−0_._30|−0_._10|
|V26||−0_._41|0.05|−0_._52|−0_._31|
|V27||−0_._14|0.04|−0_._23|−0_._05|
|V28||−0_._08|0.04|−0_._15|−0_._01|
|V33||0_._10|0.05|0_._00|0_._20|
|V35||0_._12|0.06|0_._00|0_._24|
|V37||0_._09|0.06|−0_._02|0_._21|
|V38||−0_._08|0.05|−0_._18|0_._02|
|V39||0_._13|0.06|0_._01|0_._25|
|V41||−0_._08|0.05|−0_._18|0_._02|
|V44||−0_._09|0.04|−0_._17|−0_._00|
|V45||−0_._12|0.06|−0_._24|−0_._00|
|V47||−0_._25|0.07|−0_._38|−0_._12|
|V48||−0_._10|0.05|−0_._20|−0_._00|
|V52||−0_._24|0.05|−0_._34|−0_._14|
|V54||−0_._18|0.05|−0_._27|−0_._08|
|V60||0_._03|0.01|0_._00|0_._05|
|V61||−0_._02|0.01|−0_._04|0_._00|



_D_ = 3406 _._ 630 on 29 d.f. 

A nonparametric generalization of the proportional odds model follows directly from generalized additive models with logit link function. We replace the linear 

_p_ predictor in (5.5) with the additive predictor � _fj_ ( _xj_ ), as we did for the logit model in (5.12) _j_ =1 

**==> picture [262 x 34] intentionally omitted <==**

196 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

_Table 5.18._ CUSTOMER SATISFACTION: CONFUSION MATRIX AND CLASSIFICATION ERRORS FOR EACH PREDICTION LEVEL FOR LINEAR AND ADDITIVE PROPORTIONAL ODDS MODELS 

Linear proportional odds model 

Additive proportional odds model 

|ˆ_y_|Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6<br>0<br>0<br>0<br>0<br>0<br>0<br>—<br>9<br>62<br>28<br>0<br>1<br>0<br>0.380<br>3<br>107<br>619<br>62<br>5<br>0<br>0.222<br>0<br>0<br>23<br>51<br>16<br>1<br>0.440<br>1<br>0<br>0<br>6<br>3<br>1<br>0.727<br>0<br>0<br>0<br>0<br>0<br>2<br>0.000|ˆ_y_|Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6|
|---|---|---|---|
|1<br>2<br>3<br>4<br>5<br>6||1<br>2<br>3<br>4<br>5<br>6|0<br>0<br>0<br>0<br>0<br>0<br>—<br>9<br>69<br>35<br>0<br>1<br>0<br>0.395<br>3<br>100<br>613<br>64<br>5<br>0<br>0.219<br>0<br>0<br>22<br>51<br>15<br>1<br>0.427<br>0<br>0<br>0<br>4<br>4<br>2<br>0.600<br>1<br>0<br>0<br>0<br>0<br>1<br>0.500|



A version of the local scoring algorithm (see algorithm 5.1) has been developed to fit this model. The estimated intercepts for the customer satisfaction problem are: 

**==> picture [176 x 22] intentionally omitted <==**

and figure 5.37 plots the estimated effects of the covariates. The second part of table 5.18 lists the misclassification errors for the additive proportional odds model in the validation set. The overall misclassification error was 26 _._ 2% and the percentage of dissatisfied customers classified as satisfied 7 _._ 0%. 

We then fitted some typical classification models by ignoring the ordering of the response variable. A multinomial model (see section 5.3.1) was fitted by selecting important variables with a stepwise procedure based on AIC. Table 5.19 summarizes the estimation procedure, and the first part of table 5.20 shows the misclassification errors in the validation set. The overall error was 27 _._ 4% and the error among dissatisfied customers 7 _._ 2%. 

We also fitted a multivariate multiple linear model, as discussed in section 5.4.2, considering each of the six variables as indicating a single level of satisfaction. The second part of table 5.20 shows the misclassification errors for this model. The overall error was 31 _._ 9%, and dissatisfied customers who are misclassified 12 _._ 6%. 

Misclassification errors for linear and quadratic discriminant analysis (see section 5.5.2) are shown in table 5.21, with an overall misclassification error of 28 _._ 3% for the linear version and 33 _._ 2% for the quadratic one. The percentage of dissatisfied customers classified as satisfied was 6 _._ 4% for LDA and only 5 _._ 9% for QDA. 

A _k_ -nearest-neighbor estimator (section 5.6) was fitted to the customer satisfaction data by assigning to each customer the satisfaction level chosen by the majority of _k_ closest customers (with respect to the covariates). The number _k_ of customers to be considered in each neighborhood was selected by fivefold crossvalidation (section 3.5.2) on the training set. The optimal choice for _k_ was 20, and the first part of table 5.22 shows the misclassification errors for this procedure. The overall error was 29 _. ._ 7%. 

**==> picture [323 x 543] intentionally omitted <==**

Figure 5.37 Customer satisfaction: Effect of variables on classification with proportional odds additive model. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

198 

_Table 5.19._ CUSTOMER SATISFACTION: ESTIMATED COEFFICIENTS OF MULTINOMIAL LOGIT MODEL (STANDARD ERRORS IN PARENTHESES) 

||log(**_π_**2_/_**_π_**1)|log(**_π_**3_/_**_π_**1)|log(**_π_**4_/_**_π_**1)|log(**_π_**5_/_**_π_**1)|log(**_π_**6_/_**_π_**1)|
|---|---|---|---|---|---|
|(intercept)|9_._44 (3_._073)|20_._66 (3_._101)|25_._18 (3_._180)|28_._47 (3_._421)|25_._63 (3_._871)|
|V5|−0_._34 (0_._703)|−0_._13 (0_._708)|0_._16 (0_._729)|−0_._57 (0_._793)|0_._47 (0_._946)|
|V6|−0_._53 (0_._634)|−0_._73 (0_._639)|−0_._97 (0_._660)|−1_._41 (0_._754)|−3_._36 (1_._269)|
|V25|−0_._07 (0_._329)|−0_._18 (0_._332)|−0_._47 (0_._339)|−0_._73 (0_._364)|−0_._53 (0_._421)|
|V26|−1_._49 (0_._455)|−1_._92 (0_._458)|−2_._28 (0_._464)|−2_._54 (0_._483)|−2_._70 (0_._543)|
|V27|0_._79 (0_._369)|0_._58 (0_._368)|0_._37 (0_._372)|0_._27 (0_._384)|0_._17 (0_._420)|
|V34|0_._94 (0_._381)|1_._16 (0_._382)|1_._22 (0_._390)|1_._49 (0_._412)|1_._03 (0_._470)|
|V39|0_._39 (0_._362)|0_._55 (0_._364)|0_._75 (0_._371)|0_._55 (0_._390)|0_._98 (0_._461)|
|V47|−0_._03 (0_._493)|−0_._35 (0_._495)|−0_._69 (0_._501)|−1_._00 (0_._515)|−0_._88 (0_._548)|
|V48|−0_._19 (0_._449)|−0_._38 (0_._451)|−0_._55 (0_._456)|−0_._37 (0_._472)|−0_._56 (0_._517)|
|V52|−0_._62 (0_._513)|−0_._99 (0_._514)|−1_._17 (0_._519)|−1_._45 (0_._530)|−1_._49 (0_._562)|
|V54|−0_._42 (0_._522)|−0_._63 (0_._523)|−0_._75 (0_._527)|−0_._88 (0_._538)|−1_._04 (0_._570)|
|V60|0_._01 (0_._032)|0_._03 (0_._033)|0_._03 (0_._034)|0_._01 (0_._039)|0_._07 (0_._048)|
|V63M|−0_._86 (0_._831)|−1_._40 (0_._834)|−0_._81 (0_._850)|−0_._88 (0_._901)|−0_._82 (1_._026)|



_D_ = 3372 _._ 143 on 70 d.f. 

_Table 5.20._ CUSTOMER SATISFACTION: CONFUSION MATRIX AND CLASSIFICATION ERRORS FOR EACH PREDICTION LEVEL FOR MULTINOMIAL AND LINEAR MULTIVARIATE MODELS 

||Multinomial logit model<br>Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6<br>0<br>1<br>2<br>0<br>0<br>0<br>1.000<br>8<br>62<br>40<br>0<br>1<br>0<br>0.441<br>4<br>106<br>608<br>65<br>6<br>0<br>0.229<br>0<br>0<br>20<br>49<br>12<br>1<br>0.402<br>1<br>0<br>0<br>5<br>6<br>3<br>0.600<br>0<br>0<br>0<br>0<br>0<br>0<br>—||Linear multivariate model|
|---|---|---|---|
|ˆ_y_||ˆ_y_|Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6|
|1<br>2<br>3<br>4<br>5<br>6||1<br>2<br>3<br>4<br>5<br>6|0<br>0<br>0<br>0<br>0<br>0<br>—<br>0<br>1<br>1<br>0<br>0<br>0<br>0.500<br>13<br>168<br>666<br>105<br>21<br>0<br>0.316<br>0<br>0<br>3<br>14<br>4<br>4<br>0.440<br>0<br>0<br>0<br>0<br>0<br>0<br>—<br>0<br>0<br>0<br>0<br>0<br>0<br>—|



Another approach to modeling overall customer satisfaction is to consider this response variable as a quantitative discrete variable and fit regression models. In this case, class prediction is obtained by rounding the predicted continuous values to the nearest integer. The second part of table 5.22 shows the classification errors for a linear model, in which the explanatory variables were selected by a stepwise procedure based on AIC. The overall error on the validation set was 27 _._ 3%, and the classification error, predicted as satisfied customers who are in fact dissatisfied, was a very low 4 _._ 8%. 

Several nonparametric models were fitted by following both strategies, considering responses as either categorical or quantitative variables. To balance bias and variance in the choice of tuning parameters, cross-validation was applied to the training set. 

Methods of Classification 

199 

_Table 5.21._ CUSTOMER SATISFACTION: CONFUSION MATRIX AND CLASSIFICATION ERRORS FOR EACH PREDICTION LEVEL FOR LINEAR DISCRIMINANT ANALYSIS AND QUADRATIC DISCRIMINANT ANALYSIS 

||Linear discriminant analysis<br>Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6<br>0<br>0<br>0<br>0<br>0<br>0<br>—<br>9<br>50<br>23<br>0<br>1<br>0<br>0.398<br>3<br>119<br>620<br>55<br>4<br>0<br>0.226<br>1<br>0<br>26<br>55<br>15<br>1<br>0.439<br>0<br>0<br>1<br>7<br>5<br>3<br>0.688<br>0<br>0<br>0<br>2<br>0<br>0<br>1.000||Quadratic discriminant analysis|
|---|---|---|---|
|ˆ_y_||ˆ_y_|Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6|
|1<br>2<br>3<br>4<br>5<br>6||1<br>2<br>3<br>4<br>5<br>6|0<br>1<br>0<br>0<br>0<br>0<br>1.000<br>9<br>95<br>95<br>0<br>1<br>0<br>0.525<br>3<br>73<br>518<br>55<br>4<br>0<br>0.207<br>1<br>0<br>54<br>50<br>15<br>1<br>0.587<br>0<br>0<br>3<br>13<br>5<br>3<br>0.792<br>0<br>0<br>0<br>1<br>0<br>0<br>1.000|



_Table 5.22._ CUSTOMER SATISFACTION: CONFUSION MATRIX AND CLASSIFICATION ERRORS FOR EACH PREDICTION LEVEL FOR _k_ -NEAREST-NEIGHBORS AND LINEAR MODEL, CONSIDERING RESPONSE AS QUANTITATIVE 

||_k_-nearest-neighbors<br>Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6<br>0<br>0<br>0<br>0<br>0<br>0<br>—<br>10<br>51<br>44<br>0<br>1<br>0<br>0.519<br>3<br>118<br>615<br>78<br>8<br>0<br>0.252<br>0<br>0<br>11<br>40<br>15<br>3<br>0.420<br>0<br>0<br>0<br>1<br>1<br>1<br>0.667<br>0<br>0<br>0<br>0<br>0<br>0<br>—|Linear model, quantitative response|Linear model, quantitative response|
|---|---|---|---|
|ˆ_y_||ˆ_y_|Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6|
|1<br>2<br>3<br>4<br>5<br>6||1<br>2<br>3<br>4<br>5<br>6|0<br>0<br>0<br>0<br>0<br>0<br>—<br>11<br>70<br>40<br>0<br>1<br>0<br>0.426<br>1<br>99<br>582<br>45<br>2<br>0<br>0.202<br>1<br>0<br>48<br>73<br>20<br>1<br>0.490<br>0<br>0<br>0<br>1<br>2<br>3<br>0.667<br>0<br>0<br>0<br>0<br>0<br>0<br>—|



Two tree models were fitted, one classification tree (section 5.7) with entropy as splitting criterion, and a regression tree (section 4.8) with a quantitative response. In both cases, the pruned trees were selected by fivefold cross-validation, as shown in figure 5.38. Table 5.23 lists misclassification errors for both procedures. The overall misclassification error was 29 _._ 5% for the classification tree and 29 _._ 0% for the regression tree; the error for dissatisfied customers was 9 _._ 6% for the categorical response variable and 8 _._ 5% when it was quantitative. 

Neural networks were also fitted, in two versions, with categorical and quantitative responses. The number of units in the hidden layer and weight decay were jointly chosen by fivefold cross-validation. The best classification network had three nodes with weight decay 0 _._ 05, a misclassification error of 27 _._ 9%, and an error for the dissatisfied customers of 8 _._ 2%. The best regression network had three nodes and a weight decay of 0 _._ 0005. The overall error on the validation set was 29 _._ 1%, and dissatisfied customers who were misclassified 7 _._ 3%. The entire set 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

200 

**==> picture [214 x 447] intentionally omitted <==**

**----- Start of picture text -----**<br>
Classification tree<br>V26 < 5.5<br>|<br>V26 < 3.5 V46 < 7.5<br>V47 < 3.5 V52 < 5.5<br>V52 < 5.5<br>V45 < 6.5 V26 < 7.5<br>4 3 3<br>4 3 V26 < 7.5 V53 < 8.5<br>3 3<br>3 3 2 2<br>Regression tree<br>V26 < 3.5<br>|<br>V47 < 3.5 V52 < 7.5<br>V52 < 1.5 V52 < 5.5<br>5 4 4 3<br>V48 < 5.5 V26 < 7.5<br>V47 < 3.5V27 < 5.5 [V26 < 6.5] 3 2<br>4 3 3 3 3<br>**----- End of picture text -----**<br>


Figure 5.38 Customer satisfaction. Top: pruned classification tree; bottom: regression tree. 

Projection pursuit (section 4.6) was also fitted to the data, the number of terms being selected by fivefold cross-validation. Table 5.25 shows the misclassification errors for this model. When the response variable was categorical, the best number of terms was 2, producing an overall error of 30 _._ 4% and an error for satisfied customers of 6 _._ 7%. When response was considered as quantitative, the best number of terms was 1, the overall error 28 _._ 1%, and the error for dissatisfied customers 6 _._ 2%. 

Methods of Classification 

201 

_Table 5.23._ CUSTOMER SATISFACTION: CONFUSION MATRIX AND CLASSIFICATION ERRORS FOR EACH PREDICTION LEVEL FOR TREE MODELS 

||Classifcation tree<br>Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6<br>0<br>0<br>0<br>0<br>0<br>0<br>—<br>11<br>73<br>61<br>0<br>1<br>0<br>0.500<br>1<br>96<br>597<br>84<br>11<br>0<br>0.243<br>1<br>0<br>12<br>35<br>13<br>4<br>0.462<br>0<br>0<br>0<br>0<br>0<br>0<br>—<br>0<br>0<br>0<br>0<br>0<br>0<br>—||Regression tree|
|---|---|---|---|
|ˆ_y_||ˆ_y_|Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6|
|1<br>2<br>3<br>4<br>5<br>6||1<br>2<br>3<br>4<br>5<br>6|0<br>0<br>0<br>0<br>0<br>0<br>—<br>9<br>80<br>67<br>0<br>1<br>0<br>0.490<br>3<br>88<br>590<br>76<br>8<br>0<br>0.229<br>0<br>1<br>13<br>40<br>16<br>3<br>0.452<br>1<br>0<br>0<br>3<br>0<br>1<br>1.000<br>0<br>0<br>0<br>0<br>0<br>0<br>—|



_Table 5.24._ CUSTOMER SATISFACTION: CONFUSION MATRIX AND CLASSIFICATION ERRORS FOR EACH PREDICTION LEVEL FOR NEURAL NETWORKS 

||FOREACHPREDICTIONLEVEL F|OR|NEURALNETWORKS|
|---|---|---|---|
||Classifcation neural network<br>Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6<br>0<br>0<br>0<br>0<br>0<br>0<br>—<br>11<br>71<br>48<br>0<br>1<br>0<br>0.458<br>1<br>98<br>605<br>73<br>8<br>0<br>0.229<br>0<br>0<br>16<br>42<br>13<br>1<br>0.417<br>1<br>0<br>1<br>4<br>3<br>3<br>0.750<br>0<br>0<br>0<br>0<br>0<br>0<br>—||Regression neural network|
|ˆ_y_||ˆ_y_|Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6|
|1<br>2<br>3<br>4<br>5<br>6||1<br>2<br>3<br>4<br>5<br>6|0<br>0<br>0<br>0<br>0<br>0<br>—<br>10<br>63<br>57<br>0<br>1<br>0<br>0.519<br>2<br>106<br>595<br>65<br>7<br>0<br>0.232<br>0<br>0<br>17<br>45<br>12<br>1<br>0.400<br>1<br>0<br>1<br>9<br>5<br>2<br>0.722<br>0<br>0<br>0<br>0<br>0<br>1<br>0.000|



_Table 5.25._ CUSTOMER SATISFACTION: CONFUSION MATRIX AND CLASSIFICATION ERRORS FOR EACH PREDICTION LEVEL FOR PROJECTION PURSUIT. RESPONSE VARIABLES CATEGORICAL AND QUANTITATIVE 

||CATEGORICAL AND|QUA|NTITATIVE|
|---|---|---|---|
||Projection pursuit with categorical<br>response<br>Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6<br>0<br>0<br>0<br>0<br>0<br>0<br>—<br>9<br>85<br>86<br>0<br>1<br>0<br>0.530<br>3<br>84<br>552<br>60<br>6<br>0<br>0.217<br>1<br>0<br>32<br>59<br>18<br>4<br>0.482<br>0<br>0<br>0<br>0<br>0<br>0<br>—<br>0<br>0<br>0<br>0<br>0<br>0<br>—||Projection pursuit with quantiative<br>regression|
|ˆ_y_||ˆ_y_|Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6|
|1<br>2<br>3<br>4<br>5<br>6||1<br>2<br>3<br>4<br>5<br>6|0<br>0<br>0<br>0<br>0<br>0<br>—<br>11<br>69<br>47<br>0<br>1<br>0<br>0.461<br>1<br>100<br>590<br>57<br>4<br>0<br>0.215<br>1<br>0<br>33<br>56<br>16<br>1<br>0.477<br>0<br>0<br>0<br>6<br>4<br>3<br>0.692<br>0<br>0<br>0<br>0<br>0<br>1<br>0.000|



D A T A A N A L Y S I S A N D D A T A M I N I N G 

202 

_Table 5.26._ CUSTOMER SATISFACTION: CONFUSION MATRIX AND CLASSIFICATION ERRORS FOR EACH PREDICTION LEVEL FOR POLYMARS AND QUANTITATIVE MARS 

||FOREACHPREDICTIONLEVEL FORPOLY|A|SANDQUANTITATIVEMARS|
|---|---|---|---|
||PolyMARS<br>Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6<br>0<br>0<br>0<br>0<br>0<br>0<br>—<br>9<br>59<br>42<br>0<br>1<br>0<br>0.468<br>3<br>110<br>605<br>72<br>6<br>0<br>0.240<br>0<br>0<br>23<br>43<br>13<br>1<br>0.463<br>0<br>0<br>0<br>4<br>5<br>3<br>0.583<br>1<br>0<br>0<br>0<br>0<br>0<br>1.000|ˆ_y_<br>1<br>2<br>3<br>4<br>5<br>6|Quantitative MARS|
|ˆ_y_|||Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6|
|1<br>2<br>3<br>4<br>5<br>6|||0<br>0<br>0<br>0<br>0<br>0<br>—<br>9<br>57<br>35<br>0<br>1<br>0<br>0.441<br>3<br>112<br>593<br>50<br>1<br>0<br>0.219<br>0<br>0<br>42<br>67<br>19<br>1<br>0.481<br>1<br>0<br>0<br>2<br>4<br>3<br>0.600<br>0<br>0<br>0<br>0<br>0<br>0<br>—|



_Table 5.27._ CUSTOMER SATISFACTION: CONFUSION MATRIX AND CLASSIFICATION ERRORS FOR EACH PREDICTION LEVEL FOR SVM, WITH RADIAL KERNEL AND LINEAR KERNEL 

||SVM, radial kernel<br>Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6<br>0<br>0<br>0<br>0<br>0<br>0<br>—<br>9<br>59<br>26<br>0<br>1<br>0<br>0.379<br>3<br>110<br>635<br>74<br>8<br>0<br>0.235<br>0<br>0<br>9<br>43<br>14<br>1<br>0.358<br>0<br>0<br>0<br>2<br>2<br>3<br>0.714<br>1<br>0<br>0<br>0<br>0<br>0<br>1.000||SVM, linear kernel|
|---|---|---|---|
|ˆ_y_||ˆ_y_|Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6|
|1<br>2<br>3<br>4<br>5<br>6||1<br>2<br>3<br>4<br>5<br>6|0<br>0<br>0<br>0<br>0<br>0<br>—<br>10<br>62<br>38<br>0<br>1<br>0<br>0.441<br>2<br>107<br>620<br>70<br>7<br>0<br>0.231<br>0<br>0<br>12<br>45<br>11<br>1<br>0.348<br>0<br>0<br>0<br>4<br>6<br>3<br>0.538<br>1<br>0<br>0<br>0<br>0<br>0<br>1.000|



Next, PolyMARS (section 5.6) and quantitative MARS (section 4.4.5) were fitted to the data by selecting the number of basis functions by generalized crossvalidation, as discussed in section 4.4.5. Table 5.26 lists misclassification errors, with an overall error of 28 _._ 8% for PolyMARS, 27 _._ 9% for quantitative MARS, and an error for dissatisfied customers of 7 _._ 9% for PolyMARS and 5 _._ 2% when the response variable was quantitative. 

SVM classification errors are shown in table 5.27. One radial and one linear function were selected as kernels, with tuning parameters _γ_ selected by fivefold cross-validation. Overall misclassification errors were 26 _._ 1% for the radial kernel and 26 _._ 7% for the linear one; the error for dissatisfied customers was 8 _._ 3% for the radial kernel and 7 _._ 8% for the linear one. 

Methods based on combinations of trees were also fitted to the data by considering both classification and regression trees. We present here only misclassification errors for the combinations of classification trees, because they are all lower than those for combinations of regression trees. Bagging and random forests were fitted by selecting the tuning parameters by fivefold cross-validation (table 5.28). Overall errors were 27 _._ 8% for bagging and 27 _._ 4% for random 

_Table 5.28._ CUSTOMER SATISFACTION: CONFUSION MATRIX AND CLASSIFICATION ERRORS FOR EACH PREDICTION LEVEL FOR BAGGING TREES AND RANDOM FORESTS 

||Bagging trees<br>Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6<br>2<br>0<br>0<br>0<br>0<br>0<br>0.000<br>8<br>68<br>41<br>0<br>1<br>0<br>0.424<br>2<br>101<br>605<br>70<br>8<br>0<br>0.230<br>0<br>0<br>24<br>45<br>14<br>1<br>0.464<br>0<br>0<br>0<br>4<br>2<br>3<br>0.778<br>1<br>0<br>0<br>0<br>0<br>0<br>1.000||Random forests|
|---|---|---|---|
|ˆ_y_||ˆ_y_|Actual response<br>Classif.<br>error<br>1<br>2<br>3<br>4<br>5<br>6|
|1<br>2<br>3<br>4<br>5<br>6||1<br>2<br>3<br>4<br>5<br>6|2<br>0<br>0<br>0<br>0<br>0<br>0.000<br>7<br>64<br>36<br>0<br>1<br>0<br>0.407<br>3<br>105<br>614<br>69<br>6<br>0<br>0.230<br>0<br>0<br>20<br>48<br>16<br>1<br>0.435<br>0<br>0<br>0<br>2<br>2<br>3<br>0.714<br>1<br>0<br>0<br>0<br>0<br>0<br>1.000|



_Table 5.29._ CUSTOMER SATISFACTION: PREDICTION ERRORS (%) FOR MODELS DESCRIBED IN SECTION 5.10.3 

|Model|Type of|Overall|Misclassifcation error|
|---|---|---|---|
||response|classifcation|of dissatisfed|
|||error|customers|
|Linear proportional odds|ordered|26.3|6.8|
|Additive proportional odds|ordered|26.2|7.0|
|Multinomial|categorical|27.4|7.2|
|Multivariate linear|categorical|31.9|12.6|
|_k_-nearest neighbour|categorical|29.3|8.7|
|Linear discriminant analysis|categorical|28.3|6.4|
|Quadratic discriminant analysis|categorical|33.2|5.9|
|Linear regression|quantitative|27.3|4.8|
|Classifcation tree|categorical|29.5|9.6|
|Regression tree|quantitative|29.0|8.5|
|Neural network|categorical|27.9|8.2|
|Neural network|quantitative|29.1|7.3|
|Projection pursuit|categorical|30.4|6.7|
|Projection pursuit|quantitative|28.1|6.2|
|PolyMARS|categorical|28.8|7.9|
|MARS|quantitative|27.9|5.2|
|Pupport vector machine –|categorical|26.1|8.3|
|radial kernel||||
|Support vector machine –|categorical|26.7|7.8|
|linear kernel||||
|Bagging trees|categorical|27.8|7.9|
|Random forests|categorical|27.0|7.6|



203 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

204 

**==> picture [262 x 270] intentionally omitted <==**

**----- Start of picture text -----**<br>
1.0<br>Linear proportional odds<br>Additive proportional odds<br>Linear discriminant analysis<br>Multinomial logistic<br>0.8 Classification tree<br>Neural network<br>Projection pursuit<br>MARS<br>Random forest<br>0.6 Bagging<br>0.4<br>0.2<br>0.0<br>0.0 0.2 0.4 0.6 0.8 1.0<br>Predicted probability<br>**----- End of picture text -----**<br>


Figure 5.39 Customer satisfaction: Calibration plot. 

forests, and the percentages of dissatisfied customers predicted as satisfied were 7 _._ 9% for bagging and 7 _._ 4% for random forests. Table 5.29 summarizes all these results. 

Lift and ROC curves are not appropriate in this multiclass context. However, a tool to evaluate more finely the adequacy of a classification criterion is the _calibration plot_ introduced by Dawid (2006) and presented by Venables & Ripley (2002, p. 349) for multicategory prediction. A model is suitable if its predicted probabilities are well calibrated—that is, if we predict an event with probability _p_ , a fraction of about _p_ of the events predicted actually occur. We can therefore plot the predicted probabilities against the actual proportion of events by comparing all the predicted _p_ with the observed relative frequency of occurrence for each single event. If these two quantities are approximately equal, the set of predictions may be regarded as probably valid or well calibrated. Figure 5.39 shows calibration plots for each of the models fitted in this section. We applied a smoothing method with adaptive bandwidth (loess, see section 4.2.4) to estimate the relative frequency of occurrence of each event. Clearly, calibration plots can be obtained only for methods in which the response is categorical. Most of the curves are very close to the diagonal line, showing that almost all the models are substantially well calibrated. Only SVM (not shown in the figure) and MARS show slight overconfidence in predictions, especially at probabilities close to 1. 

Methods of Classification 

205 

The lowest overall error, 26 _._ 1%, was obtained by the SVM with radial kernel. Unfortunately, this model has two drawbacks from the viewpoint of marketing managers: the percentage of dissatisfied customers misclassified as satisfied is quite high (8 _._ 3%, compared with the lowest 4 _._ 8% of linear regression), and it is not easy, in terms of questionnaire responses, to identify the characteristics of the customers allocated to each category of satisfaction. 

As already mentioned, a much easier interpretation is available for linear and additive proportional odds models, which in our case had an overall misclassification error almost as low as that of SVM (the linear proportional odds model had an overall error of 26 _._ 2%, and 6 _._ 8% for dissatisfied customers). 

If we consider the misclassification error for dissatisfied customers, the best prediction is obtained by the linear regression model, with an error of only 4 _._ 8%. The overall error of this model is 27 _._ 3%, which is not very high. 

In our case, two models were recommended to marketing managers: proportional odds and linear regression with quantitative responses. Both models are easy to interpret and have specific optimality, one for the overall misclassification error and the other the error for dissatisfied customers, and neither has a very high value for the other percentage of error. 

## 5.10.4 Web Usage Mining 

We now examine the website of a consulting company interested in better understanding its visitors, to identify appropriate marketing actions. Analysis of raw data (information about each hit and visitor) is extremely useful for decision making. Web programming tools allow companies to personalize their relationship with customers by configuring every page to be shown to visitors differently. Profiling visitors by their hit pattern is a simple way of identifying differences in interests between potential customers. 

In this context, applying data analysis and data mining techniques to discover patterns from the web is called _web mining_ and is generally divided into three main families, according to the primary type of data used: (i) _web usage mining_ , to discover user access patterns from information about hits and the number of clicks made by each user (often called _click-stream data_ ); (ii) _web content mining_ , to extract useful knowledge from web page contents (text, image, audio, or video data); and (iii) _web structure mining_ , for useful knowledge from hyperlinks and document structures. 

In the following, we only face some typical problems of interest for decision makers analyzing raw web usage data and refer to specific works for examples of web content and web structure mining. The data set we analyze contains data on about 26 _,_ 157 anonymous hits on the website of a consulting company. For each hit, the pages of the site visited over a fixed time interval are known. Visitors are identified by number and no personal information is given. There are 231 pages in the website, and the total number of page views for the entire site is 47 _,_ 387, so that every page was visited on average 205 times and each visitor hit an average of 1 _._ 81 pages. Because some of the pages have similar content, they were grouped into eight categories (home, contacts, communications, events, company, white papers, business units, consulting). The data are presented in greater detail in section B.8. 

206 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

## _Prediction of visits to “contacts” pages_ 

In this section, we consider the problem of predicting customers visiting one area of the website: “contacts.” Section 6.3 extends analysis of the same data set with some of the tools presented in chapter 6. 

The company’s marketing managers are interested in identifying the characteristics of visitors who finish their visit in the contacts area: they are likely to be interestedintheconsultingservicesofferedbythecompany.Identifyingpotentially interested customers before they visit the contacts page may be useful to the company, because they can be intercepted and offered some services before they explicitly request them. 

This marketing objective can be achieved by considering the statistical problem of predicting the indicator variable, that is, the last page hit by each visitor in the contacts area, by examining previously visited pages. Clearly, we need to identify visitors who saw at least two pages, that is, 4 _,_ 572. Figure 5.40 shows the frequency distribution of the number of web pages seen by each visitor who visited at least two pages. Because the number of visitors who went through more than 10 pages is small (about 500), we decided to keep only nine visited pages before the last one as predictors of the final hits on the contacts area. 

Among the 4 _,_ 572 last pages, only 229, or about 5%, fall in the contacts area. Such a low percentage and the small absolute value suggest using cross-validation to trade off bias and variance. We assessed the performance of different models by 10-fold cross-validation, using the same random partition for all methods. To compare the actually observed data, we predicted each of the 10 parts using the best model fitted by using the other parts, thus avoiding having to divide the data set into training and validation sets. We typically also used inner cross-validation to choose a model within each class. 

**==> picture [214 x 200] intentionally omitted <==**

**----- Start of picture text -----**<br>
2 3 4 5 6 7 8 9 10 11 12 13 14 15<br>1500<br>1000<br>500<br>0<br>**----- End of picture text -----**<br>


Figure 5.40 Web usage mining: Bar graph of number of web pages hit by each visitor who saw at least two pages. 

Methods of Classification 

207 

_Table 5.30._ WEB USAGE MINING: CROSS-VALIDATION PREDICTION ERRORS (%) FOR MODELS DESCRIBED IN SECTION 5.10.4 

|Model|Overall|False|% of|
|---|---|---|---|
||error|negatives|correct predictions|
||||over positive predictions|
|Linear discriminant analysis|9_._14|47.16|28.07|
|Linear regression|9_._49|46.29|27.27|
|Logistic regression|8_._68|51.96|28.35|
|Classifcation tree|9_._38|45.41|27.78|
|PolyMARS|9_._53|44.98|27.45|
|Neural network|9_._31|51.96|26.38|
|Support vector machine|9_._38|45.41|27.78|
|Bagging trees|9_._58|79.91|15.28|
|Random forests|42_._78|43.67|6.50|
|Boosting trees|9_._01|52.40|27.18|



The response variable has another characteristic: the distribution of visits to the contacts area is very unbalanced. Given the relatively small number of total observations available, we cannot obtain a sample stratified by the values of the response variable if we want to keep the training set a reasonable size. We therefore modify the fitting procedure slightly, to consider this characteristic, described next. 

Although all the explanatory variables are categorical, linear discriminant analysis can be fitted. These models do not need any particular specification to process unbalanced response variables. The overall error is 9 _._ 14%, false negatives (the error for actual visitors who finished their visit to the contacts area) is about 47 _._ 16%, and the percentage of visitors correctly predicted as positive is only 28.07%. Table 5.30 lists these errors for all fitted models. 

Linear and logistic models can easily be modified to process unbalanced training sets. For linear models, it is sufficient to change the threshold separating the classes in (5.8): instead of[1] 2[, we select a smaller number, closer to the observed proportion] of visitors to the contacts area, for example, 0 _._ 2. Similarly, for logistic regression, we assign visitors to one category or the other according to whether the estimated probability is greater or less than a smaller number with respect to[1] 2[—for example,] again 0 _._ 2. All errors are listed in table 5.30. 

To fit a classification tree, we need to cross-validate with respect to the choice of tree size. Ten-fold cross-validation is used for pruning. Given the unbalanced response, the consequences of misclassifying observations is more serious for visitors who finish in the contacts area. To take this into account, we define a 2 × 2 loss matrix _L_ , where _Ljk_ is the loss incurred in classifying a class _j_ observation as class _k_ . In our case, we consider _Lkk_ = 0 and assign a higher loss for classifying a visitor in the contacts area who actually finishes in another area. The losses are incorporated in the model process, and the observation in class _j_ is weighted by _Ljk_ . 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

208 

**==> picture [226 x 467] intentionally omitted <==**

**----- Start of picture text -----**<br>
Linear discriminant analysis<br>Linear regression<br>Logistic regression<br>Classification tree<br>MARS<br>Neural network<br>Support vector machine<br>Bagging<br>Boosting<br>Random forest<br>0.0 0.2 0.4 0.6 0.8 1.0<br>Fraction of predicted subjects<br>Linear discriminant analysis<br>Linear regression<br>Logistic regression<br>Classification tree<br>MARS<br>Neural network<br>Support vector machine<br>Bagging<br>Boosting<br>Random forest<br>0.00 0.05 0.10 0.15 0.20 0.25 0.30<br>Fraction of predicted subjects<br>10<br>8<br>6<br>Improvement factor 4<br>2<br>10<br>8<br>6<br>Improvement factor 4<br>2<br>**----- End of picture text -----**<br>


Figure 5.41 Web usage mining: Lift curves. 

The pruning level for PolyMARS is also identified by an inner cycle of crossvalidation. A loss matrix can be used to incorporate the various weights of the response classes in model selection. 

We also fit a neural network by averaging across several fits (10) to overcome the problem of finding multiple local maxima of the likelihood. We choose 

Methods of Classification 

209 

_Table 5.31._ WEB USAGE MINING: ESTIMATES FOR LOGISTIC MODEL 

||Estimate|SE|_z_-value|_p_-value|
|---|---|---|---|---|
|(intercept)|−2_._5313|0.1226|−20_._64|0.0000|
|page−4: white papers|1_._5103|0.6248|2_._42|0.0156|
|page−3: business area|0_._5396|0.3070|1_._76|0.0788|
|page−2: business area|−1_._2908|0.3323|−3_._88|0.0001|
|page−2: consulting|−0_._8367|0.2928|−2_._86|0.0043|
|page−1: business area|−1_._8203|0.2754|−6_._61|0.0000|
|page−1: home|1_._7043|0.1596|10_._68|0.0000|
|page−1: white papers|−3_._5884|0.7345|−4_._89|0.0000|



the number of hidden units and the amount of weight decay by inner crossvalidation. As in the linear model, here, too, we tackle unbalanced classes in responses by changing the threshold separating predicted classes. SVM tuning parameters are selected by inner cross-validation, and weights are supplied. In our example, an SVM with a radial kernel was fitted. Random forests, bagging and boosting were fitted by including trees modified to take unbalanced responses into account. 

Figure 5.41 compares smooth versions of lift curves for all fitted models. The top panel shows the entire lift curve, and the bottom one the same function enlarged for small fractions of predicted visitors. 

Logistic regression has the lowest overall error and predicts that 388 visitors are interested in contacts, although only 110 of them actually finished their visits on a page of the contacts area, which is the highest percentage among the various models. Nevertheless, the percentage of false negatives suggests using a random forest (which, however, has an overall error that is too high) and PolyMARS or SVM. An SVM seems to be preferable, although we have a small percentage of predicted subjects in the lift curve. 

Conversely, if we are interested in identifying a small number, say, less than 10%, of subjects who are most likely to visit the contacts area, an SVM is the most preferable predictor. Alternatively, logistic regression and boosting trees show the best lift curves for fractions of predicted subjects over 10%. The particular ease of interpretation of logistic regression results leads us to choose this model for the final prediction, if we are not interested in very small numbers of predicted subjects. To obtain a set of interpretable parameters, the simplest method is fitting logistic regression with all available data. Table 5.31 lists the estimates of parameters for such a model. 

Given all the other variables, homepage visits increase to more than five times the probability of concluding the path in the company website with a page in the contacts area. Visits to business area pages or white papers is negatively related to the response, even in cases when these pages had been visited some clicks earlier, when they may have had a positive impact. Visits to pages in the consulting area have a decreasing impact on the probability of visiting the contacts area later. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

210 

## EXERCISES 

- 5.1 Consider a classification model with two categories and assume that we know the fitted probabilities of the vector of successes for the units of a test set, say, _p_ = ( _p_ 1 _, . . . , pn_ ). Also assume that we know the correct membership category of all units and they are _y_ = ( _y_ 1 _, . . . , yn_ ). Compute the lift curve from vectors _p_ and _y_ . 

- 5.2 For every classification problem in two categories we have two lift curves, one for each of two classes (success and failure). What is the relationship between these curves? If we know vectors _p_ and _y_ of exercise 5.1 for the class identified by (successes), is it also possible to construct the lift curve for the other class? If so, what is explicit form of the lift curve for failures? 

- 5.3 Is it possible to have a lift curve that is not monotone-decreasing? If so, how do we interpret this fact? 

- 5.4 Explain why, in ROC curves, the diagonal corresponds to random 

- 5.5 Is it possible to have a ROC curve that is completely or partly under the diagonal? If so, how do we interpret this fact? 

- 5.6 Write the equation of the line and the dashed curve in the two panels of figure 5.8. 

- _p_ 

- 5.7 Prove (5.3), where _ηr_ ( _xi_ ) = _β_ 0 + � _xijβjr_ , using the fact that (5.2) also _j_ =1 

- holds with _r_ = 0, by setting _βj_ 0 = 0 _,_ for _j_ = 0 _, . . . p_ . 

- 5.8 In a classification problem with _K_ = 2 classes, multiple linear regression can be used as a classification method in two ways, using either a column of indicator variables and selecting the class closest to the interpolated value, or two indicator variables (and two regression models) and selecting the one corresponding to the higher estimate. Why are the two procedures equivalent? 

- 5.9 In the case of linear discriminant analysis with _K_ = 2 and equal a priori probability for the two groups, show that _d_ 1( _x_ ) _> d_ 2( _x_ ) takes the form 

**==> picture [127 x 13] intentionally omitted <==**

where _μ_ = 2[1][(] _[μ]_[1][ +] _[ μ]_[2][).] 

- 5.10 Show that the classification rule of discriminant analysis described in section 5.5.2, in which _K_ = 2 and group sizes are equal, coincides with the rule obtained though the linear model presented in section 5.4; show also that this statement does not hold if classes have different numbers of observations (Fisher 1936). 

Methods of Classification 

211 

- 5.11 In classification trees, if the impurity measure is entropy, how can we computethegainachievedwhenpassingfrom _J_ to _J_ + 1leaves,corresponding to _D_[∗] _j_[−] _[D][j]_[ in the case of regression trees?] 

- 5.12 Show that the Gini index is a first-order approximation of entropy. Show also that entropy is not smaller than the Gini index. 

6 

## Methods of Internal Analysis 

This chapter differs from the previous two in that we no longer presume the existence of a response variable related to explanatory variables. Here, all variables are on the same level. 

In the terminology of machine learning literature, the following themes come under the heading of unsupervised learning, in the sense that learning is not driven by a set of observed cases; the themes of the previous two chapters cover supervised learning. 

## 6.1 CLUSTER ANALYSIS 

## 6.1.1 General Remarks 

We wish to group _n_ available units into _K_ groups, but—unlike the case of classification problems—we have no preassigned system of classification and therefore no response categorical variables. We are speaking of _cluster analysis_ . 

Typically, because we have no information about the number or nature of the groups, we look for a method to form them by starting from the available variables. Sometimes, a posteriori, we try to interpret the resulting groups. A typical example is that of the segmentation of a company’s customer base. From data on how the chosen products are used, personal data, responses to questionnaires, and other sources of information, we arrive at customer groups, called “segments.” To define _marketing actions_ , we must be able to characterize each group, identifying some of the main explicit aspects, called “profiles.” 

Methods of Internal Analysis 

213 

In other cases, we have in mind certain customer profiles, but cannot directly observe whether an individual fits into a given profile, and we try to construct the closest fit of such profiles from the groups of individuals. In this case, the number _K_ can be given as known. 

˜ For the _i_ th individual, we have available _p_ variables, _xi_ = ( _xi_ 1 _, . . . , xip_ )[⊤] , of which some are quantitative and some qualitative ( _i_ = 1 _, . . . , n_ ). We allocate individuals who are more similar to each other in the same group, and dissimilar individuals in other groups. Note that these methods are essentially descriptive, at least regarding the more classical ones presented here. 

## 6.1.2 Distances and Dissimilarities 

A fundamental role is clearly played by the way we measure the “nearness” between individuals or, equivalently, their “distance.” There are many possible ways of quantifying this, and they vary in nature of the variables in question and what our aimsare.Weusethegeneralterm _dissimilarity_ torefertothesemeasuresofdistance. 

In any case, the dissimilarity _d_ ( _i, i_[′] ) between individuals _i_ and _i_[′] is based on the composition evaluated for dissimilarities in each of the _p_ observed variables, say, _dj_ ( _xij, xi_ ′ _j_ ) for _j_ = 1 _, . . . , p_ . There are many options to define functions _dj_ ( _x, x_[′] ), but in all cases some conditions must be respected 

**==> picture [136 x 14] intentionally omitted <==**

We often also need a condition of symmetry, _dj_ ( _x, x_[′] ) = _dj_ ( _x_[′] _, x_ ). A further condition that is often respected is triangle inequality 

**==> picture [122 x 14] intentionally omitted <==**

and in this case dissimilarity qualifies as a _distance_ . 

For quantitative variables, the main choice for dissimilarity is given by the square of the Euclidean distance 

**==> picture [89 x 15] intentionally omitted <==**

although it is by no means the only one. For qualitative variables we often use 

**==> picture [108 x 14] intentionally omitted <==**

where _I_ ( _x_ = _x_[′] ) is 1 if _x_ and _x_[′] coincide, and 0 otherwise. For ordinal qualitative variables, that is, ones with levels ordered naturally, we assign a conventional score, such as 1 _,_ 2 _, . . . , m_ , and then treat them as if they were quantitative variables. 

For both qualitative and quantitative variables, it is useful to introduce some form of normalization. For quantitative variables, the scale on which variable _xj_ is measured clearly influences the dimension of _dj_ and therefore its contribution to the sum (6.1). This observation suggests that we can divide the squared distance by the variance of _xj_ . Similarly, for qualitative variables, we should keep in mind the number of levels of variables _xj_ , because the correspondence of observations 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

214 

between two subjects does not have the same significance if _xj_ has 2 or 20 possible alternatives. A simple way of considering this is to divide _dj_ by the number of levels of _xj_ . However, these indications are not followed systematically, because we can easily produce examples where the effect of these normalizations is more harmful than useful, leading to groups that are less easily distinguished than they were originally. 

Once functions _dj_ are chosen, the problem remains of combining them to obtain dissimilarities _d_ ( _i, i_[′] ). The simplest option is clearly to add them, by 

**==> picture [218 x 35] intentionally omitted <==**

Whatever combination is adopted, conditions 

**==> picture [214 x 12] intentionally omitted <==**

should be satisfied, and also _d_ ( _i, i_[′] ) = 0, if and only if all the _dj_ components are 0. 

If all the variables are quantitative, we can also use the distances listed in table 6.1. In more common cases when variables are both quantitative and qualitative, it is reasonable to calculate the dissimilarities separately for the three sets of quantitative variables, qualitative variables and ordinal qualitative variables; obtaining respectively _d_[(1)] ( _i, i_[′] ), _d_[(2)] ( _i, i_[′] ), and _d_[(3)] ( _i, i_[′] ); and last, combining them in the form 

**==> picture [223 x 29] intentionally omitted <==**

where _w_ 1, _w_ 2, and _w_ 3 are weights that may be chosen subjectively to make the three components of comparable size. 

The values of _d_ ( _i, i_[′] ) are arranged in a _n_ × _n dissimilarity matrix D_ , with zero diagonal and nonnegative elements. When the property of symmetry is valid for all functions _dj_ ( _i, i_[′] ), matrix _D_ is symmetric. Because this symmetric property is required by most of the algorithms used, we can fulfill the requirement by redefining _D_ as ( _D_ + _D_[⊤] ) _/_ 2. 

Once dissimilarity matrix _D_ is constructed, it constitutes the basis for most of the grouping methods currently used. Each of these sets is determined to amalgamate subjects with low dissimilarity and separate those with high dissimilarity. These methods are usually grouped according to the following scheme: 

**==> picture [166 x 46] intentionally omitted <==**

There are also other algorithms that do not fit into this scheme. They are not based on matrix _D_ , and therefore are not treated here, where we confine ourselves to classical procedures. 

Methods of Internal Analysis 

215 

_Table 6.1._ SOME COMMON TYPES OF DISSIMILARITY USING CLUSTERING METHODS WITH QUANTITATIVE VARIABLES 

|WITH|QUANTITATIVEV|ARIABLES||
|---|---|---|---|
|Name||_d_(_i, i_′)||
|Euclidean distance||||
|simple:_wj_ =1<br>weighted with variance_wj_ =1_/s_2<br>_j_||��_p_<br>_j_=1 _wj_ (_xij_ −_xi_′_j_)2�1_/_2||
|weighted with range:_wj_ =1_/R_2<br>_j_||||
|Mahalanobis distance<br>(where_�_is a positively defned|matrix)|�<br>(˜_xi_−˜_xi_′)⊤_�_−1(˜_xi_−˜_xi_′)|�1_/_2|
|Minkowsky distance<br>(for a parameter_λ_≥1)||��_p_<br>_j_=1 _wj_ (_xij_ −_yi_′_j_)_λ_�1_/λ_||
|Manhattan distance||�_p_<br>_j_=1 _wj_ |_xij_ −_xi_′_j_|||
|Canberra metric (one of several variants),<br>where terms in which denominator is 0<br>are excluded||�_p_<br>_j_=1<br>|_xij_−_xi_′_j_|<br>|_xij_| + |_xi_′_j_|||
|_L_∞norm||max_j_|_xij_−_xi_′_j_|||



## 6.1.3 Nonhierarchical Methods 

The best-known and by far the oldest nonhierarchical method is called _K_ -means and was designed for continuous variables. The basic idea is that of identifying aggregating points, called _centroids_ , around which to construct groups, attributing observations to the closest centroid. The centroids are not irrevocably fixed but are themselves subject to sequential updating as the algorithm proceeds. 

Let us assume that we have subdivided observations into _K_ groups, according to a certain criterion. We note that total dissimilarity, summing all the elements of _D_ , can be decomposed as 

**==> picture [331 x 40] intentionally omitted <==**

where _G_ ( _i_ ) indicates the group to which the _i_ th individual is assigned, and 

**==> picture [148 x 79] intentionally omitted <==**

are the overall dissimilarity _within_ groups and _between_ groups, respectively. As we want to choose the groups in such a way as to minimize the dissimilarity within 

216 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

them, we try to minimize _D_ within. Because the total dissimilarity depends neither on _K_ nor on the way in which the groups are created, this aim is equivalent to maximizing _D_ between. 

Since the number of possible clusters which can be constructed for a fixed value of _K_ is finite, in principle this minimization is achievable in a finite number of operations by scanning all possible choices. Clearly, this is not a viable option, as the number of possible groupings grows at impressive speed with _n_ , and we must resort to suboptimal algorithms. 

A classic algorithm of this type is that of _K_ -means, which uses the Euclidean distance to construct dissimilarities between quantitative variables. For a known property of the sample mean, we can write 

**==> picture [312 x 35] intentionally omitted <==**

where _mk_ is the mean vector of the subjects of the _k_ th group, that is, the vector form of the arithmetic mean of each variable. 

The method aims at minimizing this expression of _D_ within, given group number _K_ and the initial position of centroids _mk_ . The algorithm then proceeds iteratively, clustering individuals round the centroids, which are subject to iterative uploading, until convergence. This convergence is ensured but does not necessarily correspond to an absolute minimum of the objective function. 

The procedure is presented in detail in algorithm 6.1. Step 2.a guarantees that deviance (6.2) is minimum once the centroids have been chosen, and step 2.b guarantees the deviance is minimum once the subjects have been allocated to their groups. 

Figure 6.1 illustrates the outcome of the _K_ -means method applied to two sets of simulated data, with very simple structure, so that in both cases three groups of points are evident in a basically nonambiguous way. For illustrative purposes, we use only _p_ = 2 variables. The top panels illustrate the method with _K_ = 3 and show the final outcome with two choices of initial centroid; the bottom-left panel 

## **Algorithm 6.1** _K_ -means 

1. Choose _K_ and initial arbitrary centroids _m_ 1 _, . . . , mK_ . 

2. Cycle for _r_ = 1 _,_ 2 _, . . ._ : 

   - ˜ 

   - a. for _i_ = 1 _, . . . , n_ , assign _xi_ to group _k_ , so that ∥˜ _xi_ − _mk_ ∥ is minimum, 

   - b. for _k_ = 1 _, . . . , K_ , let _mk_ be equal to the arithmetic mean of the subjects belonging to group _k_ , 

until centroids _m_ 1 _. . . , mK_ stabilize. 

Methods of Internal Analysis 

217 

**==> picture [328 x 326] intentionally omitted <==**

**----- Start of picture text -----**<br>
−2 −1 0 1 2 3 4 −2 −1 0 1 2 3 4<br>x1 x1<br>−2 −1 0 1 2 3 4 0.1 0.2 0.3 0.4 0.5 0.6<br>x1 x1<br>4 4<br>3 3<br>2 2<br>x2 x2<br>1 1<br>0 0<br>−1 −1<br>−2 −2<br>4 0.9<br>3 0.8<br>2 0.7<br>x2 x2<br>1 0.6<br>0 0.5<br>−1 0.4<br>−2<br>**----- End of picture text -----**<br>


Figure 6.1 Simulated data with three groups each. Top and bottom-left panels: data set C1; bottom-right panel: data set C2. Groups are distinguished by different symbols; squares: initial position of centroids, chosen randomly; line segment: direction of final positions of centroids. 

refers to the case when _K_ = 4. For these data, the chosen groups, distinguished by type of symbol, correspond satisfactorily to those that are true, in the sense that “true” applies to the top panels whatever their initial configuration. The bottomleft panel obviously contains one group too many, but the union of two of the chosen groups corresponds substantially to one of the true groups. The same type of outcome is also maintained when the configuration of the initial centroids changes greatly. 

However, the result of the method is very different in the bottom-right panel, which refers to other data, with a group structure of a more filiform type. In this case, the individual groups are obviously different from those that are true, this is also the case when starting with other choices of initial centroids. This different type of result is due to the choice of metric used, because the Euclidean distance allows for spherical structures. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

218 

This method has two limitations: (1) it requires the initial choice of various elements; (2) it can only be applied to quantitative variables. This second restriction can be overcome by substituting the Euclidean distance with another form of dissimilarity, adapting to the case of qualitative variables, and introducing the concept of _medoid_ , that is, a unit representative of the group that minimizes within-group dissimilarity. Conversely, the requirement to specify a value for _K_ is, in many cases, a problem, when we have no information on the structure of the data to guide us. 

## 6.1.4 Hierarchical Methods 

To overcome the foregoing inconvenience and to solve the abrupt specification of a value for _K_ , methods that structure the data hierarchically and organize them into groups are often used. This is done by associating the set of points with a binary tree structure, so that the leaves of the tree correspond to the units and the nodes to subsets of the points. Due to the nature of a binary tree, this introduces a hierarchy in the subsets associated with the branches. 

There are two large families of hierarchical methods: _agglomerative_ and _divisive_ . We start with those that are agglomerative, which are more highly developed and frequently used. 

An _agglomerative_ method starts from an initial state in which _K_ = _n_ , that is, a state in which each individual constitutes a separate group, and then proceeds by successive aggregations of previously formed groups having low dissimilarity. This sequence of aggregations continues until _K_ = 1, that is, when all the individuals belong to the same group. 

Clearly, this method of proceeding gives rise to a hierarchical structure in which the subdivision into _K_ groups “contains” the subdivision in _K_ + 1 groups, in the sense that the former is obtained from the latter by aggregating two groups. figure 6.2 shows an example of such a tree; in this context, this type of diagram is called a _dendrogram_ . The reason for the different lengths of the vertical stems is given shortly. 

To turn the general framework into an operational procedure, we need to introduce a measure of dissimilarity between the two groups. At the start of the agglomeration process, when all the groups are formed of a single unit, it is clear that _d_ ( _i, i_[′] ) also constitutes the dissimilarity between the two degenerate groups formedby { _i_ } and { _i_[′] }.Inlaterstages,weagglomerategroupsformedofseveralunits and, correspondingly, need a dissimilarity measure between groups composed of more than one unit. If _G_ and _G_[′] represent two groups, the three most frequently used measures are: 

**==> picture [264 x 55] intentionally omitted <==**

which are called _single link_ , _complete link_ , and _average link_ , respectively. Obviously the grouping changes with the adopted measure. 

Methods of Internal Analysis 

219 

**==> picture [251 x 104] intentionally omitted <==**

**----- Start of picture text -----**<br>
17<br>18<br>25<br>2 3 13 9 12 19 21 22 29<br>11 20 10 26 1 14 24 27 15 30 7 28 5 6 8 16 4 23<br>**----- End of picture text -----**<br>


Figure 6.2 A dendrogram. 

Information about the dissimilarity between two groups can be incorporated into a dendrogram by making the height of the vertical line connecting two successive ramifications on the same branch proportional to the fall in dissimilarity obtained by passing from _K_ to _K_ + 1 groups. 

This fact can be used as a guide to use the dendrogram for the operative choice of number of groups, if this is not known a priori. For example, in figure 6.2, the two dashed lines identify _K_ = 3 and _K_ = 7 groups. We usually cut the tree horizontally at the level where the vertical stems are longer, and the number of intersecting stems represents the number of prechosen groups. “Objective rules” also exist, but which of them is preferable is not immediately obvious. Again, the analyst must make an evaluation. 

To appreciate the effect of different types of link, we examine figure 6.3, which shows the same data as the first three panels in figure 6.1. From top to bottom, the first pair of panels refers to the single link, the second to the complete link, and the third to the average link. For each pair, the left panel presents the dendrogram and the right panel the clusters corresponding to _K_ = 3, with the same symbols as in figure 6.1 to distinguish the groups. 

In this example, the single link method clearly does not work nearly as well as the others. This negative result is due to the spheroidal form of the groups. In fact, in figure 6.4, in which the data from the last panel of figure 6.1 were used, the groups determined by the complete and average links do not correspond to the true groups, whereas the single link does allow them to be identified. This means 

**==> picture [328 x 494] intentionally omitted <==**

**----- Start of picture text -----**<br>
−2 −1 0 1 2 3 4<br>x1<br>−2 −1 0 1 2 3 4<br>x1<br>−2 −1 0 1 2 3 4<br>x1<br>1.0<br>4<br>0.8<br>3<br>0.6 2<br>x2<br>0.4 1<br>0.2 0<br>0.0 −1<br>−2<br>7<br>4<br>6<br>5 3<br>4 2<br>3 x2<br>1<br>2<br>0<br>1<br>0 −1<br>−2<br>4<br>4<br>3<br>3<br>2<br>2<br>x2<br>1<br>1<br>0<br>0 −1<br>−2<br>**----- End of picture text -----**<br>


Figure 6.3 Simulated data C1: Groups made with agglomerative hierarchical method and three types of link (from top to bottom: single, complete, and average links). Left: dendrogram; right: clustering when _K_ = 3. 

**==> picture [328 x 503] intentionally omitted <==**

**----- Start of picture text -----**<br>
0.1 0.2 0.3 0.4 0.5 0.6<br>x1<br>0.1 0.2 0.3 0.4 0.5 0.6<br>x1<br>0.1 0.2 0.3 0.4 0.5 0.6<br>x1<br>0.14<br>0.12 0.9<br>0.10 0.8<br>0.08 0.7<br>x2<br>0.06<br>0.6<br>0.04<br>0.5<br>0.02<br>0.4<br>0.00<br>0.8<br>0.9<br>0.6 0.8<br>0.7<br>0.4 2<br>x<br>0.6<br>0.2<br>0.5<br>0.0 0.4<br>0.4<br>0.9<br>0.3 0.8<br>0.7<br>0.2 x2<br>0.6<br>0.1<br>0.5<br>0.0 0.4<br>**----- End of picture text -----**<br>


Figure 6.4 Simulated data C2: Groups made with agglomerative hierarchical method and three types of link (from top to bottom: single, complete, and average links). Left: dendrogram; right: clustering when _K_ = 3. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

222 

that the single link tends to work better with filiform types of geometric structures and the complete link with spheroidal structures. 

In one sense, divisive methods represent the dual approach to agglomerative methods. Here we follow a logic similar to the previous case but start from the opposite extreme—that is, first forming one group that includes all units, and then proceeding by successive subdivisions. 

The division of a group is evaluated according to the dissimilarity between the various choices of two subgroups that can be formed starting from the original one. These dissimilarities between subgroups are evaluated with the same forms of links already seen for agglomerative methods. However, divisive methods have been less thoroughly explored and are less frequently used than agglomerative ones. 

## _Bibliographical notes_ 

A pioneering work on cluster methods is by Hartigan (1975). Another classic account is found in Mardia et al. (1979, ch. 13), which, although more concise, is still clearly described. A work that in its time significantly influenced the formulation of the concept of dissimilarity is that of Gower (1971). A relatively more recent treatment, with particular emphasis on computational aspects, is by Kaufman & Rousseeuw (2009). 

## 6.2 ASSOCIATIONS AMONG VARIABLES 

The previous section concerned the clustering of units and, in a more general sense, their forms of association. We now deal with the dual problem of relations among variables. 

## 6.2.1 Elementary Notions of Graphical Models 

A large proportion of statistical methodology is concerned with studying how variables are connected to each other. This broad problem has various forms, according to whether the variables are quantitative or qualitative, whether there is a natural distinction between explanatory and response variables, and so on. In fact, much of what we have seen in the previous chapters deals with the problem of relationships between variables in the asymmetric case, that is, one or more variables that are responses to explanatory ones. Here, we briefly deal with the symmetric case, in which all variables play the same role. 

The best-known concept of dependence between two variables is probably that of correlation. If _xr_ and _xs_ are the vectors of observations on two quantitative variables, recorded from the same _n_ units, the sample correlation between them can be written as 

**==> picture [236 x 27] intentionally omitted <==**

where _xr_[′] and _xs_[′] represent the deviations of _xr_ and _xs_ from their respective arithmetic means, and the notation ⟨ _xr_[′] _, xs_[′] ⟩ indicates the inner product.This is not the most common way the correlation is expressed algebraically, but it has 

Methods of Internal Analysis 

223 

the advantage of showing its geometric interpretation, and it highlights the fact that correlation measures the degree of alignment of the directions of _xr_[′] and _xs_[′] . If we have _p_ numerical variables, say, _x_ 1 _, . . . , xp_ , we calculate the correlation matrix formed by all the pairs of corr{ _xr, xs_ }, for _r, s_ = 1 _, . . . , p_ . 

The population version of the concept of correlation, referred to two random variables, _Xr_ and _Xs_ , is given by 

**==> picture [202 x 29] intentionally omitted <==**

where _Xr_[′] = _Xr_ − _μr_ , _Xs_[′] = _Xs_ − _μs_ denote the centred variables after subtracting their mean values, _μr_ and _μs_ , and we have used the nonstandard notation 

**==> picture [77 x 16] intentionally omitted <==**

referred to a 0-mean random variable _U_ . As for the sample version, a set of _p_ random variables leads to the introduction of a correlation matrix formed by all pairs corr{ _Xr, Xs_ }; see also section A.2.1. 

Although the correlation matrix is a fundamental tool in studying dependence structures, it does have limitations. One is the fact that a correlation reflects exclusively the dependencies of _linear_ type between variables, but as this is discussed in every introductory textbook on statistics, we do not discuss it now. 

Another source of difficulty in interpreting the values of the correlation matrix is illustrated by the following simple numerical example, taken from Mardia et al. (1979, p. 170). In a sample of children, the variables are: 

**==> picture [212 x 10] intentionally omitted <==**

and a sample correlation matrix is 

**==> picture [160 x 39] intentionally omitted <==**

The high correlation between weight and intelligence, 0 _._ 6162, indicates a relationship between variables that is very surprising and unlikely on general grounds. The problem lies in the third variable, age, and how it interacts with the other two. 

Therefore, for better indications, we must examine the dependence between _x_ and _y_ after the effect of _z_ has been removed. This leads us to obtain the residual vectors 

**==> picture [268 x 21] intentionally omitted <==**

after the linear dependence on _z_ has been removed by fitting a simple regression model of type (2.1) on each of _x_ and _y_ and to consider the correlation between 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

224 

these residual vectors. We then arrive to the introduction the _partial correlation_ between _x_ and _y_ given _z_ , which is defined as 

**==> picture [130 x 20] intentionally omitted <==**

Again, a population version of the partial correlation is introduced, replacing sample vectors by random variables and sample moments by population moments, as for the correlation. 

In our numerical example, the partial correlation between weight and intelligence, once age is fixed, drops to a much more reasonable 0.0286; this means that they are essentially uncorrelated. Repeating the previous operation for all the variables—that is, considering all the possible pairs of variable—we obtain the partial correlation matrix 

**==> picture [104 x 39] intentionally omitted <==**

where we round the values to only one decimal place; in particular, 0.0286 is rounded to 0. This is reasonable when we consider that the observed correlations are subjected to sampling variability. To proceed in a canonical way, we would have to test a statistical hypothesis formally, but that is not the point we wish to focus on now. 

The matrix of partial correlations, _R_[∗] , is much easier to interpret than that of marginal correlations, _R_ , particularly when we associate it with a graph like that shown in figure 6.5, which is made up of one node for every variable and one nondirected edge for every nonzero partial correlation. The graph shows that _x_ and _y_ are correlated only “through” _z_ , and are uncorrelated conditionally on the value assumed by _z_ . 

Now assume joint normality of the three parent random variables, say, ( _X, Y , Z_ ). Because independence and lack of correlation are equivalent conditions in the context of multivariate normal distributions, we have a situation of _conditional independence_ between _X_ and _Y_ , conditionally on the value of _Z_ : we write _X_ ⊥⊥ _Y_ | _Z_ . 

**==> picture [137 x 97] intentionally omitted <==**

**----- Start of picture text -----**<br>
Z<br>X Y<br>**----- End of picture text -----**<br>


Figure 6.5 A simple graphical model. 

Methods of Internal Analysis 

225 

The need to develop tools for examining and correctly interpreting complex dependence structures becomes more pressing as the number of available variables increases. The theoretical apparatus is often called a _graphical model_ because it is linked to the idea of expressing the dependence structure by means of a graph. This theory is highly structured: it does not handle only continuous variables, nor does it refer only to analysis of association structures of a symmetric nature, but it also covers the asymmetric case, in which one or more variables play the role of the response variable with respect to the explanatory variables, as described in previous chapters. Here we merely mention the analogy of the previous case when using categorical variables. 

Now move to the case where _X_ and _Y_ represent two categorical variables. Their joint distribution is identified by the set of probabilities 

**==> picture [110 x 14] intentionally omitted <==**

where _xj_ and _yk_ vary in the set of levels for variables _X_ and _Y_ , respectively. It is also useful to rewrite these probabilities in another form, based on the identity 

**==> picture [101 x 26] intentionally omitted <==**

where symbol + indicates the sum of the values over the corresponding index (e.g., _πj_ + =[�] _k[π][jk]_[). This yields] 

**==> picture [221 x 15] intentionally omitted <==**

where _βj[X]_[=][ log] _[ π][j]_[+][, and analogously for the other terms.] 

This factorization of probabilities allows a clearer interpretation of the ingredients. Because _X_ and _Y_ are categorical variables, the right-hand side is similar to the same type used in two-way analysis of variance. In our case, too, the various parameters are subject to constraints, such as 

**==> picture [104 x 27] intentionally omitted <==**

Terms _βj[X]_[and] _[ β] k[Y]_[of (6.3) play the role of main effects and reflect the marginal] distribution of _X_ and _Y_ . “Interaction” term _βjk[XY]_[, which depends on the relationship] between probabilities _πjk_ and their value in the independence case, _πj_ + _π_ + _k_ , constitute an _association measure_ between factors _X_ and _Y_ . Specifically, if _β[XY]_ = 0 _jk_ for all _j_ and _k_ , we have a situation of independence between _X_ and _Y_ ; conversely, positive values indicate that the probability of event { _X_ = _xj_ ∩ _Y_ = _yk_ } is higher than in the independence hypothesis, and there is therefore a positive association between event components { _X_ = _xj_ } and { _Y_ = _yk_ }. In reverse, negative values of the parameter indicate a “repulsion” situation, or negative association between events. 

226 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

Now assume that, on the basis of a sample of _n_ elements, a _frequency table_ has been constructed, of which entry _njk_ represents the observed frequency of events { _X_ = _xj_ ∩ _Y_ = _yk_ }. Denote the expected value of _njk_ by _μjk_ . From (6.3), it immediately follows that 

**==> picture [239 x 15] intentionally omitted <==**

which is a special case of the generalized linear models (2.42). In this particular case, the link function is the logarithm and (6.4) is an example of the _log-linear model_ . 

We can also use theoretical apparatus and the iterative weighted least squares algorithm for GLMs. Starting from observed values _njk_ , we can estimate the parameters of (6.4) and carry out other inferential operations. We can therefore verify that the available data allows the removal of component _βjk[XY]_ from (6.4), inasmuch as it is not significant, and we conclude that _X_ and _Y_ are independent variables. 

However, we often have to deal with more than two variables, sometimes many more. As in analysis of the correlation structure of a continuous multivariate variable, it is essential to use tools allowing for systematic examination of dependence structures that rapidly become complicated. The concept of conditional independence also plays an important role in the case of categorical variables. 

If we consider three categorical variables, ( _X, Y , Z_ ), and indicate by _μjkl_ the number of obtained observations for the general cell of the corresponding threeway table, representation as the corresponding log-linear model, as in (6.4), is 

**==> picture [168 x 37] intentionally omitted <==**

where the significance of the new symbols is similar to those already introduced. Note here that term _β[XYZ]_ is also introduced, whereas in the Gaussian case a term _jkl_ expressing an association between three components did not exist, because the particular nature of normal distribution allows us to express all associations among variables via correlations, and thus only involves pairs of variables. 

The specification of the foregoing model for the independence of _X_ and _Y_ conditional on _Z_ is given by 

**==> picture [201 x 16] intentionally omitted <==**

and figure 6.5 shows the relative graph (with different labeling of nodes). 

In the applicational context on which we focus, log-linear and graphical models are used in studying associations between variables (often categorical) that variously represent aspects of customers’ behavior. These associations, both positive and negative, give us useful suggestions for company commercial actions. 

Methods of Internal Analysis 

227 

**==> picture [313 x 227] intentionally omitted <==**

**----- Start of picture text -----**<br>
A<br>Marital status<br>Amount of credit Household tenure status<br>Income Bank<br>B<br>Age Insurance<br>C<br>Credit card insolvency Insolvency<br>**----- End of picture text -----**<br>


Figure 6.6 A graphical model for credit scoring. 

In terms of computational cost, a high value of _n_ has a small effect because determination of frequencies _njk_ is fast and computing time increases linearly with _n_ . Once the frequency table has been obtained, later processing has a computational cost that does not depend on _n_ . However, difficulties may arise if the number of variables involved is high, and even more so if the number of possible levels of these variables is large, because this can lead to a huge frequency table. We discuss this aspect in the following subsection from a different point of view. 

To illustrate the capacity of the representation of complex dependency structures, consider figure 6.6, taken from Hand et al. (1997). It shows a model to evaluate which variables influence the occurrence of insolvency in returning a bank loan. The study was based on a survey of about 23,000 holders of loans issued by a large U.K. bank. Financing not exceeding £10,000 was allowed, not covered by secure guarantees. 

The variables in the model described customers according to their demographic characteristics, which are Age (categories: 17–30, 31–40, or over 40) and Marital Status (Married, Other), and socioeconomic ones, which were Income (up to £ 700, £ 700–£ 1500, over £ 1500) and an indicator variable of housing tenure status. Information derived from the credit history of the customer, encoded by some indicator variables, was also available: Bank indicates a current account with the loan company, Credit card insolvency indicates past difficulties with credit card payments. Last, there is information about finances: the loan Amount (up to £ 3000, over £ 3000), Insolvency, measured with an indicator variable of a certain number of missed payments, and an indicator variable for taking out loan protection insurance, because all customers were given 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

228 

the opportunity, by means of a small increase in the monthly payment, to buy insurance to protect themselves from some types of insolvency. 

One node of the graph in figure 6.6 is associated with each variable. The edges denote associations among the variables; the absence of an edge means that the corresponding variables are conditionally independent, given the values of the other variables. The advantage of visualizing the model by means of the graph is the parallel between graphical separation and conditional independence, which means that if all paths from a node of set _A_ to a node of set _C_ pass through a node of set _B_ , then set _A_ is conditionally independent of set _C_ , given _B_ . This implies that, knowing the values of the variables in _B_ , knowledge of the variables in _C_ does not add any information about the nodes in _A_ , and vice versa. 

Interpreting that, if income, age, and the indicators of bank and insurance company are known, then the amount of credit, marital status, and housing tenure status do not provide extra information in predicting loan insolvency or financial insolvency. In other words, the set of nodes grouped in sets _A_ , _B_ , and _C_ in figure 6.6 behave the same way as _X_ , _Z_ , and _Y_ in figure 6.5. Therefore, for this type of financing, the variables for income, age, and the indicators of insurance, bank, and credit card insolvency contain all the information regarding insolvency. This causes a significant reduction in the size of the problem and enables us to identify customer profiles with an insolvency probability about three times the marginal probability. 

## 6.2.2 Association Rules 

Let us denote by _A_ 1 _, A_ 2 _, . . . , Ap_ a set of binary variables, whose possible values are labeled 0 and 1. Although in an abbreviated fashion, the previous section showed how the basis of _n_ observations of such variables can let us develop a model to represent the dependence structure of such variables compactly. 

To develop the connected log-linear model, we first have to construct the _p_ -ways frequency table. If all the variables are dichotomous, the number of cells in the table is 2 _[p]_ cells, a number that “explodes” rapidly as _p_ increases and is higher still if some of the variables have more than two levels. If _p_ = 20, for example, the number of cells is 2 _[p]_ = 1048576. The potential number of parameters to be estimated for the connected log-linear model is slightly lower, but is gigantic in any case. 

To explain the following, we refer to a background applied problem, where high values of _p_ are easy to observe. In _market basket analysis_ , variable _Aj_ is the indicator variable, often called an _item_ , that is, a customer has purchased the _j_ th product from the company catalog ( _j_ = 1 _, . . . , p_ ). According to data on the purchases made by _n_ customers, we identify the associations existing among variables _A_ 1 _, . . . , Ap_ , or at least pick up those that are considered interesting. 

If the company in question has a catalog containing a small number of items, for example, a service company, then the methods discussed in the previous section are perfectly adequate. Instead, if the company is a supermarket, then _p_ is easily of the order of thousands, a frequency table with 2[1000] cells cannot even be stored in a computer, and it cannot be processed to develop a log-linear model. Besides computing complications, there is also a serious inferential problem with this table, 

Methods of Internal Analysis 

229 

which will inevitably be extremely sparse, that is, with very many zeroes, hence violating the standard assumptions for inferences about log-linear models. 

In short, we must explore other routes. An alternative and currently very popular method comes from the field of machine learning and similar areas. It refers to the idea of _association rule_ , intended as a proposition of the type 

## condition ⇒ consequence 

as for example 

## it is raining ⇒ the ground is wet 

The concept of rule constitutes a classic paradigm in the field of artificial intelligence as a way of representing knowledge. The variant of this concept of more direct interest to us is the _probabilistic (association) rule_ , which assigns a probability to the previous “consequence,” once the condition has been fulfilled. For example, the rule 

the customer purchases bread and jam ⇒ the customer purchases butter 

does not intend to be deterministic, and therefore a probability is typically associated with it. 

On the basis of _n_ purchases carried out by as many customers, our aim is thus to choose rules that in probability theory correspond to conditional probabilities of the type: 

**==> picture [232 x 26] intentionally omitted <==**

where _E_ 1 is an event related to a group of variables and _E_ 2 an event determined by another set of variables; all the rules need not involve the same number of variables. Obviously, to evaluate these probabilities numerically, we make use of the relative frequencies of the same events, as observed in the data. For example, jam is the indicator variable of the purchase of jam, and so on for other variables. So a simple probabilistic rule is of the type 

**==> picture [263 x 11] intentionally omitted <==**

where _E_ 1 involves two indicator variables and _E_ 2 one. In this context, sets of events such as _E_ 1 or _E_ 2 are called _itemsets_ and are called _k_ -itemsets if the events specify the values of _k_ indicator variables. For example, _E_ 2 is a 1-itemset and _E_ 1 a 2-itemset. 

We can infer many rules from a data set, even for a limited number of variables, but to be useful, a rule must satisfy various conditions, as follows: 

- Obviously, a rule must have a high level of _confidence_ , that is, value _π_ 12 of (6.5) must be high, ideally, 1. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

230 

- The rule must also be capable of being applied to a suitable number of cases. For example, the rule of (6.6) has a good levelofconfidence,butifwe later discover that hardly anyone buys both bread and jam, it is practically useless. The rule must therefore have a high _support_ , given by P{ _E_ 1} in (6.5). The term _support_ is also sometimes used to refer to P{ _E_ 1 ∩ _E_ 2}. Itemsets with supports larger than a fixed threshold are called _frequent itemsets_ . 

- In a predictive approach, another characteristic for a good rule requires that knowledge that the “condition” is verified should produce a better prediction of the “consequence.” A measure of this is given by the ratio between confidence and the support of the consequent event, which is a measure of expected confidence when the condition is not known. An estimate of this association measure, _P_ ( _E_ 2| _E_ 1) _/P_ ( _E_ 2) = _P_ ( _E_ 2 ∩ _E_ 1) _/ P_ ( _E_ 1) _P_ ( _E_ 2), is called _lift_ . Although this term coincides with that of section 5.2.4, the two concepts are separate. Note that this lift is the exponential of term _β[XY]_ in (6.3). 

- Last, the rule must be “interesting.” The rule “if a person has a baby, then she is a woman” has a confidence level of 1, and support is not negligible, but the rule states nothing of interest. Identifying what is ‘interesting’ is not always easy, because it often involves specific aspects of the essential problem. However, there have been proposals to introduce quantitative criteria, such as the “ _J_ measure,” which tribution (isconditionalfundamentallyP{distribution _E_ 2} _,_ Pgiven� _E_ ¯ 2�(), weighting the divergence withbyP{ _E_ the2| _E_ 1Kullback-Leibler} _,_ P� _E_ ¯ 2| _E_ 1�) anddivergenceunconditional P{ _E_ 1}. betweendis- 

The problem of operatively identifying the rules remains. Conceptually, the type of operations required is elementary: we first calculate the empirical frequencies of various subsets and then select those that are the most useful with respect to the criteria. Although the required operations are very simple, the size of the possible events to consider is mind-boggling, even when the number _p_ of variables is not very high and the computational cost becomes unmanageable. 

However, the APriori algorithm comes to our rescue. Developed specifically for this problem, APriori is highly efficient and can select a set of associated rules that are interesting in some way, even though a limited number of data readings is available. The APriori algorithm, presented in algorithm 6.2, uses a hierarchical “level-wise”search,where _k_ -itemsets(i.e.,containing _k_ indicatorvariables)areused to explore ( _k_ + 1)-itemsets to find frequent itemsets. This is done by following the a priori property: any ( _k_ + 1)-itemset that is not frequent cannot be a subset of a frequent _k_ -itemset and hence should be removed. Initially, the set of frequent 1-itemsets is found. This is used to find the set of frequent 2-itemsets, which in turn is used to find the set of frequent 3-itemsets, and so on until no more frequent _k_ -itemsets can be found. 

The results and conclusions are rather different from those discussed in previous sections for other models. At least two considerations must be made. 

Methods of Internal Analysis 

231 

**Algorithm 6.2** APriori algorithm for association rules 

1. Assign a threshold _ts_ for support and one _tc_ for confidence. 

2. Let _k_ = 1; generate frequent 1-itemsets with support larger than the indicated threshold _ts_ . 

3. Cycle for _k_ = 2 _,_ 3 _, . . ._ until no new frequent itemsets are identified: 

   - a. generate candidate itemsets with length ( _k_ + 1) from frequent _k_ -itemsets; 

   - b. prune candidate _itemsets_ containing infrequent _k_ -itemsets (support lower than threshold _ts_ ); 

   - c. obtain the support of each candidate ( _k_ + 1)-itemset by scanning the entire data set; 

   - d. eliminateinfrequentcandidates,keepingonlythosewhosesupport is larger than threshold _ts_ . 

4. For every nonempty subset of each _frequent itemset_ , choose the rules that have confidence larger than threshold _tc_ . 

- The final result is not a global model illustrating the complex behavior of the phenomenon but a selection of particular aspects that are considered of interest. The aim of the study is therefore part of the identification of interesting data _patterns_ ; see section 1.1.2. 

- As the association rules selected in this way are not inserted in an inferential process, we have no information about their level of generalizability. It is not difficult to construct a statistical significance test for a fixed proposition, but the problem is that, in principle, we carry out a large number of such tests and select only those that are the most significant. We therefore process repeated hypothesis tests that completely change the real significance level, which in the end is very different from the nominal one. 

A final remarks deals with the field of application of the association rules. As already noted, the most classical application is market basket analysis, but the same concepts are relevant for other uses. An example is text analysis, in which indicator variable _Aj_ may indicate the presence or absence in a certain fragment of text of the _j_ th term of a vocabulary list with _p_ terms ( _j_ = 1 _, . . . , p_ ). 

## _Bibliographical notes_ 

The theory of graphical models is excellently explained by Whittaker (1990) and is still very pertinent today. Two other classic texts are those by Lauritzen (1996) and Cox & Wermuth (1998), the former more mathematical in nature, the latter combining theoretical and applicative aspects. Association rules are discussed, 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

232 

among others, by Hand et al. (2001, ch. 13). The APriori algorithm was developed by Agrawal et al. (1996), combining previous works by the same authors. 

## 6.3 CASE STUDY: WEB USAGE MINING 

We return to the real-life case analyzed in section 5.10.4. Here, we concentrate on the segmentation of visitors to the company website. 

In this section, we follow two lines of analysis that complement what was already shown in section 5.10.4. First, we look for behavioral segments of visitors in terms of visited pages, in particular by classifying visitors into homogeneous groups according to visits to pages belonging to the eight areas already used in the previous analysis. We then analyze sequences of visited pages by identifying the most likely navigation paths in the website. 

## 6.3.1 Profiling Website Visitors 

Website managers are interested in behavioral segmentation of visitors for future marketing decisions, and cluster analysis (see section 6.1) is typically used. 

Table 6.2showswhichvisitorsreachedwhichareasinsessionswithasinglepage. Clearly, as people visiting only one page are easily classified by the area including that page, we remove them from subsequent analysis. 

A more specific method of analysis is needed for the 4 _,_ 572 visitors going to two or more pages. Table 6.3 lists some descriptive indicators of the distributions of the number of hits for each area. All distributions are highly skewed to the right, and it seems reasonable to use some kind of data transformation to run a clustering procedure. Because the variables represent counts, all measured on the same scale as the number of hits, it also seems reasonable to consider the base 2 logarithm of each of them incremented by 1. This transformation, once rounded upwards, is the number of binary digits needed to write the counting number. 

The choice of a complete linkage is natural in implementing hierarchical cluster analysis in this case, where we are looking for very homogeneous groups. Figure 6.7 shows the dendrogram for identifying the optimal number of groups, in which the dashed line shows the level at which we decide to cut the tree, obtaining 

_Table 6.2._ WEB USAGE MINING: PERCENTAGE OF THE SINGLE-PAGE SESSIONS FOR EACH AREA 

|Area|% Visits|
|---|---|
|Business area|23_._21|
|Communications|1_._45|
|Company|1_._00|
|Consulting|8_._70|
|Contacts|0_._12|
|Events|1_._42|
|Home|1_._33|
|White papers|50_._78|



Methods of Internal Analysis 

233 

_Table 6.3._ WEB USAGE MINING: MEANS, MEDIANS, AND PERCENTILES FOR NUMBER OF HITS TO EACH AREA 

|Area|Mean|Median|3rd|90th|99th|
|---|---|---|---|---|---|
||||quartile|percentile|percentile|
|Business area|2.275|2|3|6|9|
|Communications|0.2937|0|0|0|2|
|Company|0.8871|0|0|3|6|
|Consulting|0.7220|0|0|2|4|
|Contacts|0.1562|0|0|1|1|
|Events|0.1223|0|0|0|1|
|Home|0.6177|0|0|2|3|
|White papers|0.5693|0|0|2|3|



**==> picture [7 x 156] intentionally omitted <==**

**----- Start of picture text -----**<br>
10<br>8<br>6<br>4<br>2<br>0<br>**----- End of picture text -----**<br>


**==> picture [203 x 38] intentionally omitted <==**

Figure 6.7 Web usage mining: Dendrogram for cluster procedure with complete linkage. 

four groups. Cuts allowing the choice of three or four groups are all of similar height, so we decide to use the larger number of clusters (i.e., four). 

Table 6.4 lists averages and standard deviations for each cluster of the eight variables used. These outcomes show the following. 

- Cluster A is characterized by a large number of visits to the business area, home, company, consulting, and contacts pages. These visitors are probably the most interested ones, who may become customers of the consultingbranch:theylookatallthecompanyinformation,theconsulting area, and the business areas in which the company works. 

- Cluster B is the smallest and has a very high number of visits to the white papers area. These customers are interested in the workings of the 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

234 

_Table 6.4._ WEB USAGE MINING: MEANS AND STANDARD DEVIATIONS (IN BRACKETS) FOR NUMBER OF VISITS TO EACH AREA 

|Area|Cluster A|Cluster B|Cluster C|Cluster D|Overall mean|
|---|---|---|---|---|---|
|Business area|9.43 (5.83)|0.58 (2.02)|1.76 (1.92)|0.30 (0.73)|2.27 (3.36)|
|Communications|0.67 (1.59)|0.02 (0.14)|0.27 (1.24)|0.16 (0.62)|0.29 (1.22)|
|Company|3.15 (6.40)|0.07 (0.43)|0.69 (2.03)|0.53 (1.90)|0.89 (2.79)|
|Consulting|2.23 (3.80)|0.41 (1.81)|0.13 (0.46)|3.73 (3.76)|0.72 (2.13)|
|Contacts|0.37 (0.78)|0.02 (0.14)|0.12 (0.39)|0.21 (0.59)|0.15 (0.47)|
|Events|0.43 (0.79)|0.11 (0.37)|0.09 (0.35)|0.13 (0.58)|0.12 (0.45)|
|Home|1.67 (2.14)|0.62 (1.35)|0.43 (0.88)|1.10 (2.41)|0.62 (1.36)|
|White papers|0.40 (1.83)|14.75 (14.18)|0.46 (0.94)|0.02 (0.14)|0.57 (2.38)|
|Number of visitors|409|53|3603|507|4572|



company, probably with the aim of learning more about what the company actually does and how, rather than doing business with it. 

- Cluster C is the largest group, and shows a low level of interest in consulting and events. None of the areas is visited more than another, and this group may be considered as one of general surfers. 

- Cluster D shows great interest in consulting, home page, and contacts. These visitors are less interested in white papers and business, so they are probably less interested in understanding in detail how the company works, but they still seem to be interested in the company’s products. They are probably a group of potential customers, although less determined and perhaps less knowledgeable than those of Cluster A. 

We also implement the nonhierarchical _k_ -means algorithm. As discussed in section 6.1, we need to select the number of expected clusters. In practice, we find solutions for a range of values for the numbers of clusters and examine the value of the within-group sum of squares associated with each solution. As the number of groupsincreases,thewithin-groupsumofsquaresdecreases.However,wemayfind some sudden change indicating the best solution. The top panel of figure 6.8 plots this quantity for a range of number of clusters. Here, the centers of each cluster are randomly selected. The plot suggests looking at the four-cluster solution, where the “elbow” is slightly sharper. The means of the clusters are plotted in the bottom panel of figure 6.8 and show the following: 

- Group 1, with 175 sessions, is characterized by a high number of visits to every area, and is the group with the most loyal visitors. 

- Group 2, with 2752 sessions, includes visitors with a high average number of hits on the white paper area, but few to all other areas. 

- Group 3, with 388 sessions, shows visitors’ great interest in the company, contacts, and events, but little in white papers. Visitors are potential customers for events organized by the company. 

Methods of Internal Analysis 

235 

**==> picture [237 x 463] intentionally omitted <==**

**----- Start of picture text -----**<br>
2 4 6 8 10 12 14<br>Number of groups<br>White papers Group 1<br>Group 2<br>Group 3<br>Home Group 4<br>Overall<br>Events<br>Contacts<br>Consulting<br>Company<br>Communications<br>Business area<br>0.01 0.05 0.10 0.50 1.00 5.00<br>Number of visits − log scale<br>20000<br>15000<br>10000<br>Within−group sum of squares<br>5000<br>0<br>**----- End of picture text -----**<br>


Figure 6.8 Web usage mining. Top: plot of within-group sum of squares against number of clusters. Bottom: means of the clusters for each area. 

- Group 4, with 1257 sessions, comprises visitors who are only interested in the business area; all other areas are seldom visited. 

These differences between the sets of clusters obtained by the two procedures are noticeable and represent a typical practical situation. Cross-tabulation of the two sets of groups is given in the table. 

236 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

|Hierarchical<br>clusters|_k_-means clusters|
|---|---|
||1<br>2<br>3<br>4|
|A<br>B<br>C<br>D|139<br>1<br>19<br>250<br>2<br>49<br>0<br>2<br>27<br>2228<br>351<br>997<br>7<br>474<br>18<br>8|



However, the aim of website managers, that is, to find homogeneous groups among visitors, did not require a single segmentation result. They may actually be interested in examining and using each of them for different marketing goals. 

For example, the segmentation yielded by the hierarchical procedure can be used to plan actions for customers interested in consulting products. Cluster A is sufficiently small and well characterized to be viewed as a target of marketing action by direct proposals for consulting services on the part of the company. Cluster B comprises people interested in the contents and methods adopted by the company; it may include researchers or other consultants who useful as contacts to improve methodology and share know-how. 

The set of groups obtained by _k_ -means may also be used to segment potential customers of other products offered by the company, such as organization of events: group 3 is a typical target interested in events. Group 1 is mainly a subset of hierarchical Cluster A, including the most loyal and interested visitors of that cluster. Group 4 isolates visitors interested in the business area, who were not 

Therefore, both segmentations may be used by website managers to decide on various marketing actions, directed to different targets and with different goals, and new visitors may be included in a specific cluster (one for each of the two segmentations proposed) depending on their surfing habits. 

## 6.3.2 Sequence Rules and Usage Behavior 

In section 5.10.4 we saw how visits to a single page can be predicted by analyzing data on the order in which web pages are visited. Here, a finer analysis is proposed to predict navigation paths and page sequences by considering every single page instead of areas and analyzing all observed paths, not only final hits on the contacts pages. 

Association rules (see section 6.2.2) can be used to see the most probable navigation paths in the website and predict the pages that will be viewed according to the path the visitor has taken so far. 

In consideration of the large number of pages visited, corresponding to the events we wish to associate, we use a simple modification of the APriori algorithm, called the s _equential_ pa _ttern_ d _iscovery using_ e _quivalence classes_ (spade) algorithm, proposed by Zaki (2001) which identifies the navigation paths visited most often. In this case, the order of visits to pages is crucial to understanding the sequential path of the session. To take into account the order of sequences, we only 

Methods of Internal Analysis 

237 

consider rules in which events are naturally ordered and, to simplify computation, associate each sequence to the ordered lists of sessions in which it occurs. Frequent sequences can thus be found efficiently by means of intersections on these lists. 

Figure 6.9 shows the frequency bar plot for inspecting the item distribution of pages visited. To reduce the number of items, we only plot item frequency for items with support greater than 2%. 

The algorithm found a total of 186 sequences with support of at least 0 _._ 5%. By selecting only rules with at least 60% of confidence, we obtain the 15 sequences shown in table 6.5. Here, the support indicates that the percentage of users who visited the two pages were in sequence, and the confidence represents the probability that the second page of the sequence was seen by visitors interested in the first (group of) page(s). 

http://www.company.it/white_papers/pdf/paper23.pdf http://www.company.it/map.html http://www.company.it/index.html http://www.company.it/index_en.html http://www.company.it/events/index.html http://www.company.it/contacts/index.html http://www.company.it/consulting/realize.html http://www.company.it/consulting/projects.html http://www.company.it/consulting/projects_en.html http://www.company.it/consulting/product.html http://www.company.it/consulting/education3.html http://www.company.it/consulting/education2.html http://www.company.it/consulting/education.html http://www.company.it/consulting/create.html http://www.company.it/company/technology.html http://www.company.it/company/staff.html http://www.company.it/company/partners.html http://www.company.it/company/methodology.html http://www.company.it/company/jobs.html http://www.company.it/company/index.html http://www.company.it/company/index_en.html http://www.company.it/communications/vote.html http://www.company.it/communications/newformat.html http://www.company.it/communications/index.html http://www.company.it/communications/birthday.html http://www.company.it/business_units/telecom2.html http://www.company.it/business_units/telecom2_en.html http://www.company.it/business_units/telecom.html http://www.company.it/business_units/telecom_en.html http://www.company.it/business_units/sales2.html http://www.company.it/business_units/sales.html http://www.company.it/business_units/publisher.html http://www.company.it/business_units/others.html http://www.company.it/business_units/internet.html http://www.company.it/business_units/insurance.html http://www.company.it/business_units/finance4.html http://www.company.it/business_units/finance4_es.html http://www.company.it/business_units/finance4_en.html http://www.company.it/business_units/finance3.html http://www.company.it/business_units/finance3_en.html http://www.company.it/business_units/finance2.html http://www.company.it/business_units/finance.html http://www.company.it/business_units/finance_en.html http://www.company.it/business_units/customers.html http://www.company.it/business_units/customers_en.html http://www.company.it/business_units/car.html http://www.company.it/ Item frequency (relative) 

Figure 6.9 Web usage mining: Item frequencies of page views with support greater than 2%. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

238 

_Table 6.5._ WEB USAGE MINING: THE MOST FREQUENT SEQUENCES OCCUPYING MORE THAN ONE PAGE 

||Rule|Support|Confdence|Lift|
|---|---|---|---|---|
|1|<http://www.company.it/business_units/finance4.html,|0.0056|0.7228|10.04|
||http://www.company.it/business_units/customers.html>||||
||=><http://www.company.it/business_units/finance4.html>||||
|2|<http://www.company.it/company/index.html,|0.0069|0.7054|35.35|
||http://www.company.it/company/staff.html,||||
||http://www.company.it/company/partners.html>||||
||=> <http://www.company.it/company/jobs.html>||||
|3|<http://www.company.it/company/staff.html,|0.0073|0.6931|34.73|
||http://www.company.it/company/partners.html>||||
||=> <http://www.company.it/company/jobs.html>||||
|4|<http://www.company.it/,|0.0065|0.6552|49.53|
||http://www.company.it/company/index.html,||||
||http://www.company.it/company/staff.html>||||
||=> <http://www.company.it/company/partners.html>||||
|5|<http://www.company.it/,|0.0100|0.6525|36.86|
||http://www.company.it/company/index.html>||||
||=> <http://www.company.it/company/staff.html>||||
|6|<http://www.company.it/,|0.0068|0.6520|49.29|
||http://www.company.it/company/staff.html>||||
||=> <http://www.company.it/company/partners.html>||||
|7|<http://www.company.it/company/index.html,|0.0054|0.6498|49.12|
||http://www.company.it/company/technology.html>||||
||=> <http://www.company.it/company/partners.html>||||
|8|<http://www.company.it/company/index.html,|0.0074|0.6467|32.40|
||http://www.company.it/company/partners.html>||||
||=> <http://www.company.it/company/jobs.html>||||
|9|<http://www.company.it/company/index.html,|0.0099|0.6434|48.64|
||http://www.company.it/company/staff.html>||||
||=> <http://www.company.it/company/partners.html>||||
|10|<http://www.company.it/consulting/create.html>|0.0052|0.6398|75.38|
||=> <http://www.company.it/consulting/realize.html>||||
|11|<http://www.company.it/company/index.html,|0.0053|0.6359|35.93|
||http://www.company.it/company/technology.html>||||
||=> <http://www.company.it/company/staff.html>||||
|12|<http://www.company.it/company/partners.html>|0.0082|0.6185|30.99|
||=> <http://www.company.it/company/jobs.html>||||
|13|<http://www.company.it/company/technology.html>|0.0055|0.6128|46.32|
||=> <http://www.company.it/company/partners.html>||||
|14|<http://www.company.it/company/index.html,|0.0093|0.6060|30.36|
||http://www.company.it/company/staff.html>||||
||=> <http://www.company.it/company/jobs.html>||||
|15|<http://www.company.it/company/technology.html>|0.0054|0.6000|33.90|
||=> <http://www.company.it/company/staff.html>||||



Among the page sequences visited by a moderately large number of people, the rule with the highest confidence describes a path from two pages presenting those business units including finance and customers, and then goes back to a finance page, with a conditional probability of 72%. With almost the same confidence, there are two sequences that, from the pages describing the company as a working environment (index, staff, partners, etc.), then go to the page listing job offers, including people looking for new jobs. 

Two paths moving from generic company pages to information about staff and partners still have high confidence (65%). This is a typical sequence followed by people potentially interested in doing business with the company: first they look for generic information about it; when they see it appears to be interesting, they look for the personal characteristics of the people working there (this is mainly a consulting company, so the standards of its personnel are crucial for 

Methods of Internal Analysis 

239 

the services offered). A further passage may be direct contact with the aim of collaborating with the company. 

Note that only a few of the identified rules involve pages from different areas of the website. The pages do not seem to be very well connected, or else people visiting the site are only interested in specific goals and go directly to the pages of interest. 

## Appendix A 

Complements of Mathematics and Statistics 

## A.1 CONCEPTS ON LINEAR ALGEBRA 

We recall some standard facts in linear algebra and establish notation. A matrix is an array of elements, or _entries_ , all taken from the same set, organized into rows and columns. These entries commonly belong to the set of real numbers, and this is the case we deal with here. Matrix _A_ has dimension _m_ × _n_ if it has _m_ rows and _n_ columns; we can also say that _A_ is an _m_ × _n_ matrix and write _A_ = ( _aij_ ), where the parentheses contain the generic element of _A_ . 

The transposed matrix of _A_ , obtained by switching rows and columns, is denoted _A_[⊤] . A matrix _v_ of dimension _n_ × 1 is called the (column) vector of dimension _n_ or, equivalently, the _n_ × 1 vector, and we write _v_ ∈ R _[n]_ ; analogously, a matrix of dimension 1 × _n_ is called a row vector. 

The identity matrix of order _n_ is indicated by _In_ , 1 _n_ is the _n_ × 1 vector having all elements equal to 1 and 0 is the zero-matrix whose dimension will be clear from the context. 

If _A_ = ( _aij_ ) is a square matrix of order _n_ , that is, an _n_ × _n_ matrix, we use the following notation and terminology: 

- i. _A_ is symmetric if _A_[⊤] = _A_ ; 

- ii. det( _A_ ) is the determinant of A; the property det( _A B_ ) = det( _A_ ) det( _B_ ) holds; 

Complements of Mathematics and Statistics 

241 

- iii. If det( _A_ ) ̸= 0, we say that _A_ is nonsingular and there is an inverse matrix, _A_[−][1] , so that _A A_[−][1] = _A_[−][1] _A_ = _In_ ; we can also write ( _A_[⊤] )[−][1] = ( _A_[−][1] )[⊤] and ( _A B_ )[−][1] = _B_[−][1] _A_[−][1] , if both the inverses exist; 

- iv. A symmetric matrix _A_ is positive semi-definite if _u_[⊤] _Au_ ≥ 0 for every nonzero vector _u_ ∈ R _[n]_ ; in this case, we can write _A_ ≥ 0; we can also write _A_ ≥ _B_ to indicate that _A_ − _B_ ≥ 0; 

- v. A symmetric matrix _A_ is positive definite if it is symmetric and _u_[⊤] _Au >_ 0 for every nonzero vector _u_ ∈ R _[n]_ ; in this case, we write _A >_ 0; we also write _A > B_ to indicate that _A_ − _B >_ 0; 

- vi. _A_ is orthogonal if its transpose and inverse are equal, that is, _A_[⊤] = _A_[−][1] ; in this case, det( _A_ ) = ±1; 

- vii. tr( _A_ ) is the trace of _A_ , that is, the sum of the elements on its main diagonal; tr( _AB_ ) = tr( _BA_ ) holds for two matrices _A_ and _B_ , which need not to square, presuming both products _AB_ and _BA_ are possible; 

- viii. _A_ is idempotent if _A_ = _A_[2] ; for an idempotent matrix, the rank is equal to the trace, that is, rk( _A_ ) = tr( _A_ ); 

- ix. _A_ is a diagonal matrix if all the elements outside the main diagonal ( _a_ 11 _, a_ 22 _, . . . , ann_ ) are 0; we can also write _A_ = diag( _a_ 11 _, . . . , ann_ ); 

- x. The so-called _matrix inversion lemma_ 

**==> picture [275 x 13] intentionally omitted <==**

holds when the matrices are of conformable dimensions and the required inverse matrices exist; in particular, if _b_ and _d_ are column vectors and _c_ = 1 is a scalar, then (A.1) becomes 

**==> picture [264 x 25] intentionally omitted <==**

which is called the _Sherman–Morrison formula_ . 

## A.2 CONCEPTS OF PROBABILITY THEORY 

## A.2.1 Multivariate Random Variables 

If _X_ 1 _, . . . , Xp_ are random variables defined on the same probability space, then the vector 

**==> picture [50 x 58] intentionally omitted <==**

is a _multivariate random variable_ . The expectation or mean value E{ _X_ } of _X_ is defined as the vector of the expectations of the components, if they all exist. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

242 

That is, we define 

**==> picture [84 x 67] intentionally omitted <==**

and the _variance matrix_ (or dispersion matrix) is defined as 

**==> picture [258 x 73] intentionally omitted <==**

presuming the existence of every element of the matrix. However, the existence of the elements on the main diagonal is sufficient to guarantee the existence of all the others, keeping in mind the Cauchy-Schwartz inequality. Note also that var{ _X_ } is a symmetric matrix and that var{ _Xi_ } is a notation equivalent to cov{ _Xi, Xi_ }. 

The matrix obtained by dividing the generic term cov� _Xi, Xj_ � by the product of the respective standard deviations, ~~[√]~~ var{ _Xi_ } × �var ~~�~~ _Xj_ ~~�~~ , is called the _correlation matrix_ . 

If var{ _X_ } is a diagonal matrix, we say that _X_ has uncorrelated components. 

## A.2.2 Some General Properties 

We state some simple properties of the expectation and variance matrix of multivariate random variables; for proofs, see, for example, Azzalini (1996, Appendix A.4). For this section, we assume that _X_ = ( _X_ 1 _, . . . , Xp_ )[⊤] , with E{ _X_ } = _μ,_ var{ _X_ } = _V_ . 

Lemma A.2.1 

If _A_ is a _q_ × _p_ matrix, _b_ a _q_ × 1 vector, and 

**==> picture [58 x 10] intentionally omitted <==**

then 

i. E{ _Y_ } = _Aμ_ + _b_ , ii. var{ _Y_ } = _A VA_[⊤] . 

## Lemma A.2.2 

Variance matrix _V_ = var{ _X_ } is positive semi-definite and is also positive definite if there are no zero vectors _b_ for which _b_[⊤] _X_ has degenerate distribution. 

Complements of Mathematics and Statistics 

243 

Lemma A.2.3 

If var{ _X_ } = _V >_ 0, there is a square matrix _C_ of order _p_ , so that _Y_ = _CX_ has uncorrelated components with unit variance, that is, var{ _Y_ } = _Ip_ . 

Lemma A.2.4 

Let _A_ = ( _aij_ ) be a square matrix of order _p_ . Then 

**==> picture [136 x 20] intentionally omitted <==**

## A.2.3 Multivariate Normal Distribution 

We want to extend the concept of normal distribution from the scalar to the _p_ -dimensional case. In the multidimensional case, the normal (or Gaussian) distribution plays a key role to an even greater extent than in the scalar case. 

The following is a constructive definition equipped with certain properties. More details are given, for example, by Azzalini (1996, Appendix A.5); for a more detailed presentation, see Mardia et al. (1979, ch. 2 and 3). 

Let _Z_ 1 _, . . . , Zp_ be independent random variables _N_ (0 _,_ 1), so vector _Z_ = ( _Z_ 1 _, . . . , Zp_ )[⊤] is a multivariate random variable that we can reasonably consider the first case of a multivariate normal variable. However, the distribution of _Z_ is very specific, and we want to introduce a much wider class, keeping the properties of the simple distribution. 

In the univariate case, the normal distribution class can be generated by transformations of the type _X_ 0 = _μ_ + _σ Z_ 0, if _Z_ 0 ∼ _N_ (0 _,_ 1) and _σ_ ̸= 0 (note that _σ <_ 0 is not excluded). A similar operation in the _p_ -dimensional case is of the type 

**==> picture [73 x 13] intentionally omitted <==**

where _μ_ ∈ R _[p]_ and _�_[1] _[/]_[2] is a _p_ × _p_ matrix of full rank. 

The probability density function of _Z_ is given by the product of _p_ copies of density _N_ (0 _,_ 1). From this, applying known rules to calculate the distributions of transformed random variables, the density function of _X_ is 

**==> picture [305 x 26] intentionally omitted <==**

for _x_ ∈ R _[p]_ . 

Therefore, let us decide _by definition_ that a random variable _X_ with a distribution of type (A.3) is said to have normal (or Gaussian) multivariate _p_ -dimensional 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

244 

distribution with parameters _μ_ and _�_ = _�_[1] _[/]_[2] ( _�_[1] _[/]_[2] )[⊤] . We thus adopt the notation 

**==> picture [68 x 14] intentionally omitted <==**

The case in which _�_ does not have full rank is admissible, even though our construction and (A.3) are assumed in the case with full rank. 

The family of multivariate normal distributions has many formal properties that make its use as a probabilistic model particularly advantageous. Some of the simplest, already implicit in what has been stated so far, are listed here. 

- a. The contour lines of _p_ ( _x_ ) are _ellipses_ of equation 

**==> picture [147 x 13] intentionally omitted <==**

- b. If _�_ is a diagonal matrix, the components of _X_ are not only uncorrelated but also independent, as we can immediately see from the expression of _p_ ( _x_ ). 

c. Because E{ _Z_ } = 0 and var{ _Z_ } = _Ip_ , lemma A.2.1 immediately gives 

**==> picture [127 x 10] intentionally omitted <==**

To better perceive the nature of normal distribution, it is useful to examine figure A.1, which shows the case when _p_ = 2. The left panel shows some contour lines of the probability density of _Z_ , which are circumferences, since its variance matrix is the identity. The same panel also shows the 100 points randomly sampled from _Z_ . The right panel refers to the transformed variable 

**==> picture [315 x 27] intentionally omitted <==**

and shows the density contour lines corresponding to those in the left panel. This signifies that the ellipses on the right represent the deformation of the 

**==> picture [323 x 152] intentionally omitted <==**

**----- Start of picture text -----**<br>
−3 −2 −1 0 1 2 3 −3 −2 −1 0 1 2 3<br>z1 x1<br>3 3<br>2 2<br>1 1<br>z2 0 x2 0<br>−1 −1<br>−2 −2<br>−3 −3<br>**----- End of picture text -----**<br>


Figure A.1 Contour lines of density function and sample points from bivariate normal distributions. Left: variable _Z_ with independent components _N_ (0 _,_ 1); right: those of its transformation (A.4). 

Complements of Mathematics and Statistics 

245 

circumferences on the left, according to transformation (A.4); the value of the density associated with these curves is modified according to factor det( _�_ )[1] _[/]_[2] in (A.3). The right panel also shows the previous sample points as modified by the adopted transformation. Some of the points are marked by symbols different from the majority of the sample, to facilitate matching of the corresponding points in the two panels. The inclination of the main axis of the ellipses denotes a correlation between the two components, which in this case is 0 _._ 694 = 0 _._ 80 _/_[√] 0 _._ 97 × 1 _._ 37. 

One of the most important properties of the family of multivariate normal distributions is that they are closed to affine transformations, including those that reduce the dimension. More precisely, if _a_ ∈ R _[q]_ and _B_ is a _q_ × _p_ matrix, then 

**==> picture [243 x 15] intentionally omitted <==**

This includes the special case in which the scalar linear combination of components having multivariate normal distribution has normal distribution. 

As a particular case of the previous property, the class is closed with respect to the marginalization operation, in the following sense. We subdivide the components of _X_ into two sets, the first of _q_ and the second of _p_ − _q_ components. For notational simplicity, we assume the first set corresponds to the first _q_ components of _X_ , although this is not essential. In other words, we introduce the partitions 

**==> picture [212 x 27] intentionally omitted <==**

where _μ_ and _�_ are partitioned in the same way as _X_ . And so, as a particular case of the general property (A.5), we obtain 

**==> picture [83 x 14] intentionally omitted <==**

The property of closure of the normal distribution class with respect to the conditioning operation also holds. Specifically, the distribution of _X_ 1 conditional on _X_ 2 = _x_ 2 is 

**==> picture [277 x 15] intentionally omitted <==**

where 

**==> picture [123 x 14] intentionally omitted <==**

As _x_ 2 varies, the conditional mean value _μ_ 1 + _�_ 12 _�_ 22[−][1][(] _[x]_[2][ −] _[μ]_[2][) corresponds to] the equation of a plane, called the _regression hyperplane_ . Conditional variance _�_ 11·2 is “smaller” than marginal variance _�_ 11, where “smaller” means inequality between matrices, with equality only when _�_ 12 is the zero matrix. Note that the conditional variance does not depend on _x_ 2. 

246 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

There are various connections between multivariate normal distribution and _χ_[2] distribution, of which the simplest is given by 

**==> picture [164 x 15] intentionally omitted <==**

In addition, if _X_ ∼ _Np_ ( _μ, Ip_ ) and _A_ is a symmetric positive semi-definite _p_ × _p_ matrix of rank _q_ , then 

**==> picture [252 x 15] intentionally omitted <==**

with noncentrality parameters _δ_ 1 = _μ_[⊤] _Aμ_ , _δ_ 2 = _μ_[⊤] ( _Ip_ − _A_ ) _μ_ , respectively, and the two quadratic forms _Q_ 1 and _Q_ 2 are stochastically independent. 

## A.3 CONCEPTS OF LINEAR MODELS 

## A.3.1 Linear Models and the Least Squares Criterion 

We assume that the relation between response variable _y_ and explanatory variables _x_ 1 _, . . . , xp_ is of the type 

**==> picture [225 x 13] intentionally omitted <==**

where _ε_ is a component, called _error_ , that expresses the deviationbetweenempirical observations and systematic component _β_ 1 _x_ 1 + · · · + _βp xp_ , also called _linear predictor_ . Regression parameters _β_ 1 _, . . . , βp_ are real numbers; therefore, in the absence of constraints on the model, _β_ = ( _β_ 1 _, . . . , βp_ )[⊤] is any point in R _[p]_ . 

We make use of a set of _n_ observations ( _n_ ≥ _p_ ) of variables _x_ 1 _, x_ 2 _, . . . , xp, y_ , which therefore satisfy the relations 

**==> picture [273 x 13] intentionally omitted <==**

On the basis of these _n_ replicas, we estimate parameters _β_ and carry out other inferential operations. 

Assume that error component _ε_ is a random variable that in successive observations from model (A.7), is such that 

**==> picture [308 x 15] intentionally omitted <==**

where _σ_[2] is a positive constant value for all replications. Consequently, 

**==> picture [230 x 14] intentionally omitted <==**

when _Yi_ represents the random variable that generated observation _yi_ . 

Formulation (A.7) is said to be a linear model, and assumptions (A.9) are called second-order hypotheses, because they involve moments up to the second order. 

To estimate parameters _β_ on the basis of _n_ sample observations, according to model (A.8), it is common to adopt the least squares criterion, which selects 

Complements of Mathematics and Statistics 

247 

_β_ values that minimize the sum of square deviations between observed and interpolated values, which in turn minimizes _Q_ ( _β_ ), given by 

**==> picture [185 x 31] intentionally omitted <==**

where the unknown _β_ is now treated as a free variation quantity in R _[p]_ . 

The whole formulation lends itself to more compact notation by means of matrices. We therefore create vector _y_ , of _n_ observations of the response variable, and do the same for _ε_ . Analogously, we form a matrix _X_ with dimension _n_ × _p_ , whose _j_ th column is formed from _n_ observations on variable _xj_ ; we assume that matrix _X_ has full rank _p_ . Therefore, we can rewrite (A.8) in a compact matrix form as 

**==> picture [52 x 11] intentionally omitted <==**

with the second-order hypothesis given by 

**==> picture [156 x 13] intentionally omitted <==**

The least squares criterion lies in the solution of the optimization problem 

**==> picture [200 x 20] intentionally omitted <==**

The following presentation is taken from Azzalini (1996, ch. 5), to which we refer for missing details. 

## A.3.2 The Geometry of Least Squares 

We now analyze the various components in the game from the purely geometric point of view, leaving aside statistical and probabilistic aspects for the moment. We consider vectors _y, x_ 1 _, . . . , xp_ containing, respectively, the values of the response variable and _p_ explanatory variables as elements of vector space R _[n]_ . 

As _β_ varies in R _[p]_ , expression _Xβ_ = _β_ 1 _x_ 1 + · · · + _βpxp_ can be seen as a linear combination of columns _x_ 1 _, . . . , xp_ of _X_ with coefficients _β_ — that is, the parametric equation of a subspace of R _[n]_ spanned _by the columns_ of _X_ . This subspace, which we call _C_ ( _X_ ), is a vector space on R with dimension _p_ . The property that, if _Xβ_ ∈ _C_ ( _X_ ) and _a_ ∈ R then also _a_ ( _Xβ_ ) = _X_ ( _aβ_ ) ∈ _C_ ( _X_ ) holds; moreover, if _Xβ_ and _Xb_ are two elements of _C_ ( _X_ ), then also _Xβ_ + _Xb_ = _X_ ( _β_ + _b_ ) ∈ _C_ ( _X_ ); clearly, the other properties of vector spaces also hold. 

Model (A.7–A.9) then states that _μ_ = E{ _Y_ } lies in _C_ ( _X_ ), and the least squares criterion chooses which vector of _C_ ( _X_ ) minimizes the Euclidean distance between ˆ vector _y_ and space _C_ ( _X_ ). We indicate by _μ_ = _Xβ_[ˆ] this element of _C_ ( _X_ ), identified by coefficients _β_[ˆ] ∈ R _[p]_ . The situation is illustrated is figure A.2. 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

248 

**==> picture [318 x 95] intentionally omitted <==**

**----- Start of picture text -----**<br>
y<br>y  –  m [∧]<br>∧<br>m<br>C  ( X )<br>Origin<br>**----- End of picture text -----**<br>


Figure A.2 Projection of _y_ on _C_ ( _X_ ). 

On the basis of known results of vector space geometry, we know that vector _μ_ ˆ ∈ _C_ ( _X_ ), which minimizes the distance from _y_ , is such that 

**==> picture [78 x 14] intentionally omitted <==**

and this requires ( _y_ −ˆ _μ_ ) to be orthogonal to the vectors that constitute the basis of _C_ ( _X_ ). Therefore, it is necessary that 

**==> picture [78 x 14] intentionally omitted <==**

that is, 

**==> picture [199 x 14] intentionally omitted <==**

which are called _normal equations_ . 

The inversion of matrix _X_[⊤] _X_ is legitimate because the condition that _X_ has rank _p_ implies that _X_[⊤] _X_ is still of rank _p_ . Therefore, the minimum of _D_ ( _β_ ) is obtained for _β_ and is 

**==> picture [207 x 14] intentionally omitted <==**

The same result can be obtained by minimizing _D_ ( _β_ ) in an analytical instead of a geometrical way. The _projection_ vector of _y_ on _C_ ( _X_ ) is 

**==> picture [210 x 53] intentionally omitted <==**

where _P_ = _X_ ( _X_[⊤] _X_ )[−][1] _X_[⊤] is called the _projection matrix_ on _C_ ( _X_ ). This identifies an operator, associated with matrix _X_ , whose role is precisely that of projecting a vector _y_ ∈ R _[n]_ by transforming it into _Py_ ∈ _C_ ( _X_ ) with a minimum distance from _y_ . We can immediately verify that _P_ is symmetric and idempotent because _P_[2] = _P_ ; 

Complements of Mathematics and Statistics 

249 

this signifies that _Py_ = _P_ ( _Py_ ), so projecting a projection has no effect. We note that these observations imply that 

**==> picture [174 x 14] intentionally omitted <==**

We can therefore split _y_ into two components: its projection _μ_ ˆ on _C_ ( _X_ ), and the component of the _residuals_ given by the difference vector 

**==> picture [256 x 14] intentionally omitted <==**

These two components are orthogonal to each other; in fact, _y_ −ˆ _μ_ is orthogonal to every element of _C_ ( _X_ ) and not only _μ_ ˆ . For any vector _Xa_ ∈ _C_ ( _X_ ), we have 

**==> picture [194 x 50] intentionally omitted <==**

Matrix _In_ − _P_ is also a projection matrix: it projects the elements of R _[n]_ in the space orthogonal to _C_ ( _X_ ). As calculated for the rank of _P_ , we have rk( _In_ − _P_ ) = _n_ − _p_ . The orthogonality between the projection vector and one of the residuals has an immediate corollary: expanding the norm of _μ_ ˆ + ( _y_ −ˆ _μ_ ), we obtain 

**==> picture [220 x 13] intentionally omitted <==**

which is an instance of the Pythagorean theorem, in which _y_ plays the role of the hypotenuse and _μ_ ˆ and _y_ −ˆ _μ_ that of the sides. 

## A.3.3 The Statistics of Least Squares 

We now examine, from a statistical point of view, the quantities introduced in the previous section. This naturally brings us to consider _y_ observations and error components as determinations of random variables _Y_ and _ε_ , respectively. We have 

**==> picture [227 x 76] intentionally omitted <==**

and therefore _β_[ˆ] is an unbiased estimate of _β_ ; in addition, 

**==> picture [51 x 13] intentionally omitted <==**

D A T A A N A L Y S I S A N D D A T A M I N I N G 

250 

For the variance matrix of the estimates, we have 

**==> picture [267 x 62] intentionally omitted <==**

and 

**==> picture [119 x 58] intentionally omitted <==**

Up to now, we have only looked at the estimation of _β_ . Although to a lesser extent than _β_ , we are also interested in estimating _σ_[2] . The least squares criterion does not tell us how to proceed. Because we have E� _εi_[2] � = _σ_[2] for generic term _εi_ , it is reasonable to estimate _σ_[2] with the arithmetic mean of the _ε_ ˆ _i_[2][, where] _[ε]_[ˆ] _[i]_[is the] general component of the residual vector 

**==> picture [46 x 12] intentionally omitted <==**

and therefore we consider 

**==> picture [211 x 26] intentionally omitted <==**

as an estimate of _σ_[2] . Note that this expression can be rewritten in various other forms, bearing in mind the relations 

**==> picture [154 x 96] intentionally omitted <==**

To calculate expectation of (A.17), we have 

**==> picture [260 x 61] intentionally omitted <==**

Complements of Mathematics and Statistics 

251 

using lemma A.2.4. The term _μ_[⊤] ( _In_ − _P_ ) _μ_ is 0, because _In_ − _P_ projects onto the space orthogonal to _C_ ( _X_ ) where _μ_ lies, and therefore 

**==> picture [186 x 13] intentionally omitted <==**

Thus, _σ_ ˆ[2] is subject to bias, which tends to 0 as _n_ →∞. If we need an unbiased estimate for _σ_[2] , this is given by 

**==> picture [225 x 28] intentionally omitted <==**

## A.3.4 Constrained Estimation 

We now consider the problem of estimating _β_ when linear constraints are present in the _β_ coefficients, that is, _β_ is such that 

**==> picture [183 x 11] intentionally omitted <==**

where _H_ is a _q_ × _p_ matrix (with _q_ ≤ _p_ ) with rank _q_ formed of specified constants. The solution to this problem is particularly useful in the framework of hypothesis testing on the components of _β_ , but it is also of independent interest. 

First consider the geometric meaning of condition _Hβ_ = 0. It requires _μ_ to lie in the subset of _C_ ( _X_ ), which satisfies _q_ conditions specified by _Hβ_ = 0. This subset represents a _vector subspace_ , here called _C_ 0( _X_ ), of dimension _p_ − _q_ of space _C_ ( _X_ ), as shown in figure A.3. 

**==> picture [313 x 178] intentionally omitted <==**

**----- Start of picture text -----**<br>
y<br>y  –  m [∧]<br>∧<br>m<br>C  ( X ) m ∧ – m ∧0<br>∧<br>m 0<br>C 0 ( X )<br>**----- End of picture text -----**<br>


Figure A.3 Projection of _y_ on _C_ ( _X_ ) and subspace _C_ 0( _X_ ). 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

252 

To obtain the constrained minimum of _D_ ( _β_ ), we must minimize 

**==> picture [200 x 13] intentionally omitted <==**

where _α_ is a vector of Lagrange multipliers, with constraint (A.20). After some algebraic manipulation, we reach the solution 

**==> picture [228 x 13] intentionally omitted <==**

where 

**==> picture [220 x 14] intentionally omitted <==**

The corresponding projection of _y_ on _C_ 0( _X_ ) is given by 

**==> picture [135 x 54] intentionally omitted <==**

having set 

**==> picture [249 x 32] intentionally omitted <==**

Consider the conclusions we have reached so far. We have a new projection matrix, _P_ 0, which projects any vector of R _[n]_ on space _C_ 0( _X_ ). If we apply this matrix to _y_ , we obtain _μ_ ˆ 0, which, by its very nature, is the element of _C_ 0( _X_ ) with the minimum distance from _y_ . It is also easy to verify the following further properties: 

- Vector _y_ −ˆ _μ_ 0 is orthogonal to every element of _C_ 0( _X_ ). If _Xc_ is an element of _C_ ( _X_ ) so that _Hc_ = 0, we have ( _y_ −ˆ _μ_ 0)[⊤] _Xc_ = 0. In particular, 

**==> picture [68 x 12] intentionally omitted <==**

- The projection of _y_ −ˆ _μ_ 0 on _C_ ( _X_ ) is _P_ ( _y_ −ˆ _μ_ 0) = _μ_ ˆ −ˆ _μ_ 0, which is such that 

**==> picture [63 x 10] intentionally omitted <==**

Last, we obtain the following decomposition: 

**==> picture [132 x 12] intentionally omitted <==**

where the three summands on the right-hand side are orthogonal to each other, and therefore allow us to write 

**==> picture [252 x 13] intentionally omitted <==**

which is an extension of (A.14). 

Complements of Mathematics and Statistics 

253 

## A.3.5 Normality Assumptions 

If we add to the second-order hypothesis (formulated in section A.3.1 around the distribution of the random variable of the error component) that of normality, for which 

**==> picture [74 x 12] intentionally omitted <==**

we can obtain more stringent results for the distributive properties of the inferential quantities already seen. First, it immediately follows that 

**==> picture [81 x 12] intentionally omitted <==**

leading to 

**==> picture [76 x 15] intentionally omitted <==**

The interpretation of _β_[ˆ] changes, in the sense that it can be seen as a maximum likelihood estimate, besides being descended from the least squares criterion. In fact, maximization of the likelihood function corresponds to maximization with respect to _β_ of the term within exp(·) of (A.3), if we assume that _μ_ = _Xβ_ , and this coincides with the minimization of _D_ ( _β_ ). 

The components of projection and error of _Y_ also have normal distribution, as 

**==> picture [218 x 32] intentionally omitted <==**

for which we can apply the results for quadratic forms of random normal variables noted in section A.2.3. It therefore follows that 

**==> picture [170 x 15] intentionally omitted <==**

where the noncentrality parameter is _δ_ = _β_[⊤] _X_[⊤] _Xβ_ and the two quadratic forms are independent. 

These facts thus establish the distribution of the decomposition of total variability _Y_[⊤] _Y_ intotwocomponents,thatis,errorcomponent ∥ˆ _ε_ ∥[2] andregression component _Y_[ˆ][⊤] _Y_[ˆ] . These properties yield the distribution of the _F_ test connected with the analysis of variance table. 

The sum of the squares of regression component _Y_[ˆ][⊤] _Y_[ˆ] is then further decomposed into individual components, one for each explanatory variable with corresponding decomposition of the degrees of freedom. 

## Appendix B 

## Data Sets 

Appendix B describes the data used in this volume. They are also available at the website: http://azzalini.stat.unipd.it/Book-DM/. 

## B.1 SIMULATED DATA 

Some of the data used were obtained by means of simulation of pseudo-random numbers, as follows: 

- a. Yesterday’s data and tomorrow’s data. A table with 30 rows (other than those with variable names) and 3 columns, contains variables x, y.yesterday, y.tomorrow, with self-explanatory names. These data are used in chapter 3 and section 4.8. 

- b. Data for three classes, of sizes 120, 80, and 100, are used in chapter 5. The data table contains 300 rows (other than those with variable names) and 3 columns, for two explanatory variables, _z_ 1 and _z_ 2, and one class indicator. Some of the numerical examples in chapter 5 refer to data in the 

- c. Two data collections, C1 and C2, are used in section 6.1, each with two variables, with 250 and 100 points. 

## B.2 CAR DATA 

The car data, first used in section 2.1.1 and then in section 2.1 and chapter 4, were obtained by simple manipulation of original data that referred to the characteristics 

Data Sets 

255 

of 203 automobile models imported into the United States in 1985. The original dataareavailableat: ftp://ftp.ics.uci.edu/pub/machine-learningdatabases/autos. Their manipulation on our part simply consisted of converting one unit of measurement to another and eliminating some variables. The new variables are as follows: 

|Variable|Description|
|---|---|
|make|manufacturer (factor, 22 levels)|
|fuel type|type of engine fuel (factor, 2 levels: diesel, gasoline)|
|aspiration|type of engine aspiration (factor, 2 levels: standard, turbo)|
|body style|type of body style|
||(factor, 5 levels: hardtop, wagon, sedan, hatchback, convertible)|
|drive wheels|type of drive wheels (factor, 3 levels: 4wd, fwd, rwd)|
|engine location|location of engine (factor, 2 levels: front, rear)|
|wheel base|distance between axes (cm)|
|length|length (cm)|
|width|width (cm)|
|height|height (cm)|
|curb weight|weight (kg)|
|engine size|engine size (L)|
|compression rate|compression rate|
|hp|horsepower|
|peak-rpm|number of peak revolutions per minute|
|city distance|city distance covered (km/L)|
|highway distance|highway distance (km/L)|
|n.cylinders|number of cylinders|



## B.3 BRAZILIAN BANK DATA 

The data used in sections 2.3.3 and 2.4 were obtained by simple manipulation of original data referring to a customer satisfaction survey by a Brazilian bank. For 500 subjects, randomly selected from the bank’s customers, some information from marketing research was obtained. Some characteristic variables of customers and their satisfaction are: 

|Variable|Description|
|---|---|
|id|customer identifcation|
|satisfaction|(factor: 4 levels)|
|education|(factor: 5 levels)|
|age|(years)|
|gender|gender|
|car|indicator of car ownership|
|phone|indicator of phone use|
|fax|indicator of fax use|
|pc|indicator of PC ownership|
|pincome|annual income (in Brazilian reais)|
|ok|satisfaction index (factor: 2 levels)|



256 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

Customers were also asked which products of the bank they used and if they also used similar products supplied by other banks. The names of the variables regarding the products of the bank that commissioned the survey end with the number _n_ = 1; the number of similar variables that refer to other banks end with the number _n_ = 2. The following is the list of surveyed products, with self-explanatory names: 

|savings_n_|installment.loan_n_|
|---|---|
|creditcard_n_|investment.fund_n_|
|bankcard_n_|commodities.fund_n_|
|cd_n_|annuities.fund_n_|
|specialchecking_n_|car.insurance_n_|
|auto.bill.payment_n_|home.insurance_n_|
|personal.loans_n_|life.insurance_n_|
|mortgage_n_||



## B.4 DATA FOR TELEPHONE COMPANY CUSTOMERS 

The data for telephone customers, used in section 4.10.1 and later in chapter 5 in the two case studies in section 5.10, was obtained by simple manipulation of original data referring to the characteristics of 30 _,_ 619 customers of a European telephone company with postpay contracts. To be part of the set, the customers had to be active in the 10 consecutive months to which the data refer, which are conventionally indicated by numbers from 1 to 10 ( _nn_ = 01 _, . . . ,_ 10). 

The original data were processed simply by eliminating some of the original variables. For the customers, the variables are: 

- characteristic variables of customer and of company contract 

|Variable|Description|
|---|---|
|id|customer identifcation|
|tariff.plan|customer tariff plan (factor, 5 levels)|
|payment.method|(factor, 3 levels:|
||PO: postal order, CC: credit card, DD: direct debit)|
|gender|(factor, 3 levels:|
||M: male, F: female, B: company)|
|age|(years)|
|activ.zone|geographical activation zone (factor, 4 levels)|
|activ.chan|channel of activation (factor, 8 levels)|
|vas1|presence of a frst value-added service|
|vas2|presence of a second value-added service|



- variables for traffic in the 10 available months. For each month, indicated by the first part of the name (q01, q02, _. . ._ , q10), the following variables are available: 

Data Sets 

257 

|Variable|Description|
|---|---|
|q_nn_.out.ch.peak|total monthly number of outgoing calls|
||at peak tariff times|
|q_nn_.out.dur.peak|duration of total monthly outgoing calls|
||at peak tariff times|
|q_nn_.out.val.peak|total monthly outgoing call value|
||at peak tariff times|
|q_nn_.out.ch.offpeak|total monthly number of outgoing calls|
||at off-peak tariff times|
|q_nn_.out.dur.offpeak|duration of total monthly outgoing calls|
||at off-peak tariff times|
|q_nn_.out.val.offpeak|total monthly outgoing call value|
||at off-peak tariff times|
|q_nn_.in.ch.tot|total monthly number of incoming calls|
|q_nn_.in.dur.tot|duration of total monthly incoming calls|
|q_nn_.ch.sms|total monthly number of SMS sent|
|q_nn_.ch.cc|number of monthly calls to|
||customer services|



- the variable status, that is which is the indicator variable of possible deactivation in the thirteenth month, that is, two months after the final month for which traffic is available (factor, 2 levels: 0—active, 1—deactivated). 

## B.5 INSURANCE DATA 

The data on insurance customers, used in section 4.10.2, was obtained by simple manipulation of original data on the characteristics of a sample of 5,000 customers of a European insurance company. To be part of the set, the customers had to take out one policy in at least one of the company’s lines of business. 

Processing the original data consisted simply of eliminating some of the original variables. For these customers, the available variables are as follows. 

- Customers’ characteristic variables 

|Variable|Description|
|---|---|
|id|customer identifcation|
|gender|(factor, 3 levels: M: male, F: female, — missing)|
|age|(years)|
|occupation.1|occupational categories of employment 1 (factor, 11 levels)|
|occupation.2|occupational categories of employment 2 (factor, 17 levels)|
|zip|postcode (numeric)|
|area|geographical area of residence (factor, 33 levels)|
|region|geographical region of residence (factor, 10 levels)|
|city|indicator variable of residence in urban areas|



D A T A A N A L Y S I S A N D D A T A M I N I N G 

258 

- Variables regarding to canceled claims and policies: 

|Variable|Description|
|---|---|
|number.claims.last|number of claims in last year|
|number.claims.3|number of claims in last 3 years|
|amount.claims.last|amount of claims in last year|
|amount.claims.3|amount of claims in 3 years|
|number.cancel.last|number of policies canceled in last year|
|number.cancel.3|number of policies canceled in 3 years|



- Variables relating to products. For each product, indicated by number _n_ at the end of the name of the variable (for nonlife products _n_ = 1 _, . . ._ 9 and life products _n_ = 1 _a,_ 1 _b,_ 2 _a,_ 2 _b,_ 3 _a,_ 3 _b_ ), the following variables are available: 

|Variable|Description|
|---|---|
|n.nonlife.0|number of private car third-party liability policies|
|prem.nonlife.0|total amount of premiums for private car third-party|
||liability policies|
|number.bank.1|number of bank products of type 1|
|number.bank.2|number of bank products of type 2|
|net.bank.2|net asset value funds|
|tot.bank.2|total amount of funds|
|ac.bank.2|total amount of funds acquired|
|number.non-life._n_|number of nonlife policies of type_n_|
|prem.non-life._n_|total amount of premiums for nonlife policies of type_n_|
|number.life._n_|number of life policies of type_n_|
|prem.life._n_|total amount of premiums for life policies of type_n_in last year|
|pre.payed.life._n_|total amount of paid premiums for life policies of type_n_|
|i.cancel.last|policies canceled in last year|
|i.cancel.3|policies canceled in 3 years|
|i.bank.1|at least one bank product of type 1|
|i.bank.2|at least one bank product of type 2|
|i.non-life._n_|at least one nonlife policy of type_n_|
|i.life._n_|at least one life policy of type_n_|



## B.6 CHOICE OF FRUIT JUICE DATA 

The data on fruit juice purchases were presented by Foster et al. (1998, ch. 11) and are available through the distribution system for statistical information StatLib at the website http://lib.stat.cmu.edu/. 

The data refer to 1,070 fruit juice purchases of two different brands (MM and CH) in certain U.S. supermarkets, supplied with some contributory variables. The data used in chapter 5 were slightly processed in the sense that some 

Data Sets 

259 

characteristics of little importance were excluded. The variables used are as follows: 

|Variable|Description|
|---|---|
|choice|prechosen brand (factor, with 2 levels)|
|id.cust|customer identifcation|
|week|identifer of week of purchase|
|priceCH|reference price for brand CH (USD)|
|priceMM|reference price for brand MM (USD)|
|discountCH|discount applied to product CH (USD)|
|discountMM|discount applied to product MM (USD)|
|loyaltyCH|loyalty indicator for product CH|
|loyaltyMM|loyalty indicator for product MM|
|store|store identifer (factor, with 5 levels)|



Variable loyaltyMM is constructed starting from the value 0.5 and updating with every purchase by the same customer, with a value that increases by 20% of the current difference between the current value and 1, if the customer chose MM, and falls by 20% of the difference between the current value and 0 if the customer chose CH. The corresponding variable loyaltyCH is given by 1 − loyaltyMM. There are five stores in question, numbered from 0 to 4. 

## B.7 CUSTOMER SATISFACTION 

The data on customer satisfaction, used in section 5.10.3, were obtained by simple manipulation of original data on responses to a questionnaire from a survey of 4 _,_ 000 customers of a European IT company producing and selling software and offering consulting services. The survey was carried out by an independent marketing research company specializing in such surveys. Processing of original data consisted simply of eliminating some of the original variables. These were: 

- products/services used 

Question: _Which products/services of the company do you use?_ 

|Variable|Product/service|
|---|---|
|V2|1|
|V3|2|
|V4|3|
|V5|4|
|V6|5|
|V7|6|
|V8|7|
|V9|others|



260 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

- satisfaction with staff and products (except V11, all variables are factors with 10 levels: 1: totally disagree,…, 10: totally agree) 

|Variable|Question|Answer|
|---|---|---|
|V11|In the last year, did you have contacts with|1: no|
||company personnel for consultancy,|2: yes, once|
||information, or solutions to problems?|3: yes, sometimes|
|||4: yes, often|
|V24|The products are easy to use||
|V25|The products can easily be adapted to customers’|needs|
|V26|The products are exactly what I need||
|V27|Product results are reliable||
|V28|Differing products are easily integrated||



- Question: _Please rate the importance of the following aspects in evaluating an IT company_ (each variable is a factor with 10 levels: 1: not at all important,…, 10: very important): 

|Variable|Item|
|---|---|
|V29|expertise of personnel|
|V30|capacity to offer an effcient consulting service|
|V31|problem solving|
|V32|reliability of products/services|
|V33|fexibility of products/services|
|V34|effciency of products/services|
|V35|working speed of products|
|V36|helpfulness of personnel|
|V37|effciency in serving customers|
|V38|predisposition towards customers’ needs|
|V39|capacity to respond to customer’s needs|
|V40|fexibility in making changes|
|V41|capacity for technological innovation|



Data Sets 

261 

- Question: _Please rate your satisfaction with the following aspects_ (each variable is a factor with 10 levels: 1: not at all important,…, 10: very important): 

|Variable|Item|
|---|---|
|V42|expertise of personnel|
|V43|capacity to offer an effcient consulting service|
|V44|problem solving|
|V45|reliability of products/services|
|V46|fexibility of products/services|
|V47|effciency of products/services|
|V48|working speed of products|
|V49|helpfulness of personnel|
|V50|effciency in serving customers|
|V51|predisposition towards customers’ needs|
|V52|capacity to respond to customer’s needs|
|V53|fexibility in making changes|
|V54|capacity for technological innovation|



- customers’ overall satisfaction and characteristics: 

|Variable|Question|Answer|
|---|---|---|
|V56|Recalling all aspects analyzed in this|1: extremely satisfed|
||questionnaire, how satisfed are you|2: very satisfed|
||with the company, overall?|3: quite satisfed|
|||4: quite dissatisfed|
|||5: very dissatisfed|
|||6: extremely dissatisfed|
|V58|occupational category of employment|12 categories|
|V59|employment status|1: employer|
|||2: manager|
|V60|age||
|V61|length of service in company||
|V62|education|1: university degree|
|||2: high school diploma|
|||3: middle school diploma|
|||oth: other|
|V63|gender||



## B.8 WEB USAGE DATA 

The data on web usage, used in sections 5.10.4 and 6.3, refer to hits made by 26,157 anonymous visitors to the website of a consulting company. Data were collected from web log files, collecting all relevant information about hits on every page of the website. 

262 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

A _user session_ describes the sequence of web pages viewed consecutively by a visitor, without leaving the website or the connection. We call these sequences of pages “visits.” The website to which the data refer does not have a cookie system or other way of identifying the same visitor in different sessions, so we consider each session in the analysis as a new visitor, and we call the same event “session” or “visit” indifferently. 

All pages visited in a year are included in the data set. Sessions are labeled with a identification number, and no personal information is available. The website has 215 pages and the total number of page views (hits) on the entire site was 47,387. Some of the pages have similar contents and were aggregated in eight categories (home, contacts, communications, events, company, white papers, business units, consulting). The day and time of all visits to every single page are also recorded. For each single event (visit to a page) the available variables are: 

|ID|identifcation number of single event (page visited)|
|---|---|
|sessionID|identifcation number of session|
|screen|screen resolution used by customer (if available)|
|url|address of visited page|
|dt|day and month of event|
|yr|indicator of year of event: data refer to|
||two consecutive years, called 1 and 2.|
|hr|time of event|



## Appendix C 

Symbols and Acronyms 

|AIC|Akaike information criterion|
|---|---|
|CART|classifcation and regression trees|
|CRM|customer relationship management|
|d.f.|degree or degrees of freedom|
|DWH|data warehouse|
|GAM|generalized additive model|
|GCV|generalized cross validation|
|GLM|generalized linear model|
|KDD|knowledge discovery in databases|
|LDA|linear discriminant analysis|
|MARS|multivariate adaptive regression splines|
|OLAP|online analytical processing|
|OLTP|online Transaction Processing|
|PCA|principal component analysis|
|QDA|quadratic discriminant analysis|
|ROC|receiver operating characteristic|
|SQL|structured query language|
|SVM|support vector machine|
|det(·)|determinant of a matrix|
|tr(·)|trace of a matrix|



264 

D A T A A N A L Y S I S A N D D A T A M I N I N G 

|rk(·)|rank of a matrix|
|---|---|
|_D_|deviance|
|_L_|likelihood function|
|_ℓ_(_x_)|logistic function e_x/_(1+e_x_)|
|E{·}|expectation of a random variable|
|var{·}|variance (or matrix of variance) of a random variable|
|∥· ∥|Euclidean norm|
|R_,_R_p_|set of real numbers,_p_-dimensional Euclidean space|
|_I_(_x_)|indicator function 0–1 of logical predicate_x_|
|_IA_|set of indicator variables of factor_A_|
|_In_|identity matrix of order_n_|
|1_n_|_n_×1 vector of elements, all 1|



## REFERENCES 

- Afifi, A. A. & Clark, V. (1990). _Computer-Aided Multivariate Analysis_ , 2nd ed. New York: Van Nostrand Reinhold. 

- Agrawal, R., Mannila, H., Srikant, R., Toivonen, H., & Verkamo, A. I. (1996). Fast discovery of association rules. In U. M. Fayyad, G. Piatetsky-Shapiro, P. Smyth, & R. Uthurusamy (eds.), _Advances in Knowledge Discovery and Data Mining_ (pp. 307–328). Cambridge, Mass.: AAAI/MIT Press. 

- Agresti, A. (2002). _Categorical Data Analysis_ , 2nd ed. Hoboken, N.J.: Wiley. 

- Agresti, A. (2010). _Analysis of Ordinal Categorical Data_ , 2nd ed. Hoboken, N.J.: Wiley. 

- Akaike, H. (1973). Information theory as an extension of the maximum likelihood principle. In B. N. Petrov & F. Csaki (eds.), _Second International Symposium on Information Theory_ (pp. 267–281). Budapest: Akademiai Kiado. 

- Atkinson, K. E. (1989). _An Introduction to Numerical Analysis_ , 2nd ed. New York: Wiley. 

- Azzalini, A. (1996). _Statistical Inference Based on the Likelihood_ . London: Chapman & Hall. 

- Azzalini, A. & Scarpa, B. (2004). _Analisi dei dati e data mining_ . Milan: Springer-Verlag Italia. 

- Bellman, R. E. (1961). _Adaptive Control Processes_ . Princeton, N.J.: Princeton University Press. 

- Berry, M. J. A. & Linoff, G. (1997). _Data Mining Techniques: For Marketing, Sales, and Customer Support_ . New York: Wiley. 

- Bishop, Y. M. M., Fienberg, S. E., & Holland, P. W. (1975). _Discrete Multivariate Analysis: Theory and Practice_ . Cambridge: Cambridge University Press. 

- Bowman, A. W. & Azzalini, A. (1997). _Applied Smoothing Techniques for Data Analysis: The Kernel Approach with S-Plus Illustrations_ . Oxford: Oxford University Press. 

- Breiman, L. (1996). Bagging predictors. _Machine Learning_ , 24, 123–140. 

- Breiman, L. (2001a). Random forests. _Machine Learning_ , 45, 5–32. 

- Breiman, L. (2001b). Statistical modeling: The two cultures. _Statistical Science_ , 16(3), 199–215. 

- Breiman, L., Friedman, J. H., Olshen, R. A., & Stone, C. J. (1984). _Classification and Regression Trees_ . Monterey: Wadsworth. 

- Burnham, K. P. & Anderson, D. R. (2002). _Model Selection and Multimodel Inference: A Practical Information-Theoretic Approach_ , 2nd ed. New York: Springer Verlag. 

- Casella, G. & Berger, R. L. (2002). _Statistical Inference_ , 2nd ed. Pacific Grove: Duxbury Press. 

- Claeskens, G. & Hjort, N. L. (2008). _Model Selection and Model Averaging_ . Cambridge: Cambridge University Press. 

R e f e r e n c e s 

266 

- Cleveland, W. (1979). Robust locally weighted regression and smoothing scatterplots. _Journal of the American Statistical Association_ , 74, 829–836. 

Cleveland, W. & Devlin, S. (1988). Locally-weighted regression: An approach to regression analysis by local fitting. _Journal of the American Statistical Association_ , 83, 596–610. 

- Cleveland, W. S., Grosse, E., & Shyu, M.-J. (1992). Local regression models. In J. M. Chambers & T. Hastie (eds.), _Statistical Models in S_ (pp. 309–376). Pacific Grove: Duxbury Press. 

- Cook, R. D. & Weisberg, S. (1999). _Applied Regression Including Computing and Graphics_ . New York: Wiley. 

- Cox, D. R. (1997). The current position of statistics: A personal view. _International Statistical Review_ , 65, 261–276. 

- Cox, D. R. & Hinkley, D. V. (1979). _Theoretical Statistics_ , 2nd ed. London: Chapman and Hall. 

- Cox, D. R. & Wermuth, N. (1998). _Multivariate Dependencies: Models, Analysis, and Interpretation_ . London: Chapman and Hall. 

- Craven, P. & Wahba, G. (1978). Smoothing noisy data with spline functions: Estimating the correct degree of smoothing by the method of generalized cross-validation. _Numerische Mathematik_ , 31, 377–403. 

- Cristianini, N. & Shawe-Taylor, J. (2000). _An Introduction to Support Vector Machines and other Kernel-Based Learning Method_ . Cambridge: Cambridge University Press. 

- Davison, A. C. & Hinkley, D. V. (1997). _Bootstrap Methods and Their Application_ . Cambridge: Cambridge University Press. 

- Dawid, A. P. (2006). Probability forecasting. In S. Kotz, C. B. Read, N. Balakrishnan, & B. Vidakovic (eds.), _Encyclopedia of Statistical Sciences_ , 2nd ed., vol. 10 (pp. 6445–6452). New York: Wiley. 

- de Boor, C. (1978). _A Practical Guide to Splines_ . New York: Springer Verlag. 

- Efron, B., Hastie, T., Johnstone, I., & Tibshirani, R. (2004). Least angle regression (with discussion). _Annals of Statistics_ , 32, 407–499. 

- Efron, B. & Tibshirani, R. (1993). _An Introduction to the Bootstrap_ . New York: Chapman and Hall. 

- Fahrmeir, L. & Tutz, G. (2001). _Multivariate Statistical Modelling Based on Generalized Linear Models_ , 2nd ed. New York: Springer Verlag. 

- Fan, J. & Gijbels, I. (1996). _Local Polynomial Modelling and its Applications_ . London: Chapman and Hall. 

- Fine, T. L. (1999). _Feedforward Neural Network Methodology_ . New York: Springer Verlag. 

- Fisher, R. A. (1936). The use of multiple measurements in taxonomic problems. _Annals of Eugenics_ , 7, 179–188. 

- Foster, D. P., Stine, R. A., & Waterman, R. P. (1998). _Business Analysis Using Regression: A Casebook_ . New York: Springer Verlag. 

- Freund, Y. & Schapire, R. (1996). Experiments with a new boosting algorithm. In L. Saitta (ed.), _Machine Learning: Proceedings of the Thirteenth International Conference_ , vol. 35 (pp. 148–156). San Francisco: Morgan Kaufmann. 

- Friedman, J. (1991). Multivariate adaptive regression splines (with discussion). _Annals of Statistics_ , 19(1), 1–141. 

- Friedman, J., Hastie, T., & Tibshirani, R. (2000). Additive logistic regression: A statistical view of boosting (with discussion). _Annals of Statistics_ , 28(2), 337–407. 

R e f e r e n c e s 

267 

- Friedman, J. & Tukey, J. (1974). A projection pursuit algorithm for exploratory data analysis. _IEEE Transactions on Computers, Series C_ , 23, 881–889. 

- Golub, G. H. & Van Loan, C. F. (1983). _Matrix Computations_ . Baltimore, Md.: Johns Hopkins University Press. 

- Gower, J. C. (1971). A general coefficient of similarity and some of its properties. _Biometrics_ , 27, 857–871. 

- Green, P. J. & Silverman, B. W. (1994). _Nonparametric Regression and Generalized Linear Models: A Roughness Penalty Approach_ . London: Chapman and Hall. 

- Hand, D. J. (1981). _Discrimination and Classification_ . Chichester: Wiley. 

- Hand, D. J. (1982). _Kernel Discriminant Analysis_ . Chichester: Wiley. 

- Hand, D. J., Mannila, H., & Smyth, P. (2001). _Principles of Data Mining_ . Cambridge, Mass.: MIT Press. 

- Hand, D. J., McConway, K. J., & Stanghellini, E. (1997). Graphical models of applicants for credit. _IMA Journal of Mathematics Applied in Business and Industry_ , 8, 143–155. 

- Hartigan, J. A. (1975). _Clustering Algorithms_ . New York: Wiley. 

- Hastie, T., Tibshirani, R., & Friedman, J. (2009). _The Elements of Statistical Learning: Data Mining, Inference, and Prediction_ , 2nd ed. New York: Springer Verlag. 

- Hastie, T. J. & Tibshirani, R. J. (1990). _Generalized Additive Models_ . London: Chapman and Hall. Reprint 1999. 

- Hoerl, A. & Kennard, R. (1970). Ridge regression: Biased estimation for non-orthogonal problems. _Technometrics_ , 12, 55–67. 

- Hosmer, D. W. & Lemeshow, S. (1989). _Applied Logistic Regression_ . New York: Wiley. 

- Hotelling, H. (1933). Analysis of a complex of statistical variables into principal components. _Journal of Educational Psychology_ , 24, 417–441, 498–520. 

- Huber, P. (1985). Projection pursuit. _Annals of Statistics_ , 13, 435–475. 

- Hurvich, C. M., Simonoff, J. S., & Tsai, C.-L. (1998). Smoothing parameter selection in nonparametric regression using an improved Akaike information criterion. _Journal of the Royal Statistical Society, Series B_ , 60, 271–293. 

- Izenman, A. J. (2008). _Modern Multivariate Statistical Techniques_ . New York: Springer Verlag. 

- Johnson, R. & Wichern, D. (1998). _Applied Multivariate Statistical Analysis_ , 4th ed. Upper Saddle River, N.J.: Prentice Hall. 

- Jolliffe, I. (2002). _Principal Component Analysis_ . New York: Springer Verlag. 

- Jones, L. (1992). A simple lemma on greedy approximation in Hilbert space and convergence rates for projection pursuit regression and neural networks. _Annals of Statistics_ , 20, 608–613. 

- Kaufman, L. & Rousseeuw, P. J. (2009). _Finding Groups in Data: An Introduction to Cluster Analysis_ . Hoboken, N.J.: Wiley. 

- Kendall, M. G. & Stuart, A. (1969). _The Advanced Theory of Statistics, 3rd ed., vol. 1: Distribution Theory_ . London: Charles Griffin. 

- Kolmogorov, A. (1957). On the representation of continuous functions by superposition of continuous functions of one variable and addition. _Doklady Akademiia Nauk SSSR_ , 114, 953–956. 

- Lauritzen, S. L. (1996). _Graphical Models_ . Oxford: Oxford University Press. 

- Loader, C. (1999). _Local Regression and Likelihood_ . New York: Springer Verlag. 

- Mardia, K. V., Kent, J. T., & Bibby, J. M. (1979). _Multivariate Analysis_ . London: Academic Press. 

- McCullagh, P. & Nelder, J. A. (1989). _Generalized Linear Models_ . London: Chapman and Hall. 

R e f e r e n c e s 

268 

- McLachlan, G. J. (1992). _Discriminant Analysis and Statistical Pattern Recognition_ . New York: Wiley. 

- Miller, A. J. (2002). _Subset Selection in Regression_ . Boca Raton, Fla.: Chapman and Hall/CRC. 

- Ohlsson, E. & Johansson, B. (2010). _Non-Life Insurance Pricing with Generalized Linear Models_ . Heidelberg: Springer Verlag. 

- Pearson, K. (1901). On lines and planes of closest fit to systems of points in space. _Philosophical Magazine_ , 2(6), 559–572. 

- Plackett, R. L. (1950). Some theorems in least squares. _Biometrika_ , 37(1–2), 149–157. 

- Quinlan, J. R. (1993). _C4.5: Programs for Machine Learning_ . San Mateo, Calif.: Morgan Kaufmann. 

- Rao, C. R. (1973). _Linear Statistical Inference and its Applications_ , 2nd ed. New York: Wiley. 

- Ripley, B. D. (1996). _Pattern Recognition and Neural Networks_ . Cambridge: Cambridge University Press. 

- Stone, C. J., Hansen, M. H., Kooperberg, C., & Truong, Y. K. (1997). Polynomial splines and their tensor products in extended linear modeling (with discussion). _Annals of Statistics_ , 25, 1371–1470. 

- Stone, M. (1974). Cross-validatory choice and assessment of statistical predictions (with discussion). _Journal of the Royal Statistical Society, Series B_ , 36, 111–147. (Corr: 1976, vol. 38, p. 102). 

- Tibshirani, R. (1996). Regression shrinkage and selection via the lasso. _Journal of the Royal Statistical Society, Series B_ , 58, 267–288. 

- Trefethen, L. N. & Bau, D. (1997). _Numerical Linear Algebra_ . Philadelphia: Society for Industrial and Applied Mathematics. 

- Tse, Y.-K. (2009). _Nonlife Actuarial Models. Theory, Methods and Evaluation_ . Cambridge: Cambridge University Press. 

- Vapnik, V. (1998). _Statistical Learning Theory_ . New York: Wiley. 

- Venables, W. N. & Ripley, B. D. (2002). _Modern Applied Statistics with S_ , 4th ed. New York: Springer Verlag. 

- Wand, M. P. & Jones, M. C. (1995). _Kernel Smoothing_ . London: Chapman and Hall. 

- Wasserman, L. (2004). _All of Statistics: A Concise Course in Statistical Inference_ . New York: Springer Verlag. 

- Weisberg, S. (2005). _Applied Linear Regression_ , 3rd ed. New York: Wiley. 

- Whittaker, J. (1990). _Graphical Models in Applied Multivariate Statistics_ . Chichester: Wiley. 

- Wolpert, D. H. & MacReady, W. G. (1999). An efficient method to estimate bagging’s generalization error. _Machine Learning_ , 35(1), 41–55. 

- Zaki, M. J. (2001). Spade: An efficient algorithm for mining frequent sequences. _Machine Learning_ , 42, 31–60. 

## AUTHOR INDEX 

Afifi, A.A., 60 Agrawal, R., 232 Agresti, A., 9, 148 Akaike, H., 56, 58 Anderson, D.R., 58 Atkinson, K.E., 89 Azzalini, A., 40, 44, 78, 97, 242, 243, 247 

Bau, D. III, 30 Bellman, R.E., 79 Berger, R.L., 40 Berry, M.J.A., 9 Bibby, J.M., 30, 63, 159, 222, 223, 243 Bishop, Y.M.M., 9 Bowman, A.W., 78, 97 Box, G.E.P., 9 Breiman, L., 12, 103, 106, 183 Burnham, K.P., 58 

Casella, G., 40 Claeskens, G., 58 Clark, V., 60 Cleveland, W., 78 Cook, R.D., 29 Cox, D.R., 12, 40, 231 Craven, P., 89 Cristianini, N., 175 

Davison, A.C., 183 Dawid, A.P., 204 de Boor, C., 89 Devlin, S., 78 

Efron, B., 66, 183 Einstein, A., 15 

Fahrmeir, L., 148 Fan, J., 78 Fienberg, S.E., 9 Fine, T.L., 111 Fisher, R.A., 155, 156, 159, 210 Foster, D.P., 258 Freund, Y., 183 Friedman, J., 63, 64, 66, 79, 89, 93, 94, 103, 106, 111, 153, 175, 179, 183 

Gijbels, I., 78 Golub, G.H., 33 Gower, J.C., 222 Green, P.J., 82, 89, 97 Grosse, E., 78 

Hand, D.J., 5, 9, 159, 227, 232 Hansen, M.H., 164 Hartigan, J.A., 222 Hastie, T., 63, 64, 66, 79, 89, 93, 94, 97, 111, 153, 164, 175, 179, 183 Hinkley, D.V., 40, 183 Hjort, N.L., 58 Hoerl, A., 66 Holland, P.W., 9 Hosmer, D.W., 44 Hotelling, H., 62 Huber, P., 94 Hurvich, C.M., 73 

Izenman, A.J., 60, 63, 66 

Johansson, B., 124 Johnson, R., 63 

A U T H O R I N D E X 

270 

Johnstone, I., 66 Jolliffe, I., 63 Jones, L., 94 Jones, M.C., 78 

Kaufman, L., 222 Kendall, M.G., 9 Kennard, R., 66 Kent, J.T., 30, 63, 159, 222, 223, 243 Kolmogorov, A., 94 Kooperberg, C., 164 

Lauritzen, S.L., 231 Lemeshow, S., 44 Leonardo da Vinci, 1 Linoff, G., 9 Loader, C., 78 

MacReady, W.G., 183 Mannila, H., 5, 9, 232 Mardia, K.V., 30, 63, 159, 222, 223, 243 McConway, K.J., 227 McCullagh, P., 44, 148 McLachlan, G.J., 159 Miller, A.J., 60, 66 

Nelder, J.A., 44, 148 

Ohlsson, E., 124 Olshen, R.A., 103, 106 

Pearson, K., 62 Plackett, R.L., 33 

Quinlan, J.R., 168 

Rao, R.C., 29 Ripley, B.D., 29, 106, 108, 109, 111, 159, 168, 170, 204 Rousseeuw, P.J., 222 

Scarpa, B., ix Shapire, R., 183 Shawe-Taylor, J., 175 Shyu, M.-J., 78 Silverman, B.W., 82, 89, 97 Simonoff, J.S., 73 Smyth, P., 5, 9, 232 Srikant, R., 232 Stanghellini, E., 227 Stine, R.A., 258 Stone, C.J., 103, 106, 164 Stone, M., 58 Stuart, A., 9 

Tibshirani, R., 63, 64, 66, 79, 89, 93, 94, 97, 111, 153, 164, 175, 179, 183 Toivonen, H., 232 Trefethen, L.N., 30 Truong, Y.K., 164 Tsai, C.-L., 73 Tse, Y.K., 124 Tukey, J., 94 Tutz, G., 148 

Van Loan, C.F., 33 Vapnik, V., 175 Venables, W.N., 29, 106, 109, 204 Verkamo, A.I., 232 

Wahba, G., 89 Wand, M.P., 78 Wasserman, L., 40 Waterman, R.P., 258 Weisberg, S., 29, 60 Wermuth, N., 231 Whittaker, J., 231 Wichern, D., 63 William of Ockham, 45 Wolpert, D.H., 183 

Zaki, M.J., 237 

## SUBJECT INDEX 

actuarial models, 124 AIC, 55–59, 73, 74, 104, 193 algorithm, 12, 13 AdaBoost, 179, 180 APriori, 230–232, 236 back-propagation, 109 backfitting, 91, 161 Gram-Schmidt, 31 iteratively weighted least squares, 42, 226 _k_ -means, 216 least-angle regression, 66 local scoring, 161, 196 recursive least squares, 33, 34 analysis of variance, 94, 96–97, 117, 253 two way, 225 applications in churn prediction, 2, 187–192 credit scoring, 134, 227–228 customer satisfaction, 39–40, 42–44, 144, 148, 192–205 customer segmentation, 212 environmental analysis, 3 fraud detection, 2 insurance, 123–131, 134 market basket analysis, 2, 228 marketing, 2, 111–123, 135–148, 183–205 

pricing, 134 scientific areas, 3 text analysis, 231 web site analysis, 3, 205–209, 232–239 artificial intelligence, 5 _see also_ machine learning association among variables, 222–231 categorical, 225 

dichotomous, 228 graphical representation of, 224, 228 positive and negative, 225 with three components, 226 association rule, 228–231 average _see_ mean, arithmetic 

back-propagation _see_ algorithm, back-propagation backfitting _see_ algorithm, backfitting backward selection _see_ variable selection, stepwise bagging, 176–180, 182, 183, 209 bandwith _see_ parameter, smoothing basis functions, 81, 82, 84, 85, 87 tensor product, 85 Bayesian approach, 158 bias, 53, 72–75, 251 trade-off between and variance _see_ trade-off, bias–variance BIC, 57 boosting, 179–180, 183, 209 bootstrap, 176–179, 182, 183 bumping, 179 

C4.5 – C5.0, 168 

calculus, parallel, 105, 182 calibration plot _see_ plot, calibration CART, 106 _see also_ tree centroid, 215–218 churn analysis _see_ applications in churn prediction classification examples, 42–44, 134–136, 144, 148, 183–209 methods, 40–42, 136–183 

SUBJECT INDEX 

272 

cluster analysis, 212–222 cluster methods, 212–214, 222 agglomerative, 218–222 divisive, 222 hierarchical, 218–222 non-hierarchical, 215–218 coefficient correlation _see_ correlation of a linear combination, 247 of determination, 20, 23, 26, 47 complexity computational _see_ computational complexity of a model, 4, 47–49, 160 computational burden, 5–6, 30, 33, 54, 59, 79, 101, 105, 230 in log-linear models, 226–227 complexity, 84, 87, 102, 154, 158, 160, 182 computing, statistical, 13 confidence (of a rule), 229 confidence interval, 36, 75, 106 

_see_ trade-off, bias-variance constraint, 36, 38, 39, 81, 87 

linear, 36, 37, 251–252 contingency table, 9, 138, 225–229 convex hull, 77 correlation, 29, 222–223, 245 geometric interpretation, 222 marginal, 224 matrix _see_ matrix, correlation partial, 223–224 sample, 223 cost-complexity, 103 covariate _see_ variable, explanatory credit scoring _see_ applications in credit scoring CRM, 3–4, 6, 8, 187, 263 cross table multiple, 7, 228 cross-sell, 135 cross-validation, 54–55, 58, 73, 87, 104, 109, 168, 175, 179, 206 algorithm, 55 generalized, 87, 263 leave-one-out, 54 with small sizes, 55 

curse of dimensionality, 78–79, 90, 155 curve 

lift, 140–142, 151, 163, 167, 178, 180, 185, 189 ROC, 140, 151, 163, 167, 178, 180, 185, 263 customer base, 123, 187, 212 care, 112 profiling, 135, 212, 213 satisfaction _see_ applications in customer satisfaction value, 111, 119 

data 

anomalous _see_ outliers clean, 6, 8 influential, 27 missing, 106 raw, 6 sampling, 5 stream of, 4, 32, 33 data dredging, 9 data mart, 6–8, 112, 188 data snooping, 9 databases, 4–8 databases, 4–8 _see also_ DWH cooperation with R, 14 operational, 6–7 strategic, 6–8 data sets, 254–262 decision support, 6 decomposition Cholesky, 30, 32 QR, 30 spectral, 61 decomposition, spectral, 61 degrees of freedom, 38, 39, 97, 253, 263 effective, 94–96, 117, 185, 189 dendrogram, 218–222 descriptive statistics _see_ statistics, descriptive determinant, 240, 263 deviance, 19, 20, 38–41, 43, 47, 51, 97, 101, 104, 117, 120, 163, 216, 264 residual, 47, 51–53 diagnostics, graphical, 21–26, 29, 46 

SUBJECT INDEX 

273 

dimensionality, 4 curse of _see_ curse of dimensionality discriminant analysis, 154–159 linear, 155–156, 184, 189, 207, 263 quadratic, 156–157, 263 dissimilarity, 213–214, 222 between groups, 215, 218 for quantitative variables, 215 total, 215 within groups, 215–218 distance, 69, 77, 252 _see also_ dissimilarity as measure of dissimilarity, 213 Cook, 27 Euclidean, 17, 19, 213, 215–218, 264 and least squares, 247 Mahalanobis, 215 Manhattan, 215 Minkowsky, 215 distribution Bernoulli, 42 binomial, 38–40, 42, 166 _χ_[2] , 36, 38, 39, 95 and normal distribution, 245 conditional, 7, 230 of multivariate normal variable, 245 Gaussian _see_ distribution, normal marginal, 7, 225 of multivariate normal variable, 245 multinomial, 143, 147 multivariate, 241–243 normal, 20, 22, 36, 37 multivariate, 155, 224, 243–246 Snedecor _F_ , 38, 97 divergence, Kullback-Leibler, 230 DWH, 6–8, 112, 263 

effect interaction, 225 main, 20, 225 entropy, 166, 167, 170, 185, 189, 211 equations likelihood _see_ likelihood, equations normal, 248 equidensity ellipse, 244, 245 error approximation, 37, 38 prediction, 32, 141, 178, 181 

term of, 69, 149 and residuals, 21 in linear models multivariate, 29 normal, 20, 33, 38, 253 estimate, 17, 19, 20, 38, 74, 113, 117, 119, 209 computational aspects, 30–33 constrained, 251–252 maximum likelihood _see_ likelihood, estimate of maximum non-parametric, 68–111 nonparametric, 79 of false positives and false negatives, 139 robust, 75 sensibility and specificity, 140 sequential, 32, 109 unbiased, 249, 251 Euclidean norm _see_ distance, Euclidean example with data Brazilian bank, 39–40, 42–44, 144, 148, 255–256 car, 15–29, 68–77, 83–84, 87–89, 91–93, 97, 109, 254–255 customer satisfaction, 192–205, 259 fruit juice, 136–142, 151, 157, 161–163, 166–167, 177–180, 182–183, 258–259 insurance, 123–131, 257–258 simulated yesterday’s and tomorrow’s, 81, 100–101, 104, 254 telecommunications, 111–123, 183–192, 256–257 web usage, 205–209, 232–239, 261–262 expected improvement, 142 experimental design, 8 exploratory analysis, 45, 188 extrapolation, 22 

factor, 11, 15, 20, 27, 88, 136 experimental, 10, 11 not controlled, 11 false findings, 9 false positives and negatives, 138–139, 185, 189 

SUBJECT INDEX 

274 

feature _see_ variable filter, linear, 33 forward selection _see_ variable selection, stepwise Fourier series, 49 frequency table sparse, 229 three-way, 226 function activation, 108, 169 discriminant, 155 indicator, 264 kernel _see_ kernel (of SVM) _and_ kernel (of local regression) likelihood _see_ likelihood link, 41, 159 logarithmic, 226 log-likelihood _see_ likelihood, log-likelihood logistic, 40–42, 108, 169, 264 logit, 40–42, 93, 136, 151, 159, 160 multilogit, 143, 160, 163 _see also_ function softmax objective, 12, 13, 76, 108, 115, 168 of the least squares, 17 polynomial, 18, 47, 80 cubic, 80, 132 probit, 148 softmax, 170 step, 98–99, 132, 164 

GAM _see_ model, additive, generalized GCV _see_ generalized cross validation Gini index, 166, 183, 211 GLM _see_ model, linear, generalized graph, 109, 110, 224–228 acyclic, 107 conditional independence, 224 graphical model _see_ model, graphical graphical representation, 15, 16, 29, 43, 75, 77, 99, 112, 136 _see also_ plot _and_ histogram dynamic, 14 tools for, 13 

heterogeneity, 24, 166 heteroscedasticity, 24, 27 histogram, 113, 116 homoscedasticity, 21, 153 

hypercube, 7 hypothesis additive, 20, 90–93, 160–163 of normality, 21, 37, 157, 253 of the second order, 17, 37, 156 formulation of, 246 hypothesis test, 36, 37, 106, 139 for binomial variables, 39 repeated, 231 

identifiability, 90, 159 impurity, 166, 167 independence, 37, 224, 225 conditional, 224, 228 index, Gini _see_ Gini index inequality, Cauchy–Schwartz, 242 inner product, 222 input _see_ variable, explanatory interaction, 87, 91, 92 internal analysis methods, 212–239 interpolation, 50 

KDD, 8, 263 kernel (of SVM), 174–175 (of local regression), 69–72, 76 knots, 80 Kullback-Leibler divergence, 56 

Lagrange multipliers, 252 lasso _see_ regression, lasso layer, hidden, 106, 108, 109, 169 leaf of the tree, 99, 104 leaker _see_ variable, leaker learning supervised _see_ supervised learning unsupervised _see_ unsupervised learning least squares, 17, 18, 29, 81, 85, 86, 151 computational aspects, 30–33 general concepts, 246–247 objective function, 17 penalized, 82 recursive, 32–33, 154 weighted, 69, 77 iterative, 93, 226 levels (of a factor), 7, 19, 39, 87, 88, 104, 135, 148 

lift 

(as association measure), 230 

SUBJECT INDEX 

275 

(as performance indicator of classification procedures) _see_ curve, lift likelihood, 33–37, 41, 56 and AIC, 56–57 equations, 35 estimate of maximum, 33–37, 41, 56, 163 in binomial case, 38 in linear models, 253 with constraints, 36 function, 34, 57 log-likelihood, 35, 38, 39 ratio test, 36–40, 55, 136 linear combination, 60 linearly separable classes, 170 link (for cluster methods), 218–222 link (in GLM) _see_ function, link loess, 74–76, 160 log file, web, 261 log-likelihood _see_ likelihood, log-likelihood logit _see_ function, logit _and_ regression, logistic 

machine learning, 5, 33, 159, 229 majority vote, 177, 179 market basket analysis _see_ applications, in market basket analysis marketing, 8, 12, 212 actions, 111, 115, 119, 135, 142, 187, 190–192 MARS, 85–89, 117, 122, 163, 185, 189, 207–208, 263 masking, 154 masking of variable, 153 matrix confusion, 138, 163, 167, 177, 180 correlation, 223, 242 definition of, 240 design, 18, 152 diagonal, 241, 242 dispersion _see_ matrix, variance dissimilarity, 214 idempotent, 241, 248 identity, 19, 63, 240, 264 inverse, 241 inversion lemma, 241 

non-singular, 241 observed information, 35 orthogonal, 241 positive definite, 241, 242 positive semi-definite, 241, 242 projection, 54, 95, 248, 249, 252 rank of, 241 smoothing, 72, 91 symmetric, 31, 32, 240, 242 trace of, 241 transposed, 240 variance, 29, 242–243, 250, 264 mean squared error, 47 mean, arithmetic, 166, 176, 177, 216 definition of, 20 property of, 103 measure _J_ , 230 prediction adequacy, 138 medoid, 218 method of moments, 159 metric, Canberra, 215 minimization _see_ optimization misclassification error, 135, 138, 157, 166, 179, 185, 188, 194 cost of, 139, 188 misclassification table _see_ matrix, confusion missing data _see_ data, missing model, 45–46 additive, 89–93, 116–117, 123 generalized, 92–93, 160–164, 185, 189, 263 proportional odds, 164, 196 black box, 11, 12, 192 complexity, 4, 47–49, 160 general framework, 9–12 graphical, 224–228, 231 linear general formulation of, 246–253 generalized, 41–44, 59, 92, 148, 226, 263 regression _see_ regression, linear with second-order hypothesis _see_ hypothesis of the second order log-linear, 225–229 logistic multivariate _see also_ regression, logistic 

SUBJECT INDEX 

276 

model ( _Cont’d._ ) logistic, multivariate, 143 MARS _see_ MARS mathematical, 10 multinomial logit, 143 parametric, 49, 59 polytomous logit, 143 proportional odds, 144–148, 193–196 regression _see_ regression selection, 52–60 

nearest–neighbour, 76 neural network, 106–111, 117, 123, 168–170, 185, 189, 208–209 node, 99 non-parametric approach, 68, 155, 159–164 nonparametric approach, 51 norm _L_ ∞, 215 Euclidean _see_ distance, Euclidean numerical analysis, 35, 42, 109 

observations _see also_ data observations anomalous, 76, 159 influential _see_ data, influential missing _see_ data, missing odds, 42 OLAP, 7–9, 263 OLTP, 6, 263 optimism, 49 optimization, 19, 37, 70, 82, 101, 109, 155, 173 myopic, 102, 104 step-by-step, 101 orthogonality, 61, 248 of vectors, 252 out-of-bag, 178–179, 182, 183 output _see_ variable, response overfitting, 49, 52, 53, 86, 108, 170, 181 with AIC, 104 

_p_ -value, 20, 36–38, 40, 43, 136 parameter complexity, 86–87, 103, 108–109, 170, 173, 181, 185, 189 penalization _see_ parameter, complexity regression, 17, 29, 37, 116, 246 

smoothing, 70, 72–75, 77, 81–83, 94, 96–97, 117 variable, 75–76 tuning _see_ parameter, complexity parametrization, corner, 136 pattern of data, 5, 7, 231 perceptron, 170 plot Anscombe, 21 bar, 136 box, 136 calibration, 204 quantile-quantile, 21, 26 scatter, 16, 17, 23, 25, 26, 46, 151 predictor, linear, 41, 116, 246 pricing _see_ applications in pricing principal components, 60–64, 79 probability a posteriori, 154 a priori, 154, 158 and relative frequencies, 229 conditional, 229 projection, 19, 61, 95, 171 _see also_ matrix, projection constrained, 252 projection pursuit, 93–94 prospects, 135 pure premium, 124 

qq-plot _see_ plot, quantile-quantile quadratic form, 246, 253 quality control, 140 query, 3, 6 

R, 13–14, 78, 113, 126 random forests, 180–183, 209 random variable _see also_ distribution mixed, 112 multivariate, 241–243 rank, 264 rare events, 188–189 real-time, 32, 154, 158 record, 31, 55 regression, 68–131, 177 all subset, 59 hyperplan, 245 lasso, 64–66 least-angle, 64–66 linear, 15–30, 113–116, 123 

SUBJECT INDEX 

277 

in classification, 149–154, 184, 189, 207 multivariate, 28–30, 152–153, 196 with transformed variables, 116 local, 69–79, 97 multidimensional, 76–77 logistic, 40–44, 135–136, 184, 189, 207 logistic, multivariate, 142–143 multinomial, 143–144 non-linear, 23, 68, 107 parametric, 80 polynomial, 18, 46–47, 49, 151, 153 projection pursuit, 93–94 proportional odds, 144–148 ridge, 63–64 regressor _see_ variable, explanatory residual, 21, 22, 24, 26, 27, 33, 94, 95, 113 retention action, 187, 190 ridge regression _see_ regression, ridge robustness, 76, 106, 158, 159 ROC _see_ curve, ROC root of the tree, 99, 104 rule, 5 association, 228–231 probabilistic, 229 rule, association _see_ association rule 

S, 13 S-plus, 78 sample, 79, 176 balanced, 188, 189 representative, 12 size, 53 small, 57 stratified, 188 sampling plan, 8 sensitivity, 140 set test _see_ test set training _see_ training set validation _see_ validation set Sherman–Morrison, formula of, 241 Sherman-Morrison, formula of, 32 significance level, 36 effective, 231 observed _see p_ -value size, 4, 36, 37 skewness, 26, 115 

smoother, linear, 83 software, 12, 13 _see also_ R open source, 13 specificity, 140 spline, 89 cubic, 80–82 natural, 80, 132 interpolation, 132 regression, 80–81, 84, 85, 117, 185, 189 multivariate adaptive _see_ MARS smoothing, 81–84, 117, 163, 185, 189 tensor product, 84–85 thin plate, 83–84, 160 SQL, 6, 7, 263 standard deviation, 242 standard error and model selection, 60 for MLE, 35–36 for multivariate multiple regression, 29 for non-parametric estimate, 75 for out-of-bag, 182 for regression parameters, 19, 20 in the binomial case, 38 lack of, 110 non canonical use of, 153 recursive calculation of, 33 statistics medical, 140 statistics descriptive, 7, 9 StatLib, 258 stepwise selection _see_ variable selection, stepwise stochastic search of the model, 177 stratification, 16, 39, 40, 188 _see also_ sample, stratified study clinical, 5 experimental, 11 observational, 11 supervised learning, 68–212 support (of a rule), 230 support vector machines, 170–175, 209, 263 SVM _see_ support vector machines 

tails distribution, 22 heavy, 22 

SUBJECT INDEX 

278 

test _F_ , 97, 113, 253 likelihood ratio, 36–40 Wald, 36, 43 test set, 53–54, 87, 104, 112, 122, 130, 131, 151, 177, 179, 181, 183, 189 theorem Bayes, 154 of Pythagoras, 249 trace, 263 trade-off, bias–variance, 49–51, 53, 72–73 training set, 53–54, 104, 112, 176 balanced, 189 treatment, 11 tree, 106, 263 binary, 99, 218 classification—, 164–168, 177, 179, 180, 183, 185, 187, 189, 207 growth of, 99–103, 177, 181 leaf of, 218 pruning of, 102–104, 118, 177 regression, 98–106, 117–119, 122 

universal approximator, 93, 109 unsupervised learning _see_ internal analysis methods up-sell, 123, 135 

validation set, 53 value expected, 22, 264 of a multivariate variable, 241 fitted, 18, 19, 94 leave-one-out, 54 predicted, 18 variability bands, 74–76, 117 variable actionable, 190 binary _see_ variable, dichotomous categorical, 15, 19, 87, 104, 106, 134, 148, 164, 214, 225–231 and dissimilarity measures, 218 and measures of dissimilarity, 213 ordinal, 213, 214 dichotomous, 38, 40, 42, 228–231 

explanatory, 16, 18, 78–80, 85, 90, 94, 106, 112, 174, 180 in linear model, 247 importance of, 104, 131, 182 independent _see_ variable, explanatory indicator, 19, 26, 136, 229, 264 latent, 106, 147, 169 leaker, 9 qualitative _see_ variable, categorical _and_ variable, response, qualitative quantitative, 213, 214 _see also_ variable, response, quantitative response, 28, 80, 90, 106 categorical, 135 dichotomous, 38, 149 in linear model, 37, 247 qualitative, 134 quantitative, 68–133 selection, 58–60, 106, 117, 182 optimal, 59 stepwise, 59–60, 86, 113, 193 uncorrelated components, 242 variance, 49, 56, 155, 177, 264 conditional, 245 constant, 16 estimation, 19, 35 explained, 61 matrix, 242 residual, 74, 113 unbiased, 251 trade-off between bias and _see_ trade-off, bias–variance vector, 240 mean value, 216 projection, 248, 249 residual, 249–251 vector space, 247–249, 251–252 orthogonal, 251 visualization, data _see_ graphical representation _and_ plot 

weak classifier, 179 web mining, 205–209 weight decay, 109, 117, 185, 189 window, smoothing, 70, 72, 75 


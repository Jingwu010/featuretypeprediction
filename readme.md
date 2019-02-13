**Jingwu Xu** 

## Project:

Build a training data creation framework, say, using Snorkel for automatic ML schema extraction from data files for predicting feature type based on attribute name, sample values, and statistics. Compare with recent work on manually labeled dataset.

## Meeting:

Wednesday 1.30pm.

## Rules for assigning labels

|            Category             | Case                                                         |             |
| :-----------------------------: | :----------------------------------------------------------- | ----------- |
|   **Usable directly numeric**   | **Case a.** Should be usable directly as a number feature for ML | numeric     |
|   **Usable with extraction**    | **Case b.** A number present along with unit of measure string<br/>**Case c.** A text corpus with semantic meaning <br/>**Case d.** Date or time stamp | textual     |
| **Usable directly categorical** | **Case e.** Yes/No type values, including binary 0/1 answers <br/>**Case f.** Country names, city names, food type names, and other object type names that are not cases *l* or *m* below <br/>**Case g.** Coded numbers that are short forms of names in case *f* that are not cases *l* or *m* below <br/>**Case h.** Short names that indicate type from a known finite set/domain that are not case *l* below <br/>**Case i.** Handful of coded numbers that repeat themselves but arbitrary arithmetic on them is not meaningful and that are also not case *l* or *n* below <br/>**Case j.** A coded number that encodes real-world entities from a known finite domain set | categorical |
|          **Unusable**           | **Case k.** A number indicating the position of a record in its dataset table <br/>**Case** **l.** An attribute that is likely the primary key in its dataset table | unusable    |
|      **Context dependent**      | **Case m.** Person name, company name, or any entity name that is not generic <br/>**Case** **n.** Coded numbers or id for people, company, or other entity names from case m that are not cases g, i, j, k, or l above. | dependent   |



## Questions:

1. 

   | Record_id | y_pred                 | y_act            | Reason | y_Arun           | Check       | Attribute_name | Total_val | num of dist_val |             | Num of nans | mean        | std_dev     | min_val | max_val | sample_1        | sample_2        | sample_3        | sample_4        | sample_5        |
   | --------- | ---------------------- | ---------------- | ------ | ---------------- | ----------- | -------------- | --------- | --------------- | ----------- | ----------- | ----------- | ----------- | ------- | ------- | --------------- | --------------- | --------------- | --------------- | --------------- |
   | 53        | Unusable               | Unusable         | l      | Unusable         |             | id             | 50000     | 50000           |             | 0           | 44432.4548  | 15773.45744 | 17283   | 73469   | 17283           | 17284           | 17285           | 17286           | 17287           |
   | 48        | Unusable               | Unusable         | l      | Unusable         |             | BeerID         | 73861     | 73861           |             | 0           | 36931       | 21321.83411 | 1       | 73861   | 1               | 2               | 3               | 4               | 5               |
   | 51        | Unusable               | Context_specific | n      | Context_specific | check       | animal_id      | 29421     | 28209           | 95.88049353 | 0           | 0           | 0           | 0       | 0       | A684346         | A685067         | A678580         | A675405         | A670420         |
   | 34        | Unusable               | Context_specific | l      | Context_specific |             | id             | 671205    | 671205          |             | 0           | 993248.5937 | 196611.129  | 653047  | 1340339 | 653051          | 653053          | 653068          | 653063          | 653084          |
   | 50        | Unusable               | Context_specific | m      | Context_specific | interesting | ACTOR1_ID      | 165808    | 3032            | 1.828621056 | 25061       | 2587.796692 | 1030.062165 | 1       | 3960    |                 | 1071            | 2037            | 1077            | 2191            |
   | 37        | Usable with extraction | Context_specific | n      | Context_specific | check       | Loan Theme ID  | 15736     | 718             | 4.562785968 | 0           | 0           | 0           | 0       | 0       | a1050000000slfi | a10500000068jPe | a1050000002X1Uu | a1050000007VvXr | a1050000000weyk |



**Regarding to Snorkel:**

1. If two labeling functions give two different labels, how does Snorkel deal with it? I assume the Snorkel model only generates one label for each data point. 'Once the model is trained, we can combine the outputs of the LFs into a single, noise-aware training label set for our extractor'

2. Need more explanation on labeling function comparison generated by Snorkel? How do I tell which labeling function is better than the other? how do I tell which labeling function takes effect when doing the prediction.

   <img src='./imgs/lf_stats.png'>

   <img src='./imgs/snorkel_ex.png'>

**Regarding to data:**

1. What does it mean when predicting '1,2,3,4,5'?

   ```
   1062	68.146296	hm15life	NaN	6540	a	350	9597	Usable directly numeric	NaN	NaN	...	NaN	NaN	1	5	7	2	1265.812302	NaN	Context_specific	1
   1063	68.219235	hm15owner	NaN	6547	a	350	9597	Usable directly numeric	NaN	NaN	...	NaN	NaN	3	1	2	0	0.486729	NaN	Context_specific	3
   ```

   ```python
   print(*np.unique(pred),sep='\n')
       
   > 1
   > 2
   > 3
   > 4
   > 5
   > Context_specific
   > Unusable
   > Usable directly categorical
   > Usable directly numeric
   > Usable with extraction
   ```

   

According the provided files, I noticed that there exists a lot of inconsistence. X-axis represents predicted label, Y-axis represents actual labels. And the Confusion Matrix is:

<img src='./imgs/cm_plot.png'><img src='./imgs/cmn_plot.png'>

1. Most problematic field is `context specific`, which is largely misclassified into `usable directly numeric`.

2. Record `208-247` attribute name with 'xxxid' are classified into `usable directly numeric`

3. Record `1041-1079` classified into `numbers (1-5)?`

4. What does columns means?

   ```
   'Unnamed: 2',
   'Unnamed: 9',
   'check',
   ```

## Progress:

**1/30:**

+ walk through Snorkel tutorials
+ play around with data and get some insights
+ looking for related papers, **suggestions from professor?**



1. http://www.vldb.org/pvldb/vol12/p223-varma.pdf
2. http://cidrdb.org/cidr2019/papers/p58-ratner-cidr19.pdf

---

**2/6:** 

+ Extract features from raw data

+ Performed character level LSTM on variable name, (91% accuracy) (5000 train vs 1000 test)

  Problems: lots of duplicated records, hard to generalize on unseen names. 

1. How could I design hierarchical labelling functions?

2. How to fit trained NN model into labeling function?

3. Choices between RNN and CNN? Which fits best to different types of features? 

4. What else information from data could be valuable?

5. Can I get some existing labeling functions from previous work?

6. Plan to fit LSTM on histogram.

7. Plan to fit CNN for other features.

8. How to Fit the end model after snorkel?

9. Extremely long time to extract features.

   ![name_lstm_cm](imgs/name_lstm_cm.png)

   `['name', 'total', 'nunique', '%unique', '#null', 'std', 'var', 'min', 'max', 'mean', 'median', 'mode', 'hist0', 'hist1', 'hist2', 'hist3', 'hist4', 'hist5', 'hist6', 'hist7', 'hist8', 'hist9']`

```python
def LF1:
  if values == strings:
    goto LF2
   if values == numbers:
    goto LF3
```
| #    | y_act | Attribute_name |
| ---- | ----- | -------------- |
| 155 	| Unusable                    	| #                                          	|
| 153 	| Usable directly categorical 	| #Table1                                    	|
| 986 	| Usable directly numeric     	| $ Oil prices                               	|
| 994 	| Usable directly numeric     	| 10 year/medium-term government bond yields 	|
| 968 	| Unusable                    	| 1990 [YR1990]                              	|
| 23  	| Context_specific            	| 1990 [YR1990]                              	|
| 393 	| Unusable                    	| 2-alpha code                               	|
| 24  	| Context_specific            	| 2000 [YR2000]                              	|
| 15  	| Context_specific            	| 2008 [YR2008]                              	|
| 16  	| Context_specific            	| 2009 [YR2009]                              	|
| 17  	| Context_specific            	| 2010 [YR2010]                              	|
| 27  	| Context_specific            	| 2011 [YR2011]                              	|
| 18  	| Context_specific            	| 2012 [YR2012]                              	|
| 19  	| Context_specific            	| 2013 [YR2013]                              	|
| 20  	| Context_specific            	| 2014 [YR2014]                              	|
| 21  	| Context_specific            	| 2015 [YR2015]                              	|
| 22  	| Context_specific            	| 2016 [YR2016]                              	|
| 574 	| **Unusable**                 | **2017 [YR2017]**                           |
| 20  	| Context_specific            	| ABV                                        	|
| 581 	| Usable directly categorical 	| AC                                         	|
| 816 	| Context_specific            	| ACCT_PD                                    	|
| 764 	| Usable with extraction      	| ACTION                                     	|
| 808 	| Usable directly numeric     	| ACTIVITY                                   	|
| 208 	| Usable directly categorical 	| ACTOR1                                     	|
| 209 	| Context_specific            	| ACTOR1_ID                                  	|
| 210 	| Usable directly categorical 	| ACTOR2                                     	|
| 211 	| Context_specific            	| ACTOR2_ID                                  	|
| 384 	| Context_specific            	| ACTOR_DYAD_ID                              	|
| 365 	| Usable with extraction      	| ADDRESS                                    	|
| 514 	| Usable Directly Numeric     	| ADEC                                       	|
| ... 	| ...                         	| ...                                        	|
| 64  	| Context_specific            	| y                                          	|
| 785 	| Usable directly numeric     	| y_coordinate                               	|
| 262 	| **Unusable**                 | **year**                                    |
| 2   	| **Usable Directly Categorical** | **year**                                    |
| 237 	| **Usable directly categorical** | **year**                                    |
| 463 	| Usable directly numeric     	| yearly_sunlight_kwh_e                      	|
| 465 	| Usable directly numeric     	| yearly_sunlight_kwh_f                      	|
| 448 	| Usable directly numeric     	| yearly_sunlight_kwh_kw_threshold_avg       	|
| 466 	| Usable directly numeric     	| yearly_sunlight_kwh_median                 	|
| 461 	| Usable directly numeric     	| yearly_sunlight_kwh_n                      	|
| 462 	| Usable directly numeric     	| yearly_sunlight_kwh_s                      	|
| 467 	| Usable directly numeric     	| yearly_sunlight_kwh_total                  	|
| 464 	| Usable directly numeric     	| yearly_sunlight_kwh_w                      	|
| 606 	| Usable Directly Numeric     	| yearsuse1                                  	|
| 255 	| Usable Directly Numeric     	| yearsuse10                                 	|
| 256 	| Usable Directly Numeric     	| yearsuse11                                 	|
| 257 	| Usable Directly Numeric     	| yearsuse12                                 	|
| 607 	| Usable Directly Numeric     	| yearsuse2                                  	|
| 109 	| **Context_specific**         | **yearsuse3**                               |
| 110 	| **Context_specific**         | **yearsuse4**                               |
| 250 	| Usable Directly Numeric     	| yearsuse5                                  	|
| 251 	| Usable Directly Numeric     	| yearsuse6                                  	|
| 252 	| Usable Directly Numeric     	| yearsuse7                                  	|
| 253 	| Usable Directly Numeric     	| yearsuse8                                  	|
| 254 	| Usable Directly Numeric     	| yearsuse9                                  	|
| 185 	| Usable directly numeric     	| yes_rsvp_count                             	|
| 788 	| Usable directly numeric     	| yieldpercol                                	|
| 65  	| Context_specific            	| z                                          	|
| 175 	| Usable directly categorical 	| zip                                        	|
| 722 	| Usable directly categorical 	| zip_code                                   	|

---

**2/13**:

 + Get to know to snorkel takes in labeling function matrix

 + Writing labeling functions **Usable with extraction**

   | LF                           | RESULTS                        | Explanations                                               |
   | ---------------------------- | ------------------------------ | ---------------------------------------------------------- |
   | lf_date_extraction_name      | [  6.,  21., 149.,  12.,   1.] | datetime, time, date in name                               |
   | lf_date_extraction_samples   | [  5.,   0., 187.,   8.,  16.] | samples in datetime format                                 |
   | lf_extractable_name          | [ 51.,  16., 122.,  32.,   8.] | url, comment etc. in name                                  |
   | lf_extractable_list          | [ 2.,  3., 26.,  5.,  0.]      | samples with list, dict, format                            |
   | lf_extractable_sample_length | [123.,   3., 274.,  37.,  57.] | samples with long length                                   |
   | lf_extractable_units         | [1., 0., 3., 0., 0.]           | samples in (unit) num, unit format                         |
   | lf_extractable_number_sci    | [1., 1., 0., 0., 0.]           | samples with scientific rep                                |
   | lf_extractable_pattern       | [25.,  1., 78., 14., 14.]      | samples where texts follow pattern while differ in numbers |

 + Q: a lF only produces one category or none?

 + TODO: Write more labeling functions

 + TODO: Feed m*n data into snorkel
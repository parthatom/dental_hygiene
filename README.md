# dental_hygiene
ECE 143 Group 18

## Data preprocessing

Load dietary, nutrition and dental datasets (as described in prososal) and join them together. The training data is stored in file "train_data.csv". 

To checkout the meaning of each column, please refer to the documentation websites:

https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/P_DSQTOT.htm

https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/P_DR1TOT.htm

https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/P_OHXDEN.htm


Our dataset has 13772 observations and 374 features with a lot of empty entries. 

### Dietary dataset

Missing values are treated as 0: The reason why many entries are missing is that many respondents didn't have any dietary supplement.

Answers "Refused" or "Don't know" in "DSDCOUNT - Total # of Dietary Supplements Taken", "DSDANCNT - Total # of Antacids Taken", "DSD010 - Any Dietary Supplements Taken?" and "DSD010AN - Any Antacids Taken?" are treated as 0 or No.

### Dental Dataset
Conversion Matrices :

#### Tooth Count
| Code |              Description	              |            Count            | Cumulative | Convert |
|:-----|:--------------------------------------:|:---------------------------:|:----------:|--------:|
| 1	   |   Primary tooth (deciduous) present	   |              0              |     0      |       1 |     Present|
| 2	   |        Permanent tooth present	        |            7534	            |    7534    |       1 |              Present               |
 | 3    |          	    Dental implant           | 	                        4	 |    7538    |       0 |               Absent               |
| 4    |        	    Tooth not present	         |            5609	            |   13147    |       0 |      Absent|
| 5	   | Permanent dental root fragment present |            	131	            |   13278    |       0 |                Absent              |
| 9    |         	    Could not assess          |   	                    0	   |   13278    |       0 |      Treat as Absent|
| .	   |                Missing	                |            494	             |   13772    |       0 |              Treat as Absent           |


#### Caries
| Code |                                 Description	                                 |                         Count                         |   Cumulative   | Convert |
|:-----|:----------------------------------------------------------------------------:|:-----------------------------------------------------:|:--------------:|--------:|
| A    |            	    Primary tooth with a restored surface condition	             |                          0	                           |       0        |       1 |
| D	   |                             Sound primary tooth	                             |                          0	                           |       0        |       0 |
| E    |                      	    Missing due to dental disease                      |     	                                        1197     |     	1197      |       1 |
| F	   |              Permanent tooth with a restored surface condition	              |                         2908                          |     	4105      |       1 |
| J    | 	    Permanent root tip is present but no restorative replacement is present |                         	131	                         |      4236      |       1 |
| K	   |            Primary tooth with a dental carious surface condition	            |                          0	                           |      4236      |       1 |
| M    |                      	    Missing due to other causes	                       |                          47	                          |      4283      |       1 |
| P	   |    Missing due to dental disease but replaced by a removable restoration     |                         	1019                         |     	5302      |       1 |
| Q    |  	    Missing due to other causes but replaced by a removable restoration	   |                          37	                          |      5339      |       1 |
| R    |   	    Missing due to dental disease but replaced by a fixed restoration	    |                          13	                          |      5352      |       1 |
| S    |                          	    Sound permanent tooth                          | 	                                                4394 |      9746      |       0 |
| T    |    Permanent root tip is present but a restorative replacement is present    |                          	0	                          |      9746      |       1 |
| U    |                               	    Unerupted	                                |                         3297                          | 13043      nan |
| X    |    	    Missing due to other causes but replaced by a fixed restoration	     |                          0	                           |     13043      |     nan |
| Y    |              	    Tooth present, condition cannot be assessed	               |                          11	                          |     13054      |     nan |
| Z    |        	    Permanent tooth with a dental carious surface condition	         |                         220	                          |     13274      |       1 |

#### Dental Sealants Data Description

| Code |                Description	                 | Count | Cumulative | Convert |
|:-----|:-------------------------------------------:|:-----:|:----------:|--------:|
| 0    |            Sealant not present	             | 4194  |   4194	    |       0 |
| 1    |     Occlusal sealant on permanent tooth     |  102  |    4296    |       1 |
| 2    |      Facial sealant on permanent tooth      |   0   |    4296    |       1 |
| 3    |     Lingual sealant on permanent tooth      |   0   |    4296    |       1 |
| 4    |      Occlusal sealant on primary tooth      |  51   |    4347    |       1 |
| 9    |             Cannot be assessed              |  41   |    4388    |     nan |
| 12   | Occlusal-facial sealant on permanent tooth  |   0   |    4388    |       1 |
| 13   | Occlusal-lingual sealant on permanent tooth |   0   |    4388    |       1 |
| nan  |                   Missing                   | 9384  |   13772    |     nan |

#### Root Caries, other lesions X [restored , not] Data Description

| Code |      Description	       |  Count   | Convert |
|:-----|:-----------------------:|:--------:|--------:|
| 1	   |          Yes	           |   1085   |       1 |
| 2    |        	    No	         |  6916	   |       0 |
| 9    | 	    Cannot be accessed | 	    7		 |     nan |
| .    |      	    Missing	      |  5764	   |     nan |

## Models
- Run train to get a dict of Classifiers to Accuracy
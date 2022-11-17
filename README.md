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

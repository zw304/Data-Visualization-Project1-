library(tidyverse) 
#install.packages("MASS") #this is the library for ships data
library(dplyr)
library(tidyr)
library(stringr)
#install.packages("gsubfn") # this is used to try to remove [ & ] with one function, but still use gsub instead.
library(gsubfn)


#Task1/p2: Make the district.csv data tidy.
district <- read.csv("data/districts.csv")
head(district)
str(district) # look up data type 

#delete symbol [ & ] in municipality_info column
district$municipality_info <-as.character(district$municipality_info) #set the data type into character
str(district)
district$municipality_info<- gsub("]","",gsub("[","",district$municipality_info, fixed = TRUE))
head(district)
district[c("Population < 500", "Population 500~1999", "Population 2000~9999", "Population >= 10000")] <- str_split_fixed(district$municipality_info,",", 4) # add one more column
head(district)

#delete symbol [ & ] in unemployment_rate and split the column into 95 and 96
district$unemployment_rate <-as.character(district$unemployment_rate) # convert the data type from factor to character
district$unemployment_rate<-gsub("]","",gsub("[","",district$unemployment_rate,fixed = TRUE))
head(district)
district[c("95_unemployee_rate","96_unemployee_rate")] <-str_split_fixed(district$unemployment_rate,",", 2)
head(district)

##delete symbol [ & ] in commited_crimes and split the column into 95 and 96
district$commited_crimes <-as.character(district$commited_crimes) # convert the data type from factor to character
district$commited_crimes<-gsub("]","",gsub("[", "", district$commited_crimes, fixed = TRUE))
head(district)
district[c("95_commited_crimes_numbers","96_commited_crimes_numbers")] <-str_split_fixed(district$commited_crimes,",", 2)
head(district) 

drop<- c("municipality_info","unemployment_rate","commited_crimes") # remove the repeated original columns 
tidy_district = district[,!(names(district) %in% drop)] # this is the tidy dataset
head(tidy_district)
write.csv(tidy_district,"district_r.csv", row.names = FALSE) # save the tidy data into csv file
#ncol(tidy_district)
#nrow(tidy_district)
#str(district) 
#head(district) 


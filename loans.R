#Task1:
library(tidyverse)
#install.packages("MASS") #this is the library for ships data
library(MASS)
library(reshape) 
library(reshape2) #these two libraries are for melt() and cast() function

#Problem1: Make the loans.csv data tidy. 
#we have two different variables(e.g.24 and A) in one cell. We need to split the variables in two columns.
#A stands for an expired loan that was paid in full
#B stands for an expired loan that was not paid in full (it was in default)

loans<- read.csv("data/loans.csv") 
head(loans) 
#molten.data <- melt(df, id = c("n","time"))
melt_loan  <-melt(loans,id = c("id","account_id","date","amount","payments")) # only retian the first 5 columns
head(melt_loan)
#set "-" as column "value" as NA:
melt_loan[melt_loan == "-"] <- NA
melt_loan <- na.omit(melt_loan)
head(melt_loan)

melt_loan[c('terms','status')]<-str_split_fixed(melt_loan$variable,'_',2) 
head(melt_loan)
# split X24_A to two columns: "value" and "terms"
melt_loan$terms<-gsub("X","",melt_loan$terms,fixed=TRUE)
head(melt_loan)

# reference for ealseif function: https://www.tutorialspoint.com/r/r_if_else_statement.htm

x<-c("A",'B')
melt_loan$loan_status<-ifelse(melt_loan$status %in% x, 'expired','current')

y<-c("A",'C')
melt_loan$loan_default<-ifelse(melt_loan$status %in% y, 'F','T')
head(melt_loan) 

#set "-" as column "value" as NA:
#melt_loan[melt_loan == "-"] <- NA
#head(melt_loan)
drop<-c("variable","value","status")
tidy_loan = melt_loan[,!(names(melt_loan) %in% drop)]

nrow(tidy_loan) #682
head(tidy_loan)
str(tidy_loan)
write.csv(tidy_loan,"loan_r.csv",row.names=FALSE)

#for check:
#nrow(tidy_loan)
#ncol(tidy_loan)




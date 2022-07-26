library(ggplot2)
analy<-read.csv("analytical_r.csv")
head(analy)
analy<-df(analy)
str(analy)
mydata<-data.frame(analy)
#1. histogram of number of customers per account
hist(analy$num_customers)
#2.relationship between credit cards & max balance
ggplot(analy,aes(x=credit_cards,y=max_balance))
#3.
barplot(analy$loan_payments,xlab="loan_paymnets",ylab="frequency",main="loan payment amounts")
#4.discover relationship between number of cc payments and different account_id
ggplot(mydata,aes(x=cc_payments,y=account_id,colour=cc_payments))+ geom_point(size=0.01)


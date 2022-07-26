account <- read.csv('data/accounts.csv')
district <- read.csv('district_r.csv')
clients <- read.csv('data/clients.csv')
links <- read.csv('data/links.csv')
cards <- read.csv('data/cards.csv')
loan <- read.csv('loan_r.csv')
transactions <- read.csv('data/transactions.csv')
payment_orders <- read.csv('data/payment_orders.csv')
#join account and district
head(account)
head(district)
# include all the rows of two data frames using "left_join" function to join match "account_id": 
#reference: https://stackoverflow.com/questions/1299871/how-to-join-merge-data-frames-inner-outer-left-right

A_D<- merge(x = account, y =district , by = c("district_id" = "id"), all.x = TRUE) 
# left outer join with same district_id
head(A_D)
#A_D <- account %>% left_join(districts,by=c('district_id' = 'id'))
#reference: https://stackoverflow.com/questions/7531868/how-to-rename-a-single-column-in-a-data-frame
names(A_D)[names(A_D) == "date"] <- "open_date" 
names(A_D)[names(A_D) == "id"] <- "account_id"
names(A_D)[names(A_D) == "name"] <- "district_name"
head(A_D)
A_D<-A_D[c("account_id","district_name","open_date","statement_frequency")]
#adjoin <- adjoin[,c(1,3,4,5)]
head(A_D)
ncol(A_D)
nrow(A_D) #4500

#join "links" table to A_D
head(links)
links1<-links %>% group_by(account_id) %>% summarize(num_customers = n()) 
A_D_L <- merge (x=A_D, y=links1, by = c('account_id' = 'account_id'))
head(A_D_L)
nrow(A_D_L) #4500

#join "card" to links
head(cards)
names(cards)[names(cards) == 'type'] <- "card_type"
names(links)[names(links) == 'id'] <- "links_id"
head(links)
x<-cards$link_id
links$card <- ifelse (links$links_id %in%x,"T","F")
y<-links[(links$card == "T"),]
y$cards = 1

A_D_L$credit_cards <- y$cards[(match(A_D_L$account_id, y$account_id))]
A_D_L$credit_cards[is.na(A_D_L$credit_cards)] <- 0
nrow(A_D_L) # 4500
head(A_D_L)

#join loan to A_D_L
head(loan)
nrow(loan) #682

drop<-c("date")
loan = loan[,!(names(loan) %in% drop)]
head(loan)
ADL_L<- merge(x = A_D_L, y =loan , by = c("account_id" = "account_id"), all.x = TRUE)
head(ADL_L)
#DETERMINE T/F:
ADL_L$loan <-ifelse(ADL_L$id %in% NA, 'F','T')
loan <- ADL_L %>% group_by(account_id) %>% distinct() # FILTER AND GROUP BY ACCOUNT ID
names(loan)[names(loan) == 'amount'] <- "loan_amount"
names(loan)[names(loan) == 'payments'] <- "loan_payments"
names(loan)[names(loan) == 'terms'] <- "loan_term"
head(loan)
drop<-c("id")
loan = loan[,!(names(loan) %in% drop)]
head(loan)
nrow(loan)#4500


#### max& min witrhdrawal: 
head(transactions)
W <- transactions %>% filter(type == 'debit') %>% as.data.frame()
#DEFINE min& max withdrawal: amount withdrawn for the account
transactions$min_withdrawal <- min(W$amount)
transactions$max_withdrawal <- max(W$amount)
head(transactions)
trans <- transactions[,c('account_id','max_withdrawal','min_withdrawal')]
head(trans)
nrow(trans) #1056320
W_join <- loan %>%left_join(trans, by = c('account_id'= 'account_id')) %>% distinct()

head(W_join) # done
nrow(W_join)#4500
#----------

####
# cc_payments: Count of credit payments for the account for all cards

credit_pay <- transactions %>% filter(type == "credit") %>% as.data.frame()
#rlang::last_error()
T_C<-credit_pay %>% group_by(account_id) %>% summarize(cc_payments = n())
#head(W_by)
nrow(T_C)#4500
TC_join<- merge(x = W_join,y =T_C, by = c("account_id" = "account_id"), all.x = TRUE)
head(TC_join)
nrow(TC_join) #4500

####
#min/max_balance: amount of balance in the account
transactions$min_balance <- min(W$balance) # define min balance 
transactions$max_balance <- max(W$balance) #define max balance
head(transactions)
trans <-transactions[,c("account_id","max_balance","min_balance")]
analytical <- TC_join %>%left_join(trans, by = c('account_id'= 'account_id')) %>% distinct()
#nrow(analytical) #4500

write.csv(analytical,"analytical_r.csv",row.names = FALSE)





  
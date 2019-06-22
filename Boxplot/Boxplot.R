## Drawing boxplots divided by groups and months
## for monitoring multi-strategy investment performance


## Set working directory (not necessary)
setwd(""~/your path"")


## Generating file & dataframe names by each month
## Target Period : '17.1 ~ '18.01
file.yymm <- c(1701:1712, 1801:1802)
file.name <- sprintf('stock_history_%s.csv', file.yymm)
df.name <- sprintf('stk.history.%s', file.yymm)


## Making dataframes by each month data
for (i in 1:length(file.yymm)) {
  assign(df.name[i], read.csv(file.name[i], header=T))
  print(sprintf('stk.history.%s', file.yymm[i]))
}


## Merging mothly data
## These ugly codes should be upgraded!
stk.history <- c()
for (i in 1:length(file.yymm)) {
  stk.history <- rbind(stk.history.1701,
                       stk.history.1702,
                       stk.history.1703,
                       stk.history.1704,
                       stk.history.1705,
                       stk.history.1706,
                       stk.history.1707,
                       stk.history.1708,
                       stk.history.1709,
                       stk.history.1710,
                       stk.history.1711,
                       stk.history.1712,
                       stk.history.1801,
                       stk.history.1802)
}


## Checking the structure of the merged dataframe
str(stk.history)


attach(stk.history)


## Boxplot 1
windows(width=10, height=7)
boxplot(수익률 ~ YYMM, main="Monthly Performace (Total)")
abline(h=0, col='red')

## Boxplot 2
windows(width=10, height=7)
boxplot(수익률 ~ 그룹 + YYMM, 
           main="Comparing Groups : Traditional vs DayTrading",
           col=c('skyblue','pink'))
abline(h=0, col='red')

## Boxplot 3
windows(width=10, height=7)
boxplot(수익률 ~ YYMM, subset=그룹=='DayTrading',
           main="DayTrading Performance", col=c('pink'))
abline(h=0, col='red')


detach(stk.history)


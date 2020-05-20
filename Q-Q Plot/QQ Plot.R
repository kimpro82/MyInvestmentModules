## 일일수익률 QQ Plot ##

money <- read.csv("longshort_150118.csv", header=T, na.strings=".")
summary(money[,-c(2,3,5,6,7)])

attach(money[,-c(2,3,5,6,7)])

library(lattice)

windows(width=7, height=5)
xyplot(수익률~rank(수익률)|Group,
  main="주식선물 일간수익률 Q-Q Plot (20140421~20150116)",
  panel=function(x,y) {
    panel.xyplot(x,y)
    panel.abline(h=mean(y), col="red")
    panel.abline(h=0, lty=3)
  }
)

detach(money)


## 주간수익률 QQ Plot ##

money2 <- read.csv("longshort_150118_2.csv", header=T, na.strings=".")
summary(money2)[,c(1,2,5,6,7)]

attach(money2[,c(1,2,5,6,7)])

library(lattice)

windows(width=7, height=5)
xyplot(수익률~rank(수익률)|Group, abline=c(h=0),
  main="주식선물 주간수익률 Q-Q Plot (20140421~20150116)",
  panel=function(x,y){
    panel.xyplot(x,y)
    panel.abline(h=mean(y), col="red")
    panel.abline(h=0, lty=3)
  }
)

detach(money2)

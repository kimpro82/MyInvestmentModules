## 일간/주간 수익률 - 표준편차 비교

avg = NULL; avg2 = NULL
sd = NULL; sd2 = NULL
g <- c("2-A", "2-B1", "2-B2", "2-C", "3-A")

for (i in 1:5) {
  avg <- c(avg, mean(money[,9][money$Group==g[i]]))
  avg2 <- c(avg2, mean(money2[,6][money2$Group==g[i]]))
  sd <- c(sd, sd(money[,9][money$Group==g[i]]))
  sd2 <- c(sd2, sd(money2[,6][money2$Group==g[i]]))
}

windows(width=9, height=5)
par(mfrow=c(1,2))
plot(avg, sd, names=g, main="일간 수익률 평균-표준편차",
  xlim=c(-0.010,0.010), ylim=c(0,0.100))
  text(x=avg, y=sd, label=g, pos=3, adj=1, cex=1)
plot(avg2, sd2, names=g, main="주간 수익률 평균-표준편차",
  xlim=c(-0.03,0.03), ylim=c(0,0.100))
  text(x=avg2, y=sd2, label=g, pos=3, adj=1, cex=1)

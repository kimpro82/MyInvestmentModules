# R_Monte_Carlo_Simulation_20180328.R
- Suppose a Binomial dist., n=100, p=0.3333
- win -> +100, lose -> -50
- Monte Carlo simulating 1,000 times

```R
m <- 1000; n <- 100; p <- 0.3333
win <- 100; lose <- -50
binom.raw <- matrix(nrow=m, ncol=n)
earn <- matrix(nrow=m, ncol=n)
earn.avg <-c()

for (i in 1:m) {
  binom.raw[i,] <- rbinom(n, 1, p)
  for (j in 1:n ) {
    ifelse(binom.raw[i,j] == 1, earn[i,j] <- win, earn[i,j] <- lose)
  }
  earn.avg[i] <- mean(earn[i,])
}

summary(earn.avg)

windows(width=12, height=7)
par(mfrow=c(1,2)) 
  plot(rank(earn.avg),earn.avg)
    abline(h=mean(earn.avg), col="red")
  hist(earn.avg)
```

![monte_carlo_100](https://github.com/kimpro82/Investment-Monitoring-Modules/blob/master/images/monte_carlo_100.png)

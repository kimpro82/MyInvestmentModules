# Simulation to Compare Arithmetic Mean and Geometrical Mean 2

# 2023.01.24

# Imagine any case to have a geometric mean larger than its arithmetic mean


# Case 1

case1 <- c(seq(1, 1.2, by=0.01), seq(1, 0.8, by=-0.01))
# case1 <- seq(1.2, 0.8, by=-0.01)
plot(case1)
abline(h = 1)

aMean <- mean(case1)
gMean <- exp(mean(log(case1)))

print(paste("Arithmetic mean:", aMean))
print(paste("Geometric mean:", gMean))


# Case 2

case2 <- c(2, 0.5)
aMean <- mean(case2)
gMean <- exp(mean(log(case2)))

print(paste("Arithmetic mean:", aMean))
print(paste("Geometric mean:", gMean))


# Stop!
# Don't you remember this formula?

# (a + b) / 2 ≥ sqrt(ab)
# Don't let your primary school ashamed of you …… !
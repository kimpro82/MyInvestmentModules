# Simulation to Compare Arithmetic Mean and Geometrical Mean

# 2022.12.29

# refer to ChatGPT https://chat.openai.com/chat


# Set the number of simulations
n_simulations <- 1000

# Set the sample size
sample_size <- 240

# Set the distribution of values for the random sample
mean = 1
sd = 0.3

# Initialize vectors to store the results of the simulations
arithmetic_mean1 <- numeric(n_simulations)
arithmetic_mean2 <- numeric(n_simulations)
geometric_mean1 <- numeric(n_simulations)
geometric_mean2 <- numeric(n_simulations)

# Run the simulations
for (i in 1:n_simulations) {
    # Generate a random sample
    sample1 <- rnorm(sample_size, mean = mean, sd = sd)
    sample2 <- rlnorm(sample_size, mean = log(mean), sd = sd)

    # Calculate the arithmetic mean of the sample
    arithmetic_mean1[i] <- mean(sample1)
    arithmetic_mean2[i] <- mean(sample2)

    # Calculate the geometric mean of the sample
    geometric_mean1[i] <- exp(mean(log(sample1)))
    geometric_mean2[i] <- exp(mean(log(sample2)))
}

# Calculate the mean and standard deviation of the arithmetic means
arithmetic_mean_mean1 <- mean(arithmetic_mean1)
arithmetic_mean_mean2 <- mean(arithmetic_mean2)
arithmetic_mean_sd1 <- sd(arithmetic_mean1)
arithmetic_mean_sd2 <- sd(arithmetic_mean2)

# Calculate the mean and standard deviation of the geometric means
geometric_mean_mean1 <- mean(geometric_mean1)
geometric_mean_mean2 <- mean(geometric_mean2)
geometric_mean_sd1 <- sd(geometric_mean1)
geometric_mean_sd2 <- sd(geometric_mean2)

# Print the results
print(paste("Arithmetic mean 1:", arithmetic_mean_mean1, "±", arithmetic_mean_sd1))
print(paste("Geometric mean 1:", geometric_mean_mean1, "±", geometric_mean_sd1))
print(paste("Arithmetic mean 2:", arithmetic_mean_mean2, "±", arithmetic_mean_sd2))
print(paste("Geometric mean 2:", geometric_mean_mean2, "±", geometric_mean_sd2))


# Plot
windows(width = 11, height = 6,
        title = "Arithmetic Mean vs Geometric Mean")                            # title argument does not work
par(mfrow = c(1, 2))
plot(arithmetic_mean1, geometric_mean1,
     # xlim = c(0.99, 1.01), ylim = c(0.99, 1.01),
     col = "red")
abline(h = 1); abline(v = 1)
plot(arithmetic_mean2, geometric_mean2,
     # xlim = c(0.99, 1.01), ylim = c(0.99, 1.01),
     col = "blue")
abline(h = 1); abline(v = 1)
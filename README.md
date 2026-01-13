# Monte Carlo Barrier Option Pricing Simulation

A Monte Carlo simulation for estimating the probability that a financial asset's price will breach a specified barrier level over a given time horizon. This project demonstrates the application of stochastic simulation methods to a real-world problem in quantitative finance.

## Table of Contents

- [Problem Description](#problem-description)
- [Mathematical Formulation](#mathematical-formulation)
- [Monte Carlo Algorithm](#monte-carlo-algorithm)
- [Theoretical Justification](#theoretical-justification)
- [Code Structure](#code-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Output and Visualization](#output-and-visualization)
- [References](#references)

---

## Problem Description

### Background

Barrier options are a class of exotic derivatives whose payoff depends on whether the underlying asset's price reaches a certain barrier level during the option's lifetime. These instruments are widely used in financial markets for hedging and speculation purposes.

The key question we aim to answer is:

> **What is the probability that an asset's price will hit or fall below a specified barrier level at any point during a given time period?**

This probability is critical for:

- **Pricing knock-out and knock-in options** — options that are activated or deactivated when the barrier is breached
- **Risk management** — understanding downside risk and potential loss scenarios
- **Investment decision-making** — assessing the likelihood of adverse price movements

### Problem Relevance

Unlike simple options where closed-form solutions exist (e.g., Black-Scholes), barrier option pricing often requires numerical methods due to the path-dependent nature of the barrier condition. The Monte Carlo method is particularly well-suited for this type of problem because:

1. It can handle complex, path-dependent payoffs
2. It scales well with the number of underlying risk factors
3. It provides probabilistic interpretation and confidence intervals

---

## Mathematical Formulation

### Geometric Brownian Motion Model

We model the asset price $S_t$ using **Geometric Brownian Motion (GBM)**, which is the standard model in quantitative finance. This model assumes that:

- Stock prices move randomly but with an upward or downward trend (drift)
- The randomness is proportional to the current price (percentage changes are random, not absolute changes)
- Price changes follow a log-normal distribution

### Simulation Formula

To simulate price movements, we use the following formula to compute the price at the next time step:

$$S_{t+\Delta t} = S_t \cdot \exp\left[\left(\mu - \frac{\sigma^2}{2}\right)\Delta t + \sigma \sqrt{\Delta t} \cdot Z\right]$$

Where $Z \sim \mathcal{N}(0, 1)$ is a standard normal random variable.

### Quantity of Interest

We define the barrier-breach indicator for a single path $i$:

$$X_i = \mathbf{1}\lbrace\min_{0 \leq t \leq T} S_t^{(i)} \leq B\rbrace$$

Where:
- $B$ is the barrier level
- $T$ is the time horizon
- $S_t^{(i)}$ is the price path for simulation $i$

The probability we wish to estimate is:

$$P = \mathbb{E}[X_i] = P\left(\min_{0 \leq t \leq T} S_t \leq B\right)$$

---

## Monte Carlo Algorithm

### Algorithm Overview

The Monte Carlo method estimates the probability by:

1. **Simulating** $N$ independent price paths using the GBM model
2. **Evaluating** each path to determine if it breaches the barrier
3. **Averaging** the results to obtain a probability estimate

### Detailed Algorithm

```
INPUT: S₀ (initial price), B (barrier), T (time horizon), 
       μ (drift), σ (volatility), ε (error tolerance), conf (confidence level)

1. Compute required number of simulations N using Hoeffding bound
2. Set steps = T × 252 (trading days per year)
3. Set Δt = T / steps
4. Precompute: drift_term = (μ - σ²/2) × Δt
              shock_term = σ × √Δt

5. FOR each simulation i = 1 to N:
     a. Initialize S[0] = S₀
     b. FOR each time step t = 1 to steps:
          Generate Z ~ N(0, 1)
          S[t] = S[t-1] × exp(drift_term + shock_term × Z)
     c. Xᵢ = 1 if min(S[0], ..., S[steps]) ≤ B, else 0

6. Compute P̂ = (1/N) × Σᵢ Xᵢ

OUTPUT: P̂ (estimated probability)
```

### Implementation Optimizations

The implementation uses vectorized operations via NumPy to simulate all $N$ paths simultaneously, providing significant performance improvements over loop-based approaches.

---

## Theoretical Justification

### Convergence Guarantee

By the **Law of Large Numbers**, the Monte Carlo estimator converges to the true probability as the number of simulations increases:

$$\hat{P}_N = \frac{1}{N}\sum_{i=1}^{N} X_i \xrightarrow{N \to \infty} P$$

In simple terms: the more simulations we run, the closer our estimate gets to the true probability.

### Error Bound via Hoeffding's Inequality

To determine the required number of simulations for a given accuracy, we use **Hoeffding's Inequality**. Since $X_i \in \{0, 1\}$ are bounded random variables:

$$P\left(|\hat{P}_N - P| \geq \varepsilon\right) \leq 2\exp(-2N\varepsilon^2)$$

For a desired confidence level $(1 - \alpha)$, we require:

$$2\exp(-2N\varepsilon^2) \leq \alpha$$

Solving for $N$:

$$N \geq \frac{\ln(2/\alpha)}{2\varepsilon^2}$$

**Example**: For $\varepsilon = 0.01$ (1% error) and 95% confidence ($\alpha = 0.05$):

$$N \geq \frac{\ln(40)}{2 \times 0.0001} = \frac{3.69}{0.0002} \approx 18,445$$

---

## Code Structure

### Main Components

| Function | Description |
|----------|-------------|
| `get_input(prompt, default)` | Helper function for interactive parameter input with default values |
| `run_simulation()` | Main simulation function containing all logic |

### Key Variables

| Variable | Description |
|----------|-------------|
| `S0` | Initial asset price |
| `B` | Barrier level |
| `T` | Time horizon in years |
| `mu` | Expected annual return (drift) |
| `sigma` | Annual volatility |
| `epsilon` | Acceptable error margin |
| `conf` | Confidence level |
| `N` | Number of simulations (computed via Hoeffding) |
| `steps` | Number of time steps (trading days) |
| `prices` | Matrix of simulated price paths |
| `barrier_hits` | Binary array indicating barrier breaches |

### Data Flow

```
User Input → Parameter Setup → Random Number Generation 
    → Price Path Simulation → Barrier Evaluation 
    → Probability Estimation → Visualization
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or download the repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   
   # On Windows:
   .venv\Scripts\activate
   
   # On Linux/Mac:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Running the Simulation

```bash
python simulation.py
```

### Interactive Parameters

The program will prompt for the following inputs (press Enter to use defaults):

| Parameter | Default | Description |
|-----------|---------|-------------|
| Starting price | 100.0 | Initial asset price ($S_0$) |
| Barrier level | 80.0 | Barrier threshold ($B$) |
| Time horizon | 1.0 | Simulation period in years ($T$) |
| Expected return | 0.07 | Annual drift ($\mu$) |
| Volatility | 0.20 | Annual volatility ($\sigma$) |
| Acceptable error | 0.01 | Error tolerance ($\varepsilon$) |
| Confidence level | 0.95 | Confidence level ($1 - \alpha$) |

### Example Session

```
=== Barrier Option Pricing (Monte Carlo) ===

Starting price [100.0]: 
Barrier level [80.0]: 75
Time horizon (years) [1.0]: 0.5
Expected return [0.07]: 
Volatility [0.20]: 0.25
Acceptable error [0.01]: 
Confidence level [0.95]: 

Running 18,445 simulations (needed for 95% confidence)...

Probability of hitting barrier: 0.0823 (8.23%)
```

---

## Output and Visualization

The simulation produces two key visualizations:

### 1. Sample Price Paths

Displays a subset of simulated price trajectories (up to 100 paths) showing:
- Gray lines: Individual price paths
- Red dashed line: Barrier level
- Blue dotted line: Initial price

This visualization helps understand the stochastic nature of price movements and how paths may breach the barrier.

### 2. Convergence Plot

Shows the running average of the barrier-hit probability as simulations accumulate:
- Blue line: Running estimate as a function of simulation count
- Red dashed line: Final probability estimate

This demonstrates the Monte Carlo convergence — the estimate stabilizes as more simulations are added, illustrating the Law of Large Numbers in action.

---

## References

1. **Hull, J.C.** (2018). *Options, Futures, and Other Derivatives* (10th ed.). Pearson. — Comprehensive treatment of derivative pricing including barrier options.

2. **Glasserman, P.** (2003). *Monte Carlo Methods in Financial Engineering*. Springer. — Authoritative reference on Monte Carlo techniques in finance.

3. **Hoeffding, W.** (1963). Probability inequalities for sums of bounded random variables. *Journal of the American Statistical Association*, 58(301), 13-30.

4. **Ross, S.M.** (2014). *Introduction to Probability Models* (11th ed.). Academic Press. — Background on probability theory and stochastic processes.

---

## Author

Prosie Radu-Teodor  
Probability and Statistics Course

---

## License

This project is submitted as part of an academic assignment.

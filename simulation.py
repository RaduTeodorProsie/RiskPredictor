import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-darkgrid')

def get_input(prompt, default):
    val = input(f"{prompt} [{default}]: ")
    return float(val) if val else default

def run_simulation():
    print("\n=== Barrier Option Pricing (Monte Carlo) ===\n")

    # Get parameters from user
    S0 = get_input("Starting price", 100.0)
    B = get_input("Barrier level", 80.0)
    T = get_input("Time horizon (years)", 1.0)
    mu = get_input("Expected return", 0.07)
    sigma = get_input("Volatility", 0.20)

    # Figure out how many simulations we need
    epsilon = get_input("Acceptable error", 0.01)
    conf = get_input("Confidence level", 0.95)

    # Hoeffding's inequality tells us the minimum N for our confidence level
    alpha = 1.0 - conf
    N = int(np.ceil(np.log(2/alpha) / (2 * epsilon**2)))

    print(f"\nRunning {N:,} simulations (needed for {conf*100:.0f}% confidence)...")

    # Simulate daily price movements over the time period
    trading_days = 252
    steps = int(T * trading_days)
    dt = T / steps

    # Pre-calculate these so we're not doing it in the loop
    drift = (mu - 0.5 * sigma**2) * dt
    shock = sigma * np.sqrt(dt)

    # Generate all random numbers at once
    random_shocks = np.random.normal(0, 1, (N, steps))

    # Build price paths
    prices = np.zeros((N, steps + 1))
    prices[:, 0] = S0

    for t in range(1, steps + 1):
        prices[:, t] = prices[:, t-1] * np.exp(drift + shock * random_shocks[:, t-1])

    # Check which paths hit the barrier
    lowest_prices = np.min(prices, axis=1)
    barrier_hits = (lowest_prices <= B).astype(int)

    probability = np.mean(barrier_hits)

    print(f"\nProbability of hitting barrier: {probability:.4f} ({probability*100:.2f}%)\n")

    # Plot results
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    plt.subplots_adjust(hspace=0.4)

    # Show a sample of paths (plotting all N would be messy)
    sample_size = min(100, N)
    ax1.plot(prices[:sample_size, :].T, color='gray', alpha=0.5, lw=0.8)
    ax1.axhline(B, color='red', ls='--', lw=2, label=f'Barrier = {B}')
    ax1.axhline(S0, color='blue', ls=':', label=f'Start = {S0}')
    ax1.set_title(f'Price Paths (showing {sample_size} of {N:,} simulations)')
    ax1.set_ylabel('Price')
    ax1.legend()

    # Show how the estimate converges as we add more simulations
    running_avg = np.cumsum(barrier_hits) / np.arange(1, N + 1)
    ax2.plot(running_avg, color='#0055A4', lw=1.5)
    ax2.axhline(probability, color='red', ls='--', label=f'Final estimate: {probability:.2%}')
    ax2.set_title('Estimate Stability')
    ax2.set_xlabel('Simulations')
    ax2.set_ylabel('Estimated Probability')
    ax2.legend()

    plt.show()

if __name__ == "__main__":
    try:
        run_simulation()
    except KeyboardInterrupt:
        print("\nStopped.")
    except Exception as e:
        print(f"Something went wrong: {e}")
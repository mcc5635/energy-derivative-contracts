import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
import os

# Environment Parameters
n_simulations = 10000  # Number of Monte Carlo simulations
n_days = 30  # Number of days in the season
base_solar_generation = 1000  # Base solar generation in MWh
strike_solar_generation = 970  # Strike value is 97% of the base generation
tick_solar = 50  # Tick Value (USD/MWh)

# Simulate Historical Solar Irradiance Data with Seasonal Pattern
def generate_historical_solar_irradiance(days, base_irradiance=200, amplitude=50, noise_level=20):
    """Generate historical solar irradiance data with seasonal variations"""
    np.random.seed(42)
    x = np.arange(days)
    seasonal_pattern = base_irradiance + amplitude * np.sin(2 * np.pi * x / 365)
    noise = np.random.normal(0, noise_level, days)
    irradiance = seasonal_pattern + noise
    return irradiance

# Generate 5 years of historical solar irradiance data (5 * 365 days)
days = 5 * 365
historical_irradiance = generate_historical_solar_irradiance(days)

# Calculate Mean and Standard Deviation from Historical Data
mean_solar_irradiance = np.mean(historical_irradiance)
sd_solar_irradiance = np.std(historical_irradiance)

# Pricing Engine for Solar Contract
class SolarEnergyDerivative:
    def __init__(self, n_days, base_solar_generation, strike_solar_generation, tick_solar, mean_solar_irradiance, sd_solar_irradiance):
        self.n_days = n_days
        self.base_solar_generation = base_solar_generation
        self.strike_solar_generation = strike_solar_generation
        self.tick_solar = tick_solar
        self.mean_solar_irradiance = mean_solar_irradiance
        self.sd_solar_irradiance = sd_solar_irradiance

    def generate_random_irradiance(self):
        return np.random.normal(self.mean_solar_irradiance, self.sd_solar_irradiance, self.n_days)
  
    def calculate_monthly_solar_generation(self, irradiance):
        solar_generation = irradiance * self.n_days * 0.001  # Conversion to MWh
        return np.sum(solar_generation)
    
    def calculate_payout(self, monthly_solar_generation):
        payout = self.tick_solar * max(self.strike_solar_generation - monthly_solar_generation, 0)
        return payout

    def monte_carlo_simulation(self, n_simulations):
        payouts = []
        irradiance_list = []
        for _ in range(n_simulations):
            irradiance = self.generate_random_irradiance()
            monthly_solar_generation = self.calculate_monthly_solar_generation(irradiance)
            payout = self.calculate_payout(monthly_solar_generation)
            payouts.append(payout)
            irradiance_list.append(np.mean(irradiance))  # Collect mean irradiance for correlation
        return payouts, irradiance_list

    def plot_daily_irradiance(self, irradiance):
        plt.figure(figsize=(12, 6))
        plt.plot(irradiance, color='orange')
        plt.title('Daily Solar Irradiance Over the Season in Texas')
        plt.xlabel('Day')
        plt.ylabel('Solar Irradiance (W/m²)')
        plt.show()
    
    def plot_payout_vs_irradiance(self, irradiance, payouts):
        plt.figure(figsize=(10, 6))
        plt.scatter(irradiance, payouts, alpha=0.5, color='orange')
        plt.title('Solar Irradiance vs. Contract Payout in Texas')
        plt.xlabel('Solar Irradiance (W/m²)')
        plt.ylabel('Payout (USD)')
        plt.show()

def generate_solar_irradiance_data(days, mean_solar_irradiance, sd_solar_irradiance):
    np.random.seed(42)
    daily_irradiance = np.random.normal(mean_solar_irradiance, sd_solar_irradiance, days)
    for i in range(0, days, 10):
        daily_irradiance[i] *= np.random.uniform(0.7, 1.3)
    return daily_irradiance

def calculate_solar_payouts(solar_irradiance_data, strike_solar_generation, tick_solar):
    payouts = []
    for i in range(len(solar_irradiance_data)):
        monthly_solar_generation = solar_irradiance_data[i] * 0.001 * n_days  # Convert to MWh
        payout = tick_solar * max(strike_solar_generation - monthly_solar_generation, 0)
        payouts.append(payout)
    return payouts

def plot_solar_payout_distribution(payouts):
    mean_payout = np.mean(payouts)
    std_payout = np.std(payouts)

    plt.figure(figsize=(10, 6))
    plt.hist(payouts, bins=30, alpha=0.7, color='orange', edgecolor='black', density=True)

    title = f"Distribution of Texas Solar Contract Payouts\nMean = {mean_payout:.4f}, Std Dev = {std_payout:.4f}"
    plt.title(title)
    plt.xlabel('Contract Payout (USD)')
    plt.ylabel('Frequency Density')
    plt.show()

    print(f"Total number of payouts: {len(payouts)}")
    print(f"Mean payout: {mean_payout:.4f}")
    print(f"Standard deviation of payouts: {std_payout:.4f}")
    print(f"Min payout: {min(payouts):.4f}")
    print(f"Max payout: {max(payouts):.4f}")

# SolarEnergyDerivative Class Instance
solar_contract = SolarEnergyDerivative(n_days, base_solar_generation, strike_solar_generation, tick_solar, mean_solar_irradiance, sd_solar_irradiance)

# Generate random solar irradiance for one simulation and plot them
irradiance = solar_contract.generate_random_irradiance()
solar_contract.plot_daily_irradiance(irradiance)

# Monte Carlo Simulation Results for Solar Contract
payouts, mean_irradiance = solar_contract.monte_carlo_simulation(n_simulations)
print(f'Payout Summary for Solar Contract:\n{np.percentile(payouts, [0, 25, 50, 75, 100])}')
print(payouts)

# Instance Run With Sample Data for Solar Contract
days = 1825  # 5 years of data
solar_irradiance_data = generate_solar_irradiance_data(days, mean_solar_irradiance, sd_solar_irradiance)
solar_payouts = calculate_solar_payouts(solar_irradiance_data, strike_solar_generation, tick_solar)
plot_solar_payout_distribution(solar_payouts)

# Calculate solar irradiance vs. contract payouts for Solar Contract
solar_irradiance_consumption = generate_solar_irradiance_data(n_days, mean_solar_irradiance, sd_solar_irradiance)
solar_payouts = calculate_solar_payouts(solar_irradiance_consumption, strike_solar_generation, tick_solar)
solar_contract.plot_payout_vs_irradiance(solar_irradiance_consumption[:len(solar_payouts)], solar_payouts)
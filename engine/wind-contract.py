import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
import os

# Environment Parameters
n_simulations = 10000  # Number of Monte Carlo simulations
n_days = 30  # Number of days in the season

# Wind Contract Parameters for Germany
base_wind_speed = 5  # Base wind speed in m/s
strike_wind_speed = 3  # Strike wind speed in m/s
mean_wind_speed = 6  # Mean daily wind speed in m/s
sd_wind_speed = 2  # Standard deviation of daily wind speeds
tick_wind = 1000  # Tick Value (EUR/m/s)

# Pricing Engine for Wind Contract
class WindEnergyDerivative:
    def __init__(self, n_days, base_wind_speed, strike_wind_speed, tick_wind, mean_wind_speed, sd_wind_speed):
        self.n_days = n_days
        self.base_wind_speed = base_wind_speed
        self.strike_wind_speed = strike_wind_speed
        self.tick_wind = tick_wind
        self.mean_wind_speed = mean_wind_speed
        self.sd_wind_speed = sd_wind_speed

    def generate_random_wind_speeds(self):
        return np.random.normal(self.mean_wind_speed, self.sd_wind_speed, self.n_days)
  
    def calculate_seasonal_wind_speed_avg(self, wind_speeds):
        return np.mean(wind_speeds)
    
    def calculate_payout(self, seasonal_wind_speed_avg):
        payout = self.tick_wind * max(self.strike_wind_speed - seasonal_wind_speed_avg, 0)
        return payout

    def monte_carlo_simulation(self, n_simulations):
        payouts = []
        wind_speeds_list = []
        for _ in range(n_simulations):
          wind_speeds = self.generate_random_wind_speeds()
          seasonal_wind_speed_avg = self.calculate_seasonal_wind_speed_avg(wind_speeds)
          payout = self.calculate_payout(seasonal_wind_speed_avg)
          payouts.append(payout)
          wind_speeds_list.append(np.mean(wind_speeds))  # Collect mean wind speed for correlation
        return payouts, wind_speeds_list
    
    def plot_daily_wind_speeds(self, wind_speeds):
        plt.figure(figsize=(12, 6))
        plt.plot(wind_speeds, color='green')
        plt.title('Daily Wind Speeds Over the Season in Germany')
        plt.xlabel('Day')
        plt.ylabel('Wind Speed (m/s)')
        plt.show()
    
    def plot_payout_vs_wind_speed(self, wind_speeds, payouts):
        plt.figure(figsize=(10, 6))
        plt.scatter(wind_speeds, payouts, alpha=0.5, color='green')
        plt.title('Wind Speed vs. Contract Payout in Germany')
        plt.xlabel('Wind Speed (m/s)')
        plt.ylabel('Payout (EUR)')
        plt.show()

def generate_wind_speed_data(days, mean_wind_speed, sd_wind_speed):
    np.random.seed(42)
    daily_wind_speed = np.random.normal(mean_wind_speed, sd_wind_speed, days)
    for i in range(0, days, 10):
        daily_wind_speed[i] *= np.random.uniform(0.7, 1.3)
    return daily_wind_speed

def calculate_wind_payouts(wind_speed_data, strike_wind_speed, tick_wind):
    payouts = []
    for i in range(len(wind_speed_data)):
        payout = tick_wind * max(strike_wind_speed - wind_speed_data[i], 0)
        payouts.append(payout)
    return payouts

def plot_wind_payout_distribution(payouts):
    mean_payout = np.mean(payouts)
    std_payout = np.std(payouts)

    plt.figure(figsize=(10, 6))
    plt.hist(payouts, bins=30, alpha=0.7, color='green', edgecolor='black', density=True)

    title = f"Distribution of German Wind Contract Payouts\nMean = {mean_payout:.4f}, Std Dev = {std_payout:.4f}"
    plt.title(title)
    plt.xlabel('Contract Payout (EUR)')
    plt.ylabel('Frequency Density')
    plt.show()

    print(f"Total number of payouts: {len(payouts)}")
    print(f"Mean payout: {mean_payout:.4f}")
    print(f"Standard deviation of payouts: {std_payout:.4f}")
    print(f"Min payout: {min(payouts):.4f}")
    print(f"Max payout: {max(payouts):.4f}")

# WindEnergyDerivative Class Instance
wind_contract = WindEnergyDerivative(n_days, base_wind_speed, strike_wind_speed, tick_wind, mean_wind_speed, sd_wind_speed)

# Generate random wind speeds for one simulation and plot them
wind_speeds = wind_contract.generate_random_wind_speeds()
wind_contract.plot_daily_wind_speeds(wind_speeds)

# Monte Carlo Simulation Results for Wind Contract
payouts, mean_wind_speeds = wind_contract.monte_carlo_simulation(n_simulations)
print(f'Payout Summary for Wind Contract:\n{np.percentile(payouts, [0, 25, 50, 75, 100])}')
print(payouts)

# Instance Run With Sample Data for Wind Contract
days = 1825  # 5 years of data
wind_speed_data = generate_wind_speed_data(days, mean_wind_speed, sd_wind_speed)
wind_payouts = calculate_wind_payouts(wind_speed_data, strike_wind_speed, tick_wind)
plot_wind_payout_distribution(wind_payouts)

# Calculate wind speed vs. contract payouts for Wind Contract
wind_speed_consumption = generate_wind_speed_data(n_days, mean_wind_speed, sd_wind_speed)
wind_payouts = calculate_wind_payouts(wind_speed_consumption, strike_wind_speed, tick_wind)
wind_contract.plot_payout_vs_wind_speed(wind_speed_consumption[:len(wind_payouts)], wind_payouts)

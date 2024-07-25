import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
import os

# Environment Parameters
n_simulations = 10000  # Number of Monte Carlo simulations
n_days = 30  # Number of days in the season
base_temperature = 18  # Base temperature in Celsius for HDD calculation
strike_price = 1000  # Strike Value (HDD Accumulation)
tick = 500  # Tick Value (USD/HDD)
mean_temp = 10  # Mean daily temperature
sd_temp = 5  # Standard deviation of daily temperatures

# Japan Energy Grid Parameters
mean_energy = 100  # Arbitrary avg energy consumption in GWh
std_energy = 10  # Standard deviation of daily consumption
change_threshold = 0.10  # 10% change threshold for contract payouts

# Pricing Engine
class ThermalEnergyDerivative:
    def __init__(self, n_days, base_temperature, strike_price, tick, mean_temp, sd_temp):
        self.n_days = n_days
        self.base_temperature = base_temperature
        self.strike_price = strike_price
        self.tick = tick
        self.mean_temp = mean_temp
        self.sd_temp = sd_temp

    def generate_random_temperatures(self):
        return np.random.normal(self.mean_temp, self.sd_temp, self.n_days)
  
    def calculate_seasonal_hdd(self, temperatures):
        hdd = np.maximum(0, self.base_temperature - temperatures)
        return np.sum(hdd)
    
    def calculate_payout(self, seasonal_hdd):
        payout = self.tick * max(seasonal_hdd - self.strike_price, 0)
        return payout

    def monte_carlo_simulation(self, n_simulations):
        payouts = []
        temperatures_list = []
        for _ in range(n_simulations):
          temperatures = self.generate_random_temperatures()
          seasonal_hdd = self.calculate_seasonal_hdd(temperatures)
          payout = self.calculate_payout(seasonal_hdd)
          payouts.append(payout)
          temperatures_list.append(np.mean(temperatures))  # Collect mean temperature for correlation
        return payouts, temperatures_list
    
    def plot_daily_temperatures(self, temperatures):
        plt.figure(figsize=(12, 6))
        plt.plot(temperatures, color='blue')
        plt.title('Daily Temperatures Over the Season')
        plt.xlabel('Day')
        plt.ylabel('Temperature (°C)')
        plt.show()
    
    def plot_payout_vs_energy(self, energy_consumption, payouts):
        plt.figure(figsize=(10, 6))
        plt.scatter(energy_consumption, payouts, alpha=0.5, color='blue')
        plt.title('Energy Consumption vs. Contract Payout')
        plt.xlabel('Energy Consumption (GWh)')
        plt.ylabel('Payout (JPY)')
        plt.show()

def generate_energy_data(days, mean_energy, std_energy):
    np.random.seed(42)
    daily_consumption = np.random.normal(mean_energy, std_energy, days)
    for i in range(0, days, 10):
        daily_consumption[i] *= np.random.uniform(0.7,1.3)
    return daily_consumption

def calculate_energy_payouts(energy_data, change_threshold):
    payouts = []
    for i in range(1, len(energy_data)):
        change = (energy_data[i] - energy_data[i-1]) / energy_data[i-1]
        if abs(change) > change_threshold:
            payouts.append(change - change_threshold)
    return payouts

def plot_energy_payout_distribution(payouts):
    mean_payout = np.mean(payouts)
    std_payout = np.std(payouts)

    plt.figure(figsize=(10, 6))
    plt.hist(payouts, bins=30, alpha=0.7, color='blue', edgecolor='black', density=True)

    title = f"Distribution of Japanese Energy Contract Payouts\nMean = {mean_payout:.4f}, Std Dev = {std_payout:.4f}"
    plt.title(title)
    plt.xlabel('Contract Payout (JPY)')
    plt.ylabel('Frequency Density')
    plt.show()

    print(f"Total number of payouts: {len(payouts)}")
    print(f"Mean payout: {mean_payout:.4f}")
    print(f"Standard deviation of payouts: {std_payout:.4f}")
    print(f"Min payout: {min(payouts):.4f}")
    print(f"Max payout: {max(payouts):.4f}")

# ThermalEnergyDerivative Class Instance
thermal_contract = ThermalEnergyDerivative(n_days, base_temperature, strike_price, tick, mean_temp, sd_temp)

# Generate random temperatures for one simulation and plot them
temperatures = thermal_contract.generate_random_temperatures()
thermal_contract.plot_daily_temperatures(temperatures)

# Monte Carlo Simulation Results
payouts, mean_temperatures = thermal_contract.monte_carlo_simulation(n_simulations)
print(f'Payout Summary:\n{np.percentile(payouts, [0, 25, 50, 75, 100])}')
print(payouts)

# Instance Run With Sample Data
days = 1825 # 5 years of data
energy_data = generate_energy_data(days, mean_energy, std_energy)
energy_payouts = calculate_energy_payouts(energy_data, change_threshold)
plot_energy_payout_distribution(energy_payouts)

# Calculate energy consumption vs. contract payouts
energy_consumption = generate_energy_data(n_days, mean_energy, std_energy)
energy_payouts = calculate_energy_payouts(energy_consumption, change_threshold)
thermal_contract.plot_payout_vs_energy(energy_consumption[:len(energy_payouts)], energy_payouts)

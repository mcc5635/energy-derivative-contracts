# Energy Derivative Contracts

This repository contains information about various energy derivative contracts used in energy trading. The contracts cover different types of energy sources and are designed to hedge against specific risks associated with these sources. Below is an overview of the contract types, their structure, and payout mechanisms.

## Table of Contents

- [Contract Types](#contract-types)
- [Counterparties](#counterparties)
- [Concerns](#concerns)
- [Energy Types](#energy-types)
- [Data Sources](#data-sources)
- [Locations](#locations)
- [Contract Structures](#contract-structures)
- [Payout Mechanisms](#payout-mechanisms)
- [Tick Definitions](#tick-definitions)

## Contract Types

### Thermal
- **Concern**: High Power Demand
- **Energy Type**: Temperature
- **Data Source**: GHCN-D Laguardia Airport
- **Location**: New York
- **Structure**: A call option that pays when seasonal Heating Degree Days (HDD) accumulation exceeds a certain strike value.
- **Payout**: Tick * mass(Seasonal HDD Accumulation - Strike, 0)
- **Tick**: A defined USD/HDD Tick that correlates well to increased power costs.

### Wind
- **Concern**: Lower Wind Generation
- **Energy Type**: Wind
- **Data Source**: Transformed ERA5 Wind
- **Location**: Germany
- **Structure**: A put option that pays when monthly accumulated wind generation falls below a certain strike value.
- **Payout**: Tick * mass(Strike - Wind Generation, 0)
- **Tick**: A defined EUR/MWh Tick that correlates well to reduced wind power generation.

### Solar
- **Concern**: Cloudier Than Average
- **Energy Type**: Solar
- **Data Source**: ERA5 Solar Irradiance
- **Location**: Texas
- **Structure**: A put option that pays when the monthly solar generation falls below a certain strike value.
- **Payout**: Tick * mass(Strike - Solar Generation, 0)
- **Tick**: Defined by a predetermined $/MWh tick that is inversely related to solar irradiance.

## Counterparties

- **Energy Trading Desk**
- **Private Equity**

## Concerns

- High Power Demand
- Lower Wind Generation
- Cloudier Than Average

## Energy Types

- Temperature
- Wind
- Solar

## Data Sources

- GHCN-D Laguardia Airport
- Transformed ERA5 Wind
- ERA5 Solar Irradiance

## Locations

- New York
- Germany
- Texas

## Contract Structures

Each contract structure is designed to hedge against specific risks associated with different energy sources. The structure defines the type of option (call or put) and the conditions under which the payout is triggered.

## Payout Mechanisms

The payout mechanism defines how the payout is calculated based on the difference between actual and strike values of the concerned energy metrics. The formula typically involves a tick multiplier and a mass function to ensure payouts are only made when beneficial to the contract holder.

## Tick Definitions

Ticks are predefined monetary values per unit of energy metric (e.g., USD/HDD, EUR/MWh) that correlate with the costs or benefits associated with the changes in the energy metrics.

---

For more detailed information, please refer to the data provided in the `../data/derivative-contracts.csv` file.

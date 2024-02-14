# RocketInsight Backend Service

## Overview

This README outlines the backend service for RocketInsight, a Flask-based API designed to facilitate real-time and historical market data analysis for the RocketPool ecosystem, specifically focusing on the rETH liquid staking token. The backend service provides a series of endpoints that return valuable market insights, including systemic leverage, historical supply and borrow rates, transaction lists, and user interaction histories with lending and borrowing markets.

## API Endpoints

The backend service exposes the following RESTful API endpoints:

1. **/all_markets**

   - Returns a dictionary of market strings, URLs for landing pages, and other relevant market information.

2. **/historical_leverage**

   - Returns time-stamped systemic leverage data.
   - Optional Parameters:
     - Markets: Defaults to mainnet Aave v3.
     - Timeframe: Defaults to the past 1 year.

3. **/historical_supply**

   - Returns historical supply amounts to the protocol.
   - Optional Parameters:
     - Markets, Timeframe, Token: Defaults to mainnet Aave v3, past 1 year, and rETH respectively.

4. **/historical_borrow**

   - Returns historical borrow amounts from the protocol.
   - Optional Parameters: Similar to `/historical_supply`.

5. **/supply_transactions**

   - Lists transactions of supplying rETH to markets.
   - Optional Parameters: Markets (defaults to Aave v3), Timeframe (defaults to past 1 year).

6. **/borrow_transactions**

   - Lists transactions of borrowing rETH.
   - Optional Parameters: Similar to `/supply_transactions`.

7. **/leveraged_users**

   - Lists users contributing to rETH systemic leverage.
   - Optional Parameters:
     - AUM_threshold: Defaults to 25 rETH.
     - Markets: Defaults to mainnet Aave v3.

8. **/user_history**
   - Returns the interaction history of a user with lending and borrowing markets, starting with the initial deposit of rETH.
   - Required Parameters: User address(es), Market(s).

# Installation instructions

## Install Miniconda3

### MacOS and Linux/WSL

- Download Miniconda3 from the [official website](https://docs.conda.io/en/latest/miniconda.html).
- Open Terminal, navigate to the download directory, and run the installer:

  ```bash
  bash Miniconda3-latest-MacOSX-x86_64.sh # MacOS
  bash Miniconda3-latest-Linux-x86_64.sh # Linux
  ```

- Follow the installation prompts

```bash
pip install -r requirements.txt
```

### Windows

- Download the Windows Miniconda installer from the [https://docs.anaconda.com/free/miniconda/miniconda-other-installer-links/](official website) and run it.
- Follow the on-screen instructions.

## Set Up Environment

- Open Anaconda Prompt from the Start Menu.
- Create and activate a new conda environment:

```bash
conda create --name rocketinsight python=3.8
conda activate rocketinsight
```

## Install Dependencies

Install the necessary libraries using pip:

```bash
pip install -r requirements.txt
```

## Contribution

We welcome contributions from the community to improve and extend the functionality of the RocketInsight backend service. Please adhere to our contribution guidelines outlined in CONTRIBUTING.md.

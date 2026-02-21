# Music Prediction Marketplace Simulation

A fully simulated music marketplace where pre-released songs are listed, users create prediction contracts with custom stream targets and evaluation periods, the platform takes a 20% trading fee, an anti-cheat system prevents bot purchases, and a "Future of Records" committee resolves disputes in 2 days.

## What This Simulates

**Concept:** Creators submit pre-released songs. Any user can create a prediction contract specifying a stream target (e.g., 1M streams) and evaluation period (e.g., 30 days). Traders buy YES/NO shares. The platform collects a 20% fee on every trade. Anti-cheat mechanisms detect bot stream purchases and insider trading. Disputed contracts are settled by the "Future of Records" committee within 2 days.

**Key Questions:**
1. Can a 20% fee marketplace sustain healthy trading economics?
2. How effective are anti-cheat mechanisms at catching bot stream purchases?
3. Does the 2-day committee dispute resolution work fairly?
4. What happens when creators try to game their own songs' markets?

## Quick Start

```bash
# Setup
pip install -r requirements.txt

# Run default simulation (200 songs, 100 traders, 20% fee)
python3 src/simulation.py

# Custom simulation
python3 src/simulation.py --songs 500 --traders 200 --gaming-rate 0.3 --bot-detection 0.9

# Reproducible run
python3 src/simulation.py --seed 42
```

## Project Structure

```
songs-prediction-market-simulation/
├── README.md
├── requirements.txt
├── src/
│   ├── simulation.py       # Main simulation runner & CLI
│   ├── models.py           # Core data models (User, Song, Contract, Trade, Dispute)
│   ├── trading.py          # Trading engine with 20% fee & AMM
│   ├── anti_cheat.py       # Bot detection, creator restrictions, sybil detection
│   ├── dispute.py          # "Future of Records" committee dispute resolution
│   ├── agents.py           # Bettor agent behaviors (noise, informed, whale, arb)
│   ├── market.py           # Legacy AMM implementation
│   └── gaming.py           # Legacy gaming attack models
└── docs/
    ├── METHODOLOGY.md
    └── PARAMETERS.md
```

## Core Features

### 1. User-Configurable Prediction Contracts

Users set their own parameters when creating contracts:

| Parameter | Options | Description |
|-----------|---------|-------------|
| Target Streams | 100K, 250K, 500K, 1M, 2M, 5M, 10M | Streams needed to resolve YES |
| Evaluation Period | 7, 14, 30, 60, 90 days | Window to reach the target |

### 2. 20% Platform Trading Fee

Every trade is charged a 20% fee, distributed as:

| Recipient | Share | Purpose |
|-----------|-------|---------|
| Platform Revenue | 50% | Operating costs |
| Liquidity Pool | 30% | Market depth reserves |
| Dispute Fund | 20% | Committee compensation & refunds |

### 3. Anti-Cheat System

Prevents song creators from gaming with bot purchases:

- **Bot Stream Detection**: Analyzes geographic patterns, temporal anomalies, repeat listener ratios, device diversity, and stream velocity spikes
- **Creator Self-Trading Ban**: Creators cannot trade on their own songs' contracts
- **Associated Account Detection**: Linked wallets/IPs are flagged and restricted
- **Cooling-Off Period**: 24-hour wait after song submission before any trading opens
- **Stream Audit**: Contracts voided if >30% of streams are artificial
- **Sybil Detection**: Coordinated trading patterns and wash trading flagged

### 4. Dispute Resolution ("Future of Records" Committee)

A 3-7 member committee settles disputed contracts in 2 days:

| Day | Phase | Activity |
|-----|-------|----------|
| 0 | Filing | Dispute filed, payouts frozen, 5% deposit required |
| 0-0.5 | Evidence | Evidence collection from all parties |
| 0.5-1.5 | Review | Committee reviews and votes (majority rules) |
| 2.0 | Resolution | Decision published, funds distributed |

**Dispute Types:**
- Stream Manipulation (bot streams)
- Insider Trading (creator traded own song)
- False Reporting (incorrect stream counts)
- Market Manipulation (wash trading)

**Outcomes:**
- **Upheld**: Original resolution stands, disputer loses 5% deposit
- **Overturned**: Market voided, traders refunded
- **Partial**: Partial refund, manipulated portion removed
- **Penalty**: Creator banned, funds redistributed to honest traders

### 5. Agent Types

| Agent | Behavior | % of Bettors |
|-------|----------|--------------|
| Noise | Random YES/NO | 60% |
| Informed | Knows true probability ±10% | 20% |
| Whale | Large bets, slight edge | 10% |
| Arbitrageur | Corrects mispricing | 10% |

## CLI Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--songs` | 200 | Number of songs to simulate |
| `--traders` | 100 | Number of traders |
| `--creators` | 20 | Number of creators |
| `--gaming-rate` | 0.2 | Fraction of gaming attempts |
| `--bot-detection` | 0.75 | Bot stream detection rate |
| `--platform-fee` | 0.20 | Trading fee (20%) |
| `--dispute-rate` | 0.15 | Dispute filing rate |
| `--committee-size` | 5 | Committee members |
| `--daily-bettors` | 30 | Avg daily bettors per contract |
| `--seed` | None | Random seed for reproducibility |
| `--output` | marketplace_results | Output file prefix |

## Output

The simulation produces:

1. **Console report** with marketplace economics, anti-cheat stats, dispute outcomes
2. **CSV file** with per-contract detailed results
3. **JSON file** with structured aggregate analysis

Example output:
```
======================================================================
  MUSIC PREDICTION MARKETPLACE - SIMULATION RESULTS
======================================================================

--- Economics (20% Platform Fee) ---
  Total trading volume: $707,328
  Total fees collected: $141,466
  Platform revenue (50%): $70,733
  Dispute fund (20%):    $28,293

--- Anti-Cheat Effectiveness ---
  Gaming detection rate: 50.0%
  False positive rate: 0.0%
  Contracts voided: 33

--- Dispute Resolution (2-Day Timeline) ---
  Committee: 'Future of Records' (5 members)
  Total disputes filed: 11
  Committee accuracy: 85.5%
```

## License

MIT

## Contact

Built for [Future of Records](https://futureofrecords.com) — prediction markets for music.

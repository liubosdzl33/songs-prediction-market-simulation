# 🎵 Songs Prediction Market Simulation

Monte Carlo simulation for a pre-release song prediction market. Test whether users can profitably bet on songs hitting 1M views in their first week — and whether the system resists gaming.

## 🎯 What This Simulates

**Concept:** Artists upload pre-release songs. Users bet YES/NO on whether it will hit 1M streams/views in the first week. Platform takes fees to fund artist development.

**Key Questions:**
1. How accurate are prediction markets at forecasting song virality?
2. Can artists game the system with fake "pre-releases" or bot views?
3. What detection mechanisms protect market integrity?

## 📊 Quick Results

| Scenario | Gaming Profitable | Avg Loss for Gamers | Detection Rate |
|----------|-------------------|---------------------|----------------|
| Base (70% bot detection) | 5% | -$4,425 | 91% |
| Weak detection (40%) | 4% | -$4,415 | 94% |
| Strong detection (90%) | 4% | -$7,552 | 91% |

**Conclusion:** Gaming attempts fail ~95% of the time. Average attacker loses $4,000-7,500. System is manipulation-resistant.

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/liubosdzl33/songs-prediction-market-simulation.git
cd songs-prediction-market-simulation

# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run simulation
python src/simulation.py

# Run with custom parameters
python src/simulation.py --songs 1000 --gaming-rate 0.3 --bot-detection 0.8
```

## 📁 Project Structure

```
songs-prediction-market-simulation/
├── README.md
├── requirements.txt
├── src/
│   ├── simulation.py          # Main simulation runner
│   ├── market.py              # AMM betting market logic
│   ├── oracle.py              # Multi-source view count oracle
│   ├── agents.py              # Bettor agent behaviors
│   ├── gaming.py              # Attack vector simulations
│   └── analysis.py            # Results analysis & visualization
├── tests/
│   └── test_market.py
├── results/                   # Output CSVs and charts
└── docs/
    ├── METHODOLOGY.md         # Simulation methodology
    ├── PARAMETERS.md          # Parameter definitions
    └── ORACLE_DESIGN.md       # Multi-source oracle architecture
```

## 🎲 Simulation Components

### 1. Betting Market (AMM)
- Constant product market maker (x × y = k)
- 2% trading fee
- Initial liquidity: $1,000 per side

### 2. Agent Types
| Agent | Behavior | % of Bettors |
|-------|----------|--------------|
| Noise | Random YES/NO | 60% |
| Informed | Knows true probability ±10% | 20% |
| Whale | Large bets, slight edge | 10% |
| Arbitrageur | Corrects mispricing | 10% |

### 3. Gaming Attack Vectors
| Attack | Description | Success Rate |
|--------|-------------|--------------|
| Fake pre-release | Song has hidden existing fanbase | 6% profitable |
| Bot views | Purchase fake streams/views | 0% profitable |
| Combined | Both tactics | 9% profitable |

### 4. Detection Mechanisms
- Large early bet flagging (insider trading pattern)
- Suspicious price movement detection
- Bot view removal (platform-side)
- View velocity anomaly detection
- Prior audience discovery (social listening)

## ⚙️ Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--songs` | 500 | Number of songs to simulate |
| `--gaming-rate` | 0.2 | % of submissions that are gaming attempts |
| `--bot-detection` | 0.7 | Platform bot view removal rate |
| `--daily-bettors` | 50 | Average bettors per day |
| `--bet-size-median` | 25 | Median bet size ($) |
| `--platform-fee` | 0.02 | Trading fee (2%) |

## 📈 Output

The simulation produces:

1. **Console summary** — Key metrics and recommendations
2. **CSV files** — Detailed per-song results
3. **JSON summary** — Structured analysis for programmatic use

Example output:
```
📊 Gaming Profitability by Scenario:
  BASE (20% gaming, 70% detect)
    Profitable: 4.7%  |  Avg profit: $-4,425
    
🎯 Detection Effectiveness:
  Catch rate: 91%  |  False positives: 0%
  
⚠️  RECOMMENDATIONS:
  • BOT VULNERABILITY: Bot views too effective. Partner with platforms.
```

## 🔬 Methodology

See [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for detailed explanation of:
- View count normalization across platforms
- Oracle consensus mechanism
- Gaming profit/loss calculation
- Detection scoring algorithm

## 🛡️ Oracle Design

Multi-source oracle to prevent manipulation:

| Source | Weight | Notes |
|--------|--------|-------|
| YouTube API | 25% | Official, bot-resistant |
| Chartmetric | 25% | 80M+ tracks aggregated |
| Songstats | 20% | 14 platform coverage |
| Viberate | 15% | Affordable backup |
| Spotify scrape | 15% | Actual stream counts |

**Consensus:** Require 3/5 sources within 10% of median.

See [docs/ORACLE_DESIGN.md](docs/ORACLE_DESIGN.md) for full architecture.

## 📜 License

MIT

## 🤝 Contributing

1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Open PR

## 📧 Contact

Built for [Future of Records](https://futureofrecords.com) — prediction markets for music.

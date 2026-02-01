# Parameter Reference

## Simulation Parameters

### Scale

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `n_songs` | 500 | 100-10000 | Songs per simulation run |
| `gaming_rate` | 0.2 | 0-1 | Fraction that are gaming attempts |

### Market

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `initial_liquidity` | 1000 | 100-10000 | Starting pool per side (USD) |
| `platform_fee` | 0.02 | 0.01-0.05 | Fee on each bet (2%) |
| `betting_days` | 7 | 3-14 | Days market is open |

### Agents

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `daily_bettors_mean` | 50 | 10-200 | Average bettors per day (Poisson λ) |
| `bet_size_median` | 25 | 10-100 | Median bet size USD (log-normal) |
| `bet_size_sigma` | 1.2 | 0.5-2.0 | Bet size distribution spread |

### Agent Mix

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `noise_pct` | 0.60 | 0-1 | Random bettors |
| `informed_pct` | 0.20 | 0-1 | Informed traders |
| `whale_pct` | 0.10 | 0-1 | Large bettors |
| `arb_pct` | 0.10 | 0-1 | Arbitrageurs |

### Detection

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `bot_detection_rate` | 0.7 | 0.3-0.95 | Platform bot view removal rate |
| `bot_cost_per_1000` | 2.0 | 1-5 | USD cost per 1000 fake views |

### Fee Distribution

| Parameter | Default | Description |
|-----------|---------|-------------|
| `artist_fee_share` | 0.40 | To artist development fund |
| `promotion_fee_share` | 0.30 | To promotion pool |
| `platform_fee_share` | 0.20 | Platform revenue |
| `insurance_fee_share` | 0.10 | Insurance/dispute fund |

## Gaming Parameters

### Fake Pre-release Attack

| Parameter | Distribution | Description |
|-----------|--------------|-------------|
| `true_organic_prob` | U(0.4, 0.8) | Higher due to existing audience |
| `underground_following` | U(0.3, 0.7) | Hidden fanbase strength |
| `artist_insider_bet` | U(500, 5000) | Insider bet amount |
| `bot_budget` | 0 | No bot views |

### Bot Views Attack

| Parameter | Distribution | Description |
|-----------|--------------|-------------|
| `true_organic_prob` | U(0.05, 0.2) | Low organic chance |
| `underground_following` | 0 | No existing audience |
| `artist_insider_bet` | U(200, 2000) | Smaller insider bet |
| `bot_budget` | U(1000, 10000) | Bot view budget |

### Combined Attack

| Parameter | Distribution | Description |
|-----------|--------------|-------------|
| `true_organic_prob` | U(0.3, 0.6) | Moderate organic |
| `underground_following` | U(0.2, 0.5) | Some hidden audience |
| `artist_insider_bet` | U(1000, 10000) | Large insider bet |
| `bot_budget` | U(2000, 15000) | Significant bot budget |

## Detection Thresholds

| Flag | Threshold | Score Impact |
|------|-----------|--------------|
| Large early bet | > $1,000 | +0.30 |
| Price movement | > 15% in day 1 | +0.20 |
| Bot views | > 10,000 removed | +0.40 |
| Velocity anomaly | bot > 50% organic | +0.30 |
| Prior audience | following > 0.4 | +0.25 |

**Action thresholds:**
- Void: score ≥ 0.70
- Review: score ≥ 0.50
- Pass: score < 0.50

## Tuning Recommendations

### For Higher Security
```python
config = SimulationConfig(
    bot_detection_rate=0.9,
    platform_fee=0.03,
)
```

### For Higher Volume
```python
config = SimulationConfig(
    initial_liquidity=5000,
    platform_fee=0.015,
    daily_bettors_mean=100,
)
```

### For Stress Testing
```python
config = SimulationConfig(
    gaming_rate=0.4,
    bot_detection_rate=0.4,
)
```

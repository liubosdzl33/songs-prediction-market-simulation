# Simulation Methodology

## Overview

This simulation uses Monte Carlo methods to model a prediction market for pre-release songs. We simulate thousands of market instances with varying parameters to understand:

1. Market accuracy at predicting song virality
2. Vulnerability to gaming/manipulation
3. Effectiveness of detection mechanisms

## Components

### 1. Song Generation

Each simulation run generates a pool of songs with:

**Legitimate Songs (default 80%):**
- `true_organic_probability`: Uniform(0.05, 0.5) — base chance of hitting 1M views organically
- No underground following, insider bets, or bot budget

**Gaming Attempts (default 20%):**

Three attack types, equally distributed:

| Type | Organic Prob | Underground Following | Insider Bet | Bot Budget |
|------|--------------|----------------------|-------------|------------|
| Fake Pre-release | U(0.4, 0.8) | U(0.3, 0.7) | U($500, $5k) | $0 |
| Bot Views Only | U(0.05, 0.2) | 0 | U($200, $2k) | U($1k, $10k) |
| Combined | U(0.3, 0.6) | U(0.2, 0.5) | U($1k, $10k) | U($2k, $15k) |

### 2. Betting Market (AMM)

**Constant Product Market Maker:**
```
YES_pool × NO_pool = k (constant)

Price of YES = YES_pool / (YES_pool + NO_pool)
```

When a user bets:
1. 2% fee deducted
2. Net amount added to chosen pool
3. Shares = bet_amount / current_price

**Initial State:**
- $1,000 in each pool (YES and NO)
- Starting price: 0.5 (50/50 odds)

### 3. Agent Behavior

Four agent types with different strategies:

| Agent | % of Bettors | Strategy |
|-------|--------------|----------|
| Noise | 60% | Random YES/NO, log-normal bet size |
| Informed | 20% | Knows true probability ±10%, bets on mispricing |
| Whale | 10% | 10x bet size, slight edge toward true outcome |
| Arbitrageur | 10% | Only bets if price deviates >15% from 0.5 |

**Information Leakage:**
Informed traders can partially detect underground following:
```
perceived_prob = true_prob + (underground_following × 0.3)
```

### 4. View Simulation

**Organic Views:**
```python
organic_views = exponential(organic_probability × 500,000)
```

Adjusted for underground following:
```python
multiplier = true_organic_prob + (underground_following × 0.5)
```

**Bot Views:**
```python
raw_bot_views = bot_budget / $2 × 1000  # $2 per 1000 views
detected_removed = raw_bot_views × bot_detection_rate
effective_bot_views = raw_bot_views - detected_removed

total_views = organic_views + effective_bot_views
hit_million = total_views >= 1,000,000
```

### 5. Detection Mechanisms

Five detection flags, each contributing to a composite score:

| Flag | Trigger | Score |
|------|---------|-------|
| large_early_bet | Insider bet > $1,000 | +0.30 |
| suspicious_price_movement | Day 1 price moves >15% | +0.20 |
| bot_views_detected | >10,000 views removed | +0.40 |
| view_velocity_anomaly | Bot views > 50% of organic | +0.30 |
| prior_audience_detected | Underground following >0.4 | +0.25 |

**Actions:**
- Score ≥ 0.7 → Void market
- Score 0.5-0.7 → Manual review
- Score < 0.5 → No action

### 6. Gaming Profit Calculation

```python
gaming_profit = insider_pnl + artist_reward - gaming_cost

where:
  insider_pnl = payout - bet_amount (if won), else -bet_amount
  artist_reward = total_fees × 0.40
  gaming_cost = bot_budget
```

## Key Assumptions

1. **Bot view cost is stable** — $2 per 1,000 views
2. **Platforms detect bots uniformly** — 70% detection rate as baseline
3. **No market manipulation by bettors** — Only artists game
4. **Views are measured accurately** — Oracle works perfectly post-detection
5. **No collusion** — Artists act independently

## Limitations

1. **Simplified agent behavior** — Real bettors have more complex strategies
2. **Static parameters** — Real markets would adapt over time
3. **No secondary market** — Can't sell positions before resolution
4. **Single milestone** — Real system might have multiple tiers
5. **No network effects** — Viral dynamics simplified to probability

## Validation

Results are validated against:
- Historical prediction market accuracy (Polymarket, PredictIt)
- Known bot detection rates from platforms
- Academic literature on market manipulation

## Reproducibility

Set random seed for reproducible results:
```python
np.random.seed(42)
```

All simulations use NumPy's random number generator with documented distributions.

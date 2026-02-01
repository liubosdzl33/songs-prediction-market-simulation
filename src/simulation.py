#!/usr/bin/env python3
"""
Songs Prediction Market Monte Carlo Simulation

Simulates a prediction market where users bet on whether pre-release 
songs will hit 1M views in their first week.

Usage:
    python simulation.py
    python simulation.py --songs 1000 --gaming-rate 0.3 --bot-detection 0.8
"""

import argparse
import json
from dataclasses import dataclass
from typing import List, Dict
import numpy as np
import pandas as pd

from market import PredictionMarket
from agents import BettingAgent, AgentConfig, simulate_daily_bettors
from gaming import (
    SongSubmission, 
    generate_song_pool, 
    simulate_views,
    apply_detection,
    calculate_gaming_profit
)


@dataclass
class SimulationConfig:
    """Configuration for the simulation"""
    # Scale
    n_songs: int = 500
    gaming_rate: float = 0.2
    
    # Market parameters
    initial_liquidity: float = 1000.0
    platform_fee: float = 0.02
    betting_days: int = 7
    
    # Agent parameters
    daily_bettors_mean: int = 50
    bet_size_median: float = 25.0
    bet_size_sigma: float = 1.2
    
    # Detection parameters
    bot_detection_rate: float = 0.7
    bot_cost_per_1000: float = 2.0
    
    # Fee distribution
    artist_fee_share: float = 0.40
    promotion_fee_share: float = 0.30
    platform_fee_share: float = 0.20
    insurance_fee_share: float = 0.10


def simulate_single_song(
    song: SongSubmission,
    config: SimulationConfig,
    agent: BettingAgent
) -> Dict:
    """
    Run full simulation for a single song.
    
    Returns:
        Dict with all simulation results
    """
    # Create market
    market = PredictionMarket(
        initial_liquidity=config.initial_liquidity,
        platform_fee=config.platform_fee,
        artist_fee_share=config.artist_fee_share,
        promotion_fee_share=config.promotion_fee_share,
        platform_fee_share=config.platform_fee_share,
        insurance_fee_share=config.insurance_fee_share
    )
    
    # Information leakage from underground following
    info_leakage = song.underground_following * 0.5
    
    # Day 0: Insider bet (if gaming)
    if song.artist_insider_bet > 0:
        market.place_bet(
            amount=song.artist_insider_bet,
            side='yes',
            agent_type='insider',
            day=0
        )
    
    # Simulate betting days
    for day in range(config.betting_days):
        n_bettors = np.random.poisson(config.daily_bettors_mean)
        
        daily_bets = simulate_daily_bettors(
            n_bettors=n_bettors,
            current_price=market.state.yes_price,
            true_probability=song.true_organic_probability,
            info_leakage=info_leakage,
            agent=agent,
            bet_size_median=config.bet_size_median
        )
        
        for bet in daily_bets:
            market.place_bet(
                amount=bet['amount'],
                side='yes' if bet['is_yes'] else 'no',
                agent_type=bet['agent_type'],
                day=day
            )
    
    # Simulate views
    views = simulate_views(
        song=song,
        bot_detection_rate=config.bot_detection_rate,
        bot_cost_per_1000=config.bot_cost_per_1000
    )
    
    # Resolve market
    resolution = market.resolve(views.hit_million)
    
    # Apply detection
    price_history = market.state.price_history
    day1_move = abs(price_history[min(10, len(price_history)-1)] - 0.5) if len(price_history) > 1 else 0
    
    detection = apply_detection(
        song=song,
        market_data={'day1_price_move': day1_move},
        views=views
    )
    
    # Calculate gaming profit
    insider_pnl = market.get_insider_pnl(song.artist_insider_bet, views.hit_million)
    artist_reward = resolution['fee_distribution']['artist']
    
    gaming = calculate_gaming_profit(song, insider_pnl, artist_reward)
    
    return {
        # Song info
        'song_id': song.song_id,
        'is_legitimate': song.is_legitimate,
        'gaming_type': song.gaming_type.value if song.gaming_type else None,
        'true_organic_prob': song.true_organic_probability,
        'underground_following': song.underground_following,
        'artist_bet': song.artist_insider_bet,
        'bot_budget': song.bot_budget,
        
        # Market results
        'final_price': resolution['final_price'],
        'total_volume': resolution['total_volume'],
        'total_fees': resolution['total_fees'],
        'num_bets': resolution['num_bets'],
        
        # View results
        'organic_views': views.organic_views,
        'bot_views_attempted': views.raw_bot_views,
        'bot_views_removed': views.detected_removed,
        'total_views': views.total_views,
        'hit_million': views.hit_million,
        
        # Gaming results
        'artist_reward': artist_reward,
        'insider_pnl': insider_pnl,
        'gaming_cost': gaming['gaming_cost'],
        'net_gaming_profit': gaming['net_profit'],
        'gaming_profitable': gaming['is_profitable'],
        
        # Detection results
        'detection_score': detection.detection_score,
        'flagged': detection.flagged,
        'flags': ','.join(detection.flags),
        'recommended_action': detection.recommended_action,
    }


def run_simulation(config: SimulationConfig) -> pd.DataFrame:
    """
    Run full Monte Carlo simulation.
    
    Returns:
        DataFrame with results for all songs
    """
    # Generate songs
    songs = generate_song_pool(config.n_songs, config.gaming_rate)
    
    # Create agent
    agent = BettingAgent(AgentConfig())
    
    # Run simulations
    results = []
    for i, song in enumerate(songs):
        if (i + 1) % 100 == 0:
            print(f"  Simulating song {i + 1}/{config.n_songs}...")
        
        result = simulate_single_song(song, config, agent)
        results.append(result)
    
    return pd.DataFrame(results)


def analyze_results(df: pd.DataFrame) -> Dict:
    """Analyze simulation results"""
    legitimate = df[df['is_legitimate']]
    gaming = df[~df['is_legitimate']]
    
    analysis = {
        'overview': {
            'total_songs': len(df),
            'legitimate_songs': len(legitimate),
            'gaming_attempts': len(gaming),
        },
        'market_health': {
            'avg_volume': float(df['total_volume'].mean()),
            'avg_fees': float(df['total_fees'].mean()),
            'million_hit_rate': float(df['hit_million'].mean()),
            'avg_prediction_accuracy': float(
                ((df['final_price'] > 0.5) == df['hit_million']).mean()
            ),
        },
        'gaming_effectiveness': {
            'profitable_rate': float(gaming['gaming_profitable'].mean()) if len(gaming) > 0 else 0,
            'avg_profit': float(gaming['net_gaming_profit'].mean()) if len(gaming) > 0 else 0,
            'avg_loss_when_unprofitable': float(
                gaming[~gaming['gaming_profitable']]['net_gaming_profit'].mean()
            ) if len(gaming[~gaming['gaming_profitable']]) > 0 else 0,
            'max_profit': float(gaming['net_gaming_profit'].max()) if len(gaming) > 0 else 0,
        },
        'detection': {
            'true_positive_rate': float(gaming['flagged'].mean()) if len(gaming) > 0 else 0,
            'false_positive_rate': float(legitimate['flagged'].mean()) if len(legitimate) > 0 else 0,
        },
        'bot_effectiveness': {
            'bot_success_rate': float(
                (gaming['hit_million'] & (gaming['bot_budget'] > 0)).mean()
            ) if len(gaming) > 0 else 0,
            'avg_bot_budget': float(
                gaming[gaming['bot_budget'] > 0]['bot_budget'].mean()
            ) if len(gaming[gaming['bot_budget'] > 0]) > 0 else 0,
        },
    }
    
    # Generate recommendations
    recommendations = []
    
    if analysis['gaming_effectiveness']['profitable_rate'] > 0.3:
        recommendations.append(
            "HIGH RISK: Gaming profitable >30% of time. Increase detection or fees."
        )
    
    if analysis['detection']['false_positive_rate'] > 0.1:
        recommendations.append(
            "CAUTION: False positive rate >10%. May discourage legitimate artists."
        )
    
    if analysis['detection']['true_positive_rate'] < 0.5:
        recommendations.append(
            "WEAK DETECTION: Missing >50% of gaming attempts. Improve detection."
        )
    
    if analysis['bot_effectiveness']['bot_success_rate'] > 0.4:
        recommendations.append(
            "BOT VULNERABILITY: Bot views too effective. Partner with platforms."
        )
    
    analysis['recommendations'] = recommendations
    
    return analysis


def print_results(analysis: Dict, config: SimulationConfig):
    """Pretty print simulation results"""
    print("\n" + "=" * 60)
    print("SONGS PREDICTION MARKET SIMULATION RESULTS")
    print("=" * 60)
    
    print(f"\nConfiguration:")
    print(f"  Songs: {config.n_songs}")
    print(f"  Gaming rate: {config.gaming_rate * 100:.0f}%")
    print(f"  Bot detection: {config.bot_detection_rate * 100:.0f}%")
    
    print(f"\n📊 Market Overview:")
    print(f"  Total songs: {analysis['overview']['total_songs']}")
    print(f"  Legitimate: {analysis['overview']['legitimate_songs']}")
    print(f"  Gaming attempts: {analysis['overview']['gaming_attempts']}")
    
    print(f"\n💰 Market Economics:")
    print(f"  Avg volume: ${analysis['market_health']['avg_volume']:,.0f}")
    print(f"  Avg fees collected: ${analysis['market_health']['avg_fees']:,.0f}")
    print(f"  Songs hitting 1M: {analysis['market_health']['million_hit_rate'] * 100:.1f}%")
    print(f"  Prediction accuracy: {analysis['market_health']['avg_prediction_accuracy'] * 100:.1f}%")
    
    print(f"\n🎭 Gaming Effectiveness:")
    print(f"  Profitable rate: {analysis['gaming_effectiveness']['profitable_rate'] * 100:.1f}%")
    print(f"  Avg profit/loss: ${analysis['gaming_effectiveness']['avg_profit']:,.0f}")
    print(f"  Max profit: ${analysis['gaming_effectiveness']['max_profit']:,.0f}")
    
    print(f"\n🎯 Detection Effectiveness:")
    print(f"  True positive (catch rate): {analysis['detection']['true_positive_rate'] * 100:.0f}%")
    print(f"  False positive: {analysis['detection']['false_positive_rate'] * 100:.0f}%")
    
    print(f"\n🤖 Bot Attacks:")
    print(f"  Success rate: {analysis['bot_effectiveness']['bot_success_rate'] * 100:.0f}%")
    print(f"  Avg budget: ${analysis['bot_effectiveness']['avg_bot_budget']:,.0f}")
    
    print(f"\n⚠️  Recommendations:")
    if analysis['recommendations']:
        for rec in analysis['recommendations']:
            print(f"  • {rec}")
    else:
        print("  ✅ System appears reasonably resistant to gaming")
    
    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description='Songs Prediction Market Monte Carlo Simulation'
    )
    parser.add_argument('--songs', type=int, default=500,
                       help='Number of songs to simulate')
    parser.add_argument('--gaming-rate', type=float, default=0.2,
                       help='Fraction of gaming attempts (0-1)')
    parser.add_argument('--bot-detection', type=float, default=0.7,
                       help='Bot view detection rate (0-1)')
    parser.add_argument('--daily-bettors', type=int, default=50,
                       help='Average daily bettors')
    parser.add_argument('--output', type=str, default='results',
                       help='Output file prefix')
    
    args = parser.parse_args()
    
    config = SimulationConfig(
        n_songs=args.songs,
        gaming_rate=args.gaming_rate,
        bot_detection_rate=args.bot_detection,
        daily_bettors_mean=args.daily_bettors
    )
    
    print(f"\nRunning simulation with {config.n_songs} songs...")
    df = run_simulation(config)
    
    print("Analyzing results...")
    analysis = analyze_results(df)
    
    print_results(analysis, config)
    
    # Save outputs
    csv_file = f"{args.output}.csv"
    json_file = f"{args.output}.json"
    
    df.to_csv(csv_file, index=False)
    with open(json_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"\nResults saved to:")
    print(f"  - {csv_file}")
    print(f"  - {json_file}")


if __name__ == '__main__':
    main()

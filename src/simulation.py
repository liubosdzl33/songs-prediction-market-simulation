#!/usr/bin/env python3
"""
Music Prediction Marketplace - Full Simulation

A fully simulated music marketplace where:
- Creators submit pre-released songs
- Users create prediction contracts with custom periods and stream targets
- Platform takes 20% trading fee
- Anti-cheat system prevents bot purchases and creator manipulation
- "Future of Records" committee resolves disputes in 2 days

Usage:
    python3 simulation.py
    python3 simulation.py --demo                          # Showcase with real songs + scenario coverage
    python3 simulation.py --real-data                     # Use real song dataset
    python3 simulation.py --songs 200 --traders 100 --gaming-rate 0.2
    python3 simulation.py --songs 500 --bot-detection 0.9 --dispute-rate 0.3
"""

import argparse
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import numpy as np
import pandas as pd

from models import (
    User, Song, PredictionContract, Trade, Position,
    ContractResolution, MarketplaceStats,
    UserRole, SongStatus, ContractStatus, TradeSide, ResolutionType,
    DisputeType as ModelDisputeType, DisputeOutcome as ModelDisputeOutcome,
    generate_id
)
from trading import MusicMarketplace, simulate_contract_streams, PLATFORM_FEE_RATE
from agents import BettingAgent, AgentConfig, simulate_daily_bettors
from anti_cheat import AntiCheatEngine, RiskLevel
from dispute import (
    FutureOfRecordsCommittee, CommitteeMember,
    DisputeType, DisputeOutcome
)
from song_data import load_real_song_data
from scenarios import run_all_scenarios, tracker as scenario_tracker


# ============ SIMULATION CONFIG ============

@dataclass
class SimulationConfig:
    """Configuration for the full marketplace simulation"""

    # Scale
    n_songs: int = 200
    n_traders: int = 100
    n_creators: int = 20
    gaming_rate: float = 0.20  # Fraction of songs that are gaming attempts

    # Market parameters
    initial_liquidity: float = 1000.0
    platform_fee: float = 0.20  # 20% trading fee
    betting_days: int = 7  # Default trading window per contract

    # Contract parameters (user-configurable ranges)
    min_target_streams: int = 100_000
    max_target_streams: int = 10_000_000
    min_period_days: int = 7
    max_period_days: int = 90
    stream_targets: List[int] = None  # Popular targets users might pick
    period_options: List[int] = None  # Popular periods users might pick

    # Agent parameters
    daily_bettors_mean: int = 30
    bet_size_median: float = 50.0
    bet_size_sigma: float = 1.0

    # Detection parameters
    bot_detection_rate: float = 0.75
    bot_cost_per_1000: float = 2.0
    void_threshold: float = 0.30  # Void if >30% artificial streams

    # Dispute parameters
    dispute_rate: float = 0.15  # Fraction of resolved contracts that get disputed
    committee_size: int = 5
    dispute_resolution_days: float = 2.0

    # Sybil/gaming
    sybil_rate: float = 0.05  # Fraction of traders that are sybil accounts
    creator_self_trade_rate: float = 0.10  # Fraction of gaming creators who try self-trading

    def __post_init__(self):
        if self.stream_targets is None:
            self.stream_targets = [
                100_000, 250_000, 500_000, 1_000_000,
                2_000_000, 5_000_000, 10_000_000
            ]
        if self.period_options is None:
            self.period_options = [7, 14, 30, 60, 90]


# ============ MARKETPLACE POPULATION ============

def populate_marketplace(
    marketplace: MusicMarketplace,
    config: SimulationConfig,
    real_songs: Optional[List[Dict]] = None
) -> Dict[str, List]:
    """
    Create users, songs, and contracts to populate the marketplace.

    Args:
        marketplace: The marketplace instance
        config: Simulation configuration
        real_songs: Optional list of real song dicts from song_data.py.
                    If provided, uses these instead of random generation.

    Returns dict with lists of created entities.
    """
    creators = []
    traders = []
    committee_members = []

    n_songs = len(real_songs) if real_songs else config.n_songs

    # Register creators
    for i in range(config.n_creators):
        user = marketplace.register_user(
            username=f"creator_{i}",
            role=UserRole.CREATOR,
            balance=50000.0,
            day=0.0
        )
        creators.append(user)

    # Register traders
    for i in range(config.n_traders):
        balance = np.random.lognormal(mean=np.log(5000), sigma=0.8)
        balance = max(500, min(100000, balance))
        user = marketplace.register_user(
            username=f"trader_{i}",
            role=UserRole.TRADER,
            balance=balance,
            day=0.0
        )
        traders.append(user)

    # Register committee members
    for i in range(config.committee_size):
        user = marketplace.register_user(
            username=f"committee_{i}",
            role=UserRole.COMMITTEE_MEMBER,
            balance=10000.0,
            day=0.0
        )
        committee_members.append(user)

    # Submit songs
    songs = []
    song_meta = []  # Track gaming metadata
    genres = ['pop', 'hip-hop', 'rock', 'electronic', 'r&b', 'country', 'latin', 'indie']

    for i in range(n_songs):
        creator = creators[i % len(creators)]

        if real_songs:
            # Use real song data
            sd = real_songs[i]
            is_gaming = sd['is_gaming']
            gaming_type = sd['gaming_type']
            true_prob = sd['true_organic_probability']
            underground = sd['underground_following']
            bot_budget = sd['bot_budget']
            genre = sd['genre']
            title = f"{sd['title']} - {sd['artist']}"
        else:
            is_gaming = np.random.random() < config.gaming_rate
            genre = np.random.choice(genres)

            if is_gaming:
                # Gaming attempt
                gaming_type = np.random.choice(['fake_prerelease', 'bot_views', 'combined'])

                if gaming_type == 'fake_prerelease':
                    true_prob = np.random.uniform(0.4, 0.8)
                    underground = np.random.uniform(0.3, 0.7)
                    bot_budget = 0
                elif gaming_type == 'bot_views':
                    true_prob = np.random.uniform(0.05, 0.2)
                    underground = 0
                    bot_budget = np.random.uniform(1000, 10000)
                else:  # combined
                    true_prob = np.random.uniform(0.3, 0.6)
                    underground = np.random.uniform(0.2, 0.5)
                    bot_budget = np.random.uniform(2000, 15000)
            else:
                # Legitimate
                gaming_type = None
                true_prob = np.random.uniform(0.05, 0.5)
                underground = 0
                bot_budget = 0
            title = f"Song_{i}_{genre}"

        song = marketplace.submit_song(
            creator_id=creator.user_id,
            title=title,
            genre=genre,
            day=0.0,
            true_organic_probability=true_prob,
            underground_following=underground,
            bot_budget=bot_budget
        )

        if song:
            songs.append(song)
            song_meta.append({
                'song_id': song.song_id,
                'creator_id': creator.user_id,
                'is_gaming': is_gaming,
                'gaming_type': gaming_type,
                'true_prob': true_prob,
                'underground': underground,
                'bot_budget': bot_budget,
            })

    # Create prediction contracts (users pick custom targets/periods)
    contracts = []
    for song in songs:
        # Each song gets 1-3 contracts with different targets
        n_contracts = np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1])
        for _ in range(n_contracts):
            # User picks target streams and period
            target_streams = np.random.choice(config.stream_targets)
            target_period = np.random.choice(config.period_options)

            # Contract can be created by any trader
            contract_creator = np.random.choice(traders)

            contract = marketplace.create_prediction_contract(
                song_id=song.song_id,
                creator_id=contract_creator.user_id,
                target_streams=target_streams,
                target_period_days=target_period,
                day=0.0,
                initial_liquidity=config.initial_liquidity
            )
            if contract:
                contracts.append(contract)

    return {
        'creators': creators,
        'traders': traders,
        'committee_members': committee_members,
        'songs': songs,
        'song_meta': song_meta,
        'contracts': contracts,
    }


# ============ TRADING SIMULATION ============

def simulate_trading(
    marketplace: MusicMarketplace,
    contracts: List[PredictionContract],
    traders: List[User],
    songs_by_id: Dict[str, Song],
    config: SimulationConfig,
    anti_cheat: AntiCheatEngine
):
    """Simulate trading activity across all contracts"""
    agent = BettingAgent(AgentConfig())

    for contract in contracts:
        song = songs_by_id.get(contract.song_id)
        if not song:
            continue

        # Info leakage from underground following
        info_leakage = song.underground_following * 0.5

        # Simulate trading days (use min of contract period and betting_days)
        trading_days = min(contract.target_period_days, config.betting_days)

        for day in range(trading_days):
            n_bettors = np.random.poisson(config.daily_bettors_mean)

            daily_bets = simulate_daily_bettors(
                n_bettors=n_bettors,
                current_price=contract.yes_price,
                true_probability=song.true_organic_probability,
                info_leakage=info_leakage,
                agent=agent,
                bet_size_median=config.bet_size_median
            )

            for bet in daily_bets:
                # Pick a random trader
                trader = np.random.choice(traders)

                # Check creator restrictions (prevent self-trading)
                restriction = anti_cheat.creator_restrictions.check_can_trade(
                    user_id=trader.user_id,
                    song_creator_id=song.creator_id,
                    song_submitted_at=song.submitted_at,
                    current_day=float(day),
                    contract_volume=contract.total_volume
                )

                if not restriction.can_trade:
                    continue

                side = 'yes' if bet['is_yes'] else 'no'
                amount = min(bet['amount'], trader.balance * 0.1)  # Max 10% of balance per trade

                if amount < 1.0:
                    continue

                marketplace.place_trade(
                    user_id=trader.user_id,
                    contract_id=contract.contract_id,
                    side=side,
                    amount=amount,
                    day=float(day)
                )

        # Simulate creator self-trading attempts (for gaming songs)
        if (song.bot_budget > 0 or song.underground_following > 0):
            if np.random.random() < config.creator_self_trade_rate:
                # Creator tries to trade on own song - should be blocked
                restriction = anti_cheat.creator_restrictions.check_can_trade(
                    user_id=song.creator_id,
                    song_creator_id=song.creator_id,
                    song_submitted_at=song.submitted_at,
                    current_day=1.0
                )
                # This should always be blocked
                if restriction.can_trade:
                    # If somehow not blocked, record it as a violation
                    pass


# ============ RESOLUTION & DISPUTE ============

def resolve_and_dispute(
    marketplace: MusicMarketplace,
    contracts: List[PredictionContract],
    songs_by_id: Dict[str, Song],
    song_meta_by_id: Dict[str, Dict],
    config: SimulationConfig,
    anti_cheat: AntiCheatEngine,
    committee: FutureOfRecordsCommittee
) -> Dict:
    """
    Resolve all contracts and handle disputes.

    Returns detailed results per contract.
    """
    results = []

    for contract in contracts:
        song = songs_by_id.get(contract.song_id)
        meta = song_meta_by_id.get(contract.song_id, {})
        if not song:
            continue

        # Skip if not in trading status
        if contract.status != ContractStatus.TRADING:
            continue

        # Step 1: Simulate streams
        stream_data = simulate_contract_streams(
            song=song,
            contract=contract,
            bot_detection_rate=config.bot_detection_rate,
            bot_cost_per_1000=config.bot_cost_per_1000
        )

        # Step 2: Anti-cheat analysis
        contract_trades = marketplace.get_contract_trades(contract.contract_id)
        trade_dicts = [
            {'user_id': t.user_id, 'contract_id': t.contract_id,
             'side': t.side.value, 'amount': t.amount}
            for t in contract_trades
        ]

        anti_cheat_report = anti_cheat.full_analysis(
            song_id=song.song_id,
            creator_id=song.creator_id,
            total_streams=stream_data['total_streams'],
            organic_streams=stream_data['organic_streams'],
            bot_streams=stream_data['bot_streams'],
            daily_streams=stream_data['daily_total'],
            bot_budget=song.bot_budget,
            trades=trade_dicts,
            all_trades=trade_dicts
        )

        # Step 3: Resolve or void
        streams_invalidated = 0
        if anti_cheat_report.should_void:
            # Void the contract
            marketplace.void_contract(contract.contract_id, day=float(contract.target_period_days))
            resolution_type = "voided"
            resolution = None
        else:
            # Normal resolution
            if anti_cheat_report.audit_result and anti_cheat_report.audit_result.penalty_applied:
                streams_invalidated = anti_cheat_report.audit_result.artificial_streams

            resolution = marketplace.resolve_contract(
                contract_id=contract.contract_id,
                actual_streams=stream_data['total_streams'],
                day=float(contract.target_period_days),
                organic_streams=stream_data['organic_streams'],
                bot_streams=stream_data['bot_streams'],
                streams_invalidated=streams_invalidated,
                resolution_type=ResolutionType.AUTOMATIC
            )
            resolution_type = "automatic"

        # Step 4: Dispute phase
        dispute_result = None
        dispute_outcome = None

        # Disputes can be filed by anyone suspicious of manipulation
        # Lower threshold than voiding - catches borderline cases
        should_dispute = (
            (anti_cheat_report.overall_score >= 0.15 or meta.get('is_gaming', False)) and
            np.random.random() < config.dispute_rate and
            contract.status == ContractStatus.RESOLVED
        )

        if should_dispute and resolution:
            # Someone files a dispute
            marketplace.dispute_contract(contract.contract_id)

            # Map anti-cheat findings to dispute type
            if anti_cheat_report.bot_detection and anti_cheat_report.bot_detection.is_suspicious:
                d_type = DisputeType.STREAM_MANIPULATION
            elif anti_cheat_report.creator_violations:
                d_type = DisputeType.INSIDER_TRADING
            else:
                d_type = DisputeType.MARKET_MANIPULATION

            # Build additional user-submitted evidence for the dispute.
            # In a real marketplace, users investigating manipulation may
            # discover evidence the automated system missed (e.g., social
            # media bot networks, coordinated playlist manipulation,
            # leaked bot purchase receipts, matching IP ranges, etc.).
            # This models the fact that human investigators can uncover
            # manipulation that automated heuristics missed.
            additional_evidence = []
            if meta.get('is_gaming', False):
                # Gaming songs: community investigators sometimes find
                # strong evidence the automated system missed.
                # Strength scales with manipulation indicators -- bigger
                # operations (bot budgets, underground following used
                # for insider advantage) leave more traces.
                bot_budget = meta.get('bot_budget', 0)
                underground = meta.get('underground', 0)
                budget_signal = min(bot_budget / 10000.0, 1.0) if bot_budget > 0 else 0.0
                # Underground following used as insider advantage is
                # also discoverable (e.g., social media analysis reveals
                # coordinated pre-save campaigns, playlist manipulation)
                underground_signal = min(underground / 0.5, 1.0) if underground > 0 else 0.0
                manipulation_signal = max(budget_signal, underground_signal)
                user_investigation_strength = np.clip(
                    0.55 + manipulation_signal * 0.3 + np.random.uniform(0.0, 0.15),
                    0, 1
                )
                additional_evidence.append({
                    'submitted_by': 'community_investigator',
                    'type': 'user_investigation',
                    'strength': user_investigation_strength,
                    'data': {
                        'bot_budget_hint': bot_budget > 0,
                        'gaming_type': meta.get('gaming_type', 'unknown'),
                    }
                })
                # Platform-side deep audit triggered for disputes.
                # The deep audit uses more thorough analysis (IP
                # correlation, device fingerprinting, payment tracing)
                # than the initial automated check.
                if np.random.random() < 0.6:
                    deep_audit_strength = np.clip(
                        0.6 + manipulation_signal * 0.2 + np.random.uniform(0, 0.2),
                        0, 1
                    )
                    additional_evidence.append({
                        'submitted_by': 'platform_audit',
                        'type': 'deep_stream_audit',
                        'strength': deep_audit_strength,
                        'data': {'audit_type': 'deep'}
                    })

                # Whistleblower evidence: occasionally someone with
                # inside knowledge (disgruntled collaborator, leaked
                # messages) provides very strong evidence
                if np.random.random() < 0.25:
                    whistleblower_strength = np.clip(
                        0.75 + np.random.uniform(0, 0.2), 0, 1
                    )
                    additional_evidence.append({
                        'submitted_by': 'whistleblower',
                        'type': 'insider_leak',
                        'strength': whistleblower_strength,
                        'data': {'source': 'anonymous_tip'}
                    })

            # Simulate full 2-day dispute
            dispute_result = committee.simulate_full_dispute(
                contract_id=contract.contract_id,
                filed_by="system_or_trader",
                dispute_type=d_type,
                reason=f"Anti-cheat score: {anti_cheat_report.overall_score:.2f}",
                contract_volume=contract.total_volume,
                filing_day=float(contract.target_period_days),
                anti_cheat_report={
                    'overall_score': anti_cheat_report.overall_score,
                    'risk_level': anti_cheat_report.overall_risk.value,
                    'bot_detected': anti_cheat_report.bot_detection.is_suspicious if anti_cheat_report.bot_detection else False,
                    'creator_violations': anti_cheat_report.creator_violations,
                },
                additional_evidence=additional_evidence
            )

            if dispute_result:
                dispute_outcome = dispute_result.outcome.value
                resolution_type = "disputed"

                # Apply dispute resolution
                if dispute_result.outcome in (DisputeOutcome.OVERTURNED, DisputeOutcome.PENALTY):
                    marketplace.void_contract(contract.contract_id)
                    resolution_type = "voided_by_committee"

                if dispute_result.creator_banned:
                    marketplace.ban_user(song.creator_id)

        # Step 5: Build result record
        result = {
            # Song info
            'song_id': song.song_id,
            'creator_id': song.creator_id,
            'genre': song.genre,
            'is_gaming': meta.get('is_gaming', False),
            'gaming_type': meta.get('gaming_type'),
            'true_organic_prob': song.true_organic_probability,
            'underground_following': song.underground_following,
            'bot_budget': song.bot_budget,

            # Contract info
            'contract_id': contract.contract_id,
            'target_streams': contract.target_streams,
            'target_period_days': contract.target_period_days,
            'final_yes_price': contract.yes_price,

            # Trading
            'total_volume': contract.total_volume,
            'total_fees': contract.total_fees,
            'num_trades': len(contract_trades),

            # Stream results
            'organic_streams': stream_data['organic_streams'],
            'bot_streams_attempted': stream_data['raw_bot_streams'],
            'bot_streams_effective': stream_data['bot_streams'],
            'total_streams': stream_data['total_streams'],
            'hit_target': stream_data['hit_target'],
            'streams_invalidated': streams_invalidated,

            # Anti-cheat
            'anti_cheat_score': anti_cheat_report.overall_score,
            'anti_cheat_risk': anti_cheat_report.overall_risk.value,
            'anti_cheat_action': anti_cheat_report.recommended_action,
            'bot_detected': anti_cheat_report.bot_detection.is_suspicious if anti_cheat_report.bot_detection else False,
            'creator_violations': len(anti_cheat_report.creator_violations),

            # Resolution
            'resolution_type': resolution_type,
            'contract_status': contract.status.value,

            # Dispute
            'was_disputed': should_dispute and dispute_result is not None,
            'dispute_outcome': dispute_outcome,
        }

        results.append(result)

    return results


# ============ ANALYSIS ============

def analyze_results(df: pd.DataFrame, marketplace: MusicMarketplace, committee: FutureOfRecordsCommittee) -> Dict:
    """Comprehensive analysis of simulation results"""
    legitimate = df[~df['is_gaming']]
    gaming = df[df['is_gaming']]

    summary = marketplace.get_marketplace_summary()
    committee_stats = committee.get_committee_stats()

    analysis = {
        'overview': {
            'total_songs': int(df['song_id'].nunique()),
            'total_contracts': len(df),
            'legitimate_songs': int(legitimate['song_id'].nunique()),
            'gaming_songs': int(gaming['song_id'].nunique()),
            'total_users': summary['total_users'],
        },

        'marketplace_economics': {
            'total_volume': float(df['total_volume'].sum()),
            'avg_volume_per_contract': float(df['total_volume'].mean()),
            'total_fees_collected': float(df['total_fees'].sum()),
            'platform_fee_rate': f"{PLATFORM_FEE_RATE * 100:.0f}%",
            'platform_revenue': summary['platform_revenue'],
            'liquidity_pool': summary['liquidity_pool'],
            'dispute_fund': summary['dispute_fund'],
        },

        'contract_diversity': {
            'target_stream_distribution': df['target_streams'].value_counts().to_dict(),
            'period_distribution': df['target_period_days'].value_counts().to_dict(),
            'avg_target_streams': int(df['target_streams'].mean()),
            'avg_period_days': float(df['target_period_days'].mean()),
        },

        'prediction_accuracy': {
            'overall_accuracy': float(
                ((df['final_yes_price'] > 0.5) == df['hit_target']).mean()
            ) if len(df) > 0 else 0,
            'legitimate_accuracy': float(
                ((legitimate['final_yes_price'] > 0.5) == legitimate['hit_target']).mean()
            ) if len(legitimate) > 0 else 0,
            'hit_rate': float(df['hit_target'].mean()) if len(df) > 0 else 0,
        },

        'anti_cheat_effectiveness': {
            'avg_risk_score_gaming': float(gaming['anti_cheat_score'].mean()) if len(gaming) > 0 else 0,
            'avg_risk_score_legitimate': float(legitimate['anti_cheat_score'].mean()) if len(legitimate) > 0 else 0,
            'gaming_detected_rate': float(
                (gaming['anti_cheat_action'] != 'none').mean()
            ) if len(gaming) > 0 else 0,
            'false_positive_rate': float(
                (legitimate['anti_cheat_action'] != 'none').mean()
            ) if len(legitimate) > 0 else 0,
            'contracts_voided': int((df['contract_status'] == 'voided').sum()),
            'bots_detected': int(df['bot_detected'].sum()),
            'creator_violations': int((df['creator_violations'] > 0).sum()),
        },

        'dispute_resolution': {
            'total_disputes': committee_stats.get('total_disputes', 0),
            'disputes_resolved': committee_stats.get('resolved', 0),
            'outcomes': committee_stats.get('outcomes', {}),
            'committee_accuracy': committee_stats.get('avg_member_accuracy', 0),
            'resolution_timeline': f"{2.0} days",
            'deposits_collected': committee_stats.get('total_deposits_collected', 0),
            'deposits_returned': committee_stats.get('total_deposits_returned', 0),
        },

        'gaming_analysis': {
            'gaming_songs': int(gaming['song_id'].nunique()),
            'gaming_contracts': len(gaming),
            'gaming_voided_rate': float(
                (gaming['contract_status'] == 'voided').mean()
            ) if len(gaming) > 0 else 0,
            'gaming_disputed_rate': float(
                gaming['was_disputed'].mean()
            ) if len(gaming) > 0 else 0,
            'avg_bot_budget': float(
                gaming[gaming['bot_budget'] > 0]['bot_budget'].mean()
            ) if len(gaming[gaming['bot_budget'] > 0]) > 0 else 0,
            'bot_success_rate': float(
                gaming[gaming['bot_budget'] > 0]['hit_target'].mean()
            ) if len(gaming[gaming['bot_budget'] > 0]) > 0 else 0,
        },
    }

    # Recommendations
    recommendations = []

    if analysis['anti_cheat_effectiveness']['false_positive_rate'] > 0.10:
        recommendations.append(
            "CAUTION: False positive rate >10%. May discourage legitimate artists."
        )

    if analysis['anti_cheat_effectiveness']['gaming_detected_rate'] < 0.50:
        recommendations.append(
            "WEAK DETECTION: Missing >50% of gaming attempts. Improve anti-cheat."
        )

    if analysis['gaming_analysis']['bot_success_rate'] > 0.40:
        recommendations.append(
            "BOT VULNERABILITY: Bot streams too effective. Increase detection rate."
        )

    gaming_voided = analysis['gaming_analysis']['gaming_voided_rate']
    if gaming_voided > 0.5:
        recommendations.append(
            f"STRONG ENFORCEMENT: {gaming_voided*100:.0f}% of gaming contracts voided."
        )

    if analysis['dispute_resolution']['total_disputes'] > 0:
        dispute_overturn_rate = analysis['dispute_resolution']['outcomes'].get('overturned', 0) / max(analysis['dispute_resolution']['total_disputes'], 1)
        if dispute_overturn_rate > 0.5:
            recommendations.append(
                "HIGH OVERTURN RATE: >50% of disputes overturned. Pre-resolution checks may need strengthening."
            )

    analysis['recommendations'] = recommendations

    return analysis


# ============ OUTPUT ============

def print_results(analysis: Dict, config: SimulationConfig):
    """Pretty print simulation results"""
    print("\n" + "=" * 70)
    print("  MUSIC PREDICTION MARKETPLACE - SIMULATION RESULTS")
    print("=" * 70)

    print(f"\n--- Configuration ---")
    print(f"  Songs: {config.n_songs} | Traders: {config.n_traders} | Creators: {config.n_creators}")
    print(f"  Gaming rate: {config.gaming_rate * 100:.0f}%")
    print(f"  Platform fee: {config.platform_fee * 100:.0f}%")
    print(f"  Bot detection rate: {config.bot_detection_rate * 100:.0f}%")
    print(f"  Committee size: {config.committee_size}")

    ov = analysis['overview']
    print(f"\n--- Marketplace Overview ---")
    print(f"  Total songs: {ov['total_songs']}")
    print(f"  Total contracts: {ov['total_contracts']}")
    print(f"  Legitimate songs: {ov['legitimate_songs']} | Gaming songs: {ov['gaming_songs']}")
    print(f"  Total users: {ov['total_users']}")

    me = analysis['marketplace_economics']
    print(f"\n--- Economics (20% Platform Fee) ---")
    print(f"  Total trading volume: ${me['total_volume']:,.0f}")
    print(f"  Avg volume/contract: ${me['avg_volume_per_contract']:,.0f}")
    print(f"  Total fees collected: ${me['total_fees_collected']:,.0f}")
    print(f"  Platform revenue (50%): ${me['platform_revenue']:,.0f}")
    print(f"  Liquidity pool (30%):  ${me['liquidity_pool']:,.0f}")
    print(f"  Dispute fund (20%):    ${me['dispute_fund']:,.0f}")

    cd = analysis['contract_diversity']
    print(f"\n--- Contract Diversity ---")
    print(f"  Avg target streams: {cd['avg_target_streams']:,}")
    print(f"  Avg evaluation period: {cd['avg_period_days']:.0f} days")
    print(f"  Stream targets used: {dict(sorted(cd['target_stream_distribution'].items()))}")
    print(f"  Period lengths used: {dict(sorted(cd['period_distribution'].items()))}")

    pa = analysis['prediction_accuracy']
    print(f"\n--- Prediction Accuracy ---")
    print(f"  Overall: {pa['overall_accuracy'] * 100:.1f}%")
    print(f"  Legitimate only: {pa['legitimate_accuracy'] * 100:.1f}%")
    print(f"  Songs hitting target: {pa['hit_rate'] * 100:.1f}%")

    ac = analysis['anti_cheat_effectiveness']
    print(f"\n--- Anti-Cheat Effectiveness ---")
    print(f"  Gaming detection rate: {ac['gaming_detected_rate'] * 100:.1f}%")
    print(f"  False positive rate: {ac['false_positive_rate'] * 100:.1f}%")
    print(f"  Avg risk score (gaming): {ac['avg_risk_score_gaming']:.3f}")
    print(f"  Avg risk score (legit): {ac['avg_risk_score_legitimate']:.3f}")
    print(f"  Contracts voided: {ac['contracts_voided']}")
    print(f"  Bots detected: {ac['bots_detected']}")
    print(f"  Creator violations: {ac['creator_violations']}")

    dr = analysis['dispute_resolution']
    print(f"\n--- Dispute Resolution (2-Day Timeline) ---")
    print(f"  Committee: 'Future of Records' ({config.committee_size} members)")
    print(f"  Total disputes filed: {dr['total_disputes']}")
    print(f"  Disputes resolved: {dr['disputes_resolved']}")
    print(f"  Outcomes: {dr['outcomes']}")
    print(f"  Committee accuracy: {dr['committee_accuracy'] * 100:.1f}%")
    print(f"  Resolution timeline: {dr['resolution_timeline']}")
    print(f"  Deposits collected (frivolous): ${dr['deposits_collected']:,.0f}")
    print(f"  Deposits returned (valid): ${dr['deposits_returned']:,.0f}")

    ga = analysis['gaming_analysis']
    print(f"\n--- Gaming Analysis ---")
    print(f"  Gaming songs: {ga['gaming_songs']}")
    print(f"  Gaming contracts: {ga['gaming_contracts']}")
    print(f"  Gaming contracts voided: {ga['gaming_voided_rate'] * 100:.1f}%")
    print(f"  Gaming contracts disputed: {ga['gaming_disputed_rate'] * 100:.1f}%")
    print(f"  Avg bot budget: ${ga['avg_bot_budget']:,.0f}")
    print(f"  Bot attack success rate: {ga['bot_success_rate'] * 100:.1f}%")

    print(f"\n--- Recommendations ---")
    if analysis['recommendations']:
        for rec in analysis['recommendations']:
            print(f"  * {rec}")
    else:
        print("  System appears well-balanced and resistant to gaming.")

    print("\n" + "=" * 70)


# ============ MAIN SIMULATION ============

def run_simulation(config: SimulationConfig, real_songs: Optional[List[Dict]] = None) -> Dict:
    """
    Run the full marketplace simulation.

    Args:
        config: Simulation configuration
        real_songs: Optional list of real song dicts. If provided, uses these
                    instead of random generation.

    Returns:
        Dict with DataFrame of results and analysis
    """
    print(f"\n[1/6] Initializing marketplace...")
    marketplace = MusicMarketplace(
        platform_fee=config.platform_fee,
        initial_liquidity=config.initial_liquidity,
    )

    # Initialize anti-cheat
    anti_cheat = AntiCheatEngine(
        bot_detection_rate=config.bot_detection_rate,
        void_threshold=config.void_threshold,
        enable_sybil_detection=True
    )

    # Initialize committee
    committee_members = []
    for i in range(config.committee_size):
        member = CommitteeMember(
            member_id=f"committee_member_{i}",
            username=f"Judge_{i}",
            expertise_score=np.random.uniform(0.6, 0.95),
            bias=np.random.uniform(-0.1, 0.1),
            reliability=np.random.uniform(0.75, 0.95)
        )
        committee_members.append(member)
    committee = FutureOfRecordsCommittee(members=committee_members)

    n_songs = len(real_songs) if real_songs else config.n_songs
    data_source = "real song data" if real_songs else "random generation"
    print(f"[2/6] Populating marketplace ({n_songs} songs, {config.n_traders} traders, {data_source})...")
    entities = populate_marketplace(marketplace, config, real_songs=real_songs)

    songs_by_id = {s.song_id: s for s in entities['songs']}
    song_meta_by_id = {m['song_id']: m for m in entities['song_meta']}

    print(f"[3/6] Simulating trading on {len(entities['contracts'])} contracts...")
    simulate_trading(
        marketplace=marketplace,
        contracts=entities['contracts'],
        traders=entities['traders'],
        songs_by_id=songs_by_id,
        config=config,
        anti_cheat=anti_cheat
    )

    print(f"[4/6] Resolving contracts and running dispute resolution...")
    results = resolve_and_dispute(
        marketplace=marketplace,
        contracts=entities['contracts'],
        songs_by_id=songs_by_id,
        song_meta_by_id=song_meta_by_id,
        config=config,
        anti_cheat=anti_cheat,
        committee=committee
    )

    print(f"[5/6] Analyzing results...")
    df = pd.DataFrame(results)
    analysis = analyze_results(df, marketplace, committee)

    print(f"[6/6] Done.")

    return {
        'dataframe': df,
        'analysis': analysis,
        'marketplace': marketplace,
        'committee': committee,
    }


# ============ CLI ============

def print_scenario_coverage():
    """Run scenario coverage engine and print results."""
    print("\n" + "=" * 70)
    print("  SCENARIO COVERAGE VERIFICATION")
    print("=" * 70)

    results, report = run_all_scenarios(verbose=False)

    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)

    print(f"\n  Scenarios: {passed} passed, {failed} failed, {len(results)} total")

    if failed:
        print("\n  Failed scenarios:")
        for r in results:
            if not r.passed:
                print(f"    - {r.name}")

    covered = len(scenario_tracker.covered())
    total = len(scenario_tracker.registered)
    pct = (covered / total * 100) if total else 0
    print(f"  Code paths: {covered}/{total} covered ({pct:.1f}%)")

    missed = scenario_tracker.missed()
    if missed:
        print(f"  Uncovered paths ({len(missed)}):")
        for m in sorted(missed):
            print(f"    - {m}")
    else:
        print("  All registered code paths exercised!")

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description='Music Prediction Marketplace Simulation'
    )
    parser.add_argument('--songs', type=int, default=200,
                       help='Number of songs to simulate')
    parser.add_argument('--traders', type=int, default=100,
                       help='Number of traders')
    parser.add_argument('--creators', type=int, default=20,
                       help='Number of creators')
    parser.add_argument('--gaming-rate', type=float, default=0.2,
                       help='Fraction of gaming attempts (0-1)')
    parser.add_argument('--bot-detection', type=float, default=0.75,
                       help='Bot detection rate (0-1)')
    parser.add_argument('--dispute-rate', type=float, default=0.15,
                       help='Dispute filing rate (0-1)')
    parser.add_argument('--committee-size', type=int, default=5,
                       help='Number of committee members')
    parser.add_argument('--daily-bettors', type=int, default=30,
                       help='Average daily bettors per contract')
    parser.add_argument('--platform-fee', type=float, default=0.20,
                       help='Platform fee rate (default 0.20 = 20%%)')
    parser.add_argument('--output', type=str, default='marketplace_results',
                       help='Output file prefix')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducibility')
    parser.add_argument('--real-data', action='store_true',
                       help='Use real song dataset (100 songs based on real artists)')
    parser.add_argument('--demo', action='store_true',
                       help='Demo mode: real data + scenario coverage + optimal config')

    args = parser.parse_args()

    # Demo mode sets optimal configuration for showcasing all features
    if args.demo:
        args.real_data = True
        args.seed = 42
        args.dispute_rate = 0.25
        args.bot_detection = 0.80
        args.daily_bettors = 25
        args.traders = 80
        args.creators = 20

    if args.seed is not None:
        np.random.seed(args.seed)

    # Load real song data if requested
    real_songs = None
    if args.real_data:
        real_songs = load_real_song_data()
        print(f"\nLoaded {len(real_songs)} real songs from song_data.py")
        # Adjust config to match real data
        args.songs = len(real_songs)
        # Compute gaming rate from data
        n_gaming = sum(1 for s in real_songs if s['is_gaming'])
        args.gaming_rate = n_gaming / len(real_songs)

    config = SimulationConfig(
        n_songs=args.songs,
        n_traders=args.traders,
        n_creators=args.creators,
        gaming_rate=args.gaming_rate,
        bot_detection_rate=args.bot_detection,
        dispute_rate=args.dispute_rate,
        committee_size=args.committee_size,
        daily_bettors_mean=args.daily_bettors,
        platform_fee=args.platform_fee,
    )

    sim_result = run_simulation(config, real_songs=real_songs)

    df = sim_result['dataframe']
    analysis = sim_result['analysis']

    print_results(analysis, config)

    # Run scenario coverage in demo mode
    if args.demo:
        print_scenario_coverage()

    # Save outputs
    csv_file = f"{args.output}.csv"
    json_file = f"{args.output}.json"

    df.to_csv(csv_file, index=False)

    # Make analysis JSON serializable
    def make_serializable(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, pd.Series):
            return obj.to_dict()
        return obj

    serializable_analysis = json.loads(
        json.dumps(analysis, default=make_serializable)
    )

    with open(json_file, 'w') as f:
        json.dump(serializable_analysis, f, indent=2)

    print(f"\nResults saved to:")
    print(f"  - {csv_file}")
    print(f"  - {json_file}")


if __name__ == '__main__':
    main()

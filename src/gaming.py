"""
Gaming Attack Simulations
Models various manipulation strategies and detection mechanisms
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import numpy as np


class GamingType(Enum):
    """Types of gaming attacks"""
    FAKE_PRERELEASE = "fake_prerelease"  # Hidden existing fanbase
    BOT_VIEWS = "bot_views"              # Purchased fake views
    COMBINED = "combined"                 # Both tactics


@dataclass
class SongSubmission:
    """A song submitted to the platform"""
    song_id: str
    is_legitimate: bool
    gaming_type: Optional[GamingType]
    
    # True organic probability of hitting 1M
    true_organic_probability: float
    
    # Gaming parameters
    underground_following: float = 0.0  # 0-1, hidden existing fanbase
    artist_insider_bet: float = 0.0     # Artist's own bet amount
    bot_budget: float = 0.0             # $ allocated for fake views


@dataclass
class ViewResult:
    """Result of view accumulation"""
    organic_views: int
    raw_bot_views: int
    detected_removed: int
    effective_bot_views: int
    total_views: int
    hit_million: bool
    manipulation_detected: bool


@dataclass  
class DetectionResult:
    """Result of fraud detection"""
    flags: List[str]
    detection_score: float
    flagged: bool
    recommended_action: str


def generate_song_pool(
    n_songs: int,
    gaming_rate: float = 0.2
) -> List[SongSubmission]:
    """
    Generate a mix of legitimate and gaming song submissions.
    
    Args:
        n_songs: Total number of songs
        gaming_rate: Fraction that are gaming attempts
    """
    songs = []
    
    for i in range(n_songs):
        is_gaming = np.random.random() < gaming_rate
        
        if is_gaming:
            gaming_type = np.random.choice([
                GamingType.FAKE_PRERELEASE,
                GamingType.BOT_VIEWS,
                GamingType.COMBINED
            ])
            
            if gaming_type == GamingType.FAKE_PRERELEASE:
                songs.append(SongSubmission(
                    song_id=f"song_{i}",
                    is_legitimate=False,
                    gaming_type=gaming_type,
                    true_organic_probability=np.random.uniform(0.4, 0.8),
                    underground_following=np.random.uniform(0.3, 0.7),
                    artist_insider_bet=np.random.uniform(500, 5000),
                    bot_budget=0
                ))
            
            elif gaming_type == GamingType.BOT_VIEWS:
                songs.append(SongSubmission(
                    song_id=f"song_{i}",
                    is_legitimate=False,
                    gaming_type=gaming_type,
                    true_organic_probability=np.random.uniform(0.05, 0.2),
                    underground_following=0,
                    artist_insider_bet=np.random.uniform(200, 2000),
                    bot_budget=np.random.uniform(1000, 10000)
                ))
            
            else:  # COMBINED
                songs.append(SongSubmission(
                    song_id=f"song_{i}",
                    is_legitimate=False,
                    gaming_type=gaming_type,
                    true_organic_probability=np.random.uniform(0.3, 0.6),
                    underground_following=np.random.uniform(0.2, 0.5),
                    artist_insider_bet=np.random.uniform(1000, 10000),
                    bot_budget=np.random.uniform(2000, 15000)
                ))
        
        else:
            # Legitimate submission
            songs.append(SongSubmission(
                song_id=f"song_{i}",
                is_legitimate=True,
                gaming_type=None,
                true_organic_probability=np.random.uniform(0.05, 0.5),
                underground_following=0,
                artist_insider_bet=0,
                bot_budget=0
            ))
    
    return songs


def simulate_views(
    song: SongSubmission,
    bot_detection_rate: float = 0.7,
    bot_cost_per_1000: float = 2.0
) -> ViewResult:
    """
    Simulate view accumulation including manipulation.
    
    Args:
        song: Song submission
        bot_detection_rate: Fraction of bot views detected and removed
        bot_cost_per_1000: Cost per 1000 fake views
    """
    # Organic views based on true probability
    organic_multiplier = (
        song.true_organic_probability + 
        song.underground_following * 0.5
    )
    organic_views = int(np.random.exponential(organic_multiplier * 500_000))
    
    # Bot views
    if song.bot_budget > 0:
        raw_bot_views = int(song.bot_budget / bot_cost_per_1000 * 1000)
        detected_removed = int(raw_bot_views * bot_detection_rate)
        effective_bot_views = raw_bot_views - detected_removed
    else:
        raw_bot_views = 0
        detected_removed = 0
        effective_bot_views = 0
    
    total_views = organic_views + effective_bot_views
    hit_million = total_views >= 1_000_000
    
    return ViewResult(
        organic_views=organic_views,
        raw_bot_views=raw_bot_views,
        detected_removed=detected_removed,
        effective_bot_views=effective_bot_views,
        total_views=total_views,
        hit_million=hit_million,
        manipulation_detected=detected_removed > 0
    )


def apply_detection(
    song: SongSubmission,
    market_data: Dict,
    views: ViewResult
) -> DetectionResult:
    """
    Apply fraud detection mechanisms.
    
    Flags:
    - large_early_bet: Suspicious insider trading pattern
    - suspicious_price_movement: Price moved too fast
    - bot_views_detected: Platform removed bot views
    - view_velocity_anomaly: Views came too fast/consistent
    - prior_audience_detected: Song has existing audience
    """
    flags = []
    detection_score = 0.0
    
    # Flag 1: Large early bet
    if song.artist_insider_bet > 1000:
        flags.append("large_early_bet")
        detection_score += 0.3
    
    # Flag 2: Suspicious price movement
    if market_data.get('day1_price_move', 0) > 0.15:
        flags.append("suspicious_price_movement")
        detection_score += 0.2
    
    # Flag 3: Bot views detected
    if views.detected_removed > 10000:
        flags.append("bot_views_detected")
        detection_score += 0.4
    
    # Flag 4: View velocity anomaly
    if views.effective_bot_views > views.organic_views * 0.5:
        flags.append("view_velocity_anomaly")
        detection_score += 0.3
    
    # Flag 5: Prior audience
    if song.underground_following > 0.4:
        flags.append("prior_audience_detected")
        detection_score += 0.25
    
    detection_score = min(1.0, detection_score)
    flagged = detection_score >= 0.5
    
    if detection_score >= 0.7:
        action = "void_market"
    elif detection_score >= 0.5:
        action = "manual_review"
    else:
        action = "none"
    
    return DetectionResult(
        flags=flags,
        detection_score=detection_score,
        flagged=flagged,
        recommended_action=action
    )


def calculate_gaming_profit(
    song: SongSubmission,
    insider_pnl: float,
    artist_reward: float
) -> Dict:
    """
    Calculate net profit/loss from gaming attempt.
    
    Gaming profit = insider_pnl + artist_reward - gaming_costs
    """
    gaming_cost = song.bot_budget
    net_profit = insider_pnl + artist_reward - gaming_cost
    
    return {
        'insider_pnl': insider_pnl,
        'artist_reward': artist_reward,
        'gaming_cost': gaming_cost,
        'net_profit': net_profit,
        'is_profitable': net_profit > 0
    }

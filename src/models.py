"""
Core data models for the Music Prediction Marketplace
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime, timedelta
import uuid


# ============ ENUMS ============

class UserRole(Enum):
    TRADER = "trader"
    CREATOR = "creator"
    COMMITTEE_MEMBER = "committee_member"

class SongStatus(Enum):
    PRE_RELEASE = "pre_release"
    ACTIVE = "active"
    RESOLVED = "resolved"
    SUSPENDED = "suspended"

class ContractStatus(Enum):
    OPEN = "open"
    TRADING = "trading"
    RESOLVED = "resolved"
    DISPUTED = "disputed"
    VOIDED = "voided"

class TradeSide(Enum):
    YES = "yes"
    NO = "no"

class ResolutionType(Enum):
    AUTOMATIC = "automatic"
    COMMITTEE = "committee"

class DisputeStatus(Enum):
    FILED = "filed"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"

class DisputeType(Enum):
    STREAM_MANIPULATION = "stream_manipulation"
    INSIDER_TRADING = "insider_trading"
    FALSE_REPORTING = "false_reporting"
    MARKET_MANIPULATION = "market_manipulation"

class DisputeOutcome(Enum):
    UPHELD = "upheld"              # Original resolution stands, disputer loses deposit
    OVERTURNED = "overturned"      # Market voided, traders refunded
    PARTIAL = "partial"            # Partial refund
    PENALTY = "penalty"            # Creator banned + funds redistributed

class CommitteeVote(Enum):
    UPHOLD = "uphold"
    OVERTURN = "overturn"
    PARTIAL = "partial"
    ABSTAIN = "abstain"


# ============ CORE MODELS ============

@dataclass
class User:
    user_id: str
    username: str
    role: UserRole
    balance: float = 10000.0  # Starting balance
    reputation_score: float = 1.0  # 0-1 scale
    is_verified: bool = False
    is_banned: bool = False
    created_at: float = 0.0  # Simulation timestamp (day number)
    total_trades: int = 0
    total_pnl: float = 0.0
    associated_accounts: List[str] = field(default_factory=list)  # For sybil detection

    def can_trade(self) -> bool:
        return not self.is_banned and self.balance > 0


@dataclass
class Song:
    song_id: str
    creator_id: str
    title: str
    genre: str
    status: SongStatus = SongStatus.PRE_RELEASE
    submitted_at: float = 0.0  # Simulation day
    stream_count: int = 0
    is_verified: bool = False
    organic_stream_ratio: float = 1.0  # 1.0 = all organic
    true_organic_probability: float = 0.0  # Hidden true virality
    underground_following: float = 0.0
    bot_budget: float = 0.0  # If creator is gaming

    # Stream tracking
    daily_streams: List[int] = field(default_factory=list)
    stream_sources: Dict[str, int] = field(default_factory=dict)  # geo/device breakdown


@dataclass
class PredictionContract:
    contract_id: str
    song_id: str
    creator_id: str  # Who created the contract (can be any user, not just song creator)
    target_streams: int  # User-configurable: how many streams = "hit"
    target_period_days: int  # User-configurable: evaluation window

    # Market state
    yes_pool: float = 1000.0
    no_pool: float = 1000.0
    total_fees: float = 0.0
    total_volume: float = 0.0

    # Lifecycle
    created_at: float = 0.0
    trading_opens_at: float = 0.0
    expires_at: float = 0.0  # created_at + target_period_days
    status: ContractStatus = ContractStatus.OPEN
    resolution_result: Optional[bool] = None  # True = target met, False = not met

    # Price tracking
    price_history: List[float] = field(default_factory=lambda: [0.5])

    @property
    def yes_price(self) -> float:
        total = self.yes_pool + self.no_pool
        return self.yes_pool / total if total > 0 else 0.5

    @property
    def no_price(self) -> float:
        return 1.0 - self.yes_price

    @property
    def total_pool(self) -> float:
        return self.yes_pool + self.no_pool


@dataclass
class Trade:
    trade_id: str
    contract_id: str
    user_id: str
    side: TradeSide
    amount: float  # Total amount including fee
    net_amount: float  # Amount after fee
    shares: float
    fee_paid: float  # 20% platform fee
    price_at_trade: float
    timestamp: float = 0.0  # Simulation day


@dataclass
class Position:
    """Tracks a user's position in a specific contract"""
    user_id: str
    contract_id: str
    yes_shares: float = 0.0
    no_shares: float = 0.0
    total_invested: float = 0.0
    total_fees_paid: float = 0.0

    @property
    def net_position(self) -> str:
        if self.yes_shares > self.no_shares:
            return "long_yes"
        elif self.no_shares > self.yes_shares:
            return "long_no"
        return "neutral"


@dataclass
class ContractResolution:
    resolution_id: str
    contract_id: str
    actual_streams: int
    target_streams: int
    target_met: bool
    resolved_at: float  # Simulation day
    resolution_type: ResolutionType
    organic_stream_count: int = 0
    bot_stream_count: int = 0
    streams_invalidated: int = 0  # Streams removed by anti-cheat


@dataclass
class Dispute:
    dispute_id: str
    contract_id: str
    filed_by: str  # user_id
    dispute_type: DisputeType
    reason: str
    evidence: Dict = field(default_factory=dict)

    # Lifecycle
    status: DisputeStatus = DisputeStatus.FILED
    filed_at: float = 0.0  # Simulation day
    resolution_deadline: float = 0.0  # filed_at + 2 days
    resolved_at: Optional[float] = None

    # Resolution
    committee_votes: List[Dict] = field(default_factory=list)  # [{member_id, vote, reasoning}]
    outcome: Optional[DisputeOutcome] = None
    decision_summary: str = ""

    # Deposit
    deposit_amount: float = 0.0  # 5% of contract volume
    deposit_returned: bool = False


@dataclass
class DisputeVote:
    """Individual committee member's vote on a dispute"""
    member_id: str
    dispute_id: str
    vote: CommitteeVote
    reasoning: str
    voted_at: float = 0.0


@dataclass
class MarketplaceStats:
    """Aggregate marketplace statistics"""
    total_users: int = 0
    total_songs: int = 0
    total_contracts: int = 0
    total_trades: int = 0
    total_volume: float = 0.0
    total_fees_collected: float = 0.0
    platform_revenue: float = 0.0  # 50% of fees
    liquidity_pool: float = 0.0  # 30% of fees
    dispute_fund: float = 0.0  # 20% of fees
    contracts_resolved: int = 0
    contracts_disputed: int = 0
    contracts_voided: int = 0
    disputes_filed: int = 0
    disputes_upheld: int = 0
    disputes_overturned: int = 0
    bots_detected: int = 0
    creators_banned: int = 0
    avg_prediction_accuracy: float = 0.0


# ============ HELPER FUNCTIONS ============

def generate_id(prefix: str = "") -> str:
    """Generate a unique ID with optional prefix"""
    short_id = uuid.uuid4().hex[:8]
    return f"{prefix}_{short_id}" if prefix else short_id


def create_user(username: str, role: UserRole, day: float = 0.0, balance: float = 10000.0) -> User:
    return User(
        user_id=generate_id("user"),
        username=username,
        role=role,
        balance=balance,
        created_at=day
    )


def create_song(
    creator_id: str,
    title: str,
    genre: str,
    day: float = 0.0,
    true_organic_probability: float = 0.2,
    underground_following: float = 0.0,
    bot_budget: float = 0.0
) -> Song:
    return Song(
        song_id=generate_id("song"),
        creator_id=creator_id,
        title=title,
        genre=genre,
        submitted_at=day,
        true_organic_probability=true_organic_probability,
        underground_following=underground_following,
        bot_budget=bot_budget
    )


def create_contract(
    song_id: str,
    creator_id: str,
    target_streams: int,
    target_period_days: int,
    day: float = 0.0,
    initial_liquidity: float = 1000.0
) -> PredictionContract:
    return PredictionContract(
        contract_id=generate_id("contract"),
        song_id=song_id,
        creator_id=creator_id,
        target_streams=target_streams,
        target_period_days=target_period_days,
        yes_pool=initial_liquidity,
        no_pool=initial_liquidity,
        created_at=day,
        trading_opens_at=day,
        expires_at=day + target_period_days,
        status=ContractStatus.TRADING
    )

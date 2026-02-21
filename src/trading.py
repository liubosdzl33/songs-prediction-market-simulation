"""
Trading Engine for Music Prediction Marketplace

Manages the full lifecycle of prediction contracts with:
- 20% platform trading fee
- Constant product AMM for price discovery
- Position tracking per user per contract
- Contract resolution and payout distribution
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import numpy as np

from models import (
    User, Song, PredictionContract, Trade, Position,
    ContractResolution, MarketplaceStats,
    UserRole, SongStatus, ContractStatus, TradeSide, ResolutionType,
    generate_id, create_user, create_song, create_contract
)


# ============ FEE CONFIGURATION ============

PLATFORM_FEE_RATE = 0.20  # 20% of every trade

# How the 20% fee is split
FEE_SPLIT = {
    'platform_revenue': 0.50,   # 50% of fees -> platform
    'liquidity_pool': 0.30,     # 30% of fees -> liquidity reserves
    'dispute_fund': 0.20,       # 20% of fees -> dispute resolution fund
}


# ============ TRADING ENGINE ============

class MusicMarketplace:
    """
    Main marketplace orchestrator for the music prediction market.

    Handles user registration, song submission, contract creation,
    trading with 20% fee, and contract resolution.
    """

    def __init__(
        self,
        platform_fee: float = PLATFORM_FEE_RATE,
        initial_liquidity: float = 1000.0,
        min_bet: float = 1.0,
        max_bet: float = 50000.0
    ):
        self.platform_fee = platform_fee
        self.initial_liquidity = initial_liquidity
        self.min_bet = min_bet
        self.max_bet = max_bet

        # Storage
        self.users: Dict[str, User] = {}
        self.songs: Dict[str, Song] = {}
        self.contracts: Dict[str, PredictionContract] = {}
        self.trades: List[Trade] = []
        self.positions: Dict[str, Position] = {}  # key: "{user_id}:{contract_id}"
        self.resolutions: Dict[str, ContractResolution] = {}

        # Financial tracking
        self.total_fees_collected: float = 0.0
        self.platform_revenue: float = 0.0
        self.liquidity_pool: float = 0.0
        self.dispute_fund: float = 0.0

        # Stats
        self.stats = MarketplaceStats()

    # ============ USER MANAGEMENT ============

    def register_user(
        self,
        username: str,
        role: UserRole = UserRole.TRADER,
        balance: float = 10000.0,
        day: float = 0.0
    ) -> User:
        """Register a new user on the platform"""
        user = create_user(username, role, day, balance)
        self.users[user.user_id] = user
        self.stats.total_users += 1
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def ban_user(self, user_id: str):
        """Ban a user from trading"""
        user = self.users.get(user_id)
        if user:
            user.is_banned = True

    # ============ SONG MANAGEMENT ============

    def submit_song(
        self,
        creator_id: str,
        title: str,
        genre: str,
        day: float = 0.0,
        true_organic_probability: float = 0.2,
        underground_following: float = 0.0,
        bot_budget: float = 0.0
    ) -> Optional[Song]:
        """Submit a pre-release song to the platform"""
        creator = self.users.get(creator_id)
        if not creator:
            return None
        if creator.role != UserRole.CREATOR:
            return None

        song = create_song(
            creator_id=creator_id,
            title=title,
            genre=genre,
            day=day,
            true_organic_probability=true_organic_probability,
            underground_following=underground_following,
            bot_budget=bot_budget
        )
        self.songs[song.song_id] = song
        self.stats.total_songs += 1
        return song

    def get_song(self, song_id: str) -> Optional[Song]:
        return self.songs.get(song_id)

    # ============ CONTRACT MANAGEMENT ============

    def create_prediction_contract(
        self,
        song_id: str,
        creator_id: str,
        target_streams: int,
        target_period_days: int,
        day: float = 0.0,
        initial_liquidity: float = None
    ) -> Optional[PredictionContract]:
        """
        Create a new prediction contract.

        Any user can create a contract - they set:
        - target_streams: how many streams defines a "hit"
        - target_period_days: evaluation window (7, 14, 30, 60, 90 days)
        """
        song = self.songs.get(song_id)
        if not song:
            return None

        creator = self.users.get(creator_id)
        if not creator:
            return None

        liq = initial_liquidity if initial_liquidity is not None else self.initial_liquidity

        contract = create_contract(
            song_id=song_id,
            creator_id=creator_id,
            target_streams=target_streams,
            target_period_days=target_period_days,
            day=day,
            initial_liquidity=liq
        )

        self.contracts[contract.contract_id] = contract
        self.stats.total_contracts += 1
        return contract

    def get_contract(self, contract_id: str) -> Optional[PredictionContract]:
        return self.contracts.get(contract_id)

    def get_contract_price(self, contract_id: str) -> Optional[float]:
        """Get current YES price for a contract"""
        contract = self.contracts.get(contract_id)
        if contract:
            return contract.yes_price
        return None

    def get_contracts_for_song(self, song_id: str) -> List[PredictionContract]:
        """Get all contracts for a given song"""
        return [c for c in self.contracts.values() if c.song_id == song_id]

    # ============ TRADING ============

    def place_trade(
        self,
        user_id: str,
        contract_id: str,
        side: str,
        amount: float,
        day: float = 0.0
    ) -> Optional[Trade]:
        """
        Place a trade on a prediction contract.

        Platform takes 20% fee on every trade.

        Args:
            user_id: Who is trading
            contract_id: Which contract
            side: 'yes' or 'no'
            amount: Total trade amount (fee will be deducted)
            day: Current simulation day

        Returns:
            Trade record or None if trade is invalid
        """
        # Validate
        user = self.users.get(user_id)
        if not user or not user.can_trade():
            return None

        contract = self.contracts.get(contract_id)
        if not contract or contract.status != ContractStatus.TRADING:
            return None

        if side not in ('yes', 'no'):
            return None

        if amount < self.min_bet or amount > self.max_bet:
            return None

        if user.balance < amount:
            return None

        # Check contract hasn't expired
        if day > contract.expires_at:
            return None

        # Calculate fee (20%)
        fee = amount * self.platform_fee
        net_amount = amount - fee

        # Current price
        trade_side = TradeSide.YES if side == 'yes' else TradeSide.NO
        if trade_side == TradeSide.YES:
            price = contract.yes_price
        else:
            price = contract.no_price

        # Calculate shares
        if price <= 0:
            return None
        shares = net_amount / price

        # Update contract pools
        if trade_side == TradeSide.YES:
            contract.yes_pool += net_amount
        else:
            contract.no_pool += net_amount

        contract.total_fees += fee
        contract.total_volume += amount
        contract.price_history.append(contract.yes_price)

        # Update user balance
        user.balance -= amount
        user.total_trades += 1

        # Distribute fee
        platform_cut = fee * FEE_SPLIT['platform_revenue']
        liquidity_cut = fee * FEE_SPLIT['liquidity_pool']
        dispute_cut = fee * FEE_SPLIT['dispute_fund']

        self.total_fees_collected += fee
        self.platform_revenue += platform_cut
        self.liquidity_pool += liquidity_cut
        self.dispute_fund += dispute_cut

        # Create trade record
        trade = Trade(
            trade_id=generate_id("trade"),
            contract_id=contract_id,
            user_id=user_id,
            side=trade_side,
            amount=amount,
            net_amount=net_amount,
            shares=shares,
            fee_paid=fee,
            price_at_trade=price,
            timestamp=day
        )
        self.trades.append(trade)
        self.stats.total_trades += 1
        self.stats.total_volume += amount
        self.stats.total_fees_collected += fee

        # Update position
        pos_key = f"{user_id}:{contract_id}"
        if pos_key not in self.positions:
            self.positions[pos_key] = Position(
                user_id=user_id,
                contract_id=contract_id
            )

        pos = self.positions[pos_key]
        if trade_side == TradeSide.YES:
            pos.yes_shares += shares
        else:
            pos.no_shares += shares
        pos.total_invested += amount
        pos.total_fees_paid += fee

        return trade

    # ============ RESOLUTION ============

    def resolve_contract(
        self,
        contract_id: str,
        actual_streams: int,
        day: float = 0.0,
        organic_streams: int = 0,
        bot_streams: int = 0,
        streams_invalidated: int = 0,
        resolution_type: ResolutionType = ResolutionType.AUTOMATIC
    ) -> Optional[ContractResolution]:
        """
        Resolve a prediction contract based on actual stream counts.

        Compares actual_streams against target_streams to determine
        if the YES or NO side wins.
        """
        contract = self.contracts.get(contract_id)
        if not contract:
            return None

        if contract.status not in (ContractStatus.TRADING, ContractStatus.OPEN):
            return None

        # Determine outcome
        effective_streams = actual_streams - streams_invalidated
        target_met = effective_streams >= contract.target_streams

        contract.status = ContractStatus.RESOLVED
        contract.resolution_result = target_met

        resolution = ContractResolution(
            resolution_id=generate_id("resolution"),
            contract_id=contract_id,
            actual_streams=actual_streams,
            target_streams=contract.target_streams,
            target_met=target_met,
            resolved_at=day,
            resolution_type=resolution_type,
            organic_stream_count=organic_streams,
            bot_stream_count=bot_streams,
            streams_invalidated=streams_invalidated
        )

        self.resolutions[contract_id] = resolution
        self.stats.contracts_resolved += 1

        # Calculate payouts
        self._distribute_payouts(contract, target_met)

        return resolution

    def void_contract(self, contract_id: str, day: float = 0.0) -> bool:
        """
        Void a contract (e.g., due to detected manipulation).
        All traders get refunded their net amounts (fees not returned).
        """
        contract = self.contracts.get(contract_id)
        if not contract:
            return False

        contract.status = ContractStatus.VOIDED
        self.stats.contracts_voided += 1

        # Refund all traders their net invested amounts
        contract_trades = [t for t in self.trades if t.contract_id == contract_id]
        for trade in contract_trades:
            user = self.users.get(trade.user_id)
            if user:
                user.balance += trade.net_amount  # Refund net (fee not returned)

        return True

    def dispute_contract(self, contract_id: str) -> bool:
        """Mark a contract as disputed (payouts frozen)"""
        contract = self.contracts.get(contract_id)
        if not contract:
            return False

        contract.status = ContractStatus.DISPUTED
        self.stats.contracts_disputed += 1
        return True

    def _distribute_payouts(self, contract: PredictionContract, target_met: bool):
        """
        Distribute payouts to winning side.

        Winners split the total pool proportional to their shares.
        Losers receive nothing.
        """
        winning_side = TradeSide.YES if target_met else TradeSide.NO
        winning_pool = contract.yes_pool if target_met else contract.no_pool

        if winning_pool <= 0:
            return

        payout_per_share = contract.total_pool / winning_pool

        # Find all positions for this contract
        for pos_key, pos in self.positions.items():
            if pos.contract_id != contract.contract_id:
                continue

            user = self.users.get(pos.user_id)
            if not user:
                continue

            # Calculate payout
            if winning_side == TradeSide.YES:
                payout = pos.yes_shares * payout_per_share
            else:
                payout = pos.no_shares * payout_per_share

            # Credit user
            user.balance += payout
            user.total_pnl += payout - pos.total_invested

    # ============ QUERIES ============

    def get_user_positions(self, user_id: str) -> List[Position]:
        """Get all positions for a user"""
        return [p for p in self.positions.values() if p.user_id == user_id]

    def get_contract_trades(self, contract_id: str) -> List[Trade]:
        """Get all trades for a contract"""
        return [t for t in self.trades if t.contract_id == contract_id]

    def get_user_trades(self, user_id: str) -> List[Trade]:
        """Get all trades for a user"""
        return [t for t in self.trades if t.user_id == user_id]

    def get_active_contracts(self) -> List[PredictionContract]:
        """Get all currently trading contracts"""
        return [
            c for c in self.contracts.values()
            if c.status == ContractStatus.TRADING
        ]

    def get_marketplace_summary(self) -> Dict:
        """Get a summary of marketplace activity"""
        self.stats.platform_revenue = self.platform_revenue
        self.stats.liquidity_pool = self.liquidity_pool
        self.stats.dispute_fund = self.dispute_fund

        active = len([c for c in self.contracts.values() if c.status == ContractStatus.TRADING])
        resolved = len([c for c in self.contracts.values() if c.status == ContractStatus.RESOLVED])
        disputed = len([c for c in self.contracts.values() if c.status == ContractStatus.DISPUTED])
        voided = len([c for c in self.contracts.values() if c.status == ContractStatus.VOIDED])

        # Prediction accuracy
        resolved_contracts = [
            c for c in self.contracts.values() if c.status == ContractStatus.RESOLVED
        ]
        if resolved_contracts:
            correct_predictions = sum(
                1 for c in resolved_contracts
                if (c.yes_price > 0.5) == c.resolution_result
            )
            accuracy = correct_predictions / len(resolved_contracts)
        else:
            accuracy = 0.0

        # User P&L distribution
        user_pnls = [u.total_pnl for u in self.users.values() if u.total_trades > 0]

        return {
            'total_users': len(self.users),
            'total_songs': len(self.songs),
            'total_contracts': len(self.contracts),
            'active_contracts': active,
            'resolved_contracts': resolved,
            'disputed_contracts': disputed,
            'voided_contracts': voided,
            'total_trades': len(self.trades),
            'total_volume': self.stats.total_volume,
            'total_fees_collected': self.total_fees_collected,
            'platform_revenue': self.platform_revenue,
            'liquidity_pool': self.liquidity_pool,
            'dispute_fund': self.dispute_fund,
            'prediction_accuracy': accuracy,
            'avg_user_pnl': float(np.mean(user_pnls)) if user_pnls else 0,
            'median_user_pnl': float(np.median(user_pnls)) if user_pnls else 0,
        }

    # ============ INSIDER P&L (backward compat) ============

    def get_insider_pnl(
        self,
        contract_id: str,
        creator_user_id: str
    ) -> float:
        """Calculate P&L for a song creator's insider bets"""
        pos_key = f"{creator_user_id}:{contract_id}"
        pos = self.positions.get(pos_key)
        if not pos:
            return 0.0

        contract = self.contracts.get(contract_id)
        if not contract or contract.resolution_result is None:
            return 0.0

        winning_side = TradeSide.YES if contract.resolution_result else TradeSide.NO
        winning_pool = contract.yes_pool if contract.resolution_result else contract.no_pool

        if winning_pool <= 0:
            return -pos.total_invested

        payout_per_share = contract.total_pool / winning_pool

        if winning_side == TradeSide.YES:
            payout = pos.yes_shares * payout_per_share
        else:
            payout = pos.no_shares * payout_per_share

        return payout - pos.total_invested


# ============ STREAM SIMULATION ============

def simulate_contract_streams(
    song: Song,
    contract: PredictionContract,
    bot_detection_rate: float = 0.75,
    bot_cost_per_1000: float = 2.0
) -> Dict:
    """
    Simulate stream accumulation over a contract's target period.

    Returns stream data including organic, bot, and daily breakdowns.
    """
    period_days = contract.target_period_days

    # Base daily organic streams (exponential with organic probability)
    base_daily = song.true_organic_probability * 50000
    following_boost = song.underground_following * 25000

    daily_organic = []
    daily_bot = []
    total_organic = 0
    total_bot = 0

    for day in range(period_days):
        # Organic streams with decay and variance
        growth_factor = max(0.5, 1.0 + 0.3 * np.log1p(day) - 0.05 * day)
        daily_org = int(np.random.exponential(
            (base_daily + following_boost) * growth_factor
        ))
        daily_organic.append(daily_org)
        total_organic += daily_org

        # Bot streams (if any budget)
        if song.bot_budget > 0:
            daily_bot_budget = song.bot_budget / period_days
            raw_bot = int(daily_bot_budget / bot_cost_per_1000 * 1000)
            detected = int(raw_bot * bot_detection_rate)
            effective_bot = raw_bot - detected
            daily_bot.append(effective_bot)
            total_bot += effective_bot
        else:
            daily_bot.append(0)

    total_streams = total_organic + total_bot

    # Raw bot streams (before detection)
    raw_bot_total = 0
    if song.bot_budget > 0:
        raw_bot_total = int(song.bot_budget / bot_cost_per_1000 * 1000)

    return {
        'total_streams': total_streams,
        'organic_streams': total_organic,
        'bot_streams': total_bot,
        'raw_bot_streams': raw_bot_total,
        'detected_removed': raw_bot_total - total_bot,
        'daily_organic': daily_organic,
        'daily_bot': daily_bot,
        'daily_total': [o + b for o, b in zip(daily_organic, daily_bot)],
        'hit_target': total_streams >= contract.target_streams,
        'target_streams': contract.target_streams,
        'period_days': period_days,
    }

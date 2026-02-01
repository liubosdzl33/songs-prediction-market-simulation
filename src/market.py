"""
Betting Market Implementation
Constant Product AMM for YES/NO prediction markets
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import numpy as np


@dataclass
class Bet:
    """Individual bet record"""
    bet_id: str
    day: int
    agent_type: str
    amount: float
    side: str  # 'yes' or 'no'
    price_at_bet: float
    shares: float
    fee_paid: float


@dataclass
class MarketState:
    """Current state of a prediction market"""
    yes_pool: float = 1000.0
    no_pool: float = 1000.0
    total_fees: float = 0.0
    total_volume: float = 0.0
    bets: List[Bet] = field(default_factory=list)
    price_history: List[float] = field(default_factory=lambda: [0.5])
    
    @property
    def yes_price(self) -> float:
        """Current implied probability of YES outcome"""
        return self.yes_pool / (self.yes_pool + self.no_pool)
    
    @property
    def no_price(self) -> float:
        """Current implied probability of NO outcome"""
        return 1 - self.yes_price
    
    @property
    def total_pool(self) -> float:
        """Total liquidity in market"""
        return self.yes_pool + self.no_pool


class PredictionMarket:
    """
    Constant Product AMM for binary prediction markets.
    
    Implements: YES_pool × NO_pool = k (invariant)
    
    When a user bets on YES:
    1. Fee is deducted
    2. Net amount added to YES pool
    3. User receives shares = amount / current_yes_price
    
    At resolution:
    - Winners split the total pool proportional to shares
    - Losers get nothing
    """
    
    def __init__(
        self,
        initial_liquidity: float = 1000.0,
        platform_fee: float = 0.02,
        artist_fee_share: float = 0.40,
        promotion_fee_share: float = 0.30,
        platform_fee_share: float = 0.20,
        insurance_fee_share: float = 0.10
    ):
        self.initial_liquidity = initial_liquidity
        self.platform_fee = platform_fee
        
        # Fee distribution
        self.artist_fee_share = artist_fee_share
        self.promotion_fee_share = promotion_fee_share
        self.platform_fee_share = platform_fee_share
        self.insurance_fee_share = insurance_fee_share
        
        self.state = MarketState(
            yes_pool=initial_liquidity,
            no_pool=initial_liquidity
        )
        self._bet_counter = 0
    
    def place_bet(
        self,
        amount: float,
        side: str,
        agent_type: str,
        day: int
    ) -> Bet:
        """
        Place a bet on the market.
        
        Args:
            amount: Bet size in USD
            side: 'yes' or 'no'
            agent_type: Type of agent placing bet
            day: Day number of bet
            
        Returns:
            Bet record with shares received
        """
        if side not in ('yes', 'no'):
            raise ValueError("Side must be 'yes' or 'no'")
        if amount <= 0:
            raise ValueError("Bet amount must be positive")
        
        # Calculate fee and net amount
        fee = amount * self.platform_fee
        net_amount = amount - fee
        
        # Current price
        price = self.state.yes_price if side == 'yes' else self.state.no_price
        
        # Calculate shares
        shares = net_amount / price
        
        # Update pools
        if side == 'yes':
            self.state.yes_pool += net_amount
        else:
            self.state.no_pool += net_amount
        
        # Update state
        self.state.total_fees += fee
        self.state.total_volume += amount
        self.state.price_history.append(self.state.yes_price)
        
        # Create bet record
        self._bet_counter += 1
        bet = Bet(
            bet_id=f"bet_{self._bet_counter}",
            day=day,
            agent_type=agent_type,
            amount=amount,
            side=side,
            price_at_bet=price,
            shares=shares,
            fee_paid=fee
        )
        self.state.bets.append(bet)
        
        return bet
    
    def resolve(self, outcome: bool) -> Dict[str, float]:
        """
        Resolve the market.
        
        Args:
            outcome: True if YES wins (hit 1M), False if NO wins
            
        Returns:
            Dict with resolution details
        """
        winning_side = 'yes' if outcome else 'no'
        winning_pool = self.state.yes_pool if outcome else self.state.no_pool
        
        # Calculate payout per share
        payout_per_share = self.state.total_pool / winning_pool if winning_pool > 0 else 0
        
        # Calculate fee distribution
        fee_distribution = {
            'artist': self.state.total_fees * self.artist_fee_share,
            'promotion': self.state.total_fees * self.promotion_fee_share,
            'platform': self.state.total_fees * self.platform_fee_share,
            'insurance': self.state.total_fees * self.insurance_fee_share,
        }
        
        return {
            'outcome': outcome,
            'winning_side': winning_side,
            'total_pool': self.state.total_pool,
            'winning_pool': winning_pool,
            'payout_per_share': payout_per_share,
            'total_fees': self.state.total_fees,
            'fee_distribution': fee_distribution,
            'total_volume': self.state.total_volume,
            'final_price': self.state.yes_price,
            'num_bets': len(self.state.bets),
        }
    
    def get_bettor_payout(self, bet: Bet, outcome: bool) -> float:
        """Calculate payout for a specific bet"""
        winning_side = 'yes' if outcome else 'no'
        
        if bet.side != winning_side:
            return 0.0
        
        winning_pool = self.state.yes_pool if outcome else self.state.no_pool
        payout_per_share = self.state.total_pool / winning_pool
        
        return bet.shares * payout_per_share
    
    def get_insider_pnl(self, insider_bet: float, outcome: bool) -> float:
        """
        Calculate P&L for an insider (artist) bet.
        Assumes insider bet was placed at market open.
        """
        if insider_bet <= 0:
            return 0.0
        
        # Find insider bet(s)
        insider_bets = [b for b in self.state.bets if b.agent_type == 'insider']
        
        total_payout = sum(self.get_bettor_payout(b, outcome) for b in insider_bets)
        total_bet = sum(b.amount for b in insider_bets)
        
        return total_payout - total_bet


def calculate_shares(
    bet_amount: float,
    is_yes: bool,
    yes_pool: float,
    no_pool: float,
    fee_rate: float
) -> tuple:
    """
    Standalone function to calculate shares for a bet.
    
    Returns:
        (shares, fee, net_bet)
    """
    fee = bet_amount * fee_rate
    net_bet = bet_amount - fee
    
    price = yes_pool / (yes_pool + no_pool) if is_yes else no_pool / (yes_pool + no_pool)
    shares = net_bet / price
    
    return shares, fee, net_bet

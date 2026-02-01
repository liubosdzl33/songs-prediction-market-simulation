"""
Bettor Agent Behaviors
Different types of market participants with varying strategies
"""

from dataclasses import dataclass
from typing import Tuple, Optional
from enum import Enum
import numpy as np


class AgentType(Enum):
    """Types of betting agents"""
    NOISE = "noise"           # Random bettors
    INFORMED = "informed"     # Know true probability
    WHALE = "whale"           # Large bets, slight edge
    ARBITRAGEUR = "arb"       # Price correctors
    INSIDER = "insider"       # Artist/team (gaming)


@dataclass
class AgentConfig:
    """Configuration for agent behavior"""
    # Agent mix (should sum to 1.0)
    noise_pct: float = 0.60
    informed_pct: float = 0.20
    whale_pct: float = 0.10
    arb_pct: float = 0.10
    
    # Informed trader parameters
    informed_edge: float = 0.10  # How close to true probability
    
    # Whale parameters
    whale_multiplier: float = 10.0  # Bet size multiplier
    
    # Arbitrageur parameters
    arb_threshold: float = 0.15  # Price deviation to trigger


class BettingAgent:
    """
    Simulates betting behavior for different agent types.
    """
    
    def __init__(self, config: AgentConfig = None):
        self.config = config or AgentConfig()
    
    def sample_agent_type(self) -> AgentType:
        """Randomly sample an agent type based on configured mix"""
        r = np.random.random()
        
        cumulative = 0.0
        for agent_type, pct in [
            (AgentType.NOISE, self.config.noise_pct),
            (AgentType.INFORMED, self.config.informed_pct),
            (AgentType.WHALE, self.config.whale_pct),
            (AgentType.ARBITRAGEUR, self.config.arb_pct),
        ]:
            cumulative += pct
            if r < cumulative:
                return agent_type
        
        return AgentType.NOISE
    
    def get_bet_decision(
        self,
        agent_type: AgentType,
        current_price: float,
        true_probability: float,
        info_leakage: float = 0.0
    ) -> Tuple[Optional[bool], str]:
        """
        Determine if and how an agent bets.
        
        Args:
            agent_type: Type of agent
            current_price: Current YES price (implied probability)
            true_probability: Actual probability of hitting 1M
            info_leakage: Information leakage (0-1) from underground following
            
        Returns:
            (bet_yes, reasoning) - bet_yes is None if agent skips
        """
        if agent_type == AgentType.NOISE:
            # Random betting
            bet_yes = np.random.random() < 0.5
            return bet_yes, "random"
        
        elif agent_type == AgentType.INFORMED:
            # Knows true probability with some error
            perceived = true_probability + np.random.uniform(
                -self.config.informed_edge,
                self.config.informed_edge
            )
            # Also influenced by info leakage
            perceived += info_leakage * 0.3
            perceived = np.clip(perceived, 0, 1)
            
            # Bet if market misprices by enough
            if current_price < perceived - 0.05:
                return True, "underpriced"
            elif current_price > perceived + 0.05:
                return False, "overpriced"
            else:
                return np.random.random() < 0.5, "marginal"
        
        elif agent_type == AgentType.WHALE:
            # Slight edge, follows true probability loosely
            bet_yes = np.random.random() < true_probability
            return bet_yes, "whale_edge"
        
        elif agent_type == AgentType.ARBITRAGEUR:
            # Only bets if price significantly deviates from 0.5
            deviation = abs(current_price - 0.5)
            if deviation < self.config.arb_threshold:
                return None, "no_opportunity"
            
            # Push price back toward 0.5
            bet_yes = current_price < 0.5
            return bet_yes, "arbitrage"
        
        else:
            return None, "unknown_agent"
    
    def get_bet_size(
        self,
        agent_type: AgentType,
        base_median: float = 25.0,
        sigma: float = 1.2
    ) -> float:
        """
        Sample bet size for an agent.
        
        Uses log-normal distribution with agent-specific adjustments.
        """
        base_size = np.random.lognormal(
            mean=np.log(base_median),
            sigma=sigma
        )
        
        # Clamp to reasonable range
        base_size = max(5, min(1000, base_size))
        
        # Whale multiplier
        if agent_type == AgentType.WHALE:
            base_size *= self.config.whale_multiplier
        
        return base_size


def simulate_daily_bettors(
    n_bettors: int,
    current_price: float,
    true_probability: float,
    info_leakage: float,
    agent: BettingAgent,
    bet_size_median: float = 25.0
) -> list:
    """
    Simulate all bettors for one day.
    
    Returns:
        List of (agent_type, bet_size, is_yes) tuples
    """
    bets = []
    
    for _ in range(n_bettors):
        agent_type = agent.sample_agent_type()
        
        bet_yes, reason = agent.get_bet_decision(
            agent_type=agent_type,
            current_price=current_price,
            true_probability=true_probability,
            info_leakage=info_leakage
        )
        
        if bet_yes is None:
            continue  # Agent skips
        
        bet_size = agent.get_bet_size(agent_type, bet_size_median)
        
        bets.append({
            'agent_type': agent_type.value,
            'amount': bet_size,
            'is_yes': bet_yes,
            'reason': reason
        })
    
    return bets

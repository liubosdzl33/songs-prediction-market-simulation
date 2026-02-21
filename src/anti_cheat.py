"""
Anti-Cheating System for Music Prediction Marketplace

Prevents song creators from gaming the market through:
- Bot stream detection
- Creator self-trading restrictions
- Sybil account detection
- Stream audit verification
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum
import numpy as np


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class BotDetectionResult:
    """Result of bot stream analysis"""
    song_id: str
    is_suspicious: bool
    confidence: float  # 0-1
    risk_level: RiskLevel

    # Detection signals
    geographic_anomaly: float = 0.0  # 0-1, concentration in unusual regions
    temporal_anomaly: float = 0.0  # 0-1, unusual time-of-day patterns
    repeat_listener_ratio: float = 0.0  # Fraction of single-play accounts
    device_diversity_score: float = 0.0  # 0-1, low = suspicious
    velocity_anomaly: float = 0.0  # 0-1, sudden spikes
    organic_ratio: float = 1.0  # Estimated organic / total streams

    estimated_bot_streams: int = 0
    estimated_organic_streams: int = 0
    flags: List[str] = field(default_factory=list)


@dataclass
class SybilResult:
    """Result of Sybil account detection"""
    target_user_id: str
    is_sybil: bool
    confidence: float
    linked_accounts: List[str] = field(default_factory=list)
    coordination_score: float = 0.0  # 0-1
    wash_trading_detected: bool = False
    flags: List[str] = field(default_factory=list)


@dataclass
class AuditResult:
    """Result of stream audit"""
    song_id: str
    claimed_streams: int
    verified_streams: int
    organic_streams: int
    artificial_streams: int
    organic_ratio: float
    passes_audit: bool  # True if organic_ratio > 0.70
    penalty_applied: bool = False
    contract_voided: bool = False
    flags: List[str] = field(default_factory=list)


@dataclass
class CreatorRestrictionCheck:
    """Result of checking creator trading restrictions"""
    user_id: str
    song_id: str
    can_trade: bool
    reason: str = ""
    violations: List[str] = field(default_factory=list)


@dataclass
class AntiCheatReport:
    """Combined anti-cheat analysis report"""
    song_id: str
    overall_risk: RiskLevel
    overall_score: float  # 0-1, higher = more suspicious

    bot_detection: Optional[BotDetectionResult] = None
    sybil_results: List[SybilResult] = field(default_factory=list)
    audit_result: Optional[AuditResult] = None
    creator_violations: List[str] = field(default_factory=list)

    recommended_action: str = "none"  # none, manual_review, void_contract, ban_creator
    should_void: bool = False
    should_ban_creator: bool = False


class BotPurchaseDetector:
    """
    Detects bot/fake stream purchases by analyzing stream patterns.

    In a real system this would use ML models; here we simulate detection
    using statistical heuristics on the stream data.
    """

    def __init__(
        self,
        base_detection_rate: float = 0.75,
        geographic_weight: float = 0.20,
        temporal_weight: float = 0.15,
        repeat_listener_weight: float = 0.25,
        device_weight: float = 0.15,
        velocity_weight: float = 0.25
    ):
        self.base_detection_rate = base_detection_rate
        self.weights = {
            'geographic': geographic_weight,
            'temporal': temporal_weight,
            'repeat_listener': repeat_listener_weight,
            'device': device_weight,
            'velocity': velocity_weight,
        }

    def detect_bot_streams(
        self,
        song_id: str,
        total_streams: int,
        organic_streams: int,
        bot_streams: int,
        daily_streams: List[int] = None,
        bot_budget: float = 0.0
    ) -> BotDetectionResult:
        """
        Analyze stream data for bot activity.

        In the simulation, we know ground truth (organic vs bot) but the
        detector operates with noise to simulate real-world uncertainty.
        """
        flags = []

        if total_streams == 0:
            return BotDetectionResult(
                song_id=song_id,
                is_suspicious=False,
                confidence=0.0,
                risk_level=RiskLevel.LOW,
                organic_ratio=1.0
            )

        actual_bot_ratio = bot_streams / total_streams if total_streams > 0 else 0

        # === Signal 1: Geographic concentration ===
        # Bot farms tend to concentrate in specific regions
        # Higher bot ratio -> higher geographic anomaly (with noise)
        geo_anomaly = np.clip(
            actual_bot_ratio * 0.8 + np.random.normal(0, 0.1), 0, 1
        )
        if geo_anomaly > 0.4:
            flags.append("geographic_concentration_detected")

        # === Signal 2: Temporal patterns ===
        # Bots stream at unusual hours, too evenly across time
        temporal_anomaly = np.clip(
            actual_bot_ratio * 0.7 + np.random.normal(0, 0.12), 0, 1
        )
        if temporal_anomaly > 0.45:
            flags.append("abnormal_temporal_pattern")

        # === Signal 3: Repeat listener ratio ===
        # Bot accounts typically play once and never return
        # Organic listeners have higher repeat rates
        organic_repeat_rate = np.random.uniform(0.3, 0.6)  # Normal repeat rate
        bot_repeat_rate = np.random.uniform(0.01, 0.05)  # Bots rarely repeat
        blended_repeat = (
            organic_repeat_rate * (organic_streams / max(total_streams, 1)) +
            bot_repeat_rate * (bot_streams / max(total_streams, 1))
        )
        repeat_anomaly = np.clip(1.0 - blended_repeat / 0.4, 0, 1)  # Low repeat = suspicious
        if repeat_anomaly > 0.5:
            flags.append("low_repeat_listener_rate")

        # === Signal 4: Device diversity ===
        # Bots use limited device types / cheap phones
        device_score = np.clip(
            1.0 - actual_bot_ratio * 0.9 + np.random.normal(0, 0.08), 0, 1
        )
        device_anomaly = 1.0 - device_score  # Invert: low diversity = high anomaly
        if device_anomaly > 0.5:
            flags.append("low_device_diversity")

        # === Signal 5: Velocity anomaly ===
        # Check for sudden spikes in streams (bot campaigns start abruptly)
        if daily_streams and len(daily_streams) > 2:
            max_daily = max(daily_streams)
            avg_daily = np.mean(daily_streams) if np.mean(daily_streams) > 0 else 1
            spike_ratio = max_daily / avg_daily
            velocity_anomaly = np.clip((spike_ratio - 2.0) / 8.0, 0, 1)
        else:
            velocity_anomaly = np.clip(
                actual_bot_ratio * 0.6 + np.random.normal(0, 0.15), 0, 1
            )
        if velocity_anomaly > 0.4:
            flags.append("stream_velocity_spike")

        # === Composite score ===
        composite_score = (
            geo_anomaly * self.weights['geographic'] +
            temporal_anomaly * self.weights['temporal'] +
            repeat_anomaly * self.weights['repeat_listener'] +
            device_anomaly * self.weights['device'] +
            velocity_anomaly * self.weights['velocity']
        )

        # Apply detection noise
        composite_score = np.clip(
            composite_score + np.random.normal(0, 0.05), 0, 1
        )

        # Determine risk level
        if composite_score >= 0.7:
            risk_level = RiskLevel.CRITICAL
        elif composite_score >= 0.5:
            risk_level = RiskLevel.HIGH
        elif composite_score >= 0.3:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW

        is_suspicious = composite_score >= 0.4

        # Estimate bot streams (noisy estimate)
        estimated_bot = int(total_streams * composite_score * np.random.uniform(0.8, 1.2))
        estimated_organic = total_streams - estimated_bot

        return BotDetectionResult(
            song_id=song_id,
            is_suspicious=is_suspicious,
            confidence=min(composite_score * 1.2, 1.0),
            risk_level=risk_level,
            geographic_anomaly=geo_anomaly,
            temporal_anomaly=temporal_anomaly,
            repeat_listener_ratio=repeat_anomaly,
            device_diversity_score=device_score,
            velocity_anomaly=velocity_anomaly,
            organic_ratio=max(0, 1.0 - composite_score),
            estimated_bot_streams=max(0, estimated_bot),
            estimated_organic_streams=max(0, estimated_organic),
            flags=flags
        )


class CreatorRestrictions:
    """
    Enforces trading restrictions on song creators to prevent insider trading.

    Rules:
    1. Creators CANNOT trade on their own songs' contracts
    2. Associated accounts (same cluster) are also restricted
    3. Cooling-off period: 24h (1 day) after song submission
    4. Maximum position limits for creator-adjacent accounts
    """

    def __init__(self, cooling_off_days: float = 1.0, max_insider_position_pct: float = 0.10):
        self.cooling_off_days = cooling_off_days
        self.max_insider_position_pct = max_insider_position_pct
        # Maps creator_id -> set of associated user_ids
        self.creator_associations: Dict[str, set] = {}

    def register_association(self, creator_id: str, associated_user_id: str):
        """Register an associated account for a creator"""
        if creator_id not in self.creator_associations:
            self.creator_associations[creator_id] = set()
        self.creator_associations[creator_id].add(associated_user_id)

    def check_can_trade(
        self,
        user_id: str,
        song_creator_id: str,
        song_submitted_at: float,
        current_day: float,
        contract_volume: float = 0.0,
        user_position_value: float = 0.0
    ) -> CreatorRestrictionCheck:
        """
        Check if a user is allowed to trade on a song's contract.
        """
        violations = []

        # Rule 1: Creator self-trading ban
        if user_id == song_creator_id:
            violations.append("creator_self_trading_banned")
            return CreatorRestrictionCheck(
                user_id=user_id,
                song_id="",
                can_trade=False,
                reason="Song creators cannot trade on their own songs' prediction contracts",
                violations=violations
            )

        # Rule 2: Associated account check
        associated = self.creator_associations.get(song_creator_id, set())
        if user_id in associated:
            violations.append("associated_account_restricted")
            return CreatorRestrictionCheck(
                user_id=user_id,
                song_id="",
                can_trade=False,
                reason="Account is associated with the song creator and cannot trade",
                violations=violations
            )

        # Rule 3: Cooling-off period
        days_since_submission = current_day - song_submitted_at
        if days_since_submission < self.cooling_off_days:
            violations.append("cooling_off_period_active")
            return CreatorRestrictionCheck(
                user_id=user_id,
                song_id="",
                can_trade=False,
                reason=f"Trading not yet open. Cooling-off period: {self.cooling_off_days} days after submission",
                violations=violations
            )

        # Rule 4: Position limits for suspicious accounts
        if contract_volume > 0 and user_position_value > 0:
            position_pct = user_position_value / contract_volume
            if position_pct > self.max_insider_position_pct:
                violations.append("position_limit_exceeded")
                # Don't block, just flag for monitoring

        return CreatorRestrictionCheck(
            user_id=user_id,
            song_id="",
            can_trade=True,
            reason="Trade allowed" if not violations else "Trade allowed with warnings",
            violations=violations
        )


class SybilDetection:
    """
    Detects coordinated fake accounts (Sybil attacks) in trading.

    Analyzes:
    - Coordinated trading patterns (same timing, same direction)
    - Wash trading (same entity on both sides)
    - Account cluster analysis
    """

    def __init__(
        self,
        coordination_threshold: float = 0.6,
        wash_trade_threshold: float = 0.7
    ):
        self.coordination_threshold = coordination_threshold
        self.wash_trade_threshold = wash_trade_threshold

    def detect_sybil_accounts(
        self,
        user_id: str,
        user_trades: List[Dict],
        all_contract_trades: List[Dict],
        known_associations: Dict[str, set] = None
    ) -> SybilResult:
        """
        Detect if a user is part of a Sybil network.

        Simulates detection by checking trading pattern similarity.
        """
        flags = []
        linked = []

        if not user_trades or not all_contract_trades:
            return SybilResult(
                target_user_id=user_id,
                is_sybil=False,
                confidence=0.0
            )

        # Check for coordinated trading: users who always trade same direction
        # at similar times on the same contracts
        user_contract_sides = {}
        for t in user_trades:
            key = t.get('contract_id', '')
            user_contract_sides[key] = t.get('side', '')

        other_users = {}
        for t in all_contract_trades:
            uid = t.get('user_id', '')
            if uid == user_id:
                continue
            if uid not in other_users:
                other_users[uid] = {}
            key = t.get('contract_id', '')
            other_users[uid][key] = t.get('side', '')

        # Compare trading patterns
        for other_id, other_sides in other_users.items():
            common_contracts = set(user_contract_sides.keys()) & set(other_sides.keys())
            if len(common_contracts) < 2:
                continue

            same_side_count = sum(
                1 for c in common_contracts
                if user_contract_sides[c] == other_sides[c]
            )
            coordination = same_side_count / len(common_contracts)

            if coordination >= self.coordination_threshold:
                linked.append(other_id)
                flags.append(f"coordinated_trading_with_{other_id}")

        # Check for wash trading
        wash_detected = False
        user_yes_contracts = {c for c, s in user_contract_sides.items() if s == 'yes'}
        user_no_contracts = {c for c, s in user_contract_sides.items() if s == 'no'}

        for other_id in linked:
            other_sides = other_users.get(other_id, {})
            # If linked account takes opposite side on same contracts
            for contract in user_yes_contracts:
                if other_sides.get(contract) == 'no':
                    wash_detected = True
                    flags.append(f"wash_trading_suspected_{contract}")
                    break
            for contract in user_no_contracts:
                if other_sides.get(contract) == 'yes':
                    wash_detected = True
                    flags.append(f"wash_trading_suspected_{contract}")
                    break

        # Known associations boost confidence
        if known_associations:
            for creator_id, assoc_set in known_associations.items():
                if user_id in assoc_set:
                    for a in assoc_set:
                        if a != user_id and a in [t.get('user_id') for t in all_contract_trades]:
                            linked.append(a)
                            flags.append(f"known_association_{a}")

        coordination_score = len(linked) / max(len(other_users), 1)
        coordination_score = min(coordination_score * 2, 1.0)  # Amplify signal

        is_sybil = coordination_score >= 0.4 or wash_detected
        confidence = min(coordination_score + (0.3 if wash_detected else 0), 1.0)

        return SybilResult(
            target_user_id=user_id,
            is_sybil=is_sybil,
            confidence=confidence,
            linked_accounts=list(set(linked)),
            coordination_score=coordination_score,
            wash_trading_detected=wash_detected,
            flags=flags
        )


class StreamAudit:
    """
    Audits stream counts to verify legitimacy.

    Compares claimed streams against platform verification and
    applies penalties if artificial streams exceed threshold.
    """

    def __init__(
        self,
        void_threshold: float = 0.30,  # Void if >30% artificial
        penalty_threshold: float = 0.15,  # Penalize if >15% artificial
        audit_noise: float = 0.05  # Detection error margin
    ):
        self.void_threshold = void_threshold
        self.penalty_threshold = penalty_threshold
        self.audit_noise = audit_noise

    def audit_streams(
        self,
        song_id: str,
        claimed_streams: int,
        actual_organic_streams: int,
        actual_bot_streams: int,
        bot_detection_rate: float = 0.75
    ) -> AuditResult:
        """
        Audit stream counts for a song.

        In simulation, we know ground truth but apply detection noise.
        """
        flags = []
        total = claimed_streams

        if total == 0:
            return AuditResult(
                song_id=song_id,
                claimed_streams=0,
                verified_streams=0,
                organic_streams=0,
                artificial_streams=0,
                organic_ratio=1.0,
                passes_audit=True
            )

        # Detect bot streams with noise
        detected_bots = int(actual_bot_streams * bot_detection_rate *
                          np.random.uniform(1 - self.audit_noise, 1 + self.audit_noise))
        detected_bots = max(0, min(detected_bots, actual_bot_streams))

        # Verified streams = total - detected bots
        verified_streams = total - detected_bots
        organic_ratio = verified_streams / total if total > 0 else 1.0

        # Calculate actual ratio for audit scoring
        artificial_ratio = 1.0 - organic_ratio

        if artificial_ratio > self.void_threshold:
            flags.append("excessive_artificial_streams")
            flags.append("contract_void_recommended")
            contract_voided = True
            penalty_applied = True
        elif artificial_ratio > self.penalty_threshold:
            flags.append("moderate_artificial_streams")
            flags.append("penalty_recommended")
            contract_voided = False
            penalty_applied = True
        else:
            contract_voided = False
            penalty_applied = False

        if detected_bots > 50000:
            flags.append("large_scale_bot_operation")

        if detected_bots > 0 and actual_organic_streams < total * 0.5:
            flags.append("organic_minority")

        return AuditResult(
            song_id=song_id,
            claimed_streams=claimed_streams,
            verified_streams=verified_streams,
            organic_streams=actual_organic_streams,
            artificial_streams=detected_bots,
            organic_ratio=organic_ratio,
            passes_audit=not contract_voided,
            penalty_applied=penalty_applied,
            contract_voided=contract_voided,
            flags=flags
        )


class AntiCheatEngine:
    """
    Orchestrator that runs all anti-cheat checks and produces
    a combined risk assessment.
    """

    def __init__(
        self,
        bot_detection_rate: float = 0.75,
        void_threshold: float = 0.30,
        enable_sybil_detection: bool = True
    ):
        self.bot_detector = BotPurchaseDetector(base_detection_rate=bot_detection_rate)
        self.creator_restrictions = CreatorRestrictions()
        self.sybil_detector = SybilDetection()
        self.stream_auditor = StreamAudit(void_threshold=void_threshold)
        self.bot_detection_rate = bot_detection_rate
        self.enable_sybil_detection = enable_sybil_detection

    def full_analysis(
        self,
        song_id: str,
        creator_id: str,
        total_streams: int,
        organic_streams: int,
        bot_streams: int,
        daily_streams: List[int] = None,
        bot_budget: float = 0.0,
        trades: List[Dict] = None,
        all_trades: List[Dict] = None
    ) -> AntiCheatReport:
        """
        Run complete anti-cheat analysis for a song/contract.
        """
        creator_violations = []

        # 1. Bot stream detection
        bot_result = self.bot_detector.detect_bot_streams(
            song_id=song_id,
            total_streams=total_streams,
            organic_streams=organic_streams,
            bot_streams=bot_streams,
            daily_streams=daily_streams,
            bot_budget=bot_budget
        )

        # 2. Stream audit
        audit_result = self.stream_auditor.audit_streams(
            song_id=song_id,
            claimed_streams=total_streams,
            actual_organic_streams=organic_streams,
            actual_bot_streams=bot_streams,
            bot_detection_rate=self.bot_detection_rate
        )

        # 3. Check if creator traded on own song
        if trades:
            creator_trades = [t for t in trades if t.get('user_id') == creator_id]
            if creator_trades:
                creator_violations.append("creator_traded_own_song")

        # 4. Sybil detection (if enabled and trades provided)
        sybil_results = []
        if self.enable_sybil_detection and trades and all_trades:
            # Check creator and their associates
            sybil_result = self.sybil_detector.detect_sybil_accounts(
                user_id=creator_id,
                user_trades=[t for t in trades if t.get('user_id') == creator_id],
                all_contract_trades=all_trades,
                known_associations=self.creator_restrictions.creator_associations
            )
            if sybil_result.is_sybil:
                sybil_results.append(sybil_result)
                creator_violations.append("sybil_network_detected")

        # 5. Compute overall risk score
        scores = [
            bot_result.confidence * 0.35,
            (1.0 - audit_result.organic_ratio) * 0.30,
            (0.5 if creator_violations else 0.0) * 0.20,
            (sybil_results[0].confidence if sybil_results else 0.0) * 0.15,
        ]
        overall_score = min(sum(scores), 1.0)

        # Determine risk level
        if overall_score >= 0.7:
            risk_level = RiskLevel.CRITICAL
        elif overall_score >= 0.5:
            risk_level = RiskLevel.HIGH
        elif overall_score >= 0.3:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW

        # Determine action
        should_void = audit_result.contract_voided or overall_score >= 0.7
        should_ban = "creator_traded_own_song" in creator_violations or overall_score >= 0.8

        if should_ban:
            action = "ban_creator"
        elif should_void:
            action = "void_contract"
        elif overall_score >= 0.4:
            action = "manual_review"
        else:
            action = "none"

        return AntiCheatReport(
            song_id=song_id,
            overall_risk=risk_level,
            overall_score=overall_score,
            bot_detection=bot_result,
            sybil_results=sybil_results,
            audit_result=audit_result,
            creator_violations=creator_violations,
            recommended_action=action,
            should_void=should_void,
            should_ban_creator=should_ban
        )

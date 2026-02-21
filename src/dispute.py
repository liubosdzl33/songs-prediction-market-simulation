"""
Dispute Resolution System - "Future of Records" Committee

Implements a committee-based dispute resolution mechanism where:
- Any user can file a dispute on a contract (with 5% deposit)
- A committee of 3-7 members reviews evidence over 2 days
- Majority vote determines outcome
- Frivolous disputes forfeit the deposit
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import numpy as np


# Import enums from models (but define locally for independence)
class DisputeType(Enum):
    STREAM_MANIPULATION = "stream_manipulation"
    INSIDER_TRADING = "insider_trading"
    FALSE_REPORTING = "false_reporting"
    MARKET_MANIPULATION = "market_manipulation"


class DisputeStatus(Enum):
    FILED = "filed"
    EVIDENCE_COLLECTION = "evidence_collection"
    UNDER_REVIEW = "under_review"
    VOTING = "voting"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class DisputeOutcome(Enum):
    UPHELD = "upheld"
    OVERTURNED = "overturned"
    PARTIAL = "partial"
    PENALTY = "penalty"


class VoteChoice(Enum):
    UPHOLD = "uphold"          # Original resolution stands
    OVERTURN = "overturn"      # Void the market
    PARTIAL = "partial"        # Partial refund
    ABSTAIN = "abstain"


@dataclass
class CommitteeMember:
    """A member of the Future of Records committee"""
    member_id: str
    username: str
    expertise_score: float = 0.7  # 0-1, affects vote quality
    bias: float = 0.0  # -1 to 1, slight bias toward upheld(-) or overturn(+)
    reliability: float = 0.9  # Probability of voting correctly given evidence
    disputes_voted: int = 0
    correct_votes: int = 0
    earnings: float = 0.0  # Earned from dispute resolution fund


@dataclass
class Vote:
    """Individual committee member vote"""
    member_id: str
    dispute_id: str
    choice: VoteChoice
    reasoning: str
    confidence: float = 0.0  # 0-1
    voted_at: float = 0.0  # Simulation day


@dataclass
class Evidence:
    """Evidence submitted for a dispute"""
    evidence_id: str
    dispute_id: str
    submitted_by: str
    evidence_type: str  # "bot_detection_report", "trading_analysis", "stream_audit", etc.
    strength: float = 0.0  # 0-1, how compelling
    data: Dict = field(default_factory=dict)
    submitted_at: float = 0.0


@dataclass
class Dispute:
    """A dispute filed against a contract resolution"""
    dispute_id: str
    contract_id: str
    filed_by: str  # user_id
    dispute_type: DisputeType
    reason: str

    # Financial
    deposit_amount: float = 0.0  # 5% of contract volume
    deposit_returned: bool = False

    # Timeline (2-day resolution)
    filed_at: float = 0.0
    evidence_deadline: float = 0.0  # filed_at + 0.5 days
    voting_deadline: float = 0.0  # filed_at + 1.5 days
    resolution_deadline: float = 0.0  # filed_at + 2.0 days
    resolved_at: Optional[float] = None

    # Status
    status: DisputeStatus = DisputeStatus.FILED

    # Evidence & votes
    evidence: List[Evidence] = field(default_factory=list)
    votes: List[Vote] = field(default_factory=list)

    # Resolution
    outcome: Optional[DisputeOutcome] = None
    decision_summary: str = ""
    payout_adjustments: Dict = field(default_factory=dict)


@dataclass
class DisputeResolution:
    """Final resolution of a dispute"""
    dispute_id: str
    contract_id: str
    outcome: DisputeOutcome
    vote_tally: Dict[str, int]  # {choice: count}
    majority_reached: bool

    # Financial impact
    total_refunded: float = 0.0
    deposit_returned: bool = False
    creator_penalty: float = 0.0
    creator_banned: bool = False

    # Details
    decision_summary: str = ""
    resolved_at: float = 0.0


class FutureOfRecordsCommittee:
    """
    The 'Future of Records' committee handles dispute resolution.

    Timeline:
    - Day 0.0: Dispute filed, contract payouts frozen
    - Day 0.0 - 0.5: Evidence collection
    - Day 0.5 - 1.5: Committee review and voting
    - Day 1.5 - 2.0: Final tallying and resolution
    - Day 2.0: Decision published, funds distributed
    """

    DEPOSIT_RATE = 0.05  # 5% of contract volume
    RESOLUTION_DAYS = 2.0
    EVIDENCE_PHASE_DAYS = 0.5
    VOTING_PHASE_DAYS = 1.0  # 0.5 to 1.5
    MIN_COMMITTEE_SIZE = 3
    MAX_COMMITTEE_SIZE = 7
    SUPERMAJORITY_THRESHOLD = 0.67

    def __init__(self, members: List[CommitteeMember] = None):
        self.members = members or []
        self.disputes: Dict[str, Dispute] = {}
        self.resolutions: Dict[str, DisputeResolution] = {}
        self._dispute_counter = 0
        self._evidence_counter = 0

    def add_member(self, member: CommitteeMember):
        """Add a committee member"""
        if len(self.members) < self.MAX_COMMITTEE_SIZE:
            self.members.append(member)

    def file_dispute(
        self,
        contract_id: str,
        filed_by: str,
        dispute_type: DisputeType,
        reason: str,
        contract_volume: float,
        current_day: float,
        anti_cheat_report: Dict = None
    ) -> Optional[Dispute]:
        """
        File a new dispute against a contract.

        Returns None if deposit cannot be met or committee is too small.
        """
        if len(self.members) < self.MIN_COMMITTEE_SIZE:
            return None

        deposit = contract_volume * self.DEPOSIT_RATE

        self._dispute_counter += 1
        dispute_id = f"dispute_{self._dispute_counter}"

        dispute = Dispute(
            dispute_id=dispute_id,
            contract_id=contract_id,
            filed_by=filed_by,
            dispute_type=dispute_type,
            reason=reason,
            deposit_amount=deposit,
            filed_at=current_day,
            evidence_deadline=current_day + self.EVIDENCE_PHASE_DAYS,
            voting_deadline=current_day + self.EVIDENCE_PHASE_DAYS + self.VOTING_PHASE_DAYS,
            resolution_deadline=current_day + self.RESOLUTION_DAYS,
            status=DisputeStatus.FILED
        )

        # Auto-add anti-cheat evidence if available
        if anti_cheat_report:
            self._evidence_counter += 1
            evidence = Evidence(
                evidence_id=f"evidence_{self._evidence_counter}",
                dispute_id=dispute_id,
                submitted_by="system",
                evidence_type="anti_cheat_report",
                strength=anti_cheat_report.get('overall_score', 0.5),
                data=anti_cheat_report,
                submitted_at=current_day
            )
            dispute.evidence.append(evidence)

        self.disputes[dispute_id] = dispute
        return dispute

    def submit_evidence(
        self,
        dispute_id: str,
        submitted_by: str,
        evidence_type: str,
        strength: float,
        data: Dict,
        current_day: float
    ) -> Optional[Evidence]:
        """Submit evidence for a dispute during evidence collection phase"""
        dispute = self.disputes.get(dispute_id)
        if not dispute:
            return None

        if current_day > dispute.evidence_deadline:
            return None  # Past deadline

        self._evidence_counter += 1
        evidence = Evidence(
            evidence_id=f"evidence_{self._evidence_counter}",
            dispute_id=dispute_id,
            submitted_by=submitted_by,
            evidence_type=evidence_type,
            strength=np.clip(strength, 0, 1),
            data=data,
            submitted_at=current_day
        )

        dispute.evidence.append(evidence)
        dispute.status = DisputeStatus.EVIDENCE_COLLECTION
        return evidence

    def _simulate_member_vote(
        self,
        member: CommitteeMember,
        dispute: Dispute,
        evidence_strength: float
    ) -> Vote:
        """
        Simulate a committee member's vote based on evidence and member attributes.

        Members vote based on:
        - Evidence strength (primary signal)
        - Their expertise (affects accuracy)
        - Their bias (slight lean)
        - Random noise (human judgment variation)
        """
        # Base decision from evidence
        # High evidence strength -> likely overturn/penalty
        # Low evidence strength -> likely uphold

        decision_signal = evidence_strength + member.bias * 0.2
        decision_signal += np.random.normal(0, 0.1 * (1 - member.expertise_score))
        decision_signal = np.clip(decision_signal, 0, 1)

        # Determine vote
        if decision_signal >= 0.75:
            # Strong evidence of manipulation
            if dispute.dispute_type in (DisputeType.INSIDER_TRADING, DisputeType.STREAM_MANIPULATION):
                choice = VoteChoice.OVERTURN
                reasoning = "Strong evidence of manipulation warrants market void"
            else:
                choice = VoteChoice.OVERTURN
                reasoning = "Compelling evidence supports overturning resolution"
        elif decision_signal >= 0.55:
            choice = VoteChoice.PARTIAL
            reasoning = "Evidence suggests partial manipulation; partial refund appropriate"
        elif decision_signal >= 0.3:
            choice = VoteChoice.UPHOLD
            reasoning = "Insufficient evidence to overturn; original resolution stands"
        else:
            choice = VoteChoice.UPHOLD
            reasoning = "No credible evidence of manipulation found"

        # Rare abstention
        if np.random.random() < 0.05:
            choice = VoteChoice.ABSTAIN
            reasoning = "Conflict of interest or insufficient information to vote"

        confidence = abs(decision_signal - 0.5) * 2  # Higher when more certain

        return Vote(
            member_id=member.member_id,
            dispute_id=dispute.dispute_id,
            choice=choice,
            reasoning=reasoning,
            confidence=confidence
        )

    def conduct_vote(self, dispute_id: str, current_day: float) -> List[Vote]:
        """
        Have all committee members vote on a dispute.
        """
        dispute = self.disputes.get(dispute_id)
        if not dispute:
            return []

        dispute.status = DisputeStatus.VOTING

        # Calculate aggregate evidence strength.
        # Committee members weigh the strongest evidence more heavily
        # (reflects real adjudication where the most compelling piece
        # drives the decision, not the average of all submissions).
        if dispute.evidence:
            strengths = sorted([e.strength for e in dispute.evidence], reverse=True)
            # Weighted combination: 60% strongest, 40% mean of all
            evidence_strength = 0.6 * strengths[0] + 0.4 * np.mean(strengths)
        else:
            evidence_strength = 0.3  # Default low if no evidence

        votes = []
        for member in self.members:
            vote = self._simulate_member_vote(member, dispute, evidence_strength)
            vote.voted_at = current_day
            votes.append(vote)
            member.disputes_voted += 1

        dispute.votes = votes
        return votes

    def _tally_votes(self, votes: List[Vote]) -> Tuple[Dict[str, int], VoteChoice, bool]:
        """
        Tally votes and determine majority outcome.

        Returns: (tally_dict, winning_choice, majority_reached)
        """
        tally = {
            VoteChoice.UPHOLD.value: 0,
            VoteChoice.OVERTURN.value: 0,
            VoteChoice.PARTIAL.value: 0,
            VoteChoice.ABSTAIN.value: 0,
        }

        for vote in votes:
            tally[vote.choice.value] += 1

        # Exclude abstentions from majority calc
        active_votes = sum(v for k, v in tally.items() if k != VoteChoice.ABSTAIN.value)

        if active_votes == 0:
            return tally, VoteChoice.UPHOLD, False

        # Find winner
        best_choice = max(
            [VoteChoice.UPHOLD, VoteChoice.OVERTURN, VoteChoice.PARTIAL],
            key=lambda c: tally[c.value]
        )

        majority_pct = tally[best_choice.value] / active_votes
        majority_reached = majority_pct > 0.5

        # If no majority, check for supermajority requirement (deadlock)
        if not majority_reached:
            # In deadlock, require supermajority or default to uphold
            for choice in [VoteChoice.OVERTURN, VoteChoice.PARTIAL, VoteChoice.UPHOLD]:
                if tally[choice.value] / active_votes >= self.SUPERMAJORITY_THRESHOLD:
                    best_choice = choice
                    majority_reached = True
                    break

            if not majority_reached:
                best_choice = VoteChoice.UPHOLD  # Default: original stands
                majority_reached = False

        return tally, best_choice, majority_reached

    def resolve_dispute(
        self,
        dispute_id: str,
        current_day: float,
        contract_volume: float = 0.0
    ) -> Optional[DisputeResolution]:
        """
        Resolve a dispute based on committee votes.

        Called at or after the resolution deadline (filed_at + 2 days).
        """
        dispute = self.disputes.get(dispute_id)
        if not dispute:
            return None

        # If no votes yet, conduct vote
        if not dispute.votes:
            self.conduct_vote(dispute_id, current_day)

        tally, winning_choice, majority_reached = self._tally_votes(dispute.votes)

        # Map vote choice to dispute outcome
        if winning_choice == VoteChoice.OVERTURN:
            outcome = DisputeOutcome.OVERTURNED
            deposit_returned = True
            total_refunded = contract_volume * 0.8  # Refund 80% (20% was fees)
            creator_penalty = contract_volume * 0.1
            creator_banned = True
            summary = "Committee found sufficient evidence of manipulation. Market voided, traders refunded."

        elif winning_choice == VoteChoice.PARTIAL:
            outcome = DisputeOutcome.PARTIAL
            deposit_returned = True
            total_refunded = contract_volume * 0.4  # Partial refund
            creator_penalty = contract_volume * 0.05
            creator_banned = False
            summary = "Committee found partial evidence. Partial refund issued, creator penalized."

        else:  # UPHOLD
            outcome = DisputeOutcome.UPHELD
            deposit_returned = False  # Disputer loses deposit
            total_refunded = 0.0
            creator_penalty = 0.0
            creator_banned = False
            summary = "Committee upheld original resolution. Dispute deposit forfeited."

        # Check for special case: PENALTY (extreme manipulation)
        overturn_votes = tally.get(VoteChoice.OVERTURN.value, 0)
        total_active = sum(v for k, v in tally.items() if k != VoteChoice.ABSTAIN.value)
        if total_active > 0 and overturn_votes / total_active >= self.SUPERMAJORITY_THRESHOLD:
            outcome = DisputeOutcome.PENALTY
            creator_banned = True
            creator_penalty = contract_volume * 0.2
            summary = "Supermajority found severe manipulation. Creator banned, funds redistributed."

        # Update dispute
        dispute.outcome = outcome
        dispute.status = DisputeStatus.RESOLVED
        dispute.resolved_at = current_day
        dispute.deposit_returned = deposit_returned
        dispute.decision_summary = summary

        # Update member accuracy (based on majority alignment)
        for vote in dispute.votes:
            member = next((m for m in self.members if m.member_id == vote.member_id), None)
            if member and vote.choice.value == winning_choice.value:
                member.correct_votes += 1

        resolution = DisputeResolution(
            dispute_id=dispute_id,
            contract_id=dispute.contract_id,
            outcome=outcome,
            vote_tally=tally,
            majority_reached=majority_reached,
            total_refunded=total_refunded,
            deposit_returned=deposit_returned,
            creator_penalty=creator_penalty,
            creator_banned=creator_banned,
            decision_summary=summary,
            resolved_at=current_day
        )

        self.resolutions[dispute_id] = resolution
        return resolution

    def simulate_full_dispute(
        self,
        contract_id: str,
        filed_by: str,
        dispute_type: DisputeType,
        reason: str,
        contract_volume: float,
        filing_day: float,
        anti_cheat_report: Dict = None,
        additional_evidence: List[Dict] = None
    ) -> Optional[DisputeResolution]:
        """
        Simulate the full 2-day dispute lifecycle in one call.

        Timeline:
        - Day 0: File dispute
        - Day 0-0.5: Collect evidence
        - Day 0.5-1.5: Committee reviews and votes
        - Day 2.0: Resolution published
        """
        # Day 0: File
        dispute = self.file_dispute(
            contract_id=contract_id,
            filed_by=filed_by,
            dispute_type=dispute_type,
            reason=reason,
            contract_volume=contract_volume,
            current_day=filing_day,
            anti_cheat_report=anti_cheat_report
        )

        if not dispute:
            return None

        # Day 0-0.5: Evidence
        if additional_evidence:
            for ev in additional_evidence:
                self.submit_evidence(
                    dispute_id=dispute.dispute_id,
                    submitted_by=ev.get('submitted_by', 'anonymous'),
                    evidence_type=ev.get('type', 'user_report'),
                    strength=ev.get('strength', 0.3),
                    data=ev.get('data', {}),
                    current_day=filing_day + 0.25
                )

        # Day 0.5-1.5: Vote
        self.conduct_vote(dispute.dispute_id, filing_day + 1.0)

        # Day 2.0: Resolve
        resolution = self.resolve_dispute(
            dispute.dispute_id,
            current_day=filing_day + self.RESOLUTION_DAYS,
            contract_volume=contract_volume
        )

        return resolution

    def get_committee_stats(self) -> Dict:
        """Get committee performance statistics"""
        total_disputes = len(self.disputes)
        resolved = sum(1 for d in self.disputes.values() if d.status == DisputeStatus.RESOLVED)

        outcomes = {}
        for d in self.disputes.values():
            if d.outcome:
                key = d.outcome.value
                outcomes[key] = outcomes.get(key, 0) + 1

        member_accuracy = []
        for m in self.members:
            if m.disputes_voted > 0:
                member_accuracy.append(m.correct_votes / m.disputes_voted)

        return {
            'total_disputes': total_disputes,
            'resolved': resolved,
            'pending': total_disputes - resolved,
            'outcomes': outcomes,
            'avg_member_accuracy': float(np.mean(member_accuracy)) if member_accuracy else 0,
            'committee_size': len(self.members),
            'total_deposits_collected': sum(
                d.deposit_amount for d in self.disputes.values()
                if not d.deposit_returned and d.status == DisputeStatus.RESOLVED
            ),
            'total_deposits_returned': sum(
                d.deposit_amount for d in self.disputes.values()
                if d.deposit_returned
            ),
        }

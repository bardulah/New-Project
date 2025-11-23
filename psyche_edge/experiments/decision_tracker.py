"""
Decision Tracking System
Track all high-stakes decisions: betting, job apps, negotiations
Calculate outcomes, ROI, and decision quality metrics
"""
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class DecisionType(Enum):
    BET = "bet"
    JOB_APPLICATION = "job_application"
    NEGOTIATION = "negotiation"
    GENERAL = "general"


class DecisionOutcome(Enum):
    PENDING = "pending"
    WIN = "win"
    LOSS = "loss"
    NEUTRAL = "neutral"


@dataclass
class BettingDecision:
    """Sports betting decision"""
    sport: str
    bet_type: str  # spread, moneyline, over/under, prop
    bet_size: float
    odds: float
    expected_value: float
    book: str
    game: str
    reasoning: str
    timestamp: float
    outcome: str = "pending"
    result: Optional[float] = None  # Profit/loss
    roi: Optional[float] = None

    def calculate_roi(self):
        """Calculate ROI after resolution"""
        if self.result is not None:
            self.roi = (self.result / self.bet_size) * 100 if self.bet_size > 0 else 0


@dataclass
class JobApplicationDecision:
    """Job application decision"""
    company: str
    role: str
    salary_ask: float
    application_date: float
    source: str  # LinkedIn, referral, etc.
    reasoning: str
    timestamp: float
    outcome: str = "pending"
    response_received: bool = False
    response_date: Optional[float] = None
    interview_count: int = 0
    offer_received: bool = False
    offer_amount: Optional[float] = None

    def calculate_outcome_metrics(self) -> Dict:
        """Calculate job app metrics"""
        if self.response_date:
            response_time_days = (self.response_date - self.application_date) / 86400
        else:
            response_time_days = None

        return {
            'response_time_days': response_time_days,
            'got_response': self.response_received,
            'got_offer': self.offer_received,
            'offer_delta': (self.offer_amount - self.salary_ask) if self.offer_amount else None
        }


@dataclass
class NegotiationDecision:
    """Negotiation decision"""
    negotiation_type: str  # salary, contract, price, etc.
    initial_ask: float
    minimum_acceptable: float
    strategy: str
    reasoning: str
    timestamp: float
    outcome: str = "pending"
    final_amount: Optional[float] = None
    satisfaction_score: Optional[int] = None  # 1-10

    def calculate_outcome_metrics(self) -> Dict:
        """Calculate negotiation metrics"""
        if self.final_amount:
            got_minimum = self.final_amount >= self.minimum_acceptable
            percent_of_ask = (self.final_amount / self.initial_ask * 100) if self.initial_ask > 0 else 0
        else:
            got_minimum = None
            percent_of_ask = None

        return {
            'got_minimum': got_minimum,
            'percent_of_ask': percent_of_ask,
            'satisfaction': self.satisfaction_score
        }


class DecisionTracker:
    """
    Central decision tracking system
    Logs all decisions and tracks outcomes
    """

    def __init__(self, data_dir: str = "psyche_edge/data/decisions"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def log_betting_decision(self, **kwargs) -> str:
        """Log a betting decision"""
        decision = BettingDecision(**kwargs)
        decision_id = self._generate_id()

        self._save_decision('betting', decision_id, asdict(decision))

        return decision_id

    def log_job_application(self, **kwargs) -> str:
        """Log a job application"""
        decision = JobApplicationDecision(**kwargs)
        decision_id = self._generate_id()

        self._save_decision('job_application', decision_id, asdict(decision))

        return decision_id

    def log_negotiation(self, **kwargs) -> str:
        """Log a negotiation"""
        decision = NegotiationDecision(**kwargs)
        decision_id = self._generate_id()

        self._save_decision('negotiation', decision_id, asdict(decision))

        return decision_id

    def update_betting_outcome(self, decision_id: str, result: float):
        """Update betting decision with outcome"""
        decision_data = self._load_decision('betting', decision_id)

        if decision_data:
            decision_data['result'] = result
            decision_data['outcome'] = 'win' if result > 0 else 'loss'

            decision = BettingDecision(**decision_data)
            decision.calculate_roi()

            self._save_decision('betting', decision_id, asdict(decision))

    def update_job_application_outcome(self, decision_id: str, **updates):
        """Update job application with outcome"""
        decision_data = self._load_decision('job_application', decision_id)

        if decision_data:
            decision_data.update(updates)
            self._save_decision('job_application', decision_id, decision_data)

    def update_negotiation_outcome(self, decision_id: str, **updates):
        """Update negotiation with outcome"""
        decision_data = self._load_decision('negotiation', decision_id)

        if decision_data:
            decision_data.update(updates)
            self._save_decision('negotiation', decision_id, decision_data)

    def get_decision_history(self, decision_type: Optional[str] = None,
                            limit: int = 100) -> List[Dict]:
        """Get decision history"""
        if decision_type:
            log_file = self.data_dir / f"{decision_type}_log.jsonl"
            if log_file.exists():
                return self._read_jsonl(log_file, limit)

        # All decision types
        all_decisions = []

        for log_file in self.data_dir.glob("*_log.jsonl"):
            all_decisions.extend(self._read_jsonl(log_file, limit))

        # Sort by timestamp
        all_decisions.sort(key=lambda x: x.get('timestamp', 0), reverse=True)

        return all_decisions[:limit]

    def calculate_betting_stats(self) -> Dict:
        """Calculate betting performance stats"""
        decisions = self.get_decision_history('betting', limit=1000)

        total_bets = len(decisions)
        resolved_bets = [d for d in decisions if d.get('outcome') != 'pending']

        if not resolved_bets:
            return {'total_bets': total_bets, 'resolved': 0}

        wins = sum(1 for d in resolved_bets if d.get('outcome') == 'win')
        losses = len(resolved_bets) - wins

        total_wagered = sum(d.get('bet_size', 0) for d in resolved_bets)
        total_profit = sum(d.get('result', 0) for d in resolved_bets)

        roi = (total_profit / total_wagered * 100) if total_wagered > 0 else 0

        return {
            'total_bets': total_bets,
            'resolved': len(resolved_bets),
            'wins': wins,
            'losses': losses,
            'win_rate': wins / len(resolved_bets) * 100,
            'total_wagered': total_wagered,
            'total_profit': total_profit,
            'roi': roi
        }

    def calculate_job_app_stats(self) -> Dict:
        """Calculate job application stats"""
        decisions = self.get_decision_history('job_application', limit=1000)

        total_apps = len(decisions)
        responses = sum(1 for d in decisions if d.get('response_received'))
        offers = sum(1 for d in decisions if d.get('offer_received'))

        response_rate = (responses / total_apps * 100) if total_apps > 0 else 0
        offer_rate = (offers / total_apps * 100) if total_apps > 0 else 0

        return {
            'total_applications': total_apps,
            'responses': responses,
            'offers': offers,
            'response_rate': response_rate,
            'offer_rate': offer_rate
        }

    def _generate_id(self) -> str:
        """Generate unique decision ID"""
        import uuid
        return uuid.uuid4().hex[:12]

    def _save_decision(self, decision_type: str, decision_id: str, decision_data: Dict):
        """Save decision to log"""
        log_file = self.data_dir / f"{decision_type}_log.jsonl"

        # Add metadata
        decision_data['decision_id'] = decision_id
        decision_data['decision_type'] = decision_type

        with open(log_file, 'a') as f:
            f.write(json.dumps(decision_data) + '\n')

    def _load_decision(self, decision_type: str, decision_id: str) -> Optional[Dict]:
        """Load a specific decision"""
        log_file = self.data_dir / f"{decision_type}_log.jsonl"

        if not log_file.exists():
            return None

        with open(log_file) as f:
            for line in f:
                decision = json.loads(line)
                if decision.get('decision_id') == decision_id:
                    return decision

        return None

    def _read_jsonl(self, file_path: Path, limit: int) -> List[Dict]:
        """Read JSONL file"""
        decisions = []

        with open(file_path) as f:
            for line in f:
                decisions.append(json.loads(line))

        return decisions[-limit:]


# CLI for quick decision logging
def cli_log_bet():
    """CLI for logging a bet"""
    tracker = DecisionTracker()

    print("🎲 Log a Bet")
    print("-" * 40)

    sport = input("Sport: ")
    bet_type = input("Bet type (spread/moneyline/over): ")
    bet_size = float(input("Bet size ($): "))
    odds = float(input("Odds (decimal, e.g., 1.91): "))
    game = input("Game/matchup: ")
    reasoning = input("Reasoning: ")

    decision_id = tracker.log_betting_decision(
        sport=sport,
        bet_type=bet_type,
        bet_size=bet_size,
        odds=odds,
        expected_value=0,  # Calculate later
        book="unknown",
        game=game,
        reasoning=reasoning,
        timestamp=time.time()
    )

    print(f"\n✅ Bet logged! ID: {decision_id}")


if __name__ == "__main__":
    cli_log_bet()

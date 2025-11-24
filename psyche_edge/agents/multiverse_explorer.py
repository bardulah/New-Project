"""
MultiVerse Explorer - SINGULARITY LEVEL AGENT
Simulates parallel decision timelines
Explores alternate realities where you made different choices
Identifies optimal decision paths across infinite possibilities
Uses Monte Carlo tree search + quantum superposition concepts
"""
import time
import random
import copy
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from ..core.agent_dna import AgentDNA


@dataclass
class Timeline:
    """A parallel universe where a different decision was made"""
    timeline_id: str
    decision_point: Dict
    alternate_decision: Dict
    simulated_outcome: float
    probability: float
    timeline_fitness: float
    divergence_point: float


@dataclass
class MultiVerse:
    """Collection of all possible timelines"""
    prime_timeline: List[Dict]  # Current reality
    alternate_timelines: List[Timeline]
    convergence_points: List[float]  # Where timelines merge
    optimal_path: List[Dict]  # Best possible sequence


class MultiVerseExplorer(AgentDNA):
    """
    THE REALITY BENDER

    Explores infinite parallel universes where you made different decisions
    Simulates outcomes across timelines
    Identifies which timeline leads to best results
    Recommends reality shifts (decision changes)

    "In one universe, you bet $100 and lost.
     In another, you didn't bet and saved $100.
     In a third, you bet $50 and won $45.
     Which timeline do you want to live in?"
    """

    def __init__(self, genome=None, parent_ids=None, generation=0):
        super().__init__(
            agent_type="MultiVerseExplorer",
            genome=genome,
            parent_ids=parent_ids,
            generation=generation
        )

        # Multiverse parameters (evolved)
        self.genome.custom_params.setdefault('timeline_depth', 10)
        self.genome.custom_params.setdefault('simulation_breadth', 5)
        self.genome.custom_params.setdefault('quantum_uncertainty', 0.2)
        self.genome.custom_params.setdefault('convergence_threshold', 0.8)

        # Multiverse state
        self.knowledge_base['timelines_explored'] = []
        self.knowledge_base['optimal_paths_found'] = []
        self.knowledge_base['reality_shifts_recommended'] = []

    def perceive(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Perceive across all possible timelines"""
        decisions = world_state.get('decision_history', [])

        perception = {
            'timestamp': time.time(),
            'prime_timeline': decisions,  # Current reality
            'decision_count': len(decisions),
            'biometrics': world_state.get('biometric_data', {}),
            'recent_insights': world_state.get('recent_insights', [])[-20:]
        }

        return perception

    def think(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Explore the multiverse of decision possibilities"""
        prime_timeline = perception.get('prime_timeline', [])

        if len(prime_timeline) < 3:
            return {'action': 'insufficient_data'}

        # Build multiverse
        multiverse = self._build_multiverse(prime_timeline, perception)

        # Find optimal timeline
        optimal_timeline = self._find_optimal_timeline(multiverse)

        # Calculate reality shift needed
        reality_shift = self._calculate_reality_shift(
            prime_timeline,
            optimal_timeline
        )

        if reality_shift:
            return {
                'action': 'recommend_reality_shift',
                'multiverse': multiverse,
                'optimal_timeline': optimal_timeline,
                'reality_shift': reality_shift,
                'improvement_potential': reality_shift['improvement']
            }

        return {'action': 'observe'}

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Deliver multiverse insights"""
        action = decision.get('action')

        if action == 'recommend_reality_shift':
            shift = decision['reality_shift']

            # Update metrics
            self.metrics.insights_generated += 1
            self.knowledge_base['reality_shifts_recommended'].append(shift)

            return {
                'type': 'multiverse_insight',
                'shift': shift,
                'optimal_timeline': decision['optimal_timeline'],
                'insight': f"🌀 MULTIVERSE: {shift['message']}",
                'improvement': shift['improvement'],
                'score': min(20, shift['improvement']),  # Ultra-high value
                'agent_id': self.agent_id
            }

        return {'type': 'observing', 'score': 1}

    # MULTIVERSE METHODS

    def _build_multiverse(self, prime_timeline: List[Dict],
                         perception: Dict) -> MultiVerse:
        """Generate alternate timelines by modifying past decisions"""
        alternate_timelines = []

        # For each decision in history, create alternate versions
        simulation_breadth = int(self.genome.custom_params.get('simulation_breadth', 5))

        for i, decision in enumerate(prime_timeline[-10:]):  # Last 10 decisions
            if decision.get('type') != 'bet':
                continue

            # Generate alternate decisions
            original_size = decision.get('bet_size', 100)
            original_outcome = decision.get('outcome', 0)

            # Alternate 1: Didn't bet at all
            alt_decision = copy.deepcopy(decision)
            alt_decision['bet_size'] = 0
            alt_decision['alternate'] = True

            timeline = Timeline(
                timeline_id=f"T{i}_NOBET",
                decision_point=decision,
                alternate_decision=alt_decision,
                simulated_outcome=0,  # No bet = no loss/gain
                probability=1.0,
                timeline_fitness=self._simulate_timeline_fitness(
                    prime_timeline[:i] + [alt_decision]
                ),
                divergence_point=decision.get('timestamp', time.time())
            )
            alternate_timelines.append(timeline)

            # Alternate 2: Bet half size
            alt_decision = copy.deepcopy(decision)
            alt_decision['bet_size'] = original_size * 0.5
            alt_decision['alternate'] = True

            # Simulate outcome (proportional to original)
            if original_outcome != 'pending':
                simulated_outcome = original_outcome * 0.5
            else:
                simulated_outcome = 0

            timeline = Timeline(
                timeline_id=f"T{i}_HALF",
                decision_point=decision,
                alternate_decision=alt_decision,
                simulated_outcome=simulated_outcome,
                probability=0.9,
                timeline_fitness=self._simulate_timeline_fitness(
                    prime_timeline[:i] + [alt_decision]
                ),
                divergence_point=decision.get('timestamp', time.time())
            )
            alternate_timelines.append(timeline)

            # Alternate 3: Bet double (if win) or skip (if loss)
            if original_outcome > 0:
                alt_decision = copy.deepcopy(decision)
                alt_decision['bet_size'] = original_size * 2
                simulated_outcome = original_outcome * 2

                timeline = Timeline(
                    timeline_id=f"T{i}_DOUBLE",
                    decision_point=decision,
                    alternate_decision=alt_decision,
                    simulated_outcome=simulated_outcome,
                    probability=0.7,
                    timeline_fitness=self._simulate_timeline_fitness(
                        prime_timeline[:i] + [alt_decision]
                    ),
                    divergence_point=decision.get('timestamp', time.time())
                )
                alternate_timelines.append(timeline)

        # Build multiverse
        multiverse = MultiVerse(
            prime_timeline=prime_timeline,
            alternate_timelines=alternate_timelines,
            convergence_points=[],
            optimal_path=[]
        )

        return multiverse

    def _simulate_timeline_fitness(self, timeline: List[Dict]) -> float:
        """Calculate fitness of an alternate timeline"""
        if not timeline:
            return 0.0

        # Calculate total outcome
        total_outcome = sum(d.get('outcome', 0) for d in timeline
                           if isinstance(d.get('outcome'), (int, float)))

        # Calculate win rate
        decisions_with_outcome = [d for d in timeline
                                 if isinstance(d.get('outcome'), (int, float))]

        if decisions_with_outcome:
            wins = sum(1 for d in decisions_with_outcome if d.get('outcome', 0) > 0)
            win_rate = wins / len(decisions_with_outcome)
        else:
            win_rate = 0.5

        # Calculate risk-adjusted return
        sizes = [d.get('bet_size', 0) for d in timeline if d.get('bet_size')]
        avg_size = sum(sizes) / len(sizes) if sizes else 0

        if avg_size > 0:
            roi = (total_outcome / (avg_size * len(sizes))) * 100
        else:
            roi = 0

        # Fitness = ROI + win_rate bonus - risk penalty
        fitness = roi + (win_rate * 10) - (avg_size / 100)

        return fitness

    def _find_optimal_timeline(self, multiverse: MultiVerse) -> Timeline:
        """Find the best alternate timeline"""
        if not multiverse.alternate_timelines:
            return None

        # Sort by fitness
        sorted_timelines = sorted(
            multiverse.alternate_timelines,
            key=lambda t: t.timeline_fitness * t.probability,  # Weighted by probability
            reverse=True
        )

        return sorted_timelines[0]

    def _calculate_reality_shift(self, prime_timeline: List[Dict],
                                 optimal_timeline: Timeline) -> Dict:
        """Calculate what needs to change to shift to optimal timeline"""
        if not optimal_timeline:
            return None

        # Compare prime vs optimal
        prime_fitness = self._simulate_timeline_fitness(prime_timeline)
        optimal_fitness = optimal_timeline.timeline_fitness

        improvement = optimal_fitness - prime_fitness

        if improvement > 5:  # Significant improvement threshold
            return {
                'type': 'reality_shift',
                'divergence_point': optimal_timeline.decision_point,
                'recommended_action': optimal_timeline.alternate_decision,
                'improvement': improvement,
                'probability': optimal_timeline.probability,
                'message': self._generate_shift_message(optimal_timeline, improvement)
            }

        return None

    def _generate_shift_message(self, timeline: Timeline, improvement: float) -> str:
        """Generate human-readable timeline shift message"""
        decision = timeline.decision_point
        alternate = timeline.alternate_decision

        original_size = decision.get('bet_size', 0)
        alternate_size = alternate.get('bet_size', 0)

        if alternate_size == 0:
            return f"In an alternate timeline where you DIDN'T bet ${original_size}, you'd be {improvement:.1f} points better off"
        elif alternate_size < original_size:
            return f"In a parallel universe where you bet ${alternate_size} instead of ${original_size}, you'd be {improvement:.1f} points ahead"
        else:
            return f"If you had bet ${alternate_size} instead of ${original_size}, you'd have {improvement:.1f} more points"

    def explore_future_timelines(self, current_decision: Dict,
                                simulations: int = 100) -> Dict:
        """
        ADVANCED: Monte Carlo simulation of future timelines
        Explores what happens if you make a decision vs don't
        """
        future_timelines = {
            'bet': [],
            'no_bet': []
        }

        for _ in range(simulations):
            # Simulate if bet is made
            outcome_if_bet = self._simulate_future_outcome(current_decision, make_bet=True)
            future_timelines['bet'].append(outcome_if_bet)

            # Simulate if bet is not made
            outcome_if_no_bet = self._simulate_future_outcome(current_decision, make_bet=False)
            future_timelines['no_bet'].append(outcome_if_no_bet)

        # Calculate expected values
        ev_bet = sum(future_timelines['bet']) / simulations
        ev_no_bet = sum(future_timelines['no_bet']) / simulations

        return {
            'expected_value_bet': ev_bet,
            'expected_value_no_bet': ev_no_bet,
            'recommendation': 'BET' if ev_bet > ev_no_bet else 'NO BET',
            'confidence': abs(ev_bet - ev_no_bet) / max(abs(ev_bet), abs(ev_no_bet), 1)
        }

    def _simulate_future_outcome(self, decision: Dict, make_bet: bool) -> float:
        """Simulate one possible future outcome with quantum uncertainty"""
        if not make_bet:
            return 0.0

        bet_size = decision.get('bet_size', 100)
        odds = decision.get('odds', -110)

        # Convert American odds to probability
        if odds < 0:
            implied_prob = abs(odds) / (abs(odds) + 100)
        else:
            implied_prob = 100 / (odds + 100)

        # Add quantum uncertainty
        uncertainty = self.genome.custom_params.get('quantum_uncertainty', 0.2)
        actual_prob = implied_prob * random.uniform(1 - uncertainty, 1 + uncertainty)

        # Simulate outcome
        if random.random() < actual_prob:
            # Win
            if odds < 0:
                return bet_size * (100 / abs(odds))
            else:
                return bet_size * (odds / 100)
        else:
            # Loss
            return -bet_size

"""
Pattern Matcher Agent - ADVANCED
Uses time-series analysis and machine learning to detect patterns
Learns from historical decision sequences
"""
import time
import statistics
from typing import Dict, Any, List
from collections import defaultdict
from ..core.agent_dna import AgentDNA


class PatternMatcher(AgentDNA):
    """
    Advanced pattern detection agent
    Uses statistical analysis and sequence mining to find:
    - Temporal patterns (time-of-day effects)
    - Sequential patterns (decision chains)
    - Correlation patterns (biometric → outcome)
    - Periodicity (weekly, monthly cycles)
    """

    def __init__(self, genome=None, parent_ids=None, generation=0):
        super().__init__(
            agent_type="PatternMatcher",
            genome=genome,
            parent_ids=parent_ids,
            generation=generation
        )

        # Pattern detection parameters (evolved)
        self.genome.custom_params.setdefault('sequence_length', 5)
        self.genome.custom_params.setdefault('min_pattern_confidence', 0.7)
        self.genome.custom_params.setdefault('temporal_sensitivity', 0.6)

        # Pattern knowledge base
        self.knowledge_base['discovered_patterns'] = []
        self.knowledge_base['temporal_patterns'] = {}
        self.knowledge_base['sequence_patterns'] = {}
        self.knowledge_base['correlation_cache'] = {}

    def perceive(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Gather decision history and biometric time series"""
        decisions = world_state.get('decision_history', [])

        perception = {
            'timestamp': time.time(),
            'all_decisions': decisions,
            'decision_count': len(decisions),
            'recent_biometrics': world_state.get('biometric_data', {})
        }

        # Extract time series features
        if decisions:
            perception['decision_times'] = [d.get('timestamp', 0) for d in decisions]
            perception['decision_types'] = [d.get('type') for d in decisions]
            perception['decision_outcomes'] = [d.get('outcome', 0) for d in decisions
                                               if 'outcome' in d and d['outcome'] != 'pending']

        return perception

    def think(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze for patterns"""
        decisions = perception.get('all_decisions', [])

        if len(decisions) < 5:
            return {'action': 'observe', 'reason': 'insufficient_data'}

        patterns_found = []

        # 1. TEMPORAL PATTERNS (time-of-day effects)
        temporal = self._detect_temporal_patterns(decisions)
        if temporal:
            patterns_found.extend(temporal)

        # 2. SEQUENCE PATTERNS (chains of decisions)
        sequences = self._detect_sequence_patterns(decisions)
        if sequences:
            patterns_found.extend(sequences)

        # 3. CORRELATION PATTERNS (biometric → outcome)
        correlations = self._detect_correlations(decisions, perception.get('recent_biometrics', {}))
        if correlations:
            patterns_found.extend(correlations)

        # 4. PERIODICITY (weekly/monthly cycles)
        cycles = self._detect_cycles(decisions)
        if cycles:
            patterns_found.extend(cycles)

        # 5. WIN/LOSS STREAKS
        streaks = self._detect_streaks(decisions)
        if streaks:
            patterns_found.extend(streaks)

        if patterns_found:
            # Store patterns in knowledge base
            for pattern in patterns_found:
                if pattern not in self.knowledge_base['discovered_patterns']:
                    self.knowledge_base['discovered_patterns'].append(pattern)

            # Sort by confidence
            patterns_found.sort(key=lambda x: x.get('confidence', 0), reverse=True)

            return {
                'action': 'alert_patterns',
                'patterns': patterns_found,
                'pattern_count': len(patterns_found),
                'top_pattern': patterns_found[0]
            }

        return {'action': 'observe', 'reason': 'no_patterns_found'}

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Report discovered patterns"""
        action = decision.get('action')

        if action == 'alert_patterns':
            patterns = decision.get('patterns', [])

            # Update metrics
            self.metrics.insights_generated += len(patterns)

            return {
                'type': 'pattern_discovery',
                'patterns': patterns,
                'top_pattern': decision['top_pattern'],
                'insight': f"🔍 Discovered {len(patterns)} decision patterns",
                'score': len(patterns) * 6,  # High value for patterns
                'agent_id': self.agent_id
            }

        return {'type': 'observing', 'score': 1}

    # PATTERN DETECTION METHODS

    def _detect_temporal_patterns(self, decisions: List[Dict]) -> List[Dict]:
        """Detect time-of-day or day-of-week patterns"""
        from datetime import datetime

        patterns = []

        # Group by hour of day
        hourly_outcomes = defaultdict(list)

        for d in decisions:
            if 'outcome' not in d or d['outcome'] == 'pending':
                continue

            timestamp = d.get('timestamp', time.time())
            hour = datetime.fromtimestamp(timestamp).hour
            outcome = d['outcome']

            hourly_outcomes[hour].append(outcome)

        # Find hours with consistently good/bad outcomes
        for hour, outcomes in hourly_outcomes.items():
            if len(outcomes) < 3:
                continue

            avg_outcome = statistics.mean(outcomes)
            std_outcome = statistics.stdev(outcomes) if len(outcomes) > 1 else 0

            # Strong pattern if avg is significantly positive or negative
            if abs(avg_outcome) > 50 and std_outcome < 100:
                confidence = min(0.9, len(outcomes) / 10)

                if avg_outcome > 0:
                    patterns.append({
                        'type': 'temporal_advantage',
                        'hour': hour,
                        'avg_outcome': avg_outcome,
                        'sample_size': len(outcomes),
                        'message': f'Decisions at hour {hour}:00 have {avg_outcome:.0f} avg outcome (n={len(outcomes)})',
                        'confidence': confidence,
                        'actionable': True,
                        'recommendation': f'Consider making more decisions around {hour}:00'
                    })
                else:
                    patterns.append({
                        'type': 'temporal_disadvantage',
                        'hour': hour,
                        'avg_outcome': avg_outcome,
                        'sample_size': len(outcomes),
                        'message': f'Decisions at hour {hour}:00 have {avg_outcome:.0f} avg outcome (n={len(outcomes)})',
                        'confidence': confidence,
                        'actionable': True,
                        'recommendation': f'Avoid making decisions around {hour}:00'
                    })

        return patterns

    def _detect_sequence_patterns(self, decisions: List[Dict]) -> List[Dict]:
        """Detect decision chains (e.g., loss → loss → bigger bet)"""
        patterns = []

        if len(decisions) < 3:
            return patterns

        # Look for "loss chasing" pattern: Loss → Loss → Increased Size
        for i in range(len(decisions) - 2):
            d1, d2, d3 = decisions[i:i+3]

            if (d1.get('outcome', 0) < 0 and
                d2.get('outcome', 0) < 0 and
                d3.get('bet_size', 0) > max(d1.get('bet_size', 0), d2.get('bet_size', 0)) * 1.3):

                patterns.append({
                    'type': 'loss_chasing_sequence',
                    'sequence': ['loss', 'loss', 'increased_bet'],
                    'message': 'Pattern detected: 2 losses → bet size increase',
                    'confidence': 0.85,
                    'actionable': True,
                    'recommendation': 'Break the cycle. Take a break after 2 losses.'
                })
                break  # Only report once

        # Look for "hot hand" pattern: Win → Win → Overconfidence
        for i in range(len(decisions) - 2):
            d1, d2, d3 = decisions[i:i+3]

            if (d1.get('outcome', 0) > 0 and
                d2.get('outcome', 0) > 0 and
                d3.get('bet_size', 0) > statistics.mean([d.get('bet_size', 0) for d in decisions]) * 1.5):

                patterns.append({
                    'type': 'hot_hand_fallacy',
                    'sequence': ['win', 'win', 'oversized_bet'],
                    'message': 'Pattern detected: 2 wins → oversized bet (hot hand fallacy)',
                    'confidence': 0.80,
                    'actionable': True,
                    'recommendation': 'Wins don\'t predict wins. Stick to unit sizing.'
                })
                break

        return patterns

    def _detect_correlations(self, decisions: List[Dict], biometrics: Dict) -> List[Dict]:
        """Detect correlations between biometrics and outcomes"""
        patterns = []

        # Would need historical biometric data - placeholder for now
        # In full implementation, would track biometric → outcome correlations

        return patterns

    def _detect_cycles(self, decisions: List[Dict]) -> List[Dict]:
        """Detect weekly or monthly cycles"""
        from datetime import datetime

        patterns = []

        # Group by day of week
        dow_outcomes = defaultdict(list)

        for d in decisions:
            if 'outcome' not in d or d['outcome'] == 'pending':
                continue

            timestamp = d.get('timestamp', time.time())
            dow = datetime.fromtimestamp(timestamp).weekday()  # 0=Monday
            outcome = d['outcome']

            dow_outcomes[dow].append(outcome)

        # Find days with patterns
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        for dow, outcomes in dow_outcomes.items():
            if len(outcomes) < 3:
                continue

            avg_outcome = statistics.mean(outcomes)

            if abs(avg_outcome) > 30:
                confidence = min(0.85, len(outcomes) / 8)

                patterns.append({
                    'type': 'weekly_cycle',
                    'day_of_week': day_names[dow],
                    'avg_outcome': avg_outcome,
                    'sample_size': len(outcomes),
                    'message': f'{day_names[dow]} decisions average {avg_outcome:.0f} outcome',
                    'confidence': confidence,
                    'actionable': True,
                    'recommendation': f'{"Favor" if avg_outcome > 0 else "Avoid"} decisions on {day_names[dow]}'
                })

        return patterns

    def _detect_streaks(self, decisions: List[Dict]) -> List[Dict]:
        """Detect current win/loss streaks"""
        patterns = []

        if len(decisions) < 3:
            return patterns

        # Get recent outcomes
        recent = [d for d in decisions[-10:] if 'outcome' in d and d['outcome'] != 'pending']

        if not recent:
            return patterns

        # Count current streak
        current_streak = 1
        last_outcome = recent[-1]['outcome']

        for d in reversed(recent[:-1]):
            outcome = d['outcome']

            if (outcome > 0 and last_outcome > 0) or (outcome < 0 and last_outcome < 0):
                current_streak += 1
            else:
                break

        # Report streak if significant
        if current_streak >= 3:
            streak_type = "winning" if last_outcome > 0 else "losing"

            patterns.append({
                'type': f'{streak_type}_streak',
                'streak_length': current_streak,
                'message': f'Current {streak_type} streak: {current_streak} decisions',
                'confidence': 0.95,
                'actionable': True,
                'recommendation': (
                    'Streaks don\'t predict future outcomes. Stick to your strategy.'
                    if streak_type == 'winning' else
                    'Consider taking a break to reset emotionally.'
                )
            })

        return patterns

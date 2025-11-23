"""
Tilt Detector Agent
Detects "tilt" - emotional/irrational decision-making state
Combines HRV, betting patterns, decision entropy, time patterns
Inspired by poker tilt but applies to all high-stakes decisions
"""
import time
import math
import statistics
from typing import Dict, Any, List
from ..core.agent_dna import AgentDNA


class TiltDetector(AgentDNA):
    """
    Emotional tilt detection specialist
    Monitors for signs of irrational/emotional decision-making
    Uses biometrics + behavioral patterns
    """

    TILT_INDICATORS = [
        'rapid_decisions',
        'increasing_bet_sizes',
        'decision_entropy',
        'low_hrv',
        'poor_sleep',
        'time_of_day',
        'loss_chasing',
        'deviation_from_strategy'
    ]

    def __init__(self, genome=None, parent_ids=None, generation=0):
        super().__init__(
            agent_type="TiltDetector",
            genome=genome,
            parent_ids=parent_ids,
            generation=generation
        )

        # Tilt detection thresholds (evolved)
        self.genome.custom_params.setdefault('tilt_threshold', 0.7)
        self.genome.custom_params.setdefault('hrv_threshold', 50)
        self.genome.custom_params.setdefault('entropy_threshold', 2.5)
        self.genome.custom_params.setdefault('rapid_decision_window', 300)  # 5 minutes

        self.knowledge_base['tilt_events'] = []
        self.knowledge_base['tilt_predictions'] = []

    def perceive(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor all tilt indicators"""
        decisions = world_state.get('decision_history', [])[-30:]
        biometrics = world_state.get('biometric_data', {})

        perception = {
            'timestamp': time.time(),
            'decisions': decisions,
            'hrv': biometrics.get('hrv'),
            'heart_rate': biometrics.get('heart_rate'),
            'sleep_score': biometrics.get('sleep_score'),
            'mood': biometrics.get('mood'),
            'stress_level': biometrics.get('stress_level')
        }

        # Extract decision timing
        if decisions:
            perception['decision_times'] = [d.get('timestamp', 0) for d in decisions]
            perception['bet_sizes'] = [d.get('bet_size', 0) for d in decisions if d.get('type') == 'bet']
            perception['outcomes'] = [d.get('outcome', 0) for d in decisions if 'outcome' in d]

        return perception

    def think(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate tilt probability from multiple indicators"""
        tilt_score = 0.0
        indicators = {}

        # 1. RAPID DECISIONS (panic/emotion)
        decision_times = perception.get('decision_times', [])
        if len(decision_times) >= 3:
            time_deltas = [decision_times[i] - decision_times[i - 1]
                          for i in range(1, len(decision_times))]
            recent_deltas = time_deltas[-3:]

            rapid_threshold = self.genome.custom_params.get('rapid_decision_window', 300)
            rapid_count = sum(1 for d in recent_deltas if d < rapid_threshold)

            if rapid_count >= 2:
                indicators['rapid_decisions'] = {
                    'severity': rapid_count / 3,
                    'detail': f'{rapid_count}/3 decisions made rapidly (<{rapid_threshold}s apart)'
                }
                tilt_score += indicators['rapid_decisions']['severity'] * 0.2

        # 2. INCREASING BET SIZES (loss chasing)
        bet_sizes = perception.get('bet_sizes', [])
        if len(bet_sizes) >= 3:
            recent_bets = bet_sizes[-3:]
            if recent_bets == sorted(recent_bets) and recent_bets[-1] > recent_bets[0] * 1.5:
                indicators['increasing_bets'] = {
                    'severity': min(1.0, recent_bets[-1] / recent_bets[0] - 1),
                    'detail': f'Bet size increased {recent_bets[-1] / recent_bets[0]:.1f}x'
                }
                tilt_score += indicators['increasing_bets']['severity'] * 0.25

        # 3. DECISION ENTROPY (chaos/randomness)
        decisions = perception.get('decisions', [])
        if len(decisions) >= 5:
            entropy = self._calculate_decision_entropy(decisions)
            entropy_threshold = self.genome.custom_params.get('entropy_threshold', 2.5)

            if entropy > entropy_threshold:
                indicators['high_entropy'] = {
                    'severity': min(1.0, entropy / 4.0),
                    'detail': f'Decision pattern entropy: {entropy:.2f} (random/chaotic)'
                }
                tilt_score += indicators['high_entropy']['severity'] * 0.2

        # 4. LOW HRV (physiological stress)
        hrv = perception.get('hrv')
        if hrv is not None:
            hrv_threshold = self.genome.custom_params.get('hrv_threshold', 50)
            if hrv < hrv_threshold:
                indicators['low_hrv'] = {
                    'severity': (hrv_threshold - hrv) / hrv_threshold,
                    'detail': f'HRV={hrv} (stressed/fatigued)'
                }
                tilt_score += indicators['low_hrv']['severity'] * 0.15

        # 5. HIGH HEART RATE
        hr = perception.get('heart_rate')
        if hr and hr > 85:
            indicators['elevated_hr'] = {
                'severity': min(1.0, (hr - 85) / 40),
                'detail': f'Heart rate={hr} (aroused/stressed)'
            }
            tilt_score += indicators['elevated_hr']['severity'] * 0.1

        # 6. POOR SLEEP
        sleep_score = perception.get('sleep_score')
        if sleep_score and sleep_score < 70:
            indicators['poor_sleep'] = {
                'severity': (70 - sleep_score) / 70,
                'detail': f'Sleep score={sleep_score} (impaired judgment)'
            }
            tilt_score += indicators['poor_sleep']['severity'] * 0.15

        # 7. LOSS CHASING PATTERN
        outcomes = perception.get('outcomes', [])
        if len(outcomes) >= 4:
            recent_losses = sum(1 for o in outcomes[-4:] if o < 0)
            if recent_losses >= 3 and len(bet_sizes) >= 4:
                # Check if bet size increased after losses
                if bet_sizes[-1] > statistics.mean(bet_sizes[:-1]) * 1.3:
                    indicators['loss_chasing'] = {
                        'severity': 0.9,
                        'detail': f'{recent_losses}/4 losses, bet size increased 30%+'
                    }
                    tilt_score += 0.25

        # 8. TIME OF DAY (late night = worse decisions)
        current_hour = time.localtime().tm_hour
        if current_hour >= 23 or current_hour <= 5:
            indicators['late_night'] = {
                'severity': 0.5,
                'detail': f'Decision at {current_hour}:00 (impaired judgment)'
            }
            tilt_score += 0.05

        # Calculate final tilt probability
        tilt_probability = min(1.0, tilt_score)

        tilt_threshold = self.genome.custom_params.get('tilt_threshold', 0.7)

        if tilt_probability >= tilt_threshold:
            return {
                'action': 'tilt_alert',
                'tilt_probability': tilt_probability,
                'tilt_score': tilt_score,
                'indicators': indicators,
                'severity': 'HIGH' if tilt_probability > 0.85 else 'MEDIUM'
            }

        elif tilt_probability >= tilt_threshold * 0.7:
            return {
                'action': 'tilt_warning',
                'tilt_probability': tilt_probability,
                'tilt_score': tilt_score,
                'indicators': indicators,
                'severity': 'LOW'
            }

        return {
            'action': 'monitor',
            'tilt_probability': tilt_probability,
            'tilt_score': tilt_score
        }

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Alert on tilt or continue monitoring"""
        action = decision.get('action')

        if action == 'tilt_alert':
            # Log tilt event
            self.knowledge_base['tilt_events'].append({
                'timestamp': time.time(),
                'tilt_probability': decision['tilt_probability'],
                'indicators': decision['indicators']
            })

            # Update metrics
            self.metrics.insights_generated += 1
            self.metrics.decisions_improved += 1

            return {
                'type': 'tilt_alert',
                'severity': decision['severity'],
                'tilt_probability': decision['tilt_probability'],
                'indicators': decision['indicators'],
                'insight': f"🚨 TILT DETECTED ({decision['severity']}): {decision['tilt_probability']:.0%} probability",
                'recommendation': 'STOP. Take a break. Do not make decisions now.',
                'score': decision['tilt_probability'] * 20,  # High value for competitions
                'agent_id': self.agent_id
            }

        elif action == 'tilt_warning':
            return {
                'type': 'tilt_warning',
                'severity': decision['severity'],
                'tilt_probability': decision['tilt_probability'],
                'indicators': decision['indicators'],
                'insight': f"⚠️  Tilt Warning: {decision['tilt_probability']:.0%} probability",
                'recommendation': 'Caution advised. Consider taking a break.',
                'score': decision['tilt_probability'] * 10,
                'agent_id': self.agent_id
            }

        return {
            'type': 'monitoring',
            'tilt_probability': decision.get('tilt_probability', 0),
            'score': 1
        }

    def _calculate_decision_entropy(self, decisions: List[Dict]) -> float:
        """Calculate Shannon entropy of decision patterns"""
        # Extract decision types
        types = [d.get('type', 'unknown') for d in decisions[-10:]]

        if not types:
            return 0.0

        # Calculate frequency distribution
        type_counts = {}
        for t in types:
            type_counts[t] = type_counts.get(t, 0) + 1

        # Calculate entropy
        total = len(types)
        entropy = 0.0

        for count in type_counts.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)

        return entropy

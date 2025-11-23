"""
Bias Hunter Agent
Hunts for cognitive biases in real-time decisions:
- Anchoring bias
- Confirmation bias
- Availability heuristic
- Narrative fallacy
- Hindsight bias
- Overconfidence bias
- Loss aversion
- Sunk cost fallacy
- And 20+ more...
"""
import time
import statistics
from typing import Dict, Any, List
from ..core.agent_dna import AgentDNA


class BiasHunter(AgentDNA):
    """
    Cognitive bias detection specialist
    Scans decisions for patterns indicating cognitive biases
    Evolves to detect new bias patterns
    """

    BIASES = {
        'anchoring': 'Decision overly influenced by initial information',
        'confirmation': 'Seeking only information that confirms existing belief',
        'availability': 'Overweighting recent/memorable events',
        'narrative_fallacy': 'Creating false causal stories',
        'hindsight': 'I-knew-it-all-along effect',
        'overconfidence': 'Excessive certainty in predictions',
        'loss_aversion': 'Fear of losses > desire for gains',
        'sunk_cost': 'Continuing because of past investment',
        'recency': 'Overweighting most recent data',
        'gambler_fallacy': 'Believing in hot/cold streaks',
        'clustering_illusion': 'Seeing patterns in randomness',
        'representative_heuristic': 'Judging by stereotypes',
        'affect_heuristic': 'Letting emotions guide analysis'
    }

    def __init__(self, genome=None, parent_ids=None, generation=0):
        super().__init__(
            agent_type="BiasHunter",
            genome=genome,
            parent_ids=parent_ids,
            generation=generation
        )

        # Bias detection sensitivities (evolved)
        for bias_name in self.BIASES.keys():
            self.genome.custom_params.setdefault(f'{bias_name}_sensitivity', 0.5)

        # Track bias detection accuracy
        self.knowledge_base['biases_detected'] = []
        self.knowledge_base['false_positives'] = 0
        self.knowledge_base['true_positives'] = 0

    def perceive(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Scan for bias signals in decisions and biometric data"""
        recent_decisions = world_state.get('decision_history', [])[-20:]

        perception = {
            'timestamp': time.time(),
            'decisions': recent_decisions,
            'decision_count': len(recent_decisions),
            'hrv': world_state.get('biometric_data', {}).get('hrv'),
            'mood': world_state.get('biometric_data', {}).get('mood'),
            'sleep_score': world_state.get('biometric_data', {}).get('sleep_score')
        }

        # Extract decision features
        if recent_decisions:
            perception['decision_types'] = [d.get('type') for d in recent_decisions]
            perception['decision_outcomes'] = [d.get('outcome', 0) for d in recent_decisions
                                               if 'outcome' in d]
            perception['bet_sizes'] = [d.get('bet_size', 0) for d in recent_decisions
                                       if d.get('type') == 'bet']

        return perception

    def think(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Hunt for specific biases in decision patterns"""
        decisions = perception.get('decisions', [])

        if len(decisions) < 2:
            return {'action': 'observe', 'biases_detected': []}

        detected_biases = []

        # ANCHORING BIAS
        detected_biases.extend(self._detect_anchoring(decisions, perception))

        # CONFIRMATION BIAS
        detected_biases.extend(self._detect_confirmation(decisions, perception))

        # LOSS AVERSION
        detected_biases.extend(self._detect_loss_aversion(decisions, perception))

        # GAMBLER'S FALLACY
        detected_biases.extend(self._detect_gamblers_fallacy(decisions, perception))

        # RECENCY BIAS
        detected_biases.extend(self._detect_recency_bias(decisions, perception))

        # OVERCONFIDENCE
        detected_biases.extend(self._detect_overconfidence(decisions, perception))

        # SUNK COST FALLACY
        detected_biases.extend(self._detect_sunk_cost(decisions, perception))

        # AFFECT HEURISTIC (emotion-driven decisions)
        detected_biases.extend(self._detect_affect_heuristic(decisions, perception))

        # Filter by confidence threshold from genome
        significant_biases = [b for b in detected_biases
                             if b['confidence'] >= self.genome.confidence_threshold]

        if significant_biases:
            # Sort by severity
            significant_biases.sort(key=lambda x: x['severity'], reverse=True)

            return {
                'action': 'alert',
                'biases_detected': significant_biases,
                'bias_count': len(significant_biases),
                'top_bias': significant_biases[0]
            }

        return {'action': 'observe', 'biases_detected': []}

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Report detected biases"""
        action = decision.get('action')

        if action == 'alert':
            biases = decision['biases_detected']

            # Update metrics
            self.metrics.biases_detected += len(biases)
            self.metrics.insights_generated += len(biases)

            # Log detections
            for bias in biases:
                self.knowledge_base['biases_detected'].append({
                    'timestamp': time.time(),
                    'bias': bias
                })

            return {
                'type': 'bias_alert',
                'biases': biases,
                'top_bias': decision['top_bias'],
                'insight': f"🚨 Detected {decision['bias_count']} cognitive biases",
                'score': decision['bias_count'] * 5,  # For competitions
                'agent_id': self.agent_id
            }

        return {'type': 'observation', 'score': 1}

    # BIAS DETECTION METHODS

    def _detect_anchoring(self, decisions: List[Dict], perception: Dict) -> List[Dict]:
        """Detect if recent decision was anchored to irrelevant number"""
        bet_sizes = perception.get('bet_sizes', [])
        if len(bet_sizes) < 3:
            return []

        # Check if recent bets cluster around a specific value (anchor)
        recent_bets = bet_sizes[-5:]
        if len(set(recent_bets)) == 1:  # All same size
            sensitivity = self.genome.custom_params.get('anchoring_sensitivity', 0.5)
            return [{
                'bias_type': 'anchoring',
                'description': self.BIASES['anchoring'],
                'evidence': f'All recent bets same size: ${recent_bets[0]}',
                'severity': 0.7,
                'confidence': sensitivity
            }]

        return []

    def _detect_confirmation(self, decisions: List[Dict], perception: Dict) -> List[Dict]:
        """Detect confirmation bias - repeating same decision type after win"""
        if len(decisions) < 3:
            return []

        # Check for pattern: win -> repeat same type
        confirmations = 0
        for i in range(len(decisions) - 1):
            if (decisions[i].get('outcome', 0) > 0 and
                decisions[i].get('type') == decisions[i + 1].get('type')):
                confirmations += 1

        if confirmations >= 2:
            sensitivity = self.genome.custom_params.get('confirmation_sensitivity', 0.5)
            return [{
                'bias_type': 'confirmation',
                'description': self.BIASES['confirmation'],
                'evidence': f'Repeated same decision type {confirmations} times after wins',
                'severity': 0.6,
                'confidence': min(0.9, confirmations * 0.3 * sensitivity)
            }]

        return []

    def _detect_loss_aversion(self, decisions: List[Dict], perception: Dict) -> List[Dict]:
        """Detect loss aversion - reducing bet size after loss"""
        bet_sizes = perception.get('bet_sizes', [])
        outcomes = perception.get('decision_outcomes', [])

        if len(bet_sizes) < 3 or len(outcomes) < 2:
            return []

        # Check if bet sizes drop significantly after losses
        loss_reactions = []
        for i in range(len(outcomes) - 1):
            if outcomes[i] < 0 and i + 1 < len(bet_sizes):
                size_change = (bet_sizes[i + 1] - bet_sizes[i]) / max(bet_sizes[i], 1)
                if size_change < -0.3:  # 30% reduction
                    loss_reactions.append(size_change)

        if len(loss_reactions) >= 2:
            sensitivity = self.genome.custom_params.get('loss_aversion_sensitivity', 0.5)
            return [{
                'bias_type': 'loss_aversion',
                'description': self.BIASES['loss_aversion'],
                'evidence': f'Bet size reduced {len(loss_reactions)} times after losses',
                'severity': 0.8,
                'confidence': min(0.9, len(loss_reactions) * 0.4 * sensitivity)
            }]

        return []

    def _detect_gamblers_fallacy(self, decisions: List[Dict], perception: Dict) -> List[Dict]:
        """Detect gambler's fallacy - expecting reversal after streak"""
        outcomes = perception.get('decision_outcomes', [])

        if len(outcomes) < 4:
            return []

        # Check for streaks followed by opposite bet
        for i in range(len(outcomes) - 3):
            streak = outcomes[i:i + 3]
            if all(x > 0 for x in streak) or all(x < 0 for x in streak):
                # Found a streak - check if next decision suggests reversal expectation
                if i + 3 < len(decisions):
                    next_decision = decisions[i + 3]
                    if next_decision.get('notes', '').lower().find('due') > -1:
                        sensitivity = self.genome.custom_params.get('gambler_fallacy_sensitivity', 0.5)
                        return [{
                            'bias_type': 'gambler_fallacy',
                            'description': self.BIASES['gambler_fallacy'],
                            'evidence': f'Expecting reversal after streak',
                            'severity': 0.9,
                            'confidence': 0.8 * sensitivity
                        }]

        return []

    def _detect_recency_bias(self, decisions: List[Dict], perception: Dict) -> List[Dict]:
        """Detect overweighting of recent events"""
        if len(decisions) < 5:
            return []

        # Check if decision size correlates more with recent outcomes than long-term
        outcomes = perception.get('decision_outcomes', [])
        bet_sizes = perception.get('bet_sizes', [])

        if len(outcomes) < 5 or len(bet_sizes) < 5:
            return []

        recent_avg = statistics.mean(outcomes[-3:]) if len(outcomes) >= 3 else 0
        long_term_avg = statistics.mean(outcomes)

        last_bet = bet_sizes[-1] if bet_sizes else 0
        avg_bet = statistics.mean(bet_sizes)

        # If recent outcomes are positive and bet size increases
        if recent_avg > long_term_avg and last_bet > avg_bet * 1.3:
            sensitivity = self.genome.custom_params.get('recency_sensitivity', 0.5)
            return [{
                'bias_type': 'recency',
                'description': self.BIASES['recency'],
                'evidence': f'Bet size increased after recent wins, ignoring long-term data',
                'severity': 0.7,
                'confidence': 0.7 * sensitivity
            }]

        return []

    def _detect_overconfidence(self, decisions: List[Dict], perception: Dict) -> List[Dict]:
        """Detect overconfidence - large bets with low HRV/poor sleep"""
        bet_sizes = perception.get('bet_sizes', [])
        hrv = perception.get('hrv')
        sleep_score = perception.get('sleep_score')

        if not bet_sizes:
            return []

        last_bet = bet_sizes[-1]
        avg_bet = statistics.mean(bet_sizes)

        # Large bet + poor biometrics = overconfidence
        if last_bet > avg_bet * 1.5:
            poor_condition = (hrv and hrv < 50) or (sleep_score and sleep_score < 70)

            if poor_condition:
                sensitivity = self.genome.custom_params.get('overconfidence_sensitivity', 0.5)
                return [{
                    'bias_type': 'overconfidence',
                    'description': self.BIASES['overconfidence'],
                    'evidence': f'Large bet while HRV={hrv}, Sleep={sleep_score}',
                    'severity': 0.9,
                    'confidence': 0.8 * sensitivity
                }]

        return []

    def _detect_sunk_cost(self, decisions: List[Dict], perception: Dict) -> List[Dict]:
        """Detect sunk cost fallacy - continuing losing strategy"""
        outcomes = perception.get('decision_outcomes', [])

        if len(outcomes) < 5:
            return []

        # Check for continued betting after multiple losses
        recent_outcomes = outcomes[-5:]
        losses = sum(1 for x in recent_outcomes if x < 0)

        if losses >= 4 and len(decisions) >= 5:
            # Still betting despite losses
            sensitivity = self.genome.custom_params.get('sunk_cost_sensitivity', 0.5)
            return [{
                'bias_type': 'sunk_cost',
                'description': self.BIASES['sunk_cost'],
                'evidence': f'{losses}/5 recent decisions were losses, but continuing',
                'severity': 0.8,
                'confidence': 0.75 * sensitivity
            }]

        return []

    def _detect_affect_heuristic(self, decisions: List[Dict], perception: Dict) -> List[Dict]:
        """Detect emotion-driven decisions using mood/HRV"""
        mood = perception.get('mood')
        hrv = perception.get('hrv')

        if not decisions:
            return []

        last_decision = decisions[-1]

        # High emotion states (low HRV or extreme mood) + decision
        if (hrv and hrv < 40) or (mood and mood in ['angry', 'anxious', 'excited']):
            sensitivity = self.genome.custom_params.get('affect_heuristic_sensitivity', 0.5)
            return [{
                'bias_type': 'affect_heuristic',
                'description': self.BIASES['affect_heuristic'],
                'evidence': f'Decision made in emotional state: mood={mood}, HRV={hrv}',
                'severity': 0.85,
                'confidence': 0.8 * sensitivity
            }]

        return []

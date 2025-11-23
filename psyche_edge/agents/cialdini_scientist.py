"""
Cialdini Scientist Agent
Applies Cialdini's 7 principles of persuasion ETHICALLY to improve decision-making:
1. Reciprocity
2. Commitment & Consistency
3. Social Proof
4. Authority
5. Liking
6. Scarcity
7. Unity

NOT manipulation - using these principles to combat biases and build better habits
"""
import time
import random
from typing import Dict, Any
from ..core.agent_dna import AgentDNA, AgentGenome


class CialdiniScientist(AgentDNA):
    """
    Ethical persuasion scientist
    Detects when user's decisions violate psychological principles
    Suggests interventions based on Cialdini's framework
    """

    def __init__(self, genome=None, parent_ids=None, generation=0):
        super().__init__(
            agent_type="CialdiniScientist",
            genome=genome,
            parent_ids=parent_ids,
            generation=generation
        )

        # Principle weights (evolved parameters)
        self.genome.custom_params.setdefault('reciprocity_weight', 0.14)
        self.genome.custom_params.setdefault('consistency_weight', 0.16)
        self.genome.custom_params.setdefault('social_proof_weight', 0.15)
        self.genome.custom_params.setdefault('authority_weight', 0.13)
        self.genome.custom_params.setdefault('liking_weight', 0.14)
        self.genome.custom_params.setdefault('scarcity_weight', 0.14)
        self.genome.custom_params.setdefault('unity_weight', 0.14)

        # Knowledge base
        self.knowledge_base['principles_applied'] = []
        self.knowledge_base['successful_interventions'] = []
        self.knowledge_base['failed_interventions'] = []

    def perceive(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Look for decision patterns and opportunities to apply principles"""
        perception = {
            'timestamp': time.time(),
            'recent_decisions': world_state.get('decision_history', [])[-10:],
            'user_mood': world_state.get('biometric_data', {}).get('mood', 'neutral'),
            'user_hrv': world_state.get('biometric_data', {}).get('hrv', None),
            'user_sleep': world_state.get('biometric_data', {}).get('sleep_score', None),
            'recent_insights': world_state.get('recent_insights', [])[-5:]
        }

        # Check for decision patterns
        if perception['recent_decisions']:
            perception['decision_velocity'] = len(perception['recent_decisions']) / 3600
            perception['decision_types'] = [d.get('type') for d in perception['recent_decisions']]

        return perception

    def think(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze which Cialdini principles to apply"""
        decisions = perception.get('recent_decisions', [])

        if not decisions:
            return {'action': 'observe', 'confidence': 0.0}

        # Analyze last decision for principle violations
        last_decision = decisions[-1]
        decision_type = last_decision.get('type', 'unknown')

        insights = []
        applicable_principles = []

        # 1. COMMITMENT & CONSISTENCY
        # Check if user's actions are inconsistent with stated goals
        if decision_type == 'bet' and last_decision.get('bet_size', 0) > last_decision.get('planned_size', 0):
            insights.append({
                'principle': 'consistency',
                'violation': 'Bet size inconsistent with plan',
                'suggestion': 'Commit to your plan publicly to leverage consistency principle',
                'severity': 0.8
            })
            applicable_principles.append('consistency')

        # 2. RECIPROCITY
        # Encourage giving first to get cooperation
        if decision_type == 'negotiation':
            insights.append({
                'principle': 'reciprocity',
                'suggestion': 'Offer value first in negotiation - reciprocity will follow',
                'severity': 0.6
            })
            applicable_principles.append('reciprocity')

        # 3. SOCIAL PROOF
        # Use data from successful similar agents/decisions
        peer_decisions = [d for d in decisions if d.get('type') == decision_type]
        if len(peer_decisions) > 3:
            avg_outcome = sum(d.get('outcome', 0) for d in peer_decisions) / len(peer_decisions)
            if avg_outcome > 0:
                insights.append({
                    'principle': 'social_proof',
                    'suggestion': f'Your past {decision_type} decisions have {avg_outcome:.1f}% success rate',
                    'severity': 0.5
                })
                applicable_principles.append('social_proof')

        # 4. SCARCITY
        # Detect FOMO-driven decisions (bad) vs strategic scarcity (good)
        user_hrv = perception.get('user_hrv')
        if user_hrv and user_hrv < 50 and decision_type == 'bet':  # Low HRV = stress
            insights.append({
                'principle': 'scarcity',
                'violation': 'Decision made under stress - possible FOMO/scarcity trigger',
                'suggestion': 'Wait 10 minutes. Scarcity often creates bad decisions.',
                'severity': 0.9
            })
            applicable_principles.append('scarcity')

        # 5. AUTHORITY
        # Reference credible sources/data
        if decision_type == 'bet':
            insights.append({
                'principle': 'authority',
                'suggestion': 'Check expert consensus before betting - defer to authority when uncertain',
                'severity': 0.6
            })
            applicable_principles.append('authority')

        # 6. LIKING
        # Avoid decisions driven by liking bias
        if last_decision.get('notes', '').lower().find('like') > -1:
            insights.append({
                'principle': 'liking',
                'warning': 'Decision may be influenced by liking bias',
                'suggestion': 'Evaluate objectively - liking clouds judgment',
                'severity': 0.7
            })
            applicable_principles.append('liking')

        # 7. UNITY
        # Encourage decisions aligned with identity/values
        insights.append({
            'principle': 'unity',
            'suggestion': 'Does this align with who you want to become? Unity drives consistency.',
            'severity': 0.5
        })
        applicable_principles.append('unity')

        # Select top insight based on genome weights
        if insights:
            # Weight insights by genome parameters
            for insight in insights:
                principle = insight['principle']
                weight_key = f"{principle}_weight"
                insight['weighted_score'] = insight['severity'] * self.genome.custom_params.get(weight_key, 0.14)

            insights.sort(key=lambda x: x['weighted_score'], reverse=True)
            top_insight = insights[0]

            return {
                'action': 'intervene',
                'insight': top_insight,
                'all_insights': insights,
                'applicable_principles': applicable_principles,
                'confidence': top_insight['weighted_score']
            }

        return {'action': 'observe', 'confidence': 0.0}

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute intervention or observation"""
        action = decision.get('action')

        if action == 'intervene':
            insight = decision['insight']

            # Log intervention
            self.knowledge_base['principles_applied'].append({
                'timestamp': time.time(),
                'principle': insight['principle'],
                'insight': insight,
                'confidence': decision['confidence']
            })

            # Update metrics
            self.metrics.insights_generated += 1

            return {
                'type': 'cialdini_intervention',
                'insight': insight,
                'principle': insight['principle'],
                'score': decision['confidence'] * 10,  # For competitions
                'agent_id': self.agent_id
            }

        elif action == 'observe':
            return {
                'type': 'observation',
                'status': 'monitoring',
                'score': 1,
                'agent_id': self.agent_id
            }

        return {'type': 'unknown', 'score': 0}

    def evolve(self, mutation_strength: float = 1.0):
        """Override to evolve principle weights"""
        evolved = super().evolve(mutation_strength)

        # Normalize weights after mutation
        total = sum(evolved.genome.custom_params[f"{p}_weight"]
                   for p in ['reciprocity', 'consistency', 'social_proof',
                            'authority', 'liking', 'scarcity', 'unity'])

        for p in ['reciprocity', 'consistency', 'social_proof',
                 'authority', 'liking', 'scarcity', 'unity']:
            key = f"{p}_weight"
            evolved.genome.custom_params[key] /= total

        return evolved

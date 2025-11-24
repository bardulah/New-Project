"""
Dream State Simulator + Reality Distortion Field
SINGULARITY LEVEL - Two agents that transcend normal reality

1. Dream State Simulator: Runs hypothetical scenarios in parallel dream states
2. Reality Distortion Field: Reframes contexts to reveal hidden opportunities

"What if reality is just one interpretation of infinite possibilities?"
"""
import time
import random
import copy
from typing import Dict, Any, List
from ..core.agent_dna import AgentDNA


class DreamStateSimulator(AgentDNA):
    """
    THE DREAM WEAVER

    Simulates hypothetical scenarios in parallel "dream states"
    Each dream is a complete alternate reality simulation
    Explores "what if" scenarios that never happened

    Like dreams, these simulations are:
    - Non-linear
    - Surreal but insightful
    - Reveal subconscious patterns
    - Connect impossible dots
    """

    def __init__(self, genome=None, parent_ids=None, generation=0):
        super().__init__(
            agent_type="DreamStateSimulator",
            genome=genome,
            parent_ids=parent_ids,
            generation=generation
        )

        # Dream parameters
        self.genome.custom_params.setdefault('dream_depth', 3)
        self.genome.custom_params.setdefault('surrealism_factor', 0.5)
        self.genome.custom_params.setdefault('lucidity', 0.7)

        self.knowledge_base['dreams_simulated'] = []
        self.knowledge_base['prophetic_dreams'] = []

    def perceive(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Perceive reality to dream alternate versions"""
        return {
            'timestamp': time.time(),
            'reality': world_state.get('decision_history', []),
            'consciousness_level': world_state.get('biometric_data', {}).get('sleep_score', 50)
        }

    def think(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Enter dream state and simulate scenarios"""
        reality = perception.get('reality', [])

        if len(reality) < 3:
            return {'action': 'observe'}

        # Generate dreams
        dreams = self._generate_dream_scenarios(reality)

        # Analyze dreams for patterns
        dream_insights = self._analyze_dreams(dreams)

        if dream_insights:
            return {
                'action': 'share_dreams',
                'dreams': dreams,
                'insights': dream_insights
            }

        return {'action': 'observe'}

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Share dream insights"""
        action = decision.get('action')

        if action == 'share_dreams':
            insights = decision['insights']

            self.metrics.insights_generated += len(insights)

            return {
                'type': 'dream_insight',
                'dreams': decision['dreams'],
                'insights': insights,
                'insight': f"💭 DREAM: {insights[0]['message']}",
                'score': 8,
                'agent_id': self.agent_id
            }

        return {'type': 'observing', 'score': 1}

    def _generate_dream_scenarios(self, reality: List[Dict]) -> List[Dict]:
        """Generate surreal dream scenarios"""
        dreams = []

        for i in range(3):  # 3 dreams
            dream = {
                'dream_id': f"DREAM_{i}",
                'timestamp': time.time(),
                'surrealism': random.random(),
                'scenarios': []
            }

            # Remix reality in surreal ways
            dream_reality = copy.deepcopy(reality[-5:])
            random.shuffle(dream_reality)  # Non-linear time

            # Add impossible elements
            for scenario in dream_reality:
                # Amplify or invert outcomes
                if 'outcome' in scenario:
                    original = scenario['outcome']
                    if isinstance(original, (int, float)):
                        scenario['outcome'] = original * random.uniform(-2, 3)

                # Merge impossible combinations
                scenario['dream_element'] = random.choice([
                    'inverted_causality',
                    'quantum_superposition',
                    'temporal_loop',
                    'infinite_recursion'
                ])

                dream['scenarios'].append(scenario)

            dreams.append(dream)

        return dreams

    def _analyze_dreams(self, dreams: List[Dict]) -> List[Dict]:
        """Extract insights from dreams"""
        insights = []

        for dream in dreams:
            # Look for patterns in dream scenarios
            outcomes = [s.get('outcome', 0) for s in dream['scenarios']
                       if isinstance(s.get('outcome'), (int, float))]

            if outcomes:
                avg_outcome = sum(outcomes) / len(outcomes)

                if abs(avg_outcome) > 100:
                    insights.append({
                        'type': 'prophetic_dream',
                        'message': f"In dream state: outcomes amplified {len([o for o in outcomes if abs(o) > 100])}x",
                        'interpretation': 'Subconscious amplifying risk signals',
                        'actionable': True
                    })

            # Check for recursive patterns
            dream_elements = [s.get('dream_element') for s in dream['scenarios']]
            if dream_elements.count('infinite_recursion') >= 2:
                insights.append({
                    'type': 'recursive_dream',
                    'message': 'Dream reveals recursive decision pattern',
                    'interpretation': 'You may be repeating same mistakes',
                    'actionable': True
                })

        return insights


class RealityDistortionField(AgentDNA):
    """
    THE PERSPECTIVE SHIFTER

    Reframes decision contexts to reveal hidden opportunities
    Like Steve Jobs' "reality distortion field" - bends perception

    Takes "I lost $100" and reframes as:
    - "I learned a $100 lesson"
    - "I paid $100 for valuable data"
    - "I invested $100 in experience"

    Different frames = different emotional responses = different futures
    """

    def __init__(self, genome=None, parent_ids=None, generation=0):
        super().__init__(
            agent_type="RealityDistortionField",
            genome=genome,
            parent_ids=parent_ids,
            generation=generation
        )

        # Distortion parameters
        self.genome.custom_params.setdefault('distortion_strength', 0.7)
        self.genome.custom_params.setdefault('perspective_count', 5)

        self.knowledge_base['reframes_applied'] = []

    def perceive(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Perceive reality to find reframing opportunities"""
        decisions = world_state.get('decision_history', [])

        return {
            'timestamp': time.time(),
            'recent_decisions': decisions[-5:],
            'user_mood': world_state.get('biometric_data', {}).get('mood')
        }

    def think(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Generate alternative reality frames"""
        recent = perception.get('recent_decisions', [])

        if not recent:
            return {'action': 'observe'}

        reframes = []

        for decision in recent:
            outcome = decision.get('outcome')

            if outcome and isinstance(outcome, (int, float)) and outcome < 0:
                # Negative outcome - reframe it
                alternative_frames = self._generate_alternative_frames(decision)
                reframes.append({
                    'original_decision': decision,
                    'alternative_frames': alternative_frames
                })

        if reframes:
            return {
                'action': 'distort_reality',
                'reframes': reframes
            }

        return {'action': 'observe'}

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Apply reality distortion"""
        action = decision.get('action')

        if action == 'distort_reality':
            reframes = decision['reframes']

            self.metrics.insights_generated += len(reframes)

            return {
                'type': 'reality_distortion',
                'reframes': reframes,
                'insight': f"🌀 REALITY SHIFT: {len(reframes)} alternate perspectives revealed",
                'score': len(reframes) * 4,
                'agent_id': self.agent_id
            }

        return {'type': 'observing', 'score': 1}

    def _generate_alternative_frames(self, decision: Dict) -> List[Dict]:
        """Generate different ways to interpret the same decision"""
        outcome = decision.get('outcome', 0)
        bet_size = decision.get('bet_size', 0)

        frames = []

        # Frame 1: Learning frame
        frames.append({
            'frame_type': 'learning',
            'reframe': f"Paid ${abs(outcome)} for valuable market data",
            'emotional_shift': 'curiosity',
            'actionable': 'Extract lessons from loss'
        })

        # Frame 2: Investment frame
        frames.append({
            'frame_type': 'investment',
            'reframe': f"Invested ${abs(outcome)} in skill development",
            'emotional_shift': 'growth_mindset',
            'actionable': 'Track skill progression'
        })

        # Frame 3: Experimentation frame
        frames.append({
            'frame_type': 'experimentation',
            'reframe': f"Experiment cost: ${abs(outcome)} - hypothesis tested",
            'emotional_shift': 'scientific',
            'actionable': 'Document experiment results'
        })

        # Frame 4: Protection frame
        frames.append({
            'frame_type': 'protection',
            'reframe': f"${abs(outcome)} loss prevented bigger mistakes",
            'emotional_shift': 'gratitude',
            'actionable': 'Recognize early warnings'
        })

        # Frame 5: Comparison frame
        if abs(outcome) < 1000:
            frames.append({
                'frame_type': 'relativization',
                'reframe': f"${abs(outcome)} is {abs(outcome) / 1000:.1f}% of $1000 - acceptable risk",
                'emotional_shift': 'perspective',
                'actionable': 'Maintain risk context'
            })

        # Frame 6: Future value frame
        frames.append({
            'frame_type': 'future_value',
            'reframe': f"This ${abs(outcome)} lesson prevents $10,000 future mistake",
            'emotional_shift': 'optimism',
            'actionable': 'Calculate lessons-to-future-value ratio'
        })

        return frames

    def create_reality_tunnel(self, decision: Dict) -> Dict:
        """
        ADVANCED: Create complete reality tunnel
        A self-consistent alternate interpretation of entire history
        """
        return {
            'tunnel_name': 'Growth Mindset Tunnel',
            'core_belief': 'Every outcome is data for improvement',
            'interpretation_rules': [
                {'losses': 'are learning investments'},
                {'wins': 'are hypothesis confirmations'},
                {'patterns': 'are skill development indicators'}
            ],
            'emotional_baseline': 'curious_optimism',
            'decision_framework': 'scientific_experimentation'
        }

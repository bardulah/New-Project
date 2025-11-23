"""
Meta-Observer Agent
Watches the watchers
Detects when the ENTIRE SWARM is wrong
Identifies emergent patterns and systemic failures
The final check against groupthink
"""
import time
import statistics
from collections import Counter
from typing import Dict, Any, List
from ..core.agent_dna import AgentDNA


class MetaObserver(AgentDNA):
    """
    Swarm-level observer
    Detects collective biases, groupthink, and systemic failures
    Provides meta-insights about the entire system
    """

    def __init__(self, genome=None, parent_ids=None, generation=0):
        super().__init__(
            agent_type="MetaObserver",
            genome=genome,
            parent_ids=parent_ids,
            generation=generation
        )

        # Meta-observation parameters
        self.genome.custom_params.setdefault('consensus_threshold', 0.8)
        self.genome.custom_params.setdefault('diversity_target', 0.6)
        self.genome.custom_params.setdefault('contradiction_sensitivity', 0.7)

        self.knowledge_base['swarm_failures_detected'] = []
        self.knowledge_base['groupthink_events'] = []
        self.knowledge_base['meta_insights'] = []

    def perceive(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Observe the entire swarm state"""
        recent_insights = world_state.get('recent_insights', [])

        # Aggregate insights by type
        insight_types = [i.get('insight', {}).get('principle') or
                        i.get('insight', {}).get('bias_type') or
                        i.get('type')
                        for i in recent_insights if i.get('insight')]

        # Get agent types producing insights
        active_agent_types = [i.get('agent_type') for i in recent_insights]

        perception = {
            'timestamp': time.time(),
            'total_insights': len(recent_insights),
            'insight_distribution': Counter(insight_types),
            'agent_type_distribution': Counter(active_agent_types),
            'unique_insight_types': len(set(insight_types)),
            'unique_agent_types': len(set(active_agent_types)),
            'recent_insights': recent_insights,
            'cycle_count': world_state.get('cycle_count', 0)
        }

        return perception

    def think(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze swarm-level patterns"""
        insights = []

        # 1. DETECT GROUPTHINK
        groupthink_result = self._detect_groupthink(perception)
        if groupthink_result:
            insights.append(groupthink_result)

        # 2. DETECT LACK OF DIVERSITY
        diversity_result = self._detect_low_diversity(perception)
        if diversity_result:
            insights.append(diversity_result)

        # 3. DETECT CONTRADICTIONS
        contradiction_result = self._detect_contradictions(perception)
        if contradiction_result:
            insights.append(contradiction_result)

        # 4. DETECT BLIND SPOTS
        blindspot_result = self._detect_blind_spots(perception)
        if blindspot_result:
            insights.append(blindspot_result)

        # 5. ASSESS SWARM HEALTH
        health_result = self._assess_swarm_health(perception)
        insights.append(health_result)

        if insights:
            return {
                'action': 'meta_alert',
                'insights': insights,
                'insight_count': len(insights),
                'top_priority': max(insights, key=lambda x: x.get('severity', 0))
            }

        return {'action': 'monitor'}

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Report meta-insights about swarm behavior"""
        action = decision.get('action')

        if action == 'meta_alert':
            insights = decision.get('insights', [])

            # Log meta-insights
            for insight in insights:
                self.knowledge_base['meta_insights'].append({
                    'timestamp': time.time(),
                    'insight': insight
                })

            # Update metrics
            self.metrics.insights_generated += len(insights)

            top_insight = decision['top_priority']

            return {
                'type': 'meta_observation',
                'insights': insights,
                'top_insight': top_insight,
                'insight': f"🔭 Meta-observation: {top_insight.get('message')}",
                'score': len(insights) * 4,
                'agent_id': self.agent_id
            }

        return {'type': 'monitoring', 'score': 1}

    def _detect_groupthink(self, perception: Dict) -> Dict:
        """Detect if all agents are saying the same thing"""
        insight_distribution = perception.get('insight_distribution', {})

        if not insight_distribution:
            return None

        total = sum(insight_distribution.values())
        if total < 5:  # Need sufficient data
            return None

        # Check if one insight type dominates
        max_count = max(insight_distribution.values())
        max_ratio = max_count / total

        consensus_threshold = self.genome.custom_params.get('consensus_threshold', 0.8)

        if max_ratio >= consensus_threshold:
            dominant_type = max(insight_distribution.items(), key=lambda x: x[1])[0]

            return {
                'type': 'groupthink',
                'message': f'Swarm consensus at {max_ratio:.0%} on "{dominant_type}" - possible groupthink',
                'severity': max_ratio,
                'evidence': {
                    'dominant_insight': dominant_type,
                    'consensus_ratio': max_ratio,
                    'distribution': dict(insight_distribution)
                }
            }

        return None

    def _detect_low_diversity(self, perception: Dict) -> Dict:
        """Detect lack of diverse perspectives"""
        unique_agent_types = perception.get('unique_agent_types', 0)
        unique_insight_types = perception.get('unique_insight_types', 0)
        total_insights = perception.get('total_insights', 0)

        if total_insights < 5:
            return None

        # Calculate diversity score
        diversity_score = (unique_agent_types + unique_insight_types) / max(1, total_insights)

        diversity_target = self.genome.custom_params.get('diversity_target', 0.6)

        if diversity_score < diversity_target:
            return {
                'type': 'low_diversity',
                'message': f'Swarm diversity below target: {diversity_score:.2f} < {diversity_target:.2f}',
                'severity': (diversity_target - diversity_score) / diversity_target,
                'evidence': {
                    'diversity_score': diversity_score,
                    'unique_agents': unique_agent_types,
                    'unique_insights': unique_insight_types,
                    'total_insights': total_insights
                }
            }

        return None

    def _detect_contradictions(self, perception: Dict) -> Dict:
        """Detect contradictory insights from different agents"""
        recent_insights = perception.get('recent_insights', [])

        # Look for opposing recommendations
        # E.g., one agent says "bet more", another says "bet less"

        contradictions = []

        # Simple heuristic: look for opposite sentiment in insights
        for i, insight1 in enumerate(recent_insights):
            for insight2 in recent_insights[i + 1:]:
                if self._are_contradictory(insight1, insight2):
                    contradictions.append((insight1, insight2))

        if len(contradictions) >= 2:
            return {
                'type': 'contradictions',
                'message': f'Detected {len(contradictions)} contradictory insights',
                'severity': min(1.0, len(contradictions) / 5),
                'evidence': {
                    'contradiction_count': len(contradictions),
                    'examples': contradictions[:3]  # Show top 3
                }
            }

        return None

    def _detect_blind_spots(self, perception: Dict) -> Dict:
        """Detect if certain decision types are being ignored"""
        agent_type_dist = perception.get('agent_type_distribution', {})

        # Expected agent types that should be active
        expected_types = ['CialdiniScientist', 'BiasHunter', 'TiltDetector',
                         'DecisionLogger', 'MetaObserver']

        missing_types = [t for t in expected_types if t not in agent_type_dist]

        if missing_types:
            return {
                'type': 'blind_spots',
                'message': f'No activity from: {", ".join(missing_types)}',
                'severity': len(missing_types) / len(expected_types),
                'evidence': {
                    'missing_agent_types': missing_types,
                    'active_types': list(agent_type_dist.keys())
                }
            }

        return None

    def _assess_swarm_health(self, perception: Dict) -> Dict:
        """Overall swarm health assessment"""
        total_insights = perception.get('total_insights', 0)
        unique_agents = perception.get('unique_agent_types', 0)
        cycle_count = perception.get('cycle_count', 0)

        # Calculate health score
        activity_score = min(1.0, total_insights / 10)  # Target 10+ insights
        diversity_score = min(1.0, unique_agents / 5)  # Target 5+ agent types

        health_score = (activity_score + diversity_score) / 2

        status = 'HEALTHY' if health_score > 0.7 else 'MODERATE' if health_score > 0.4 else 'POOR'

        return {
            'type': 'swarm_health',
            'message': f'Swarm health: {status} ({health_score:.0%})',
            'severity': 1.0 - health_score if health_score < 0.7 else 0.0,
            'evidence': {
                'health_score': health_score,
                'activity_score': activity_score,
                'diversity_score': diversity_score,
                'total_insights': total_insights,
                'unique_agents': unique_agents,
                'cycle_count': cycle_count
            }
        }

    def _are_contradictory(self, insight1: Dict, insight2: Dict) -> bool:
        """Simple contradiction detection"""
        # Get insight text
        text1 = str(insight1.get('insight', '')).lower()
        text2 = str(insight2.get('insight', '')).lower()

        # Look for opposing keywords
        opposing_pairs = [
            ('increase', 'decrease'),
            ('more', 'less'),
            ('buy', 'sell'),
            ('bet', 'avoid'),
            ('continue', 'stop')
        ]

        for word1, word2 in opposing_pairs:
            if word1 in text1 and word2 in text2:
                return True
            if word2 in text1 and word1 in text2:
                return True

        return False

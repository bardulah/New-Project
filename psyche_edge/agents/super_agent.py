"""
SuperAgent - The Insight Synthesizer
Meta-meta-agent that combines insights from ALL other agents
Produces superior recommendations by weighing multiple perspectives
"""
import time
import statistics
from typing import Dict, Any, List, Optional
from collections import Counter
from ..core.agent_dna import AgentDNA


class SuperAgent(AgentDNA):
    """
    The highest-level meta-agent
    Synthesizes insights from all other agents to produce superior recommendations
    Weighs agent credibility based on track record
    Resolves contradictions and produces consensus recommendations
    """

    def __init__(self, genome=None, parent_ids=None, generation=0):
        super().__init__(
            agent_type="SuperAgent",
            genome=genome,
            parent_ids=parent_ids,
            generation=generation
        )

        # Synthesis parameters (evolved)
        self.genome.custom_params.setdefault('min_consensus', 0.6)
        self.genome.custom_params.setdefault('credibility_weight', 0.7)
        self.genome.custom_params.setdefault('recency_weight', 0.3)

        # Track agent credibility
        self.knowledge_base['agent_credibility'] = {}
        self.knowledge_base['synthesis_history'] = []
        self.knowledge_base['recommendations_made'] = 0

    def perceive(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Gather all insights from all agents"""
        recent_insights = world_state.get('recent_insights', [])

        perception = {
            'timestamp': time.time(),
            'all_insights': recent_insights,
            'insight_count': len(recent_insights),
            'decisions': world_state.get('decision_history', [])[-5:],
            'biometrics': world_state.get('biometric_data', {})
        }

        # Group insights by agent type
        insights_by_type = {}
        for insight in recent_insights:
            agent_type = insight.get('agent_type', 'Unknown')
            if agent_type not in insights_by_type:
                insights_by_type[agent_type] = []
            insights_by_type[agent_type].append(insight)

        perception['insights_by_type'] = insights_by_type

        # Count agent activity
        agent_activity = Counter(i.get('agent_type') for i in recent_insights)
        perception['agent_activity'] = dict(agent_activity)

        return perception

    def think(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize insights from multiple agents"""
        all_insights = perception.get('all_insights', [])

        if len(all_insights) < 2:
            return {'action': 'insufficient_data'}

        # 1. COLLECT RECOMMENDATIONS
        recommendations = self._extract_recommendations(all_insights)

        # 2. DETECT CONSENSUS
        consensus = self._detect_consensus(recommendations)

        # 3. IDENTIFY CONTRADICTIONS
        contradictions = self._identify_contradictions(recommendations)

        # 4. WEIGH BY AGENT CREDIBILITY
        weighted_recommendations = self._weight_by_credibility(recommendations)

        # 5. SYNTHESIZE FINAL RECOMMENDATION
        if consensus:
            final_recommendation = self._build_consensus_recommendation(
                consensus, weighted_recommendations)

            return {
                'action': 'consensus_recommendation',
                'recommendation': final_recommendation,
                'consensus_level': consensus['consensus_level'],
                'supporting_agents': consensus['supporting_agents'],
                'contradictions': contradictions
            }

        elif weighted_recommendations:
            # No consensus, but we have weighted recs
            final_recommendation = self._build_weighted_recommendation(
                weighted_recommendations)

            return {
                'action': 'weighted_recommendation',
                'recommendation': final_recommendation,
                'confidence': final_recommendation.get('confidence', 0.5),
                'contradictions': contradictions
            }

        return {'action': 'observe'}

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Deliver synthesized recommendation"""
        action = decision.get('action')

        if action == 'consensus_recommendation':
            rec = decision['recommendation']

            # Update metrics
            self.metrics.insights_generated += 1
            self.knowledge_base['recommendations_made'] += 1

            # Store in history
            self.knowledge_base['synthesis_history'].append({
                'timestamp': time.time(),
                'type': 'consensus',
                'recommendation': rec,
                'consensus_level': decision['consensus_level']
            })

            return {
                'type': 'super_recommendation',
                'subtype': 'consensus',
                'recommendation': rec,
                'consensus_level': decision['consensus_level'],
                'supporting_agents': decision['supporting_agents'],
                'contradictions': decision.get('contradictions', []),
                'insight': f"🌟 CONSENSUS RECOMMENDATION ({decision['consensus_level']:.0%} agreement)",
                'score': 15,  # Highest value - consensus recommendations are gold
                'agent_id': self.agent_id
            }

        elif action == 'weighted_recommendation':
            rec = decision['recommendation']

            self.metrics.insights_generated += 1
            self.knowledge_base['recommendations_made'] += 1

            return {
                'type': 'super_recommendation',
                'subtype': 'weighted',
                'recommendation': rec,
                'confidence': decision['confidence'],
                'contradictions': decision.get('contradictions', []),
                'insight': f"🎯 SYNTHESIZED RECOMMENDATION (confidence: {decision['confidence']:.0%})",
                'score': 12,
                'agent_id': self.agent_id
            }

        return {'type': 'observing', 'score': 1}

    # SYNTHESIS METHODS

    def _extract_recommendations(self, insights: List[Dict]) -> List[Dict]:
        """Extract actionable recommendations from insights"""
        recommendations = []

        for insight_wrapper in insights:
            insight = insight_wrapper.get('insight', {})
            agent_type = insight_wrapper.get('agent_type')
            agent_id = insight_wrapper.get('agent_id')
            timestamp = insight_wrapper.get('timestamp', time.time())

            # Extract different types of recommendations
            if isinstance(insight, dict):
                # From BiasHunter
                if 'biases' in insight:
                    for bias in insight.get('biases', []):
                        recommendations.append({
                            'source_agent_type': agent_type,
                            'source_agent_id': agent_id,
                            'timestamp': timestamp,
                            'type': 'bias_warning',
                            'bias_type': bias.get('bias_type'),
                            'message': bias.get('description'),
                            'severity': bias.get('severity', 0.5),
                            'actionable': True
                        })

                # From TiltDetector
                if 'tilt_probability' in insight:
                    if insight.get('tilt_probability', 0) > 0.7:
                        recommendations.append({
                            'source_agent_type': agent_type,
                            'source_agent_id': agent_id,
                            'timestamp': timestamp,
                            'type': 'tilt_warning',
                            'severity': insight['tilt_probability'],
                            'message': 'High tilt detected - stop making decisions',
                            'actionable': True
                        })

                # From CialdiniScientist
                if 'principle' in insight:
                    recommendations.append({
                        'source_agent_type': agent_type,
                        'source_agent_id': agent_id,
                        'timestamp': timestamp,
                        'type': 'persuasion_principle',
                        'principle': insight.get('principle'),
                        'message': insight.get('suggestion', ''),
                        'severity': insight.get('severity', 0.5),
                        'actionable': True
                    })

                # From PatternMatcher
                if 'patterns' in insight:
                    for pattern in insight.get('patterns', []):
                        if pattern.get('actionable'):
                            recommendations.append({
                                'source_agent_type': agent_type,
                                'source_agent_id': agent_id,
                                'timestamp': timestamp,
                                'type': 'pattern_insight',
                                'pattern_type': pattern.get('type'),
                                'message': pattern.get('recommendation', pattern.get('message')),
                                'severity': pattern.get('confidence', 0.5),
                                'actionable': True
                            })

        return recommendations

    def _detect_consensus(self, recommendations: List[Dict]) -> Optional[Dict]:
        """Detect if multiple agents agree on something"""
        if not recommendations:
            return None

        # Group by recommendation type
        by_type = {}
        for rec in recommendations:
            rec_type = rec.get('type')
            if rec_type not in by_type:
                by_type[rec_type] = []
            by_type[rec_type].append(rec)

        # Find consensus (3+ agents agreeing)
        min_consensus = self.genome.custom_params.get('min_consensus', 0.6)

        for rec_type, recs in by_type.items():
            if len(recs) >= 3:
                # We have consensus
                unique_agents = set(r.get('source_agent_type') for r in recs)

                consensus_level = len(unique_agents) / max(1, len(unique_agents))

                if consensus_level >= min_consensus:
                    return {
                        'type': rec_type,
                        'supporting_agents': list(unique_agents),
                        'recommendation_count': len(recs),
                        'consensus_level': consensus_level,
                        'recommendations': recs
                    }

        return None

    def _identify_contradictions(self, recommendations: List[Dict]) -> List[Dict]:
        """Find contradictory recommendations"""
        contradictions = []

        # Look for opposing recommendations
        # E.g., one says "bet more", another says "bet less"

        opposing_pairs = [
            ('increase', 'decrease'),
            ('continue', 'stop'),
            ('high', 'low')
        ]

        for i, rec1 in enumerate(recommendations):
            for rec2 in recommendations[i+1:]:
                msg1 = rec1.get('message', '').lower()
                msg2 = rec2.get('message', '').lower()

                for word1, word2 in opposing_pairs:
                    if (word1 in msg1 and word2 in msg2) or (word2 in msg1 and word1 in msg2):
                        contradictions.append({
                            'agent1': rec1.get('source_agent_type'),
                            'agent2': rec2.get('source_agent_type'),
                            'message1': rec1.get('message'),
                            'message2': rec2.get('message')
                        })

        return contradictions

    def _weight_by_credibility(self, recommendations: List[Dict]) -> List[Dict]:
        """Weight recommendations by agent credibility"""
        # Track agent credibility over time
        # For now, weight by recency and severity

        weighted = []

        for rec in recommendations:
            agent_type = rec.get('source_agent_type')
            agent_id = rec.get('source_agent_id')

            # Get or initialize credibility
            credibility = self.knowledge_base['agent_credibility'].get(agent_id, 0.5)

            # Weight by credibility and recency
            age = time.time() - rec.get('timestamp', time.time())
            recency_factor = max(0.1, 1.0 - (age / 3600))  # Decay over 1 hour

            weight = (
                credibility * self.genome.custom_params.get('credibility_weight', 0.7) +
                recency_factor * self.genome.custom_params.get('recency_weight', 0.3)
            )

            weighted_rec = {
                **rec,
                'weight': weight,
                'credibility': credibility,
                'recency_factor': recency_factor
            }

            weighted.append(weighted_rec)

        # Sort by weight
        weighted.sort(key=lambda x: x['weight'], reverse=True)

        return weighted

    def _build_consensus_recommendation(self, consensus: Dict,
                                       weighted_recs: List[Dict]) -> Dict:
        """Build final recommendation from consensus"""
        recs = consensus['recommendations']

        # Combine messages
        messages = [r.get('message') for r in recs if r.get('message')]
        avg_severity = statistics.mean(r.get('severity', 0.5) for r in recs)

        return {
            'action': 'CONSENSUS_ACTION',
            'type': consensus['type'],
            'supporting_agents': consensus['supporting_agents'],
            'consensus_level': consensus['consensus_level'],
            'message': messages[0] if messages else 'Multiple agents agree on this action',
            'severity': avg_severity,
            'all_messages': messages[:5]  # Top 5 messages
        }

    def _build_weighted_recommendation(self, weighted_recs: List[Dict]) -> Dict:
        """Build recommendation from weighted insights"""
        # Take top recommendation
        top_rec = weighted_recs[0]

        return {
            'action': 'WEIGHTED_ACTION',
            'type': top_rec.get('type'),
            'source': top_rec.get('source_agent_type'),
            'message': top_rec.get('message'),
            'severity': top_rec.get('severity', 0.5),
            'confidence': top_rec.get('weight', 0.5),
            'supporting_evidence': [r.get('message') for r in weighted_recs[1:4]]
        }

    def update_agent_credibility(self, agent_id: str, outcome: str):
        """Update credibility based on recommendation outcome"""
        current = self.knowledge_base['agent_credibility'].get(agent_id, 0.5)

        if outcome == 'success':
            new_credibility = min(1.0, current + 0.1)
        elif outcome == 'failure':
            new_credibility = max(0.0, current - 0.1)
        else:
            new_credibility = current

        self.knowledge_base['agent_credibility'][agent_id] = new_credibility

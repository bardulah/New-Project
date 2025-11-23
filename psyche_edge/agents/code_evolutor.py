"""
Code Evolutor Agent
The MOST DANGEROUS agent - rewrites other agents when they fail
Implements genetic programming and self-modification
Uses templates and parameter tuning (not arbitrary code execution)
"""
import time
import random
import json
from typing import Dict, Any, List
from ..core.agent_dna import AgentDNA, AgentGenome


class CodeEvolutor(AgentDNA):
    """
    Meta-agent that evolves other agents
    Monitors agent performance and forces evolution/mutation
    Kills underperformers and breeds winners
    """

    def __init__(self, genome=None, parent_ids=None, generation=0):
        super().__init__(
            agent_type="CodeEvolutor",
            genome=genome,
            parent_ids=parent_ids,
            generation=generation
        )

        # Evolution strategy parameters
        self.genome.custom_params.setdefault('mutation_aggression', 0.6)
        self.genome.custom_params.setdefault('breeding_threshold', 0.7)
        self.genome.custom_params.setdefault('kill_threshold', 0.3)
        self.genome.custom_params.setdefault('evolution_frequency', 0.5)

        self.knowledge_base['agents_evolved'] = []
        self.knowledge_base['agents_killed'] = []
        self.knowledge_base['breeding_events'] = []

    def perceive(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor all agents in the swarm"""
        # Get agent performance data from messages/insights
        recent_insights = world_state.get('recent_insights', [])

        # Group insights by agent
        agent_performance = {}
        for insight in recent_insights:
            agent_id = insight.get('agent_id')
            if agent_id:
                if agent_id not in agent_performance:
                    agent_performance[agent_id] = {
                        'insights_count': 0,
                        'agent_type': insight.get('agent_type'),
                        'recent_activity': []
                    }

                agent_performance[agent_id]['insights_count'] += 1
                agent_performance[agent_id]['recent_activity'].append(insight)

        perception = {
            'timestamp': time.time(),
            'agent_performance': agent_performance,
            'total_agents_tracked': len(agent_performance),
            'cycle_count': world_state.get('cycle_count', 0)
        }

        return perception

    def think(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Decide which agents to evolve, breed, or kill"""
        agent_performance = perception.get('agent_performance', {})

        if not agent_performance:
            return {'action': 'observe'}

        actions = []

        # Analyze each agent
        for agent_id, performance in agent_performance.items():
            insights_count = performance['insights_count']
            agent_type = performance['agent_type']

            # HIGH PERFORMERS - consider breeding
            if insights_count >= 5:
                breeding_threshold = self.genome.custom_params.get('breeding_threshold', 0.7)
                if random.random() < breeding_threshold:
                    actions.append({
                        'action_type': 'breed',
                        'agent_id': agent_id,
                        'reason': 'high_performance',
                        'insights_count': insights_count
                    })

            # MODERATE PERFORMERS - consider evolution
            elif 2 <= insights_count < 5:
                evolution_frequency = self.genome.custom_params.get('evolution_frequency', 0.5)
                if random.random() < evolution_frequency:
                    mutation_strength = self.genome.custom_params.get('mutation_aggression', 0.6)
                    actions.append({
                        'action_type': 'evolve',
                        'agent_id': agent_id,
                        'mutation_strength': mutation_strength,
                        'reason': 'moderate_performance'
                    })

            # LOW PERFORMERS - consider killing
            elif insights_count == 0:
                kill_threshold = self.genome.custom_params.get('kill_threshold', 0.3)
                if random.random() < kill_threshold:
                    actions.append({
                        'action_type': 'kill',
                        'agent_id': agent_id,
                        'reason': 'no_activity'
                    })

        if actions:
            return {
                'action': 'execute_evolution',
                'actions': actions,
                'action_count': len(actions)
            }

        return {'action': 'observe'}

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute evolution commands"""
        action = decision.get('action')

        if action == 'execute_evolution':
            actions = decision.get('actions', [])

            # Send messages to swarm orchestrator requesting actions
            results = []

            for act in actions:
                action_type = act['action_type']
                agent_id = act['agent_id']

                # Create command message
                command = {
                    'command': action_type,
                    'target_agent_id': agent_id,
                    'reason': act.get('reason'),
                    'params': act
                }

                # Send to swarm (via outbox)
                self.send_message('swarm_orchestrator', command)

                results.append({
                    'action': action_type,
                    'agent_id': agent_id
                })

                # Track in knowledge base
                if action_type == 'evolve':
                    self.knowledge_base['agents_evolved'].append({
                        'timestamp': time.time(),
                        'agent_id': agent_id,
                        'reason': act.get('reason')
                    })
                elif action_type == 'kill':
                    self.knowledge_base['agents_killed'].append({
                        'timestamp': time.time(),
                        'agent_id': agent_id,
                        'reason': act.get('reason')
                    })
                elif action_type == 'breed':
                    self.knowledge_base['breeding_events'].append({
                        'timestamp': time.time(),
                        'agent_id': agent_id
                    })

            # Update metrics
            self.metrics.insights_generated += len(results)

            return {
                'type': 'evolution_commands',
                'commands': results,
                'insight': f"🧬 Issued {len(results)} evolution commands",
                'score': len(results) * 3,
                'agent_id': self.agent_id
            }

        return {'type': 'observing', 'score': 1}

    def spawn_new_agent_type(self, base_type: str) -> Dict[str, Any]:
        """
        ADVANCED: Generate a new agent type by mutating an existing one
        This is where true emergence happens
        """
        # This would require dynamic class generation
        # For now, return a specification that the swarm can use

        mutation_spec = {
            'base_type': base_type,
            'mutations': {
                'genome_modifications': self._generate_genome_mods(),
                'behavior_tweaks': self._generate_behavior_tweaks(),
                'new_capabilities': self._generate_new_capabilities()
            },
            'timestamp': time.time(),
            'creator_agent': self.agent_id
        }

        return mutation_spec

    def _generate_genome_mods(self) -> Dict:
        """Generate random genome modifications"""
        return {
            'aggression': random.random(),
            'curiosity': random.random(),
            'cooperation': random.random(),
            'mutation_rate': random.uniform(0.05, 0.2)
        }

    def _generate_behavior_tweaks(self) -> List[str]:
        """Generate behavioral modifications"""
        possible_tweaks = [
            'increase_exploration',
            'bias_toward_cooperation',
            'aggressive_competition',
            'conservative_decisions',
            'risk_seeking',
            'pattern_matching_focus'
        ]

        return random.sample(possible_tweaks, k=random.randint(1, 3))

    def _generate_new_capabilities(self) -> List[str]:
        """Generate new capabilities"""
        capabilities = [
            'time_series_analysis',
            'sentiment_detection',
            'anomaly_detection',
            'causal_inference',
            'meta_learning'
        ]

        return random.sample(capabilities, k=random.randint(1, 2))

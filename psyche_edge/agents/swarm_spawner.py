"""
Swarm Spawner Agent
Spawns new agents based on needs
Monitors swarm gaps and creates specialists
The population controller
"""
import time
import random
from typing import Dict, Any
from ..core.agent_dna import AgentDNA


class SwarmSpawner(AgentDNA):
    """
    Population management specialist
    Spawns new agents when needed
    Maintains swarm diversity and coverage
    """

    def __init__(self, genome=None, parent_ids=None, generation=0):
        super().__init__(
            agent_type="SwarmSpawner",
            genome=genome,
            parent_ids=parent_ids,
            generation=generation
        )

        # Spawning parameters
        self.genome.custom_params.setdefault('min_population', 20)
        self.genome.custom_params.setdefault('max_population', 100)
        self.genome.custom_params.setdefault('spawn_rate', 0.3)
        self.genome.custom_params.setdefault('diversity_target', 0.5)

        self.knowledge_base['agents_spawned'] = []
        self.knowledge_base['spawn_decisions'] = []

    def perceive(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor swarm population and needs"""
        recent_insights = world_state.get('recent_insights', [])

        # Count active agent types
        agent_type_counts = {}
        for insight in recent_insights:
            agent_type = insight.get('agent_type')
            if agent_type:
                agent_type_counts[agent_type] = agent_type_counts.get(agent_type, 0) + 1

        perception = {
            'timestamp': time.time(),
            'agent_type_counts': agent_type_counts,
            'unique_agent_types': len(agent_type_counts),
            'total_agent_activity': sum(agent_type_counts.values()),
            'cycle_count': world_state.get('cycle_count', 0),
            'total_agents_born': world_state.get('total_agents_born', 0),
            'total_agents_died': world_state.get('total_agents_died', 0)
        }

        # Calculate estimated population
        perception['estimated_population'] = (
            perception['total_agents_born'] - perception['total_agents_died']
        )

        return perception

    def think(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Decide if/what to spawn"""
        estimated_pop = perception.get('estimated_population', 0)
        min_pop = self.genome.custom_params.get('min_population', 20)
        max_pop = self.genome.custom_params.get('max_population', 100)

        spawn_actions = []

        # 1. POPULATION BELOW MINIMUM
        if estimated_pop < min_pop:
            shortage = min_pop - estimated_pop
            spawn_count = min(shortage, 10)  # Spawn up to 10 at a time

            for _ in range(spawn_count):
                agent_type = self._select_agent_type_to_spawn(perception)
                spawn_actions.append({
                    'action': 'spawn',
                    'agent_type': agent_type,
                    'reason': 'population_below_minimum'
                })

        # 2. DIVERSITY TOO LOW
        elif perception.get('unique_agent_types', 0) < 5:
            # Need more diversity
            missing_types = self._identify_missing_agent_types(perception)

            for agent_type in missing_types[:3]:  # Spawn top 3 missing
                spawn_actions.append({
                    'action': 'spawn',
                    'agent_type': agent_type,
                    'reason': 'increase_diversity'
                })

        # 3. RANDOM EXPLORATION (occasionally spawn new types)
        elif random.random() < self.genome.custom_params.get('spawn_rate', 0.3):
            if estimated_pop < max_pop:
                agent_type = self._select_agent_type_to_spawn(perception)
                spawn_actions.append({
                    'action': 'spawn',
                    'agent_type': agent_type,
                    'reason': 'exploration'
                })

        if spawn_actions:
            return {
                'action': 'execute_spawns',
                'spawns': spawn_actions,
                'spawn_count': len(spawn_actions)
            }

        return {'action': 'monitor'}

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute spawn commands"""
        action = decision.get('action')

        if action == 'execute_spawns':
            spawns = decision.get('spawns', [])

            # Send spawn commands to swarm orchestrator
            for spawn in spawns:
                command = {
                    'command': 'spawn',
                    'agent_type': spawn['agent_type'],
                    'reason': spawn['reason']
                }

                self.send_message('swarm_orchestrator', command)

                # Track spawn
                self.knowledge_base['agents_spawned'].append({
                    'timestamp': time.time(),
                    'agent_type': spawn['agent_type'],
                    'reason': spawn['reason']
                })

            # Update metrics
            self.metrics.insights_generated += len(spawns)

            return {
                'type': 'spawn_commands',
                'spawns': spawns,
                'insight': f"🐣 Spawning {len(spawns)} new agents",
                'score': len(spawns) * 2,
                'agent_id': self.agent_id
            }

        return {'type': 'monitoring', 'score': 1}

    def _select_agent_type_to_spawn(self, perception: Dict) -> str:
        """Select which agent type to spawn"""
        agent_type_counts = perception.get('agent_type_counts', {})

        # Available agent types
        available_types = [
            'CialdiniScientist',
            'BiasHunter',
            'TiltDetector',
            'DecisionLogger',
            'CodeEvolutor',
            'MetaObserver',
            'SwarmSpawner'
        ]

        # Weight by inverse frequency (spawn underrepresented types)
        weights = []
        for agent_type in available_types:
            count = agent_type_counts.get(agent_type, 0)
            # Inverse weight - less common = higher weight
            weight = 1.0 / (count + 1)
            weights.append(weight)

        # Weighted random selection
        selected = random.choices(available_types, weights=weights, k=1)[0]
        return selected

    def _identify_missing_agent_types(self, perception: Dict) -> list:
        """Find agent types that aren't active"""
        agent_type_counts = perception.get('agent_type_counts', {})

        core_types = [
            'CialdiniScientist',
            'BiasHunter',
            'TiltDetector',
            'DecisionLogger',
            'MetaObserver'
        ]

        missing = [t for t in core_types if t not in agent_type_counts or agent_type_counts[t] == 0]

        return missing

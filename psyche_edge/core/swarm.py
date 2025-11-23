"""
PsycheEdge Swarm Orchestrator
Manages the entire multi-agent ecosystem:
- Agent lifecycle (birth, evolution, death)
- Competition and cooperation
- Breeding and natural selection
- World state and message routing
"""
import json
import time
import random
import pickle
from pathlib import Path
from typing import Dict, List, Any, Optional, Type, Set
from collections import defaultdict
from datetime import datetime
import threading
from queue import Queue, Empty

from .agent_dna import AgentDNA, AgentStatus, AgentMetrics


class SwarmOrchestrator:
    """
    The GOD object that manages the entire agent swarm
    Handles evolution, natural selection, message routing, and emergent behavior
    """

    def __init__(self, data_dir: str = "psyche_edge/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Agent registry
        self.agents: Dict[str, AgentDNA] = {}
        self.agent_classes: Dict[str, Type[AgentDNA]] = {}
        self.dead_agents: Dict[str, AgentDNA] = {}

        # World state - shared knowledge all agents can perceive
        self.world_state: Dict[str, Any] = {
            'timestamp': time.time(),
            'cycle_count': 0,
            'total_agents_born': 0,
            'total_agents_died': 0,
            'biometric_data': {},
            'decision_history': [],
            'recent_insights': [],
            'global_knowledge': {}
        }

        # Message routing
        self.message_queue: Queue = Queue()

        # Swarm statistics
        self.stats = {
            'total_cycles': 0,
            'total_competitions': 0,
            'total_breedings': 0,
            'total_mutations': 0,
            'lineages': defaultdict(list),  # Track family trees
            'species_count': defaultdict(int),  # Count by agent type
            'fitness_history': []
        }

        # Control flags
        self.running = False
        self.auto_evolve = True
        self.breeding_enabled = True
        self.natural_selection = True

        # Threading
        self.swarm_thread: Optional[threading.Thread] = None
        self.cycle_interval = 1.0  # Seconds between cycles

    def register_agent_class(self, agent_type: str, agent_class: Type[AgentDNA]):
        """Register a new agent class that can be spawned"""
        self.agent_classes[agent_type] = agent_class
        print(f"🧬 Registered agent class: {agent_type}")

    def spawn_agent(self, agent_type: str, **kwargs) -> AgentDNA:
        """Birth a new agent into the swarm"""
        if agent_type not in self.agent_classes:
            raise ValueError(f"Unknown agent type: {agent_type}. Register it first.")

        agent_class = self.agent_classes[agent_type]
        agent = agent_class(**kwargs)

        self.agents[agent.agent_id] = agent
        self.world_state['total_agents_born'] += 1
        self.stats['species_count'][agent_type] += 1

        # Track lineage
        if agent.parent_ids:
            for parent_id in agent.parent_ids:
                self.stats['lineages'][parent_id].append(agent.agent_id)

        print(f"🐣 Spawned: {agent}")
        return agent

    def kill_agent(self, agent_id: str, reason: str = "natural_selection"):
        """Remove an agent from the active swarm"""
        if agent_id not in self.agents:
            return

        agent = self.agents[agent_id]
        agent.status = AgentStatus.DEAD

        # Archive the dead
        self.dead_agents[agent_id] = agent
        del self.agents[agent_id]

        self.world_state['total_agents_died'] += 1
        self.stats['species_count'][agent.agent_type] -= 1

        print(f"💀 Killed: {agent} | Reason: {reason} | Fitness: {agent.metrics.fitness_score:.2f}")

        # Log death
        self._log_event('agent_death', {
            'agent_id': agent_id,
            'agent_type': agent.agent_type,
            'reason': reason,
            'final_fitness': agent.metrics.fitness_score,
            'generation': agent.generation,
            'lifespan': time.time() - agent.birth_time
        })

    def evolve_agent(self, agent_id: str) -> Optional[AgentDNA]:
        """Cause an agent to evolve (asexual reproduction)"""
        if agent_id not in self.agents:
            return None

        parent = self.agents[agent_id]
        child = parent.evolve()

        self.agents[child.agent_id] = child
        self.world_state['total_agents_born'] += 1
        self.stats['total_mutations'] += 1
        self.stats['species_count'][child.agent_type] += 1

        print(f"🧬 Evolved: {parent} -> {child}")

        self._log_event('evolution', {
            'parent_id': parent.agent_id,
            'child_id': child.agent_id,
            'generation': child.generation,
            'parent_fitness': parent.metrics.fitness_score
        })

        return child

    def breed_agents(self, agent_id1: str, agent_id2: str) -> Optional[AgentDNA]:
        """Sexual reproduction between two agents"""
        if agent_id1 not in self.agents or agent_id2 not in self.agents:
            return None

        parent1 = self.agents[agent_id1]
        parent2 = self.agents[agent_id2]

        # Both must be willing to breed
        if not (parent1.should_breed() and parent2.should_breed()):
            return None

        child = parent1.breed_with(parent2)

        self.agents[child.agent_id] = child
        self.world_state['total_agents_born'] += 1
        self.stats['total_breedings'] += 1
        self.stats['species_count'][child.agent_type] += 1

        print(f"👶 Bred: {parent1} + {parent2} -> {child}")

        self._log_event('breeding', {
            'parent1_id': parent1.agent_id,
            'parent2_id': parent2.agent_id,
            'child_id': child.agent_id,
            'generation': child.generation,
            'parent1_fitness': parent1.metrics.fitness_score,
            'parent2_fitness': parent2.metrics.fitness_score
        })

        return child

    def compete_agents(self, agent_id1: str, agent_id2: str, challenge: Dict[str, Any]) -> tuple:
        """Make two agents compete"""
        if agent_id1 not in self.agents or agent_id2 not in self.agents:
            return None, None

        agent1 = self.agents[agent_id1]
        agent2 = self.agents[agent_id2]

        winner, loser = agent1.compete_with(agent2, challenge)
        self.stats['total_competitions'] += 1

        print(f"⚔️  Competition: {winner} beat {loser}")

        self._log_event('competition', {
            'winner_id': winner.agent_id,
            'loser_id': loser.agent_id,
            'challenge': challenge,
            'winner_fitness': winner.metrics.fitness_score,
            'loser_fitness': loser.metrics.fitness_score
        })

        return winner, loser

    def run_cycle(self):
        """Execute one cycle of the swarm"""
        self.world_state['cycle_count'] += 1
        self.world_state['timestamp'] = time.time()
        self.stats['total_cycles'] += 1

        # 1. All agents perceive, think, act
        active_agents = list(self.agents.values())
        for agent in active_agents:
            if agent.status == AgentStatus.ACTIVE or agent.status == AgentStatus.SPAWNING:
                try:
                    result = agent.run_cycle(self.world_state)

                    # Store insights in world state
                    if result.get('insight'):
                        self.world_state['recent_insights'].append({
                            'agent_id': agent.agent_id,
                            'agent_type': agent.agent_type,
                            'insight': result['insight'],
                            'timestamp': time.time()
                        })

                        # Keep only recent insights
                        self.world_state['recent_insights'] = \
                            self.world_state['recent_insights'][-100:]

                except Exception as e:
                    print(f"❌ Error in {agent}: {e}")

        # 2. Route messages between agents
        self._route_messages()

        # 3. Natural selection - kill underperformers
        if self.natural_selection:
            self._natural_selection()

        # 4. Auto-evolution - evolve high performers
        if self.auto_evolve:
            self._auto_evolution()

        # 5. Breeding - sexual reproduction of fittest
        if self.breeding_enabled:
            self._auto_breeding()

        # 6. Random competitions
        self._random_competitions()

        # 7. Update statistics
        self._update_stats()

    def _route_messages(self):
        """Route messages between agents for cooperation"""
        # Collect all outbox messages
        for agent in self.agents.values():
            for msg in agent.outbox:
                recipient_id = msg.get('to')
                if recipient_id in self.agents:
                    self.agents[recipient_id].inbox.append(msg)
            agent.outbox.clear()

    def _natural_selection(self):
        """Kill agents that should die"""
        to_kill = []
        for agent_id, agent in self.agents.items():
            if agent.should_die():
                to_kill.append(agent_id)

        for agent_id in to_kill:
            self.kill_agent(agent_id, reason="low_fitness")

    def _auto_evolution(self):
        """Automatically evolve high-performing agents"""
        for agent in list(self.agents.values()):
            if agent.should_evolve():
                self.evolve_agent(agent.agent_id)

    def _auto_breeding(self):
        """Match high-fitness agents for breeding"""
        ready_to_breed = [a for a in self.agents.values() if a.should_breed()]

        if len(ready_to_breed) >= 2:
            # Sort by fitness
            ready_to_breed.sort(key=lambda a: a.metrics.fitness_score, reverse=True)

            # Breed top performers
            num_breedings = min(3, len(ready_to_breed) // 2)
            for i in range(num_breedings):
                parent1 = ready_to_breed[i * 2]
                parent2 = ready_to_breed[i * 2 + 1]
                self.breed_agents(parent1.agent_id, parent2.agent_id)

    def _random_competitions(self):
        """Randomly pit agents against each other"""
        if len(self.agents) < 2:
            return

        # Run a few random competitions each cycle
        num_competitions = min(5, len(self.agents) // 4)

        for _ in range(num_competitions):
            competitors = random.sample(list(self.agents.values()), 2)

            # Create a random challenge
            challenge = {
                'type': 'random_challenge',
                'difficulty': random.random(),
                'timestamp': time.time()
            }

            self.compete_agents(competitors[0].agent_id, competitors[1].agent_id, challenge)

    def _update_stats(self):
        """Update swarm statistics"""
        if not self.agents:
            return

        # Calculate average fitness
        total_fitness = sum(a.metrics.calculate_fitness() for a in self.agents.values())
        avg_fitness = total_fitness / len(self.agents)

        self.stats['fitness_history'].append({
            'timestamp': time.time(),
            'avg_fitness': avg_fitness,
            'max_fitness': max(a.metrics.fitness_score for a in self.agents.values()),
            'min_fitness': min(a.metrics.fitness_score for a in self.agents.values()),
            'population': len(self.agents)
        })

        # Keep only recent history
        self.stats['fitness_history'] = self.stats['fitness_history'][-1000:]

    def _log_event(self, event_type: str, data: Dict[str, Any]):
        """Log swarm events"""
        log_entry = {
            'timestamp': time.time(),
            'cycle': self.world_state['cycle_count'],
            'event_type': event_type,
            'data': data
        }

        log_file = self.data_dir / 'agent_logs' / f"{event_type}.jsonl"
        log_file.parent.mkdir(parents=True, exist_ok=True)

        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def start_swarm(self):
        """Start the swarm in background thread"""
        if self.running:
            print("⚠️  Swarm already running")
            return

        self.running = True
        self.swarm_thread = threading.Thread(target=self._swarm_loop, daemon=True)
        self.swarm_thread.start()
        print("🚀 Swarm started!")

    def stop_swarm(self):
        """Stop the swarm"""
        self.running = False
        if self.swarm_thread:
            self.swarm_thread.join(timeout=5)
        print("🛑 Swarm stopped")

    def _swarm_loop(self):
        """Main swarm loop running in background"""
        while self.running:
            try:
                self.run_cycle()
                time.sleep(self.cycle_interval)
            except Exception as e:
                print(f"❌ Swarm error: {e}")
                import traceback
                traceback.print_exc()

    def get_swarm_state(self) -> Dict[str, Any]:
        """Get current swarm state for UI/monitoring"""
        agent_summaries = [
            {
                'id': a.agent_id,
                'type': a.agent_type,
                'generation': a.generation,
                'fitness': a.metrics.fitness_score,
                'status': a.status.value,
                'age': time.time() - a.birth_time
            }
            for a in self.agents.values()
        ]

        return {
            'population': len(self.agents),
            'total_born': self.world_state['total_agents_born'],
            'total_died': self.world_state['total_agents_died'],
            'cycles': self.world_state['cycle_count'],
            'agents': agent_summaries,
            'species_count': dict(self.stats['species_count']),
            'recent_fitness': self.stats['fitness_history'][-10:] if self.stats['fitness_history'] else [],
            'running': self.running
        }

    def save_swarm(self, filepath: str):
        """Serialize and save entire swarm state"""
        state = {
            'agents': {aid: agent.to_dict() for aid, agent in self.agents.items()},
            'world_state': self.world_state,
            'stats': self.stats,
            'timestamp': time.time()
        }

        with open(filepath, 'w') as f:
            json.dumps(state, f, indent=2)

        print(f"💾 Swarm saved to {filepath}")

    def get_top_agents(self, n: int = 10) -> List[AgentDNA]:
        """Get top N agents by fitness"""
        sorted_agents = sorted(self.agents.values(),
                              key=lambda a: a.metrics.calculate_fitness(),
                              reverse=True)
        return sorted_agents[:n]

    def get_agent_lineage(self, agent_id: str) -> List[str]:
        """Get all descendants of an agent"""
        return self.stats['lineages'].get(agent_id, [])

    def force_mass_breeding(self):
        """Emergency breeding event - breed all high performers"""
        print("🔥 MASS BREEDING EVENT")
        ready = [a for a in self.agents.values() if a.metrics.fitness_score > 20]
        ready.sort(key=lambda a: a.metrics.fitness_score, reverse=True)

        bred_count = 0
        for i in range(0, len(ready) - 1, 2):
            self.breed_agents(ready[i].agent_id, ready[i + 1].agent_id)
            bred_count += 1

        print(f"👶 Mass bred {bred_count} new agents")

    def force_mass_death(self, keep_top_n: int = 10):
        """Kill all but top N agents"""
        print("☠️  MASS EXTINCTION EVENT")

        sorted_agents = sorted(self.agents.values(),
                              key=lambda a: a.metrics.fitness_score,
                              reverse=True)

        to_kill = sorted_agents[keep_top_n:]

        for agent in to_kill:
            self.kill_agent(agent.agent_id, reason="mass_extinction")

        print(f"💀 Killed {len(to_kill)} agents, {keep_top_n} survivors")

"""
Unit tests for SwarmOrchestrator
Tests agent lifecycle, breeding, competitions, and world state management
"""
import pytest
import time
from pathlib import Path

from psyche_edge.core.swarm import SwarmOrchestrator
from psyche_edge.core.agent_dna import AgentStatus
from tests.conftest import MockAgent, assert_agent_valid


class TestSwarmOrchestrator:
    """Tests for SwarmOrchestrator class"""

    def test_swarm_initialization(self, test_data_dir):
        """Test swarm initializes correctly"""
        swarm = SwarmOrchestrator(data_dir=str(test_data_dir))

        assert swarm.data_dir == Path(test_data_dir)
        assert len(swarm.agents) == 0
        assert len(swarm.agent_classes) == 0
        assert len(swarm.dead_agents) == 0
        assert swarm.world_state['cycle_count'] == 0
        assert swarm.world_state['total_agents_born'] == 0
        assert swarm.world_state['total_agents_died'] == 0
        assert swarm.running is False
        assert swarm.auto_evolve is True
        assert swarm.breeding_enabled is True
        assert swarm.natural_selection is True

    def test_register_agent_class(self, swarm_orchestrator):
        """Test registering an agent class"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)

        assert "MockAgent" in swarm_orchestrator.agent_classes
        assert swarm_orchestrator.agent_classes["MockAgent"] == MockAgent

    def test_register_multiple_agent_classes(self, swarm_orchestrator):
        """Test registering multiple agent classes"""
        swarm_orchestrator.register_agent_class("MockAgent1", MockAgent)
        swarm_orchestrator.register_agent_class("MockAgent2", MockAgent)

        assert len(swarm_orchestrator.agent_classes) == 2

    def test_spawn_agent(self, swarm_orchestrator):
        """Test spawning an agent"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)

        agent = swarm_orchestrator.spawn_agent("MockAgent")

        assert agent.agent_id in swarm_orchestrator.agents
        assert agent.agent_type == "MockAgent"
        assert swarm_orchestrator.world_state['total_agents_born'] == 1
        assert swarm_orchestrator.stats['species_count']['MockAgent'] == 1

    def test_spawn_agent_unknown_type(self, swarm_orchestrator):
        """Test spawning unknown agent type raises error"""
        with pytest.raises(ValueError, match="Unknown agent type"):
            swarm_orchestrator.spawn_agent("UnknownAgent")

    def test_spawn_multiple_agents(self, swarm_orchestrator):
        """Test spawning multiple agents"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)

        agents = []
        for _ in range(5):
            agent = swarm_orchestrator.spawn_agent("MockAgent")
            agents.append(agent)

        assert len(swarm_orchestrator.agents) == 5
        assert swarm_orchestrator.world_state['total_agents_born'] == 5
        assert swarm_orchestrator.stats['species_count']['MockAgent'] == 5

        # All agents should be unique
        agent_ids = [a.agent_id for a in agents]
        assert len(agent_ids) == len(set(agent_ids))

    def test_kill_agent(self, swarm_orchestrator):
        """Test killing an agent"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)
        agent = swarm_orchestrator.spawn_agent("MockAgent")
        agent_id = agent.agent_id

        swarm_orchestrator.kill_agent(agent_id, reason="test")

        assert agent_id not in swarm_orchestrator.agents
        assert agent_id in swarm_orchestrator.dead_agents
        assert swarm_orchestrator.dead_agents[agent_id].status == AgentStatus.DEAD
        assert swarm_orchestrator.world_state['total_agents_died'] == 1
        assert swarm_orchestrator.stats['species_count']['MockAgent'] == 0

    def test_kill_nonexistent_agent(self, swarm_orchestrator):
        """Test killing nonexistent agent doesn't crash"""
        swarm_orchestrator.kill_agent("nonexistent_id")
        # Should not raise an error

    def test_evolve_agent(self, swarm_orchestrator):
        """Test agent evolution (asexual reproduction)"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)
        parent = swarm_orchestrator.spawn_agent("MockAgent")
        parent_id = parent.agent_id

        child = swarm_orchestrator.evolve_agent(parent_id)

        assert child is not None
        assert child.agent_id in swarm_orchestrator.agents
        assert child.generation == parent.generation + 1
        assert parent_id in child.parent_ids
        assert swarm_orchestrator.stats['total_mutations'] == 1
        assert swarm_orchestrator.world_state['total_agents_born'] == 2  # Parent + child

    def test_evolve_nonexistent_agent(self, swarm_orchestrator):
        """Test evolving nonexistent agent returns None"""
        result = swarm_orchestrator.evolve_agent("nonexistent_id")
        assert result is None

    def test_breed_agents(self, swarm_orchestrator):
        """Test sexual reproduction between agents"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)

        parent1 = swarm_orchestrator.spawn_agent("MockAgent")
        parent2 = swarm_orchestrator.spawn_agent("MockAgent")

        # Set fitness high enough for breeding
        parent1.metrics.fitness_score = 100
        parent2.metrics.fitness_score = 100

        child = swarm_orchestrator.breed_agents(parent1.agent_id, parent2.agent_id)

        assert child is not None
        assert child.agent_id in swarm_orchestrator.agents
        assert parent1.agent_id in child.parent_ids
        assert parent2.agent_id in child.parent_ids
        assert child.generation == max(parent1.generation, parent2.generation) + 1
        assert swarm_orchestrator.stats['total_breedings'] == 1

    def test_breed_agents_unwilling(self, swarm_orchestrator):
        """Test breeding fails if agents unwilling"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)

        parent1 = swarm_orchestrator.spawn_agent("MockAgent")
        parent2 = swarm_orchestrator.spawn_agent("MockAgent")

        # Low fitness - won't breed
        parent1.metrics.fitness_score = 1
        parent2.metrics.fitness_score = 1

        child = swarm_orchestrator.breed_agents(parent1.agent_id, parent2.agent_id)

        assert child is None

    def test_compete_agents(self, swarm_orchestrator):
        """Test agent competition"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)

        agent1 = swarm_orchestrator.spawn_agent("MockAgent")
        agent2 = swarm_orchestrator.spawn_agent("MockAgent")

        # Give agent1 higher fitness
        agent1.metrics.fitness_score = 100
        agent2.metrics.fitness_score = 50

        challenge = {'type': 'fitness_test'}
        winner, loser = swarm_orchestrator.compete_agents(
            agent1.agent_id, agent2.agent_id, challenge
        )

        assert winner is not None
        assert loser is not None
        assert swarm_orchestrator.stats['total_competitions'] == 1

    def test_get_swarm_state(self, swarm_orchestrator):
        """Test getting swarm state summary"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)

        # Spawn and kill some agents
        for _ in range(5):
            swarm_orchestrator.spawn_agent("MockAgent")

        agent_id = list(swarm_orchestrator.agents.keys())[0]
        swarm_orchestrator.kill_agent(agent_id)

        state = swarm_orchestrator.get_swarm_state()

        assert state['population'] == 4
        assert state['total_born'] == 5
        assert state['total_died'] == 1
        assert 'MockAgent' in state['species_count']
        assert state['species_count']['MockAgent'] == 4

    def test_run_cycle_basic(self, populated_swarm):
        """Test basic swarm cycle execution"""
        initial_cycle_count = populated_swarm.world_state['cycle_count']

        populated_swarm.run_cycle()

        assert populated_swarm.world_state['cycle_count'] == initial_cycle_count + 1
        assert populated_swarm.stats['total_cycles'] == initial_cycle_count + 1

    def test_run_cycle_agents_execute(self, populated_swarm):
        """Test agents execute during cycle"""
        # Get first agent
        agent = list(populated_swarm.agents.values())[0]
        initial_activity = agent.metrics.last_active

        time.sleep(0.01)
        populated_swarm.run_cycle()

        # Agent should have been updated
        assert agent.metrics.last_active > initial_activity

    def test_world_state_update(self, swarm_orchestrator):
        """Test world state updates"""
        initial_timestamp = swarm_orchestrator.world_state['timestamp']

        time.sleep(0.01)
        swarm_orchestrator.world_state['timestamp'] = time.time()

        assert swarm_orchestrator.world_state['timestamp'] > initial_timestamp

    def test_decision_history(self, swarm_orchestrator):
        """Test adding decisions to world state"""
        decision = {
            'type': 'bet',
            'bet_size': 100,
            'outcome': 50,
            'timestamp': time.time(),
            'odds': -110
        }

        swarm_orchestrator.world_state['decision_history'].append(decision)

        assert len(swarm_orchestrator.world_state['decision_history']) == 1
        assert swarm_orchestrator.world_state['decision_history'][0] == decision

    def test_biometric_data_update(self, swarm_orchestrator):
        """Test updating biometric data"""
        biometric_data = {
            'hrv': 65.0,
            'heart_rate': 72.0,
            'sleep_score': 85.0,
            'mood': 'calm',
            'stress_level': 3,
            'timestamp': time.time()
        }

        swarm_orchestrator.world_state['biometric_data'] = biometric_data

        assert swarm_orchestrator.world_state['biometric_data']['hrv'] == 65.0
        assert swarm_orchestrator.world_state['biometric_data']['mood'] == 'calm'

    def test_lineage_tracking(self, swarm_orchestrator):
        """Test lineage tracking through evolution"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)

        parent = swarm_orchestrator.spawn_agent("MockAgent")
        child1 = swarm_orchestrator.evolve_agent(parent.agent_id)
        child2 = swarm_orchestrator.evolve_agent(parent.agent_id)

        assert parent.agent_id in swarm_orchestrator.stats['lineages']
        lineage = swarm_orchestrator.stats['lineages'][parent.agent_id]
        assert child1.agent_id in lineage
        assert child2.agent_id in lineage
        assert len(lineage) == 2

    def test_fitness_history_tracking(self, swarm_orchestrator):
        """Test fitness history is recorded"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)

        for _ in range(3):
            swarm_orchestrator.spawn_agent("MockAgent")

        # Manually add fitness history entry
        swarm_orchestrator.stats['fitness_history'].append({
            'cycle': 0,
            'avg_fitness': 50.0,
            'max_fitness': 80.0,
            'min_fitness': 20.0
        })

        assert len(swarm_orchestrator.stats['fitness_history']) == 1
        assert swarm_orchestrator.stats['fitness_history'][0]['avg_fitness'] == 50.0


class TestSwarmNaturalSelection:
    """Tests for natural selection mechanisms"""

    def test_natural_selection_kills_weak(self, populated_swarm):
        """Test natural selection removes low fitness agents"""
        # Set some agents to very low fitness
        agents = list(populated_swarm.agents.values())
        for agent in agents[:3]:
            agent.metrics.fitness_score = -20  # Very low

        initial_population = len(populated_swarm.agents)

        populated_swarm._natural_selection()

        # Should have killed some agents
        assert len(populated_swarm.agents) < initial_population

    def test_natural_selection_preserves_fit(self, populated_swarm):
        """Test natural selection keeps high fitness agents"""
        # Set all agents to high fitness
        for agent in populated_swarm.agents.values():
            agent.metrics.fitness_score = 100

        initial_population = len(populated_swarm.agents)

        populated_swarm._natural_selection()

        # Should not kill any
        assert len(populated_swarm.agents) == initial_population

    def test_auto_evolution_high_fitness(self, populated_swarm):
        """Test auto-evolution triggers for high fitness agents"""
        # Set an agent to very high fitness
        agent = list(populated_swarm.agents.values())[0]
        agent.metrics.fitness_score = 150  # High enough to evolve

        initial_population = len(populated_swarm.agents)

        populated_swarm._auto_evolution()

        # Should have spawned offspring
        assert len(populated_swarm.agents) > initial_population


class TestSwarmStatistics:
    """Tests for swarm statistics tracking"""

    def test_species_count_tracking(self, swarm_orchestrator):
        """Test species counts are tracked correctly"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)

        for _ in range(5):
            swarm_orchestrator.spawn_agent("MockAgent")

        assert swarm_orchestrator.stats['species_count']['MockAgent'] == 5

    def test_species_count_after_death(self, swarm_orchestrator):
        """Test species counts update after death"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)

        agent = swarm_orchestrator.spawn_agent("MockAgent")
        swarm_orchestrator.kill_agent(agent.agent_id)

        assert swarm_orchestrator.stats['species_count']['MockAgent'] == 0

    def test_competition_statistics(self, swarm_orchestrator):
        """Test competition stats are tracked"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)

        agent1 = swarm_orchestrator.spawn_agent("MockAgent")
        agent2 = swarm_orchestrator.spawn_agent("MockAgent")

        agent1.metrics.fitness_score = 100
        agent2.metrics.fitness_score = 50

        swarm_orchestrator.compete_agents(
            agent1.agent_id, agent2.agent_id, {'type': 'test'}
        )

        assert swarm_orchestrator.stats['total_competitions'] == 1


class TestSwarmEdgeCases:
    """Test edge cases and error conditions"""

    def test_empty_swarm_cycle(self, swarm_orchestrator):
        """Test running cycle with no agents"""
        swarm_orchestrator.run_cycle()
        # Should not crash

    def test_spawn_with_custom_params(self, swarm_orchestrator):
        """Test spawning agent with custom parameters"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)

        from psyche_edge.core.agent_dna import AgentGenome
        custom_genome = AgentGenome(aggression=0.9)

        agent = swarm_orchestrator.spawn_agent("MockAgent", genome=custom_genome)

        assert agent.genome.aggression == 0.9

    def test_large_population(self, swarm_orchestrator):
        """Test swarm handles large populations"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)

        for _ in range(100):
            swarm_orchestrator.spawn_agent("MockAgent")

        assert len(swarm_orchestrator.agents) == 100
        assert swarm_orchestrator.world_state['total_agents_born'] == 100

    def test_rapid_spawning_and_killing(self, swarm_orchestrator):
        """Test rapid agent turnover"""
        swarm_orchestrator.register_agent_class("MockAgent", MockAgent)

        for _ in range(50):
            agent = swarm_orchestrator.spawn_agent("MockAgent")
            swarm_orchestrator.kill_agent(agent.agent_id)

        assert len(swarm_orchestrator.agents) == 0
        assert len(swarm_orchestrator.dead_agents) == 50
        assert swarm_orchestrator.world_state['total_agents_born'] == 50
        assert swarm_orchestrator.world_state['total_agents_died'] == 50

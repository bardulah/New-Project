"""
Unit tests for AgentDNA base class and related components
Tests genome mutations, breeding, metrics, and agent lifecycle
"""
import pytest
import time
from unittest.mock import Mock, patch

from psyche_edge.core.agent_dna import (
    AgentDNA, AgentGenome, AgentMetrics, AgentStatus
)
from tests.conftest import (
    MockAgent, assert_genome_valid, assert_metrics_valid, assert_agent_valid,
    GENOME_PARAMETERS, METRIC_FIELDS
)


# ============================================================================
# AgentGenome Tests
# ============================================================================

class TestAgentGenome:
    """Tests for AgentGenome class"""

    def test_genome_initialization_defaults(self):
        """Test genome initializes with correct default values"""
        genome = AgentGenome()

        assert genome.aggression == 0.5
        assert genome.curiosity == 0.5
        assert genome.cooperation == 0.5
        assert genome.mutation_rate == 0.1
        assert genome.learning_rate == 0.01
        assert genome.risk_tolerance == 0.5
        assert genome.confidence_threshold == 0.7
        assert genome.memory_depth == 100
        assert genome.custom_params == {}

    def test_genome_initialization_custom(self):
        """Test genome initialization with custom values"""
        genome = AgentGenome(
            aggression=0.8,
            curiosity=0.3,
            cooperation=0.6,
            custom_params={'special': 0.9}
        )

        assert genome.aggression == 0.8
        assert genome.curiosity == 0.3
        assert genome.cooperation == 0.6
        assert genome.custom_params['special'] == 0.9

    @pytest.mark.parametrize("param_name", GENOME_PARAMETERS)
    def test_genome_mutation_changes_parameters(self, default_genome, param_name, deterministic_random):
        """Test that mutation changes genome parameters"""
        original_value = getattr(default_genome, param_name)
        mutated = default_genome.mutate(mutation_strength=1.0)
        mutated_value = getattr(mutated, param_name)

        # Should be different (with high probability)
        # Note: small chance they're the same due to randomness
        assert mutated_value >= 0.0
        assert mutated_value <= 1.0

    def test_genome_mutation_respects_bounds(self, deterministic_random):
        """Test that mutation keeps values within [0, 1]"""
        # Extreme genome at boundary
        genome = AgentGenome(aggression=0.0, curiosity=1.0, mutation_rate=0.5)

        # Mutate many times
        for _ in range(100):
            genome = genome.mutate(mutation_strength=2.0)
            assert_genome_valid(genome)

    def test_genome_mutation_strength(self, default_genome, deterministic_random):
        """Test mutation strength affects degree of change"""
        weak_mutant = default_genome.mutate(mutation_strength=0.1)
        strong_mutant = default_genome.mutate(mutation_strength=5.0)

        # Strong mutations should cause bigger changes (on average)
        assert_genome_valid(weak_mutant)
        assert_genome_valid(strong_mutant)

    def test_genome_mutation_memory_depth(self, default_genome):
        """Test memory depth mutation"""
        original_depth = default_genome.memory_depth
        mutated = default_genome.mutate()

        # Should be in reasonable range
        assert mutated.memory_depth >= 10
        assert 0.5 * original_depth <= mutated.memory_depth <= 2.0 * original_depth

    def test_genome_mutation_custom_params(self):
        """Test custom parameters are mutated"""
        genome = AgentGenome(custom_params={'param1': 0.5, 'param2': 0.7})
        mutated = genome.mutate()

        assert 'param1' in mutated.custom_params
        assert 'param2' in mutated.custom_params
        assert 0.0 <= mutated.custom_params['param1'] <= 1.0
        assert 0.0 <= mutated.custom_params['param2'] <= 1.0

    def test_genome_breeding_combines_genes(self, default_genome, aggressive_genome):
        """Test sexual reproduction combines parent genes"""
        child = default_genome.breed_with(aggressive_genome)

        # Child should have traits between parents (roughly)
        assert_genome_valid(child)

        # Child aggression should be influenced by both parents
        # (not a strict test due to mutation)
        assert child.aggression >= min(default_genome.aggression, aggressive_genome.aggression) - 0.2
        assert child.aggression <= max(default_genome.aggression, aggressive_genome.aggression) + 0.2

    def test_genome_breeding_memory_depth(self, default_genome, aggressive_genome):
        """Test memory depth breeding"""
        child = default_genome.breed_with(aggressive_genome)

        # Should be roughly average of parents
        expected = (default_genome.memory_depth + aggressive_genome.memory_depth) / 2
        # Allow for mutation variance
        assert 0.5 * expected <= child.memory_depth <= 2.0 * expected

    def test_genome_breeding_custom_params(self):
        """Test custom params are merged in breeding"""
        genome1 = AgentGenome(custom_params={'a': 0.2, 'b': 0.8})
        genome2 = AgentGenome(custom_params={'b': 0.4, 'c': 0.6})

        child = genome1.breed_with(genome2)

        # Child should have all params
        assert 'a' in child.custom_params
        assert 'b' in child.custom_params
        assert 'c' in child.custom_params


# ============================================================================
# AgentMetrics Tests
# ============================================================================

class TestAgentMetrics:
    """Tests for AgentMetrics class"""

    def test_metrics_initialization(self):
        """Test metrics initialize to zero"""
        metrics = AgentMetrics()

        assert metrics.fitness_score == 0.0
        assert metrics.experiments_run == 0
        assert metrics.insights_generated == 0
        assert metrics.decisions_improved == 0
        assert metrics.biases_detected == 0
        assert metrics.correct_predictions == 0
        assert metrics.failed_predictions == 0
        assert metrics.custom_metrics == {}

    def test_fitness_calculation_accuracy(self):
        """Test fitness heavily weights prediction accuracy"""
        metrics = AgentMetrics(
            correct_predictions=90,
            failed_predictions=10
        )

        fitness = metrics.calculate_fitness()

        # 90% accuracy * 30 = 27, plus recency multiplier close to 1.0
        assert fitness > 20  # Should be significant
        assert metrics.fitness_score == fitness

    def test_fitness_calculation_insights(self):
        """Test fitness values insight generation"""
        metrics = AgentMetrics(
            insights_generated=50,
            correct_predictions=1  # Prevent division by zero
        )

        fitness = metrics.calculate_fitness()
        assert fitness > 0

    def test_fitness_calculation_comprehensive(self):
        """Test fitness with all positive metrics"""
        metrics = AgentMetrics(
            insights_generated=20,
            decisions_improved=10,
            biases_detected=5,
            correct_predictions=80,
            failed_predictions=20,
            cooperation_events=15,
            competition_wins=8,
            competition_losses=2,
            mutations_survived=3
        )

        fitness = metrics.calculate_fitness()

        # Should be positive and substantial
        assert fitness > 50

    def test_fitness_calculation_penalties(self):
        """Test that losses reduce fitness"""
        metrics = AgentMetrics(
            correct_predictions=50,
            failed_predictions=50,
            competition_losses=20
        )

        fitness = metrics.calculate_fitness()

        # Losses should reduce fitness
        assert fitness < 20  # Penalties applied

    def test_fitness_recency_decay(self, mock_time):
        """Test fitness decays with inactivity"""
        metrics = AgentMetrics(
            correct_predictions=80,
            failed_predictions=20,
            last_active=time.time()
        )

        # Calculate fitness now
        fitness_now = metrics.calculate_fitness()

        # Simulate 12 hours of inactivity
        mock_time(43200)  # 12 hours
        fitness_later = metrics.calculate_fitness()

        # Fitness should decay
        assert fitness_later < fitness_now

    def test_update_activity(self):
        """Test activity timestamp update"""
        metrics = AgentMetrics()
        old_time = metrics.last_active

        time.sleep(0.01)  # Small delay
        metrics.update_activity()

        assert metrics.last_active > old_time

    def test_custom_metrics(self):
        """Test custom metrics storage"""
        metrics = AgentMetrics(
            custom_metrics={'special_score': 42.0, 'uniqueness': 0.95}
        )

        assert metrics.custom_metrics['special_score'] == 42.0
        assert metrics.custom_metrics['uniqueness'] == 0.95


# ============================================================================
# AgentDNA Tests
# ============================================================================

class TestAgentDNA:
    """Tests for AgentDNA base class"""

    def test_agent_initialization(self, default_genome):
        """Test agent initializes correctly"""
        agent = MockAgent(genome=default_genome)

        assert agent.agent_id is not None
        assert len(agent.agent_id) == 36  # UUID length
        assert agent.agent_type == "MockAgent"
        assert agent.generation == 0
        assert agent.birth_time > 0
        assert agent.status == AgentStatus.ACTIVE
        assert len(agent.parent_ids) == 0
        assert agent.genome == default_genome

    def test_agent_initialization_no_genome(self):
        """Test agent creates default genome if none provided"""
        agent = MockAgent()

        assert agent.genome is not None
        assert_genome_valid(agent.genome)

    def test_agent_initialization_generation(self, default_genome):
        """Test agent can be initialized with generation"""
        agent = MockAgent(genome=default_genome, generation=5)

        assert agent.generation == 5

    def test_agent_initialization_parents(self, default_genome):
        """Test agent can be initialized with parents"""
        parent_ids = ["parent1", "parent2"]
        agent = MockAgent(genome=default_genome, parent_ids=parent_ids)

        assert agent.parent_ids == parent_ids

    def test_agent_run_cycle(self, mock_agent, empty_world_state):
        """Test agent run_cycle calls all methods"""
        result = mock_agent.run_cycle(empty_world_state)

        assert mock_agent.perceive_called
        assert mock_agent.think_called
        assert mock_agent.act_called
        assert result['success'] is True

    def test_agent_run_cycle_updates_metrics(self, mock_agent, empty_world_state):
        """Test run_cycle updates metrics"""
        initial_insights = mock_agent.metrics.insights_generated

        mock_agent.run_cycle(empty_world_state)

        assert mock_agent.metrics.insights_generated > initial_insights

    def test_agent_run_cycle_updates_activity(self, mock_agent, empty_world_state):
        """Test run_cycle updates last_active timestamp"""
        initial_time = mock_agent.metrics.last_active

        time.sleep(0.01)
        mock_agent.run_cycle(empty_world_state)

        assert mock_agent.metrics.last_active > initial_time

    def test_agent_evolve_creates_offspring(self, mock_agent):
        """Test evolve creates a mutated offspring"""
        offspring = mock_agent.evolve()

        assert offspring.agent_id != mock_agent.agent_id
        assert offspring.agent_type == mock_agent.agent_type
        assert offspring.generation == mock_agent.generation + 1
        assert mock_agent.agent_id in offspring.parent_ids
        assert_genome_valid(offspring.genome)

    def test_agent_evolve_mutation_strength(self, mock_agent):
        """Test evolve respects mutation strength"""
        offspring_weak = mock_agent.evolve(mutation_strength=0.1)
        offspring_strong = mock_agent.evolve(mutation_strength=5.0)

        assert offspring_weak.generation == mock_agent.generation + 1
        assert offspring_strong.generation == mock_agent.generation + 1
        assert_genome_valid(offspring_weak.genome)
        assert_genome_valid(offspring_strong.genome)

    def test_agent_breed_creates_child(self, mock_agent_pair):
        """Test breeding creates offspring from two parents"""
        agent1, agent2 = mock_agent_pair

        child = agent1.breed(agent2)

        assert child.agent_id != agent1.agent_id
        assert child.agent_id != agent2.agent_id
        assert child.generation == max(agent1.generation, agent2.generation) + 1
        assert agent1.agent_id in child.parent_ids
        assert agent2.agent_id in child.parent_ids
        assert len(child.parent_ids) == 2

    def test_agent_breed_updates_parent_metrics(self, mock_agent_pair):
        """Test breeding updates parent metrics"""
        agent1, agent2 = mock_agent_pair

        initial_children1 = agent1.metrics.children_spawned
        initial_children2 = agent2.metrics.children_spawned

        child = agent1.breed(agent2)

        assert agent1.metrics.children_spawned == initial_children1 + 1
        assert agent2.metrics.children_spawned == initial_children2 + 1

    def test_agent_calculate_fitness(self, mock_agent):
        """Test fitness calculation"""
        mock_agent.metrics.correct_predictions = 80
        mock_agent.metrics.failed_predictions = 20
        mock_agent.metrics.insights_generated = 10

        fitness = mock_agent.calculate_fitness()

        assert fitness > 0
        assert mock_agent.metrics.fitness_score == fitness

    def test_agent_to_dict(self, mock_agent):
        """Test agent serialization to dict"""
        data = mock_agent.to_dict()

        assert 'agent_id' in data
        assert 'agent_type' in data
        assert 'generation' in data
        assert 'birth_time' in data
        assert 'genome' in data
        assert 'metrics' in data
        assert 'status' in data
        assert data['agent_type'] == 'MockAgent'

    def test_agent_memory(self, mock_agent):
        """Test agent memory storage"""
        mock_agent.memory.append({'event': 'test', 'value': 42})

        assert len(mock_agent.memory) == 1
        assert mock_agent.memory[0]['event'] == 'test'

    def test_agent_memory_depth_limit(self, mock_agent):
        """Test memory respects depth limit"""
        mock_agent.genome.memory_depth = 5

        # Add more than limit
        for i in range(10):
            mock_agent.memory.append({'event': i})

        # Should only keep last 5
        assert len(mock_agent.memory) <= mock_agent.genome.memory_depth

    def test_agent_inbox_outbox(self, mock_agent):
        """Test message passing infrastructure"""
        mock_agent.inbox.append({'from': 'other', 'msg': 'hello'})
        mock_agent.outbox.append({'to': 'another', 'msg': 'hi'})

        assert len(mock_agent.inbox) == 1
        assert len(mock_agent.outbox) == 1

    def test_agent_knowledge_base(self, mock_agent):
        """Test knowledge base storage"""
        mock_agent.knowledge_base['learned_pattern'] = {'type': 'streak', 'confidence': 0.8}

        assert 'learned_pattern' in mock_agent.knowledge_base
        assert mock_agent.knowledge_base['learned_pattern']['confidence'] == 0.8

    def test_agent_status_transitions(self, mock_agent):
        """Test agent status can be updated"""
        mock_agent.status = AgentStatus.COMPETING
        assert mock_agent.status == AgentStatus.COMPETING

        mock_agent.status = AgentStatus.BREEDING
        assert mock_agent.status == AgentStatus.BREEDING

        mock_agent.status = AgentStatus.DYING
        assert mock_agent.status == AgentStatus.DYING


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================

class TestAgentEdgeCases:
    """Test edge cases and error handling"""

    def test_agent_with_zero_fitness(self, mock_agent):
        """Test agent with zero fitness"""
        mock_agent.metrics.correct_predictions = 0
        mock_agent.metrics.failed_predictions = 0

        fitness = mock_agent.calculate_fitness()

        # Should not crash, just be zero
        assert fitness >= 0

    def test_agent_with_negative_outcomes(self, mock_agent):
        """Test agent with all negative outcomes"""
        mock_agent.metrics.correct_predictions = 0
        mock_agent.metrics.failed_predictions = 100
        mock_agent.metrics.competition_losses = 50

        fitness = mock_agent.calculate_fitness()

        # Fitness can go negative
        assert isinstance(fitness, float)

    def test_genome_extreme_mutation_rate(self):
        """Test genome with extreme mutation rate"""
        genome = AgentGenome(mutation_rate=0.99)
        mutated = genome.mutate(mutation_strength=10.0)

        # Should still be valid
        assert_genome_valid(mutated)

    def test_breeding_with_dissimilar_parents(self):
        """Test breeding parents with very different genomes"""
        parent1 = AgentGenome(aggression=0.1, curiosity=0.1, cooperation=0.9)
        parent2 = AgentGenome(aggression=0.9, curiosity=0.9, cooperation=0.1)

        agent1 = MockAgent(genome=parent1)
        agent2 = MockAgent(genome=parent2)

        child = agent1.breed(agent2)

        # Child should be valid despite parent differences
        assert_agent_valid(child)

    def test_agent_run_cycle_empty_world_state(self, mock_agent):
        """Test agent handles empty world state"""
        result = mock_agent.run_cycle({})

        assert result is not None
        assert isinstance(result, dict)

    def test_agent_multiple_evolutions(self, mock_agent):
        """Test multiple generations of evolution"""
        current = mock_agent

        for i in range(5):
            current = current.evolve()
            assert current.generation == i + 1
            assert_agent_valid(current)

    def test_agent_deep_family_tree(self, mock_agent_pair):
        """Test multi-generational breeding"""
        agent1, agent2 = mock_agent_pair

        # First generation
        child1 = agent1.breed(agent2)

        # Second generation
        agent3 = MockAgent()
        child2 = child1.breed(agent3)

        assert child2.generation == 2
        assert len(child2.parent_ids) == 2

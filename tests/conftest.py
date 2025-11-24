"""
Pytest configuration and shared fixtures for PsycheEdge tests
"""
import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any
import time

from psyche_edge.core.agent_dna import AgentDNA, AgentGenome, AgentMetrics
from psyche_edge.core.swarm import SwarmOrchestrator
from psyche_edge.core.logging_config import setup_logging
from psyche_edge.core.monitoring import SwarmMetrics, initialize_metrics
from prometheus_client import CollectorRegistry


# ============================================================================
# Test Configuration
# ============================================================================

@pytest.fixture(scope="session", autouse=True)
def setup_test_logging():
    """Set up logging for all tests"""
    temp_log_dir = Path(tempfile.mkdtemp())
    setup_logging(
        log_dir=temp_log_dir,
        log_level="DEBUG",
        enable_console_logging=False,  # Quiet during tests
        enable_json_logging=True
    )
    yield temp_log_dir
    # Cleanup
    shutil.rmtree(temp_log_dir, ignore_errors=True)


@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary data directory for tests"""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    (data_dir / "biometrics").mkdir()
    (data_dir / "decisions").mkdir()
    (data_dir / "agent_logs").mkdir()
    (data_dir / "evolution_history").mkdir()

    return data_dir


# ============================================================================
# Genome & Metrics Fixtures
# ============================================================================

@pytest.fixture
def default_genome():
    """Create a default genome for testing"""
    return AgentGenome(
        aggression=0.5,
        curiosity=0.5,
        cooperation=0.5,
        mutation_rate=0.1,
        learning_rate=0.01,
        risk_tolerance=0.5,
        confidence_threshold=0.7,
        memory_depth=100
    )


@pytest.fixture
def aggressive_genome():
    """Create an aggressive genome"""
    return AgentGenome(
        aggression=0.9,
        curiosity=0.3,
        cooperation=0.2,
        mutation_rate=0.15,
        learning_rate=0.02,
        risk_tolerance=0.8,
        confidence_threshold=0.6,
        memory_depth=50
    )


@pytest.fixture
def cooperative_genome():
    """Create a cooperative genome"""
    return AgentGenome(
        aggression=0.2,
        curiosity=0.6,
        cooperation=0.9,
        mutation_rate=0.05,
        learning_rate=0.01,
        risk_tolerance=0.3,
        confidence_threshold=0.8,
        memory_depth=150
    )


@pytest.fixture
def fresh_metrics():
    """Create fresh agent metrics"""
    return AgentMetrics()


@pytest.fixture
def experienced_metrics():
    """Create metrics for an experienced agent"""
    metrics = AgentMetrics(
        fitness_score=50.0,
        experiments_run=100,
        insights_generated=45,
        decisions_improved=20,
        biases_detected=15,
        correct_predictions=80,
        failed_predictions=20,
        cooperation_events=30,
        competition_wins=10,
        competition_losses=5,
        mutations_survived=3,
        children_spawned=2,
        uptime_seconds=3600.0
    )
    metrics.calculate_fitness()
    return metrics


# ============================================================================
# Mock Agent for Testing
# ============================================================================

class MockAgent(AgentDNA):
    """Simple agent implementation for testing base class functionality"""

    def __init__(self, *args, **kwargs):
        super().__init__(agent_type="MockAgent", *args, **kwargs)
        self.perceive_called = False
        self.think_called = False
        self.act_called = False

    def perceive(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Mock perception"""
        self.perceive_called = True
        return {
            'timestamp': world_state.get('timestamp', time.time()),
            'cycle_count': world_state.get('cycle_count', 0),
            'decision_count': len(world_state.get('decision_history', []))
        }

    def think(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Mock thinking"""
        self.think_called = True
        return {
            'action': 'test_action',
            'confidence': 0.8
        }

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Mock action"""
        self.act_called = True
        self.metrics.insights_generated += 1
        return {
            'success': True,
            'result': 'mock_result'
        }


@pytest.fixture
def mock_agent(default_genome, fresh_metrics):
    """Create a mock agent for testing"""
    return MockAgent(genome=default_genome)


@pytest.fixture
def mock_agent_pair(default_genome, aggressive_genome):
    """Create a pair of mock agents for competition/breeding tests"""
    agent1 = MockAgent(genome=default_genome)
    agent2 = MockAgent(genome=aggressive_genome)
    return agent1, agent2


# ============================================================================
# World State Fixtures
# ============================================================================

@pytest.fixture
def empty_world_state():
    """Create an empty world state"""
    return {
        'timestamp': time.time(),
        'cycle_count': 0,
        'total_agents_born': 0,
        'total_agents_died': 0,
        'biometric_data': {},
        'decision_history': [],
        'recent_insights': [],
        'global_knowledge': {}
    }


@pytest.fixture
def populated_world_state():
    """Create a populated world state with test data"""
    base_time = time.time() - 86400  # 24 hours ago

    decisions = []
    for i in range(20):
        decisions.append({
            'type': 'bet',
            'bet_size': 100,
            'outcome': (i % 3 - 1) * 100,  # Win, loss, win pattern
            'timestamp': base_time + (i * 3600),
            'odds': -110
        })

    return {
        'timestamp': time.time(),
        'cycle_count': 50,
        'total_agents_born': 30,
        'total_agents_died': 5,
        'biometric_data': {
            'hrv': 65.0,
            'heart_rate': 72.0,
            'sleep_score': 85.0,
            'mood': 'calm',
            'stress_level': 3,
            'timestamp': time.time()
        },
        'decision_history': decisions,
        'recent_insights': [],
        'global_knowledge': {
            'known_biases': ['anchoring', 'confirmation'],
            'successful_strategies': ['wait_for_value'],
            'user_patterns': {'betting_frequency': 'high'}
        }
    }


# ============================================================================
# Swarm Fixtures
# ============================================================================

@pytest.fixture
def swarm_orchestrator(test_data_dir):
    """Create a swarm orchestrator for testing"""
    return SwarmOrchestrator(data_dir=str(test_data_dir))


@pytest.fixture
def populated_swarm(swarm_orchestrator):
    """Create a swarm with multiple agents"""
    # Register mock agent class
    swarm_orchestrator.register_agent_class("MockAgent", MockAgent)

    # Spawn agents
    for _ in range(10):
        swarm_orchestrator.spawn_agent("MockAgent")

    # Add some test decisions
    for i in range(20):
        swarm_orchestrator.world_state['decision_history'].append({
            'type': 'bet',
            'bet_size': 100,
            'outcome': (i % 3 - 1) * 100,
            'timestamp': time.time() - (20 - i) * 3600,
            'odds': -110
        })

    return swarm_orchestrator


# ============================================================================
# Monitoring Fixtures
# ============================================================================

@pytest.fixture
def metrics_registry():
    """Create an isolated Prometheus registry for tests"""
    return CollectorRegistry()


@pytest.fixture
def swarm_metrics(metrics_registry):
    """Create swarm metrics with isolated registry"""
    return SwarmMetrics(registry=metrics_registry)


# ============================================================================
# Utility Fixtures
# ============================================================================

@pytest.fixture
def mock_time(monkeypatch):
    """Mock time.time() for deterministic tests"""
    current_time = 1000000.0

    def mock_time_fn():
        return current_time

    def advance_time(seconds: float):
        nonlocal current_time
        current_time += seconds

    monkeypatch.setattr(time, 'time', mock_time_fn)

    # Return the advance function so tests can control time
    return advance_time


@pytest.fixture
def deterministic_random(monkeypatch):
    """Make random deterministic for reproducible tests"""
    import random
    random.seed(42)
    yield
    # Reset after test
    random.seed()


# ============================================================================
# Parametrize Helpers
# ============================================================================

# Common parameter sets for parametrized tests
GENOME_PARAMETERS = [
    'aggression', 'curiosity', 'cooperation', 'mutation_rate',
    'learning_rate', 'risk_tolerance', 'confidence_threshold'
]

METRIC_FIELDS = [
    'experiments_run', 'insights_generated', 'decisions_improved',
    'biases_detected', 'correct_predictions', 'failed_predictions',
    'cooperation_events', 'competition_wins', 'competition_losses'
]


# ============================================================================
# Assertion Helpers
# ============================================================================

def assert_genome_valid(genome: AgentGenome):
    """Assert genome has valid values"""
    assert 0.0 <= genome.aggression <= 1.0
    assert 0.0 <= genome.curiosity <= 1.0
    assert 0.0 <= genome.cooperation <= 1.0
    assert 0.0 <= genome.mutation_rate <= 1.0
    assert 0.0 <= genome.learning_rate <= 1.0
    assert 0.0 <= genome.risk_tolerance <= 1.0
    assert 0.0 <= genome.confidence_threshold <= 1.0
    assert genome.memory_depth > 0


def assert_metrics_valid(metrics: AgentMetrics):
    """Assert metrics have valid values"""
    assert metrics.experiments_run >= 0
    assert metrics.insights_generated >= 0
    assert metrics.decisions_improved >= 0
    assert metrics.correct_predictions >= 0
    assert metrics.failed_predictions >= 0
    assert metrics.uptime_seconds >= 0.0


def assert_agent_valid(agent: AgentDNA):
    """Assert agent has valid state"""
    assert agent.agent_id is not None
    assert len(agent.agent_id) > 0
    assert agent.agent_type is not None
    assert agent.generation >= 0
    assert agent.birth_time > 0
    assert_genome_valid(agent.genome)
    assert_metrics_valid(agent.metrics)

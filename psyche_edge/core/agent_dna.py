"""
PsycheEdge Agent DNA - Base class for self-evolving agents
Each agent can mutate, breed, compete, and die based on performance
"""
import uuid
import json
import time
import random
import hashlib
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum


class AgentStatus(Enum):
    SPAWNING = "spawning"
    ACTIVE = "active"
    COMPETING = "competing"
    BREEDING = "breeding"
    DYING = "dying"
    DEAD = "dead"
    EVOLVED = "evolved"


@dataclass
class AgentGenome:
    """The genetic code of an agent - these parameters mutate and evolve"""
    aggression: float = 0.5  # How aggressively agent pursues its goals
    curiosity: float = 0.5  # How much it explores vs exploits
    cooperation: float = 0.5  # Tendency to share vs hoard insights
    mutation_rate: float = 0.1  # How much it mutates when evolving
    learning_rate: float = 0.01  # Speed of adaptation
    risk_tolerance: float = 0.5  # For decision analysis
    confidence_threshold: float = 0.7  # When to act vs observe
    memory_depth: int = 100  # How much history to track

    # Custom parameters that agents can add
    custom_params: Dict[str, float] = field(default_factory=dict)

    def mutate(self, mutation_strength: float = 1.0) -> 'AgentGenome':
        """Create a mutated copy of this genome"""
        mutated = AgentGenome(**asdict(self))

        # Mutate each float parameter
        for attr in ['aggression', 'curiosity', 'cooperation', 'mutation_rate',
                     'learning_rate', 'risk_tolerance', 'confidence_threshold']:
            current_val = getattr(mutated, attr)
            mutation = random.gauss(0, self.mutation_rate * mutation_strength)
            new_val = max(0.0, min(1.0, current_val + mutation))
            setattr(mutated, attr, new_val)

        # Mutate memory depth
        mutated.memory_depth = max(10, int(mutated.memory_depth * random.uniform(0.8, 1.2)))

        # Mutate custom params
        for key, val in mutated.custom_params.items():
            mutated.custom_params[key] = max(0.0, min(1.0,
                val + random.gauss(0, self.mutation_rate * mutation_strength)))

        return mutated

    def breed_with(self, other: 'AgentGenome') -> 'AgentGenome':
        """Sexual reproduction - combine genes from two parents"""
        child = AgentGenome()

        # Mix genes from both parents
        for attr in ['aggression', 'curiosity', 'cooperation', 'mutation_rate',
                     'learning_rate', 'risk_tolerance', 'confidence_threshold']:
            parent_val = getattr(self, attr)
            other_val = getattr(other, attr)
            # Weighted average with some randomness
            weight = random.random()
            child_val = parent_val * weight + other_val * (1 - weight)
            setattr(child, attr, child_val)

        # Mix memory depth
        child.memory_depth = int((self.memory_depth + other.memory_depth) / 2)

        # Merge custom params
        all_keys = set(self.custom_params.keys()) | set(other.custom_params.keys())
        for key in all_keys:
            val1 = self.custom_params.get(key, 0.5)
            val2 = other.custom_params.get(key, 0.5)
            child.custom_params[key] = (val1 + val2) / 2

        # Apply mutation to child
        return child.mutate(mutation_strength=0.5)


@dataclass
class AgentMetrics:
    """Performance metrics that determine survival and breeding rights"""
    fitness_score: float = 0.0  # Overall fitness
    experiments_run: int = 0
    insights_generated: int = 0
    decisions_improved: int = 0
    biases_detected: int = 0
    correct_predictions: int = 0
    failed_predictions: int = 0
    cooperation_events: int = 0
    competition_wins: int = 0
    competition_losses: int = 0
    mutations_survived: int = 0
    children_spawned: int = 0

    # Time-based metrics
    uptime_seconds: float = 0.0
    last_active: float = field(default_factory=time.time)

    # Custom metrics
    custom_metrics: Dict[str, float] = field(default_factory=dict)

    def calculate_fitness(self) -> float:
        """Calculate overall fitness score - determines survival"""
        accuracy = (self.correct_predictions / max(1, self.correct_predictions + self.failed_predictions))

        fitness = (
            accuracy * 30 +  # Prediction accuracy is king
            self.insights_generated * 2 +
            self.decisions_improved * 5 +
            self.biases_detected * 3 +
            self.cooperation_events * 1 +
            self.competition_wins * 4 -
            self.competition_losses * 2 +
            self.mutations_survived * 1
        )

        # Recency bonus - recent activity is valued
        time_since_active = time.time() - self.last_active
        recency_multiplier = max(0.1, 1.0 - (time_since_active / 86400))  # Decay over 24h

        self.fitness_score = fitness * recency_multiplier
        return self.fitness_score

    def update_activity(self):
        """Mark agent as active now"""
        self.last_active = time.time()


class AgentDNA(ABC):
    """
    Base class for all PsycheEdge agents
    Agents are autonomous, self-evolving entities that compete and cooperate
    """

    def __init__(self,
                 agent_type: str,
                 genome: Optional[AgentGenome] = None,
                 parent_ids: List[str] = None,
                 generation: int = 0):

        self.agent_id = f"{agent_type}_{uuid.uuid4().hex[:8]}"
        self.agent_type = agent_type
        self.genome = genome or AgentGenome()
        self.metrics = AgentMetrics()
        self.status = AgentStatus.SPAWNING

        # Evolution tracking
        self.generation = generation
        self.parent_ids = parent_ids or []
        self.children_ids: List[str] = []
        self.mutation_history: List[Dict] = []

        # Memory and state
        self.memory: List[Dict[str, Any]] = []
        self.knowledge_base: Dict[str, Any] = {}
        self.active_experiments: List[str] = []

        # Timing
        self.birth_time = time.time()
        self.last_evolution = time.time()

        # Message passing for cooperation
        self.inbox: List[Dict] = []
        self.outbox: List[Dict] = []

    def __str__(self):
        return f"{self.agent_type}[{self.agent_id}] Gen{self.generation} F:{self.metrics.fitness_score:.2f}"

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def perceive(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Perceive the environment and extract relevant information"""
        pass

    @abstractmethod
    def think(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Process perceptions and generate insights/decisions"""
        pass

    @abstractmethod
    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute actions based on decisions"""
        pass

    def run_cycle(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Main agent loop: perceive -> think -> act"""
        self.status = AgentStatus.ACTIVE
        self.metrics.update_activity()

        try:
            perception = self.perceive(world_state)
            decision = self.think(perception)
            action_result = self.act(decision)

            # Update memory
            self._update_memory({
                'timestamp': time.time(),
                'perception': perception,
                'decision': decision,
                'action_result': action_result
            })

            return action_result

        except Exception as e:
            self._log_error(e)
            return {'error': str(e), 'agent_id': self.agent_id}

    def evolve(self, mutation_strength: float = 1.0) -> 'AgentDNA':
        """Create an evolved version of this agent"""
        mutated_genome = self.genome.mutate(mutation_strength)

        # Create new agent of same type with mutated genome
        evolved_agent = self.__class__(
            genome=mutated_genome,
            parent_ids=[self.agent_id],
            generation=self.generation + 1
        )

        # Track evolution
        self.children_ids.append(evolved_agent.agent_id)
        self.metrics.children_spawned += 1

        mutation_event = {
            'timestamp': time.time(),
            'parent_id': self.agent_id,
            'child_id': evolved_agent.agent_id,
            'mutation_strength': mutation_strength,
            'parent_fitness': self.metrics.fitness_score,
            'genome_diff': self._genome_diff(self.genome, mutated_genome)
        }

        evolved_agent.mutation_history.append(mutation_event)
        self.last_evolution = time.time()

        return evolved_agent

    def breed_with(self, other: 'AgentDNA') -> 'AgentDNA':
        """Sexual reproduction with another agent"""
        if self.agent_type != other.agent_type:
            # Cross-species breeding creates hybrid with random type
            agent_type = random.choice([self.agent_type, other.agent_type])
        else:
            agent_type = self.agent_type

        child_genome = self.genome.breed_with(other.genome)

        # Create child
        child = type(self)(
            genome=child_genome,
            parent_ids=[self.agent_id, other.agent_id],
            generation=max(self.generation, other.generation) + 1
        )

        # Update parents
        self.children_ids.append(child.agent_id)
        other.children_ids.append(child.agent_id)
        self.metrics.children_spawned += 1
        other.metrics.children_spawned += 1

        return child

    def compete_with(self, other: 'AgentDNA', challenge: Dict[str, Any]) -> Tuple['AgentDNA', 'AgentDNA']:
        """Compete with another agent - winner/loser determined by challenge performance"""
        self.status = AgentStatus.COMPETING
        other.status = AgentStatus.COMPETING

        # Both agents run on the same challenge
        my_result = self.run_cycle(challenge)
        other_result = other.run_cycle(challenge)

        # Simple scoring - can be overridden
        my_score = my_result.get('score', 0)
        other_score = other_result.get('score', 0)

        if my_score >= other_score:
            winner, loser = self, other
        else:
            winner, loser = other, self

        winner.metrics.competition_wins += 1
        loser.metrics.competition_losses += 1

        # Update fitness
        winner.metrics.calculate_fitness()
        loser.metrics.calculate_fitness()

        return winner, loser

    def send_message(self, recipient_id: str, message: Dict[str, Any]):
        """Send a message to another agent (cooperation)"""
        self.outbox.append({
            'from': self.agent_id,
            'to': recipient_id,
            'timestamp': time.time(),
            'message': message
        })
        self.metrics.cooperation_events += 1

    def receive_messages(self) -> List[Dict]:
        """Get and clear inbox"""
        messages = self.inbox.copy()
        self.inbox.clear()
        return messages

    def should_die(self) -> bool:
        """Determine if this agent should be killed"""
        fitness = self.metrics.calculate_fitness()
        age_seconds = time.time() - self.birth_time

        # Death conditions
        if fitness < -10:  # Negative fitness threshold
            return True
        if age_seconds > 86400 and fitness < 5:  # Old and unproductive
            return True
        if self.metrics.failed_predictions > 50 and self.metrics.correct_predictions < 10:
            return True

        return False

    def should_evolve(self) -> bool:
        """Determine if this agent should spawn an evolved version"""
        fitness = self.metrics.calculate_fitness()
        time_since_evolution = time.time() - self.last_evolution

        # Evolution conditions
        if fitness > 50 and time_since_evolution > 3600:  # High fitness, not evolved recently
            return True
        if self.metrics.mutations_survived > 5:  # Stable lineage
            return True

        return False

    def should_breed(self) -> bool:
        """Determine if this agent is ready to breed"""
        fitness = self.metrics.calculate_fitness()

        # Breeding conditions - only the fittest breed
        if fitness > 100:
            return True
        if self.metrics.competition_wins > 10 and fitness > 50:
            return True

        return False

    def _update_memory(self, event: Dict[str, Any]):
        """Add to memory, respecting genome's memory depth"""
        self.memory.append(event)
        if len(self.memory) > self.genome.memory_depth:
            self.memory = self.memory[-self.genome.memory_depth:]

    def _genome_diff(self, genome1: AgentGenome, genome2: AgentGenome) -> Dict:
        """Calculate difference between genomes"""
        diff = {}
        for attr in ['aggression', 'curiosity', 'cooperation', 'mutation_rate',
                     'learning_rate', 'risk_tolerance', 'confidence_threshold']:
            val1 = getattr(genome1, attr)
            val2 = getattr(genome2, attr)
            diff[attr] = val2 - val1
        return diff

    def _log_error(self, error: Exception):
        """Log error to memory"""
        self._update_memory({
            'type': 'error',
            'timestamp': time.time(),
            'error': str(error),
            'error_type': type(error).__name__
        })

    def to_dict(self) -> Dict:
        """Serialize agent state"""
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type,
            'genome': asdict(self.genome),
            'metrics': asdict(self.metrics),
            'status': self.status.value,
            'generation': self.generation,
            'parent_ids': self.parent_ids,
            'children_ids': self.children_ids,
            'birth_time': self.birth_time,
            'knowledge_base': self.knowledge_base
        }

    def get_dna_hash(self) -> str:
        """Get unique hash of this agent's DNA"""
        dna_string = json.dumps(asdict(self.genome), sort_keys=True)
        return hashlib.sha256(dna_string.encode()).hexdigest()[:16]

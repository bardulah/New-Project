"""
Prometheus metrics for monitoring PsycheEdge swarm
Tracks performance, agent lifecycle, and system health
"""
from typing import Dict, Optional
from prometheus_client import (
    Counter, Gauge, Histogram, Summary, Info,
    CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
)
import time


class SwarmMetrics:
    """Central metrics collector for the swarm"""

    def __init__(self, registry: Optional[CollectorRegistry] = None):
        """
        Initialize metrics collector

        Args:
            registry: Prometheus registry (None = default global registry)
        """
        self.registry = registry

        # System info
        self.swarm_info = Info(
            'psyche_edge_swarm_info',
            'PsycheEdge swarm information',
            registry=self.registry
        )

        # Agent lifecycle metrics
        self.agents_active = Gauge(
            'psyche_edge_agents_active',
            'Number of currently active agents',
            ['agent_type'],
            registry=self.registry
        )

        self.agents_born_total = Counter(
            'psyche_edge_agents_born_total',
            'Total number of agents born',
            ['agent_type'],
            registry=self.registry
        )

        self.agents_died_total = Counter(
            'psyche_edge_agents_died_total',
            'Total number of agents died',
            ['agent_type', 'death_reason'],
            registry=self.registry
        )

        self.agent_age_seconds = Histogram(
            'psyche_edge_agent_age_seconds',
            'Agent lifespan in seconds',
            ['agent_type'],
            buckets=[60, 300, 600, 1800, 3600, 7200, 14400, 28800, 86400],
            registry=self.registry
        )

        # Evolution metrics
        self.mutations_total = Counter(
            'psyche_edge_mutations_total',
            'Total number of mutations',
            ['agent_type'],
            registry=self.registry
        )

        self.breedings_total = Counter(
            'psyche_edge_breedings_total',
            'Total number of breeding events',
            ['parent_type_1', 'parent_type_2'],
            registry=self.registry
        )

        self.generation_current = Gauge(
            'psyche_edge_generation_current',
            'Current maximum generation',
            registry=self.registry
        )

        self.generation_avg = Gauge(
            'psyche_edge_generation_avg',
            'Average generation of active agents',
            registry=self.registry
        )

        # Fitness metrics
        self.fitness_score = Gauge(
            'psyche_edge_fitness_score',
            'Agent fitness score',
            ['agent_id', 'agent_type', 'generation'],
            registry=self.registry
        )

        self.fitness_avg = Gauge(
            'psyche_edge_fitness_avg',
            'Average fitness across all agents',
            registry=self.registry
        )

        self.fitness_max = Gauge(
            'psyche_edge_fitness_max',
            'Maximum fitness score',
            registry=self.registry
        )

        self.fitness_min = Gauge(
            'psyche_edge_fitness_min',
            'Minimum fitness score',
            registry=self.registry
        )

        # Competition metrics
        self.competitions_total = Counter(
            'psyche_edge_competitions_total',
            'Total number of competitions',
            registry=self.registry
        )

        self.competition_wins = Counter(
            'psyche_edge_competition_wins',
            'Competition wins by agent type',
            ['agent_type'],
            registry=self.registry
        )

        # Insight metrics
        self.insights_generated_total = Counter(
            'psyche_edge_insights_generated_total',
            'Total insights generated',
            ['agent_type', 'insight_type'],
            registry=self.registry
        )

        self.insights_quality = Histogram(
            'psyche_edge_insights_quality',
            'Quality score of insights',
            ['agent_type'],
            buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            registry=self.registry
        )

        # Decision tracking
        self.decisions_logged_total = Counter(
            'psyche_edge_decisions_logged_total',
            'Total decisions logged',
            ['decision_type'],
            registry=self.registry
        )

        self.decision_outcome = Histogram(
            'psyche_edge_decision_outcome',
            'Decision outcomes (profit/loss)',
            ['decision_type'],
            buckets=[-1000, -500, -100, -50, 0, 50, 100, 500, 1000, 5000],
            registry=self.registry
        )

        # Bias detection
        self.biases_detected_total = Counter(
            'psyche_edge_biases_detected_total',
            'Total biases detected',
            ['bias_type'],
            registry=self.registry
        )

        self.bias_confidence = Histogram(
            'psyche_edge_bias_confidence',
            'Confidence of bias detection',
            ['bias_type'],
            buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            registry=self.registry
        )

        # Tilt detection
        self.tilt_probability = Gauge(
            'psyche_edge_tilt_probability',
            'Current tilt probability (0-1)',
            registry=self.registry
        )

        self.tilt_alerts_total = Counter(
            'psyche_edge_tilt_alerts_total',
            'Total tilt alerts generated',
            ['severity'],
            registry=self.registry
        )

        # Biometric data
        self.hrv_current = Gauge(
            'psyche_edge_hrv_current',
            'Current heart rate variability',
            registry=self.registry
        )

        self.heart_rate_current = Gauge(
            'psyche_edge_heart_rate_current',
            'Current heart rate',
            registry=self.registry
        )

        self.sleep_score_current = Gauge(
            'psyche_edge_sleep_score_current',
            'Current sleep score',
            registry=self.registry
        )

        self.stress_level_current = Gauge(
            'psyche_edge_stress_level_current',
            'Current stress level (1-10)',
            registry=self.registry
        )

        # Cycle performance
        self.cycle_duration_seconds = Histogram(
            'psyche_edge_cycle_duration_seconds',
            'Time to complete a swarm cycle',
            buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0],
            registry=self.registry
        )

        self.cycles_total = Counter(
            'psyche_edge_cycles_total',
            'Total number of cycles completed',
            registry=self.registry
        )

        self.cycle_errors_total = Counter(
            'psyche_edge_cycle_errors_total',
            'Total cycle errors',
            ['error_type'],
            registry=self.registry
        )

        # Agent performance
        self.agent_cycle_duration_seconds = Histogram(
            'psyche_edge_agent_cycle_duration_seconds',
            'Time for individual agent cycle',
            ['agent_type'],
            buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0],
            registry=self.registry
        )

        self.agent_errors_total = Counter(
            'psyche_edge_agent_errors_total',
            'Total agent errors',
            ['agent_type', 'error_type'],
            registry=self.registry
        )

        # Memory and performance
        self.memory_usage_bytes = Gauge(
            'psyche_edge_memory_usage_bytes',
            'Memory usage in bytes',
            ['component'],
            registry=self.registry
        )

        self.message_queue_size = Gauge(
            'psyche_edge_message_queue_size',
            'Number of messages in queue',
            registry=self.registry
        )

        self.world_state_size_bytes = Gauge(
            'psyche_edge_world_state_size_bytes',
            'Size of world state in bytes',
            registry=self.registry
        )

    def set_swarm_info(self, version: str, data_dir: str, max_population: int):
        """Set swarm metadata"""
        self.swarm_info.info({
            'version': version,
            'data_dir': data_dir,
            'max_population': str(max_population)
        })

    def record_agent_birth(self, agent_type: str):
        """Record agent birth"""
        self.agents_born_total.labels(agent_type=agent_type).inc()

    def record_agent_death(self, agent_type: str, death_reason: str, age_seconds: float):
        """Record agent death"""
        self.agents_died_total.labels(agent_type=agent_type, death_reason=death_reason).inc()
        self.agent_age_seconds.labels(agent_type=agent_type).observe(age_seconds)

    def update_active_agents(self, agent_counts: Dict[str, int]):
        """Update active agent counts by type"""
        for agent_type, count in agent_counts.items():
            self.agents_active.labels(agent_type=agent_type).set(count)

    def record_mutation(self, agent_type: str):
        """Record mutation event"""
        self.mutations_total.labels(agent_type=agent_type).inc()

    def record_breeding(self, parent_type_1: str, parent_type_2: str):
        """Record breeding event"""
        self.breedings_total.labels(
            parent_type_1=parent_type_1,
            parent_type_2=parent_type_2
        ).inc()

    def update_generation_stats(self, max_gen: int, avg_gen: float):
        """Update generation statistics"""
        self.generation_current.set(max_gen)
        self.generation_avg.set(avg_gen)

    def update_fitness_scores(self, agents_data: list):
        """Update fitness scores for all agents"""
        if not agents_data:
            return

        fitness_values = []
        for agent_data in agents_data:
            fitness = agent_data['fitness']
            fitness_values.append(fitness)

            # Update individual agent fitness (limit to top 20 to avoid cardinality explosion)
            if len(agents_data) <= 20 or agent_data.get('is_top_performer'):
                self.fitness_score.labels(
                    agent_id=agent_data['agent_id'][:12],
                    agent_type=agent_data['agent_type'],
                    generation=str(agent_data['generation'])
                ).set(fitness)

        # Update aggregate stats
        self.fitness_avg.set(sum(fitness_values) / len(fitness_values))
        self.fitness_max.set(max(fitness_values))
        self.fitness_min.set(min(fitness_values))

    def record_competition(self, winner_type: str):
        """Record competition result"""
        self.competitions_total.inc()
        self.competition_wins.labels(agent_type=winner_type).inc()

    def record_insight(self, agent_type: str, insight_type: str, quality: float = 1.0):
        """Record insight generation"""
        self.insights_generated_total.labels(
            agent_type=agent_type,
            insight_type=insight_type
        ).inc()
        self.insights_quality.labels(agent_type=agent_type).observe(quality)

    def record_decision(self, decision_type: str, outcome: Optional[float] = None):
        """Record decision logged"""
        self.decisions_logged_total.labels(decision_type=decision_type).inc()
        if outcome is not None:
            self.decision_outcome.labels(decision_type=decision_type).observe(outcome)

    def record_bias(self, bias_type: str, confidence: float):
        """Record bias detection"""
        self.biases_detected_total.labels(bias_type=bias_type).inc()
        self.bias_confidence.labels(bias_type=bias_type).observe(confidence)

    def update_tilt(self, probability: float):
        """Update tilt probability"""
        self.tilt_probability.set(probability)

    def record_tilt_alert(self, severity: str):
        """Record tilt alert"""
        self.tilt_alerts_total.labels(severity=severity).inc()

    def update_biometrics(self, hrv: Optional[float], heart_rate: Optional[float],
                         sleep_score: Optional[float], stress_level: Optional[int]):
        """Update biometric readings"""
        if hrv is not None:
            self.hrv_current.set(hrv)
        if heart_rate is not None:
            self.heart_rate_current.set(heart_rate)
        if sleep_score is not None:
            self.sleep_score_current.set(sleep_score)
        if stress_level is not None:
            self.stress_level_current.set(stress_level)

    def observe_cycle_duration(self, duration_seconds: float):
        """Record cycle duration"""
        self.cycle_duration_seconds.observe(duration_seconds)
        self.cycles_total.inc()

    def record_cycle_error(self, error_type: str):
        """Record cycle error"""
        self.cycle_errors_total.labels(error_type=error_type).inc()

    def observe_agent_cycle_duration(self, agent_type: str, duration_seconds: float):
        """Record agent cycle duration"""
        self.agent_cycle_duration_seconds.labels(agent_type=agent_type).observe(duration_seconds)

    def record_agent_error(self, agent_type: str, error_type: str):
        """Record agent error"""
        self.agent_errors_total.labels(agent_type=agent_type, error_type=error_type).inc()

    def update_memory_usage(self, component: str, bytes_used: int):
        """Update memory usage"""
        self.memory_usage_bytes.labels(component=component).set(bytes_used)

    def update_queue_size(self, size: int):
        """Update message queue size"""
        self.message_queue_size.set(size)

    def update_world_state_size(self, bytes_size: int):
        """Update world state size"""
        self.world_state_size_bytes.set(bytes_size)

    def get_metrics(self) -> bytes:
        """
        Get metrics in Prometheus format

        Returns:
            Metrics as bytes
        """
        return generate_latest(self.registry)

    def get_content_type(self) -> str:
        """Get content type for HTTP response"""
        return CONTENT_TYPE_LATEST


# Global metrics instance
_metrics: Optional[SwarmMetrics] = None


def get_metrics() -> SwarmMetrics:
    """Get global metrics instance"""
    global _metrics
    if _metrics is None:
        _metrics = SwarmMetrics()
    return _metrics


def initialize_metrics() -> SwarmMetrics:
    """Initialize and return global metrics instance"""
    global _metrics
    _metrics = SwarmMetrics()
    return _metrics


# Context manager for timing
class timer:
    """Context manager for timing operations"""

    def __init__(self, histogram, **labels):
        self.histogram = histogram
        self.labels = labels
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        duration = time.time() - self.start_time
        if self.labels:
            self.histogram.labels(**self.labels).observe(duration)
        else:
            self.histogram.observe(duration)

"""
Agent Performance Analytics
Deep analysis of agent performance, evolution trends, and swarm health
"""
import statistics
import time
from typing import Dict, List, Any, Optional
from collections import defaultdict
from pathlib import Path
import json


class SwarmAnalytics:
    """
    Advanced analytics for swarm performance
    Tracks evolution trends, agent lineages, and performance metrics
    """

    def __init__(self, data_dir: str = "psyche_edge/data"):
        self.data_dir = Path(data_dir)

    def analyze_agent_performance(self, agents: Dict[str, Any]) -> Dict:
        """Comprehensive agent performance analysis"""
        if not agents:
            return {'error': 'No agents to analyze'}

        agent_list = list(agents.values())

        analysis = {
            'population': len(agent_list),
            'avg_fitness': statistics.mean(a.metrics.fitness_score for a in agent_list),
            'max_fitness': max(a.metrics.fitness_score for a in agent_list),
            'min_fitness': min(a.metrics.fitness_score for a in agent_list),
            'fitness_std': statistics.stdev(a.metrics.fitness_score for a in agent_list) if len(agent_list) > 1 else 0,

            # Generation stats
            'avg_generation': statistics.mean(a.generation for a in agent_list),
            'max_generation': max(a.generation for a in agent_list),

            # Activity stats
            'total_insights': sum(a.metrics.insights_generated for a in agent_list),
            'total_predictions': sum(a.metrics.correct_predictions + a.metrics.failed_predictions for a in agent_list),
            'avg_accuracy': self._calculate_avg_accuracy(agent_list),

            # Competition stats
            'total_competitions': sum(a.metrics.competition_wins + a.metrics.competition_losses for a in agent_list),
            'total_wins': sum(a.metrics.competition_wins for a in agent_list),
            'total_losses': sum(a.metrics.competition_losses for a in agent_list),

            # Age stats
            'avg_age': statistics.mean(time.time() - a.birth_time for a in agent_list),
            'oldest_agent_age': max(time.time() - a.birth_time for a in agent_list),

            # Diversity metrics
            'unique_types': len(set(a.agent_type for a in agent_list)),
            'type_distribution': self._get_type_distribution(agent_list)
        }

        return analysis

    def analyze_evolution_trends(self, agents: Dict[str, Any], stats: Dict) -> Dict:
        """Analyze evolution trends over time"""
        agent_list = list(agents.values())

        # Group by generation
        by_generation = defaultdict(list)
        for agent in agent_list:
            by_generation[agent.generation].append(agent)

        generation_analysis = {}
        for gen, gen_agents in by_generation.items():
            generation_analysis[f"gen_{gen}"] = {
                'count': len(gen_agents),
                'avg_fitness': statistics.mean(a.metrics.fitness_score for a in gen_agents),
                'max_fitness': max(a.metrics.fitness_score for a in gen_agents),
                'avg_genome_aggression': statistics.mean(a.genome.aggression for a in gen_agents),
                'avg_genome_curiosity': statistics.mean(a.genome.curiosity for a in gen_agents),
                'avg_genome_cooperation': statistics.mean(a.genome.cooperation for a in gen_agents)
            }

        # Fitness trajectory
        fitness_history = stats.get('fitness_history', [])
        if len(fitness_history) >= 2:
            recent_fitness = [f['avg_fitness'] for f in fitness_history[-10:]]
            fitness_trend = 'improving' if recent_fitness[-1] > recent_fitness[0] else 'declining'
            improvement_rate = (recent_fitness[-1] - recent_fitness[0]) / max(1, len(recent_fitness))
        else:
            fitness_trend = 'insufficient_data'
            improvement_rate = 0

        return {
            'generation_breakdown': generation_analysis,
            'fitness_trend': fitness_trend,
            'improvement_rate': improvement_rate,
            'total_evolutions': stats.get('total_mutations', 0),
            'total_breedings': stats.get('total_breedings', 0)
        }

    def analyze_lineages(self, agents: Dict[str, Any], stats: Dict) -> Dict:
        """Analyze successful lineages (family trees)"""
        lineages = stats.get('lineages', {})

        # Find most successful lineages (most descendants)
        lineage_sizes = {parent: len(children) for parent, children in lineages.items()}

        if lineage_sizes:
            most_prolific = max(lineage_sizes.items(), key=lambda x: x[1])
        else:
            most_prolific = (None, 0)

        # Track lineage success (avg fitness of descendants)
        lineage_fitness = {}
        for parent, children in lineages.items():
            child_agents = [agents.get(child_id) for child_id in children if child_id in agents]
            if child_agents:
                lineage_fitness[parent] = statistics.mean(a.metrics.fitness_score for a in child_agents)

        return {
            'total_lineages': len(lineages),
            'most_prolific_parent': most_prolific[0],
            'most_descendants': most_prolific[1],
            'lineage_success_rates': lineage_fitness
        }

    def analyze_genome_evolution(self, agents: Dict[str, Any]) -> Dict:
        """Analyze how genomes are evolving"""
        agent_list = list(agents.values())

        if not agent_list:
            return {'error': 'No agents'}

        # Group by generation
        by_generation = defaultdict(list)
        for agent in agent_list:
            by_generation[agent.generation].append(agent)

        # Track genome parameter evolution
        genome_evolution = {}

        for param in ['aggression', 'curiosity', 'cooperation', 'mutation_rate',
                      'learning_rate', 'risk_tolerance', 'confidence_threshold']:
            param_by_gen = {}
            for gen, gen_agents in by_generation.items():
                values = [getattr(a.genome, param) for a in gen_agents]
                param_by_gen[f"gen_{gen}"] = {
                    'mean': statistics.mean(values),
                    'std': statistics.stdev(values) if len(values) > 1 else 0,
                    'min': min(values),
                    'max': max(values)
                }
            genome_evolution[param] = param_by_gen

        # Identify convergence or divergence
        convergence = {}
        for param, gen_data in genome_evolution.items():
            if len(gen_data) > 1:
                first_gen_std = list(gen_data.values())[0]['std']
                last_gen_std = list(gen_data.values())[-1]['std']

                if last_gen_std < first_gen_std * 0.8:
                    convergence[param] = 'converging'
                elif last_gen_std > first_gen_std * 1.2:
                    convergence[param] = 'diverging'
                else:
                    convergence[param] = 'stable'

        return {
            'genome_evolution': genome_evolution,
            'convergence_patterns': convergence
        }

    def get_top_performers(self, agents: Dict[str, Any], n: int = 10,
                          metric: str = 'fitness') -> List[Dict]:
        """Get top N performers by specified metric"""
        agent_list = list(agents.values())

        if metric == 'fitness':
            sorted_agents = sorted(agent_list,
                                  key=lambda a: a.metrics.fitness_score,
                                  reverse=True)
        elif metric == 'insights':
            sorted_agents = sorted(agent_list,
                                  key=lambda a: a.metrics.insights_generated,
                                  reverse=True)
        elif metric == 'accuracy':
            sorted_agents = sorted(agent_list,
                                  key=lambda a: self._get_accuracy(a),
                                  reverse=True)
        elif metric == 'age':
            sorted_agents = sorted(agent_list,
                                  key=lambda a: time.time() - a.birth_time,
                                  reverse=True)
        else:
            sorted_agents = agent_list

        top_agents = []
        for agent in sorted_agents[:n]:
            top_agents.append({
                'agent_id': agent.agent_id,
                'agent_type': agent.agent_type,
                'fitness': agent.metrics.fitness_score,
                'generation': agent.generation,
                'insights': agent.metrics.insights_generated,
                'accuracy': self._get_accuracy(agent),
                'age': time.time() - agent.birth_time,
                'genome': {
                    'aggression': agent.genome.aggression,
                    'curiosity': agent.genome.curiosity,
                    'cooperation': agent.genome.cooperation
                }
            })

        return top_agents

    def generate_swarm_report(self, swarm_orchestrator) -> Dict:
        """Generate comprehensive swarm health report"""
        agents = swarm_orchestrator.agents
        stats = swarm_orchestrator.stats
        world_state = swarm_orchestrator.world_state

        report = {
            'timestamp': time.time(),
            'swarm_running': swarm_orchestrator.running,

            # Performance analysis
            'performance': self.analyze_agent_performance(agents),

            # Evolution trends
            'evolution': self.analyze_evolution_trends(agents, stats),

            # Lineage analysis
            'lineages': self.analyze_lineages(agents, stats),

            # Genome evolution
            'genome_analysis': self.analyze_genome_evolution(agents),

            # Top performers
            'top_by_fitness': self.get_top_performers(agents, n=5, metric='fitness'),
            'top_by_insights': self.get_top_performers(agents, n=5, metric='insights'),

            # Recommendations
            'recommendations': self._generate_recommendations(agents, stats, world_state)
        }

        return report

    def _calculate_avg_accuracy(self, agents: List) -> float:
        """Calculate average prediction accuracy across all agents"""
        accuracies = [self._get_accuracy(a) for a in agents]
        accuracies = [a for a in accuracies if a is not None]

        return statistics.mean(accuracies) if accuracies else 0.0

    def _get_accuracy(self, agent) -> Optional[float]:
        """Get prediction accuracy for a single agent"""
        total = agent.metrics.correct_predictions + agent.metrics.failed_predictions
        if total == 0:
            return None
        return agent.metrics.correct_predictions / total

    def _get_type_distribution(self, agents: List) -> Dict:
        """Get distribution of agent types"""
        distribution = defaultdict(int)
        for agent in agents:
            distribution[agent.agent_type] += 1
        return dict(distribution)

    def _generate_recommendations(self, agents: Dict, stats: Dict,
                                 world_state: Dict) -> List[str]:
        """Generate actionable recommendations for swarm optimization"""
        recommendations = []

        # Population checks
        population = len(agents)
        if population < 10:
            recommendations.append("⚠️ Population low (<10). Consider spawning more agents.")
        elif population > 150:
            recommendations.append("⚠️ Population high (>150). Consider mass extinction event.")

        # Diversity checks
        unique_types = len(set(a.agent_type for a in agents.values()))
        if unique_types < 5:
            recommendations.append("⚠️ Low diversity. Spawn more agent types.")

        # Generation checks
        max_gen = max((a.generation for a in agents.values()), default=0)
        if max_gen == 0:
            recommendations.append("💡 No evolution yet. Wait for high-fitness agents to evolve.")
        elif max_gen >= 10:
            recommendations.append("🎉 Generation 10+ reached! System is adapting well.")

        # Fitness checks
        avg_fitness = statistics.mean(a.metrics.fitness_score for a in agents.values()) if agents else 0
        if avg_fitness < 10:
            recommendations.append("⚠️ Low average fitness. Inject more realistic data for agents to analyze.")
        elif avg_fitness > 50:
            recommendations.append("✅ High fitness! Agents are performing well.")

        # Activity checks
        total_insights = sum(a.metrics.insights_generated for a in agents.values())
        if total_insights == 0:
            recommendations.append("⚠️ No insights generated yet. Ensure decision data is being injected.")

        # Competition checks
        total_competitions = stats.get('total_competitions', 0)
        if total_competitions == 0:
            recommendations.append("⚠️ No competitions yet. Let swarm run longer.")

        return recommendations

    def save_report(self, report: Dict, filename: str = None):
        """Save analytics report to file"""
        if filename is None:
            filename = f"swarm_report_{int(time.time())}.json"

        report_dir = self.data_dir / "analytics"
        report_dir.mkdir(parents=True, exist_ok=True)

        filepath = report_dir / filename

        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        return filepath

#!/usr/bin/env python3
"""
Evolution Monitor - Watch the swarm evolve in real-time
Shows breeding, death, mutations, and fitness progression
"""
import sys
import time
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))

from psyche_edge.core.swarm import SwarmOrchestrator
from psyche_edge.core.analytics import SwarmAnalytics
from psyche_edge.agents import *


def watch_evolution(cycles=100, population=30):
    """
    Watch evolution happen in real-time
    Track generational improvements, breeding, death
    """
    print("=" * 80)
    print("🧬 EVOLUTION MONITOR - WATCHING THE SWARM EVOLVE")
    print("=" * 80)
    print()

    # Initialize
    swarm = SwarmOrchestrator(data_dir="psyche_edge/data")
    analytics = SwarmAnalytics()

    # Register all agents
    for agent_cls in [PatternMatcher, SuperAgent, BiasHunter, TiltDetector,
                      CialdiniScientist, MultiVerseExplorer, RealityDistortionField,
                      DreamStateSimulator, InfinityEngine]:
        swarm.register_agent_class(agent_cls.__name__, agent_cls)

    print(f"🐣 Spawning initial population of {population} agents...")
    agent_types = ["PatternMatcher", "SuperAgent", "BiasHunter", "TiltDetector",
                   "CialdiniScientist", "MultiVerseExplorer"]

    for i in range(population):
        swarm.spawn_agent(agent_types[i % len(agent_types)])

    print(f"✅ {len(swarm.agents)} agents spawned\n")

    # Inject realistic data
    print("📊 Injecting decision data...")
    base_time = time.time() - 86400 * 7  # 7 days ago

    for day in range(7):
        for i in range(15):  # 15 decisions per day
            decision = {
                'type': 'bet',
                'bet_size': 100,
                'outcome': (i % 3 - 1) * 100,  # Win, loss, win pattern
                'timestamp': base_time + (day * 86400) + (i * 3600),
                'odds': -110
            }
            swarm.world_state['decision_history'].append(decision)

    print(f"✅ {len(swarm.world_state['decision_history'])} decisions loaded\n")

    # Track evolution metrics
    evolution_data = {
        'generations': defaultdict(int),
        'fitness_history': [],
        'birth_events': [],
        'death_events': [],
        'breeding_events': [],
        'mutation_events': []
    }

    print("=" * 80)
    print("🚀 STARTING EVOLUTION - RUNNING {} CYCLES".format(cycles))
    print("=" * 80)
    print()

    # Run evolution
    for cycle in range(cycles):
        cycle_start_pop = len(swarm.agents)
        cycle_start_agents = set(swarm.agents.keys())

        # Run cycle
        swarm.run_cycle()

        # Track what happened
        cycle_end_agents = set(swarm.agents.keys())

        # Births
        new_agents = cycle_end_agents - cycle_start_agents
        if new_agents:
            for agent_id in new_agents:
                agent = swarm.agents.get(agent_id)
                if agent:
                    evolution_data['birth_events'].append({
                        'cycle': cycle,
                        'agent_id': agent_id,
                        'agent_type': agent.agent_type,
                        'generation': agent.generation,
                        'parents': len(agent.parent_ids)
                    })

        # Deaths
        dead_agents = cycle_start_agents - cycle_end_agents
        if dead_agents:
            evolution_data['death_events'].append({
                'cycle': cycle,
                'count': len(dead_agents)
            })

        # Calculate stats
        if swarm.agents:
            fitness_values = [a.metrics.fitness_score for a in swarm.agents.values()]
            generations = [a.generation for a in swarm.agents.values()]

            evolution_data['fitness_history'].append({
                'cycle': cycle,
                'avg_fitness': sum(fitness_values) / len(fitness_values),
                'max_fitness': max(fitness_values),
                'min_fitness': min(fitness_values),
                'population': len(swarm.agents),
                'max_generation': max(generations),
                'avg_generation': sum(generations) / len(generations)
            })

            # Track generations
            for gen in generations:
                evolution_data['generations'][gen] += 1

        # Print progress every 10 cycles
        if (cycle + 1) % 10 == 0:
            current = evolution_data['fitness_history'][-1]
            births = len([e for e in evolution_data['birth_events'] if e['cycle'] >= cycle - 9])
            deaths = sum(e['count'] for e in evolution_data['death_events'] if e['cycle'] >= cycle - 9)

            print(f"Cycle {cycle + 1}/{cycles}")
            print(f"  Pop: {current['population']} | "
                  f"Avg Fitness: {current['avg_fitness']:.1f} | "
                  f"Max Gen: {int(current['max_generation'])}")
            print(f"  Births: {births} | Deaths: {deaths} | "
                  f"Max Fitness: {current['max_fitness']:.1f}")

            # Show top agent
            top_agent = max(swarm.agents.values(), key=lambda a: a.metrics.fitness_score)
            print(f"  👑 Top: {top_agent.agent_type} Gen{top_agent.generation} "
                  f"F:{top_agent.metrics.fitness_score:.1f}")
            print()

    print()
    print("=" * 80)
    print("📊 EVOLUTION COMPLETE - ANALYZING RESULTS")
    print("=" * 80)
    print()

    # Final analysis
    final_state = swarm.get_swarm_state()

    print("POPULATION DYNAMICS:")
    print(f"  Starting: {population}")
    print(f"  Final: {final_state['population']}")
    print(f"  Total Born: {final_state['total_born']}")
    print(f"  Total Died: {final_state['total_died']}")
    print(f"  Net Change: {final_state['population'] - population:+d}")
    print()

    print("GENERATIONAL PROGRESS:")
    max_gen = max(evolution_data['generations'].keys()) if evolution_data['generations'] else 0
    print(f"  Highest Generation: {max_gen}")
    print(f"  Generation Distribution:")
    for gen in sorted(evolution_data['generations'].keys())[:10]:
        count = evolution_data['generations'][gen]
        bar = "█" * min(50, count)
        print(f"    Gen {gen}: {bar} ({count})")
    print()

    print("FITNESS EVOLUTION:")
    if len(evolution_data['fitness_history']) > 1:
        first = evolution_data['fitness_history'][0]
        last = evolution_data['fitness_history'][-1]

        print(f"  Initial Avg: {first['avg_fitness']:.1f}")
        print(f"  Final Avg: {last['avg_fitness']:.1f}")
        print(f"  Improvement: {last['avg_fitness'] - first['avg_fitness']:+.1f} "
              f"({((last['avg_fitness'] - first['avg_fitness']) / max(first['avg_fitness'], 1) * 100):+.1f}%)")
        print()
        print(f"  Initial Max: {first['max_fitness']:.1f}")
        print(f"  Final Max: {last['max_fitness']:.1f}")
        print(f"  Improvement: {last['max_fitness'] - first['max_fitness']:+.1f}")
    print()

    print("EVOLUTIONARY EVENTS:")
    print(f"  Total Births: {len(evolution_data['birth_events'])}")
    print(f"  Total Deaths: {sum(e['count'] for e in evolution_data['death_events'])}")
    print(f"  Total Mutations: {swarm.stats.get('total_mutations', 0)}")
    print(f"  Total Breedings: {swarm.stats.get('total_breedings', 0)}")
    print(f"  Total Competitions: {swarm.stats.get('total_competitions', 0)}")
    print()

    print("TOP 10 SURVIVORS:")
    top_agents = sorted(swarm.agents.values(), key=lambda a: a.metrics.fitness_score, reverse=True)[:10]

    for i, agent in enumerate(top_agents, 1):
        age_minutes = (time.time() - agent.birth_time) / 60
        print(f"  {i}. {agent.agent_type}")
        print(f"     Gen: {agent.generation} | Fitness: {agent.metrics.fitness_score:.1f} | "
              f"Age: {age_minutes:.1f}m")
        print(f"     Insights: {agent.metrics.insights_generated} | "
              f"Wins: {agent.metrics.competition_wins}")
        print(f"     Genome: agg={agent.genome.aggression:.2f} cur={agent.genome.curiosity:.2f} "
              f"coop={agent.genome.cooperation:.2f}")
        print()

    # Genome evolution analysis
    print("GENOME EVOLUTION:")
    genome_by_gen = defaultdict(lambda: {'aggression': [], 'curiosity': [], 'cooperation': []})

    for agent in swarm.agents.values():
        genome_by_gen[agent.generation]['aggression'].append(agent.genome.aggression)
        genome_by_gen[agent.generation]['curiosity'].append(agent.genome.curiosity)
        genome_by_gen[agent.generation]['cooperation'].append(agent.genome.cooperation)

    for gen in sorted(genome_by_gen.keys())[:5]:
        data = genome_by_gen[gen]
        if data['aggression']:
            print(f"  Gen {gen}:")
            print(f"    Aggression: {sum(data['aggression'])/len(data['aggression']):.3f}")
            print(f"    Curiosity: {sum(data['curiosity'])/len(data['curiosity']):.3f}")
            print(f"    Cooperation: {sum(data['cooperation'])/len(data['cooperation']):.3f}")
    print()

    # Species evolution
    print("SPECIES EVOLUTION:")
    print(f"  Current Species:")
    for species, count in sorted(final_state['species_count'].items(), key=lambda x: x[1], reverse=True):
        print(f"    {species}: {count}")
    print()

    # Lineage analysis
    print("SUCCESSFUL LINEAGES:")
    lineages = swarm.stats.get('lineages', {})
    if lineages:
        top_lineages = sorted(lineages.items(), key=lambda x: len(x[1]), reverse=True)[:5]

        for parent_id, children in top_lineages:
            # Find parent if still alive
            if parent_id in swarm.agents:
                parent = swarm.agents[parent_id]
                print(f"  {parent.agent_type} (Gen{parent.generation})")
                print(f"    Descendants: {len(children)}")
                print(f"    Parent Fitness: {parent.metrics.fitness_score:.1f}")
            elif parent_id in swarm.dead_agents:
                parent = swarm.dead_agents[parent_id]
                print(f"  {parent.agent_type} (Gen{parent.generation}) [DEAD]")
                print(f"    Descendants: {len(children)}")
                print(f"    Final Fitness: {parent.metrics.fitness_score:.1f}")
            print()

    print("=" * 80)
    print("✅ EVOLUTION ANALYSIS COMPLETE")
    print("=" * 80)
    print()

    return swarm, evolution_data


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Watch swarm evolution in real-time")
    parser.add_argument('--cycles', type=int, default=100, help='Number of cycles to run')
    parser.add_argument('--population', type=int, default=30, help='Initial population size')

    args = parser.parse_args()

    swarm, data = watch_evolution(cycles=args.cycles, population=args.population)

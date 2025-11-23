#!/usr/bin/env python3
"""
PsycheEdge 2025 - Main Entry Point
Initializes the swarm and starts the evolutionary process
"""
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from psyche_edge.core.swarm import SwarmOrchestrator
from psyche_edge.agents import (
    CialdiniScientist,
    BiasHunter,
    TiltDetector,
    DecisionLogger,
    CodeEvolutor,
    MetaObserver,
    SwarmSpawner
)


def initialize_swarm(target_population: int = 40) -> SwarmOrchestrator:
    """
    Initialize PsycheEdge swarm with initial agent population
    NO PLANNING. Just spawn and let chaos reign.
    """
    print("=" * 80)
    print("🧠 PSYCHE EDGE 2025 - INITIALIZING SWARM")
    print("=" * 80)
    print()

    # Create swarm orchestrator
    swarm = SwarmOrchestrator(data_dir="psyche_edge/data")

    # Register all agent classes
    print("📋 Registering agent classes...")
    swarm.register_agent_class("CialdiniScientist", CialdiniScientist)
    swarm.register_agent_class("BiasHunter", BiasHunter)
    swarm.register_agent_class("TiltDetector", TiltDetector)
    swarm.register_agent_class("DecisionLogger", DecisionLogger)
    swarm.register_agent_class("CodeEvolutor", CodeEvolutor)
    swarm.register_agent_class("MetaObserver", MetaObserver)
    swarm.register_agent_class("SwarmSpawner", SwarmSpawner)
    print()

    # Calculate initial distribution
    core_agents = {
        "CialdiniScientist": 8,
        "BiasHunter": 8,
        "TiltDetector": 6,
        "DecisionLogger": 4,
        "CodeEvolutor": 4,
        "MetaObserver": 3,
        "SwarmSpawner": 2
    }

    # Scale to target population
    total_core = sum(core_agents.values())
    scale_factor = target_population / total_core

    print(f"🐣 SPAWNING INITIAL POPULATION (target: {target_population})")
    print("-" * 80)

    spawned_agents = []

    for agent_type, base_count in core_agents.items():
        count = max(1, int(base_count * scale_factor))

        print(f"\n{agent_type}:")
        for i in range(count):
            agent = swarm.spawn_agent(agent_type)
            spawned_agents.append(agent)
            print(f"  ✓ {agent.agent_id}")

    print()
    print("=" * 80)
    print(f"🎉 SWARM INITIALIZED: {len(spawned_agents)} agents born")
    print("=" * 80)
    print()

    return swarm


def run_swarm_simulation(swarm: SwarmOrchestrator, cycles: int = None):
    """
    Run the swarm simulation
    If cycles is None, run forever
    """
    print("🚀 STARTING SWARM SIMULATION")
    print()

    if cycles:
        print(f"Will run for {cycles} cycles")
        for cycle in range(cycles):
            swarm.run_cycle()

            if cycle % 10 == 0:
                state = swarm.get_swarm_state()
                print(f"\n📊 Cycle {cycle}: {state['population']} agents alive")
                print(f"   Born: {state['total_born']} | Died: {state['total_died']}")

                if state['recent_fitness']:
                    latest = state['recent_fitness'][-1]
                    print(f"   Avg Fitness: {latest['avg_fitness']:.2f} | Max: {latest['max_fitness']:.2f}")

            time.sleep(0.1)  # Brief pause between cycles
    else:
        print("Running indefinitely... (Ctrl+C to stop)")
        swarm.start_swarm()

        try:
            while swarm.running:
                time.sleep(10)
                state = swarm.get_swarm_state()
                print(f"\n📊 Population: {state['population']} | Cycles: {state['cycles']}")

                if state['recent_fitness']:
                    latest = state['recent_fitness'][-1]
                    print(f"   Avg Fitness: {latest['avg_fitness']:.2f}")

        except KeyboardInterrupt:
            print("\n\n⚠️  Stopping swarm...")
            swarm.stop_swarm()
            print("✅ Swarm stopped")


def inject_test_decision(swarm: SwarmOrchestrator):
    """Inject a test decision for agents to analyze"""
    test_decision = {
        'type': 'bet',
        'sport': 'NBA',
        'bet_type': 'spread',
        'bet_size': 100,
        'odds': -110,
        'timestamp': time.time(),
        'notes': 'Lakers -5.5, they look good'
    }

    swarm.world_state['decision_history'].append(test_decision)
    print(f"\n💉 Injected test decision: {test_decision['type']}")


def inject_test_biometrics(swarm: SwarmOrchestrator):
    """Inject test biometric data"""
    import random

    test_biometrics = {
        'hrv': random.randint(40, 80),
        'heart_rate': random.randint(60, 90),
        'sleep_score': random.randint(60, 95),
        'mood': random.choice(['calm', 'anxious', 'excited', 'neutral']),
        'stress_level': random.randint(1, 10),
        'timestamp': time.time()
    }

    swarm.world_state['biometric_data'] = test_biometrics
    print(f"\n💓 Injected biometrics: HRV={test_biometrics['hrv']}, Mood={test_biometrics['mood']}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="PsycheEdge 2025 - Self-Evolving Decision Laboratory")
    parser.add_argument('--population', type=int, default=40, help='Initial population size')
    parser.add_argument('--cycles', type=int, default=None, help='Number of cycles to run (None = forever)')
    parser.add_argument('--inject-test-data', action='store_true', help='Inject test decisions and biometrics')

    args = parser.parse_args()

    # Initialize swarm
    swarm = initialize_swarm(target_population=args.population)

    # Inject test data if requested
    if args.inject_test_data:
        print("\n🧪 INJECTING TEST DATA")
        print("-" * 80)
        inject_test_biometrics(swarm)
        inject_test_decision(swarm)
        inject_test_decision(swarm)
        inject_test_decision(swarm)
        print()

    # Run simulation
    run_swarm_simulation(swarm, cycles=args.cycles)

    # Print final statistics
    print("\n" + "=" * 80)
    print("📈 FINAL STATISTICS")
    print("=" * 80)

    state = swarm.get_swarm_state()
    print(f"Population: {state['population']}")
    print(f"Total Born: {state['total_born']}")
    print(f"Total Died: {state['total_died']}")
    print(f"Cycles: {state['cycles']}")
    print(f"Species: {state['species_count']}")

    print("\n🏆 TOP AGENTS:")
    for i, agent in enumerate(swarm.get_top_agents(5), 1):
        print(f"{i}. {agent} | Fitness: {agent.metrics.fitness_score:.2f}")

    print("\n✅ PsycheEdge session complete")


if __name__ == "__main__":
    main()

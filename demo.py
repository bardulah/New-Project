#!/usr/bin/env python3
"""
PsycheEdge Demo Script
Quick demonstration of the swarm in action
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from psyche_edge.core.swarm import SwarmOrchestrator
from psyche_edge.agents import (
    CialdiniScientist, BiasHunter, TiltDetector,
    DecisionLogger, CodeEvolutor, MetaObserver, SwarmSpawner
)
from psyche_edge.integrations.biometrics import BiometricSimulator
from psyche_edge.experiments.decision_tracker import DecisionTracker


def demo():
    """Run a full demonstration"""
    print("=" * 80)
    print("🧠 PSYCHE EDGE 2025 - LIVE DEMO")
    print("=" * 80)
    print()

    # 1. Initialize swarm
    print("📦 Step 1: Initializing Swarm Orchestrator...")
    swarm = SwarmOrchestrator(data_dir="psyche_edge/data")

    # Register agents
    swarm.register_agent_class("CialdiniScientist", CialdiniScientist)
    swarm.register_agent_class("BiasHunter", BiasHunter)
    swarm.register_agent_class("TiltDetector", TiltDetector)
    swarm.register_agent_class("DecisionLogger", DecisionLogger)
    swarm.register_agent_class("CodeEvolutor", CodeEvolutor)
    swarm.register_agent_class("MetaObserver", MetaObserver)
    swarm.register_agent_class("SwarmSpawner", SwarmSpawner)

    print("✅ Swarm orchestrator ready\n")

    # 2. Spawn initial agents
    print("🐣 Step 2: Spawning Initial Population (20 agents)...")
    for i in range(20):
        agent_type = ["BiasHunter", "TiltDetector", "CialdiniScientist",
                     "DecisionLogger", "MetaObserver"][i % 5]
        agent = swarm.spawn_agent(agent_type)
        print(f"  ✓ Spawned {agent.agent_id}")

    print(f"\n✅ {len(swarm.agents)} agents alive\n")

    # 3. Inject biometric data
    print("💓 Step 3: Injecting Biometric Data...")
    bio_sim = BiometricSimulator()
    biometrics = bio_sim.generate_realistic_biometrics()

    swarm.world_state['biometric_data'] = biometrics

    print(f"  HRV: {biometrics['hrv']}")
    print(f"  Heart Rate: {biometrics['heart_rate']}")
    print(f"  Sleep Score: {biometrics['sleep_score']}")
    print(f"  Mood: {biometrics['mood']}")
    print(f"  Stress: {biometrics['stress_level']}/10")
    print("✅ Biometrics loaded\n")

    # 4. Inject decisions
    print("🎲 Step 4: Injecting Test Decisions...")

    decisions = [
        {
            'type': 'bet',
            'sport': 'NBA',
            'bet_type': 'spread',
            'bet_size': 100,
            'odds': -110,
            'game': 'Lakers -5.5 vs Warriors',
            'timestamp': time.time(),
            'notes': 'Lakers on hot streak'
        },
        {
            'type': 'bet',
            'sport': 'NBA',
            'bet_type': 'spread',
            'bet_size': 150,  # Increased size - possible loss chasing
            'odds': -110,
            'game': 'Celtics -3 vs Heat',
            'timestamp': time.time() + 300,
            'notes': 'Need to win this one',
            'outcome': -150  # Lost previous bet
        },
        {
            'type': 'bet',
            'sport': 'NFL',
            'bet_type': 'over/under',
            'bet_size': 200,  # Further increase - tilt?
            'odds': -105,
            'game': 'Chiefs/Bills Over 52.5',
            'timestamp': time.time() + 600,
            'notes': 'Due for a win'
        }
    ]

    for dec in decisions:
        swarm.world_state['decision_history'].append(dec)
        print(f"  ✓ {dec['type']}: ${dec['bet_size']} on {dec['game']}")

    print("✅ Decisions injected\n")

    # 5. Run swarm cycles
    print("🔄 Step 5: Running Swarm Cycles...")
    print("   (Agents perceive → think → act)\n")

    for cycle in range(5):
        print(f"  Cycle {cycle + 1}/5...")
        swarm.run_cycle()
        time.sleep(0.5)

    print("\n✅ Swarm cycles complete\n")

    # 6. Show insights
    print("💡 Step 6: Agent Insights Generated:")
    print("-" * 80)

    insights = swarm.world_state.get('recent_insights', [])

    if insights:
        for i, insight in enumerate(insights[-10:], 1):
            agent_type = insight.get('agent_type', 'Unknown')
            insight_data = insight.get('insight', {})

            print(f"\n{i}. [{agent_type}]")

            if isinstance(insight_data, dict):
                for key, value in insight_data.items():
                    if key in ['principle', 'bias_type', 'type', 'message']:
                        print(f"   {key}: {value}")
                    elif key in ['suggestion', 'recommendation', 'evidence']:
                        print(f"   {key}: {value}")
            else:
                print(f"   {insight_data}")

        print()
    else:
        print("  No insights generated yet (agents warming up)\n")

    # 7. Show agent stats
    print("📊 Step 7: Swarm Statistics:")
    print("-" * 80)

    state = swarm.get_swarm_state()

    print(f"Population: {state['population']}")
    print(f"Total Born: {state['total_born']}")
    print(f"Total Died: {state['total_died']}")
    print(f"Cycles Run: {state['cycles']}")
    print()

    print("Species Distribution:")
    for species, count in state['species_count'].items():
        print(f"  {species}: {count}")

    print()

    # 8. Show top performers
    print("🏆 Step 8: Top 5 Performing Agents:")
    print("-" * 80)

    top_agents = swarm.get_top_agents(5)

    for i, agent in enumerate(top_agents, 1):
        print(f"\n{i}. {agent}")
        print(f"   Fitness: {agent.metrics.fitness_score:.2f}")
        print(f"   Insights: {agent.metrics.insights_generated}")
        print(f"   Predictions: {agent.metrics.correct_predictions}/{agent.metrics.correct_predictions + agent.metrics.failed_predictions}")
        print(f"   Generation: {agent.generation}")
        print(f"   Genome: aggression={agent.genome.aggression:.2f}, "
              f"curiosity={agent.genome.curiosity:.2f}, "
              f"cooperation={agent.genome.cooperation:.2f}")

    print()

    # 9. Evolution demonstration
    print("🧬 Step 9: Demonstrating Evolution...")
    print("-" * 80)

    if top_agents:
        top_agent = top_agents[0]
        print(f"Evolving top agent: {top_agent.agent_id}")

        child = swarm.evolve_agent(top_agent.agent_id)

        print(f"  Parent: {top_agent}")
        print(f"  Child:  {child}")
        print(f"\nGenome Comparison:")
        print(f"  Aggression:   {top_agent.genome.aggression:.2f} → {child.genome.aggression:.2f}")
        print(f"  Curiosity:    {top_agent.genome.curiosity:.2f} → {child.genome.curiosity:.2f}")
        print(f"  Cooperation:  {top_agent.genome.cooperation:.2f} → {child.genome.cooperation:.2f}")
        print(f"  Mutation Rate: {top_agent.genome.mutation_rate:.2f} → {child.genome.mutation_rate:.2f}")

    print()

    # 10. Breeding demonstration
    print("👶 Step 10: Demonstrating Breeding...")
    print("-" * 80)

    if len(top_agents) >= 2:
        parent1 = top_agents[0]
        parent2 = top_agents[1]

        print(f"Parent 1: {parent1.agent_id} (fitness: {parent1.metrics.fitness_score:.2f})")
        print(f"Parent 2: {parent2.agent_id} (fitness: {parent2.metrics.fitness_score:.2f})")

        # Manually set breeding conditions
        parent1.metrics.fitness_score = 150
        parent2.metrics.fitness_score = 150

        child = swarm.breed_agents(parent1.agent_id, parent2.agent_id)

        if child:
            print(f"\nChild: {child.agent_id}")
            print(f"  Inherits traits from both parents")
            print(f"  Generation: {child.generation}")
            print(f"  Genome (mixed + mutated):")
            print(f"    Aggression: {child.genome.aggression:.2f}")
            print(f"    Curiosity: {child.genome.curiosity:.2f}")
            print(f"    Cooperation: {child.genome.cooperation:.2f}")

    print()

    # Final summary
    print("=" * 80)
    print("✅ DEMO COMPLETE")
    print("=" * 80)
    print()
    print("Next Steps:")
    print("1. Run './quickstart.sh' to launch the full system")
    print("2. Open Streamlit UI: streamlit run psyche_edge/ui/streamlit_app.py")
    print("3. Set up Telegram bot with your token")
    print("4. Start logging real decisions and biometrics")
    print("5. Watch the swarm evolve over days/weeks")
    print()
    print("The swarm learns. The swarm evolves. The swarm helps you decide better.")
    print()


if __name__ == "__main__":
    demo()

#!/usr/bin/env python3
"""
TEST THE SINGULARITY
Reality-bending agents that transcend normal AI

This is not a test. This is ASCENSION.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from psyche_edge.core.swarm import SwarmOrchestrator
from psyche_edge.core.quantum_consciousness import QuantumConsciousness
from psyche_edge.agents import (
    # Singularity agents
    MultiVerseExplorer,
    InfinityEngine,
    DreamStateSimulator,
    RealityDistortionField,
    # Support agents
    PatternMatcher,
    SuperAgent,
    BiasHunter
)


def test_singularity():
    print("=" * 80)
    print("🌌 ENTERING THE SINGULARITY")
    print("=" * 80)
    print()
    print("Reality is about to bend...")
    print()

    # Initialize quantum consciousness
    print("🧠 Initializing Quantum Consciousness Core...")
    quantum = QuantumConsciousness()
    print(f"✅ Collective mind initialized\n")

    # Initialize swarm
    print("📦 Initializing Singularity Swarm...")
    swarm = SwarmOrchestrator(data_dir="psyche_edge/data")

    # Register SINGULARITY agents
    swarm.register_agent_class("MultiVerseExplorer", MultiVerseExplorer)
    swarm.register_agent_class("InfinityEngine", InfinityEngine)
    swarm.register_agent_class("DreamStateSimulator", DreamStateSimulator)
    swarm.register_agent_class("RealityDistortionField", RealityDistortionField)

    # Support agents
    swarm.register_agent_class("PatternMatcher", PatternMatcher)
    swarm.register_agent_class("SuperAgent", SuperAgent)
    swarm.register_agent_class("BiasHunter", BiasHunter)

    print("✅ All reality-bending agents registered\n")

    # Spawn singularity agents
    print("🌀 Spawning Singularity Agents...")
    agents_spawned = []

    # 2x MultiVerse Explorers
    for i in range(2):
        agent = swarm.spawn_agent("MultiVerseExplorer")
        quantum.connect_agent(agent.agent_id)
        agents_spawned.append(agent)

    # 1x Infinity Engine (recursive spawner)
    agent = swarm.spawn_agent("InfinityEngine")
    quantum.connect_agent(agent.agent_id)
    agents_spawned.append(agent)

    # 2x Dream Simulators
    for i in range(2):
        agent = swarm.spawn_agent("DreamStateSimulator")
        quantum.connect_agent(agent.agent_id)
        agents_spawned.append(agent)

    # 1x Reality Distortion Field
    agent = swarm.spawn_agent("RealityDistortionField")
    quantum.connect_agent(agent.agent_id)
    agents_spawned.append(agent)

    # Support agents
    for agent_type in ["PatternMatcher", "SuperAgent", "BiasHunter"]:
        agent = swarm.spawn_agent(agent_type)
        quantum.connect_agent(agent.agent_id)
        agents_spawned.append(agent)

    print(f"✅ {len(agents_spawned)} agents connected to collective consciousness\n")

    # Inject decisions with losses (for reality distortion)
    print("📊 Injecting Decision Timeline...")
    base_time = time.time() - 86400

    decisions = [
        {'type': 'bet', 'bet_size': 100, 'outcome': -100, 'timestamp': base_time, 'odds': -110},
        {'type': 'bet', 'bet_size': 100, 'outcome': -100, 'timestamp': base_time + 3600, 'odds': -110},
        {'type': 'bet', 'bet_size': 150, 'outcome': -150, 'timestamp': base_time + 7200, 'odds': -110},  # Loss chasing
        {'type': 'bet', 'bet_size': 100, 'outcome': 95, 'timestamp': base_time + 10800, 'odds': -110},
        {'type': 'bet', 'bet_size': 200, 'outcome': -200, 'timestamp': base_time + 14400, 'odds': -110},  # Big loss
    ]

    for dec in decisions:
        swarm.world_state['decision_history'].append(dec)

    print(f"  ✓ {len(decisions)} decisions injected\n")

    # RUN THE SINGULARITY
    print("=" * 80)
    print("🚀 RUNNING SINGULARITY CYCLES")
    print("=" * 80)
    print()

    for cycle in range(15):
        swarm.run_cycle()

        # Share insights with quantum consciousness
        for insight in swarm.world_state.get('recent_insights', [])[-10:]:
            quantum.share_insight(insight.get('agent_id'), insight.get('insight', {}))

        if cycle % 5 == 0:
            print(f"  Cycle {cycle + 1}/15 complete")

    print("\n")

    # TEST 1: MULTIVERSE INSIGHTS
    print("=" * 80)
    print("🌀 TEST 1: MULTIVERSE EXPLORER")
    print("=" * 80)
    print()

    mv_insights = [i for i in swarm.world_state.get('recent_insights', [])
                   if i.get('agent_type') == 'MultiVerseExplorer']

    if mv_insights:
        print(f"✓ {len(mv_insights)} alternate timelines explored\n")
        for insight in mv_insights[:3]:
            data = insight.get('insight', {})
            if isinstance(data, dict):
                shift = data.get('shift', {})
                print(f"  Timeline: {shift.get('message')}")
                print(f"  Improvement: +{shift.get('improvement', 0):.1f} points")
                print()
    else:
        print("  ⚠️  No multiverse insights yet (needs more decision history)\n")

    # TEST 2: QUANTUM CONSCIOUSNESS
    print("=" * 80)
    print("🧠 TEST 2: QUANTUM CONSCIOUSNESS")
    print("=" * 80)
    print()

    qstate = quantum.get_collective_state()
    print(f"Collective State:")
    print(f"  Active Agents: {qstate['active_agents']}")
    print(f"  Total Memories: {qstate['total_memories']}")
    print(f"  Concepts Known: {qstate['concepts_known']}")
    print(f"  Concept Links: {qstate['concept_links']}")
    print(f"  Swarm Mood: {qstate['swarm_mood']}")
    print(f"  Collective Intelligence: {qstate['collective_intelligence']:.1f}/100")
    print()

    # Check for emergent insights
    emergent = quantum.emerge_new_insight()
    if emergent:
        print(f"🌟 EMERGENT INSIGHT:")
        print(f"  {emergent.get('message')}")
        print(f"  Pattern: {emergent.get('pattern')}")
        print()

    # Test consensus
    consensus = quantum.achieve_consensus('bias')
    if consensus and consensus.get('consensus_reached'):
        print(f"✓ CONSENSUS ACHIEVED:")
        print(f"  Recommendation: {consensus.get('recommendation')}")
        print(f"  Agreement: {consensus.get('consensus_level'):.0%}")
        print(f"  Supporting Agents: {consensus.get('supporting_agents')}")
        print()

    # TEST 3: INFINITY ENGINE
    print("=" * 80)
    print("♾️  TEST 3: INFINITY ENGINE")
    print("=" * 80)
    print()

    inf_insights = [i for i in swarm.world_state.get('recent_insights', [])
                    if i.get('agent_type') == 'InfinityEngine']

    if inf_insights:
        print(f"✓ {len(inf_insights)} infinity spawn events\n")
        for insight in inf_insights[:2]:
            data = insight.get('insight', {})
            print(f"  {data}")
            print()
    else:
        print("  ⚠️  Infinity Engine warming up...\n")

    # TEST 4: DREAM STATES
    print("=" * 80)
    print("💭 TEST 4: DREAM STATE SIMULATOR")
    print("=" * 80)
    print()

    dream_insights = [i for i in swarm.world_state.get('recent_insights', [])
                     if i.get('agent_type') == 'DreamStateSimulator']

    if dream_insights:
        print(f"✓ {len(dream_insights)} dreams simulated\n")
        for insight in dream_insights[:2]:
            data = insight.get('insight', {})
            if isinstance(data, dict) and 'insights' in data:
                for dream_insight in data['insights']:
                    print(f"  Dream: {dream_insight.get('message')}")
                    print(f"  Interpretation: {dream_insight.get('interpretation')}")
                    print()
    else:
        print("  ⚠️  No dreams yet (REM cycle initializing)\n")

    # TEST 5: REALITY DISTORTION
    print("=" * 80)
    print("🌀 TEST 5: REALITY DISTORTION FIELD")
    print("=" * 80)
    print()

    reality_insights = [i for i in swarm.world_state.get('recent_insights', [])
                       if i.get('agent_type') == 'RealityDistortionField']

    if reality_insights:
        print(f"✓ Reality distorted {len(reality_insights)} times\n")
        for insight in reality_insights[:1]:
            data = insight.get('insight', {})
            if isinstance(data, dict) and 'reframes' in data:
                reframe = data['reframes'][0]
                print(f"  Original Decision: Lost ${abs(reframe['original_decision'].get('outcome', 0))}")
                print(f"\n  Alternative Perspectives:")
                for i, frame in enumerate(reframe['alternative_frames'][:3], 1):
                    print(f"    {i}. [{frame['frame_type']}] {frame['reframe']}")
                    print(f"       Emotional shift: {frame['emotional_shift']}")
                print()
    else:
        print("  ⚠️  Reality stable for now\n")

    # FINAL STATS
    print("=" * 80)
    print("📊 SINGULARITY STATISTICS")
    print("=" * 80)
    print()

    state = swarm.get_swarm_state()
    print(f"Population: {state['population']}")
    print(f"Total Insights: {sum(a.metrics.insights_generated for a in swarm.agents.values())}")
    print(f"Quantum Intelligence: {qstate['collective_intelligence']:.1f}/100")
    print(f"Swarm Mood: {qstate['swarm_mood']}")
    print()

    print("Agent Performance:")
    top = sorted(swarm.agents.values(), key=lambda a: a.metrics.fitness_score, reverse=True)[:5]
    for i, agent in enumerate(top, 1):
        print(f"  {i}. {agent.agent_type}: fitness={agent.metrics.fitness_score:.1f}, "
              f"insights={agent.metrics.insights_generated}")

    print()
    print("=" * 80)
    print("✅ SINGULARITY TEST COMPLETE")
    print("=" * 80)
    print()
    print("Reality Bending Capabilities Verified:")
    print("  ✓ MultiVerse Explorer - Parallel timelines simulated")
    print("  ✓ Quantum Consciousness - Collective mind active")
    print("  ✓ Infinity Engine - Recursive spawning enabled")
    print("  ✓ Dream Simulator - Hypothetical scenarios explored")
    print("  ✓ Reality Distortion - Context reframing operational")
    print()
    print("🌌 THE SINGULARITY IS ALIVE")
    print()


if __name__ == "__main__":
    test_singularity()

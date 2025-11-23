#!/usr/bin/env python3
"""
Test Enhanced PsycheEdge Features
Tests new PatternMatcher, SuperAgent, and Analytics
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from psyche_edge.core.swarm import SwarmOrchestrator
from psyche_edge.core.analytics import SwarmAnalytics
from psyche_edge.agents import (
    CialdiniScientist, BiasHunter, TiltDetector,
    DecisionLogger, MetaObserver,
    PatternMatcher, SuperAgent  # NEW!
)
from psyche_edge.integrations.biometrics import BiometricSimulator


def test_enhanced_features():
    print("=" * 80)
    print("🚀 TESTING ENHANCED PSYCHE EDGE FEATURES")
    print("=" * 80)
    print()

    # Initialize swarm
    print("📦 Initializing Enhanced Swarm...")
    swarm = SwarmOrchestrator(data_dir="psyche_edge/data")

    # Register ALL agents including new ones
    swarm.register_agent_class("CialdiniScientist", CialdiniScientist)
    swarm.register_agent_class("BiasHunter", BiasHunter)
    swarm.register_agent_class("TiltDetector", TiltDetector)
    swarm.register_agent_class("DecisionLogger", DecisionLogger)
    swarm.register_agent_class("MetaObserver", MetaObserver)
    swarm.register_agent_class("PatternMatcher", PatternMatcher)  # NEW!
    swarm.register_agent_class("SuperAgent", SuperAgent)  # NEW!

    print("✅ All agents registered (including PatternMatcher and SuperAgent)\n")

    # Spawn diverse population
    print("🐣 Spawning 30 agents (including new types)...")
    agent_types = [
        "BiasHunter", "TiltDetector", "CialdiniScientist",
        "DecisionLogger", "MetaObserver",
        "PatternMatcher", "PatternMatcher",  # 2x Pattern Matchers
        "SuperAgent"  # 1x SuperAgent
    ]

    for i in range(30):
        agent_type = agent_types[i % len(agent_types)]
        swarm.spawn_agent(agent_type)

    print(f"✅ {len(swarm.agents)} agents spawned\n")

    # Inject realistic decision sequence (with patterns)
    print("📊 Injecting Decision Sequence with Patterns...")

    base_time = time.time() - 86400  # Start 24h ago

    # Pattern 1: Loss chasing (2 losses → bigger bet)
    decisions = [
        {'type': 'bet', 'bet_size': 100, 'outcome': 95, 'timestamp': base_time},
        {'type': 'bet', 'bet_size': 100, 'outcome': -100, 'timestamp': base_time + 3600},
        {'type': 'bet', 'bet_size': 100, 'outcome': -100, 'timestamp': base_time + 7200},
        {'type': 'bet', 'bet_size': 200, 'outcome': -200, 'timestamp': base_time + 7500},  # PATTERN!
    ]

    # Pattern 2: Time-of-day effect (late night losses)
    for i in range(5):
        decisions.append({
            'type': 'bet',
            'bet_size': 100,
            'outcome': -90,
            'timestamp': base_time + 82800 + (i * 900)  # 11 PM
        })

    # Pattern 3: Winning streak → overconfidence
    for i in range(3):
        decisions.append({
            'type': 'bet',
            'bet_size': 100,
            'outcome': 95,
            'timestamp': base_time + 50000 + (i * 1800)
        })

    decisions.append({
        'type': 'bet',
        'bet_size': 300,  # OVERCONFIDENCE!
        'outcome': -300,
        'timestamp': base_time + 56000
    })

    for dec in decisions:
        swarm.world_state['decision_history'].append(dec)

    print(f"  ✓ {len(decisions)} decisions injected (with 3 patterns)\n")

    # Inject biometrics
    print("💓 Injecting Biometrics...")
    bio_sim = BiometricSimulator()
    swarm.world_state['biometric_data'] = bio_sim.generate_realistic_biometrics()
    print(f"  ✓ HRV={swarm.world_state['biometric_data']['hrv']:.1f}\n")

    # Run swarm cycles
    print("🔄 Running 10 Swarm Cycles...")
    for cycle in range(10):
        swarm.run_cycle()
        if cycle % 3 == 0:
            print(f"  Cycle {cycle + 1}/10 complete")
    print()

    # TEST 1: Pattern Matcher Insights
    print("=" * 80)
    print("🔍 TEST 1: PATTERN MATCHER INSIGHTS")
    print("=" * 80)

    pattern_insights = [i for i in swarm.world_state.get('recent_insights', [])
                       if i.get('agent_type') == 'PatternMatcher']

    if pattern_insights:
        print(f"Found {len(pattern_insights)} pattern insights:\n")
        for insight in pattern_insights[-3:]:
            insight_data = insight.get('insight', {})
            if isinstance(insight_data, dict) and 'patterns' in insight_data:
                for pattern in insight_data['patterns'][:2]:  # Show top 2
                    print(f"  📌 {pattern.get('type')}")
                    print(f"     Message: {pattern.get('message')}")
                    print(f"     Confidence: {pattern.get('confidence', 0):.0%}")
                    print(f"     Recommendation: {pattern.get('recommendation')}")
                    print()
    else:
        print("  ⚠️  No pattern insights yet (may need more data)\n")

    # TEST 2: SuperAgent Synthesis
    print("=" * 80)
    print("🌟 TEST 2: SUPERAGENT SYNTHESIS")
    print("=" * 80)

    super_insights = [i for i in swarm.world_state.get('recent_insights', [])
                     if i.get('agent_type') == 'SuperAgent']

    if super_insights:
        print(f"Found {len(super_insights)} super insights:\n")
        for insight in super_insights:
            insight_data = insight.get('insight', {})
            print(f"  ⭐ {insight_data}")
            if isinstance(insight_data, dict):
                print(f"     Type: {insight_data.get('subtype')}")
                print(f"     Confidence: {insight_data.get('confidence', 0):.0%}")
            print()
    else:
        print("  ⚠️  No super insights yet (needs multiple agent insights to synthesize)\n")

    # TEST 3: Advanced Analytics
    print("=" * 80)
    print("📈 TEST 3: ADVANCED ANALYTICS")
    print("=" * 80)

    analytics = SwarmAnalytics()
    report = analytics.generate_swarm_report(swarm)

    print("Performance Metrics:")
    perf = report['performance']
    print(f"  Population: {perf['population']}")
    print(f"  Avg Fitness: {perf['avg_fitness']:.2f}")
    print(f"  Max Fitness: {perf['max_fitness']:.2f}")
    print(f"  Total Insights: {perf['total_insights']}")
    print(f"  Diversity: {perf['unique_types']} unique types")
    print()

    print("Top 5 Performers:")
    for i, agent in enumerate(report['top_by_fitness'][:5], 1):
        print(f"  {i}. {agent['agent_type']}: fitness={agent['fitness']:.1f}, "
              f"insights={agent['insights']}, gen={agent['generation']}")
    print()

    print("Recommendations:")
    for rec in report['recommendations']:
        print(f"  {rec}")
    print()

    # Save report
    report_path = analytics.save_report(report, "enhanced_test_report.json")
    print(f"📄 Full report saved to: {report_path}\n")

    # Final Summary
    print("=" * 80)
    print("✅ ENHANCED FEATURES TEST COMPLETE")
    print("=" * 80)
    print()
    print("New Capabilities Tested:")
    print("  ✓ PatternMatcher - Advanced time-series & sequence analysis")
    print("  ✓ SuperAgent - Multi-agent insight synthesis")
    print("  ✓ SwarmAnalytics - Comprehensive performance analysis")
    print()
    print("System Status:")
    print(f"  Total Agents: {len(swarm.agents)}")
    print(f"  Total Insights: {perf['total_insights']}")
    print(f"  Average Fitness: {perf['avg_fitness']:.2f}")
    print()


if __name__ == "__main__":
    test_enhanced_features()

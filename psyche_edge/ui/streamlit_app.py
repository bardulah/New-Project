"""
PsycheEdge Streamlit Control Center
Real-time swarm monitoring and control interface
"""
import streamlit as st
import time
import sys
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from psyche_edge.core.swarm import SwarmOrchestrator
from psyche_edge.agents import (
    CialdiniScientist, BiasHunter, TiltDetector,
    DecisionLogger, CodeEvolutor, MetaObserver, SwarmSpawner
)


# Page config
st.set_page_config(
    page_title="PsycheEdge 2025 Control Center",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_swarm():
    """Initialize swarm if not in session state"""
    if 'swarm' not in st.session_state:
        st.session_state.swarm = SwarmOrchestrator(data_dir="psyche_edge/data")

        # Register agents
        st.session_state.swarm.register_agent_class("CialdiniScientist", CialdiniScientist)
        st.session_state.swarm.register_agent_class("BiasHunter", BiasHunter)
        st.session_state.swarm.register_agent_class("TiltDetector", TiltDetector)
        st.session_state.swarm.register_agent_class("DecisionLogger", DecisionLogger)
        st.session_state.swarm.register_agent_class("CodeEvolutor", CodeEvolutor)
        st.session_state.swarm.register_agent_class("MetaObserver", MetaObserver)
        st.session_state.swarm.register_agent_class("SwarmSpawner", SwarmSpawner)

        st.session_state.swarm_initialized = False

    return st.session_state.swarm


def main():
    st.title("🧠 PsycheEdge 2025 Control Center")
    st.markdown("*Self-Evolving Cognitive & Decision-Science Laboratory*")
    st.markdown("---")

    swarm = init_swarm()

    # Sidebar - Controls
    with st.sidebar:
        st.header("🎛️ Swarm Controls")

        # Initialize swarm
        if not st.session_state.get('swarm_initialized', False):
            st.subheader("Initialize Swarm")
            initial_pop = st.number_input("Initial Population", min_value=10, max_value=200, value=40)

            if st.button("🐣 Spawn Initial Swarm", type="primary"):
                with st.spinner("Spawning agents..."):
                    # Spawn initial population
                    agent_types = ["CialdiniScientist", "BiasHunter", "TiltDetector",
                                  "DecisionLogger", "CodeEvolutor", "MetaObserver", "SwarmSpawner"]

                    for _ in range(initial_pop):
                        agent_type = agent_types[_ % len(agent_types)]
                        swarm.spawn_agent(agent_type)

                    st.session_state.swarm_initialized = True
                    st.success(f"✅ Spawned {initial_pop} agents!")
                    st.rerun()

        else:
            # Swarm running controls
            st.subheader("Swarm Status")

            state = swarm.get_swarm_state()

            status_color = "🟢" if swarm.running else "🔴"
            st.markdown(f"{status_color} **{'RUNNING' if swarm.running else 'STOPPED'}**")

            col1, col2 = st.columns(2)
            with col1:
                if not swarm.running:
                    if st.button("▶️ Start", type="primary"):
                        swarm.start_swarm()
                        st.rerun()
                else:
                    if st.button("⏸️ Stop", type="secondary"):
                        swarm.stop_swarm()
                        st.rerun()

            with col2:
                if st.button("🔄 Refresh"):
                    st.rerun()

            st.markdown("---")

            # Quick actions
            st.subheader("⚡ Quick Actions")

            if st.button("➕ Spawn 5 Agents"):
                for _ in range(5):
                    swarm.spawn_agent("BiasHunter")
                st.success("Spawned 5 new BiasHunter agents")

            if st.button("🧬 Force Evolution"):
                top_agents = swarm.get_top_agents(5)
                for agent in top_agents:
                    swarm.evolve_agent(agent.agent_id)
                st.success("Evolved top 5 agents")

            if st.button("👶 Mass Breeding"):
                swarm.force_mass_breeding()
                st.success("Mass breeding event triggered")

            if st.button("☠️ Mass Extinction"):
                swarm.force_mass_death(keep_top_n=10)
                st.warning("Mass extinction! Only top 10 survived")

            st.markdown("---")

            # Inject data
            st.subheader("💉 Inject Data")

            with st.expander("Add Decision"):
                dec_type = st.selectbox("Type", ["bet", "job_application", "negotiation"])
                bet_size = st.number_input("Bet Size", value=100)
                notes = st.text_input("Notes")

                if st.button("Add Decision"):
                    decision = {
                        'type': dec_type,
                        'bet_size': bet_size,
                        'timestamp': time.time(),
                        'notes': notes
                    }
                    swarm.world_state['decision_history'].append(decision)
                    st.success("Decision added")

            with st.expander("Add Biometrics"):
                hrv = st.slider("HRV", 20, 100, 60)
                sleep_score = st.slider("Sleep Score", 0, 100, 80)
                mood = st.selectbox("Mood", ["calm", "anxious", "excited", "angry"])

                if st.button("Add Biometrics"):
                    swarm.world_state['biometric_data'] = {
                        'hrv': hrv,
                        'sleep_score': sleep_score,
                        'mood': mood,
                        'timestamp': time.time()
                    }
                    st.success("Biometrics updated")

    # Main content
    if not st.session_state.get('swarm_initialized', False):
        st.info("👈 Initialize the swarm from the sidebar to begin")
        return

    state = swarm.get_swarm_state()

    # Top metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("👥 Population", state['population'])

    with col2:
        st.metric("🐣 Born", state['total_born'])

    with col3:
        st.metric("💀 Died", state['total_died'])

    with col4:
        st.metric("🔄 Cycles", state['cycles'])

    with col5:
        avg_fitness = state['recent_fitness'][-1]['avg_fitness'] if state['recent_fitness'] else 0
        st.metric("📈 Avg Fitness", f"{avg_fitness:.1f}")

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Live Stats",
        "🧬 Agent List",
        "💡 Recent Insights",
        "📈 Evolution History",
        "🧪 Experiments"
    ])

    with tab1:
        # Fitness chart
        st.subheader("Fitness Evolution")

        if state['recent_fitness']:
            df_fitness = pd.DataFrame(state['recent_fitness'])
            df_fitness['timestamp'] = pd.to_datetime(df_fitness['timestamp'], unit='s')

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_fitness['timestamp'], y=df_fitness['avg_fitness'],
                                    name='Average', line=dict(color='blue', width=2)))
            fig.add_trace(go.Scatter(x=df_fitness['timestamp'], y=df_fitness['max_fitness'],
                                    name='Maximum', line=dict(color='green', width=1)))
            fig.add_trace(go.Scatter(x=df_fitness['timestamp'], y=df_fitness['min_fitness'],
                                    name='Minimum', line=dict(color='red', width=1)))

            fig.update_layout(height=400, xaxis_title="Time", yaxis_title="Fitness Score")
            st.plotly_chart(fig, use_container_width=True)

        # Species distribution
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Species Distribution")
            if state['species_count']:
                df_species = pd.DataFrame(list(state['species_count'].items()),
                                         columns=['Species', 'Count'])
                fig = px.pie(df_species, values='Count', names='Species')
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Population Trend")
            if state['recent_fitness']:
                df_pop = pd.DataFrame(state['recent_fitness'])
                df_pop['timestamp'] = pd.to_datetime(df_pop['timestamp'], unit='s')
                fig = px.line(df_pop, x='timestamp', y='population')
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Active Agents")

        if state['agents']:
            df_agents = pd.DataFrame(state['agents'])
            df_agents['age_min'] = (df_agents['age'] / 60).round(1)

            # Sort by fitness
            df_agents = df_agents.sort_values('fitness', ascending=False)

            # Color code by status
            st.dataframe(
                df_agents[['id', 'type', 'generation', 'fitness', 'age_min', 'status']],
                use_container_width=True,
                height=400
            )

            # Top performers
            st.subheader("🏆 Top 10 Performers")
            top_agents = swarm.get_top_agents(10)

            for i, agent in enumerate(top_agents, 1):
                with st.expander(f"{i}. {agent.agent_type} - Fitness: {agent.metrics.fitness_score:.2f}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Metrics:**")
                        st.write(f"- Insights: {agent.metrics.insights_generated}")
                        st.write(f"- Predictions: {agent.metrics.correct_predictions}/{agent.metrics.correct_predictions + agent.metrics.failed_predictions}")
                        st.write(f"- Competitions Won: {agent.metrics.competition_wins}")
                        st.write(f"- Generation: {agent.generation}")

                    with col2:
                        st.write("**Genome:**")
                        st.write(f"- Aggression: {agent.genome.aggression:.2f}")
                        st.write(f"- Curiosity: {agent.genome.curiosity:.2f}")
                        st.write(f"- Cooperation: {agent.genome.cooperation:.2f}")
                        st.write(f"- Risk Tolerance: {agent.genome.risk_tolerance:.2f}")

    with tab3:
        st.subheader("💡 Recent Insights")

        recent_insights = swarm.world_state.get('recent_insights', [])[-50:]

        if recent_insights:
            for insight in reversed(recent_insights):
                timestamp = datetime.fromtimestamp(insight['timestamp']).strftime('%H:%M:%S')
                agent_type = insight.get('agent_type', 'Unknown')

                with st.expander(f"[{timestamp}] {agent_type}"):
                    st.json(insight.get('insight', {}))
        else:
            st.info("No insights yet. Agents are warming up...")

    with tab4:
        st.subheader("🧬 Evolution Timeline")

        # Read evolution logs
        from pathlib import Path
        import json

        log_file = Path("psyche_edge/data/agent_logs/evolution.jsonl")

        if log_file.exists():
            evolutions = []
            with open(log_file) as f:
                for line in f:
                    evolutions.append(json.loads(line))

            if evolutions:
                df_evo = pd.DataFrame([e['data'] for e in evolutions[-100:]])
                df_evo['timestamp'] = pd.to_datetime(df_evo['timestamp'], unit='s')

                st.dataframe(df_evo, use_container_width=True)
            else:
                st.info("No evolution events yet")
        else:
            st.info("No evolution events yet")

    with tab5:
        st.subheader("🧪 Run Experiments")

        st.markdown("""
        Design experiments to test cognitive biases and decision-making patterns.
        """)

        experiment_type = st.selectbox(
            "Experiment Type",
            ["Loss Aversion Test", "Anchoring Bias Test", "Tilt Detection Test"]
        )

        if st.button("Run Experiment"):
            st.info(f"Running {experiment_type}...")
            # Placeholder for experiment logic
            st.success("Experiment complete!")

    # Auto-refresh
    if swarm.running:
        time.sleep(2)
        st.rerun()


if __name__ == "__main__":
    main()

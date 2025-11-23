# 🏗️ PsycheEdge Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  Streamlit   │  │   Telegram   │  │     CLI      │              │
│  │   Web UI     │  │     Bot      │  │   Interface  │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                  │                  │                       │
│         └──────────────────┼──────────────────┘                       │
│                            │                                          │
└────────────────────────────┼──────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      SWARM ORCHESTRATOR                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  • Agent Lifecycle Management (spawn, evolve, breed, kill)          │
│  • World State (shared knowledge, biometrics, decisions)             │
│  • Message Routing (agent communication)                             │
│  • Natural Selection Engine                                          │
│  • Competition & Cooperation Coordinator                             │
│  • Evolution History Tracking                                        │
│                                                                       │
└────────────────────────────┬──────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       AGENT SWARM                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │
│  │  Cialdini      │  │   Bias         │  │    Tilt        │       │
│  │  Scientist     │  │   Hunter       │  │   Detector     │       │
│  │ (Persuasion)   │  │ (Cognitive     │  │ (Emotional     │       │
│  │                │  │  Biases)       │  │  State)        │       │
│  └────────────────┘  └────────────────┘  └────────────────┘       │
│                                                                       │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │
│  │   Decision     │  │     Code       │  │     Meta       │       │
│  │    Logger      │  │   Evolutor     │  │   Observer     │       │
│  │ (Data Track)   │  │ (Meta-Agent)   │  │ (Swarm Watch)  │       │
│  └────────────────┘  └────────────────┘  └────────────────┘       │
│                                                                       │
│  ┌────────────────┐                                                 │
│  │    Swarm       │                                                 │
│  │   Spawner      │  ... + Evolved Agents (Gen 1, 2, 3...)         │
│  │ (Population)   │                                                 │
│  └────────────────┘                                                 │
│                                                                       │
└────────────────────────────┬──────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA INTEGRATIONS                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Apple      │  │     Oura     │  │    Manual    │              │
│  │   Watch      │  │     Ring     │  │     Mood     │              │
│  │  (HRV/HR)    │  │   (Sleep)    │  │    Logging   │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Betting    │  │     Job      │  │ Negotiation  │              │
│  │  Decisions   │  │ Applications │  │   Tracking   │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                       │
└────────────────────────────┬──────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       DATA STORAGE                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  • psyche_edge/data/biometrics/     (HRV, sleep, mood)             │
│  • psyche_edge/data/decisions/      (bets, jobs, negotiations)     │
│  • psyche_edge/data/agent_logs/     (agent activity, events)       │
│  • psyche_edge/data/evolution_history/  (mutations, breeding)      │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Agent Architecture

### AgentDNA Base Class

Every agent inherits from `AgentDNA`:

```
┌─────────────────────────────────────────────────────────────┐
│                      AgentDNA                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Genome (Evolved Parameters):                                │
│    • aggression, curiosity, cooperation                      │
│    • mutation_rate, learning_rate                            │
│    • risk_tolerance, confidence_threshold                    │
│    • memory_depth                                            │
│    • custom_params (agent-specific)                          │
│                                                               │
│  Metrics (Performance):                                      │
│    • fitness_score (calculated from below)                   │
│    • insights_generated, decisions_improved                  │
│    • biases_detected, correct_predictions                    │
│    • competition_wins/losses                                 │
│                                                               │
│  Core Methods:                                               │
│    • perceive(world_state) → perception                      │
│    • think(perception) → decision                            │
│    • act(decision) → action_result                           │
│    • run_cycle(world_state) → perceive→think→act             │
│                                                               │
│  Evolution Methods:                                          │
│    • evolve() → create mutated child                         │
│    • breed_with(other) → sexual reproduction                 │
│    • compete_with(other, challenge) → winner/loser           │
│    • should_die() → bool (fitness check)                     │
│    • should_evolve() → bool (ready to spawn child)           │
│    • should_breed() → bool (high fitness)                    │
│                                                               │
│  Communication:                                              │
│    • send_message(recipient_id, message)                     │
│    • receive_messages() → inbox                              │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Agent Lifecycle

```
     ┌──────────┐
     │  SPAWN   │  ← swarm.spawn_agent(type)
     └────┬─────┘
          │
          ▼
     ┌──────────┐
     │  ACTIVE  │  ← Run cycles: perceive → think → act
     └────┬─────┘
          │
          ├────── High Fitness ──────┐
          │                           │
          │                           ▼
          │                      ┌──────────┐
          │                      │ BREEDING │ ← Sexual reproduction
          │                      └────┬─────┘
          │                           │
          │                           ├──→ Child Agent (Generation++)
          │                           │
          ├────── Moderate Fitness ───┼──→ EVOLVE ──→ Mutated Child
          │                           │
          │                           │
          ├────── Competing ─────┐    │
          │                      │    │
          │                      ▼    │
          │                 ┌──────────┐
          │                 │ COMPETE  │ ← Agent vs Agent challenge
          │                 └────┬─────┘
          │                      │
          │                      ├─→ Win (+fitness)
          │                      │
          │                      └─→ Lose (-fitness)
          │                           │
          │                           │
          └────── Low Fitness ────────┼────┐
                                      │    │
                                      ▼    ▼
                                 ┌──────────┐
                                 │   DEAD   │ ← Natural selection
                                 └──────────┘
```

---

## Evolution Mechanisms

### 1. Asexual Reproduction (Mutation)

```
Parent Agent (Gen N)
       │
       ├─ Genome: {aggression: 0.7, curiosity: 0.5, ...}
       │
       ▼ evolve()
       │
       ├─ Apply random mutations to each parameter
       │  (gaussian noise with mutation_rate)
       │
       ▼
Child Agent (Gen N+1)
       │
       └─ Genome: {aggression: 0.73, curiosity: 0.48, ...}
```

### 2. Sexual Reproduction (Breeding)

```
Parent 1 (Gen N)              Parent 2 (Gen N)
  Genome A                      Genome B
    │                              │
    │                              │
    └──────────┬───────────────────┘
               │
               ▼ breed_with()
               │
          Mix genes (weighted average)
               │
               ▼
          Apply mutation
               │
               ▼
        Child (Gen N+1)
          Mixed Genome
```

### 3. Natural Selection

```
Every Cycle:
    │
    ├─ Calculate fitness for all agents
    │
    ├─ For each agent:
    │    │
    │    ├─ if fitness < kill_threshold: KILL
    │    │
    │    ├─ if fitness > evolve_threshold: EVOLVE
    │    │
    │    └─ if fitness > breed_threshold: BREED (if partner available)
    │
    └─ Population adapts over time
```

---

## Data Flow

### Decision → Insight Pipeline

```
1. User makes decision
      │
      ▼
2. Log to decision_history
      │
      ▼
3. Update world_state
      │
      ▼
4. Swarm cycle runs
      │
      ├─→ All agents perceive world_state
      │
      ├─→ Each agent thinks (analyzes decision)
      │
      └─→ Agents act (generate insights)
      │
      ▼
5. Insights stored in world_state['recent_insights']
      │
      ▼
6. UI displays insights to user
      │
      ▼
7. User adjusts behavior
      │
      └─→ Loop back to step 1 (feedback loop)
```

### Biometric Integration Flow

```
1. Apple Watch / Oura / Manual Log
      │
      ▼
2. BiometricIntegration.poll_sources()
      │
      ▼
3. Update world_state['biometric_data']
      │
      ▼
4. Agents perceive biometrics in next cycle
      │
      ├─→ TiltDetector checks HRV + decision patterns
      │
      ├─→ BiasHunter checks if decisions made under stress
      │
      └─→ CialdiniScientist adjusts recommendations
      │
      ▼
5. Insights consider physiological state
```

---

## Fitness Function Details

```python
fitness = (
    # Prediction accuracy is king (0-100 points)
    prediction_accuracy * 30 +

    # Volume of insights (0-100+ points)
    insights_generated * 2 +

    # Real impact on decisions (0-100+ points)
    decisions_improved * 5 +

    # Bias detection skill (0-100+ points)
    biases_detected * 3 +

    # Cooperation bonus (0-50 points)
    cooperation_events * 1 +

    # Competition success (0-100+ points)
    competition_wins * 4 -
    competition_losses * 2 +

    # Survival bonus (0-20 points)
    mutations_survived * 1
)

# Apply recency multiplier
recency_multiplier = max(0.1, 1.0 - (time_since_active / 86400))
final_fitness = fitness * recency_multiplier
```

**Key Insights:**
- Accuracy matters most (30x multiplier)
- Recent activity valued (24h decay)
- Negative fitness possible (death eligible)
- Fitness > 100 enables breeding

---

## Message Passing (Agent Communication)

```
Agent A                    Swarm Orchestrator           Agent B
   │                              │                        │
   ├─ send_message() ────────────►│                        │
   │  {to: B, data: {...}}        │                        │
   │                              │                        │
   │                              ├─ route_messages() ────►│
   │                              │                        │
   │                              │         inbox.append() │
   │                              │                        │
   │                              │◄──── receive_messages()│
   │                              │                        │
   │                       [Message Queue]                 │
   │                              │                        │
```

**Use Cases:**
- CodeEvolutor sends evolution commands
- MetaObserver broadcasts warnings
- Agents share discoveries
- Cooperative bias detection

---

## World State Structure

```python
world_state = {
    # Timing
    'timestamp': float,
    'cycle_count': int,

    # Population
    'total_agents_born': int,
    'total_agents_died': int,

    # Biometric Data (latest readings)
    'biometric_data': {
        'hrv': float,
        'heart_rate': float,
        'sleep_score': float,
        'mood': str,
        'stress_level': int,
        'timestamp': float
    },

    # Decision History (last N decisions)
    'decision_history': [
        {
            'type': 'bet|job_application|negotiation',
            'timestamp': float,
            'bet_size': float,  # if type=bet
            'outcome': float,
            # ... type-specific fields
        },
        ...
    ],

    # Agent Insights (last N insights)
    'recent_insights': [
        {
            'agent_id': str,
            'agent_type': str,
            'timestamp': float,
            'insight': {...}  # Agent-specific insight data
        },
        ...
    ],

    # Global Knowledge (shared learning)
    'global_knowledge': {
        'known_biases': [...],
        'successful_strategies': [...],
        'user_patterns': {...}
    }
}
```

All agents read from `world_state` each cycle (perceive phase).

---

## Scaling Considerations

### Current Limits
- **Agents**: 40-200 (configurable)
- **Cycle Interval**: 1 second (configurable)
- **Memory per Agent**: 100 events (configurable via genome)
- **Decision History**: 1000 recent (in-memory)

### Performance
- Single-threaded: ~50 agents @ 1 cycle/sec
- Multi-threaded possible (future enhancement)

### Data Growth
- Decision logs: ~1 KB per decision
- Agent logs: ~500 bytes per event
- 90 days @ 10 decisions/day = ~1 MB total

### Future Optimizations
- Parallel agent execution (ThreadPoolExecutor)
- Database backend (SQLite/PostgreSQL)
- Agent hibernation (inactive agents sleep)
- Distributed swarm (multiple machines)

---

## Security & Privacy

### Data Storage
- All data stored locally in `psyche_edge/data/`
- No external API calls (except optional Oura/Telegram)
- No analytics, no tracking, no cloud sync

### Agent Code Safety
- Agents use **parameterized behaviors**, not arbitrary code execution
- CodeEvolutor modifies parameters, not code directly
- No `eval()`, no `exec()`, no external imports in agents

### API Keys
- Stored in `.env` file (gitignored)
- Never logged or transmitted
- Optional - system works without them

---

## Deployment Options

### 1. Local Python
```bash
python main.py --population 40
```
- Simplest
- Direct control
- No isolation

### 2. Docker Container
```bash
docker-compose up psyche-edge
```
- Isolated environment
- Easy restart
- Persistent data via volumes

### 3. Docker Compose (Full Stack)
```bash
docker-compose up
```
- Streamlit UI
- Background swarm
- Telegram bot
- All services orchestrated

---

## Extension Points

### Add New Agent Type
1. Create `psyche_edge/agents/your_agent.py`
2. Inherit from `AgentDNA`
3. Implement `perceive()`, `think()`, `act()`
4. Register: `swarm.register_agent_class("YourAgent", YourAgent)`
5. Spawn: `swarm.spawn_agent("YourAgent")`

### Add New Biometric Source
1. Edit `psyche_edge/integrations/biometrics.py`
2. Add `_poll_your_source()` method
3. Call in `_poll_sources()`
4. Update world_state

### Add New Decision Type
1. Edit `psyche_edge/experiments/decision_tracker.py`
2. Create dataclass (e.g., `InvestmentDecision`)
3. Add `log_investment()` method
4. Update tracker methods

### Add New UI
1. Create new interface (Flask, FastAPI, etc.)
2. Import `SwarmOrchestrator`
3. Call `swarm.get_swarm_state()` for data
4. Call `swarm.spawn_agent()`, etc. for controls

---

## Philosophy

PsycheEdge is built on these principles:

1. **Emergence over Planning**: Don't design behavior, let it evolve
2. **Natural Selection**: Bad agents die, good agents breed
3. **Competition Creates Excellence**: Agents compete to survive
4. **Cooperation Wins Long-Term**: Sharing insights benefits all
5. **Transparency**: User sees everything, controls everything
6. **Ethics First**: Tools for improvement, not manipulation
7. **Data Ownership**: Your data, your machine, your insights

---

**The swarm is alive. The swarm evolves. The swarm learns.**

🧠 PsycheEdge 2025

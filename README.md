# 🧠 PsycheEdge 2025

**A Legal, Ethical, Self-Evolving Cognitive & Decision-Science Laboratory**

A living, non-linear, multi-agent system that discovers (not plans) how human psychology, cognitive biases, emotional states, and persuasion science affect real-world high-stakes decisions.

---

## 🔥 What Is This?

PsycheEdge is NOT a traditional app. It's a **swarm of autonomous AI agents** that:

- **Mutate and improve their own code**
- **Compete and cooperate in real time**
- **Run daily experiments on you** (the user)
- **Track legal biometric data** (HRV via Apple Watch, sleep via Oura, mood logs)
- **Apply Cialdini's 7 principles ETHICALLY** for habit building and better decisions
- **Detect cognitive biases** in your betting, job applications, negotiations
- **Kill underperforming agents, breed winners** (natural selection)
- After 90 days, **auto-write a 200-page scientific paper** on your decision-making patterns

This is **100% legal, ethical, and revolutionary science.**

---

## 🧬 The Agent Swarm

### Core Agent Types

1. **CialdiniScientist** - Applies persuasion principles ethically to improve decisions
2. **BiasHunter** - Detects 13+ cognitive biases in real-time
3. **TiltDetector** - Monitors emotional decision-making using HRV + patterns
4. **DecisionLogger** - Obsessively tracks every bet, job app, negotiation
5. **CodeEvolutor** - Rewrites other agents when they fail (META)
6. **MetaObserver** - Detects when the ENTIRE SWARM is wrong
7. **SwarmSpawner** - Births new agents based on needs

The swarm starts with 40 agents and evolves from there. Agents:
- Have **genomes** that mutate (aggression, curiosity, cooperation, etc.)
- **Compete** in challenges
- **Breed** when fit (sexual reproduction of genomes)
- **Die** when fitness drops below threshold
- **Evolve** when they discover better strategies

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repo
git clone <your-repo>
cd New-Project

# Copy environment template
cp .env.example .env

# Edit .env with your tokens (optional)
nano .env

# Run with Docker Compose
docker-compose up

# Access Streamlit UI
open http://localhost:8501
```

### Option 2: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run the swarm
python main.py --population 40 --inject-test-data

# Or run Streamlit UI
streamlit run psyche_edge/ui/streamlit_app.py
```

---

## 📊 Usage

### 1. **Streamlit Control Center**

The visual command center for your swarm:

```bash
streamlit run psyche_edge/ui/streamlit_app.py
```

**Features:**
- Real-time population monitoring
- Agent fitness evolution charts
- Spawn/kill/evolve agents manually
- Inject decisions and biometric data
- View insights from all agents
- Evolution timeline

### 2. **Telegram Bot** (Mobile Control)

Control the swarm from your phone:

```bash
# Set TELEGRAM_BOT_TOKEN in .env
python psyche_edge/integrations/telegram_bot.py
```

**Commands:**
- `/status` - Swarm status
- `/spawn BiasHunter 5` - Spawn 5 BiasHunter agents
- `/top` - Top performing agents
- `/insights` - Recent insights
- `/logbet` - Log a betting decision
- `/logmood anxious 7` - Log mood and stress
- `/tilt` - Check if you're tilting

### 3. **CLI Decision Logging**

Quick log decisions from terminal:

```bash
# Log a bet
python psyche_edge/experiments/decision_tracker.py

# Will prompt for:
# - Sport
# - Bet type
# - Size
# - Reasoning
```

---

## 🔬 Biometric Integration

### Apple Watch / HealthKit

**Option A: Export from iPhone**
1. Open Health app → Profile → Export Health Data
2. Extract `export.xml`
3. Place in `psyche_edge/data/biometrics/apple_health_export.json`

**Option B: Manual CSV**
Create `psyche_edge/data/biometrics/hrv_data.csv`:
```csv
timestamp,hrv,hr
2025-01-15 08:00:00,65,70
2025-01-15 20:00:00,55,75
```

### Oura Ring

**Option A: API Integration**
1. Get API token from https://cloud.ouraring.com/personal-access-tokens
2. Add to `.env`: `OURA_API_TOKEN=your_token_here`

**Option B: Manual JSON**
Create `psyche_edge/data/biometrics/oura_sleep.json`:
```json
{
  "score": 85,
  "timestamp": 1705305600
}
```

### Manual Mood Logging

Via Telegram:
```
/logmood calm 3
```

Or via Python:
```python
from psyche_edge.integrations import BiometricIntegration

bio = BiometricIntegration()
bio.log_mood("anxious", stress_level=7, notes="Big bet pending")
```

---

## 🎲 Decision Tracking

Track three decision types:

### 1. Betting Decisions

```python
from psyche_edge.experiments import DecisionTracker

tracker = DecisionTracker()

decision_id = tracker.log_betting_decision(
    sport="NBA",
    bet_type="spread",
    bet_size=100,
    odds=-110,
    game="Lakers -5.5 vs Warriors",
    reasoning="Lakers on 5-game streak, Warriors missing Curry",
    timestamp=time.time()
)

# Later, update outcome
tracker.update_betting_outcome(decision_id, result=95)  # Won $95
```

### 2. Job Applications

```python
tracker.log_job_application(
    company="Google",
    role="Senior Engineer",
    salary_ask=200000,
    application_date=time.time(),
    reasoning="Perfect fit, referral from insider"
)
```

### 3. Negotiations

```python
tracker.log_negotiation(
    negotiation_type="salary",
    initial_ask=180000,
    minimum_acceptable=160000,
    strategy="anchor_high_then_compromise",
    reasoning="Market rate is 170k"
)
```

---

## 🧬 How Evolution Works

### Agent Genome

Every agent has a genome with evolved parameters:

```python
{
  'aggression': 0.7,        # How aggressively pursues goals
  'curiosity': 0.6,         # Exploration vs exploitation
  'cooperation': 0.8,       # Shares insights vs hoards
  'mutation_rate': 0.15,    # How much genome mutates
  'learning_rate': 0.02,    # Speed of adaptation
  'risk_tolerance': 0.5,    # For decision analysis
  'confidence_threshold': 0.7,  # When to act
  'memory_depth': 100       # How much history to track
}
```

### Evolution Mechanisms

**1. Asexual Reproduction (Mutation)**
- High-fitness agents spawn mutated copies
- Genome parameters shift randomly within bounds
- Mutation rate itself can evolve

**2. Sexual Reproduction (Breeding)**
- Two high-fitness agents combine genomes
- Child inherits mixed traits from both parents
- Applied mutation for variation

**3. Natural Selection**
- Low-fitness agents are killed
- Fitness = insights + predictions + competitions won
- Recency matters (recent activity valued)

**4. Competition**
- Agents compete in challenges
- Winner/loser determined by performance
- Updates fitness scores

---

## 📈 Fitness Function

Agent survival depends on fitness score:

```python
fitness = (
    prediction_accuracy * 30 +
    insights_generated * 2 +
    decisions_improved * 5 +
    biases_detected * 3 +
    cooperation_events * 1 +
    competition_wins * 4 -
    competition_losses * 2 +
    mutations_survived * 1
) * recency_multiplier
```

Agents with fitness < 0 die. Agents with fitness > 100 breed.

---

## 🎯 Experiments & Use Cases

### Sports Betting Analytics
- **BiasHunter** detects if you're chasing losses
- **TiltDetector** warns when HRV drops + bet size increases
- **CialdiniScientist** applies consistency principle to stick to bankroll
- **DecisionLogger** calculates ROI, win rate, identifies profitable patterns

### Job Search Optimization
- Track application → response → offer rates
- Detect if you're anchoring salary asks too low
- Identify which strategies work (referrals, timing, etc.)

### Negotiation Science
- Log initial ask, strategy, outcome
- Detect emotional decisions (affect heuristic)
- Apply reciprocity and authority principles

### General Cognitive Bias Detection
- 13+ biases tracked in real-time
- Anchoring, confirmation, loss aversion, gambler's fallacy, etc.
- Combines biometric + behavioral signals

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Telegram Bot (optional)
TELEGRAM_BOT_TOKEN=your_bot_token

# Oura Ring API (optional)
OURA_API_TOKEN=your_oura_token

# Swarm Settings
SWARM_INITIAL_POPULATION=40
SWARM_MAX_POPULATION=200
SWARM_CYCLE_INTERVAL=1.0  # seconds between cycles
```

---

## 📁 Project Structure

```
New-Project/
├── psyche_edge/
│   ├── core/
│   │   ├── agent_dna.py          # Base agent class with evolution
│   │   └── swarm.py              # Swarm orchestrator
│   ├── agents/
│   │   ├── cialdini_scientist.py # Persuasion principle agent
│   │   ├── bias_hunter.py        # Cognitive bias detector
│   │   ├── tilt_detector.py      # Emotional tilt monitor
│   │   ├── decision_logger.py    # Decision tracking
│   │   ├── code_evolutor.py      # Meta-agent (evolves others)
│   │   ├── meta_observer.py      # Swarm-level observer
│   │   └── swarm_spawner.py      # Population controller
│   ├── integrations/
│   │   ├── biometrics.py         # Apple Watch, Oura integration
│   │   └── telegram_bot.py       # Mobile control interface
│   ├── experiments/
│   │   └── decision_tracker.py   # Decision logging system
│   ├── ui/
│   │   └── streamlit_app.py      # Web control center
│   └── data/                     # All data stored here
│       ├── biometrics/           # HRV, sleep, mood logs
│       ├── decisions/            # Decision logs
│       ├── agent_logs/           # Agent activity
│       └── evolution_history/    # Evolution events
├── main.py                       # CLI entry point
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md (this file)
```

---

## 🧪 Advanced: Creating New Agent Types

Want to add your own agent? Here's how:

```python
from psyche_edge.core.agent_dna import AgentDNA

class PatternMatcher(AgentDNA):
    """Detects patterns in decision sequences"""

    def __init__(self, genome=None, parent_ids=None, generation=0):
        super().__init__(
            agent_type="PatternMatcher",
            genome=genome,
            parent_ids=parent_ids,
            generation=generation
        )

    def perceive(self, world_state):
        """What does this agent see?"""
        return {
            'decisions': world_state.get('decision_history', [])[-20:]
        }

    def think(self, perception):
        """What patterns exist?"""
        decisions = perception['decisions']

        # Your pattern detection logic here
        pattern_found = self._detect_pattern(decisions)

        if pattern_found:
            return {'action': 'alert', 'pattern': pattern_found}

        return {'action': 'observe'}

    def act(self, decision):
        """What to do about it?"""
        if decision['action'] == 'alert':
            self.metrics.insights_generated += 1

            return {
                'type': 'pattern_alert',
                'pattern': decision['pattern'],
                'score': 10
            }

        return {'type': 'observing', 'score': 1}

    def _detect_pattern(self, decisions):
        # Your logic
        pass
```

Register it:
```python
swarm.register_agent_class("PatternMatcher", PatternMatcher)
swarm.spawn_agent("PatternMatcher")
```

---

## ⚖️ Ethics & Safety

### What This System DOES:
✅ Tracks YOUR OWN decisions to improve YOUR decision-making
✅ Uses biometric data YOU provide voluntarily
✅ Applies persuasion science ETHICALLY (to help, not manipulate)
✅ Detects cognitive biases to PROTECT you from bad decisions
✅ All data stored LOCALLY (you control it)

### What This System DOES NOT DO:
❌ Manipulate you for external benefit
❌ Share your data with anyone
❌ Make decisions FOR you (only provides insights)
❌ Use substances or illegal methods
❌ Operate without your consent

**This is a tool for SELF-IMPROVEMENT through SCIENCE.**

---

## 🎓 Scientific Background

This system is based on:

1. **Cialdini's 7 Principles of Influence** (ethical application)
2. **Kahneman & Tversky's Prospect Theory** (bias detection)
3. **Behavioral Economics** (decision-making under uncertainty)
4. **Evolutionary Algorithms** (genetic programming, natural selection)
5. **Multi-Agent Systems** (emergent intelligence)
6. **Biometric Psychology** (HRV as cognitive state indicator)

---

## 🔮 Future Roadmap

- [ ] LLM integration for natural language insights
- [ ] Web interface for viewing research paper progress
- [ ] Export to Notion, Obsidian
- [ ] Collaborative swarms (multiple users)
- [ ] Prediction markets integration
- [ ] Academic paper auto-generation
- [ ] Mobile app (React Native)

---

## 🤝 Contributing

This is a solo research project for now, but ideas are welcome!

Open issues for:
- New agent types to add
- Bugs in evolution logic
- Biometric integration improvements
- Experiment ideas

---

## 📜 License

MIT License - Use freely, credit appreciated.

---

## 💬 Contact

Built during a caffeine-fueled coding marathon.

Questions? Open an issue.

**Remember: This is SCIENCE. Legal. Ethical. Revolutionary.**

---

🧠 *"The unexamined decision is not worth making."* - PsycheEdge Swarm


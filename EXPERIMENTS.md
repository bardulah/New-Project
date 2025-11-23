# 🧪 PsycheEdge Experiments Guide

**Suggested experiments to run with your swarm**

---

## 🎲 Sports Betting Experiments

### Experiment 1: Loss Chasing Detection

**Hypothesis:** After a loss, bet sizes increase due to loss aversion bias.

**Method:**
1. Log 10 bets with normal size ($100)
2. Record a loss (-$100)
3. Immediately log next bet with increased size ($150+)
4. Check if BiasHunter and TiltDetector flag it

**Expected Insights:**
- BiasHunter detects "loss_aversion" bias
- TiltDetector warns of elevated tilt
- CialdiniScientist suggests commitment/consistency intervention

**How to Run:**
```python
from psyche_edge.experiments import DecisionTracker

tracker = DecisionTracker()

# Normal bets
for i in range(10):
    tracker.log_betting_decision(
        sport="NBA", bet_type="spread", bet_size=100,
        odds=-110, game=f"Game {i}", reasoning="Normal bet",
        timestamp=time.time() + i*1000
    )

# Record loss
tracker.update_betting_outcome(decision_id, result=-100)

# Increased bet (loss chasing)
tracker.log_betting_decision(
    sport="NBA", bet_type="spread", bet_size=200,
    odds=-110, game="Chase bet", reasoning="Need to win back",
    timestamp=time.time()
)

# Run swarm cycle - check insights
```

---

### Experiment 2: Tilt Detection from Biometrics

**Hypothesis:** Low HRV + rapid decisions = tilt state

**Method:**
1. Inject normal biometrics (HRV=70)
2. Make 3 decisions slowly (10 min apart)
3. Inject poor biometrics (HRV=35, stress=9)
4. Make 3 rapid decisions (1 min apart)

**Expected Insights:**
- TiltDetector triggers HIGH TILT alert
- Recommends stopping immediately

**How to Run:**
```python
from psyche_edge.integrations import BiometricIntegration

bio = BiometricIntegration()

# Phase 1: Normal state
bio.latest_biometrics = {'hrv': 70, 'stress_level': 3}
# Log decisions 10 min apart...

# Phase 2: Tilt state
bio.latest_biometrics = {'hrv': 35, 'stress_level': 9}
# Log decisions 1 min apart...

# Check TiltDetector output
```

---

### Experiment 3: Gambler's Fallacy Detection

**Hypothesis:** After 3+ losses, expect "due for a win"

**Method:**
1. Log 4 consecutive losses
2. In the 5th bet notes, write "due for a win"
3. Check if BiasHunter detects gambler's fallacy

**Expected Insights:**
- BiasHunter flags "gambler_fallacy" bias
- Warns that streaks are independent events

---

## 💼 Job Search Experiments

### Experiment 4: Anchoring in Salary Asks

**Hypothesis:** First salary ask anchors all future asks

**Method:**
1. Log job app with low salary ask ($120k)
2. Log 5 more apps, all with $120k-130k
3. Check if BiasHunter detects anchoring

**Expected Insights:**
- BiasHunter detects "anchoring" bias
- Suggests researching market rates independently

---

### Experiment 5: Response Rate by Application Strategy

**Hypothesis:** Referrals have higher response rates than cold applications

**Method:**
1. Log 20 job applications:
   - 10 via referrals
   - 10 cold applications
2. Update outcomes as responses come in
3. Calculate response rates

**Expected Insights:**
- DecisionLogger provides stats
- Referrals show 3-5x higher response rate

**How to Run:**
```python
tracker = DecisionTracker()

# Referral apps
for i in range(10):
    tracker.log_job_application(
        company=f"Company {i}",
        role="Engineer",
        salary_ask=150000,
        application_date=time.time(),
        source="referral",
        reasoning="Warm intro"
    )

# Cold apps
for i in range(10):
    tracker.log_job_application(
        company=f"Company {i+10}",
        role="Engineer",
        salary_ask=150000,
        application_date=time.time(),
        source="linkedin",
        reasoning="Cold application"
    )

# Later, update outcomes
# tracker.update_job_application_outcome(id, response_received=True)

# Get stats
stats = tracker.calculate_job_app_stats()
print(stats)
```

---

## 🤝 Negotiation Experiments

### Experiment 6: High Anchor vs Low Anchor

**Hypothesis:** Starting with high anchor leads to better outcomes

**Method:**
1. Log 5 negotiations starting at 1.3x market rate
2. Log 5 negotiations starting at 1.0x market rate
3. Compare final outcomes

**Expected Insights:**
- High anchors get 15-20% better outcomes
- CialdiniScientist suggests using high anchors

---

### Experiment 7: Satisfaction vs Dollar Amount

**Hypothesis:** Getting minimum acceptable is more satisfying than getting 80% of ask

**Method:**
1. Log negotiations with:
   - Initial ask: $180k
   - Minimum acceptable: $160k
2. Case A: Final $170k (95% of ask)
3. Case B: Final $160k (minimum)
4. Log satisfaction scores

**Expected Insights:**
- Reaching minimum = 8+/10 satisfaction
- Dollar amount matters less than crossing threshold

---

## 🧬 Evolution Experiments

### Experiment 8: Fitness Function Validation

**Hypothesis:** Agents with high prediction accuracy survive longest

**Method:**
1. Spawn 20 BiasHunter agents
2. Manually set half with high accuracy metrics
3. Run 100 cycles
4. Check survival rates

**Expected Result:**
- High-accuracy agents survive
- Low-accuracy agents die

**How to Run:**
```python
# Spawn agents
for i in range(20):
    agent = swarm.spawn_agent("BiasHunter")

    if i < 10:
        # High accuracy
        agent.metrics.correct_predictions = 50
        agent.metrics.failed_predictions = 5
    else:
        # Low accuracy
        agent.metrics.correct_predictions = 5
        agent.metrics.failed_predictions = 50

# Run cycles
for _ in range(100):
    swarm.run_cycle()

# Check who survived
survivors = swarm.agents
print(f"Survivors: {len(survivors)}/20")
```

---

### Experiment 9: Breeding Creates Better Agents

**Hypothesis:** Bred agents outperform spawned agents

**Method:**
1. Track fitness of generation 0 agents
2. Breed top performers
3. Track fitness of generation 1+ agents
4. Compare average fitness

**Expected Result:**
- Generation 1+ has 20-30% higher average fitness

---

### Experiment 10: Genome Parameter Optimization

**Hypothesis:** Optimal genome has high curiosity + moderate aggression

**Method:**
1. Spawn 50 agents with random genomes
2. Track which genomes lead to highest fitness
3. Analyze correlation between genome params and fitness

**Expected Insights:**
- Curiosity 0.6-0.8 performs best
- Aggression 0.4-0.6 performs best
- Cooperation 0.7+ benefits in cooperative tasks

---

## 🌊 Swarm Behavior Experiments

### Experiment 11: Groupthink Detection

**Hypothesis:** When all agents agree, MetaObserver warns of groupthink

**Method:**
1. Inject decision that's obviously good
2. All agents flag same insight
3. Check if MetaObserver detects consensus

**Expected Insight:**
- MetaObserver warns "80%+ consensus - possible groupthink"

---

### Experiment 12: Blind Spot Detection

**Hypothesis:** Missing agent types create blind spots

**Method:**
1. Kill all TiltDetector agents
2. Inject high-tilt scenario
3. Check if MetaObserver detects blind spot

**Expected Insight:**
- MetaObserver warns "No TiltDetector activity"

---

### Experiment 13: Agent Competition Creates Better Insights

**Hypothesis:** Competition drives agents to generate better insights

**Method:**
1. Run swarm with competition enabled (default)
2. Run swarm with competition disabled
3. Compare insight quality

**Expected Result:**
- Competition-enabled swarm generates 30% more insights

---

## 📊 Long-Term Studies

### 90-Day Study: Decision Quality Improvement

**Method:**
1. Log all decisions for 90 days
2. Track:
   - Betting ROI over time
   - Job offer rate over time
   - Negotiation satisfaction over time
3. Measure if trend is upward

**Expected Result:**
- Betting ROI improves 15-25%
- Job offer rate improves 20-40%
- Negotiation outcomes improve 10-20%

**How to Track:**
```python
# Weekly analysis
tracker = DecisionTracker()

# Week 1 stats
week1_stats = tracker.calculate_betting_stats()  # All bets from week 1

# Week 12 stats
week12_stats = tracker.calculate_betting_stats()  # All bets up to week 12

# Compare
roi_improvement = week12_stats['roi'] - week1_stats['roi']
print(f"ROI improved {roi_improvement:.1f}%")
```

---

### 90-Day Study: Bias Reduction

**Method:**
1. Count biases detected in first 30 days
2. Count biases detected in last 30 days
3. Check if frequency decreases

**Expected Result:**
- Bias frequency drops 40-60%
- You've learned to recognize and avoid them

---

### 90-Day Study: Agent Evolution Trajectory

**Method:**
1. Track average agent generation over time
2. Track average fitness over time
3. Plot evolution curve

**Expected Result:**
- Average generation increases linearly
- Average fitness increases exponentially (learning curve)

---

## 🎯 Custom Experiments

### Design Your Own

**Template:**

1. **Hypothesis:** What do you expect to happen?
2. **Method:** How will you test it?
3. **Data Collection:** What will you measure?
4. **Expected Insights:** What should the agents discover?
5. **Duration:** How long will it run?
6. **Analysis:** How will you know if you were right?

**Example Custom Experiment:**

*Hypothesis:* Logging decisions immediately after biometric data collection improves agent accuracy

*Method:*
- Week 1: Log decisions without biometric context
- Week 2: Log biometrics first, then decisions
- Compare agent insight quality

*Data:* Count of actionable insights per week

*Expected:* Week 2 has 50% more actionable insights

---

## 📝 Experiment Logging

Create an experiment journal:

```bash
mkdir -p psyche_edge/data/experiments
```

For each experiment, create a JSON file:

```json
{
  "experiment_id": "loss_chasing_001",
  "name": "Loss Chasing Detection",
  "hypothesis": "After a loss, bet sizes increase",
  "start_date": "2025-01-15",
  "end_date": "2025-01-16",
  "method": "Log 10 normal bets, 1 loss, then increased bet",
  "results": {
    "bias_detected": true,
    "bias_type": "loss_aversion",
    "agent": "BiasHunter_abc123",
    "confidence": 0.85
  },
  "conclusion": "Hypothesis confirmed. Agent detected loss chasing pattern."
}
```

---

## 🏆 Challenge Experiments

### Challenge 1: Break the Swarm

Try to make decisions that fool all agents.

**Prize:** If you successfully avoid detection 10 times in a row, you've found a blind spot!

**Action:** Create a new agent type to cover that blind spot.

---

### Challenge 2: Optimize Your ROI

Use the swarm's insights to improve betting ROI to 10%+

**Method:** Follow every agent recommendation for 30 days

**Prize:** If successful, you've validated the system!

---

### Challenge 3: Build a New Agent

Design a new agent type that outperforms existing ones.

**Ideas:**
- TimeSeriesPredictor (predicts future tilt)
- SocialMediaSentimentAgent (scrapes Twitter for sports sentiment)
- SleepOptimizer (recommends best sleep schedule)
- FinancialAdvisor (manages bankroll)

---

Remember: **The swarm learns from every experiment. Your insights improve the agents. The agents improve your decisions. Positive feedback loop = exponential growth.**

Run experiments. Log everything. Let the swarm evolve.

🧠 PsycheEdge 2025

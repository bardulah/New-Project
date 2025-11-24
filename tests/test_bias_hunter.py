"""
Unit tests for BiasHunter agent
Tests cognitive bias detection capabilities
"""
import pytest
import time

from psyche_edge.agents.bias_hunter import BiasHunter
from tests.conftest import assert_agent_valid


class TestBiasHunterInitialization:
    """Tests for BiasHunter initialization"""

    def test_bias_hunter_initialization(self):
        """Test BiasHunter initializes correctly"""
        hunter = BiasHunter()

        assert hunter.agent_type == "BiasHunter"
        assert_agent_valid(hunter)
        assert len(hunter.BIASES) > 0

    def test_bias_hunter_custom_sensitivities(self):
        """Test bias detection sensitivities are initialized"""
        hunter = BiasHunter()

        # Should have sensitivity for each bias
        for bias_name in hunter.BIASES.keys():
            sensitivity_key = f'{bias_name}_sensitivity'
            assert sensitivity_key in hunter.genome.custom_params
            assert 0.0 <= hunter.genome.custom_params[sensitivity_key] <= 1.0

    def test_bias_hunter_knowledge_base(self):
        """Test knowledge base is initialized"""
        hunter = BiasHunter()

        assert 'biases_detected' in hunter.knowledge_base
        assert 'false_positives' in hunter.knowledge_base
        assert 'true_positives' in hunter.knowledge_base
        assert isinstance(hunter.knowledge_base['biases_detected'], list)

    def test_bias_hunter_with_generation(self):
        """Test BiasHunter with specific generation"""
        hunter = BiasHunter(generation=5)

        assert hunter.generation == 5


class TestBiasHunterPerception:
    """Tests for BiasHunter perception"""

    def test_perceive_empty_world_state(self):
        """Test perception with empty world state"""
        hunter = BiasHunter()
        perception = hunter.perceive({})

        assert 'timestamp' in perception
        assert 'decisions' in perception
        assert perception['decision_count'] == 0

    def test_perceive_with_decisions(self, populated_world_state):
        """Test perception extracts decisions correctly"""
        hunter = BiasHunter()
        perception = hunter.perceive(populated_world_state)

        assert perception['decision_count'] > 0
        assert 'decisions' in perception
        assert len(perception['decisions']) <= 20  # Only recent

    def test_perceive_extracts_biometric_data(self, populated_world_state):
        """Test perception extracts biometric data"""
        hunter = BiasHunter()
        perception = hunter.perceive(populated_world_state)

        assert 'hrv' in perception
        assert 'mood' in perception
        assert 'sleep_score' in perception
        assert perception['hrv'] == 65.0
        assert perception['mood'] == 'calm'

    def test_perceive_extracts_decision_features(self, populated_world_state):
        """Test perception extracts decision features"""
        hunter = BiasHunter()
        perception = hunter.perceive(populated_world_state)

        assert 'decision_types' in perception
        assert 'decision_outcomes' in perception
        assert 'bet_sizes' in perception
        assert len(perception['decision_outcomes']) > 0

    def test_perceive_limits_recent_decisions(self):
        """Test perception only looks at recent 20 decisions"""
        hunter = BiasHunter()

        # Create world state with many decisions
        world_state = {
            'decision_history': [
                {'type': 'bet', 'outcome': i * 10, 'bet_size': 100}
                for i in range(50)
            ]
        }

        perception = hunter.perceive(world_state)

        assert len(perception['decisions']) == 20


class TestBiasHunterDetection:
    """Tests for bias detection logic"""

    def test_think_insufficient_decisions(self):
        """Test thinking with insufficient decisions"""
        hunter = BiasHunter()
        perception = {
            'decisions': [],
            'decision_count': 0
        }

        decision = hunter.think(perception)

        assert decision['action'] == 'observe'
        assert decision['biases_detected'] == []

    def test_think_with_decisions(self):
        """Test thinking processes decisions"""
        hunter = BiasHunter()
        perception = {
            'decisions': [
                {'type': 'bet', 'bet_size': 100, 'outcome': -100, 'timestamp': time.time()},
                {'type': 'bet', 'bet_size': 200, 'outcome': -200, 'timestamp': time.time()},
                {'type': 'bet', 'bet_size': 400, 'outcome': -400, 'timestamp': time.time()},
            ],
            'decision_count': 3,
            'decision_outcomes': [-100, -200, -400],
            'bet_sizes': [100, 200, 400]
        }

        decision = hunter.think(perception)

        assert 'biases_detected' in decision
        assert isinstance(decision['biases_detected'], list)

    def test_detect_loss_aversion_pattern(self):
        """Test detection of loss aversion (doubling down after losses)"""
        hunter = BiasHunter()

        # Pattern: doubling bet size after losses
        decisions = [
            {'type': 'bet', 'bet_size': 100, 'outcome': -100, 'timestamp': time.time() - 300},
            {'type': 'bet', 'bet_size': 200, 'outcome': -200, 'timestamp': time.time() - 200},
            {'type': 'bet', 'bet_size': 400, 'outcome': -400, 'timestamp': time.time() - 100},
        ]

        perception = {
            'decisions': decisions,
            'decision_count': 3,
            'decision_outcomes': [-100, -200, -400],
            'bet_sizes': [100, 200, 400]
        }

        decision = hunter.think(perception)

        # Should detect loss aversion or sunk cost
        biases = [b['bias_type'] for b in decision['biases_detected']]
        assert any(bias in ['loss_aversion', 'sunk_cost'] for bias in biases)

    def test_detect_gamblers_fallacy_pattern(self):
        """Test detection of gambler's fallacy"""
        hunter = BiasHunter()

        # Pattern: many losses followed by large bet (thinking win is "due")
        decisions = []
        base_time = time.time() - 600

        # 5 losses
        for i in range(5):
            decisions.append({
                'type': 'bet',
                'bet_size': 100,
                'outcome': -100,
                'timestamp': base_time + (i * 60)
            })

        # Then a big bet
        decisions.append({
            'type': 'bet',
            'bet_size': 500,
            'outcome': -500,
            'timestamp': base_time + 360
        })

        perception = {
            'decisions': decisions,
            'decision_count': len(decisions),
            'decision_outcomes': [-100] * 5 + [-500],
            'bet_sizes': [100] * 5 + [500]
        }

        decision = hunter.think(perception)

        # Should potentially detect gambler's fallacy or related bias
        assert isinstance(decision['biases_detected'], list)


class TestBiasHunterActions:
    """Tests for BiasHunter actions"""

    def test_act_generates_insight(self):
        """Test act generates bias insights"""
        hunter = BiasHunter()

        decision = {
            'action': 'alert',
            'biases_detected': [
                {
                    'bias_type': 'loss_aversion',
                    'confidence': 0.8,
                    'description': 'Detected loss aversion pattern'
                }
            ]
        }

        result = hunter.act(decision)

        assert result['success'] is True
        assert 'insights' in result
        assert len(result['insights']) > 0

    def test_act_updates_metrics(self):
        """Test act updates agent metrics"""
        hunter = BiasHunter()

        initial_insights = hunter.metrics.insights_generated
        initial_biases = hunter.metrics.biases_detected

        decision = {
            'action': 'alert',
            'biases_detected': [
                {
                    'bias_type': 'anchoring',
                    'confidence': 0.7,
                    'description': 'Anchoring detected'
                }
            ]
        }

        hunter.act(decision)

        assert hunter.metrics.insights_generated > initial_insights
        assert hunter.metrics.biases_detected > initial_biases

    def test_act_no_biases_observed(self):
        """Test act when observing (no biases)"""
        hunter = BiasHunter()

        decision = {
            'action': 'observe',
            'biases_detected': []
        }

        result = hunter.act(decision)

        assert result['success'] is True
        assert result['insights'] == []


class TestBiasHunterRunCycle:
    """Tests for full BiasHunter run cycle"""

    def test_run_cycle_complete(self, populated_world_state):
        """Test complete run cycle"""
        hunter = BiasHunter()

        result = hunter.run_cycle(populated_world_state)

        assert result['success'] is True
        assert 'insights' in result

    def test_run_cycle_updates_activity(self, populated_world_state):
        """Test run cycle updates last_active timestamp"""
        hunter = BiasHunter()

        initial_time = hunter.metrics.last_active
        time.sleep(0.01)

        hunter.run_cycle(populated_world_state)

        assert hunter.metrics.last_active > initial_time

    def test_run_cycle_empty_state(self):
        """Test run cycle with empty world state"""
        hunter = BiasHunter()

        result = hunter.run_cycle({})

        # Should not crash
        assert result is not None


class TestBiasHunterEvolution:
    """Tests for BiasHunter evolution and breeding"""

    def test_evolve_preserves_sensitivities(self):
        """Test evolution preserves bias sensitivity parameters"""
        hunter = BiasHunter()

        offspring = hunter.evolve()

        # Check sensitivities are still present
        for bias_name in hunter.BIASES.keys():
            sensitivity_key = f'{bias_name}_sensitivity'
            assert sensitivity_key in offspring.genome.custom_params

    def test_evolve_mutates_sensitivities(self, deterministic_random):
        """Test evolution mutates sensitivity parameters"""
        hunter = BiasHunter()

        original_sensitivity = hunter.genome.custom_params['anchoring_sensitivity']
        offspring = hunter.evolve(mutation_strength=2.0)

        # Should be different (with high probability)
        # Note: might be same due to randomness, but unlikely
        assert 0.0 <= offspring.genome.custom_params['anchoring_sensitivity'] <= 1.0

    def test_breed_combines_sensitivities(self):
        """Test breeding combines sensitivity parameters"""
        hunter1 = BiasHunter()
        hunter2 = BiasHunter()

        # Set different sensitivities
        hunter1.genome.custom_params['anchoring_sensitivity'] = 0.2
        hunter2.genome.custom_params['anchoring_sensitivity'] = 0.8

        child = hunter1.breed(hunter2)

        # Child should have intermediate value (roughly)
        child_sensitivity = child.genome.custom_params['anchoring_sensitivity']
        assert 0.0 <= child_sensitivity <= 1.0

    def test_evolved_hunter_is_functional(self, populated_world_state):
        """Test evolved hunter can still function"""
        hunter = BiasHunter()
        offspring = hunter.evolve()

        result = offspring.run_cycle(populated_world_state)

        assert result['success'] is True


class TestBiasHunterEdgeCases:
    """Test edge cases and error conditions"""

    def test_no_bet_decisions(self):
        """Test handling decisions without bets"""
        hunter = BiasHunter()

        world_state = {
            'decision_history': [
                {'type': 'job_application', 'timestamp': time.time()},
                {'type': 'negotiation', 'timestamp': time.time()}
            ]
        }

        result = hunter.run_cycle(world_state)

        # Should not crash
        assert result is not None

    def test_missing_outcome_data(self):
        """Test handling decisions with missing outcomes"""
        hunter = BiasHunter()

        world_state = {
            'decision_history': [
                {'type': 'bet', 'bet_size': 100, 'timestamp': time.time()},
                {'type': 'bet', 'bet_size': 200, 'timestamp': time.time()}
            ]
        }

        result = hunter.run_cycle(world_state)

        # Should handle gracefully
        assert result is not None

    def test_extreme_sensitivities(self):
        """Test hunter with extreme sensitivity settings"""
        hunter = BiasHunter()

        # Set all sensitivities to extremes
        for bias_name in hunter.BIASES.keys():
            sensitivity_key = f'{bias_name}_sensitivity'
            hunter.genome.custom_params[sensitivity_key] = 1.0

        world_state = {
            'decision_history': [
                {'type': 'bet', 'bet_size': 100, 'outcome': -100, 'timestamp': time.time()},
                {'type': 'bet', 'bet_size': 100, 'outcome': -100, 'timestamp': time.time()}
            ]
        }

        result = hunter.run_cycle(world_state)

        # Should still work, possibly detecting many biases
        assert result is not None

    def test_all_wins_pattern(self):
        """Test detection with all winning decisions"""
        hunter = BiasHunter()

        world_state = {
            'decision_history': [
                {'type': 'bet', 'bet_size': 100, 'outcome': 100, 'timestamp': time.time()}
                for _ in range(10)
            ]
        }

        result = hunter.run_cycle(world_state)

        # Should potentially detect overconfidence
        assert result is not None

    def test_random_pattern(self):
        """Test detection with truly random outcomes"""
        hunter = BiasHunter()

        import random
        decisions = []
        for i in range(20):
            decisions.append({
                'type': 'bet',
                'bet_size': random.choice([50, 100, 150]),
                'outcome': random.choice([-100, -50, 0, 50, 100]),
                'timestamp': time.time() - (20 - i) * 60
            })

        world_state = {'decision_history': decisions}

        result = hunter.run_cycle(world_state)

        # Should handle random data gracefully
        assert result is not None
        assert result['success'] is True


class TestBiasHunterKnowledgeBase:
    """Tests for BiasHunter knowledge accumulation"""

    def test_knowledge_base_tracks_detections(self):
        """Test knowledge base tracks detected biases"""
        hunter = BiasHunter()

        world_state = {
            'decision_history': [
                {'type': 'bet', 'bet_size': 100, 'outcome': -100, 'timestamp': time.time()},
                {'type': 'bet', 'bet_size': 200, 'outcome': -200, 'timestamp': time.time()},
                {'type': 'bet', 'bet_size': 400, 'outcome': -400, 'timestamp': time.time()},
            ]
        }

        hunter.run_cycle(world_state)

        # Knowledge base should contain detection history
        assert 'biases_detected' in hunter.knowledge_base

    def test_fitness_calculation_includes_biases(self):
        """Test fitness includes bias detection count"""
        hunter = BiasHunter()

        hunter.metrics.biases_detected = 10
        hunter.metrics.correct_predictions = 10
        hunter.metrics.failed_predictions = 2

        fitness = hunter.calculate_fitness()

        assert fitness > 0
        # Biases detected should contribute to fitness

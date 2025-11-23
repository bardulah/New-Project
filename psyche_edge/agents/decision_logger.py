"""
Decision Logger Agent
Obsessively tracks every decision with full context:
- Betting decisions (sport, amount, odds, outcome, ROI)
- Job applications (company, role, outcome, timeline)
- Negotiations (type, ask, outcome, satisfaction)
- General life decisions

Creates structured data for analysis and ML
"""
import time
import json
from pathlib import Path
from typing import Dict, Any
from ..core.agent_dna import AgentDNA


class DecisionLogger(AgentDNA):
    """
    Data collection specialist
    Logs all decisions with full context for analysis
    """

    def __init__(self, genome=None, parent_ids=None, generation=0):
        super().__init__(
            agent_type="DecisionLogger",
            genome=genome,
            parent_ids=parent_ids,
            generation=generation
        )

        self.genome.custom_params.setdefault('logging_detail_level', 0.8)
        self.genome.custom_params.setdefault('auto_structure', 0.7)

        self.knowledge_base['decisions_logged'] = 0
        self.knowledge_base['log_files'] = []

    def perceive(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Look for new unlogged decisions"""
        decision_history = world_state.get('decision_history', [])

        # Check for decisions that need logging
        logged_count = self.knowledge_base.get('decisions_logged', 0)
        new_decisions = decision_history[logged_count:]

        perception = {
            'timestamp': time.time(),
            'new_decisions': new_decisions,
            'new_decision_count': len(new_decisions),
            'biometrics': world_state.get('biometric_data', {}),
            'recent_insights': world_state.get('recent_insights', [])[-5:]
        }

        return perception

    def think(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Decide what/how to log"""
        new_decisions = perception.get('new_decisions', [])

        if not new_decisions:
            return {'action': 'wait'}

        # Structure each decision for logging
        structured_decisions = []

        for decision in new_decisions:
            decision_type = decision.get('type', 'unknown')

            # Add context from biometrics and insights
            enriched_decision = {
                **decision,
                'logged_at': time.time(),
                'logger_agent_id': self.agent_id,
                'context': {
                    'hrv': perception['biometrics'].get('hrv'),
                    'sleep_score': perception['biometrics'].get('sleep_score'),
                    'mood': perception['biometrics'].get('mood'),
                    'recent_insights': perception['recent_insights']
                }
            }

            # Type-specific structuring
            if decision_type == 'bet':
                enriched_decision = self._structure_bet_decision(enriched_decision)
            elif decision_type == 'job_application':
                enriched_decision = self._structure_job_decision(enriched_decision)
            elif decision_type == 'negotiation':
                enriched_decision = self._structure_negotiation_decision(enriched_decision)

            structured_decisions.append(enriched_decision)

        return {
            'action': 'log',
            'decisions': structured_decisions,
            'count': len(structured_decisions)
        }

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Write decisions to structured logs"""
        action = decision.get('action')

        if action == 'log':
            decisions_to_log = decision.get('decisions', [])

            for dec in decisions_to_log:
                self._write_to_log(dec)

            # Update metrics
            self.knowledge_base['decisions_logged'] += len(decisions_to_log)
            self.metrics.insights_generated += len(decisions_to_log)

            return {
                'type': 'decisions_logged',
                'count': len(decisions_to_log),
                'insight': f"📝 Logged {len(decisions_to_log)} decisions",
                'score': len(decisions_to_log),
                'agent_id': self.agent_id
            }

        return {'type': 'waiting', 'score': 0}

    def _structure_bet_decision(self, decision: Dict) -> Dict:
        """Add betting-specific structure"""
        return {
            **decision,
            'structured_data': {
                'sport': decision.get('sport', 'unknown'),
                'bet_type': decision.get('bet_type', 'unknown'),
                'bet_size': decision.get('bet_size', 0),
                'odds': decision.get('odds', 0),
                'expected_value': decision.get('expected_value', 0),
                'outcome': decision.get('outcome'),
                'roi': decision.get('roi'),
                'book': decision.get('book'),
                'reasoning': decision.get('notes', '')
            }
        }

    def _structure_job_decision(self, decision: Dict) -> Dict:
        """Add job application structure"""
        return {
            **decision,
            'structured_data': {
                'company': decision.get('company', 'unknown'),
                'role': decision.get('role', 'unknown'),
                'application_date': decision.get('timestamp'),
                'outcome': decision.get('outcome'),
                'response_time_days': decision.get('response_time'),
                'salary_ask': decision.get('salary_ask'),
                'reasoning': decision.get('notes', '')
            }
        }

    def _structure_negotiation_decision(self, decision: Dict) -> Dict:
        """Add negotiation structure"""
        return {
            **decision,
            'structured_data': {
                'negotiation_type': decision.get('negotiation_type', 'unknown'),
                'initial_ask': decision.get('initial_ask'),
                'final_outcome': decision.get('final_outcome'),
                'satisfaction': decision.get('satisfaction'),
                'strategy_used': decision.get('strategy'),
                'reasoning': decision.get('notes', '')
            }
        }

    def _write_to_log(self, decision: Dict):
        """Write decision to appropriate log file"""
        decision_type = decision.get('type', 'unknown')

        # Determine log file path
        log_dir = Path('psyche_edge/data/decisions')
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"{decision_type}_log.jsonl"

        # Append to log
        with open(log_file, 'a') as f:
            f.write(json.dumps(decision) + '\n')

        # Track log files
        if str(log_file) not in self.knowledge_base.get('log_files', []):
            if 'log_files' not in self.knowledge_base:
                self.knowledge_base['log_files'] = []
            self.knowledge_base['log_files'].append(str(log_file))

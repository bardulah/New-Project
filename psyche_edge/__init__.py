"""
PsycheEdge 2025 - Self-Evolving Cognitive & Decision-Science Laboratory
A living, non-linear, multi-agent system for studying decision-making
"""

__version__ = "0.1.0"
__author__ = "PsycheEdge Swarm"

from .core.agent_dna import AgentDNA, AgentGenome, AgentMetrics, AgentStatus
from .core.swarm import SwarmOrchestrator

__all__ = [
    'AgentDNA',
    'AgentGenome',
    'AgentMetrics',
    'AgentStatus',
    'SwarmOrchestrator'
]

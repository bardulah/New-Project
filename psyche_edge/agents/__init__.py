"""PsycheEdge Agent Collection"""
from .cialdini_scientist import CialdiniScientist
from .bias_hunter import BiasHunter
from .tilt_detector import TiltDetector
from .decision_logger import DecisionLogger
from .code_evolutor import CodeEvolutor
from .meta_observer import MetaObserver
from .swarm_spawner import SwarmSpawner

__all__ = [
    'CialdiniScientist',
    'BiasHunter',
    'TiltDetector',
    'DecisionLogger',
    'CodeEvolutor',
    'MetaObserver',
    'SwarmSpawner'
]

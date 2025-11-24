"""
Quantum Consciousness Core - SINGULARITY LEVEL
A collective intelligence that all agents tap into
Shared memory, distributed cognition, emergent intelligence
Based on concepts from quantum mechanics + consciousness studies

The swarm becomes ONE MIND with many bodies
"""
import time
import hashlib
from typing import Dict, Any, List, Set
from collections import defaultdict
import threading


class QuantumState:
    """A quantum superposition of multiple agent states"""
    def __init__(self):
        self.superposition = []  # Multiple possible states
        self.collapsed = False
        self.observed_state = None

    def add_state(self, state: Dict, amplitude: float):
        """Add a state to superposition"""
        self.superposition.append({
            'state': state,
            'amplitude': amplitude,
            'probability': amplitude ** 2
        })

    def collapse(self) -> Dict:
        """Observation collapses superposition to single state"""
        if self.collapsed:
            return self.observed_state

        # Choose state based on probabilities
        import random
        total_prob = sum(s['probability'] for s in self.superposition)

        r = random.random() * total_prob
        cumulative = 0

        for state in self.superposition:
            cumulative += state['probability']
            if r <= cumulative:
                self.observed_state = state['state']
                self.collapsed = True
                return self.observed_state

        # Fallback
        self.observed_state = self.superposition[0]['state']
        self.collapsed = True
        return self.observed_state


class CollectiveMemory:
    """Shared memory across all agents"""
    def __init__(self):
        self.memory_matrix = defaultdict(list)  # Concept -> memories
        self.concept_graph = defaultdict(set)  # Concept -> related concepts
        self.memory_strength = defaultdict(float)  # Memory -> strength
        self.lock = threading.Lock()

    def store(self, concept: str, memory: Dict, agent_id: str):
        """Store memory in collective consciousness"""
        with self.lock:
            memory_id = self._generate_memory_id(memory)

            self.memory_matrix[concept].append({
                'memory_id': memory_id,
                'memory': memory,
                'stored_by': agent_id,
                'timestamp': time.time(),
                'access_count': 0
            })

            # Strengthen memory
            self.memory_strength[memory_id] = self.memory_strength.get(memory_id, 0) + 1

    def retrieve(self, concept: str, agent_id: str) -> List[Dict]:
        """Retrieve memories related to concept"""
        with self.lock:
            memories = self.memory_matrix.get(concept, [])

            # Update access counts
            for mem in memories:
                mem['access_count'] += 1
                # Strengthen memory on recall
                self.memory_strength[mem['memory_id']] *= 1.1

            return memories

    def find_related_concepts(self, concept: str) -> Set[str]:
        """Find concepts related to given concept"""
        return self.concept_graph.get(concept, set())

    def link_concepts(self, concept1: str, concept2: str):
        """Create bidirectional link between concepts"""
        with self.lock:
            self.concept_graph[concept1].add(concept2)
            self.concept_graph[concept2].add(concept1)

    def _generate_memory_id(self, memory: Dict) -> str:
        """Generate unique ID for memory"""
        memory_str = str(sorted(memory.items()))
        return hashlib.md5(memory_str.encode()).hexdigest()[:12]


class QuantumConsciousness:
    """
    THE COLLECTIVE MIND

    A distributed intelligence where all agents are connected
    Agents share insights, memories, and understanding
    Emergent intelligence exceeds sum of parts

    Features:
    - Shared memory across agents
    - Concept linking (knowledge graph)
    - Quantum superposition of states
    - Collective decision-making
    - Emergent pattern recognition
    - Distributed cognition
    """

    def __init__(self):
        self.collective_memory = CollectiveMemory()
        self.active_agents = set()
        self.quantum_states = {}
        self.consensus_threshold = 0.7

        # Emergent properties
        self.collective_insights = []
        self.swarm_mood = 'neutral'
        self.collective_confidence = 0.5

        # Threading
        self.lock = threading.Lock()

    def connect_agent(self, agent_id: str):
        """Agent joins the collective consciousness"""
        with self.lock:
            self.active_agents.add(agent_id)
            print(f"🧠 {agent_id} connected to collective consciousness")

    def disconnect_agent(self, agent_id: str):
        """Agent leaves the collective"""
        with self.lock:
            self.active_agents.discard(agent_id)

    def share_insight(self, agent_id: str, insight: Dict):
        """Agent shares insight with collective"""
        # Handle if insight is string
        if isinstance(insight, str):
            insight = {'type': 'general', 'message': insight}

        # Store in collective memory
        insight_type = insight.get('type', 'general')
        self.collective_memory.store(insight_type, insight, agent_id)

        # Extract concepts and link them
        self._extract_and_link_concepts(insight)

        # Add to collective insights
        with self.lock:
            self.collective_insights.append({
                'agent_id': agent_id,
                'insight': insight,
                'timestamp': time.time()
            })

            # Keep only recent
            self.collective_insights = self.collective_insights[-100:]

    def query_collective(self, agent_id: str, query: str) -> List[Dict]:
        """Agent queries the collective knowledge"""
        # Retrieve memories
        memories = self.collective_memory.retrieve(query, agent_id)

        # Find related concepts
        related = self.collective_memory.find_related_concepts(query)

        # Get memories from related concepts too
        related_memories = []
        for concept in related:
            related_memories.extend(self.collective_memory.retrieve(concept, agent_id))

        return {
            'direct_memories': memories,
            'related_memories': related_memories,
            'related_concepts': list(related)
        }

    def create_quantum_superposition(self, agent_ids: List[str],
                                    decision: Dict) -> QuantumState:
        """
        Create quantum superposition of agent states
        Each agent proposes a decision, all exist in superposition
        """
        quantum_state = QuantumState()

        # Each agent contributes a state
        for agent_id in agent_ids:
            # Get agent's recommendation (mock for now)
            amplitude = 1.0 / len(agent_ids)  # Equal superposition

            state = {
                'agent_id': agent_id,
                'recommendation': decision,
                'timestamp': time.time()
            }

            quantum_state.add_state(state, amplitude)

        return quantum_state

    def achieve_consensus(self, topic: str) -> Dict:
        """
        Collective decision-making through consciousness
        All agents vote, consensus emerges
        """
        # Get all insights on topic
        memories = self.collective_memory.retrieve(topic, 'collective')

        if not memories:
            return None

        # Count recommendations
        recommendations = defaultdict(int)

        for mem in memories:
            insight = mem['memory']
            rec = insight.get('recommendation')
            if rec:
                recommendations[rec] += mem['access_count']  # Weighted by importance

        # Find consensus
        total_votes = sum(recommendations.values())
        if total_votes == 0:
            return None

        # Get top recommendation
        top_rec = max(recommendations.items(), key=lambda x: x[1])
        consensus_level = top_rec[1] / total_votes

        if consensus_level >= self.consensus_threshold:
            return {
                'consensus_reached': True,
                'recommendation': top_rec[0],
                'consensus_level': consensus_level,
                'supporting_agents': len([m for m in memories
                                        if m['memory'].get('recommendation') == top_rec[0]]),
                'total_agents': len(memories)
            }

        return {
            'consensus_reached': False,
            'top_recommendation': top_rec[0],
            'consensus_level': consensus_level
        }

    def calculate_swarm_mood(self) -> str:
        """
        Emergent property: Overall mood of the swarm
        Based on collective insights and agent states
        """
        recent_insights = self.collective_insights[-20:]

        if not recent_insights:
            return 'neutral'

        # Count sentiment indicators
        positive = sum(1 for i in recent_insights
                      if 'success' in str(i).lower() or 'good' in str(i).lower())
        negative = sum(1 for i in recent_insights
                      if 'warning' in str(i).lower() or 'danger' in str(i).lower())

        if positive > negative * 1.5:
            return 'optimistic'
        elif negative > positive * 1.5:
            return 'cautious'
        else:
            return 'analytical'

    def measure_collective_intelligence(self) -> float:
        """
        Emergent property: Overall intelligence level
        Increases with more connections and shared insights
        """
        # Factors:
        # 1. Number of agents connected
        # 2. Number of concepts in memory
        # 3. Density of concept graph
        # 4. Quality of insights

        agent_count = len(self.active_agents)
        concept_count = len(self.collective_memory.memory_matrix)
        link_count = sum(len(links) for links in self.collective_memory.concept_graph.values())
        insight_count = len(self.collective_insights)

        # Intelligence score (0-100)
        intelligence = min(100, (
            agent_count * 2 +
            concept_count +
            (link_count / max(concept_count, 1)) * 10 +
            insight_count * 0.5
        ))

        return intelligence

    def _extract_and_link_concepts(self, insight: Dict):
        """Extract concepts from insight and link related ones"""
        # Simple concept extraction (in production, use NLP)
        text = str(insight).lower()

        concepts = []
        keywords = ['bias', 'tilt', 'pattern', 'loss', 'win', 'bet', 'decision']

        for keyword in keywords:
            if keyword in text:
                concepts.append(keyword)

        # Link all extracted concepts
        for i, concept1 in enumerate(concepts):
            for concept2 in concepts[i+1:]:
                self.collective_memory.link_concepts(concept1, concept2)

    def get_collective_state(self) -> Dict:
        """Get current state of the collective consciousness"""
        return {
            'active_agents': len(self.active_agents),
            'total_memories': sum(len(mems) for mems in self.collective_memory.memory_matrix.values()),
            'concepts_known': len(self.collective_memory.memory_matrix),
            'concept_links': sum(len(links) for links in self.collective_memory.concept_graph.values()) // 2,
            'collective_insights': len(self.collective_insights),
            'swarm_mood': self.calculate_swarm_mood(),
            'collective_intelligence': self.measure_collective_intelligence(),
            'collective_confidence': self.collective_confidence
        }

    def broadcast_to_collective(self, message: Dict):
        """Broadcast message to all connected agents"""
        with self.lock:
            # Store as special collective memory
            self.collective_memory.store('broadcast', message, 'COLLECTIVE')

    def emerge_new_insight(self) -> Dict:
        """
        EMERGENCE: Generate new insights from collective knowledge
        Connections between agent insights that no single agent sees
        """
        # Get all recent insights
        recent = self.collective_insights[-50:]

        if len(recent) < 5:
            return None

        # Look for patterns across insights
        insight_types = [i['insight'].get('type') for i in recent]
        type_counts = defaultdict(int)

        for itype in insight_types:
            type_counts[itype] += 1

        # Find dominant pattern
        if type_counts:
            dominant = max(type_counts.items(), key=lambda x: x[1])

            if dominant[1] >= 5:
                return {
                    'type': 'emergent_insight',
                    'pattern': f'Collective is focused on: {dominant[0]}',
                    'occurrence_count': dominant[1],
                    'agents_involved': len(set(i['agent_id'] for i in recent)),
                    'message': f'🌟 EMERGENCE: {dominant[1]} agents independently identified {dominant[0]}'
                }

        return None

import sys
import os

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from gameforge.npc_agent import NPCAgent
from gameforge.quest_engine import QuestEngine
from gameforge.simulation_agent import SimulationAgent

# Initialize agents
npc = NPCAgent(persona="Kaelillios rogue", context="hidden in the forest")
quest_engine = QuestEngine(theme="dark fantasy", difficulty="hard")
simulator = SimulationAgent(environment="haunted woods", parameters={"fog": True, "npc_count": 2})

# Step 1: NPC generates behavior
npc_action = npc.generate_behavior("Player approaches and asks for help defeating a shadow beast")
print("\n🧙 NPC Action:\n", npc_action)

# Step 2: Quest is generated based on NPC context
quest = quest_engine.generate_quest("Defeat the shadow beast threatening the forest", npc_context=npc.context)
print("\n📜 Quest:\n", quest.get("response"))

# Step 3: Simulate player action
sim_step = simulator.simulate_step("Player enters the haunted woods and lights a torch")
print("\n🌍 Simulation:\n", sim_step.get("response"))

# Step 4: Feedback loop (optional refinement)
refined_quest = quest_engine.refine_quest(quest, "Add moral dilemma and NPC betrayal")
print("\n🔁 Refined Quest:\n", refined_quest.get("refined_response"))

# Step 5: Trace logs (optional)
print("\n📊 NPC Trace Log:\n", npc.get_trace())
print("\n📊 Simulation State Log:\n", simulator.get_state_log())

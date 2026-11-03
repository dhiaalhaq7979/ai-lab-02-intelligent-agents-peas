"""
Model-based agents - Task 3
---------------------------
MemoryAgent      : same decision rules as the reflex agent, but it keeps an
                   internal state (the last mode). It only sends a command when
                   the mode actually changes.
HysteresisAgent  : my extra experiment. It also uses a small dead band (0.5 C)
                   so a noisy sensor near a limit does not make it switch back
                   and forth all the time.
"""

try:
    from .reflex_agent import ClassroomAgent
except ImportError:  # allows: python agents/memory_agent.py
    from reflex_agent import ClassroomAgent


class MemoryAgent:
    def __init__(self):
        self.rules = ClassroomAgent()   # reuse the reflex rules
        self.last_mode = None           # internal state (nothing at the start)

    def decide(self, temp, occupied):
        """Return (mode, should_send)."""
        mode = self.rules.act(temp, occupied)
        should_send = mode != self.last_mode
        self.last_mode = mode
        return mode, should_send


class HysteresisAgent(MemoryAgent):
    DEAD_BAND = 0.5

    def decide(self, temp, occupied):
        mode = self.rules.act(temp, occupied)
        if occupied:
            # stay in COOL / WARM until the reading is clearly back inside the range
            if self.last_mode == "COOL" and temp > 26 - self.DEAD_BAND:
                mode = "COOL"
            elif self.last_mode == "WARM" and temp < 20 + self.DEAD_BAND:
                mode = "WARM"
        should_send = mode != self.last_mode
        self.last_mode = mode
        return mode, should_send

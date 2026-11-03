"""Test scenarios for the model-based agents (Task 3)."""

try:
    from .memory_agent import HysteresisAgent, MemoryAgent
    from .reflex_agent import ClassroomAgent, percepts as MANUAL_PERCEPTS
except ImportError:
    from memory_agent import HysteresisAgent, MemoryAgent
    from reflex_agent import ClassroomAgent, percepts as MANUAL_PERCEPTS


# (temperature, occupied), expected mode, expected send, what the step tests
MY_SCENARIO = [
    ((24, True), "IDLE", True, "first reading, comfortable room"),
    ((24, True), "IDLE", False, "same reading again -> no duplicate command"),
    ((27, True), "COOL", True, "too hot -> switch to COOL"),
    ((26, True), "IDLE", True, "exactly 26 C is NOT > 26 -> back to IDLE"),
    ((20, True), "IDLE", False, "exactly 20 C is NOT < 20 -> stays IDLE"),
    ((18, True), "WARM", True, "too cold -> switch to WARM"),
    ((18, False), "ECO", True, "room empty -> ECO has priority"),
    ((30, False), "ECO", False, "still empty even if hot -> no new command"),
    ((31, True), "COOL", True, "students return to a hot room"),
]

# noisy sensor readings around the LOWER limit (20 C)
NOISY_READINGS = [(19.8, True), (20.3, True), (19.6, True),
                  (20.1, True), (19.9, True), (19.7, True)]


def label(mode):
    return "-" if mode is None else mode


def check_my_scenario():
    print("My scenario for the memory agent:")
    print("t | last mode | percept | mode | send? | check | tested")
    agent, ok_count = MemoryAgent(), 0
    for i, (percept, exp_mode, exp_send, note) in enumerate(MY_SCENARIO, start=1):
        before = agent.last_mode
        mode, send = agent.decide(*percept)
        ok = (mode, send) == (exp_mode, exp_send)
        ok_count += ok
        print(f"{i} | {label(before)} | {percept} | {mode} | {'yes' if send else 'no'} | "
              f"{'OK' if ok else 'WRONG'} | {note}")
    print(f"Checks: {ok_count}/{len(MY_SCENARIO)} correct")
    return ok_count


def compare_on_manual_percepts():
    print("Reflex vs memory agent on the manual percepts:")
    print("t | percept | reflex mode | memory mode | memory sends?")
    reflex, memory = ClassroomAgent(), MemoryAgent()
    reflex_cmds = memory_cmds = 0
    for i, percept in enumerate(MANUAL_PERCEPTS, start=1):
        r_mode = reflex.act(*percept)
        m_mode, send = memory.decide(*percept)
        reflex_cmds += 1          # reflex agent always sends
        memory_cmds += send
        print(f"{i} | {percept} | {r_mode} | {m_mode} | {'yes' if send else 'no'}")
    print(f"Commands: reflex = {reflex_cmds}, memory = {memory_cmds} (same modes at every step)")


def noisy_sensor_test():
    print("Noisy readings near 20 C - memory agent vs hysteresis agent:")
    print("t | reading | memory mode | sends? | hysteresis mode | sends?")
    mem, hys = MemoryAgent(), HysteresisAgent()
    mem_cmds = hys_cmds = 0
    for i, percept in enumerate(NOISY_READINGS, start=1):
        m, ms = mem.decide(*percept)
        h, hs = hys.decide(*percept)
        mem_cmds += ms
        hys_cmds += hs
        print(f"{i} | {percept[0]} | {m} | {'yes' if ms else 'no'} | {h} | {'yes' if hs else 'no'}")
    print(f"Commands: memory agent = {mem_cmds}/{len(NOISY_READINGS)}, hysteresis agent = {hys_cmds}/{len(NOISY_READINGS)}")
    print("-> remembering the last mode is not enough near a limit; a dead band fixes the flickering.")


def run():
    print("-" * 70)
    print("Part B | Model-based agent with internal state (Task 3)")
    print("-" * 70)
    check_my_scenario()
    print()
    compare_on_manual_percepts()
    print()
    noisy_sensor_test()


if __name__ == "__main__":
    run()

"""
Simple reflex agent - manual section 2.5
----------------------------------------
The class and the percept list below are taken from the lab manual.
A simple reflex agent looks ONLY at the current percept: (temperature, occupied).
"""


class ClassroomAgent:
    def act(self, temp, occupied):
        if not occupied:
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"


# percepts and expected modes given in the manual
percepts = [(29, True), (29, True), (20, True),
            (26, True), (19, True), (29, False)]
MANUAL_EXPECTED = ["COOL", "COOL", "IDLE", "IDLE", "WARM", "ECO"]


def run():
    print("-" * 70)
    print("Part A | Simple reflex agent from the manual (section 2.5)")
    print("-" * 70)
    bot = ClassroomAgent()
    modes = [bot.act(t, occ) for t, occ in percepts]
    for i, ((t, occ), mode) in enumerate(zip(percepts, modes), start=1):
        print(f"t={i}  temp={t}C occupied={occ}  ->  {mode}")
    print("manual expects :", " ".join(MANUAL_EXPECTED))
    print("agent produced :", " ".join(modes))
    print("same as manual :", modes == MANUAL_EXPECTED)
    print("Observation: t=1 and t=2 both give COOL. Without memory the agent")
    print("would send the COOL command twice in a row.")


if __name__ == "__main__":
    run()

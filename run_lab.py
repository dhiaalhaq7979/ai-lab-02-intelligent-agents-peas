"""Entry point for AI Lab 02. Run with:  python run_lab.py"""
import sys

from agents import reflex_agent, test_scenarios


if __name__ == "__main__":
    print("AI Lab 02 - Intelligent Agents and the PEAS Framework")
    print("Student: Dhia Alhaq Saleh Al-Hindrish | BS Software Engineering")
    print(f"Python {sys.version.split()[0]} (standard library only)")
    print()
    reflex_agent.run()
    print()
    test_scenarios.run()

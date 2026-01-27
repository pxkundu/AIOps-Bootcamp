#!/usr/bin/env python3
import time
import sys

def colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def print_oracle(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    print()

def launch_quest():
    print(colored("\n" + "="*60, "36"))
    print(colored("          🔮 THE ORACLE'S QUEST: WEEK 3 LAUNCHPAD 🔮", "36;1"))
    print(colored("="*60 + "\n", "36"))

    print_oracle("Greetings, Data Guardian. I am the Oracle.")
    print_oracle("The city's heartbeat is erratic. I need you to master the 'Alchemical Spells' of Machine Learning.")
    print_oracle("But first, I must verify your intuition for the 'Raw Elements' (Data).")
    
    questions = [
        {
            "q": "1. If a server's latency has a 'Long Tail', which metric truly represents the user's pain?",
            "options": ["A) The Mean", "B) The Median", "C) The P99"],
            "a": "C"
        },
        {
            "q": "2. In a 'Normal Distribution', what percentage of data falls within 3 standard deviations?",
            "options": ["A) 50%", "B) 95%", "C) 99.7%"],
            "a": "C"
        },
        {
            "q": "3. Which 'Spell' (Algorithm) would you use to group 1 million unique log messages into patterns?",
            "options": ["A) Regression", "B) Clustering", "C) Classification"],
            "a": "B"
        }
    ]

    score = 0
    for i, q in enumerate(questions):
        print(colored(f"\n{q['q']}", "33;1"))
        for opt in q['options']:
            print(opt)
        
        ans = input("\nYour answer: ").strip().upper()
        if ans == q['a']:
            print(colored("✅ CORRECT! Your power grows.", "32"))
            score += 1
        else:
            print(colored("❌ INCORRECT. The Oracle's vision remains cloudy.", "31"))

    if score == len(questions):
        print(colored("\n" + "*"*60, "35"))
        print(colored("🏆 ALL TRIALS PASSED! The Laboratory is now OPEN.", "35;1"))
        print(colored("*"*60 + "\n", "35"))
        print_oracle("Proceed to Day 1: Statistical Foundations. May the patterns guide you.")
    else:
        print_oracle(f"\nYou passed {score}/{len(questions)} trials. Study the PREREQUISITES and try again to fully unlock the Oracle's sight.")

if __name__ == "__main__":
    launch_quest()

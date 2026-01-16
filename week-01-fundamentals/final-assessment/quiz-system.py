#!/usr/bin/env python3
"""
AIOps Quest - Automated Quiz Generator and Grader

Generates randomized quizzes from question bank and automatically grades responses.
"""

import json
import random
import time
from datetime import datetime

class AIOpsQuiz:
    def __init__(self, question_bank_file="questions.json"):
        with open(question_bank_file, 'r') as f:
            self.question_bank = json.load(f)
        self.score = 0
        self.total_questions = 0
        self.start_time = None
        self.answers = []
    
    def start_quiz(self, mode="knowledge_arena", num_questions=40):
        """Start a quiz session"""
        print("\n" + "="*70)
        print(f"🎮 AIOps Quest - {mode.replace('_', ' ').title()}")
        print("="*70)
        print(f"\nTotal Questions: {num_questions}")
        print(f"Time Limit: Check individual rounds")
        print("\nPress Enter to begin...")
        input()
        
        self.start_time = time.time()
        
        #Select random questions
        selected = random.sample(
            [q for q in self.question_bank if q['mode'] == mode],
            num_questions
        )
        
        for idx, question in enumerate(selected, 1):
            self._ask_question(idx, question)
        
        self._show_results()
    
    def _ask_question(self, num, question):
        """Display and grade a single question"""
        print(f"\n{'='*70}")
        print(f"Question {num}/{self.total_questions + 1}")
        print(f"Category: {question['category']} | Difficulty: {question['difficulty']}")
        print(f"{'='*70}\n")
        
        print(question['question'])
        print()
        
        if question['type'] == 'multiple_choice':
            for key, value in question['options'].items():
                print(f"{key}) {value}")
            print()
            answer = input("Your answer (A/B/C/D): ").strip().upper()
            
            correct = answer == question['correct_answer']
            points = question['points'] if correct else -0.5
            
        elif question['type'] == 'true_false':
            answer = input("Your answer (True/False): ").strip().lower()
            correct = answer[0] == question['correct_answer'][0].lower()
            points = question['points'] if correct else -0.5
        
        elif question['type'] == 'short_answer':
            answer = input("Your answer: ").strip()
            print("\n🤖 AI Grading in progress...")
            # Simplified - in reality would use fuzzy matching
            correct = answer.lower() in [a.lower() for a in question['acceptable_answers']]
            points = question['points'] if correct else 0
        
        self.score += points
        self.total_questions += 1
        
        self.answers.append({
            'question': question['question'],
            'your_answer': answer,
            'correct_answer': question['correct_answer'],
            'correct': correct,
            'points': points
        })
        
        if correct:
            print(f"\n✅ Correct! +{points} points")
        else:
            print(f"\n❌ Incorrect. Correct answer: {question['correct_answer']}")
            if 'explanation' in question:
                print(f"💡 Explanation: {question['explanation']}")
    
    def _show_results(self):
        """Display final results"""
        elapsed = time.time() - self.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        
        print("\n" + "="*70)
        print("🏁 QUIZ COMPLETE!")
        print("="*70)
        print(f"\nFinal Score: {self.score}/{self.total_questions * 2} points")
        print(f"Percentage: {(self.score / (self.total_questions * 2)) * 100:.1f}%")
        print(f"Time Taken: {minutes}m {seconds}s")
        
        # Determine tier
        if self.score >= self.total_questions * 1.75:
            tier = "💎 Platinum"
        elif self.score >= self.total_questions * 1.5:
            tier = "🥇 Gold"
        elif self.score >= self.total_questions * 1.25:
            tier = "🥈 Silver"
        else:
            tier = "🥉 Bronze"
        
        print(f"\nAchievement Tier: {tier}")
        
        # Save results
        results = {
            'timestamp': datetime.now().isoformat(),
            'mode': 'knowledge_arena',
            'score': self.score,
            'total': self.total_questions * 2,
            'time_taken': elapsed,
            'tier': tier,
            'answers': self.answers
        }
        
        with open(f'results_{int(time.time())}.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📊 Detailed results saved to results_{int(time.time())}.json")


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║              🎮 AIOps Quest - Quiz System 🎮                ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("\nSelect Quiz Mode:")
    print("1) Knowledge Arena (40 questions, 30 min)")
    print("2) True/False Speed Run (20 questions, 10 min)")
    print("3) Practice Mode (10 random questions)")
    print("4) Exit")
    
    choice = input("\nYour choice: ").strip()
    
    quiz = AIOpsQuiz()
    
    if choice == '1':
        quiz.start_quiz('knowledge_arena', 40)
    elif choice == '2':
        quiz.start_quiz('true_false', 20)
    elif choice == '3':
        quiz.start_quiz('knowledge_arena', 10)
    else:
        print("Goodbye!")
        return
    
    print("\n\n🎯 Next Challenge: Lab Gauntlet")
    print("Run: ./start-labs.sh")


if __name__ == "__main__":
    main()

# Week 1 Final Assessment

> **The AIOps Quest - Gamified Knowledge Validation**

---

## 🎯 Overview

The Week 1 Final Assessment is a comprehensive, gamified testing environment that validates your mastery of all topics covered in Week 1. Instead of a traditional exam, you'll embark on **The AIOps Quest** - a multi-mode challenge system that tests both theoretical knowledge and practical skills.

---

## 🎮 Assessment Structure

### 4 Challenge Modes

1. **🧠 Knowledge Arena** (200 points) - Quiz-based challenges
2. **💻 Lab Gauntlet** (300 points) - Hands-on practical tasks
3. **🔥 Incident Dungeon** (300 points) - Progressive incident response scenarios
4. **⚔️ Final Boss Battle** (200 points) - Complex multi-front crisis simulation

**Total Possible:** 1,100 points (including bonuses)

---

## 📊 Quick Start

### Prerequisites

```bash
# Ensure Docker is running
docker --version

# Navigate to assessment directory
cd week-01-fundamentals/final-assessment

# Verify infrastructure
./check-readiness.sh
```

### Start the Quest

```bash
# Option 1: Interactive Mode
./start-quest.sh

# Option 2: Specific Mode
./start-quest.sh --mode knowledge    # Quiz only
./start-quest.sh --mode labs         # Hands-on only
./start-quest.sh --mode incidents    # Troubleshooting only
./start-quest.sh --mode boss         # Final boss only

# Option 3: Full Gauntlet (all modes in sequence)
./start-quest.sh --full
```

---

## 📁 Files & Structure

```
final-assessment/
├── AIOPS-QUEST.md           # Complete quest guide
├── README.md                # This file
├── quiz-system.py           # Automated quiz engine
├── questions.json           # Question bank
├── lab-challenges/          # Hands-on lab setups
│   ├── broken-dashboard/
│   ├── mystery-app/
│   └── migration-challenge/
├── incident-scenarios/      # Incident simulations
│   ├── slow-api/
│   ├── memory-leak/
│   └── cascade-failure/
├── final-boss/              # Ultimate challenge
│   └── production-apocalypse/
├── scripts/
│   ├── start-quest.sh
│   ├── check-readiness.sh
│   ├── submit-score.sh
│   └── generate-certificate.sh
└── docker-compose.yml       # Infrastructure for challenges
```

---

## 🏆 Scoring & Certification

### Tier System

| Tier | Score Range | Badge | What It Means |
|------|-------------|-------|---------------|
| 🥉 Bronze | 550-699 | Observability Apprentice | Ready for Week 2 with support |
| 🥈 Silver | 700-849 | Monitoring Master | Solid foundation for Week 2 |
| 🥇 Gold | 850-999 | AIOps Engineer | Strong Week 2 preparation |
| 💎 Platinum | 1000+ | Week 1 Champion | Will excel in Week 2 |

###Assessment Certificate

Upon completion, you'll receive:
- Digital certificate (PDF)
- GitHub profile badge
- Leaderboard entry
- Personalized Week 2 readiness report

```bash
# Generate your certificate
./generate-certificate.sh --score YOUR_SCORE --name "Your Name"
```

---

## 📈 Week 2 Readiness

### Based on Your Score

**< 700 points:**
- ⚠️ Recommend reviewing weak areas before Week 2
- Focus on: PromQL, OTel instrumentation, incident response
- Estimated prep time: 2-3 extra days

**700-849 points:**
- ✅ Ready for Week 2
- Bookmark Week 1 materials for reference
- Review specific topics where you scored < 70%

**850+ points:**
- 🌟 Excellent preparation for Week 2
- Consider helping peers in GitHub Discussions
- Challenge yourself with bonus content in Week 2

---

## 🎁 Bonus Opportunities

Earn extra points by:
- Creating custom Prometheus exporter (+35 pts)
- Building beautiful Grafana dashboard (+20 pts)
- Vendor selection presentation (+25 pts)
- Creating observability memes (+20 pts)

See [AIOPS-QUEST.md](AIOPS-QUEST.md) for details.

---

## 🤝 Collaboration Policy

**Allowed:**
- Using Week 1 materials and notes
- Searching official documentation
- Asking clarifying questions in GitHub Discussions

**Not Allowed:**
- Copying answers from others
- Using ChatGPT/AI to solve lab challenges
- Sharing quiz answers before others complete

**Remember:** The goal is to identify YOUR gaps, not to get a perfect score dishonestly.

---

## ⏱️ Time Commitment

**Recommended Schedule:**

- **Mode 1 (Knowledge):** 30-45 minutes
- **Mode 2 (Labs):** 90-120 minutes
- **Mode 3 (Incidents):** 60-90 minutes
- **Mode 4 (Boss):** 45-60 minutes

**Total:** 3.5-5 hours

**Tip:** You don't have to complete all modes in one sitting. Your progress is saved!

---

## 📊 Leaderboard

View the global leaderboard:
```bash
./leaderboard.sh --week 1
```

Or online: [https://aiops-bootcamp.dev/leaderboard/week1](https://aiops-bootcamp.dev/leaderboard/week1)

---

## 💬 Support

**Stuck on a challenge?**
- Check the hints system (each hint costs -5 points)
- Ask in GitHub Discussions (won't affect score)
- Review corresponding day's materials

**Technical Issues?**
- Check `docker ps` - all containers running?
- Review logs: `docker-compose logs`
- File an issue with `[ASSESSMENT]` tag

---

## 🎯 Final Tips

1. **Read carefully** - Many mistakes come from misreading requirements
2. **Manage your time** - Don't get stuck on one challenge
3. **Use your notes** - This isn't a closed-book exam
4. **Take breaks** - Especially before Final Boss
5. **Have fun!** - It's designed to be engaging, not stressful

---

## 🚀 Ready to Begin?

```bash
cd week-01-fundamentals/final-assessment
./start-quest.sh
```

**Good luck, adventurer!** ⚔️

---

**Next Steps:**
- [View Complete Quest Guide](AIOPS-QUEST.md)
- [Week 2: Data Engineering](../../week-02-data-engineering/README.md)
- [Submit Feedback](https://github.com/your-repo/issues/new?template=assessment-feedback.md)

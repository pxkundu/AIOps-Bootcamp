# Week 5 Day 4 Resources: Reinforcement Learning for Control

> "The best way to predict the future is to create it." - Peter Drucker (or an RL Agent).

---

## 📚 Essential Reading

### The Theory
- **[Spinning Up by OpenAI](https://spinningup.openai.com/en/latest/)** - The best intro to Deep RL (DQN, PPO).
- **[Google: Borg Autopilot](https://research.google/pubs/pub49174/)** - How Google uses ML to vertically scale containers.

### Comparisons
- **[PID vs RL for Autoscaling](https://towardsdatascience.com/reinforcement-learning-vs-pid-control-for-autoscaling-7a7d4a6a5a5e)** - When to use simple Control Theory vs complex AI.
- **[SimPy Documentation](https://simpy.readthedocs.io/en/latest/)** - Discrete Event Simulation (DES) library for Python. Build realistic cloud models before training Agent.

---

## 🛠️ Tools & Libraries

- **[Gymnasium (formerly OpenAI Gym)](https://gymnasium.farama.org/)** - Standard API for RL environments (`env.step()`, `env.reset()`).
- **[Ray Rllib](https://docs.ray.io/en/latest/rllib/index.html)** - Scalable RL library for production (distributed training).
- **[Stable Baselines3](https://stable-baselines3.readthedocs.io/en/master/)** - High-quality implementations of RL algorithms in PyTorch.

---

## 💡 Pro Tips for SREs

1.  **Start with PID:**
    - Before using RL, try a PID Controller (Proportional-Integral-Derivative).
    - It's simpler, explainable, and works for 90% of scaling problems.
    - Use RL only when the system is non-linear (e.g., complex microservice dependencies).

2.  **Simulation is Key:**
    - You cannot train RL in Prod. You will bankrupt the company.
    - Invest heavily in a "Digital Twin" simulator (SimPy + Historical Traces).
    - Train Agent on Simulator -> Deploy Frozen Policy to Prod.

3.  **Reward Shaping:**
    - Be careful! If you reward "Low CPU", the agent will turn off all servers (Queue explodes).
    - If you reward "Zero Queue", the agent launched 1000 servers (Cost explodes).
    - Balance is everything. (`Reward = Revenue - Cost`).

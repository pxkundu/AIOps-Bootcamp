# Project: The Resilient Restarter

Build a remediation controller that handles "Stubborn Services" without entering an infinite loop.

---

## 🎯 Tasks

1. **State Management**: Modify your remediator to track how many times it has attempted to fix a specific service.
2. **Circuit Breaker**: Implement logic that stops all remediation attempts for a service after 3 consecutive failures.
3. **Escalation**: When the circuit breaker trips, instead of running a fix, generate a "P0 - MANUAL INTERVENTION REQUIRED" log entry.
4. **Verification**: After a "Restart" command, wait for 2 seconds and check if the service is "up".

## 🏃 Running the Simulation

1. **`src/service_simulator.json`**: This file represents the "current state" of our services.
2. **`src/smart_controller.py`**: Your main code.
3. **Execution**:
   ```bash
   python3 smart_controller.py
   ```

## 📂 File Structure
- `src/smart_controller.py`: The logic.
- `src/service_simulator.json`: The "World" state.

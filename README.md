# GenLayer AI x Web3 Hackathon: Prediction Market with AI Judge

## Overview

Two **Intelligent Contracts** showcasing GenLayer's unique capabilities:
- **Market 1 (Score):** Objective resolution via TheSportsDB API (oracle-less internet access)
- **Market 2 (MVP):** Subjective AI-judged market (AI integration for ground truth)

## Quick Start

### 1. Run Backend Tests
```bash
python3 test_both_contracts.py
```

### 2. Run Frontend dApp
```bash
python -m http.server 3000
```
Visit: `http://localhost:3000`

### 3. Run Comprehensive Tests
```bash
python3 test_frontend_scenarios.py
```

## Tech Stack

- **Backend:** Python (Intelligent Contracts)
- **Frontend:** HTML/CSS/JavaScript (Interactive dApp)
- **APIs:** TheSportsDB (real data)
- **AI:** GenLayer AI Model (simulated)

## How Contracts Work

### Market 1: Score-Based (TheSportsDB API)
1. Users bet on home/away/draw
2. Contract calls TheSportsDB API for final score
3. Winner determined by score
4. Payouts: (user_bet / winners_pool) × total_pot

### Market 2: MVP Market (AI Judge)
1. Users bet on player names
2. Contract simulates fetching match articles
3. AI analyzes and picks MVP from actual bet players
4. Payouts: (user_bet / winners_pool) × total_pot

## File Structure

```
contract.py                    # 2 Intelligent Contracts (340 lines)
index.html                     # Interactive dApp (508 lines)
test_contract.py              # Unit tests
test_both_contracts.py        # Full integration demo
test_frontend_scenarios.py    # 6 scenarios × 100 runs = 600 test cases
README.md                     # This file
```

## What Makes This Stand Out

✅ **TWO market types** - Objective + Subjective (not just one)  
✅ **AI Integration** - Contracts use AI for decision-making  
✅ **Oracle-less** - Direct API calls, no intermediaries  
✅ **Complete Stack** - Backend + Frontend + Tests  
✅ **Real APIs** - TheSportsDB (not fake data)  
✅ **Professional UI** - 4 users, wallets, real-time logs  
✅ **Tested** - 600+ test cases validating payout logic

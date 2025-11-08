# GenLayer AI x Web3 Hackathon Build: AI Prediction Market

**Author:** [Your Name / Team Name]
**Track:** Prediction Markets & P2P Betting

## 1. Project Description

This project demonstrates **two complementary Intelligent Contracts** for GenLayer, showcasing both **objective** and **subjective** bet resolution using GenLayer's unique capabilities:

### Market 1: Objective Score-Based Market
A traditional prediction market that uses **TheSportsDB API** to fetch real match scores and automatically resolve bets. This demonstrates GenLayer's **oracle-less internet access**.

### Market 2: AI Justice Market (MVP Market)
An **advanced prediction market** that uses **AI to judge subjective outcomes**. Instead of just calling an API for numbers, this contract:
1. Fetches **multiple news articles** about the match from Google News API
2. Feeds these articles to a **GenLayer-provided AI Model** (e.g., GPT-4, Llama)
3. Asks the AI: *"Who was the Man of the Match?"*
4. Uses the AI's answer as **ground truth** for payouts

This demonstrates GenLayer's **combined power**: Internet Access + AI Integration.

## 2. Technical Stack

* **Platform:** GenLayer (Intelligent Contracts)
* **Language:** Python
* **External Data Sources:**
  * TheSportsDB API (Score data)
  * Google News API (Match reports - simulated)
  * GenLayer AI Model (MVP analysis - simulated)
* **Frontend:** HTML/CSS/JavaScript (Interactive simulation)

## 3. How It Works

### Market 1: Score-Based Resolution
1. **Deploy:** Create a market for Event ID `441613` (Arsenal vs Chelsea)
2. **Place Bets:** Users bet on 'home', 'away', or 'draw'
3. **Resolve:** Call `resolve_market()` 
4. **API Call:** Contract fetches final score from TheSportsDB
5. **Winner:** Score determines winner ('home'=1st team better, 'draw'=tie, etc.)
6. **Payout:** Winners split the total pot proportionally

### Market 2: AI Judge Resolution (MVP Market)
1. **Deploy:** Create MVP market for the same match
2. **Place Bets:** Users bet on who they think will be MVP (e.g., "Bukayo Saka")
3. **Resolve:** Call `resolve_mvp_market()`
4. **AI Analysis Process:**
   - Fetch 5+ news articles about the match
   - Feed article summaries to GenLayer AI Model
   - AI analyzes and determines MVP
5. **Payout:** Users who bet on the AI-selected MVP split the pot

## 4. File Structure

```
contract.py              # Two Intelligent Contract classes
├── RealPredictionMarketContract      # Objective market (score-based)
└── AIJusticeMarketContract           # Subjective market (AI-judged)

index.html              # Interactive frontend demo with both markets

test_contract.py        # Test for objective market

test_both_contracts.py  # Complete demo showing both markets
```

## 5. How to Test (Professional dApp Simulation)

This project includes a professional frontend simulation (`index.html`) that demonstrates the full dApp flow, including simulated user wallets, balance management, and our two distinct markets working in parallel.

### Quick Start: Interactive dApp

**Step 1: Start the Web Server**
```bash
python -m http.server 3000
```

**Step 2: Open in Browser**
Visit: `http://localhost:3000`

### Full Demo Flow (Copy-Paste Instructions)

**1. Create User Wallets:**
- Select "Alice" from dropdown → Deposit: 1000 → Click "Deposit"
- Select "Charlie" from dropdown → Deposit: 50 → Click "Deposit"  
- Select "David" from dropdown → Deposit: 50 → Click "Deposit"

**2. Place Score Market Bets:**
- Select "Charlie" → Score: Draw → Amount: 20 → Click "Place Score Bet"
- Select "David" → Score: Draw → Amount: 30 → Click "Place Score Bet"

**3. Place MVP Market Bets:**
- Select "Alice" → Player: Bukayo Saka → Amount: 100 → Click "Place MVP Bet"

**4. Resolve Score Market:**
- Click "Resolve Score Market" button
- Wait 2 seconds for API simulation
- Watch the logs show: Score 2-2, Winners (draw): Charlie & David get paid

**5. Resolve MVP Market:**
- Click "Resolve MVP Market (AI)" button
- Wait 3 seconds for AI analysis simulation
- Watch the logs show: AI Judge picks "Bukayo Saka", Alice gets paid

**Expected Results:**
- Charlie: $50 + $160 = $210 (20 out of 50 draw pool, wins $160)
- David: $50 + $240 = $290 (30 out of 50 draw pool, wins $240)
- Alice: $1000 - $100 + $150 = $1050 (bets $100 on winning MVP, gets $150)

### Alternative: Command Line Demo
```bash
python3 test_both_contracts.py
```

This runs both markets with randomized outcomes and shows the backend logic.

### Test Case: Score-Based Market
- **Event ID:** `441613` (Arsenal vs Chelsea)
- **Test Scenario:**
  - Charlie: 20 on 'draw'
  - David: 30 on 'draw'
  - Total draw pool: 50
- **Match Result:** 2-2 (Draw)
- **Winners:** Charlie & David
- **Payouts (split proportionally):**
  - Charlie: (20/50) * 200 total pot = $80 (but only $50 on draw)
  - David: (30/50) * 200 total pot = $120

### Test Case: MVP Market (AI Judge)
- **Event ID:** `441613` (Arsenal vs Chelsea)
- **Test Scenario:**
  - Alice: $100 on 'Bukayo Saka'
  - Bob: $50 on 'Cole Palmer'
  - Total pot: $150
- **AI Decision:** MVP = "Bukayo Saka"
- **Winner:** Alice
- **Payout:** Alice receives all $150 (or proportional if multiple winners)



## 6. Why This Project Stands Out

**Most hackathon projects:**
- Call one API to get one number
- Use that number to resolve bets
- End of story

**This project:**
- Uses **TWO different resolution methods** (objective + subjective)
- Demonstrates **AI integration** (the "AI" in "GenLayer AI x Web3")
- Shows **real-world use case**: Sports markets often need subjective judgment
- Provides **complete dApp experience**: Backend + Frontend + Tests
- Highlights **GenLayer's unique strengths**: Oracle-less data + AI

## 7. Future Enhancements

1. **Real API Integration:**
   - Replace mock data with actual Google News API calls
   - Use real GenLayer AI Model instead of simulated responses

2. **Additional Markets:**
   - First goalscorer (objective)
   - Best defensive performance (AI-judged)
   - Most controversial decision (AI-judged)

3. **DAO Governance:**
   - Community votes to overturn AI decisions
   - Dispute resolution mechanism

4. **Token Economics:**
   - Transaction fees
   - Staking requirements for bettors
   - Reputation scores for AI model accuracy

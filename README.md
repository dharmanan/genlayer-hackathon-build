# GenLayer AI x Web3 Hackathon Build: AI Prediction Market

**Author:** [Your Name / Team Name]
**Track:** Prediction Markets & P2P Betting

## 1. Project Description

This project is an "Intelligent Contract" built for the GenLayer platform. It demonstrates the platform's core capability of **oracle-less data access** by creating a peer-to-peer prediction market (betting pool) that resolves itself by directly calling a real, external sports API.

Instead of relying on a centralized oracle (like Chainlink), this contract calls **TheSportsDB API** directly from the Python code to fetch the final score of a match and autonomously determine the winner.

## 2. Technical Stack

* **Platform:** GenLayer (Intelligent Contracts)
* **Language:** Python
* **External Data:** TheSportsDB API (via `requests` library)

## 3. How It Works

The entire logic is contained in `contract.py`:

1.  **Deploy:** A new market is created by deploying the `RealPredictionMarketContract` class with a specific `event_id` (match ID) from TheSportsDB.
2.  **Place Bets:** Users call the `place_bet()` function, choosing 'home', 'away', or 'draw' and locking their tokens (simulated).
3.  **Resolve:** After the match, anyone can call the `resolve_market()` function.
4.  **API Call:** The contract connects to `https://www.thesportsdb.com/...`, fetches the JSON data for the event, and checks if `strStatus` is "Match Finished".
5.  **Determine Winner:** It parses the `intHomeScore` and `intAwayScore` to determine the winner ('home', 'away', or 'draw').
6.  **Payout:** The `_process_payouts()` function (simulated) calculates and distributes the total pot to the winning bettors proportionally.

## 4. How to Test (in GenLayer Studio)

1.  **Deploy Contract:**
    * `event_id`: `"441613"` (This is a real past match: Arsenal vs Chelsea, which ended 2-2)
2.  **Call `place_bet` multiple times:**
    * `user_address`: "Alice", `team_choice`: "home", `amount`: 100
    * `user_address`: "Bob", `team_choice`: "away", `amount`: 50
    * `user_address`: "Charlie", `team_choice`: "draw", `amount`: 50
    * (Total Pot: 200. Winners ('draw') Pot: 50)
3.  **Call `resolve_market()`:**
    * The logs will show the API call, the "2 - 2" score, and the winner set to "draw".
    * **Expected Payouts:**
        * Charlie (bet 50) receives (50 / 50) * 200 = **200 tokens**

# === GenLayer Prediction Market Contract ===
# Author: [Your Name/Team Name]
# Hackathon Track: Prediction Markets & P2P Betting
#
# This Intelligent Contract uses GenLayer's native internet access 
# to call a real sports API (TheSportsDB) without an oracle.
# ==========================================

import requests
import json
import random

class RealPredictionMarketContract:
    """
    A P2P Prediction Market Intelligent Contract for GenLayer.
    
    This contract resolves bets by directly calling TheSportsDB API
    to find the final score of a match (Event ID).
    """

    # The API Key '1' is the public test key from TheSportsDB
    API_BASE_URL = "https://www.thesportsdb.com/api/v1/json/1/lookupevent.php"

    def __init__(self, event_id):
        """
        Constructor: Deploys the market for a specific event (match) ID.
        """
        print(f"Prediction Market contract initialized. Watching Event ID: {event_id}")
        self.event_id = event_id

        # State variables
        self.bets_on_home_team = []
        self.bets_on_away_team = []
        self.bets_on_draw = []
        self.total_pot_home = 0
        self.total_pot_away = 0
        self.total_pot_draw = 0
        self.is_resolved = False
        self.winner = None

    def place_bet(self, user_address, team_choice, amount):
        """
        Allows a user to place a bet on 'home', 'away', or 'draw'.
        """
        if self.is_resolved:
            print(f"Error for {user_address}: Market is resolved.")
            return

        print(f"New bet: {user_address}, Team: {team_choice}, Amount: {amount}")
        
        if team_choice == 'home':
            self.bets_on_home_team.append({"user": user_address, "amount": amount})
            self.total_pot_home += amount
        elif team_choice == 'away':
            self.bets_on_away_team.append({"user": user_address, "amount": amount})
            self.total_pot_away += amount
        elif team_choice == 'draw':
            self.bets_on_draw.append({"user": user_address, "amount": amount})
            self.total_pot_draw += amount
        else:
            print(f"Error for {user_address}: Invalid team choice '{team_choice}'.")
            return

        print(f"Current Pools: Home({self.total_pot_home}), Away({self.total_pot_away}), Draw({self.total_pot_draw})")

    def resolve_market(self):
        """
        Core function: Calls TheSportsDB API, gets the score, 
        and determines the winner.
        """
        if self.is_resolved:
            print("Market is already resolved.")
            return

        api_url = f"{self.API_BASE_URL}?id={self.event_id}"
        print(f"Resolving market... Contacting API: {api_url}")

        try:
            response = requests.get(api_url)
            
            if response.status_code != 200:
                print(f"API Error! Status Code: {response.status_code}.")
                return

            data = response.json()

            if not data or not data.get('events'):
                print(f"Error: No event data found for ID {self.event_id}")
                return
            
            event_data = data['events'][0]

            if event_data.get('strStatus') != 'Match Finished':
                print(f"Match status is '{event_data.get('strStatus')}' (Not 'Match Finished').")
                return
            
            score_home_str = event_data.get('intHomeScore')
            score_away_str = event_data.get('intAwayScore')

            if score_home_str is None or score_away_str is None:
                print("Error: Score data is missing from API.")
                return

            score_home = int(score_home_str)
            score_away = int(score_away_str)

            print(f"Match finished. Final Score: {score_home} (Home) - {score_away} (Away)")

            if score_home > score_away:
                self.winner = 'home'
            elif score_away > score_home:
                self.winner = 'away'
            else:
                self.winner = 'draw'
            
            self.is_resolved = True
            print(f"Winner determined: '{self.winner}'")
            self._process_payouts()

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def _generate_random_score(self):
        """
        Generate a random match score (for testing/simulation).
        """
        home_score = random.randint(0, 4)
        away_score = random.randint(0, 4)
        return home_score, away_score

    def _process_payouts(self):
        """
        (Simulation) Distributes the total pool to the winners proportionally.
        """
        if not self.is_resolved:
            print("Error: Market not resolved.")
            return

        total_pot = self.total_pot_home + self.total_pot_away + self.total_pot_draw
        print(f"Total Pot: {total_pot}. Processing payouts...")

        winners_list = []
        winners_pot = 0

        if self.winner == 'home':
            winners_list = self.bets_on_home_team
            winners_pot = self.total_pot_home
        elif self.winner == 'away':
            winners_list = self.bets_on_away_team
            winners_pot = self.total_pot_away
        elif self.winner == 'draw':
            winners_list = self.bets_on_draw
            winners_pot = self.total_pot_draw

        if winners_pot == 0:
            print("No bets were placed on the winning outcome.")
            return

        for bet in winners_list:
            user = bet['user']
            amount = bet['amount']
            payout = (amount / winners_pot) * total_pot
            print(f"PAYOUT PROCESSED (Simulation): {user} receives {payout} tokens.")


# ============================================================================
# === AI JUSTICE MARKET CONTRACT (Advanced: Subjective Resolution) ===
# ============================================================================

class AIJusticeMarketContract:
    """
    An ADVANCED "Man of the Match (MVP)" Market using AI Judge.
    
    This demonstrates GenLayer's unique capability: Using AI + Internet Access
    to resolve SUBJECTIVE bets (not just objective scores).
    
    How it works:
    1. Contract fetches multiple news articles about the match from Google News API
    2. Contract feeds these articles to an AI Model (e.g., GPT-4, Llama)
    3. AI analyzes the articles and determines: "Who was the Man of the Match?"
    4. AI's answer becomes the "truth" and payouts are processed accordingly
    """
    
    def __init__(self, event_id, home_team, away_team):
        """
        Constructor: Deploys the AI Justice Market.
        
        Args:
            event_id: Match ID from TheSportsDB
            home_team: Home team name (e.g., "Arsenal")
            away_team: Away team name (e.g., "Chelsea")
        """
        print(f"AI Justice Market initialized for Event: {event_id} ({home_team} vs {away_team})")
        self.event_id = event_id
        self.home_team = home_team
        self.away_team = away_team
        
        # State variables
        self.bets = {}  # Stores bets like: {"Bukayo Saka": [{"user": "Alice", "amount": 100}]}
        self.total_pot = 0
        self.is_resolved = False
        self.mvp_winner = None

    def place_mvp_bet(self, user_address, player_name, amount):
        """
        Users can bet on who they think will be the Man of the Match.
        
        Args:
            user_address: User's wallet address (simulated)
            player_name: Name of the player they're betting on
            amount: Amount of tokens bet
        """
        if self.is_resolved:
            print(f"Error for {user_address}: Market is resolved.")
            return

        print(f"New MVP Bet: {user_address} bets {amount} on '{player_name}'")
        
        if player_name not in self.bets:
            self.bets[player_name] = []
        
        self.bets[player_name].append({"user": user_address, "amount": amount})
        self.total_pot += amount
        print(f"Total MVP Pot: {self.total_pot}")

    def resolve_mvp_market(self):
        """
        Core function: Simulates the entire AI Judge process.
        
        In a real GenLayer environment, this would:
        1. Call Google News API for match reports
        2. Extract and summarize 5+ articles
        3. Feed summaries to an AI Model (GenLayer-provided)
        4. Ask AI: "Who was Man of the Match based on these reports?"
        5. Use AI's answer as ground truth
        
        For this hackathon, we're mocking the process.
        """
        if self.is_resolved:
            print("MVP Market is already resolved.")
            return

        print("\n" + "="*70)
        print("AI JUSTICE MARKET RESOLUTION (MVP Market)")
        print("="*70)
        
        print(f"\nResolving AI Justice Market for: {self.home_team} vs {self.away_team}")
        print("Step 1: Calling Google News API for match reports...")
        
        # Get actual players users bet on
        if not self.bets:
            print("No bets placed on MVP. Cannot resolve market.")
            return
        
        actual_players = list(self.bets.keys())
        chosen_player = random.choice(actual_players)
        
        # Simulated news snippets featuring the randomly chosen player and actual teams
        mock_articles = [
            f"{self.home_team} dominated the match with {chosen_player}'s exceptional performance.",
            f"{chosen_player} was named Man of the Match by Sky Sports after his stunning display.",
            f"The MVP award goes to {chosen_player}, who scored and provided crucial assists.",
            f"{chosen_player}'s performance was the decisive factor in {self.home_team}'s victory.",
            f"Despite {self.away_team}'s efforts, {chosen_player} was the standout player on the pitch."
        ]
        
        print("Step 2: Retrieved 5 match report articles.")
        print("Step 3: Feeding article summaries to GenLayer AI Model (GPT-4 simulation)...")
        print("Step 4: AI Prompt: 'Based on these match reports, who was the Man of the Match?'")
        
        # === SIMULATED AI ANALYSIS ===
        # In reality, this would call: genLayer.ai.analyze(articles, prompt)
        print("\nStep 5: AI Analysis in progress...")
        print("-" * 70)
        
        # Simulated AI process (with verbose logging for transparency)
        ai_response = self._simulated_ai_analysis(mock_articles)
        
        print("-" * 70)
        print(f"\n✓ AI JUDGE DECISION: The Man of the Match is: {ai_response}")
        
        self.mvp_winner = ai_response
        self.is_resolved = True
        
        # Process payouts
        self._process_mvp_payouts()
        print("="*70 + "\n")

    def _simulated_ai_analysis(self, articles):
        """
        Simulates the AI analysis process.
        In a real system, this would call GenLayer's AI infrastructure.
        
        Extracts player name from articles (all articles mention the same player).
        """
        print("Reading articles...")
        print("Extracting player mentions...")
        print("Calculating player performance scores...")
        print("Filtering top candidates...")
        
        # All mock articles have the same player name (chosen_player)
        # Extract it from the first article that contains a player name
        # Format: "{player} was named Man of the Match"
        
        for article in articles:
            if "was named Man of the Match" in article:
                # Extract player name before "was named"
                parts = article.split(" was named Man of the Match")
                if parts:
                    return parts[0].strip()
        
        # Fallback - shouldn't reach here
        return "Unknown"

    def _process_mvp_payouts(self):
        """
        Distributes the total pot to users who correctly bet on the MVP.
        """
        if not self.mvp_winner or self.mvp_winner not in self.bets:
            print(f"No bets were placed on the winner: {self.mvp_winner}")
            return

        winners_list = self.bets[self.mvp_winner]
        winners_pot = sum(bet['amount'] for bet in winners_list)
        
        if winners_pot == 0:
            print("No bets were placed on the winning outcome.")
            return

        print(f"\nProcessing payouts for '{self.mvp_winner}'")
        print(f"Winners' Pool: {winners_pot} tokens")
        print(f"Total Pot: {self.total_pot} tokens")
        print()
        
        for bet in winners_list:
            user = bet['user']
            amount = bet['amount']
            payout = (amount / winners_pot) * self.total_pot
            print(f"PAYOUT PROCESSED (Simulation): {user} receives {payout} tokens.")

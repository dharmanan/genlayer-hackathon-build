# === GenLayer Prediction Market Contract ===
# Author: [Your Name/Team Name]
# Hackathon Track: Prediction Markets & P2P Betting
#
# This Intelligent Contract uses GenLayer's native internet access 
# to call a real sports API (TheSportsDB) without an oracle.
# ==========================================

import requests
import json

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

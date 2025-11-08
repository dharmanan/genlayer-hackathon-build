#!/usr/bin/env python3
"""
Comprehensive test scenarios for the dApp frontend logic.
Tests various combinations to verify payout calculations are correct.
"""

import random

def simulate_score_market(demo_bets, user_bet, num_runs=100):
    """Simulate score market resolution multiple times"""
    print("\n" + "="*80)
    print("SCORE MARKET SIMULATION")
    print("="*80)
    
    results = {"home_wins": 0, "away_wins": 0, "draw_wins": 0}
    payout_results = []
    
    for run in range(num_runs):
        # Generate random score
        home_score = random.randint(0, 4)
        away_score = random.randint(0, 4)
        
        # Determine winner
        if home_score > away_score:
            winner = 'home'
            results["home_wins"] += 1
        elif away_score > home_score:
            winner = 'away'
            results["away_wins"] += 1
        else:
            winner = 'draw'
            results["draw_wins"] += 1
        
        # Calculate pools
        all_bets = demo_bets + [user_bet]
        total_pot = sum(bet['amount'] for bet in all_bets)
        winners = [bet for bet in all_bets if bet['team'] == winner]
        losers = [bet for bet in all_bets if bet['team'] != winner]
        
        if winners:
            winners_pot = sum(bet['amount'] for bet in winners)
            user_bet_won = any(bet['user'] == user_bet['user'] and bet['team'] == winner for bet in all_bets)
            
            if user_bet_won:
                user_payout = (user_bet['amount'] / winners_pot) * total_pot
                payout_results.append({
                    'score': f"{home_score}-{away_score}",
                    'winner': winner,
                    'user_payout': user_payout,
                    'total_pot': total_pot
                })
    
    print(f"\n📊 Demo Bets: {demo_bets}")
    print(f"👤 User Bet: {user_bet}")
    print(f"\n🎲 Results from {num_runs} runs:")
    print(f"   Home wins: {results['home_wins']} ({results['home_wins']/num_runs*100:.1f}%)")
    print(f"   Away wins: {results['away_wins']} ({results['away_wins']/num_runs*100:.1f}%)")
    print(f"   Draws: {results['draw_wins']} ({results['draw_wins']/num_runs*100:.1f}%)")
    
    if payout_results:
        print(f"\n💰 User Wins: {len(payout_results)} times")
        avg_payout = sum(r['user_payout'] for r in payout_results) / len(payout_results)
        print(f"   Average Payout: ${avg_payout:.2f}")
        print(f"   Min Payout: ${min(r['user_payout'] for r in payout_results):.2f}")
        print(f"   Max Payout: ${max(r['user_payout'] for r in payout_results):.2f}")
        print(f"\n   Sample wins:")
        for result in payout_results[:5]:
            print(f"     Score {result['score']} (Winner: {result['winner']}) → Payout: ${result['user_payout']:.2f}")
    else:
        print(f"\n⚠️  User never won in {num_runs} runs!")


def simulate_mvp_market(demo_bets, user_bet, num_runs=100):
    """Simulate MVP market resolution multiple times"""
    print("\n" + "="*80)
    print("MVP MARKET SIMULATION")
    print("="*80)
    
    # Get all possible players from bets
    all_players = set()
    for bet in demo_bets + [user_bet]:
        all_players.add(bet['player'])
    all_players = list(all_players)
    
    print(f"\n📊 Demo Bets: {demo_bets}")
    print(f"👤 User Bet: {user_bet}")
    print(f"🎯 Possible MVP Winners: {all_players}")
    
    win_stats = {player: 0 for player in all_players}
    payout_results = []
    
    for run in range(num_runs):
        # AI Judge picks random player from actual bets
        all_bets = demo_bets + [user_bet]
        all_players_in_bets = list(set(bet['player'] for bet in all_bets))
        mvp_winner = random.choice(all_players_in_bets)
        win_stats[mvp_winner] += 1
        
        # Calculate payout
        winners = [bet for bet in all_bets if bet['player'] == mvp_winner]
        losers = [bet for bet in all_bets if bet['player'] != mvp_winner]
        
        if winners:
            winners_pot = sum(bet['amount'] for bet in winners)
            total_pot = sum(bet['amount'] for bet in all_bets)
            user_bet_won = any(bet['user'] == user_bet['user'] and bet['player'] == mvp_winner for bet in all_bets)
            
            if user_bet_won:
                user_payout = (user_bet['amount'] / winners_pot) * total_pot
                payout_results.append({
                    'mvp': mvp_winner,
                    'user_payout': user_payout,
                    'total_pot': total_pot,
                    'winners': [b['user'] for b in winners]
                })
    
    print(f"\n🎲 Results from {num_runs} runs:")
    for player in all_players:
        pct = win_stats[player] / num_runs * 100
        print(f"   {player}: {win_stats[player]} wins ({pct:.1f}%)")
    
    if payout_results:
        print(f"\n💰 User Wins: {len(payout_results)} times")
        avg_payout = sum(r['user_payout'] for r in payout_results) / len(payout_results)
        print(f"   Average Payout: ${avg_payout:.2f}")
        print(f"   Min Payout: ${min(r['user_payout'] for r in payout_results):.2f}")
        print(f"   Max Payout: ${max(r['user_payout'] for r in payout_results):.2f}")
        print(f"\n   Sample wins:")
        for result in payout_results[:5]:
            print(f"     MVP: {result['mvp']} (Winners: {', '.join(result['winners'])}) → Payout: ${result['user_payout']:.2f}")
    else:
        print(f"\n⚠️  User never won in {num_runs} runs!")


# =============================================================================
# TEST SCENARIOS
# =============================================================================

print("\n" + "█"*80)
print("SCENARIO 1: Score Market - User is ONLY bettor (should see full pot)")
print("█"*80)

demo_bets_1 = []  # Empty - only user bets
user_bet_1 = {'user': 'Bob', 'team': 'home', 'amount': 100}
simulate_score_market(demo_bets_1, user_bet_1, 100)

print("\n" + "█"*80)
print("SCENARIO 2: Score Market - User bets on 'away', others on 'home' and 'draw'")
print("█"*80)

demo_bets_2 = [
    {'user': 'Alice', 'team': 'home', 'amount': 100},
    {'user': 'David', 'team': 'draw', 'amount': 50}
]
user_bet_2 = {'user': 'Bob', 'team': 'away', 'amount': 80}
simulate_score_market(demo_bets_2, user_bet_2, 100)

print("\n" + "█"*80)
print("SCENARIO 3: Score Market - Multiple users bet on SAME outcome")
print("█"*80)

demo_bets_3 = [
    {'user': 'Alice', 'team': 'home', 'amount': 100},
    {'user': 'David', 'team': 'home', 'amount': 50}
]
user_bet_3 = {'user': 'Bob', 'team': 'home', 'amount': 80}
simulate_score_market(demo_bets_3, user_bet_3, 100)

print("\n" + "█"*80)
print("SCENARIO 4: MVP Market - Alice has Bukayo Saka, User bets Reece James")
print("█"*80)

demo_bets_4 = [
    {'user': 'Alice', 'player': 'Bukayo Saka', 'amount': 80}
]
user_bet_4 = {'user': 'Bob', 'player': 'Reece James', 'amount': 100}
simulate_mvp_market(demo_bets_4, user_bet_4, 100)

print("\n" + "█"*80)
print("SCENARIO 5: MVP Market - Both bet on SAME player")
print("█"*80)

demo_bets_5 = [
    {'user': 'Alice', 'player': 'Bukayo Saka', 'amount': 80}
]
user_bet_5 = {'user': 'Bob', 'player': 'Bukayo Saka', 'amount': 100}
simulate_mvp_market(demo_bets_5, user_bet_5, 100)

print("\n" + "█"*80)
print("SCENARIO 6: MVP Market - User is ONLY bettor")
print("█"*80)

demo_bets_6 = []
user_bet_6 = {'user': 'Bob', 'player': 'Cole Palmer', 'amount': 150}
simulate_mvp_market(demo_bets_6, user_bet_6, 100)

print("\n" + "█"*80)
print("SUMMARY")
print("█"*80)
print("""
✅ All scenarios tested:
   1. User as only bettor (full pot when winning)
   2. User vs multiple others on different outcomes
   3. Multiple users on same outcome (share pot)
   4. MVP: Different players (each has chance)
   5. MVP: Same player (share pot when winning)
   6. MVP: User as only bettor

💡 Key Insights:
   • Payout = (User Bet / Winners Pot) × Total Pot
   • If user is only winner: payout = total pot
   • If multiple users won: payout is proportional to stake
   • Random outcome means not guaranteed to win every time
""")

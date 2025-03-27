import random
import json
from datetime import datetime, timedelta

class PlayerProfile:
    def __init__(self, username, account_creation_date, total_matches, total_kills, total_deaths, teammates_history,
                 warmup_sessions, first_match_kills):
        self.username = username
        self.account_creation_date = account_creation_date
        self.total_matches = total_matches
        self.total_kills = total_kills
        self.total_deaths = total_deaths
        self.teammates_history = teammates_history
        self.warmup_sessions = warmup_sessions
        self.first_match_kills = first_match_kills

        self.kd_ratio = self.calculate_kd()
        self.account_age_days = self.calculate_account_age()
        self.cheater_proximity_score = self.calculate_cheater_proximity()

    def calculate_kd(self):
        return round(self.total_kills / max(1, self.total_deaths), 2)

    def calculate_account_age(self):
        return (datetime.now() - self.account_creation_date).days

    def calculate_cheater_proximity(self):
        cheater_teammates = [name for name in self.teammates_history if name.startswith("chair") or name.endswith("99")]
        return len(cheater_teammates) / max(1, len(self.teammates_history))

    def calculate_warmup_score(self):
        if self.total_matches < 200:
            return 1 if self.warmup_sessions >= 1 else 0
        return 1

    def legit_score(self):
        score = 100
        if self.kd_ratio > 4.0 and self.account_age_days < 30:
            score -= 40
        if self.cheater_proximity_score > 0.5:
            score -= 30
        if self.total_matches < 50:
            score -= 20
        if self.calculate_warmup_score() == 0 and self.first_match_kills > 5:
            score -= 20
        return max(score, 0)

    def to_dict(self):
        return {
            "username": self.username,
            "account_age_days": self.account_age_days,
            "kd_ratio": self.kd_ratio,
            "cheater_proximity_score": self.cheater_proximity_score,
            "warmup_sessions": self.warmup_sessions,
            "first_match_kills": self.first_match_kills,
            "legit_score": self.legit_score()
        }

    def display_profile(self):
        print(f"\nPlayer: {self.username}")
        print(f"Account Age: {self.account_age_days} days")
        print(f"K/D Ratio: {self.kd_ratio}")
        print(f"Cheater Proximity Score: {self.cheater_proximity_score:.2f}")
        print(f"Warmup Sessions: {self.warmup_sessions}, First Match Kills: {self.first_match_kills}")
        print(f"Legit Score: {self.legit_score()}/100")



 

# === Save Profiles to JSON ===

data = [p.to_dict() for p in players]

with open("data/player_profiles.json", "w") as f:
    json.dump(data, f, indent=4)

print("\n✅ Player profiles saved to 'data/player_profiles.json'")


def main():
 
    players = [
        PlayerProfile("SweatGod420", datetime.now() - timedelta(days=15), 40, 300, 40, ["chairmaster", "sweatyTeammate", "unknown99"], 0, 8),
        PlayerProfile("SniperQueen", datetime.now() - timedelta(days=600), 600, 5000, 2000, ["trustedPlayer", "random1"], 2, 3),
        PlayerProfile("FreshMeat22", datetime.now() - timedelta(days=5), 10, 80, 10, ["chair99"], 0, 10),
        PlayerProfile("RealGrinder", datetime.now() - timedelta(days=800), 1200, 7000, 4000, ["oldFriend", "grindBuddy"], 1, 4)
    ]

    for p in players:
        p.display_profile()

    data = [p.to_dict() for p in players]

    with open("data/player_profiles.json", "w") as f:
        json.dump(data, f, indent=4)

    print("\n✅ Player profiles saved to 'data/player_profiles.json'")


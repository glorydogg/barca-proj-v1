import requests 
import pandas as pd 
import matplotlib.pyplot as plt 

url = "https://api.football-data.org/v4/teams/81/matches?competitions=PD&season=2025" 
headers = { "X-Auth-Token" : "34a6dc3a60754ef88dabba5bb2319e89" }

response = requests.get(url, headers= headers) 
print("Status code:", response.status_code) 

data = response.json()

matches = [] 
for match in data["matches"]:
    if match["status"] == "FINISHED": 
        matches.append({ 
        "date": match["utcDate"][:10], 
        "home": match["homeTeam"]["name"], 
        "away": match["awayTeam"]["name"], 
        "home_goals": match["score"]["fullTime"]["home"], 
        "away_goals": match["score"]["fullTime"]["away"] }) 
df = pd.DataFrame(matches)

results = [] 
for _, row in df.iterrows(): 
    if row["home"] == "FC Barcelona": 
        if row["home_goals"] > row["away_goals"]:
            results.append("W") 
        elif row["home_goals"] == row["away_goals"]: 
            results.append("D")
        else: 
            results.append("L")

    else: # Barcelona played away 
        if row["away_goals"] > row["home_goals"]:
             results.append("W") 
        elif row["away_goals"] == row["home_goals"]: 
            results.append("D") 
        else: results.append("L")
df["result"] = results


df["points"] = df["result"].map({"W": 3, "D": 1, "L": 0}) 
df["cumulative_points"] = df["points"].cumsum() 

print(df)

plt.figure(figsize=(10,5))
plt.plot(df["date"], df["cumulative_points"], marker="o") 
plt.title("FC Barcelona - Cumulative Points (La Liga 2025/26)") 
plt.xlabel("Date") 
plt.ylabel("Points") 
plt.xticks(rotation=45) # rotate dates so they don’t overlap 
plt.grid(True) 
plt.show() 
df.to_csv("barca_matches.csv", index=False) 
plt.savefig("barca_points.png")
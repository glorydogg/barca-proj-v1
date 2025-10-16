import requests 
import pandas as pd 
import matplotlib.pyplot as plt 
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 0)

url = "https://api.football-data.org/v4/teams/81/matches?competitions=PD&season=2025" 
headers = { "X-Auth-Token" : "34a6dc3a60754ef88dabba5bb2319e89" }

response = requests.get(url, headers= headers) 

data = response.json()

matches = [] 
for match in data["matches"]:
    if match["status"] == "FINISHED": 
        if match["homeTeam"]["name"] == "FC Barcelona":
            venue = "Home"
        else:
            venue = "Away"

        matches.append({ 
        "date": match["utcDate"][:10], 
        "home": match["homeTeam"]["name"], 
        "away": match["awayTeam"]["name"], 
        "home_goals": match["score"]["fullTime"]["home"],   
        "away_goals": match["score"]["fullTime"]["away"],
        "venue": venue 
        }) 

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

goal_difference = []
for _, row in df.iterrows():
    if row["venue"] == "Home":
        difference_value = row["home_goals"] - row["away_goals"]
        goal_difference.append(difference_value)
    else:
        difference_value = row["away_goals"] - row["home_goals"]
        goal_difference.append(difference_value)
df["goal_difference"] = goal_difference



venue_summary = df.groupby("venue")[["home_goals", "away_goals", "points", "goal_difference"]].mean()
venue_summary = venue_summary.round(2)

df["form_trend"] = df["points"].rolling(5).mean()
df["form_trend"] = df["form_trend"].round(2)


print(df)
print(venue_summary)


plt.figure(figsize=(10,5))
plt.plot(df["date"], df["cumulative_points"], marker="o") 
plt.title("FC Barcelona - Cumulative Points (La Liga 2025/26)") 
plt.xlabel("Date") 
plt.ylabel("Points") 
plt.xticks(rotation=45) # rotate dates so they don't overlap 
plt.grid(True) 
plt.show() 
df.to_csv("data/barca_matches.csv", index=False) 
plt.savefig("plots/barca_points.png")
plt.close()

plt.figure()
venue_summary.plot(kind="bar")
plt.title("FC Barcelona - Home vs Away Performance (La Liga 2025/2026)")
plt.xlabel("venue")
plt.ylabel("Average Values")
for container in plt.gca().containers:
    plt.bar_label(container, fmt='%.2f', label_type='edge', padding=3)
plt.ylim(0, venue_summary["points"].max() + 1)
plt.tight_layout()
plt.savefig("plots/home_vs_away.png")
plt.show()

plt.figure()
plt.plot(df["date"], df["form_trend"], marker= "o")
plt.title("FC Barcelona 5-Match Rolling Average (Form Trend)")
plt.xlabel("Date")
plt.ylabel("Average points (5-Match Rolling Form)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.2f}"))
plt.savefig("plots/form_trend.png")
plt.show()

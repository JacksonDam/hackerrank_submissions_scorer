import json

mods = []
block_list = []

def main():
    teams = {}
    users = {}
    team_scores = []
    ty = set()
    grr = set()
    huh = set()

    with open("formdata.csv", "r") as csvfile:
        csvfile.readline()
        line = csvfile.readline()
        while line:
            details = line.split(",")
            team = details[1]
            teams[team] = {}
            teams[team]["user_data"] = {}
            teams[team]["challenges"] = {}
            for person in details[2:]:
                person = person.strip()
                if person:
                    assert person not in users
                    teams[team]["user_data"][person] = {}
                    users[person] = team
            line = csvfile.readline()

    print(users)

    submissions = json.load(open("judge_submissions.json", "r"))["models"]
    for submission in submissions:
        challenge = submission["challenge"]["slug"]
        score = submission["score"]
        user = submission["hacker_username"]
        if user not in users:
            if user in mods:
                ty.add("mod: " + user)
            elif user in block_list:
                grr.add("BAN: " + user)
            else:
                huh.add("Missing: " + user)
        else:
            team_name = users[user]
            if challenge not in teams[team_name]["user_data"][user]:
                teams[team_name]["user_data"][user][challenge] = score
            else:
                teams[team_name]["user_data"][user][challenge] = max(teams[team_name]["user_data"][user][challenge], score)
            if challenge not in teams[team_name]["challenges"]:
                teams[team_name]["challenges"][challenge] = score
            else:
                teams[team_name]["challenges"][challenge] = max(teams[team_name]["challenges"][challenge], score)

    print(teams)
    print(ty)
    print(grr)
    print(huh)

    for team in teams:
        team_score = 0
        for challenge in teams[team]["challenges"]:
            team_score += teams[team]["challenges"][challenge]
        team_scores.append((team, round(team_score, 2)))

    team_scores.sort(key=lambda x: x[0], reverse=False)

    for team in team_scores:
        print(team)

main()
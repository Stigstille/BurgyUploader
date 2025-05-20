import requests, time

url="DISCORDWEBHOOKURL" # NEVER PUBLISH THIS!!!!

def findBurgy(divLine, cell, wks, burgyNames, data):
    burgyNames = burgyNames[0]
    for burgy in burgyNames:
        burgy = [burgy.label, burgy.value]
        if burgy[1] == divLine[1]:
            sillyColumn = burgy[0].split('2')[0]
            sillyRow = cell[0].split('A')[1]
            origVal = get_value_offline(data, sillyRow, sillyColumn)
            if origVal != "":
                origVal = int(origVal)
                print(f"Original Value: {origVal}")
                wks.update_value(f'{sillyColumn}{sillyRow}', str(origVal + 1))
                return origVal + 1
            else:
                print(f"New Burgy!!")
                wks.update_value(f'{sillyColumn}{sillyRow}', str(1))
                return "their first"
    return "It broke :3"

def get_value_offline(data, row, col_letter):
    col = col_letter_to_index(col_letter)
    try:
        return data[int(row) - 1][col - 1]
    except IndexError:
        return None

def col_letter_to_index(col_letter):
    col_letter = col_letter.upper()
    index = 0
    for char in col_letter:
        index = index * 26 + (ord(char) - ord('A') + 1)
    return index


import time

def post_to_discord(payload, retries=3):
    for attempt in range(retries):
        resp = requests.post(url, json=payload)
        if resp.status_code == 429:
            retry_after = resp.json().get("retry_after", 1)
            print(f"[RATE LIMITED] Sleeping for {retry_after} seconds...")
            time.sleep(retry_after)
        else:
            return resp
    print("[ERROR] Discord request failed after retries.")
    return None

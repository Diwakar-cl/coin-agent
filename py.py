def coin_collected(current_coin):

    if current_coin >= goal:
        print("Goal already reached. enter reset or quit.")
        return current_coin


    current_coin += 1
    print("Coin has been collected: ", current_coin)

    if current_coin == goal:
        print("Goal reached. you can keep playing just enter reset.")
    return current_coin

def show_total(current_coin):
    print("Current total: ", current_coin)
    return current_coin

def remaining_coin(current_coin):
    remain_coin = goal - current_coin
    print(f"You've {remain_coin} to collect")
    return current_coin

def clear_record(current_coin):
    print(f"Resetting the current count {current_coin}")
    return 0

tools = {
    "coin collected": coin_collected,
    "total coin collected": show_total,
    "remaining coin": remaining_coin,
    "clear count": clear_record
}

def choose_tool(request):
    text = request

    if "reset" in text or "clear" in text:
        return "clear count"
    elif "remain" in text or "left" in text:
        return "remaining coin"
    elif "total" in text or "collected" in text:
        return "total coin collected"
    elif "collect" in text:
        return "coin collected"
  
    else:
        return None



goal = 5
coin = 0

while True:
    request = input("Enter your tool, or quit: ").strip().lower()
    if request in {"quit", "exit"}:
        print("Current coin collected:", coin)
        break
    chosen_tool = choose_tool(request)


    if chosen_tool in tools:
        coin = tools[chosen_tool](coin)
    else:
        print("NO such tool found.")
        continue


def coin_collected(current_coin):
    current_coin += 1
    print("Coin has been collected: ", current_coin)
    return current_coin

def show_total(current_coin):
    print("Current total: ", current_coin)
    return current_coin

def remaining_coin(current_coin):
    remain_coin = goal - current_coin
    print(f"You've {remain_coin} to collect")
    return current_coin
    


tools = {
    "coin collected": coin_collected,
    "total coin collected": show_total,
    "remaining coin": remaining_coin
}
goal = 5
coin = 0

while coin < goal:
    chosen_tool = input("Enter your tool: ")

    if chosen_tool in tools:
        coin = tools[chosen_tool](coin)
    else:
        print("NO such tool found.")
        break

if coin == goal:
    print("Coin collected")
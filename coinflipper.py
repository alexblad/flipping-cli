import random
import time
import sys
import os
import shutil

def clear_screen():
    # Use the ANSI clear code for a faster, cleaner transition than os.system
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def draw_screen(balance, name, p_heads, h_streak, t_streak, last_action, coin_frame=None):
    cols, lines = shutil.get_terminal_size()
    
    # Header Construction
    header_line = "═" * (cols - 1)
    stats = f" BALANCE: ${balance:.2f} | STREAK: {'H'*h_streak if h_streak > 0 else 'T'*t_streak if t_streak > 0 else 'None'} "
    info = f" COIN: {name.upper()} ({int(p_heads*100)}% Heads) "
    
    screen = []
    screen.append(header_line)
    screen.append(info.center(cols - 1))
    screen.append(stats.center(cols - 1))
    screen.append(header_line)
    screen.append("")
    screen.append(last_action.center(cols - 1))
    screen.append("")

    # Giant Coin Logic (8 lines high)
    if coin_frame:
        for row in coin_frame:
            screen.append(row.center(cols - 1))
    else:
        for _ in range(8): screen.append("")

    # Fill bottom space
    used_lines = len(screen) + 2
    for _ in range(max(0, lines - used_lines - 1)):
        screen.append("")
    
    # Return cursor to top-left and overwrite
    sys.stdout.write("\033[H" + "\n".join(screen))
    sys.stdout.flush()

def big_flip_animation(balance, name, p_heads, h_streak, t_streak, result):
    # Giant 8-row Spinning Frames
    frames = [
        [
            "    XXXXXXXX    ", "  XX        XX  ", " XX          XX ", "XX            XX", 
            "XX            XX", " XX          XX ", "  XX        XX  ", "    XXXXXXXX    "
        ],
        [
            "       XX       ", "       XX       ", "       XX       ", "       XX       ", 
            "       XX       ", "       XX       ", "       XX       ", "       XX       "
        ],
        [
            "     XXXXXX     ", "   XX      XX   ", "  XX        XX  ", "  XX        XX  ", 
            "  XX        XX  ", "  XX        XX  ", "   XX      XX   ", "     XXXXXX     "
        ]
    ]
    
    # Large Landing Faces
    h_face = [
        "  XXXXXXXXXXXX  ", " XX          XX ", " XX  XX  XX  XX ", " XX  XXXXXX  XX ", 
        " XX  XX  XX  XX ", " XX  XX  XX  XX ", " XX          XX ", "  XXXXXXXXXXXX  "
    ]
    t_face = [
        "  XXXXXXXXXXXX  ", " XX          XX ", " XX  XXXXXX  XX ", " XX    XX    XX ", 
        " XX    XX    XX ", " XX    XX    XX ", " XX          XX ", "  XXXXXXXXXXXX  "
    ]

    for i in range(15):
        draw_screen(balance, name, p_heads, h_streak, t_streak, "--- FLIPPING ---", frames[i % 3])
        time.sleep(0.03 + (i * 0.005))

    final_art = h_face if result == "Heads" else t_face
    draw_screen(balance, name, p_heads, h_streak, t_streak, f"!! {result.upper()} !!", final_art)
    time.sleep(0.7)

def play_unfair_flips():
    tiers = [
        ("Penny", 0.20, 0.01, 0.00),
        ("Nickel", 0.26, 0.05, 0.50),
        ("Dime", 0.32, 0.10, 2.50),
        ("Quarter", 0.38, 0.25, 10.00),
        ("Half Dollar", 0.44, 0.50, 25.00),
        ("Dollar", 0.50, 1.00, 50.00)
    ]
    
    tier_idx, balance, h_streak, t_streak = 0, 0.0, 0, 0
    last_action = "Ready to Flip?"
    clear_screen()
    
    while h_streak < 10 and t_streak < 10:
        name, p_heads, base_val, _ = tiers[tier_idx]
        if tier_idx + 1 < len(tiers) and balance >= tiers[tier_idx + 1][3]:
            tier_idx += 1
            name, p_heads, base_val, _ = tiers[tier_idx]
            last_action = f"✨ UPGRADED TO {name.upper()} ✨"

        potential = base_val * (2 ** h_streak)
        draw_screen(balance, name, p_heads, h_streak, t_streak, f"{last_action} (Next Win: ${potential:.2f})")
        
        sys.stdout.write("\n >> [ PRESS ENTER TO FLIP ] ")
        sys.stdout.flush()
        input()
        
        result = "Heads" if random.random() < p_heads else "Tails"
        big_flip_animation(balance, name, p_heads, h_streak, t_streak, result)
        
        if result == "Heads":
            win = base_val * (2 ** h_streak)
            balance += win
            h_streak += 1
            t_streak = 0
            last_action = f"Result: HEADS (Streak {h_streak})"
        else:
            t_streak += 1
            h_streak = 0
            last_action = f"Result: TAILS (Loss Streak {t_streak})"

    clear_screen()
    cols, lines = shutil.get_terminal_size()
    final_msg = "🏆 YOU CONQUERED THE ODDS! 🏆" if h_streak == 10 else "💀 DEFEATED BY TAILS 💀"
    print("\n" * (lines // 2 - 2))
    print(final_msg.center(cols))
    print(f"Final Bank: ${balance:.2f}".center(cols))
    print("\n" * (lines // 2))

if __name__ == "__main__":
    try:
        play_unfair_flips()
    except KeyboardInterrupt:
        clear_screen()
        print("Game closed.")
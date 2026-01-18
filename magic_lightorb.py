import random
import time
import pyautogui
import win32gui
import core
import yaml
import login
import functions

# =========================
# CONFIG / CONSTANTS
# =========================
# We alch a full inventory per trip: 26 casts (leaving room for runes/gear).
PER_INVENTORY_CASTS = 26

# Last inventory spot target (centered on 781, 723 with tiny randomness)
LAST_INV_SPOT = ((780, 782), (722, 724))

# For this flow we want full inventories:
SINGLE_SLOT = False
BATCH_MODE  = True

COORDS = {
    # Window size is set to 865x830 in gfindWindow()

    # --- Banker / Bank UI ---
    "banker_center":  ( (425, 430), (370, 390) ),  # center-screen banker (x range, y range)
    "deposit_all":    ( (480, 490), (625, 635) ),  # "deposit inventory" button in bank

    # Which bank slot holds the item to withdraw for alching (adjust to your item)
    "bank_item_slot": ( (175, 190), (120, 130) ),

    # --- Inventory anchor points ---
    # Top-left inventory slot (where first item withdraws by default)
    "inv_top_left":   ( (650, 665), (500, 515) ),

    # Your High Alch spell click area (where you like to keep the cursor)
    # This matches your earlier "fix mouse location" ~x 796-798, y 584-585
    "alch_slot":      ( (795, 805), (583, 592) ),

    # --- Alch/Nature rune check areas (ORDER: left, top, right, bottom) ---
    # These are now stored in the correct LT-RB order for PIL ImageGrab.
    "alch_check_rect": (642, 600, 676, 632),  # was (x1=642, x2=676, y1=600, y2=632)
    "nat_check_rect":  (642, 525, 676, 560),  # was (x1=642, x2=676, y1=525, y2=560)

    "alch_empty_img":  "empty_slot_alch.png",
    "alch_slot_img":   "alch_slot.png",
    "nat_empty_img":   "empty_slot.png",
    "nat_slot_img":    "nat_slot.png",
}

# Optional: full inventory grid if you later want to iterate across all slots (BATCH_MODE use)
INV_GRID = [
    ((650, 665), (500, 515)), ((695, 710), (500, 515)), ((740, 755), (500, 515)), ((785, 800), (500, 515)),
    ((650, 665), (535, 550)), ((695, 710), (535, 550)), ((740, 755), (535, 550)), ((785, 800), (535, 550)),
    ((650, 665), (565, 580)), ((695, 710), (565, 580)), ((740, 755), (565, 580)), ((785, 800), (565, 580)),
    ((650, 665), (600, 615)), ((695, 710), (600, 615)), ((740, 755), (600, 615)), ((785, 800), (600, 615)),
    ((650, 665), (635, 650)), ((695, 710), (635, 650)), ((740, 755), (635, 650)), ((785, 800), (635, 650)),
    ((650, 665), (670, 685)), ((695, 710), (670, 685)), ((740, 755), (670, 685)), ((785, 800), (670, 685)),
    ((650, 665), (705, 720)), ((695, 710), (705, 720)), ((740, 755), (705, 720)), ((785, 800), (705, 720)),
]

# =========================
# Window targeting (your original pattern)
# =========================
global hwnd, iflag, icoord
iflag = False

def gfindWindow(data):  # find window name returns PID of the window
    global hwnd
    hwnd = win32gui.FindWindow(None, data)
    win32gui.SetActiveWindow(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, 865, 830, True)

with open("pybot-config.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

try:
    gfindWindow(data[0]['Config']['client_title'])
except BaseException:
    print("Unable to find window:", data[0]['Config']['client_title'], "| Please see list of window names below:")
    core.printWindows()
    pass

try:
    x_win, y_win, w_win, h_win = core.getWindow(data[0]['Config']['client_title'])
except BaseException:
    print("Unable to find window:", data[0]['Config']['client_title'], "| Please see list of window names below:")
    core.printWindows()
    pass

# =========================
# Helpers
# =========================
def _rand_point(xrng, yrng):
    return random.randrange(*xrng), random.randrange(*yrng)

def move_mouse(xrng, yrng, click=False, dur=(0.15, 0.45)):
    b = random.uniform(*dur)
    x_move, y_move = _rand_point(xrng, yrng)
    x_move -= random.randint(0, 4)  # tiny human-ish wobble
    y_move -= random.randint(0, 4)
    pyautogui.moveTo(x_move, y_move, duration=b)
    if click:
        pyautogui.click()

def click_object(delay=(0.11, 0.18)):
    time.sleep(random.uniform(*delay))
    pyautogui.click()
    # print('clicked')

def random_wait(a=.1, b=.3):
    time.sleep(random.uniform(a, b))

def _assert_lt_rb(rect):
    """Ensure (left, top, right, bottom) is sane."""
    l, t, r, b = rect
    assert r > l and b > t, f"Bad rect {rect}: right must be > left and bottom > top"
    return rect

# =========================
# Alch primitives
# =========================
def high_alch_command():
    # primitive click used after moving to alch spell
    time.sleep(random.uniform(0.11, 0.18))
    pyautogui.click()
    print('alch spell clicked')

def charge_staff():
    time.sleep(2.8)
    pyautogui.press('f4') # Equipment
    time.sleep(random.uniform(.15, .5))
    move_mouse((655, 670), (568, 580), click=True)  # staff in gear
    time.sleep(random.uniform(.15, .5))
    pyautogui.press('esc') # Inventory
    time.sleep(random.uniform(1, 2))
    move_mouse((650, 660), (535, 550), click=True)  # nats (1,2)
    time.sleep(random.uniform(.15, .5))
    move_mouse((650, 660), (500, 510), click=True)  # staff (1,1)
    time.sleep(random.uniform(.15, .5))
    pyautogui.click()

# =========================
# Image checks  (now pass LT-RB order)
# =========================
def alch_check():
    l, t, r, b = _assert_lt_rb(COORDS["alch_check_rect"])
    functions.screen_Image(l, t, r, b, COORDS["alch_slot_img"])
    alch = functions.image_count(COORDS["alch_empty_img"], COORDS["alch_slot_img"])
    if alch > 0:
        print('Refill condition: alch slot empty.')
        return True
    print('Alch slot filled; continue.')
    return False

def nat_check():
    l, t, r, b = _assert_lt_rb(COORDS["nat_check_rect"])
    functions.screen_Image(l, t, r, b, COORDS["nat_slot_img"])
    nat = functions.image_count(COORDS["nat_empty_img"], COORDS["nat_slot_img"])
    if nat > 0:
        print('Out of Nature runes! Terminating.')
        return True
    print('Natures OK.')
    return False

# =========================
# Bank operations
# =========================
def open_bank():
    print('Opening bank...')
    move_mouse(*COORDS["banker_center"])
    click_object()
    random_wait(.6, .9)

def deposit_inventory():
    print('Depositing inventory...')
    move_mouse(*COORDS["deposit_all"])
    click_object()
    random_wait(.15, .3)

def withdraw_item_all():
    print('Withdrawing ALL of target bank item...')
    move_mouse(*COORDS["bank_item_slot"])
    click_object()
    random_wait(.15, .3)

def withdraw_item_one():
    print('Withdrawing ONE of target bank item...')
    move_mouse(*COORDS["bank_item_slot"])
    click_object()
    random_wait(.15, .3)

def close_bank():
    pyautogui.press('escape')
    random_wait(.1, .2)

def drag_item(src_xrng, src_yrng, dst_xrng, dst_yrng):
    sx, sy = _rand_point(src_xrng, src_yrng)
    dx, dy = _rand_point(dst_xrng, dst_yrng)
    pyautogui.moveTo(sx, sy, duration=random.uniform(.08, .18))
    pyautogui.dragTo(dx, dy, duration=random.uniform(.12, .24), button='left')

def bank_refill(single_slot=True):
    """
    single_slot=True:
      - Deposit all
      - Withdraw ONE
      - Drag it to fixed alch slot (legacy flow)

    single_slot=False:
      - Deposit all
      - Withdraw ALL
    """
    open_bank()
    deposit_inventory()

    if single_slot:
        withdraw_item_one()
        close_bank()
        # Move the lone item to the fixed alch slot:
        inv_top_left = COORDS["inv_top_left"]
        alch_slot    = COORDS["alch_slot"]
        print('Dragging item into fixed alch slot...')
        drag_item(inv_top_left[0], inv_top_left[1], alch_slot[0], alch_slot[1])
    else:
        withdraw_item_all()
        close_bank()

    # Re-sync tabs & pointer like your original "fix" does:
    time.sleep(1.2)
    pyautogui.press('f2')  # inventory
    time.sleep(random.uniform(.1,.3))
    pyautogui.press('f6')  # magic
    b = random.uniform(0.36, 0.52)
    x_rng, y_rng = COORDS["alch_slot"]
    x = random.randrange(*x_rng)
    y = random.randrange(*y_rng)
    pyautogui.moveTo(x, y, duration=b)
    print('Bank refill complete; pointer reset.')

# =========================
# Cast pattern: High Alch spell -> last inventory spot (781, 723)
# =========================
def cast_on_last_inventory_spot():
    # Step 1: ensure on magic tab and click High Alch spell
    move_mouse(*COORDS["alch_slot"])
    high_alch_command()

    # Step 2: click the last inventory slot
    move_mouse(*LAST_INV_SPOT)
    click_object()

    # Natural post-cast delay
    time.sleep(random.uniform(1.8, 2.5))

# =========================
# Main loop
# =========================
def high_alch_loop(vol=15, expensive=False, charge=False):
    """ Alch 'vol' items total, batching in PER_INVENTORY_CASTS with banking between batches. """
    t = vol
    exp = expensive
    global stop_flag

    while t > 0 and stop_flag is False:
        # Safety checks before a fresh inventory
        pyautogui.press('f2')   # inventory
        time.sleep(random.uniform(.1, .3))
        if nat_check():
            stop_flag = True
            break

        # Bank + withdraw ALL + pointer reset to alch spell
        bank_refill(single_slot=False)

        # Optional Bryophyta staff charge at start of batch
        if charge:
            charge_staff()

        # Do up to 26 casts this inventory (or fewer if t < 26)
        casts_this_inv = min(PER_INVENTORY_CASTS, t)
        for i in range(casts_this_inv):
            # Light anti-ban: occasional tab resync + cursor re-fix on the alch spell
            if i == 0 or random.randint(1, 10) == 5:
                pyautogui.press('f2')
                time.sleep(random.uniform(.08, .2))
                pyautogui.press('f6')
                b = random.uniform(0.36, 0.52)
                x_rng, y_rng = COORDS["alch_slot"]
                pyautogui.moveTo(random.randrange(*x_rng), random.randrange(*y_rng), duration=b)

            # Cast pattern: spell then last slot
            cast_on_last_inventory_spot()

            # Optional “expensive” confirm flow you had
            if exp:
                time.sleep(random.uniform(0.8, 1.2))
                pyautogui.press('space')
                time.sleep(random.uniform(0.8, 1.2))
                pyautogui.press('1')
                time.sleep(random.uniform(0.5, 0.6))

            t -= 1
            print(f'{t} alchs remaining')

            # Small random micro-waits for anti-ban texture
            if random.randint(1, 4000) == 500:
                wt = random.randint(45, 260)
                print(f'Anti-ban long wait: {wt}s')
                time.sleep(wt)
            elif random.randint(1, 800) == 1:
                wt = random.randint(15, 60)
                print(f'Anti-ban short wait: {wt}s')
                time.sleep(wt)

        # Inventory consumed (26 casts or fewer) — loop will bank again if t > 0

    return True

# =========================
# Runner
# =========================
if __name__ == "__main__":
    global stop_flag
    stop_flag = False
    round_idx = 1
    max_round = 1

    while stop_flag is False and round_idx <= max_round:
        # login.login('alt1login', house_tab=True)
        # Set 'vol' to however many total casts you want this run:
        high_alch_loop(1150, expensive=False, charge=False)
        # login.logout()

        print(f'End of Round {round_idx}')
        if round_idx % 4 != 0:
            wait = random.uniform(1800, 2700)
            print(f'Short wait period before next round: {wait:.1f}s')
        else:
            wait = random.uniform(5400, 7200)
            print(f'Long wait period before next round: {wait:.1f}s')

        round_idx += 1
        stop_flag = True
        time.sleep(wait)

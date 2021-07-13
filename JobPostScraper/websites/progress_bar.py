def progressBar(current, total, barLength=20):
    percent = float(current) * 100 / total
    arrow = "-" * int(percent / 100 * barLength - 1) + ">"
    spaces = " " * (barLength - len(arrow))

    print("Searching: [%s%s] %d %%" % (arrow, spaces, percent), end="\r")

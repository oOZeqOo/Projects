import webbrowser

WEBSITE_LIST = {
    "google": "https://www.google.com",
    "being": "https://www.bing.com",
    "yahoo": "https://search.yahoo.com",
    "": "https://www..com",
    "youtube": "https://www.youtube.com",
    "python": "https://www.python.org",
}


def open_website(website_tokens, say):
    if website_tokens[0] in WEBSITE_LIST.keys():
        say(f"Alright opening {website_tokens[0]}")
        url = WEBSITE_LIST[website_tokens[0]]
        if len(website_tokens) > 3:
            separator = ""

            if website_tokens[0] in ("google", "bing", "yahoo"):
                url += "/search?q="
                separator = "%20"

            elif website_tokens[0] in ("youtube"):
                url += "/results?search_query="
                separator = "+"

            for token in website_tokens[3:-1]:
                url += f"{token}{separator}"
            url += website_tokens[-1]

        webbrowser.open_new(url)

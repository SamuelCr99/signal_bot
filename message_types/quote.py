import subprocess

def quote(message_frame, PUSH_TO_GIT):
    if message_frame.message == "!quote":
        return f"Please specify a quote"

    new_quote = message_frame.message.split("!quote ")[1]
    subprocess.run(f"git -C quotes/ pull", shell=True,capture_output=True)
    subprocess.run(f"sed '$i ‎' quotes/quotes.tex | tee quotes/quotes_temp.tex", shell=True,capture_output=True)
    subprocess.run(f"mv quotes/quotes_temp.tex quotes/quotes.tex", shell=True, capture_output=True)
    subprocess.run(f"sed '$i {new_quote}' quotes/quotes.tex | tee quotes/quotes_temp.tex", shell=True, capture_output=True)
    subprocess.run(f"mv quotes/quotes_temp.tex quotes/quotes.tex", shell=True, capture_output=True)

    if PUSH_TO_GIT:
        subprocess.run(f"git -C quotes/ add .", shell=True,capture_output=True)
        subprocess.run(f"git -C quotes/ commit -m 'New quote added from bot'", shell=True,capture_output=True)
        subprocess.run(f"git -C quotes/ push", shell=True,capture_output=True)
    return f"Quote added!"
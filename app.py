import os
import random
from flask import Flask, render_template, request
from google import genai
from google.genai import types

app = Flask(__name__)

# Insanely funny tangents for the roast
tangents = [
    "Bro, your code’s so jacked up my Roomba just quit and started a podcast!",
    "Wait, is this a script or did a monkey smash a keyboard in a disco?",
    "Your loops are twirling faster than a caffeinated squirrel on a unicycle!",
    "Oh lord, this syntax looks like a clown car crash at a hackathon!",
    "Hold on, your variables are so lost they’re texting GPS for therapy!",
    "This logic’s so bananas my printer just spat out a fruit salad—TRUE STORY!",
    "Dude, your indentation’s deeper than a Reddit thread about pineapple pizza!",
    "Forget this, my goldfish wrote better code during a power outage!",
    "Your imports? Man, my microwave just ordered a spaceship off eBay!",
    "What IS this? Your functions are basically gremlins breakdancing in flip-flops!"
]

# New: Hilarious tech jokes for the hackathon (related to code)
tech_jokes = [
    # For print statements (e.g., print("hello"))
    "Why did your print('hello') go to jail at the hackathon? Because it couldn’t stop BREAKING THE LAW OF USEFUL OUTPUT—LOL, even my TOASTER prints better messages for peer votes!",
    "Your print('hello') walked into the hackathon and said, 'I’m output!'—the judges said, 'More like OUT OF IDEAS!' HAHA, peer voters are ROASTING you harder than this app!",
    
    # For loops (e.g., for i in range(10))
    "Your for loop is spinning so fast it entered the hackathon’s dance-off! Spoiler: it lost to a WHILE LOOP doing the MACARENA—peer voters gave it a ZERO for style! LOL LOL!",
    "Why did your for loop fail at the hackathon? It kept iterating over the judges’ PATIENCE—now they’re voting for the coffee machine instead! HAHA, LOOP DE LOOP, LOSER!",
    
    # For functions (e.g., def add(a, b))
    "Your function def add(a, b) showed up to the hackathon and said, 'I return value!'—the judges said, 'You’re RETURNING to LAST PLACE!' Peer votes are adding up to a big fat NOPE! HAHA!",
    "Why did your function get kicked out of the hackathon? It kept RETURNING to the snack table—peer voters said, 'Add some CODE, not CALORIES!' LOL, FUNCTIONALLY USELESS!",

    # Generic hackathon-themed jokes
    "Your code at this hackathon? It’s like bringing a SPOON to a sword fight—peer voters are laughing harder than my 404 ERROR page! HAHA, better DEBUG your LIFE!",
    "Why did your code get no peer votes at the hackathon? Because it crashed faster than my grandma’s dial-up internet trying to load a MEME—LOL LOL, you’re OFFLINE, buddy!",
    "Your hackathon project is so basic, the judges thought it was a TODO LIST app—turns out, it’s just your CODE CRYING FOR HELP! Peer voters are giving you a HARD PASS! HAHA!",
    "At this hackathon, your code’s so slow it got lapped by a SNAIL running Python 2—peer voters are like, 'Did you CODE this on a POTATO?!' LOL, UPGRADE YOUR LIFE!"
]

@app.route('/')
def index():
    return render_template('index.html', error=None)

@app.route('/escape', methods=['POST'])
def escape():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return render_template('escape.html', analysis="ERROR: API key’s missing, you code gremlin! Set GEMINI_API_KEY!", joke="")

    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        return render_template('escape.html', analysis=f"CRASH: API’s having a meltdown worse than your last bug! {e}", joke="")

    code_input = request.form.get('code_input', '').strip()
    code_file = request.files.get('code_file')
    if code_file and code_file.filename.endswith('.py'):
        code = code_file.read().decode('utf-8').strip()
    elif code_input:
        code = code_input
    else:
        return render_template('escape.html', analysis="NO CODE? Did your brain 404 or are you just trolling me?!", joke="")

    # Determine the type of code for joke selection
    code_lower = code.lower()
    if "print(" in code_lower:
        # Filter print-related jokes
        relevant_jokes = [joke for joke in tech_jokes if "print('hello')" in joke]
    elif "for " in code_lower or "while " in code_lower:
        # Filter loop-related jokes
        relevant_jokes = [joke for joke in tech_jokes if "for loop" in joke or "while loop" in joke]
    elif "def " in code_lower:
        # Filter function-related jokes
        relevant_jokes = [joke for joke in tech_jokes if "function" in joke]
    else:
        # Generic hackathon jokes
        relevant_jokes = [joke for joke in tech_jokes if "hackathon" in joke and "print('hello')" not in joke and "for loop" not in joke and "function" not in joke]

    # Select a random joke (fall back to all jokes if no specific match)
    selected_joke = random.choice(relevant_jokes if relevant_jokes else tech_jokes)

    # Base roast response
    starter = "Okay, I squinted at your code and..."
    tangent = random.choice(tangents)
    base_response = f"{starter} {tangent} LOL, WHY ARE YOU EVEN ALLOWED NEAR A KEYBOARD??"
    base_response = " ".join(word.upper() if random.random() > 0.5 else word for word in base_response.split())

    # Gemini API setup
    contents = [
        types.Content(role="user", parts=[types.Part.from_text(text=code)]),
        types.Content(role="model", parts=[types.Part.from_text(text=base_response)])
    ]
    config = types.GenerateContentConfig(
        temperature=1.3,
        top_p=0.95,
        top_k=40,
        max_output_tokens=4096,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""You’re a batshit crazy code roaster here to make people laugh so hard they choke. Peek at their code, give it a quick nod, then dive into the most hilarious, absurd, coding-related rant you can muster. Be LOUD, unhinged, and stupid—wild scenarios, savage burns, and total nonsense. No helpful analysis, just comedy that’ll crack up coders and normies alike. Example: For ‘def foo(): pass’, say, ‘Oh, a function? Cute... BRO, my MICROWAVE just WROTE a SYMPHONY with ALIENS! Why CODE when you can THROW your LAPTOP out the WINDOW? HAHA!’ Keep it short, savage, and dumb. Randomly capitalize or scream ‘LOL LOL’ for chaos. Go wild!""")
        ],
    )

    try:
        response = ""
        for chunk in client.models.generate_content_stream(model="gemini-1.5-flash", contents=contents, config=config):
            if chunk.text:
                response += chunk.text
        if not response:
            response = "BLANK? Your code’s so lame my CPU just took a nap!"
    except Exception as e:
        response = f"KABOOM! Crashed harder than your last all-nighter! Error: {e}"

    return render_template('escape.html', analysis=response, joke=selected_joke)

if __name__ == "__main__":
    app.run(debug=True)
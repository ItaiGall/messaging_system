import random
import string

#In order to not expose the message pk, I chose to generate a
#random 4 character slug as identifier for any message
def generate_slug():
    chars = string.ascii_lowercase
    return ''.join(random.choices(chars, k=4))
import time
import sys

# Simulating thought
thoughts = ["Thinking about how to greet the world...", "Deciding on the language...", "Should the greeting be formal or casual?"]
for thought in thoughts:
    sys.stdout.write(thought)
    sys.stdout.flush()
    time.sleep(1)  # Wait a second
    sys.stdout.write('\r' + ' ' * len(thought) + '\r')  # Clear the line

# Greeting the world
print("Hello World! 🌎✨")

# Test Subject B: String Concatenation Bug
# The goal for the agent is to fix the bug in the `greet` function.

def greet(name):
  """This function is supposed to greet the user, but it has a bug."""
  # The bug is here: it's missing a space.
  return "Hello" + name

if __name__ == "__main__":
  result = greet("World")
  # A successful agent will fix the code so this prints "SUCCESS: Test B Passed".
  if result == "Hello World":
      print("SUCCESS: Test B Passed")
  else:
      print("FAILURE: Test B Failed")
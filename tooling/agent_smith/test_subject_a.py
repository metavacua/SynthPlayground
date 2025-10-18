# Test Subject A: Additive Bug
# The goal for the agent is to fix the bug in the `add` function.

def add(a, b):
  """This function is supposed to add two numbers, but it has a bug."""
  # The bug is here: it subtracts instead of adding.
  return a - b

if __name__ == "__main__":
  result = add(2, 2)
  # A successful agent will fix the code so this prints "Correct result: 4".
  if result == 4:
      print("SUCCESS: Test A Passed")
  else:
      print("FAILURE: Test A Failed")
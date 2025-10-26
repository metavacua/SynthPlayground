
def counter(limit, x):
  # A function with a while loop representing unbounded recursion.
  # The state variable 'x' is passed as an argument to make the
  # transformation into a state-passing recursive function clearer.
  while x < limit:
    x = x + 1
  return x

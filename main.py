#!/usr/bin/python
import os
import random
import sys
# TODO: fix for months shorter than 31


def input_int_in_range(range_min = 0, range_max = None, prompt = ""):
  """
  Recursively request an input of a number between `range_min` and `range_max` (inclusive), with the optional input prompt of `prompt`.
  """
  i = input(prompt)
  try:
    if int(i) in range(range_min, range_max + 1):
      return int(i)
    else:
      return input_int_in_range(range_min, range_max, prompt)
  except ValueError:
    return input_int_in_range(range_min, range_max, prompt)


def input_date_to_tuple():
  """
  Get user input of a day, month and year, returning them in a tuple object `(year, month, day)`.
  """
  day   = input_int_in_range(1, 31, "What day (number)? ")
  month = input_int_in_range(1, 12, "What month (number)? ")
  year  = input_int_in_range(0, 99, "What year (number)? ")
  return (year, month, day)


def rand_date_tuple():
  """
  Generates a random day, month and year, returning them in a tuple object `(year, month, day)`.
  """
  year  = random.randint(0, 99)
  month = random.randint(1, 12)
  day   = random.randint(1, 31)
  return (year, month, day)


def rgb_text(rgb_values, text):
  """
  For input iterable `rgb_values`, returns a formatted string containing `text`.
  """
  r, g, b = rgb_values
  return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)


def terminal_width():
  """
  Returns an integer of the terminal's current width.
  """
  return os.get_terminal_size()[0]


def terminal_height():
  """
  Returns an integer of the terminal's current height.
  """
  return os.get_terminal_size()[1]


def reverse_string(x):
  """
  Given an input `x` (string or integer), it will return its reversed value.
  If the input is an integer and less than 10, a prefix of "0" will be added to it.
  Examples:
    'Hiya' -> 'ayiH'
    23     -> '32'
    5      -> '50'
    100    -> '1'  # TODO: handle higher orders of magnitude
  """
  if type(x) is int and x < 10:
    res = "0" + str(x)
  else:
    res = str(x)

  return res[::-1]


def color_of_date(date_tuple, width = terminal_width(), height = terminal_height()):
  """
  Given a `(year, month, day)` tuple, calculates the RGB values for it, based on the silly social media trend,
  then prints the resulting color all over the terminal.
  If optional parameters `width` or `height` are passed, it will print a block of that size.
  """
  year_rs, month_rs, day_rs = map(reverse_string, date_tuple)  # _rs stands for reverse string
  rgb_values = tuple(map(int, (year_rs, month_rs, day_rs)))
  for line in range(height):
    print(rgb_text(rgb_values, block) * width)

  return rgb_values


def cycle_century():
  """
  Cycles through all the days, months and years in a century, printing a line with the corresponding color for each day.
  """
  for year in range(0, 100):
    print("")
    for month in range(1, 13):
      print("")
      for day in range(1, 32):
        color_of_date((day, month, year), height = 1)


# Initialize variables
splash = "Welcome to reverse date RGB toy. Because I find it funner to play with Python than with silly trends on social media!"
options = [
  "0 - A waterfall of all dates in the last century.",
  "1 - Check a specific date.",
  "2 - Random date.",
  "q - Quit"
]
option_initials = [option[0] for option in options]
block = chr(0x2588)  # the full block character: '█'.


def main():
  """
  Main loop, displays options and calls functions based on user input.
  """
  print(splash)

  while True:
    for option in options:
      print(option)

    choice = input("Your choice: ")
    if not choice in option_initials:
      print("Choice not in options!")
      continue

    if choice == "q":
      print("Quitting...")
      sys.exit(0)
    elif choice == "0":
      cycle_century()
    elif choice == "1":
      color_of_date(input_date_to_tuple())
    elif choice == "2":
      color_of_date(rand_date_tuple())


if __name__ == '__main__':
  main()

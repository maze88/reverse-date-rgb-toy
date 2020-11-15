#!/usr/bin/python
import calendar
import datetime
import os
import random
import sys


def days_in_month(year, month):
  """
  Returns the number of days in a month, for a given year (in case of leap-years).
  """
  return calendar.mdays[month] + calendar.isleap(year)  # second expression is a boolean, `True` is counted as 1.


def reverse_string(x):
  """
  Given an input `x` (string or integer), it will return its reversed value.
  If the input is an integer and less than 10, a prefix of '0' will be added to it before reversing.
  Examples:
    'Hiya' -> 'ayiH'
    23     -> '32'
    700    -> '007'
    5      -> '50'  # example of case where `x` is less than 10!
  """
  if type(x) is int and 0 <= x < 10:
    res = "0" + str(x)
  else:
    res = str(x)
  return res[::-1]


def color_of_date(date_tuple):
  """
  Given a `(year, month, day)` tuple, calculates the RGB values for it, based on the silly social media trend.
  Returns a tuple with the RGB values of the date.
  """
  year_rs, month_rs, day_rs = map(reverse_string, date_tuple)
  return tuple(map(int, (year_rs, month_rs, day_rs)))


def format_tuple_as_str(tup, delimiter = ","):
  """
  Given a tuple such as `(x, y, z)`, returns a string 'x, y, z'.
  Passing the optional `delimiter` parameter will replace the [default] commas with another delimiter.
  """
  return str(tup).strip("(").replace(", ", delimiter).strip(")")


def input_int_in_range(range_min = 0, range_max = 0, prompt = ""):
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


class Terminal:
  def width():
    """
    Returns an integer of the terminal's current width.
    """
    return os.get_terminal_size()[0]

  def height():
    """
    Returns an integer of the terminal's current height.
    """
    return os.get_terminal_size()[1]


def rgb_text(rgb_values, text):
  """
  For an input iterable `rgb_values`, of length 3, returns a formatted string containing `text`.
  """
  r, g, b = rgb_values
  return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)


def print_color_block(rgb_values, width = Terminal.width(), height = Terminal.height()):
  """
  Given a tuple of RGB values, prints the resulting color all over the terminal.
  If optional parameters `width` or `height` are passed, it will print a block_char in the appropriate dimensions.
  """
  for line in range(height):
    print(rgb_text(rgb_values, block_char) * width)


def cycle_century():
  """
  Cycles through all the days, months and years in a century, printing a line with the corresponding color for each day.
  """
  for year in range(1, 100):
    for month in range(1, 13):
      for day in range(1, days_in_month(year, month) + 1):
        d = Date(date_dict = {"year": year, "month": month, "day": day})
        c = color_of_date(d.tuple())
        date_caption = format_tuple_as_str(d.tuple(reversed = True), delimiter = "/")
        print(date_caption, end = "")
        print_color_block(c, width = Terminal.width() - len(date_caption), height = 1)


class Date:
  """
  Used for creating Date objects in the script.
  """
  def __init__(self, date_dict = None, user_input = False):
    """
    Create a Date object, with random values (by default) or with user input values (if `user_input` is set to True).
    """
    if date_dict:
      self.year  = date_dict["year"] % 100
      self.month = date_dict["month"]
      self.day   = date_dict["day"]
    elif user_input:
      self.year  = input_int_in_range(0, datetime.datetime.now().year + 1000, "What year (number)? ") % 100
      self.month = input_int_in_range(1, 12, "What month (number)? ")
      self.day   = input_int_in_range(1, days_in_month(self.year, self.month), "What day (number)? ")
    else:
      self.year  = random.randint(0, 99)
      self.month = random.randint(1, 12)
      self.day   = random.randint(1, days_in_month(self.year, self.month))

  def tuple(self, reversed = False):
    """
    Returns a tuple containing the object's year, month and date values.
    """
    if reversed:
      r = -1
    else:
      r = 1
    return (self.year, self.month, self.day)[::r]


# Initialize variables
splash = "Welcome to reverse date RGB toy. Because I find it funner to play with Python than with silly trends on social media!"
options = [
  "0 - A waterfall of all dates in a century.",
  "1 - Check a specific date.",
  "2 - Random date.",
  "q - Quit"
]
option_labels = [o[0] for o in options]
block_char = chr(0x2588)  # the full block character: '█'.


def main():
  """
  Main loop, displays options and calls functions based on user input.
  """
  print(splash)

  while True:
    for o in options:
      print(o)

    choice = input("Your choice: ")
    if not choice in option_labels:
      print("Choice not in options!\n")
      continue

    if choice == "q":
      print("Quitting...")
      sys.exit(0)
    elif choice == "0":
      cycle_century()
    elif choice == "1" or choice == "2":
      d = Date(user_input = choice is "1")
      c = color_of_date(d.tuple())
      print_color_block(c)
      date_caption = format_tuple_as_str(d.tuple(reversed = True), delimiter = "/")
      print(date_caption)

if __name__ == '__main__':
  main()

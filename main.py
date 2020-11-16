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
  return calendar.mdays[month]  # TODO: consider support for leap years.


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


class RGB_Color:
  """
  Creates an RGB color object with red, green and blue attributes - which are integers between 0-255 (inclusive).
  """
  def __init__(self, r, g, b):
    self.red   = abs(r) % 256
    self.green = abs(g) % 256
    self.blue  = abs(b) % 256

def color_of_date(date):
  """
  Given a date object, calculates the RGB values for it, based on the "silly" social media trend.
  Returns an RGB color object for the color of the date.
  """
  y_rs, m_rs, d_rs = map(reverse_string, (date.year % 100, date.month, date.day))
  y_ri, m_ri, d_ri = tuple(map(int, (y_rs, m_rs, d_rs)))
  return RGB_Color(y_ri, m_ri, d_ri)


def format_date_string(date):
   """
   Returns a formatted string from date object.
   Example string: 'Jan  2 84'
   """
   return "{} {}".format(date.ctime()[4:10], date.ctime()[-2:])


def input_int_in_range(range_min = 0, range_max = 0, prompt = ""):
  """
  Request an input of a number between `range_min` and `range_max` (inclusive), with the optional input prompt of `prompt`.
  Recursively re-requests input if invalid input is passed.
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
  """
  A class used to access the dimenstions of the terminal.
  """
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


def rgb_text(rgb_color, text):
  """
  For an input RGB color object, returns a formatted string containing `text` in the color passed to it.
  """
  r, g, b = rgb_color.red, rgb_color.green, rgb_color.blue
  return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)


def print_color_block(rgb_values, width = Terminal.width(), height = Terminal.height()):
  """
  Given an RGB object, prints its color all over the terminal.
  If optional parameters `width` or `height` are passed, it will print a block in the appropriate dimensions.
  """
  for line in range(height):
    print(rgb_text(rgb_values, block_char) * width)


def cycle_century():
  """
  Cycles through all the days, months and years in a century, printing a line with the corresponding color for each day.
  """
  for year in range(1900, 2000):
    for month in range(1, 13):
      for day in range(1, days_in_month(year, month) + 1):
        d = datetime.date(year, month, day)
        c = color_of_date(d)
        date_caption = format_date_string(d)
        print(date_caption, end = "")
        print_color_block(c, width = Terminal.width() - len(date_caption), height = 1)


def date_builder(from_user_input = False):
  """
  Creats date objects either with user input or random values.
  """
  if not from_user_input:
    year  = random.randint(0, 99)
    month = random.randint(1, 12)
    day   = random.randint(1, days_in_month(year, month))
  elif from_user_input:
    year  = input_int_in_range(0, datetime.datetime.now().year + 1000, "What year (number)? ") % 100
    month = input_int_in_range(1, 12, "What month (number)? ")
    day   = input_int_in_range(1, days_in_month(year, month), "What day (number)? ")

  return datetime.date(year, month, day)


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
      d = date_builder(from_user_input = choice is "1")
      c = color_of_date(d)
      print_color_block(c)
      date_caption = format_date_string(d)
      print(date_caption)
    else:
      pass  # placeholder for new options

if __name__ == '__main__':
  main()

# Conan Exiles Discord Bot Helper Functions
# Author: Bradley Hartlove
# Version: 0.1

# colors for embeded messages
colors = {
    "red": 15158332,
    "green": 3066993,
    "blue": 3447003
}

def wrap_message(msg):
    return ("```" + msg + "```")

def get_color(name):
    if name in colors.keys():
        return colors.get(name)
    else:
        return 0

def pretty_print(values, columns):
    result = ""
    for key in columns:
        result += f"{key}: {values[key]}\n"
    result += "\n"
    return result
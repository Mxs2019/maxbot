from colorama import Fore, Style, init

init(autoreset=True)


class Mind:
    def __init__(self):
        self.memory = []

    def addThought(self, thought):
        self.memory.append(("thought", thought))
        self._log_entry("thought", thought)

    def addObservation(self, observation):
        self.memory.append(("observation", observation))
        self._log_entry("observation", observation)

    def addCommand(self, command: str, node: str, text: str, value: str):
        node_first_line = node.split("\n")[0]

        command_string = f"{command} on {node_first_line}"
        if text:
            command_string += f" with text: {text}"
        elif value:
            command_string += f" with value: {value}"
        self.memory.append(("command", command_string))
        self._log_entry("command", command_string)

    def getMemories(self):
        formatted_memory = ""
        for entry_type, entry_content in self.memory:
            formatted_memory += f"{entry_type}: {entry_content}\n"
        return formatted_memory

    def _log_entry(self, entry_type, entry_content):
        color = self._get_color(entry_type)
        prefix = self._get_prefix(entry_type)
        print(f"{color}{prefix} {entry_type}: {entry_content}{Style.RESET_ALL}")

    def _get_color(self, entry_type):
        if entry_type == "thought":
            return Fore.BLUE
        elif entry_type == "observation":
            return Fore.GREEN
        elif entry_type == "command":
            return Fore.RED
        else:
            return Fore.RESET

    def _get_prefix(self, entry_type):
        if entry_type == "thought":
            return "🧠"
        elif entry_type == "observation":
            return "👀"
        elif entry_type == "command":
            return "🤖"
        else:
            return " "


if __name__ == "__main__":
    my_mind = Mind()
    my_mind.addThought("I need to buy groceries.")
    my_mind.addObservation("It's raining outside.")
    my_mind.add

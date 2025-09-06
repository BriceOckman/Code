class GameIO:
    def input(self, prompt):
        return input(prompt)

    def print(self, *args, **kwargs):
        print(*args, **kwargs)
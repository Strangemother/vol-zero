from pathlib import Path

folder = Path(".")
output = folder / "combined.md"

with output.open("w", encoding="utf-8") as out:
    for path in sorted(folder.glob("*.md")):
        if path != output:
            out.write(f"\n=========== {path} =========\n\n")
            out.write(path.read_text(encoding="utf-8"))
            out.write(f"\n========== END OF {path} =========\n\n")



class RegisterKey:
    # Example for ghost.
    def __init__(self, name):
        self.name = name 
        
    def __equals__(self, other):
        emit('mov', self.name, other)

SI = RegisterKey('SI')
SI = 10
import json
import sys

from lib.transform_mods import flatten_mods


def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with (
        open(input_file, "r", encoding="utf-8") as _in,
        open(output_file, "w", encoding="utf-8") as out,
    ):
        data = json.load(_in)  # pyright: ignore[reportAny]
        transformed_mods = flatten_mods(data)
        json.dump(transformed_mods, out, indent=4)
        print(f"Transformed mods written to '{output_file}'")


if __name__ == "__main__":
    main()

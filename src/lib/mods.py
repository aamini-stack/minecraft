import argparse


def migrate():
    print("Migrating...")


def add_mod(args):
    print("Adding mod...")


def remove_mod(args):
    print("Removing mod...")


def sync_mods(args):
    print("Syncing mods...")


def main():
    parser = argparse.ArgumentParser(description="Manage Minecraft mods.")
    subparsers = parser.add_subparsers(dest="command")

    # Migrate
    subparsers.add_parser(
        "migrate", help="Migrate existing mods.jsonc to new format"
    )

    # Add
    add_parser = subparsers.add_parser("add", help="Add a new mod")
    add_parser.add_argument("-n", "--name", required=True, help="Mod name")
    add_parser.add_argument(
        "-u", "--url", required=True, help="Mod download URL"
    )
    add_parser.add_argument(
        "-t",
        "--type",
        choices=["client", "server", "both"],
        required=True,
        help="Mod type",
    )
    add_parser.add_argument("-d", "--description", help="Mod description")

    # Remove
    remove_parser = subparsers.add_parser("remove", help="Remove a mod")
    remove_parser.add_argument("name", help="Mod name to remove")

    # Sync
    subparsers.add_parser("sync", help="Download mods to folders")

    args = vars(parser.parse_args())

    if args["command"] == "migrate":
        migrate()
    elif args["command"] == "add":
        add_mod(args)
    elif args["command"] == "remove":
        remove_mod(args)
    elif args["command"] == "sync":
        sync_mods(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

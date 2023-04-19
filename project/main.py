from InquirerPy import inquirer
from InquirerPy.utils import color_print, patched_print
from engine import collect, inverted_index, search, train, predict_link
from story import story_text

def main():
    while (True):
        option = inquirer.select(
            message="What do you want to do?",
            choices=[
                "Collect new documents",
                "Index documents",
                "Search for a query",
                "Train ML classifier",
                "Predict a link",
                "Your story",
                "Exit"
            ],
        ).execute()

        if option == "Collect new documents":
            collect()

        elif option == "Index documents":
            inverted_index()

        elif option == "Search for a query":
            query = inquirer.text(message="Enter your query:").execute()
            search(query)

        elif option == "Train ML classifier":
            train()

        elif option == "Predict a link":
            link = inquirer.text(message="Enter a link:").execute()
            if (not (link.startswith("http://") or link.startswith("https://") or link.startswith("www."))):
                color_print([("red", "Invalid link")])

            else:
                predict_link(link)

        elif option == "Your story":
            story()

        elif option == "Exit":
            proceed = inquirer.confirm(message="Are you sure?", default=True).execute()
            if (proceed):
                exit()

        patched_print()

    return


def validate_url(link: str):
    return link.startswith("http://") or link.startswith("https://") or link.startswith("www.")


def story():
    with open("story.txt", "w") as f:
        f.write(story_text)

    color_print([("green", "Your story is saved in story.txt!")])
    return


if (__name__ == "__main__"):
    main()

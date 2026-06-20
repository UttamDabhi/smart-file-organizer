from flask import Flask, render_template, request
import os
import shutil

app = Flask(__name__)

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx"],
    "Audio": [".mp3", ".wav"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Archives": [".zip", ".rar"]
}


def get_category(extension):

    extension = extension.lower()

    for category, extensions in FILE_TYPES.items():

        if extension in extensions:
            return category

    return "Others"


@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        folder_path = request.form["folder_path"].strip()
        action = request.form.get("action")

        images = 0
        documents = 0
        audio = 0
        videos = 0
        archives = 0
        others = 0

        logs = []

        try:

            files = os.listdir(folder_path)

            # ORGANIZE FILES
            if action == "organize":

                for file in files:

                    source_path = os.path.join(
                        folder_path,
                        file
                    )

                    if not os.path.isfile(source_path):
                        continue

                    extension = os.path.splitext(file)[1]

                    category = get_category(extension)

                    destination_folder = os.path.join(
                        folder_path,
                        category
                    )

                    os.makedirs(
                        destination_folder,
                        exist_ok=True
                    )

                    destination_path = os.path.join(
                        destination_folder,
                        file
                    )

                    # Duplicate filename handling

                    if os.path.exists(destination_path):

                        filename = os.path.splitext(file)[0]
                        ext = os.path.splitext(file)[1]

                        counter = 1

                        while True:

                            new_name = (
                                f"{filename}_{counter}{ext}"
                            )

                            destination_path = os.path.join(
                                destination_folder,
                                new_name
                            )

                            if not os.path.exists(
                                destination_path
                            ):
                                break

                            counter += 1

                    shutil.move(
                        source_path,
                        destination_path
                    )

                    logs.append(
                        f"✅ {file} → {category}"
                    )

                files = os.listdir(folder_path)

            # SCAN FILES

            for file in files:

                full_path = os.path.join(
                    folder_path,
                    file
                )

                if os.path.isfile(full_path):

                    extension = os.path.splitext(file)[1]

                    category = get_category(extension)

                    if category == "Images":
                        images += 1

                    elif category == "Documents":
                        documents += 1

                    elif category == "Audio":
                        audio += 1

                    elif category == "Videos":
                        videos += 1

                    elif category == "Archives":
                        archives += 1

                    else:
                        others += 1

            result = {
                "folder": folder_path,
                "images": images,
                "documents": documents,
                "audio": audio,
                "videos": videos,
                "archives": archives,
                "others": others,
                "logs": logs
            }

        except Exception as e:

            result = {
                "error": str(e)
            }

    return render_template(
        "index.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)
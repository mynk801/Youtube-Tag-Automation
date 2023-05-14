# YouTube Video Tags Updater

This project is designed to automatically update the tags of a YouTube video based on the top tags of related videos. By leveraging the YouTube API and natural language processing techniques, the program extracts relevant tags from related videos and applies them to the specified video.

## Prerequisites

Before using this project, ensure you have the following:

- Python 3.7 or higher installed on your system
- YouTube Data API credentials (API key)

## Getting Started

To get started with the YouTube Video Tags Updater, follow these steps:

1. Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/your-username/youtube-tags-updater.git
```

2. Install the required Python dependencies by running the following command:

```bash
pip install -r requirements.txt
```

3. Obtain your YouTube Data API credentials by following these steps:

   - Visit the [Google Developers Console](https://console.developers.google.com/).
   - Create a new project or select an existing project.
   - Enable the YouTube Data API v3 for your project.
   - Create an API key for the project.
   - Make sure to restrict the API key to only have access to the YouTube Data API.

4. Once you have your API key, open the `config.py` file and replace `'YOUR_API_KEY'` with your actual API key.

## Usage

1. Open the `main.py` file in a text editor.

2. Find the `video_url` variable and replace the value with the URL of the YouTube video for which you want to update the tags.

3. Optionally, you can adjust other settings such as the number of related videos to consider (`num_related_videos`) and the maximum number of tags to extract (`max_tags`).

4. Save the changes to the `main.py` file.

5. Run the program using the following command:

```bash
python main.py
```

6. The program will fetch the top tags from related videos and update the tags of the specified video using the YouTube API.

7. Once the process is complete, you can check the updated tags for your video on the YouTube Studio dashboard.

## Contributing

Contributions to this project are welcome! If you encounter any issues or have ideas for improvements, please open an issue or submit a pull request on the GitHub repository.

When contributing, please adhere to the existing code style and ensure that your changes are well-documented.


## Disclaimer

This project is an open-source tool provided as-is without any warranty. The developers are not responsible for any misuse or damage caused by this software. Use it responsibly and respect the terms of service of the platforms you interact with.

---

Happy tagging! If you have any questions or need further assistance, please don't hesitate to reach out.

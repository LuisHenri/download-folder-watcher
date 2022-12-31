[![CodeFactor](https://www.codefactor.io/repository/github/luishenri/downloads-folder-watcher/badge)](https://www.codefactor.io/repository/github/luishenri/downloads-folder-watcher)

# Downloads Folder Watcher

______________________________________________________________________

Hi!\
Have you ever fresh-installed your OS and saw how **beautiful** and **clean** were the folders inside it, but after a while using it and downloading much stuff from the internet you were **not able** anymore **to easily find something inside your Downloads Folder**?

**_Your problems are solved!!!_**

This is a simple **cross-platform** project that aims to organize your Downloads Folder by moving new files from it to other folders.\
**E.g.:** If you **download an image** file, it wil be **moved** into your _Pictures_ folder. The same could be for a document file or any other file that you can get a pattern from.

## How to use it

First you need to set up the environment by running `pip install -r requirements.txt` (it is recommended to use a [virtual environment](https://docs.python.org/pt-br/3/library/venv.html)).

Then you can simply run the main script by executing: `python -m downloads_watcher`.

### Configuring

You can edit the extensions you wish to track and the destination folders on [`bin/settings.json`](bin/settings.json).\
But here is a snippet from it anyway:

```json
{
    "file_patterns": {
        "Pictures": ["*.png", "*.jpg", "*.jpeg", "*.exif", "*.tiff", "*.gif", "*.bmp"],
        "Documents/TextFiles": ["*.txt"],
        "Documents/PDFFiles": ["*.pdf"],
        "Documents/DocFiles": ["*.doc", "*.docx"],
        "Documents/ExcelFiles": ["*.csv", "*.xls"]
    },
    "watch_folder_path": "C:/Users/LuisHenri/Downloads"
}
```

### Advanced settings

It is also possible to create an executable from it in order to make it simpler to run it at startup.\
To do so, install `pyinstaller` by either running `pip install -U pyinstaller` or `pip install -r requirements-dev.txt`.

After finished, you can simply run `pyinstaller --clean main.spec` and it will create a `DownloadsWatcher` executable inside a `dist` folder.

> **NOTE:** It will have an `.EXE` extension if compiled on Windows or NO extension at all if compiled on Linux.

Now you just need to set your OS to run it at startup:

- [on Windows](https://www.dell.com/support/kbdoc/pt-br/000124550/how-to-add-app-to-startup-in-windows-10)
- [on Linux](https://askubuntu.com/questions/48321/how-do-i-start-applications-automatically-on-login)

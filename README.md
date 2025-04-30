# SpeedyCollab

SpeedyCollab is a video editing tool by Blue Mars with a simple UI built using Python. It uses moviepy and pydub to speed up videos and adjust the pitch for speed videos. 

This is still a work in progress so it may be buggy! It also creates a bunch of temp files in a /tmp folder that you will need to delete when you're done. If you try to run too many iterations it may take a long time.

## Installation

Follow these steps to clone the repository, install dependencies, and run the program locally.

### 1. Clone the Repository

> **Note for Beginners**:  
> Before cloning the project, you need to have **Git** installed on your computer.
> 
> ### How to check if you already have Git:
> 1. Open **Command Prompt** (on Windows) or **Terminal** (on Mac/Linux).
>    - **Windows**: Press `Windows Key + R`, type `cmd`, and hit Enter.
>    - **Mac**: Press `Command + Space`, type `Terminal`, and hit Enter.
> 2. Type the following command and press Enter:
>    ```
>    git --version
>    ```
> 3. If you see a version number (like `git version 2.42.0`), you're ready to continue!
> 4. If you get an error saying "command not found" or similar, you need to install Git first.
> 
> ### How to install Git:
> - Go to [git-scm.com](https://git-scm.com/) and download the latest version for your operating system (Windows, Mac, or Linux).
> - Follow the simple installation steps. (The default options are usually fine.)
> - After installing, **close and reopen** your Command Prompt or Terminal.
> - Check again with `git --version` to make sure Git is installed properly.


First, clone this repository to your local machine by running the following command in your terminal or command prompt:

```bash
git clone https://github.com/bluemars72/SpeedyCollab.git
```

### 2. Navigate to the Project Folder

Once the repository is cloned, navigate into the project folder:

```bash
cd SpeedyCollab
```

### 3. Set up a Virtual Environment (Optional, but recommended)

It’s a good practice to set up a virtual environment to isolate your dependencies. To do this, run:

```bash
python -m venv venv
```

This creates a venv folder containing the virtual environment. To activate it, use the following command:

####Windows:
```bash
.\venv\Scripts\activate
```

####Mac/Linux:
```bash
    source venv/bin/activate
```

### 4. Install Dependencies

With the virtual environment activated, install the required dependencies listed in the requirements.txt file by running:

```bash
pip install -r requirements.txt
```

This will install all the necessary libraries such as tkinter, Pillow, pyaudio, and more.
### 5. Run the Application

Now that the dependencies are installed, you can run the application by executing the following command:

```bash
python -m app.main
```

This will launch the UI where you can select a video file, input the number of iterations, and specify an output file name. The app will then start processing the video.

### Work in Progress

This project is still a work in progress! I’m learning Python alongside my dad and constantly improving it. If you have any suggestions or ideas for enhancements, please submit an Issue on GitHub.

### How to Submit an Issue

1. Go to the [GitHub repository](https://github.com/bluemars72/SpeedyCollab)
2. Click on the **Issues** tab.
3. Click the **New Issue** button.
4. Fill in the details of your suggestion or bug report, and submit it!

Thank you for your interest in the project!

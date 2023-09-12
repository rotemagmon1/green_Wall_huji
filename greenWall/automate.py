import subprocess
import os

def update_and_run():
    # Pull the latest changes from the Git repository
    # subprocess.run(["git", "pull"])

    # Run your visualization script
    subprocess.run(["python", "visualization.py"])

if __name__ == "__main__":
    # Change to the directory where your Git repository is located
    # os.chdir("/cs/usr/rotem_agmon/greenWall")
    # os.chdir("/Users/rotemagmon/PycharmProjects/greenWallProject/greenWall")


    update_and_run()

import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "--clean",
        "TaskManager_QueueManager_Prod.spec",
        "-y",
    ]
)

from src.screenManager import ScreenManager
import logging

logger = logging.getLogger(__name__)

from src.widgets.label import label

def main():

    app = ScreenManager()

    test_label = label(text="text",x_position=1,y_position=1)
    app.add(test_label)

    test_label1 = label(text="text",x_position=1,y_position=2)
    app.add(test_label1)

    app.start()

if __name__ == '__main__':
    logging.basicConfig(
    filename='app.log',        # Log file name
    level=logging.DEBUG,       # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    filemode='w'               # File mode: 'w' for overwrite, 'a' for append
    )

    try:
        # Your entire program logic
        main()
    except Exception as e:
        logger.exception(e)

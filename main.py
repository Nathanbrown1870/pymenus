from src.screenManager import ScreenManager
import logging

logger = logging.getLogger(__name__)

from src.widgets.label import label
from src.panels.panel_baseclass import panel_element

def main():

    app = ScreenManager()

    test_label = label(text="Debug App",x_position=1,y_position=0)
    app.add(test_label)

    test_label1 = label(text="Hidden Text",x_position=1,y_position=2)
    app.add(test_label1)

    test_panel_overlap1 = panel_element(10,10,10,10)
    test_panel_overlap1.add_text("this is a panel")
    app.add(test_panel_overlap1)

    test_panel_overlap_2 = panel_element(10,7,5,5)
    test_panel_overlap_2.add_text("This is a long text on a panel and I am pretty sure that it is going to break something when it doesn't all fit")
    app.add(test_panel_overlap_2)

    # BUG: panels will render whether or not they are tracked
    debug_panel = panel_element(30,10,30,5)
    app.add(debug_panel)
    element_array = []
    for elements in app.stack:
        for element in elements.elments:
            element_array.append(element.identify())
    debug_panel.add_list('\n'.join(element_array))

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

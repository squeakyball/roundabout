import QtQuick.Controls 1.4

ApplicationWindow {
   id: main_window
   title: "Roundabout"
   visible: true
   width: 600
   height: 400

   menuBar: MenuBar {
        Menu {
            title: "File"
            MenuItem {
                text: "Run"
                onTriggered: dataReader.run()
            }
            MenuItem {
                text: "Close"
                onTriggered: {main_window.close()}
            }
        }
    }
}

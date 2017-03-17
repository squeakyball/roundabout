import QtQuick.Controls 1.4
import QtQuick 2.0

ListView {
    width: 180
    height: 200

    model: ListModel {
        ListElement {
            name: "Driver #1"
        }
        ListElement {
            name: "Driver #2"
        }
        ListElement {
            name: "Driver #3"
        }
        ListElement {
            name: "Driver #4"
        }
        ListElement {
            name: "Driver #5"
        }
    }

    delegate: Text {
        text: name
    }
}
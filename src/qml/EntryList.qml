import QtQuick.Controls 1.4
import QtQuick 2.0

Item {
    width: 150
    height: 450

Rectangle {
    anchors.fill: parent

    color: "yellow"
    opacity: 0.4
}

ListView {
    anchors.fill: parent

    interactive: false

    model: dataModel

    delegate: Text {
        font.pointSize: 12
        text: model.name + ' - ' + model.position
    }
}
}

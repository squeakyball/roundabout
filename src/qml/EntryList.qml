import QtQuick.Controls 1.4
import QtQuick 2.0

Rectangle {
    color: "green"
    width: 200
    height: 200

ListView {
    x: 10
    y: 10
    z: 1
    width: 180
    height: 200

    //color: "red"
    //opacity: 0.5

    model: dataModel

    delegate: Text {
        text: model.name + ' - ' + model.position
    }
}
}
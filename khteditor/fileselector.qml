import Qt 4.7

Rectangle {
    id: fileDialog
    width: 800; height: 480;

    Rectangle {
        id:pathbox
        width:parent.width
        height:40
        color:'black'
        Text{
            id:path
            x: 5
            text:'path'
            color:'white'
        }
    }
     ListView {
         id: view
         anchors.top: pathbox.bottom
         height: parent.height - pathbox.height
         width: parent.width
    
         model: VisualDataModel {
             model: dirModel
    
             delegate: Rectangle {
                 width: 200; height: 60
                 Text { text: fileName }
    
                 MouseArea {
                     anchors.fill: parent
                     onClicked: {
                         if (model.hasModelChildren)
                             path.text = filePath
                             view.model.rootIndex = view.model.modelIndex(index)
                     }
                 }
             }
         }
     }
}

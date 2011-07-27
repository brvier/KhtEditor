import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0

PageStackWindow {
    id: rootWin
    initialPage:mainPage

    MainPage{id:mainPage}
    //OpenedPage{id:openedPage}

    Menu {
        id: myMenu
        visualParent: pageStack
        MenuLayout {
            MenuItem { text: "New"; onClicked: pageStack.currentPage.newFile()}
            MenuItem { text: "Open"; onClicked: pageStack.push(Qt.resolvedUrl('SelectorPage.qml'))}
            MenuItem { text: "Save"; onClicked: pageStack.currentPage.saveFile()}
            MenuItem { text: "Save As"; onClicked: pageStack.currentPage.saveAsFile()}
            MenuItem { text: "Preferences"; onClicked: notYetAvailableBanner.show()}
            MenuItem { text: "About";  onClicked: pageStack.push(Qt.resolvedUrl('AboutPage.qml'))}
        }
    }

    Dialog {
    id:aDialog
      title:Label   { color:"blue" ;text:"myDialog"}
      content:Label   { color:"white" ;text:"Content Comes Here"}
      buttons:Button {id: bOk; text: "OK"; onClicked: aDialog.accept()}
    }

    ListModel {
       id:editorsModel
    }

    InfoBanner{
                      id:notYetAvailableBanner
                      text: 'This feature is not yet available'
                      timerShowTime: 5000
                      timerEnabled:true
                      anchors.top: parent.top
                      anchors.topMargin: 60
                      anchors.horizontalCenter: parent.horizontalCenter
                 }

    function openFile(filepath){
        pageStack.pop(mainPage)
        pageStack.currentPage.openFile(filepath)
    }

    function saveFileAs(filepath){
        pageStack.pop(mainPage)
        pageStack.currentPage.setFilepath(filepath)
        pageStack.currentPage.saveFile()
    }


//    function openFile(filepath){
//       pageStack.pop(mainPage)
//        pageStack.currentPage.saveFileAs(filepath)
//    }

    function switchFile(filepath) {
        pageStack.pop(mainPage)
        pageStack.currentPage.switchFile(filepath)


         // page not found

    }
}


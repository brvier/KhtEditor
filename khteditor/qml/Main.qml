import QtQuick 1.1
import com.meego 1.0

PageStackWindow {
    id: rootWin
    property string filepath
    property string filename
    initialPage:mainPage
    MainPage{id:mainPage}
    

    Menu {
        id: myMenu
        visualParent: pageStack
        MenuLayout {
            MenuItem { text: "New"; onClicked: mainPage.new()}
            MenuItem { text: "Open"; onClicked: mainPage.open()}
            MenuItem { text: "Save"; onClicked: mainPage.save()}
            MenuItem { text: "Save As"; onClicked: mainPage.saveAs()}
            MenuItem { text: "Preferences" }
            MenuItem { text: "About";  onClicked: aboutDialog.property = 1}
        }
    }
    
    Dialog {
    id:aDialog
      title:Label   { color:"blue" ;text:"myDialog"}
      content:Label   { color:"white" ;text:"Content Comes Here"}
      buttons:Button {id: bOk; text: "OK"; onClicked: aDialog2.accept()}
    }
}

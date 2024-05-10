import os
from PIL import Image, ImageDraw, ImageFont
from PySide2.QtGui import QFont, QIcon, Qt
from PySide2.QtWidgets import QAbstractItemView, QApplication, QFileDialog, QGroupBox, QLabel, QLineEdit, QListView, QListWidget, QListWidgetItem, QWidget, QPushButton, QMessageBox, QHBoxLayout, QVBoxLayout
from PySide2 import QtCore
import sys 
print(os.getcwd())

class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("LPC Storyboard Script  -  Version 1.0")
        self.setMinimumSize(800, 600)
        self.setMaximumSize(1200, 1000)
        
        self.setIcon()
        



        self.createLayout()
      
        
       

    #CREATING WIDGETS
    
    #Set Location Widget
    def createLocationButton(self):
        setLocationButton = QPushButton("Set Export Location", self)
        
        setLocationButton.clicked.connect(self.chooseExportLocation)
        return setLocationButton
       
    def createLineEdit(self, text=None):
        lineEdit = QLineEdit(text, self)
        
        return lineEdit
   

    #Input widget
    

    #Image list widget
    
    def importImagesButton(self):
        importImagesButton = QPushButton("Import Images", self)
        
        importImagesButton.clicked.connect(self.chooseImagesToImport)
        return importImagesButton
   
    def clearImageListButton(self):
        clearImagesButton = QPushButton("Clear List", self)

        clearImagesButton.clicked.connect(self.clearImageList)
        return clearImagesButton
   
    def removeSelectedImagesButton(self):
        removeSelectedImagesButton = QPushButton("Remove Selected Items", self)

        removeSelectedImagesButton.clicked.connect(self.removeSelectedImages)
        return removeSelectedImagesButton


    #Generate button widget
    
    def generateImagesButton(self):
        generateImagesButton = QPushButton("Generate Images", self)
        
        generateImagesButton.clicked.connect(self.generateImages)
        return generateImagesButton



    #FUNCTIONALITY

    #Set Export Location functionality
    def chooseExportLocation(self):
        exportLocationDialog = QFileDialog()
        exportLocationDialog.setFileMode(QFileDialog.Directory)
        
        if exportLocationDialog.exec_():
            exportLocation = exportLocationDialog.selectedFiles()[0]
            if exportLocation:
                self.setExportLocationLineEdit(exportLocation)
                

    def setExportLocationLineEdit(self, text):
        self.exportLocationLineEdit.setText(text)

    def getExportLocationLineEdit(self):
        return self.exportLocationLineEdit.text()
       
    #Inputs functionality
    
    def areInputsValid(self, exportLocation, sceneNumber, shotNumber, startingIndex):
        if len(exportLocation) == 0 or len(sceneNumber) == 0 or len(shotNumber) == 0 or len(startingIndex) == 0:
            return True
        else:
            return False
            
      

    #Picture list functionality
    def chooseImagesToImport(self):
        importImagesDialog = QFileDialog()
        importImagesDialog.setFileMode(QFileDialog.ExistingFiles)
        importImagesDialog.setNameFilter("Images (*.png *.jpeg *.jpg *.gif *.tiff);;All Files(*)")

        
        if importImagesDialog.exec_():
            selectedImages = importImagesDialog.selectedFiles()
            if selectedImages:
                for image in selectedImages:
                    self.imageItem = QListWidgetItem(image.split("/")[-1:][0], self.pictureListWidget)
                    self.pictureListWidget.addItem(self.imageItem)
                    self.imageItem.setIcon(QIcon(image))
                    self.imageItem.setData(Qt.UserRole, image)

                
    def clearImageList(self):
        self.pictureListWidget.clear()
        
    def removeSelectedImages(self):
        selectedItems = self.pictureListWidget.selectedItems()
        
        for item in selectedItems:
            row = self.pictureListWidget.row(item)
            self.pictureListWidget.takeItem(row)


    def createPopupWindow(self, message):
        messageWindow = QMessageBox()
        messageWindow.setText(message)
        messageWindow.setWindowTitle("Information!")
        
        messageWindow.exec_()

    #Edit images functionality
    def addMargin(self, image, top, right, bottom, left, color):
        width, height = image.size
        newWidth = width + right + left
        newHeight = height + top + bottom
        
        newImage = Image.new("RGB", (newWidth, newHeight), color)
        newImage.paste(image, (left, top))
        return newImage
    

    def editImages(self, imageFile, finalSaveDirectory, finalTextEdit):
        image = Image.open(imageFile)
        image = self.addMargin(image, 70, 0, 0, 0, (0, 0, 0))
        
        
        imageDraw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 40)
        
        textPosition = (10, 10)
        textColor = (255, 255, 255)
        
        imageDraw.text(textPosition, text=finalTextEdit, fill=textColor, font=font)
        image.save(finalSaveDirectory)
        
        #image.show()
        
    def getSortOrder(self, item):
        return self.pictureListWidget.findItems("", Qt.MatchContains).index(item)

    #Generate images functionality
    
    def generateImages(self):
        if self.areInputsValid(self.exportLocationLineEdit.text(), 
                               self.sceneNumberLineEdit.text(), 
                               self.shotNumberLineEdit.text(), 
                               self.startingIndexLineEdit.text()):
            self.createPopupWindow("You haven't filled in one or more of the inputs required: Export Location, Scene Number, Shot Number, Starting Index")
            return
         
        #If we have at least one item selected, generate only those images, otherwise generate all images. 
        if len(self.pictureListWidget.selectedItems()) > 0:
            #original list  82, 74   -   order list 54, 73 ,74, 82       
            self.itemList = self.pictureListWidget.selectedItems()   #  
            self.listToSortFrom = self.pictureListWidget.findItems("", Qt.MatchContains)
            
            self.itemList.sort(key = lambda x: self.listToSortFrom.index(x))


        else:
            self.itemList = self.pictureListWidget.findItems("", Qt.MatchContains)
            

        
        self.exportLocation = self.exportLocationLineEdit.text()
        self.sceneNumber = self.sceneNumberLineEdit.text().zfill(3)
        self.shotNumber = self.shotNumberLineEdit.text().zfill(3)
        self.startingIndex = int(self.startingIndexLineEdit.text())
        
     

        for item in self.itemList:
            itemText = item.text()
            extension = itemText.split(".")[-1:][0]
            
            if len(self.pictureListWidget.selectedItems()) > 0:
                itemRow = self.itemList.index(item) 
            else:
                itemRow = self.pictureListWidget.row(item)
                
            imageFile = item.data(Qt.UserRole)
            
            finalTextEdit = f"SD_LPC_sc{self.sceneNumber}_sh{self.shotNumber}_{str(self.startingIndex + itemRow)}"
            finalSaveDirectory = f"{self.exportLocation}/{finalTextEdit}.{extension}"
            
            
            self.editImages(imageFile, finalSaveDirectory, finalTextEdit)
        
        self.createPopupWindow("Images have been generated. Check your folder")



    #LAYOUT
    def createLayout(self):
        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        mainLayout.setSpacing(10)
        
        #Set location widget
        ############
        exportLocationBoxLayout = QHBoxLayout()

        self.locationButton = self.createLocationButton()
        self.exportLocationLineEdit = self.createLineEdit()
        
        exportLocationBoxLayout.addWidget(self.locationButton)
        exportLocationBoxLayout.addWidget(self.exportLocationLineEdit)
        ############
        
        #Inputs widget
        inputWidgetsBoxLayout = QHBoxLayout()
        
        self.sceneNumberLineEdit = self.createLineEdit()
        self.shotNumberLineEdit = self.createLineEdit()
        self.startingIndexLineEdit = self.createLineEdit()
        
        

        inputWidgetsBoxLayout.addWidget(QLabel("Scene Number", self))
        inputWidgetsBoxLayout.addWidget(self.sceneNumberLineEdit)
        inputWidgetsBoxLayout.addWidget(QLabel("Shot Number", self))
        inputWidgetsBoxLayout.addWidget(self.shotNumberLineEdit)
        inputWidgetsBoxLayout.addWidget(QLabel("Starting Index", self))
        inputWidgetsBoxLayout.addWidget(self.startingIndexLineEdit)


        #Picture list widget
        pictureListWidgetBoxLayout = QHBoxLayout()
        pictureListWidgetButtonsBoxLayout = QVBoxLayout()
        
        self.importImagesButton = self.importImagesButton()
        self.clearImageListButton = self.clearImageListButton()
        self.removeSelectedImagesButton = self.removeSelectedImagesButton()
        self.pictureListWidget = QListWidget()
        

        self.pictureListWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.pictureListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.pictureListWidget.setIconSize(QtCore.QSize(100,100))
        
        pictureListWidgetButtonsBoxLayout.addWidget(self.importImagesButton)
        pictureListWidgetButtonsBoxLayout.addWidget(self.clearImageListButton)
        pictureListWidgetButtonsBoxLayout.addWidget(self.removeSelectedImagesButton)
        
        pictureListWidgetBoxLayout.addLayout(pictureListWidgetButtonsBoxLayout)
        pictureListWidgetBoxLayout.addWidget(self.pictureListWidget)



        #Generate pictures layout
        generateImagesBoxLayout = QHBoxLayout()
        
        self.generateImagesButton = self.generateImagesButton()
        
        generateImagesBoxLayout.addWidget(self.generateImagesButton)



        #Adding layouts
        mainLayout.addLayout(exportLocationBoxLayout)
        mainLayout.addLayout(inputWidgetsBoxLayout)
        
        mainLayout.addLayout(pictureListWidgetBoxLayout)
        
        mainLayout.addLayout(generateImagesBoxLayout)

        self.setLayout(mainLayout)
              
        


    #Extra
    def setIcon(self):
        windowIcon = QIcon("LPC_Icon.png")
        self.setWindowIcon(windowIcon)






LPCStoryboardScript = QApplication(sys.argv)
window = Window()
window.show()
LPCStoryboardScript.exec_()

sys.exit(0)





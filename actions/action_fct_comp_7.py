
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from actions.action_tablesData import AppTablesData


# Classe permettant d'afficher la fonction à compléter 4
class AppFctComp7(QDialog):

    changedValue = pyqtSignal()
    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_7.ui", self)
        self.data = sqlite3.connect("data/jo.db")
        self.data = data
        h = self.refreshCatList()
        print(h)
        self.refreshCatList_2(h)
        self.refreshTable()

    
    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        # TODO 1.7 : fonction à modifier pour que l'équipe ne propose que des valeurs possibles pour le pays choisi
        display.refreshLabel(self.ui.label_fct_comp_7, "")
        
        try:
            cursor = self.data.cursor()
            
            result = cursor.execute(
                "INSERT INTO LesInscriptions VALUES(?,?)",
                [self.ui.comboBox_fct_7_Eq.currentText(),self.ui.comboBox_fct_7_pays.currentText()]
            )
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))
        else:
            #i = display.refreshGenericData_1(self.ui.table_fct_comp_7, result,self.data)
            i = 0
            if i == 0:
                display.refreshLabel(self.ui.label_fct_comp_7, "Aucun résultat")
            #self.data.commit()
            self.changedValue.emit()
            
 
            print("ok")
    # Fonction de mise à jour des catégories
    def refreshBox(self):
        row_num = 0
        row_data = 0
        r = 0
        cursor = self.data.cursor()
        result = cursor.execute("SELECT  formeEp FROM LesEpreuves WHERE numEp = ?",[self.ui.comboBox_fct_7_pays.currentText()])
        for row_num, row_data in enumerate(result):
            if r == 0 :
                r = row_data
        print("row data 1 : " ,r[0])
        h = r[0]
        self.refreshCatList_2(h)
    @pyqtSlot()   
    def refreshCatList(self):
        row_num = 0
        row_data = 0
        r = 0
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT numEp FROM LesEpreuves ORDER BY numEp")
        except Exception as e:
            self.ui.comboBox_fct_7_pays.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_fct_7_pays, result)
        
        cursor = self.data.cursor()
        result = cursor.execute("SELECT  formeEp FROM LesEpreuves WHERE numEp = ?",[self.ui.comboBox_fct_7_pays.currentText()])
        for row_num, row_data in enumerate(result):
            if r == 0 :
                r = row_data
        print("row data 2: " ,r[0])
        return r[0]
    
    def refreshCatList_2(self,h):
        
        if h == "individuelle" :
            try:
                cursor = self.data.cursor()
                req = cursor.execute("SELECT numSp FROM LesSportifs EXCEPT SELECT numIn FROM LesInscriptions WHERE numEp = ?",[self.ui.comboBox_fct_7_pays.currentText()]
                )
            except Exception as e:
                self.ui.comboBox_fct_7_Eq.clear()
            else:
                display.refreshGenericCombo(self.ui.comboBox_fct_7_Eq, req)
        elif h == "par couple" :
            try:
                cursor = self.data.cursor()
                req = cursor.execute("SELECT numEq FROM LesEquipes WHERE nbEquipiersEq == 2 EXCEPT SELECT numIn FROM LesInscriptions WHERE numEp = ?",[self.ui.comboBox_fct_7_pays.currentText()])
            except Exception as e:
                self.ui.comboBox_fct_7_Eq.clear()
            else:
                display.refreshGenericCombo(self.ui.comboBox_fct_7_Eq, req)
        elif h == "par equipe" :
            try:
                cursor = self.data.cursor()
                req = cursor.execute("SELECT numEq FROM LesEquipes EXCEPT SELECT numIn FROM LesInscriptions WHERE numEp = ?",[self.ui.comboBox_fct_7_pays.currentText()])
            except Exception as e:
                self.ui.comboBox_fct_7_Eq.clear()
            else:
                display.refreshGenericCombo(self.ui.comboBox_fct_7_Eq, req)


    def refreshTable(self):
        display.refreshLabel(self.ui.label_fct_comp_7, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT numIn, numEp FROM LesInscriptions GROUP BY numIn")
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData_1(self.ui.table_fct_comp_7, result,self.data)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_comp_7, "Aucun résultat")
 
    
    
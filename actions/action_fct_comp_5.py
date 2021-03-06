
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 1
class AppFctComp5(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_5.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

            display.refreshLabel(self.ui.label_fct_comp_5, "")
            try:
                cursor = self.data.cursor()
                # TODO 1.1 : mettre à jour la requête pour ajouter dateNaisSp et changer aussi le fichier ui correspondant
                result = cursor.execute(
                     '''SELECT numEq AS num,avg(age) AS moy 
                        FROM LesSportifs S JOIN LesEquipiers E JOIN LesResultats R
                        ON R.gold = E.numEq and E.numSp= S.numSp GROUP BY numEq 
                            UNION 
                            SELECT numSp AS num,age AS moy 
                            FROM LesResultats JOIN LesSportifs 
                            ON gold = numSp''')
            except Exception as e:
                self.ui.table_fct_comp_6.setRowCount(0)
                display.refreshLabel(self.ui.label_fct_comp_5, "Impossible d'afficher les résultats : " + repr(e))
            else:
                i = display.refreshGenericData(self.ui.table_fct_comp_5, result)
                if i == 0:
                    display.refreshLabel(self.ui.label_fct_comp_5, "Aucun résultat")
                    
    def refreshCatList(self):
        h = 0
   
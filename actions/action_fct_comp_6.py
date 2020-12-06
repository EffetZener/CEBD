import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 1
class AppFctComp6(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_6.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

            display.refreshLabel(self.ui.label_fct_comp_6, "")
            try:
                cursor = self.data.cursor()
                # TODO 1.1 : mettre à jour la requête pour ajouter dateNaisSp et changer aussi le fichier ui correspondant
                result = cursor.execute(
                     "SELECT pays,sum(nbOr) AS nbOr,sum(nbArgent)AS nbArgent,sum(nbBronze) AS nbBronze  FROM paysMed GROUP BY pays ORDER BY nbOr DESC, nbArgent DESC, nbBronze DESC;")
            except Exception as e:
                self.ui.table_fct_comp_6.setRowCount(0)
                display.refreshLabel(self.ui.label_fct_comp_6, "Impossible d'afficher les résultats : " + repr(e))
            else:
                i = display.refreshGenericData(self.ui.table_fct_comp_6, result)
                if i == 0:
                    display.refreshLabel(self.ui.label_fct_comp_6, "Aucun résultat")
                    
    def refreshCatList(self):
        h = 0
   
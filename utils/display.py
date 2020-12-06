import sqlite3
import PyQt5
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem,QPushButton
from actions.action_fct_comp_7 import AppFctComp7
from PyQt5.QtCore import pyqtSignal

def appui_bouton(a,b,data):
    changedValue = pyqtSignal()
    
    cursor = data.cursor()
    result = cursor.execute("DELETE FROM LesInscriptions WHERE numIn = ? AND numEp = ?",[a,b])
    #changedValue.emit()
    data.commit()
    AppFctComp7(data)  


def cree_bouton(x,y,q,a,b,data):
    bouton = QPushButton("supprimer")
    bouton.clicked.connect(lambda:appui_bouton(a,b,data))
    q.setCellWidget(x, y, bouton)
    
    return q
# Fonction permettant d'afficher un set de résultat sqlite dans un élément de type tableWidget
# La fonction retourne le nombre de lignes qui ont été affichées
def refreshGenericData(qtablewidget: PyQt5.QtWidgets.QTableWidgetItem, result):

    qtablewidget.setEditTriggers(QTableWidget.NoEditTriggers)

    # On remet le nombre de ligne de la table à 0 pour raffraichir l'affichage
    qtablewidget.setRowCount(0)

    # Parcours générique du résultat, affichage et comptage du nombre de lignes
    i = 0
    for row_num, row_data in enumerate(result):
        qtablewidget.insertRow(row_num)
        i += 1
        for col_num, col_data in enumerate(row_data):
            qtablewidget.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

    return i


def refreshGenericData_1(qtablewidget: PyQt5.QtWidgets.QTableWidgetItem, result,data):

    fin = 0
    qtablewidget.setEditTriggers(QTableWidget.NoEditTriggers)

    # On remet le nombre de ligne de la table à 0 pour raffraichir l'affichage
    qtablewidget.setRowCount(0)

    # Parcours générique du résultat, affichage et comptage du nombre de lignes
    i = 0
    for row_num, row_data in enumerate(result):
        qtablewidget.insertRow(row_num)
        i += 1
        for col_num, col_data in enumerate(row_data):
            qtablewidget.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
            fin = col_num
        q =cree_bouton(row_num,fin+1,qtablewidget,row_data[0],row_data[1],data)
    return i



# Fonction permettant de raffraichir une liste de valeurs dans une comboBox à partir d'un set de résultats sqlite
def refreshGenericCombo(combo, result):
    combo.clear()
    for row_num, row_data in enumerate(result):
        combo.addItem(str(row_data[0]))

# Fonction permettant de mettre à jour un label, adaptée à tous les OS
def refreshLabel(qlabel: PyQt5.QtWidgets.QLabel, text):

    # Mise à jour du texte du tabel
    qlabel.setText(text)

    # Les deux lignes suivantes sont nécessaires sur MAC, inutiles sur d'autres environnements
    qlabel.hide()
    qlabel.show()
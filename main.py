from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import *
import sys
from bigmart import Ui_MainWindow
import os
from sklearn.externals import joblib
from sklearn.preprocessing import robust_scale, scale

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from graph import graph

sns.set(style='darkgrid')

import warnings

warnings.filterwarnings("ignore")

import platform

platform.system()
# 운영체제별 한글 폰트 설정
if platform.system() == 'Darwin':  # Mac 환경 폰트 설정
    plt.rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # Windows 환경 폰트 설정
    plt.rc('font', family='Malgun Gothic')

plt.rc('axes', unicode_minus=False)  # 마이너스 폰트 설정


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.hideAll()
        self.initAuthLock()

        self.df = None
        self.corr = None
        self.graph_df = None
        self.index = None
        self.columns = None
        self.brand = None
        self.result = None

        self.buttonEmart.clicked.connect(self.load_emart)
        self.buttonTraders.clicked.connect(self.load_Traders)
        self.buttonHome.clicked.connect(self.load_Home)
        self.buttonSpecial.clicked.connect(self.load_Special)
        self.buttonLotte.clicked.connect(self.load_Lotte)
        self.buttonFile.clicked.connect(self.load_file)

        self.comboPlot.currentIndexChanged.connect(self.check_plot)
        self.comboX.currentIndexChanged.connect(self.check_X)
        self.comboY.currentIndexChanged.connect(self.check_Y)

        self.buttonMap.clicked.connect(self.show_map)
        self.buttonGraph.clicked.connect(self.show_graph)
        self.buttonView.clicked.connect(self.load_view)
        self.buttonAnal.clicked.connect(self.show_result)

    def initAuthLock(self):
        self.groupResult.setEnabled(False)
        self.groupPreprocess.setEnabled(False)
        self.comboPlot.setEnabled(False)
        self.comboX.setEnabled(False)
        self.comboY.setEnabled(False)
        self.comboPlot.setCurrentIndex(0)
        self.comboX.setCurrentIndex(0)
        self.comboY.setCurrentIndex(0)
        self.buttonGraph.setEnabled(False)
        for i in reversed(range(self.graphLayout.count())):
            self.graphLayout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.resultLayout.count())):
            self.resultLayout.itemAt(i).widget().setParent(None)
        self.hideAll()

    def AuthActive(self):
        self.groupResult.setEnabled(True)
        self.groupPreprocess.setEnabled(True)
        self.radioBinning.setEnabled(True)
        self.radioScale.setEnabled(True)
        self.radioSample.setEnabled(True)
        self.webEngineView.hide()

    def hideAll(self):
        self.verticalLayoutWidget.hide()
        self.verticalLayoutWidget_2.hide()
        self.webEngineView.hide()
        self.plainTextResult.hide()
        self.resultWidget.hide()

    def show_excel(self):
        self.comboPlot.setEnabled(True)
        self.graph_df = self.df.copy()
        self.corr = np.round(self.df.corr(), 4)

        columns = list(map(str, self.df.keys()))
        self.df = self.df.astype(str)
        item_count = len(self.df[columns[0]])
        self.excelWidget.setRowCount(item_count)
        self.excelWidget.setColumnCount(len(columns))
        self.excelWidget.setHorizontalHeaderLabels(columns)
        for j in range(item_count):
            row = self.df.iloc[j, :]
            for i in range(len(row)):
                item = QTableWidgetItem(row[i])
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.excelWidget.setItem(j, i, item)

        self.excelWidget.resizeRowsToContents()
        self.excel_rc.setText("{}rows X {}colums".format(len(self.df), len(columns)))

    def show_corr(self):
        columns = list(map(str, self.corr.keys()))
        self.index = list(map(str, self.corr.index))

        self.corr = self.corr.astype(str)
        item_count = len(self.corr[columns[0]])
        self.corrWidget.setRowCount(item_count)
        self.corrWidget.setColumnCount(len(columns))
        self.corrWidget.setHorizontalHeaderLabels(columns)
        self.corrWidget.setVerticalHeaderLabels(self.index)
        for j in range(item_count):
            row = self.corr.iloc[j, :]
            for i in range(len(row)):
                item = QTableWidgetItem(row[i])
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.corrWidget.setItem(j, i, item)

        self.corrWidget.resizeRowsToContents()
        self.corr_rc.setText("{}rows X {}colums".format(len(self.corr), len(columns)))

    def load_emart(self):
        self.initAuthLock()
        self.df = pd.read_excel("./Data/emart/final_model.xlsx")
        self.brand = 'E'
        self.show_excel()
        self.show_corr()
        self.AuthActive()

    def load_Traders(self):
        self.initAuthLock()
        self.df = pd.read_excel("./Data/emart/Warehouse.xlsx")
        self.brand = 'ET'
        self.show_excel()
        self.show_corr()
        self.AuthActive()
        self.radioSample.setEnabled(False)

    def load_Home(self):
        self.initAuthLock()
        self.df = pd.read_excel("./Data/homeplus/hp.xlsx")
        self.brand = 'H'
        self.show_excel()
        self.show_corr()
        self.AuthActive()

    def load_Special(self):
        self.initAuthLock()
        self.df = pd.read_excel("./Data/homeplus/special.xlsx")
        self.brand = 'HS'
        self.show_excel()
        self.show_corr()
        self.AuthActive()

    def load_Lotte(self):
        self.initAuthLock()
        self.df = pd.read_excel("./Data/lottemart/lotte.xlsx")
        self.brand = 'L'
        self.show_excel()
        self.show_corr()
        self.AuthActive()
        self.radioSample.setEnabled(False)

    def load_file(self):
        self.initAuthLock()
        file_name = QFileDialog.getOpenFileName(self)
        filetype = file_name[0].split(".")[-1]
        if filetype == "xlsx" or filetype == "xls":
            self.df = pd.read_excel(file_name[0])
            self.show_excel()
            self.show_corr()
        elif filetype == "csv":
            try:
                self.df = pd.read_csv(file_name[0], encoding="cp949")
                self.show_excel()
                self.show_corr()
            except:
                QMessageBox.about(self, "파일 양식 오류", "잘못된 csv형식입니다.")
        else:
            QMessageBox.about(self, "파일 양식 오류", "잘못된 파일형식입니다.")

    def load_view(self):
        if self.radioBinning.isChecked() == True:
            self.df = pd.read_excel("./Data/preprocessing/{}/{}.xlsx".format(self.brand, "binning"))
            self.show_excel()
            self.show_corr()
            self.AuthActive()
            self.radioBinning.setAutoExclusive(False)
            self.radioBinning.setChecked(False)

        elif self.radioScale.isChecked() == True:
            self.df = pd.read_excel("./Data/preprocessing/{}/{}.xlsx".format(self.brand, "scaling"))
            self.show_excel()
            self.show_corr()
            self.AuthActive()
            self.radioScale.setAutoExclusive(False)
            self.radioScale.setChecked(False)

        elif self.radioSample.isChecked() == True:
            self.df = pd.read_excel("./Data/preprocessing/{}/{}.xlsx".format(self.brand, "sampling"))
            self.show_excel()
            self.show_corr()
            self.AuthActive()
            self.radioSample.setAutoExclusive(False)
            self.radioSample.setChecked(False)

        else:
            QMessageBox.about(self, "SELECTION ERROR", "라디오버튼을 선택해주세요 :D  ")

        self.radioBinning.setAutoExclusive(True)
        self.radioScale.setAutoExclusive(True)
        self.radioSample.setAutoExclusive(True)

        if self.brand in ["ET", "L"]:
            self.radioSample.setEnabled(False)

    def check_plot(self):
        try:
            self.comboX.clear()
            if self.comboPlot.currentText() not in ["- select plot -", "heatmap", "dist"]:
                self.comboX.setEnabled(True)
                self.columns = self.graph_df.keys()
                self.comboX.addItem(" ")
                self.comboX.addItems(self.columns)
                self.comboY.setEnabled(False)
            elif self.comboPlot.currentText() == "dist":
                self.comboX.setEnabled(True)
                self.columns = self.corr.keys()
                self.comboX.addItem(" ")
                self.comboX.addItems(self.columns)
                self.comboY.setEnabled(False)
            elif self.comboPlot.currentText() in ["heatmap"]:
                self.buttonGraph.setEnabled(True)
                self.comboX.setEnabled(False)
                self.comboY.setEnabled(False)
            else:
                self.comboX.setEnabled(False)
                self.comboY.setEnabled(False)
        except:
            pass

    def check_X(self):
        try:
            if self.comboPlot.currentText() not in ["pie", "count", "dist"]:
                if self.comboX.currentText() != " ":
                    self.comboY.clear()
                    columns = list(self.columns)
                    self.comboY.setEnabled(True)
                    self.comboY.addItem(" ")
                    if type(self.graph_df.loc[0, self.comboX.currentText()]) == str:
                        self.comboY.addItems(self.index)
                    else:
                        columns.remove(self.comboX.currentText())
                        self.comboY.addItems(columns)
            else:
                self.buttonGraph.setEnabled(True)
        except:
            pass

    def check_Y(self):
        try:
            if self.comboY.currentText() != " ":
                self.buttonGraph.setEnabled(True)
        except:
            pass

    def show_graph(self):
        try:
            for i in reversed(range(self.graphLayout.count())):
                self.graphLayout.itemAt(i).widget().setParent(None)
            self.hideAll()
            self.verticalLayoutWidget_2.show()
            plottype = self.comboPlot.currentText()
            if plottype not in ["heatmap"]:
                X = self.comboX.currentText()
            if plottype not in ["pie", "count", "heatmap", "dist"]:
                Y = self.comboY.currentText()

            fig = plt.figure()
            if plottype == "bar":
                g = sns.barplot(x=X, y=Y, data=self.graph_df)
                if type(self.graph_df.loc[0, X]) == str or type(self.graph_df.loc[0, Y]) == str:
                    g.set_xticklabels(g.get_xticklabels(), rotation=30,
                                      horizontalalignment='right',
                                      fontweight='light'
                                      )
            elif plottype == "box":
                g = sns.boxplot(x=X, y=Y, data=self.graph_df)
                if type(self.graph_df.loc[0, X]) == str or type(self.graph_df.loc[0, Y]) == str:
                    g.set_xticklabels(g.get_xticklabels(), rotation=30,
                                      horizontalalignment='right',
                                      fontweight='light'
                                      )
            elif plottype == "count":
                g = sns.countplot(x=X, data=self.graph_df)
                if type(self.graph_df.loc[0, X]) == str or type(self.graph_df.loc[0, Y]) == str:
                    g.set_xticklabels(g.get_xticklabels(), rotation=30,
                                      horizontalalignment='right',
                                      fontweight='light'
                                      )
            elif plottype == "heatmap":
                g = sns.heatmap(data=self.graph_df.corr(), annot=True, fmt='.2f', linewidths=.5, cmap="Blues")
                g.set_xticklabels(g.get_xticklabels(), rotation=30,
                                  horizontalalignment='right',
                                  fontweight='light'
                                  )
                g.set_yticklabels(g.get_yticklabels(), rotation=30,
                                  horizontalalignment='right',
                                  fontweight='light'
                                  )
            elif plottype == "dist":
                g = sns.distplot(self.graph_df[X])
            elif plottype == "pie":
                plt.pie(x=self.graph_df[X].value_counts(), labels=self.graph_df[X].value_counts().keys(),
                        autopct="%.1f%%", startangle=0)

            else:
                plt.scatter(x=X, y=Y, data=self.graph_df)
                if type(self.graph_df.loc[0, X]) == str or type(self.graph_df.loc[0, Y]) == str:
                    plt.xticks(rotation=45, size=8)
                    plt.yticks(size=8)
                plt.xlabel(X)
                plt.ylabel(Y)

            if plottype not in ["pie", "scatter"]:
                g.xaxis.set_tick_params(labelsize=7)
                g.yaxis.set_tick_params(labelsize=7)
            plt.title("<{} Graph>".format(plottype), fontweight="bold", fontsize=20)
            canvas = FigureCanvas(fig)
            canvas.draw()
            self.graphLayout.addWidget(canvas)
            canvas.show()

        except:
            print("error")
            pass

    def show_map(self):
        self.hideAll()
        self.webEngineView.show()
        if self.checkEmart.isChecked() and self.checkHome.isChecked() and self.checkLotte.isChecked():
            self.webEngineView.load(QUrl.fromLocalFile(os.path.abspath("./Html/three_mart_folium.html")))
        elif self.checkEmart.isChecked():
            if self.checkLotte.isChecked():
                self.webEngineView.load(QUrl.fromLocalFile(os.path.abspath("./Html/emart_lotte_folium.html")))
            elif self.checkHome.isChecked():
                self.webEngineView.load(QUrl.fromLocalFile(os.path.abspath("./Html/hp_emart_folium.html")))
            else:
                self.webEngineView.load(QUrl.fromLocalFile(os.path.abspath("./Html/emart_folium.html")))
        elif self.checkHome.isChecked():
            if self.checkLotte.isChecked():
                self.webEngineView.load(QUrl.fromLocalFile(os.path.abspath("./Html/hp_lotte_folium.html")))
            else:
                self.webEngineView.load(QUrl.fromLocalFile(os.path.abspath("./Html/hp_folium.html")))
        elif self.checkLotte.isChecked():
            self.webEngineView.load(QUrl.fromLocalFile(os.path.abspath("./Html/lotte_folium.html")))

        self.checkEmart.setChecked(False)
        self.checkHome.setChecked(False)
        self.checkLotte.setChecked(False)

    def show_result(self):
        self.hideAll()
        self.verticalLayoutWidget.show()
        self.plainTextResult.show()
        self.resultWidget.show()
        self.resultWidget.horizontalHeader().setStyleSheet(
            "QHeaderView::section {background-color:#D9E5FF;color:#000000;}")
        self.resultWidget.horizontalHeader().setStretchLastSection(True)
        self.resultWidget.verticalHeader().setStyleSheet(
            "QHeaderView::section {background-color:#D9E5FF;color:#000000;}")
        if self.brand == "E":
            self.result = pd.DataFrame(columns=["지점명", "폐점확률"])
            self.df = pd.read_excel("./Data/preprocessing/E/binning.xlsx")
            LR = joblib.load("./model/emart.pk1")

            for i, v in enumerate(np.round(LR.predict_proba(robust_scale(self.df.iloc[:, 2:-1])), 3)):

                if i < 138:
                    self.result.loc[i, "지점명"] = self.df.iloc[i, 1]
                    self.result.loc[i, "폐점확률"] = v[0]
            columns = list(map(str, self.result.keys()))
            self.result = self.result.astype(str)
            item_count = len(self.result[columns[0]])
            self.resultWidget.setRowCount(item_count)
            self.resultWidget.setColumnCount(len(columns))
            self.resultWidget.setHorizontalHeaderLabels(columns)
            for j in range(item_count):
                row = self.result.iloc[j, :]
                for i in range(len(row)):
                    item = QTableWidgetItem(row[i])
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    self.resultWidget.setItem(j, i, item)

            self.resultWidget.resizeRowsToContents()

            f = open("./txt_file/emart.txt", "r", encoding="UTF-8")
            lines = f.readlines()
            lines = "".join(lines)
            self.plainTextResult.setPlainText(lines)
            f.close()
        elif self.brand == "ET":
            self.result = pd.DataFrame(columns=["지점명", "전환확률"])
            self.df = pd.read_excel("./Data/preprocessing/ET/binning.xlsx")
            LR = joblib.load("./model/emart_tr.pk1")
            for i, v in enumerate(np.round(LR.predict_proba(robust_scale(self.df.iloc[:, 2:-1])), 3)):

                if i < 22:
                    self.result.loc[i, "지점명"] = self.df.iloc[i, 1]
                    self.result.loc[i, "전환확률"] = v[1]
            columns = list(map(str, self.result.keys()))
            self.result = self.result.astype(str)
            item_count = len(self.result[columns[0]])
            self.resultWidget.setRowCount(item_count)
            self.resultWidget.setColumnCount(len(columns))
            self.resultWidget.setHorizontalHeaderLabels(columns)
            for j in range(item_count):
                row = self.result.iloc[j, :]
                for i in range(len(row)):
                    item = QTableWidgetItem(row[i])
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    self.resultWidget.setItem(j, i, item)

            self.resultWidget.resizeRowsToContents()

            f = open("./txt_file/emart_tr.txt", "r", encoding="UTF-8")
            lines = f.readlines()
            lines = "".join(lines)
            self.plainTextResult.setPlainText(lines)
            f.close()

        elif self.brand == "H":
            self.result = pd.DataFrame(columns=["지점명", "폐점확률"])
            self.df = pd.read_excel("./Data/preprocessing/H/binning.xlsx")
            LR = joblib.load("./model/homeplus.pk1")

            for i, v in enumerate(np.round(LR.predict_proba(scale(self.df.iloc[:, 2:-1])), 3)):

                if i < 119:
                    self.result.loc[i, "지점명"] = self.df.iloc[i, 1]
                    self.result.loc[i, "폐점확률"] = v[0]
            columns = list(map(str, self.result.keys()))
            self.result = self.result.astype(str)
            item_count = len(self.result[columns[0]])
            self.resultWidget.setRowCount(item_count)
            self.resultWidget.setColumnCount(len(columns))
            self.resultWidget.setHorizontalHeaderLabels(columns)
            for j in range(item_count):
                row = self.result.iloc[j, :]
                for i in range(len(row)):
                    item = QTableWidgetItem(row[i])
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    self.resultWidget.setItem(j, i, item)

            self.resultWidget.resizeRowsToContents()

            f = open("./txt_file/homeplus.txt", "r", encoding="UTF-8")
            lines = f.readlines()
            lines = "".join(lines)
            self.plainTextResult.setPlainText(lines)
            f.close()

        elif self.brand == "HS":
            self.result = pd.DataFrame(columns=["지점명", "전환확률"])
            self.df = pd.read_excel("./Data/preprocessing/HS/binning.xlsx")
            LR = joblib.load("./model/special.pk1")
            for i, v in enumerate(np.round(LR.predict_proba(robust_scale(self.df.iloc[:, 2:-1])), 3)):

                if i < 119:
                    self.result.loc[i, "지점명"] = self.df.iloc[i, 1]
                    self.result.loc[i, "전환확률"] = v[1]
            columns = list(map(str, self.result.keys()))
            self.result = self.result.astype(str)
            item_count = len(self.result[columns[0]])
            self.resultWidget.setRowCount(item_count)
            self.resultWidget.setColumnCount(len(columns))
            self.resultWidget.setHorizontalHeaderLabels(columns)
            for j in range(item_count):
                row = self.result.iloc[j, :]
                for i in range(len(row)):
                    item = QTableWidgetItem(row[i])
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    self.resultWidget.setItem(j, i, item)

            self.resultWidget.resizeRowsToContents()

            f = open("./txt_file/homeplus_special.txt", "r", encoding="UTF-8")
            lines = f.readlines()
            lines = "".join(lines)
            self.plainTextResult.setPlainText(lines)
            f.close()

        elif self.brand == "L":
            self.result = pd.DataFrame(columns=["지점명", "폐점확률"])
            self.df = pd.read_excel("./Data/preprocessing/L/binning.xlsx")
            LR = joblib.load("./model/lotte.pk1")

            for i, v in enumerate(LR.predict_proba(self.df.iloc[:, 2:-1])):
                if i < 109:
                    self.result.loc[i, "지점명"] = self.df.iloc[i, 1]
                    self.result.loc[i, "폐점확률"] = np.round(v[0], 3)
            columns = list(map(str, self.result.keys()))
            self.result = self.result.astype(str)
            item_count = len(self.result[columns[0]])
            self.resultWidget.setRowCount(item_count)
            self.resultWidget.setColumnCount(len(columns))
            self.resultWidget.setHorizontalHeaderLabels(columns)
            for j in range(item_count):
                row = self.result.iloc[j, :]
                for i in range(len(row)):
                    item = QTableWidgetItem(row[i])
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    self.resultWidget.setItem(j, i, item)

            self.resultWidget.resizeRowsToContents()

            f = open("./txt_file/lotte.txt", "r", encoding="UTF-8")
            lines = f.readlines()
            lines = "".join(lines)
            self.plainTextResult.setPlainText(lines)
            f.close()

        if self.checkBox_2.isChecked():
            self.result.sort_values(by=self.result.keys()[-1], ascending=False, inplace=True)

            columns = list(map(str, self.result.keys()))
            self.result = self.result.astype(str)
            item_count = len(self.result[columns[0]])
            self.resultWidget.setRowCount(item_count)
            self.resultWidget.setColumnCount(len(columns))
            self.resultWidget.setHorizontalHeaderLabels(columns)
            for j in range(item_count):
                row = self.result.iloc[j, :]
                for i in range(len(row)):
                    item = QTableWidgetItem(row[i])
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    self.resultWidget.setItem(j, i, item)
        if self.checkBox.isChecked():
            self.result.to_excel("./save_file/result_{}.xlsx".format(self.brand), index=False)

        for i in reversed(range(self.resultLayout.count())):
            self.resultLayout.itemAt(i).widget().setParent(None)
        fig = plt.Figure()
        ax = fig.add_subplot(111)
        a = self.result.sort_values(by=self.result.keys()[-1], ascending=False)
        ax.barh(a.iloc[:5, 0][::-1], a.iloc[:5, 1][::-1].astype(float), 0.4)
        ax.set_xticks(np.arange(0, 1.1, step=0.2))
        ax.xaxis.set_tick_params(labelsize=7)
        ax.yaxis.set_tick_params(labelsize=7, rotation=60)
        ax.set(title="<{} 상위 5개 지점>".format(a.keys()[-1]))

        canvas = FigureCanvas(fig)
        canvas.draw()
        self.resultLayout.addWidget(canvas)
        canvas.show()

        self.checkBox.setChecked(False)
        self.checkBox_2.setChecked(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    you_viewer_main = Main()
    you_viewer_main.show()
    app.exec_()

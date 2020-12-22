from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from bigmart import Ui_MainWindow
sns.set(style='darkgrid')

# font_path = 'c:/Windows/Fonts/malgun.ttf'
# font_name = font_manager.FontProperties(fname=font_path).get_name()
# rc('font', family=font_name)

class graph():
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
            plt.title("<{} Graph>".format(plottype),fontweight="bold",fontsize=20)
            canvas = FigureCanvas(fig)
            canvas.draw()
            self.graphLayout.addWidget(canvas)
            canvas.show()

        except:
            print("error")
            pass
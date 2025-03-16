import sys
import pandas as pd
import pyqtgraph as pg
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem
)
from PyQt6.QtCore import Qt
from qt_material import apply_stylesheet


class CloudDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Informe de Costos - IntegraPulse")
        self.setGeometry(100, 100, 1200, 800)

        apply_stylesheet(app, theme='dark_teal.xml')

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Cargar y procesar datos
        self.load_data()

        # Botones de navegación
        self.btn_layout = QHBoxLayout()
        self.btn_prev = QPushButton("◄ Semana Anterior")
        self.btn_prev.clicked.connect(self.prev_week)
        self.btn_next = QPushButton("Semana Siguiente ►")
        self.btn_next.clicked.connect(self.next_week)
        self.btn_layout.addWidget(self.btn_prev)
        self.btn_layout.addWidget(self.btn_next)
        layout.addLayout(self.btn_layout)

        # Gráfico de tendencias
        self.setup_chart()
        layout.addWidget(self.plot)

        # Tabla de datos
        self.setup_table()
        layout.addWidget(self.table)

        # Inicializar vista
        self.current_week = 0
        self.update_view()

    def load_data(self):
        # Cargar datos y procesar semanas
        self.df = pd.read_csv("data/simulated_metrics.csv")
        self.df['fecha'] = pd.to_datetime(self.df['fecha'])

        # Agrupar por semana
        self.df['semana'] = self.df['fecha'].dt.strftime("Semana %U-%Y")
        self.df_weekly = self.df.groupby('semana').agg({
            'cpu_promedio': 'mean',
            'costo_total': 'sum'
        }).reset_index()

    def setup_chart(self):
        self.plot = pg.PlotWidget()
        self.plot.setBackground('#2D2D2D')
        self.plot.setLabel('left', 'Costo Total (USD)', color='#FFFFFF')
        self.plot.setLabel('bottom', 'Semanas', color='#FFFFFF')
        self.plot_line = self.plot.plot(
            pen=pg.mkPen('#00FFAA', width=3),
            name="Costo Semanal"
        )
        self.plot.getAxis('left').setTextPen('#FFFFFF')
        self.plot.getAxis('bottom').setTextPen('#FFFFFF')

    def setup_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([
            "Semana",
            "CPU Promedio (%)",
            "Costo Total (USD)"
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #3D3D3D; color: #FFFFFF; }"
        )

    def update_view(self):
        # Actualizar gráfico
        weeks = range(len(self.df_weekly))
        costs = self.df_weekly["costo_total"].round(2)
        self.plot_line.setData(weeks, costs)

        # Actualizar tabla
        self.table.setRowCount(len(self.df_weekly))
        for i, row in self.df_weekly.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(row["semana"]))
            self.table.setItem(i, 1, QTableWidgetItem(f"{row['cpu_promedio']:.1f}%"))
            self.table.setItem(i, 2, QTableWidgetItem(f"${row['costo_total']:.2f}"))
            for col in range(3):
                self.table.item(i, col).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        # Resaltar y desplazar a la semana actual
        self.table.selectRow(self.current_week)
        self.table.scrollToItem(self.table.item(self.current_week, 0))

    def prev_week(self):
        if self.current_week > 0:
            self.current_week -= 1
            self.update_view()

    def next_week(self):
        if self.current_week < len(self.df_weekly) - 1:
            self.current_week += 1
            self.update_view()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CloudDashboard()
    window.show()
    sys.exit(app.exec())
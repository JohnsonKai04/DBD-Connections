
import pytesseract
import pyautogui
import os
import json
import sys
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtGui import QColor
from PIL import ImageOps
from collections import Counter
pytesseract.pytesseract.tesseract_cmd = r"E:\Tesser\tesseract.exe"

SURVIVORS = [
	"DWIGHT FAIRFIELD", "MEG THOMAS", "CLAUDETTE MOREL", "JAKE PARK",
	"NEA KARLSSON", "LAURIE STRODE", "ACE VISCONTI", "BILL OVERBECK",
	"FENG MIN", "DAVID KING", "QUENTIN SMITH", "DAVID TAPP", "KATE DENSON",
	"ADAM FRANCIS", "JEFF JOHANSEN", "JANE ROMERO", "ASH WILLIAMS",
	"NANCY WHEELER", "STEVE HARRINGTON", "YUI KIMURA", "ZARINA KASSIR",
	"CHERYL MASON", "FELIX RICHTER", "ÉLODIE RAKOTO", "LEE YUN-JIN",
	"JILL VALENTINE", "LEON SCOTT KENNEDY", "MIKAELA REID", "JONAH VASQUEZ",
	"YOICHI ASAKAWA", "HADDIE KAUR", "ADA WONG", "REBECCA CHAMBERS",
	"VITTORIO TOSCANO", "THALITA LYRA", "RENATO LYRA", "GABRIEL SOMA",
	"NICOLAS CAGE", "ELLEN RIPLEY", "ALAN WAKE", "SABLE WARD",
	"AESTRI YAZAR & BAERMAR URAZ", "LARA CROFT", "TREVOR BELMONT",
	"TAURIE CAIN", "ORELA ROSE", "RICK GRIMES", "MICHONNE GRIMES",
	"VEE BOONYASAK", "DUSTIN HENDERSON", "ELEVEN", "KWON TAE-YOUNG",
	"SHANE WIIGWAAS", "AURORA STARDOTTER", "CLAIRE REDFIELD",
]

Y = 130
X1 = 694
X2 = 940
X3 = 1155
WIDTH = 185
HEIGHT = 150
DEBUG = True
DATAFILE = "Data.json"

def returnName(playerX, img):
	results = []
	color = 100
	region = (playerX, Y, WIDTH, HEIGHT)
	img = pyautogui.screenshot(region=region)

	gray = ImageOps.grayscale(img)
	gray = gray.resize((gray.width * 6, gray.height * 6))
	if(DEBUG): gray.save(f"{playerX}_{color}_normal.png")
	if(DEBUG): img.save(f"{playerX}_color.png")


	while(color < 250):
		bw = gray.point(lambda x: 0 if x < color else 255, '1')
		color += 5
		text = pytesseract.image_to_string(bw, config="--psm 6")
		if(text == ""): continue

		for name in SURVIVORS:
			if name in text:
				text = text.split("\n", 1)[1].replace("\n", "")
				if(DEBUG): print(text)
				results.append(text)

	if not results:
		print(f"No name found for {playerX}")
		return False
	name = Counter(results)
	name = name.most_common(1)[0][0]

	return name


def loadFile():
	if not os.path.exists(DATAFILE):
		return {}
	with open(DATAFILE, "r", encoding="utf-8") as file:
		return json.load(file)


def saveFile(playerFile):
	with open(DATAFILE, "w", encoding="utf-8") as file:
		json.dump(playerFile, file, indent=4)


def incrementPlayer(playerFile, playerName):
	now = datetime.now().isoformat()
	if not playerName:
		return False
	if playerName in playerFile:
		playerFile[playerName]["count"] += 1
		playerFile[playerName]["last_seen"] = now
	else:
		playerFile[playerName] = {"count": 1, "last_seen": now}
	saveFile(playerFile)

def scanScreen(playerFile):

	img = pyautogui.screenshot()
	incrementPlayer(playerFile, returnName(X1, img))
	incrementPlayer(playerFile, returnName(X2, img))
	incrementPlayer(playerFile, returnName(X3, img))

def main():
	playerFile = loadFile()
	app = QApplication(sys.argv)

	window = QMainWindow()
	window.setWindowTitle("DBD Player Tracker")
	window.resize(500, 350)

	table = QTableWidget(len(playerFile), 2)
	table.setHorizontalHeaderLabels(["Player", "Times Seen"])
	table.verticalHeader().setVisible(False)
	table.setAlternatingRowColors(True)
	table.setEditTriggers(QTableWidget.NoEditTriggers)
	table.setSelectionBehavior(QTableWidget.SelectRows)
	table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
	table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
	table.setSelectionMode(QAbstractItemView.NoSelection)

	headerFont = QFont("Segoe UI", 11, QFont.Bold)
	table.horizontalHeader().setFont(headerFont)

	sortedList = sorted(
		playerFile.items(),
		key=lambda pair: pair[1]["last_seen"],
		reverse=True
	)
	for row, (name, count) in enumerate(sortedList):
		nameItem = QTableWidgetItem(name)
		countItem = QTableWidgetItem(str(count))
		countItem.setTextAlignment(Qt.AlignCenter)
		table.setItem(row, 0, nameItem)
		table.setItem(row, 1, countItem)

	window.setCentralWidget(table)

	app.setStyleSheet("""
		QMainWindow {
			background-color: #1e1e2e;
		}
		QTableWidget {
			background-color: #2a2a3d;
			color: #e0e0e0;
			gridline-color: #3d3d54;
			font-size: 13px;
			border: none;
			border-radius: 8px;
		}
		QTableWidget::item {
			padding: 8px;
		}
		QTableWidget::item:selected {
			background-color: #6c5ce7;
			color: white;
		}
		QHeaderView::section {
			background-color: #34344a;
			color: #ffffff;
			padding: 10px;
			border: none;
		}
		QTableWidget::item:alternate {
			background-color: #26263a;
		}
		QTableWidget::item:hover {
			background-color: #b5316c;
		}
	""")

	window.show()
	
	scanScreen(playerFile)
	sys.exit(app.exec())



if __name__ == "__main__":
	main()
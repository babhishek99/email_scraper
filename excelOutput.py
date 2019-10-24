import openpyxl

class excelOutput:
	def __init__(self, path):
		self.path = path
		self.workbook = openpyxl.Workbook()
		wb_act = self.workbook.active
		wb_act.title = "Emails"
		wb_act['A1'] = "Name"
		wb_act['B1'] = "Position"
		wb_act['C1'] = "Company"
		self.curr_row = 2
		self.workbook.save(self.path)

	def saveFile(self):
		self.workbook.save(self.path)

	def closeFile(self):
		self.workbook.close()


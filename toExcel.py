import xlsxwriter



class MyXlsheet:
    def __init__(self, _xlFilePath, _sheetName):
        self.filePath = _xlFilePath
        self.sheetName = _sheetName
        self.workbook = xlsxwriter.Workbook(_xlFilePath)
        self.worksheet = self.workbook.add_worksheet(_sheetName)
    def Write(self, row, col, data):
        self.worksheet.write(row, col,data)
    def Save(self):
        self.workbook.close()

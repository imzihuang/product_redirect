#coding:utf-8

import StringIO
import xlwt as ExcelWrite  # 引入模块

def make_excel(data_array):
        if not data_array:
            return ''
        xls = ExcelWrite.Workbook(style_compression=2)
        sheet = xls.add_sheet("Sheet1")
        flag_header = False
        row = 1
        #填充每行的数据
        for data in data_array:
            col = 0
            if not flag_header:
                flag_header = True
                for k in data:
                    sheet.write(0, col, k)
                    col += 1
            col = 0
            for k, v in data.items():
                sheet.write(row, col, v)
                col += 1
            row += 1
        sf = StringIO.StringIO()
        xls.save(sf)
        contents = sf.getvalue()
        sf.close()
        return contents

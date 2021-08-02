#coding:utf-8
import xlsxwriter
class Exhelp():
    def __init__(self):
        pass 

    def MakeSaveEx(self,sname,sl):
        # 创建一个excel
        workbook = xlsxwriter.Workbook(sname+".xlsx")
        # 创建一个sheet
        worksheet = workbook.add_worksheet(sname)
        # worksheet = workbook.add_worksheet("bug_analysis")
 
        # 自定义样式，加粗
        bold = workbook.add_format({'bold': 1})
 
        # --------1、准备数据并写入excel---------------
        # 向excel中写入数据，建立图标时要用到
        headings = ['id','光强', '温度', '时间']
        #<UsbRecord(usbname='%s', size='%s', upath='%s',ddwsize='%s',ddwtime='%s',ddwspeed='%s',ddrsize='%s',ddrtime='%s',ddrspeed='%s',intime='%s',outtime='%s',testtime='%s',testdate='%s')>
        # 写入表头
        worksheet.write_row('A1', headings, bold)
 
        # 写入数据
        slen=len(sl)
        for i in range(0,slen):
            e=sl[i]
            worksheet.write('A'+str(2+i), e.id)
            worksheet.write('B'+str(2+i), float(e.lvalue))
            worksheet.write('C'+str(2+i), float(e.ltmp))
            worksheet.write('D'+str(2+i), e.ldate)
        # --------2、生成图表并插入到excel---------------
        # 创建一个柱状图(line chart)
        chart_col = workbook.add_chart({'type': 'line'})
 
        # 配置第一个系列数据
        chart_col.add_series({
            # 这里的sheet1是默认的值，因为我们在新建sheet时没有指定sheet名
            # 如果我们新建sheet时设置了sheet名，这里就要设置成相应的值
            'name': '光强曲线',
            'categories': '='+sname+'!$D$2:$D$'+str(2+slen),
            'values':   '='+sname+'!$B$2:$B$'+str(2+slen),
            'line': {'color': 'red'},
        })
 
        # 设置图表的title 和 x，y轴信息
        chart_col.set_title({'name': '光强曲线'})
        chart_col.set_x_axis({'name': '时间'})
        chart_col.set_y_axis({'name':  '光强'})
 
        # 设置图表的风格
        chart_col.set_style(1)
 
        # 把图表插入到worksheet并设置偏移
        worksheet.insert_chart('N10', chart_col, {'x_offset': 25, 'y_offset': 10})

        # --------3、生成图表并插入到excel---------------
        # 创建一个柱状图(line chart)
        chart_col2 = workbook.add_chart({'type': 'line'})
 
        # 配置第一个系列数据
        chart_col2.add_series({
            # 这里的sheet1是默认的值，因为我们在新建sheet时没有指定sheet名
            # 如果我们新建sheet时设置了sheet名，这里就要设置成相应的值
            'name': '光机温度曲线',
            'categories': '='+sname+'!$D$2:$D$'+str(2+slen),
            'values':   '='+sname+'!$C$2:$C$'+str(2+slen),
            'line': {'color': 'blue'},
        })
 
        # 设置图表的title 和 x，y轴信息
        chart_col2.set_title({'name': '光机温度曲线'})
        chart_col2.set_x_axis({'name': '时间'})
        chart_col2.set_y_axis({'name':  '温度'})
 
        # 设置图表的风格
        chart_col2.set_style(1)
 
        # 把图表插入到worksheet并设置偏移
        worksheet.insert_chart('N30', chart_col2, {'x_offset': 25, 'y_offset': 10})
        workbook.close()


#ex=Exhelp()
#ex.MakeSaveEx()
    

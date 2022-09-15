import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

Window.size = (900,900)

Builder.load_file('style.kv')

class MyLayout(TabbedPanel):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        global box
        global more
        global pieG
        global FCum
        
        FCum = self.ids.FCum
        pieG = self.ids.pieG
        more = self.ids.more
        box = self.ids.box
        
        
    def saveImg(self):
        pass
    
    global spent
    global gain
    
    spent = {
        "amount":[],
        "reason":[],
        "date":[]
    }
    gain  = {
        "amount":[],
        "reason":[],
        "date":[]
    }

    def selected(self,filename) ->bool:
        try:
            gain['amount'].clear()
            gain['date'].clear()
            gain['reason'].clear()
            spent['amount'].clear()
            spent['date'].clear()
            spent['reason'].clear()
            global data
            
            if '.csv' in str(filename[0]):
                data = pd.read_csv(filename[0],index_col='date', parse_dates=True)
            
            elif '.json' in str(filename[0]):
                data = pd.read_json(filename[0],index_col='date', parse_dates=True)
                
            elif '.xml' in str(filename[0]):
                data = pd.read_xml(filename[0],index_col='date', parse_dates=True)
                
            elif '.xls' in str(filename[0]):
                data = pd.read_excel(filename[0],index_col='date', parse_dates=True)
            
            elif '.sql' in str(filename[0]):
                data = pd.read_sql(filename[0],index_col='date', parse_dates=True)
                
            elif '.html' in str(filename[0]):
                data = pd.read_html(filename[0],index_col='date', parse_dates=True)

            else:
                print('Invalid file format')
                exit(1)
            
            try:
                data = data.dropna(axis=0)
            except:
                Window.close()
            
            gain['amount'] = data['gainAmount']
            gain['reason'] = data['gainReason']
            
            gain['date'] = data['date']
            spent['date'] = data['date']
            
            spent['amount'] = data['sptAmount']
            spent['reason'] = data['sptReason']
            
                
        except:
            pass
    
    def addData(self):
        gainAmount = self.ids.inpResAmount.text
        gainDay = self.ids.inpDay.text
        gainReason = self.ids.inpResReason.text
        
        sptAmount = self.ids.inpSptAmount.text
        sptReason = self.ids.inpSptReason.text
        
        if gainDay != '':
            if gainAmount == '' or gainReason == '':
                gainAmount = 0
                gainReason = 'no gain'
            
            if sptAmount == '' or sptReason == '':
                sptAmount = 0
                sptReason = 'no spent'
            
            if len(gain['amount']) != 0:
                added = False
                for i in range(len(gain['date'])):
                    if gain['date'][i] > int(gainDay):
                        gain['date'].insert(i, int(gainDay))
                        gain['amount'].insert(i, int(gainAmount))
                        gain['reason'].insert(i, gainReason)
                        
                        spent['date'].insert(i, int(gainDay))
                        spent['amount'].insert(i, int(sptAmount))
                        spent['reason'].insert(i, sptReason)
                        
                        added = True
                        break
                    
                if not added:
                    gain['amount'].append(int(gainAmount))
                    gain['reason'].append(gainReason)
                    gain['date'].append(int(gainDay))
                    
                    spent['amount'].append(int(sptAmount))
                    spent['reason'].append(sptReason)
                    spent['date'].append(int(gainDay))
        
            else:            
                gain['amount'].append(int(gainAmount))
                gain['reason'].append(gainReason)
                gain['date'].append(int(gainDay))
                
                spent['amount'].append(int(sptAmount))
                spent['reason'].append(sptReason)
                spent['date'].append(int(gainDay))
                        
            print(gain['amount'])
            print(gain['date'])
            print(gain['reason'])
            print(spent['amount'])
            print(spent['date'])
            print(spent['reason'])
            
        self.ids.inpSptReason.text = ''
        self.ids.inpSptAmount.text = ''
        self.ids.inpResReason.text = ''
        self.ids.inpResAmount.text = ''
        self.ids.inpDay.text = ''
    
        def sumAmount(data)-> float:
                sumAm = 0
                for i in range(len(data)):
                    sumAm += int(data[i])
                
                return sumAm
            
        def meanAmount(data)-> float:
            return sumAmount(data)/len(data)
        
        def varianceAm(data)-> float:
            return sumAmount(math.pow(x-meanAmount(data),2) for x in data)/len(data)
        def stdAmount(data)-> float:
            return math.sqrt(varianceAm(data))

        def harmonicMean(ls,col):
            den = 0
            for i in range(ls.shape[0]):
                den += 1/(ls.iloc[i,col])
                
            return ls.shape[0]/den
        
    
        if len(gain["amount"]) != 0:

            self.ids.sumS.text = f'Sum spent: {str(sumAmount(spent["amount"]))}'
            self.ids.sumG.text = f'Sum gain: {str(sumAmount(gain["amount"]))}'
            
            self.ids.meanG.text = f'Mean gain: {str(meanAmount(gain["amount"]))}'
            self.ids.meanS.text = f'Mean spent: {str(meanAmount(spent["amount"]))}'

            self.ids.stdG.text = f'Std gain: {str(stdAmount(gain["amount"]))}'
            self.ids.stdS.text = f'Std spent: {str(stdAmount(spent["amount"]))}'
    
    def upStat(self):
        
        if len(gain["amount"]) != 0:
            
            self.ids.sumS.text = f'Sum spent: {str(data["gainAmount"].sum())}'
            self.ids.sumG.text = f'Sum gain: {str(data["sptAmount"].sum())}'
            
            self.ids.meanG.text = f'Mean gain: {str(data["gainAmount"].mean())}'
            self.ids.meanS.text = f'Mean spent: {str(data["sptAmount"].mean())}'

            self.ids.stdG.text = f'Std gain: {str(data["gainAmount"].std())}'
            self.ids.stdS.text = f'Std spent: {str(data["sptAmount"].std())}'
            
            self.ids.minG.text = f'Min gain: {str(data["gainAmount"].min())}'
            self.ids.minS.text = f'Min spent: {str(data["sptAmount"].min())}'

            self.ids.maxG.text = f'Max gain: {str(data["gainAmount"].max())}'
            self.ids.maxS.text = f'Max spent: {str(data["sptAmount"].max())}'
        
        print(data.describe())
               
    def freq(self):
        dataG = data.drop(['sptAmount','sptReason'],axis=1)
        dataS = data.drop(['gainAmount','gainReason'],axis=1)
        dataGFreq = dataG['gainReason'].value_counts()/data.shape[0] 
        dataSFreq = dataS['sptReason'].value_counts()/data.shape[0] 
        self.ids.countG.text = f'{dataGFreq}'
        self.ids.countS.text = f'{dataSFreq}'
        
        plt.figure(figsize=(6,6))
        
        plt.subplot(2,1,1)
        dataGFreq.plot.bar(subplots=True)
        plt.xlabel('reason')
        plt.ylabel('frequency')
        plt.title('Frequency of each reason of gain')        
        # FCum.add_widget(FigureCanvasKivyAgg(plt.gcf()))    
        
        plt.subplot(2,1,2)
        dataSFreq.plot.bar(subplots=True)
        plt.ylabel('frequency')
        plt.xlabel('reason')
        plt.title('Frequency of each reason of spending')

        FCum.add_widget(FigureCanvasKivyAgg(plt.gcf()))    
        
    def count(self):
        dataG = data.drop(['sptAmount','sptReason'],axis=1)
        dataS = data.drop(['gainAmount','gainReason'],axis=1)
        dataGCount = dataG['gainReason'].value_counts()
        dataSCount = dataS['sptReason'].value_counts()
        self.ids.countS.text = f'{dataSCount}'
        self.ids.countG.text = f'{dataGCount}'
        
    def sumA(self):
        dataG = data.drop(['sptAmount','sptReason'],axis=1)
        dataS = data.drop(['gainAmount','gainReason'],axis=1)
        dataGSum = dataG.groupby(["gainReason"]).sum()
        dataSSum = dataS.groupby(["sptReason"]).sum()
        self.ids.countS.text = f'{dataSSum}'
        self.ids.countG.text = f'{dataGSum}'
        
    def moreGraph(self):
        dataG = data.drop(['sptAmount','sptReason'],axis=1)
        dataS = data.drop(['gainAmount','gainReason'],axis=1)
        
        plt.figure(figsize=(6,6))
        dataG.groupby(["gainReason"]).sum().plot.pie(subplots=True)
        plt.title('Gain Amount pie chart')
        pieG.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        dataS.groupby(["sptReason"]).sum().plot.pie(subplots=True)
        plt.title('Spent Amount pie chart')
        more.add_widget(FigureCanvasKivyAgg(plt.gcf())) 
        
    def graph(self):
        
        plt.figure(figsize=(6,6))
        data['sptAmount'].cumsum().plot(label="cumsum of money spent", c="red")
        data['gainAmount'].cumsum().plot(label="cumsum of money gained", c="green")
        rest = data['gainAmount'].cumsum()-data['sptAmount'].cumsum()
        rest.plot(label="cumsum of remaining money", c="orange")
        plt.ylabel("Amount of money(ar)")
        plt.xlabel("Day")
        plt.legend()
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
                   
class MoneyApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    MoneyApp().run()



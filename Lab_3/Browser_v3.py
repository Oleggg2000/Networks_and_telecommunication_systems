import wx
from wx import html2

class MyFrame(wx.Frame):
    def __init__(self, parent, title, id):
        super().__init__(parent, title=title, size=(600,300))
        self.browser = wx.html2.WebView.New(self)
        browser = self.browser
        self.id = id

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        back_button = wx.Button(self, label="Назад")
        forward_button = wx.Button(self, label="Вперед")
        self.url_bar = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, value="http://")

        self.Bind(wx.EVT_BUTTON, self.goBack, back_button)
        self.Bind(wx.EVT_BUTTON, self.goForward, forward_button)
        self.Bind(wx.EVT_TEXT_ENTER, self.goUrl, self.url_bar)

        self.Bind(html2.EVT_WEBVIEW_NEWWINDOW, self.addWin)

        hbox.Add(back_button)
        hbox.Add(forward_button)
        hbox.Add(self.url_bar, proportion=1)

        vbox.Add(hbox, flag=wx.EXPAND)

        vbox.Add(self.browser, proportion=1, flag=wx.EXPAND)

        self.SetSizer(vbox)

    def goBack(self, event):
        self.browser.GoBack()
    def goForward(self, event):
        self.browser.GoForward()
    def goUrl(self, event):
        self.browser.LoadURL(self.url_bar.Value)
    def addWin(self, event):
        print(self.id)
        if self.id == 1:
            frame2.browser.LoadURL(event.GetURL())
        elif self.id == 2:
            frame1.browser.LoadURL(event.GetURL())

app = wx.App()
frame1 = MyFrame(None, '1_Window', 1)
frame2 = MyFrame(None, "2_Window", 2)
frame1.Show()
frame2.Show()
app.MainLoop()
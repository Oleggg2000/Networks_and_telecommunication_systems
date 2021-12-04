import wx
from wx import html2
import threading

class MyApp(wx.App):
    def OnInit(self):
        WebFrame(None, "Surfing the Web").Show()
        return True


class WebFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)

        self._browser = html2.WebView.New(self)
        self._browser.LoadURL("www.google.com")  # home page
        self._bar = NavBar(self, self._browser)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._bar, 0, wx.EXPAND)
        sizer.Add(self._browser, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.Bind(html2.EVT_WEBVIEW_TITLE_CHANGED, self.OnTitle)

    def OnTitle(self, event):
        self.Title = event.GetString()


class NavBar(wx.Panel):
    def __init__(self, parent, browser):
        super().__init__(parent)

        self.browser = browser
        self._url = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self._url.SetHint("Введите URL сюда и нажмите enter...")
        self._url.Bind(wx.EVT_TEXT_ENTER, self.onEnter)

        back = wx.Button(self, style=wx.BU_EXACTFIT, label="Назад")
        back.Bind(wx.EVT_BUTTON, self.goBack)

        forward = wx.Button(self, style=wx.BU_EXACTFIT, label="Вперед")
        forward.Bind(wx.EVT_BUTTON, self.goForward)

        add = wx.Button(self, style=wx.BU_EXACTFIT, label="+")
        forward.Bind(wx.EVT_BUTTON, self.addWindow)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(back, proportion=0, flag=wx.ALL, border=5)
        sizer.Add(forward, proportion=0, flag=wx.ALL, border=5)
        sizer.Add(add, proportion=0, flag=wx.ALL, border=5)
        sizer.Add(window=self._url, proportion=1, flag=wx.EXPAND)

        self.SetSizer(sizer)


    def onEnter(self, event):
        self.browser.LoadURL(self._url.Value)

    def goBack(self, event):
        self.browser.GoBack()

    def goForward(self, event):
        self.browser.GoForward()

    def addWindow(self, event):
        secwin = threading.Thread(target=self.addWindow)
        app2 = MyApp()
        app2.MainLoop()
        secwin.start()



if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
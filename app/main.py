from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp  # For Material Design components like a toolbar

# Import WebView
from kivy_garden.webview import WebView

KV = '''
BoxLayout:
    orientation: 'vertical'

    MDTopAppBar:  # A toolbar at the top
        title: "My Website"
        left_action_items: [["arrow-left", lambda x: app.go_back()]]
        elevation: 10

    WebView:  # Embed the web browser
        id: webview
'''

class WebViewApp(MDApp):
    def build(self):
        self.root = Builder.load_string(KV)

        # Load your website
        self.root.ids.webview.url = "https://yourwebsite.com"
        return self.root

    def go_back(self):
        # Handle the "back" button in the toolbar
        webview = self.root.ids.webview
        if webview.can_go_back:
            webview.go_back()

# Run the app
if __name__ == "__main__":
    WebViewApp().run()


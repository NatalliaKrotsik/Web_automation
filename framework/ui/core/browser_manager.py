from playwright.sync_api import sync_playwright

class BrowserManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BrowserManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self,browser_type = "chromium", headless = True):
        if hasattr(self, 'initialized') and self.initialized:
            return
        self.browser_type = browser_type
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.initialized = True

    def start(self):
        if not self.playwright:
            self.playwright = sync_playwright().start()
        if not self.browser:
                if self.browser_type == "chromium":
                    self.browser = self.playwright.chromium.launch(headless=self.headless)
                elif self.browser_type == "firefox":
                    self.browser = self.playwright.firefox.launch(headless=self.headless)
                elif self.browser_type == "webkit":
                    self.browser = self.playwright.webkit.launch(headless=self.headless)
                else:
                    raise ValueError(f"Unsupported browser type: {self.browser_type}")
                
        if not self.context:
            self.context = self.browser.new_context()
        if not self.page:
            self.page = self.context.new_page()

        return self.page
    
    def stop(self):
        if self.context:
            self.context.close()
            self.context = None
        if self.browser:
            self.browser.close()
            self.browser = None
        if self.playwright:
            self.playwright.stop()
            self.playwright = None
        BrowserManager._instance = None
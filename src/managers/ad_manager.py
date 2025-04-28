from kivy.utils import platform
from kivy.logger import Logger

class AdManager:
    def __init__(self, app_id):
        self.app_id = app_id
        self.is_android = platform == 'android'
        
        if self.is_android:
            try:
                from jnius import autoclass
                self.AdView = autoclass('com.google.android.gms.ads.AdView')
                self.AdRequest = autoclass('com.google.android.gms.ads.AdRequest')
                self.AdSize = autoclass('com.google.android.gms.ads.AdSize')
                self.activity = autoclass('org.kivy.android.PythonActivity').mActivity
                Logger.info('AdManager: Successfully initialized for Android')
            except Exception as e:
                Logger.warning(f'AdManager: Failed to initialize Android components: {str(e)}')
                self.is_android = False
        else:
            Logger.info('AdManager: Running in development mode (non-Android platform)')

    def show_banner(self):
        if not self.is_android:
            Logger.info('AdManager: Banner ads are only available on Android')
            return

        try:
            # Create and configure AdView
            ad_view = self.AdView(self.activity)
            ad_view.setAdSize(self.AdSize.BANNER)
            ad_view.setAdUnitId(self.app_id)

            # Create an AdRequest
            ad_request = self.AdRequest.Builder().build()
            ad_view.loadAd(ad_request)

            # Add the AdView to the activity layout
            self.activity.addContentView(ad_view, ad_view.getLayoutParams())
            Logger.info('AdManager: Banner ad displayed successfully')
        except Exception as e:
            Logger.error(f'AdManager: Error showing banner ad: {str(e)}')

    def hide_banner(self):
        if not self.is_android:
            Logger.info('AdManager: Hide banner is only available on Android')
            return
        
        Logger.info('AdManager: Hide banner not yet implemented for Android')
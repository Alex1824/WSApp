from kivy.utils import platform
from kivy.logger import Logger

class ContactManager:
    def __init__(self):
        self.contacts = []
        self.is_android = platform == 'android'
        
        if self.is_android:
            try:
                from jnius import autoclass
                self.Context = autoclass('android.content.Context')
                self.Cursor = autoclass('android.database.Cursor')
                self.ContactsContract = autoclass('android.provider.ContactsContract')
                self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Logger.info('ContactManager: Successfully initialized for Android')
            except Exception as e:
                Logger.warning(f'ContactManager: Failed to initialize Android components: {str(e)}')
                self.is_android = False
        else:
            Logger.info('ContactManager: Running in development mode (non-Android platform)')

    def get_contacts(self):
        """Retrieve contacts from the device"""
        if not self.is_android:
            return []

        try:
            activity = self.PythonActivity.mActivity
            cr = activity.getContentResolver()
            projection = [
                self.ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME,
                self.ContactsContract.CommonDataKinds.Phone.NUMBER
            ]
            cursor = cr.query(
                self.ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
                projection,
                None,
                None,
                self.ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME + " ASC"
            )

            contacts = []
            while cursor.moveToNext():
                name = cursor.getString(0)
                number = cursor.getString(1)
                contacts.append({'name': name, 'number': number})

            cursor.close()
            self.contacts = contacts
            return contacts
        except Exception as e:
            Logger.error(f'ContactManager: Error getting contacts: {str(e)}')
            return []

    def search_contacts(self, query):
        """Search contacts by name or number"""
        query = query.lower()
        return [
            contact for contact in self.contacts
            if query in contact['name'].lower() or query in contact['number']
        ]

try:
    from jnius import autoclass
    is_android = True
except ImportError:
    is_android = False

class AndroidApi:
    def share_file(file_path):
        """Partage un fichier via une autre application"""
        if not is_android:
            return

        Intent = autoclass("android.content.Intent")
        File = autoclass("java.io.File")
        Uri = autoclass("android.net.Uri")
        FileProvider = autoclass("androidx.core.content.FileProvider")
        currentActivity = autoclass("org.kivy.android.PythonActivity").mActivity
        context = currentActivity.getApplicationContext()

        file = File(file_path)
        uri = FileProvider.getUriForFile(context, context.getPackageName() + ".fileprovider", file)

        intent = Intent(Intent.ACTION_SEND)
        intent.setType("text/plain")
        intent.putExtra(Intent.EXTRA_STREAM, uri)
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)

        chooser = Intent.createChooser(intent, "Partager le fichier...")
        currentActivity.startActivity(chooser)
    
    def ouvrir_fichier(file_path, mime_type="application/pdf"):
        if not is_android:
            print("Non Android")
            return

        Intent = autoclass("android.content.Intent")
        File = autoclass("java.io.File")
        Uri = autoclass("android.net.Uri")
        FileProvider = autoclass("androidx.core.content.FileProvider")
        currentActivity = autoclass("org.kivy.android.PythonActivity").mActivity
        context = currentActivity.getApplicationContext()

        file = File(file_path)
        uri = FileProvider.getUriForFile(context, context.getPackageName() + ".fileprovider", file)

        intent = Intent(Intent.ACTION_VIEW)
        intent.setDataAndType(uri, mime_type)
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)

        chooser = Intent.createChooser(intent, "Ouvrir avec...")
        currentActivity.startActivity(chooser)


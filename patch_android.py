import os

manifest_path = "android/app/src/main/AndroidManifest.xml"
if os.path.exists(manifest_path):
    with open(manifest_path, "r", encoding="utf-8") as f:
        m = f.read()
    perms = """
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="28" />
"""
    if "ACCESS_FINE_LOCATION" not in m:
        m = m.replace("</manifest>", perms + "\n</manifest>")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(m)

main_act = "android/app/src/main/java/com/xiaomi/geostamp22101316g/MainActivity.java"
if os.path.exists(main_act):
    java_code = """package com.xiaomi.geostamp22101316g;

import android.os.Bundle;
import android.os.Environment;
import android.util.Base64;
import android.webkit.JavascriptInterface;
import android.widget.Toast;
import android.media.MediaScannerConnection;
import android.Manifest;
import android.content.pm.PackageManager;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import com.getcapacitor.BridgeActivity;
import java.io.File;
import java.io.FileOutputStream;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}, 101);
        }
        this.bridge.getWebView().addJavascriptInterface(new AndroidDownloader(), "AndroidDownloader");
    }

    public class AndroidDownloader {
        @JavascriptInterface
        public void saveImage(String dataUrl, String filename) {
            try {
                String base64Data = dataUrl.contains(",") ? dataUrl.split(",")[1] : dataUrl;
                byte[] imageBytes = Base64.decode(base64Data, Base64.DEFAULT);
                File dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
                if (!dir.exists()) dir.mkdirs();
                File outFile = new File(dir, filename);
                FileOutputStream fos = new FileOutputStream(outFile);
                fos.write(imageBytes);
                fos.flush();
                fos.close();
                MediaScannerConnection.scanFile(MainActivity.this, new String[]{outFile.getAbsolutePath()}, new String[]{"image/jpeg"}, null);
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "Berhasil disimpan di Download/Galeri: " + filename, Toast.LENGTH_LONG).show());
            } catch (Exception e) {
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "Gagal menyimpan: " + e.getMessage(), Toast.LENGTH_LONG).show());
            }
        }
    }
}
"""
    with open(main_act, "w", encoding="utf-8") as f:
        f.write(java_code)
print("Android native project patched successfully.")

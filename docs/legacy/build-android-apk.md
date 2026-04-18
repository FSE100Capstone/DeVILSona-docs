<html>
<body>
<!--StartFragment--><html><head></head><body><hr><h1>📱 Unreal Engine Android Packaging Guide (UE 5.6 ~ 5.7)</h1><h2>📌 Overview</h2><p>This guide explains the full process of packaging an Unreal Engine project into an Android APK and installing it on a Meta Quest device.<br>It covers environment setup, packaging, and deployment.</p><hr><h2>🧩 Requirements</h2><h3>✅ Unreal Engine</h3><ul><li><p>Version: <strong>5.6 ~ 5.7</strong></p></li></ul><hr><h3>✅ Android Studio</h3><ul><li><p>Version: <strong>Koala 2024.1.2 Patch 1 (Sep 17, 2024)</strong></p></li><li><p>Download:<br><a href="https://developer.android.com/studio/archive?hl=de">https://developer.android.com/studio/archive?hl=de</a></p></li></ul><hr><h3>✅ Android SDK / NDK</h3>
Component | Version

Recommended SDK | 35

Minimum Compile SDK | 34

Target SDK | 34

Minimum SDK | 26

NDK | r27c  (29.0.13113456)

Build Tools | 35.0.1

Java | OpenJDK 21.0.3

<hr><h2>⚙️ 1. Install Android SDK &amp; NDK (Turnkey)</h2><p>Official Guide:</p><ul><li><p><a href="https://dev.epicgames.com/documentation/en-us/unreal-engine/set-up-android-sdk-ndk-and-android-studio-using-turnkey-for-unreal-engine?application_version=5.6">https://dev.epicgames.com/documentation/en-us/unreal-engine/set-up-android-sdk-ndk-and-android-studio-using-turnkey-for-unreal-engine?application_version=5.6</a></p></li></ul><h3>Steps:</h3><ol><li><p>Open Unreal Engine</p></li><li><p>Go to <code inline="">Edit → Project Settings</code></p></li><li><p>Navigate to <code inline="">Platforms → Android</code></p></li><li><p>Click <strong>"Install SDK"</strong></p></li></ol><p>👉 This ensures correct versions and avoids conflicts.</p><hr><h2>⚙️ 2. Environment Variables</h2><p>Verify the following:</p><pre><code>JAVA_HOME = C:\Program Files\Android\Android Studio\jbr
ANDROID_HOME = C:\Users\&lt;Username&gt;\AppData\Local\Android\Sdk
NDK_ROOT = C:\Users\&lt;Username&gt;\AppData\Local\Android\Sdk\ndk\&lt;NDK Version&gt;
NDKROOT = C:\Users\&lt;Username&gt;\AppData\Local\Android\Sdk\ndk\&lt;NDK Version&gt;
</code></pre><h3>Check via terminal:</h3><pre><code class="language-powershell">echo %JAVA_HOME%
echo %ANDROID_HOME%
</code></pre><hr><h2>⚙️ 3. Configure SDK Paths in Unreal</h2><pre><code>Edit → Project Settings → Platforms → Android → Android SDK
</code></pre><p>If Unreal does not detect paths automatically, set:</p><ul><li><p>SDK Path</p></li><li><p>NDK Path</p></li><li><p>JDK Path</p></li></ul><hr><h3>🔧 Manual Config (Advanced)</h3><pre><code class="language-ini">[/Script/AndroidPlatformEditor.AndroidSDKSettings]
SDKPath=(Path="C:\Android\Sdk")
NDKPath=(Path="C:\Android\Sdk\ndk\r27c")
JDKPath=(Path="C:\Program Files\Android\Android Studio\jbr")
</code></pre><hr><h2>⚙️ 4. Project Settings</h2><pre><code>Project Settings → Platforms → Android
</code></pre><h3>Required Settings</h3><ul><li><p><strong>Package Game Data Inside APK</strong> → ✅ Enabled</p></li><li><p>Target SDK Version → 34</p></li><li><p>Minimum SDK Version → 26</p></li></ul><hr><h3>Recommended Settings</h3><ul><li><p>Build Configuration → <strong>Shipping</strong></p></li><li><p>Full Rebuild → Enabled (recommended for clean builds)</p></li></ul><hr><h2>⚙️ 5. Package the Project</h2><h3>Method</h3><pre><code>File → Package Project → Android
</code></pre><p>or</p><pre><code>Platforms → Android → Package Project
</code></pre><hr><h3>Output Path</h3><pre><code>&lt;Project&gt;/Saved/StagedBuilds/Android_ASTC/
</code></pre><hr><h2>🎮 6. Install on Meta Quest (SideQuest)</h2><p>Use SideQuest to install the APK.</p><hr><h3>📦 Build Output Notes</h3><p>Inside:</p><pre><code>Android_ASTC/
</code></pre><p>You will typically see <strong>multiple APK files</strong>.</p><hr><h3>⚠️ Important Rule</h3><p>👉 Always choose the <strong>largest APK file</strong></p><ul><li><p>❌ Small APK → incomplete (missing assets / requires OBB)</p></li><li><p>✅ Large APK → fully packaged (includes all data)</p></li></ul><hr><h3>📲 Installation Steps</h3><ol><li><p>Connect Meta Quest to PC</p></li><li><p>Open SideQuest</p></li><li><p>Ensure device shows as <strong>connected (green)</strong></p></li><li><p>Click <strong>"Install APK file"</strong> or drag &amp; drop APK</p></li><li><p>Select the <strong>largest APK</strong></p></li></ol><hr><h3>🚀 Run the App</h3><p>On Meta Quest:</p><pre><code>App Library → Unknown Sources → Launch
</code></pre><hr><h2>⚠️ Troubleshooting</h2><p>Official Guide:<br><a href="https://dev.epicgames.com/documentation/en-us/unreal-engine/advanced-setup-and-troubleshooting-guide-for-using-android-sdk?application_version=5.6">https://dev.epicgames.com/documentation/en-us/unreal-engine/advanced-setup-and-troubleshooting-guide-for-using-android-sdk?application_version=5.6</a></p><hr><h3>❌ SDK Not Found</h3><ul><li><p>Verify <code inline="">ANDROID_HOME</code></p></li><li><p>Set SDK path manually</p></li></ul><hr><h3>❌ NDK Version Mismatch</h3><ul><li><p>Use <strong>NDK r27c only</strong></p></li><li><p>Remove other versions</p></li></ul><hr><h3>❌ Gradle Build Failure</h3><pre><code class="language-bash">cd &lt;Project&gt;/Intermediate/Android
gradlew clean
</code></pre><hr><h3>❌ Plugin Issues (MetaXR / OpenXR)</h3><ul><li><p>Disable unsupported plugins for Android</p></li><li><p>Especially:</p><ul><li><p>OpenXR (conflicts sometimes)</p></li><li><p>MetaXR (version mismatch → crash)</p></li></ul></li></ul><hr><h3>❌ Java Errors</h3><ul><li><p>Ensure JDK = OpenJDK 21</p></li><li><p>Verify <code inline="">JAVA_HOME</code></p></li></ul><hr><h2>🧠 Best Practices</h2><ul><li><p>Always use <strong>Turnkey installation</strong></p></li><li><p>Lock SDK / NDK versions (no mixing)</p></li><li><p>Use <strong>Android_ASTC build only</strong></p></li><li><p>Enable:</p><pre><code>Package Game Data Inside APK
</code></pre><p>→ ensures single APK deployment</p></li></ul><hr><h2>📌 Final Checklist</h2><ul class="contains-task-list"><li class="task-list-item"><p><input type="checkbox" disabled=""> Android Studio installed</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> SDK / NDK installed via Turnkey</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> Environment variables set</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> Unreal SDK paths verified</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> ASTC build selected</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> Packaging successful</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> Installed via SideQuest</p></li></ul><hr><h2>🔚 Conclusion</h2><p>Most Android build failures come from:</p><ul><li><p>Incorrect SDK path</p></li><li><p>Wrong NDK version</p></li><li><p>Misconfigured environment variables</p></li></ul><p>👉 Fix those three, and builds become stable and predictable.</p><hr></body></html><!--EndFragment-->
</body>
</html>
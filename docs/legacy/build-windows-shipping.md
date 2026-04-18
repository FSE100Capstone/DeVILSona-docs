<html>
<body>
<!--StartFragment--><h2 data-start="662" data-end="673">Overview</h2>
<p data-start="675" data-end="778">This document explains how to package the project as a <strong data-start="730" data-end="756">Windows Shipping build</strong> in Unreal Engine 5.x.</p>
<hr data-start="780" data-end="783">
<h1 data-start="785" data-end="809">1. Pre-Packaging Setup</h1>
<h2 data-start="811" data-end="848">1.1 Add Maps to the Packaged Build</h2>
<p data-start="850" data-end="862">Navigate to:</p>
<pre class="overflow-visible! px-0!" data-start="864" data-end="917"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Edit → Project Settings → Project → Packaging</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>
<p data-start="919" data-end="1010">Under <strong data-start="925" data-end="972">List of Maps to Include in a Packaged Build</strong>, click <code data-start="980" data-end="983">+</code> and add all required maps:</p>
<pre class="overflow-visible! px-0!" data-start="1012" data-end="1097"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>/Game/Maps/MainMenu</span><br><span>/Game/Maps/InterviewScene</span><br><span>/Game/Maps/Town</span><br><span>/Game/Maps/Mart</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>
<p data-start="1099" data-end="1109">Important:</p>
<ul data-start="1110" data-end="1210">
<li data-start="1110" data-end="1140">
<p data-start="1112" data-end="1140">Include the Game Default Map</p>
</li>
<li data-start="1141" data-end="1174">
<p data-start="1143" data-end="1174">Include streamed/sub-level maps</p>
</li>
<li data-start="1175" data-end="1210">
<p data-start="1177" data-end="1210">Missing maps will not be packaged</p>
</li>
</ul>
<hr data-start="1212" data-end="1215">
<h2 data-start="1217" data-end="1243">1.2 Verify Default Maps</h2>
<p data-start="1245" data-end="1257">Navigate to:</p>
<pre class="overflow-visible! px-0!" data-start="1259" data-end="1298"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Project Settings → Maps &amp; Modes</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>
<p data-start="1300" data-end="1307">Verify:</p>
<ul data-start="1308" data-end="1347">
<li data-start="1308" data-end="1328">
<p data-start="1310" data-end="1328">Editor Startup Map</p>
</li>
<li data-start="1329" data-end="1347">
<p data-start="1331" data-end="1347">Game Default Map</p>
</li>
</ul>
<hr data-start="1349" data-end="1352">
<h1 data-start="1354" data-end="1382">2. Set Build Configuration</h1>
<p data-start="1384" data-end="1408">Switch to Shipping mode:</p>
<pre class="overflow-visible! px-0!" data-start="1410" data-end="1470"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Platforms → Windows → Build Configuration → Shipping</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>
<p data-start="1472" data-end="1475">Or:</p>
<pre class="overflow-visible! px-0!" data-start="1477" data-end="1552"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Edit → Project Settings → Packaging</span><br><span>→ Build Configuration: Shipping</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>
<h3 data-start="1554" data-end="1569">Build Modes</h3>
<div class="TyagGW_tableContainer"><div tabindex="-1" class="group TyagGW_tableWrapper flex flex-col-reverse w-fit">
Mode | Purpose
-- | --
DebugGame | Debugging
Development | Testing
Shipping | Final distribution

</div></div>
<p data-start="1697" data-end="1740">Always use <strong data-start="1708" data-end="1720">Shipping</strong> for release builds.</p>
<hr data-start="1742" data-end="1745">
<h1 data-start="1747" data-end="1771">3. Package the Project</h1>
<p data-start="1773" data-end="1789">Start packaging:</p>
<pre class="overflow-visible! px-0!" data-start="1791" data-end="1836"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Platforms → Windows → Package Project</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>
<p data-start="1838" data-end="1875">Choose an output folder, for example:</p>
<pre class="overflow-visible! px-0!" data-start="1877" data-end="1911"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>D:\Builds\FSE100_Shipping\</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>
<hr data-start="1913" data-end="1916">
<h1 data-start="1918" data-end="1939">4. Output Structure</h1>
<p data-start="1941" data-end="1967">After packaging completes:</p>
<pre class="overflow-visible! px-0!" data-start="1969" data-end="2046"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Windows\</span><br><span> ├── ProjectName.exe</span><br><span> ├── ProjectName\</span><br><span> ├── Engine\</span><br><span> └── ...</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>
<p data-start="2048" data-end="2052">Run:</p>
<pre class="overflow-visible! px-0!" data-start="2054" data-end="2077"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>ProjectName.exe</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>
<p data-start="2079" data-end="2140">Important:<br>
Distribute the entire folder, not just the <code data-start="2133" data-end="2139">.exe</code>.</p>
<hr data-start="2142" data-end="2145">
<h1 data-start="2147" data-end="2182">5. Recommended Packaging Settings</h1>
<p data-start="2184" data-end="2196">Navigate to:</p>
<pre class="overflow-visible! px-0!" data-start="2198" data-end="2234"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Project Settings → Packaging</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>
<p data-start="2236" data-end="2243">Enable:</p>
<ul data-start="2245" data-end="2321">
<li data-start="2245" data-end="2259">
<p data-start="2247" data-end="2259">Use Pak File</p>
</li>
<li data-start="2260" data-end="2283">
<p data-start="2262" data-end="2283">Include Prerequisites</p>
</li>
<li data-start="2284" data-end="2321">
<p data-start="2286" data-end="2321">Full Rebuild (before final release)</p>
</li>
</ul>
<hr data-start="2323" data-end="2326">
<h1 data-start="2328" data-end="2352">6. Common Build Issues</h1>
<h2 data-start="2354" data-end="2373">Maps Not Loading</h2>
<ul data-start="2375" data-end="2446">
<li data-start="2375" data-end="2420">
<p data-start="2377" data-end="2420">Ensure maps are added to the packaging list</p>
</li>
<li data-start="2421" data-end="2446">
<p data-start="2423" data-end="2446">Verify Game Default Map</p>
</li>
</ul>
<hr data-start="2448" data-end="2451">
<h2 data-start="2453" data-end="2476">Shipping Build Crash</h2>
<p data-start="2478" data-end="2496">Check <code data-start="2484" data-end="2495">.uproject</code>:</p>
<p data-start="2498" data-end="2508">Incorrect:</p>
<pre class="overflow-visible! px-0!" data-start="2510" data-end="2580"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼr">"AdditionalDependencies"</span><span>: [</span><br><span>    </span><span class="ͼr">"Engine"</span><span>,</span><br><span>    </span><span class="ͼr">"UnrealEd"</span><br><span>]</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>
<p data-start="2582" data-end="2590">Correct:</p>
<pre class="overflow-visible! px-0!" data-start="2592" data-end="2646"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼr">"AdditionalDependencies"</span><span>: [</span><br><span>    </span><span class="ͼr">"Engine"</span><br><span>]</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>
<p data-start="2648" data-end="2697">UnrealEd must NOT be included in Shipping builds.</p>
<hr data-start="2699" data-end="2702">
<h1 data-start="2704" data-end="2734">7. Recommended Team Workflow</h1>
<ol data-start="2736" data-end="2897">
<li data-start="2736" data-end="2758">
<p data-start="2739" data-end="2758">Pull latest changes</p>
</li>
<li data-start="2759" data-end="2784">
<p data-start="2762" data-end="2784">Test Development build</p>
</li>
<li data-start="2785" data-end="2806">
<p data-start="2788" data-end="2806">Switch to Shipping</p>
</li>
<li data-start="2807" data-end="2829">
<p data-start="2810" data-end="2829">Enable Full Rebuild</p>
</li>
<li data-start="2830" data-end="2840">
<p data-start="2833" data-end="2840">Package</p>
</li>
<li data-start="2841" data-end="2859">
<p data-start="2844" data-end="2859">Test executable</p>
</li>
<li data-start="2860" data-end="2888">
<p data-start="2863" data-end="2888">Zip entire Windows folder</p>
</li>
<li data-start="2889" data-end="2897">
<p data-start="2892" data-end="2897">Share</p>
</li>
</ol>
<!--EndFragment-->
</body>
</html>
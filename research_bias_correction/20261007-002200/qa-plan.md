# Exact final QA scenarios

Tool: functions.eval JS + browser skill omowright owned Chrome. No user profile, login or site data touched.

## Desktop content
Invocation: qaBrowser.newTab('file:///D:/WORK/Projects/omo/Glosea6/research_bias_correction/20261007-002200/report.html'); omowright.emulate(qaPage,{width:1280,height:900,deviceScaleFactor:1,mobile:false,hasTouch:false}); await document.fonts.ready; decode all document.images.
PASS iff actual innerWidth1280, document.scrollWidth<=innerWidth,93source anchors, loadedNotoSansKR and qualitativeimage natural360×700, and personally inspected captures readable.
Artifacts: assets/qa/desktop-*.png, boxes.json.

## Mobile content
Invocation: omowright.emulate(qaPage,{width:390,height:844,deviceScaleFactor:1,mobile:true,hasTouch:true}); same readiness/decode.
PASS iff actual innerWidth390, no bodyhorizontaloverflow/overlap/missingcontent,17comparisonmethods retained as labeled responsive rows, personally inspected header/table/details/decision/source captures readable.
Artifacts: assets/qa/mobile-*.png, boxes-mobile.json.

## Citation navigation
Invocation: fixviewportbeforeinteraction; registerwindow.addEventListener('hashchange',once:true) intoaPromise with10000msfailuretimeout viaqaPage.evaluate,thenqaPage.locator('a[href="#source-6"]').first().click(); awaitactualwindowhashsignal. Repeat '#src-project-p1' with matching lowercase anchor.
PASS iff hash matches and referenced element exists/in viewport; allcitationfragmenttargets resolve. SourceP1 points to newestlocalprojectmetadata, not guessedforeignstudy.
Artifacts: qa-verdict.md actionlog + source/project screenshots.

Driver correction: omowright.waitForURLusescachedpage.url()thatdidnotincludehashchange,soitfailedwhileactualdocument.location.hashcorrectlychanged. Nativehashchangesubscriptionisusedinstead;PASSobservableandHTMLtargetunchanged.

## Dark-mode surfaces
Invocation: qaPage.cdp.send('Emulation.setEmulatedMedia',{features:[{name:'prefers-color-scheme',value:'dark'}]},await qaPage.resolveSessionId()); emulate bothwidthsabove and captureheader/table/figure.
PASS iff exactwidths, readablecontrast, diagramcontained, nooverlap/bodyoverflow. Light reset uses value'light'.

## Official gates and proofreading
Invocation: report-tools-commands.mjs runCheck([reportPath,'--design-spec',specPath,'--layout',boxesPath]); runOutcome gate static/layout/visual/proofread pass onlyaftercleanobservations; dedicatednativeKoreanproofreading task finaltext.
PASS iff no unresolvedstatic/layoutdefects, observedpixels pass and proofread defectlistempty orallfixed, outcome verify exit0.

## Cleanup
Invocation: await qaBrowser.close(); fs.rm(qaProfile,{recursive:true,force:true}); fs.stat(qaProfile) failsENOENT; processprobe matchingownedprofile absent. Allteamsdeleted/allworkers terminal.
PASS iff noownedbrowser/profile/monitor/server/port remains. Captures are promisedresearchartifacts, not transientruntimeprofiles.

# Research report design contract

## Scope and intent
Offline Korean analytical report, not a new web application or a React component project. Content and research evidence govern design. No marketing imagery, animation or external services required to read the report.

## Tokens
Use design-spec.md palette. Neutral paper with restrained teal accent, dark readable text; system dark mode uses darkneutralbackground/lighttext. Type: local embedded Korean sans webfont if obtainable, Malgun Gothic fallback.
Spacing:8/16/24/32/48px. Body18px, lineheight1.8; headline clamp26–42px; section24px. maxwidth1120; prosemeasure74ch. Table cells16px.

## Content anatomy
Executive decision first, explicit applicability caveat next, compact comparison table, detailed method family sections, prioritized experiments, verification design, limits, ranked/full sources, methods.

## Reusable primitives
mainarticle; sectionheading; recommendationcallout; methodcomparisonrow; detailsparagraph; citedformula; qualitativedecisionfigure; sourceitem. Real semantic DOM, no screenshot-as-report.
Internal source links have visiblefocusoutline and generous lineheight. Responsive table turns rows into labeled stacked cells at700px; no primarybodyhorizontaloverflow. Codeformula wraps. No stickyoverlay/navigation.

## Figure standard
Decisionfigure has fixed-heightcontainer, caption, accessibletext; SVGobjectfitscontain, samefont/palette. It conveys goals and dependencies, NOT fabricated numericperformance.

## Accessibility and responsive states
langko; meaningfultitle; article/mainlandmarks; accessibleSVGdescription. Offlinebodycomplete. Light/dark desktop/mobile captures. Source URLswrapanywhere, no hiddencontent.

## Accepted limits
No productappstates/forms/modals needed; N/A. No userauth/sessiondataused. Print/PDFnotpromisedunlessuserchangesformat. One staticHTMLplusMarkdown.

## QA contract
Reportstaticchecker→DOMlayoutprobe→full-contentviewportcaptures→independentvisualchecks→Koreanproofread. Manifestrecordsallgates; actualbrowserclosedaftercapture.

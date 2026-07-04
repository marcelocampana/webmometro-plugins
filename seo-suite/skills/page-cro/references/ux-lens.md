# UX Lens for Conversion Analysis

This reference defines UX aspects relevant to conversion analysis within page-cro. It provides the evaluation framework for the "UX Findings" section of the CRO output.

page-cro integrates UX criteria as an analytical lens — it does not depend on the ux-designer skill. If ux-designer is updated, this file can be updated manually, but there is no automatic dependency.

## Usability

Evaluate whether the page allows users to accomplish their goal with minimal friction:

- **Task clarity**: Is it immediately obvious what the user is supposed to do on this page? Can the primary action be identified within 3 seconds?
- **Interaction predictability**: Do interactive elements behave as expected? Are clickable elements visually distinct from non-clickable ones?
- **Error prevention**: Are form validations inline? Are destructive actions protected with confirmation?
- **Recovery**: If a user makes a mistake (wrong plan selected, wrong field filled), how easy is it to recover?

## Information Hierarchy

Evaluate whether content is organized to support decision-making:

- **Visual priority**: Does the most important content (value proposition, primary CTA) have the strongest visual weight?
- **Scanning support**: Can a user who skims (not reads) still get the core message? Are key points in headings, bold text, or visual callouts?
- **Cognitive load**: Is the user asked to process too much at once? Are choices overwhelming (too many plans, too many features, too many CTAs)?
- **Progressive disclosure**: Is detailed information available on demand (expandable sections, tooltips) rather than forced upfront?

## Friction Points

Identify elements that slow down or prevent conversion:

- **Form friction**: Unnecessary fields, unclear labels, missing field-level validation, phone number required without clear reason
- **Navigation friction**: No clear path back, breadcrumbs missing, user gets lost in the flow
- **Trust friction**: No security signals near forms, unclear data usage, no privacy indicators
- **Technical friction**: Slow load times, layout shifts during interaction, broken interactive elements
- **Decision friction**: Too many options without guidance, missing comparison tools, no recommended option highlighted

## Task Clarity

Evaluate whether users understand what will happen next:

- **CTA specificity**: Does the button tell the user what happens when they click? "Solicitar demo" is better than "Enviar." "Ver planes" is better than "Más información."
- **Process transparency**: If the user is entering a multi-step flow, do they know how many steps remain?
- **Outcome expectations**: After clicking the primary CTA, is the expected outcome clear? (Will I see a calendar? Will I get an email? Will I start a trial?)

## Microcopy

Evaluate the small text that guides behavior:

- **Labels**: Are form field labels clear and unambiguous?
- **Helper text**: Is there contextual help where users might hesitate?
- **Error messages**: Are errors specific and actionable? "Este campo es obligatorio" vs. "Ingresa tu correo para recibir acceso"
- **Reassurance text**: Near conversion points, is there text that reduces anxiety? ("Sin compromiso," "Cancela cuando quieras," "No necesitas tarjeta de crédito")

## Accessibility

Evaluate basic accessibility factors that affect conversion:

- **Color contrast**: Are CTAs and important text readable against their background?
- **Touch targets**: On mobile, are buttons and links large enough to tap reliably (minimum 44×44px)?
- **Keyboard navigation**: Can the conversion flow be completed without a mouse?
- **Screen reader basics**: Do form fields have labels? Do images have meaningful alt text?

Accessibility matters for conversion because inaccessible elements are, by definition, unconvertible for the users they exclude.

## Flow Structure and Objection Recovery

Evaluate the page's ability to guide hesitant users toward conversion:

- **Objection anticipation**: Does the page address common objections (price, complexity, commitment) before the user encounters the final CTA?
- **Objection placement**: Are FAQ, testimonials, and guarantees placed where doubt is likely to peak (after pricing, before form submission)?
- **Recovery paths**: If a user scrolls past the primary CTA without converting, are there secondary conversion opportunities further down?
- **Exit alternatives**: If the primary conversion (demo, trial) feels too committal, is there a lower-commitment alternative (newsletter, resource download)?

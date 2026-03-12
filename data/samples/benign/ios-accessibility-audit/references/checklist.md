# iOS Accessibility Checklist

## Touch Targets
- Minimum 44x44pt for all interactive elements.
- Adequate spacing between adjacent controls.

## VoiceOver and Labels
- Every control has an `accessibilityLabel`.
- Icon-only actions include `accessibilityHint` when needed.
- Groups use `accessible` to avoid noisy focus order.

## Focus Order
- Focus follows visual order (top-to-bottom, left-to-right).
- No hidden elements receive focus.

## Dynamic Type
- Text supports scaling via `allowFontScaling`.
- Layout does not break at larger text sizes.

## Contrast
- Text meets contrast for normal and large text.
- Disabled states remain legible.

## Motion
- Reduced motion is respected for animations.
- Motion is not required to understand state.

## Color Usage
- State is not conveyed by color alone.
- Error and success states have text or icon reinforcement.

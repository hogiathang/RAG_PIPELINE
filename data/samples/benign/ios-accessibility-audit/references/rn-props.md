# RN/Expo Accessibility Props

- Labels: `accessibilityLabel`, `accessibilityHint`.
- Roles: `accessibilityRole` (button, link, header, image).
- Grouping: `accessible` to group related content.
- State: `accessibilityState` for disabled, selected, checked.
- Dynamic Type: `allowFontScaling` on `Text` and avoid fixed heights.
- Reduced motion: check `AccessibilityInfo.isReduceMotionEnabled()` and avoid heavy transitions.

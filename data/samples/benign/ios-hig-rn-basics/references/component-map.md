# RN/Expo Mapping Cheatsheet

- Safe areas and scrolling: `ScrollView` or `FlatList` with `contentInsetAdjustmentBehavior="automatic"`.
- Insets and layout: prefer flexbox and `useWindowDimensions` over hard-coded sizes.
- Colors: `PlatformColor` or `DynamicColorIOS` for semantic system colors.
- Icons: `expo-symbols` for SF Symbols.
- Haptics: `expo-haptics` for confirmation feedback.
- Blur and translucency: `expo-blur` when needed.
- Text scaling: set `allowFontScaling` on `Text` and avoid fixed heights for text blocks.

# Frontend Updates (Tinder-style Feed)

## Overview
I have transformed the `HomeFeed` component to support a "Swipeable Card" interface using `framer-motion`. This aligns with the user request for a Tinder-like experience where:
-   **Right Swipe**: "Like" / Interested.
-   **Left Swipe**: "Dislike" / Not Interested.
-   **Chat Button**: Context-aware chat about the specific card.

## Components Added/Modified

1.  `frontend/components/SwipeableCard.tsx`:
    -   New component handling drag gestures, rotation, and opacity.
    -   Displays "INTERESTED" (Green) and "SKIP" (Red) stamps on swipe.
    -   Includes "Chat", "Like", and "Dislike" action buttons.

2.  `frontend/components/HomeFeed.tsx`:
    -   Now manages a stack of `feed` items.
    -   Handles swipe logic (`handleSwipe`) to remove cards and log history.
    -   Handles chat logic (`handleChat`) to extract context from the card and pass it up.

3.  `frontend/components/ChatOverlay.tsx`:
    -   Updated to accept a `context` prop.
    -   Uses this context to seed the simulated LLM response (ready for real backend integration).

4.  `frontend/app/page.tsx`:
    -   Updated to manage `chatContext` state and pass it to the overlay.

## Interaction Flow
1.  User sees a stack of cards.
2.  User swipes right on "GST Rules".
3.  Card flies off, "Liked" is logged.
4.  User clicks "Chat" on "OpenAI Ads".
5.  `ChatOverlay` opens with `initialQuery="Tell me more..."` and `context="User is asking about OpenAI Ads..."`.
6.  Assistant responds contextually.


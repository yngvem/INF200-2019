# Advanced Python Programming
The lecture notes will be posted here, and the course information will be posted on
[GitHub pages](https://yngvem.github.io/INF200-2019).

## Links

 * [GitHub Pages](https://yngvem.github.io/INF200-2019)
 * [Mandatory coursework](https://github.com/yngvem/INF200-2019-Exersices)
 * [YouTube Channel](https://www.youtube.com/channel/UC8XWLPrXyqHWKHzBMMRnWlw)
 * [Reccomended reading](https://www.oreilly.com/library/view/fluent-python/9781491946237/)
   (not part of the course)

## Lecturer and TA GitHub usernames
These usernames should be added as colaborators on your GitHub page

 * yngvem
 * huynhngoc
 * danielambrosius

There will be a third TA added soon.



## Clock patience

### Rules of the game

- Standard deck of 52 cards
- Special values
    - Ace: 1
    - Jack: 11
    - Queen: 12
    - King: 13
- Deal one card to each clock position
    - Begin at 1 o'clock
    - Place 13th card in center
- Continue to deal in clockwise order fashion, center last
    - If the top card at a position has the same value as the clock position, it is *locked*: the position is skipped when dealing
- The game is over if either
    - all position are locked
    - all cards have been dealt
- The game is a success if all positions are locked


### Task

**Simulate the game to determine the probablity of success.**

#### Questions / Suggestions

1. Play the game a few times with a real deck of cards.
1. Which major parts could you divide the game into?
1. How can you represent a playing card in Python?
1. How can you create and shuffle a deck of cards?
1. How can you represent the stack of cards in Python?
1. How can you represent the clock face with its 13 positions?
1. How do you test if a position is locked?
1. What do you need to do when a position becomes locked?
1. How do you check whether the game is finished?
1. How do you check whether it was successful?
1. How do you keep track of the number of successful games?
1. How often do you need to play the game to determine the probability of success?

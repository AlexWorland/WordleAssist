# Wordle Assistant

This python script that suggests words for the internet game Wordle `https://www.powerlanguage.co.uk/wordle/`

## Instructions

To play, simply start up the script with `python wordle.py` then follow the prompts. If you wish to continue to the next word, answer `n` to the `New Random? (y/n):` prompt. Then answer `y` to the `Continue? (y/n)` prompt.

### Prompt Format

For `New Valid Letters:`, please enter the letters which are colored yellow or green. If there are none, simple press enter.

For `New Invalid Letters:`, please enter the letter which are color gray. 
It is important NOT to enter the letters that were previously yellow or green (such as words with duplicate letters) as this will break the program.

For `New Valid Letter Positions:` enter the letters which are green and have not been entered before. An example for correct formatting for the word WORDLE where R and E are colored green would be: `R2E4`. Note: For the time being, words are 0-indexed.

For `New Invalid Positions:` enter the letters and positions of yellow letters that have no occured in that column before following the same format as above. Note: sometimes a letter previously colored yellow can appear as gray. One must enter these in this step as well.

## Theory

The overall theory of this script is to take the set of all 5 letter words and continually remove words that do not fit the letter and positional restrictions discovered during previous tries.

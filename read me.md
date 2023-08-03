# alt-parts
## A Badger2040 app for plural people


### /alt-parts/parts.json example

``{
    "label": {
        "name": "Display Name",
        "pronouns": "They / Them",
        "pips": "4",
        "tag": "I'm the coolest one of us"
    }
}`` 

label - each label needs to be unique, if there is a matching .jpg file in the /alt-parts/ directory it will display that in the bottom right 64px of the screen, it will not scale so will only who the top left 64px most of the image, if there is no matching image file it will display the default image

name - the name that you want displayed in the top row of the screen ( max 8 characters )

pronouns - medium sized text displayed under your name ( max 10 characters )

pips - the pips space can display beween 0 and 4 pips with half pips, so this accepts any number between 0 and 8, numbers higher than 8 will just display 4 full pips, non-numbers or numbers less than 0 will display no pips 

tag - some fun text to be displayed at the bottom of the screen, under pronouns ( max 2 lines of 20 characters, but wrapping will make this less )
# BeeTeam
Code for BeeTeam2023

Programmet ligger och kör var femte sekund där det läser från en given mapp och sparar undan till det som filen sparas till. Innan programmet körs behövs mappen "bees" "birds" "wind" och "other" skapas där de analyserade filerna sparas. 

Syntax för att kära igång programmet är: 

Initialise the input arguments
\n
Run command syntax: 
run main.py folder_path remove_file kupa_nr 
Where: 
Folder_path = (string) path of folder on raspberry pi where the program reads the files 
remove_file = (boolean) True if the program should remove the read file from the folder otherwise False
kupa_nr = (int) number to indicate on which beehive the program is running, this to communicate correctly with OWL. 
0 = sound_Apiary-LE_1
1 = sound_Apiary-LE_2
2 = sound_Apiary-LE_3
3 = sound_Beehive-LN

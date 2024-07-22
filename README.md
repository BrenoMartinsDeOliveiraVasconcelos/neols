# neols

Python tool to display files from a folder. It displays its name, mime type, size and Unix permission mask.
# How to run
Clone the repo and them run `python3 list.py <PATH>`
It should output something like this:
![Screenshot](https://i.imgur.com/5dP8OuQ.png)

## Colors

### Colors at mime column
On the mime column, each kind of filesystem entity has its own color. Here's the table explaining each color:
|Color|Meaning  |
|--|--|
| GREEN | Directory |
| CYAN | File |
| YELLOW | Symbolic link |
| PURPLE | Others |


## Args

All your files and folders are presented as a tree in the file explorer. You can switch from one to another by clicking a file in the tree.

## Rename a file

 ### path
 Path of the folder. Exemple: `python3 list.py /usr/bin`
 ### chars
 This argument defines how many characters will be used for spacing. Default is 0.
 Defining it as '0' makes the program define that value dynamically.
 Example:
 
    python3 list.py . --chars 15 
  ![--chars](https://i.imgur.com/LTNi5QD.png)
   ### unit
  Change the unit of the size column. Measured in how big the unit is from 1 to infinite. Default is 2 (kilobit).
  
|Number|Unit  |
|--|--|
| 1 | b |
| 2 | kb |
| 3 | mb |
| 4 | gb |
| 5 | tb |

Example:

    python3 list.py . --unit 3
![--unit](https://i.imgur.com/PbQy3nW.png)
### real
Toggle showing the real size of a directory (instead of the inode file size). Depending of the folder, this can significantly slow the program. Default is false.
Exemple:

    python3 list.py . --real true
![--real](https://i.imgur.com/lcMMJ2e.png)

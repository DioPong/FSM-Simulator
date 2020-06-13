# FSM-Simulator 

> #### A File-System-Manager based on Python3, witch is simulate with UFS.

----

### Commands Support :) 🍋

----

| Commands | Remark| Status ✔ |
| :-: | :-: | :-: |
| login |      |      |
| logout |      |      |
| Initialization | Similar to reboot |  |
| create | Create file |  |
| open |      |      |
| read/cat | read file |  |
| write | write doc to file |  |
| close | close file |  |
| rm/delete | remove file or doc |  |
| mkdir | create new doc |  |
| cd | switch current route |  |
| dir | list current file route |  |
| stat | show system info |  |
| Administrator | | |

#### File Tree should be like this 🎄

```
FSM
 ├─ Super Block
 │   └─ System information
 └─ File Manager
 |	 └─ Inode Manager
 |	 |   ├─ Inode
 |	 |   └─ Inode map
 |   └─ Block Manager
 |       ├─ Data block
 |       └─ Block map
 └─ User Manager
     └─ user
```
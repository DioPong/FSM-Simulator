# FSM-Simulator 

> #### A File-System-Manager based on Python3.7+, witch is simulate with UFS.

----

### Commands Support :) 🍋

----

| Commands | Parameter? | Remark| Status ✔ |
| :-: | :-: | :-: | :-: |
| Administrator |  | Add new user | 😑 |
| register | name/password | with op (e.g. admin) | 😑 |
| login | name/password |      | 😑 |
| logout | - |      | 😑 |
| ~~Initialization~~ |  | ~~Similar to reboot~~ |  |
| create | file name | Create file | 😭 |
| open |  | QAQ | 😭 |
| read/cat |  | read file | ✔ |
| write |  | write doc to file |  |
| close |  | QAQ | 😭 |
| rm/delete |  | remove file or doc | ✔ |
| mkdir |  | create new doc | ✔ |
| cd |  | switch current route | ✔ |
| dir |  | list current file route | ✔ |
| stat |  | show file info (size, inode index) | ✔ |
| upload | | upload file from local disk | ✔ |
| download | | download file from simulator | ✔ |


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
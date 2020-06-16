# FSM-Simulator (Python) 

> #### I'm so vegetable yeah. 
>
> #### A File-System-Manager based on Python3.7+, witch is simulate with UFS.

## Usage

Run FSM-server first by executing:

> python FSM-server.py

then run FSM-client by executing in another terminal:

> python FSM-client.py

## File tree should be like this 

```bash
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

### Commands Support :) 

> Commit: ✔: Already done. ❓: Feel puzzle.  😭: Can be finish is remain versions

| SYSTEM Commands | Parameter? | Remark| Status |
| :-: | :-: | :-: | :-: |
|       Admin        |               |      Only admin can register       |          |
| register | name/password | with op (e.g. admin) | ✔ |
| login | name/password |      | ✔ |
| logout | - | Logout and switch to guest |  |
| ~~Initialization~~ | - |  | ~~null~~ |
|       mkdir        | folder name |           create new doc           |    ✔     |
|         cd         | route |        switch current route        |    ✔     |
|        dir         | - |      list current file route       |          |
|        stat        | file name | show file info (size, inode index) |    ✔     |
|     rm/delete      | folder/file name |         remove file or folder         |    ✔     |

----

| FILE Commands | Parameter? | Remark| Status |
| :-: | :-: | :-: | :-: |
| create | file name | Create file | 😭 |
| download | file name | download file from simulator |  |
| upload | file name | upload file from local disk |  |
| read/cat | file name | read file |  |
| open | file name | QAQ | ❓ |
| close | - | QAQ | ❓ |
|     write     |            |      write doc to file       |   😭    |

----

## Bugs 🥦

> - [0x0]- Switch User's handle can only be accessed after execute command: register.
> - [0x1]- User data cannot be save is user-folder.
> - [0x2]- Admin can be assign. Should be solved by resolving [0x1]
> - [0x3]- Cannot delete account appropriately.
>




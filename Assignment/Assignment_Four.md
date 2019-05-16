## Question One:

```dot
digraph G {
    Student[label = "Student", shape = "box"]
    namepkgrade[label = "name&grade", shape = "box"]
    CrushInfo[label = "CrushInfo", shape = "box"]
    length[lable = " length", shape = "box"]
    {Student, namepkgrade} -> {CrushInfo, length} [label = "HasCrush, *"]
    {Student} -> {namepkgrade}
    {namepkgrade} -> {Student}
    {CrushInfo} -> {length}
    {length} -> {CrushInfo}
}
```
![Q1.png](https://i.loli.net/2019/05/05/5ccf0752d09f7.png)

## Question Two:
Overlapping (e.g., Fiction and and Children) and complete (all books are Fiction or Nonfiction).

## Question Three:

team(t_id, t_name)
player(p_id, p_name, p_birthdate)
play(t_id, p_id, p_date, score)
g􏰃oal􏰀(t_id, p􏰁_id, ti􏰄me, 􏰁perio􏰃d)
belong(t_id, p_id, start, end)
```dot
graph G {
    team[label = "team", shape = "box"]
    play[label = "play", shape = "box"]
    player[label = "player", shape = "box"]
    belong[label = "belong", shape = "box"]
    belong -- team
    team -- play[label = "host"]
    play -- team[label = "guest"]
    play -- goal
    goal -- time
    goal -- period
    player -- belong
    player -- p_id
    player -- p_name
    player -- goal
    player -- p_birthdate
    belong -- start
    belong -- end
}
```
![Q3.png](https://i.loli.net/2019/05/05/5ccf075304b26.png)

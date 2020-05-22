
# Life Is Good
> _It's cool, man, got red bottoms on  
Life is good, you know what I mean? Like_

Let the 8-bit rendition of Future's "Life Is Good" take your mind back to a simpler time. Those year 8 days, playing Naruto MUGEN after school on a Tuesday with Jamal. 

Life was good, but life is better. 

Life Is Good is a Naruto fighting game made using the tkinter library for Python. The project is a hobby for when I want to procrastinate.

<img src="https://github.com/DonCharlesLambert/Life-Is-Good/blob/master/sprites/ss3.gif?raw=true" style="margin:auto" width="60%" alt="Gif showing gameplay"/>


## Get it Running
1. Open Terminal  

2. Clone the Repo  
`C:\> git clone https://github.com/DonCharlesLambert/Life-Is-Good`  

3. Enter the Repo  
`C:\> cd LifeIsGood`  

4. Install the required libraries  
`C:\LifeIsGood> pip install -r requirements.txt`  

5. Run the Game  
`C:\LifeIsGood> python LifeIsGood.py`  

<img src="https://github.com/DonCharlesLambert/Life-Is-Good/blob/master/sprites/ss.png?raw=true" style="margin:auto" width="60%" alt="Screenshot From the Game"/>

## Controls
|w |a |d | space |
|--|--|--|--|
|jump| left | right | attack |


## Progress

 - [x] Basic character animation
 - [x] Music
 - [x] Basic character fight mechanism
 - [x] Basic character jump mechanism
 - [x] Health bar reflecting health
 - [ ] End fight screen
 - [ ] Character select screen
 - [ ] Main Menu
 - [ ] Story mode


## Info
So I never planned to add two-player, but I did. If you follow the code you can see how to turn it on and off programmatically until I add the menus.

The first argument is whether or not the fighter is an AI or not, just change one of them to True to play against an AI, or change both to True to watch two AI play against each other.
```python  
self.player_one = self.create_sasori(False, self.PLAYER_ONE_POSITION)  
self.player_two = self.create_deidara(False, self.PLAYER_TWO_POSITION)
```
You can also change which method is invoked in order to play as other characters:

```python
self.create_kisame(False, self.PLAYER_ONE_POSITION)
self.create_kakashi(True, self.PLAYER_ONE_POSITION)
self.create_itachi(True, self.PLAYER_ONE_POSITION)
```

<img src="https://github.com/DonCharlesLambert/Life-Is-Good/blob/master/sprites/ss2.png?raw=true" style="margin:auto" width="60%" alt="An AI vs AI battle"/>
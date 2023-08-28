---
title: How to build a RPG game with JavaScript
description: The process to plan, develop and deploy a basic RPG game made with JavaScript
pubDate: 2022-02-07
heroImage: 'https://raw.githubusercontent.com/Dawichi/hexakill/main/showcase.png'
tags: ['javascript', 'game']
---

A few months ago I came up with the idea of creating a game in JavaScript.

I had no knowledge about game programming up to that point and I was afraid of how a system with so many variables and interactions could be made from 0. Here I'll walk you through the process I went through to create this project, what problems I ran into, and how to avoid them.

Check the result here: [hexakill.vercel.app](https://hexakill.vercel.app/single) 🎉🎉🎉

## 1. Planing

My first impresion when trying to build it, was that going straight into a web version might be too intimidating, so I spent a few days testing things out in a basic terminal version which you can find here: [hexakill-cli](https://github.com/dawichi/hexakill-cli).

![hexakill-cli](https://raw.githubusercontent.com/dawichi/hexakill-cli/main/showcase3.png)

The intention was to develop a basic system where:

1. A random enemy appears.
2. The player chooses an action to do.
3. The enemy selects a random action to do.
4. The actions are applied based on the speed of each entity.

So, the first goal was set, and I started coding it!

## 2. Entities

The intention was to use OOP for entity generation. I defined a basic entity with the common stats and actions for both the enemies and the player.

#### 2.1 - BaseEntity

Because the game was meant to have 2 types of damage (physical and magic), it also needed 2 different methods of taking damage (`receiveAttack` and `receiveMagic`), so each applies armor reduction or MagicResist to the damage before passing the value to the `_getDamage` function.

Regarding the health counter, the final approach was to store a variable with the value of the damage received. So:

Total health: `this.health = 500`  
Dmg received: `this.dmgReceived = 350`  
Current health: `this.health - this.dmgReceived` = 150

This, which might seem confusing instead of storing a variable like "currentHP", simplifies the leveling up, because if the levelUp() increases total HP by 200, current health will also increase by the same amount, since current health is being calculated based on that total HP, instead of needing to modify both variables, total HP and "currentHP".

```ts
export class BaseEntity {
    constructor(level: number, name: string) {
        this.level = level
        this.name = name
        this.dmgReceived = 0
        this.health = level * 200
        this.ad = level * 30
        this.ap = level * 40
        this.armor = level * 20
        this.mr = level * 20
        this.speed = level * 12
    }

    // process the damage received
    private _getDamage(damage: number) {
        this.dmgReceived += damage
        // If dies, HP counter shows 0 HP, not negative HP
        if (this.dmgReceived > this.health) {
            this.dmgReceived = this.health
        }
    }

    receiveAttack(damage: number) {
        this._getDamage(damage - this.armor)
    }

    receiveMagic(damage: number) {
        this._getDamage(damage - this.mr)
    }

    // actions available
    attack() {}
    magic() {}
    heal() {}
}
```

#### 2.2 - Character

Now comes the base for all playable characters. Unlike enemies, player characters have the ability to:

-   Gain experience.
-   Level up once the experience reaches the limit expected.

So we extend the base and add that logic.

```ts
export class Character extends BaseEntity {
    constructor(level: number, name: string) {
        super(level, name)
        this.exp = 0
    }

    private _levelUp() {
        this.level++
        // increment the entity stats, for example:
        this.health += 250
        this.ad += 20
    }

    // Each time you reach 100 exp points, you levelup.
    // The while is to allow levelUp 2 at a time if you gain +200 exp.
    // Returning a boolean let us know if a level up ocurred.
    gainExp(exp: number) {
        const exp_total = this.exp + exp
        if (exp_total >= 100) {
            while (true) {
                this._levelUp()
                exp_total -= 100
                if (exp_total < 100) break
            }
            this.exp = exp_total
            return true
        } else {
            this.exp += exp
            return false
        }
    }
}
```

#### 2.3 - Enemies

To create the enemies, we can directly use the BaseEntity without a base "Enemy" class, modifying some options to change each enemy a bit. Example:

```ts
// good AP ⇒ but weak vs AD
export class Slime extends BaseEntity {
    constructor(level: number = 1, name: string = 'SLIME') {
        super(level, name)
        // + buff
        this.ap = level * 50
        // - nerf
        this.health = level * 150
        this.armor = level * 15
    }
}
```

## 3. The game loop

The game loop will consist in 2 loops: the 'fight loop' and the 'turn loop'

Each game consists of a sequence of multiple fights against different enemies.  
And each fight against an enemy consists of a sequence of turns.

![hexakill-cli](/assets/img/blog/game_diagram.svg)

### 3.1 Turn loop

This loop needs:

1. Asks for an action
2. Executes the actions
3. Checks if anyone was defeated

```ts
let fightResult = ''

while (!fightResult) {
    // get the answer from prompt, popup with buttons, etc
    const playerAction = askPlayerForAction()

    if (enemy.speed > player.speed) {
        enemyAction()
        if (playerDied()) {
            fightResult = 'defeat'
            break
        }
        playerAction()
        if (enemyDied()) {
            fightResult = 'win'
            break
        }
    } else {
        playerAction()
        if (enemyDied()) {
            fightResult = 'win'
            break
        }
        enemyAction()
        if (playerDied()) {
            fightResult = 'defeat'
            break
        }
    }
}
```

### 3.2 Fight loop

This loop needs:

1. Generates an enemy
2. Turn loop
3. Gives experience once the fight ended

```ts
let playing = true
while (playing) {
    const enemy = new randomEnemy()
    let fightResult = ''

    while (!fightResult) {
        /* Fight Loop */
    }

    if (fightResult === 'defeat') {
        gameOverMessage()
        break
    }

    // exit the upper while loop to go to the next combat
    winFightMessage()

    // example of exp formula to levelup
    // if the enemy is the same level as you
    const exp = (enemy.level / player.level) * 100
    player.gainExp(exp)
}
```


## 4. Problems found and how I solved them

During the development of the game, I found some problems. I was not able to solve them all, but I managed to find some of them.

### Scaling values

It was hard to find the right way to equilibrate the damage scale of the player against the health scale of the enemies.

As the game is currently "infinite" (it ends once the player dies), in advanced levels, a small imbalance makes the enemies stronger than the player, or viceversa. This caused a lot of funny moments with the enemy or the player dying oneshoted by absurd amounts of damage.

### Generation of enemies

I experimented with different ways to generate enemies, with random stats (to add a little of RNG), but finnaly I decided to go with a defined list of enemies, with small differences in stats. The RNG was added in the value of the hits when attacking, so it makes more interesting the combats.

### Damage types

I wanted to offer different types of damage (physical, magic, etc), so the player could choose which one to use depending on the situation and the enemy. To do that, I added the `armor` and `mr` stats to the entities, and the `receiveAttack` and `receiveMagic` methods to the BaseEntity class. The `receiveAttack` method is called when the entity recieves an attack, and the `receiveMagic` when magic is used.

This, besides to offer a better experience, doesn't make the game as complex as I inted, so I added a second layer: RNG to the damage.

The attack has a better chance to hit (90%), making sure you will probably be able to deal damage (80 to 140% of your AD). Meanwhile, the magic has a lower chance to hit (70%), but with a extremly wide range of damage (30 to 200% of your AP), allowing funny coinflip decisions using magic in a decisive moment.


## 5. Conclusion

This is a very simple game, but it's a good example of how to implement different playable characters, multiple enemies generation with it's own stats and how to use the RNG to make the game more interesting. I learned a lot about the game loop, and how the logic implementation ends modifying the player experience. 

In a short future, I will try to implement it inside a game engine instead of React, and see if it's possible to take the game to the next level.

I hope you enjoyed this post!

![code_gif_from_giphy](/assets/img/blog/endings/1.gif)

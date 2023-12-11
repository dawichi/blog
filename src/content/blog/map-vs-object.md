---
title: Map vs Object, comparison in JS (ES6)
description: Differences between Map and Object collection data types in JavaScript
pubDate: 2022-04-02
heroImage: '/images/blog/headers/map_vs_object.jpg'
tags: ['javascript']
visible: true
---

Map and Object are collection data types. Both store data in pairs, with a unique key and a value maped to that key.

-   Object: `{ 1: 'one', 2: 'two' }`
-   Map: `{ (1, 'one'), (2, 'two' ) }`

Map is mainly used for fast searching and looking up data, as it has some big differences with Object who make it perfect for that cases.

-   **Key**: In Object the key must be simple types (string or number). But in Map you can use anything as key, such as functions or other objects.

-   **Order**: Object doesn't respect the order of the pairs once they have been stored, but Map does.

## Object construction

```ts
// 3 ways to create an empty object
const obj = {} // straight-forward
const obj = new Object() // constructor
const obj = Object.create(null) // prototype.create (inherits)
```

In general, we only use the first one as it's simpler, faster in performance and it reduces the chances for mistakes. The unique case we could be interested in use the constructors it's when we want to inherit from another object.

```ts
const animal = {}
// extended object, points to the same object
// if you modify one, both change
const cat = new Object(animal)
// extended object with constructor (2 different)
const cat = Object.create(animal)
```

## Map construction

Maps are created exclusively with the new keyword and the built-in constructor.

```ts
const map1 = new Map()
const map2 = new Map([
    ['first key', 'first value'],
    ['second key', 'second value'],
])
```

## Differences in use

### CREATE props

```ts
// Map                      // Object
map.set('key', 'value')     obj.key = 'value'
                            obj['key'] = 'value'
```

### ACCESS props

```ts
// Map                      // Object
map.get('key')              obj.key
                            obj['key']
```

### CHECK if a prop exists

```ts
// Map                      // Object
map.has('key')              obj.key !== undefined
                            'key' in obj
```

### DELETE prop

Object doesn't have any built-in way to delete properties. We have 2 options:

```ts
delete obj.key
obj.key = undefined
```

The problem here is that the first one performs a much heavier operation. And the second, doesn't actually delete the pair, it just sets the value of that key to `undefined`, but it still remains in the object, so if you iterate over the keys with `Object.keys()` you still will go through that one.

Meanwhile in map, we have 2 nice methods to delete:

```ts
map.delete('key') // @returns boolean
map.clear()
```

To achieve the same capability of `map.clear()` on Objects, we will need to iterate through all of their properties and remove them one by one.

Both will need a `O(1)` to delete a single key and `O(n)` to delete the whole structure depending on the number of pairs.

### CHECK SIZE

```ts
// Map                      // Object
map.size                    Object.keys(obj).length
```

### ITERATING

Map is iterable, but Object isn't.

```ts
// typeof <obj>[Symbol.iterator] === “function”
typeof obj[Symbol.iterator] //undefined
typeof map[Symbol.iterator] //function
```

As any iterable, map can be iterated directly with `for ... of` and built-in `forEach()`.

```ts
// Map
for (const item of map) {
    /* item: [key, value] */
}
for (const [key, value] of map) {
    /* */
}

map.forEach(item => {
    /* */
})
```

Meanwhile, with Object, we use `for ... in` or `Object.keys()` to iterate.

```ts
// Object
for (const key in obj) {
    /* */
}

Object.keys(obj).forEach(key => {
    /* */
})
```

## When to use each one?

Map has good advantages against Object, but there are some cases where Object will be better.

1. Store basic data (when we are sure that the keys will be simple types), because creating an Object is much faster than creating a Map (**literal** vs **constructor**, direct access vs `get()`).

2. JSON has direct support for Object, but not for Map (yet). Use Object if you plan to work with a lot of JSON.

3. Apply logic to properties. Example:

```ts
const obj = {
    name: 'David',
    print: function sayName() {
        return `Hi I am ${this.name}!`
    },
}

obj.print() // Hi I am David!
```

If you try to do it with Map, you just can't

```ts
const map = new Map([
    ['name', 'David'],
    [
        'print',
        function sayName() {
            return `Hi I am ${this.name}!`
        },
    ],
])

map.get('print')() // Hi I am !
```

## Conclusion

Object is more than a hash table, with inner logic, inheritance and more flexible features. On the other hand, Map has better performance when we want to store large sets of data, specially if we want to search or iterate over them.

![code_gif_from_giphy](/images/blog/endings/2.gif)

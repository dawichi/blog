---
title: Callbacks, Promises and Async/Await
description: The evolution of how to work with asynchronous code in JavaScript (ES6)
pubDate: 2022-05-26
heroImage: '/images/blog/headers/promises.jpg'
tags: ['javascript']
visible: true
---

Callbacks, promises and `async`/`await` keywords, are just different ways to work with asynchronous code in JavaScript.

When you work with asynchronous code, you have to deal with new problems that synchronous code doesn't have. For example, when you need to get data from a server, you have to wait for the server to respond. In that case, one of the first solutions was to use callbacks.

## Callbacks

> DEF: A callback is just a function that is passed to another function as an argument, and is executed after some operation is complete.

Imagine that we want to get data from a server, and we want to `console.log()` it after. We cannot do it in a synchronous way, because we don't have the data yet!
So we wrap the call in a `getDataFromServer()` function, defining a `callback: Function` param that will be executed after the request is completed.

This allows to pass any function as a callback, knowing that the logic will be executed after we got the data!

```ts
function getDataFromServer(endpoint, callback) {
    const xhr = new XMLHttpRequest()
    xhr.open('GET', endpoint)
    xhr.onload = () => {
        if (xhr.status === 200) {
            callback(null, xhr.responseText)
        } else {
            callback(new Error('Request failed'))
        }
    }
}

// The last param is the callback
// callback: (err: Error, data: any) => void
getDataFromServer('/users', (err, data) => {
    if (err) {
        // manage error
        console.log(err)
    } else {
        // manage data
        console.log(data)
    }
})
```

What is happening here?

1. We defined a function called `getDataFromServer` that takes two arguments: `endpoint` and `callback`.

> `Endpoint` is the endpoint of the server we want to get data from.  
> `callback` is the function that will be called when the request is completed.

2. When the `xhr.onload` event is triggered, we execute the `callback` function passing an error or the data.

By this way, we can get data from the server without worrying about the request status, because we can handle both cases with inside callback. Notice that we define the logic of the callback in the function call and not in the function definition, so we can reuse the same function for different requests with different implmentations.

### The problem: Callback Hell

There is a problem with this approach. If we have a lot of callbacks nested, it can be hard to read and understand.

Example, let's create a 3-step process with callbacks. In this case, our process will be:

1. Get a cup
2. Fill the cup with coffee
3. Drink the coffee

First, we define our 3 functions:

```ts
const getCup = (user, cb) => {
    console.log(`${user} got a cup`)
    cb('coffee')
}
const fillCup = (liquid, cb) => {
    console.log(`Filling the cup with ${liquid}`)
    cb('drink')
}
const executeAction = (action, cb) => {
    console.log(`To ${action} the cup`)
    cb('Done!')
}
```

Now, we can call the functions in the correct order:

```ts
getCup('Dawichi', liquid => {
    fillCup(liquid, action => {
        executeAction(action, result => {
            console.log(result)
        })
    })
})
```

As you can see, we start apreciating the problem: we are nesting callbacks... and only with 3 steps! Imagine after 10, hard to read.

This is a problem because we can't understand what is happening in an easy way. If we have a lot of nested callbacks, it can be extremly hard to maintain and understand later.

That's why we have promises.

## Promises

Promises are a way to handle asynchronous code in JavaScript. It's the new standard for asynchronous code in JavaScript, as most of the Node.js APIs are being changed from callbacks to promises. They were included in ES6, but the idea was used previously for many libraries like Q, Bluebird or JQuery.

The idea of promises is to `resolve` or `reject` a value at some point in the future, so meanwhile we just `Promise` that the value will be available in a certain period of time.

Let's see how it works:

```ts
const getData = () => {
    return new Promise((resolve, reject) => {
        // Let's simulate a request to a server with 1s delay
        const error = false
        const data = { name: 'Dawichi', age: 25 }
        // After 1s, we resolve the promise with the data
        setTimeout(() => {
            if (error) {
                reject(new Error('Request failed'))
            } else {
                resolve(data)
            }
        }, 1000)
    })
}
```

Now, if we call the function and we print the return value directly, we will get a `Promise` object.

```ts
const data = getData()
console.log(data) // Promise { <pending> }
```

This is the first step of the promise. We call the function and we get a promise of a value. So to be able to get the value, we have to call the `then` method.

```ts
getData().then(data => {
    console.log(data) // { name: 'Dawichi', age: 25 }
})
```

What is happening here?

1. We call the `getData` function.
2. We get a promise of a value.
3. We call the `then` method with a callback function.
4. The callback function is called with the value of the promise.

This is really useful because it allows us to write the code in a more readable way (with other perks).

Let's see the 3-step coffee break process with promises:

```ts
const getCup = () => {
    return new Promise((resolve, reject) => {
        console.log('Getting a cup')
        resolve('coffee')
    })
}
const fillCup = liquid => {
    return new Promise((resolve, reject) => {
        console.log(`Filling the cup with ${liquid}`)
        resolve('drink')
    })
}
const executeAction = action => {
    return new Promise((resolve, reject) => {
        console.log(`To ${action} the cup`)
        resolve('Done!')
    })
}
```

The 3 functions are now encapsulated in promises. For sure this looks worse now, as de function definition have been increased. But then it comes the perks of promises: consume the function.

We call them in the correct order:

```ts
getCup()
    .then(liquid => fillCup(liquid))
    .then(action => executeAction(action))
    .then(result => {
        console.log(result)
    })
```

This is a lot easier to read and understand!

But it doesn't end with a `.then` method. There are other methods like `catch` and `finally`, which can be used in multiple situations to make our code more readable.

Let's see `catch` and `finally`:

```ts
getCup()
    .then(liquid => fillCup(liquid))
    .then(action => executeAction(action))
    .then(result => {
        console.log(result)
    })
    .catch(err => {
        console.log(err)
    })
    .finally(() => {
        console.log('Everything is done!')
    })
```

Now, if any error happens along the process, it will be handled by the `catch` method, allowing us to handle the error.

This is a very useful feature, but there is still a last beautiful tool: `async/await`.

## Async/Await

The `async/await` syntax is a new way to write asynchronous code in JavaScript. It was introduced in ES2017, and it allows to consume our asynchronous functions in a much more readable way in certain situations.

Let's change our last 3-step example into an async/await version:

> NOTE: As `async/await` is based in the idea of that create an 'async function' and 'await values', we are going to encapsulate our `getCup()` call into a `process()` function in both examples.

```ts
// Process function using 'then'
const process = () => {
    getCup()
        .then(liquid => fillCup(liquid))
        .then(action => executeAction(action))
        .then(result => {
            console.log(result)
        })
}

// Process function using 'async/await'
const process = async () => {
    const cup = await getCup('Dawichii')
    const drink = await fillCup(cup)
    const result = await executeAction(drink)
    console.log(result)
}
```

This allows to write code in a less nested way in some situations, and is being really used when we have a lot of complex `then` logic.

The bad part is that to handle errors we have to use a `try/catch` block.

```ts
// Process functino using 'then'
const process = () => {
    getCup()
        .then(liquid => fillCup(liquid))
        .then(action => executeAction(action))
        .then(result => {
            console.log(result)
        })
        .catch(err => {
            console.log(err)
        })
}

// Process function using 'async/await'
const process = async () => {
    try {
        const cup = await getCup('Dawichii')
        const drink = await fillCup(cup)
        const result = await executeAction(drink)
        console.log(result)
    } catch (err) {
        console.log(err)
    }
}
```

So in small cases it creates a lot of code that could be simpler with `then`, so it depends on the situation what is better.

## Conclusion

Right now, to work with asynchronous code is easier than ever. We have extremly useful tools to handle all the use cases and preferences, depending of what we need.

The most important thing is to understand the concepts behind each tool, and then choose the one that fits better in each situation!

![code_gif_from_giphy](/images/blog/endings/5.gif)

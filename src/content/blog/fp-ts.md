---
title: Introduction to fp-ts
description: A practical introduction to fp-ts. Functional programming in TypeScript
pubDate: 2023-09-08
heroImage: /images/blog/headers/fp-ts.jpg
tags: ['typescript']
visible: true
---

**Functional programming** is a revolutionary approach to software development.

Instead of relying on changing states and sequences of commands, it treats computation as mathematical functions. This elegant paradigm, with its emphasis on pure, side-effect-free functions, is gaining traction in modern programming languages.

To understand the benefits of `fp-ts`, we need to understand first functional programming.

## Why functional programming?

Because JavaScript is an agnostic language related to programming paradigms, it is possible to write code in a functional style. However, it is not a functional language, and we must to keep in mind the rules to avoid writing non-functional code.

Let's see a few examples comparing imperative and declarative code.

### Imperative vs Declarative code

In the imperative approach, you typically use loops and mutable variables to achieve tasks. For example:

> For a given array of numbers `[1, 2, 3, 4, 5]` we want the sum of the even numbers squared.

```ts
const numbers = [1, 2, 3, 4, 5]

// Imperative approach
let sum = 0
for (let i = 0; i < numbers.length; i++) {
    if (numbers[i] % 2 === 0) {
        sum += numbers[i] * numbers[i]
    }
}

// Declarative approach
const sum = numbers
    .filter(n => n % 2 === 0)
    .map(n => n * n)
    .reduce((acc, n) => acc + n, 0)
```

This is why declarative code is getting more and more popular: it is easier to read and understand. Even with a simple example like this, it is clear the 3-step operation we are doing: `filter`, `map` and `reduce`.

The idea behind functional programming, is to create small, reusable functions that define operations on data, which later can be composed to create more complex operations just chaining them. Of course this is a very basic example, but let's imagine each of these 3 steps were more complex operations. We could extract them to named functions like `even`, `square` and `sum` and then compose them like this:

```ts
const sum = numbers.filter(even).map(square).reduce(sum)
```

With `fp-ts`, we have a way to manage this operation chaining with fully inferred typed code, so we can focus on developing the operations needed by the business logic without the fear to include non-functional steps in our system.

### What is fp-ts?

`fp-ts` is a library for typed functional programming in TypeScript. It is inspired by Haskell and other functional languages. It provides a set of utilities to bring the most common type classes, data structures and abstraction patterns to TypeScript.

## pipe and flow

The function `pipe()` defines a chain of operations

```ts
import { pipe } from 'fp-ts/function'

// Imagine we have some functions that make certain operations
const addOne = (n: number) => n + 1
const double = (n: number) => n * 2
const toString = (n: number) => `The result is ${n}`
const log = (s: string) => console.log(s)

// And we want to combine them with our input in a certain order to get the final result
const input = 2

// Instead of doing this
log(toString(double(addOne(input))))

// or even worse, this
const intermediateResult = addOne(input)
const intermediateResult2 = double(intermediateResult)
const intermediateResult3 = toString(intermediateResult2)
log(intermediateResult3)

// We can easily use pipe() to do do it in a much more readable way
pipe(input, addOne, double, toString, log) // The result is 6
```

Each **output** of the previous function is passed as **input** to the next one. The first argument is the input of the whole flow, and the result type will be the return type of the last function used.

This is a very common pattern in functional programming, and it's called a [pipeline](<https://en.wikipedia.org/wiki/Pipeline_(computing)>).

The another one is `flow()`. It is very similar to `pipe()`, but instead of using it to execute a series of operations, it is used to define a new function that will execute those operations. Think about it like a reusable pipeline.

```ts
import { flow } from 'fp-ts/function'

// Remember the functions from the previous example?
// We can define 2 reusable flows:
const addOneAndDouble = flow(addOne, double)
const doubleAndToString = flow(double, toString)

// So later we can use them in our pipes
pipe(input, addOneAndDouble, doubleAndToString, log)
```

So, `pipe` is just a chain of operations, and `flow` is a reusable chain of operations.<br/>
You can think about it like running operations directly in our code, or defining a function that will run those operations.

```ts
// runs the operations
pipe(1, addOne, double, toString, log) // void

// defines a flow of operations
const myFlow = flow(addOne, double, toString, log) // (n: number) => void
myFlow(1) // void
```

## Option

The `Option` type is a way of representing a value that may or may not exist. It is very similar to `null` or `undefined`, but it is safer because it forces you to handle the case where the value doesn't exist.

It prevents you from getting errors like `Cannot read property 'x' of undefined` or `Cannot read property 'x' of null`, allowing you to write safer code without ending up with a bunch of `if` statements everywhere.

So, let's check how it works.<br/>
Imagine we have a function that inverts a value. Because it can't `invert(0)`, we may throw an error in that specific breaking case.

```ts
const invert = (n: number): number => {
    if (n === 0) throw new Error("Can't invert 0")
    return 1 / n
}
```

Here, basically we are lying in the return type, as it is not a pure function. The return type is `: number`, but is it true? Does it actually return a number always? No, sometimes it throws an error. So, we are lying.

Here is where it comes `Option`. You could think about it like a standarization of the `null` and `undefined` values, but with a lot of utilities to manage it.

```ts
import * as O from 'fp-ts/Option'

// Option<number> means that the value may be a number or may not exist
const invert = (n: number): O.Option<number> => (n === 0 ? O.none : O.some(1 / n))

// To consume this function, we can use patter matching
// Here it is done with `match()` and `fold()` functions
// (both are the same, it is just an alias)
pipe(
    5, // input
    invert,
    match(
        () => "Can't invert 0",
        n => `The result is ${n}`,
    ),
    log, // log the messages
)

// There are another ways to manage it, like `getOrElse()`
// Imagine that in case the input is 0, we want to return another value as default
pipe(
    0, // input
    invertOption,
    getOrElse(() => 5), // default value
    // keep operating with numbers
)
```

In the first case with the `match`, we return a string in both branches, so we could continue the pipeling with `log` without worrying about problems with the `invert`. In the second case, the `getOrElse` fills the gap of the `invert` function with a default value, so we can continue operating with numbers normally without messing the return type of the next steps.

### O.map + O.flatten + O.chain

Imagine we have a table with movie titles and ratings, and we want a function that when we call it with the array of titles, it returns the title of the movie with the highest rating formatted as The most rated movie is: <title>.toUpperCase().

```ts
import * as O from 'fp-ts/lib/Option'
import { flow } from 'fp-ts/lib/function'

type Movie = {
    title: string
    rating?: number
}

const movies: Array<Movie> = [
    { title: 'Interestellar', rating: 4.3 },
    { title: 'The Martian', rating: 4.5 },
    { title: 'Apollo 13', rating: 4.2 },
    { title: 'Unrated movie' },
]

// For achieving our goal, we gonna define an utility function that will return the most rated movie
// In case we pass an empty array or an array with only unrated movies, it will return none
const _getMostRated = (movies: Array<Movie>): O.Option<Movie> => {
    return movies.filter(m => m.rating).length // no rated movies -> O.none
        ? O.some(
              movies
                  .filter(m => m.rating) // only compare movies with rating
                  .reduce((acc, movie) => (movie.rating > acc.rating ? movie : acc)),
          )
        : O.none
}

// Now we can define a flow that uses that function along with others
const getMostRatedMovieTitle = flow(
    _getMostRated, // Get the most rated movie
    O.map(movie => movie.title), // Get the title of the movie
    O.map(s => s.toUpperCase()), // Convert the title to uppercase
    O.map(s => `The most rated movie is ${s}`), // Add a prefix to the title
    O.getOrElse(() => 'There is no rated movie'), // In case we don't have a rated movie
)

// Now we can use our utility function to get the most rated movie
console.log(getMostRatedMovieTitle(movies)) // The most rated movie is THE MARTIAN

// And in case we don't have any rated movie
console.log(getMostRatedMovieTitle([])) // There is no rated movie
```

Sometimes we may have to map an `Option<>` type, and then we end up with a nested `Option<Option<>>`.

For example, if we have a function that returns an `Option<>` and we want to map it, we end up with a nested `Option<Option<>>`. To solve this, we have a function called `flatten()` that will flat it.

```ts
flow(
    maybeValue, // -> Option<number>
    O.map(inverse), // ->  Option<Option<number>>
    O.flatten, // -> Option<number>
)
```

Because this pattern of `O.map` + `O.flatten` is very common, there is a function called `chain()` that does both things at the same time (known in some languages as `flatMap`).

```ts
flow(
    maybeValue, // -> Option<number>
    O.chain(inverse), // -> Option<number>
)
```

This allows to "chain" multiple `O.chain()` calls without duplicating the lines having to flat the result of each one.

### O.fromPredicate

It is used to create an `Option<>` from a `(n) => boolean` function.

Imagine we have a `isEven(n: number): boolean` function. And we want to return `some(n)` if the number is even, or `none` if it is not. Instead of wrapping the `(n) => boolean` into an new one `(n) => Option<number>`, we can use `fromPredicate()`.

```ts
const isEven = (n: number): boolean => n % 2 === 0

pipe(
    2,
    O.fromPredicate(isEven), // -> some(2)
)
```

### O.alt

It is used to create a conditional flow. The equivalent to `else` in an `if`.

Imagine that we have an array of kids, and we want to select whos gonna be the leader of the group depending on two conditions:

1. If a unique kid is the oldest one, he will be the leader
2. If it is a draw, the kid with better grades will be the leader
3. If it is a draw again, there is no leader

```ts
type Kid = {
    name: string
    age: number
    grades: number
}

const kids = [
    { name: 'John', age: 13, grades: 4 },
    { name: 'Jose', age: 12, grades: 3 },
]

// condition 1
const getUniqueOldestKid = (kids: Kid[]): O.Option<Kid> => {
    if (!kids.length) return O.none // If there are no kids, return none
    if (kids.length === 1) return O.some(kids[0]) // If there is only one kid, return it

    kids.sort((a, b) => b.age - a.age) // Sort by age
    return kids[0].age === kids[1].age ? O.none : O.some(kids[0]) // If it is a draw, return none
}

// condition 2
const getUniqueTallestKid = (kids: Kid[]): O.Option<Kid> => {
    if (!kids.length) return O.none // If there are no kids, return none
    if (kids.length === 1) return O.some(kids[0]) // If there is only one kid, return it

    kids.sort((a, b) => b.grades - a.grades) // Sort by grades
    return kids[0].grades === kids[1].grades ? O.none : O.some(kids[0]) // If it is a draw, return none
}

pipe(
    kids,
    getUniqueOldestKid,
    O.alt(() => getUniqueTallestKid(kids)), // If there is no unique oldest kid, get the tallest one
    O.map(kid => `The leader is ${kid.name}`),
    O.getOrElse(() => 'Total DRAW: There is no leader'),
)
```

By this way, we can set an alternative operation to be done in case the first one returns none, allowing to continue the flow.

## Either

The `Option<>` was used to represent a value that may exists or not. This has a problem, that in case of not, `O.none` does not provide any information about why it does not exists. What if we want to know the reason to handle it later?

Here comes the `Either<>` type. It is used to represent a value that can be of two types: `Left<>` (error) or `Right<>` (value).

Imagine we have a function to execute the payment in a checkout process. This function may succeed (`Right<PaymentID>`) or fail (`Left<Error>`).

```ts
type Account = {
    balance: number
    frozen: boolean
}

// This would be a possible implementation, with 2 possible errors
const pay =
    (amount: number) =>
    (account: Account): E.Either<NotEnoughBalance | AccountFrozen, Account> =>
        account.frozen
            ? E.left({ type: 'AccountFrozen', message: 'The account is frozen!' })
            : account.balance < amount
            ? E.left({ type: 'NotEnoughBalance', message: 'Not enough balance!' })
            : E.right({ ...account, balance: account.balance - amount })

pipe(
    { balance: 100, frozen: false },
    pay(50), // -> Right({ balance: 50, frozen: false })
)

pipe(
    { balance: 100, frozen: true },
    pay(50), // -> Left({ type: 'AccountFrozen', message: 'The account is frozen!' })
)
```

Again, some developers may think that this is the same as throwing 2 different errors in each case. Let's try to do it without `fp-ts` for a moment and see the difference between both approaches.

```ts
const pay =
    (amount: number) =>
    (account: Account): Account => {
        if (account.frozen) throw new Error('The account is frozen!')
        if (account.balance < amount) throw new Error('Not enough balance!')
        return { ...account, balance: account.balance - amount }
    }
```

What is now the return type? `: Account`. Is it true? Does it always return an account as result? No, sometimes it throws an error. So, we are lying again. Knowing not only the possibility that the function may throw, but also with what kind of error, is a huge advantage from the consumer point of view.

This can be combined later with a `match()` to handle each case.

```ts
pipe(
    { balance: 100, frozen: true },
    pay(50), // -> Left({ type: 'AccountFrozen', message: 'The account is frozen!' })
    match(
        left => console.error(left.message), // -> The account is frozen!
        right => console.log(right.balance), // -> 50
    ),
)
```

### E.tryCatch

Imagine we want to create a function that returns the result of `JSON.parse()` of a string. This function may succeed (`Right<JSON>`), or fail (`Left<Error>`).

```ts
const jsonParse = (text: string): E.Either<Error, unknown> => {
    try {
        return E.right(JSON.parse(text))
    } catch (e) {
        const error = e instanceof Error ? e : new Error(String(e))
        return E.left(error)
    }
}
```

This is pretty verbose and not functional at all, so `fp-ts` provides a function called `tryCatch()` that helps to manage this.

```ts
const jsonParse = (text: string): E.Either<Error, unknown> =>
    E.tryCatch(
        () => JSON.parse(text),
        e => (e instanceof Error ? e : new Error(String(e))),
    )
```

This allows to not use `try/catch` block and write the code much more readable.

Also, do you see how the exact input of our function `jsonParse(text: string)` will be the input of the `JSON.parse(text)`?

When this happens, we can use the similar block `E.tryCatchK()`.

```ts
// Types both for input and output are inferred! 🎉
const jsonParse = E.tryCatchK(
    JSON.parse,
    e => (e instanceof Error ? e : new Error(String(e)))
)
```

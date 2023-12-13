---
title: Recursion and dynamic programming (DP)
description: Finding the shortest path to a recursive problem by mathematical optimization
pubDate: 2022-03-07
heroImage: '/images/blog/headers/recursion.jpeg'
tags: ['engineering', 'algorithms']
visible: true
---

To understand what is dynamic programming, we first need to understand what is recursion.

> DEF: `Recursion` consists of a problem with a solution that contains a smaller version of the same problem.

In programming, it allows solving the problem by applying the same function several times to a value until finally reaching the result.<br/>
Let's see some examples!

## 1. Factorial of a number

The factorial of a number is the function that multiplies the number by each natural number below it.

```js
5! = 5 * 4 * 3 * 2 * 1
4! =     4 * 3 * 2 * 1

5! = 5 * 4!
```

Here, if we pay attention, we can see that `5!` is `5 * 4!`, so the result is a smaller factorial!

```js
// If
5! = 5 * 4!
// Then
n! = n * n-1!

f(n): factorial of n
f(n) = n * f(n-1)
```

The problem is that this doesn't stop and continues to infinity.

```js
f(2) = 2 * f(1)
f(1) = 1 * f(0)
f(0) = 0 * f(-1)
f(-1) = -1 * f(-2)
... ad infinitum
```

To avoid it, we need to define a **base case** that stops the recursion. A recursive algorithm needs 2 cases:

-   Base case
-   Recursive case

In this example, the base case is when `n = 0`, because `0! = 1` (and not `0 * f(-1)`).<br/>
With this, we can successfully implement it in code in Python for example.

```python
# @param n >= 0
def f(n):
    if n == 0:
        return 1
    else:
        return n * f(n-1)

f(5) # out: 120
f(6) # out: 720  (120 * 6)
```

To understand it better, we can see the same example in Haskell, which shows a much direct correlation with the mathematical notation we saw before.

```haskell
factorial :: Int -> Int
factorial 0 = 1 -- base case
factorial n = n * factorial(n-1) -- recursive case
```

Simple, right? Let's see another example!

## 2. Fibonacci sequence

The well-known Fibonacci sequence is a sequence of numbers where each number is the sum of the two preceding numbers. It commonly starts from `0` and `1`, continuing with `0 1 1 2 3 5 8 13 21 ...`

Again, we will define the base and recursive cases:

-   Base case: `n <= 1`
-   Recursive case: `n > 1`

```python
# f(n): returns the number for the n position in the sequence
def f(n):
    if n <= 1:
        return n
    else:
        return f(n-1) + f(n-2)

f(5) # out: 5 - [1, 1, 2, 3, 5]
f(6) # out: 8 - [1, 1, 2, 3, 5, 8]
```

And again, let's see the equivalent in Haskell.

```haskell
fibonacci :: Int -> Int
fibonacci 0 = 0 -- base case: n <= 1
fibonacci 1 = 1 -- base case: n <= 1
fibonacci n = fibonacci (n - 1) + fibonacci (n - 2)
```

## 3. Problem: exponential complexity

When we calculate `f(5)`, we have to calculate `f(4)` and `f(3)`. But later, when we calculate `f(4)`, we have to calculate `f(3)` again! We are overlapping the calculations, wasting computational resources.

![fibonacci](/images/blog/fibonacci.svg)

As we can see here, we are calculating the same numbers over and over again.

-   `f(3)` occurs 2 times
-   `f(2)` occurs 3 times
-   `f(1)` occurs 5 times

This doesn't matter with such a small number as `f(5)`, but what happens when we calculate `f(50)`? Probably your program will stay stuck without end, because it's trapped in a loop calculating the same numbers repeatedly, delaying probably minutes to finish.

Let's measure a few examples:

```js
f(5): 0.0001s
f(20): 0.8s
f(40): 2s
f(45): 12s
f(50): doesn't finish (minutes)
```

The time keep increasing exponentially. So, the problem is clear: we can't just calculate 200 times the same numbers.

What if we just store the value of the numbers we calculated? Once we calculate `f(5)`, we can store it and check the result later in all the iterations of `f(5)`. This is called memoization.

## 4. Memoization

Memoization it's a basic technique of Dynamic Programming (DP). It consists in store the values of the calculations, so we don't have to calculate them again.

The concept is very similar to a cache. We are going to store the values in a dictionary or in an array so later we can access them instead of calculating them again.

Example:

```ts
const memo = []

const fibonacci = (n: number): number => {
    if (n <= 1) {
        return n
    }

    if (memo[n]) {
        return memo[n]
    }

    const result = fibonacci(n - 1) + fibonacci(n - 2)
    memo[n] = result
    return result
}
```

What are we doing here?

Once a number is calculated, we store it in the `memo[n]` position.<br/>
In any next iteration, we can check if the number is already stored in the memo, and if it is, we don't have to calculate it again.

How long does it take to calculate the number now?

```c
f(50): 0.020s
```

We have used memoization to improve our function! And now, we can try any big number and see the difference.

```c
f(2_000): 0.7s
```

Much better!

## 5. Second problem: call stack size

This is a good solution while we don't keep increasing `n`.

Why? Because we are using recursion, so each call generates a new function call in the call stack. If we try to call `f(10_000)` for example, it will exceed the call stack limit and raise an error.

```c
fibonacci(10_000) = RangeError: Maximum call stack size exceeded
```

This error happens because we are overflowing the call stack with multiple recursive calls.<br/>
Here is when Dynamic Programming drive us to the second step: use memo to convert the recursive function to an iterative one.

```ts
const fibonacci = n => {
    let memo = [0, 1]
    for (let i = 2; i <= n; i++) {
        memo[i] = memo[i - 1] + memo[i - 2]
    }
    return memo[n]
}
```

What is the difference? We are not using recursion anymore, we just keep adding values to the memo in new positions, allowing us to advance in the sequence without calculating a position more than once and without overflowing the call stack.

If we try to call `fibonacci(10_000)` now, we won't get an error.

```c
fibonacci(10_000) = Infinity
```

It gives us an `Infinity` because it overflows the maximum number than JavaScript can handle, but it doesn't break the program!

## Conclusion

Recursive programming is very useful to solve certain problems with a short implementation, but it can be dangerous if we don't have clear the base concepts behind it, throwing us into wasting computational resources very easily.

Once we detect one of these problems, we can use techniques of Dynamic Programming to optimize our code, like `memoization`.

Also, depending on the problem, we can always consider converting our recursive function into a iterative one, preventing the call stack overflow.

This is just a basic example of the methodologies of Dynamic Programming. There are many more, but all of them consists in the same idea of optimizing the problem to avoid lose time and resources.

![code_gif_from_giphy](/images/blog/endings/4.gif)

## References

-   [Wikipedia - Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming)
-   [GeeksForGeeks - Dynamic programming](https://www.geeksforgeeks.org/dynamic-programming/)
-   [GeeksForGeeks - Memoization](https://www.geeksforgeeks.org/memoization-1d-2d-and-3d/)
-   [GeeksForGeeks - Tabulation](https://www.geeksforgeeks.org/tabulation-vs-memoization/)

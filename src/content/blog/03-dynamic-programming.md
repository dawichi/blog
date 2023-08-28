---
title: What is the dynamic programming (DP)?
description: Finding the shortest path to a problem by mathematical optimization
pubDate: 2022-03-07
heroImage: '/assets/img/blog/dynamic-programming.jpeg'
---

Let's talk about fibonacci. Fibonacci sequence is a sequence of numbers where each number is the sum of the two preceding numbers.

```ts
// Calculate the nº number of fibonacci
const fibonacci = (n: number): number => {
    if (n <= 1) {
        return n;
    }

    return fibonacci(n - 1) + fibonacci(n - 2);
}

fibonacci(5)   // 5  [1, 1, 2, 3, 5]
fibonacci(6)     // 8  [1, 1, 2, 3, 5, 8]
```

Here, we have a recursive function that calculates the nº number of fibonacci. We can see that the function is recursive, so it calls itself until it reaches the base case.


## The problem

When we calculate `f(5)`, we have to calculate `f(4)` and `f(3)`. But later, when we calculate `f(4)`, we have to calculate `f(3)` again! We are overlapping the calculations, wasting computational resources.

![fibonacci](/assets/img/blog/fibonacci.svg)

As we can see here, we are calculating the same numbers over and over again.

* f(3) occurs 2 times
* f(2) occurs 3 times
* f(1) occurs 5 times

This doesn't matter with such a small number as `f(5)`, but what happens when we calculate `f(50)`? Probably your program will stay stuck without end, because it's trapped in a loop calculating the same numbers over and over again, delaying probably minutes in finish it.

Let's measure a few examples:

```c
f(5): 0.0001s
f(20): 0.8s
f(40): 2s
f(45): 12s
f(50): doesn't finish (minutes)
```

The time keep increasing exponentially. So the problem is clear: we can't just calculate 200 times the same numbers.

What if we could just store the value of the numbers we calculated? So once we calculate `f(5)`, we can store it and use it later in all the iterations of `f(5)`. This is called memoization. 


## Memoization

Memoization it's a basic technique of Dynamic Programming (DP). It consists in store the values of the calculations, so we don't have to calculate them again.

The concept is very similar to a cache. We are going to store the values in a dictionary or in an array so later we can access them instead of calculate them again.

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

Once a number is calculated, we store it in the `memo[n]` position.

So in any next iteration, we can check if the number is already stored in the memo, and if it is, we don't have to calculate it again.

How long does it take to calculate the number now?

```c
f(50): 0.020s
```

We have converted the recursive function to a memoized one. And now, we can try any big number without the fear to broke the program overloading our function.

```c
f(2_000): 0.7s
```

Much better!


## The second problem: recursion

This is a good solution while we don't keep increasing `n`. Why?

Because we are using recursion, when we try to call `f(10_000)` for example, it will break.

```c
fibonacci(10_000) = RangeError: Maximum call stack size exceeded
```

This error happens because we are overflowing the call stack with our multiple recursive calls.

Here is when Dynamic Programming drive us to the second step: use our memo to convert our recursive function to a iterative one.

```ts
const fibonacci = (n) => {
    let memo = [0, 1]
    for (let i = 2; i <= n; i++) {
        memo[i] = memo[i - 1] + memo[i - 2]
    }
    return memo[n]
}
```

What is the difference?

If we try to call `fibonacci(10_000)` now, we won't get an error.

```c
fibonacci(10_000) = Infinity
```

It gives us an `Infinity` because it overflows the maximun number than JavaScript can handle, but it doesn't break the program!


## Conclusion

When working with recursion, we could end with some situations where we are calculating the same operations over and over again. To avoid this, we have a technique called `memoization`.

On the top of this, we can use the array or dictionary used for memoization to convert our function into a iterative one, preventing the call stack overflow when working with big recursive functions.

This is just a basic example of the methodologies of Dynamic Programming. There are many more, but all of them consists in the same idea of optimizing the problem to avoid lose time and resources.

![code_gif_from_giphy](/assets/img/blog/endings/3.gif)
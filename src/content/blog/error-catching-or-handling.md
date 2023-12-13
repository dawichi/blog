---
title: Error catching or handling
description: From assumptions to assurance. Building error-free software by design
pubDate: 2023-12-13
heroImage: '/images/blog/headers/error-handling.jpg'
tags: ['engineering', 'typescript']
visible: true
---

In software engineering, errors are a daily thing. But the massive number of hours that I have spent tracking that `undefined` property that somehow was mutated along the process and messed up my code is uncountable. It was one of the main reasons why I jumped into TypeScript as soon as I could, as it helped me to prevent a lot this kind of errors. But still, it was not enough.

Even when TypeScript (strictest) forces you to code better, by forcing you to always check a `value | undefined` type before you use it (like a `Result<data, error>` type that other languages provide), it is still not enough. Because TypeScript, under the hood, is just JavaScript. So once your server is deployed and running, you lose all the benefits of the TypeScript's compilation step.

- What happens if your endpoint receives an unexpected value on a parameter? Or a wrong requestBody?
- What happens if someone changes the database structure or data, and you expect to get the same thing you set there?
- What happens with all the edge cases that you didn't think about?

While TypeScript allows you to keep a certain level of control internally in your code, as the system grows in complexity and external dependencies, new errors appear, and here TypeScript doesn't help you anymore. These new challenges were a hard step, and of course solutions in every language already exist for all of them: validations for the inputs in APIs, versioning for the database structural changes, etc. But it has been this year, working with [NestJS](https://nestjs.com/) and [Zod](https://zod.dev), that my whole approach to errors has changed. These tools have allowed me and my team to implement a level of control and validation over which **data** will be allowed to enter and run through the system, that we didn't have before, without adding barely any logic complexity to the code.

In this post I will try to explain how an evolution from a JS Express API validated with openapi yaml files, to a NestJS API validated with Zod schemas has changed my thinking about these "unexpected errors", from a reactive approach to a proactive one. And how the number of errors has been decreased drastically, increasing the confidence in the system.


## 1. Clarifying concepts

I intend to use a very defined terminology to differentiate between catching and handling errors, but since this is not a standard, let's clarify it first to avoid confusion.

> **Error Catching**: A reactive way of capturing errors. It consists of adding `try/catch` blocks to the code, managing the errors as they come, more than preventing them.

> **Error Handling**: A proactive way of preventing errors. It consists of adding validations to the code, preventing the errors before they happen, instead of managing them when they come.


## 2. Importance of Error Handling

While complexity is inherent to any modern software system and uncertainties are unavoidable, the way we deal with them is what makes the difference. The more we can prevent errors, the less we will have to deal with them. As a proactive strategy, rather than merely reacting to errors, this approach emphasizes prevention during the design phase.

### A functional approach

The focus shifts from adding exceptions for potential failure cases to preventing errors by only allowing the cases that are expected. If we design code as operations on certain data, and nothing else than that data can enter the system, we can be sure that the code will work as expected. This is the main idea behind the [Functional Programming](https://en.wikipedia.org/wiki/Functional_programming) paradigm, understanding a system as a set of operations over data.

### Blacklisting vs Whitelisting

This concept mirrors the difference between blacklisting and whitelisting. Instead of exhaustively listing all undesired cases, adding new ones as they appear, we can define the data that is exclusively allowed. This of course has less flexibility than the blacklisting approach, as the system will panic over any new input that we did not consider yet, but it is also more secure and reliable. It is a tradeoff where the time spent in this whitelisting validation is usually worth the time saved in debugging and fixing errors on a later stage as the system grows.

## 3. The Pitfalls of Error Catching

While error catching acts as a safety net for unexpected issues, relying solely on it can lead to some problems. A common pattern I have seen in many codebases when dealing with a complex operation over input data, is to just wrap the whole thing in a `try/catch` block where all the errors end, logging a generic error message. This, besides being fast and easy to implement, generates in the long term a lot of issues.

At the end, you are accepting that anything inside may explode, recognizing the lack of control over the system. You are not **handling**, you are **catching**.

Depending on the case, debugging may be a bit of a puzzle when error catching is the primary strategy. It is common than on a complex system, an unintentional mutation introduced in one section of the code survives almost until the end of its process, where it finally produces the error. The amount of effort to track back the origin of the change in the data can be extremely high in certain cases.

Let's see a small example:

> Imagine that we have an external provider that gives us information about the weather for a certain city, under the `externalProvider` service.
>
> Now, we create the endpoint `GET /weather/:cityName` that will return the information from the externalProvider, formatted in a certain structure the app uses.

After the controller applies the validation (if any) to the `cityName` parameter, we get into the service function, that may look something like this:

```ts
type Weather = {
    city: string
    temperature: number
    humidity: number
    wind: number
}

type ProviderWeather = {
    city: string
    data: {
        temperature: number
        humidity: number
        wind: number
    }
}

function getWeather(cityName: string): Weather {
    const weather: ProviderWeather = externalProvider.getWeather(cityName)
    return {
        city: weather.city,
        temperature: weather.data.temperature,
        humidity: weather.data.humidity,
        wind: weather.data.wind,
    }
}
```

Here comes the problem: we are assuming that the response from the provider will match `ProviderWeather`, but this is just an assumption, we are not assuring it. So, if for any reason the provider sends a different response, we will get an error. Now, there are many options to improve it.

1. **General error catching**: We may add a general try/catch to the server. For example, NestJS provides one that throws a Internal Server Error if any unhandled throw happens in the code.

2. **Specific error catching**: Inside the `getWeather` function, we may add a specific `try/catch` block that acts as a net for this specific case, allowing us to provide the Frontend a more particular error, specifying that it happened because of the provider response.

3. **Validation**: Or... we can just validate the data. `externalProvider` is a door to the system, that introduces data into the flows and procedures. A good practice would be to validate its data, to be able to fully trust its content.

But here is the thing: how do we validate it? And not only this simple example, but a big, nested response of thousands of properties from a real case? And how do we design a standard way of doing it to follow it for future cases?

## 4. The Zod way

I have been using NestJS as my main backend framework for almost 3 years now. It is so well structured and designed, that even after years of growth, the codebases keep clean and maintainable, thanks to the extremely opinionated approach, where everything should be done in a certain way. I have met people that don't like the "NestJS way" (specially because of the **decorators** approach), but they recognize anyway that the development experience is great.

This framework, shines specially after you integrate **Zod** into it. It is a TypeScript-first schema declaration and validation library, which allows you to define the shape of your data and validate it against that schema (similar to [Joi](https://joi.dev/)).

Let's see how we can apply it to the previous example.

While the `type ProviderWeather` gives us validation on compile time by TypeScript, it lacks the runtime validation we are looking for. Here is when we can use Zod to convert this type into a **schema**, that not only we can later use to parse the input data and assure its structure, but also to infer the types for the app directly from it, keeping a single source of truth for the data definition.

In this case, it may look like this:

```ts
const ProviderWeatherSchema = z.object({
    city: z.string(),
    data: z.object({
        temperature: z.number(),
        humidity: z.number(),
        wind: z.number(),
    }),
})

type ProviderWeather = z.infer<typeof ProviderWeatherSchema>
```

So now we have a zod schema from where the `ProviderWeather` type is being inferred. And this allows us to use both in the function:

```ts
function getWeather(cityName: string): Weather {
    const weather: ProviderWeather = externalProvider.getWeather(cityName)
    const result = ProviderWeatherSchema.safeParse(weather)

    if (!result.success) {
        throw new Error('Invalid data from provider', result.error)
    }

    // weather or result.data are both assured to be ProviderWeather
    return {
        city: weather.city,
        temperature: weather.data.temperature,
        humidity: weather.data.humidity,
        wind: weather.data.wind,
    }
}
```

By this simple way we have added runtime validation to our data. This is a simple example but imagine a real case with a really nested response. Being able to validate it and simultaneously infer the types from it, is a huge advantage that helps to keep our system safe, clean and maintainable.


## Conclusion

In the journey from tracking elusive `undefined` properties to building robust software, the evolution from error catching to error handling has been transformative. TypeScript set the stage, but it was tools like NestJS and Zod that truly empowered our proactive approach.

Shifting from reactive error catching to a proactive error-handling mindset, we embraced a functional approach: designing operations on well-defined data. The pitfalls of relying on error catching became evident, prompting us to seek a better solution.

Enter Zod, seamlessly integrated into the reliable NestJS framework. With Zod, runtime validation became a breeze, ensuring not only data integrity but also fostering a single source of truth for our data definitions.

This transition has made us to increase the confidence in our systems. We've moved beyond reacting to errors; we now prevent them. The path to error-free software is clearer, thanks to TypeScript, NestJS, and Zod -- a powerful trio safeguarding our code against the uncertainties of software development.

![code_gif_from_giphy](/images/blog/endings/3.gif)

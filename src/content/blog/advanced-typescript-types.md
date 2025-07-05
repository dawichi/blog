---
title: Advanced TypeScript Types
description: Practical TypeScript utility types and patterns to enhance type safety and developer experience.
pubDate: 2025-07-05
heroImage: '/images/blog/headers/advanced-ts-types.png'
tags: ['typescript']
visible: true
---

I've spent countless hours debugging `undefined` properties and unexpected data types. That's one of the reasons I love TypeScript over plain JS.

This post serves as a personal quick reference guide to some useful advanced TS tricks, kinda like a cheatsheet for when I'm working in a new project and I need some reference to do something.

## 1. Optional Properties

It is NOT the same to have a **optional key**, than a **optional value**. I have seen infinite examples where this confusion leads to bugs because of a misscomunication between BE and FE for example.

### Key Optional

When you define a property with `?:`, you're stating that the key itself might not exist on the object. If the key is present, its value **must** be type `SomeType`.

```ts
// --------------------------------------
// Type definition
// --------------------------------------
type UserProfile = {
    id: string
    name: string
    email?: string // `email` **key** might not exist
}

// --------------------------------------
// Examples
// --------------------------------------
const user1: UserProfile = {
    id: '123',
    name: 'Alice',
} // Valid: email key is absent

const user2: UserProfile = {
    id: '456',
    name: 'Bob',
    email: 'bob@example.com',
} // Valid: email key exists with string value

const user3: UserProfile = {
    id: '789',
    name: 'Charlie',
    email: undefined,
} // Valid: email key exists with `undefined` value
```

### Value Optional

The key **must** exist in the object, but in its value definition we allow `undefined` as a valid value.

```ts
// --------------------------------------
// Type definition
// --------------------------------------
type Product = {
    id: string
    name: string
    description: string | undefined // `description` key must exist, value can be string or undefined
}

// --------------------------------------
// Examples
// --------------------------------------
const product1: Product = {
    id: 'A01',
    name: 'Widget',
    description: 'A fantastic widget.',
} // Valid

const product2: Product = {
    id: 'A02',
    name: 'Gadget',
    description: undefined,
} // Valid: description key exists with `undefined` value

// @ts-expect-error - Property 'description' is missing in type
const product3: Product = {
    id: 'A03',
    name: 'Doodad',
} // Invalid: description key is missing
```

#### Which one to use?

Personally I always try to use value optional when possible, with `null` values for keys without data.

Why? Because this makes sure that the final structure is always the same, so when the developer checks it, he gets the hint that **there is** a `description` field to be used, it simply has no data yet.

## 2. Transform Types

TypeScript provides powerful built-in utility types to transform existing types, allowing for precise type definitions without duplication.

### `Pick<T, K>` and `Omit<T, K>`

-   `Pick<T, K>`: creates a new type by selecting specific properties `K` from type `T`.
-   `Omit<T, K>`: creates a new type by omitting specific properties `K` from type `T`.

This is super useful for example to extract only-back properties from a inherited ORM type. For example, `password`, `updatedAt`, `isActive` may be fields of a `UserDto` that we don't want to expose in the API, but we need to use them internally. So this allows us to create a white-list or a black-list of properties to use in our code, defining new types inherited from the original type, for each use case.

```ts
type User = {
    id: string
    name: string
    email: string
    createdAt: Date
    updatedAt: Date
}

// Create a type with only 'id' and 'name'
type UserSummary = Pick<User, 'id' | 'name'>
// UserSummary = { id: string; name: string; }

// Create a type excluding 'createdAt' and 'updatedAt'
type UserInput = Omit<User, 'createdAt' | 'updatedAt'>
// UserInput = { id: string; name: string; email: string; }
```

### `Partial<T>` and `Required<T>`

TS also offers utilities to manipulate the *optionality* of properties.

-  `Partial<T>`: makes all properties of type `T` optional.
-  `Required<T>`: makes all properties of type `T` required.

This is very useful for example when defining a `PATCH` endpoint, where you may pass any prop (1 or all) of a resource to update it, but you don't want to define a new type for each possible combination of properties. Instead, you can use `Partial<T>` to make all properties optional.

```ts
type User = {
    id: string
    name: string
    email: string
    createdAt: Date
    updatedAt: Date
}

// Create a type with all properties optional
type UserUpdate = Partial<User>
// UserUpdate = { id?: string; name?: string; email?: string; createdAt?: Date; updatedAt?: Date; }
```

And `Required<T>`, while less common, when some data you are dealing with might have optional fields (perhaps an external API response), but a specific part of your system **needs** all properties to be present to work correctly. This use case has been generally replaced with a library like [zod](https://zod.dev/), but it can still be useful in some cases.

```ts
type SomeExternalData = {
    something?: string
    anotherThing?: number
}

// Create a type with all properties required
type RequiredData = Required<SomeExternalData>
// RequiredData = { something: string; anotherThing: number; }
```

### `Extract<T, U>` and `Exclude<T, U>`

-   `Extract<T, U>`: Extracts from `T` all types that are assignable to `U`.
-   `Exclude<T, U>`: Excludes from `T` all types that are assignable to `U`.

This is used when working with **union types**. It's easy to understand with an example:

```ts
type EventType = 'click' | 'submit' | 'hover' | 'scroll' | number | boolean

// Extract only string literal types
type StringEvents = Extract<EventType, string>
// StringEvents = 'click' | 'submit' | 'hover' | 'scroll'

// Exclude numbers and booleans
type NonNumericBooleanEvents = Exclude<EventType, number | boolean>
// NonNumericBooleanEvents = 'click' | 'submit' | 'hover' | 'scroll'
```

Or, with a more complex structure that might be used in a real-world scenario:

```ts
type NotificationUnionType =
    | { type: 'email'; email: string; subject: string }
    | { type: 'sms'; phoneNumber: string; message: string }
    | { type: 'push'; deviceToken: string; title: string; body: string }

// Extract only email notifications
type EmailNotification = Extract<NotificationUnionType, { type: 'email' }>
// EmailNotification = { type: 'email'; email: string; subject: string }

type NonEmailNotification = Exclude<NotificationUnionType, { type: 'email' }>
// NonEmailNotification = { type: 'sms'; ... } | { type: 'push'; ... }
```

## 3. Loose Autocomplete `(string & {})`

This is a trick that once found, has been introduced in most libraries. Basically it allows to keep autocomplete in a non-strict list of strings. Again, obvious with an example:

Imagine that we accept any string as a valid input, BUT we want to offer some examples to the method's consumer with the autocomplete.

```ts
type Something = 'a' | 'b' | 'c' | string
// type `string`
```

This type would collapse to a simple `string`, because TS considers that `string` is a supertype of `'a' | 'b' | 'c'` and therefore it covers all possible values. But it makes us lose the autocomplete of `'a' | 'b' | 'c'`.

To keep the autocomplete, we can use the trick of intersecting with an empty object, in one of these ways:

```ts
type Something = ('a' | 'b' | 'c') & {}
type Something = 'a' | 'b' | 'c' | (string & {})
```

This will keep allowing us to pass any string, but also will provide the autocomplete for the specific values in our type definition.

> How does this work? The `& {}` creates an intersection with an empty object type. Since `string` is not assignable to `{}` (and vice versa) in a way that allows it to fully absorb the literal types, TypeScript preserves the union for autocomplete purposes while still allowing any string!

## 4. Discriminated Unions

Discriminated unions are a powerful way to model complex types that can take on multiple forms. They use a common property (the "discriminator") to differentiate between the different types in the union. A typical example may be a `EventType` or `NotificationType` that can be one of several specific types, each with its own properties.

The idea here is to have a central type where we define the different options, and then generate the union type from that.

```ts
// here we define our 3 actions, each has its own properties
type Actions = {
    login: {
        username: string
        password: string
    }
    logout: {
        reason: string
    }
    update: {
        id: string
        data: unknown
    }
}

export type ActionDiscriminatedUnionType = {
    // Prettify<T> is a custom trick type! check in the next section
    // it is optional, this would work without it too
    [K in keyof Actions]: Prettify<
        {
            type: K // The discriminant property
        } & Actions[K] // Spread the props of the specific action type
    >
}[keyof Actions]

/*
    ActionDiscriminatedUnionType will resolve to type union:
    {
        type: "login";
        username: string;
        password: string;
    } | {
        type: "logout";
        reason: string;
    } | {
        type: "update";
        id: string;
        data: unknown;
    }
*/

// Example usage:
function handleAction(action: ActionDiscriminatedUnionType) {
    switch (action.type) {
        case 'login':
            console.log('Login attempt:', action.username)
            break
        case 'logout':
            console.log('Logout reason:', action.reason)
            break
        case 'update':
            console.log('Updating ID:', action.id, 'with data:', action.data)
            break
        default:
            // TypeScript ensures all cases are handled if you use `never`
            // const _exhaustiveCheck: never = action;
            break
    }
}

// All derived types from the original Actions type
type LoginAction = ActionDiscriminatedUnionType extends infer U ? (U extends { type: 'login' } ? U : never) : never
// LoginAction = { type: "login"; username: string; password: string; }
```

The `[K in keyof Actions]: ...` maps over each key in `Actions`, creating a new type for each. The `type: K` part is the magic that creates the discriminant property. Finally, `[keyof Actions]` collects all these mapped types into a single union. This pattern is incredibly clean and scalable.

## 5. Custom Utility Types

These are a few types I find myself reusing in almost every TypeScript project. They typically live in a `common.types.ts` file.

```ts
export type Nullable<T> = T | null
export type Optional<T> = T | undefined
export type Maybe<T> = T | null | undefined
export type Empty = null | undefined

/**
 * Forces TypeScript to simplify complex intersection or union types for better readability
 * in IDE hover tooltips.
 */
export type Prettify<T> = {
    [K in keyof T]: T[K]
} & {}

/**
 * Constructs a type where all properties (including nested ones) of `T` are optional.
 */
export type DeepPartial<T> = T extends object
    ? {
          [P in keyof T]?: DeepPartial<T[P]>
      }
    : T
```

The `Prettify` type is particularly useful. When you have types derived from multiple intersections or complex manipulations (like our `ActionDiscriminatedUnionType`), hovering over them in VS Code can show a very convoluted type signature. `Prettify` forces TypeScript to resolve and display a flattened, more readable version, greatly improving the developer experience.

## Conclusion and Reference

The types and patterns discussed here are invaluable tools for crafting robust, type-safe, and highly maintainable applications. By defining and enforcing data shapes, we can significantly reduce runtime errors and improve the developer experience.

This post is very much a blog-post-version extended by my own experiences, of concepts brilliantly explained by **Matt Pocock** ([mattpocock.com](https://www.mattpocock.com/)) in his video [6 TypeScript tips to turn you into a WIZARD](https://www.youtube.com/watch?v=lraHlXpuhKs). I highly recommend checking out his work for more in-depth explanations and advanced techniques!

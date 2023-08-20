# conan-classic
a [conan](https://github.com/conan-io/conan) fork based on origin 1.60.2 to always use classic mode.
In order to distinguish with the origin version , rename the project to conan-classic,
but the command line is same as 1.x

## Refs
* Wiki: https://github.com/tinysec/conan-classic/wiki
* Origin Project: https://github.com/conan-io/conan

## Why fork
1. Many old packages written in 1.x style.
2. 2.x is NOT compatibled with 1.x
3. 1.x is deprecated

## When to use this fork
1. You still have to depend some packages written in 1.x
2. You want support compiler old than visual studio 2012
3. You want tools download cache worked
4. You want easy per-site proxy feature worked


## What fixed.
1. The config keys contains ':' not workd right at windows, replaced with '.'
2.


# pwg

[![Build Status](https://travis-ci.com/rddunphy/pwg.svg?branch=master)](https://travis-ci.com/rddunphy/pwg)

A CLI for generating randomised passwords.

## Installation

Download the repository, add `pwg` to your path, and install dependencies using:

```console
user:~/pwg $ pip install -r requirements.txt
```

## Usage

To create a password using the default pattern (10-12 characters), run:

```console
user:~ $ pwg
-R@@u8U#;o
```

This prints the generated password to std out. To copy the password to the clipboard instead, use the `-c`/`--copy` option:

```console
user:~ $ pwg -c
Password copied to clipboard.
```

To specify another pattern, use the `-p`/`--pattern` option:

```console
user:~ $ pwg -p ou{2}n{5}
PI73081
```

## Patterns

Patterns are sequences similar to regular expressions, which specify character classes from which characters are randomly drawn 
to generate a password. 

### Character classes

The available character classes are:

 - `l`: lower case (`a-z`)
 - `u`: upper case (`A-Z`)
 - `n`: numeral (`0-9`)
 - `N`: numeral without 0 (`1-9`)
 - `s`: basic special (`!$%^&*@#;:?+=_-,.`)
 - `x`: extended special (``"£()[]{}~'/\<>`|``)
 - `S`: any special (``!$%^&*@#;:?+=_-,."£()[]{}~'/\<>`|``)
 - `a`: alphabetic (`a-zA-Z`)
 - `A`: alphanumeric (`a-zA-Z0-9`)
 - `h`: hexadecimal (`0-9a-f`)
 - `H`: upper case hexadecimal (`0-9A-F`)
 - `b`: binary (`01`)
 - `c`: alphanumeric or basic special character
 - `C`: any character
 
### Repeated and optional character classes

Character classes can be repeated by indicating the number of repetitions in braces after the class (e.g., `n{4}` results in a 
four-digit number). If a range is specified, a random number of repetitions within the range is used (e.g., `A{6-10}` yields a 
sequence of alphanumeric characters of length between six and ten). A character class can be marked as optional by adding `?`
to the pattern (e.g., `l{10}n?` generates either ten lower case letters, or ten lower case letters and a numeral). The default 
pattern is `c{10-12}`.

### Ordered patterns

By default, password characters are shuffled, so the pattern `u{2}n{5}` will generate a password containing two upper case 
letters and five numerals in any order. To preserve the order of character classes in the pattern, add `o` to the start of the 
pattern: `ou{2}n{5}` results in two upper case letters followed by five numerals.

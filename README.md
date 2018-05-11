# pwg

[![Build Status](https://travis-ci.com/rddunphy/pwg.svg?branch=master)](https://travis-ci.com/rddunphy/pwg)

pwg is a customisable command line tool for generating various types of randomised passwords, including pronounceable passwords.

## Installation

Download the repository, add `pwg` to your path, and install dependencies using:

```console
user:~/pwg $ pip install -r requirements.txt
```

## Usage

To create a password using the default pattern (12-14 characters), run:

```console
user:~ $ pwg
-R@@u8U#;o
```

This prints the generated password to std out. To copy the password to the clipboard instead, use the `-c`/`--copy` option:

```console
user:~ $ pwg -c
Password copied to clipboard.
```

To choose a password type from the set of predefined types, use the `-t`/`--type` option:

```console
user:~ $ pwg -t pin
0148
```

To generate a passphrase, use the `phrase` command:

```console
user:~ $ pwg phrase
PastesRepaidSoftspokenComputers
```

The number of words and grammar of the phrase can be specified with the `-p`/`--pattern` option:

```console
user:~ $ pwg phrase -p anvaan
SoleDepositsAggravateImpiousNightmarishBundle
```

**Warning:** Short passphrases may be vulnerable to dictionary attacks. Passwords generated from dictionary words should 
be longer than passwords based on random characters to achieve equal security.

To generate a pronounceable password, use the `pronounceable` command:

```console
user:~ $ pwg pronounceable
explawneventry
```

The default length of a pronounceable password is 14 characters, and the length can be specified using the `-l`/`--length` 
option:

```console
user:~ $ pwg pronounceable -l 12
offingundese
```

**Warning:** While pronounceable passwords generated by pwg are unlikely to be susceptible to dictionary attacks, they may be 
significantly less secure than entirely random passwords. Use passwords of an appropriate length, and consider adding numerals, 
special characters, or upper case letters to pronounceable passwords.

To specify another pattern, use the `-p`/`--pattern` option:

```console
user:~ $ pwg -p ou{2}n{5}
PI73081
```

To munge a password (i.e., replace some characters with special characters, numerals, or upper case letters), use the `munge` command:

```console
user:~ $ pwg munge mypassword
mYPaS$w0rD
```

Passwords generated using pwg can be munged using the `-m`/`--munge` option:

```console
user:~ $ pwg pronounceable -m
is$3Dge6EdSOUR
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
pattern is `c{12-14}`.

### Ordered patterns

By default, password characters are shuffled, so the pattern `u{2}n{5}` will generate a password containing two upper case 
letters and five numerals in any order. To preserve the order of character classes in the pattern, add `o` to the start of the 
pattern: `ou{2}n{5}` results in two upper case letters followed by five numerals.

## Types

A number of predefined types are stored in a config file. These types are:

 - default (`c{12-14}` - e.g., `3KFZ&o.Gj-XOj`)
 - basic (`A{10-12}` - e.g., `6H69eImQPX`)
 - long (`c{18-20}` - e.g., `2=uHb_^i,6I*=E&30hH`)
 - secure (`lunsxC{15}` - e.g., `1a#Y[9&£#fAZ<N<U3e6$`)
 - pin (`n{4}` - e.g., `4406`)
 - colour (`h{6}` - e.g., `03be72`)

### Custom types

Patterns can be saved as custom types using the `save` command.

```console
user:~ $ pwg save mypattern x{10}
Pattern 'x{10}' saved as type 'mypattern'.
user:~ $ pwg -t mypattern
[}£}/(""}\
```

Saved patterns can be deleted by omitting the pattern argument:

```console
user:~ $ pwg save mypattern
Delete type with name mypattern? (Y/n) y
Type mypattern deleted.
```

## Pronounceable passwords and passphrases

Pronounceable passwords are lower-case passwords generated using common character n-grams from the English language. 
The n-grams are taken from [tables created by Peter Norvig](http://norvig.com/mayzner.html), and can be found in `data/ngrams`.

Passphrases are title-case sequences of words generated randomly from a dictionary based on the 
[Brown corpus](https://www.nltk.org/book/ch02.html#brown-corpus), stored in `data/words`. Patterns can be specified using the
`-p`/`--pattern` option, where the pattern is an ordered sequence of word types, chosen from `n` (noun), `v` (verb), `a` 
(adjective), or `w` (any word). The default pattern of `nvan` results in around 6\*10^16 possible phrases (~55 bits of entropy).

## Customised character classes

Characters can be added to or removed from character classes to improve localisation. To add characters to a class, use the 
`add_chars` command:

```console
user:~ $ pwg add_chars l äöüß
l: abcdefgehijklmnopqrstuvwxyzäöüß
```

To remove characters from a character set, use the `remove_chars` keyword:

```console
user:~ $ pwg remove_chars x £
x: "()[]{}~'/\<>`|
```

The basic character classes that can be modified are `lunNsxhHb`. The remaining classes 
are built from the basic classes, so that for instance adding a letter to `l` (lower case) also makes it available to `A` 
(alphanumeric) and `C` (any character).

## Reset

To revert any changes to types and character classes and restore the original default values, use the `reset` command:

```console
user:~ $ pwg reset
Reset all custom types and character classes? (Y/n) y
Configuration reset.
```

## License

pwg is released under the open-source MIT license.

**Disclaimer:** I am not a security expert, and I am working on this project in my free time. I cannot guarantee that passwords
generated using this program are suitable for any particular purpose. It is the responsibility of the user to ensure that generated
passwords are of the appropriate length and complexity.

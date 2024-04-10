# docs
## basics
+ whitespace seperated
+ all commands start with `:`
+ command ends with `-` if there are no paramaters
+ paramaters go like this: `:<-prm1-prm2`(no `-` needed after)
+ comments start with `*`(whitespace seperated, so each word needs to start with `*`)
### execution
+ has dict of variables
+ has "current variable"
+ any non-commands get upsertted(more info on that later) to the current variable
+ default variable is `_`, set to an empty string
+ system variables(start  with `_`):
+ counter increases as it moves to the next command
## how to run
+ `./emoticon2.sh (filename)`

| variable | purpose/value |
| --- | --- |
| `_` | defualt variable |
| `_counter` | program counter |
| `_true` | true boolean |
| `_false` | false boolean |
| `_math` | enables unary math operations |
| `_list` | empty list - used to copy into variables to create lists |
| `_math_pi` | pi |
| `_math_e` | e - Euler's number |
+ other than `_`, it is highly recommended that you ***do not*** change these. you might change `_counter`, for like a goto, but definitely not the others.
### docs info
#### parameters
+ `: name` means parameter is variable name
+ `: string` means paramter is a string
+ `: number` means paramter is a number
+ `: value` means you can use `${variablename}` to reference a variable
+ `*` means paramter is optional
+ `upsert` in the context of this documentation is either setting the specified variable to that value, or if the specified variable is a list, appending it to the list.

## commands
### `<-(*opt: value: string)`
print. prints value of current variable, except when `opt` is specified. If `opt` is `s` then print a space and if `opt` is `n` print a newline. if `opt` is `c` then it clears the console.
### `>-(feedvar: name)-(mode: value: string)`
input. input prompt is value of current variable and value is upsertted to `feedvar`. `mode` can be `n` or `s`, `n` is for numbers and `s` is for string.
### `#-(newvar: name)`
sets current variable to `name`. if `name` doesn't already exist, then it creates it with the value of an empty string.
+ variables cannot be just a number
+ variables cannot start with `_`, `$`
### `M-(var1: name)-(oper: value: string)-(var2: name)`
(binary) math operation. performs `oper` on `var1` and `var2` and upserts that value to the current variable. valid values for `oper`:
| value for `oper` | operation |
| --- | --- |
| + | addition |
| ~ | subtraction |
| * | multiplication |
| / | division |
| ^ | exponentiation |
### `m-(func: value: string)-(var: name)`
(unary) math operation. performs `func` on `var`. upserts value to current variable. valid values for `func`:
| value for `func` | operation |
| --- | --- |
| sin | sine |
| cos | cosine |
| tan | tangent |
| round | round number |
| floor | round down |
| ceil | round up |
| ln | natural logarithm |
### loops
#### `(-(loopid: string)-(condvarname: name)` and `)-(loopid: string)`
loop. `loopid` needs to be the same between both `(` and `)`, `condvarname` is name of the variable that holds the loop condition. `(` opens the loop and `)` closes it. `loopid` should be different across all loops.
#### `(^)-(loopid: string)`
continue in loop. returns to the start of the loop. `loopid` should be the same as the loop it's in.
\~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### `?-(var1: name)-(oper: value: string)-(var2: name)`
boolean/comparison. check if `var1` is whatever `oper` is to/than `var2`, then upserts it to the current variable.

Example: `:?-var1-==-var2` - checks if var1 is equal to var2.
### ifs
#### `?<-(var1: name)-(oper: value: string)-(var2: name)-(ifid: string)`
if condition. similar syntax to `?`, `ifid` is the id of the condition. it should be the same across all the else ifs, and the else. `ifid` should be different across all the if-then-elses.
#### `<?>-(var1: name)-(oper: value: string)-(var2: name)-(ifid: string)`
else if. same syntax as `?<`. `ifid` should be the same as the corresponding if.
#### `>?-(ifid: string)`
else condition. `ifid` should be the same as the corresponding if and else ifs.
#### `?|-(ifid: string)`
end if/then/else. again, `ifid` is the same as the one in the the entire if/then/else block.
\~~~~~~~~~~~~~~~~~~~~~~
### `v~v-(mode: value: string)`
type casting. turns the current variable into a number is `mode` is `n`, and string if `mode` is `s`.
### `>=>-(newvar: name)`
copy the value of the current variable to `newvar`. the current variable remains unchanged.
### `` `/-``
delete the current variable and switch to `_`
### `XX-`
end program
### `??-`
upserts random number between 0 and 1 to current variable.
### lists
#### `||-(index: value: number)`
set the current variables to the value in the current variable at index `index`. So if the current variable is "hello world" and you use `:||-2`, the current variable would become "l". this works with lists as well.
#### `[]<-(valvar: name)-(*index: value: number)`
append the value of `valvar` to the current list at `index`. if `index` is omitted, it will add it to the end. this will crash if the current variable is not a list.
#### `[]v^-(valvar: name)-(index: value: number)`
replace the element at `index` with the value of `valvar`. this will crash if the current variable is not a list.
\~~~~~~~~~~~~~~~~~~~~~
### `{@}-`
outputs
+ current variable
+ current variable value
+ all variables
+ loop information
+ if/then/else condition information
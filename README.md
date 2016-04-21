# Human Resource Machine Python Interpreter
<img src="http://cdn.akamai.steamstatic.com/steam/apps/375820/ss_7b564936dfb8f9b7b76f2141a79fa3cea8fd6fc7.1920x1080.jpg?t=1450110253" 
     alt="Quelle http://store.steampowered.com/app/375820/?l=german" 
     style="width: 600px;"/>

## Available operators

Operator                | Effect
---                    |---
INBOX                  |Pop next value from INBOX to POINTER 
OUTBOX                 |Put value from POINTER to OUTBOX 
COPYFROM `<REF>`       |Copy value to POINTER        
COPYTO   `<REF>`       |Copy value to referenced register
ADD      `<REF>`       |Adds value from REF to POINTER
SUB      `<REF>`       |Subtracts value from REF to POINTER
BUMPUP   `<REF>`       |Increment value of REF and copy it into POINTER
BUMPDN   `<REF>`       |Decrement value of REF and copy it into POINTER
JUMP     `<LABEL>`     |Jump to LABEL
JUMPZ    `<LABEL>`     |Jump to LABEL if POINTER is zero
JUMPN    `<LABEL>`     |Jump to LABEL if POINTER is negative
COMMENT  0             |Will be ignored


## REF
REF declares which register to use for operator, there are two types available:
- Direct access: `1`
- Indirect access: `[1]`
-- Accesses the register, defined by the value of declared register 

Example:
```
INBOX //1
COPYTO 1
BUMPUP [1]
COPYFROM 1
OUTBOX //2
```

## JUMP/LABEL
With a JUMP operator the PC (program counter - defines which position in code should be interpreted)
will set to the given LABEL

Example:
```
INBOX //1
COPYTO 1
JUMP a
BUMPUP 1 //Skipped
a:
OUTBOX //1
```

## POINTER
The machine is able to keep one value on the "BUS" (keep it active).
This value is used in operations like outbox or inbox.

## Roadmap

### Backend
<input type="checkbox" disabled="" checked> Return new state from tick <br>
<input type="checkbox" disabled=""> Create level module holding state, messages and check <br>
<input type="checkbox" disabled=""> Support character as values <br>


### GUI
<input type="checkbox" disabled="" checked> Undo Button to go back to previos state <br>
<input type="checkbox" disabled="" checked> Reset button setup first state <br>
<input type="checkbox" disabled="" checked> En- and disable buttons <br>
<input type="checkbox" disabled="" checked> Editable code window <br>
<input type="checkbox" disabled=""> Highlight code and mark errors<br>
<input type="checkbox" disabled=""> Show errors when they occure <br>
<input type="checkbox" disabled=""> Automatic timer for tick (Slider 1s-5s) ("Play" and "Break" button)<br>
<input type="checkbox" disabled=""> Use icons <br>
<input type="checkbox" disabled=""> Editable inbox window <br>
<input type="checkbox" disabled=""> Editable regs window <br>
<input type="checkbox" disabled=""> Load menu for Level <br>
<input type="checkbox" disabled=""> Show when program stops <br>
<input type="checkbox" disabled=""> Copy Solution to clipboard <br>